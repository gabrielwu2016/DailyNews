@echo off
chcp 65001 >nul
echo ==========================================
echo    极客每日精选 - GitHub部署工具
echo ==========================================
echo.

set /p GITHUB_USERNAME=请输入你的GitHub用户名: 
set /p REPO_NAME=请输入仓库名称(默认: geek-daily-blog): 

if "%REPO_NAME%"=="" set REPO_NAME=geek-daily-blog

echo.
echo [步骤1/4] 创建GitHub远程仓库...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git 2>nul

echo [步骤2/4] 切换到public分支(GitHub Pages需要)...
cd public
git init
git add -A
git commit -m "Deploy to GitHub Pages"

echo [步骤3/4] 推送到GitHub...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git 2>nul
git push -f origin master:gh-pages

echo.
echo ==========================================
echo    部署完成！
echo ==========================================
echo.
echo 访问地址: https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/
echo.
echo 注意: 
echo 1. 如果首次部署，请在GitHub创建仓库: https://github.com/new
echo 2. 仓库名填: %REPO_NAME%
echo 3. 前往 Settings -^> Pages 开启GitHub Pages
echo.
pause
