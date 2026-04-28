"""
Example: Khám phá elements trên một trang web.
Dùng script này để debug hoặc tìm đúng selectors trước khi viết test thật.

Cách chạy:
    python examples/element_discovery.py

Source: anthropics/skills (Apache-2.0)
"""
from playwright.sync_api import sync_playwright

URL = 'http://localhost:3000'  # Thay URL của project

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL)
    page.wait_for_load_state('networkidle')

    # Khám phá buttons
    buttons = page.locator('button').all()
    print(f"Found {len(buttons)} buttons:")
    for i, btn in enumerate(buttons):
        text = btn.inner_text() if btn.is_visible() else "[hidden]"
        print(f"  [{i}] '{text}'")

    # Khám phá links
    links = page.locator('a[href]').all()
    print(f"\nFound {len(links)} links:")
    for link in links[:5]:
        text = link.inner_text().strip()
        href = link.get_attribute('href')
        print(f"  - '{text}' -> {href}")

    # Khám phá input fields
    inputs = page.locator('input, textarea, select').all()
    print(f"\nFound {len(inputs)} input fields:")
    for inp in inputs:
        name = inp.get_attribute('name') or inp.get_attribute('id') or "[unnamed]"
        itype = inp.get_attribute('type') or 'text'
        print(f"  - {name} ({itype})")

    # Chụp screenshot để xem UI
    screenshot_path = '/tmp/page_discovery.png'
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"\n📸 Screenshot saved: {screenshot_path}")

    browser.close()
