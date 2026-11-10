#!/usr/bin/env python3
"""MMIFusion EN/SD/SF demo. Install: pip install pillow numpy
Usage: python fusion_metrics.py image.png [image2.png ...]
Uses 8-bit grayscale, population SD and valid-neighbour SF; no resizing.
Original implementation (MIT). Reference toolbox:
https://github.com/Linfeng-Tang/Evaluation-for-Image-Fusion
"""
import csv
import sys
import numpy as np
from PIL import Image, ImageOps

def evaluate(path):
    image=ImageOps.exif_transpose(Image.open(path)).convert('RGBA')
    rgba=np.asarray(image,dtype=np.float64)
    alpha=rgba[:,:,3:4]/255
    rgb=rgba[:,:,:3]*alpha+255*(1-alpha)
    gray=np.floor(rgb@np.array([.299,.587,.114])+.5).clip(0,255).astype(np.uint8)
    counts=np.bincount(gray.ravel(),minlength=256)
    p=counts[counts>0]/gray.size
    en=float(-np.sum(p*np.log2(p)))
    values=gray.astype(np.float64)
    sd=float(np.std(values,ddof=0))
    dx=np.diff(values,axis=1); dy=np.diff(values,axis=0)
    sf=float(np.sqrt((np.mean(dx*dx) if dx.size else 0)+(np.mean(dy*dy) if dy.size else 0)))
    return [str(path),image.width,image.height,en,sd,sf]

if __name__=='__main__':
    if len(sys.argv)<2: raise SystemExit(__doc__)
    writer=csv.writer(sys.stdout); writer.writerow(['file','width','height','EN','SD','SF'])
    for filename in sys.argv[1:]: writer.writerow(evaluate(filename))
