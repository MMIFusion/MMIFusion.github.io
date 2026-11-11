"""The full dataset library, rendered inside the shared MMIFusion website."""
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
ITEMS = json.loads((ROOT/'data/datasets.json').read_text())
CATEGORIES = list(dict.fromkeys(d['category'] for d in ITEMS))
SHORT_CATEGORIES = ['红外与可见光','多聚焦图像融合','多曝光图像融合','遥感与光谱图像','医学与显微图像','其他模态与任务']
E = lambda value: html.escape(str(value), quote=True)

def external(url, label, css='text-link'):
    return f'<a class="{css}" href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(label)} ↗</a>'

def profile(item):
    fields = [('研究方向',item['category']),('适用任务',item['tagsOriginal'] or item['task']),
        ('论文题目',item['paper']),('团队与作者',item['team']),('发表信息',item['publication'])]
    if item['status'] != '见原文说明': fields.append(('开放状态',item['status']+'（按原文标注）'))
    attributes = ''.join(f'<dt>{label}</dt><dd>{E(value)}</dd>' for label,value in fields)
    links = ''.join(external(link['url'],link['label'],'button secondary') for link in item['links'])
    notes = ''.join(f'<dt>{E(label)}</dt><dd>{E(value)}</dd>' for label,value in item['linkNotes'].items())
    figures = ''.join(f'<figure><a href="{E(image["src"])}" target="_blank" rel="noopener noreferrer" aria-label="打开 {E(item["name"])} 第 {i+1} 张原图"><img src="{E(image["src"])}" alt="{E(item["name"])} 原始示例图 {i+1}" loading="lazy" decoding="async"></a><figcaption>示例图 {i+1} · 点击查看原图{(" · "+external(image["source"],"图片来源")) if image.get("source") else ""}</figcaption></figure>' for i,image in enumerate(item['images']))
    feedback = 'contribute.html?'+urlencode({'type':'内容勘误','title':item['name']+' 数据资源勘误',
        'source':item['links'][0]['url'] if item['links'] else 'https://mmifusion.github.io/datasets.html#dataset='+item['id']})
    return f'''<div class="dataset-profile"><div class="dataset-profile-links">{links}</div><dl class="dataset-fields">{attributes}</dl><h3>完整介绍</h3><p class="dataset-description">{E(item['description'])}</p>{('<details class="dataset-link-notes"><summary>链接与下载补充说明</summary><dl class="dataset-fields">'+notes+'</dl></details>') if notes else ''}<div class="dataset-figures">{figures}</div><p class="dataset-source-note">规模、划分、发表信息、开放状态与使用许可，请以原论文和官方说明为准。本站提供资源索引；原图与数据版权归各自作者所有。</p><div class="dataset-profile-footer"><a href="papers.html?{E(urlencode({'q':item['name']}))}" class="text-link">搜索相关解读 →</a><a href="{E(feedback)}" class="text-link">反馈条目信息 →</a></div></div>'''

