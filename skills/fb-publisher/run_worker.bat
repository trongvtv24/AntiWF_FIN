@echo off
chcp 65001 >nul
title FB Publisher — Facebook Auto-Publisher

SET SCRIPTS_DIR=%~dp0scripts
SET PYTHONPATH=%SCRIPTS_DIR%

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   📢 FACEBOOK AUTO-PUBLISHER                    ║
echo  ║   Powered by Psycho-Content-Engineer            ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  Chọn chế độ:
echo.
echo  [1] 🔍 Verify Setup ^(kiểm tra token, config^)
echo  [2] 📝 Fill Queue ^(tạo nội dung vào hàng đợi^)
echo  [3] 👀 Preview Content ^(xem nội dung sẽ tạo^)
echo  [4] 📋 Xem Queue Status
echo  [5] 🤖 Chạy Worker AUTO ^(đăng theo lịch + auto-fill^)
echo  [6] ⚡ Đăng Ngay ^(post-now tất cả pending^)
echo  [7] 🔍 Dry Run ^(test, không đăng thật^)
echo  [8] 🔄 Retry Bài Lỗi
echo  [9] ❌ Thoát
echo.
set /p choice=  Nhập số [1-9]: 

if "%choice%"=="1" goto verify
if "%choice%"=="2" goto fill
if "%choice%"=="3" goto preview
if "%choice%"=="4" goto status
if "%choice%"=="5" goto auto
if "%choice%"=="6" goto now
if "%choice%"=="7" goto dryrun
if "%choice%"=="8" goto retry
if "%choice%"=="9" goto end

echo  ❌ Lựa chọn không hợp lệ!
pause
goto end

:verify
echo.
echo  🔍 Đang verify setup...
cd /d "%SCRIPTS_DIR%"
python setup_verify.py
pause
goto end

:fill
echo.
echo  📝 Đang fill queue...
cd /d "%SCRIPTS_DIR%"
python content_bridge.py --run
pause
goto end

:preview
echo.
echo  👀 Preview content...
cd /d "%SCRIPTS_DIR%"
python content_bridge.py --preview
pause
goto end

:status
echo.
echo  📋 Queue Status...
cd /d "%SCRIPTS_DIR%"
python queue_manager.py --summary
echo.
python queue_manager.py --list
pause
goto end

:auto
echo.
echo  🤖 Khởi động Worker AUTO MODE...
echo  Nhấn Ctrl+C để dừng.
echo.
cd /d "%SCRIPTS_DIR%"
python worker.py --mode auto
pause
goto end

:now
echo.
echo  ⚡ Đang đăng ngay tất cả bài pending...
cd /d "%SCRIPTS_DIR%"
python worker.py --mode now
pause
goto end

:dryrun
echo.
echo  🔍 Chạy Dry Run (không đăng thật)...
cd /d "%SCRIPTS_DIR%"
python worker.py --mode dry-run
pause
goto end

:retry
echo.
echo  🔄 Reset bài lỗi về pending...
cd /d "%SCRIPTS_DIR%"
python queue_manager.py --retry
pause
goto end

:end
echo.
echo  👋 Tạm biệt!
timeout /t 2 >nul
