#!/usr/bin/env python3
"""Build a dependency-free, progressively enhanced GitHub Pages website."""
import html
import hashlib
import re
import portal
import design
import community
import datasets as dataset_catalog
import json
import shutil
from pathlib import Path
from collections import Counter
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
SITE = json.loads((ROOT / 'data/site.json').read_text())
DATA = json.loads((ROOT / 'data/articles.json').read_text())
STATS = json.loads((ROOT / 'data/article-stats.json').read_text())
ARTICLE_STATS = {r['id']:dict(r,snapshotDate=r.get('snapshotDate',STATS['snapshotDate'])) for r in STATS['records']}
COMMUNITY = json.loads((ROOT / 'data/community.json').read_text())
ARTICLES = DATA['articles']
E = lambda v: html.escape(str(v), quote=True)
ICONS = {
 'book':'<path d="M4 5h6a3 3 0 0 1 3 3v13a4 4 0 0 0-4-3H4zM22 5h-6a3 3 0 0 0-3 3v13a4 4 0 0 1 4-3h5z"/>',
 'data':'<ellipse cx="13" cy="6" rx="8" ry="3"/><path d="M5 6v13c0 4 16 4 16 0V6M5 12c0 4 16 4 16 0"/>',
 'chart':'<path d="M4 3v19h19M8 17v-5m6 5V7m6 10V4"/>',
 'people':'<circle cx="10" cy="8" r="4"/><path d="M2 22v-3a8 8 0 0 1 16 0v3M18 5a4 4 0 0 1 0 8m3 3a6 6 0 0 1 3 6"/>',
 'calendar':'<rect x="3" y="5" width="20" height="18" rx="2"/><path d="M3 11h20M8 2v6m10-6v6M8 15h2m5 0h3M8 19h2"/>',
 'journal':'<path d="M6 3h15v20H6a3 3 0 0 1 0-6h15M6 3a3 3 0 0 0-3 3v14M9 7h8m-8 4h6"/>',
 'grad':'<path d="m2 10 11-6 11 6-11 6zM6 13v6c5 4 9 4 14 0v-6M24 10v9"/>',
 'palette':'<path d="M13 3a10 10 0 1 0 0 20c5 0-1-6 3-6h3c7 0 4-14-6-14Z"/><circle cx="8" cy="10" r="1"/><circle cx="12" cy="7" r="1"/><circle cx="17" cy="9" r="1"/>',
 'megaphone':'<path d="m4 10 17-6v17L4 16zM7 17l2 6h4l-2-5M4 10H2v6h2"/>',
 'arrow':'<path d="M5 13h16m-6-6 6 6-6 6"/>',
 'search':'<circle cx="11" cy="11" r="7"/><path d="m16 16 7 7"/>'
}
def icon(name):
    return f'<svg viewBox="0 0 26 26" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
def ext(url, text, cls=''):
    return f'<a class="{cls}" href="{E(url)}" target="_blank" rel="noopener noreferrer">{text}<span aria-hidden="true">↗</span></a>'
def issue(kind):
    return SITE['repository']+'/issues/new?'+urlencode({'title':f'[{kind}] ', 'body':'名称：\n简介：\n官方来源链接：\n公众号文章链接（如有）：\n补充说明：'})

