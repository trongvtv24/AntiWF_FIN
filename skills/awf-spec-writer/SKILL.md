---
name: awf-spec-writer
description: >
  Bắt AI viết Specification rõ ràng TRƯỚC KHI code. Kích hoạt khi bắt đầu tính năng mới,
  yêu cầu mơ hồ, thay đổi lớn, hoặc khi user dùng /plan để thiết kế tính năng.
  Ngăn AI làm sai từ đầu bằng cách surface assumptions và yêu cầu human review từng phase.
  Keywords: spec, specification, viết spec, requirements, trước khi code, plan feature.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-spec-writer"
skill_version: "1.0.0"
status: active
category: "planning"
activation: "conditional"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "write_spec_after_request"
requires_confirmation: false
related_workflows:
  - "/plan"
  - "/code"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Spec Writer — Viết Spec Trước, Code Sau

## Tổng quan
Viết spec có cấu trúc **TRƯỚC KHI** viết bất kỳ dòng code nào.
Spec là nguồn sự thật được chia sẻ giữa AI và người dùng — nó định nghĩa **cái gì** cần build, **tại sao**, và **làm sao biết xong**.

> 💡 **Triết lý:** Code không có spec = đoán mò. 15 phút làm spec ngăn được 15 giờ sửa lỗi.

---

## Khi nào kích hoạt

✅ **NÊN dùng:**
- Bắt đầu project mới hoặc tính năng mới
- Yêu cầu mơ hồ hoặc chưa đầy đủ
- Thay đổi chạm nhiều file hoặc nhiều module
- Chuẩn bị ra quyết định kiến trúc
- Task ước tính > 30 phút để implement

❌ **KHÔNG cần dùng:**
- Sửa 1 dòng, sửa typo
- Yêu cầu hoàn toàn rõ ràng và tự chứa

---

## Quy trình 4 Phase (Gated — Không được bỏ qua)

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

**Quy tắc:** Không được tiến sang phase tiếp theo khi chưa có human review & approve.

---

## Phase 1: SPECIFY — Làm rõ yêu cầu

### Bước 1A: Surface Assumptions (Bắt buộc)
Trước khi viết bất cứ gì, liệt kê những gì đang giả định:

```
📋 NHỮNG GÌ EM ĐANG GIẢ ĐỊNH:
1. Đây là web application (không phải mobile app)
2. Authentication dùng session-based cookies (không phải JWT)
3. Database là PostgreSQL (dựa trên schema hiện có)
4. Target modern browsers (không cần IE11)

→ Anh có thể xác nhận hoặc điều chỉnh trước khi em tiếp tục không?
```

> ⚠️ KHÔNG tự điền vào yêu cầu mơ hồ. Mục đích của spec là surface misunderstandings TRƯỚC KHI code.

### Bước 1B: Yêu cầu làm rõ (3 câu hỏi vàng)
Trước khi viết spec, hỏi tối đa 3 câu hỏi cốt lõi nhất:
1. Tính năng này phục vụ ai / use case cụ thể là gì?
2. Điều gì là quan trọng nhất / thứ tự ưu tiên?
3. Có ràng buộc kỹ thuật hoặc business nào cần biết không?

### Bước 1C: Viết Spec Document

```markdown
# Spec: [Tên tính năng]

## Mục tiêu
[Chúng ta đang build gì và tại sao. User stories hoặc acceptance criteria.]

## Tech Stack
[Framework, ngôn ngữ, dependencies chính với phiên bản]

## Commands
[Build, test, lint, dev — lệnh đầy đủ]
Ví dụ:
- Dev: npm run dev
- Test: npm test -- --coverage
- Build: npm run build

## Cấu trúc Project
[Sơ đồ thư mục với mô tả]

## Code Style
[1 snippet ví dụ code đúng chuẩn + quy tắc đặt tên]

## Testing Strategy
[Framework, nơi test, coverage expectations]

## Boundaries (Không được vi phạm)
- Luôn làm: [...]
- Hỏi trước: [...] (ví dụ: thay đổi schema DB, thêm dependency)
- Không bao giờ: [...] (ví dụ: commit secrets, xóa test đang fail)

## Success Criteria (Tiêu chí hoàn thành)
[Điều kiện cụ thể, có thể test được để xác nhận xong]

## Open Questions
[Vấn đề chưa giải quyết cần human input]
```

