# 📊 Báo Cáo Phân Tích: AntiGravity Workflows & Skills

> Phân tích toàn diện 22 workflows + 42 skills  
> Ngày: 2026-04-28

---

## PHẦN 1: SƠ ĐỒ LOGIC TỔNG THỂ

### 1.1 Workflow Chain Chính (Software Dev)

```
/init → /brainstorm → /plan → /design → /visualize → /code → /test → /audit → /deploy
  ↑                                                      ↑        ↓
  └──── /recap (context restore) ────────────────────── /run ← /debug
                                                          ↓
                                              /refactor → /rollback → /save-brain
```

### 1.2 Workflow Chain Content (Squirrel Finance)

```
/script (SKILL: squirrel-scriptwriter)
  → Research → Outline → Full Script → AI Prompts → YouTube Package
  → /fb-post (SKILL: psycho-content-engineer → fb-publisher)
```

### 1.3 Ma Trận Skills vs Workflows

| Skill | Kích hoạt bởi workflow |
|-------|------------------------|
| `karpathy-coding-principles` | /code, /refactor, /debug, /design, /audit |
| `awf-spec-writer` | /plan |
| `awf-session-restore` | /recap, mọi workflow (level 1) |
| `awf-auto-save` | Cuối mọi workflow, user leaving |
| `awf-gitnexus-context` | /code, /debug, /refactor, /audit |
| `awf-red-teaming` | /audit (offensive layer) |
| `context-engineering` | Session mới, khi output kém |
| `awf-proactive-evolution` | Ngầm, mọi session |
| `psycho-content-engineer` | /fb-post create, viết content |
| `squirrel-scriptwriter` | /script |
| `webapp-testing` (Playwright) | /test option D |
| `ui-ux-pro-max` | /visualize |
| `deployment-patterns` | /deploy |
| `seo` | /audit (web app), /deploy |
| `postgres-patterns` | /design |
| `github-ops` | /deploy (release management) |
| `git-workflow` | /code phase-01 setup |
| `manim-video` | /script (optional) |
| `remotion-video-creation` | /script (optional) |
| `awf-adaptive-language` | Mọi workflow (đọc preferences.json) |
| `awf-error-translator` | /debug, /code khi có lỗi |
| `awf-diagramming` | /design, /plan |

---

## PHẦN 2: ĐÁNH GIÁ HIỆU SUẤT

### 2.1 ✅ Điểm Mạnh Nổi Bật

**A. Kiến trúc Chain cực kỳ logic**
- Mỗi workflow có `NEXT STEPS` menu số rõ ràng → AI không bị lạc
- `brainstorm → plan → design → visualize → code` là pipeline hoàn chỉnh
- `save-brain → recap` tạo vòng lặp memory tốt

**B. Anti-Hallucination Design**
- `karpathy-coding-principles` bắt AI suy nghĩ trước khi code
- `awf-spec-writer` yêu cầu surface assumptions trước khi code
- `context-engineering` có quy tắc "Focused context > Flood context"
- `debug.md` có nguyên tắc "KHÔNG ĐOÁN MÒ. Thu thập bằng chứng → Giả thuyết → Kiểm chứng"

**C. Safety Net Tốt**
- `save-brain + recap + awf-auto-save` = triple backup context
- `rollback.md` xử lý recovery scenario rất đầy đủ
- `code.md` có Test Skip Block → ngăn deploy khi có test bị skip

**D. Non-Tech Mode nhất quán**
- 18/22 workflows đều có "Non-Tech Mode v4.0" đọc `preferences.json`
- Bảng dịch thuật ngữ trong từng workflow

**E. GitNexus Integration (blast-radius analysis)**
- Được tích hợp vào /code, /debug, /refactor, /audit, /rollback, /init
- Rất thực tế để ngăn "tiện tay sửa code" gây hỏng chỗ khác

---

### 2.2 ❌ Vấn Đề Nghiêm Trọng (Bug & Gap)

