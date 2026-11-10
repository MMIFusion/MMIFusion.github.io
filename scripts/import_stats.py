#!/usr/bin/env python3
"""Read only: import explicitly requested engagement counts from a WeChat XLSX."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from import_articles import read_rows

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'reads': '阅读数', 'likes': '点赞数', 'watching': '在看数', 'shares': '转发数'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('workbook', type=Path)
    args = parser.parse_args()
    source = json.loads((ROOT / 'data/articles.json').read_text())
    rows = dict(read_rows(args.workbook))
    columns = {name: col for col, name in rows[1].items()}
    records = []
    for article in source['articles']:
        row = rows[article['sourceRow']]
        assert row[columns['文章标题']] == article['title'], article['id']
        parsed = urlsplit(row[columns['文章链接']])
        assert parsed.hostname == 'mp.weixin.qq.com'
        query = parse_qs(parsed.query)
        essential = {k: query[k][0] for k in ['__biz', 'mid', 'idx', 'sn'] if k in query}
        url = 'https://mp.weixin.qq.com' + parsed.path + ('?' + urlencode(essential) if essential else '')
        assert hashlib.sha256(url.encode()).hexdigest()[:12] == article['id'], article['id']
        values = {}
        for key, label in FIELDS.items():
            raw = row.get(columns[label], '').strip()
            if not raw:
                values[key] = None
            else:
                assert raw.isdigit(), (article['sourceRow'], label, raw)
                values[key] = int(raw)
        records.append({'id': article['id'], 'sourceRow': article['sourceRow'], **values})
    result = {'sourceFile': args.workbook.name, 'sourceSheet': source['sourceSheet'],
              'snapshotDate': source['snapshotDate'], 'sourceColumns': {k: columns[v] for k, v in FIELDS.items()},
              'favoritesAvailable': '收藏数' in columns, 'records': records}
    assert not result['favoritesAvailable'], 'Review new favorite-count column before publishing.'
    (ROOT / 'data/article-stats.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Imported {len(records)} records; four original metrics; no favorite-count column.')

if __name__ == '__main__':
    main()
