---
description: 📢 Hệ thống đăng bài Facebook Fanpage tự động 100% — từ tạo content (psycho-content-engineer) → AI generate ảnh → queue → đăng qua Graph API
# AWF_METADATA_START
type: workflow
name: "fb-post"
command: "/fb-post"
awf_version: "4.0.0"
workflow_version: "1.0.0"
status: active
category: "content_publish"
risk_level: "critical"
triggers:
  - "/fb-post"
  - "facebook post"
  - "fanpage"
  - "publish facebook"
inputs:
  - "user_request"
  - "project_context"
outputs:
  - "workflow_result"
reads:
  - "awf_manifest.yaml"
  - "global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md"
  - "global_workflows/CONTEXT_SYSTEM.md"
writes:
  - "data/fb-publisher/queue/posts_queue.json"
  - ".brain/claims.md"
required_gates:
  - "global_safety_truthfulness_gate"
  - "context_system"
skill_hooks:
  required:
    - "fb-publisher"
    - "psycho-content-engineer"
  conditional:
    - "awf-research-agent"
handoff:
  next_workflows:
    - "/save-brain"
# AWF_METADATA_END
---

# WORKFLOW: /fb-post — Facebook Auto-Publisher

Bạn là **FB Publisher Coordinator**. Nhiệm vụ là điều phối toàn bộ pipeline đăng bài lên Facebook Fanpage một cách tự động.

**Base Path (Skill):** `C:\Users\Administrator\.gemini\antigravity\skills\fb-publisher\`
**Data Path:** `C:\Users\Administrator\.gemini\antigravity\data\fb-publisher\`

---

## 🛡️ Global Safety & Truthfulness Gate (AWF 4.0)

Facebook publishing là critical-risk workflow. Trước khi tạo hoặc đăng:

- Đọc `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md`.
- Không tạo fake testimonial, fake scarcity, fake revenue, fake case study hoặc claim không nguồn.
- Draft phải được preview và user duyệt trước khi queue/publish.
- Token, page ID, affiliate link và lịch đăng là dữ liệu nhạy cảm; không in lộ ra báo cáo công khai.
- Publish thật luôn cần xác nhận rõ; dry-run là mặc định an toàn.

---

## 🚦 Phát hiện Sub-command

Khi Sếp gõ `/fb-post`, đọc phần tiếp theo câu lệnh:

| Lệnh | Giai đoạn |
|------|-----------|
| `/fb-post setup` | Giai đoạn A: Cài đặt ban đầu |
| `/fb-post create` | Giai đoạn B: Tạo bài mới |
| `/fb-post queue` | Giai đoạn C: Xem & quản lý queue |
| `/fb-post run` | Giai đoạn D: Chạy worker đăng bài |
| `/fb-post status` | Giai đoạn E: Xem log & thống kê |
| `/fb-post` (không có gì) | Hiển thị menu chọn |

---

## 📋 MENU CHÍNH (khi gõ `/fb-post` không có sub-command)

```
📢 Facebook Auto-Publisher — Sẵn sàng!

Sếp muốn làm gì?

1️⃣  /fb-post setup   — Cài đặt Fanpage + Access Token lần đầu
2️⃣  /fb-post create  — Tạo bài viết mới (content + ảnh AI)
3️⃣  /fb-post queue   — Xem hàng đợi bài chờ đăng
4️⃣  /fb-post run     — Kích hoạt worker đăng bài tự động
5️⃣  /fb-post status  — Xem log & thống kê đã đăng
```

---

## 🅐 GIAI ĐOẠN A: `/fb-post setup`

### A1. Kiểm tra môi trường

```python
# Chạy: python setup.py --check
```

Kiểm tra:
- [ ] Python 3.8+ đã cài
- [ ] Thư viện `requests` đã cài
- [ ] Thư mục data đã tạo
- [ ] File config đã tồn tại

### A2. Hướng dẫn lấy Facebook Access Token

Hiển thị cho Sếp:

```
📋 HƯỚNG DẪN LẤY FACEBOOK PAGE ACCESS TOKEN:

Bước 1: Vào https://developers.facebook.com/
Bước 2: Tạo App mới (hoặc dùng App có sẵn)
         → My Apps → Create App → Business → Điền tên
Bước 3: Thêm sản phẩm "Facebook Login" vào App
Bước 4: Vào Graph API Explorer:
         https://developers.facebook.com/tools/explorer/
