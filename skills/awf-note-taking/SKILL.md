---
name: awf-note-taking
description: >
  Personal Knowledge Management (PKM) — capture atomic notes, link concepts, build second brain.
  Lưu insights, learnings, decisions và knowledge vào hệ thống có structure thay vì để mất.
  Tích hợp với Obsidian-style linking. Kích hoạt khi user muốn ghi chú, lưu learnings,
  build knowledge base, hoặc cuối một session quan trọng.
  Keywords: ghi chú, note, PKM, second brain, obsidian, knowledge base, lưu lại, capture insight,
  atomic note, zettelkasten, learning log.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-note-taking"
skill_version: "1.0.0"
status: active
category: "context"
activation: "explicit_or_confirmed"
priority: "low"
risk_level: "medium"
allowed_side_effects:
  - "write_note_after_confirmation"
requires_confirmation: true
related_workflows:
  - "/save-brain"
  - "/review"
  - "/recap"
required_gates:
  - "global_safety_truthfulness_gate"
  - "context_system"
# AWF_METADATA_END
---

# AWF Note-Taking — Second Brain Cho Antigravity

## Tổng quan
Insight không được ghi lại = insight bị mất. Mỗi research session, decision, hoặc lesson learned
cần được capture vào hệ thống có structure để có thể tìm lại và build on sau này.

> 💡 **Triết lý:** Ghi lại không phải để nhớ — mà để **suy nghĩ rõ hơn** và **kết nối ý tưởng** sau này.

---

## Context System Boundary (AWF 4.0)

Skill này không còn là writer tự do cho memory dự án.

- Chỉ ghi note khi user xác nhận rõ ràng.
- Project decisions phải đi vào `.brain/decisions.md` hoặc ADR theo format đã nêu.
- Claim, số liệu, nguồn, assumption phải đi vào `.brain/claims.md` nếu chưa kiểm chứng.
- Không ghi đè `.brain/brain.json` hoặc `.brain/session.json`; việc đó thuộc `/save-brain`.
- Khi note lấy từ nguồn ngoài, phải ghi `Source` và trạng thái kiểm chứng.

---

## Khi nào kích hoạt

✅ **Tự động trigger:**
- Cuối session `/research` → offer capture key findings
- Sau `awf-idea-refine` → offer save refined concept
- Sau `/design` → save ADRs (Architecture Decision Records)
- Khi user nói: "ghi lại cái này", "lưu lại", "note lại", "nhớ cái này nhé"
- Khi user học được điều gì quan trọng trong conversation

---

## 3 Loại Notes

### 1. Atomic Notes (Fleeting → Permanent)
Ý tưởng đơn lẻ, một concept, một insight.

```markdown
---
type: atomic-note
topic: [Chủ đề]
date: 2026-04-13
links: [[concept-A]], [[concept-B]]
---

# [Tên concept ngắn gọn]

[Mô tả bằng lời của mình, không copy-paste. 3-5 câu max.]

## Tại sao quan trọng
[Context — tại sao note này matter?]

## Connections
- Liên quan đến: [[note-khác]]
- Contradict với: [[note-khác]]
- Builds on: [[note-khác]]

## Source
[Từ đâu? Conversation nào? URL nào?]
```

### 2. Project Notes (Working notes)
Theo dõi progress, decisions, blockers của một project cụ thể.

```markdown
---
type: project-note
project: [Tên project]
date: 2026-04-13
status: active | paused | done
---

# [Project Name] — Working Notes

## Mục tiêu
[1-2 câu về project này làm gì]

## Decisions Log
| Date | Decision | Lý do | Alternatives rejected |
|------|---------|-------|----------------------|
| ... | ... | ... | ... |

## Open Questions
- [ ] [Câu hỏi chưa có câu trả lời]

## Lessons Learned
- [Điều learn được trong quá trình làm]

## Next Actions
- [ ] [Action cụ thể]
```

### 3. Reference Notes (External knowledge)
Tóm tắt books, articles, repos, conversations quan trọng.

```markdown
---
type: reference
source: [Book/Article/Repo/Video]
author: [Tác giả]
date-read: 2026-04-13
rating: ⭐⭐⭐⭐⭐
---

# [Tên source]

## Idea chính (bằng lời của mình)
[Không phải summary — là mình rút ra được gì]

## Quotes / Excerpts đáng nhớ
> "[Quote]" — [Context]

## Ứng dụng được vào
[Cách áp dụng vào công việc/project hiện tại]

## Connections
- [[concept-liên-quan]]
```

---

## Capture Workflow

### Khi session đang chạy (Live capture)
```
1. Note key insights ngay khi phát sinh — đừng để "ghi sau"
2. Format: [Keyword]: [Insight ngắn gọn]
   Ví dụ: "Performance: N+1 query là nguồn gốc của 80% perf issues trong app này"
3. Tag với context: #decision #insight #blocker #learning
```

### Cuối session (Consolidation)
AI sẽ tự động:
```
"📝 Session này có vài điểm đáng lưu lại:
1. [Insight 1 từ session]
2. [Decision được đưa ra]
3. [Open question chưa giải quyết]

Anh muốn em lưu vào knowledge base không? (y/n)
Lưu vào: docs/notes/[topic]/[date].md"
```

---

## Folder Structure Gợi ý

```
docs/
├── notes/
│   ├── inbox/          # Fleeting notes chưa processed
│   ├── concepts/       # Atomic notes về concepts
│   ├── projects/       # Working notes theo project
│   ├── references/     # Book/article summaries
│   └── decisions/      # ADRs (Architecture Decision Records)
├── daily/              # Daily notes (optional)
└── index.md            # Map of content — entry point
```

---

## ADR Template (Architecture Decision Records)

Dùng khi có decision quan trọng về tech/architecture trong `/design` hoặc `/code`:

```markdown
# ADR-[number]: [Tên quyết định]

**Date:** 2026-04-13
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-X
**Deciders:** [Ai tham gia quyết định]

## Context
[Tình huống dẫn đến phải ra quyết định này]

## Decision
[Chúng ta chọn gì]

## Rationale
[Tại sao chọn cái này]

## Alternatives Considered
| Option | Pros | Cons | Lý do reject |
|--------|------|------|-------------|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |

## Consequences
- ✅ [Lợi ích]
- ⚠️ [Trade-off phải chấp nhận]
- ❌ [Điều phải từ bỏ]
```

---

## Tích hợp với AWF

| Workflow/Skill | Note-taking tích hợp như thế nào |
|---------------|----------------------------------|
| `/design` | Auto-offer save ADR sau mỗi architectural decision |
| `/research` + `awf-research-agent` | Auto-capture key findings vào reference notes |
| `awf-idea-refine` | Save refined concept vào atomic notes |
| `/save-brain` | Tổng hợp session notes vào knowledge base chuẩn |
| `/recap` | Pull từ saved notes để restore context nhanh hơn |

---

## 🚩 Red Flags

- Ghi note nhưng không đọc lại bao giờ → knowledge graveyard
- Notes quá dài, mỗi note nhìn như một essay → không atomic
- Không có connections/links giữa các notes → isolated knowledge, không compound
- Copy-paste không diễn đạt lại bằng lời mình → không thực sự học
- Không có inbox processing workflow → notes tích đống không xử lý