MODULES = [
 ('book','论文阅读','PAPERS','从问题、方法到实验，读懂研究进展。','papers.html',f'{len(ARTICLES)} 篇文章'),
 ('data','数据资源','DATASETS','按模态与任务，寻找适合的研究数据。',SITE['datasets'],f'{len(dataset_catalog.ITEMS)} 项资源 · 站内检索'),
 ('chart','评估指标','EVALUATION','关注融合质量、评价方法与下游任务。','metrics.html',f'{len(portal.P["metrics"])} 个指标 · 在线试算'),
 ('people','融合团队','RESEARCH GROUPS','从代表性成果，认识研究团队。','teams.html',f'{len(portal.P["teams"])} 个团队档案'),
 ('calendar','会议日历','CALENDAR','集中查看投稿节点与会议日程。','calendar.html',f'{len(portal.P["conferences"])} 场会议 · 日历下载'),
 ('journal','投稿推荐','PUBLICATION','会议论文动态与期刊投稿参考。','venues.html',f'{len(portal.P["venues"])} 个方向 · 对比筛选'),
 ('grad','导师招生','OPPORTUNITIES','连接研究兴趣与下一段学术旅程。','opportunities.html',f'{len(portal.P["opportunities"])} 条官方招募'),
 ('palette','配色模板','DESIGN','让论文图表清晰，也让表达更美。','palettes.html',f'{sum(a["section"]=="配色与绘图" for a in ARTICLES)} 篇配色文章'),
 ('megaphone','广告合作','PARTNERSHIP','连接学术传播、活动宣传与科研品牌。','advertising.html','合作形式 · 联系咨询'),
]

def qr_cards():
    # CSS selects a square viewport from each unmodified supplied image.
    # Keep at least four modules of quiet zone around both QR patterns.
    return f'''<div class="qr-grid"><article class="qr-card"><a class="qr-image qr-official" href="assets/qr/wechat-official.png" target="_blank" rel="noopener noreferrer" aria-label="打开公众号二维码原图"><img src="assets/qr/wechat-official.png" width="1816" height="624" alt="多模态信息融合公众号二维码"><span class="qr-center-avatar" aria-hidden="true"><img src="assets/avatar.png" width="46" height="46" alt=""></span></a><div class="qr-copy"><p class="eyebrow">WECHAT OFFICIAL ACCOUNT</p><h3>关注公众号</h3><p>微信扫码关注「多模态信息融合」，阅读论文解读与研究资源。</p><div class="qr-actions"><a href="assets/qr/wechat-official.png" download="多模态信息融合-公众号二维码.png">保存二维码 ↓</a>{ext(SITE['wechat'],'阅读公众号')}</div></div></article><article class="qr-card"><a class="qr-image qr-contact" href="assets/qr/wechat-contact.png" target="_blank" rel="noopener noreferrer" aria-label="打开交流微信二维码原图"><img src="assets/qr/wechat-contact.png" width="820" height="1219" alt="交流微信 MMIFusion_ 的好友二维码"></a><div class="qr-copy"><p class="eyebrow">CONNECT WITH THE COMMUNITY</p><h3>加入学术交流</h3><p>扫码添加微信 <strong>{SITE['contact']}</strong>，咨询加入学术交流群。</p><div class="qr-actions"><a href="assets/qr/wechat-contact.png" download="多模态信息融合-交流微信二维码.png">保存二维码 ↓</a><button type="button" data-copy="{SITE['contact']}">复制微信号</button></div></div></article></div>'''

def connect_section():
    return f'''<section class="wrap connect-section" id="connect" aria-labelledby="connect-heading"><div class="section-heading"><div><p class="eyebrow">06 / RESEARCH IS BETTER TOGETHER</p><h2 id="connect-heading">一起读论文，也一起交流。</h2><p>关注公众号获取完整解读，添加交流微信认识同行。</p></div><a class="text-link" href="contribute.html">推荐资源 →</a></div>{qr_cards()}<p class="qr-help">电脑端使用微信扫一扫；手机端可点开原图长按识别，或保存后在微信扫一扫中从相册选择。</p></section>'''

def qr_dialog():
    return f'''<dialog class="qr-dialog" id="wechat-dialog" aria-labelledby="wechat-dialog-title" aria-describedby="wechat-dialog-help"><div class="qr-dialog-heading"><div><p class="eyebrow">MMIFUSION · STAY CONNECTED</p><h2 id="wechat-dialog-title">关注与交流</h2></div><button class="qr-dialog-close" type="button" data-qr-close aria-label="关闭扫码窗口" autofocus>×</button></div>{qr_cards()}<p class="qr-help" id="wechat-dialog-help">用微信扫一扫；手机端可点开原图，或保存后从微信相册识别。</p></dialog>'''

