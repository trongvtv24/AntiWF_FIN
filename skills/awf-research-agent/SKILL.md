---
name: awf-research-agent
description: >
  Deep research workflow — thu thập, triangulate và tổng hợp thông tin từ nhiều nguồn
  thành báo cáo có cấu trúc, có dẫn chứng rõ ràng. Khác với browse/search thông thường:
  đây là research methodology có hệ thống. Tích hợp tốt với data-scraper-agent và local-coccoc-control.
  Keywords: research, tìm hiểu, khảo sát, phân tích thị trường, báo cáo, investigate, deep dive,
  market research, competitive analysis, fact-check, tổng hợp.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-research-agent"
skill_version: "1.0.0"
status: active
category: "research"
activation: "conditional"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "web_research"
  - "generate_report"
requires_confirmation: false
related_workflows:
  - "/brainstorm"
  - "/plan"
  - "/script"
  - "/fb-post"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Research Agent — Research Có Phương Pháp, Không Phải Browse Ngẫu Nhiên

## Tổng quan
Browse ngẫu nhiên cho bạn thông tin. Research có phương pháp cho bạn **insight**.
Skill này áp dụng framework nghiên cứu học thuật vào context thực tế: business, technology, market.

> 💡 **Triết lý:** Một nguồn = opinion. Hai nguồn = comparison. Ba nguồn+ = pattern.

---

## Khi nào kích hoạt

✅ **Triggers:**
- "Research về...", "Tìm hiểu sâu về...", "Phân tích thị trường..."
- "So sánh X và Y", "Competitive analysis", "Market overview"
- "Fact-check", "Verify", "Kiểm chứng thông tin"
- "Báo cáo về...", "Tổng hợp..."
- Sau khi `/brainstorm` — cần validate assumptions bằng data

---

## 3 Loại Research Task

### Type A: Factual Research (Tìm sự thật)
> "Số liệu thực tế về thị trường X là gì?"

**Process:** Search → Verify across 3+ sources → Extract facts → Note discrepancies

### Type B: Comparative Research (So sánh)
> "X và Y khác nhau thế nào? Cái nào phù hợp hơn cho use case Z?"

**Process:** Define criteria → Research both → Create comparison matrix → Recommend

### Type C: Synthesis Research (Tổng hợp)
> "Landscape của industry X hiện tại ra sao? Xu hướng đang đi đâu?"

**Process:** Broad survey → Cluster findings → Identify patterns → Extract insights → Forecast

---

## Quy trình 5 Bước Chuẩn

### Bước 1: FRAME — Đóng khung vấn đề
Trước khi search bất cứ gì, làm rõ:

```
Research Question: [Một câu hỏi trung tâm cụ thể]
Scope: [Thời gian? Địa lý? Industry segment?]
Output needed: [Báo cáo? Decision support? Quick facts?]
Key uncertainties: [Những gì đang không biết và cần biết nhất?]
```

> ⚠️ Không research rộng → hỏi user câu hỏi trung tâm là gì trước khi bắt đầu.

### Bước 2: SOURCE — Lên kế hoạch nguồn
Xác định nguồn theo tier:

| Tier | Loại nguồn | Độ tin cậy | Ví dụ |
|------|-----------|-----------|-------|
| **Tier 1** | Primary data | ⭐⭐⭐⭐⭐ | Official reports, surveys, raw data |
| **Tier 2** | Expert analysis | ⭐⭐⭐⭐ | Industry analysts (Gartner, McKinsey), peer-reviewed |
| **Tier 3** | Quality journalism | ⭐⭐⭐ | The Economist, FT, Bloomberg, VnExpress Kinh tế |
| **Tier 4** | Practitioner content | ⭐⭐ | Blog từ practitioners (có bias nhưng có insight) |
| **Tier 5** | General web | ⭐ | Dùng để triangulate, không phải cite |

**Rule:** Mỗi claim quan trọng phải có ít nhất 2 nguồn Tier 1-3.

### Bước 3: COLLECT — Thu thập thông tin
Với mỗi nguồn, extract:
```
- Claim chính là gì?
- Evidence là gì? (data, case study, expert opinion?)
- Khi nào? (recency matters)
- Ai publish? Có conflict of interest không?
- Có contradict nguồn khác không?
```

### Bước 4: TRIANGULATE — Kiểm chứng chéo
```
Claim X được xác nhận bởi: [Source A] [Source B] → CONFIRMED
Claim Y chỉ có: [Source A] → UNCONFIRMED — cần thêm evidence
Claim Z: [Source A] says X, [Source B] says Y → CONFLICTING — note disagreement
```

**Quan trọng:** Report conflicting findings, đừng cherry-pick nguồn phù hợp với kết luận mình muốn.

### Bước 5: SYNTHESIZE — Tổng hợp thành output

---

## Output Format Chuẩn

```markdown
# Research Report: [Topic]
**Ngày:** [Date] | **Scope:** [Defined scope] | **Confidence:** High/Medium/Low

## TL;DR (Executive Summary)
[3-5 bullet points — key findings only. Người bận nhất đọc phần này vẫn nắm được.]

## Findings

### [Finding 1 — Rõ ràng, có thể action]
[Mô tả finding]
> 📌 Source: [Tên nguồn, link, năm]

### [Finding 2]
...

## Conflicting Evidence
[Những điểm mà các nguồn không đồng ý — ĐỪNG bỏ qua phần này]
- [Claim X]: Source A nói..., Source B nói... → Em chưa confirm được

## Gaps — Những gì vẫn còn unclear
- [Câu hỏi 1 không tìm được câu trả lời reliable]
- [Data cần nhưng không available publicly]

## Sources
| # | Nguồn | Tier | Link | Ngày access |
|---|-------|------|------|-------------|
| 1 | ... | T1 | ... | ... |
```

---

## Chế độ Research Nhanh (Quick Research)

Khi user chỉ cần overview nhanh (không cần deep research):

```
⚡ Quick Research Mode (5 phút):
- 3-5 sources only
- Focus on Tier 1-2
- Output: bullet summary, không phải full report
- Flag: "Cần deep research để verify?"
```

---

## Tích hợp với AWF Skills khác

| Kết hợp với | Tác dụng |
|------------|---------|
| `awf-idea-refine` | Research → validate assumptions của idea trước khi refine |
| `/brainstorm` | Sau brainstorm, research để fact-check hypotheses |
| `data-scraper-agent` | Research để xác định data sources cần scrape |
| `awf-diagramming` | Research findings → visualize dưới dạng market map, comparison chart |
| `psycho-content-engineer` | Research audience psychology → inform content strategy |

---

## ⚠️ Anti-Rationalization

| Sai lầm phổ biến | Thực tế |
|---|---|
| "Google 5 phút là đủ" | Google search trả về SEO content, không phải research. Cần methodology. |
| "Nguồn này đáng tin vì nổi tiếng" | Reputation ≠ accuracy cho topic cụ thể. Verify từng claim. |
| "Các nguồn đồng ý = đúng" | Có thể tất cả đều cite cùng 1 nguồn gốc lỗi. Check primary source. |
| "Không tìm được evidence = không có" | Có thể evidence tồn tại nhưng không public. Note as gap, không confirm. |
| "Bỏ qua conflicting findings" | Conflicting findings thường là nơi có insight thực sự. |

---

## 🚩 Red Flags

- Research report không có sources list cụ thể
- Tất cả sources từ cùng 1 lĩnh vực → echo chamber
- Không có "gaps" section → researcher chưa biết mình không biết gì
- Claims mạnh mà không có Tier 1-2 evidence
- Research date > 1 năm cho fast-moving topics (AI, crypto, regulatory)
