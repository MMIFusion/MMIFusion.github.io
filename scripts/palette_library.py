"""Original MMIFusion palettes and deterministic downloadable library.

Run --initialize once to expand the curated seeds; normal builds only read data.
Colors are sRGB HEX, not claimed to be official named-color standards.
"""
import colorsys
import csv
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = [
    ('red','红色',5,.64), ('orange','橙色',27,.72),
    ('amber','琥珀',39,.74), ('yellow','黄色',50,.72),
    ('lime','黄绿',78,.55), ('green','绿色',138,.45),
    ('mint','薄荷',158,.43), ('teal','青绿',174,.48),
    ('cyan','青色',188,.55), ('sky','天蓝',201,.64),
    ('blue','蓝色',214,.59), ('indigo','靛蓝',238,.51),
    ('periwinkle','蓝紫',253,.51), ('purple','紫色',276,.45),
    ('magenta','洋红',309,.50), ('pink','粉色',336,.58),
    ('rose','玫瑰',350,.55), ('brown','棕色',29,.35),
    ('sand','沙色',43,.30), ('warm-gray','暖灰',30,.09),
    ('cool-gray','冷灰',215,.10), ('gray','中性灰',220,0),
]
BASIC_STYLES = [
    ('classic','经典',0,1,[.95,.81,.64,.45,.27]),
    ('mist','柔雾',-5,.58,[.965,.87,.75,.60,.42]),
    ('vivid','明亮',4,1.28,[.95,.83,.65,.47,.30]),
    ('vintage','复古',-9,.72,[.925,.78,.61,.43,.255]),
    ('deep','深邃',7,.90,[.90,.74,.56,.365,.19]),
    ('muted','灰调',2,.28,[.94,.82,.68,.51,.33]),
]
MEETING_STYLES = ['冷暖对照','柔和分组','重点强调','多组对比','模块流程','深色演示']
BASIC_USAGE = {
    '经典':(['量级热图','区域标注'],'按浅至深表达递增量级；浅色铺底，中间色填充，深色用于轮廓和重点。'),
    '柔雾':(['模块示意','浅色背景'],'适合大面积模块填充；浅色块之间增加留白或深色边框，避免投影时边界消失。'),
    '明亮':(['重点标注','结果强调'],'选择中间色突出关键结果；高纯度颜色控制面积，图中正文优先使用深色。'),
    '复古':(['学术海报','组会封面'],'适合低饱和的海报与章节页；用最浅色作底，最深色建立标题层级。'),
    '深邃':(['强调层级','区域标注'],'深色适合重点块、标题或细线；大面积深色填充时参考各色位的建议字色。'),
    '灰调':(['辅助信息','消融实验'],'适合背景方法、辅助区域与消融层级；关键方法可另外使用一组强调色。'),
}
MEETING_USAGE = {
    '冷暖对照':(['方法对比','双模态示意'],['冷端深色','冷端主色','过渡浅色','暖端浅色','暖端强调'],'前三色组织一侧信息，后两色组织另一侧；例如可见光与红外、基线与改进。','浅色背景'),
    '柔和分组':(['模块示意','组会封面'],['主模块','次模块','留白底色','辅助模块','强调模块'],'适合框架图的大色块与章节页；用深色描边或编号补充分组。','浅色背景'),
    '重点强调':(['结果强调','消融实验'],['正文辅助','基线方法','背景区域','次要结果','核心结果'],'前三色弱化背景信息，后两色突出结果；将核心方法固定使用最后一色。','浅色背景'),
    '多组对比':(['方法对比','多组实验'],['方法一','方法二','方法三','方法四','方法五'],'五种颜色用于不同方法或实验组；曲线配合线型、标记和图例，不依赖颜色单独区分。','浅色背景'),
    '模块流程':(['模块示意','双模态示意'],['输入分支','特征提取','融合模块','任务模块','输出结果'],'按流程给模块分配固定颜色；同类模块保持同色，箭头和文字使用统一深色。','浅色背景'),
    '深色演示':(['深色幻灯','组会封面'],['主曲线','辅助曲线','参考曲线','次要强调','核心强调'],'建议搭配 #111827 深色画布；这些颜色用于图形与强调，正文使用白色或浅灰。','深色背景'),
}

