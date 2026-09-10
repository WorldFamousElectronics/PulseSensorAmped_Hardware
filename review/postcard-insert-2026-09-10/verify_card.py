from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib
from pypdf import PdfReader
R=Path(__file__).parent
# Independent terminal map used to audit the manually laid-out simplified schematic.
pins={'R1':['LED_K','GND'],'R2':['U1_IOUT','GND'],'R3':['VREF','GND'],'R4':['VDD_IN','VREF'],'R5':['FILTER_STAGE_2','AMP_INVERTING'],'R6':['AMP_INVERTING','SIGNAL'],'C1':['FILTER_STAGE_1','GND'],'C2':['U1_IOUT','FILTER_STAGE_1'],'C3':['FILTER_STAGE_1','FILTER_STAGE_2'],'C4':['FILTER_STAGE_2','VREF'],'C5':['VDD_IN','GND'],'D1':['LED_K','VDD_IN'],'D2':['VDD_PROTECTED','VDD_IN'],'J1':['GND','VDD_IN','SIGNAL'],'U1':{'1':'VDD_PROTECTED','4':'GND','6':'U1_IOUT'},'U2':['SIGNAL','GND','VREF','AMP_INVERTING','VDD_PROTECTED']}
expected={}
for ref,v in pins.items():
 for pin,net in (v.items() if isinstance(v,dict) else [(str(i+1),n) for i,n in enumerate(v)]):expected[(ref,pin)]=net
source=R.parent/'power-color-2026-09-09/color-10-package/VALIDATION/netlist.xml';x=ET.parse(source);actual={}
for net in x.findall('./nets/net'):
 if net.attrib['name'].startswith('unconnected-'):continue
 for node in net.findall('node'):actual[(node.attrib['ref'],node.attrib['pin'])]=net.attrib['name'].lstrip('/')
assert expected==actual
report={'electrical_terminal_map_matches_native_netlist':True,'connected_terminals':len(expected),'diagram_review':'Terminal mapping verified against native netlist; drawn connections visually inspected. IC supplies use named labels; unused U1 pins omitted.','bom':'All 16 component references included; equal-value passives grouped. R1 described by function, with no invented resistance.','outputs':{}}
for name,size in [('PulseSensor-4x4-card.pdf',288),('PulseSensor-4x4-card-bleed.pdf',306)]:
 p=R/'output'/name;reader=PdfReader(p);assert len(reader.pages)==2
 for page in reader.pages:
  assert float(page.mediabox.width)==size and float(page.mediabox.height)==size
  t=page.extract_text()
  for forbidden in ['finger','PPG','blood','EVT_MATRIX','test unit']:assert forbidden.lower() not in t.lower()
 report['outputs'][name]={'pages':2,'media_box_pt':[size,size],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Verified',len(expected),'connected terminals; both two-page PDF sizes; hardware-only text.')
