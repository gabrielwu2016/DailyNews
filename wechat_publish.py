#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动发布脚本
功能：将每日科技新闻自动发布到微信公众号
"""

import os
import re
import json
import time
from datetime import datetime
from pathlib import Path

class WechatPublisher:
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.date_display = self.today.strftime('%Y年%m月%d日')
        self.weekday = ['一', '二', '三', '四', '五', '六', '日'][self.today.weekday()]
        
    def log(self, message):
        """打印日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        try:
            print(f"[{timestamp}] {message}")
        except UnicodeEncodeError:
            # 如果控制台不支持emoji，移除emoji再打印
            clean_message = message.encode('gbk', 'ignore').decode('gbk')
            print(f"[{timestamp}] {clean_message}")
        
    def generate_wechat_article(self, news_items, my_views=None):
        """
        生成微信公众号图文内容
        
        Args:
            news_items: 新闻列表，每项包含 title, summary, source, category
            my_views: 每条新闻的点评（可选）
        """
        if my_views is None:
            my_views = ["" for _ in news_items]
        
        # 公众号标题
        title = f"【今日科技精选 | {self.date_display}】"
        
        # 公众号正文（HTML格式）
        content_html = f"""<h1 style="font-size: 22px; color: #333; margin-bottom: 20px;">📱 今日科技精选（{len(news_items)}条）</h1>
<p style="color: #888; font-size: 14px; margin-bottom: 30px;">{self.date_display} 星期{self.weekday}</p>
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
"""
        
        # 每条新闻
        for i, (news, view) in enumerate(zip(news_items, my_views), 1):
            content_html += f"""
<div style="margin: 25px 0; padding: 20px; background: #f9f9f9; border-radius: 8px;">
    <h2 style="font-size: 18px; color: #2c3e50; margin-bottom: 10px;">
        <span style="background: #3498db; color: white; padding: 2px 8px; border-radius: 4px; font-size: 14px; margin-right: 8px;">{i}</span>
        {news['title']}
    </h2>
    <p style="color: #666; font-size: 14px; margin-bottom: 10px;">
        <strong>来源：</strong>{news['source']} | <strong>分类：</strong>{news['category']}
    </p>
    <p style="color: #333; font-size: 15px; line-height: 1.8; margin-bottom: 15px;">
        {news['summary']}
    </p>
    <div style="background: #e8f4f8; padding: 12px; border-left: 4px solid #3498db; margin: 15px 0;">
        <p style="color: #555; font-size: 14px; margin: 0;"><strong>💬 极客点评：</strong>{view or '值得关注的技术动态，建议深入了解。'}</p>
    </div>
    <p style="color: #e74c3c; font-size: 14px; margin: 10px 0;">
        <strong>💡 互动话题：</strong>你对这条新闻怎么看？欢迎在评论区分享观点👇
    </p>
</div>
"""
        
        # 结尾
        content_html += f"""
<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
<div style="background: #fffbeb; padding: 20px; border-radius: 8px; text-align: center;">
    <h3 style="color: #d97706; margin-bottom: 10px;">💡 今日小结</h3>
    <p style="color: #666; font-size: 14px;">今日科技新闻涵盖{self._get_categories(news_items)}等多个领域，建议持续关注行业发展趋势。</p>
</div>
<div style="text-align: center; margin: 30px 0; padding: 20px; background: #f0f9ff; border-radius: 8px;">
    <p style="color: #3498db; font-size: 16px; margin-bottom: 10px;">📬 关注「极客每日精选」</p>
    <p style="color: #666; font-size: 14px;">每天早上7:30，为你精选全球科技新闻</p>
    <p style="color: #999; font-size: 12px; margin-top: 15px;">点击右上角「···」分享给朋友</p>
</div>
"""
        
        return {
            "title": title,
            "content": content_html,
            "digest": f"今日精选{len(news_items)}条科技新闻：{', '.join([n['title'][:15] + '...' for n in news_items[:3]])}",
            "thumb_media_id": "",  # 封面图片素材ID，需要提前上传
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }
    
    def _get_categories(self, news_items):
        """获取新闻分类列表"""
        categories = list(set([n['category'] for n in news_items]))
        return '、'.join(categories[:5])
    
    def save_wechat_article(self, article_data):
        """保存公众号文章到文件"""
        output_dir = Path("wechat_articles")
        output_dir.mkdir(exist_ok=True)
        
        # 保存HTML格式（用于复制粘贴到公众号编辑器）
        html_path = output_dir / f"{self.date_str}_wechat.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(article_data['content'])
        
        # 保存JSON格式（包含完整信息）
        json_path = output_dir / f"{self.date_str}_wechat.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        # 保存纯文本格式（用于预览）
        txt_path = output_dir / f"{self.date_str}_wechat.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"标题：{article_data['title']}\n\n")
            f.write(f"摘要：{article_data['digest']}\n\n")
            f.write("内容预览：\n")
            # 提取纯文本预览
            text_preview = re.sub(r'<[^>]+>', '', article_data['content'])
            f.write(text_preview[:500] + "...")
        
        self.log(f"✅ 公众号文章已保存：")
        self.log(f"   HTML: {html_path}")
        self.log(f"   JSON: {json_path}")
        self.log(f"   TXT:  {txt_path}")
        
        return html_path, json_path, txt_path
    
    def generate_sample_news(self):
        """生成示例新闻"""
        return [
            {
                "title": "Android 17 Beta 1 正式发布",
                "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计，为2026年移动战略拉开序幕。",
                "source": "9to5Google",
                "category": "Android"
            },
            {
                "title": "DHS向社交平台施压索取ICE批评者信息",
                "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息，引发隐私争议。",
                "source": "The Verge",
                "category": "隐私"
            },
            {
                "title": "Samsung Galaxy A17评测出炉",
                "summary": "三星入门级手机承诺6年Android更新，但$199价位硬件性能有限，评测质疑长期实用性。",
                "source": "9to5Google",
                "category": "手机"
            },
            {
                "title": "Sony WH-1000XM6推出Sand Pink新配色",
                "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市，为最佳降噪耳机再添时尚选择。",
                "source": "9to5Google",
                "category": "耳机"
            },
            {
                "title": "Pokemon 30周年限量版弹珠机发布",
                "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999，配备精灵球拉杆等主题元素。",
                "source": "The Verge",
                "category": "游戏"
            },
        ]
    
    def run(self):
        """运行完整流程"""
        self.log("=" * 60)
        self.log(f"📝 生成微信公众号文章: {self.date_display}")
        self.log("=" * 60)
        
        # 1. 获取新闻
        self.log("📰 正在获取新闻...")
        news_items = self.generate_sample_news()
        self.log(f"✅ 获取到 {len(news_items)} 条新闻")
        
        # 2. 生成点评（可以自定义）
        my_views = [
            "Android 17的发布标志着Google移动战略的演进，Pixel启动器的重新设计值得关注。",
            "隐私问题再次成为焦点，这种针对批评者的信息收集应该引起警惕。",
            "Samsung用长更新周期做差异化，但硬件性能是否能支撑6年使用存疑。",
            "新配色策略很聪明，既能吸引新用户，又不会让老用户觉得被背刺。",
            "Pokemon IP的粉丝经济确实强大，限量版的收藏价值可能超过使用价值。"
        ]
        
        # 3. 生成公众号文章
        self.log("✍️ 正在生成公众号文章...")
        article_data = self.generate_wechat_article(news_items, my_views)
        
        # 4. 保存文件
        self.log("💾 正在保存文件...")
        html_path, json_path, txt_path = self.save_wechat_article(article_data)
        
        # 5. 输出摘要
        self.log("=" * 60)
        self.log("✅ 公众号文章生成完成！")
        self.log("=" * 60)
        self.log(f"\n📋 文章信息：")
        self.log(f"   标题：{article_data['title']}")
        self.log(f"   字数：{len(article_data['content'])} 字符")
        self.log(f"   新闻数：{len(news_items)} 条")
        self.log(f"\n📂 文件位置：")
        self.log(f"   HTML（复制到公众号）：{html_path}")
        self.log(f"   JSON（程序化使用）：{json_path}")
        self.log(f"   TXT（预览）：{txt_path}")
        self.log(f"\n💡 下一步操作：")
        self.log(f"   1. 打开 {html_path}")
        self.log(f"   2. 复制全部内容")
        self.log(f"   3. 粘贴到微信公众号编辑器")
        self.log(f"   4. 添加封面图片，设置推送时间")
        self.log("=" * 60)

if __name__ == "__main__":
    publisher = WechatPublisher()
    publisher.run()
