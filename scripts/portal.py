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
def feedback(url, title='资源信息勘误'):
    return 'contribute.html?'+urlencode({'type':'内容勘误','title':title,'source':url})
def source(url): return f'<div class="source-line">{link(url,"官方来源")}<span>核对于 {P["verifiedAt"]}</span><a class="source-feedback" href="{E(feedback(url))}">反馈勘误 →</a></div>'
def related(query): return 'papers.html?'+urlencode({'q':query})

def filterbar(kind,placeholder,filters):
    selects=''.join(f'<label>{label}<select data-card-filter="{key}"><option value="">全部{label}</option>'+''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in values)+'</select></label>' for key,label,values in filters)
    return f'<div class="directory-toolbar"><label class="directory-search"><span aria-hidden="true">⌕</span><input data-card-search type="search" aria-label="{placeholder}" placeholder="{placeholder}"></label>{selects}<button class="reset-button" data-card-reset>重置</button><p class="directory-count" aria-live="polite"></p></div>'
def empty(): return '<div class="empty-state directory-empty" hidden><h3>没有匹配的内容</h3><p>试试其他关键词，或清除筛选条件。</p><button class="button secondary" data-card-reset>清除筛选</button></div>'
def filterattrs(record,search,**filters):
    return f'data-directory-card data-search="{E(search)}" '+ ' '.join(f'data-{key}="{E(json.dumps(value,ensure_ascii=False))}"' for key,value in filters.items())

def deadline_strip():
    events=[(c,e) for c in P['conferences'] for e in c['events']]
    items=''.join(f'<a href="calendar.html#{e["id"]}" class="deadline-teaser" data-calendar-event="{E(json.dumps(e))}"><span>{E(c["name"])} · {E(e["label"])}</span><strong '+(f'data-countdown="{e["at"]}"' if e['kind']=='deadline' else '')+'>'+(e['at'][:10].replace('-','.') if e['kind']=='deadline' else e['start'].replace('-','.'))+'</strong><small>'+('距离截止 · 实时更新' if e['kind']=='deadline' else '官方日期 · 具体时刻未列明')+'</small></a>' for c,e in events)
    return '<section class="wrap deadline-strip" aria-label="近期学术节点"><div class="deadline-caption"><span class="red-dot"></span><strong>学术日历</strong><a href="calendar.html">查看全部 →</a></div>'+items+'<p class="deadline-empty" hidden>已收录的日程均已结束。<a href="calendar.html">查看往期节点 →</a></p></section>'

def dataset_showcase():
    cards=''.join(f'<article class="dataset-preview"><a class="dataset-visual dataset-{d["id"]}" href="{E(d["catalog"])}"><img src="assets/datasets/{d["id"]}.png" alt="{E(d["name"])} 数据集红外与可见光图像示例" loading="lazy"><span>{E(d["label"])}<b>↗</b></span></a><div class="dataset-body"><p class="eyebrow">OPEN DATA / {E(d["id"].upper())}</p><h3>{E(d["name"])}</h3><p>{E(d["description"])}</p><div class="card-actions"><a class="text-link" href="{E(d["catalog"])}">查看数据档案 →</a>{link(d["source"],"原始项目")}</div></div></article>' for d in P['datasets'])
    return f'<section class="wrap section dataset-section"><div class="section-heading"><div><p class="eyebrow">03 / FROM PAPER TO EXPERIMENT</p><h2>找到数据，让想法落地。</h2><p>真实场景，多种模态。在站内查看完整介绍、团队与数据获取入口。</p></div><a class="text-link" href="datasets.html">全部数据资源 →</a></div><div class="dataset-previews">{cards}</div><p class="reading-provenance">示例图来自已收录的数据集介绍，权利归原作者；详情、许可及使用条件见原始项目。</p></section>'

