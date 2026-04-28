# 💡 BRIEF: YouTube Intelligence Desktop App

**Ngày tạo:** 2026-04-24
**Tên tạm:** `YT-Intel` (YouTube Intelligence)

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT

Content Creator / Strategist cần theo dõi 50-100 kênh YouTube đối thủ để:
- Phát hiện **chủ đề đang được khán giả quan tâm nhiều**
- Hiểu **pattern thành công** của đối thủ (tiêu đề, độ dài, tần suất đăng)
- Khai thác **nội dung comment** để tìm pain point của khán giả
- **Xuất kịch bản (transcript)** để phân tích sâu bằng AI bên ngoài

Hiện tại không có tool nào làm được tất cả điều này trong một giao diện duy nhất, offline, không subscription.

---

## 2. GIẢI PHÁP ĐỀ XUẤT

**Desktop App (Windows)** — Python backend + Tauri frontend (React UI).
Chạy local, lưu dữ liệu SQLite, không cần server hay tài khoản.

### Luồng hoạt động chính:
```
Thêm kênh vào Watchlist
       ↓
App tự động pull data theo lịch (Smart Scheduler)
       ↓
Dashboard hiển thị: trending videos, spike alerts, engagement metrics
       ↓
Người dùng click vào video → xem transcript + comments
       ↓
Export transcript → .md / .txt → phân tích bằng AI ngoài
```

---

## 3. ĐỐI TƯỢNG SỬ DỤNG

- **Primary:** Content Creator / Content Strategist (1 người, dùng riêng)
- **Secondary:** Team nhỏ nếu share file export

---

## 4. NGHIÊN CỨU THỊ TRƯỜNG

### Đối thủ cạnh tranh:
| Tool | Điểm mạnh | Điểm yếu |
|------|-----------|----------|
| TubeBuddy | Tích hợp YouTube Studio | Subscription, chỉ phân tích kênh mình |
| VidIQ | Dashboard đẹp, keyword research | Subscription đắt, không lấy transcript |
| Social Blade | Theo dõi nhiều kênh | Chỉ có số liệu cơ bản, không có comment/transcript |
| Noxinfluencer | Competitor analysis | Web-only, không export được |

### Điểm khác biệt của YT-Intel:
- ✅ **Offline, local** — Dữ liệu thuộc về anh, không lo bị xóa/block
- ✅ **Transcript export** — Tính năng cực hiếm, chuyên cho AI analysis workflow
- ✅ **Comment mining** — Tập trung khai thác insight từ comment
- ✅ **Không subscription** — Chỉ tốn API quota miễn phí
- ✅ **50-100 kênh cùng lúc** — Quy mô lớn hơn hầu hết tool

---

## 5. KIẾN TRÚC KỸ THUẬT

### Tech Stack:
```
Frontend:  Tauri + React + TypeScript
Backend:   Python (FastAPI local server)
Database:  SQLite (local)
APIs:      YouTube Data API v3 (multi-key rotation)
           youtube-transcript-api (Python, không tốn quota)
```

### Chiến lược YouTube API:
- **Multi API Key Rotation** — Tự động chuyển key khi gần hết quota
- **Smart Quota Manager** — Ưu tiên kênh VIP, giảm tần suất kênh phụ
- **Transcript riêng** — Dùng `youtube-transcript-api` (không tốn quota)
- **Daily refresh schedule** — Mặc định refresh 1 lần/ngày, có thể manual refresh

### Cấu trúc lưu trữ:
```
SQLite:
  channels       — Danh sách kênh, nhóm, metadata
  videos         — Thông tin video, metrics theo thời gian
  comments       — Comment đã crawl + sentiment
  transcripts    — Transcript raw text
  api_keys       — Danh sách API keys + quota tracking
  alerts         — Lịch sử alert

Export folder (user config):
  /exports/transcripts/[channel_name]/[video_id].md
  /exports/transcripts/[channel_name]/[video_id].txt
  /exports/reports/weekly_[date].pdf
```

---

## 6. TÍNH NĂNG CHI TIẾT

### 🚀 MVP — Phase 1 (Bắt buộc có)

#### 📺 Channel Management
- [ ] Thêm kênh bằng URL / Channel ID / Handle (@username)
- [ ] Tổ chức kênh theo **Group/Watchlist** (VD: "Đối thủ chính", "Niche tài chính", "Kênh quốc tế")
- [ ] Xem thông tin cơ bản: Tên, Avatar, Subs, Total Views, Video Count
- [ ] Xóa / ẩn / archive kênh

#### 📊 Channel Dashboard
- [ ] **Subscriber growth** theo thời gian (chart)
- [ ] **Total views** và tốc độ tăng trưởng
- [ ] Danh sách video mới nhất với metrics
- [ ] **Upload frequency** — Bao nhiêu video/tuần, ngày nào hay đăng

#### 🎬 Video Analytics
- [ ] View count, Like count, Comment count
- [ ] **View per Hour** (tính trong 24h đầu từ lúc đăng)
- [ ] **Average View Duration** (nếu API trả về)
- [ ] **Engagement Rate** = (Likes + Comments) / Views × 100
- [ ] **View Velocity Graph** — Đường cong tăng trưởng view

#### 📝 Transcript
- [ ] Tự động lấy transcript qua `youtube-transcript-api`
- [ ] Fallback: YouTube Captions API (nếu có captions)
- [ ] Hiển thị transcript có timestamp trong app
- [ ] **Export transcript** → `.md` (có heading, timestamp) hoặc `.txt` (plain)
- [ ] Batch export: Xuất toàn bộ transcript của 1 kênh

