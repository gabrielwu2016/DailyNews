#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用简化版HTML重新发布到微信公众号
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
from datetime import datetime

api = WechatAPI()

print("=" * 60)
print("重新发布文章（微信兼容版）")
print("=" * 60)

# 获取简化版文章路径
today = datetime.now().strftime('%Y-%m-%d')
html_path = f"wechat_articles/{today}_wechat_fixed.html"

if not os.path.exists(html_path):
    print(f"错误: 文件不存在 {html_path}")
    exit(1)

# 读取HTML内容
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"已读取文章: {html_path}")
print(f"内容长度: {len(content)} 字符")

# 获取封面图
cover_files = ["封面图.jpg", "封面图.jpeg", "cover.jpg", "cover.jpeg"]
cover_path = None
for f in cover_files:
    if os.path.exists(f):
        cover_path = f
        print(f"使用封面图: {cover_path}")
        break

# 上传封面
thumb_media_id = ""
if cover_path:
    thumb_media_id = api.upload_thumb_media(cover_path)
    if thumb_media_id:
        print(f"封面上传成功")

# 创建草稿
title = f"【今日科技精选 | {today}】"
media_id = api.create_draft(title, content, thumb_media_id)

if media_id:
    print("\n" + "=" * 60)
    print("草稿创建成功！")
    print("=" * 60)
    print(f"标题: {title}")
    print(f"草稿ID: {media_id}")
    print("\n请在公众号后台查看")
    print("1. 访问 mp.weixin.qq.com")
    print("2. 进入草稿箱")
    print("3. 检查文章是否显示完整")
    print("=" * 60)
else:
    print("\n草稿创建失败")
