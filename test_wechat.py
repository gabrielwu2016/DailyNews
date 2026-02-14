#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试微信公众号发布
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_api import WechatAPI

api = WechatAPI()

# 获取token测试
token = api.get_access_token()
if token:
    print("=" * 60)
    print("测试成功！")
    print("=" * 60)
    print(f"Token: {token[:20]}...")
    print("\n说明：")
    print("- AppID/AppSecret 配置正确")
    print("- IP白名单已配置")
    print("- 可以正常调用微信API")
    print("\n下一步：")
    print("1. 准备一张封面图片（建议900x500像素）")
    print("2. 放在 my-blog/cover.jpg")
    print("3. 运行: python wechat_api.py")
    print("=" * 60)
else:
    print("获取Token失败，请检查配置")
