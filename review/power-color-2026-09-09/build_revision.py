from pathlib import Path
import sys,json,math,shutil,uuid,hashlib
sys.path.insert(0,'/Users/PulsesensorCorp/.codex/tmp/pulsesensor-art-tools')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'sendoff-candidate-2026-09-09'))
from native_sexpr import parse,children,apply
from shapely.geometry import Polygon,Point,box,LineString
from shapely.ops import unary_union
from shapely.affinity import translate,rotate,scale
from shapely import constrained_delaunay_triangles
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
R=Path(__file__).resolve().parent;OLD=R.parent/'sendoff-candidate-2026-09-09';src=OLD/'candidate-05';out=R/'mono-06';out.mkdir(exist_ok=True)
for p in src.iterdir():
 if p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym'] or p.name in ['fp-lib-table','sym-lib-table']:shutil.copy2(p,out/p.name)
for name in ['3dmodels','PulseSensor_Amped.pretty']:
 if not (out/name).exists():shutil.copytree(src/name,out/name)
text=(src/'PulseSensor-JST-Educational.kicad_pcb').read_text();root=parse(text)
def ch(n,k):return children(n,k)[0]['items'][1:]
def polyshape(n):return Polygon([tuple(map(float,x['items'][1:])) for x in children(children(n,'pts')[0],'xy')]).buffer(0)
def polylist(s):return [s] if s.geom_type=='Polygon' else [p for p in getattr(s,'geoms',[]) if p.geom_type=='Polygon']
def serial(s):return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in polylist(s)]
def deserial(items):return unary_union([Polygon(p['outer'],p['holes']).buffer(0) for p in items])
bnodes=[n for n in children(root,'gr_poly') if ch(n,'layer')[0]=='B.SilkS']
heartnodes=[n for n in bnodes if (polyshape(n).bounds[2]-polyshape(n).bounds[0]>8 or abs(polyshape(n).bounds[1]-102.8169)<.0001)]
heart=unary_union([polyshape(n) for n in heartnodes]);tail=[p for p in polylist(heart) if p.bounds[1]>102][0]
rounded=tail.intersection(box(90,90,110,103.15)).union(tail.buffer(-.20).buffer(.20).intersection(box(90,103.15,110,110)))
heart=heart.difference(tail).union(rounded)
qa=json.loads((src/'qa-geometry.json').read_text())
openings={s:unary_union([deserial(o['polygons']) for o in qa['openings'][s]]) for s in ['F','B']}
body=Point(100,100).buffer(7.9375,quad_segs=256)
class Flatten(BasePen):
 def __init__(self,g):super().__init__(g);self.contours=[];self.p=[]
 def _moveTo(self,p):self.p=[p]
 def _lineTo(self,p):self.p.append(p)
 def _qCurveToOne(self,c,b):
  a=self._getCurrentPoint()
  for i in range(1,13):
   t=i/12;self.p.append(tuple((1-t)**2*a[j]+2*(1-t)*t*c[j]+t*t*b[j] for j in [0,1]))
 def _curveToOne(self,c,d,b):
  a=self._getCurrentPoint()
  for i in range(1,17):
   t=i/16;self.p.append(tuple((1-t)**3*a[j]+3*(1-t)**2*t*c[j]+3*(1-t)*t*t*d[j]+t**3*b[j] for j in [0,1]))
 def _closePath(self):self.contours.append(self.p);self.p=[]
 def _endPath(self):self._closePath()
font=TTFont('/System/Library/Fonts/Supplemental/Arial Bold.ttf');gs=font.getGlyphSet();cm=font.getBestCmap();glyphs={}
for c in set('pulsesensor.com'):
 pen=Flatten(gs);gs[cm[ord(c)]].draw(pen);s=Polygon()
 for contour in pen.contours:
  if len(contour)>2:s=s.symmetric_difference(Polygon(contour).buffer(0))
 glyphs[c]=s
word='pulsesensor.com'
def wordmark(height,radius):
 sc=height/font['OS/2'].sxHeight;adv=[font['hmtx'][cm[ord(c)]][0]*sc for c in word];gap=.16;cursor=-(sum(adv)+gap*(len(word)-1))/2;letters=[]
 for c,w in zip(word,adv):
  phi=(cursor+w/2)/radius
  s=scale(glyphs[c],xfact=sc,yfact=-sc,origin=(0,0));s=translate(s,xoff=-w/2,yoff=height/2);s=rotate(s,-phi*180/math.pi,origin=(0,0));s=translate(s,xoff=100+radius*math.sin(phi),yoff=100+radius*math.cos(phi));s=scale(s,xfact=-1,yfact=1,origin=(100,100));letters.append(s);cursor+=w+gap
 return unary_union(letters)
