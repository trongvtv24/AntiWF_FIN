---
name: local-coccoc-control
description: >-
  Control the local Cốc Cốc (Chromium) browser on user's PC via Chrome DevTools Protocol (CDP).
  Uses remote debugging port to navigate, click, extract data and take screenshots.
  Keywords: coccoc, browser, local, chromium, navigate, click, extract, screenshot, research, google.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "local-coccoc-control"
skill_version: "1.0.0"
status: active
category: "browser_control"
activation: "explicit_or_intent"
priority: "medium"
risk_level: "high"
allowed_side_effects:
  - "browser_control_after_confirmation"
requires_confirmation: true
related_workflows:
  - "/brainstorm"
  - "/test"
  - "/debug"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# Local CocCoc Browser Control Skill

Skill này cho phép điều khiển trình duyệt Cốc Cốc đang chạy trên máy PC của người dùng thông qua Chrome DevTools Protocol (CDP).

## Cách hoạt động

```
[Antigravity Agent]
      │
      ▼ (run_command)
[launch_coccoc.ps1] → Khởi động Cốc Cốc + --remote-debugging-port=9222
      │
      ▼
[Cốc Cốc Process]  ←→  http://localhost:9222  ←→  [cdp_control.py]
                                                          │
                                                          ▼ (kết quả)
                                               [Antigravity Agent đọc]
```

## Điều kiện kích hoạt (Auto-activate)

Kích hoạt khi người dùng hoặc agent cần:
- Research thông tin trên web bằng tài khoản Google đã đăng nhập
- Thu thập dữ liệu từ các trang web yêu cầu đăng nhập
- Sử dụng **Profile cụ thể** của Cốc Cốc (ví dụ: Profile 53)
- Muốn thấy kết quả Google Search thực tế (không bị block)

## Cấu hình

```json
{
  "coccoc_exe": "C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe",
  "profile_path": "%LOCALAPPDATA%\\CocCoc\\Browser\\User Data",
  "profile_dir": "Profile 53",
  "debug_port": 9222,
  "scripts_dir": "%USERPROFILE%\\.gemini\\antigravity\\skills\\local-coccoc-control\\scripts"
}
```

## Workflow sử dụng Skill

### Bước 1: Kiểm tra Cốc Cốc có đang mở không

```powershell
# Kiểm tra process
Get-Process -Name "browser" -ErrorAction SilentlyContinue
```

### Bước 2: Khởi động Cốc Cốc ở chế độ Debug

Nếu Cốc Cốc chưa mở hoặc chưa có debug port:

```powershell
# Đóng tất cả instance cũ
Stop-Process -Name "browser" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Khởi động Cốc Cốc với remote debugging
& "C:\Program Files\CocCoc\Browser\Application\browser.exe" `
  --remote-debugging-port=9222 `
  --profile-directory="Profile 53" `
  --user-data-dir="C:\Users\Administrator\AppData\Local\CocCoc\Browser\User Data" `
  --no-first-run `
  --restore-last-session
```

### Bước 3: Chạy script điều khiển

```powershell
# Điều hướng đến URL
python "$env:USERPROFILE\.gemini\antigravity\skills\local-coccoc-control\scripts\cdp_control.py" navigate "https://google.com"

# Tìm kiếm Google
python "$env:USERPROFILE\.gemini\antigravity\skills\local-coccoc-control\scripts\cdp_control.py" google_search "từ khóa tìm kiếm"

# Lấy nội dung trang hiện tại
python "$env:USERPROFILE\.gemini\antigravity\skills\local-coccoc-control\scripts\cdp_control.py" get_content

# Chụp ảnh màn hình
python "$env:USERPROFILE\.gemini\antigravity\skills\local-coccoc-control\scripts\cdp_control.py" screenshot "output.png"

# Lấy kết quả Google Search (trả về JSON)
python "$env:USERPROFILE\.gemini\antigravity\skills\local-coccoc-control\scripts\cdp_control.py" get_search_results
```

## Output Format

Script trả về JSON:
```json
{
  "status": "success",
  "action": "google_search",
  "query": "...",
  "url": "https://...",
  "title": "...",
  "content": "...",
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ]
}
```

## Lỗi thường gặp & xử lý

| Lỗi | Nguyên nhân | Xử lý |
|-----|-------------|-------|
| `Connection refused port 9222` | Cốc Cốc chưa start debug mode | Chạy lại launch_coccoc.ps1 |
| `Profile is locked` | Cốc Cốc đang mở với profile đó | Đóng Cốc Cốc trước |
| `Python not found` | Python chưa cài | Cài Python 3.x |
| `Module not found: websocket` | Thiếu thư viện | `pip install websocket-client requests` |

## Cài đặt nếu chưa có

```powershell
# Cài thư viện Python cần thiết
pip install websocket-client requests pyperclip
```