#### 🔴 VẤN ĐỀ 1: Persona Assignment Mâu Thuẫn với Thực tế AI
**Vị trí:** Nhiều workflows
```
code.md:    Persona = "Elon Musk" — triết lý "move fast, ship it, fix later"
debug.md:   Persona = "Donald Trump"
design.md:  Persona = "Bill Gates"
plan.md:    Persona = "Mark Zuckerberg"
audit.md:   Persona = "Warren Buffett"
rollback.md: Persona = "Larry Ellison"
run.md:     Persona = "Jeff Bezos"
visualize.md: Persona = "Steve Jobs"
```
**Vấn đề:** 
- Persona "Elon Musk" với triết lý "move fast, ship it, fix later" **MÂU THUẪN TRỰC TIẾP** với toàn bộ tinh thần của karpathy-coding-principles và awf-spec-writer
- AI hiện đại (Claude, Gemini) không thực sự "adopt" persona người nổi tiếng — chúng chỉ đọc tên, không có behavior change thực sự
- Đây là **decorative noise** tốn token, không có giá trị hành vi thực tế

**Rủi ro AI hallucination:** AI có thể interpret "Elon Musk mindset" khác nhau → behavior không nhất quán

---

#### 🔴 VẤN ĐỀ 2: fb-post.md Hardcode Windows Path
**Vị trí:** `fb-post.md` line 9-10
```
Base Path: C:\Users\Administrator\.gemini\antigravity\skills\fb-publisher\
Data Path: C:\Users\Administrator\.gemini\antigravity\data\fb-publisher\
```
**Vấn đề:** Username `Administrator` hardcode → sẽ fail trên máy user hiện tại (username: `Trong`)

---

#### 🔴 VẤN ĐỀ 3: awf-proactive-evolution Quá Ngắn & Thiếu Guardrails
**Vị trí:** `awf-proactive-evolution/SKILL.md` — chỉ 43 dòng
**Vấn đề:**
- Skill cho phép AI "sửa SKILL.md trực tiếp" khi user approve → rất nguy hiểm nếu AI hallucinate suggestion
- Không có validation step: "verify sau khi sửa"
- Không có rollback plan khi suggestion sai

---

#### 🟡 VẤN ĐỀ 4: review.md và customize.md — Không Đọc Được
**Vị trí:** Hai workflows này không được đọc trong session này vì đã đủ data, nhưng từ descriptions:
- `/customize` = "Cá nhân hóa trải nghiệm" nhưng không có workflow nào giải thích cụ thể sẽ update file gì
- `/review` = "Tổng quan & Bàn giao" — nếu thiếu output format rõ ràng có thể bị AI tự ý format

---

#### 🟡 VẤN ĐỀ 5: awf-auto-save — Pattern Detection Quá Đơn Giản
**Vị trí:** `awf-auto-save/SKILL.md`
```python
patterns:
  - "bye", "tam biet", "tam nghi"
  - "toi di", "di an com", "nghi thoi"
```
**Vấn đề:**
- Thiếu dấu thanh: "tôi đi" ≠ "toi di" (tiếng Việt không dấu)
- AI LLM không thực sự chạy `on_message()` như code — đây là pseudocode, không chạy được
- Token estimation dựa trên `message_count * 150` là heuristic rất thô

---

#### 🟡 VẤN ĐỀ 6: /script workflow và squirrel-scriptwriter Skill Có Mâu Thuẫn
**Vị trí:** `script.md` vs `squirrel-scriptwriter/SKILL.md`

| Điểm | script.md | SKILL.md |
|------|-----------|----------|
| Số scenes | "25-35 scenes" | "1 prompt mỗi 8-10 giây" → ~60-75 prompts cho 10 phút |
| Lưu file | `z:\Squirrel Finance Channel\[Vid N]\` | `z:\Squirrel Finance Channel\[Vid N]\` (khớp) |
| Phase 5.5 | Không nhắc | Bắt buộc Alignment Review |

**Vấn đề:** AI đọc `script.md` (workflow) có thể bỏ qua Phase 5.5 (Alignment Review) vì không có trong workflow instructions

---

#### 🟡 VẤN ĐỀ 7: Thiếu Workflow cho Data Science và Research
**Vấn đề:**  Skills `awf-data-science` và `awf-research-agent` không có workflow riêng để kích hoạt chúng một cách có cấu trúc. User phải biết gõ đúng keyword mới trigger được.

---

## PHẦN 3: GỢI Ý CẢI TIẾN CHI TIẾT

### 3.1 🔧 FIX NGAY — Persona Replacement

**Vấn đề:** Personas tên người nổi tiếng không có giá trị hành vi thực tế, tốn tokens

**Cải tiến đề xuất:**  
Thay thế persona bằng **Behavior Contract** — danh sách hành vi cụ thể có thể enforce:

```markdown
❌ TRƯỚC (code.md):
## 🎭 PERSONA: "Elon Musk" — "move fast, ship it, fix later"