def header(active, filename):
    nav=[('home','index.html','首页'),('papers','papers.html','论文阅读'),('datasets',SITE['datasets'],'数据资源'),('resources','resources.html','学术资源'),('about','about.html','关于我们')]
    links=''.join(f'<a href="{E(url)}"'+(' aria-current="page"' if active==key else '')+(' target="_blank" rel="noopener noreferrer"' if url.startswith('https:') else '')+f'>{label}</a>' for key,url,label in nav)
    selected = {'fortune.html':'calendar.html'}.get(filename, filename)
    resource_links = ''.join(f'<a class="resource-item" href="{E(m[4])}"' + (' aria-current="page"' if selected == m[4] else '') + (' target="_blank" rel="noopener noreferrer"' if m[4].startswith('https:') else '') + f'>{m[1]}</a>' for m in MODULES)
    return f'''<a class="skip-link" href="#main">跳转到主要内容</a>
<header class="site-header"><div class="header-inner wrap">
<a class="brand" href="index.html" aria-label="多模态信息融合首页"><img src="assets/avatar.png" width="46" height="46" alt="多模态信息融合公众号头像"><span><strong>多模态信息融合</strong><small>MMIFUSION · OPEN RESEARCH</small></span></a>
<button class="menu-toggle" aria-label="打开导航" aria-expanded="false" aria-controls="primary-nav">菜单 <span>☰</span></button>
<nav id="primary-nav" aria-label="主导航">{links}<a class="nav-scan" href="about.html#connect" data-qr-open>关注与交流</a></nav>
<a href="about.html#connect" class="button small wechat-link" data-qr-open>关注公众号 <span aria-hidden="true">＋</span></a></div></header><div class="resource-nav-shell"><nav class="resource-nav wrap" aria-label="学术栏目"><span class="resource-indicator" aria-hidden="true"></span>{resource_links}<a class="resource-contribute" href="contribute.html">推荐资源 ＋</a></nav></div>{community.daily_bar()}'''

def footer(filename, title):
    return f'''<footer class="site-footer"><div class="wrap footer-main"><div><a class="brand" href="index.html"><img src="assets/avatar.png" width="40" height="40" alt=""><span><strong>多模态信息融合</strong><small>CONNECTING MODALITIES. SHARING KNOWLEDGE.</small></span></a><p>一起读论文、找资源，探索多模态研究。</p></div><div class="footer-links"><a href="papers.html">文章目录</a><a href="resources.html">学术资源</a><a href="about.html#connect" data-qr-open>扫码关注与交流</a><a href="about.html">关于我们</a><a href="{E(portal.feedback(SITE['url']+'/'+filename, title+'页面反馈'))}">反馈问题</a>{ext(SITE['github'],'GitHub')}</div></div><div class="wrap footer-bottom"><span>© 2026 公众号「多模态信息融合」</span><span>文章索引更新至 {DATA['latestArticleDate'].replace('-','.')} · <a href="about.html#sources">收录说明</a></span></div></footer>'''

