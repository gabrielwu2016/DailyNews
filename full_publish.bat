@echo off
chcp 65001 >nul
echo ==========================================
echo    完整发布流程 - 博客 + 微信公众号
echo ==========================================
echo.
echo 本流程将自动完成：
echo   1. 生成当日科技新闻
echo   2. 更新博客网站
echo   3. 推送到GitHub Pages
echo   4. 生成微信公众号文章
echo   5. 发布到微信公众号（草稿+预览）
echo.

cd /d "%~dp0"

echo [步骤1/5] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

echo [步骤2/5] 生成博客文章...
python daily_update.py
if errorlevel 1 (
    echo ⚠️ 博客更新遇到问题，继续...
)

echo.
echo [步骤3/5] 生成公众号文章...
python wechat_publish.py
if errorlevel 1 (
    echo ⚠️ 公众号文章生成遇到问题
    pause
    exit /b 1
)

echo.
echo [步骤4/5] 安装依赖...
pip show requests >nul 2>&1
if errorlevel 1 (
    pip install requests -q
)

echo.
echo [步骤5/5] 发布到微信公众号...
set TODAY=%date:~0,4%-%date:~5,2%-%date:~8,2%
python wechat_api.py "wechat_articles\%TODAY%_wechat.html"

echo.
echo ==========================================
echo    🎉 完整发布流程完成！
echo ==========================================
echo.
echo 📱 博客地址：
echo    https://gabrielwu2016.github.io/DailyNews/
echo.
echo 💬 微信公众号：
echo    - 文章已创建为草稿
echo    - 预览已发送给管理员
echo    - 请检查手机微信确认效果
echo.
echo 📋 后续操作：
echo    1. 检查手机微信预览
echo    2. 如需修改，在公众号后台编辑
echo    3. 确认无误后点击群发
echo.
pause
