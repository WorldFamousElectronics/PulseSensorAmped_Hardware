from pathlib import Path
import sys,math,json,shutil,uuid
sys.path.insert(0,'/Users/PulsesensorCorp/.codex/tmp/pulsesensor-art-tools')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'sendoff-candidate-2026-09-09'))
from native_sexpr import parse,children,apply
from shapely.geometry import Polygon,Point,LineString,box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from PIL import Image,ImageDraw
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
R=Path(__file__).resolve().parent;src=R/'mono-06';out=R/'color-07';out.mkdir(exist_ok=True)
for p in src.iterdir():
 if p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym'] or p.name in ['fp-lib-table','sym-lib-table']:shutil.copy2(p,out/p.name)
for n in ['3dmodels','PulseSensor_Amped.pretty']:
 if not (out/n).exists():shutil.copytree(src/n,out/n)
s=(src/'PulseSensor-JST-Educational.kicad_pcb').read_text();root=parse(s)
def val(n,k):return children(n,k)[0]['items'][1:]
def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def load(items):return unary_union([Polygon(p['outer'],p.get('holes',[])).buffer(0) for p in items])
def serial(g):return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in polys(g)]
qa=json.loads((src/'qa-geometry.json').read_text());ink=unary_union([load(o['polygons']) for o in qa['silk']['F']]);openings=unary_union([load(o['polygons']) for o in qa['openings']['F']]);board=Point(100,100).buffer(7.9375,quad_segs=256)
# Entire color-printed F side uses white mask plus a printed dark background.
allowed=board.buffer(-.20).difference(openings.buffer(.16))
clear=allowed.difference(ink.buffer(.12))
colors={'/VDD_IN':'#ff6569','/VDD_PROTECTED':'#ffbe55','/GND':'#4bd1dd','/LED_K':'#ffbe55'}
traces=[];chunks={};evidence=[]
for n in children(root,'segment'):
 net=val(n,'net')[0];layer=val(n,'layer')[0]
 if net not in colors:continue
 a=list(map(float,val(n,'start')));b=list(map(float,val(n,'end')));line=LineString([a,b]);width=.18
 evidence.append({'net':net,'layer':layer,'start':a,'end':b,'original_width_mm':float(val(n,'width')[0])})
 if layer=='B.Cu':
  seg=[];d=0
  while d<line.length:
   z=min(d+.30,line.length)
   if z>d:seg.append(LineString([line.interpolate(d),line.interpolate(z)]).buffer(width/2,quad_segs=4))
   d+=.50
  geom=unary_union(seg)
 else:geom=line.buffer(width/2,quad_segs=4)
 key=(net,layer);chunks.setdefault(key,[]).append(geom)
# Ground is a copper plane, not a single wire. Show the true F-plane region in muted blue.
planes=[]
for z in children(root,'zone'):
 if val(z,'net')[0]!='/GND' or val(z,'layer')[0]!='F.Cu':continue
 for fp in children(z,'filled_polygon'):
  pts=children(fp,'pts')[0];p=Polygon([list(map(float,x['items'][1:])) for x in children(pts,'xy')]).buffer(0);planes.append(p)
plane=unary_union(planes).intersection(allowed).buffer(-.08).buffer(.08).intersection(allowed)
# Printed guide segments are kept separate from the actual supply net overlays.
layers=[('background','#101519',allowed),('ground-plane','#153e48',plane)]
for (net,side),items in sorted(chunks.items(),key=lambda k:0 if k[0][1]=='B.Cu' else 1):
 shape=unary_union(items).intersection(clear)
 # Keep small but drawable runs, removing orphan slivers below 0.015 mm².
 shape=unary_union([p for p in polys(shape) if p.area>=.015]);layers.append((net+' '+side,colors[net],shape))
# Dotted logical signal guide gets its own color; native component markings remain white.
guide=unary_union([LineString([list(map(float,val(n,'start'))),list(map(float,val(n,'end')))]).buffer(float(val(n,'stroke')[0]['items'][1]['items'][1])/2) for n in []]) if False else Polygon()
for n in children(root,'gr_line'):
 if val(n,'layer')[0]=='F.SilkS':
  stroke=children(n,'stroke')[0];w=float(val(stroke,'width')[0]);guide=guide.union(LineString([list(map(float,val(n,'start'))),list(map(float,val(n,'end')))]).buffer(w/2,quad_segs=8))
changes=json.loads((src/'artwork-change.json').read_text());marks=unary_union([load(m['polygons']) for m in changes['polarity_marks']])
layers += [('signal-guide','#c4a1ff',guide.intersection(allowed)),('labels','#ffffff',ink.difference(guide.buffer(.0005)).difference(marks))]
for m in changes['polarity_marks']:layers.append((m['symbol'], '#ff6569' if m['symbol']=='+' else '#4bd1dd',load(m['polygons'])))
# Colored solder-land surrounds identify power nets without putting ink on metal.
for f in children(root,'footprint'):
 ref=next(p['items'][2] for p in children(f,'property') if p['items'][1]=='Reference')
 if val(f,'layer')[0]!='F.Cu':continue
 for pad in children(f,'pad'):
  nn=children(pad,'net')
  if not nn or nn[0]['items'][1] not in colors:continue
  net=nn[0]['items'][1];pin=pad['items'][1]
  o=next((o for o in qa['openings']['F'] if o['ref']==ref and o['pin']==pin),None)
  if o:
   g=load(o['polygons']);halo=g.buffer(.34).difference(g.buffer(.17)).intersection(clear);layers.append((ref+'.'+pin+' '+net,colors[net],halo))
