"""
notifier.py — Logging & Báo cáo cho Facebook Publisher
"""

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler


# ─── Setup ────────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
SETTINGS_FILE = SKILL_DIR / "config" / "settings.json"

_logger = None


def _get_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_logger():
    global _logger
    if _logger:
        return _logger

    s = _get_settings()
    log_cfg = s["logging"]
    log_path = Path(log_cfg["file"])
    log_path.parent.mkdir(parents=True, exist_ok=True)

    _logger = logging.getLogger("fb_publisher")
    _logger.setLevel(getattr(logging, log_cfg["level"], logging.INFO))

    # File handler với rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=log_cfg["max_bytes"],
        backupCount=log_cfg["backup_count"],
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)
    return _logger


# ─── Log Functions ────────────────────────────────────────────────────────────

def log_info(msg: str):
    _get_logger().info(msg)


def log_warning(msg: str):
    _get_logger().warning(msg)


def log_error(msg: str):
    _get_logger().error(msg)


def log_success(post_id: str, fanpage_name: str, fb_post_id: str):
    msg = f"✅ POSTED [{post_id}] → {fanpage_name} | FB Post ID: {fb_post_id}"
    _get_logger().info(msg)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ─── Report Generator ─────────────────────────────────────────────────────────

def generate_report(days: int = 1) -> str:
    """
    Tạo báo cáo từ queue data cho N ngày gần nhất.
    """
    s = _get_settings()
    queue_path = Path(s["queue"]["file_path"])

    if not queue_path.exists():
        return "📋 Queue trống — chưa có bài viết nào."

    with open(queue_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    cutoff = datetime.now() - timedelta(days=days)

    # Filter theo khoảng thời gian
    recent = [
        p for p in posts
        if p.get("posted_at") and
        datetime.fromisoformat(p["posted_at"]) >= cutoff
    ]

    posted = [p for p in posts if p["status"] == "posted"]
    failed = [p for p in posts if p["status"] == "failed"]
    pending = [p for p in posts if p["status"] == "pending"]

    # Group by fanpage
    by_fanpage = {}
    for p in posted:
        name = p.get("fanpage_name", "Unknown")
        by_fanpage[name] = by_fanpage.get(name, 0) + 1

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 BÁO CÁO FACEBOOK PUBLISHER
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Đã đăng thành công: {len(posted)} bài
❌ Thất bại:           {len(failed)} bài
⏳ Đang chờ trong queue: {len(pending)} bài

📌 PHÂN BỔ THEO FANPAGE:"""

    for name, count in by_fanpage.items():
        report += f"\n   • {name}: {count} bài"

    if failed:
        report += "\n\n⚠️  BÀI THẤT BẠI:"
        for p in failed[-5:]:  # Show 5 bài lỗi gần nhất
            error_msg = p.get("error", "Unknown error")
            report += f"\n   [{p['id']}] {p.get('fanpage_name', '?')} — {error_msg[:60]}"

    # Token warnings
    try:
        from pathlib import Path as P
        cfg_path = P(__file__).parent.parent / "config" / "fanpages.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        warnings = []
        for fp in cfg.get("fanpages", []):
            exp = fp.get("token_expires")
            if exp:
                days_left = (datetime.strptime(exp, "%Y-%m-%d") - datetime.now()).days
                if days_left <= 14:
                    warnings.append(f"   ⚠️  {fp['name']} — Token hết hạn sau {days_left} ngày!")
        if warnings:
            report += "\n\n🔑 CẢNH BÁO TOKEN:\n" + "\n".join(warnings)
    except Exception:
        pass

    report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    return report


def tail_log(lines: int = 50) -> str:
    """Đọc N dòng cuối của log file."""
    s = _get_settings()
    log_path = Path(s["logging"]["file"])
    if not log_path.exists():
        return "Log file chưa tồn tại."
    with open(log_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return "".join(all_lines[-lines:])


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reporter CLI")
    parser.add_argument("--report", action="store_true", help="Tạo báo cáo tổng quan")
    parser.add_argument("--days", type=int, default=1, help="Số ngày lùi về (mặc định: 1)")
    parser.add_argument("--log", action="store_true", help="Xem 50 dòng log cuối")
    parser.add_argument("--lines", type=int, default=50, help="Số dòng log cần xem")
    args = parser.parse_args()

    if args.report:
        print(generate_report(days=args.days))
    elif args.log:
        print(tail_log(lines=args.lines))
    else:
        parser.print_help()
