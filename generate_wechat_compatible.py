#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微信兼容的公众号文章
只使用微信支持的基本HTML标签
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
        "source": "9to5Google",
        "category": "Android",
        "view": "Android 17的发布标志着Google移动战略的演进，值得关注。"
    },
    {
        "title": "DHS向社交平台施压索取ICE批评者信息",
        "summary": "美国国土安全部向Google、Reddit、Discord、Meta发出传票，要求提供批评ICE的账户信息，引发隐私争议。",
        "source": "The Verge",
        "category": "隐私",
        "view": "隐私问题再次成为焦点，这种针对批评者的信息收集应该引起警惕。"
    },
    {
        "title": "Samsung Galaxy A17评测出炉",
        "summary": "三星入门级手机承诺6年Android更新，但$199价位硬件性能有限，评测质疑长期实用性。",
        "source": "9to5Google",
        "category": "手机",
        "view": "Samsung用长更新周期做差异化，但硬件性能是否能支撑6年使用存疑。"
    },
    {
        "title": "Sony WH-1000XM6推出Sand Pink新配色",
        "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市，为最佳降噪耳机再添时尚选择。",
        "source": "9to5Google",
        "category": "耳机",
        "view": "新配色策略很聪明，既能吸引新用户，又不会让老用户觉得被背刺。"
    },
    {
        "title": "Pokemon 30周年限量版弹珠机发布",
        "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价$12,999，配备精灵球拉杆等主题元素。",
        "source": "The Verge",
        "category": "游戏",
        "view": "Pokemon IP的粉丝经济确实强大，限量版的收藏价值可能超过使用价值。"
    }
]

# 生成微信兼容的HTML（只使用基本标签）
content = f"""<h1>今日科技精选（{len(news_items)}条）</h1>
<p><strong>{date_display} 星期{weekday}</strong></p>
<p>为你精选今日最值得关注的科技新闻：</p>
"""

for i, news in enumerate(news_items, 1):
    content += f"""
<p>------------------------------</p>
<h2>{i}. {news['title']}</h2>
<p><strong>来源：</strong>{news['source']} | <strong>分类：</strong>{news['category']}</p>
<p>{news['summary']}</p>
<p><strong>💬 极客点评：</strong>{news['view']}</p>
<p><strong>💡 互动：</strong>你对这条新闻怎么看？欢迎在评论区分享观点！</p>
"""

content += """
<p>------------------------------</p>
<h3>今日小结</h3>
<p>今日科技新闻涵盖Android、隐私、消费电子等多个领域，建议持续关注行业发展趋势。</p>
<p><strong>关注「老吴评科技」，每天早上获取最新科技资讯！</strong></p>
<br/>
<p><em>点击右上角「···」可以分享给朋友</em></p>
"""

# 保存
output_dir = Path("wechat_articles")
output_dir.mkdir(exist_ok=True)

html_path = output_dir / f"{date_str}_wechat_fixed.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"微信兼容版文章已生成: {html_path}")
print(f"内容长度: {len(content)} 字符")
print(f"\n文章预览：")
print(content[:500] + "...")
