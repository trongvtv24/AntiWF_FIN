---
name: timestamp-to-visual-prompt
description: >
  Chuyển kịch bản có timestamp thành visual prompts JSON tối ưu cho AI tạo hình (Kling, Udio, Runway, v.v.) theo format chuẩn kênh Squirrel Finance. Tự động phân đoạn cảnh, tính thời lượng, áp dụng Symbolic Dictionary (Sóc tài chính), và xuất JSON raw thuần túy sẵn sàng paste vào tool. Kích hoạt bằng lệnh /timestamp-to-prompt. Keywords: /timestamp-to-prompt, visual prompt, timestamp, json, scene, tạo ảnh, hình ảnh, create image, kịch bản, squirrel, sóc, prompt ảnh, ai image, generate image.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "timestamp-to-visual-prompt"
skill_version: "1.0.0"
status: active
category: "video"
activation: "explicit_or_intent"
priority: "medium"
risk_level: "medium"
allowed_side_effects:
  - "draft_prompts"
requires_confirmation: false
related_workflows:
  - "/script"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# 🎬 Timestamp → Visual Prompt Generator

## MÔ TẢ
Skill này biến kịch bản YouTube (có timestamp) thành một mảng JSON chứa **visual prompts tối ưu cho AI tạo hình**, theo phong cách chuẩn kênh **Money Explained by a Squirrel**.

---

## TRIGGER
Kích hoạt khi:
- User gõ lệnh **`/timestamp-to-prompt`** ← lệnh chính
- User paste kịch bản có timestamp và yêu cầu tạo prompt ảnh
- User nhắc "tạo prompt ảnh", "visual prompt", "tạo hình từ kịch bản", "scene prompt", "prompt cho AI tạo hình"

---

## HƯỚNG DẪN THỰC HIỆN

### BƯỚC 1 — NHẬN INPUT
Yêu cầu user cung cấp (nếu chưa có):
- **Kịch bản** có timestamp theo định dạng: `[MM:SS]` hoặc `[HH:MM:SS]`
- Mỗi dòng là một câu/đoạn narration tương ứng với timestamp

Ví dụ input:
```
[00:00] Chào mừng các bạn đến với kênh Sóc Tài Chính!
[00:05] Hôm nay chúng ta sẽ nói về lạm phát — kẻ thù thầm lặng của túi tiền bạn.
[00:12] Tưởng tượng mỗi ngày, cái bóng của con cáo ngày càng lớn hơn...
```

---

### BƯỚC 2 — PHÂN ĐOẠN CẢNH (SCENE SEGMENTATION)

1. **Đọc toàn bộ kịch bản** và hiểu ngữ nghĩa từng đoạn
2. **Ghép các câu ngắn** nếu cần để tạo cảnh có thời lượng lý tưởng **4–6 giây/cảnh**
3. **Tính toán thời gian**:
   - Chuyển timestamp sang giây thập phân: `[01:15]` → `75.0`
   - `start_sec`: Timestamp bắt đầu cảnh
   - `end_sec`: Timestamp của cảnh **tiếp theo**
   - `duration_sec`: `end_sec - start_sec`
   - Cảnh **cuối cùng**: mặc định `duration_sec = 5.0`

---

### BƯỚC 3 — TẠO VISUAL PROMPT (THE FORMULA)

Mỗi `visual_prompt` PHẢI viết bằng **Tiếng Anh** và theo đúng cấu trúc 3 phần:

#### PART A — Base Style & Character (BẮT BUỘC ở đầu mỗi prompt)
```
2D animated cartoon, modern cute vector style, flat vibrant colors, clean thick black outlines, smooth cel-shaded motion, pure white background, 16:9 aspect ratio, 8 seconds loop. Friendly wise old anthropomorphic brown squirrel with rich brown fur, large fluffy tail, long white beard, white bushy eyebrows, light beige belly.
```

#### PART B — Action & Props (Thích nghi theo nội dung narration)

Mô tả hành động của Sóc dựa trên ngữ cảnh. **PHẢI dùng Symbolic Dictionary** sau để dịch khái niệm tài chính thành ẩn dụ hình ảnh:

| Khái niệm Tài chính | Ẩn dụ Hình ảnh |
|---|---|
| Tài sản / Giá trị | Acorn (Hạt dẻ) |
| Tiền bạc / Thu nhập | Golden Leaves (Lá vàng) |
| Bất động sản / Tài sản cứng | Walnut (Quả óc chó) |
| Side hustle / Hàng ngắn hạn | Pinecone (Quả thông) |
| Quỹ dự phòng / Tiền mặt | Nest / Deep Bunker |
| Tăng trưởng dài hạn | Oak Tree (Cây sồi) |
| Đa dạng hóa đầu tư | Canopy (Tán cây) |
| Cố vấn tài chính | Owl with glasses (Cú đeo kính) |
| Suy thoái / Nghỉ hưu | Winter / Snow |
| Thị trường tăng | Spring / Rain |
| Khủng hoảng thị trường | Wildfire / Storm |
| Vòng quay lao động / Rat Race | Squirrel Wheel |
| Lạm phát | Shadow of a Fox |
| Lừa đảo / Đầu tư độc hại | Bright Poisonous Mushroom |
| Nợ xấu / Bẫy tín dụng | Cage Trap |

