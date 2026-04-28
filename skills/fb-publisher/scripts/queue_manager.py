"""
queue_manager.py — Quản lý hàng đợi bài viết Facebook
CRUD operations cho posts_queue.json
"""

import json
import uuid
import argparse
from datetime import datetime
from pathlib import Path


# ─── Path Setup ───────────────────────────────────────────────────────────────

DATA_DIR = Path("C:/Users/Administrator/.gemini/antigravity/data/fb-publisher")
SETTINGS_FILE = DATA_DIR / "config" / "settings.json"


def _load_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_queue_path() -> Path:
    s = _load_settings()
    path = Path(s["queue"]["file_path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# ─── Queue I/O ────────────────────────────────────────────────────────────────

def _read_queue() -> dict:
    path = _get_queue_path()
    if not path.exists():
        return {"posts": [], "stats": {"total_added": 0, "total_posted": 0, "total_failed": 0}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_queue(data: dict):
    path = _get_queue_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── CRUD Operations ──────────────────────────────────────────────────────────

def add_post(fanpage_id: str, fanpage_name: str, post_text: str,
             image_path: str, image_prompt: str = "",
             aff_link: str = None, scheduled_at: str = None,
             priority: int = 1) -> str:
    """
    Thêm bài mới vào queue.
    Returns: post_id (uuid)
    """
    data = _read_queue()
    post_id = str(uuid.uuid4())[:8]

    post = {
        "id": post_id,
        "fanpage_id": fanpage_id,
        "fanpage_name": fanpage_name,
        "post_text": post_text,
        "image_prompt": image_prompt,
        "image_path": image_path,
        "aff_link": aff_link,
        "status": "pending",
        "priority": priority,
        "scheduled_at": scheduled_at,
        "created_at": datetime.now().isoformat(),
        "posted_at": None,
        "fb_post_id": None,
        "error": None,
        "retry_count": 0
    }

    data["posts"].append(post)
    data["stats"]["total_added"] = data["stats"].get("total_added", 0) + 1
    _write_queue(data)
    return post_id


def get_next_pending(fanpage_id: str = None) -> dict | None:
    """
    Lấy bài tiếp theo cần đăng.
    - Nếu có scheduled_at: chỉ lấy bài đã đến giờ
    - Nếu không có scheduled_at: lấy ngay
    - Ưu tiên theo priority (thấp = cao hơn)
    """
    data = _read_queue()
    now = datetime.now()
    candidates = []

    for post in data["posts"]:
        if post["status"] != "pending":
            continue
        if fanpage_id and post["fanpage_id"] != fanpage_id:
            continue

        if post.get("scheduled_at"):
            scheduled = datetime.fromisoformat(post["scheduled_at"])
            if scheduled > now:
                continue  # Chưa đến giờ

        candidates.append(post)

    if not candidates:
        return None

    # Sort: priority thấp (1) lên trước, rồi theo thời gian tạo
    candidates.sort(key=lambda x: (x.get("priority", 1), x["created_at"]))
    return candidates[0]


def update_status(post_id: str, status: str,
                  fb_post_id: str = None, error: str = None):
    """
    Cập nhật trạng thái bài viết.
    status: pending | processing | posted | failed
    """
    data = _read_queue()

    for post in data["posts"]:
        if post["id"] == post_id:
            post["status"] = status
            if fb_post_id:
                post["fb_post_id"] = fb_post_id
                post["posted_at"] = datetime.now().isoformat()
            if error:
                post["error"] = error
                post["retry_count"] = post.get("retry_count", 0) + 1
            break

    # Update stats
    if status == "posted":
        data["stats"]["total_posted"] = data["stats"].get("total_posted", 0) + 1
    elif status == "failed":
        data["stats"]["total_failed"] = data["stats"].get("total_failed", 0) + 1

    _write_queue(data)


def delete_post(post_id: str) -> bool:
    """Xoá bài khỏi queue. Returns True nếu tìm thấy và xoá."""
    data = _read_queue()
    original_len = len(data["posts"])
    data["posts"] = [p for p in data["posts"] if p["id"] != post_id]

    if len(data["posts"]) < original_len:
        _write_queue(data)
        return True
    return False


def retry_failed_posts(max_retries: int = 3):
    """Reset các bài failed (dưới ngưỡng retry) về pending để thử lại."""
    data = _read_queue()
    s = _load_settings()
    max_r = s["queue"]["max_failed_before_skip"]
    count = 0

    for post in data["posts"]:
        if post["status"] == "failed" and post.get("retry_count", 0) < max_r:
            post["status"] = "pending"
            post["error"] = None
            count += 1

    _write_queue(data)
    return count


def get_queue_summary() -> dict:
    """Tổng quan trạng thái queue."""
    data = _read_queue()
    summary = {
        "total": len(data["posts"]),
        "by_status": {"pending": 0, "processing": 0, "posted": 0, "failed": 0},
        "by_fanpage": {},
        "stats": data.get("stats", {})
    }

    for post in data["posts"]:
        status = post.get("status", "unknown")
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

        fp_name = post.get("fanpage_name", post.get("fanpage_id", "unknown"))
        if fp_name not in summary["by_fanpage"]:
            summary["by_fanpage"][fp_name] = {"pending": 0, "posted": 0, "failed": 0}
        if status in summary["by_fanpage"][fp_name]:
            summary["by_fanpage"][fp_name][status] += 1

    return summary


def list_posts(status_filter: str = None, fanpage_id: str = None,
               limit: int = 20) -> list:
    """Liệt kê bài viết trong queue với filter tuỳ chọn."""
    data = _read_queue()
    posts = data["posts"]

    if status_filter:
        posts = [p for p in posts if p.get("status") == status_filter]
    if fanpage_id:
        posts = [p for p in posts if p.get("fanpage_id") == fanpage_id]

    return posts[-limit:]


# ─── CLI Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Queue Manager CLI")
    parser.add_argument("--list", action="store_true", help="Liệt kê tất cả bài trong queue")
    parser.add_argument("--summary", action="store_true", help="Tóm tắt trạng thái queue")
    parser.add_argument("--retry", action="store_true", help="Retry các bài failed")
    parser.add_argument("--delete", type=str, help="Xoá bài theo ID")
    parser.add_argument("--status", type=str, help="Filter theo status")
    args = parser.parse_args()

    if args.summary:
        summary = get_queue_summary()
        print("\n📋 QUEUE SUMMARY")
        print(f"   Total: {summary['total']}")
        for status, count in summary["by_status"].items():
            emoji = {"pending": "⏳", "posted": "✅", "failed": "❌", "processing": "🔄"}.get(status, "•")
            print(f"   {emoji} {status.capitalize()}: {count}")
        print("\n📌 BY FANPAGE:")
        for name, counts in summary["by_fanpage"].items():
            print(f"   {name}: {counts}")

    elif args.list:
        posts = list_posts(status_filter=args.status)
        if not posts:
            print("Queue trống!")
        for p in posts:
            status_emoji = {"pending": "⏳", "posted": "✅", "failed": "❌"}.get(p["status"], "•")
            preview = p["post_text"][:60].replace("\n", " ") + "..."
            print(f"[{p['id']}] {status_emoji} [{p['fanpage_name']}] {preview}")

    elif args.retry:
        count = retry_failed_posts()
        print(f"✅ Reset {count} bài failed về pending để retry")

    elif args.delete:
        if delete_post(args.delete):
            print(f"✅ Đã xoá bài {args.delete}")
        else:
            print(f"❌ Không tìm thấy bài {args.delete}")

    else:
        parser.print_help()
