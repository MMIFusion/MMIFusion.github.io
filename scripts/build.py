#!/usr/bin/env python3
"""Build a dependency-free, progressively enhanced GitHub Pages website."""
import html
import portal
import json
import shutil
from pathlib import Path
from collections import Counter
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
SITE = json.loads((ROOT / 'data/site.json').read_text())
DATA = json.loads((ROOT / 'data/articles.json').read_text())
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
 ('data','数据集','DATASETS','按模态与任务，寻找适合的研究数据。',SITE['datasets'],'独立资源站 ↗'),
 ('chart','评估指标','EVALUATION','关注融合质量、评价方法与下游任务。','metrics.html',f'{len(portal.P["metrics"])} 个指标 · 在线试算'),
 ('people','融合团队','RESEARCH GROUPS','从代表性成果，认识研究团队。','teams.html',f'{len(portal.P["teams"])} 个团队档案'),
 ('calendar','会议时间','CALENDAR','集中查看投稿节点与会议日程。','calendar.html',f'{len(portal.P["conferences"])} 场会议 · 日历下载'),
 ('journal','会议期刊推荐','PUBLICATION','会议论文动态与期刊投稿参考。','venues.html',f'{len(portal.P["venues"])} 个方向 · 对比筛选'),
 ('grad','导师招生','OPPORTUNITIES','连接研究兴趣与下一段学术旅程。','opportunities.html',f'{len(portal.P["opportunities"])} 条官方招募'),
 ('palette','配色模板','DESIGN','让论文图表清晰，也让表达更美。','palettes.html',f'{sum(a["section"]=="配色与绘图" for a in ARTICLES)} 篇配色文章'),
]

def header(active):
    nav=[('home','index.html','首页'),('papers','papers.html','论文阅读'),('datasets',SITE['datasets'],'数据集 ↗'),('resources','resources.html','学术资源'),('about','about.html','关于我们')]
    links=''.join(f'<a href="{E(url)}"'+(' aria-current="page"' if active==key else '')+(' target="_blank" rel="noopener noreferrer"' if key=='datasets' else '')+f'>{label}</a>' for key,url,label in nav)
    return f'''<a class="skip-link" href="#main">跳转到主要内容</a>
<header class="site-header"><div class="header-inner wrap">
<a class="brand" href="index.html" aria-label="多模态信息融合首页"><img src="assets/avatar.png" width="46" height="46" alt="多模态信息融合公众号头像"><span><strong>多模态信息融合</strong><small>MMIFUSION · RESEARCH COMMUNITY</small></span></a>
<button class="menu-toggle" aria-label="打开导航" aria-expanded="false" aria-controls="primary-nav">菜单 <span>☰</span></button>
<nav id="primary-nav" aria-label="主导航">{links}</nav>
{ext(SITE['wechat'],'关注公众号','button small wechat-link')}</div></header><nav class="resource-nav wrap" aria-label="学术栏目">{''.join(f'<a href="{E(m[4])}">{m[1]}</a>' for m in MODULES)}<a href="contribute.html">推荐资源 ＋</a></nav>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap footer-main"><div><a class="brand" href="index.html"><img src="assets/avatar.png" width="40" height="40" alt=""><span><strong>多模态信息融合</strong><small>CONNECTING MODALITIES. SHARING KNOWLEDGE.</small></span></a><p>一起读论文、找资源，探索多模态研究。</p></div><div class="footer-links"><a href="papers.html">文章目录</a><a href="resources.html">学术资源</a><a href="about.html">关于与联系</a>{ext(SITE['github'],'GitHub')}</div></div><div class="wrap footer-bottom"><span>© 2026 公众号「多模态信息融合」 · 汐萌、囗〇</span><span>文章索引更新至 {DATA['latestArticleDate'].replace('-','.')} · <a href="about.html#sources">收录说明</a></span></div></footer>'''

