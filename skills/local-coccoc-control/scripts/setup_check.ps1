# setup_check.ps1
# Kiểm tra môi trường và cài đặt các thư viện cần thiết

Write-Host "=== Local CocCoc Control - Setup Check ===" -ForegroundColor Cyan
Write-Host ""

$allOk = $true

# 1. Kiểm tra Cốc Cốc
Write-Host "1. Kiểm tra Cốc Cốc..." -NoNewline
$candidatePaths = @(
    (Join-Path $env:ProgramFiles "CocCoc\Browser\Application\browser.exe"),
    (Join-Path $env:LOCALAPPDATA "CocCoc\Browser\Application\browser.exe")
)
$coccoc = $candidatePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($coccoc) {
    Write-Host " ✅ OK" -ForegroundColor Green
    Write-Host "   Path: $coccoc"
} else {
    Write-Host " ❌ KHÔNG TÌM THẤY" -ForegroundColor Red
    Write-Host "   Đã kiểm tra:"
    $candidatePaths | ForEach-Object { Write-Host "   - $_" }
    $allOk = $false
}

# 2. Kiểm tra Python
Write-Host ""
Write-Host "2. Kiểm tra Python..." -NoNewline
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅ OK" -ForegroundColor Green
    Write-Host "   $pythonVersion"
} else {
    Write-Host " ❌ KHÔNG TÌM THẤY" -ForegroundColor Red
    Write-Host "   Cài Python tại: https://www.python.org/downloads/"
    $allOk = $false
}

# 3. Kiểm tra thư viện websocket-client
Write-Host ""
Write-Host "3. Kiểm tra thư viện websocket-client..." -NoNewline
$wsCheck = python -c "import websocket; print(websocket.__version__)" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅ OK ($wsCheck)" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Chưa cài" -ForegroundColor Yellow
    Write-Host "   Đang cài đặt..."
    pip install websocket-client --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Đã cài xong websocket-client" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Cài đặt thất bại" -ForegroundColor Red
        $allOk = $false
    }
}

# 4. Kiểm tra thư viện requests
Write-Host ""
Write-Host "4. Kiểm tra thư viện requests..." -NoNewline
$reqCheck = python -c "import requests; print(requests.__version__)" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅ OK ($reqCheck)" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Chưa cài" -ForegroundColor Yellow
    Write-Host "   Đang cài đặt..."
    pip install requests --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Đã cài xong requests" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Cài đặt thất bại" -ForegroundColor Red
        $allOk = $false
    }
}

# 5. Kiểm tra kết nối debug port
Write-Host ""
Write-Host "5. Kiểm tra Cốc Cốc debug port (9222)..." -NoNewline
$portCheck = Test-NetConnection -ComputerName "localhost" -Port 9222 -WarningAction SilentlyContinue -InformationLevel Quiet 2>$null
if ($portCheck) {
    Write-Host " ✅ OK - Cốc Cốc đang chạy debug mode" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Chưa mở" -ForegroundColor Yellow
    Write-Host "   Cần chạy launch_coccoc.ps1 để mở Cốc Cốc ở chế độ debug"
}

# 6. Kiểm tra Profile 53
Write-Host ""
Write-Host "6. Kiểm tra Profile 53..." -NoNewline
$profilePath = Join-Path $env:LOCALAPPDATA "CocCoc\Browser\User Data\Profile 53"
if (Test-Path $profilePath) {
    Write-Host " ✅ OK" -ForegroundColor Green
    Write-Host "   Path: $profilePath"
} else {
    Write-Host " ❌ KHÔNG TÌM THẤY" -ForegroundColor Red
    Write-Host "   Kiểm tra lại đường dẫn profile"
    $allOk = $false
}

Write-Host ""
Write-Host "=== Kết quả ===" -ForegroundColor Cyan
if ($allOk) {
    Write-Host "✅ Tất cả điều kiện OK! Skill sẵn sàng sử dụng." -ForegroundColor Green
    Write-Host ""
    Write-Host "Để sử dụng:"
    Write-Host "  1. Chạy: .\launch_coccoc.ps1"
    Write-Host "  2. Sau đó: python cdp_control.py info"
} else {
    Write-Host "⚠️  Một số điều kiện chưa đáp ứng. Hãy khắc phục theo hướng dẫn trên." -ForegroundColor Yellow
}
