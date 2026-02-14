@echo off
chcp 65001 >nul
echo ==========================================
echo    推送博客到 GitHub
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Git状态...
git status --short

echo.
echo [2/3] 尝试推送到GitHub...
set RETRY_COUNT=0
set MAX_RETRY=5

:RETRY
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo ✅ 推送成功！
    goto SUCCESS
) else (
    set /a RETRY_COUNT+=1
    echo.
    echo ⚠️ 推送失败，第 %RETRY_COUNT% 次重试...
    if %RETRY_COUNT% lss %MAX_RETRY% (
        echo 等待 5 秒后重试...
        timeout /t 5 /nobreak >nul
        goto RETRY
    ) else (
        echo ❌ 已达到最大重试次数，推送失败
        echo.
        echo 可能的解决方案：
        echo 1. 检查网络连接
        echo 2. 使用 GitHub Desktop 手动推送
        echo 3. 稍后重试
        pause
        exit /b 1
    )
)

:SUCCESS
echo.
echo [3/3] 验证推送...
git log --oneline -1
echo.
echo ==========================================
echo    推送完成！
echo ==========================================
echo.
echo 🌐 访问地址: https://gabrielwu2016.github.io/DailyNews/
echo ⏱️  GitHub Pages 将在 1-3 分钟后自动更新
echo.
pause
