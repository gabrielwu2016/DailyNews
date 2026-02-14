@echo off
chcp 65001 >nul
echo ==========================================
echo    使用SSH推送到GitHub
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查SSH连接...
ssh -T git@github.com 2>&1 | findstr "successfully" >nul
if errorlevel 1 (
    echo ⚠️ SSH连接未配置，请先运行 setup_ssh.bat
    pause
    exit /b 1
)

echo ✅ SSH连接正常

echo.
echo [2/2] 推送到GitHub...
git push origin main

if errorlevel 1 (
    echo ❌ 推送失败
    echo 请检查网络连接或SSH配置
    pause
    exit /b 1
)

echo.
echo ==========================================
echo    推送成功！
echo ==========================================
echo.
echo 🌐 访问地址: https://gabrielwu2016.github.io/DailyNews/
echo ⏱️  1-3分钟后自动更新
echo.
pause