def page(filename, title, body, active='resources', description=None):
    description=description or SITE['description']
    canonical=SITE['url']+'/' + ('' if filename=='index.html' else filename)
    doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · 多模态信息融合</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#b43c35"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{E(title)} · 多模态信息融合"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE['url']}/assets/avatar.png"><link rel="icon" href="assets/avatar.png" type="image/png"><link rel="apple-touch-icon" href="assets/avatar.png"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/portal.css"><script src="assets/metrics-core.js" defer></script><script src="assets/app.js" defer></script><script src="assets/portal.js" defer></script></head><body>{header(active)}<main id="main">{body}</main>{footer()}<div id="toast" role="status" aria-live="polite"></div></body></html>'''
    doc=doc.replace('</head>', '<noscript><style>.collection-controls,.menu-toggle,.directory-toolbar,.calendar-tools label,.compare-check,.comparison-bar,.bookmark-button,.metric-lab,.contribution-form,.submission-preview{display:none}.hero-search{display:none}@media(max-width:640px){.header-inner{height:auto;min-height:72px;flex-wrap:wrap;padding-block:12px}.header-inner nav{position:static;display:flex;flex-direction:row;flex-wrap:wrap;padding:0;box-shadow:none;border:0;margin:0}.header-inner nav a{font-size:12px;padding:8px}.header-inner nav a[aria-current]:after{bottom:2px}}</style></noscript></head>')
    if filename=='404.html':
        doc=doc.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex">')
    (OUT/filename).write_text(doc)

def modules():
    return '<div class="module-grid">'+''.join(f'''<a class="module" href="{E(url)}" {'target="_blank" rel="noopener noreferrer"' if url.startswith('https:') else ''}><div class="module-top">{icon(i)}<span class="module-number">0{n+1}</span></div><h3>{name}<span aria-hidden="true">↗</span></h3><p>{desc}</p><div class="module-foot"><span>{en}</span><small>{status}</small></div></a>''' for n,(i,name,en,desc,url,status) in enumerate(MODULES))+'</div>'

def row(a):
    return f'''<article class="article-row" data-article-id="{a['id']}"><div class="article-date"><time datetime="{a['date']}">{a['date'].replace('-','.')}</time><span>{E(a['section'])}</span></div><div class="article-body"><div class="article-tags">{''.join('<span>'+E(t)+'</span>' for t in a['topics'][:3])}</div><h3>{ext(a['url'],E(a['title']))}</h3></div><button class="bookmark-button" data-bookmark="{a['id']}" aria-pressed="false" aria-label="收藏文章">☆<span>收藏</span></button></article>'''

def collection(items, scope='all', filterable=True):
    sections=Counter(a['section'] for a in items)
    topic_counts=Counter(t for a in items for t in a['topics'])
    venues=sorted(set(a['venue'] for a in items if a['venue']))
    controls=''
    if filterable:
        options=lambda entries: ''.join(f'<option value="{E(s)}">{E(s)}</option>' for s in entries)
        tabs=''.join(f'<button type="button" data-section="{E(s)}" aria-pressed="false">{E(s)} <span>{n}</span></button>' for s,n in sections.items())
        controls=f'''<div class="collection-controls"><div class="search-and-sort"><label class="search-input">{icon('search')}<input type="search" id="article-search" placeholder="搜索论文、方法、学校或关键词…" autocomplete="off" aria-label="搜索文章"><kbd>/</kbd></label><label class="select-label">排序<select id="sort-order"><option value="newest">最新发布</option><option value="oldest">最早发布</option></select></label></div><div class="filter-line"><label>研究方向<select id="topic-filter"><option value="">全部方向</option>{options(sorted(topic_counts))}</select></label><label>会议 / 期刊<select id="venue-filter"><option value="">全部会议期刊</option>{options(venues)}</select></label><label class="saved-filter"><input type="checkbox" id="saved-only">只看收藏</label><button class="reset-button" type="button" id="reset-filters">重置筛选 ↺</button></div><div class="section-tabs" aria-label="文章类型"><button type="button" data-section="" class="active" aria-pressed="true">全部 <span>{len(items)}</span></button>{tabs}</div></div>'''
    return f'''<section class="collection" data-scope="{scope}" data-page-size="12">{controls}<div class="result-summary"><p id="result-count" role="status" aria-live="polite">共 {len(items)} 篇文章</p><span>标题直达公众号 · 收藏保存在当前浏览器</span></div><div id="article-list">{''.join(row(a) for a in items)}</div><div id="empty-results" class="empty-state" hidden>{icon('search')}<h3>没有找到匹配的文章</h3><p>试试方法名、研究方向，或缩短关键词。</p><button type="button" class="button secondary" data-reset>清除筛选</button></div><div class="pagination" id="pagination" hidden><button class="button secondary" id="prev-page">← 上一页</button><span id="page-info"></span><button class="button secondary" id="next-page">下一页 →</button></div></section>'''

