#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成简化版公众号文章（纯文字，无样式）
"""

import os
import json
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
        "summary": "Google发布Android 17首个测试版，Pixel启动器迎来重大重新设计。",
        "source": "9to5Google",
        "category": "Android"
    },
    {
        "title": "DHS向社交平台施压索取ICE批评者信息",
        "summary": "美国国土安全部向Google、Reddit等发出传票，要求提供批评ICE的账户信息。",
        "source": "The Verge",
        "category": "隐私"
    },
    {
        "title": "Samsung Galaxy A17评测出炉",
        "summary": "三星入门级手机承诺6年Android更新，但硬件性能有限。",
        "source": "9to5Google",
        "category": "手机"
    },
    {
        "title": "Sony WH-1000XM6推出新配色",
        "summary": "索尼旗舰降噪耳机新增沙粉色配色，情人节前夕上市。",
        "source": "9to5Google",
        "category": "耳机"
    },
    {
        "title": "Pokemon 30周年限量版弹珠机发布",
        "summary": "Stern推出Pokemon 30周年弹珠机，顶配限量版售价12999美元。",
        "source": "The Verge",
        "category": "游戏"
    }
]

# 生成简化版HTML（纯文字，无复杂样式）
content = f"""<h1>今日科技精选（{len(news_items)}条）</h1>
<p>{date_display} 星期{weekday}</p>
<hr/>
"""

for i, news in enumerate(news_items, 1):
    content += f"""
<h2>{i}. {news['title']}</h2>
<p><strong>来源：</strong>{news['source']} | <strong>分类：</strong>{news['category']}</p>
<p>{news['summary']}</p>
<p><strong>点评：</strong>值得关注的技术动态。</p>
<p><strong>互动：</strong>你对这条新闻怎么看？欢迎评论！</p>
<hr/>
"""

content += """
<h3>今日小结</h3>
<p>今日科技新闻涵盖Android、隐私、消费电子等多个领域。</p>
<p><strong>关注「老吴评科技」，每天早上获取最新科技资讯！</strong></p>
"""

# 保存
output_dir = Path("wechat_articles")
output_dir.mkdir(exist_ok=True)

html_path = output_dir / f"{date_str}_wechat_simple.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"简化版文章已生成: {html_path}")
print(f"内容长度: {len(content)} 字符")