def card(item, index):
    identity = E(item['id'])
    searchable = ' '.join(str(item.get(k,'')) for k in ['name','title','category','task','tagsOriginal','paper','team','description','publication'])
    match = re.search(r'(?:19|20)\d{2}',item['publication'])
    year = match.group() if match else '0'
    excerpt = item['description'][:150]+('…' if len(item['description'])>150 else '')
    picture = (f'<img src="{E(item["images"][0]["src"])}" alt="{E(item["name"])} 数据资源示例图" loading="lazy" decoding="async">' if item['images'] else f'<span class="dataset-no-image"><span>DATASET / {index+1:03}</span><strong>{E(item["name"])}</strong><small>完整说明见资源档案</small></span>')
    links = ''.join(external(link['url'],link['label']) for link in item['links'])
    status = f'<span class="dataset-status">{E(item["status"])}</span>' if item['status']!='见原文说明' else ''
    return f'''<article class="catalog-card" data-dataset-id="{identity}" data-name="{E(item['name'])}" data-title="{E(item['title'])}" data-order="{index}" data-year="{year}" data-category="{item['categoryIndex']}" data-task="{E(item['task'])}" data-search="{E(searchable)}"><div class="catalog-card-main"><div class="catalog-card-meta"><span>{E(item['task'])}</span><span>{E(item['publication'])}</span>{status}</div><h3><a href="#dataset={identity}" data-dataset-open="{identity}">{E(item['name'])}<span aria-hidden="true">↗</span></a></h3><p class="catalog-card-paper">{E(item['paper'])}</p><p class="catalog-card-description">{E(excerpt)}</p><div class="catalog-card-links">{links}<a class="text-link" href="#dataset={identity}" data-dataset-open="{identity}">完整介绍 →</a></div></div><a class="catalog-card-image" href="#dataset={identity}" data-dataset-open="{identity}" aria-label="查看 {E(item['name'])} 完整介绍">{picture}</a><details class="catalog-inline-detail" id="dataset={identity}"><summary>展开完整档案 · {E(item['name'])}</summary>{profile(item)}</details></article>'''

def page():
    counts = Counter(d['categoryIndex'] for d in ITEMS)
    category_buttons = f'<button type="button" data-dataset-category="" aria-pressed="true"><span>全部资源</span><b>{len(ITEMS)}</b></button>'
    category_buttons += ''.join(f'<button type="button" data-dataset-category="{i}" aria-pressed="false" title="{E(category)}"><span>{SHORT_CATEGORIES[i]}</span><b>{counts[i]}</b></button>' for i,category in enumerate(CATEGORIES))
    cards = ''.join(card(d,i) for i,d in enumerate(ITEMS))
    return f'''<div class="wrap dataset-library" data-dataset-catalog>
<section class="dataset-overview" aria-label="资源概览"><div><span class="eyebrow">MANY MODALITIES · ONE LIBRARY</span><h2>从数据出发，让研究走得更远。</h2><p>整理：汐萌、囗〇 · 公众号「多模态信息融合」</p><div class="dataset-overview-links"><a href="#catalog">浏览完整目录 ↓</a><a href="contribute.html?type=数据集">推荐数据资源 ＋</a></div></div><div class="dataset-totals"><div><strong>{len(ITEMS)}</strong><span>项资源</span></div><div><strong>{len(CATEGORIES):02}</strong><span>研究方向</span></div><div><strong>{len(set(d['task'] for d in ITEMS)):02}</strong><span>任务分组</span></div></div></section>
<div class="dataset-library-note"><span>收录包括原创数据、衍生版本、评测基准与资源集合；按主要用途归类，展示顺序不作排名。</span><a href="#dataset-about">收录说明 ↓</a></div>
<section class="catalog-layout" id="catalog" aria-label="数据资源目录"><aside class="catalog-sidebar"><div class="catalog-category-panel" data-catalog-controls hidden><h2>研究方向</h2><div class="catalog-categories" role="group" aria-label="筛选研究方向">{category_buttons}</div></div><div class="catalog-sidebar-note"><p class="eyebrow">BEFORE THE EXPERIMENT</p><h3>先看任务，再选数据。</h3><p>关注输入模态、配准情况、标注、训练测试划分与使用许可。</p><a href="metrics.html">搭配评估指标 →</a></div></aside><div class="catalog-main">
<div class="catalog-tools" data-catalog-controls hidden><label class="catalog-search"><span aria-hidden="true">⌕</span><input id="dataset-search" type="search" aria-label="搜索数据资源" placeholder="搜索名称、任务、论文、团队或作者…" autocomplete="off"><kbd>/</kbd></label><div class="catalog-filters"><label>细分任务<select id="dataset-task"><option value="">全部任务</option></select></label><label>排序<select id="dataset-sort"><option value="source">整理顺序</option><option value="name">名称 A–Z</option><option value="year">发表年份 ↓</option></select></label><button class="reset-button" type="button" data-dataset-reset>重置筛选 ↺</button></div></div>
<div class="catalog-result-summary"><p id="dataset-result-count" role="status">共 {len(ITEMS)} 项资源</p><span>点击名称查看完整档案</span></div><p class="catalog-message" id="dataset-message" role="status" hidden></p><div id="dataset-results">{cards}</div><div class="empty-state" id="dataset-empty" hidden><h3>没有找到匹配的资源</h3><p>试试数据集简称、作者或任务名称，也可以清除筛选条件。</p><button type="button" class="button secondary" data-dataset-reset>清除筛选</button></div><div class="catalog-pagination" data-catalog-controls hidden><button class="button secondary" type="button" id="dataset-more">显示更多资源 ↓</button><p id="dataset-load-status" role="status"></p></div><noscript><p class="note-box">当前显示完整目录。点击每项下方的“展开完整档案”可阅读全部介绍；启用 JavaScript 后可使用搜索与筛选。</p></noscript></div></section>
{about()}
</div><dialog id="dataset-dialog" class="dataset-dialog" aria-labelledby="dataset-dialog-title" aria-describedby="dataset-dialog-subtitle"><div class="dataset-dialog-heading"><div><p class="eyebrow">DATASET PROFILE</p><h2 id="dataset-dialog-title">数据资源档案</h2></div><button type="button" data-dataset-close aria-label="关闭数据资源档案" autofocus>×</button></div><p id="dataset-dialog-subtitle"></p><div class="dataset-dialog-actions"><button type="button" class="button secondary" data-dataset-copy>复制条目链接 ↗</button><span>论文、团队、介绍与原始示例</span></div><div id="dataset-dialog-content"></div></dialog>'''