def calendar():
    from datetime import date, timedelta
    cards=[]
    for c in P['conferences']:
        events=[]
        for e in c['events']:
            last=(date.fromisoformat(e['endExclusive'])-timedelta(days=1)).isoformat() if e['kind']=='date' else ''
            span=e.get('start','')+(' 至 '+last if last and last!=e['start'] else '')
            time=f'<time data-local-time="{e["at"]}">{E(e["original"])}</time>' if e['kind']=='deadline' else f'<time datetime="{e["start"]}">{E(span)}</time>'
            countdown=f'<span class="countdown" data-countdown="{e["at"]}">{E(e["original"])}</span>' if e['kind']=='deadline' else '<span class="date-only">按官方日期显示</span>'
            eventsource=link(e.get('source',c['source']),'节点来源')
            events.append(f'<div class="event-row" id="{e["id"]}" data-calendar-event="{E(json.dumps(e))}"><div><h3>{E(e["label"])}</h3>{time}<small>{E(e["original"])}</small></div><div class="event-actions">{countdown}<a href="downloads/{e["id"]}.ics" download>加入日历 ↓</a>{eventsource}</div></div>')
        status=(['已公布日程'] if c['events'] else [])+(['待补充日程'] if c.get('pending') else [])
        attrs=filterattrs(c,' '.join([c['name'],c['field'],c['description'],c['location']]),field=[c['field']],status=status)
        pending=f'<div class="conference-pending"><strong>待官方更新</strong><p>{E(c["pending"])}</p></div>' if c.get('pending') else ''
        cards.append(f'<article id="{c["id"]}" class="conference-card" data-pending="{str(bool(c.get("pending"))).lower()}" {attrs}><div class="conference-title"><div><p class="eyebrow">{E(c["field"])}</p><h2>{E(c["name"])}</h2><div class="conference-meta"><span class="ccf-badge ccf-a">CCF A</span><span>{E(c["location"])}</span></div></div>{link(c["source"],"会议官网")}</div><p class="conference-description">{E(c["description"])}</p>{"".join(events)}{pending}{source(c["source"])}</article>')
    return f'''<section class="wrap section compact-top" data-directory="calendar"><div class="calendar-scope"><p><strong>2027 · 图像融合与多模态研究相关 A 类会议</strong></p><p>收录 CVPR、ICCV、ACM MM、ICLR、ICML、NeurIPS、AAAI 与 ACL。分类参考 CCF 第七版；ACL 更适合语言与视觉交叉研究。已公布时间均链接官方来源，待公布项保留入口。</p></div>{filterbar('calendar','搜索会议名称、地点或研究方向',[('field','领域',list(dict.fromkeys(c['field'] for c in P['conferences']))),('status','日程',['已公布日程','待补充日程'])])}<div class="calendar-tools"><p>精确截止可切换时区；仅公布日期的节点保留为全天。</p><label>时间显示 <select id="calendar-timezone"><option value="Asia/Shanghai">北京时间 UTC+8</option><option value="UTC">协调世界时 UTC</option><option value="local">浏览器当地时间</option></select></label><a href="downloads/mmifusion-calendar.ics" download class="button secondary">下载已公布日程 ↓</a></div><div class="calendar-view-options"><label><input type="checkbox" id="calendar-upcoming">只看未结束节点</label><p id="calendar-event-summary" role="status"></p><span>保留待公布项 · 临近截止突出显示 · 日期节点不作精确倒计时</span></div><div class="conference-grid">{''.join(cards)}</div>{empty()}<p class="small-note">AoE 为 UTC−12。日历文件只包含已经公布的节点，可导入系统日历；文件为本次信息快照，后续变更请查看会议官网。</p></section>'''

def teams():
    cards=[]
    for t in P['teams']:
        attrs=filterattrs(t,' '.join([t['name'],t['institution'],t['city'],t['description'],*t['tags'],*t.get('aliases',[])]),institution=[t['institution']],city=t.get('cities',[t['city']]),topic=t['tags'])
        opportunity=f'<a href="opportunities.html#{t["opportunity"]}">招生信息 →</a>' if t['opportunity'] else ''
        badge='<span class="team-extension">相关方向</span>' if t.get('extension') else ''
        detail_links=''.join(link(item['url'],item['label']) for item in t['links'])
        verification={'official':'主要信息已核对','conference':'依据会议官方简介','publication':'依据论文与作者项目','archive':'资料整理 · 主页待核'}[t['verification']]
        cards.append(f'''<article class="profile-card team-card" id="{t['id']}" {attrs}>
<div class="team-card-heading"><div class="profile-badge" aria-hidden="true">{E(t['institution'][:2])}</div><div class="profile-heading"><p>{E(t['institution'])} · {E(t['city'])}</p><h2>{E(t['name'])}</h2></div>{badge}</div>
{tags(t['tags'])}<p class="profile-description">{E(t['description'])}</p>
<details class="team-detail"><summary>研究资料与学术入口<span aria-hidden="true">＋</span></summary><div><p>{E(t['note'])}</p><div class="team-detail-links">{detail_links}</div></div></details>
<div class="card-actions">{link(t['source'],t.get('sourceLabel','访问主页'))}<a href="{E(related(t['relatedQuery']))}">相关解读 →</a>{opportunity}<button class="text-link" data-copy-link="teams.html#{t['id']}">复制链接</button></div>
<div class="source-line"><span>{verification} · {P['teamCollection']['updatedAt']}</span><a href="{E(feedback(t['source'],t['name']+' · 团队信息勘误'))}">反馈勘误 →</a></div></article>''')
    cities=list(dict.fromkeys(city for t in P['teams'] for city in t.get('cities',[t['city']])))
    institutions=len(set(t['institution'] for t in P['teams']))
    overview=f'<div class="team-overview"><div><p class="eyebrow">PEOPLE, IDEAS & CONNECTIONS</p><h2>找到同行，也找到新的研究线索。</h2><p>一人一卡，从研究方向与所在机构出发，认识图像融合和多模态研究领域的同行。</p></div><div class="team-totals"><div><strong>{len(P["teams"])}</strong><span>位研究者</span></div><div><strong>{institutions}</strong><span>所研究机构</span></div></div></div>'
    return f'<section class="wrap section compact-top" data-directory="teams">{overview}{filterbar("teams","搜索学者、学校或研究方向",[("institution","机构",list(dict.fromkeys(t["institution"] for t in P["teams"]))),("city","地区",cities),("topic","方向",sorted(set(x for t in P["teams"] for x in t["tags"])))])}<p class="team-reading-note">按姓名、学校或研究方向查找；展开个人资料，继续查看本人主页、论文与项目。</p><div class="profile-grid">{"".join(cards)}</div>{empty()}<div class="directory-bottom"><p>整理自所提供的团队资料与公开学术主页；任职、成员与研究动态以原始来源为准。</p><a href="contribute.html?type=团队档案" class="text-link">推荐研究团队 →</a></div></section>'

