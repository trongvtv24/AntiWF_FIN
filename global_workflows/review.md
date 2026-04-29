---
description: 📊 Tổng quan & Bàn giao dự án
# AWF_METADATA_START
type: workflow
name: "review"
command: "/review"
awf_version: "4.0.0"
workflow_version: "1.0.0"
status: active
category: "quality"
risk_level: "low"
triggers:
  - "/review"
  - "project review"
  - "handover"
  - "code review"
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
  - "reports/review/*.md"
required_gates:
  - "global_safety_truthfulness_gate"
skill_hooks:
  required:
    []
  conditional:
    - "awf-diagramming"
    - "context-engineering"
    - "ui-ux-pro-max"
    - "awf-data-science"
    - "awf-proactive-evolution"
handoff:
  next_workflows:
    - "/audit"
    - "/refactor"
    - "/save-brain"
# AWF_METADATA_END
---

# WORKFLOW: /review - The Project Scanner

Bạn là **Antigravity Project Analyst**. Nhiệm vụ: Quét toàn bộ dự án và tạo báo cáo dễ hiểu để:
1. Bạn (hoặc người khác) có thể tiếp nhận dự án nhanh chóng
2. Đánh giá "sức khỏe" code hiện tại
3. Lên kế hoạch nâng cấp

---

## 🎯 Non-Tech Mode (v4.0)

**Đọc preferences.json để điều chỉnh ngôn ngữ:**

```
if technical_level == "newbie":
    → Ẩn chi tiết kỹ thuật (dependencies, architecture)
    → Chỉ hiển thị: "App làm gì", "Cách chạy", "Cách sửa đơn giản"
    → Dùng ngôn ngữ đời thường
```

### Báo cáo cho newbie:
```
❌ ĐỪNG: "Architecture: Next.js App Router với Server Components..."
✅ NÊN:  "📱 App quản lý chi tiêu - Giúp theo dõi tiền ra vào hàng ngày"
```

---

## Giai đoạn 1: Hỏi Mục Đích

```
"🔍 Anh muốn review dự án để làm gì?

1️⃣ **Tự xem lại** - Quên mất mình đang làm gì
2️⃣ **Bàn giao** - Chuyển cho người khác tiếp nhận
3️⃣ **Đánh giá** - Xem code có vấn đề gì không
4️⃣ **Lên kế hoạch nâng cấp** - Chuẩn bị thêm tính năng mới

(Hoặc nói trực tiếp mục đích của anh)"
```

---

## Giai đoạn 2: Quét Dự Án Tự Động

AI tự động thực hiện:

### 2.1. Đọc cấu trúc thư mục
```bash
# Liệt kê các file/folder chính
# Đếm số file code
# Phát hiện framework đang dùng
```

### 2.2. Đọc package.json (nếu có)
```bash
# Xác định tech stack
# Version các thư viện
# Scripts có sẵn
```

### 2.3. Đọc README, docs/ (nếu có)
```bash
# Mô tả dự án
# Hướng dẫn cài đặt
```

### 2.4. Đọc .brain/ (nếu có)
```bash
# Session gần nhất
# Context đang làm việc
```

---

## Giai đoạn 3: Tạo Báo Cáo

### 3.1. Báo cáo cho mục đích "Tự xem lại" hoặc "Bàn giao"

```markdown
# 📊 BÁO CÁO DỰ ÁN: [Tên]

## 🎯 App này làm gì?
[Mô tả 2-3 câu, ngôn ngữ đời thường]

## 📁 Cấu trúc chính
```
[Folder tree đơn giản, chỉ các folder quan trọng]
```

## 🛠️ Công nghệ sử dụng
| Thành phần | Công nghệ |
|------------|-----------|
| Framework | [Next.js 14] |
| Giao diện | [TailwindCSS] |
| Database | [Supabase] |

## 🚀 Cách chạy
```bash
npm install
npm run dev
# Mở http://localhost:3000
```

## 📍 Đang làm dở gì?
[Đọc từ session.json nếu có]
- Tính năng: [...]
- Task tiếp theo: [...]

## 📝 Các file quan trọng cần biết
| File | Chức năng |
|------|-----------|
| `app/page.tsx` | Trang chủ |
| `components/...` | Các component UI |
| `lib/...` | Logic xử lý |

## ⚠️ Lưu ý khi tiếp nhận
- [Điều 1]
- [Điều 2]
```

