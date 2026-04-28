#!/usr/bin/env python3
"""
cdp_control.py - Điều khiển Cốc Cốc (Chromium) qua Chrome DevTools Protocol (CDP)
Skill: local-coccoc-control v1.0.0

Usage:
    python cdp_control.py <action> [args...]

Actions:
    navigate <url>              - Điều hướng đến URL
    google_search <query>       - Tìm kiếm trên Google
    get_content                 - Lấy nội dung trang hiện tại
    get_search_results          - Lấy kết quả Google Search dạng JSON
    screenshot [filename]       - Chụp ảnh màn hình
    click <selector>            - Click vào element
    type <selector> <text>      - Gõ text vào element
    eval <js_code>              - Chạy JavaScript
    list_tabs                   - Liệt kê các tab đang mở
    tabs                        - Alias của list_tabs
    new_tab <url>               - Mở tab mới
    close_tab                   - Đóng tab hiện tại
    info                        - Thông tin trình duyệt hiện tại
"""

import sys
import json
import time
import base64
import urllib.request
import urllib.parse
import socket
import os

# Cấu hình mặc định
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9222
DEFAULT_TIMEOUT = 10
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def check_debug_port(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Kiểm tra xem debug port có mở không"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False


def get_tabs(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Lấy danh sách tab từ CDP"""
    try:
        url = f"http://{host}:{port}/json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return None


def get_active_tab(host=DEFAULT_HOST, port=DEFAULT_PORT, target_id=None):
    """Lấy tab đang active hoặc theo ID"""
    tabs = get_tabs(host, port)
    if not tabs:
        return None

    if target_id:
        for tab in tabs:
            if tab.get("id") == target_id:
                return tab
        return None

    # Tự động tìm tab type 'page'
    for tab in tabs:
        if tab.get("type") == "page":
            return tab
    return tabs[0] if tabs else None


def cdp_command(ws_url, method, params=None, timeout=30):
    """Gửi lệnh CDP qua WebSocket"""
    try:
        import websocket
        ws = websocket.create_connection(ws_url, timeout=timeout)
        cmd_id = int(time.time() * 1000) % 100000
        cmd = {"id": cmd_id, "method": method, "params": params or {}}
        ws.send(json.dumps(cmd))

        # Đợi response với đúng id
        start = time.time()
        while time.time() - start < timeout:
            try:
                msg = ws.recv()
                data = json.loads(msg)
                if data.get("id") == cmd_id:
                    ws.close()
                    return data
            except:
                break
        ws.close()
        return None
    except ImportError:
        return {"error": "Missing dependency 'websocket-client'. Install: pip install websocket-client"}
    except Exception as e:
        return {"error": str(e)}


def cdp_command_via_devtools_rest(method, params=None, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Fallback: thực thi lệnh qua REST API của CDP"""
    return {
        "error": (
            "REST fallback is not supported for generic CDP commands. "
            "Install websocket-client: pip install websocket-client"
        )
    }


def extract_runtime_value(response, default=None):
    """Extract Runtime.evaluate value safely."""
    if not response:
        return default
    try:
        return response.get("result", {}).get("result", {}).get("value", default)
    except Exception:
        return default


def navigate_to(url, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Điều hướng đến URL"""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab nào"}

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return {"status": "error", "message": "Không có WebSocket URL"}

    result = cdp_command(ws_url, "Page.navigate", {"url": url})
    time.sleep(2)  # Chờ trang load

    # Lấy title sau khi navigate
    title_result = cdp_command(ws_url, "Runtime.evaluate", {
        "expression": "document.title",
        "returnByValue": True
    })
    title = ""
    if title_result and "result" in title_result:
        title = title_result["result"].get("result", {}).get("value", "")

    return {
        "status": "success",
        "action": "navigate",
        "url": url,
        "title": title,
        "tab_id": tab.get("id")
    }


def extract_search_results(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Lấy kết quả tìm kiếm từ trang hiện tại (ưu tiên Google SERP)."""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return {"status": "error", "message": "Không có WebSocket URL"}

    js_extract = """
    (function() {
        var results = [];
        var searchItems = document.querySelectorAll('.g');

        searchItems.forEach(function(item, idx) {
            if (idx >= 10) return;
            var titleEl = item.querySelector('h3');
            var linkEl = item.querySelector('a');
            var snippetEl = item.querySelector('.VwiC3b, .st, [data-sncf="1"], .s');
            if (titleEl && linkEl) {
                results.push({
                    title: titleEl.textContent.trim(),
                    url: linkEl.href,
                    snippet: snippetEl ? snippetEl.textContent.trim().substring(0, 200) : ''
                });
            }
        });

        if (results.length === 0) {
            document.querySelectorAll('a[data-ved]').forEach(function(a, idx) {
                if (idx >= 15) return;
                var h3 = a.querySelector('h3');
                if (h3 && a.href && !a.href.includes('google.com/search')) {
                    results.push({
                        title: h3.textContent.trim(),
                        url: a.href,
                        snippet: ''
                    });
                }
            });
        }

        return JSON.stringify({
            title: document.title || '',
            url: location.href || '',
            count: results.length,
            results: results,
            page_text: document.body ? document.body.innerText.substring(0, 3000) : ''
        });
    })();
    """

    result = cdp_command(ws_url, "Runtime.evaluate", {
        "expression": js_extract,
        "returnByValue": True
    })

    raw_val = extract_runtime_value(result, "{}")
    try:
        search_data = json.loads(raw_val)
    except Exception:
        search_data = {"raw": raw_val}

    return {
        "status": "success",
        "action": "get_search_results",
        "title": search_data.get("title", tab.get("title", "")),
        "url": search_data.get("url", tab.get("url", "")),
        "results": search_data.get("results", []),
        "page_text": search_data.get("page_text", ""),
        "count": search_data.get("count", 0)
    }


def google_search(query, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Tìm kiếm Google"""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=vi"
    nav_result = navigate_to(search_url, host, port)
    if nav_result["status"] != "success":
        return nav_result

    time.sleep(2)  # Chờ kết quả load
    extracted = extract_search_results(host, port)
    if extracted.get("status") != "success":
        return extracted

    return {
        "status": "success",
        "action": "google_search",
        "query": query,
        "url": search_url,
        "title": nav_result.get("title", ""),
        "results": extracted.get("results", []),
        "page_text": extracted.get("page_text", ""),
        "count": extracted.get("count", 0)
    }


def click_element(selector, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Click vào element theo CSS selector."""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    selector_json = json.dumps(selector)
    js_code = f"""
    (function() {{
        var el = document.querySelector({selector_json});
        if (!el) return JSON.stringify({{ok:false, error:"selector_not_found"}});
        el.click();
        return JSON.stringify({{ok:true}});
    }})();
    """
    r = cdp_command(ws_url, "Runtime.evaluate", {"expression": js_code, "returnByValue": True})
    raw = extract_runtime_value(r, "{}")
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {"ok": False, "error": "invalid_response"}

    if not parsed.get("ok"):
        return {"status": "error", "action": "click", "selector": selector, "message": parsed.get("error", "click_failed")}
    return {"status": "success", "action": "click", "selector": selector}


def type_text(selector, text, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Gõ text vào input theo CSS selector."""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    selector_json = json.dumps(selector)
    text_json = json.dumps(text)
    js_code = f"""
    (function() {{
        var el = document.querySelector({selector_json});
        if (!el) return JSON.stringify({{ok:false, error:"selector_not_found"}});
        el.focus();
        el.value = {text_json};
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return JSON.stringify({{ok:true}});
    }})();
    """
    r = cdp_command(ws_url, "Runtime.evaluate", {"expression": js_code, "returnByValue": True})
    raw = extract_runtime_value(r, "{}")
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {"ok": False, "error": "invalid_response"}

    if not parsed.get("ok"):
        return {"status": "error", "action": "type", "selector": selector, "message": parsed.get("error", "type_failed")}
    return {"status": "success", "action": "type", "selector": selector}


def close_tab_by_id(tab_id, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Đóng tab theo tab id."""
    try:
        url = f"http://{host}:{port}/json/close/{tab_id}"
        with urllib.request.urlopen(url, timeout=5) as resp:
            raw = resp.read().decode().strip()
        return {"status": "success", "action": "close_tab", "tab_id": tab_id, "response": raw}
    except Exception as e:
        return {"status": "error", "action": "close_tab", "tab_id": tab_id, "message": str(e)}


def get_page_content(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Lấy nội dung trang hiện tại"""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    js_code = """
    (function() {
        return JSON.stringify({
            title: document.title,
            url: location.href,
            text: document.body ? document.body.innerText.substring(0, 5000) : '',
            links: Array.from(document.querySelectorAll('a[href]')).slice(0, 20).map(function(a) {
                return {text: a.textContent.trim(), href: a.href};
            })
        });
    })();
    """
    result = cdp_command(ws_url, "Runtime.evaluate", {
        "expression": js_code,
        "returnByValue": True
    })

    page_data = {}
    if result and "result" in result:
        raw_val = result["result"].get("result", {}).get("value", "{}")
        try:
            page_data = json.loads(raw_val)
        except:
            page_data = {"raw": raw_val}

    return {
        "status": "success",
        "action": "get_content",
        "title": page_data.get("title", ""),
        "url": page_data.get("url", ""),
        "text": page_data.get("text", ""),
        "links": page_data.get("links", [])
    }


def take_screenshot(filename=None, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Chụp ảnh màn hình"""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    result = cdp_command(ws_url, "Page.captureScreenshot", {"format": "png", "quality": 90})

    if not result or "result" not in result:
        return {"status": "error", "message": "Chụp ảnh thất bại"}

    image_data = result["result"].get("data", "")
    if not image_data:
        return {"status": "error", "message": "Không có dữ liệu ảnh"}

    # Lưu file
    if not filename:
        filename = f"screenshot_{int(time.time())}.png"
    filename = os.path.basename(filename)

    # Lưu vào thư mục tạm
    output_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "coccoc_screenshots")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_data))

    return {
        "status": "success",
        "action": "screenshot",
        "filepath": filepath,
        "size_kb": os.path.getsize(filepath) // 1024
    }


def evaluate_js(js_code, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Thực thi JavaScript trong trang hiện tại"""
    tab = get_active_tab(host, port)
    if not tab:
        return {"status": "error", "message": "Không tìm thấy tab"}

    ws_url = tab.get("webSocketDebuggerUrl")
    result = cdp_command(ws_url, "Runtime.evaluate", {
        "expression": js_code,
        "returnByValue": True
    })

    return {
        "status": "success",
        "action": "eval",
        "result": result.get("result", {}).get("result", {}).get("value") if result else None
    }


def list_tabs_info(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Liệt kê các tab đang mở"""
    tabs = get_tabs(host, port)
    if tabs is None:
        return {"status": "error", "message": f"Không thể kết nối đến port {port}. Hãy chạy launch_coccoc.ps1 trước."}

    tab_list = []
    for tab in tabs:
        if tab.get("type") == "page":
            tab_list.append({
                "id": tab.get("id"),
                "title": tab.get("title", ""),
                "url": tab.get("url", ""),
                "type": tab.get("type")
            })

    return {
        "status": "success",
        "action": "list_tabs",
        "total": len(tab_list),
        "tabs": tab_list
    }


def get_browser_info(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Lấy thông tin trình duyệt"""
    try:
        url = f"http://{host}:{port}/json/version"
        with urllib.request.urlopen(url, timeout=5) as resp:
            version_info = json.loads(resp.read().decode())

        active = get_active_tab(host, port)
        return {
            "status": "success",
            "action": "info",
            "browser": version_info.get("Browser", ""),
            "protocol_version": version_info.get("Protocol-Version", ""),
            "user_agent": version_info.get("User-Agent", ""),
            "debug_port": port,
            "current_tab": {
                "title": active.get("title", "") if active else "",
                "url": active.get("url", "") if active else ""
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Thiếu action. Dùng: python cdp_control.py <action> [--tab-id ID] [args]"}))
        sys.exit(1)

    # Xử lý --tab-id
    target_tab_id = None
    args = sys.argv[1:]
    if "--tab-id" in args:
        idx = args.index("--tab-id")
        if idx + 1 < len(args):
            target_tab_id = args[idx + 1]
            args.pop(idx + 1)
            args.pop(idx)

    action = args[0].lower() if args else "info"

    # Kiểm tra kết nối trước
    if not check_debug_port():
        launch_script = os.path.join(SCRIPT_DIR, "launch_coccoc.ps1")
        print(json.dumps({
            "status": "error",
            "message": f"Không thể kết nối đến Cốc Cốc trên port {DEFAULT_PORT}. Hãy chạy launch_coccoc.ps1 trước.",
            "hint": f"powershell -ExecutionPolicy Bypass -File \"{launch_script}\""
        }))
        sys.exit(1)

    result = {}

    def get_tab():
        return get_active_tab(target_id=target_tab_id)

    if action == "navigate":
        url = args[1] if len(args) > 1 else "about:blank"
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab"}
        else:
            ws_url = tab.get("webSocketDebuggerUrl")
            cdp_command(ws_url, "Page.navigate", {"url": url})
            time.sleep(2)
            result = {"status": "success", "action": "navigate", "url": url, "tab_id": tab.get("id")}

    elif action == "google_search" or action == "search":
        query = " ".join(args[1:]) if len(args) > 1 else ""
        # Google search use default logic for now as it navigates
        result = google_search(query)

    elif action == "get_search_results":
        result = extract_search_results()

    elif action == "get_content" or action == "content":
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab"}
        else:
            ws_url = tab.get("webSocketDebuggerUrl")
            js_code = """
            (function() {
                return JSON.stringify({
                    title: document.title,
                    url: location.href,
                    text: document.body ? document.body.innerText.substring(0, 5000) : ''
                });
            })();
            """
            r = cdp_command(ws_url, "Runtime.evaluate", {"expression": js_code, "returnByValue": True})
            raw = extract_runtime_value(r, "{}")
            try:
                page_data = json.loads(raw)
            except Exception:
                page_data = {"raw": raw}
            result = {"status": "success", "action": "get_content", "data": page_data}

    elif action == "screenshot":
        filename = args[1] if len(args) > 1 else f"ss_{int(time.time())}.png"
        filename = os.path.basename(filename)
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab"}
        else:
            ws_url = tab.get("webSocketDebuggerUrl")
            r = cdp_command(ws_url, "Page.captureScreenshot", {"format": "png"})
            if r and "result" in r:
                import base64
                path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), filename)
                with open(path, "wb") as f:
                    f.write(base64.b64decode(r["result"]["data"]))
                result = {"status": "success", "filepath": path}
            else:
                result = {"status": "error", "message": "Screenshot failed"}

    elif action == "eval":
        js_code = " ".join(args[1:]) if len(args) > 1 else ""
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab"}
        else:
            ws_url = tab.get("webSocketDebuggerUrl")
            r = cdp_command(ws_url, "Runtime.evaluate", {"expression": js_code, "returnByValue": True})
            result = {"status": "success", "action": "eval", "result": r.get("result", {}).get("result", {}).get("value") if r else None}

    elif action == "click":
        if len(args) < 2:
            result = {"status": "error", "message": "Thiếu selector. Dùng: click <selector>"}
        else:
            selector = args[1]
            result = click_element(selector)

    elif action == "type":
        if len(args) < 3:
            result = {"status": "error", "message": "Thiếu tham số. Dùng: type <selector> <text>"}
        else:
            selector = args[1]
            text = " ".join(args[2:])
            result = type_text(selector, text)

    elif action == "info":
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab"}
        else:
            result = {"status": "success", "action": "info", "current_tab": {"title": tab.get("title"), "url": tab.get("url"), "id": tab.get("id")}}

    elif action == "list_tabs":
        result = list_tabs_info()

    elif action == "tabs":
        result = list_tabs_info()

    elif action == "new_tab":
        url = args[1] if len(args) > 1 else "about:blank"
        tab = get_active_tab()  # Use any tab to create new one
        if tab and tab.get("webSocketDebuggerUrl"):
            ws_url = tab.get("webSocketDebuggerUrl")
            cdp_command(ws_url, "Target.createTarget", {"url": url})
            result = {"status": "success", "action": "new_tab", "url": url}
        else:
            try:
                encoded = urllib.parse.quote(url, safe=":/?&=%")
                endpoint = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}/json/new?{encoded}"
                with urllib.request.urlopen(endpoint, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                result = {"status": "success", "action": "new_tab", "url": url, "tab_id": data.get("id")}
            except Exception as e:
                result = {"status": "error", "action": "new_tab", "message": str(e)}

    elif action == "close_tab":
        tab = get_tab()
        if not tab:
            result = {"status": "error", "message": "Không tìm thấy tab để đóng"}
        else:
            result = close_tab_by_id(tab.get("id"))

    else:
        result = {"status": "error", "message": f"Không biết action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
