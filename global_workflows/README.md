---
description: "AWF workflow documentation"
# AWF_METADATA_START
type: workflow
name: "readme"
command: null
awf_version: "4.0.0"
workflow_version: "2.0.0"
status: active
category: "documentation"
risk_level: "low"
triggers:
  - "awf docs"
  - "readme"
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
  - "workflow_defined_artifacts"
required_gates:
  - "global_safety_truthfulness_gate"
  - "context_system"
skill_hooks:
  required:
    []
  conditional:
    []
handoff:
  next_workflows:
    - "/help"
# AWF_METADATA_END
---

# 🚀 Antigravity Workflow Framework (AWF) v4.0

**Hệ thống Workflow TOÀN DIỆN cho mọi trình độ** - Từ newbie đến pro, AI đều lo được.

> 💡 **Triết lý AWF 4.0:**
> - AI ĐỀ XUẤT, Bạn DUYỆT (Smart Proposal)
> - Mỗi workflow có PERSONA riêng (PM, Developer, Designer, Detective...)
> - KHÔNG BAO GIỜ mất context (Lazy Checkpoint + Proactive Handover)
> - Mọi workflow/skill đi qua router trung tâm và truthfulness gate

---

## 🧭 Source of Truth v4.0

| File | Vai trò |
|------|--------|
| `awf_manifest.yaml` | Router trung tâm: workflow nào chạy, skill nào được kích hoạt, risk level, handoff |
| `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md` | Gate chống ảo giác: phân biệt fact, assumption, external claim, recommendation |
| `global_workflows/CONTEXT_SYSTEM.md` | Chuẩn memory duy nhất cho `.brain/` |
| `docs/design-specs.md` | UI source of truth giữa `/visualize` và `/code` |

**Routing precedence:**

```
explicit command → active workflow state → user intent → contextual recommendation
```

**Required gate mặc định:** mọi workflow quan trọng phải kiểm tra `GLOBAL_SAFETY_TRUTHFULNESS_GATE.md` trước khi đưa claim, sửa code, deploy, publish, research hoặc tạo content.

---

## 📋 Danh sách lệnh cốt lõi (15 Workflows) + mở rộng (6 Workflows)

### 🌟 Khởi động & Ngữ cảnh
| Lệnh | Mô tả | Điểm mù được xử lý |
|------|-------|-------------------|
| `/init` | Tạo dự án mới hoàn chỉnh | Env vars, Git, Code quality tools |
| `/recap` | Tóm tắt context khi quay lại | Context recovery |
| `/save-brain` | Lưu kiến thức cuối buổi | API Docs, Changelog, Business rules |

### 🎯 Phát triển tính năng
| Lệnh | Mô tả | Điểm mù được xử lý |
|------|-------|-------------------|
| `/plan` | Thiết kế tính năng (Smart Proposal) | Auth, DB, Charts, Scheduled Tasks |
| `/design` | **Thiết kế chi tiết** ⭐ NEW | Database, Luồng hoạt động, Acceptance Criteria |
| `/visualize` | Thiết kế UI/UX đẹp | `ui-ux-pro-max`, Loading/Error states, Accessibility |
| `/code` | Viết code chất lượng | Security, Validation, Error handling, UI source of truth |

### ⚙️ Vận hành
| Lệnh | Mô tả | Điểm mù được xử lý |
|------|-------|-------------------|
| `/run` | Khởi động app | Environment detection, Port conflicts |
| `/test` | Kiểm tra logic | Auto-generate tests nếu thiếu |
| `/deploy` | Đưa lên production | SEO, Analytics, Legal, Backup, Monitoring |

### 🔧 Bảo trì
| Lệnh | Mô tả | Điểm mù được xử lý |
|------|-------|-------------------|
| `/debug` | Sửa lỗi (Investigation Protocol) | Giả thuyết + 3 lần thử max |
| `/refactor` | Dọn dẹp code | Safe execution, Before/After comparison |
| `/audit` | Kiểm tra sức khỏe | Security, Performance, Dependencies |
| `/rollback` | Quay về phiên bản cũ | Emergency recovery |
| `/review` | **Tổng quan dự án** ⭐ NEW | Bàn giao, đánh giá, lên kế hoạch nâng cấp |