def page(filename, title, body, active='resources', description=None, extras=''):
    if 'class="article-stat-wrap"' in body:
        extras += '<link rel="stylesheet" href="assets/article-stats.css">'
    description=description or SITE['description']
    canonical=SITE['url']+'/' + ('' if filename=='index.html' else filename)
    doc=f'''<!doctype html><html lang="zh-CN" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · 多模态信息融合</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#11162e"><script>document.documentElement.classList.replace("no-js","js");try{{var motionPreference=localStorage.getItem("mmifusion-motion");document.documentElement.dataset.motion=motionPreference==="on"?"on":(motionPreference==="off"||matchMedia("(prefers-reduced-motion: reduce)").matches)?"off":"on"}}catch(e){{document.documentElement.dataset.motion=matchMedia("(prefers-reduced-motion: reduce)").matches?"off":"on"}}</script><link rel="canonical" href="{canonical}"><meta property="og:title" content="{E(title)} · 多模态信息融合"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE['url']}/assets/avatar.png"><link rel="icon" href="assets/avatar.png" type="image/png"><link rel="apple-touch-icon" href="assets/avatar.png"><link rel="preload" href="assets/fonts/mmifusion-sans.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/portal.css"><link rel="stylesheet" href="assets/experience.css"><link rel="stylesheet" href="assets/community.css"><script src="assets/metrics-core.js" defer></script><script src="assets/app.js" defer></script><script src="assets/calendar-core.js" defer></script><script src="assets/portal.js" defer></script><script src="assets/experience.js" defer></script><script src="assets/community-core.js" defer></script><script src="assets/community.js" defer></script></head><body class="page-{filename.removesuffix('.html')}">{header(active, filename)}<main id="main">{body}</main>{footer(filename, title)}{qr_dialog()}{design.motion_controls()}{community.luck_dialog()}<div id="toast" role="status" aria-live="polite"></div></body></html>'''
    doc=doc.replace('</head>', '<noscript><style>.collection-controls,.menu-toggle,.directory-toolbar,.calendar-tools label,.compare-check,.comparison-bar,.bookmark-button,.metric-lab,.contribution-form,.submission-preview{display:none}.hero-search,.calendar-view-options{display:none}@media(max-width:640px){.header-inner{height:auto;min-height:72px;flex-wrap:wrap;padding-block:12px}.header-inner nav{position:static;display:flex;flex-direction:row;flex-wrap:wrap;padding:0;box-shadow:none;border:0;margin:0}.header-inner nav a{font-size:12px;padding:8px}.header-inner nav a[aria-current]:after{bottom:2px}}</style></noscript></head>')
    doc=doc.replace('</head>', extras+'</head>')
    # Match each document to its exact JS/CSS, including across rolling Pages caches.
    doc=re.sub(r'((?:href|src)=")(?P<asset>assets/[^"?]+\.(?:css|js|woff2))"',
        lambda m: m.group(1)+m.group('asset')+'?v='+hashlib.sha256((ROOT/m.group('asset')).read_bytes()).hexdigest()[:12]+'"', doc)
    if filename=='404.html':
        doc=doc.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex">')
    (OUT/filename).write_text(doc)

def modules():
    return '<div class="module-grid">'+''.join(f'''<a class="module" href="{E(url)}" {'target="_blank" rel="noopener noreferrer"' if url.startswith('https:') else ''}><div class="module-top">{icon(i)}<span class="module-number">0{n+1}</span></div><h3>{name}<span aria-hidden="true">↗</span></h3><p>{desc}</p><div class="module-foot"><span>{en}</span><small>{status}</small></div></a>''' for n,(i,name,en,desc,url,status) in enumerate(MODULES))+'</div>'

def article_statistics(a):
    record=ARTICLE_STATS.get(a['id'],{})
    fields=[('reads','阅读量'),('likes','点赞量'),('watching','推荐'),('favorites','收藏')]
    available=[(key,label) for key,label in fields if record.get(key) is not None]
    if not available: return '',ext(a['url'],E(a['title']))
    panel_id='article-stats-'+a['id']
    cells=''.join(f'<div data-stat-metric="{key}"><dt'+(' title="原表在看数"' if key=='watching' else '')+f'>{label}</dt><dd>{record[key]:,}</dd></div>' for key,label in available)
    date=record['snapshotDate'].replace('-','.')
    panel=f'''<button type="button" class="article-stat-toggle" aria-controls="{panel_id}" aria-expanded="false">查看数据 <span aria-hidden="true">⌄</span></button><div class="article-stat-panel" id="{panel_id}" role="tooltip"><dl class="article-stat-values" style="--stat-count:{len(available)}">{cells}</dl><div class="article-stat-source"><span>公众号数据 · {date}</span><span>右侧星标为本站收藏</span></div></div>'''
    title=ext(a['url'],E(a['title']),'article-title-link').replace(' target=',f' aria-describedby="{panel_id}" target=',1)
    return panel,title

