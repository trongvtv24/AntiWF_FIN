"""
content_bridge.py — Cầu nối Psycho-Content-Engineer → FB Publisher Queue
Tự động tạo nội dung cho từng fanpage và mớm vào queue liên tục.

Hoạt động:
1. Kiểm tra queue của từng fanpage
2. Nếu pending < min_pending → gọi AI tạo nội dung mới
3. Tạo image prompt → đưa vào queue với scheduled_at theo post_times

Sử dụng:
    python content_bridge.py --run          # Chạy 1 lần fill queue
    python content_bridge.py --daemon       # Chạy liên tục (check mỗi giờ)
    python content_bridge.py --page <id>    # Fill cho 1 page cụ thể
"""

import sys
import json
import time
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

# ─── Path Setup ───────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = Path("C:/Users/Administrator/.gemini/antigravity/data/fb-publisher")
CONFIG_FILE = DATA_DIR / "config" / "fanpages.json"
SETTINGS_FILE = DATA_DIR / "config" / "settings.json"

sys.path.insert(0, str(SKILL_DIR / "scripts"))
import queue_manager as qm

# ─── Logger ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [BRIDGE] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("content_bridge")


# ─── Config Loader ────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_settings() -> dict:
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Psycho-Content Templates ─────────────────────────────────────────────────
# Module tạo nội dung dựa trên 4 hệ thống tâm lý học:
# Cialdini (thuyết phục) + Ekman (cảm xúc) + Duhigg (thói quen) + Mitnick (framing)

PSYCHO_FORMULAS = {
    "cialdini_scarcity": {
        "name": "Sự khan hiếm (Scarcity)",
        "pattern": "⚠️ {hook}\n\n{problem}\n\n✅ {solution}\n\n⏰ {urgency}\n\n{cta}",
        "emotion": "sợ bỏ lỡ, lo lắng"
    },
    "cialdini_social_proof": {
        "name": "Bằng chứng xã hội (Social Proof)",
        "pattern": "🔥 {hook}\n\n👥 {proof}\n\n💡 {insight}\n\n❓ {question}\n\n{cta}",
        "emotion": "tin tưởng, muốn thuộc về nhóm"
    },
    "ekman_surprise": {
        "name": "Bất ngờ (Surprise)",
        "pattern": "😱 {hook_surprising}\n\n❌ Sự thật phũ phàng: {paradox}\n\n✅ {reframe}\n\n{actionable}\n\n{cta}",
        "emotion": "ngạc nhiên, tò mò"
    },
    "duhigg_habit": {
        "name": "Vòng lặp thói quen (Habit Loop)",
        "pattern": "👉 {cue}\n\n📌 {routine}\n\n🎯 {reward}\n\n💬 {share_prompt}\n\n{cta}",
        "emotion": "muốn thay đổi thói quen"
    },
    "mitnick_authority": {
        "name": "Định khung quyền lực (Authority Frame)",
        "pattern": "📊 {claim}\n\n🔬 {evidence}\n\n💡 {lesson}\n\n🚀 {empowerment}\n\n{cta}",
        "emotion": "tin tưởng, học hỏi"
    },
    "storytelling": {
        "name": "Kể chuyện cảm xúc",
        "pattern": "📝 {story_hook}\n\n😔 {conflict}\n\n🌟 {turning_point}\n\n❤️ {resolution}\n\n{cta}",
        "emotion": "đồng cảm, xúc động"
    }
}