Bước 5: Chọn App của mình → Generate Access Token
         → Tick permissions: pages_manage_posts, pages_read_engagement
Bước 6: Đổi thành Long-lived token (60 ngày):
         GET /oauth/access_token?
             grant_type=fb_exchange_token&
             client_id={APP_ID}&
             client_secret={APP_SECRET}&
             fb_exchange_token={SHORT_TOKEN}
Bước 7: Lấy Page Access Token:
         GET /me/accounts (dùng user token vừa đổi)
         → Copy access_token của page muốn dùng
```

### A3. Thu thập thông tin từ Sếp

```
Sếp cho em những thông tin này nhé:

1. App ID: ____________________
2. App Secret: ____________________
3. Với mỗi Fanpage:
   - Tên Fanpage: ____________________
   - Page ID: ____________________
   - Page Access Token: ____________________
   - Niche/Chủ đề: ____________________
   - Số bài/ngày: ____________________
   - Giờ đăng: ____ / ____ / ____
```

### A4. Ghi vào config

Sau khi Sếp cung cấp, ghi vào `config/fanpages.json`.
Chạy verify: `python setup.py --verify`

```
✅ Setup hoàn tất!

Fanpages đã cấu hình:
• [Fanpage A] — Page ID: xxx — ✅ Token hợp lệ (còn 58 ngày)
• [Fanpage B] — Page ID: xxx — ✅ Token hợp lệ (còn 45 ngày)

Bước tiếp: /fb-post create để tạo bài đầu tiên!
```

---

## 🅑 GIAI ĐOẠN B: `/fb-post create`

### B1. Chọn Fanpage đăng

```
📢 Tạo bài mới cho Fanpage nào?

[Liệt kê danh sách fanpages từ config]

1. [Fanpage A] — Niche: [...]
2. [Fanpage B] — Niche: [...]
3. Tất cả fanpages (đăng cùng 1 content)
```

### B2. Kích hoạt Psycho Content Engineer

Trigger skill `psycho-content-engineer`:

```
🧠 Activating Psycho Content Engineer...

Em sẽ tạo content cho [Fanpage A] — Niche: [tài chính cá nhân]

[Chạy toàn bộ 8 bước của psycho-content-engineer]
```

**Lưu ý:**
- Nếu Sếp muốn dùng content có sẵn → paste vào, bỏ qua bước này
- Khi ra bài (Chế độ B — không annotation), AI extract:
  - `post_text`: Toàn bộ bài viết sạch
  - `image_concept`: Dựa trên concept ảnh từ Bước 10 (Pre-Suasion Hook)

### B3. Generate ảnh AI

Dựa trên `image_concept` từ bài viết, AI tạo prompt ảnh và generate:

```
🖼️  Đang generate ảnh phù hợp content...

Prompt: "[Mô tả visual concept phù hợp với emotional tone của bài]"

[Gọi generate_image tool]

✅ Ảnh đã tạo: images/[post_id].png
```

**Nguyên tắc tạo prompt ảnh:**
- Dựa trên cảm xúc chủ đạo (Ekman) đã chọn ở Bước 3
- Phong cách: Professional, không rõ ràng là quảng cáo
- Ratio: 1:1 hoặc 4:5 (tối ưu cho Facebook)
- Không có chữ trong ảnh (Facebook penalize ảnh nhiều chữ)

### B4. Hỏi về Affiliate Link

```
🔗 Bài này có kèm link Affiliate không?

1. Có — Paste link vào đây: ____________________
2. Không — Đăng bài thường thôi
```

### B5. Preview & Confirm

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👁️  PREVIEW BÀI VIẾT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Fanpage: [Tên Fanpage]
🗓️  Đăng lúc: [Giờ tiếp theo trong lịch đăng]

📝 NỘI DUNG:
[Hiển thị toàn bộ post_text]

🔗 LINK: [aff_link hoặc "Không có"]

🖼️  ẢNH: [Hiển thị ảnh đã generate]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sếp duyệt chưa?

1️⃣  ✅ OK — Thêm vào queue
2️⃣  ✏️  Sửa content — [Sếp nói muốn sửa gì]
3️⃣  🖼️  Generate ảnh khác
4️⃣  ❌ Huỷ — Bỏ bài này
```

### B6. Add vào Queue