def opportunities():
    cards=[]
    for o in P['opportunities']:
        attrs=filterattrs(o,' '.join([o['title'],o['institution'],o['team'],*o['tags']]),city=[o['city']],type=o['types'])
        cards.append(f'<article class="opportunity-card" id="{o["id"]}" {attrs}><div class="opportunity-header"><div><p class="eyebrow">{E(o["institution"])} · {E(o["city"])}</p><h2>{E(o["title"])}</h2><p>{E(o["team"])}</p></div><span class="status-label open-status">{E(o["status"])}</span></div>{tags(o["types"])}<p>{E(o["description"])}</p><details><summary>申请准备与联系渠道</summary><p>{E(o["requirements"])}</p><p>请在官方主页查看联系方式。本站不代收申请材料。</p></details><div class="card-actions">{link(o["source"],"查看官方招募说明","button primary")}<a href="teams.html#{o["teamId"]}" class="text-link">了解团队 →</a><button class="text-link" data-copy-link="opportunities.html#{o["id"]}">复制条目链接</button></div>{source(o["source"])}</article>')
    return f'<section class="wrap section compact-top" data-directory="opportunities">{filterbar("opportunities","搜索学校、导师或研究方向",[("type","类别",["硕士","博士","博士后","科研助理"]),("city","城市",["大连"])])}<div class="opportunity-list">{"".join(cards)}</div>{empty()}<div class="directory-bottom"><p>长期招募按导师公开说明收录，不等同于保证当前名额。</p><a class="text-link" href="contribute.html?type=招生信息">提交招生信息 →</a></div></section>'