def hex_color(h,s,l):
    rgb=colorsys.hls_to_rgb((h%360)/360,l,max(0,min(.9,s)))
    return '#'+''.join(f'{round(v*255):02X}' for v in rgb)

def luminance(color):
    rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722)))

def color_detail(color,role):
    y=luminance(color)
    # Black and white are compared mathematically; this is not a color-vision guarantee.
    ink='#000000' if (y+.05)/.05 >= 1.05/(y+.05) else '#FFFFFF'
    contrast=(y+.05)/.05 if ink=='#000000' else 1.05/(y+.05)
    return {'hex':color,'rgb':[int(color[i:i+2],16) for i in (1,3,5)],'role':role,'textColor':ink,'textContrast':round(contrast,2)}

def meeting_colors(h,s,style):
    sat=max(.28,min(.60,s))
    params={
      '冷暖对照':[(h,.36,.24),(h,sat,.48),(h,.30,.78),(h+175,.42,.75),(h+175,.54,.48)],
      '柔和分组':[(h-28,.32,.43),(h,.28,.63),(h+25,.30,.82),(h+145,.36,.77),(h+175,.36,.52)],
      '重点强调':[(h,.06,.28),(h,.07,.50),(h,.08,.78),(h+7,sat,.62),(h+7,min(.78,sat+.16),.42)],
      '多组对比':[(h,.56,.42),(h+65,.50,.50),(h+135,.45,.38),(h+210,.50,.55),(h+280,.56,.46)],
      '模块流程':[(h,.50,.30),(h,.40,.55),(h+70,.40,.75),(h+150,.42,.65),(h+205,.48,.40)],
      '深色演示':[(h,.60,.70),(h+52,.52,.74),(h+125,.45,.68),(h+195,.57,.77),(h+275,.62,.72)],
    }
    chroma_factor=.35+min(.8,s*1.2)
    return [hex_color(hue,saturation*chroma_factor,lightness) for hue,saturation,lightness in params[style]]

def initialize():
    path=ROOT/'data/community.json';data=json.loads(path.read_text())
    if data.get('paletteLibrary'):
        raise SystemExit('Library already initialized. Edit community.json directly; existing customizations are preserved.')
    seeds={v['id']:v for v in data['basicPalettes']}
    basics=[]
    # Start with the full color wheel; a family filter then reveals its six styles.
    for style_id,style,shift,scale,levels in BASIC_STYLES:
        for key,name,h,s in FAMILIES:
            record=dict(seeds[key]) if style_id=='classic' and key in seeds else {
                'id':key if style_id=='classic' else key+'-'+style_id,
                'name':name+' · '+style,
                'note':'浅 → 深 · '+style+'渐阶',
                'colors':[hex_color(h+shift,s*scale,l) for l in levels],
            }
            uses,tips=BASIC_USAGE[style]
            record.update(family=name,style=style,uses=uses,tips=tips,background='浅色背景',roles=['极浅底色','浅色填充','中间主色','深色强调','极深轮廓'])
            basics.append(record)
    legacy=[('blue','冷暖对照'),('green','冷暖对照'),('purple','柔和分组'),('cyan','冷暖对照')]
    combos=[]
    for record,(family,style) in zip(data['palettes'],legacy):
        record=dict(record);name=next(f[1] for f in FAMILIES if f[0]==family)
        uses,roles,tips,bg=MEETING_USAGE[style]
        record.update(id=f'{family}-{MEETING_STYLES.index(style)+1}',family=name,style=style,uses=uses,roles=roles,tips=tips,background=bg)
        combos.append(record)
    for style in MEETING_STYLES:
        for key,name,h,s in FAMILIES:
            if (key,style) in legacy:continue
            # Earth/gray families use related colored accents, while retaining their own anchor.
            anchor=h if key!='gray' else 228
            uses,roles,tips,bg=MEETING_USAGE[style]
            combos.append(dict(id=f'{key}-{MEETING_STYLES.index(style)+1}',name=name+' · '+style,note=' · '.join(uses),colors=meeting_colors(anchor,s,style),family=name,style=style,uses=uses,roles=roles,tips=tips,background=bg))
    assert len(basics)==len(combos)==132
    for rows in (basics,combos):
        assert len({tuple(v['colors']) for v in rows})==len(rows), 'Duplicate complete palette'
        assert all(len(set(v['colors']))==5 for v in rows)
    for v in basics:
        assert all(luminance(x)>luminance(y) for x,y in zip(v['colors'],v['colors'][1:])),v['id']
    data['basicPalettes']=basics;data['palettes']=combos
    data['paletteLibrary']={'version':1,'updatedAt':'2026-11-12','families':[f[1] for f in FAMILIES],'basicStyles':[s[1] for s in BASIC_STYLES],'meetingStyles':MEETING_STYLES,'creator':'多模态信息融合','license':'CC BY 4.0','note':'本站原创搭配与既有配色扩展；覆盖常用色相和中性色，不是论文取色或命名颜色标准。'}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Initialized 132 basic + 132 meeting palettes')

