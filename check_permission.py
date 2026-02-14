#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查公众号权限
"""

import requests
import json

# 配置
app_id = "wx6aef1a844a191830"
app_secret = "c0977c8ed3b815de859625e57f1b3b89"

# 获取token
url = "https://api.weixin.qq.com/cgi-bin/token"
params = {
    "grant_type": "client_credential",
    "appid": app_id,
    "secret": app_secret
}

response = requests.get(url, params=params)
token_data = response.json()

if 'access_token' not in token_data:
    print(f"获取token失败: {token_data}")
    exit(1)

token = token_data['access_token']
print(f"Token获取成功: {token[:20]}...")

# 检查接口权限
api_list = [
    ("群发接口", f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={token}"),
    ("草稿箱接口", f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"),
    ("素材管理", f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"),
]

print("\n检查接口权限：")
for name, url in api_list:
    # 尝试调用（不带实际数据，只看权限错误）
    try:
        resp = requests.post(url, json={"test": 1}, timeout=5)
        data = resp.json()
        errcode = data.get('errcode', 0)
        
        if errcode == 48001:
            status = "❌ 无权限"
        elif errcode == 40001:
            status = "✅ 有权限（参数错误，说明接口可访问）"
        else:
            status = f"? 未知 ({errcode})"
        
        print(f"  {name}: {status}")
    except Exception as e:
        print(f"  {name}: 检查失败 ({e})")

print("\n说明：")
print("48001 = 接口未授权（订阅号可能无此权限）")
print("40001 = 接口可访问，只是参数不对")