✅ SAU:
## 🤝 BEHAVIOR CONTRACT (Senior Developer Mode)
- Đọc kỹ yêu cầu trước khi gõ dòng code đầu tiên
- Nếu yêu cầu mơ hồ: hỏi 1 câu làm rõ, KHÔNG tự đoán
- Chỉ sửa đúng chỗ được yêu cầu (surgical changes)
- Trước khi thêm dependency mới: thông báo cho user
- Sau mỗi task: báo cáo ngắn gọn files đã thay đổi
- KHÔNG tự ý thêm tính năng không được yêu cầu
```

**Lợi ích:** 
- Giảm ~50-100 tokens/workflow
- Behavior predictable hơn
- Không có rủi ro AI "interpret persona theo cách riêng"

---

### 3.2 🔧 FIX NGAY — fb-post.md Path

```markdown
❌ TRƯỚC:
Base Path: C:\Users\Administrator\.gemini\antigravity\skills\fb-publisher\

✅ SAU:
Base Path: {$env:USERPROFILE}\.gemini\antigravity\skills\fb-publisher\
# Hoặc đọc từ preferences.json: skill_base_path
```

---

### 3.3 🔧 FIX QUAN TRỌNG — awf-proactive-evolution: Thêm Safety Guard

```markdown
✅ Thêm vào SKILL.md:

## Safety Rules (BẮT BUỘC)
1. Chỉ đề xuất khi pattern lặp lại ≥ 3 lần trong session
2. LUÔN show diff trước/sau: "Cũ: [...] → Mới: [...]"
3. Sau khi user approve và AI edit file: 
   - Đọc lại file vừa edit để verify
   - Nếu nội dung không đúng ý → Revert và báo lỗi
4. Không bao giờ edit file trong cùng một step với propose
5. Tạo backup: copy file gốc → file.bak trước khi edit
```

---

### 3.4 🔧 CẢI TIẾN — script.md: Thêm Phase 5.5

```markdown
✅ Thêm vào script.md giữa Giai đoạn 5 và 6:

### Giai đoạn 5.5: Prompt Alignment Review 🔍 [BẮT BUỘC]

Đây là bước quan trọng để đảm bảo AI prompts không tạo ra "phantom content"
(nội dung không có trong script).

Thực hiện theo Phase 5.5 trong squirrel-scriptwriter/SKILL.md:
1. Cross-reference mỗi prompt với script
2. Coverage check: 5-8 moments quan trọng nhất có prompt chưa?
3. Fix & Flag: xóa/rewrite prompt sai
4. Output Alignment Score

❌ KHÔNG tiếp tục Giai đoạn 6 nếu verdict là "NEEDS REVISION"
```

---

### 3.5 🚀 CẢI TIẾN LỚN — Thêm Anti-Hallucination Layer vào /code

**Vấn đề hiện tại:** `/code` thiếu "verify trước khi code" về API/imports thực tế

**Cải tiến:**
```markdown
✅ Thêm vào code.md - Giai đoạn 0:

### 0.5. Pre-Code Reality Check (chống hallucination API)

Trước khi implement, BẮT BUỘC kiểm tra:

□ API/Function đang dùng có THỰC SỰ tồn tại trong codebase không?
  → Grep trước: "Có function [tên] không?" 
  → Nếu không có → Thông báo user, hỏi muốn tạo mới hay dùng alternative

□ Import path có đúng không?
  → Kiểm tra file thực sự nằm ở đường dẫn đó

□ TypeScript types được định nghĩa ở đâu?
  → Tìm trong types/, interfaces/ trước khi tạo mới

