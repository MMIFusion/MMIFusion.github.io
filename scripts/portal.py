"""Research portal views and downloadable resources."""
import html
import json
from pathlib import Path
from urllib.parse import urlencode

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'data/portal.json').read_text())
E=lambda value: html.escape(str(value),quote=True)
def link(url,text,css='text-link'):
    return f'<a class="{css}" href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(text)} ↗</a>'
def tags(values): return '<div class="tag-list">'+''.join(f'<span>{E(t)}</span>' for t in values)+'</div>'
def source(url): return f'<div class="source-line">{link(url,"官方来源")}<span>核对于 {P["verifiedAt"]}</span></div>'
def related(query): return 'papers.html?'+urlencode({'q':query})

def filterbar(kind,placeholder,filters):
    selects=''.join(f'<label>{label}<select data-card-filter="{key}"><option value="">全部{label}</option>'+''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in values)+'</select></label>' for key,label,values in filters)
    return f'<div class="directory-toolbar"><label class="directory-search"><span aria-hidden="true">⌕</span><input data-card-search type="search" aria-label="{placeholder}" placeholder="{placeholder}"></label>{selects}<button class="reset-button" data-card-reset>重置</button><p class="directory-count" aria-live="polite"></p></div>'
def empty(): return '<div class="empty-state directory-empty" hidden><h3>没有匹配的内容</h3><p>试试其他关键词，或清除筛选条件。</p><button class="button secondary" data-card-reset>清除筛选</button></div>'
def filterattrs(record,search,**filters):
    return f'data-directory-card data-search="{E(search)}" '+ ' '.join(f'data-{key}="{E(json.dumps(value,ensure_ascii=False))}"' for key,value in filters.items())

def deadline_strip():
    events=[('CVPR 2027',P['conferences'][0]['events'][1]),('CVPR 2027',P['conferences'][0]['events'][2]),('ICLR 2027',P['conferences'][1]['events'][0])]
    items=''.join(f'<a href="calendar.html#{e["id"].rsplit("-",1)[0]}" class="deadline-teaser"><span>{name} · {e["label"]}</span><strong '+(f'data-countdown="{e["at"]}"' if e['kind']=='deadline' else '')+'>'+(e['at'][:10].replace('-','.') if e['kind']=='deadline' else e['start'].replace('-','.'))+'</strong><small>'+('距离截止 · 实时更新' if e['kind']=='deadline' else '官方日期 · 具体时刻未列明')+'</small></a>' for name,e in events)
    return '<section class="wrap deadline-strip" aria-label="近期学术节点"><div class="deadline-caption"><span class="red-dot"></span><strong>学术日历</strong><a href="calendar.html">查看全部 →</a></div>'+items+'</section>'

def dataset_showcase():
    cards=''.join(f'<article class="dataset-preview"><p class="eyebrow">{E(d["label"])}</p><h3>{E(d["name"])}</h3><p>{E(d["description"])}</p><div class="card-actions">{link(d["catalog"],"查看数据档案")}{link(d["source"],"原始项目")}</div></article>' for d in P['datasets'])
    return f'<section class="wrap section"><div class="section-heading"><div><p class="eyebrow">FROM PAPER TO EXPERIMENT</p><h2>为下一次实验，找到数据。</h2><p>从三个常用入口开始，完整介绍与下载信息由数据集独立站维护。</p></div>{link("https://mmifusion.github.io/Datasets/","全部数据集")}</div><div class="dataset-previews">{cards}</div></section>'

