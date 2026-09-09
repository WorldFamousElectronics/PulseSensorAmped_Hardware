from pathlib import Path
import json,csv,hashlib,xml.etree.ElementTree as ET
from native_sexpr import parse,children
R=Path(__file__).parent;new=R/'candidate-05/PulseSensor-JST-Educational.kicad_pcb';base=Path('/Users/PulsesensorCorp/.codex/worktrees/2f83/PulseSensor Amped Hardware/PulseSensor-Amped-Rebuild/output/pcbway-release-candidates-RC3-R1-FINAL/PulseSensor-Amped-B-PCBWay-EVT-RC3-R1-FINAL');old=base/'SOURCE_SUPPORT/PulseSensor-Amped-B-JST.kicad_pcb';package=R/'manufacturing-review-candidate'
def canonical(n,skip=('uuid','net','property','tstamp')):
 if not isinstance(n,dict):return n
 return [canonical(x,skip) for x in n['items'] if not (isinstance(x,dict) and x['items'][0] in skip)]
def netname(name):return '' if name.startswith('unconnected-') else name.lstrip('/')
def extract(p):
 root=parse(p.read_text());fps={};nets={}
 for f in children(root,'footprint'):
  ref=next(x['items'][2] for x in children(f,'property') if x['items'][1]=='Reference');fps[ref]=f
  for pad in children(f,'pad'):
   n=children(pad,'net');nets[(ref,pad['items'][1])]=netname(n[0]['items'][-1]) if n else ''
 return root,fps,nets
oldroot,oldfp,oldnets=extract(old);root,fp,nets=extract(new);checks={}
checks['references_equal']=set(fp)==set(oldfp)
checks['pin_net_connectivity_unchanged']=nets==oldnets
def local_pads(f):
 angle=float(children(f,'at')[0]['items'][3]) if len(children(f,'at')[0]['items'])>3 else 0
 result=[]
 for pad in children(f,'pad'):
  items=canonical(pad)
  for item in items:
   if isinstance(item,list) and item and item[0]=='at':
    pad_angle=float(item[3]) if len(item)>3 else 0
    item[:]=['at',float(item[1]),float(item[2]),round((pad_angle-angle)%360,6)]
  result.append(items)
 return result
checks['all_pad_shapes_sizes_and_local_geometry_unchanged']=all(local_pads(fp[r])==local_pads(oldfp[r]) for r in fp)
fixed=['D1','U1','J1'];checks['fixed_optics_and_connector_positions_sides_rotations_unchanged']=all([canonical(n) for name in ['at','layer'] for n in children(fp[r],name)]==[canonical(n) for name in ['at','layer'] for n in children(oldfp[r],name)] for r in fixed)
checks['board_outline_unchanged']=[canonical(n) for n in children(root,'gr_circle')]==[canonical(n) for n in children(oldroot,'gr_circle')]
checks['packaged_native_matches_reviewed_native']=new.read_bytes()==(package/'SOURCE'/new.name).read_bytes()
x=ET.parse(package/'VALIDATION/netlist.xml').getroot();schem={}
for net in x.findall('./nets/net'):
 for node in net.findall('node'):schem[(node.attrib['ref'],node.attrib['pin'])]=netname(net.attrib['name'])
checks['schematic_connectivity_matches']=all(nets.get(k,'')==v for k,v in schem.items()) and all(not v or schem.get(k)==v for k,v in nets.items())
rows=list(csv.DictReader((package/'ASSEMBLY/CPL.csv').open()));prior=list(csv.DictReader((base/'ASSEMBLY/PulseSensor-Amped-B-CPL.csv').open()));nr={r['Ref']:r for r in rows};pr={r['Ref']:r for r in prior}
checks['cpl_exactly_16_components']=set(nr)==set(fp) and len(rows)==16
checks['cpl_positive_common_origin']=all(float(r['PosX'])>=0 and float(r['PosY'])>=0 for r in rows)
checks['fixed_components_cpl_matches_submitted_cpl']=all(all(nr[r][key]==pr[r][key] for key in ['PosX','PosY','Rot','Side']) for r in fixed)
checks['controlled_bom_unchanged']=(package/'ASSEMBLY/BOM-controlled-components.csv').read_bytes()==(base/'ASSEMBLY/PulseSensor-Amped-B-BOM.csv').read_bytes()
checks['controlled_population_unchanged']=(package/'ASSEMBLY/R1-controlled-population.csv').read_bytes()==(base/'ASSEMBLY/PulseSensor-Amped-B-R1-POPULATION-MATRIX.csv').read_bytes()
drc=json.loads((new.parent/'drc-final.json').read_text());checks['zero_unconnected']=not drc['unconnected_items'];checks['zero_schematic_parity_issues']=not drc['schematic_parity'];checks['only_existing_optical_exception']=len(drc['violations'])==1 and drc['violations'][0]['type']=='npth_inside_courtyard'
erc=json.loads((package/'VALIDATION/erc.json').read_text());checks['erc_clear']=not any(s.get('violations') for s in erc.get('sheets',[]))
report={'classification':'DEVELOPMENT','workstation':'PulseSilverBookPro','checks':checks,'source_board_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'candidate_board_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'moved_parts':[r for r in fp if canonical(children(fp[r],'at')[0])!=canonical(children(oldfp[r],'at')[0])],'net_alias_note':'Leading / matches KiCad schematic hierarchy; U1 NC pads have distinct unconnected-net names. Electrical connectivity is unchanged.','status':'GEOMETRY_AND_ELECTRICAL_COMPARISON_PASSED' if all(checks.values()) else 'REVISE'}
(package/'VALIDATION/comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