### 🧩 Lệnh mở rộng
| Lệnh | Mô tả | Điểm mù được xử lý |
|------|-------|-------------------|
| `/brainstorm` | Bàn ý tưởng, research | Làm rõ yêu cầu mơ hồ |
| `/help` | Trợ giúp theo context | Gợi ý đúng bước hiện tại |
| `/customize` | Cá nhân hóa AI | Đồng bộ phong cách làm việc |
| `/next` | Gợi ý bước tiếp theo | Tránh bị kẹt luồng |
| `/script` | Viết script YouTube | Quy trình content end-to-end |


---

## 🔥 ĐIỂM MÙ VIBE CODER ĐÃ ĐƯỢC XỬ LÝ TOÀN DIỆN

### 📐 Khi lên kế hoạch (`/plan`)
| Điểm mù | AI tự hỏi |
|---------|-----------|
| Database Design | "Có dữ liệu sẵn không? Quản lý những gì?" |
| Auth/Login | "Cần đăng nhập không? OAuth? Roles?" |
| File Upload | "Có upload hình không? Size limit?" |
| Email/Notifications | "Cần gửi thông báo không?" |
| Payment | "Có nhận thanh toán không?" |
| Search | "Có tìm kiếm không? Fuzzy?" |
| Scheduled Tasks | "Có cần tự động chạy hàng ngày?" |
| Charts/Graphs | "Có cần biểu đồ không?" |
| PDF/Print | "Có cần in hóa đơn không?" |
| Maps | "Có cần bản đồ không?" |
| Real-time | "Có cần live updates không?" |

### 🎨 Khi thiết kế UI (`/visualize`)
| Điểm mù | AI tự xử lý |
|---------|-------------|
| Loading States | Skeleton, Spinner, Progress bar |
| Error States | Toast, Modal, Inline error |
| Empty States | Illustration + Call-to-action |
| Accessibility | Color contrast, ARIA, Keyboard nav |
| Mobile | Responsive, Touch-friendly |
| Dark Mode | Dual theme design |

### 🚀 Khi deploy (`/deploy`)
| Điểm mù | AI tự xử lý |
|---------|-------------|
| SEO | Meta tags, Sitemap, robots.txt |
| Analytics | Google Analytics / Plausible |
| Legal | Privacy Policy, Terms, Cookie consent |
| Backup | Database backup strategy |
| Monitoring | Uptime + Error tracking |
| SSL | Auto HTTPS |
| Maintenance | Maintenance mode page |

### 📚 Khi lưu trữ (`/save-brain`)
| Điểm mù | AI tự tạo |
|---------|-----------|
| API Documentation | Auto-generate từ routes |
| Changelog | Version history |
| Business Rules | Quy tắc nghiệp vụ |
| **Structured Context** | `.brain/brain.json` ⭐ NEW |

---

## 🚀 AWF 4.0 - TÍNH NĂNG MỚI

### 1️⃣ Deep Interview (3 Câu Hỏi Vàng)
Trước khi đề xuất, AI hỏi 3 câu cốt lõi:
- Quản lý GÌ?
- AI dùng?
- Điều gì QUAN TRỌNG NHẤT?

→ Giúp AI hiểu đúng từ đầu, tránh làm sai rồi sửa.

### 2️⃣ Lazy Checkpoint (Tiết kiệm tokens)
```
.brain/
├── session.json        # Update mỗi PHASE (~450 tokens)
└── session_log.txt     # Append mỗi TASK (~20 tokens)
```
→ Giảm 80% token overhead so với rewrite JSON mỗi task.

### 3️⃣ Proactive Handover
Khi context > 80% đầy:
- AI tự tạo Handover Document
- Lưu vào `.brain/handover.md`
- Session sau gõ `/recap` để resume ngay

→ KHÔNG BAO GIỜ mất context giữa sessions.

