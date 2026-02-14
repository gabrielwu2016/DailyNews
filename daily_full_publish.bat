@echo off
chcp 65001 >nul
echo ==========================================
echo    极客每日精选 - 完整每日发布流程
echo ==========================================
echo.
echo 本脚本将自动完成：
echo   1. 生成当日科技新闻
echo   2. 更新博客网站
echo   3. 推送到GitHub Pages
echo   4. 生成微信公众号文章
echo.

cd /d "%~dp0"

echo [1/5] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

echo [2/5] 生成博客文章并推送到GitHub...
python daily_update.py
if errorlevel 1 (
    echo ⚠️ 博客更新遇到问题，继续生成公众号文章...
)

echo.
echo [3/5] 生成微信公众号文章...
python wechat_publish.py
if errorlevel 1 (
    echo ⚠️ 公众号文章生成遇到问题
    pause
    exit /b 1
)

echo.
echo [4/5] 检查生成的文件...
if exist "wechat_articles\*.html" (
    echo ✅ 公众号文章已生成
    dir /b wechat_articles\*.html
) else (
    echo ⚠️ 未找到公众号文章文件
)

echo.
echo ==========================================
echo    每日发布完成！
echo ==========================================
echo.
echo 📱 博客地址：
echo    https://gabrielwu2016.github.io/DailyNews/
echo.
echo 💬 公众号文章位置：
echo    wechat_articles/ 文件夹
echo.
echo 📋 下一步操作：
echo    1. 打开 wechat_articles/ 文件夹
echo    2. 找到今天的 HTML 文件
echo    3. 复制内容到微信公众号后台
echo    4. 添加封面图片，预览后推送
echo.
pause