def calendar():
    cards=[]
    for c in P['conferences']:
        events=[]
        for e in c['events']:
            time=f'<time data-local-time="{e["at"]}">{E(e["original"])}</time>' if e['kind']=='deadline' else f'<time datetime="{e["start"]}">{E(e["start"])}</time>'
            countdown=f'<span class="countdown" data-countdown="{e["at"]}">{E(e["original"])}</span>' if e['kind']=='deadline' else '<span class="date-only">按官方日期显示</span>'
            events.append(f'<div class="event-row"><div><h3>{E(e["label"])}</h3>{time}<small>{E(e["original"])}</small></div><div class="event-actions">{countdown}<a href="downloads/{e["id"]}.ics" download>加入日历 ↓</a></div></div>')
        attrs=filterattrs(c,c['name']+' '+c['description'],field=[c['field']])
        cards.append(f'<article id="{c["id"]}" class="conference-card" {attrs}><div class="conference-title"><div><p class="eyebrow">{E(c["field"])}</p><h2>{E(c["name"])}</h2></div>{link(c["source"],"会议官网")}</div><p class="conference-description">{E(c["description"])}</p>{"".join(events)}{source(c["source"])}</article>')
    return f'''<section class="wrap section compact-top" data-directory="calendar">{filterbar('calendar','搜索会议名称或研究方向',[('field','领域',['计算机视觉','机器学习'])])}<div class="calendar-tools"><p>精确时刻可切换时区；未公布时刻的节点保留为日期。</p><label>时间显示 <select id="calendar-timezone"><option value="Asia/Shanghai">北京时间 UTC+8</option><option value="UTC">协调世界时 UTC</option><option value="local">浏览器当地时间</option></select></label><a href="downloads/mmifusion-calendar.ics" download class="button secondary">下载全部日程 ↓</a></div><div class="conference-grid">{''.join(cards)}</div>{empty()}<p class="small-note">AoE 为 UTC−12。日历文件可导入系统日历；文件为本次信息快照，日程变更请查看会议官网。</p></section>'''

def teams():
    cards=[]
    for t in P['teams']:
        attrs=filterattrs(t,' '.join([t['name'],t['lead'],t['institution'],*t['tags']]),city=[t['city']],topic=t['tags'])
        opportunity=f'<a href="opportunities.html#{t["opportunity"]}">招生信息 →</a>' if t['opportunity'] else ''
        cards.append(f'<article class="profile-card" id="{t["id"]}" {attrs}><div class="profile-badge">{E(t["institution"][:2])}</div><div class="profile-heading"><p>{E(t["institution"])} · {E(t["city"])}</p><h2>{E(t["name"])}</h2><span>负责人：{E(t["lead"])}</span></div>{tags(t["tags"])}<p class="profile-description">{E(t["description"])}</p><div class="card-actions">{link(t["source"],"官方主页")}<a href="{E(related(t["relatedQuery"]))}">相关解读 →</a>{opportunity}</div>{source(t["source"])}</article>')
    return f'<section class="wrap section compact-top" data-directory="teams">{filterbar("teams","搜索导师、团队、学校或方向",[("city","城市",["武汉","大连"]),("topic","方向",sorted(set(x for t in P["teams"] for x in t["tags"])))])}<div class="profile-grid">{"".join(cards)}</div>{empty()}<div class="directory-bottom"><p>按收录顺序展示，不作排名。团队成员与成果以官方主页为准。</p><a href="contribute.html?type=团队档案" class="text-link">推荐研究团队 →</a></div></section>'

def opportunities():
    cards=[]
    for o in P['opportunities']:
        attrs=filterattrs(o,' '.join([o['title'],o['institution'],o['team'],*o['tags']]),city=[o['city']],type=o['types'])
        cards.append(f'<article class="opportunity-card" id="{o["id"]}" {attrs}><div class="opportunity-header"><div><p class="eyebrow">{E(o["institution"])} · {E(o["city"])}</p><h2>{E(o["title"])}</h2><p>{E(o["team"])}</p></div><span class="status-label open-status">{E(o["status"])}</span></div>{tags(o["types"])}<p>{E(o["description"])}</p><details><summary>申请准备与联系渠道</summary><p>{E(o["requirements"])}</p><p>请在官方主页查看联系方式。本站不代收申请材料。</p></details><div class="card-actions">{link(o["source"],"查看官方招募说明","button primary")}<a href="teams.html#{o["teamId"]}" class="text-link">了解团队 →</a><button class="text-link" data-copy-link="opportunities.html#{o["id"]}">复制条目链接</button></div>{source(o["source"])}</article>')
    return f'<section class="wrap section compact-top" data-directory="opportunities">{filterbar("opportunities","搜索学校、导师或研究方向",[("type","类别",["硕士","博士","博士后","科研助理"]),("city","城市",["大连"])])}<div class="opportunity-list">{"".join(cards)}</div>{empty()}<div class="directory-bottom"><p>长期招募按导师公开说明收录，不等同于保证当前名额。</p><a class="text-link" href="contribute.html?type=招生信息">提交招生信息 →</a></div></section>'

