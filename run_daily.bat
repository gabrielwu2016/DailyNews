@echo off
chcp 65001 >nul
echo ==========================================
echo    极客每日精选 - 每日自动更新
echo ==========================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

echo [1/4] 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo [2/4] 正在执行每日更新脚本...
python daily_update.py

echo.
echo ==========================================
echo    更新完成！
echo ==========================================
echo.
echo 请访问 https://gabrielwu2016.github.io/DailyNews/ 查看最新内容
echo.
pause
