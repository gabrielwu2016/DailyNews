#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布完整版文章到微信公众号（带原文链接）
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
from datetime import datetime

api = WechatAPI()

print("=" * 60)
print("发布完整版文章（带原文链接）")
print("=" * 60)

# 获取完整版文章路径
today = datetime.now().strftime('%Y-%m-%d')
html_path = f"wechat_articles/{today}_wechat_full.html"

if not os.path.exists(html_path):
    print(f"错误: 文件不存在 {html_path}")
    print("请先运行: python generate_wechat_full.py")
    exit(1)

# 读取HTML内容
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 博客链接（原文链接）
blog_url = f"https://gabrielwu2016.github.io/DailyNews/posts/{today}-daily-tech-news.html"

print(f"已读取文章: {html_path}")
print(f"内容长度: {len(content)} 字符")
print(f"原文链接: {blog_url}")

# 获取封面图
cover_files = ["封面图.jpg", "封面图.jpeg"]
cover_path = None
for f in cover_files:
    if os.path.exists(f):
        cover_path = f
        break

# 上传封面
thumb_media_id = ""
if cover_path:
    thumb_media_id = api.upload_thumb_media(cover_path)

# 创建草稿（带原文链接）
title = f"【今日科技精选 | {today}】"
media_id = api.create_draft(
    title=title, 
    content=content, 
    thumb_media_id=thumb_media_id,
    digest=f"今日精选5条科技新闻，点击查看详情"  # 添加摘要
)

if media_id:
    print("\n" + "=" * 60)
    print("草稿创建成功！")
    print("=" * 60)
    print(f"草稿ID: {media_id}")
    print("\n⚠️ 重要：请在公众号后台添加「阅读原文」链接：")
    print(f"  {blog_url}")
    print("\n操作步骤：")
    print("1. 进入公众号后台 → 草稿箱")
    print("2. 找到这篇文章，点击编辑")
    print("3. 底部找到「原文链接」输入框")
    print("4. 粘贴上面的博客链接")
    print("5. 保存并群发")
    print("=" * 60)
else:
    print("\n草稿创建失败")