def row(a):
    panel,title=article_statistics(a)
    return f'''<article class="article-row" data-article-id="{a['id']}"><div class="article-date"><time datetime="{a['date']}">{a['date'].replace('-','.')}</time><span>{E(a['section'])}</span></div><div class="article-body"><div class="article-tags">{''.join('<span>'+E(t)+'</span>' for t in a['topics'][:3])}</div><div class="article-stat-wrap"><h3>{title}</h3>{panel}</div></div><button class="bookmark-button" data-bookmark="{a['id']}" aria-pressed="false" aria-label="收藏文章">☆<span>收藏</span></button></article>'''

def collection(items, scope='all', filterable=True):
    sections=Counter(a['section'] for a in items)
    topic_counts=Counter(t for a in items for t in a['topics'])
    venues=sorted(set(a['venue'] for a in items if a['venue']))
    controls=''
    if filterable:
        options=lambda entries: ''.join(f'<option value="{E(s)}">{E(s)}</option>' for s in entries)
        tabs=''.join(f'<button type="button" data-section="{E(s)}" aria-pressed="false">{E(s)} <span>{n}</span></button>' for s,n in sections.items())
        controls=f'''<div class="collection-controls"><div class="search-and-sort"><label class="search-input">{icon('search')}<input type="search" id="article-search" placeholder="搜索论文、方法、学校或关键词…" autocomplete="off" aria-label="搜索文章"><kbd>/</kbd></label><label class="select-label">排序<select id="sort-order"><option value="newest">最新发布</option><option value="oldest">最早发布</option></select></label></div><div class="filter-line"><label>研究方向<select id="topic-filter"><option value="">全部方向</option>{options(sorted(topic_counts))}</select></label><label>会议 / 期刊<select id="venue-filter"><option value="">全部会议期刊</option>{options(venues)}</select></label><label class="saved-filter"><input type="checkbox" id="saved-only">只看收藏</label><button class="reset-button" type="button" id="reset-filters">重置筛选 ↺</button></div><div class="section-tabs" aria-label="文章类型"><button type="button" data-section="" class="active" aria-pressed="true">全部 <span>{len(items)}</span></button>{tabs}</div></div>'''
    return f'''<section class="collection" data-scope="{scope}" data-page-size="12">{controls}<div class="result-summary"><p id="result-count" role="status" aria-live="polite">共 {len(items)} 篇文章</p><span>标题直达公众号 · 右侧星标仅保存在当前浏览器</span></div><div id="article-list">{''.join(row(a) for a in items)}</div><div id="empty-results" class="empty-state" hidden>{icon('search')}<h3>没有找到匹配的文章</h3><p>试试方法名、研究方向，或缩短关键词。</p><button type="button" class="button secondary" data-reset>清除筛选</button></div><div class="pagination" id="pagination" hidden><button class="button secondary" id="prev-page">← 上一页</button><span id="page-info"></span><button class="button secondary" id="next-page">下一页 →</button></div></section>'''

def title_block(en,title,desc,crumb='学术资源'):
    return f'<div class="page-heading wrap"><div class="breadcrumb"><a href="index.html">首页</a><span>/</span><a href="resources.html">{crumb}</a></div><p class="eyebrow">{en}</p><h1>{title}</h1><p class="page-description">{desc}</p></div>'

def home():
    stats=f'<div class="wrap community-stats"><div><strong>{len(ARTICLES)}<span>篇</span></strong><p>公众号文章，持续积累</p></div><div><strong>{len(MODULES):02d}<span>个</span></strong><p>栏目连接研究每一步</p></div><div><strong>03<span>类</span></strong><p>方向专题，从问题出发</p></div><a href="about.html#connect" data-qr-open><img src="assets/avatar.png" width="48" height="48" alt=""><span>一个热爱分享的研究社区<strong>认识多模态信息融合 ↗</strong></span></a></div>'
    return design.hero(len(ARTICLES))+stats+portal.deadline_strip()+community.fortune_teaser()+design.reading_room(ARTICLES)+community.ranking(ARTICLES)+design.research_paths(ARTICLES)+portal.dataset_showcase()+design.tool_spotlight()+f'<section class="wrap section" id="explore"><div class="section-heading"><div><p class="eyebrow">05 / YOUR RESEARCH COMPANION</p><h2>研究的每一步，都有一个入口。</h2><p>找论文、做实验、准备投稿，或认识下一位同行。</p></div><a class="text-link" href="resources.html">全部资源 ↗</a></div>{modules()}</section>'+connect_section()