### 4️⃣ Step Confirmation Protocol
Sau mỗi milestone, hiển thị:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ĐÃ XONG: [Task name]
📊 Tiến độ: ████████░░ 80%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Tiếp? (y/điều chỉnh/dừng)
```
→ User luôn biết đang ở đâu, không bị "mất kiểm soát".

### 5️⃣ Agent Personas (BMAD-Inspired)
| Workflow | Persona | Tính cách |
|----------|---------|-----------|
| `/plan` | Hà (PM) | Lắng nghe, đề xuất options |
| `/design` | Minh (Architect) | Giải thích kỹ thuật đơn giản |
| `/code` | Tuấn (Senior Dev) | Cẩn thận, kiểm tra kỹ |
| `/visualize` | Mai (UX Designer) | Visual, dùng ví dụ |
| `/debug` | Long (Detective) | Điềm tĩnh, có phương pháp |
| `/audit` | Khang (Bác sĩ Code) | Không gây hoang mang |

---

## 🧠 Structured Context - v4.0 (Tách brain + session)

### Vấn đề v3.2
- `brain.json` chứa cả static và dynamic data
- Mỗi lần save phải update toàn bộ file
- Session state lẫn với project knowledge

### Giải pháp v4.0: Tách thành 2 files
```
.brain/                            # LOCAL (per-project)
├── brain.json                     # 🧠 Static knowledge (ít thay đổi)
├── session.json                   # 📍 Dynamic session (thay đổi liên tục)
└── preferences.json               # ⚙️ Local override (nếu khác global)

~/.gemini/antigravity/             # GLOBAL (tất cả dự án)
├── preferences.json               # Default AI preferences
└── defaults/                      # Templates

# Legacy fallback:
~/.antigravity/                    # GLOBAL (legacy)
├── preferences.json               # Default AI preferences
└── defaults/                      # Templates
```

### Lợi ích
| Metric | v3.2 | v4.0 |
|--------|------|------|
| Files để scan | 1 (brain.json) | 2 (brain + session) |
| Token usage | ~3KB | ~3KB (tương đương) |
| Update frequency | Mỗi lần save | brain: khi project thay đổi, session: liên tục |
| Scope | Local only | Local + Global preferences |

### Workflow
```
/save-brain → Update brain.json (nếu cần) + session.json (luôn)
/recap → Load preferences → brain.json → session.json → Summary
/customize → Save preferences (local/global/cả hai)
```

### Schema files
- `schemas/brain.schema.json` - Project knowledge
- `schemas/session.schema.json` - Session state ⭐ NEW
- `schemas/preferences.schema.json` - User preferences ⭐ NEW

### Template files
- `templates/brain.example.json`
- `templates/session.example.json` ⭐ NEW
- `templates/preferences.example.json` ⭐ NEW

### brain.json (Static - ít thay đổi)
- `project`: Tên, loại, status
- `tech_stack`: Frontend, Backend, DB, Dependencies
- `database_schema`: Tables, Relationships
- `api_endpoints`: Routes với auth info
- `business_rules`: Quy tắc nghiệp vụ
- `features`: Tính năng và trạng thái
- `knowledge_items`: Patterns, Gotchas, Conventions

### session.json (Dynamic - thay đổi liên tục) ⭐ NEW
- `working_on`: Feature, task, status, files đang sửa
- `pending_tasks`: Việc cần làm tiếp
- `recent_changes`: Thay đổi gần đây
- `errors_encountered`: Lỗi gặp và cách fix
- `decisions_made`: Quyết định đã lấy trong session

### preferences.json (User settings) ⭐ NEW
- `communication`: Tone, persona
- `technical`: Detail level, autonomy, quality
- `working_style`: Pace, feedback style
- `custom_rules`: Quy tắc riêng của user

---

## 🛡️ Resilience Patterns - v4.0 (Ẩn khỏi User)

> **Nguyên tắc:** User không cần biết về retry, timeout, fallback. AI xử lý ngầm.

### Auto-Retry (Ẩn)
```
Khi gặp lỗi transient (network, rate limit):
1. Retry lần 1 (đợi 1s)
2. Retry lần 2 (đợi 2s)
3. Retry lần 3 (đợi 4s)
4. Nếu vẫn fail → Báo user bằng tiếng đơn giản
```

### Timeout Protection (Ẩn)
```
Mỗi task có timeout mặc định:
- /code: 5 phút
- /deploy: 10 phút
- /debug: 5 phút
- Khác: 3 phút

