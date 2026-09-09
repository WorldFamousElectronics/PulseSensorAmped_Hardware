import sys,json
from pathlib import Path
sys.path.insert(0,'/Users/PulsesensorCorp/.codex/tmp/pulsesensor-art-tools')
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
p=Path(sys.argv[1]);g=json.loads(p.read_text())
def geom(items):return unary_union([Polygon(x['outer'],x['holes']).buffer(0) for x in items if len(x['outer'])>=3])
issues=[];mins={}
for side in ('F','B'):
 ink=unary_union([geom(o['polygons']) for o in g['silk'][side]])
 own=unary_union([geom(o['polygons']) for o in g['silk'][side] if o['owner']=='artwork'])
 dist=[]
 for o in g['openings'][side]:
  shape=geom(o['polygons'])
  if shape.is_empty:continue
  d=ink.distance(shape);a=own.distance(shape);dist.append(d)
  if d<.149:issues.append({'side':side,'ref':o['ref'],'pin':o['pin'],'all_silk_clearance_mm':round(d,5),'new_artwork_clearance_mm':round(a,5)})
 mins[side]={'opening_clearance_mm':min(dist),'edge_clearance_mm':ink.distance(Point(100,100).buffer(7.9375,quad_segs=512).boundary)}
r={'minimums':mins,'issues':issues,'target_opening_clearance_mm':.15,'tented_vias':'No solder mask opening; separately kept away from back lettering.'};p.with_name('artwork-clearance.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