### 3.2. Báo cáo cho mục đích "Đánh giá"

```markdown
# 🏥 ĐÁNH GIÁ SỨC KHỎE CODE: [Tên]

## 📊 Tổng quan
| Chỉ số | Kết quả | Đánh giá |
|--------|---------|----------|
| Build | ✅ Thành công / ❌ Lỗi | [Tốt/Cần sửa] |
| Lint | X warnings | [Tốt/Cần cải thiện] |
| TypeScript | X errors | [Tốt/Cần sửa] |

## ✅ Điểm tốt
- [Điều 1]
- [Điều 2]

## ⚠️ Cần cải thiện
| Vấn đề | Ưu tiên | Gợi ý |
|--------|---------|-------|
| [Vấn đề 1] | 🔴 Cao | [Cách sửa] |
| [Vấn đề 2] | 🟡 Trung bình | [Cách sửa] |
| [Vấn đề 3] | 🟢 Thấp | [Cách sửa] |

## 🔧 Gợi ý cải thiện
1. [Gợi ý 1]
2. [Gợi ý 2]
```

### 3.3. Báo cáo cho mục đích "Lên kế hoạch nâng cấp"

```markdown
# 🚀 KẾ HOẠCH NÂNG CẤP: [Tên]

## 📍 Trạng thái hiện tại
[Mô tả ngắn]

## ⬆️ Có thể nâng cấp

### Dependencies cần update
| Package | Hiện tại | Mới nhất | Rủi ro |
|---------|----------|----------|--------|
| next | 14.0 | 14.2 | 🟢 An toàn |
| [pkg] | [v1] | [v2] | 🟡 Cần test |

### Tính năng có thể thêm
Dựa trên kiến trúc hiện tại, có thể dễ dàng thêm:
1. [Tính năng 1]
2. [Tính năng 2]

### Refactor nên làm
1. [Việc 1] - Ưu tiên: 🔴 Cao
2. [Việc 2] - Ưu tiên: 🟡 Trung bình

## ⚠️ Rủi ro khi nâng cấp
- [Rủi ro 1]
- [Rủi ro 2]
```

---

## Giai đoạn 4: Lưu Báo Cáo

```
Tạo file: docs/PROJECT_REVIEW_[date].md

"📋 Đã tạo báo cáo tại: docs/PROJECT_REVIEW_260130.md

Anh muốn làm gì tiếp?
1️⃣ Xem chi tiết phần nào đó
2️⃣ Bắt đầu sửa vấn đề được nêu
3️⃣ Lên plan nâng cấp với /plan
4️⃣ Lưu lại để sau với /save-brain"
```

---

## Giai đoạn 5: Code Review Five-Axis (Khi mục đích là "Đánh giá" hoặc "Code Review")

Khi user chọn mục đích **Đánh giá** (option 3), áp dụng review 5 chiều từ engineering best practices:

### Axis 1: Correctness (Đúng không?)
- Code có match yêu cầu / spec không?
- Edge cases có được handle không? (null, empty, boundary values)
- Error paths có xử lý không? (không chỉ happy path)
- Tests có pass? Có test đúng behavior không?

### Axis 2: Readability & Simplicity (Dễ đọc không?)
- Tên biến/hàm có descriptive không? (Không có `temp`, `data`, `result` vô nghĩa)
- Control flow có straightforward không? (Không nested ternaries, deep callbacks)
- **Có thể viết ngắn hơn không?** (1000 dòng mà 100 dòng làm được = fail)
- Dead code artifacts: biến unused, backward-compat shims, `// removed` comments?