def write_archives(target,entries):
    groups={'basic':[],'meeting':[]}
    for stem,record in entries:
        kind='basic' if stem.startswith('palette-basic-') else 'meeting'
        details=[color_detail(c,role) for c,role in zip(record['colors'],record['roles'])]
        groups[kind].append(dict(record,download=stem,type=kind,colorDetails=details))
    catalog=dict(creator='多模态信息融合',license='CC BY 4.0',basic=groups['basic'],meeting=groups['meeting'])
    (target/'palettes-all.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    csvfile=io.StringIO(newline='');writer=csv.writer(csvfile)
    writer.writerow(['类型','名称','色系','风格','用途','色位','HEX','R','G','B','建议字色','字色对比度'])
    for kind,rows in groups.items():
        for p in rows:
            for c in p['colorDetails']:writer.writerow(['基础色系' if kind=='basic' else '组会配色',p['name'],p['family'],p['style'],'、'.join(p['uses']),c['role'],c['hex'],*c['rgb'],c['textColor'],c['textContrast']])
    (target/'palettes-all.csv').write_bytes(csvfile.getvalue().encode('utf-8-sig'))
    instructions=(f"MMIFusion 配色库 / CC BY 4.0\n\n{len(groups['basic'])} 组基础色系，{len(groups['meeting'])} 组组会配色"+'，每组 5 色。\n基础色系从浅到深；组会配色用于类别与模块区分，不代表数值大小。\n单卡 JSON 含使用建议、RGB 和建议字色；SVG 可直接编辑。\nCSV 可在 Excel 中打开；整体 JSON 便于 Python、Matplotlib 与网页复用。\n浅色在白底上宜用于填充，细线请优先选深色；曲线配合线型和标记。\n本站原创搭配，不是论文取色，也未声明全部色板满足色觉障碍可分辨性。\n来源：https://mmifusion.github.io/palettes.html\n').encode()
    for label,kinds in [('basic',['basic']),('meeting',['meeting']),('all',['basic','meeting'])]:
        payload={'README.txt':instructions}
        for kind in kinds:
            for row in groups[kind]:
                for ext in ['svg','json']:
                    name=row['download']+'.'+ext;payload[kind+'/'+name]=(target/name).read_bytes()
        if label=='all':
            for name in ['palettes-all.json','palettes-all.csv']:payload[name]=(target/name).read_bytes()
        with zipfile.ZipFile(target/f'palettes-{label}.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
            for name,body in sorted(payload.items()):
                info=zipfile.ZipInfo(name,date_time=(2026,11,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,body)

if __name__=='__main__':
    import sys
    if '--initialize' in sys.argv:initialize()
