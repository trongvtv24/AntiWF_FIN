"""
image_generator.py — Tạo và quản lý ảnh AI cho bài đăng Facebook
Sử dụng Pollinations.AI (miễn phí, không cần API key)
"""

import os
import re
import json
import time
import requests
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import quote


# ─── Config ───────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
SETTINGS_FILE = SKILL_DIR / "config" / "settings.json"


def _load_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_image_dir() -> Path:
    s = _load_settings()
    path = Path(s["image"]["save_dir"])
    path.mkdir(parents=True, exist_ok=True)
    return path


# ─── Pollinations.AI Integration ──────────────────────────────────────────────

def generate_image_pollinations(prompt: str, post_id: str,
                                 width: int = 1080, height: int = 1080) -> dict:
    """
    Generate ảnh dùng Pollinations.AI (free, no API key).
    Returns: {"success": bool, "image_path": str|None, "error": str|None}
    """
    save_dir = _get_image_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{post_id}_{timestamp}.jpg"
    save_path = save_dir / filename

    # Build URL cho Pollinations
    safe_prompt = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{safe_prompt}"
        f"?width={width}&height={height}&nologo=true&model=flux"
        f"&seed={int(time.time())}"
    )

    try:
        print(f"🖼️  Generating image...")
        print(f"   Prompt: {prompt[:80]}...")

        r = requests.get(url, timeout=120, stream=True)
        r.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = os.path.getsize(save_path)
        if file_size < 1000:  # Ảnh quá nhỏ → lỗi
            os.remove(save_path)
            return {"success": False, "image_path": None,
                    "error": "Generated image too small (possible API error)"}

        print(f"   ✅ Saved: {save_path} ({file_size // 1024}KB)")
        return {"success": True, "image_path": str(save_path), "error": None}

    except requests.exceptions.Timeout:
        return {"success": False, "image_path": None, "error": "Image generation timeout (>120s)"}
    except Exception as e:
        return {"success": False, "image_path": None, "error": str(e)}


# ─── Prompt Engineering ───────────────────────────────────────────────────────

def build_image_prompt(post_text: str, emotion: str = None, niche: str = None) -> str:
    """
    Tự động tạo prompt ảnh tối ưu cho Facebook dựa trên nội dung bài.
    
    Nguyên tắc:
    - Không có chữ/text trong ảnh (Facebook penalize)
    - Professional, không rõ ràng là quảng cáo
    - Phù hợp với cảm xúc chủ đạo của bài (Ekman)
    - Phù hợp niche của fanpage
    """
    # Extract context từ bài viết
    text_preview = post_text[:300] if post_text else ""

    # Emotional mapping (Ekman → visual style)
    emotion_styles = {
        "fear": "dramatic lighting, dark atmosphere with hope breaking through",
        "desire": "aspirational lifestyle, bright warm colors, success symbols",
        "joy": "vibrant, warm colors, smiling faces, celebration",
        "trust": "clean professional, blue tones, reliability symbols",
        "surprise": "unexpected visual, dynamic composition, bold contrast",
        "sadness": "muted tones, relatable struggle, turning point moment",
        "anger": "high contrast, bold red accents, injustice theme"
    }

    # Niche mapping → visual context
    niche_contexts = {
        "tài chính cá nhân": "Vietnamese person managing finances, savings, investment charts",
        "kinh doanh online": "laptop entrepreneur, e-commerce, digital business success",
        "sức khoẻ": "healthy lifestyle, fresh food, active Vietnamese person",
        "làm đẹp": "beauty skincare, elegant Vietnamese woman, premium products",
        "du lịch": "scenic Vietnam landscapes, travel adventure, exploration"
    }

    style = emotion_styles.get(emotion, "professional, warm, engaging")
    context = niche_contexts.get(niche, "Vietnamese business professional, modern lifestyle")

    prompt = (
        f"Professional Facebook post image, {context}, {style}, "
        f"photorealistic, high quality, 4K, no text overlay, no watermark, "
        f"suitable for social media marketing, natural lighting, "
        f"Vietnamese context, modern aesthetic"
    )

    return prompt


# ─── Main Interface ───────────────────────────────────────────────────────────

def generate_for_post(post_id: str, post_text: str,
                       custom_prompt: str = None,
                       emotion: str = None, niche: str = None) -> dict:
    """
    Entry point chính: generate ảnh cho một bài viết.
    Dùng custom_prompt nếu có, ngược lại tự build từ post_text.
    """
    s = _load_settings()
    width = s["image"]["width"]
    height = s["image"]["height"]

    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = build_image_prompt(post_text, emotion, niche)

    return generate_image_pollinations(prompt, post_id, width, height)


def check_image_exists(image_path: str) -> bool:
    """Kiểm tra file ảnh có tồn tại và hợp lệ không."""
    if not image_path:
        return False
    p = Path(image_path)
    return p.exists() and p.stat().st_size > 1000


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Generator CLI")
    parser.add_argument("--prompt", type=str, required=True, help="Image prompt")
    parser.add_argument("--id", type=str, default="test", help="Post ID")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()

    result = generate_image_pollinations(args.prompt, args.id, args.width, args.height)
    if result["success"]:
        print(f"✅ Image saved: {result['image_path']}")
    else:
        print(f"❌ Error: {result['error']}")