# Topic templates cho từng niche
NICHE_CONTENT_MAP = {
    "nuôi con, làm mẹ, chia sẻ kinh nghiệm mẹ bỉm": {
        "topics": [
            "Mẹo hay khi bé biếng ăn",
            "Dấu hiệu bé phát triển tốt",
            "Làm mẹ không cần hoàn hảo",
            "Khoảnh khắc đẹp bên con",
            "Sai lầm mẹ trẻ hay gặp",
            "Bí quyết mẹ bỉm vượt stress",
            "Khi bé khóc đêm — làm gì?",
            "Dinh dưỡng cho bé 6-12 tháng"
        ],
        "cta_options": [
            "Mẹ đang gặp tình huống này không? Comment để cùng chia sẻ nhé! 💕",
            "Tag một người mẹ cần đọc điều này! 👇",
            "Lưu lại để không quên mẹ nhé! 📌",
            "Các mẹ đã thử chưa? Share kinh nghiệm với mình nhé!"
        ]
    },
    "sức khỏe, thực phẩm chức năng, sống lành mạnh": {
        "topics": [
            "5 thói quen buổi sáng tốt cho sức khỏe",
            "Thực phẩm tăng đề kháng tự nhiên",
            "Dấu hiệu cơ thể đang thiếu chất",
            "Uống nước đúng cách — ít ai biết",
            "Giấc ngủ ngon — chìa khóa sức khỏe",
            "Detox cơ thể sau Tết",
            "Thực phẩm chống lão hóa",
            "Lý do bạn luôn mệt mỏi"
        ],
        "cta_options": [
            "Lưu lại để áp dụng từ ngày mai nhé! 💪",
            "Bạn đã biết điều này chưa? Comment bên dưới!",
            "Share cho người thân để cùng sống khỏe! ❤️",
            "Thử ngay hôm nay và cảm nhận sự khác biệt!"
        ]
    },
    "phát triển bản thân, kiếm tiền online, tư duy thành công": {
        "topics": [
            "Tư duy của người giàu vs người nghèo",
            "1 quyết định thay đổi cuộc đời",
            "Tại sao bạn chưa thành công",
            "Bí mật người kiếm 100 triệu/tháng",
            "Cách thoát khỏi vòng lặp nghèo",
            "Thói quen của triệu phú tự thân",
            "Đọc sách đúng cách — ít ai làm",
            "Network = Net worth: Kết nối đúng người"
        ],
        "cta_options": [
            "Save lại và thực hành ngay hôm nay! 🚀",
            "Tag người bạn muốn cùng thay đổi! 💬",
            "Comment: Mục tiêu tài chính 2025 của bạn là gì?",
            "Theo dõi để không bỏ lỡ bài tiếp theo! 🔔"
        ]
    },
    "địa chính trị, thế giới sự kiện, quan hệ quốc tế": {
        "topics": [
            "Thế giới đang thay đổi như thế nào?",
            "Những bí mật quyền lực ít ai biết",
            "Tại sao các siêu cường xung đột?",
            "Kinh tế thế giới 2025 — dự báo",
            "Ảnh hưởng của AI đến địa chính trị",
            "Bài học lịch sử cho ngày hôm nay",
            "Tương lai của NATO — sẽ đi về đâu?",
            "Chiến lược nước lớn — ai thắng?"
        ],
        "cta_options": [
            "Quan điểm của bạn?  Comment bên dưới! 💬",
            "Share nếu bạn thấy đây là góc nhìn đáng suy ngẫm!",
            "Bạn đồng ý hay không? Tranh luận văn minh nhé! 🤝",
            "Follow để cập nhật góc nhìn từ khắp thế giới! 🌍"
        ]
    }
}


# ─── Content Generator (Psycho-Based) ────────────────────────────────────────

def generate_post_content(page: dict, topic: str = None) -> dict:
    """
    Tạo nội dung bài đăng dựa trên psycho-content-engineer framework.
    Returns: {post_text, image_prompt, topic}
    """
    import random

    niche = page.get("niche", "general")
    tone = page.get("tone", "thân thiện")
    page_name = page.get("name", "Page")

    # Lấy niche map phù hợp nhất
    niche_data = None
    for niche_key, data in NICHE_CONTENT_MAP.items():
        if any(word in niche for word in niche_key.split(", ")):
            niche_data = data
            break

    if not niche_data:
        niche_data = {
            "topics": ["Nội dung hữu ích cho bạn"],
            "cta_options": ["Hãy chia sẻ nếu bài viết có ích! ❤️"]
        }

    # Chọn topic nếu chưa có
    if not topic:
        topic = random.choice(niche_data["topics"])

    # Chọn công thức tâm lý học
    formula_key = random.choice(list(PSYCHO_FORMULAS.keys()))
    formula = PSYCHO_FORMULAS[formula_key]
    cta = random.choice(niche_data["cta_options"])

    # Tạo nội dung dựa trên formula (template-based, không cần API)
    post_text = _build_post_text(topic, formula, tone, cta, niche)
    image_prompt = _build_image_prompt(topic, niche, page_name)

    return {
        "topic": topic,
        "formula": formula["name"],
        "post_text": post_text,
        "image_prompt": image_prompt
    }


