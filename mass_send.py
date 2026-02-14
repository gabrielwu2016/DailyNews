#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号群发脚本
⚠️ 警告：这将发送给所有订阅者！
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI

def mass_send():
    """群发给所有用户"""
    print("=" * 60)
    print("微信公众号群发")
    print("=" * 60)
    print()
    print("⚠️  警告：这将发送给所有订阅者！")
    print()
    
    # 确认
    confirm = input("确认要群发给所有用户吗？(输入 'yes' 确认): ")
    if confirm.strip().lower() != 'yes':
        print("已取消群发")
        return False
    
    # 输入草稿ID
    media_id = input("请输入草稿ID (media_id): ")
    if not media_id:
        print("错误：未提供草稿ID")
        return False
    
    print()
    print("正在群发...")
    
    api = WechatAPI()
    success = api.mass_send(media_id)
    
    if success:
        print()
        print("=" * 60)
        print("✓ 群发成功！")
        print("=" * 60)
        print("文章已发送给所有订阅者")
        return True
    else:
        print()
        print("✗ 群发失败")
        return False

if __name__ == "__main__":
    mass_send()