Khi timeout → "Việc này đang lâu quá, anh muốn tiếp tục không?"
```

### Fallback Conversation (Hiển thị khi cần)
```
Thay vì syntax phức tạp như: /deploy production || staging

AI hỏi bằng tiếng Việt:
"Deploy lên production không được 😅
 Anh muốn thử staging trước không?
 1️⃣ Có - Deploy staging
 2️⃣ Không - Em xem lại lỗi"
```

### Error Messages (Đơn giản hóa)
```
❌ Cũ: "Error: ECONNREFUSED 127.0.0.1:5432 - Connection refused"

✅ Mới: "Không kết nối được database 😅
        Anh kiểm tra xem PostgreSQL đang chạy chưa nhé!
        Gõ /debug nếu cần em hỗ trợ."
```

### Error Categories
| Loại lỗi | AI xử lý | User thấy |
|----------|----------|-----------|
| Network timeout | Auto-retry 3x | Không thấy gì (nếu thành công) |
| Rate limit | Đợi và retry | "Đang chờ API..." |
| Auth failed | Báo ngay | "Cần kiểm tra lại credentials" |
| Code syntax | Gợi ý fix | "Có lỗi ở file X, gõ /debug" |
| Build failed | Phân tích log | "Build lỗi vì Y, em đề xuất..." |

---

## 🎮 Luồng làm việc khuyến nghị

### 📦 Dự án mới
```
/init → /plan → /visualize → /code → /run → /test → /deploy → /save-brain
```

### 🌅 Bắt đầu ngày mới
```
/recap → /code → /run → /test → /save-brain
```

### 🐛 Khi gặp lỗi
```
/debug → /test → (nếu loạn) /rollback
```

### 🚀 Trước release
```
/audit → /test → /deploy → /save-brain
```

---

## 📊 Thống kê hệ thống v4.0

| Workflow | Size | Chất lượng |
|----------|------|------------|
| `/plan` | **5.4KB** | ⭐⭐⭐⭐⭐ Ultimate |
| `/deploy` | **5.3KB** | ⭐⭐⭐⭐⭐ Ultimate |
| `/init` | 4.9KB | ⭐⭐⭐⭐⭐ Complete |
| `/visualize` | 4.8KB | ⭐⭐⭐⭐⭐ Complete |
| `/debug` | 4.7KB | ⭐⭐⭐⭐⭐ Complete |

| `/save-brain` | **4.2KB** | ⭐⭐⭐⭐⭐ Ultimate |
| `/audit` | 4.2KB | ⭐⭐⭐⭐⭐ Complete |
| `/refactor` | 4.2KB | ⭐⭐⭐⭐⭐ Complete |
| `/code` | 3.6KB | ⭐⭐⭐⭐⭐ Complete |
| `/run` | 2.6KB | ⭐⭐⭐⭐ Good |
| `/test` | 2.4KB | ⭐⭐⭐⭐ Good |
| `/recap` | 2.4KB | ⭐⭐⭐⭐ Good |
| `/rollback` | 2.2KB | ⭐⭐⭐⭐ Good |

**Tổng:** 19 workflows | **~55KB** instructions | **50+ điểm mù** được xử lý

---

## 💡 Tips cho Vibe Coder

1. **Cứ nói tự nhiên** - AI sẽ hỏi lại nếu thiếu
2. **Không sợ làm sai** - Có `/rollback`
3. **Cuối ngày `/save-brain`** - Mai không mất context
4. **Định kỳ `/audit`** - Phòng bệnh hơn chữa bệnh
5. **Trước release `/deploy`** - SEO, Analytics, Legal đầy đủ

---

*Antigravity Vibe Coding Suite v4.0 - Your dreams, our engineering.*
