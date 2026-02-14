@echo off
chcp 65001 >nul
echo ==========================================
echo    设置每日自动更新定时任务
echo ==========================================
echo.
echo 这将创建一个Windows定时任务，每天自动执行更新
echo.

set /p HOUR=请输入每天更新时间（小时，0-23，默认7）: 
if "%HOUR%"=="" set HOUR=7

set /p MINUTE=请输入分钟（0-59，默认30）: 
if "%MINUTE%"=="" set MINUTE=30

echo.
echo 设置每天 %HOUR%:%MINUTE% 自动更新...
echo.

REM 获取当前目录
set SCRIPT_PATH=%~dp0run_daily.bat

REM 创建定时任务
schtasks /create /tn "极客每日精选-自动更新" /tr "\"%SCRIPT_PATH%\"" /sc daily /st %HOUR%:%MINUTE% /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ 定时任务创建成功！
    echo 每天 %HOUR%:%MINUTE% 将自动更新博客
    echo.
    echo 如需修改或删除，打开任务计划程序查看
) else (
    echo.
    echo ⚠️ 创建失败，请以管理员身份运行此脚本
)

echo.
pause
