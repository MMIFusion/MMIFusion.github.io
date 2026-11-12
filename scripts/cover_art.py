"""Original editorial cover art. Decorative graphics, not paper figures or results."""
import html
import math
import re

# Keep one visual identity for an article when it appears in several reading tabs.
COVERS = {
    'bb15984a3a4b': ('connections', 'teal', 'THCMC', 'CONTRASTIVE LEARNING'),
    '9047bd7761e6': ('layers', 'lilac', 'ME-PMA', 'MULTI-SCALE ALIGNMENT'),
    '49a25a11adfb': ('geometry', 'violet', 'Hy-CycleAlign', 'HYPERBOLIC GEOMETRY'),
    'f2da1bf49bab': ('points', 'blue', 'MGAF', 'MULTIMODAL PERCEPTION'),
    '3f0517385784': ('thermal', 'copper', 'Thermal3D-GS', 'THERMAL RECONSTRUCTION'),
    '8717e19cbb41': ('roads', 'sky', 'CausalDrive', 'CAUSAL WORLD MODEL'),
    '892ff5d355df': ('patches', 'sage', 'DA-IVIF', 'REAL-WORLD DEGRADATION'),
    'cd7dc0320b57': ('light', 'rose', 'UAVLight', 'MULTI-LIGHT RECONSTRUCTION'),
}
STYLES = [('connections','teal'),('layers','lilac'),('geometry','violet'),('points','blue'),
          ('thermal','copper'),('roads','sky'),('patches','sage'),('light','rose')]
E = lambda value: html.escape(str(value), quote=True)

def profile(article):
    if article['id'] in COVERS: return COVERS[article['id']]
    seed = int(article['id'], 16)
    motif, palette = STYLES[seed % len(STYLES)]
    words = re.findall(r'[A-Za-z][A-Za-z0-9]*(?:[-–][A-Za-z0-9]+)*',article['title'])
    excluded={'INFFUS','TPAMI','TIP','TMM','IJCV','CVPR','ICCV','ECCV','NeurIPS','ICLR','ICML','AAAI','ACM','MM','Information','Fusion'}
    method = next((w for w in words if w not in excluded and 3<=len(w)<=18),'MMIFUSION')
    return motif,palette,method,'RESEARCH / '+article['date'][:4]

