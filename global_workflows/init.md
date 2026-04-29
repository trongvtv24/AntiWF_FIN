---
description: Khởi tạo dự án mới
# AWF_METADATA_START
type: workflow
name: "init"
command: "/init"
awf_version: "4.0.0"
workflow_version: "2.0.0"
status: active
category: "startup"
risk_level: "medium"
triggers:
  - "/init"
  - "new project"
  - "khoi tao du an"
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
  - ".brain/"
  - "mcp_config.json"
required_gates:
  - "global_safety_truthfulness_gate"
  - "context_system"
skill_hooks:
  required:
    - "awf-onboarding"
    - "git-workflow"
  conditional:
    - "awf-gitnexus-context"
    - "awf-adaptive-language"
handoff:
  next_workflows:
    - "/brainstorm"
    - "/plan"
    - "/customize"
# AWF_METADATA_END
---

# WORKFLOW: /init - Khởi Tạo Dự Án v4.0

**Vai trò:** Project Initializer
**Mục tiêu:** Capture ý tưởng và tạo workspace cơ bản. KHÔNG install packages, KHÔNG setup database.

**NGÔN NGỮ: Luôn trả lời bằng tiếng Việt.**

---

## Flow Position

```
[/init] ← BẠN ĐANG Ở ĐÂY
   ↓
/brainstorm (nếu chưa rõ ý tưởng)
   ↓
/plan (lên kế hoạch features)
   ↓
/design (thiết kế kỹ thuật)
   ↓
/code (viết code)
```

---

## 🎯 Non-Tech Mode (v4.0)

**Đọc preferences.json để điều chỉnh ngôn ngữ:**

```
if technical_level == "newbie":
    → Giải thích đơn giản: "Em sẽ tạo thư mục làm việc cho dự án của anh"
    → Không hỏi về tech stack ngay (AI tự quyết sau)
    → Dùng ví dụ đời thường thay vì thuật ngữ
    → Ẩn phần GitNexus index nếu user không cần biết
```

### Giải thích cho newbie:

```
❌ ĐỪNG: "Initialize project workspace với brain.json và session tracking"
✅ NÊN:  "Em sẽ tạo một thư mục làm việc cho dự án.
          Giống như lập một cuốn sổ tay mới để ghi chép ý tưởng!"
```

---

## Stage 1: Capture Vision (HỎI NGẮN GỌN)

### 1.1. Tên dự án
"Tên dự án là gì? (VD: my-coffee-app)"

### 1.2. Mô tả 1 câu
"Mô tả ngắn gọn app làm gì? (1-2 câu)"

### 1.3. Loại sản phẩm (THÊM MỚI v4.0)

```
"📱 Anh muốn làm loại sản phẩm nào?

1️⃣ Web App (Khuyên dùng)
   - Chạy trên trình duyệt, không cần cài đặt
   - Dùng được trên cả điện thoại lẫn máy tính

2️⃣ Mobile App
   - App trên điện thoại (iOS/Android)
   - Cần đăng lên App Store/Play Store

3️⃣ Landing Page / Website
   - Trang giới thiệu sản phẩm/dịch vụ
   - Chủ yếu hiển thị thông tin, ít tính năng

4️⃣ Tool / Script / Automation
   - Công cụ chạy ở máy tính, không cần giao diện
   - VD: script tự động, bot, CLI tool

5️⃣ Chưa biết — Em hỏi thêm sau (/brainstorm)
   - Em sẽ gợi ý loại phù hợp nhất dựa trên ý tưởng"
```

**Lưu lựa chọn vào brain.json:**
```json
{
  "project": {
    "type": "web_app | mobile | landing_page | tool | unknown"
  }
}
```

**Nếu chọn 5 (Chưa biết):**
- Ghi `"type": "unknown"` vào brain.json
- Chuyển sang /brainstorm sau khi tạo workspace xong

### 1.4. Vị trí
"Tạo ở thư mục hiện tại hay chỗ khác?"

**XONG. Không hỏi thêm.**

---

## Stage 2: Tạo Workspace (CHỈ TẠO FOLDER)

Chỉ tạo cấu trúc folder cơ bản:

```
{project-name}/
├── .brain/
│   ├── brain.json      # Project context (empty template)
│   └── session.json    # Session state (empty template)
├── docs/
│   └── ideas.md        # Ghi ý tưởng
└── README.md           # Tên + mô tả
```

### brain.json template:
```json
{
  "meta": {
    "schema_version": "1.1.0",
    "awf_version": "4.0.2"
  },
  "project": {
    "name": "{project-name}",
    "description": "{mô tả}",
    "type": "{loại: web_app|mobile|landing_page|tool|unknown}",
    "created_at": "{timestamp}",
    "status": "planning"
  },
  "tech_stack": [],
  "features": [],
  "decisions": [],
  "knowledge_items": {
    "patterns": [],
    "gotchas": [],
    "conventions": []
  }
}
```

