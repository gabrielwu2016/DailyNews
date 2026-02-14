#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成带原文链接的微信公众号文章
"""

import os
from datetime import datetime
from pathlib import Path

today = datetime.now()
date_str = today.strftime('%Y-%m-%d')
date_display = today.strftime('%Y年%m月%d日')
weekday = ['一', '二', '三', '四', '五', '六', '日'][today.weekday()]

# 博客链接
blog_url = f"https://gabrielwu2016.github.io/DailyNews/posts/{date_str}-daily-tech-news.html"

# 新闻数据
news_items = [
    {
        "title": "Android 17 Beta 1 正式发布",
        "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计。",
        "detail": "Google于本周正式发布了Android 17的首个Beta测试版本，这比她原定计划晚了两天。此次更新中，Pixel启动器的搜索栏设计迎来重大变革，被描述为'上下颠倒'的设计变革。",
        "source": "9to5Google",
        "category": "Android",
        "view": "Android 17的发布标志着Google移动战略的演进，Pixel启动器的重新设计值得关注。"
    },
    {
        "title": "DHS向社交平台施压索取ICE批评者信息",
        "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息。",
        "detail": "据The Verge报道，DHS正在积极收集批评ICE政策的社交媒体用户信息。传票要求平台提供用户的真实身份信息，包括姓名、地址、IP地址等敏感数据。",
        "source": "The Verge",
        "category": "隐私",
        "view": "隐私问题再次成为焦点，这种针对批评者的信息收集应该引起警惕。"
    },
    {
        "title": "Samsung Galaxy A17评测出炉",
        "summary": "三星入门级手机承诺6年Android更新，但硬件性能有限。",
        "detail": "三星入门级手机Galaxy A17承诺提供6年Android更新，这在同价位产品中相当罕见。但$199的售价也意味着硬件性能有限，评测质疑用户能否真正长期使用该设备。",
        "source": "9to5Google",
        "category": "手机",
        "view": "Samsung用长更新周期做差异化，但硬件性能是否能支撑6年使用存疑。"
    },
    {
        "title": "Sony WH-1000XM6推出Sand Pink新配色",
        "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市。",
        "detail": "索尼旗舰降噪耳机WH-1000XM6新增'沙粉色'配色，在情人节前夕上市。这一配色策略既能吸引新用户，又不会让老用户觉得被背刺。",
        "source": "9to5Google",
        "category": "耳机",
        "view": "新配色策略很聪明，既能吸引新用户，又不会让老用户觉得被背刺。"
    },
    {
        "title": "Pokemon 30周年限量版弹珠机发布",
        "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999。",
        "detail": "Stern为庆祝Pokemon 30周年推出三款弹珠机，顶配限量版售价高达$12,999，配备精灵球拉杆、喵喵气球等主题元素，瞄准高端收藏市场。",
        "source": "The Verge",
        "category": "游戏",
        "view": "Pokemon IP的粉丝经济确实强大，限量版的收藏价值可能超过使用价值。"
    }
]

# 生成完整版HTML（包含详细内容）
content = f"""<h1>今日科技精选（{len(news_items)}条）</h1>
<p><strong>{date_display} 星期{weekday}</strong></p>
<p>为你精选今日最值得关注的科技新闻，点击文末「阅读原文」查看详细版：</p>
"""

for i, news in enumerate(news_items, 1):
    content += f"""
<p>------------------------------</p>
<h2>{i}. {news['title']}</h2>
<p><strong>来源：</strong>{news['source']} | <strong>分类：</strong>{news['category']}</p>
<p><strong>摘要：</strong>{news['summary']}</p>
<p><strong>详情：</strong>{news['detail']}</p>
<p><strong>💬 极客点评：</strong>{news['view']}</p>
"""

content += f"""
<p>------------------------------</p>
<h3>今日小结</h3>
<p>今日科技新闻涵盖Android、隐私、消费电子等多个领域，建议持续关注行业发展趋势。</p>
<p><strong>关注「老吴评科技」，每天早上获取最新科技资讯！</strong></p>
<br/>
<p><em>点击右上角「···」可以分享给朋友</em></p>
<br/>
<p><strong>👉 点击文末「阅读原文」查看详细版（含更多图片和链接）</strong></p>
"""

# 保存
output_dir = Path("wechat_articles")
output_dir.mkdir(exist_ok=True)

html_path = output_dir / f"{date_str}_wechat_full.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"完整版文章已生成: {html_path}")
print(f"博客链接: {blog_url}")
print(f"\n提醒：发布时请在公众号后台添加「阅读原文」链接：")
print(f"  {blog_url}")
