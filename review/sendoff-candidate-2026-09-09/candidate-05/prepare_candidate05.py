from pathlib import Path
import re,json,uuid,shutil,xml.etree.ElementTree as ET
from native_sexpr import parse,children,apply
R=Path(__file__).parent;out=R/'candidate-05'
if out.exists():raise RuntimeError('Revision exists')
shutil.copytree(R/'candidate-04',out);p=out/'PulseSensor-JST-Educational.kicad_pcb';text=p.read_text();root=parse(text)
x=ET.parse(R.parent/'appearance-study-2026-09-09/color-probe/rebuild-netlist.xml').getroot();comps={c.attrib['ref']:c for c in x.findall('./components/comp')};edits=[]
rename={'Resistor_SMD:R_0402_1005Metric':'PulseSensor_Amped:R_0402_Educational','Capacitor_SMD:C_0402_1005Metric':'PulseSensor_Amped:C_0402_Educational'}
for f in children(root,'footprint'):
 props={x['items'][1]:x for x in children(f,'property')};ref=props['Reference']['items'][2]
 for field in comps[ref].findall('./fields/field'):
  key=field.attrib['name'];value=field.text or ''
  if key=='Footprint':continue
  if key in props:
   n=props[key];old=text[n['start']:n['end']];new=re.sub(r'(\(property\s+"'+re.escape(key)+r'"\s+)"(?:\\.|[^"\\])*"',lambda m:m.group(1)+json.dumps(value),old,count=1);edits.append((n['start'],n['end'],new))
  else:
   insert='\n (property '+json.dumps(key)+' '+json.dumps(value)+' (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "'+str(uuid.uuid4())+'") (effects (font (size 1 1) (thickness 0.15))))\n';edits.append((f['end']-1,f['end']-1,insert))
text=apply(text,edits)
for old,new in rename.items():text=text.replace('"'+old+'"','"'+new+'"')
p.write_text(text)
sch=out/'PulseSensor-JST-Educational.kicad_sch';text=sch.read_text()
for old,new in rename.items():text=text.replace('"'+old+'"','"'+new+'"')
sch.write_text(text)
base=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
for old,new in rename.items():
 lib,name=old.split(':');newname=new.split(':')[1];text=(base/(lib+'.pretty')/(name+'.kicad_mod')).read_text();root=parse(text);edits=[]
 for node in root['items']:
  if not isinstance(node,dict):continue
  if node['items'][0] in ('fp_line','fp_poly','fp_arc','fp_circle','fp_rect') and any(c['items'][1]=='F.SilkS' for c in children(node,'layer')):edits.append((node['start'],node['end'],''))
 text=apply(text,edits).replace('(footprint "'+name+'"','(footprint "'+newname+'"',1);(out/'PulseSensor_Amped.pretty'/(newname+'.kicad_mod')).write_text(text)
shutil.copy2(__file__,out/'prepare_candidate05.py');shutil.copy2(R/'native_sexpr.py',out/'native_sexpr.py');print('Prepared',out)