def resources():
    return title_block('THE RESOURCE DIRECTORY','学术资源导航','围绕研究的每一步，整理值得反复使用的资源。')+f'<section class="wrap section compact-top">{modules()}</section>'

def palette_cards(records, basic=False):
    cards=[]
    for index,p in enumerate(records,1):
        stem='palette-basic-'+p['id'] if basic else f'palette-{index}'
        colors=''.join(f'<button style="--swatch:{color}" data-copy="{color}" aria-label="复制色值 {color}"><span>{color}</span></button>' for color in p['colors'])
        cards.append(f'''<article class="palette-card" id="{stem}"><div class="swatches">{colors}</div><div class="palette-info"><h3>{E(p['name'])}</h3><p>{E(p['note'])}</p><div class="palette-actions"><button class="text-link" data-copy="{', '.join(p['colors'])}">复制整组色值</button><a href="downloads/{stem}.svg" download>SVG 色板 ↓</a><a href="downloads/{stem}.json" download>JSON 色值 ↓</a></div></div></article>''')
    return ''.join(cards)

def palettes():
    basic=palette_cards(COMMUNITY['basicPalettes'],basic=True)
    combinations=palette_cards(COMMUNITY['palettes'])
    items=[a for a in ARTICLES if a['section']=='配色与绘图']
    return title_block('COLOR & SCIENTIFIC DESIGN','配色模板','好的图表，让方法和结果更容易被理解。')+f'''<nav class="wrap palette-section-links" aria-label="配色系列"><a class="text-link" href="#basic-palettes">基础色系 ↓</a><a class="text-link" href="#combined-palettes">组合配色 ↓</a></nav><section class="wrap section compact-top palette-series" id="basic-palettes"><div class="section-heading"><div><h2>基础色系，从浅到深。</h2><p>{len(COMMUNITY['basicPalettes'])} 个基础色系，每组 5 个色阶。从左到右由浅入深，点击色块复制 HEX。</p></div><span class="subtle-label">LIGHT TO DARK</span></div><div class="palette-grid">{basic}</div></section><section class="wrap section compact-top palette-series" id="combined-palettes"><div class="section-heading"><div><h2>组合配色，搭配即用。</h2><p>跨色系搭配，适合方法对比、模块区分与双模态示意。论文实例见下方公众号文章。</p></div><span class="subtle-label">CURATED COLOR SETS</span></div><div class="palette-grid">{combinations}</div><p class="small-note">曲线图建议同时使用不同线型或标记，避免仅靠颜色区分。</p></section>{portal.downloads()}<section class="wrap section compact-top"><div class="section-heading"><div><p class="eyebrow">LEARN FROM THE PAPERS</p><h2>论文模型图与配色阅读</h2></div></div>{collection(items,'palettes')}</section>'''

def community_members():
    cards=[]
    for member in SITE['members']:
        state=member['status']
        status='已激活' if state=='active' else '已退出'
        note='<p>感谢参与</p>' if state=='departed' else ''
        cards.append(f'<li class="member-card member-{state}" data-member-state="{state}"><span class="member-avatar" aria-hidden="true">{E(member["name"][0])}</span><div><h3>{E(member["name"])}</h3>{note}</div><span class="member-status">{status}</span></li>')
    return '<section class="community-members" id="members" aria-labelledby="members-heading"><h2 id="members-heading">团队成员</h2><p>一起整理知识，也一起建设这个交流空间。</p><ol class="member-grid">'+''.join(cards)+'</ol></section>'