def _build_post_text(topic: str, formula: dict, tone: str, cta: str, niche: str) -> str:
    """Xây dựng bài viết theo công thức tâm lý."""
    import random

    hooks = {
        "nuôi con": [
            f"🍼 {topic} — Điều mình ước gì biết sớm hơn!",
            f"👶 Mẹ ơi, {topic.lower()} không khó như bạn nghĩ!",
            f"💕 Bài học quý giá về {topic.lower()} mình muốn chia sẻ:"
        ],
        "sức khỏe": [
            f"🏥 Bác sĩ nói về {topic.lower()} — Bạn đã biết chưa?",
            f"⚡ {topic}: Sự thật khiến nhiều người ngỡ ngàng!",
            f"🌿 {topic} — Hãy áp dụng ngay hôm nay!"
        ],
        "phát triển": [
            f"💰 {topic} — Bí mật mà người thành công không nói!",
            f"🚀 Nếu bạn muốn thành công, hãy đọc ngay: {topic}",
            f"🎯 {topic}: Điều tôi ước ai đó nói với tôi từ 10 năm trước"
        ],
        "địa chính trị": [
            f"🌍 {topic} — Góc nhìn mà truyền thông không đưa tin",
            f"⚔️ {topic}: Sự thật đằng sau những gì bạn thấy",
            f"🔍 Phân tích: {topic}"
        ]
    }

    # Chọn hook phù hợp niche
    hook = topic
    for key, hook_list in hooks.items():
        if key in niche:
            hook = random.choice(hook_list)
            break

    # Xây dựng body content
    body_templates = [
        f"""👉 Hôm nay mình muốn chia sẻ về {topic.lower()}.

Đây là điều mà rất nhiều người quan tâm nhưng ít ai hiểu đúng hoàn toàn.

✅ Điều quan trọng nhất bạn cần biết:
• Hiểu đúng vấn đề thay vì chạy theo đám đông
• Áp dụng có chọn lọc, phù hợp với hoàn cảnh của bạn
• Kiên trì — kết quả không đến trong 1 ngày

💡 Bài học thực tế:
Đừng để thông tin áp đảo bạn. Hãy bắt đầu với 1 bước nhỏ nhất.

{cta}""",

        f"""📌 Bạn có biết về {topic.lower()} không?

Nhiều người đang làm sai điều này mà không hay biết.

❌ Sai lầm phổ biến: Cố gắng làm tất cả cùng một lúc
✅ Cách đúng: Tập trung vào điều quan trọng nhất trước

🎯 3 bước đơn giản:
1️⃣ Nhận diện đúng vấn đề
2️⃣ Tìm giải pháp phù hợp với bạn  
3️⃣ Hành động ngay hôm nay

{cta}""",

        f"""💬 {topic}

Mình đã học được điều này sau rất nhiều thử nghiệm và cả thất bại.

Sự thật là: hầu hết chúng ta đều có thể làm tốt hơn — chỉ cần biết đúng cách.

Điều mình muốn bạn nhớ:
→ Đừng so sánh hành trình của bạn với người khác
→ Mỗi người có điểm xuất phát khác nhau
→ Quan trọng là bạn đang tiến về phía trước

{cta}"""
    ]

    body = random.choice(body_templates)
    full_post = f"{hook}\n\n{body}"

    return full_post


def _build_image_prompt(topic: str, niche: str, page_name: str) -> str:
    """Tạo prompt cho AI generate ảnh phù hợp với nội dung."""

    style_map = {
        "nuôi con": "warm photography, mother and baby, soft pastel colors, cozy home setting",
        "sức khỏe": "clean health lifestyle photo, fresh vegetables, bright natural light, wellness aesthetic",
        "phát triển": "motivation concept, professional success, modern office, upward arrow, gold and dark blue",
        "địa chính trị": "world map, geopolitics concept, dramatic lighting, news editorial style"
    }

    style = "modern flat design, vibrant colors, clean layout"
    for key, val in style_map.items():
        if key in niche:
            style = val
            break

    return (
        f"Facebook post image for '{topic}', {style}, "
        f"text overlay '{topic[:40]}', 1080x1080 square format, "
        f"professional social media graphic, high quality"
    )


# ─── Schedule Calculator ───────────────────────────────────────────────────────

def get_next_post_times(page: dict, count: int = 5) -> list:
    """
    Lấy danh sách các scheduled_at timestamp kế tiếp cho page.
    Dựa vào post_times cài trong fanpage config.
    """
    post_times = page.get("post_times", ["08:00", "12:00", "19:00"])
    now = datetime.now()
    scheduled_slots = []
    day_offset = 0

    while len(scheduled_slots) < count:
        target_date = now.date() + timedelta(days=day_offset)
        for time_str in sorted(post_times):
            hour, minute = map(int, time_str.split(":"))
            slot = datetime(
                target_date.year, target_date.month, target_date.day,
                hour, minute, 0
            )
            if slot > now:  # Chỉ lấy slot trong tương lai
                scheduled_slots.append(slot.isoformat())
                if len(scheduled_slots) >= count:
                    break
        day_offset += 1

    return scheduled_slots


# ─── Queue Fill Logic ─────────────────────────────────────────────────────────

