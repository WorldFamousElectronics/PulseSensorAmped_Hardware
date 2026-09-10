from pathlib import Path
import sys,json,re,xml.etree.ElementTree as ET,hashlib
sys.path.insert(0,'/Users/PulsesensorCorp/.codex/tmp/pulsesensor-art-tools')
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parent;S=R.parent/'power-color-2026-09-09/color-10'
j=json.loads((S/'color-geometry.json').read_text())
def load(v):return unary_union([Polygon(p['outer'],p.get('holes',[])) for p in v])
def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
allowed=load(j[0]['polygons'])
regions={
 'FILTER':box(92,92,98.25,98.8),
 'AMP + GAIN':Polygon([(98.25,92),(108,92),(108,97.15),(103.75,97.15),(103.75,98.8),(98.25,98.8)]),
 'BIAS':box(103.75,97.15,108,101.15),
 'LED':box(92,98.8,103.75,101.15),
 'SENSE':box(92,101.15,98,108),
 'POWER':box(98,101.15,108,108)}
colors={'FILTER':'#146C78','AMP + GAIN':'#594785','BIAS':'#A43E6B','LED':'#A16822','SENSE':'#397A62','POWER':'#276B9C'}
root=ET.parse(S/'back-positioning.svg').getroot()
def frompath(e):
 g=Polygon()
 for ring in re.findall(r'M\s*(.*?)Z',e.get('d'),re.S):
  nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',ring)));p=Polygon(list(zip(nums[::2],nums[1::2])))
  if not p.is_valid:p=p.buffer(0)
  g=g.symmetric_difference(p)
 return g
layers=[('board','#f7f7f2',frompath(root[0])),('seams','#101519',allowed)]
for name,g in regions.items():layers.append((name,colors[name],g.intersection(allowed)))
# Dotted outlines on shared module boundaries; no puzzle tabs or solid seams.
shared=[]
values=list(regions.values())
for i,g in enumerate(values):
 for h in values[i+1:]:
  edge=g.boundary.intersection(h.boundary)
  if not edge.is_empty:shared.append(edge)
boundaries=unary_union(shared)
def lines(g):
 if g.geom_type=='LineString':return [g]
 return [l for child in getattr(g,'geoms',[]) for l in lines(child)]
dots=[]
for edge in lines(boundaries):
 steps=max(1,round(edge.length/.28))
 for n in range(steps+1):dots.append(edge.interpolate(edge.length*n/steps).buffer(.070,quad_segs=12))
layers.append(('dotted module boundaries','#000000',unary_union(dots).intersection(allowed)))
for item in j:
 if item['name'] in ['labels','+','-']:layers.append((item['name'],'#ffffff',unary_union([p for p in polys(load(item['polygons'])) if p.area>=.008])))
for e in root:
 if e.get('fill') in ['#bcb5a1','#535559','#f2f0df']:layers.append(('unchanged component',e.get('fill'),frompath(e)))
def path(g):
 return ' '.join('M '+' L '.join(f'{x:.6f},{y:.6f}' for x,y in ring.coords)+' Z' for p in polys(g) for ring in [p.exterior]+list(p.interiors))
svg='<svg xmlns="http://www.w3.org/2000/svg" width="15.875mm" height="15.875mm" viewBox="92.0625 92.0625 15.875 15.875">'+''.join(f'<path fill="{c}" fill-rule="evenodd" d="{path(g)}"/>' for n,c,g in layers)+'</svg>'
(R/'modules-02-back.svg').write_text(svg)
# Render new vector polygons, retaining native coordinates and unchanged component geometry.
def render(ls,size):
 im=Image.new('RGBA',(size,size));scale=size/15.875
 for n,c,g in ls:
  mask=Image.new('L',(size,size));d=ImageDraw.Draw(mask)
  for p in polys(g):
   xy=lambda ring:[((x-92.0625)*scale,(y-92.0625)*scale) for x,y in ring.coords]
   d.polygon(xy(p.exterior),fill=255)
   for hole in p.interiors:d.polygon(xy(hole),fill=0)
  im.alpha_composite(Image.composite(Image.new('RGBA',(size,size),c),Image.new('RGBA',(size,size)),mask))
 return im
render(layers,2400).save(R/'modules-02-back.png')
# Visual comparison; images are placed without changing their artwork.
preview=Image.new('RGB',(2600,1590),'#f2f1ed');d=ImageDraw.Draw(preview);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((65,40),'PulseSensor · Dotted module outline study',font=font(52),fill='#152b34');d.text((65,110),'Sheet 24 · Color identifies a functional area · All parts and optical geometry stay in place',font=font(29),fill='#53666d')
for i,(title,p) in enumerate([('PREVIOUS / PUZZLE-01',R.parent/'puzzle-modules-2026-09-10/puzzle-01-back.png'),('ITERATION / MODULES-02',R/'modules-02-back.png')]):
 x=65+i*1260;d.text((x,181),title,font=font(31),fill='#152b34');pic=ImageOps.contain(Image.open(p).convert('RGBA'),(1170,1170),Image.Resampling.LANCZOS);preview.paste(pic,(x,242),pic)
for i,(name,col) in enumerate(colors.items()):
 x=65+i*415;d.rounded_rectangle((x,1460,x+28,1488),5,fill=col);d.text((x+40,1457),name,font=font(27),fill='#152b34')
d.text((65,1525),'Functional grouping artwork, not copper-net coloring. Native CAD and the accepted back remain unchanged.',font=font(25),fill='#53666d');preview.save(R/'comparison.png')
(R/'design-notes.json').write_text(json.dumps({'classification':'DEVELOPMENT appearance study','source':str(S),'modules':colors,'boundary_dot_diameter_mm':.14,'boundary_dot_pitch_mm':.28,'preserved':'Exact native component bodies, pad artwork, white labels, + / - marks. No CAD edits.','meaning':'Color is functional group, not voltage or net. SENSE includes input coupling C2.','removed':'Puzzle tabs and solid seams. Dots now mark module boundaries, not signal paths.','print_status':'Visual study; supplier separations and print review not yet prepared.'},indent=2))
print('Created straight module regions with black dotted outlines.')