def title_block(en,title,desc,crumb='学术资源'):
    return f'<div class="page-heading wrap"><div class="breadcrumb"><a href="index.html">首页</a><span>/</span><a href="resources.html">{crumb}</a></div><p class="eyebrow">{en}</p><h1>{title}</h1><p class="page-description">{desc}</p></div>'

def home():
    feature=ARTICLES[:3]
    pick=''.join(f'<a href="{E(a["url"])}" class="digest-item" target="_blank" rel="noopener noreferrer"><span>{a["date"].replace("-",".")}<b>{E(a["section"])}</b></span><h3>{E(a["title"])}</h3><small>阅读全文 ↗</small></a>' for a in feature)
    recent=[a for a in ARTICLES if a['section']=='论文解读'][:5]
    return f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="red-dot"></span> AN OPEN WINDOW INTO MULTIMODAL RESEARCH</p><h1>连接多模态，<br>让研究<span class="hero-accent">彼此启发。</span></h1><p class="hero-description">从一篇论文出发，发现方法、数据与新的可能。<br>这里是「多模态信息融合」的学术资源主页。</p><div class="hero-actions"><a class="button primary" href="papers.html">开始阅读 {icon('arrow')}</a><a class="button secondary" href="{SITE['datasets']}" target="_blank" rel="noopener noreferrer">探索数据集 ↗</a></div><form action="papers.html" class="hero-search" role="search"><label class="sr-only" for="home-search">搜索公众号文章</label><input id="home-search" name="q" type="search" placeholder="搜索方法、研究方向、学校…" required><button type="submit" aria-label="搜索文章">{icon('search')}</button></form><div class="hero-topic-links"><span>从这里开始</span><a href="papers.html?topic=图像融合">图像融合</a><a href="papers.html?q=多模态">多模态感知</a><a href="papers.html?saved=1">我的收藏 ☆</a></div></div><aside class="reading-digest" aria-label="近期阅读"><div class="digest-heading"><span class="eyebrow">THE READING ROOM</span><span class="issue-mark">VOL. 01</span></div><div class="digest-title"><h2>近期阅读</h2><img src="assets/avatar.png" width="48" height="48" alt=""></div>{pick}<a class="digest-all" href="papers.html">打开完整文章目录 <span>→</span></a></aside></section>