def artwork(motif, seed):
    parts=[]
    if motif=='connections':
        points=[(74,65),(104,43),(132,75),(74,116),(116,139),(158,106),(202,56),(235,88),(205,133)]
        edges=[(0,1),(0,2),(0,3),(1,2),(2,3),(2,4),(2,5),(3,4),(4,5),(5,6),(5,7),(5,8),(6,7),(7,8),(6,8)]
        parts.append('<g class="art-links" stroke="var(--art-line)" stroke-width="1.2" fill="none">')
        for a,b in edges:
            x,y=points[a];u,v=points[b];parts.append(f'<path d="M{x} {y} Q{(x+u)/2} {min(y,v)-16} {u} {v}"/>')
        parts.append('</g><g class="art-float">')
        for i,(x,y) in enumerate(points):
            parts.append(f'<circle cx="{x}" cy="{y}" r="{10 if i==5 else 6}" fill="var(--art-accent)" opacity="{.55+(i%3)*.2}"/><circle cx="{x}" cy="{y}" r="{17 if i==5 else 11}" fill="none" stroke="var(--art-line)" opacity=".5"/>')
        parts.append('</g>')
    elif motif=='layers':
        for i,(x,y) in enumerate([(98,96),(112,76),(126,56)]):
            parts.append(f'<g class="art-layer" style="--layer:{i}"><path d="M{x} {y} l72 -28 64 31 -72 30Z" fill="var(--art-accent)" fill-opacity="{.10+i*.08}" stroke="var(--art-line)"/><path d="M{x} {y} v23 l64 31 72 -30V{y+3}" fill="none" stroke="var(--art-line)" opacity=".45"/>')
            for j in range(1,4):parts.append(f'<path d="M{x+16*j} {y-7*j} l64 31 M{x+18*j} {y+8.5*j} l72 -28" stroke="var(--art-line)" stroke-width=".65" opacity=".45"/>')
            parts.append('</g>')
        parts.append('<path class="art-trace" d="M85 144 L155 173 238 137" fill="none" stroke="var(--art-second)" stroke-width="2" stroke-dasharray="4 5"/>')
    elif motif=='geometry':
        parts.append('<g fill="none" stroke="var(--art-line)"><circle cx="166" cy="100" r="78" stroke-width="1.5"/>')
        for j in range(7):
            a=j*math.pi/3.5
            x,y=166+78*math.cos(a),100+78*math.sin(a)
            u,v=166+78*math.cos(a+1.55),100+78*math.sin(a+1.55)
            parts.append(f'<path d="M{x:.1f} {y:.1f} Q166 100 {u:.1f} {v:.1f}" opacity=".55"/>')
        parts.append('<path class="art-trace" d="M93 73 Q166 100 229 146 M107 150 Q166 100 197 28" stroke="var(--art-second)" stroke-width="2" stroke-dasharray="5 7"/></g><circle class="art-pulse" cx="166" cy="100" r="8" fill="var(--art-accent)"/>')
    elif motif=='points':
        parts.append('<g stroke="var(--art-line)" stroke-width=".8" fill="none" opacity=".4"><path d="M48 151 154 185 260 134M65 130 166 161 247 120M84 111 177 139 235 106M103 91 189 118 221 95M108 97 77 163M143 108 116 177M181 120 158 184M216 130 201 165"/></g>')
        for j in range(64):
            x=65+(j*37+seed%13)%175;y=55+(j*23+seed%19)%105
            parts.append(f'<circle cx="{x}" cy="{y}" r="{1.2+(j%3)*.5}" fill="var(--art-accent)" opacity="{.25+(j%4)*.18}"/>')
        parts.append('<g class="art-float" fill="var(--art-accent)" fill-opacity=".09" stroke="var(--art-line)" stroke-width="1.4"><path d="M110 81 161 64 202 85 153 104Z M110 81v55l43 23 49-19V85 M153 104v55"/></g><path class="art-trace" d="M77 160 237 111" fill="none" stroke="var(--art-second)" stroke-width="2" stroke-dasharray="5 8"/>')
    elif motif=='thermal':
        for j in range(8):
            inset=j*7
            parts.append(f'<ellipse cx="{164+j*2}" cy="100" rx="{85-inset}" ry="{66-inset*.68}" transform="rotate(-27 164 100)" fill="var(--art-accent)" fill-opacity=".025" stroke="var(--art-line)" stroke-opacity="{.25+j*.08}"/>')
        parts.append('<path d="M83 150 142 174 241 127 M142 174v-45" fill="none" stroke="var(--art-second)" opacity=".7"/><circle class="art-pulse" cx="178" cy="91" r="14" fill="var(--art-second)"/><circle cx="178" cy="91" r="29" fill="none" stroke="var(--art-second)" opacity=".6"/>')
    elif motif=='roads':
        parts.append('<g stroke="var(--art-line)" fill="none"><path d="M65 177 160 47 258 177 M104 177 160 47 219 177" stroke-width="1.3"/><path class="art-trace" d="M162 177V51" stroke-width="2" stroke-dasharray="9 8"/>')
        for y in [83,105,133,167]:parts.append(f'<path d="M{160-(y-47)*.73:.1f} {y} H{160+(y-47)*.75:.1f}" opacity=".4"/>')
        parts.append('</g><g class="art-float" fill="var(--art-accent)" fill-opacity=".16" stroke="var(--art-line)"><path d="M110 113v-23l24-13 23 10v24l-24 15Z M110 90l23 11 24-14 M133 101v25"/><path d="M190 141v-32l23-12 20 12v32l-21 14Z M190 109l22 12 21-12 M212 121v34"/></g><circle cx="161" cy="46" r="7" fill="var(--art-second)"/>')
    elif motif=='patches':
        for j in range(9):
            x=91+(j%3)*51;y=40+(j//3)*48
            parts.append(f'<g class="art-tile" style="--layer:{j%3}"><rect x="{x}" y="{y}" width="43" height="39" rx="6" fill="var(--art-accent)" fill-opacity="{.06+(j%4)*.07}" stroke="var(--art-line)"/>')
            if j%3==0:
                parts.append(f'<path d="M{x+7} {y+30} l9-12 7 8 9-17" fill="none" stroke="var(--art-second)" stroke-width="2"/>')
            elif j%3==1:
                for k in range(3):parts.append(f'<path d="M{x+9} {y+10+k*9}h25" stroke="var(--art-line)" stroke-dasharray="3 3"/>')
            else:parts.append(f'<circle cx="{x+22}" cy="{y+19}" r="10" fill="none" stroke="var(--art-second)"/><circle cx="{x+22}" cy="{y+19}" r="3" fill="var(--art-second)"/>')
            parts.append('</g>')
    else:
        parts.append('<g fill="none" stroke="var(--art-line)"><path d="M76 145 158 180 247 135 167 105Z M76 145V97l91-43 80 35v46 M167 54v51" opacity=".6"/><ellipse cx="169" cy="106" rx="87" ry="36" transform="rotate(-28 169 106)" stroke-dasharray="3 6"/></g>')
        for j,(x,y) in enumerate([(113,71),(223,77),(153,156)]):
            parts.append(f'<g class="art-light" style="--layer:{j}"><circle cx="{x}" cy="{y}" r="21" fill="var(--art-accent)" opacity=".10"/><circle cx="{x}" cy="{y}" r="9" fill="var(--art-second)"/><path d="M{x-29} {y}h9 M{x+20} {y}h9 M{x} {y-29}v9 M{x} {y+20}v9" stroke="var(--art-line)"/></g>')
    return f'<svg class="cover-art art-{motif}" viewBox="0 0 280 210" fill="none" aria-hidden="true" focusable="false">{"".join(parts)}</svg>'

def cover(article, index, record=None, context='reading'):
    motif,palette,method,caption=profile(article)
    seed=int(article['id'],16)
    art=artwork(motif,seed)
    metrics=''
    description=''
    if record:
        date=record['snapshotDate'].replace('-','.')
        cells=''.join(f'<span><strong>{record[key]:,}</strong><small>{label}</small></span>' if record.get(key) is not None else f'<span><strong>—</strong><small>{label}</small></span>' for key,label in [('reads','阅读'),('likes','点赞'),('shares','转发')])
        stat_id=f'cover-stats-{context}-{article["id"]}'
        description=f'aria-describedby="{stat_id}"'
        metrics=f'<div class="cover-engagement" id="{stat_id}"><div class="cover-counts">{cells}</div><span class="cover-stat-date">公众号统计 · {date}</span></div>'
    return f'''<a class="reading-cover editorial-cover palette-{palette}" data-cover-art="{motif}" data-cover-article="{article['id']}" href="{E(article['url'])}" target="_blank" rel="noopener noreferrer" aria-label="阅读：{E(article['title'])}" {description}><span class="cover-top">MMIFUSION / READING NOTES <span>0{index+1}</span></span><span class="cover-identity"><strong>{E(method)}</strong><small>{E(caption)}</small></span>{art}<span class="cover-topic">{E(article['topics'][0] if article['topics'] else '研究阅读')} <b>↗</b></span>{metrics}</a>'''
