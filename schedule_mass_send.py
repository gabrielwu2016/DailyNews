#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号定时群发测试
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI
from datetime import datetime

api = WechatAPI()

print("=" * 60)
print("微信公众号定时群发设置")
print("=" * 60)
print()

# 使用最新的草稿
latest_draft_id = "Xpm6nkpuIIWSfNgVaP0SofhZ4lwJiKg5gA6g8cAt0tF9dY1k2Efb1FVfaQ3mrX9X"

print(f"草稿ID: {latest_draft_id}")
print(f"标题: 【今日科技精选 | 2026-02-14】")
print()

# 选择发送时间
print("请选择发送时间:")
print("1. 立即群发")
print("2. 定时发送（5分钟后）")
print("3. 定时发送（今晚20:00）")
print("4. 自定义时间")
print()

choice = input("输入选项 (1/2/3/4): ").strip()

if choice == "1":
    send_time = "立即"
elif choice == "2":
    send_time = "5分钟后"
elif choice == "3":
    send_time = "今晚20:00"
elif choice == "4":
    send_time = input("输入时间（格式: YYYY-MM-DD HH:MM）: ")
else:
    print("无效选项")
    exit(1)

print()
print(f"发送时间: {send_time}")

# 确认
confirm = input("\n确认要群发吗？输入 'yes' 确认: ").strip()
if confirm.lower() != 'yes':
    print("已取消")
    exit(0)

# 获取token
token = api.get_access_token()
if not token:
    print("获取token失败")
    exit(1)

print(f"\n正在设置群发...")

# 如果是定时发送，需要使用不同的API
# 这里简化处理，立即群发

if choice == "1":
    # 立即群发
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
    
    import requests
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
            print("=" * 60)
        else:
            print(f"群发失败: {result.get('errmsg', '未知错误')}")
    except Exception as e:
        print(f"请求异常: {e}")
else:
    print("\n定时群发功能需要额外配置")
    print("请手动在公众号后台设置:")
    print("1. 进入草稿箱")
    print("2. 找到草稿")
    print("3. 点击群发")
    print("4. 选择定时发送")
    print(f"5. 设置时间: {send_time}")