def venues():
    cards=[]
    for v in P['venues']:
        attrs=filterattrs(v,' '.join([v['name'],v['fullName'],*v['tags']]),type=[v['type']],topic=v['tags'])
        calendarlink=f'<a href="calendar.html#{v["calendar"]}">查看日程 →</a>' if v['calendar'] else ''
        cards.append(f'<article class="venue-card" {attrs}><div class="venue-top"><p class="eyebrow">{E(v["type"])}</p><label class="compare-check"><input type="checkbox" data-compare="{v["id"]}">加入对比</label></div><h2>{E(v["name"])}</h2><p class="venue-fullname">{E(v["fullName"])}</p>{tags(v["tags"])}<p>{E(v["scope"])}</p><div class="fit-note"><strong>选刊思路</strong><p>{E(v["fit"])}</p></div><div class="card-actions">{link(v["source"],"征稿范围")}{link(v["guide"],"作者指南")}<a href="papers.html?venue={E(v["articleVenue"])}">相关解读 →</a>{calendarlink}</div>{source(v["source"])}</article>')
    return f'''<section class="wrap section compact-top" data-directory="venues">{filterbar('venues','搜索会议、期刊或研究方向',[('type','类型',['会议','期刊']),('topic','方向',sorted(set(t for v in P['venues'] for t in v['tags'])))])}<p class="small-note">先按研究问题筛选，再对照官方征稿范围；“选刊思路”为本站整理建议，不表示录用概率。</p><div class="venue-grid">{''.join(cards)}</div>{empty()}<div class="comparison-bar"><span id="compare-count">选择 2–3 个会议期刊进行对比</span><button class="button secondary" id="compare-open" disabled>比较所选项目 →</button></div><dialog id="compare-dialog" class="portal-dialog"><div class="dialog-heading"><h2>会议期刊对比</h2><button data-close-dialog aria-label="关闭对比">×</button></div><div id="compare-content"></div></dialog></section>'''

def metrics():
    cards=''.join(f'<article class="metric-definition"><span class="metric-code">{m["id"]}</span><h3>{E(m["name"])}</h3><code>{E(m["formula"])}</code><p>{E(m["description"])}</p><small>{E(m["caution"])}</small></article>' for m in P['metrics'])
    return f'''<section class="wrap section compact-top"><div class="metric-lab" id="metric-lab"><div class="lab-heading"><div><p class="eyebrow">FUSION IMAGE LAB</p><h2>上传一张图，试算三个指标。</h2><p>图片在当前浏览器内计算，不上传服务器。</p></div><a class="text-link" href="downloads/fusion_metrics.py" download>下载 Python 实现 ↓</a></div><div class="lab-layout"><div class="lab-input"><div class="canvas-frame"><canvas id="metric-canvas" width="256" height="192" aria-label="待评估图像预览"></canvas></div><label class="button primary upload-button">选择本地图片<input type="file" id="metric-file" accept="image/png,image/jpeg,image/webp,image/bmp"></label><p class="small-note">PNG / JPEG / WebP / BMP · 最大 20 MB、1600 万像素</p><div class="sample-buttons"><span>试用示例</span><button data-metric-sample="gradient">渐变</button><button data-metric-sample="checker">棋盘</button><button data-metric-sample="flat">纯灰</button></div></div><div class="lab-results"><p id="metric-image-info">选择示例或上传图片</p><div class="metric-values" aria-live="polite"><div><span>EN · 信息熵</span><strong id="metric-en">—</strong><small>bit</small></div><div><span>SD · 标准差</span><strong id="metric-sd">—</strong><small>灰度值</small></div><div><span>SF · 空间频率</span><strong id="metric-sf">—</strong><small>灰度值</small></div></div><p id="metric-message" role="status"></p><button id="metric-export" class="button secondary" disabled>导出结果 CSV ↓</button><details class="metric-convention"><summary>查看计算约定</summary><p>彩色图按 round(0.299R + 0.587G + 0.114B) 转为 8 位灰度；透明像素先与白底合成。使用原始尺寸，不缩放。EN 使用 256 桶，SD 分母为 N，SF 各方向按有效相邻像素对归一化。浏览器解码与其他库可能有细微差异。</p></details></div></div></div><div class="metric-definitions">{cards}</div><div class="note-box"><strong>先固定评测协议，再比较方法。</strong><p>这三个指标描述图像统计特性，不是融合质量的完整结论。与论文数值比较时，需统一灰度转换、值域、裁剪与实现版本。{link(P['metricSource'],'查看完整融合评估工具箱')}</p></div></section>'''

