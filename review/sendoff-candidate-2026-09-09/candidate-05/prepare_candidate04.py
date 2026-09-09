"""Structural native-file edits avoid a KiCad 10 Python field-binding defect."""
from pathlib import Path
import re,json,uuid,shutil,xml.etree.ElementTree as ET
R=Path(__file__).parent;out=R/'candidate-04'
if out.exists():raise RuntimeError('Revision exists')
shutil.copytree(R/'candidate-01',out);p=out/'PulseSensor-JST-Educational.kicad_pcb';text=p.read_text()
stack=[];root=None
for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]|[^()\s]+',text):
 t=m.group()
 if t=='(':
  n={'start':m.start(),'items':[]}
  if stack:stack[-1]['items'].append(n)
  else:root=n
  stack.append(n)
 elif t==')':stack.pop()['end']=m.end()
 else:stack[-1]['items'].append(json.loads(t) if t.startswith('"') else t)
def children(n,kind):return [x for x in n['items'] if isinstance(x,dict) and x['items'][0]==kind]
x=ET.parse(R.parent/'appearance-study-2026-09-09/color-probe/rebuild-netlist.xml').getroot();comps={c.attrib['ref']:c for c in x.findall('./components/comp')}
edits=[];removed=0
for f in children(root,'footprint'):
 ref=next(x['items'][2] for x in children(f,'property') if x['items'][1]=='Reference')
 value=comps[ref].find('./fields/field[@name="Manufacturer"]').text or ''
 insert='\n (property "Manufacturer" '+json.dumps(value)+' (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "'+str(uuid.uuid4())+'") (effects (font (size 1 1) (thickness 0.15))))\n'
 edits.append((f['end']-1,f['end']-1,insert))
 for node in f['items']:
  if not isinstance(node,dict):continue
  if ref.startswith(('R','C')) and node['items'][0] in ('fp_line','fp_poly','fp_arc','fp_circle','fp_rect'):
   if any(c['items'][1]=='F.SilkS' for c in children(node,'layer')):edits.append((node['start'],node['end'],''));removed+=1
  if ref=='U1' and node['items'][0]=='pad' and node['items'][1] in ('2','3','5'):
   edits.append((node['end']-1,node['end']-1,' (net "unconnected-(U1-NC-Pad'+node['items'][1]+')") '))
for a,b,v in sorted(edits,reverse=True):text=text[:a]+v+text[b:]
p.write_text(text);shutil.copy2(__file__,out/'prepare_candidate04.py');print('Prepared',out,'removed',removed,'decorative marks')
