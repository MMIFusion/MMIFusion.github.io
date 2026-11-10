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
assert not errors, '\n'.join(errors)
print(f'PASS: {len(pages)} pages, {len(articles)} unique WeChat articles, all local links and anchors.')
