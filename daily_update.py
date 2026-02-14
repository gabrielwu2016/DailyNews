#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极客每日精选 - 每日自动更新脚本
功能：抓取科技新闻 → 生成文章 → 推送到GitHub Pages
"""

import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error

# 配置
CONFIG = {
    "source_dir": "source",
    "public_dir": "public",
    "posts_dir": "public/posts",
    "site_title": "极客每日精选",
    "site_tagline": "每天7:30，为科技爱好者和IT从业者精选全球科技新闻",
    "author": "极客每日精选",
    "news_sources": [
        {"name": "36氪", "url": "https://36kr.com/", "selector": "article"},
        {"name": "TechCrunch", "url": "https://techcrunch.com/", "selector": "article"},
    ]
}

class DailyBlogUpdater:
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.date_display = self.today.strftime('%Y年%m月%d日')
        self.weekday = ['一', '二', '三', '四', '五', '六', '日'][self.today.weekday()]
        
    def log(self, message):
        """打印日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
        
    def fetch_web_content(self, url, max_chars=5000):
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                # 简单提取文本
                text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
                text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:max_chars]
        except Exception as e:
            self.log(f"⚠️ 获取内容失败: {url} - {e}")
            return ""
    
    def generate_sample_news(self):
        """生成示例新闻（实际使用时应替换为真实抓取）"""
        return [
            {
                "title": f"今日科技新闻 {self.date_str}",
                "summary": "今日精选科技新闻摘要...",
                "source": "36氪",
                "url": "https://36kr.com/",
                "category": "科技"
            },
            {
                "title": "AI领域最新动态",
                "summary": "人工智能领域的最新进展...",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/",
                "category": "AI"
            }
        ]
    
    def create_markdown_article(self, news_items):
        """创建Markdown格式文章"""
        content = f"""# 📱 {self.date_display} 科技新闻合集

**发布时间：** {self.date_display} 星期{self.weekday}  
**整理：** {CONFIG['author']}

---

## 📰 今日精选新闻

"""
        for i, news in enumerate(news_items, 1):
            content += f"""
### {i}. {news['title']}

**来源：** [{news['source']}]({news['url']})  
**分类：** {news['category']}

{news['summary']}

---
"""
        
        content += f"""
## 💬 每日点评

今日科技新闻亮点总结...

## 🏷️ 标签

#科技新闻 #每日精选 #{self.date_str}

---

*本文自动整理于 {self.date_display} | 极客每日精选*
"""
        return content
    
    def save_markdown(self, content):
        """保存Markdown文件"""
        filename = f"{self.date_str}-daily-tech-news.md"
        filepath = Path(CONFIG['source_dir']) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ Markdown已保存: {filepath}")
        return filepath
    
    def create_html_article(self, news_items):
        """创建HTML格式文章"""
        news_html = ""
        for i, news in enumerate(news_items, 1):
            news_html += f"""
            <div class="news-item" style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <h3><span style="background: #3498db; color: white; padding: 3px 10px; border-radius: 12px; font-size: 14px;">{i}</span> {news['title']}</h3>
                <p><strong>来源：</strong><a href="{news['url']}" target="_blank">{news['source']}</a> | <strong>分类：</strong>{news['category']}</p>
                <p>{news['summary']}</p>
            </div>
            """
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.date_display} 科技新闻合集 - {CONFIG['site_title']}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{CONFIG['site_title']}</h1>
            <p class="tagline">{CONFIG['site_tagline']}</p>
        </header>
        
        <nav>
            <a href="/">首页</a>
            <a href="/archive.html">归档</a>
            <a href="/tags.html">标签</a>
            <a href="/about.html">关于</a>
        </nav>
        
        <article>
            <div class="article-meta">
                📅 {self.date_str} | 
                🏷️ <span class="tag">#科技新闻</span>
                <span class="tag">#每日精选</span>
            </div>
            
            <h1>📱 {self.date_display} 科技新闻合集</h1>
            
            <p>今日精选科技新闻，为您筛选最有价值的信息。</p>
            
            <hr>
            
            <h2>📰 今日精选新闻</h2>
            
            {news_html}
            
            <div class="my-view-box">
                <h3>我的看法</h3>
                <p>今日科技新闻呈现出...</p>
            </div>
            
            <a href="/" class="back-link">← 返回首页</a>
        </article>
        
        <footer>
            <p>© {self.today.year} {CONFIG['site_title']} | 每天 7:30 更新</p>
            <p>关注公众号，获取更多科技资讯</p>
        </footer>
    </div>