def downloads(palettes):
    sections=[]
    for i,p in enumerate(palettes):
        sections.append(f'<article class="download-card"><div class="mini-swatches">'+''.join(f'<span style="background:{c}"></span>' for c in p['colors'])+f'</div><h3>{E(p["name"])}</h3><p>{E(p["note"])}</p><div class="card-actions"><a href="downloads/palette-{i+1}.svg" download>SVG 色板 ↓</a><a href="downloads/palette-{i+1}.json" download>JSON 色值 ↓</a></div></article>')
    return f'''<section class="wrap section compact-top"><div class="section-heading"><div><p class="eyebrow">READY FOR YOUR NEXT FIGURE</p><h2>下载后，就能开始画。</h2><p>本站原创基础模板，均可直接下载。示意数据仅用于演示排版。</p></div></div><div class="download-grid"><article class="download-card template-feature"><span class="file-type">SVG · 可编辑</span><h3>双模态融合框架图</h3><img src="downloads/fusion-diagram.svg" width="640" height="260" alt="可编辑双模态融合框架图示例"><p>包含两路输入、编码器、融合模块和输出。可在矢量编辑器中修改。</p><a class="button secondary" href="downloads/fusion-diagram.svg" download>下载框架图 ↓</a></article><article class="download-card"><span class="file-type">PYTHON · MATPLOTLIB</span><h3>论文折线图模板</h3><p>三组演示方法、明确的线型与标记，运行后导出 PDF 和 PNG。数据集中在脚本开头，便于替换。</p><div class="line-preview" aria-hidden="true"><span>——●—— 方法 A</span><span>– – ■ – – 方法 B</span><span>····▲···· 方法 C</span></div><a class="button secondary" href="downloads/plot_template.py" download>下载绘图脚本 ↓</a></article>{''.join(sections[:3])}</div></section>'''

def contribute():
    return '''<section class="wrap section compact-top contribute-layout"><form id="contribution-form" class="contribution-form"><h2>让好的资源，被更多同行找到。</h2><p>填写后生成投稿内容，可复制，或带到 GitHub 继续提交。</p><label>资源类型<select name="type" required><option>论文推荐</option><option>数据集</option><option>评估指标</option><option>团队档案</option><option>会议日程</option><option>会议期刊</option><option>招生信息</option><option>配色模板</option><option>内容勘误</option></select></label><label>名称 / 标题<input name="title" required maxlength="150" placeholder="例如：一个红外与可见光视频融合数据集"></label><label>官方来源链接<input name="source" type="url" required maxlength="1000" placeholder="https://…"></label><label>简介与补充信息<textarea name="description" required maxlength="4000" rows="6" placeholder="请写明用途、研究方向。会议信息请补充年份与时区，招生信息请补充有效时间。"></textarea></label><button class="button primary" type="submit">生成投稿内容 →</button><p class="small-note">此页不会自动发送信息。GitHub 提交需要你登录账号并确认发布。</p></form><aside class="submission-preview"><p class="eyebrow">CONTRIBUTION PREVIEW</p><h2>投稿预览</h2><p id="submission-help">完成左侧信息后，在这里检查生成的内容。</p><textarea id="submission-text" readonly rows="13" aria-label="生成的投稿内容" hidden></textarea><div class="card-actions" id="submission-actions" hidden><button id="submission-copy" class="button secondary">复制内容</button><a id="submission-github" class="button primary" target="_blank" rel="noopener noreferrer">前往 GitHub 提交 ↗</a></div><div class="note-box"><strong>推荐内容需要什么？</strong><p>真实名称、原始来源和简要说明。团队及论文信息请保留完整作者与机构；失效链接、过期日期也欢迎反馈。</p></div></aside></section>'''

