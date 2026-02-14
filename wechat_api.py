#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动发布脚本
支持：生成草稿、预览、群发
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path

class WechatAPI:
    def __init__(self, config_path="wechat_config.json"):
        """初始化微信公众号API"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.app_id = self.config['app_id']
        self.app_secret = self.config['app_secret']
        self.admin_wx = self.config.get('admin_wx', '')
        self.access_token = None
        self.token_expires = 0
        
    def log(self, message):
        """打印日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
        
    def get_access_token(self):
        """获取微信access_token"""
        # 检查token是否过期（提前5分钟刷新）
        if self.access_token and time.time() < self.token_expires - 300:
            return self.access_token
        
        self.log("🔄 正在获取access_token...")
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'access_token' in data:
                self.access_token = data['access_token']
                self.token_expires = time.time() + data.get('expires_in', 7200)
                self.log(f"✅ 获取access_token成功，有效期7200秒")
                return self.access_token
            else:
                self.log(f"❌ 获取token失败: {data.get('errmsg', '未知错误')}")
                return None
                
        except Exception as e:
            self.log(f"❌ 请求异常: {e}")
            return None
    
    def upload_news_image(self, image_path):
        """上传图文中的图片素材"""
        token = self.get_access_token()
        if not token:
            return None
        
        self.log(f"📤 正在上传图片: {image_path}")
        
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)
                data = response.json()
                
                if 'url' in data:
                    self.log(f"✅ 图片上传成功")
                    return data['url']
                else:
                    self.log(f"⚠️ 图片上传失败: {data.get('errmsg', '未知错误')}")
                    return None
        except Exception as e:
            self.log(f"❌ 上传异常: {e}")
            return None
    
    def upload_thumb_media(self, image_path):
        """上传缩略图素材（用于封面）"""
        token = self.get_access_token()
        if not token:
            return None
        
        self.log(f"📤 正在上传封面图片: {image_path}")
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)
                data = response.json()
                
                if 'media_id' in data:
                    self.log(f"✅ 封面上传成功, media_id: {data['media_id']}")
                    return data['media_id']
                else:
                    self.log(f"⚠️ 封面上传失败: {data.get('errmsg', '未知错误')}")
                    return None
        except Exception as e:
            self.log(f"❌ 上传异常: {e}")
            return None
    
    def create_draft(self, title, content, thumb_media_id="", author="", digest=""):
        """创建草稿"""
        token = self.get_access_token()
        if not token:
            return None
        
        self.log("📝 正在创建草稿...")
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        # 处理内容中的图片（如果有本地图片路径，需要上传）
        # 这里假设内容已经是完整的HTML
        
        data = {
            "articles": [
                {
                    "title": title,
                    "author": author or "老吴评科技",
                    "digest": digest,
                    "content": content,
                    "content_source_url": "",
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 1,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if 'media_id' in result:
                self.log(f"✅ 草稿创建成功, media_id: {result['media_id']}")
                return result['media_id']
            else:
                self.log(f"❌ 草稿创建失败: {result.get('errmsg', '未知错误')}")
                return None
                
        except Exception as e:
            self.log(f"❌ 请求异常: {e}")
            return None
    
    def preview_draft(self, media_id, towxname=""):
        """发送预览给指定用户"""
        token = self.get_access_token()
        if not token:
            return False
        
        towxname = towxname or self.admin_wx
        if not towxname:
            self.log("⚠️ 未配置管理员微信号，跳过预览")
            return False
        
        self.log(f"📱 正在发送预览给: {towxname}")
        
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/preview?access_token={token}"
        
        data = {
            "touser": towxname,
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews"
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                self.log(f"✅ 预览发送成功")
                return True
            else:
                self.log(f"⚠️ 预览发送失败: {result.get('errmsg', '未知错误')}")
                return False
                
        except Exception as e:
            self.log(f"❌ 请求异常: {e}")
            return False
    
    def mass_send(self, media_id, is_to_all=True):
        """群发给所有用户（需谨慎使用）"""
        token = self.get_access_token()
        if not token:
            return False
        
        self.log("🚀 正在群发消息...")
        
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={token}"
        
        data = {
            "filter": {
                "is_to_all": is_to_all
            },
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews",
            "send_ignore_reprint": 0
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                msg_id = result.get('msg_id')
                self.log(f"✅ 群发成功, msg_id: {msg_id}")
                return True
            else:
                self.log(f"❌ 群发失败: {result.get('errmsg', '未知错误')}")
                return False
                
        except Exception as e:
            self.log(f"❌ 请求异常: {e}")
            return False
    
    def get_draft_list(self, offset=0, count=20):
        """获取草稿列表"""
        token = self.get_access_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
        
        data = {
            "offset": offset,
            "count": count,
            "no_content": 0
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except Exception as e:
            self.log(f"❌ 获取草稿列表失败: {e}")
            return None


def publish_to_wechat(html_path, title=None, author="", digest="", thumb_image=None, preview=True, send_now=False):
    """
    发布文章到微信公众号
    
    Args:
        html_path: HTML文件路径
        title: 标题（如果不传，从HTML中提取）
        author: 作者
        digest: 摘要
        thumb_image: 封面图片路径
        preview: 是否发送预览给管理员
        send_now: 是否立即群发（⚠️谨慎使用）
    """
    print("=" * 60)
    print("🚀 微信公众号自动发布")
    print("=" * 60)
    
    # 读取HTML内容
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果未提供标题，尝试从HTML中提取
    if not title:
        import re
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else "今日科技精选"
    
    # 初始化API
    api = WechatAPI()
    
    # 上传封面图片（如果有）
    thumb_media_id = ""
    if thumb_image and os.path.exists(thumb_image):
        thumb_media_id = api.upload_thumb_media(thumb_image)
    
    # 创建草稿
    media_id = api.create_draft(title, content, thumb_media_id, author, digest)
    
    if not media_id:
        print("❌ 发布失败")
        return False
    
    # 发送预览
    if preview and api.admin_wx:
        api.preview_draft(media_id)
        print(f"\n📱 预览已发送给管理员，请检查手机微信")
    
    # 群发（如果启用）
    if send_now:
        confirm = input("\n⚠️ 确认要群发给所有用户吗？(yes/no): ")
        if confirm.lower() == 'yes':
            api.mass_send(media_id)
        else:
            print("已取消群发")
    
    print("\n" + "=" * 60)
    print("✅ 操作完成")
    print(f"📝 草稿ID: {media_id}")
    print(f"📱 公众号: {api.config.get('account_name', '未知')}")
    print("=" * 60)
    
    return media_id


if __name__ == "__main__":
    import sys
    
    # 默认发布今天的文章
    today = datetime.now().strftime('%Y-%m-%d')
    default_html = f"wechat_articles/{today}_wechat.html"
    
    html_path = sys.argv[1] if len(sys.argv) > 1 else default_html
    
    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}")
        print(f"请先生成公众号文章: python wechat_publish.py")
        exit(1)
    
    # 发布（默认只创建草稿+预览，不群发）
    publish_to_wechat(
        html_path=html_path,
        preview=True,
        send_now=False
    )
