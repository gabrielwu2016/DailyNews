@echo off
chcp 65001 >nul
echo ==========================================
echo    生成微信公众号文章
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo [2/2] 正在生成公众号文章...
python wechat_publish.py

echo.
echo ==========================================
echo    生成完成！
echo ==========================================
echo.
echo 💡 下一步：
echo 1. 打开 wechat_articles/ 文件夹
echo 2. 找到今天的 HTML 文件
echo 3. 复制内容到微信公众号编辑器
echo 4. 添加封面图片，设置推送
echo.
pause