#### 💬 Comments
- [ ] Lấy Top 100 comments (Most Relevant / Most Recent)
- [ ] Hiển thị: Author, Content, Like count, Reply count, Date
- [ ] **Basic Sentiment** — Phân loại Tích cực / Tiêu cực / Câu hỏi (regex-based)
- [ ] Export comments → `.csv` / `.txt`

#### 🔔 Alert System
- [ ] **New Video Alert** — Thông báo desktop khi kênh theo dõi đăng video mới
- [ ] **View Spike Alert** — Video tăng đột biến view trong 24h (ngưỡng tùy chỉnh)

#### ⚙️ API Key Manager
- [ ] Thêm nhiều YouTube API Key
- [ ] Hiển thị quota còn lại của từng key
- [ ] Tự động rotate sang key tiếp theo khi hết quota
- [ ] Cảnh báo khi tất cả keys gần hết quota

---

### 🎯 Phase 2 — Content Intelligence

#### 🧠 Topic Discovery
- [ ] **Trending Topics** — Từ tiêu đề video, grouping bằng keyword clustering
- [ ] **Comment Question Extractor** — Tự động trích xuất câu hỏi từ comment (= ý tưởng video)
- [ ] **Content Gap Finder** — Chủ đề được hỏi nhiều trong comment nhưng chưa có video trả lời

#### 📅 Strategy View
- [ ] **Upload Calendar** — Visualize lịch đăng bài của các kênh
- [ ] **Best Time to Post** — Phân tích giờ đăng vs performance
- [ ] **Title Pattern Analyzer** — Nhóm tiêu đề theo pattern (số liệu, câu hỏi, how-to...)
- [ ] **Hook Analyzer** — Phân tích 30-60 giây đầu transcript

#### 🗂️ Idea Workspace
- [ ] **Idea Board** — Kanban: Ý tưởng → Đang nghiên cứu → Đã sản xuất
- [ ] **Video Bookmark** — Đánh dấu video hay + ghi chú cá nhân
- [ ] **Competitor Scorecard** — So sánh 2-3 kênh cạnh nhau

---

### 💭 Phase 3 — Advanced

- [ ] **Revenue Estimation** — Ước tính doanh thu dựa trên views × CPM theo niche
- [ ] **Evergreen Score** — Video tiếp tục tăng view sau 30 ngày
- [ ] **Weekly Digest Report** — Export PDF báo cáo tổng hợp
- [ ] **Multi-language Transcript** — Dịch transcript sang tiếng Việt
- [ ] **Batch Operations** — Chọn nhiều video, export transcript hàng loạt

---

## 7. EXPORT TRANSCRIPT FORMAT

### Format `.md` (cho AI analysis):

```
# [Video Title]
**Channel:** [Channel Name]
**Published:** [Date]
**Views:** [X] | **Duration:** [X min]
**URL:** https://youtube.com/watch?v=[id]

---

## Transcript

[00:00] Nội dung mở đầu...
[00:15] Tiếp theo...
[01:30] ...

---

## Comments (Top 50)

1. **[Username]** (👍 120): Nội dung comment...
2. **[Username]** (👍 45): ...
```

### Format `.txt` (plain text cho AI đơn giản):

```
TITLE: [Video Title]
CHANNEL: [Channel Name]
URL: https://...
DATE: [Published date]

TRANSCRIPT:
[Nội dung transcript không có timestamp]

COMMENTS:
[Danh sách comment]
```

---

## 8. ƯỚC TÍNH ĐỘ PHỨC TẠP

| Component | Độ phức tạp | Thời gian ước tính |
|-----------|-------------|-------------------|
| Channel Manager + DB | 🟢 Đơn giản | 1-2 ngày |
| YouTube API integration + Multi-key | 🟡 Trung bình | 2-3 ngày |
| youtube-transcript-api | 🟢 Đơn giản | 1 ngày |
| Dashboard UI (Tauri + React) | 🟡 Trung bình | 3-5 ngày |
| Comment crawl + basic sentiment | 🟡 Trung bình | 2 ngày |
| Alert system | 🟢 Đơn giản | 1 ngày |
| Export .md/.txt | 🟢 Đơn giản | 1 ngày |
| **Tổng MVP** | | **~2 tuần** |

---

## 9. RỦI RO CẦN LƯU Ý

| Rủi ro | Mức độ | Giải pháp |
|--------|--------|-----------|
| YouTube thay đổi API, block quota | 🔴 Cao | Multi-key rotation + cache aggressively |
| `youtube-transcript-api` bị block | 🟡 Trung bình | Fallback sang YouTube Captions API |
| Video không có transcript/caption | 🟡 Trung bình | Ghi chú "No transcript available", skip |
| SQLite chậm với 50-100 kênh x nhiều video | 🟢 Thấp | Index đúng cột, pagination |
| Tauri + Python IPC phức tạp | 🟡 Trung bình | Dùng FastAPI local server làm bridge |

---

## 10. BƯỚC TIẾP THEO

```
✅ Brainstorm — DONE
→ /plan      — Thiết kế chi tiết: Database schema, API flow, UI wireframe
→ /visualize — Thiết kế UI mockup
→ /code      — Build từng module
```

**Gợi ý thứ tự build:**
1. Setup Tauri + Python FastAPI bridge
2. Database schema + models
3. YouTube API manager + multi-key rotation
4. Channel crawler + basic dashboard
5. Transcript downloader + export (.md/.txt)
6. Comment crawler + basic sentiment
7. Alert system
8. UI polish
