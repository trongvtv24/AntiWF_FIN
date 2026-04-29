---
description: 🐿️ Viết kịch bản video YouTube cho kênh Squirrel Finance
# AWF_METADATA_START
type: workflow
name: "script"
command: "/script"
awf_version: "4.0.0"
workflow_version: "1.0.0"
status: active
category: "content"
risk_level: "medium"
triggers:
  - "/script"
  - "youtube script"
  - "squirrel finance"
  - "video script"
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
  - "content/scripts/*.md"
  - ".brain/claims.md"
required_gates:
  - "global_safety_truthfulness_gate"
skill_hooks:
  required:
    - "squirrel-scriptwriter"
  conditional:
    - "awf-research-agent"
    - "timestamp-to-visual-prompt"
    - "squirrel-video-director"
    - "manim-video"
    - "remotion-video-creation"
handoff:
  next_workflows:
    - "/save-brain"
# AWF_METADATA_END
---

// turbo-all

# 🐿️ /script — Viết Kịch Bản Video Squirrel Finance

## Mô tả
Command này kích hoạt **Squirrel Scriptwriter Skill** để viết kịch bản video YouTube hoàn chỉnh cho kênh Squirrel Finance.

## Safety & Truthfulness Gate

Trước khi research, viết kịch bản, tạo YouTube package, visual handoff hoặc visual prompts:

- Đọc `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md`.
- Data, số liệu, sự kiện hiện tại phải có nguồn hoặc được ghi là chưa kiểm chứng.
- Không bịa nguồn, không bịa case study, không thêm số liệu không có trong research brief.
- Visual DNA brief và visual prompts không được tạo "phantom content" ngoài nội dung script.

## Khi nào dùng
- Khi muốn viết kịch bản video mới cho kênh
- Khi cần brainstorm topic mới
- Khi cần chuẩn bị Visual DNA Brief để tạo prompt ảnh/video ở bước sau

## Workflow

### Giai đoạn 1: Nhận Topic 🎯

1. Hỏi user chủ đề video muốn viết
2. Đọc skill file: `~/.gemini/antigravity/skills/squirrel-scriptwriter/SKILL.md`
3. Đọc resources:
   - `resources/symbol-system.md`
   - `resources/content-clusters.md`
   - `resources/quality-checklist.md`
4. Phân tích topic:
   - Xác định cluster (A-F)
   - Xác định content layer (1-4)
   - Xác định series format
   - Gợi ý 3-5 title options
5. Trình bày phân tích cho user duyệt

### Giai đoạn 2: Research 🔍

6. Dùng công cụ web search có sẵn trong IDE (ví dụ `search_web` hoặc công cụ tương đương) để tìm:
   - Dữ liệu thống kê mới nhất (ưu tiên 2024-2026)
   - Câu chuyện thực tế với con số cụ thể
   - Bối cảnh lịch sử có số liệu
   - Tác động lên người bình thường hiện tại
   - Sự thật bất ngờ hoặc phản trực giác
7. Tổng hợp Research Brief:
   - 5-10 data points chính (có nguồn)
   - 2-3 câu chuyện/ví dụ thực tế
   - "Hard part" mà đa số người xem chưa hiểu
8. Map dữ liệu vào metaphor system (acorn/leaves/forest)
9. Trình bày research brief cho user review

### Giai đoạn 3: Outline 📝

10. Viết outline plain-text theo công thức 9 phần:
    1. Real-life Hook
    2. Simplified Concept
    3. Step-by-Step Mechanism
    4. Why People Get Pulled In
    5. The Catch
    6. Escalation
    7. Why It Matters Now
    8. Takeaway
    9. Community CTA
11. Ghi chú retention beats cho mỗi phần
12. Trình bày outline cho user duyệt

### Giai đoạn 4: Full Script ✍️

13. Viết long-form script hoàn chỉnh:
    - 1500-3500 từ (8-15 phút)
    - Retention beat mỗi 20-40 giây
    - Voice: conversational, absurd humor, internet-native
    - Data points thực tế được chèn tự nhiên
    - 4 câu hỏi Content Gap phải được trả lời
14. Lưu file tại `z:\Squirrel Finance Channel\[Vid N]\[Topic]_Script.md`
15. Trình bày script cho user review

### Giai đoạn 5: Visual DNA Handoff & Prompt Pipeline 🎨

