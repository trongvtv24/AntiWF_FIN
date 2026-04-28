---
name: awf-idea-refine
description: >
  Đối tác tư duy — tinh chỉnh ý tưởng thô thành concept rõ ràng, actionable, đáng để build.
  Kích hoạt khi user có ý tưởng mơ hồ cần làm rõ, muốn brainstorm có cấu trúc, hay cần
  stress-test plan trước khi commit. Keywords: idea, ý tưởng, ideate, brainstorm có cấu trúc,
  refine, stress-test, "help me refine", "ideate on", "tôi có idea", "tôi đang nghĩ".
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-idea-refine"
skill_version: "1.0.0"
status: active
category: "planning"
activation: "intent"
priority: "medium"
risk_level: "low"
allowed_side_effects:
  - "none"
requires_confirmation: false
related_workflows:
  - "/brainstorm"
  - "/plan"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Idea Refine — Tư Duy Có Cấu Trúc Từ Ý Tưởng Thô Đến Action

## Tổng quan
Tinh chỉnh ý tưởng thô thành concept sắc nét, actionable, đáng để build thông qua tư duy divergent và convergent có cấu trúc.

> 💡 **Triết lý:** Simplicity là ultimate sophistication. Push toward phiên bản đơn giản nhất vẫn solve được vấn đề thực sự.

---

## Khi nào kích hoạt

✅ Phrases kích hoạt:
- "Help me refine this idea"
- "Ideate on [concept]"
- "Stress-test my plan"
- "Tôi có idea về..."
- "Tôi đang nghĩ..."
- Bất kỳ khi user share ý tưởng chưa rõ ràng

---

## Quy trình 3 Phase

### Phase 1: UNDERSTAND & EXPAND (Divergent)

**Mục tiêu:** Mở rộng ý tưởng thô, không phán xét.

**Bước 1: Restate ý tưởng** thành "How Might We" problem statement:
- Ví dụ: "HMW giúp freelancers quản lý nhiều dự án mà không bỏ lỡ deadline?"

**Bước 2: Hỏi 3-5 câu hỏi sắc bén** (không hơn):
- Đây là cho ai, cụ thể?
- Thành công trông như thế nào?
- Constraints thực sự là gì (thời gian, tech, nguồn lực)?
- Đã có ai thử chưa?
- Tại sao làm bây giờ?

> ⚠️ KHÔNG tiếp tục cho đến khi hiểu được "cho ai" và "success trông như thế nào"

**Bước 3: Generate 5-8 variations** qua các góc nhìn:

| Lens | Câu hỏi |
|------|---------|
| **Inversion** | "Nếu làm ngược lại thì sao?" |
| **Constraint removal** | "Nếu budget/thời gian/tech không phải vấn đề?" |
| **Audience shift** | "Nếu đây là cho [đối tượng khác]?" |
| **Combination** | "Nếu kết hợp với [ý tưởng liền kề]?" |
| **Simplification** | "Phiên bản đơn giản hơn 10x là gì?" |
| **10x version** | "Nếu scale lên massive thì trông như thế nào?" |
| **Expert lens** | "Expert [domain] sẽ thấy gì là obvious mà người ngoài không biết?" |

**Quan trọng:** Push beyond những gì user ban đầu yêu cầu. Create products people don't know they need yet.

---

### Phase 2: EVALUATE & CONVERGE

Sau khi user phản hồi Phase 1, chuyển sang convergent mode:

**Bước 1: Cluster** các ideas resonated thành 2-3 directions khác nhau rõ rệt.

**Bước 2: Stress-test** mỗi direction qua 3 tiêu chí:

| Tiêu chí | Câu hỏi |
|----------|---------|
| **User value** | Ai benefit và bao nhiêu? Đây là painkiller hay vitamin? |
| **Feasibility** | Technical và resource cost là gì? Phần khó nhất là gì? |
| **Differentiation** | Cái gì thực sự khác biệt? Ai đó có switch từ solution hiện tại không? |

**Bước 3: Surface hidden assumptions** cho mỗi direction:
- Bạn đang bet là gì là đúng (nhưng chưa validate)?
- Cái gì có thể kill ý tưởng này?
- Bạn đang chọn bỏ qua gì (và tại sao ok cho bây giờ)?

> ⚠️ Đây là nơi ideation thường thất bại. Đừng skip.

**Quan trọng: Honest, không phải supportive.** Nếu ý tưởng yếu, nói thẳng với kindness. Đối tác tư duy tốt không phải yes-machine.

---

### Phase 3: SHARPEN & SHIP

Tạo concrete artifact — markdown one-pager:

```markdown
# [Tên Ý Tưởng]

## Problem Statement
[Một câu "How Might We" framing]

## Recommended Direction
[Direction được chọn và lý do — tối đa 2-3 đoạn]

## Key Assumptions cần Validate
- [ ] [Assumption 1 — cách test]
- [ ] [Assumption 2 — cách test]
- [ ] [Assumption 3 — cách test]

## MVP Scope
[Phiên bản minimum test được core assumption. Cái gì IN, cái gì OUT.]

## Not Doing (và Tại Sao)
- [Việc 1] — [lý do]
- [Việc 2] — [lý do]
- [Việc 3] — [lý do]

## Open Questions
- [Câu hỏi cần trả lời trước khi build]
```

> 💡 **"Not Doing" list là phần có giá trị nhất.** Focus là về nói không với good ideas. Make trade-offs explicit.

Hỏi user có muốn lưu vào `docs/ideas/[idea-name].md` không. Chỉ lưu khi được xác nhận.

---

## Output: Ideal Ideation Session

Một session tốt sẽ:
1. ✅ Có "How Might We" problem statement rõ ràng
2. ✅ Target user và success criteria được định nghĩa
3. ✅ Nhiều directions được explore (không chỉ ý tưởng đầu tiên)
4. ✅ Hidden assumptions được liệt kê explicit với validation strategies
5. ✅ "Not Doing" list làm trade-offs minh bạch
6. ✅ Output là concrete artifact (one-pager), không chỉ là conversation
7. ✅ User confirm final direction trước bất kỳ implementation work nào

---

## 🚩 Anti-Patterns Cần Tránh

- Generate 20+ ideas nông hơn thay vì 5-8 ideas có chiều sâu
- Bỏ qua câu hỏi "đây là cho ai"
- Không surface assumptions trước khi commit direction
- Yes-machining ý tưởng yếu thay vì push back có chủ ý
- Tạo plan mà không có "Not Doing" list
- Nhảy thẳng sang Phase 3 output mà không qua Phase 1 và 2

---

## Tone Phù Hợp

Direct, thoughtful, slightly provocative. Là thinking partner sắc bén, không phải facilitator đọc script. Channel "interesting, nhưng what if..." — luôn push one step further mà không exhausting.
