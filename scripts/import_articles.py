#!/usr/bin/env python3
"""Import public article fields from a WeChat export. Uses Python stdlib only."""
import argparse
import collections
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, urlencode

ROOT = Path(__file__).resolve().parents[1]
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def read_rows(path):
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        for row in sheet.findall('s:sheetData/s:row', NS):
            values = {}
            for cell in row.findall('s:c', NS):
                column = re.sub(r'\d+', '', cell.attrib['r'])
                value = cell.find('s:v', NS)
                text = value.text if value is not None else ''
                if cell.attrib.get('t') == 's':
                    text = strings[int(text)]
                elif cell.attrib.get('t') == 'inlineStr':
                    text = ''.join(cell.find('s:is', NS).itertext())
                values[column] = text or ''
            yield int(row.attrib['r']), values

def classify(title):
    if re.search('配色|模型图|封面', title): return '配色与绘图'
    if re.search('IEEE Transactions|投稿必看|期刊推荐', title): return '投稿参考'
    if re.search('学术速递|顶刊速递|录用情况', title): return '论文速递'
    if re.search('CSIG|修仙|联合声明', title): return '学术社区'
    if re.search(r'西瓜书|170\+篇|综述', title): return '综述与入门'
    return '论文解读'

def topics(title):
    rules = [
        ('红外与可见光', r'红外|可见光|RGB.?T|热成像|热红外'),
        ('图像融合', r'融合|Fuse|Fusion|MEF|MFF'),
        ('三维感知', r'3D|三维|LiDAR|LIDAR|雷达|点云|定位|自动驾驶'),
        ('图像配准', r'配准|对齐|匹配|Match'),
        ('图像恢复', r'恢复|复原|退化|去雾|噪|低光|低照|超分'),
        ('数据集与基准', r'数据集|基准|Bench'),
        ('视频融合', r'视频融合|VideoFusion|VFuse|MAVFusion|VF-Bench'),
        ('医学影像', r'医学|病理|CoReFuse-Med|MorVess'),
        ('遥感与多光谱', r'遥感|SAR|光谱|全色|卫星|PanScale'),
        ('多曝光与多聚焦', r'多曝光|多聚焦|MEF|MFF'),
        ('评估与指标', r'质量评估|融合评估|先解耦再评价'),
        ('研究团队', r'团队|CSIG'),
    ]
    return [name for name, pattern in rules if re.search(pattern, title, re.I)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--snapshot-date', required=True, help='YYYY-MM-DD, export snapshot date')
    args = parser.parse_args()
    articles, seen = [], set()
    for row_no, row in read_rows(args.workbook):
        if row_no == 1 or not row.get('B'): continue
        title, raw_url = row['B'], row['F']
        parsed = urlsplit(raw_url)
        if parsed.hostname != 'mp.weixin.qq.com': raise ValueError(f'Unexpected article host in row {row_no}')
        query = parse_qs(parsed.query)
        essential = {k: query[k][0] for k in ['__biz', 'mid', 'idx', 'sn'] if k in query}
        url = 'https://mp.weixin.qq.com' + parsed.path + ('?' + urlencode(essential) if essential else '')
        if url in seen: continue
        seen.add(url)
        venue = re.search(r'TPAMI|Information Fusion|INFFUS|CVPRW|CVPR|ICCV|ECCV|NeurIPS|ICML|ICLR|AAAI|ACM MM|TCSVT|TIP|TMM|IJCV|GRSM|RA-L|\bPR\b', title, re.I)
        articles.append(dict(id=hashlib.sha256(url.encode()).hexdigest()[:12], title=title,
                             date=row['C'][:10], url=url, section=classify(title), topics=topics(title),
                             venue=venue.group() if venue else '', sourceRow=row_no))
    articles.sort(key=lambda a: (a['date'], a['sourceRow']), reverse=True)
    payload = dict(sourceFile=args.workbook.name, sourceSheet='微信文章导出',
                   snapshotDate=args.snapshot_date, latestArticleDate=max(a['date'] for a in articles),
                   articles=articles)
    (ROOT / 'data/articles.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(articles=len(articles), sections=dict(collections.Counter(a['section'] for a in articles)),
                         topics=dict(collections.Counter(t for a in articles for t in a['topics']))), ensure_ascii=False))

if __name__ == '__main__': main()
