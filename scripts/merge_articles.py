#!/usr/bin/env python3
"""Merge the original WeChat export and a Yiban export without publishing private fields."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlencode, urlsplit
import xml.etree.ElementTree as ET
import zipfile

from import_articles import ROOT, NS, classify, topics

REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
METRICS = {'reads': '阅读次数', 'likes': '点赞数', 'watching': '在看数', 'shares': '分享次数'}

def canonical_url(raw):
    p = urlsplit(raw.strip())
    if p.hostname != 'mp.weixin.qq.com' or not (p.path == '/s' or p.path.startswith('/s/')):
        raise ValueError('Expected a WeChat article URL')
    q = parse_qs(p.query)
    essential = {k: q[k][0] for k in ('__biz', 'mid', 'idx', 'sn') if k in q}
    if p.path == '/s' and len(essential) != 4:
        raise ValueError('Incomplete WeChat article identifier')
    return 'https://mp.weixin.qq.com' + p.path + ('?' + urlencode(essential) if essential else '')

def read_source(path):
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        relpath = 'xl/worksheets/_rels/sheet1.xml.rels'
        rels = {e.attrib['Id']: e.attrib['Target'] for e in ET.fromstring(z.read(relpath))} if relpath in z.namelist() else {}
        links = {e.attrib['ref']: rels[e.attrib[REL]] for e in sheet.findall('s:hyperlinks/s:hyperlink', NS)}
        rows = {}
        for row in sheet.findall('s:sheetData/s:row', NS):
            values = {}
            for cell in row.findall('s:c', NS):
                col = re.sub(r'\d+', '', cell.attrib['r'])
                value = cell.find('s:v', NS)
                text = value.text if value is not None else ''
                kind = cell.attrib.get('t')
                if kind == 's': text = strings[int(text)]
                elif kind == 'inlineStr': text = ''.join(cell.find('s:is', NS).itertext())
                elif text and kind not in ('str', 'e'):
                    number = float(text)
                    text = int(number) if number.is_integer() else number
                values[col] = text if text != '' else None
            rows[int(row.attrib['r'])] = values
        name = ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets/s:sheet', NS).attrib['name']
        return {'sheet': name, 'rows': rows, 'links': links}

def count(value):
    if value in (None, ''): return None
    if isinstance(value, str): value = int(value.replace(',', ''))
    if type(value) is not int or value < 0: raise ValueError('Invalid count: ' + str(value))
    return value

def public_article(row, known):
    url = row['url']
    article_id = hashlib.sha256(url.encode()).hexdigest()[:12]
    if article_id in known:
        article = dict(known[article_id])
    else:
        title = row['title']
        venue = re.search(r'TPAMI|Information Fusion|INFFUS|CVPRW|CVPR|ICCV|ECCV|NeurIPS|ICML|ICLR|AAAI|ACM MM|TCSVT|TIP|TMM|IJCV|GRSM|RA-L|\bPR\b', title, re.I)
        article = dict(id=article_id, title=title, date=row['publishedAt'][:10], url=url,
                       section=classify(title), topics=topics(title), venue=venue.group() if venue else '')
        if '研究单位与代表成果' in title:
            article['section'] = '学术社区'
            article['topics'] = list(dict.fromkeys(article['topics'] + ['研究团队']))
        if '资源合集' in title and '数据集' in title:
            article['section'] = '综述与入门'
    article.update(sourceFile=row['sourceFile'], sourceSheet=row['sourceSheet'], sourceRow=row['sourceRow'])
    if row.get('alias'): article['urlAliases'] = [row['alias']]
    return article

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old_workbook', type=Path)
    parser.add_argument('new_workbook', type=Path)
    parser.add_argument('--old-date', required=True)
    parser.add_argument('--new-date', required=True)
    parser.add_argument('--old-name')
    parser.add_argument('--new-name')
    parser.add_argument('--exclude-row', type=int, action='append', default=[])
    parser.add_argument('--workbook-data', type=Path, required=True, help='Local, private intermediate JSON')
    args = parser.parse_args()
    for date in (args.old_date, args.new_date): datetime.strptime(date, '%Y-%m-%d')
    previous = json.loads((ROOT/'data/articles.json').read_text())
    known = {a['id']: a for a in previous['articles']}
    old, new = read_source(args.old_workbook), read_source(args.new_workbook)
    assert old['rows'][1]['B'] == '文章标题' and new['rows'][2]['A'] == '标题'
    assert all(new['rows'][2][c] == label for c, label in {'I':'阅读次数','U':'分享次数','AB':'在看数','AC':'点赞数'}.items())
    sources = []
    for path, source, name, date, columns in [
        (args.old_workbook, old, args.old_name or args.old_workbook.name, args.old_date, {'reads':'J','likes':'K','watching':'N','shares':'O'}),
        (args.new_workbook, new, args.new_name or args.new_workbook.name, args.new_date, {'reads':'I','likes':'AC','watching':'AB','shares':'U'}),
    ]:
        sources.append(dict(sourceFile=name, sourceSheet=source['sheet'], snapshotDate=date,
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest(), sourceColumns=columns))
    merged = []
    for n, raw in old['rows'].items():
        if n == 1 or not raw.get('B'): continue
        url = canonical_url(str(raw['F']))
        merged.append(dict(title=raw['B'], publishedAt=raw['C'], position=raw['D'], url=url,
            sourceFile=sources[0]['sourceFile'], sourceSheet=old['sheet'], sourceRow=n,
            snapshotDate=args.old_date, metrics={k:count(raw.get(c)) for k,c in sources[0]['sourceColumns'].items()},
            readers=None, favorites=None, comments=count(raw.get('M')), mergeNote='保留旧表记录'))
    assert len({r['url'] for r in merged}) == len(merged), 'Duplicate original URLs need review'
    original_ids = {hashlib.sha256(r['url'].encode()).hexdigest()[:12] for r in merged}
    assert original_ids.issubset(known), 'Original workbook differs from the existing site archive'
    matches, excluded = [], []
    for n, raw in new['rows'].items():
        if n <= 2 or not raw.get('A'): continue
        if n in args.exclude_row:
            excluded.append(dict(sourceFile=sources[1]['sourceFile'], sourceRow=n, title=raw['A'], reason='用户确认：统计错误记录，不收录、不计入榜单'))
            continue
        raw_url = new['links'].get('A'+str(n))
        if not raw_url: raise ValueError(f'New row {n} has no title hyperlink; requires review')
        url = canonical_url(raw_url)
        stamp = f"{raw['C']} {int(raw['D']):02d}:{int(raw['E']):02d}:00"
        row = dict(title=raw['A'], publishedAt=stamp, position=raw['B'], url=url,
            sourceFile=sources[1]['sourceFile'], sourceSheet=new['sheet'], sourceRow=n,
            snapshotDate=args.new_date, metrics={k:count(raw.get(c)) for k,c in sources[1]['sourceColumns'].items()},
            readers=count(raw.get('G')), favorites=count(raw.get('AA')), comments=count(raw.get('AD')), mergeNote='新增文章')
        exact = [r for r in merged if r['url'] == url]
        # Only a unique cross-format match on all three fields is eligible.
        # Never deduplicate by title alone, nor merge two distinct long article IDs.
        same = [r for r in merged if r['title']==row['title'] and r['publishedAt'][:10]==row['publishedAt'][:10]
                and str(r['position'])==str(row['position']) and r['sourceFile']==sources[0]['sourceFile']
                and urlsplit(r['url']).path=='/s' and urlsplit(url).path.startswith('/s/')]
        candidates = exact or same
        if len(candidates)>1: raise ValueError('Ambiguous article: '+row['title'])
        if candidates:
            target=candidates[0]
            matches.append(dict(title=row['title'], oldRow=target['sourceRow'], newRow=n,
                existingUrl=target['url'], newUrl=url, basis='同一公众号、标题、发布日期、图文位置唯一匹配' if not exact else '相同文章链接'))
            # Keep established URL/ID so bookmarks remain valid; other fields use the latest export.
            row.update(url=target['url'], alias=url,
                       mergeNote='合并重复文章，采用新表统计；保留旧链接与文章编号')
            merged[merged.index(target)]=row
        else: merged.append(row)
    merged.sort(key=lambda r:(r['publishedAt'],r['title']),reverse=True)
    articles=[public_article(r,known) for r in merged]
    records=[dict(id=a['id'],sourceFile=r['sourceFile'],sourceSheet=r['sourceSheet'],sourceRow=r['sourceRow'],
                  snapshotDate=r['snapshotDate'],**r['metrics']) for a,r in zip(articles,merged)]
    dates=sorted({r['snapshotDate'] for r in records})
    metadata=dict(sourceFile='合并文章索引',sourceSheet='合并文章',snapshotDate=args.new_date,sources=sources)
    payload=dict(metadata,latestArticleDate=max(a['date'] for a in articles),articles=articles)
    stats=dict(metadata,snapshotDates=dates,favoritesAvailable=False,
               favoritesNote='两份导出表的收藏字段覆盖不完整，未纳入网站统计。',records=records)
    for name,value in [('articles.json',payload),('article-stats.json',stats)]:
        (ROOT/'data'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    private=dict(merged=merged,sources=sources,original=old,latest=new,matches=matches,excluded=excluded,
                 summary=dict(original=len(original_ids),newRows=len(new['rows'])-2,excluded=len(excluded),
                              overlap=len(matches),added=len(merged)-len(original_ids),total=len(merged)))
    args.workbook_data.parent.mkdir(parents=True,exist_ok=True)
    args.workbook_data.write_text(json.dumps(private,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(private['summary'],ensure_ascii=False))

if __name__ == '__main__': main()
