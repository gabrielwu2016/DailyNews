@echo off
chcp 65001 >nul
echo ==========================================
echo    发布到微信公众号 - 老吴评科技
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

pip show requests >nul 2>&1
if errorlevel 1 (
    echo [2/4] 安装依赖 requests...
    pip install requests -q
)

echo [3/4] 获取今日文章...
set TODAY=%date:~0,4%-%date:~5,2%-%date:~8,2%
set HTML_FILE=wechat_articles\%TODAY%_wechat.html

if not exist "%HTML_FILE%" (
    echo ⚠️ 今日文章不存在，先生成...
    python wechat_publish.py
)

echo [4/4] 发布到微信公众号...
python wechat_api.py "%HTML_FILE%"

echo.
echo ==========================================
echo    发布流程完成！
echo ==========================================
echo.
echo 📋 说明：
echo    - 文章已创建为草稿
echo    - 预览已发送给管理员微信
echo    - 请检查手机微信预览效果
echo    - 确认无误后在公众号后台群发
echo.
pause