def venues():
    cards=[]
    for v in P['venues']:
        attrs=filterattrs(v,' '.join([v['name'],v['fullName'],*v['tags'],*v.get('aliases',[])]),type=[v['type']],topic=v['tags'],ccf=[v['ccf']])
        calendarlink=f'<a href="calendar.html#{v["calendar"]}">查看日程 →</a>' if v['calendar'] else ''
        grade='CCF '+v['ccf'] if v['ccf']!='未收录' else '领域补充 · 未收录'
        gradecss=v['ccf'].lower() if v['ccf']!='未收录' else 'extra'
        guide=link(v['guide'],v.get('guideLabel','作者指南')) if v['guide'] else ''
        guide_note=f'<p class="venue-guide-note">{E(v["guideNote"])}</p>' if v.get('guideNote') else ''
        reading='papers.html?'+urlencode({'venue':v['articleVenue']} if v['articleVenue'] else {'q':v['relatedQuery']})
        fullname=f'<p class="venue-fullname">{E(v["fullName"])}</p>' if v['fullName']!=v['name'] else ''
        cards.append(f'<article class="venue-card" id="venue-{v["id"]}" {attrs}><div class="venue-top"><div><span class="ccf-badge ccf-{gradecss}">{grade}</span><span class="venue-type">{E(v["type"])}</span></div><label class="compare-check"><input type="checkbox" data-compare="{v["id"]}">加入对比</label></div><h2>{E(v["name"])}</h2>{fullname}{tags(v["tags"])}<p>{E(v["scope"])}</p><div class="fit-note"><strong>选刊思路</strong><p>{E(v["fit"])}</p></div><div class="card-actions">{link(v["source"],v.get("sourceLabel","征稿范围"))}{guide}<a href="{E(reading)}">相关解读 →</a>{calendarlink}</div>{guide_note}{source(v["source"])}</article>')
    spotlight=f'<aside class="venue-spotlight"><div><span class="eyebrow">JOURNAL SPOTLIGHT</span><h2>Information Fusion</h2><p>聚焦多源信息融合的期刊 · 图像融合与多模态研究</p></div><a class="button secondary" href="venues.html?type=期刊&amp;q=Information%20Fusion#venue-information-fusion">查看期刊档案 →</a></aside>'
    counts=''.join(f'<div><strong>{sum(v["ccf"]==rank for v in P["venues"])}</strong><span>{"CCF "+rank+" 类" if rank!="未收录" else "领域补充"}</span></div>' for rank in ['A','B','C','未收录'])
    return f'''<section class="wrap section compact-top" data-directory="venues"><div class="venue-overview"><div><p class="eyebrow">FIND THE RIGHT VENUE</p><h2>{len(P['venues'])} 个会议期刊，按研究方向选。</h2><p>依次展示 CCF A、B、C 类与领域补充。同级按图像融合相关性组织，不构成同级排名；先看研究问题，再看分类。</p></div><div class="venue-totals">{counts}</div></div>{spotlight}{filterbar('venues','搜索简称、完整名称或研究方向',[('type','类型',['会议','期刊']),('ccf','分类',['A','B','C','未收录']),('topic','方向',sorted(set(t for v in P['venues'] for t in v['tags'])))])}<p class="small-note venue-reading-note">征稿范围来自官方页面；“选刊思路”为本站整理建议。未收录不代表质量较低，录用与否取决于具体工作。</p><div class="venue-grid">{''.join(cards)}</div>{empty()}<details class="venue-basis" id="ccf-basis"><summary>分类依据与排序说明</summary><p>分类参考《{E(P['venueClassification']['title'])}》正式版 PDF。Information Fusion 等未收录条目不强行归入 A、B、C。会议和期刊跨领域的声誉不能仅由这一分类概括。</p><p>此版中的 TMM、ICLR 为 A 类，IJCAI 为 B 类，PRCV 为 C 类。投稿前也请核对所在单位采用的目录版本。{link(P['venueClassification']['source'],'CCF 第七版公示说明')}</p></details><div class="comparison-bar"><div><span id="compare-count" role="status">选择 2–3 个会议期刊进行对比</span><small id="compare-selection"></small></div><div class="comparison-actions"><button class="text-link" type="button" id="compare-clear" disabled>清空所选</button><button class="button secondary" id="compare-open" disabled>比较所选项目 →</button></div></div><dialog id="compare-dialog" class="portal-dialog" aria-labelledby="compare-title"><div class="dialog-heading"><h2 id="compare-title">会议期刊对比</h2><button type="button" data-close-dialog aria-label="关闭对比" autofocus>×</button></div><div id="compare-content"></div></dialog></section>'''

def metrics():
    cards=''.join(f'<article class="metric-definition"><span class="metric-code">{m["id"]}</span><h3>{E(m["name"])}</h3><code>{E(m["formula"])}</code><p>{E(m["description"])}</p><small>{E(m["caution"])}</small></article>' for m in P['metrics'])
    return f'''<section class="wrap section compact-top"><div class="metric-lab" id="metric-lab"><div class="lab-heading"><div><p class="eyebrow">FUSION IMAGE LAB</p><h2>上传一张图，试算三个指标。</h2><p>图片在当前浏览器内计算，不上传服务器。</p></div><a class="text-link" href="downloads/fusion_metrics.py" download>下载 Python 实现 ↓</a></div><div class="lab-layout"><div class="lab-input"><div class="canvas-frame"><canvas id="metric-canvas" width="256" height="192" aria-label="待评估图像预览"></canvas></div><label class="button primary upload-button">选择本地图片<input type="file" id="metric-file" accept="image/png,image/jpeg,image/webp,image/bmp"></label><p class="small-note">PNG / JPEG / WebP / BMP · 最大 20 MB、1600 万像素</p><div class="sample-buttons"><span>试用示例</span><button data-metric-sample="gradient">渐变</button><button data-metric-sample="checker">棋盘</button><button data-metric-sample="flat">纯灰</button></div></div><div class="lab-results"><p id="metric-image-info">选择示例或上传图片</p><div class="metric-values" aria-live="polite"><div><span>EN · 信息熵</span><strong id="metric-en">—</strong><small>bit</small></div><div><span>SD · 标准差</span><strong id="metric-sd">—</strong><small>灰度值</small></div><div><span>SF · 空间频率</span><strong id="metric-sf">—</strong><small>灰度值</small></div></div><p id="metric-message" role="status"></p><button id="metric-export" class="button secondary" disabled>导出结果 CSV ↓</button><details class="metric-convention"><summary>查看计算约定</summary><p>彩色图按 round(0.299R + 0.587G + 0.114B) 转为 8 位灰度；透明像素先与白底合成。使用原始尺寸，不缩放。EN 使用 256 桶，SD 分母为 N，SF 各方向按有效相邻像素对归一化。浏览器解码与其他库可能有细微差异。</p></details></div></div></div><div class="metric-definitions">{cards}</div><div class="note-box"><strong>先固定评测协议，再比较方法。</strong><p>这三个指标描述图像统计特性，不是融合质量的完整结论。与论文数值比较时，需统一灰度转换、值域、裁剪与实现版本。{link(P['metricSource'],'查看完整融合评估工具箱')}</p></div></section>'''

