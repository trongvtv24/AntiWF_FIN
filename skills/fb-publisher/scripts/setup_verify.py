"""
setup_verify.py — Kiểm tra toàn bộ hệ thống FB Publisher
Chạy lần đầu để verify setup trước khi bật worker.

Usage:
    python setup_verify.py
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

DATA_DIR = Path("C:/Users/Administrator/.gemini/antigravity/data/fb-publisher")
CONFIG_FILE = DATA_DIR / "config" / "fanpages.json"
SETTINGS_FILE = DATA_DIR / "config" / "settings.json"


def print_separator(title=""):
    print(f"\n{'═'*55}")
    if title:
        print(f"  {title}")
        print(f"  {'─'*50}")


def check_config_files():
    """Kiểm tra file config tồn tại và hợp lệ."""
    print_separator("📁 KIỂM TRA CONFIG FILES")
    ok = True

    for path, label in [(CONFIG_FILE, "fanpages.json"), (SETTINGS_FILE, "settings.json")]:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"  ✅ {label} — OK ({path.stat().st_size} bytes)")
            except json.JSONDecodeError as e:
                print(f"  ❌ {label} — JSON lỗi: {e}")
                ok = False
        else:
            print(f"  ❌ {label} — KHÔNG TỒN TẠI: {path}")
            ok = False

    return ok


def check_data_dirs():
    """Kiểm tra và tạo thư mục data cần thiết."""
    print_separator("📂 KIỂM TRA THƯ MỤC DATA")
    dirs = [
        DATA_DIR / "queue",
        DATA_DIR / "images",
        DATA_DIR / "logs",
        DATA_DIR / "config",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {d.relative_to(DATA_DIR.parent.parent.parent)}")

    return True


def check_tokens():
    """Verify từng Page Access Token qua Graph API."""
    print_separator("🔑 KIỂM TRA ACCESS TOKENS")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    app_id = cfg.get("app_id", "")
    app_secret = cfg.get("app_secret", "")
    api_version = cfg.get("api_version", "v19.0")
    base_url = f"https://graph.facebook.com/{api_version}"

    if not app_id or not app_secret:
        print("  ⚠️  App ID / App Secret chưa cài trong config!")
    else:
        print(f"  ℹ️  App ID: {app_id[:15]}...")

    all_ok = True
    pages = cfg.get("pages", [])

    for page in pages:
        if not page.get("active", False):
            print(f"  ⏭️  [{page['name']}] — BỎ QUA (inactive)")
            continue

        page_id = page["id"]
        token = page["access_token"]

        # Verify token
        try:
            r = requests.get(
                f"{base_url}/{page_id}",
                params={"fields": "name,id,fan_count", "access_token": token},
                timeout=15
            )
            data = r.json()

            if "error" in data:
                print(f"  ❌ [{page['name']}] — LỖI: {data['error']['message']}")
                all_ok = False
                continue

            fan_count = data.get("fan_count", "N/A")
            print(f"  ✅ [{page['name']}] — OK | Followers: {fan_count:,}" if isinstance(fan_count, int) else f"  ✅ [{page['name']}] — OK | Followers: {fan_count}")

            # Check token expiry (nếu có app_id và app_secret)
            if app_id and app_secret:
                debug_r = requests.get(
                    f"{base_url}/debug_token",
                    params={
                        "input_token": token,
                        "access_token": f"{app_id}|{app_secret}"
                    },
                    timeout=15
                )
                debug_data = debug_r.json().get("data", {})
                expires_ts = debug_data.get("expires_at")
                is_valid = debug_data.get("is_valid", False)

                if not is_valid:
                    print(f"     ⚠️  Token KHÔNG HỢP LỆ — Cần refresh!")
                    all_ok = False
                elif expires_ts and expires_ts > 0:
                    expires_dt = datetime.fromtimestamp(expires_ts)
                    days_left = (expires_dt - datetime.now()).days
                    if days_left <= 7:
                        print(f"     ⚠️  Token hết hạn trong {days_left} ngày ({expires_dt.date()})")
                    else:
                        print(f"     ℹ️  Token hết hạn: {expires_dt.date()} ({days_left} ngày)")
                else:
                    print(f"     ✅  Token không giới hạn thời gian (long-lived)")

        except requests.exceptions.ConnectionError:
            print(f"  ❌ [{page['name']}] — Không kết nối được Internet")
            all_ok = False
        except Exception as e:
            print(f"  ❌ [{page['name']}] — Lỗi: {e}")
            all_ok = False

    return all_ok


def check_queue():
    """Kiểm tra trạng thái queue hiện tại."""
    print_separator("📋 TRẠNG THÁI QUEUE")
    try:
        import queue_manager as qm
        summary = qm.get_queue_summary()
        print(f"  📊 Tổng bài: {summary['total']}")
        for status, count in summary["by_status"].items():
            emoji = {"pending": "⏳", "posted": "✅", "failed": "❌", "processing": "🔄"}.get(status, "•")
            print(f"     {emoji} {status}: {count}")

        if summary["by_fanpage"]:
            print("\n  📌 Theo fanpage:")
            for name, counts in summary["by_fanpage"].items():
                print(f"     • {name}: pending={counts.get('pending',0)}, posted={counts.get('posted',0)}, failed={counts.get('failed',0)}")
        return True
    except Exception as e:
        print(f"  ⚠️  Chưa có queue (sẽ tự tạo khi fill): {e}")
        return True


def check_python_deps():
    """Kiểm tra dependencies."""
    print_separator("🐍 KIỂM TRA PYTHON DEPENDENCIES")
    deps = ["requests", "json", "pathlib", "uuid"]
    all_ok = True
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} — Chạy: pip install {dep}")
            all_ok = False
    return all_ok


def show_schedule():
    """Hiển thị lịch đăng bài cho từng page."""
    print_separator("📅 LỊCH ĐĂNG BÀI")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    for page in cfg.get("pages", []):
        if not page.get("active"):
            continue
        times = ", ".join(page.get("post_times", []))
        print(f"  📢 {page['name']}")
        print(f"     Giờ đăng: {times}")
        print(f"     Niche: {page.get('niche', 'N/A')}")
        print(f"     Tone: {page.get('tone', 'N/A')}")
        print()


def preview_content():
    """Preview 1 mẫu content tự động."""
    print_separator("📝 PREVIEW CONTENT TỰ ĐỘNG")
    try:
        import content_bridge as cb
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        pages = [p for p in cfg.get("pages", []) if p.get("active")]
        if pages:
            sample_page = pages[0]
            content = cb.generate_post_content(sample_page)
            print(f"  Page: {sample_page['name']}")
            print(f"  Topic: {content['topic']}")
            print(f"  Formula: {content['formula']}")
            print(f"\n  --- POST TEXT PREVIEW ---")
            print(f"  {content['post_text'][:300]}...")
            print(f"\n  --- IMAGE PROMPT ---")
            print(f"  {content['image_prompt'][:150]}...")
    except Exception as e:
        print(f"  ⚠️  {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║   🔍 FB PUBLISHER — SETUP VERIFICATION               ║
║   Kiểm tra toàn bộ hệ thống trước khi chạy worker   ║
╚══════════════════════════════════════════════════════╝""")

    results = {
        "Python Deps": check_python_deps(),
        "Config Files": check_config_files(),
        "Data Dirs":    check_data_dirs(),
        "Tokens":       check_tokens(),
        "Queue":        check_queue(),
    }

    show_schedule()
    preview_content()

    print_separator("📊 KẾT QUẢ TỔNG HỢP")
    all_pass = True
    for name, ok in results.items():
        emoji = "✅" if ok else "❌"
        print(f"  {emoji} {name}")
        if not ok:
            all_pass = False

    print()
    if all_pass:
        print("  🎉 Tất cả kiểm tra PASSED! Hệ thống sẵn sàng.")
        print()
        print("  🚀 BƯỚC TIẾP THEO:")
        print("     1. Fill queue lần đầu:")
        print("        python content_bridge.py --run")
        print()
        print("     2. Xem preview queue:")
        print("        python queue_manager.py --summary")
        print()
        print("     3. Chạy worker:")
        print("        python worker.py --mode auto")
        print()
        print("     Hoặc double-click: run_worker.bat")
    else:
        print("  ❌ Có lỗi cần sửa trước khi chạy worker!")

    print("═"*55)
