# 极客每日精选 - 自建博客

一个简洁优雅的静态博客系统，专为科技新闻博客设计。

## ✨ 特性

- 🎨 现代简洁的设计风格
- 📱 完全响应式，支持移动端
- 🌙 支持系统暗色模式
- 📝 Markdown 写作支持
- ⚡ 纯静态，极速加载
- 🔍 SEO 友好

## 🚀 部署到 GitHub Pages（推荐）

### 方式一：手动部署（简单推荐）

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 仓库名填写：`geek-daily-blog`
   - 选择 **Public**（公开）
   - 点击 **Create repository**

2. **初始化本地仓库**
   ```bash
   git init
   git add -A
   git commit -m "Initial commit"
   ```

3. **关联并推送**
   ```bash
   git branch -M main
   git remote add origin https://github.com/你的用户名/geek-daily-blog.git
   git push -u origin main
   ```

4. **开启GitHub Pages**
   - 进入仓库页面 → Settings → Pages
   - Source 选择 "Deploy from a branch"
   - Branch 选择 "main"，文件夹选择 "/ (root)"
   - 点击 Save

5. **等待部署**
   - 约1-3分钟后，访问 `https://你的用户名.github.io/geek-daily-blog/`

### 方式二：运行部署脚本

```bash
deploy.bat
```
按提示输入GitHub用户名即可。

---

## 📁 目录结构

```
my-blog/
├── source/          # Markdown 文章源文件
├── public/          # 生成的静态网站（部署这个目录）
│   ├── css/         # 样式文件
│   ├── js/          # JavaScript 文件
│   ├── posts/       # 文章 HTML
│   └── index.html   # 首页
├── build.py         # 构建脚本
├── deploy.bat       # 部署脚本
└── README.md        # 本文件
```

## 📝 添加新文章

将 Markdown 文件放入 `source/` 目录，文件名格式：
```
YYYY-MM-DD-文章标题.md
```

然后运行构建：
```bash
python build.py
```

或直接创建 HTML 文件放入 `public/posts/` 目录。

## 🔧 本地预览

```bash
cd public
python -m http.server 8000
```
访问 http://localhost:8000

---

## 🤖 每日自动更新（推荐）

### 方式一：手动运行

双击运行 `run_daily.bat`，自动完成：
1. 生成当日新闻文章
2. 更新首页和归档
3. 推送到GitHub

### 方式二：设置自动定时更新

1. **右键点击** `setup_schedule.bat` → **以管理员身份运行**
2. 输入每天更新的时间（默认 7:30）
3. 完成！系统每天自动更新

#### 查看/修改定时任务
- 按 `Win + R`，输入 `taskschd.msc` 打开任务计划程序
- 找到 "极客每日精选-自动更新"
- 可修改时间、禁用或删除

### 方式三：手动执行Python脚本

```bash
python daily_update.py
```

---

## 📝 添加自定义文章

如需手动添加特定主题文章：

1. 创建Markdown文件放入 `source/` 目录
2. 文件名格式：`YYYY-MM-DD-文章标题.md`
3. 运行 `python daily_update.py` 或手动推送到GitHub

---

## 📄 许可证

MIT License