def about():
    return '''<section class="dataset-about" id="dataset-about"><div><p class="eyebrow">A NOTE FROM THE CURATORS</p><h2>少一些寻找，多一些探索。</h2><p>先按模态与融合类型分类，再按具体任务整理。部分资源适用于多项任务，这里按主要用途归类；具体范围以原论文和数据集说明为准。</p></div><div><details><summary>汐萌 · 整理寄语</summary><p>本文80%的数据集是平时阅读论文收集整理而来，余下工作用AI查漏补缺，并补充部分信息。可能会存在一定的不足或错误，还请见谅。因此，一切信息请参考并以原文为主！希望总结的内容，能对你的研究有所帮助。最后，感谢全部开源的研究者，为信息融合完善数据基石。</p></details><details><summary>囗〇 · 给研究者的话</summary><p>希望这篇文章能让你少花一些找数据的时间，多留一点精力给真正想解决的问题。选数据前，先看它是否贴近您的任务，再核对配准、标注、训练测试划分与使用许可。遇到不一致的信息，请回到原论文和官方仓库，也欢迎把勘误与新资源分享出来。愿您的每一次实验，都离清楚、可靠的结论更近一步。</p></details><div class="dataset-about-links"><a href="contribute.html?type=数据集">补充资源 →</a><a href="https://mp.weixin.qq.com/s/ygUEl8rsOwjVFrlY5kdRDw" target="_blank" rel="noopener noreferrer">公众号原文 ↗</a><a href="https://github.com/MMIFusion/Datasets" target="_blank" rel="noopener noreferrer">来源仓库 ↗</a><a href="https://www.zhihu.com/people/MMIFusion" target="_blank" rel="noopener noreferrer">知乎 ↗</a><a href="https://v.douyin.com/WguilqNP8RQ/" target="_blank" rel="noopener noreferrer">抖音 ↗</a><a href="https://xhslink.cn/o/6F64cKjEBxg" target="_blank" rel="noopener noreferrer">小红书 ↗</a></div><p class="dataset-source-note">原创整理：公众号「多模态信息融合」· 汐萌、囗〇。第三方数据、论文和示例图遵循原始许可；本站不托管数据集本体。</p></div></section>'''