**Thêm chuyển động lặp nhẹ nhàng**: ví dụ `"His fluffy tail sways gently back and forth. Smooth looping idle animation."`

#### PART C — Text Box & Exclusions (BẮT BUỘC ở cuối mỗi prompt)
```
Bold white text box at the bottom reads exactly '[5-10 KEYWORDS TRÍCH TỪ NARRATION]' in clean sans-serif font. No background, no environment, no 3D, no realism.
```

---

### BƯỚC 4 — ĐỊNH DẠNG JSON OUTPUT (CỰC KỲ QUAN TRỌNG)

**Chỉ xuất JSON thuần túy, tuyệt đối KHÔNG:**
- Bọc trong markdown code block (` ```json `)
- Thêm text giới thiệu hoặc kết luận
- Ký tự đầu tiên PHẢI là `[`, ký tự cuối cùng PHẢI là `]`

**Cấu trúc JSON:**
```
[
  {
    "scene_id": 1,
    "start_sec": 0.0,
    "end_sec": 8.0,
    "duration_sec": 8.0,
    "narration": "Original narration text here.",
    "visual_prompt": "2D animated cartoon, modern cute vector style, flat vibrant colors, clean thick black outlines, smooth cel-shaded motion, pure white background, 16:9 aspect ratio, 8 seconds loop. Friendly wise old anthropomorphic brown squirrel with rich brown fur, large fluffy tail, long white beard, white bushy eyebrows, light beige belly. [MÔ TẢ HÀNH ĐỘNG + ẨN DỤ]. His fluffy tail sways gently back and forth. Smooth looping idle animation. Bold white text box at the bottom reads exactly 'KEYWORDS HERE' in clean sans-serif font. No background, no environment, no 3D, no realism."
  }
]
```

---

## QUY TẮC ĐẢM BẢO CHẤT LƯỢNG

1. ✅ **Mỗi cảnh phải có đủ 3 phần** A + B + C trong `visual_prompt`
2. ✅ **Thời lượng lý tưởng**: 4–6 giây/cảnh (ghép câu nếu cần)
3. ✅ **Ẩn dụ**: Luôn dùng Symbolic Dictionary, KHÔNG dùng khái niệm tài chính trực tiếp trong prompt
4. ✅ **Keywords text box**: Trích ngắn gọn 5–10 từ khóa từ narration, viết IN HOA
5. ✅ **Output RAW JSON**: Không markdown wrapper, không text thừa
6. ✅ **Cảnh cuối**: Nếu không có timestamp tiếp theo, `duration_sec = 5.0`

---

## VÍ DỤ MINH HỌA

**INPUT:**
```
[00:00] Lạm phát là kẻ thù thầm lặng của túi tiền bạn.
[00:06] Mỗi ngày bạn không đầu tư, cái bóng con cáo ngày càng lớn hơn.
```

**OUTPUT:**
```
[
  {
    "scene_id": 1,
    "start_sec": 0.0,
    "end_sec": 6.0,
    "duration_sec": 6.0,
    "narration": "Lạm phát là kẻ thù thầm lặng của túi tiền bạn.",
    "visual_prompt": "2D animated cartoon, modern cute vector style, flat vibrant colors, clean thick black outlines, smooth cel-shaded motion, pure white background, 16:9 aspect ratio, 8 seconds loop. Friendly wise old anthropomorphic brown squirrel with rich brown fur, large fluffy tail, long white beard, white bushy eyebrows, light beige belly. The squirrel clutches a pile of golden leaves protectively while a large dark fox shadow looms behind him on the ground, growing larger. His fluffy tail sways gently back and forth. Smooth looping idle animation. Bold white text box at the bottom reads exactly 'LẠM PHÁT KẺ THÙ THẦM LẶNG TÚI TIỀN' in clean sans-serif font. No background, no environment, no 3D, no realism."
  },
  {
    "scene_id": 2,
    "start_sec": 6.0,
    "end_sec": 11.0,
    "duration_sec": 5.0,
    "narration": "Mỗi ngày bạn không đầu tư, cái bóng con cáo ngày càng lớn hơn.",
    "visual_prompt": "2D animated cartoon, modern cute vector style, flat vibrant colors, clean thick black outlines, smooth cel-shaded motion, pure white background, 16:9 aspect ratio, 8 seconds loop. Friendly wise old anthropomorphic brown squirrel with rich brown fur, large fluffy tail, long white beard, white bushy eyebrows, light beige belly. The squirrel sits idle on a squirrel wheel spinning slowly, while the fox shadow behind him grows progressively larger with each rotation. His fluffy tail sways gently back and forth. Smooth looping idle animation. Bold white text box at the bottom reads exactly 'KHÔNG ĐẦU TƯ BÓNG CÁO LỚN DẦN' in clean sans-serif font. No background, no environment, no 3D, no realism."
  }
]
```

---

## GHI CHÚ THÊM
- Skill này được thiết kế riêng cho kênh **Money Explained by a Squirrel** (Squirrel Finance)
- Visual style chuẩn: **2D cartoon, flat vibrant colors, white background**
- Output JSON được dùng để nhập trực tiếp vào tool tạo slideshow (Grok_Veo_App hoặc tương tự)
- Kết hợp tốt với skill: `squirrel-scriptwriter` → `timestamp-to-visual-prompt` → `script-segmenter`