<div class="wrap stats-strip"><div><strong>{len(ARTICLES)}<small>篇</small></strong><span>公众号文章索引</span></div><div><strong>08<small>个</small></strong><span>学术资源栏目</span></div><div><strong>持续<small>积累</small></strong><span>连接论文、数据与研究者</span></div><p>为研究而整理<br>与同行一起探索<span>CURATED BY MMIFUSION</span></p></div>
{portal.deadline_strip()}<section class="wrap section" id="explore"><div class="section-heading"><div><p class="eyebrow">EXPLORE THE KNOWLEDGE</p><h2>你的下一步研究，从这里开始。</h2></div><a class="text-link" href="resources.html">全部资源 {icon('arrow')}</a></div>{modules()}</section>
<section class="latest-section"><div class="wrap latest-layout"><div class="latest-intro"><p class="eyebrow">LATEST IN RESEARCH</p><h2>近期论文<br>值得一读。</h2><p>追踪图像融合与多模态感知，<br>从具体问题走进前沿研究。</p><a class="text-link" href="papers.html?section={E('论文解读')}">查看论文解读 {icon('arrow')}</a><span class="small-note">文章索引截至 {DATA['latestArticleDate'].replace('-','.')}</span></div><div class="latest-list">{''.join(row(a) for a in recent)}</div></div></section>
{portal.dataset_showcase()}<section class="wrap community-band"><div class="community-logo"><img src="assets/avatar.png" width="86" height="86" alt="多模态信息融合公众号头像"></div><div><p class="eyebrow">RESEARCH IS BETTER TOGETHER</p><h2>把有价值的研究，分享给更多人。</h2><p>关注公众号，阅读完整解读；也欢迎推荐论文、补充资源和交流想法。</p></div><div class="community-actions">{ext(SITE['wechat'],'前往公众号','button primary')}<a href="contribute.html" class="text-link">推荐资源 →</a></div></section>'''

def resources():
    return title_block('THE RESOURCE DIRECTORY','学术资源导航','围绕研究的每一步，整理值得反复使用的资源。')+f'<section class="wrap section compact-top">{modules()}</section>'

def palettes():
    cards=''.join(f'''<article class="palette-card"><div class="swatches">{''.join(f'<button style="--swatch:{color}" data-copy="{color}" aria-label="复制色值 {color}"><span>{color}</span></button>' for color in p['colors'])}</div><div class="palette-info"><h3>{E(p['name'])}</h3><p>{E(p['note'])}</p><button class="text-link" data-copy="{', '.join(p['colors'])}">复制整组色值 ↗</button></div></article>''' for p in COMMUNITY['palettes'])
    items=[a for a in ARTICLES if a['section']=='配色与绘图']
    return title_block('COLOR & SCIENTIFIC DESIGN','配色模板','好的图表，让方法和结果更容易被理解。')+f'''<section class="wrap section compact-top"><div class="section-heading"><div><h2>基础配色，点击即用。</h2><p>本站搭配的四组色板。点击色块复制 HEX；论文实例见下方公众号文章。</p></div><span class="subtle-label">ORIGINAL COLOR SETS</span></div><div class="palette-grid">{cards}</div><p class="small-note">曲线图建议同时使用不同线型或标记，避免仅靠颜色区分。</p></section>{portal.downloads(COMMUNITY["palettes"])}<section class="wrap section compact-top"><div class="section-heading"><div><p class="eyebrow">LEARN FROM THE PAPERS</p><h2>论文模型图与配色阅读</h2></div></div>{collection(items,'palettes')}</section>'''

def about():
    return title_block('ABOUT MMIFUSION','因为热爱，所以分享。','多模态信息融合，一个围绕论文阅读与学术资源的交流空间。')+f'''<div class="wrap about-layout section compact-top"><section class="about-copy"><h2>从公众号，到学术资源主页。</h2><p>我们关注图像融合、多模态感知与相关研究。通过论文解读、研究动态和资源整理，帮助读者从具体问题出发，理解方法，也找到继续探索的入口。</p><p>主站连接公众号文章与独立的数据集网站，并逐步完善评估指标、研究团队、会议日程、投稿参考、导师招生和论文配色等栏目。</p><h2 id="sources">内容与收录说明</h2><ul class="prose-list"><li>当前文章索引来自公众号的 2026 年 10 月 28 日导出表，共 {len(ARTICLES)} 条，最新文章日期为 {DATA['latestArticleDate']}。</li><li>文章保留原始标题与发表日期。点击标题跳转公众号阅读原文；同名但链接不同的文章分别收录。</li><li>研究方向与文章类型依据标题辅助归类，会议和期刊字段也来自标题，不代表本站另行核验了录用信息。欢迎提出分类或信息勘误。</li><li>数据集由独立站维护。数据规模、许可及划分请查看对应资源的原始说明。</li><li>会议、团队、招生与投稿方向已收录首批官方来源，逐条标注核对日期。投稿建议为本站整理，不代表录用概率。</li><li>基础色板由本站搭配，不是从论文中提取；论文配色实例通过公众号文章提供。</li></ul><h2>一起完善这份资源</h2><p>欢迎分享论文、数据集、团队主页、招生信息，或指出已有内容中的错误。请附原始来源，方便核对和持续维护。</p><a href="contribute.html" class="button secondary">推荐资源 / 提交勘误 →</a></section><aside class="contact-card"><img src="assets/avatar.png" width="100" height="100" alt="多模态信息融合头像"><h2>多模态信息融合</h2><p>微信公众号 · MMIFusion</p>{ext(SITE['wechat'],'阅读公众号','button primary')}<div class="contact-id"><span>交流微信</span><strong>{SITE['contact']}</strong><button class="text-link" data-copy="{SITE['contact']}">复制微信号</button></div><p class="small-note">整理与维护：汐萌、囗〇</p>{ext(SITE['github'],'GitHub · MMIFusion','text-link')}</aside></div>'''

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    portal.build_downloads(COMMUNITY['palettes'])
    shutil.copytree(ROOT/'assets', OUT/'assets')
    shutil.copytree(ROOT/'downloads', OUT/'downloads')
    (OUT/'data').mkdir()
    for path in (ROOT/'data').glob('*.json'): shutil.copy2(path,OUT/'data'/path.name)
    page('index.html','首页',home(),'home')
    page('resources.html','学术资源',resources())
    page('papers.html','论文阅读',title_block('THE PAPER LIBRARY','读论文，也读懂问题。','检索公众号的论文解读、学术速递与研究资源。点击标题，继续阅读完整文章。','论文阅读')+f'<div class="wrap section compact-top">{collection(ARTICLES)}</div>','papers')
    metric_reading=[a for a in ARTICLES if '评估与指标' in a['topics']]
    page('metrics.html','评估指标',title_block('EVALUATION & BENCHMARKS','评估指标','读懂指标含义，试算图像统计，再建立一致的评测协议。')+portal.metrics()+f'<section class="wrap section compact-top"><div class="section-heading"><h2>继续阅读 · 融合质量评估</h2></div>{collection(metric_reading,"metrics")}</section>')
    page('teams.html','融合团队',title_block('PEOPLE BEHIND THE RESEARCH','融合团队','从研究方向认识同行，从官方主页继续探索。')+portal.teams())
    page('calendar.html','会议时间',title_block('CONFERENCE CALENDAR','会议时间','把投稿节点放在一起，按自己的时区安排研究。')+portal.calendar())
    page('venues.html','会议期刊推荐',title_block('FIND YOUR RESEARCH COMMUNITY','会议期刊推荐','从研究问题出发，筛选方向、比较范围，找到合适的交流平台。')+portal.venues())
    page('opportunities.html','导师招生',title_block('RESEARCH OPPORTUNITIES','导师招生','连接研究兴趣、团队方向与公开招募信息。')+portal.opportunities())
    page('contribute.html','推荐资源',title_block('BUILD THE COMMONS TOGETHER','一起完善这份资源。','推荐值得分享的研究资源，也欢迎指出已有内容中的错误。')+portal.contribute()+'<noscript><div class="wrap note-box"><p>启用 JavaScript 可生成投稿草稿，也可直接前往 <a href="https://github.com/MMIFusion/MMIFusion.github.io/issues/new">GitHub 提交资源</a>。</p></div></noscript>')
    page('palettes.html','配色模板',palettes())
    page('about.html','关于我们',about(),'about')
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