def fill_queue_for_page(page: dict, target_pending: int = 10) -> int:
    """
    Fill queue cho 1 page đến số lượng target.
    Returns: số bài mới đã thêm
    """
    page_id = page["id"]
    page_name = page["name"]

    # Đếm pending hiện tại
    summary = qm.get_queue_summary()
    current_pending = summary["by_fanpage"].get(page_name, {}).get("pending", 0)

    needed = target_pending - current_pending
    if needed <= 0:
        log.info(f"[{page_name}] Queue đủ ({current_pending} pending), bỏ qua")
        return 0

    log.info(f"[{page_name}] Cần thêm {needed} bài (hiện có {current_pending} pending)")

    # Lấy scheduled slots
    slots = get_next_post_times(page, count=needed)

    added = 0
    for i, scheduled_at in enumerate(slots):
        try:
            content = generate_post_content(page)
            post_id = qm.add_post(
                fanpage_id=page_id,
                fanpage_name=page_name,
                post_text=content["post_text"],
                image_path="",  # Sẽ được generate bởi worker
                image_prompt=content["image_prompt"],
                aff_link=None,
                scheduled_at=scheduled_at,
                priority=1
            )
            log.info(f"  ✅ [{page_name}] Thêm bài [{post_id}] — {content['topic']} → {scheduled_at}")
            added += 1
        except Exception as e:
            log.error(f"  ❌ [{page_name}] Lỗi tạo bài: {e}")

    return added


def fill_all_queues() -> dict:
    """Fill queue cho tất cả pages active."""
    cfg = load_config()
    s = load_settings()

    min_pending = s["queue"].get("auto_fill_min_pending", 3)
    target = s["queue"].get("auto_fill_target", 10)

    results = {}
    for page in cfg.get("pages", []):
        if not page.get("active", False):
            continue
        added = fill_queue_for_page(page, target_pending=target)
        results[page["name"]] = added

    return results


# ─── Daemon Mode ──────────────────────────────────────────────────────────────

def run_daemon(check_interval_hours: float = 1.0):
    """
    Chạy liên tục, tự động fill queue khi cạn.
    """
    log.info("🤖 Content Bridge DAEMON started")
    log.info(f"   Check interval: {check_interval_hours}h")

    while True:
        try:
            log.info("🔍 Kiểm tra queue...")
            results = fill_all_queues()
            total = sum(results.values())
            log.info(f"✅ Đã thêm {total} bài vào queue: {results}")
        except Exception as e:
            log.error(f"❌ Lỗi fill queue: {e}")

        log.info(f"💤 Ngủ {check_interval_hours}h rồi check lại...")
        time.sleep(check_interval_hours * 3600)


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Content Bridge — Psycho-Content-Engineer → FB Queue",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--run", action="store_true",
        help="Chạy 1 lần: fill queue cho tất cả pages"
    )
    parser.add_argument(
        "--daemon", action="store_true",
        help="Chạy liên tục: tự fill queue mỗi 1 giờ"
    )
    parser.add_argument(
        "--page", type=str, default=None,
        help="Fill queue cho 1 page (theo ID hoặc tên)"
    )
    parser.add_argument(
        "--count", type=int, default=10,
        help="Số bài cần có trong queue (mặc định: 10)"
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Xem preview nội dung sẽ tạo (không add vào queue)"
    )
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════╗
║   🧠 PSYCHO-CONTENT → FB QUEUE BRIDGE       ║
║   Powered by: Cialdini + Ekman + Duhigg     ║
╚══════════════════════════════════════════════╝
""")

    cfg = load_config()

    if args.preview:
        # Preview mode: tạo sample content cho mỗi page
        print("📋 PREVIEW CONTENT (không lưu vào queue)\n")
        for page in cfg.get("pages", []):
            if not page.get("active"):
                continue
            content = generate_post_content(page)
            print(f"{'='*60}")
            print(f"📢 PAGE: {page['name']}")
            print(f"🎯 TOPIC: {content['topic']}")
            print(f"🧠 FORMULA: {content['formula']}")
            print(f"\n📝 POST TEXT:\n{content['post_text']}")
            print(f"\n🖼️  IMAGE PROMPT:\n{content['image_prompt']}")
            print()

    elif args.page:
        # Fill cho 1 page cụ thể
        target_page = None
        for page in cfg.get("pages", []):
            if page["id"] == args.page or page["name"] == args.page:
                target_page = page
                break

        if not target_page:
            print(f"❌ Không tìm thấy page: {args.page}")
            print("Available pages:")
            for p in cfg.get("pages", []):
                print(f"  - {p['id']}: {p['name']}")
            sys.exit(1)

        added = fill_queue_for_page(target_page, target_pending=args.count)
        print(f"\n✅ Đã thêm {added} bài vào queue của [{target_page['name']}]")

    elif args.daemon:
        run_daemon(check_interval_hours=1.0)

    elif args.run:
        results = fill_all_queues()
        print("\n📊 KẾT QUẢ:")
        total = 0
        for page_name, added in results.items():
            emoji = "✅" if added > 0 else "⏭️"
            print(f"  {emoji} {page_name}: +{added} bài")
            total += added
        print(f"\n🎉 Tổng cộng thêm {total} bài vào queue!")

    else:
        parser.print_help()
