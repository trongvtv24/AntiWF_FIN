"""
worker.py — Main Queue Consumer Worker
Tự động consume queue và đăng bài lên Facebook theo lịch
"""

import sys
import json
import time
import signal
import logging
import argparse
from pathlib import Path
from datetime import datetime, time as dtime

# Add parent scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
import fb_api
import queue_manager as qm
import image_generator as ig
import notifier


# ─── Config ───────────────────────────────────────────────────────────────────

DATA_DIR = Path("C:/Users/Administrator/.gemini/antigravity/data/fb-publisher")
CONFIG_FILE = DATA_DIR / "config" / "fanpages.json"
SETTINGS_FILE = DATA_DIR / "config" / "settings.json"

_running = True


def _load_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_fanpages() -> list:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Key là "pages" (cấu trúc mới)
    return [fp for fp in cfg.get("pages", []) if fp.get("active", False)]


def _get_app_creds():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("app_id"), cfg.get("app_secret")


# ─── Signal Handling (Graceful Shutdown) ──────────────────────────────────────

def _handle_signal(sig, frame):
    global _running
    notifier.log_info("⛔ Nhận tín hiệu dừng. Worker sẽ tắt sau khi hoàn thành bài hiện tại...")
    _running = False


signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


# ─── Posting Time Check ───────────────────────────────────────────────────────

def _is_posting_time(fanpage: dict) -> bool:
    """
    Kiểm tra xem có đúng giờ đăng của fanpage này không.
    Mỗi giờ đăng có window ±5 phút.
    """
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")

    for post_time in fanpage.get("post_times", []):
        try:
            hour, minute = map(int, post_time.split(":"))
            target = dtime(hour, minute)
            current = dtime(now.hour, now.minute)

            # Window ±5 phút
            total_current = now.hour * 60 + now.minute
            total_target = hour * 60 + minute
            diff = abs(total_current - total_target)

            if diff <= 5:
                return True
        except Exception:
            continue

    return False


# ─── Token Warning ────────────────────────────────────────────────────────────

def _check_token_warnings():
    """Cảnh báo nếu có token sắp hết hạn."""
    fanpages = _load_fanpages()
    s = _load_settings()
    warning_days = s["token_warning"]["days_before_expiry"]

    for fp in fanpages:
        expires_str = fp.get("token_expires")
        if expires_str:
            try:
                expires = datetime.strptime(expires_str, "%Y-%m-%d")
                days_left = (expires - datetime.now()).days
                if days_left <= warning_days:
                    msg = f"⚠️  TOKEN SẮP HẾT HẠN: {fp['name']} — Còn {days_left} ngày!"
                    notifier.log_warning(msg)
                    print(msg)
            except Exception:
                pass


# ─── Process Single Post ──────────────────────────────────────────────────────

def _process_post(post: dict, fanpage: dict, dry_run: bool = False) -> bool:
    """
    Xử lý 1 bài trong queue: generate ảnh (nếu cần) → đăng lên Facebook.
    Returns: True nếu thành công
    """
    post_id = post["id"]
    fanpage_name = fanpage["name"]

    notifier.log_info(f"📝 Processing post [{post_id}] for [{fanpage_name}]")
    qm.update_status(post_id, "processing")

    # Step 1: Kiểm tra / generate ảnh
    image_path = post.get("image_path")
    if not ig.check_image_exists(image_path):
        notifier.log_info(f"   🖼️  Image not found, generating...")
        img_result = ig.generate_for_post(
            post_id=post_id,
            post_text=post.get("post_text", ""),
            custom_prompt=post.get("image_prompt"),
            niche=fanpage.get("niche")
        )
        if not img_result["success"]:
            notifier.log_error(f"   ❌ Image generation failed: {img_result['error']}")
            qm.update_status(post_id, "failed", error=f"Image gen failed: {img_result['error']}")
            return False
        image_path = img_result["image_path"]
        notifier.log_info(f"   ✅ Image ready: {image_path}")

    # Step 2: Dry run check
    if dry_run:
        notifier.log_info(f"   🔍 [DRY-RUN] Would post to {fanpage_name}:")
        notifier.log_info(f"      Text: {post['post_text'][:100]}...")
        notifier.log_info(f"      Image: {image_path}")
        notifier.log_info(f"      Link: {post.get('aff_link', 'None')}")
        qm.update_status(post_id, "pending")  # Reset về pending sau dry-run
        return True

    # Step 3: Post to Facebook
    result = fb_api.post_photo(
        page_id=fanpage["page_id"],
        access_token=fanpage["access_token"],
        image_path=image_path,
        caption=post["post_text"],
        link=post.get("aff_link")
    )

    if result["success"]:
        qm.update_status(post_id, "posted", fb_post_id=result["post_id"])
        notifier.log_success(post_id, fanpage_name, result["post_id"])
        return True
    else:
        qm.update_status(post_id, "failed", error=result["error"])
        notifier.log_error(f"   ❌ Failed to post [{post_id}] to {fanpage_name}: {result['error']}")
        return False


