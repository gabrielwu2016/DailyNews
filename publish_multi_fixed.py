#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布多篇图文到微信公众号（修复编码）
"""

import os
import json
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
from datetime import datetime

api = WechatAPI()

print("=" * 60)
print("发布多篇图文到微信公众号")
print("=" * 60)

today = datetime.now().strftime('%Y-%m-%d')
multi_dir = f"wechat_articles/multi"

# 读取发布清单
manifest_file = f"{multi_dir}/{today}_manifest.json"
if not os.path.exists(manifest_file):
    print(f"错误: 清单文件不存在 {manifest_file}")
    print("请先运行: python generate_multi.py")
    exit(1)

with open(manifest_file, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print(f"\n准备发布 {len(manifest['articles'])} 篇文章：")
for article in manifest['articles']:
    print(f"  {article['order']}. {article['title']}")

# 封面图
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
    if thumb_media_id:
        print(f"\n封面上传成功")

print("\n开始创建草稿...")

# 创建多篇图文草稿
articles_data = []
for article_info in manifest['articles']:
    with open(article_info['file'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 标题限制64字节
    title = article_info['title']
    if len(title.encode('utf-8')) > 60:
        title = title[:20]
    
    article_data = {
        "title": title,
        "author": "老吴",
        "content": content,
        "content_source_url": "",
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    
    if thumb_media_id:
        article_data["thumb_media_id"] = thumb_media_id
    
    articles_data.append(article_data)
    print(f"  已准备: {article_info['title']}")

# 创建多篇图文草稿
token = api.get_access_token()
if not token:
    print("获取token失败")
    exit(1)

import requests

url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

data = {
    "articles": articles_data
}

try:
    # 使用ensure_ascii=False保持中文，并正确设置编码
    response = requests.post(
        url,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=30
    )
    result = response.json()
    
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("多篇图文草稿创建成功！")
        print("=" * 60)
        print(f"草稿ID: {result['media_id']}")
        print(f"\n共 {len(articles_data)} 篇文章")
        print("\n请在公众号后台：")
        print("1. 进入草稿箱")
        print("2. 找到这组多篇图文")
        print("3. 检查每篇文章内容（确认中文正常）")
        print("4. 确认无误后群发")
        print("=" * 60)
    else:
        print(f"\n创建失败: {result.get('errmsg', '未知错误')}")
        
except Exception as e:
    print(f"请求异常: {e}")