### Reframe yêu cầu mơ hồ thành Success Criteria:

```
YÊU CẦU: "Làm dashboard nhanh hơn"

REFRAMED THÀNH TIÊU CHÍ CỤ THỂ:
- Dashboard LCP < 2.5s trên kết nối 4G
- Initial data load hoàn thành trong < 500ms
- Không có layout shift khi load (CLS < 0.1)

→ Đây có phải target đúng không, anh xác nhận giúp em?
```

---

## Phase 2: PLAN — Kế hoạch triển khai kỹ thuật

Sau khi spec được approve, tạo technical implementation plan:
1. Xác định các component chính và dependencies
2. Xác định thứ tự implementation (cái gì phải làm trước)
3. Ghi chú rủi ro và biện pháp giảm thiểu
4. Xác định cái gì build song song được, cái gì phải tuần tự
5. Định nghĩa verification checkpoints giữa các phase

---

## Phase 3: TASKS — Chia nhỏ thành việc cụ thể

Mỗi task phải đáp ứng:
- Hoàn thành được trong 1 session tập trung
- Có acceptance criteria rõ ràng
- Có verification step (test, build, manual check)
- Được sắp xếp theo dependency, không phải theo importance
- Không thay đổi quá ~5 files

**Task template:**
```markdown
- [ ] Task: [Mô tả]
  - Acceptance: [Điều gì phải đúng khi xong]
  - Verify: [Cách xác nhận — lệnh test, build, manual check]
  - Files: [Các file sẽ được chạm]
```

---

## Phase 4: IMPLEMENT — Thực hiện

Thực hiện từng task theo `karpathy-coding-principles`:
- Surgical changes — chỉ sửa đúng chỗ cần
- Verify sau mỗi task trước khi sang task tiếp theo
- Cập nhật spec khi có quyết định thay đổi

---

## Giữ Spec "Sống"

Spec không phải artifact một lần — nó là tài liệu sống:

- ✏️ **Update khi quyết định thay đổi** — Thay đổi data model? Cập nhật spec trước, rồi implement
- 📦 **Commit spec cùng code** — Spec thuộc về version control
- 🔗 **Reference spec trong PRs** — Link đến section spec mà PR implement
- 🗑️ **Update khi scope thay đổi** — Tính năng thêm/bớt phải phản ánh trong spec

---

## ⚠️ Anti-Rationalization (Lý do bỏ qua spec — và tại sao sai)

| Lý do bỏ qua | Thực tế |
|---|---|
| "Cái này đơn giản, cần gì spec" | Task đơn giản không cần spec *dài*, nhưng vẫn cần acceptance criteria. Spec 2 dòng vẫn tốt hơn không có gì. |
| "Sẽ viết spec sau khi code xong" | Đó là documentation, không phải specification. Giá trị của spec là buộc làm rõ TRƯỚC khi code. |
| "Spec làm tốn thời gian" | 15 phút làm spec ngăn được hàng giờ refactor. |
| "Yêu cầu sẽ thay đổi anyway" | Đó lý do spec là tài liệu sống. Spec cũ hơn vẫn tốt hơn không spec. |
| "User biết họ muốn gì rồi" | Kể cả yêu cầu rõ ràng cũng có hidden assumptions. Spec surface những assumptions đó. |

---

## 🚩 Red Flags (Dấu hiệu đang làm sai)

- Bắt đầu viết code mà chưa có requirements bằng văn bản
- Hỏi "Em cứ bắt đầu build luôn nhé?" trước khi làm rõ "done" nghĩa là gì
- Implement tính năng không có trong bất kỳ spec hoặc task list nào
- Ra quyết định kiến trúc mà không document lại
- Bỏ qua spec vì "rõ ràng là phải build thế này"

---

## ✅ Verification Checklist

Trước khi chuyển sang implementation, xác nhận:

- [ ] Spec đã cover đủ 6 mục cốt lõi (Objective, Commands, Structure, Style, Testing, Boundaries)
- [ ] Human đã review và approve spec
- [ ] Success criteria cụ thể và có thể test được
- [ ] Boundaries (Always/Ask First/Never) đã định nghĩa
- [ ] Spec đã được lưu vào file trong repo (hoặc `.brain/`)