# ─── Worker Modes ─────────────────────────────────────────────────────────────

def _auto_fill_queue_if_needed(fanpages: list, settings: dict):
    """
    Tự động gọi content_bridge để fill queue nếu pending < min_pending.
    """
    if not settings["queue"].get("auto_fill_enabled", False):
        return

    min_pending = settings["queue"].get("auto_fill_min_pending", 3)

    try:
        import content_bridge as cb
        summary = qm.get_queue_summary()

        for fp in fanpages:
            fp_name = fp["name"]
            pending = summary["by_fanpage"].get(fp_name, {}).get("pending", 0)

            if pending < min_pending:
                notifier.log_info(
                    f"⚡ Auto-fill: [{fp_name}] chỉ còn {pending} bài, đang tạo thêm..."
                )
                target = settings["queue"].get("auto_fill_target", 10)
                added = cb.fill_queue_for_page(fp, target_pending=target)
                notifier.log_info(f"   ✅ Đã thêm {added} bài mới cho [{fp_name}]")
    except Exception as e:
        notifier.log_error(f"❌ Auto-fill lỗi: {e}")


def run_auto_mode(dry_run: bool = False):
    """
    Auto mode: Chạy liên tục, kiểm tra queue mỗi N giây.
    Chỉ đăng đúng giờ đã chỉ định trong scheduled_at của từng bài.
    Tự động fill queue qua content_bridge khi cạn.
    """
    s = _load_settings()
    interval = s["worker"]["check_interval_seconds"]
    min_gap = s["worker"]["min_gap_between_posts_minutes"] * 60
    last_post_time = {}   # {fanpage_id: timestamp}
    last_fill_check = 0   # Timestamp lần cuối check auto-fill
    FILL_CHECK_INTERVAL = 300  # Check auto-fill mỗi 5 phút

    notifier.log_info("🤖 Worker started in AUTO mode (schedule-based)")
    _check_token_warnings()

    while _running:
        fanpages = _load_fanpages()
        now_ts = time.time()

        # Auto-fill queue nếu cạn (mỗi 5 phút)
        if now_ts - last_fill_check >= FILL_CHECK_INTERVAL:
            _auto_fill_queue_if_needed(fanpages, s)
            last_fill_check = now_ts

        for fp in fanpages:
            fp_id = fp["id"]

            # Kiểm tra cooldown giữa các lần đăng
            last_time = last_post_time.get(fp_id, 0)
            if now_ts - last_time < min_gap:
                continue

            # Lấy bài kế tiếp đã đến scheduled_at
            post = qm.get_next_pending(fanpage_id=fp_id)
            if not post:
                continue

            success = _process_post(post, fp, dry_run=dry_run)
            if success and not dry_run:
                last_post_time[fp_id] = time.time()
                s2 = _load_settings()
                gap = s2["worker"]["post_now_mode_gap_seconds"]
                time.sleep(gap)

        if _running:
            time.sleep(interval)

    notifier.log_info("⛔ Worker stopped gracefully")


def run_post_now_mode(dry_run: bool = False):
    """
    Post-now mode: Đăng ngay tất cả bài pending, không chờ giờ lịch.
    """
    s = _load_settings()
    gap = s["worker"]["post_now_mode_gap_seconds"]

    notifier.log_info("⚡ Worker started in POST-NOW mode")
    _check_token_warnings()

    fanpages = {fp["id"]: fp for fp in _load_fanpages()}
    posted_count = 0
    failed_count = 0

    while True:
        found_any = False

        for fp_id, fp in fanpages.items():
            post = qm.get_next_pending(fanpage_id=fp_id)
            if not post:
                continue

            found_any = True
            success = _process_post(post, fp, dry_run=dry_run)

            if success:
                posted_count += 1
            else:
                failed_count += 1

            if not dry_run:
                time.sleep(gap)

        if not found_any:
            break

    notifier.log_info(f"✅ Post-now completed: {posted_count} posted, {failed_count} failed")
    print(f"\n📊 Kết quả: ✅ {posted_count} bài đã đăng | ❌ {failed_count} lỗi")


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Facebook Publisher Worker",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "now", "dry-run"],
        default="auto",
        help=(
            "auto     = Chạy theo lịch đã cài trong fanpage config (mặc định)\n"
            "now      = Đăng ngay tất cả bài pending\n"
            "dry-run  = Chạy thử, không đăng thật"
        )
    )
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════╗
║   📢 FACEBOOK AUTO-PUBLISHER WORKER      ║
║   Mode: {args.mode.upper():<33}║
║   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<30}║
╚══════════════════════════════════════════╝
Nhấn Ctrl+C để dừng worker.
""")

    if args.mode == "auto":
        run_auto_mode(dry_run=False)
    elif args.mode == "now":
        run_post_now_mode(dry_run=False)
    elif args.mode == "dry-run":
        run_post_now_mode(dry_run=True)