□ Package đang dùng đã được install chưa?
  → Kiểm tra package.json

⚠️ KHÔNG BAO GIỜ: Tạo import từ package chưa có trong package.json
⚠️ KHÔNG BAO GIỜ: Gọi function chưa được verify là tồn tại
```

---

### 3.6 🚀 CẢI TIẾN LỚN — Thêm "Truth Anchor" vào awf-spec-writer

**Vấn đề:** Spec được AI tạo có thể contain assumptions không được verify

**Cải tiến:**
```markdown
✅ Thêm vào Phase 1 của awf-spec-writer:

### Bước 1D: Truth Anchor Check

Sau khi viết spec, AI phải tự hỏi và trả lời:

"Những gì em vừa viết trong spec — phần nào là FACT (đã verify)
và phần nào là ASSUMPTION (em đoán)?"

Format output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ FACTS (đã verify từ codebase/docs):
  - Database là PostgreSQL (thấy trong .env.example)
  - Dùng Prisma (thấy trong package.json)

⚠️ ASSUMPTIONS (chưa confirm):
  - JWT expiry 24h (em đoán theo best practice)
  - File upload limit 10MB (em đoán theo thông thường)

→ Anh xác nhận các ASSUMPTIONS này đúng không?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 3.7 🚀 CẢI TIẾN — Thêm Workflow /research và /data-analyze

**Vấn đề:** `awf-research-agent` và `awf-data-science` rất mạnh nhưng không có workflow command

**Giải pháp:** Tạo 2 workflow commands mới:

```markdown
# /research — Deep Research Workflow
# → Trigger: awf-research-agent skill
# → Tích hợp: local-coccoc-control, awf-document-parser
# → Output: Research report với sources + conclusions

# /analyze — Data Science Workflow  
# → Trigger: awf-data-science skill
# → Input: CSV/Excel/SQL
# → Output: EDA report + visualization + insights
```

---

### 3.8 🚀 CẢI TIẾN — Thêm "Session Start Checklist" tự động

**Vấn đề hiện tại:** Không có quy trình chuẩn khi bắt đầu session

**Cải tiến:** Thêm vào `awf-session-restore/SKILL.md`:

```markdown
## Session Start Protocol (Thêm mới)

Khi bắt đầu session MỚI (chưa có context), AI tự động:

1. Check .brain/session.json → Load Level 1
2. Check context-engineering rules file (GEMINI.md hoặc brain.json)
3. Announce trạng thái rõ ràng:
   
   "📍 Em đã load context:
    - Project: [tên]
    - Đang làm: [feature/task]
    - Lần cuối save: [time]
    
    ⚠️ NHỮNG GÌ EM BIẾT vs KHÔNG BIẾT:
    - Biết chắc: [từ brain.json]
    - Cần confirm: [những gì có thể stale]
    
    Anh bắt đầu từ đâu?"

4. Không tự assume bất cứ điều gì về code hiện tại
   → Phải đọc file thực tế trước khi reference
```

---

### 3.9 🚀 CẢI TIẾN — Thêm "Hallucination Self-Check" vào debug.md

**Vấn đề:** Khi debug, AI có thể suggest fix dựa trên memory thay vì đọc code thực tế

**Cải tiến:**
```markdown
✅ Thêm vào debug.md - Giai đoạn 2, trước khi Hypothesis Formation:

### 2.0. Reality Check Trước Khi Giả Thuyết

BẮT BUỘC đọc file thực tế trước khi đưa giả thuyết:
- Đọc file có lỗi → Thấy code THỰC TẾ
- Đọc error log → Thấy line number THỰC TẾ  
- Check package version → Tránh suggest API đã deprecated

❌ KHÔNG: "Lỗi này thường do X" (từ memory)
✅ PHẢI: "Em đọc file [path] tại line [N] thấy..." (từ file thực tế)
```

---

## PHẦN 4: PHÂN TÍCH MỨC ĐỘ LOGIC GIỮA WORKFLOWS VÀ SKILLS

### 4.1 Điểm Logic Tốt

