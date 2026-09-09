from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'sendoff-candidate-2026-09-09'))
from native_sexpr import parse,children
r=Path(__file__).parent;old=r.parent/'sendoff-candidate-2026-09-09/candidate-05/PulseSensor-JST-Educational.kicad_pcb';t=old.read_text();base=parse(t)
def values(root,kind):return [canonical(n) for n in children(root,kind)]
def canonical(n):return [canonical(i) if isinstance(i,dict) else i for i in n['items']]
reports={}
for name in ['mono-06','color-07','mono-08','color-09','color-10']:
 p=r/name/'PulseSensor-JST-Educational.kicad_pcb';s=p.read_text();n=parse(s);d=json.loads((p.parent/'drc-final.json').read_text())
 checks={k+'_unchanged':values(base,k)==values(n,k) for k in ['footprint','segment','via','zone','gr_circle']}
 checks['schematic_unchanged']=p.with_suffix('.kicad_sch').read_bytes()==old.with_suffix('.kicad_sch').read_bytes()
 checks['no_new_mask_drawings']=all(not(children(x,'layer') and children(x,'layer')[0]['items'][1] in ['F.Mask','B.Mask']) for x in children(n,'gr_poly')+children(n,'gr_line'))
 checks['zero_unconnected']=not d['unconnected_items'];checks['zero_schematic_mismatches']=not d['schematic_parity'];checks['only_original_optical_exception']=len(d['violations'])==1 and d['violations'][0]['type']=='npth_inside_courtyard'
 reports[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':checks,'passed':all(checks.values())}
assert all(x['passed'] for x in reports.values())
(r/'verification.json').write_text(json.dumps(reports,indent=2)+'\n');print('All five revisions preserve every footprint, copper segment, via, zone, outline and schematic; no new mask openings; original DRC exception only.')
