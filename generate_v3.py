#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成带摘要+折叠详情的微信公众号文章
- 标题、摘要、来源、分类 - 默认显示
- 详细内容 - 点击展开
- 老吴点评、互动话题 - 默认显示
"""

import os
from datetime import datetime
from pathlib import Path

today = datetime.now()
date_str = today.strftime('%Y-%m-%d')
date_display = today.strftime('%Y年%m月%d日')
weekday = ['一', '二', '三', '四', '五', '六', '日'][today.weekday()]

# 新闻数据
news_items = [
    {
        "title": "Android 17 Beta 1 正式发布",
        "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计，为2026年移动战略拉开序幕。",
        "detail": "此次更新中，Pixel启动器的搜索栏设计迎来重大变革，被描述为'上下颠倒'的设计变革，移除了之前固定不可移动的搜索栏限制。这是Google在2026年移动战略的重要一步。",
        "view": "Android 17的发布标志着Google移动战略的演进，值得关注。",
        "source": "9to5Google",
        "category": "Android"
    },
    {
        "title": "DHS向社交平台施压索取ICE批评者信息",
        "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息。",
        "detail": "据The Verge报道，DHS正在积极收集批评ICE政策的社交媒体用户信息。传票要求平台提供用户的真实身份信息，包括姓名、地址、IP地址等敏感数据，引发隐私和言论自由争议。",
        "view": "隐私问题再次成为焦点，这种针对批评者的信息收集应该引起警惕。",
        "source": "The Verge",
        "category": "隐私"
    },
    {
        "title": "Samsung Galaxy A17评测出炉",
        "summary": "三星入门级手机承诺6年Android更新，但$199价位硬件性能有限。",
        "detail": "三星入门级手机Galaxy A17承诺提供6年Android更新，但$199的售价也意味着硬件性能有限，评测质疑用户能否真正长期使用该设备。这是三星在低端市场的一次差异化尝试。",
        "view": "Samsung用长更新周期做差异化，但硬件性能是否能支撑6年使用存疑。",
        "source": "9to5Google",
        "category": "手机"
    },
    {
        "title": "Sony WH-1000XM6推出新配色",
        "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市。",
        "detail": "索尼旗舰降噪耳机WH-1000XM6新增'沙粉色'配色，在情人节前夕上市。这一配色策略既能吸引新用户，又不会让老用户觉得被背刺，是延长产品生命周期的好方法。",
        "view": "新配色策略很聪明，既能吸引新用户，又不会让老用户觉得被背刺。",
        "source": "9to5Google",
        "category": "耳机"
    },
    {
        "title": "Pokemon 30周年限量版弹珠机发布",
        "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999。",
        "detail": "Stern为庆祝Pokemon 30周年推出三款弹珠机，顶配限量版售价高达$12,999，配备精灵球拉杆、喵喵气球等主题元素，瞄准高端收藏市场。这是游戏IP商业化的极致体现。",
        "view": "Pokemon IP的粉丝经济确实强大，限量版的收藏价值可能超过使用价值。",
        "source": "The Verge",
        "category": "游戏"
    }
]

# 生成HTML
content = f"""<h1>今日科技精选（{len(news_items)}条）</h1>
<p><strong>{date_display} 星期{weekday}</strong></p>
<p>为你精选今日最值得关注的科技新闻：</p>
"""

for i, news in enumerate(news_items, 1):
    content += f"""
<p>------------------------------</p>
<h2>{i}. {news['title']}</h2>
<p><strong>来源：</strong>{news['source']} | <strong>分类：</strong>{news['category']}</p>
<p><strong>摘要：</strong>{news['summary']}</p>

<p><strong>【查看详情】</strong></p>
<p>{news['detail']}</p>

<p><strong>老吴点评：</strong>{news['view']}</p>
<p><strong>互动话题：</strong>你对这条新闻怎么看？欢迎在评论区分享观点！</p>
"""

content += """
<p>------------------------------</p>
<h3>今日小结</h3>
<p>今日科技新闻涵盖Android、隐私、消费电子等多个领域，建议持续关注行业发展趋势。</p>
<p><strong>关注「老吴评科技」，每天早上获取最新科技资讯！</strong></p>
<br/>
<p><em>觉得有用？点击右上角「···」分享给朋友</em></p>
"""

# 保存
output_dir = Path("wechat_articles")
output_dir.mkdir(exist_ok=True)

html_path = output_dir / f"{date_str}_wechat_v3.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"V3版文章已生成: {html_path}")
print(f"内容长度: {len(content)} 字符")
print(f"\n结构说明：")
print("- 标题、来源、分类 - 默认显示")
print("- 摘要 - 默认显示")
print("- 【查看详情】+ 详细内容 - 需要手动设置折叠")
print("- 老吴点评、互动话题 - 默认显示")
print(f"\n文件位置: {html_path}")
