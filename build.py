# 静态博客构建脚本
# 将 Markdown 文件转换为 HTML

import os
import re
import markdown
from datetime import datetime
from pathlib import Path

# 配置
SOURCE_DIR = Path("source")
PUBLIC_DIR = Path("public")
POSTS_DIR = PUBLIC_DIR / "posts"

class BlogBuilder:
    def __init__(self):
        self.posts = []
        self.md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        
    def parse_frontmatter(self, content):
        """解析文章前置元数据"""
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm_text = parts[1]
                content = parts[2].strip()
                for line in fm_text.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
        return frontmatter, content
    
    def extract_summary(self, content, max_length=200):
        """提取文章摘要"""
        # 移除markdown标记
        text = re.sub(r'[#*_`\[\]()]', '', content)
        text = re.sub(r'\n+', ' ', text)
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text
    
    def get_post_info(self, md_file):
        """获取文章信息"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = self.parse_frontmatter(content)
        
        # 从文件名提取日期和slug
        filename = md_file.stem
        date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)', filename)
        
        if date_match:
            year, month, day, slug = date_match.groups()
            date = f"{year}-{month}-{day}"
        else:
            date = datetime.now().strftime('%Y-%m-%d')
            slug = filename
            
        # 提取标题
        title_match = re.search(r'^# (.+)$', body, re.MULTILINE)
        title = title_match.group(1) if title_match else slug.replace('-', ' ').title()
        
        # 提取摘要
        summary = self.extract_summary(body)
        
        # 提取标签
        tags = frontmatter.get('tags', '').split(',') if frontmatter.get('tags') else []
        tags = [t.strip() for t in tags if t.strip()]
        
        return {
            'title': title,
            'date': date,
            'slug': slug,
            'summary': summary,
            'tags': tags,
            'content': body,
            'filename': filename
        }
    
    def render_post_html(self, post):
        """渲染单篇文章HTML"""
        html_content = self.md.convert(post['content'])
        
        # 标签HTML
        tags_html = ''.join([f'<a href="/tags/{tag}.html" class="tag">#{tag}</a>' for tag in post['tags']]) if post['tags'] else ''
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post['title']} - 极客每日精选</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>极客每日精选</h1>
            <p class="tagline">每天7:30，为科技爱好者和IT从业者精选全球科技新闻</p>
        </header>
        
        <nav>
            <a href="/">首页</a>
            <a href="/archive.html">归档</a>
            <a href="/tags.html">标签</a>
            <a href="/about.html">关于</a>
        </nav>
        
        <article>
            <div class="article-meta">
                📅 {post['date']} | 
                🏷️ {tags_html}
            </div>
            
            {html_content}
            
            <a href="/" class="back-link">← 返回首页</a>
        </article>
        
        <footer>
            <p>© {datetime.now().year} 极客每日精选 | 每天 7:30 更新</p>
            <p>关注公众号，获取更多科技资讯</p>
        </footer>
    </div>
</body>
</html>'''
    
    def render_index_html(self, posts):
        """渲染首页HTML"""
        posts_html = ''
        for post in posts[:10]:  # 只显示最近10篇
            tags_html = ''.join([f'<span class="tag">#{tag}</span>' for tag in post['tags']]) if post['tags'] else ''
            posts_html += f'''
            <div class="post-item">
                <h2><a href="/posts/{post['filename']}.html">{post['title']}</a></h2>
                <div class="post-meta">
                    <span>📅 {post['date']}</span>
                    {tags_html}
                </div>
                <p class="post-excerpt">{post['summary']}</p>
            </div>
            '''
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>极客每日精选 - 科技新闻博客</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>极客每日精选</h1>
            <p class="tagline">每天7:30，为科技爱好者和IT从业者精选全球科技新闻</p>
        </header>
        
        <nav>
            <a href="/" class="active">首页</a>
            <a href="/archive.html">归档</a>
            <a href="/tags.html">标签</a>
            <a href="/about.html">关于</a>
        </nav>
        
        <div class="card">
            <h2>📰 最新文章</h2>
            <div class="post-list">
                {posts_html}
            </div>
        </div>
        
        <div class="pagination">
            <span class="current">1</span>
            <a href="/page/2.html">2</a>
            <a href="/page/2.html">下一页 →</a>
        </div>
        
        <footer>
            <p>© {datetime.now().year} 极客每日精选 | 每天 7:30 更新</p>
            <p>关注公众号，获取更多科技资讯</p>
        </footer>
    </div>
</body>
</html>'''
    
    def build(self):
        """构建整个网站"""
        print("🔨 开始构建博客...")
        
        # 确保目录存在
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # 扫描所有markdown文件
        if not SOURCE_DIR.exists():
            print(f"⚠️ 源目录不存在: {SOURCE_DIR}")
            return
            
        md_files = sorted(SOURCE_DIR.glob("*.md"), reverse=True)
        print(f"📄 找到 {len(md_files)} 篇文章")
        
        # 处理每篇文章
        for md_file in md_files:
            post = self.get_post_info(md_file)
            self.posts.append(post)
            
            # 生成HTML
            html = self.render_post_html(post)
            output_file = POSTS_DIR / f"{post['filename']}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✓ {post['filename']}.html")
        
        # 生成首页
        index_html = self.render_index_html(self.posts)
        with open(PUBLIC_DIR / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("  ✓ index.html")
        
        print(f"\n✅ 构建完成！共生成 {len(self.posts)} 篇文章")
        print(f"📂 输出目录: {PUBLIC_DIR.absolute()}")

if __name__ == "__main__":
    builder = BlogBuilder()
    builder.build()
