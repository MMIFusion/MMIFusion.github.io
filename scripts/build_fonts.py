#!/usr/bin/env python3
"""Optional font refresh: pip install 'fonttools[woff]'; python scripts/build_fonts.py.
Fonts are fetched from the original Google Fonts repository, cached under ignored
outputs/, subset to site content, and served locally with their OFL licenses.
This is separate from the dependency-free normal website build.
"""
from pathlib import Path
import urllib.request
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'outputs/font-sources'
TARGET=ROOT/'assets/fonts'
FONT_SOURCES=[
    ('NotoSansSC','notosanssc','mmifusion-sans.woff2'),
    ('SpaceGrotesk','spacegrotesk','space-grotesk.woff2'),
]

def main():
    CACHE.mkdir(parents=True,exist_ok=True); TARGET.mkdir(parents=True,exist_ok=True)
    text=''.join(p.read_text() for name in ['scripts','assets','data'] for p in (ROOT/name).rglob('*') if p.suffix in ('.py','.js','.css','.json'))
    latin=''.join(chr(i) for i in range(32,128))+''.join(chr(i) for i in range(0xa0,0x180))+'→↗×−·'
    for family,folder,output in FONT_SOURCES:
        base=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{folder}/'
        source=CACHE/(family+'.ttf')
        if not source.exists():
            with urllib.request.urlopen(base+family+'%5Bwght%5D.ttf',timeout=60) as response:source.write_bytes(response.read())
        license_file=TARGET/(family+'-OFL.txt')
        if not license_file.exists():
            with urllib.request.urlopen(base+'OFL.txt',timeout=30) as response:license_file.write_bytes(response.read())
        font=TTFont(source)
        options=subset.Options();options.flavor='woff2';options.layout_features=['*']
        options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
        builder=subset.Subsetter(options=options);builder.populate(text=text+latin if family=='NotoSansSC' else latin);builder.subset(font)
        font.flavor='woff2';font.save(TARGET/output)
        print(output,(TARGET/output).stat().st_size,'bytes')

if __name__=='__main__':main()