fixedink=unary_union([deserial(o['polygons']) for o in qa['silk']['B'] if o['owner']!='artwork'])
trials=[];best=None
for h in [round(.8+.01*i,2) for i in range(71)]:
 for radius in [round(6.4+.025*i,3) for i in range(37)]:
  s=wordmark(h,radius)
  okay=body.buffer(-.20).covers(s) and s.distance(heart)>=.20 and s.distance(openings['B'])>=.16 and s.distance(fixedink)>=.15
  if okay and (best is None or h>best[0] or (h==best[0] and s.distance(heart)>best[3])):best=(h,radius,s,s.distance(heart))
 trials.append({'height_mm':h,'has_fit':best is not None and best[0]==h})
h,rad,wordshape,dist=best
cat=json.loads((OLD/'type-catalog.json').read_text())
fink=unary_union([deserial(o['polygons']) for o in qa['silk']['F']]);symbols=[]
# Place literal polarity marks near connector pins, respecting all existing ink and openings.
for symbol,pad,target in [('-', [99,102.25],[98.65,101.25]),('+',[100,102.25],[100,101.05])]:
 shape=deserial(cat[symbol]['polygons']); options=[]
 for ix in range(65):
  x=97.6+ix*.05
  for iy in range(27):
   y=100.45+iy*.05;s=translate(shape,xoff=x,yoff=y)
   if body.buffer(-.2).covers(s) and s.distance(openings['F'])>=.16 and s.distance(fink)>=.16:
    score=Point(x,y).distance(Point(target))
    if symbol=='+':score+=abs(x-100)*.6
    options.append((score,x,y,s))
 if not options:raise RuntimeError('No polarity label fit')
 _,x,y,s=min(options,key=lambda t:t[0]);symbols.append({'symbol':symbol,'x':x,'y':y,'pin': 'J1.1' if symbol=='-' else 'J1.2','polygons':serial(s)});fink=fink.union(s)
# Write planar polygons with triangulated holes; no pcbnew bindings are used.
def native(s,layer):
 entries=[]
 for p in polylist(s):
  pieces=polylist(constrained_delaunay_triangles(p)) if len(p.interiors) else [p]
  if len(p.interiors):pieces=list(constrained_delaunay_triangles(p).geoms)
  for q in pieces:
   pts=' '.join(f'(xy {x:.6f} {y:.6f})' for x,y in list(q.exterior.coords)[:-1]);entries.append(f'(gr_poly (pts {pts}) (stroke (width 0) (type solid)) (fill yes) (layer "{layer}") (uuid "{uuid.uuid4()}"))')
 return '\n'.join(entries)
edits=[(n['start'],n['end'],'') for n in bnodes];edited=apply(text,edits);extra=native(heart.union(wordshape),'B.SilkS')+'\n'+ '\n'.join(native(deserial(s['polygons']),'F.SilkS') for s in symbols)
edited=edited.rstrip()[:-1]+extra+'\n)\n';pcb=out/'PulseSensor-JST-Educational.kicad_pcb';pcb.write_text(edited)
qa['silk']['B']=[o for o in qa['silk']['B'] if o['owner']!='artwork']+[{'owner':'artwork','polygons':serial(heart.union(wordshape))}]
qa['silk']['F'] += [{'owner':'artwork','polygons':s['polygons']} for s in symbols]
(out/'qa-geometry.json').write_text(json.dumps(qa))
report={'wordmark_x_height_mm':h,'previous_x_height_mm':.8,'increase_percent':round((h/.8-1)*100,1),'arc_radius_mm':rad,'minimum_wordmark_to_heart_mm':dist,'fit_search':'0.01 mm height increments, 0.025 mm radial increments; minimum edge/heart gap 0.20 mm; fixed font and tracking','heart_tip_rounding_mm':.20,'polarity_marks':symbols,'trials':trials}
(out/'artwork-change.json').write_text(json.dumps(report,indent=2))
print('Selected wordmark',h,rad,'increase',report['increase_percent']);print('Symbols',[(s['symbol'],s['x'],s['y']) for s in symbols])