def build_downloads(palettes):
    from datetime import datetime, timedelta, timezone
    target=ROOT/'downloads'
    target.mkdir(exist_ok=True)
    def escape(s): return str(s).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
    def fold(line):
        parts=[]; current=''
        for char in line:
            if len((current+char).encode())>75:
                parts.append(current); current=' '+char
            else: current+=char
        return '\r\n'.join(parts+[current])
    def calendar_text(events):
        lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//MMIFusion//Research Calendar//ZH','CALSCALE:GREGORIAN','METHOD:PUBLISH']
        for c,e in events:
            lines+=['BEGIN:VEVENT','UID:'+e['id']+'@mmifusion.github.io','DTSTAMP:'+P['verifiedAt'].replace('-','')+'T000000Z','SUMMARY:'+escape(c['name']+' · '+e['label'])]
            if e['kind']=='deadline':
                dt=datetime.fromisoformat(e['at']).astimezone(timezone.utc)
                lines+=['DTSTART:'+dt.strftime('%Y%m%dT%H%M%SZ'),'DTEND:'+(dt+timedelta(minutes=1)).strftime('%Y%m%dT%H%M%SZ')]
            else:
                lines+=['DTSTART;VALUE=DATE:'+e['start'].replace('-',''),'DTEND;VALUE=DATE:'+e['endExclusive'].replace('-','')]
            lines+=['DESCRIPTION:'+escape(e['original']+'\n官方来源：'+c['source']+'\n核对日期：'+P['verifiedAt']),'URL:'+c['source'],'END:VEVENT']
        return '\r\n'.join(fold(l) for l in lines+['END:VCALENDAR'])+'\r\n'
    events=[(c,e) for c in P['conferences'] for e in c['events']]
    for c,e in events: (target/(e['id']+'.ics')).write_bytes(calendar_text([(c,e)]).encode())
    (target/'mmifusion-calendar.ics').write_bytes(calendar_text(events).encode())
    for i,p in enumerate(palettes):
        swatches=''.join(f'<rect x="{20+j*120}" y="65" width="120" height="110" fill="{color}"/><text x="{80+j*120}" y="205" text-anchor="middle" font-size="15" fill="#333">{color}</text>' for j,color in enumerate(p['colors']))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="250" viewBox="0 0 640 250"><rect width="640" height="250" fill="white"/><g font-family="Arial,Microsoft YaHei,sans-serif"><text x="20" y="38" font-size="21" fill="#242b30">{E(p["name"])} · MMIFusion</text>{swatches}<text x="20" y="236" font-size="11" fill="#777">Original palette · CC BY 4.0 · 多模态信息融合</text></g></svg>'
        (target/f'palette-{i+1}.svg').write_text(svg)
        (target/f'palette-{i+1}.json').write_text(json.dumps(dict(p,creator='多模态信息融合',license='CC BY 4.0'),ensure_ascii=False,indent=2)+'\n')
    (target/'fusion-diagram.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="360" viewBox="0 0 1000 360"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 8 4 0 8" fill="none" stroke="#52616a"/></marker></defs><rect width="1000" height="360" fill="white"/><g font-family="Arial,Microsoft YaHei,sans-serif" text-anchor="middle" fill="#253B53"><text x="500" y="38" font-size="22">Dual-modal fusion · Editable figure template</text><rect x="40" y="90" width="140" height="80" rx="8" fill="#B7CDD9"/><rect x="40" y="215" width="140" height="80" rx="8" fill="#E5B8A2"/><rect x="260" y="90" width="170" height="80" rx="8" fill="#dfe8ee" stroke="#6488A6"/><rect x="260" y="215" width="170" height="80" rx="8" fill="#f8e9e2" stroke="#BF5545"/><rect x="540" y="150" width="180" height="90" rx="8" fill="#edf0ec" stroke="#619282"/><rect x="800" y="150" width="160" height="90" rx="8" fill="#f3f0e8" stroke="#BD854B"/><g font-size="19"><text x="110" y="135">Visible input</text><text x="110" y="260">Infrared input</text><text x="345" y="135">Encoder A</text><text x="345" y="260">Encoder B</text><text x="630" y="202">Fusion module</text><text x="880" y="202">Fused image</text></g><text x="500" y="339" font-size="12" fill="#888">Illustrative architecture · Replace with your method · MMIFusion · CC BY 4.0</text></g><g fill="none" stroke="#52616a" stroke-width="2" marker-end="url(#arrow)"><path d="M180 130H255"/><path d="M180 255H255"/><path d="M430 130H480V177H535"/><path d="M430 255H480V213H535"/><path d="M720 195H795"/></g></svg>''')
