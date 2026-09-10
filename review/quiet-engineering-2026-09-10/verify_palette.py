from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib
from pypdf import PdfReader
R=Path(__file__).parent
# Independent terminal map used to audit the manually laid-out complete schematic.
pins={'R1':['LED_K','GND'],'R2':['U1_IOUT','GND'],'R3':['VREF','GND'],'R4':['VDD_IN','VREF'],'R5':['FILTER_STAGE_2','AMP_INVERTING'],'R6':['AMP_INVERTING','SIGNAL'],'C1':['FILTER_STAGE_1','GND'],'C2':['U1_IOUT','FILTER_STAGE_1'],'C3':['FILTER_STAGE_1','FILTER_STAGE_2'],'C4':['FILTER_STAGE_2','VREF'],'C5':['VDD_IN','GND'],'D1':['LED_K','VDD_IN'],'D2':['VDD_PROTECTED','VDD_IN'],'J1':['GND','VDD_IN','SIGNAL'],'U1':{'1':'VDD_PROTECTED','2':'NC2','3':'NC3','4':'GND','5':'NC5','6':'U1_IOUT'},'U2':['SIGNAL','GND','VREF','AMP_INVERTING','VDD_PROTECTED']}
expected={}
for ref,v in pins.items():
 for pin,net in (v.items() if isinstance(v,dict) else [(str(i+1),n) for i,n in enumerate(v)]):expected[(ref,pin)]=net
source=R.parent/'power-color-2026-09-09/color-10-package/VALIDATION/netlist.xml';x=ET.parse(source);actual={}
for net in x.findall('./nets/net'):

 for node in net.findall('node'):actual[(node.attrib['ref'],node.attrib['pin'])]=('NC'+node.attrib['pin']) if net.attrib['name'].startswith('unconnected-') else net.attrib['name'].lstrip('/')
assert expected==actual
report={'electrical_terminal_map_matches_native_netlist':True,'terminals_including_NC':len(expected),'diagram_review':'Terminal mapping verified against native netlist; drawn connections visually inspected. Continuous signal, feedback and VREF wiring visually checked. Standard matching rail and OUT labels connect remaining common nodes. All U1, U2 and J1 pins shown, including three intentional U1 no-connects. This checks the independently transcribed terminal map; it is not automated PDF wire extraction.','components':'All 16 references shown. R1 described by function, with no invented resistance.','outputs':{}}
for name,size in [('quiet-engineering-retail-purchase-card.pdf',288),('quiet-engineering-retail-purchase-card-bleed.pdf',306)]:
 p=R/'output/pdf'/name;reader=PdfReader(p);assert len(reader.pages)==2
 for page in reader.pages:
  assert float(page.mediabox.width)==size and float(page.mediabox.height)==size
  assert float(page.trimbox.width)==288 and float(page.trimbox.height)==288
  t=page.extract_text()
  for forbidden in ['finger','PPG','blood','EVT_MATRIX','test unit']:assert forbidden.lower() not in t.lower()
 report['outputs'][name]={'pages':2,'media_box_pt':[size,size],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'terminal-map.json').write_text(json.dumps(pins,indent=2)+'\n');(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Verified',len(expected),'terminals including 3 NC; both two-page PDF sizes; hardware-only text.')

# Color-only preservation checks on final exported artifacts.
from pypdf.generic import ContentStream
import xml.etree.ElementTree as ET
old=ET.parse(R.parent/'module-outlines-2026-09-10/modules-02-back.svg').getroot()
new=ET.parse(R/'quiet-06-back.svg').getroot()
assert old.attrib==new.attrib and len(old)==len(new)
for a,b in zip(old,new):
 assert a.tag==b.tag
 assert {k:v for k,v in a.attrib.items() if k!='fill'}=={k:v for k,v in b.attrib.items() if k!='fill'}
prior=PdfReader(R.parent/'full-color-retail-card-2026-09-10/output/pdf/full-color-full-schematic-retail-purchase-card.pdf')
current=PdfReader(R/'output/pdf/quiet-engineering-retail-purchase-card.pdf')
def noncolor(page,reader):
 return [(str(args),op) for args,op in ContentStream(page.get_contents(),reader).operations if op not in [b'rg',b'RG',b'g',b'G',b'k',b'K']]
for a,b in zip(prior.pages,current.pages):assert noncolor(a,prior)==noncolor(b,current)
report['color_only']={'board_svg_geometry_identical':True,'card_noncolor_pdf_operators_identical':True,'palette_source':'palette.json'}
(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('Board SVG geometry and all non-color card PDF operators match prior versions exactly.')