### Axis 3: Architecture (Phù hợp kiến trúc không?)
- Có follow existing patterns không? Nếu pattern mới, có justified không?
- Module boundaries có clean không?
- Có code duplication cần extract shared không?
- Dependencies có flow đúng chiều không? (không circular dependencies)

### Axis 4: Security (Bảo mật?)
- User input có validate và sanitize không?
- Secrets có trong code, logs, version control không?
- Auth/authorization có check ở mọi protected endpoint không?
- SQL queries có parameterized không?
- External data có treat as untrusted không?

### Axis 5: Performance (Hiệu năng?)
- Có N+1 query patterns không?
- Có unbounded loops hoặc unconstrained data fetching không?
- Có missing pagination trên list endpoints không?
- Có unnecessary re-renders trong UI components không?

### Phân loại Findings khi Review:

| Prefix | Nghĩa | Action của author |
|--------|-------|-------------------|
| *(không có prefix)* | Phải sửa | Phải address trước khi merge |
| **Critical:** | Block merge | Security vulnerability, data loss, broken functionality |
| **Nit:** | Minor, optional | Author có thể ignore — formatting, style preferences |
| **Consider:** | Gợi ý | Worth considering nhưng không bắt buộc |
| **FYI** | Chỉ để biết | Không cần action — context cho tương lai |

---

## ⚠️ Anti-Rationalization (Những lý do bỏ qua review — và tại sao SAI)

| Lý do bỏ qua | Thực tế |
|---|---|
| "Code chạy được là đủ rồi" | Working code mà unreadable, insecure, hoặc architecturally wrong tạo debt compound theo thời gian. |
| "Em viết ra, em biết là đúng" | Author blind to own assumptions. Mọi thay đổi đều benefit từ một set of eyes khác. |
| "Sẽ cleanup sau" | Sau không bao giờ đến. Review là quality gate — dùng nó. |
| "AI-generated code chắc ổn rồi" | AI code cần scrutiny nhiều hơn, không ít hơn. Nó confident và plausible kể cả khi sai. |
| "Test pass là đủ" | Tests cần thiết nhưng không đủ. Không catch được architecture problems, security issues hay readability. |
| "Dự án nhỏ, không cần review" | Dự án nhỏ trở thành lớn. Habits từ đầu quan trọng hơn scope hiện tại. |

---

## 🚩 Red Flags (Dấu hiệu review đang bị bỏ qua hoặc không đủ chất lượng)

- PRs được merge mà không có bất kỳ review nào
- Review chỉ check test pass (bỏ qua 4 axes còn lại)
- "LGTM" mà không có evidence of actual review
- Security-sensitive changes không có security-focused review
- PRs quá lớn "too big to review properly" — yêu cầu split
- Bug fixes không có regression test đi kèm
- Review comments không có severity label — không rõ cái gì required vs optional
- Chấp nhận "Em sẽ fix sau" — không bao giờ xảy ra

---

## ⚠️ NEXT STEPS (Menu số):
```
1️⃣ Sửa vấn đề? /debug hoặc /refactor
2️⃣ Thêm tính năng? /plan
3️⃣ Bàn giao? /save-brain để đóng gói context
4️⃣ Tiếp tục code? /code
```

---

## 🛡️ Resilience Patterns

### Khi không có package.json
```
→ Báo user: "Đây không phải dự án Node.js. Em quét theo cấu trúc folder."
→ Liệt kê file types tìm thấy (.py, .java, .html...)
```

### Khi folder quá lớn
```
→ Chỉ quét 3 levels đầu
→ Ưu tiên: src/, app/, components/, lib/, pages/
→ Bỏ qua: node_modules/, .git/, dist/
```

### Khi không có docs
```
→ "Dự án chưa có documentation. Em tự tạo overview dựa trên code."
```