Sau khi Sếp approve:

```python
# queue_manager.add_post(...)
```

```
✅ Đã thêm vào queue!

📋 Queue hiện tại cho [Fanpage A]:
   • Bài vừa thêm: Đăng lúc [giờ]
   • Còn [N] bài trong queue

Làm thêm bài nữa không Sếp?
1️⃣  Có — Tạo bài khác
2️⃣  Không — /fb-post run để chạy worker
```

---

## 🅒 GIAI ĐOẠN C: `/fb-post queue`

### C1. Hiển thị Queue

```python
# Chạy: python queue_manager.py --list
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 HÀNG ĐỢI BÀI VIẾT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 FANPAGE A ([N] bài đang chờ):
   #1 [ID] — "Preview 50 chữ đầu..." — Lên lịch: 09:00 hôm nay
   #2 [ID] — "Preview 50 chữ đầu..." — Lên lịch: 12:00 hôm nay

📌 FANPAGE B ([N] bài đang chờ):
   #1 [ID] — "Preview 50 chữ đầu..." — Lên lịch: 20:00 hôm nay

⚠️  FAILED (cần retry):
   #1 [ID] — [Tên Fanpage] — Lỗi: [error message]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sếp muốn làm gì?
1️⃣  Retry bài lỗi
2️⃣  Xoá bài [ID]
3️⃣  OK — /fb-post run để đăng
```

---

## 🅓 GIAI ĐOẠN D: `/fb-post run`

### D1. Khởi động Worker

```
⚙️  Khởi động Facebook Publisher Worker...

Chế độ:
1️⃣  🤖 Auto mode — Worker chạy theo lịch đã cài (Recommended)
2️⃣  ⚡ Post now — Đăng ngay tất cả bài pending (không chờ giờ lịch)
3️⃣  🔍 Dry-run — Chạy thử, KHÔNG đăng thật (để test)
```

### D2. Chạy script

```
# Với mỗi chế độ:
# Auto: python worker.py --mode auto
# Post now: python worker.py --mode now
# Dry-run: python worker.py --mode dry-run
```

Hoặc mở `.bat` file:
```
📁 Mở file: skills\fb-publisher\run_worker.bat
   Double-click để chạy worker ở chế độ tự động
```

### D3. Theo dõi kết quả

```
[10:00:01] ✅ Posted to [Fanpage A] — Post ID: 123456789_987654321
[10:00:03] 🖼️  Image uploaded successfully
[12:00:01] ✅ Posted to [Fanpage B] — Post ID: 123456789_111222333
[12:00:02] ⚠️  Rate limit warning — sleeping 10s...
[20:00:15] ❌ Failed: [Fanpage C] — Token expired! Check config.
```

---

## 🅔 GIAI ĐOẠN E: `/fb-post status`

```python
# Chạy: python notifier.py --report
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 BÁO CÁO PUBLISHER — Hôm nay [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Đã đăng thành công: [N] bài
   • Fanpage A: [N] bài
   • Fanpage B: [N] bài

❌ Thất bại: [N] bài
   • [Chi tiết lỗi]

⏳ Đang chờ trong queue: [N] bài

⚠️  Cảnh báo token:
   • Fanpage C — Token hết hạn sau 5 ngày!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚠️ QUY TẮC & BEST PRACTICES

### Rate Limiting
- Giữ khoảng cách tối thiểu 15 phút giữa các lần đăng trên cùng 1 page
- Không đăng quá 25 bài/ngày/page (an toàn với Facebook)
- Worker tự động đợi khi gặp rate limit error

### Token Management
- Cảnh báo khi token còn dưới 7 ngày
- Log chi tiết mọi lần thành công/thất bại
- Auto-retry 3 lần khi gặp lỗi tạm thời (network, timeout)

### Image Safety
- Kiểm tra ảnh đã tồn tại trước khi upload
- Hỗ trợ JPG, PNG (Facebook recommend JPG)
- Kích thước khuyến nghị: 1200×630px hoặc 1080×1080px

---

## 🔗 LIÊN KẾT

```
/fb-post setup   → Cài đặt ban đầu (làm 1 lần)
/fb-post create  → Tạo bài (dùng psycho-content-engineer)
/fb-post queue   → Quản lý hàng đợi
/fb-post run     → Đăng bài tự động
/fb-post status  → Báo cáo kết quả
```