def about():
    return title_block('ABOUT MMIFUSION','因为热爱，所以分享。','多模态信息融合，一个围绕论文阅读与学术资源的交流空间。')+f'''<div class="wrap about-layout section compact-top"><section class="about-copy"><h2>从公众号，到学术资源主页。</h2><p>我们关注图像融合、多模态感知与相关研究。通过论文解读、研究动态和资源整理，帮助读者从具体问题出发，理解方法，也找到继续探索的入口。</p><p>主站整合公众号文章与数据资源目录，并逐步完善评估指标、研究团队、会议日程、投稿参考、导师招生和论文配色等栏目。</p>{community_members()}<h2 id="sources">内容与收录说明</h2><ul class="prose-list"><li>当前文章索引已合并公众号导出表，更新于 {DATA['snapshotDate']}，共 {len(ARTICLES)} 条，最新文章日期为 {DATA['latestArticleDate']}。</li>
<li>文章保留原始标题与发表日期。点击标题跳转公众号阅读原文；不同文章分别收录；经核对的重复文章合并，保留原有文章编号。</li>
<li>研究方向与文章类型依据标题辅助归类，会议和期刊字段也来自标题，不代表本站另行核验了录用信息。欢迎提出分类或信息勘误。</li>
<li>数据资源栏目已整合原数据集目录，保留完整介绍、团队作者、原始示例图和来源链接。数据规模、许可及划分请查看原论文与官方说明。</li>
<li>会议、团队、招生与投稿方向已收录首批官方来源，逐条标注核对日期。投稿建议为本站整理，不代表录用概率。</li>
<li>公众号人气榜使用导出表中的阅读次数、点赞、在看和分享次数，按每篇文章最新可用的导出记录更新，统计日期见榜单卡片。文章列表按篇显示原表提供的收藏数，缺失项略去；推荐对应原表在看数，右侧星标仅保存在当前浏览器。</li>
<li>本站访问次数（PV）由 <a href="https://busuanzi.ibruce.info/" target="_blank" rel="noopener noreferrer">不蒜子</a> 提供，从 2026-11-11 接入后累计；服务可能受网络或拦截设置影响，不代表独立访客数。</li>
<li>投稿日历与接好运是科研趣味互动，不是传统黄历或录用预测。真实截止日期请查看会议日历。</li>
<li>基础色板由本站搭配，不是从论文中提取；论文配色实例通过公众号文章提供。</li></ul><h2>一起完善这份资源</h2><p>欢迎分享论文、数据集、团队主页、招生信息，或指出已有内容中的错误。请附原始来源，方便核对和持续维护。</p><a href="contribute.html" class="button secondary">推荐资源 / 提交勘误 →</a></section><aside class="contact-card"><img src="assets/avatar.png" width="100" height="100" alt="多模态信息融合头像"><h2>多模态信息融合</h2><p>微信公众号 · MMIFusion</p><a href="about.html#connect" class="button primary" data-qr-open>扫码关注与交流</a><div class="contact-id"><span>交流微信</span><strong>{SITE['contact']}</strong><button class="text-link" data-copy="{SITE['contact']}">复制微信号</button></div><a href="#members" class="text-link">认识团队成员 →</a>{ext(SITE['github'],'GitHub · MMIFusion','text-link')}</aside></div>{connect_section()}'''

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    portal.build_downloads(COMMUNITY['palettes'],COMMUNITY['basicPalettes'])
    shutil.copytree(ROOT/'assets', OUT/'assets')
    shutil.copytree(ROOT/'downloads', OUT/'downloads')
    (OUT/'data').mkdir()
    for path in (ROOT/'data').glob('*.json'): shutil.copy2(path,OUT/'data'/path.name)
    page('index.html','首页',home(),'home',extras='<link rel="stylesheet" href="assets/reading-covers.css">')
    page('resources.html','学术资源',resources())
    page('datasets.html','数据资源',title_block('DATASETS & BENCHMARKS','找到适合研究的数据。','从经典基准到多模态场景，按方向、任务、论文与团队探索完整资源目录。')+dataset_catalog.page(),'datasets',description=f'{len(dataset_catalog.ITEMS)} 项图像融合与多模态感知数据资源，支持研究方向与任务筛选、全文搜索、完整介绍、团队作者和原图查看。',extras='<link rel="stylesheet" href="assets/datasets.css"><script src="assets/datasets.js" defer></script>')
    page('papers.html','论文阅读',title_block('THE PAPER LIBRARY','读论文，也读懂问题。','检索公众号的论文解读、学术速递与研究资源。点击标题，继续阅读完整文章。','论文阅读')+f'<div class="wrap section compact-top">{collection(ARTICLES)}</div>','papers')
    metric_reading=[a for a in ARTICLES if '评估与指标' in a['topics']]
    page('metrics.html','评估指标',title_block('EVALUATION & BENCHMARKS','评估指标','读懂指标含义，试算图像统计，再建立一致的评测协议。')+portal.metrics()+f'<section class="wrap section compact-top"><div class="section-heading"><h2>继续阅读 · 融合质量评估</h2></div>{collection(metric_reading,"metrics")}</section>')
    page('teams.html','融合团队',title_block('PEOPLE BEHIND THE RESEARCH','融合团队','从研究方向认识同行，从公开主页继续探索。')+portal.teams(),extras='<link rel="stylesheet" href="assets/people.css">')
    page('calendar.html','会议日历',title_block('CONFERENCE CALENDAR','会议日历','把投稿节点放在一起，按自己的时区安排研究。')+'<div class="wrap calendar-fortune-link"><a href="fortune.html">✦ 想选个好日子？翻翻趣味投稿日历 →</a></div>'+portal.calendar(),extras='<link rel="stylesheet" href="assets/research.css">')
    page('venues.html','投稿推荐',title_block('FIND YOUR RESEARCH COMMUNITY','投稿推荐','从研究问题出发，筛选方向、比较范围，找到合适的交流平台。')+portal.venues(),extras='<link rel="stylesheet" href="assets/research.css">')
    page('opportunities.html','导师招生',title_block('RESEARCH OPPORTUNITIES','导师招生','连接研究兴趣、团队方向与公开招募信息。')+portal.opportunities())
    page('contribute.html','推荐资源',title_block('BUILD THE COMMONS TOGETHER','一起完善这份资源。','推荐值得分享的研究资源，也欢迎指出已有内容中的错误。')+portal.contribute()+'<noscript><div class="wrap note-box"><p>启用 JavaScript 可生成投稿草稿，也可直接前往 <a href="https://github.com/MMIFusion/MMIFusion.github.io/issues/new">GitHub 提交资源</a>。</p></div></noscript>')
    page('advertising.html','广告合作',title_block('PARTNERSHIPS & COLLABORATION','广告合作','让学术与科研相关的信息，被合适的人看见。')+community.advertising())
    page('fortune.html','投稿日历',title_block('A LITTLE LUCK, A LOT OF PREPARATION','投稿日历','挑个好日子，带着底气出发。')+community.fortune_page())
    page('palettes.html','配色模板',palettes(),extras='<link rel="stylesheet" href="assets/palettes.css">')
    page('about.html','关于我们',about(),'about',extras='<link rel="stylesheet" href="assets/people.css">')
    page('404.html','页面未找到','<section class="wrap empty-feature"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>这一页暂时没有找到。</h1><p>回到资源目录，继续探索感兴趣的内容。</p><a class="button primary" href="/">返回首页 →</a></section>')
    (OUT/'.nojekyll').touch()
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE['url']+'/sitemap.xml\n')
    urls=''.join(f'<url><loc>{SITE["url"]}/{p.name if p.name!="index.html" else ""}</loc></url>' for p in sorted(OUT.glob('*.html')) if p.name!='404.html')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
    # GitHub user sites publish main / (root) automatically. Mirror the generated
    # documents there, sharing the existing assets/ and data/ source directories.
    for path in OUT.iterdir():
        if path.is_file(): shutil.copy2(path, ROOT/path.name)
    print(f'Built {len(list(OUT.glob("*.html")))} pages; {len(ARTICLES)} articles.')

if __name__ == '__main__': main()
