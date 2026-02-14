@echo off
chcp 65001 >nul
echo ==========================================
echo    配置SSH推送到GitHub
echo ==========================================
echo.

cd /d "%~dp0"

echo [步骤1/3] 检查SSH密钥...
if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo ✅ SSH密钥已存在
    goto CONFIG_GIT
) else (
    echo ⚠️ SSH密钥不存在，需要生成
    goto GENERATE_KEY
)

:GENERATE_KEY
echo.
echo [步骤2/3] 生成SSH密钥...
echo 按提示操作，可以直接按回车使用默认设置
ssh-keygen -t rsa -b 4096 -C "blog@geekdaily.com"

if errorlevel 1 (
    echo ❌ 生成失败，请手动运行: ssh-keygen -t rsa -b 4096 -C "blog@geekdaily.com"
    pause
    exit /b 1
)

echo ✅ SSH密钥生成成功！

:CONFIG_GIT
echo.
echo [步骤3/3] 配置Git使用SSH...
git remote set-url origin git@github.com:gabrielwu2016/DailyNews.git

echo.
echo ==========================================
echo    配置完成！
echo ==========================================
echo.
echo ⚠️ 重要：请将SSH公钥添加到GitHub
echo.
echo 操作步骤：
echo 1. 复制以下内容：
type "%USERPROFILE%\.ssh\id_rsa.pub"
echo.
echo 2. 访问：https://github.com/settings/keys
echo 3. 点击 "New SSH key"
echo 4. 粘贴上面的内容，保存
echo.
echo 5. 然后运行：push_ssh.bat 推送代码
echo.
pause
