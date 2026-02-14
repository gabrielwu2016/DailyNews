@echo off
cd /d "%~dp0"

echo ==========================================
echo 发布到微信公众号 - 老吴评科技
echo ==========================================
echo.

echo [1/4] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

echo [2/4] 安装依赖...
pip show requests >nul 2>&1
if errorlevel 1 (
    pip install requests
)

echo [3/4] 检查文章...
set TODAY=%date:~0,4%-%date:~5,2%-%date:~8,2%
set HTML_FILE=wechat_articles\%TODAY%_wechat.html

if not exist "%HTML_FILE%" (
    echo 文章不存在，生成中...
    python wechat_publish.py
)

echo [4/4] 发布到公众号...
python wechat_api.py "%HTML_FILE%"

echo.
echo ==========================================
echo 发布完成！
echo ==========================================
echo.
echo 请检查手机微信预览
echo.
pause