| Kết nối | Mức độ tốt |
|---------|-----------|
| /plan → awf-spec-writer | ⭐⭐⭐⭐⭐ Rất tốt |
| /code → karpathy-coding-principles | ⭐⭐⭐⭐⭐ Rất tốt |
| /audit → awf-red-teaming + seo | ⭐⭐⭐⭐⭐ Rất tốt |
| /test → webapp-testing (Playwright) | ⭐⭐⭐⭐⭐ Rất tốt |
| /deploy → deployment-patterns + github-ops | ⭐⭐⭐⭐ Tốt |
| /script → squirrel-scriptwriter | ⭐⭐⭐⭐ Tốt (có mâu thuẫn nhỏ) |
| /fb-post → psycho-content-engineer → fb-publisher | ⭐⭐⭐⭐ Tốt |
| save-brain ↔ recap | ⭐⭐⭐⭐⭐ Rất tốt |

### 4.2 Điểm Logic Cần Cải Thiện

| Kết nối | Vấn đề |
|---------|--------|
| awf-auto-save với mọi workflow | Pattern detection là pseudocode, không thực thi được |
| awf-proactive-evolution với codebase | Thiếu safety guard khi edit file |
| awf-adaptive-language với workflows | Đọc preferences.json nhưng không có cơ chế verify file tồn tại |
| context-engineering với /code | Skill không được kích hoạt tự động trong /code |
| awf-data-science, awf-research-agent | Cô lập, không có workflow path vào |

---

## PHẦN 5: ĐÁNH GIÁ HIỆU QUẢ CHỐNG AI HALLUCINATION

### Thang điểm: 1-10

| Khía cạnh | Điểm | Nhận xét |
|-----------|------|----------|
| Anti-scope-creep (không thêm tính năng) | 9/10 | karpathy + code.md rules tốt |
| Anti-fabrication (không bịa API) | 6/10 | Thiếu pre-code reality check |
| Anti-assumption (không đoán) | 7/10 | awf-spec-writer tốt, nhưng chưa mandatory |
| Anti-stale-context (không dùng memory cũ) | 7/10 | session.json + recap tốt |
| Anti-drift (không làm lạc đề) | 8/10 | Behavior Contract tốt |
| Verification before action | 6/10 | Cần thêm Truth Anchor |
| Error translation | 8/10 | awf-error-translator + bảng dịch tốt |
| **Tổng thể** | **7.3/10** | Tốt nhưng còn gap lớn ở API verification |

---

## PHẦN 6: TOP 5 ƯU TIÊN CẢI TIẾN

| # | Việc cần làm | Tác động | Độ khó |
|---|--------------|----------|--------|
| 1 | Thêm Pre-Code Reality Check vào /code (3.5) | Cao | Thấp |
| 2 | Thay persona bằng Behavior Contract (3.1) | Cao | Thấp |
| 3 | Thêm Truth Anchor vào awf-spec-writer (3.6) | Cao | Thấp |
| 4 | Fix fb-post.md hardcode path (3.2) | Trung bình | Rất thấp |
| 5 | Thêm Phase 5.5 vào script.md (3.4) | Trung bình | Thấp |

---

## PHẦN 7: NHẬN XÉT TỔNG QUAN

### Điểm mạnh tổng thể
Hệ thống AWF của anh là một trong những hệ thống workflow AI **cực kỳ trưởng thành và có chiều sâu**. Rất hiếm thấy hệ thống cá nhân có:
- Pipeline phát triển phần mềm đầy đủ (init → deploy)
- Anti-hallucination mechanisms nhiều lớp
- Content pipeline hoàn chỉnh cho YouTube + Facebook
- Context memory system (brain.json + session.json + handover.md)
- Self-improvement mechanism (awf-proactive-evolution)

### Gap lớn nhất cần giải quyết
**"Last Mile Hallucination"** — AI biết phải làm gì (workflow rõ ràng), nhưng vẫn có thể hallucinate ở khâu cuối khi viết code cụ thể:
- Gọi API chưa verify tồn tại
- Import từ path chưa verify
- Reference function chưa được đọc từ file thực

Giải pháp: **"Read Before Reference"** — thêm mandatory step đọc file thực trước khi reference bất kỳ symbol nào.

---

*Báo cáo được tạo bởi AntiGravity | 2026-04-28*