16. Tạo **Visual DNA Brief** từ `squirrel-scriptwriter`:
    - Canonical visual style
    - Character lock
    - Symbol lock
    - Top 5-8 key visual beats
    - Overlay text candidates
    - "Must not show" notes để tránh phantom content
17. Lưu file: `[Topic]_Visual_DNA_Brief.md`
18. Nếu user muốn tạo prompt ảnh/video ngay trong luồng này:
    - Dùng `timestamp-to-visual-prompt` để tạo `[Topic]_Scene_Plan.json` từ timestamped script
    - Dùng `squirrel-video-director` để tạo `[Topic]_Visual_Prompts.json` và/hoặc `[Topic]_Visual_Prompts.txt`
    - Mặc định dùng clean prompts: không yêu cầu AI sinh text, `overlay_text` để riêng cho hậu kỳ

18b. **[TUỲ CHỌ N] Animation Video (Skill: manim-video)**

    Hỏi user:
    ```
    "🎥 Video này có khái niệm nào cần giải thích bằng animation không?
    (Ví dụ: biểu đồ tăng trưởng, so sánh số liệu, luồng tiền...)

    1️⃣ Có - Em tạo Manim scene cho đoạn đó
    2️⃣ Không cần - Dùng AI image thường"
    ```

    Nếu chọn Có (kích hoạt `manim-video` skill):
    - Xác định scene cần animate (1-3 scene tiêu biểu nhất)
    - Lên storyboard: mọi scene chỉ cần prove 1 ý tưởng
    - Viết Manim Python code cho từng scene
    - Lưu file: `[Topic]_Manim_Scenes.py`
    - Lệnh render nhanh: `manim -ql [Topic]_Manim_Scenes.py`

18c. **[TUỲ CHỌ N] Animated Captions / Charts (Skill: remotion-video-creation)**

    Hỏi user:
    ```
    "🎬 Anh có muốn thêm captions kiểu TikTok (từ sáng lên theo giọng nói)
    hoặc animated chart vào video không?

    1️⃣ Có - Em tạo Remotion component
    2️⃣ Không cần"
    ```

    Nếu chọn Có (kích hoạt `remotion-video-creation` skill):
    - Tạo React component theo đúng rules của Remotion
    - Hỗ trợ: word-highlight captions, animated bar chart, counter animation
    - Lưu file: `[Topic]_Remotion.tsx`


### Giai đoạn 6: YouTube Package 📦

19. Tạo YouTube package:
    - **Thumbnail concept**: mô tả bố cục, emotion, text
    - **Video title**: title chính + 2 alternatives
    - **Video description**: hook + nội dung + takeaway + CTA
    - **Tags**: 15-20 tags (topic + brand + trending)
    - **Sequel hooks**: 2-3 video tiếp theo được gợi ý
20. Lưu file: `[Topic]_YouTube_Package.md`

### Giai đoạn 7: Quality Review ✅

21. Chạy Pre-Publish Checklist (25 điểm từ `quality-checklist.md`)
22. Báo cáo kết quả review cho user
23. Sửa nếu cần dựa trên feedback

## Output Files

Khi hoàn thành, các file sẽ được lưu tại `z:\Squirrel Finance Channel\[Vid N]\`:

| File | Nội dung |
|------|---------|
| `[Topic]_Script.md` | Kịch bản full long-form |
| `[Topic]_Visual_DNA_Brief.md` | DNA hình ảnh, character lock, symbol lock, key visual beats |
| `[Topic]_Scene_Plan.json` | Scene plan JSON từ `timestamp-to-visual-prompt` khi user yêu cầu prompt |
| `[Topic]_Visual_Prompts.json` | Prompt pack từ `squirrel-video-director` khi user yêu cầu prompt |
| `[Topic]_Visual_Prompts.txt` | Prompts only, dùng bulk-paste khi user yêu cầu |
| `[Topic]_YouTube_Package.md` | Title, description, tags, thumbnail |

## Gợi ý sử dụng

```
/script                    → Bắt đầu viết kịch bản mới
/script leverage           → Viết kịch bản về topic "leverage"
/script "credit cards"     → Viết kịch bản về topic "credit cards"
```

## Next Steps sau /script

| Bước tiếp | Command |
|-----------|---------|
| Chạy lại viết kịch bản | `/script` |
| Xem tổng quan dự án | `/review` |
| Gợi ý topic tiếp theo | `/next` |