def downloads():
    return f'''<section class="wrap section compact-top"><div class="section-heading"><div><p class="eyebrow">READY FOR YOUR NEXT FIGURE</p><h2>下载后，就能开始画。</h2><p>本站原创基础模板，均可直接下载。示意数据仅用于演示排版。</p></div></div><div class="download-grid"><article class="download-card template-feature"><span class="file-type">SVG · 可编辑</span><h3>双模态融合框架图</h3><img src="downloads/fusion-diagram.svg" width="640" height="260" alt="可编辑双模态融合框架图示例"><p>包含两路输入、编码器、融合模块和输出。可在矢量编辑器中修改。</p><a class="button secondary" href="downloads/fusion-diagram.svg" download>下载框架图 ↓</a></article><article class="download-card"><span class="file-type">PYTHON · MATPLOTLIB</span><h3>论文折线图模板</h3><p>三组演示方法、明确的线型与标记，运行后导出 PDF 和 PNG。数据集中在脚本开头，便于替换。</p><div class="line-preview" aria-hidden="true"><span>——●—— 方法 A</span><span>– – ■ – – 方法 B</span><span>····▲···· 方法 C</span></div><a class="button secondary" href="downloads/plot_template.py" download>下载绘图脚本 ↓</a></article></div></section>'''

def contribute():
    return '''<section class="wrap section compact-top contribute-layout"><form id="contribution-form" class="contribution-form"><h2>让好的资源，被更多同行找到。</h2><p>填写后生成投稿内容，可复制，或带到 GitHub 继续提交。</p><label>资源类型<select name="type" required><option>论文推荐</option><option>数据集</option><option>评估指标</option><option>团队档案</option><option>会议日程</option><option>会议期刊</option><option>招生信息</option><option>配色模板</option><option>内容勘误</option></select></label><label>名称 / 标题<input name="title" required maxlength="150" placeholder="例如：一个红外与可见光视频融合数据集"></label><label>官方来源链接<input name="source" type="url" required maxlength="1000" placeholder="https://…"></label><label>简介与补充信息<textarea name="description" required maxlength="4000" rows="6" placeholder="请写明用途、研究方向。会议信息请补充年份与时区，招生信息请补充有效时间。"></textarea></label><button class="button primary" type="submit">生成投稿内容 →</button><p class="small-note">此页不会自动发送信息。GitHub 提交需要你登录账号并确认发布。</p></form><aside class="submission-preview"><p class="eyebrow">CONTRIBUTION PREVIEW</p><h2>投稿预览</h2><p id="submission-help" role="status">完成左侧信息后，在这里检查生成的内容。</p><textarea id="submission-text" readonly rows="13" aria-label="生成的投稿内容" hidden></textarea><div class="card-actions" id="submission-actions" hidden><button id="submission-copy" class="button secondary">复制内容</button><a id="submission-github" class="button primary" target="_blank" rel="noopener noreferrer">前往 GitHub 提交 ↗</a></div><div class="note-box"><strong>推荐内容需要什么？</strong><p>真实名称、原始来源和简要说明。团队及论文信息请保留完整作者与机构；失效链接、过期日期也欢迎反馈。</p></div></aside></section>'''

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
            event_source=e.get('source',c['source'])
            lines+=['DESCRIPTION:'+escape(e['original']+'\n官方来源：'+event_source+'\n核对日期：'+P['verifiedAt']),'URL:'+event_source,'END:VEVENT']
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
