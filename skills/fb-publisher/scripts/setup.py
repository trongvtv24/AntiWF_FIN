"""
setup.py — Cài đặt ban đầu cho Facebook Publisher
Tạo thư mục, kiểm tra dependencies, verify access tokens
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config" / "fanpages.json"
SETTINGS_FILE = SKILL_DIR / "config" / "settings.json"

# Màu terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════╗
║   📢 FACEBOOK AUTO-PUBLISHER — SETUP         ║
╚══════════════════════════════════════════════╝{RESET}
""")


# ─── Check Functions ──────────────────────────────────────────────────────────

def check_python_version():
    version = sys.version_info
    ok = version.major == 3 and version.minor >= 8
    status = f"{GREEN}✅{RESET}" if ok else f"{RED}❌{RESET}"
    print(f"   {status} Python {version.major}.{version.minor}.{version.micro} ", end="")
    print("(OK)" if ok else f"(Cần Python 3.8+)")
    return ok


def check_dependencies():
    required = ["requests"]
    all_ok = True
    for pkg in required:
        try:
            __import__(pkg)
            print(f"   {GREEN}✅{RESET} {pkg} — đã cài")
        except ImportError:
            print(f"   {RED}❌{RESET} {pkg} — CHƯA cài")
            all_ok = False
    return all_ok


def check_directories():
    with open(SETTINGS_FILE) as f:
        s = json.load(f)

    dirs_to_create = [
        Path(s["image"]["save_dir"]),
        Path(s["queue"]["file_path"]).parent,
        Path(s["logging"]["file"]).parent
    ]

    all_ok = True
    for d in dirs_to_create:
        try:
            d.mkdir(parents=True, exist_ok=True)
            print(f"   {GREEN}✅{RESET} {d}")
        except Exception as e:
            print(f"   {RED}❌{RESET} {d} — {e}")
            all_ok = False
    return all_ok


def initialize_queue():
    with open(SETTINGS_FILE) as f:
        s = json.load(f)
    queue_path = Path(s["queue"]["file_path"])

    if not queue_path.exists():
        initial = {
            "posts": [],
            "stats": {"total_added": 0, "total_posted": 0, "total_failed": 0},
            "created_at": datetime.now().isoformat()
        }
        with open(queue_path, "w", encoding="utf-8") as f:
            json.dump(initial, f, indent=2, ensure_ascii=False)
        print(f"   {GREEN}✅{RESET} Queue file khởi tạo: {queue_path}")
    else:
        print(f"   {YELLOW}ℹ️{RESET}  Queue file đã tồn tại: {queue_path}")


def verify_tokens():
    """Kiểm tra tất cả access tokens trong config."""
    try:
        import requests as req
    except ImportError:
        print(f"   {RED}❌{RESET} Cần cài: pip install requests")
        return False

    with open(CONFIG_FILE) as f:
        cfg = json.load(f)

    api_version = cfg.get("api_version", "v19.0")
    all_ok = True

    print(f"\n{BOLD}   Kiểm tra tokens...{RESET}")
    for fp in cfg.get("fanpages", []):
        if not fp.get("active"):
            print(f"   ⏸️  [{fp['name']}] — Inactive, bỏ qua")
            continue

        page_id = fp["page_id"]
        token = fp["access_token"]

        # Skip placeholder tokens
        if "YOUR_" in token or "EAAxxxxx" in token:
            print(f"   {YELLOW}⚠️{RESET}  [{fp['name']}] — Token chưa được điền! Hãy cập nhật fanpages.json")
            all_ok = False
            continue

        try:
            url = f"https://graph.facebook.com/{api_version}/{page_id}"
            r = req.get(url, params={"fields": "name,id", "access_token": token}, timeout=15)
            data = r.json()

            if "error" in data:
                print(f"   {RED}❌{RESET} [{fp['name']}] — {data['error']['message'][:60]}")
                all_ok = False
            else:
                name = data.get("name", "Unknown")

                # Check expiry
                exp_str = fp.get("token_expires")
                exp_info = ""
                if exp_str:
                    try:
                        exp = datetime.strptime(exp_str, "%Y-%m-%d")
                        days = (exp - datetime.now()).days
                        if days <= 7:
                            exp_info = f" {RED}⚠️ Hết hạn sau {days} ngày!{RESET}"
                        else:
                            exp_info = f" (còn {days} ngày)"
                    except Exception:
                        pass

                print(f"   {GREEN}✅{RESET} [{fp['name']}] → Page: {name}{exp_info}")
        except Exception as e:
            print(f"   {RED}❌{RESET} [{fp['name']}] — Lỗi kết nối: {e}")
            all_ok = False

    return all_ok


def install_dependencies():
    """Tự động cài pip packages."""
    packages = ["requests"]
    print(f"\n   Đang cài đặt dependencies...")
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
            print(f"   {GREEN}✅{RESET} {pkg} installed")
        except subprocess.CalledProcessError:
            print(f"   {RED}❌{RESET} Không thể cài {pkg}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_check():
    print_header()
    print(f"{BOLD}🔍 Kiểm tra môi trường:{RESET}\n")

    ok_python = check_python_version()
    ok_deps = check_dependencies()

    print(f"\n{BOLD}📁 Tạo thư mục data:{RESET}\n")
    ok_dirs = check_directories()
    initialize_queue()

    print(f"\n{BOLD}🔑 Kiểm tra Facebook Tokens:{RESET}")
    ok_tokens = verify_tokens()

    print(f"\n{'━'*50}")
    if ok_python and ok_deps and ok_dirs and ok_tokens:
        print(f"{GREEN}{BOLD}✅ Setup hoàn tất! Hệ thống sẵn sàng.{RESET}")
        print(f"\nBước tiếp theo:")
        print(f"  • Tạo bài: sử dụng /fb-post create")
        print(f"  • Chạy worker: python worker.py --mode auto")
        print(f"  • Hoặc double-click: run_worker.bat")
    else:
        print(f"{RED}{BOLD}❌ Setup chưa hoàn tất. Vui lòng kiểm tra các lỗi trên.{RESET}")
        if not ok_deps:
            print(f"\n  → Chạy: python setup.py --install để tự cài dependencies")
        if not ok_tokens:
            print(f"  → Cập nhật tokens trong: config/fanpages.json")


def run_install():
    install_dependencies()
    run_check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FB Publisher Setup")
    parser.add_argument("--check", action="store_true", help="Kiểm tra môi trường (mặc định)")
    parser.add_argument("--verify", action="store_true", help="Chỉ verify tokens")
    parser.add_argument("--install", action="store_true", help="Cài dependencies rồi check")
    args = parser.parse_args()

    if args.verify:
        print_header()
        verify_tokens()
    elif args.install:
        run_install()
    else:
        run_check()
