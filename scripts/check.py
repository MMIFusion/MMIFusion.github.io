#!/usr/bin/env python3
"""Validate source fidelity, URL safety, and generated internal links."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
errors = []
articles = json.loads((ROOT/'data/articles.json').read_text())['articles']
ids = [a['id'] for a in articles]
assert len(ids) == len(set(ids)), 'Duplicate article IDs'
assert len(set(a['url'] for a in articles)) == len(articles), 'Duplicate article URLs'
for a in articles:
    url = urlsplit(a['url'])
    assert url.scheme == 'https' and url.hostname == 'mp.weixin.qq.com', a['id']
    assert a['title'] and len(a['date']) == 10
    if url.path == '/s':
        assert all(k in parse_qs(url.query) for k in ('__biz','mid','idx','sn')), a['id']

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1, self.articles = [], [], 0, []
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='h1': self.h1+=1
        if 'id' in attrs: self.ids.append(attrs['id'])
        if 'data-article-id' in attrs: self.articles.append(attrs['data-article-id'])
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
        if tag=='a' and attrs.get('target')=='_blank':
            if not {'noopener','noreferrer'}.issubset(set(attrs.get('rel','').split())): errors.append('Unsafe target blank')

pages={}
for file in OUT.glob('*.html'):
    page=Page(); page.feed(file.read_text()); pages[file.name]=page
    if page.h1!=1: errors.append(f'{file.name}: expected one h1')
    if len(page.ids)!=len(set(page.ids)): errors.append(f'{file.name}: duplicate DOM ids')
for name,page in pages.items():
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        target=unquote(parsed.path).lstrip('/') or (name if parsed.fragment else 'index.html')
        if not (OUT/target).exists(): errors.append(f'{name}: missing {target}')
        if parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            errors.append(f'{name}: missing anchor {link}')
assert set(pages['papers.html'].articles)==set(ids), 'Full archive is incomplete'
palettes=json.loads((ROOT/'data/community.json').read_text())['palettes']
for index, palette in enumerate(palettes,1):
    for extension in ('svg','json'):
        assert f'downloads/palette-{index}.{extension}' in pages['palettes.html'].links, 'Palette download missing'
    download=json.loads((OUT/'downloads'/f'palette-{index}.json').read_text())
    assert download['colors']==palette['colors'] and download['name']==palette['name']

# Historical WeChat engagement remains separate from live website PV and local saves.
stats = json.loads((ROOT/'data/article-stats.json').read_text())
assert stats['snapshotDate'] == json.loads((ROOT/'data/articles.json').read_text())['snapshotDate']
assert stats['favoritesAvailable'] is False
assert stats['sourceColumns'] == {'reads':'J','likes':'K','watching':'N','shares':'O'}
assert len(stats['records']) == len(ids)
assert {r['id'] for r in stats['records']} == set(ids)
for record in stats['records']:
    for metric in ('reads','likes','watching','shares'):
        assert record[metric] is None or (type(record[metric]) is int and record[metric] >= 0)
assert len([r for r in stats['records'] if r['reads'] is not None]) >= 10

# Calendar files must encode real UTC instants or explicit all-day dates,
# preserve Unicode folding, and agree with the source records.
from datetime import datetime, timezone
portal=json.loads((ROOT/'data/portal.json').read_text())
event_ids=[]
for conference in portal['conferences']:
    assert urlsplit(conference['source']).scheme == 'https'
    for event in conference['events']:
        event_ids.append(event['id'])
        raw=(OUT/'downloads'/(event['id']+'.ics')).read_bytes()
        assert raw.endswith(b'\r\n') and not raw.replace(b'\r\n',b'').count(b'\n')
        assert all(len(line)<=75 for line in raw.split(b'\r\n'))
        content=raw.decode().replace('\r\n ','')
        if event['kind']=='deadline':
            expected=datetime.fromisoformat(event['at']).astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            assert 'DTSTART:'+expected in content
        else:
            assert event['start'] < event['endExclusive']
            assert 'DTSTART;VALUE=DATE:'+event['start'].replace('-','') in content
            assert 'DTEND;VALUE=DATE:'+event['endExclusive'].replace('-','') in content
assert len(event_ids)==len(set(event_ids))
assert set(event_ids).issubset(pages['calendar.html'].ids), 'Calendar deep links incomplete'
combined=(OUT/'downloads/mmifusion-calendar.ics').read_text()
assert combined.count('BEGIN:VEVENT')==len(event_ids)
assert 'DTSTART:20261117T115900Z' in (OUT/'downloads/cvpr2027-paper.ics').read_text()
for category in ('teams','opportunities','venues','datasets'):
    records=portal[category]
    assert len({r['id'] for r in records})==len(records)
    for record in records:
        assert urlsplit(record['source']).scheme=='https'
for record in portal['opportunities']:
    assert record['teamId'] in {team['id'] for team in portal['teams']}
assert not errors, '\n'.join(errors)
print(f'PASS: {len(pages)} pages, {len(articles)} unique WeChat articles, all local links and anchors.')
print(f'PASS: {len(event_ids)} calendar events, UTC/all-day dates, resource identities and official source links.')
