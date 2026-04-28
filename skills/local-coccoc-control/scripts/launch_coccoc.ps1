# launch_coccoc.ps1
# Khởi động trình duyệt Cốc Cốc với Remote Debugging Port 9222
# Sử dụng Profile 53 theo yêu cầu

param(
    [string]$ProfileDir = "Profile 53",
    [int]$DebugPort = 9222,
    [string]$StartUrl = "about:blank"
)

$CandidateExePaths = @(
    (Join-Path $env:ProgramFiles "CocCoc\Browser\Application\browser.exe"),
    (Join-Path $env:LOCALAPPDATA "CocCoc\Browser\Application\browser.exe")
)
$CocCocExe = $CandidateExePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
$UserDataDir = Join-Path $env:LOCALAPPDATA "CocCoc\Browser\User Data"

# Kiểm tra file thực thi
if (-not $CocCocExe) {
    Write-Error "❌ Không tìm thấy Cốc Cốc ở các đường dẫn mặc định:"
    $CandidateExePaths | ForEach-Object { Write-Host "   - $_" }
    exit 1
}

# Kiểm tra xem debug port đã được mở chưa
$portCheck = Test-NetConnection -ComputerName "localhost" -Port $DebugPort -WarningAction SilentlyContinue 2>$null
if ($portCheck.TcpTestSucceeded) {
    Write-Host "✅ Cốc Cốc đã chạy với debug port $DebugPort. Không cần khởi động lại."
    exit 0
}

# Đóng tất cả instance Cốc Cốc đang chạy (nếu có)
$existing = Get-Process -Name "browser" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "⚠️  Đang đóng Cốc Cốc hiện tại ($($existing.Count) process)..."
    Stop-Process -Name "browser" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Đã đóng Cốc Cốc."
}

# Khởi động Cốc Cốc với debug port
Write-Host "🚀 Đang khởi động Cốc Cốc..."
Write-Host "   Profile: $ProfileDir"
Write-Host "   Debug Port: $DebugPort"

$args_list = @(
    "--remote-debugging-port=$DebugPort",
    "--profile-directory=`"$ProfileDir`"",
    "--user-data-dir=`"$UserDataDir`"",
    "--no-first-run",
    "--restore-last-session",
    "--disable-features=IsolateOrigins,site-per-process",
    $StartUrl
)

Start-Process -FilePath $CocCocExe -ArgumentList $args_list

# Chờ debug port mở (tối đa 10 giây)
$maxWait = 10
$waited = 0
Write-Host "⏳ Đang chờ Cốc Cốc khởi động..."

while ($waited -lt $maxWait) {
    Start-Sleep -Seconds 1
    $waited++
    $check = Test-NetConnection -ComputerName "localhost" -Port $DebugPort -WarningAction SilentlyContinue -InformationLevel Quiet 2>$null
    if ($check) {
        Write-Host "✅ Cốc Cốc đã sẵn sàng! Debug port $DebugPort đang hoạt động."
        Write-Host "📡 CDP endpoint: http://localhost:$DebugPort"
        exit 0
    }
    Write-Host "   Đang chờ... ($waited/$maxWait)"
}

Write-Error "❌ Timeout: Cốc Cốc không khởi động được trong $maxWait giây."
exit 1
