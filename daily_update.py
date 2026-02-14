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
        
    def generate_news_from_cron_output(self):
        """从cron工作流输出读取新闻（如果存在）"""
        cron_output_path = Path("../memory") / f"{self.date_str}.md"
        
        if cron_output_path.exists():
            self.log(f"📄 找到cron工作流输出: {cron_output_path}")
            with open(cron_output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析新闻条目
            news_items = []
            # 尝试匹配表格或列表格式的新闻
            lines = content.split('\n')
            for line in lines:
                if '|' in line and '标题' not in line and '---' not in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        news_items.append({
                            "title": parts[1].strip(),
                            "summary": parts[2].strip() if len(parts) > 2 else "",
                            "source": "36氪",
                            "url": "#",
                            "category": "科技"
                        })
            
            if news_items:
                return news_items
        
        # 如果没有cron输出，使用示例数据
        return self.generate_sample_news()
    
    def generate_sample_news(self):
        """生成示例新闻（实际使用时应替换为真实抓取）"""
        return [
            {
                "title": "Android 17 Beta 1 正式发布",
                "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计。",
                "source": "9to5Google",
                "url": "https://9to5google.com/",
                "category": "Android"
            },
            {
                "title": "DHS向社交平台施压索取ICE批评者信息",
                "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息。",
                "source": "The Verge",
                "url": "https://www.theverge.com/",
                "category": "隐私"
            },
            {
                "title": "Samsung Galaxy A17评测出炉",
                "summary": "三星入门级手机承诺6年Android更新，但硬件性能有限。",
                "source": "9to5Google",
                "url": "https://9to5google.com/",
                "category": "手机"
            },
            {
                "title": "Sony WH-1000XM6推出Sand Pink新配色",
                "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市。",
                "source": "9to5Google",
                "url": "https://9to5google.com/",
                "category": "耳机"
            },
            {
                "title": "Pokemon 30周年限量版弹珠机发布",
                "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999。",
                "source": "The Verge",
                "url": "https://www.theverge.com/",
                "category": "游戏"
            },
            {
                "title": "Motorola Razr FIFA世界杯版开售",
                "summary": "摩托罗拉推出世界杯特别版折叠屏手机，售价$699并附赠Moto Tag。",
                "source": "9to5Google",
                "url": "https://9to5google.com/",
                "category": "手机"
            },
            {
                "title": "Polymarket纽约快闪免费杂货店",
                "summary": "预测市场平台Polymarket在纽约开免费杂货店，多数排队者从未听说过该平台。",
                "source": "The Verge",
                "url": "https://www.theverge.com/",
                "category": "Web3"
            },
        ]
    
    def create_markdown_article(self, news_items):
        """创建Markdown格式文章"""
        content = f"""# 📱 {self.date_display} 科技新闻合集

**发布时间：** {self.date_display} 星期{self.weekday}  
**整理：** {CONFIG['author']}

---

## 📰 今日精选新闻（{len(news_items)}条）

"""
        for i, news in enumerate(news_items, 1):
            content += f"""### {i}. {news['title']}

**来源：** [{news['source']}]({news['url']})  
**分类：** {news['category']}

{news['summary']}

---
"""
        
        content += f"""
## 💬 每日点评

今日科技新闻涵盖Android生态、隐私安全、消费电子等多个领域。Android 17的发布预示着2026年移动战略的展开，而隐私议题再次成为焦点。

## 🏷️ 相关标签

#科技新闻 #每日精选 #Android #AI #{self.date_str}

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
            
            <p>今日精选 {len(news_items)} 条科技新闻，为您筛选最有价值的信息。</p>
            
            <hr>
            
            <h2>📰 今日精选新闻</h2>
            
            {news_html}
            
            <div class="my-view-box">
                <h3>💬 我的看法</h3>
                <p>今日科技新闻呈现出多元态势。Android生态持续演进，隐私安全问题引发关注，消费电子市场新品迭出。作为科技从业者和爱好者，保持对这些趋势的敏感度很有必要。</p>
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
                    <p class="post-excerpt">今日精选 {len(news_items)} 条科技新闻，涵盖Android、隐私、消费电子等多个领域...</p>
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
    
    def git_push(self, max_retries=5):
        """推送到GitHub，带重试机制"""
        self.log("📤 开始推送到GitHub...")
        
        for attempt in range(1, max_retries + 1):
            try:
                # 添加所有更改
                result = subprocess.run(
                    ['git', 'add', '-A'], 
                    check=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                # 检查是否有更改要提交
                status_result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    capture_output=True,
                    text=True
                )
                
                if not status_result.stdout.strip():
                    self.log("ℹ️ 没有需要提交的更改")
                    return True
                
                # 提交
                commit_msg = f"Update: {self.date_display} 科技新闻"
                result = subprocess.run(
                    ['git', 'commit', '-m', commit_msg], 
                    check=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                self.log(f"✅ 已提交: {commit_msg}")
                
                # 推送
                result = subprocess.run(
                    ['git', 'push', 'origin', 'main'], 
                    check=True, 
                    capture_output=True, 
                    text=True,
                    timeout=60
                )
                self.log(f"✅ 推送成功！")
                return True
                
            except subprocess.TimeoutExpired:
                self.log(f"⚠️ 第 {attempt}/{max_retries} 次尝试超时")
                if attempt < max_retries:
                    self.log("等待 5 秒后重试...")
                    import time
                    time.sleep(5)
                else:
                    self.log("❌ 推送失败，已达到最大重试次数")
                    return False
                    
            except subprocess.CalledProcessError as e:
                self.log(f"⚠️ 第 {attempt}/{max_retries} 次尝试失败: {e.stderr}")
                if attempt < max_retries:
                    self.log("等待 5 秒后重试...")
                    import time
                    time.sleep(5)
                else:
                    self.log("❌ 推送失败，已达到最大重试次数")
                    self.log("💡 提示：请检查网络连接或稍后手动运行 git push")
                    return False
        
        return False
    
    def run(self):
        """运行完整流程"""
        self.log("=" * 60)
        self.log(f"🚀 开始每日更新: {self.date_display}")
        self.log("=" * 60)
        
        # 1. 获取新闻
        self.log("📰 正在获取科技新闻...")
        news_items = self.generate_news_from_cron_output()
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
        success = self.git_push()
        
        self.log("=" * 60)
        if success:
            self.log("🎉 每日更新完成！")
            self.log(f"🌐 访问地址: https://gabrielwu2016.github.io/DailyNews/")
            self.log("⏱️  GitHub Pages 将在 1-3 分钟后自动更新")
        else:
            self.log("⚠️ 更新过程遇到问题，请查看上方日志")
            self.log("💡 您可以稍后手动运行: git push origin main")
        self.log("=" * 60)
        
        return success

if __name__ == "__main__":
    updater = DailyBlogUpdater()
    updater.run()
