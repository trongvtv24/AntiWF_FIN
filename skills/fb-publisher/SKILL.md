---
name: fb-publisher
description: >
  Facebook Auto-Publisher — Tự động đăng bài lên nhiều Fanpage Facebook qua Graph API.
  Kích hoạt khi user dùng /fb-post hoặc nhắc đến đăng bài Facebook, quản lý fanpage, post scheduler.
  Tích hợp với psycho-content-engineer để tạo content + AI generate ảnh tự động.
keywords: [facebook, fanpage, post, đăng bài, graph api, queue, scheduler, auto-post]
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "fb-publisher"
skill_version: "1.0.0"
status: active
category: "content_publish"
activation: "explicit"
priority: "medium"
risk_level: "critical"
allowed_side_effects:
  - "queue_content"
  - "publish_after_confirmation"
requires_confirmation: true
related_workflows:
  - "/fb-post"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# 📢 FB Publisher Skill

## Mục đích
Cung cấp toàn bộ hạ tầng Python để tự động hóa việc đăng bài lên nhiều Facebook Fanpage:
- Quản lý queue bài viết
- Upload ảnh + text qua Facebook Graph API
- Worker loop tự động chạy theo lịch
- Logging & báo cáo kết quả

## Cấu trúc

```
fb-publisher/
├── SKILL.md              ← File này
├── config/
│   ├── fanpages.json     ← Danh sách fanpages + tokens (KHÔNG commit lên git!)
│   └── settings.json     ← Cài đặt hệ thống (interval, retry, log level...)
├── scripts/
│   ├── setup.py          ← Cài đặt ban đầu, verify token
│   ├── fb_api.py         ← Facebook Graph API wrapper
│   ├── queue_manager.py  ← CRUD queue items
│   ├── image_generator.py← Tạo & lưu ảnh AI
│   ├── worker.py         ← Main worker loop
│   └── notifier.py       ← Logging & báo cáo
└── run_worker.bat        ← Windows launcher (double-click để chạy)
```

## Data Storage

```
C:\Users\Administrator\.gemini\antigravity\data\fb-publisher\
├── queue\
│   └── posts_queue.json  ← Hàng đợi bài viết
├── images\               ← Ảnh đã generate (tự động tạo)
└── logs\
    └── publisher.log     ← Log toàn bộ hoạt động
```

## Kích hoạt

Skill này được kích hoạt tự động khi:
- User gõ `/fb-post` (bất kỳ sub-command nào)
- User nhắc đến "đăng bài fanpage", "post facebook", "lên lịch đăng"

## Yêu cầu

- Python 3.8+
- pip install requests
- Facebook App ID + App Secret + Page Access Token
- Quyền trên Page: `pages_manage_posts`, `pages_read_engagement`

## Lưu ý bảo mật

⚠️ File `config/fanpages.json` chứa Access Token — KHÔNG chia sẻ, KHÔNG commit lên git!
