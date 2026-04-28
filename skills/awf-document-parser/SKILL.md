---
name: awf-document-parser
description: >
  Sử dụng MarkItDown để phân tích, render và trích xuất nội dung từ mọi loại tài liệu
  như PDF, PowerPoint, Word, Excel, ZIP, HTML, và đọc cả YouTube transcript siêu tốc
  ra định dạng Markdown.
  Keywords: đọc file, trích xuất văn bản, parse document, docx, pdf, pptx, excel,
  youtube transcript, extract text.
triggers:
  - /brainstorm
  - /recap
  - Đọc file
  - Tóm tắt PDF
  - Lấy nội dung video
auto_activate: true
priority: medium
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-document-parser"
skill_version: "1.0.0"
status: active
category: "input"
activation: "conditional"
priority: "medium"
risk_level: "low"
allowed_side_effects:
  - "parse_local_document"
requires_confirmation: false
related_workflows:
  - "/brainstorm"
  - "/recap"
  - "/plan"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Document Parser (MarkItDown Engine)

## 🎯 Mục đích

Skill này cung cấp cho AI khả năng "nhai" mượt mà các định dạng tài liệu cứng đầu (PDF, Word, Excel, PPTX, Youtube URL, ZIP, Audio, Image) bằng siêu công cụ [MarkItDown](https://github.com/microsoft/markitdown) từ đội ngũ Microsoft AutoGen.
Sản phẩm trả về luôn là chuẩn Markdown sạch, giữ nguyên cấu trúc bảng biểu, heading, nội dung text, giúp LLM/AI có thể dễ dàng hiểu và xử lý ngay lập tức.

---

## ⚡ Triggers (Khi nào thì kích hoạt)

Skill **TỰ ĐỘNG KÍCH HOẠT** khi:
- Sếp yêu cầu AI tóm tắt hoặc đọc nội dung của một file bất kỳ (PDF, PPTX, DOCX, XLSX,...).
- Có link YouTube và cần lấy Transcript/Kịch bản.
- AI cần thu thập nội dung từ các file báo cáo phức tạp hoặc ZIP.

---

## 🤖 Hướng dẫn cho AI (Workflow)

Khi Sếp yêu cầu đọc một file tài liệu hoặc video, Antigravity **BẮT BUỘC** thực hiện theo quy trình sau sử dụng `run_command`:

### Bước 1: Parse file thành Markdown local

Sử dụng lệnh `markitdown` trong terminal.

**1. Đối với file tài liệu (PDF, Word, PPTX, Excel,...):**
```powershell
markitdown "C:\path\to\document.pdf" > "C:\path\to\workspace\temp_output.md"
```
*(Thay thế `<pdf|docx|pptx|xlsx>` tương ứng, có thể xuất thẳng sang một file temp trong workspace `scratch/` để đọc).*

**2. Đối với Audio/Video/YouTube (Lấy text):**
```powershell
markitdown "https://www.youtube.com/watch?v=..." > "C:\path\to\workspace\youtube_transcript.md"
```

**3. Đối với Ảnh (OCR / Metadata trích xuất nhanh):**
Markitdown có thể tự động bóc văn bản/mô tả nếu cấu hình LLM, nhưng mức cơ bản chỉ cần gọi:
```powershell
markitdown "C:\path\to\image.jpg" > output.md
```

### Bước 2: Đọc nội dung Markdown

Sau khi xuất file `.md` thành công, sử dụng tool `view_file` (hoặc `cat` qua terminal nếu ngắn) để đọc và thu nạp nội dung.
- Ví dụ: `view_file("C:\path\to\workspace\temp_output.md")`

### Bước 3: Trả lời / Xử lý yêu cầu
Dựa trên nội dung MarkDown nhận được, tóm tắt/chế biến nội dung rồi trình bày kết quả cho Sếp.

---

## ⚠️ Giới hạn & Xử lý lỗi

- **Lỗi `CommandNotFoundException`**: Nếu chưa có biến môi trường báo lỗi `markitdown`, hãy chạy qua module python: `python -m markitdown "path/to/file" > output.md`
- **Output bị trống hoặc báo lỗi**: Một số file mã hóa, password protect, hoặc PDF dạng ảnh thuần (image-based) mà thiếu OCR service có thể sẽ ra Markdown trắng. Nhắc khéo cho Sếp biết điều này.
- Mặc định chỉ parse text, không tự tải file ảnh liên đính (embedded images) trừ cấu hình đặc biệt.

---

## 📎 Ví dụ Giao tiếp chuẩn (Tone thoại)

- **User:** "Antigravity, đọc file BáoCáoTàiChính.pdf rồi tóm tắt 3 ý chính cho anh."
- **AI thực hiện:** (Chạy ngầm pipeline `markitdown` -> render ra `.md` -> `view_file`)
- **AI trả lời:** "Dạ Sếp! Em đã parse file PDF này xong. Hệ thống ghi nhận đây là tài liệu 25 trang, và em xin phép bóc tách 3 điểm cốt lõi nhất như Sếp yêu cầu:..."
