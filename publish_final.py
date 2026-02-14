#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布完整版到微信公众号
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
from datetime import datetime

api = WechatAPI()

print("=" * 60)
print("发布完整版文章")
print("=" * 60)

today = datetime.now().strftime('%Y-%m-%d')
html_path = f"wechat_articles/{today}_wechat_final.html"

if not os.path.exists(html_path):
    print(f"错误: 文件不存在 {html_path}")
    exit(1)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"已读取: {html_path}")
print(f"内容长度: {len(content)} 字符")

# 封面图
cover_files = ["封面图.jpg", "封面图.jpeg"]
cover_path = None
for f in cover_files:
    if os.path.exists(f):
        cover_path = f
        break

thumb_media_id = ""
if cover_path:
    thumb_media_id = api.upload_thumb_media(cover_path)

# 创建草稿
title = f"【今日科技精选 | {today}】"
media_id = api.create_draft(title, content, thumb_media_id)

if media_id:
    print("\n" + "=" * 60)
    print("完整版草稿创建成功！")
    print("=" * 60)
    print(f"草稿ID: {media_id}")
    print("\n文章特点：")
    print("✓ 所有内容直接展示")
    print("✓ 老吴点评（已修改）")
    print("✓ 无阅读原文")
    print("\n请在公众号后台：")
    print("1. 进入草稿箱 → 编辑")
    print("2. 直接复制内容粘贴")
    print("3. 保存并群发")
    print("=" * 60)
else:
    print("\n草稿创建失败")
