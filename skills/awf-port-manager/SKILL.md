---
name: awf-port-manager
description: Tự động quản lý, phát hiện xung đột và kill (diệt) các tiến trình đang chiếm dụng cổng (port) rác trên localhost.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-port-manager"
skill_version: "1.0.0"
status: active
category: "operations"
activation: "conditional"
priority: "medium"
risk_level: "high"
allowed_side_effects:
  - "inspect_ports"
  - "kill_process_after_confirmation"
requires_confirmation: true
related_workflows:
  - "/run"
  - "/debug"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Port Manager (Quản lý Port Localhost)

## 🎯 Mục đích
Skill này cấp cho AI (Antigravity) khả năng tự động xử lý các tình huống xung đột port (chẳng hạn lỗi `EADDRINUSE`), dọn dẹp các tiến trình bị treo (zombie process) đang chiếm dụng localhost một cách an toàn và nhanh chóng trên nền tảng Windows.

## ⚡ Triggers (Điều kiện kích hoạt)
Tự động kích hoạt khi:
- User thông báo lỗi liên quan đến port (ví dụ: `EADDRINUSE`, `port is already in use`, `cổng đang bận`).
- User yêu cầu trực tiếp: `kill port X`, `giải phóng port`, `check port`, `dọn dẹp port`.
- Keywords bảo mật: `port`, `EADDRINUSE`, `localhost`, `giải phóng cổng`, `kill process`.

## 🤖 Hướng dẫn thao tác cho AI (Workflow)

Khi trigger được kích hoạt, Antigravity **BẮT BUỘC** thực hiện các bước sau sử dụng tool `run_command` (Môi trường Windows PowerShell):

### Bước 1: Quét và Tìm ID Tiến Trình (PID)
Khi user muốn kiểm tra hoặc xử lý port cụ thể `<PORT_NUMBER>` (vd: 3000, 8080):
```powershell
# Cách 1: PowerShell thuần
Get-NetTCPConnection -LocalPort <PORT_NUMBER> -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Select-Object -First 1

# Cách 2: (Dự phòng) Sử dụng netstat nếu lệnh trên không có kết quả
netstat -ano | findstr LISTENING | findstr :<PORT_NUMBER>
```

### Bước 2: Nhận diện Tiến Trình
Sau khi có được `<PID>`, lấy thông tin chi tiết tên ứng dụng đang chạy trước khi ra tay:
```powershell
Get-Process -Id <PID> -ErrorAction SilentlyContinue | Select-Object Id, Name, Path
```

### Bước 3: Tiêu Diệt Tiến Trình (Trực tiếp hoặc Xin phép)
- **TH1:** Nếu user trực tiếp yêu cầu "kill port X", hãy thực thi lệnh kill, KHÔNG cần hỏi lại:
  ```powershell
  Stop-Process -Id <PID> -Force
  ```
- **TH2:** Nếu user chỉ báo lỗi (vd: "Anh chạy server bị lỗi port"), hãy hiển thị ứng dụng đang chiếm dụng và **hỏi ý kiến** xem có muốn kill nó không.

### Bước 4: 🛠 Tính năng dọn dẹp hàng loạt (Clean-up)
Nếu user ra lệnh chung chung như "dọn dẹp các port đang treo" hoặc "quản lý port", hãy kiểm tra một số cổng Dev phổ biến (3000, 3001, 5173, 8000, 8080) và báo cáo:
```powershell
$ports = @(3000, 3001, 4000, 5000, 5173, 8000, 8080, 8888);
foreach ($p in $ports) {
    $conn = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue;
    if ($conn) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue;
        Write-Output "Port $p is in use by $($proc.Name) (PID: $($proc.Id))"
    }
}
```

## 📝 Ví dụ Giao tiếp chuẩn (Tone thoại)
- **User:** "Antigravity, kill port 3000 cho anh"
- **AI thực hiện:** (Chạy ngầm lệnh tìm PID và Stop-Process)
- **AI trả lời:** "Dạ Sếp! Em đã quét và phát hiện `node.exe` đang chiếm port 3000. Em đã kill thành công để giải phóng port cho Sếp rồi ạ! 🚀"
