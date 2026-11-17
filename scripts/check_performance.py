#!/usr/bin/env python3
"""Check optimized assets and search metadata against their original sources."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import performance

ROOT = Path(__file__).resolve().parents[1]
articles = {a['id']: a for a in json.loads((ROOT/'data/articles.json').read_text())['articles']}

class Page(HTMLParser):
    def handle_starttag(self,tag,attributes):
        attrs = dict(attributes)
        if 'data-article-id' in attrs:
            article = articles[attrs['data-article-id']]
            assert json.loads(attrs['data-article-topics']) == article['topics']
            assert attrs['data-article-venue'] == article['venue']
        if tag == 'img' and attrs.get('src','').startswith('assets/qr/'):
            assert attrs.get('loading') == 'lazy'
        if tag == 'img': assert attrs.get('src') != 'assets/avatar.png'
        assert 'data-visit-hint' not in attrs

for page in (ROOT/'dist').glob('*.html'):
    source = page.read_text();Page().feed(source)
    assert 'assets/site.css?v=' in source and 'assets/site.js?v=' in source

for original,preview in json.loads((ROOT/'data/image-previews.json').read_text()).items():
    assert hashlib.sha256((ROOT/original).read_bytes()).hexdigest() == preview['sha256']
    data = (ROOT/preview['src']).read_bytes()
    assert data[:4] == b'RIFF' and data[8:12] == b'WEBP'
    assert hashlib.sha256(data).hexdigest().startswith(Path(preview['src']).stem)
    assert 0 < preview['width'] <= 960 and 0 < preview['height'] <= 640

for names,target in [(performance.CSS,'site.css'),(performance.JS,'site.js')]:
    bundle = (ROOT/'assets'/target).read_text()
    offsets = [bundle.index('/* Source: '+name+' */') for name in names]
    assert offsets == sorted(offsets)
    assert all((ROOT/'assets'/name).read_text() in bundle for name in names)
    assert (ROOT/'dist/assets'/target).read_text() == bundle
print('PASS: original image hashes, immutable WebP previews, lazy QR images, complete inline search metadata and exact shared bundles.')
