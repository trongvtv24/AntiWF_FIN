---
name: webapp-testing
description: >-
  E2E Testing toolkit cho web app bằng Playwright (Python). Tự động điều khiển
  browser để kiểm tra UI, fill form, click button, chụp screenshot, kiểm tra
  DOM. Kích hoạt khi: user yêu cầu test browser/UI/E2E, chạy /test với option
  E2E, kiểm tra tính năng web app trực quan. Keywords: playwright, e2e, browser
  test, UI test, screenshot, selenium, automation, webapp.
version: 1.0.0
source: https://github.com/anthropics/skills/tree/main/skills/webapp-testing
license: Apache-2.0
# AWF_METADATA_START
type: skill
name: "webapp-testing"
skill_version: "1.0.0"
status: active
category: "quality"
activation: "conditional"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "run_browser_tests"
  - "screenshots"
requires_confirmation: false
related_workflows:
  - "/test"
  - "/code"
  - "/deploy"
  - "/visualize"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Webapp Testing (Playwright E2E)

Skill này bổ sung khả năng **E2E browser testing** cho AWF, cho phép AI tự
điều khiển trình duyệt để test web app như người dùng thật.

## Khi nào dùng skill này?

- Unit test đã pass nhưng cần xác nhận UI hoạt động đúng
- Test luồng người dùng phức tạp (đăng nhập → thêm giỏ hàng → checkout)
- Chụp screenshot để so sánh UI trước/sau
- Debug lỗi chỉ xuất hiện trên browser
- Regression test sau khi deploy

## Yêu cầu môi trường

```bash
# Cài đặt Playwright (chỉ cần làm 1 lần)
pip install playwright
playwright install chromium
```

## Helper Scripts

Skill cung cấp 2 scripts hỗ trợ tại thư mục `scripts/` trong skill này:
- `with_server.py` — Khởi động dev server trước khi test, tắt sau khi xong
- `examples/element_discovery.py` — Khám phá elements trên trang (dùng để debug)

**Luôn chạy `--help` trước khi dùng:**
```bash
python "C:\Users\Administrator\.gemini\antigravity\skills\webapp-testing\scripts\with_server.py" --help
```

## Decision Tree: Chọn cách tiếp cận

```
Task test UI?
    ├── Static HTML file?
    │   → Đọc HTML để lấy selectors → Viết Playwright script trực tiếp
    │
    └── Dynamic web app (React/Next.js/Vue...)?
        ├── Server đã chạy?
        │   → Dùng Playwright trực tiếp, goto('http://localhost:PORT')
        │
        └── Server chưa chạy?
            → Dùng with_server.py để start server trước khi test
```

## Pattern Cơ Bản (Dùng Mọi Script)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Luôn dùng headless
    page = browser.new_page()

    # Truy cập app
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')  # QUAN TRỌNG: Chờ JS load xong

    # --- Viết test logic ở đây ---

    browser.close()
```

## Reconnaissance-Then-Action (Khám phá trước, hành động sau)

**KHÔNG** đoán mò selectors. Luôn khám phá trang trước:

```python
# Bước 1: Chụp screenshot để xem UI
page.screenshot(path='/tmp/inspect.png', full_page=True)

# Bước 2: Xem DOM
content = page.content()

# Bước 3: Liệt kê buttons, inputs
buttons = page.locator('button').all()
inputs = page.locator('input, textarea, select').all()

# Bước 4: Tìm selector đúng rồi mới tương tác
page.click('button:has-text("Đăng nhập")')
```

## Ví Dụ Test Thực Tế

### Test Form Đăng Nhập
```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:3000/login')
    page.wait_for_load_state('networkidle')

    # Fill form
    page.fill('input[name="email"]', 'test@example.com')
    page.fill('input[name="password"]', 'password123')
    page.click('button[type="submit"]')

    # Đợi redirect
    page.wait_for_url('**/dashboard')

    # Kiểm tra đăng nhập thành công
    expect(page.locator('h1')).to_contain_text('Dashboard')
    page.screenshot(path='/tmp/login_success.png')

    print("✅ Test đăng nhập: PASS")
    browser.close()
```

### Test với Server Chưa Chạy
```bash
python scripts/with_server.py \
  --server "npm run dev" --port 3000 \
  -- python my_test.py
```

### Test App Full-Stack (Backend + Frontend)
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 8000 \
  --server "cd frontend && npm run dev" --port 3000 \
  -- python my_e2e_test.py
```

## Báo Cáo Kết Quả

Sau khi test, luôn báo cáo theo format:

```
🎭 KẾT QUẢ E2E TEST (Playwright)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PASS: Test đăng nhập (1.2s)
✅ PASS: Test thêm sản phẩm vào giỏ (0.8s)
❌ FAIL: Test checkout - Không tìm thấy button "Thanh toán"

📸 Screenshots: /tmp/test_results/
📊 Tổng kết: 2/3 tests passed

Nguyên nhân FAIL: Button thanh toán có thể chưa hiển thị
do điều kiện giỏ hàng trống. Cần thêm sản phẩm trước.

→ Muốn em debug không? (/debug)
```

## Common Pitfalls (Lỗi Thường Gặp)

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| Element not found | JS chưa render xong | Thêm `wait_for_load_state('networkidle')` |
| Timeout | Server chưa chạy | Dùng `with_server.py` |
| Click không làm gì | Element bị overlay | Dùng `force=True` hoặc scroll vào view |
| Text không đúng | Encoding UTF-8 | Kiểm tra encoding file |

## Tích Hợp Với AWF Workflows

Skill này tự động kích hoạt khi:
- `/test` → User chọn option E2E hoặc Browser Test
- `/debug` → Bug chỉ xuất hiện trên UI
- `/deploy` → Smoke test trước khi deploy (verify app chạy được)

Sau khi E2E test pass → Tự động gợi ý `/deploy` hoặc `/save-brain`.
