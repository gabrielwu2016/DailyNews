#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号立即群发（无交互）
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
import requests

print("=" * 60)
print("微信公众号立即群发")
print("=" * 60)
print()

# 最新草稿ID
latest_draft_id = "Xpm6nkpuIIWSfNgVaP0SofhZ4lwJiKg5gA6g8cAt0tF9dY1k2Efb1FVfaQ3mrX9X"

print(f"草稿ID: {latest_draft_id}")
print(f"标题: 【今日科技精选 | 2026-02-14】")
print()

api = WechatAPI()
token = api.get_access_token()

if not token:
    print("获取token失败")
    exit(1)

print("正在群发...")

url = f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={token}"

data = {
    "filter": {
        "is_to_all": True
    },
    "mpnews": {
        "media_id": latest_draft_id
    },
    "msgtype": "mpnews",
    "send_ignore_reprint": 0
}

try:
    response = requests.post(url, json=data, timeout=10)
    result = response.json()
    
    if result.get('errcode') == 0:
        msg_id = result.get('msg_id')
        print()
        print("=" * 60)
        print("群发成功！")
        print("=" * 60)
        print(f"消息ID: {msg_id}")
        print("文章已发送给所有订阅者")
        print()
        print("请在手机微信查看效果")
        print("检查：")
        print("1. 点击文章标题能否显示完整内容")
        print("2. 中文是否正常显示")
        print("3. 底部是否有原文链接")
        print("=" * 60)
    else:
        print(f"群发失败: {result.get('errmsg', '未知错误')}")
        print(f"错误码: {result.get('errcode')}")
        
except Exception as e:
    print(f"请求异常: {e}")
