#!/usr/bin/env python3
"""Optional maintenance step: derive display assets without modifying originals.

Requires Pillow. Normal builds and CI use the checked-in derivatives/manifest.
Dataset detail images and QR codes always retain their original bytes.
"""
import hashlib
import io
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'assets/previews'

def main():
    DEST.mkdir(exist_ok=True)
    sources = {image['src'] for item in json.loads((ROOT/'data/datasets.json').read_text()) for image in item['images'][:1]}
    sources.update(str(p.relative_to(ROOT)) for p in (ROOT/'assets/datasets').glob('*') if p.suffix.lower() in ('.png','.jpg','.jpeg'))
    sources.add('assets/avatar.png')
    manifest = {}
    for source in sorted(sources):
        path = ROOT/source
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        avatar = source == 'assets/avatar.png'
        image = ImageOps.exif_transpose(Image.open(path)).convert('RGBA')
        image.thumbnail((200,200) if avatar else (960,640),Image.Resampling.LANCZOS)
        encoded = io.BytesIO()
        image.save(encoded,format='WEBP',lossless=avatar,quality=86,method=6)
        target = DEST/(hashlib.sha256(encoded.getvalue()).hexdigest()[:16]+'.webp')
        target.write_bytes(encoded.getvalue())
        manifest[source] = {'src':str(target.relative_to(ROOT)),'width':image.width,'height':image.height,'sha256':digest}
        if avatar:
            icon = image.copy();icon.thumbnail((64,64),Image.Resampling.LANCZOS)
            icon.save(ROOT/'assets/favicon.png',optimize=True)
            apple = image.copy();apple.thumbnail((180,180),Image.Resampling.LANCZOS)
            apple.save(ROOT/'assets/apple-touch-icon.png',optimize=True)
    (ROOT/'data/image-previews.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    before = sum((ROOT/p).stat().st_size for p in manifest)
    after = sum((ROOT/p['src']).stat().st_size for p in manifest.values())
    print(f'{len(manifest)} previews: {before:,} -> {after:,} bytes; all original files unchanged.')

if __name__ == '__main__':
    main()