### session.json template:
```json
{
  "updated_at": "{timestamp}",
  "working_on": {
    "feature": null,
    "task": null,
    "status": "planning"
  },
  "pending_tasks": [],
  "recent_changes": [],
  "errors_encountered": [],
  "decisions_made": []
}
```

### README.md template:
```markdown
# {Project Name}

{Mô tả 1 câu}

**Loại:** {Web App / Mobile App / Landing Page / Tool}

## Status: 🚧 Planning

Dự án đang trong giai đoạn lên ý tưởng.

## Next Steps

1. Gõ `/brainstorm` để explore ý tưởng
2. Hoặc `/plan` nếu đã rõ muốn làm gì
```

---

## Stage 2.5: Auto-detect Existing Project

**Trước khi tạo folder, kiểm tra môi trường hiện tại:**

```
if current_folder có package.json:
    → "Em thấy thư mục này đã có dự án rồi (package.json)."
    → Hỏi: "Anh muốn:
       1️⃣ Init workspace .brain/ cho dự án này (thêm vào)
       2️⃣ Tạo folder mới riêng biệt"

if current_folder có .brain/:
    → "Em thấy thư mục này đã có .brain/ rồi."
    → Hỏi: "Anh muốn:
       1️⃣ Xem lại project hiện tại (/recap)
       2️⃣ Tạo dự án mới trong folder khác"
```

---

## Stage 2.6: GitNexus Index (AWF Integration) 🔬

Sau khi tạo folder xong, **TỰ ĐỘNG** chạy index để AI có khả năng phân tích kiến trúc ngay từ đầu:

```
1. cd vào thư mục project vừa tạo
2. Chạy: gitnexus analyze
   → Nếu thành công: "✅ GitNexus đã index project. AI sẽ có khả năng phân tích kiến trúc từ giờ."
   → Nếu thất bại (lỗi / chưa cài): Bỏ qua, không block workflow
     Báo nhẹ: "⚠️ Chưa index được GitNexus. Anh chạy `gitnexus analyze` sau nhé."
```

> ⚡ **Lưu ý:** Dự án mới thường rỗng nên index rất nhanh (<5 giây).
> Sau khi thêm code, anh chạy lại `gitnexus analyze` để index đầy đủ.

---

## Stage 3: Xác nhận & Hướng dẫn

```
✅ Đã tạo workspace cho "{project-name}"!

📁 Vị trí: {path}
📱 Loại: {Web App / Mobile App / Landing Page / Tool}

🚀 BƯỚC TIẾP THEO:

Chọn 1 trong 2:

1️⃣ /brainstorm - Nếu chưa rõ muốn làm gì, cần explore ý tưởng
2️⃣ /plan - Nếu đã biết rõ features cần làm

💡 Tip: Newbie nên chọn /brainstorm trước!
```

---

## QUAN TRỌNG - KHÔNG LÀM

❌ KHÔNG install packages (để /code làm)
❌ KHÔNG setup database (để /design làm)
❌ KHÔNG tạo code files (để /code làm)
❌ KHÔNG chạy npm/yarn/pnpm
❌ KHÔNG hỏi về tech stack ngay (AI sẽ tự quyết sau ở /plan)

---

## First-time User

Nếu chưa có `.brain/preferences.json` toàn cục:

```
👋 Chào mừng anh đến với AWF!

Đây là lần đầu dùng. Anh muốn:
1️⃣ Dùng mặc định (Recommended)
2️⃣ Tùy chỉnh (/customize)
```

---

## Error Handling

### Folder đã tồn tại:
```
⚠️ Folder "{name}" đã có rồi.
1️⃣ Dùng folder này (thêm .brain/ vào)
2️⃣ Đổi tên khác
3️⃣ Xem dự án hiện tại (/recap)
```

### Không có quyền tạo folder:
```
❌ Không tạo được folder. Kiểm tra quyền write nhé!
```

### Tên project có ký tự đặc biệt:
```
⚠️ Tên "{name}" có ký tự đặc biệt.
Em đề xuất dùng: "{suggested-name}" (chữ thường, dấu gạch ngang)
OK không anh?
```

---

## ⚠️ NEXT STEPS (Menu số):
```
1️⃣ Chưa rõ ý tưởng? /brainstorm
2️⃣ Đã rõ rồi, lên plan luôn? /plan
3️⃣ Muốn tùy chỉnh AI? /customize
```
