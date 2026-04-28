"""
fb_api.py — Facebook Graph API Wrapper
Xử lý tất cả requests đến Facebook Graph API
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path


# ─── Config ───────────────────────────────────────────────────────────────────

DATA_DIR = Path("C:/Users/Administrator/.gemini/antigravity/data/fb-publisher")
CONFIG_FILE = DATA_DIR / "config" / "fanpages.json"
SETTINGS_FILE = DATA_DIR / "config" / "settings.json"


def _load_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_api_base():
    s = _load_settings()
    cfg = _load_config()
    version = cfg.get("api_version", "v19.0")
    base = s["facebook"]["api_base"]
    return f"{base}/{version}"


def _timeout():
    return _load_settings()["facebook"]["request_timeout_seconds"]


# ─── Token Utils ──────────────────────────────────────────────────────────────

def verify_token(page_id: str, access_token: str) -> dict:
    """
    Kiểm tra token có hợp lệ không.
    Returns: {"valid": bool, "name": str, "error": str|None}
    """
    url = f"{_get_api_base()}/{page_id}"
    params = {
        "fields": "name,id",
        "access_token": access_token
    }
    try:
        r = requests.get(url, params=params, timeout=_timeout())
        data = r.json()
        if "error" in data:
            return {"valid": False, "name": None, "error": data["error"]["message"]}
        return {"valid": True, "name": data.get("name", "Unknown"), "error": None}
    except Exception as e:
        return {"valid": False, "name": None, "error": str(e)}


def check_token_expiry(access_token: str, app_id: str, app_secret: str) -> dict:
    """
    Kiểm tra thời hạn token.
    Returns: {"expires_at": datetime|None, "days_remaining": int, "is_expiring_soon": bool}
    """
    url = f"{_get_api_base()}/debug_token"
    params = {
        "input_token": access_token,
        "access_token": f"{app_id}|{app_secret}"
    }
    try:
        r = requests.get(url, params=params, timeout=_timeout())
        data = r.json().get("data", {})
        expires_at_ts = data.get("expires_at")
        if expires_at_ts:
            expires_at = datetime.fromtimestamp(expires_at_ts)
            days_remaining = (expires_at - datetime.now()).days
            return {
                "expires_at": expires_at.isoformat(),
                "days_remaining": days_remaining,
                "is_expiring_soon": days_remaining <= 7
            }
        return {"expires_at": None, "days_remaining": 999, "is_expiring_soon": False}
    except Exception as e:
        return {"expires_at": None, "days_remaining": -1, "is_expiring_soon": False, "error": str(e)}


# ─── Posting ──────────────────────────────────────────────────────────────────

def post_photo(page_id: str, access_token: str, image_path: str,
               caption: str, link: str = None) -> dict:
    """
    Đăng ảnh + caption lên Facebook Page.
    Nếu có link Aff, nhúng vào cuối caption.
    Returns: {"success": bool, "post_id": str|None, "error": str|None}
    """
    url = f"{_get_api_base()}/{page_id}/photos"

    # Nhúng link vào caption nếu có
    full_caption = caption
    if link:
        full_caption = f"{caption}\n\n🔗 {link}"

    if not os.path.exists(image_path):
        return {"success": False, "post_id": None, "error": f"Image not found: {image_path}"}

    try:
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            data = {
                "caption": full_caption,
                "access_token": access_token,
                "published": "true"
            }
            r = requests.post(url, files=files, data=data, timeout=_timeout())
            result = r.json()

        if "error" in result:
            return {"success": False, "post_id": None, "error": result["error"]["message"]}

        post_id = result.get("post_id") or result.get("id")
        return {"success": True, "post_id": post_id, "error": None}

    except requests.exceptions.Timeout:
        return {"success": False, "post_id": None, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "post_id": None, "error": str(e)}


def post_text_only(page_id: str, access_token: str,
                   message: str, link: str = None) -> dict:
    """
    Đăng bài text (không có ảnh) lên Facebook Page.
    Returns: {"success": bool, "post_id": str|None, "error": str|None}
    """
    url = f"{_get_api_base()}/{page_id}/feed"

    full_message = message
    if link:
        full_message = f"{message}\n\n🔗 {link}"

    data = {
        "message": full_message,
        "access_token": access_token
    }
    try:
        r = requests.post(url, data=data, timeout=_timeout())
        result = r.json()

        if "error" in result:
            return {"success": False, "post_id": None, "error": result["error"]["message"]}

        return {"success": True, "post_id": result.get("id"), "error": None}

    except requests.exceptions.Timeout:
        return {"success": False, "post_id": None, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "post_id": None, "error": str(e)}


def get_page_info(page_id: str, access_token: str) -> dict:
    """Lấy thông tin cơ bản của Page."""
    url = f"{_get_api_base()}/{page_id}"
    params = {
        "fields": "name,id,fan_count,category",
        "access_token": access_token
    }
    try:
        r = requests.get(url, params=params, timeout=_timeout())
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ─── Batch Operations ─────────────────────────────────────────────────────────

def post_to_multiple_pages(fanpages: list, image_path: str,
                            caption: str, link: str = None) -> list:
    """
    Đăng cùng 1 bài lên nhiều fanpages.
    fanpages: list of {"page_id": ..., "access_token": ..., "name": ...}
    Returns: list of results
    """
    results = []
    for page in fanpages:
        result = post_photo(
            page_id=page["page_id"],
            access_token=page["access_token"],
            image_path=image_path,
            caption=caption,
            link=link
        )
        result["fanpage_name"] = page.get("name", page["page_id"])
        results.append(result)
    return results


if __name__ == "__main__":
    # Quick test: verify token
    import sys
    cfg = _load_config()
    for fp in cfg.get("pages", []):
        if fp.get("active"):
            result = verify_token(fp["id"], fp["access_token"])
            status = "✅" if result["valid"] else "❌"
            print(f"{status} {fp['name']}: {result.get('name') or result.get('error')}")
