#!/usr/bin/env python3
"""Import the existing Datasets catalogue without changing its scholarly content."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='The existing Datasets/docs directory')
    parser.add_argument('--check', action='store_true', help='Compare the imported copy without writing')
    args = parser.parse_args()
    source = args.source.resolve()
    raw = (source/'data/datasets.json').read_bytes()
    items = json.loads(raw)
    ids = [d['id'] for d in items]
    assert len(ids) == len(set(ids)) and all(re.fullmatch(r'[a-z0-9-]+', i) for i in ids)
    copies = {}
    for item in items:
        for image in item['images']:
            original = (source/image['src']).resolve()
            assert original.is_file() and original.is_relative_to(source/'assets/images')
            target = 'assets/dataset-catalog/'+original.name
            assert target not in copies or copies[target] == original
            copies[target] = original
            image['src'] = target
    manifest = {'sourceRepository':'https://github.com/MMIFusion/Datasets',
        'sourceFile':'docs/data/datasets.json',
        'sourceCommit':subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip(),
        'sourceSha256':hashlib.sha256(raw).hexdigest(), 'count':len(items),
        'images':{target:hashlib.sha256(path.read_bytes()).hexdigest() for target,path in sorted(copies.items())}}
    if args.check:
        assert json.loads((ROOT/'data/datasets.json').read_text()) == items, 'Catalogue content differs'
        imported = json.loads((ROOT/'data/datasets-provenance.json').read_text())
        # The source repository may gain a redirect or documentation commit after
        # migration. Compare content while retaining the original import commit.
        assert {k:v for k,v in imported.items() if k != 'sourceCommit'} == {
            k:v for k,v in manifest.items() if k != 'sourceCommit'}
        for target, original in copies.items():
            assert (ROOT/target).read_bytes() == original.read_bytes(), target
        print(f'PASS: {len(items)} complete records and {len(copies)} byte-identical original images.')
        return
    for target, original in copies.items():
        (ROOT/target).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(original,ROOT/target)
    for name,data in [('datasets.json',items),('datasets-provenance.json',manifest)]:
        (ROOT/'data'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    shutil.copy2(source.parent/'LICENSE',ROOT/'docs/DATASETS-LICENSE.txt')
    print(f'Imported {len(items)} records and {len(copies)} original images; content and attribution preserved.')

if __name__ == '__main__':
    main()
