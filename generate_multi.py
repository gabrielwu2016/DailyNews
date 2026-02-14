#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成多篇图文文章（详细版+概览版）
- 5篇详细文章（每条新闻一篇）
- 1篇概览文章（带超链接到详细文章）
"""

import os
import json
from datetime import datetime
from pathlib import Path

today = datetime.now()
date_str = today.strftime('%Y-%m-%d')
date_display = today.strftime('%Y年%m月%d日')
weekday = ['一', '二', '三', '四', '五', '六', '日'][today.weekday()]

# 新闻数据（详细版）
news_items = [
    {
        "id": 1,
        "title": "Android 17发布",
        "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计。",
        "detail": "Google于本周正式发布了Android 17的首个Beta测试版本，这比她原定计划晚了两天。此次更新中，Pixel启动器的搜索栏设计迎来重大变革，被描述为'上下颠倒'的设计变革，移除了之前固定不可移动的搜索栏限制。",
        "source": "9to5Google",
        "category": "Android",
        "view": "Android 17的发布标志着Google移动战略的演进，Pixel启动器的重新设计值得关注。",
        "url": "https://9to5google.com/"
    },
    {
        "id": 2,
        "title": "DHS索取社交平台信息",
        "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息。",
        "detail": "据The Verge报道，DHS正在积极收集批评ICE政策的社交媒体用户信息。传票要求平台提供用户的真实身份信息，包括姓名、地址、IP地址等敏感数据，引发隐私和言论自由争议。",
        "source": "The Verge",
        "category": "隐私",
        "view": "隐私问题再次成为焦点，这种针对批评者的信息收集应该引起警惕。",
        "url": "https://www.theverge.com/"
    },
    {
        "id": 3,
        "title": "三星A17评测",
        "summary": "三星入门级手机承诺6年Android更新，但$199价位硬件性能有限。",
        "detail": "三星入门级手机Galaxy A17承诺提供6年Android更新，这在同价位产品中相当罕见。但$199的售价也意味着硬件性能有限，评测质疑用户能否真正长期使用该设备。",
        "source": "9to5Google",
        "category": "手机",
        "view": "Samsung用长更新周期做差异化，但硬件性能是否能支撑6年使用存疑。",
        "url": "https://9to5google.com/"
    },
    {
        "id": 4,
        "title": "索尼耳机新配色",
        "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市。",
        "detail": "索尼旗舰降噪耳机WH-1000XM6新增'沙粉色'配色，在情人节前夕上市。这一配色策略既能吸引新用户，又不会让老用户觉得被背刺，是延长产品生命周期的好方法。",
        "source": "9to5Google",
        "category": "耳机",
        "view": "新配色策略很聪明，既能吸引新用户，又不会让老用户觉得被背刺。",
        "url": "https://9to5google.com/"
    },
    {
        "id": 5,
        "title": "Pokemon弹珠机发布",
        "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999。",
        "detail": "Stern为庆祝Pokemon 30周年推出三款弹珠机，顶配限量版售价高达$12,999，配备精灵球拉杆、喵喵气球等主题元素，瞄准高端收藏市场。",
        "source": "The Verge",
        "category": "游戏",
        "view": "Pokemon IP的粉丝经济确实强大，限量版的收藏价值可能超过使用价值。",
        "url": "https://www.theverge.com/"
    }
]

output_dir = Path("wechat_articles/multi")
output_dir.mkdir(exist_ok=True)

# 生成5篇详细文章
for news in news_items:
    # 确保标题不超过60字节
    title = news['title']
    if len(title.encode('utf-8')) > 55:
        title = title[:18] + "..."
    
    content = f"""<p><strong>{title}</strong></p>
<p>来源：{news['source']} | 分类：{news['category']}</p>
<p>时间：{date_display}</p>
<p>摘要：{news['summary']}</p>
<p>详情：{news['detail']}</p>
<p>老吴点评：{news['view']}</p>
<p>互动：你对这条新闻怎么看？欢迎评论！</p>
<p>原文：{news['url']}</p>
<p>关注「老吴评科技」获取每日科技资讯</p>
"""
    
    filename = output_dir / f"{date_str}_detail_{news['id']}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"详细文章 {news['id']}: {filename}")

# 生成概览文章（多篇图文的第1篇）
overview_content = f"""<p><strong>今日精选（{len(news_items)}条）</strong></p>
<p>{date_display} 星期{weekday}</p>
<p>为你精选今日科技新闻：</p>
"""

for news in news_items:
    overview_content += f"""
<p>--------------</p>
<p><strong>{news['id']}. {news['title']}</strong></p>
<p>来源：{news['source']} | {news['category']}</p>
<p>{news['summary']}</p>
<p>老吴点评：{news['view']}</p>
<p>（点击下方第{news['id']+1}篇文章查看详情）</p>
"""

overview_content += """
<p>--------------</p>
<p><strong>今日小结</strong></p>
<p>今日科技新闻涵盖Android、隐私、消费电子等领域。</p>
<p>关注「老吴评科技」获取每日资讯</p>
<p>点击右上角「···」可分享</p>
"""

overview_file = output_dir / f"{date_str}_overview.html"
with open(overview_file, 'w', encoding='utf-8') as f:
    f.write(overview_content)

print(f"\n概览文章: {overview_file}")

# 生成发布清单
manifest = {
    "date": date_str,
    "articles": [
        {
            "order": 1,
            "type": "overview",
            "title": f"今日精选",
            "file": str(overview_file),
            "content_type": "多篇图文第1篇"
        }
    ] + [
        {
            "order": i+2,
            "type": "detail",
            "title": news['title'],
            "file": str(output_dir / f"{date_str}_detail_{news['id']}.html"),
            "content_type": f"多篇图文第{news['id']+1}篇",
            "category": news['category']
        }
        for i, news in enumerate(news_items)
    ]
}

manifest_file = output_dir / f"{date_str}_manifest.json"
with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n发布清单: {manifest_file}")
print("\n发布说明：")
print("1. 共生成 6 篇文章（1篇概览 + 5篇详细）")
print("2. 需要在公众号后台作为【多篇图文】一起群发")
print("3. 概览文章在第1篇，详细文章在第2-6篇")
print("4. 由于订阅号每天限群发1次，这6篇会一起推送")