</body>
</html>"""
        
        filename = f"{self.date_str}-daily-tech-news.html"
        filepath = Path(CONFIG['posts_dir']) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log(f"✅ HTML已保存: {filepath}")
        return filepath
    
    def update_index(self, news_items):
        """更新首页，添加新文章链接"""
        index_path = Path(CONFIG['public_dir']) / "index.html"
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建新文章条目
        new_post = f"""
                <div class="post-item">
                    <h2><a href="/posts/{self.date_str}-daily-tech-news.html">📱 {self.date_display} 科技新闻合集</a></h2>
                    <div class="post-meta">
                        <span>📅 {self.date_str}</span>
                        <span class="tag">#科技新闻</span>
                        <span class="tag">#每日精选</span>
                    </div>
                    <p class="post-excerpt">今日精选科技新闻，为您筛选最有价值的信息...</p>
                </div>
                """
        
        # 在 post-list 开头插入新文章
        pattern = r'(<div class="post-list">)'
        replacement = r'\1' + new_post
        content = re.sub(pattern, replacement, content, count=1)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 首页已更新: {index_path}")
    
    def update_archive(self):
        """更新归档页面"""
        archive_path = Path(CONFIG['public_dir']) / "archive.html"
        
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建新归档条目
        new_entry = f"""
                <li style="padding: 10px 0; border-bottom: 1px solid #ecf0f1;">
                    <span style="color: #7f8c8d; font-size: 14px;">{self.date_str[5:]}</span>
                    <a href="/posts/{self.date_str}-daily-tech-news.html" style="margin-left: 15px; color: #333; text-decoration: none;">📱 {self.date_display} 科技新闻合集</a>
                </li>
                """
        
        # 在归档列表开头插入
        pattern = r'(<ul style="list-style: none; padding: 0;">)'
        replacement = r'\1' + new_entry
        content = re.sub(pattern, replacement, content, count=1)
        
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 归档页面已更新: {archive_path}")
    
    def git_push(self):
        """推送到GitHub"""
        try:
            # 添加所有更改
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
            
            # 提交
            commit_msg = f"Update: {self.date_display} 科技新闻"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            # 推送
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
            
            self.log(f"✅ 已推送到GitHub: {commit_msg}")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"⚠️ Git推送失败: {e}")
            return False
    
    def run(self):
        """运行完整流程"""
        self.log("=" * 50)
        self.log(f"🚀 开始每日更新: {self.date_display}")
        self.log("=" * 50)
        
        # 1. 获取新闻（示例数据，实际可替换为真实抓取）
        self.log("📰 正在获取科技新闻...")
        news_items = self.generate_sample_news()
        self.log(f"✅ 获取到 {len(news_items)} 条新闻")
        
        # 2. 创建Markdown（留档）
        self.log("📝 正在生成Markdown文章...")
        md_content = self.create_markdown_article(news_items)
        self.save_markdown(md_content)
        
        # 3. 创建HTML
        self.log("🌐 正在生成HTML页面...")
        self.create_html_article(news_items)
        
        # 4. 更新首页
        self.log("🏠 正在更新首页...")
        self.update_index(news_items)
        
        # 5. 更新归档
        self.log("📂 正在更新归档...")
        self.update_archive()
        
        # 6. 推送到GitHub
        self.log("📤 正在推送到GitHub...")
        if self.git_push():
            self.log("🎉 每日更新完成！")
            self.log(f"🌐 访问地址: https://gabrielwu2016.github.io/DailyNews/")
        else:
            self.log("❌ 推送失败，请手动检查")
        
        self.log("=" * 50)

if __name__ == "__main__":
    updater = DailyBlogUpdater()
    updater.run()