# Exact-coordinate SVG and raster print assets. SVG path holes use even-odd winding.
def path(g):
 d=[]
 for p in polys(g):
  for ring in [p.exterior]+list(p.interiors):d.append('M '+' L '.join(f'{x:.6f},{y:.6f}' for x,y in ring.coords)+' Z')
 return ' '.join(d)
def svg(layers,width='15.875mm',view='92.0625 92.0625 15.875 15.875'):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="'+width+'" height="'+width+'" viewBox="'+view+'">'+''.join(f'<path fill="{c}" fill-rule="evenodd" d="{path(g)}"/>' for _,c,g in layers)+'</svg>'
(out/'F-color-print.svg').write_text(svg(layers));(out/'color-geometry.json').write_text(json.dumps([{'name':n,'color':c,'polygons':serial(g)} for n,c,g in layers]))
(out/'net-path-source.json').write_text(json.dumps({'derived_from':'mono-06 native track segments and filled F.Cu GND zone','solid':'F.Cu projection','dashed':'B.Cu projection at same board coordinates','ground':'F.Cu plane; does not prescribe a unique current path','segments':evidence},indent=2))
# Vector-based renderer, no modification of existing raster images.
def render(ls,dest,size=1800):
 im=Image.new('RGBA',(size,size),(0,0,0,0));factor=size/15.875
 for _,color,g in ls:
  mask=Image.new('L',(size,size));d=ImageDraw.Draw(mask)
  def xy(r):return [((x-92.0625)*factor,(y-92.0625)*factor) for x,y in r.coords]
  for p in polys(g):
   d.polygon(xy(p.exterior),fill=255)
   for h in p.interiors:d.polygon(xy(h),fill=0)
  layer=Image.new('RGBA',(size,size),color);im.alpha_composite(Image.composite(layer,Image.new('RGBA',(size,size)),mask))
 im.save(dest,dpi=(size/15.875*25.4,)*2)
render(layers,out/'F-color-print.png',2400)
# 1:1 PDF, with no labels or positioning marks in the printing artwork itself.
mm=72/25.4;c=Canvas(str(out/'F-color-print.pdf'),pagesize=(15.875*mm,15.875*mm))
for _,color,g in layers:
 c.setFillColor(HexColor(color));p=c.beginPath()
 for q in polys(g):
  for ring in [q.exterior]+list(q.interiors):
   points=list(ring.coords);p.moveTo((points[0][0]-92.0625)*mm,(107.9375-points[0][1])*mm)
   for x,y in points[1:]:p.lineTo((x-92.0625)*mm,(107.9375-y)*mm)
   p.close()
 c.drawPath(p,fill=1,stroke=0,fillMode=0)
c.showPage();c.save()
# Placement proof shows exact pad openings and component package outlines, not photorealistic bodies.
proof=[('board','#f7f7f2',board)]+layers+[('pads','#bcb5a1',openings)]
for f in children(root,'footprint'):
 if val(f,'layer')[0]!='F.Cu':continue
 at=val(f,'at');x,y=map(float,at[:2]);a=float(at[2]) if len(at)>2 else 0
 ref=next(p['items'][2] for p in children(f,'property') if p['items'][1]=='Reference')
 size=(.65,.38) if ref.startswith(('R','C')) else {'D1':(2.0,2.0),'D2':(.6,.35),'U2':(2.0,1.25),'J1':(4.0,3.3)}.get(ref,(1,1))
 g=translate(rotate(box(-size[0]/2,-size[1]/2,size[0]/2,size[1]/2),-a,origin=(0,0)),xoff=x,yoff=y)
 proof.append((ref+' body','#f2f0df' if ref in ['D1','J1'] else '#535559',g))
(out/'back-positioning.svg').write_text(svg(proof));render(proof,out/'back.png')
# Record unambiguous color CAD layers; fabrication electrical layers remain unchanged.
extra=[]
for net,layer in [('/VDD_IN','User.1'),('/VDD_PROTECTED','User.2'),('/GND','User.3'),('/LED_K','User.4')]:
 for e in evidence:
  if e['net']!=net:continue
  a,b=e['start'],e['end'];extra.append(f'(gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width 0.18) (type {"solid" if e["layer"]=="F.Cu" else "dash"})) (layer "{layer}") (uuid "{uuid.uuid4()}"))')
# Metadata describes the actual UV substrate; default native 3D cannot display multiple legend colors.
setup=children(root,'setup')[0];stack=children(setup,'stackup')[0];fm=next(n for n in children(stack,'layer') if n['items'][1]=='F.Mask');co=children(fm,'color')[0]
s=apply(s,[(co['start'],co['end'],'(color "White")')]);s=s.rstrip()[:-1]+'\n'+'\n'.join(extra)+'\n)\n';(out/'PulseSensor-JST-Educational.kicad_pcb').write_text(s)
inkunion=unary_union([g for _,_,g in layers]);report={'minimum_print_to_openings_mm':inkunion.distance(openings),'minimum_print_to_edge_mm':inkunion.distance(board.boundary),'copper_and_mask_openings':'Unchanged. Color paths are ink over solder mask, not exposed conductors.','base':'White F mask plus dark UV background; B optical face remains black mask and white silk.','projections':'Solid F.Cu, dashed B.Cu; blue area is F ground plane. Geometry clipped at labels and solder openings.','status':'SUPPLIER_PRINT_REVIEW_REQUIRED','layer_count':len(layers)}
(out/'print-clearance.json').write_text(json.dumps(report,indent=2));print(report)
