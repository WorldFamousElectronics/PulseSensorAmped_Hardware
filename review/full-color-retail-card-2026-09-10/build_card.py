from pathlib import Path
import json, xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
R=Path(__file__).resolve().parent; O=R/'output/pdf'
for n,f in [('Regular','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
C=dict(paper='#f1e8ce',ink='#24251f',soft='#45483e',red='#24251f',amber='#24251f',cyan='#24251f',violet='#24251f',panel='#eee4c9',power='#bfd0d8',led='#e7c78f',sense='#c1cfb2',filter='#b6cfca',amp='#ccc1d7',bias='#ddbdc5')
def make(path,bleed):
 w=288+2*bleed;c=canvas.Canvas(str(path),pagesize=(w,w));c.setTitle('Full-Color Full Schematic Retail Purchase Card');c.setAuthor('World Famous Electronics LLC')
 def start():
  c.setFillColor(HexColor(C['paper']));c.rect(0,0,w,w,fill=1,stroke=0);c.saveState();c.translate(bleed,bleed);c.scale(.48,.48)
 def t(x,y,s,z=14,b=False,col='ink',a='left'):
  c.setFillColor(HexColor(C.get(col,col)));c.setFont('Bold' if b else 'Regular',z);getattr(c,{'left':'drawString','center':'drawCentredString','right':'drawRightString'}[a])(x,600-y,s)
 def l(p,col='ink',width=1.5):
  c.setStrokeColor(HexColor(C[col]));c.setLineWidth(width);q=c.beginPath();q.moveTo(p[0][0],600-p[0][1]);[q.lineTo(x,600-y) for x,y in p[1:]];c.drawPath(q)
 def box(x,y,w,h,col='panel'):
  c.setFillColor(HexColor(C[col]));c.roundRect(x,600-y-h,w,h,10,fill=1,stroke=0)
 def dot(x,y,col='violet'):
  c.setFillColor(HexColor(C[col]));c.circle(x,600-y,2.8,fill=1,stroke=0)
 def g(x,y):
  l([(x,y-8),(x,y)],'cyan')
  for off,half in [(0,8),(4,5),(8,2)]:l([(x-half,y+off),(x+half,y+off)],'cyan')
 def res(x,y,ref,val,col='ink',vert=False):
  p=[(-24,0),(-16,0),(-12,-5),(-6,5),(0,-5),(6,5),(12,-5),(16,0),(24,0)]
  l([(x+dy,y+dx) if vert else (x+dx,y+dy) for dx,dy in p])
  if vert:t(x+11,y-1,ref,14,True);t(x+11,y+15,val,14,col='soft')
  else:t(x,y-13,ref,14,True,a='center');t(x,y+22,val,14,col='soft',a='center')
 def cap(x,y,ref,val,vert=False):
  if vert:
   l([(x,y-20),(x,y-4)],'violet');l([(x,y+4),(x,y+20)],'violet');l([(x-9,y-4),(x+9,y-4)],'violet');l([(x-9,y+4),(x+9,y+4)],'violet');t(x+13,y,ref,14,True);t(x+13,y+16,val,14,col='soft')
  else:
   l([(x-20,y),(x-4,y)],'violet');l([(x+4,y),(x+20,y)],'violet');l([(x-4,y-9),(x-4,y+9)],'violet');l([(x+4,y-9),(x+4,y+9)],'violet');t(x,y-15,ref,14,True,a='center');t(x,y+24,val,14,col='soft',a='center')
 def diode(x,y,ref,led=False):
  l([(x-25,y),(x-10,y)],'amber');l([(x+10,y),(x+25,y)],'amber');l([(x-10,y-8),(x+7,y),(x-10,y+8),(x-10,y-8)],'amber');l([(x+9,y-10),(x+9,y+10)],'amber')
  if not led:l([(x+5,y-10),(x+9,y-10)],'amber');l([(x+9,y+10),(x+13,y+10)],'amber')
  if led:
   for dx in [0,9]:l([(x-2+dx,y-12),(x+5+dx,y-21),(x+1+dx,y-20)],'amber')
  t(x-15,y+20,'2',13.5,col='soft');t(x+14,y+20,'1',13.5,col='soft');t(x+34,y-13,ref,14,True)
 def head(x,y,label,col):t(x,y,label,15,True,col)
 # One continuous signal schematic; functional color washes have no enclosing boxes.
 start()
 t(25,28,'PULSESENSOR  /  ELECTRONIC ASSEMBLY SERIES',13,True)
 l([(24,38),(576,38)],width=2)
 t(24,65,'FULL-COLOR FULL SCHEMATIC',25,True)
 t(24,89,'RETAIL PURCHASE CARD',25,True)
 t(24,111,'CIRCUIT DIAGRAM & PARTS REFERENCE  /  JST EDITION',13,True)
 # Continuous print-tint background, keyed to the board's six functional colors.
 for x,y,bw,bh,col in [(24,126,274,119,'power'),(298,126,278,119,'led'),(24,245,171,213,'sense'),(195,245,145,213,'filter'),(340,245,236,213,'amp'),(24,458,278,99,'power'),(302,458,274,99,'bias')]:
  c.setFillColor(HexColor(C[col]));c.rect(x,600-y-bh,bw,bh,fill=1,stroke=0)
 t(35,146,'POWER',13,True);t(311,146,'LED',13,True)
 # J1 explicit, all connector terminals. Standard equal-name labels join rails.
 l([(39,161),(85,161),(85,228),(39,228),(39,161)])
 t(62,179,'J1',16,True,a='center')
 for y,n,label in [(186,'1','GND'),(203,'2','+V'),(220,'3','OUT')]:
  t(71,y-3,n,13.5);l([(85,y),(107,y)]);t(111,y+4,label,14,True)
 # Incoming bypass C5, protective D2, and U1 supply linked by wire.
 t(179,166,'+V',14,True,a='center');l([(179,169),(179,183)]);cap(179,203,'C5','2.2uF',True);l([(179,223),(179,224)]);g(179,232)
 t(232,174,'+V',14,True,a='center');l([(232,176),(232,185),(237,185)]);diode(262,185,'');t(263,166,'D2',14,True,a='center')
 l([(287,185),(291,185),(291,259),(69,259),(69,300)]);t(256,237,'PROT',14,True)
 # Independent illumination branch.
 t(314,185,'+V',14,True);l([(340,181),(344,181)]);diode(369,181,'D1',True);l([(394,181),(416,181)]);res(440,181,'R1','LED limit');l([(464,181),(548,181),(548,210)]);g(548,218)
 t(314,235,'D1 + R1 form the LED current path.',13)
 # Sensor and uninterrupted left-to-right signal path.
 t(100,283,'SENSE',13,True);t(207,283,'FILTER',13,True);t(354,283,'AMPLIFY',13,True)
 l([(39,300),(99,300),(99,365),(39,365),(39,300)])
 t(69,319,'U1',17,True,a='center');t(69,338,'APDS-',13,a='center');t(69,354,'9008',13,a='center');t(75,298,'1',13)
 for y,n in [(312,'2'),(334,'3'),(356,'5')]:
  l([(30,y),(39,y)]);l([(27,y-3),(33,y+3)]);l([(27,y+3),(33,y-3)]);t(40,y-2,n,13)
 t(38,383,'NC',13);l([(69,365),(69,410)]);t(75,379,'4',13);g(69,418)
 l([(99,333),(145,333)]);t(102,329,'6',13);t(124,318,'IOUT',13,True,a='center')
 dot(125,333);l([(125,333),(125,372)]);res(125,396,'R2','12k',vert=True);l([(125,420),(125,424)]);g(125,432)
 cap(165,333,'C2','4.7uF');l([(185,333),(238,333)]);dot(213,333)
 cap(258,333,'C3','4.7uF');l([(278,333),(342,333)]);dot(307,333)
 res(366,333,'R5','10k');l([(390,333),(443,333)]);dot(420,333)
 l([(213,333),(213,373)]);cap(213,393,'C1','4.7uF',True);l([(213,413),(213,425)]);g(213,433)
 l([(307,333),(307,373)]);cap(307,393,'C4','2.2uF',True)
 # U2 signal pins and feedback remain physically joined; power uses standard PROT label.
 l([(443,318),(443,390),(495,354),(443,318)])
 t(447,339,'-',16,True);t(447,379,'+',16,True);t(467,359,'U2',15,True,a='center');t(430,329,'4',13);t(430,373,'3',13)
 l([(495,354),(561,354)]);t(499,349,'1',13);t(557,375,'OUT',14,True,a='right');dot(546,354)
 l([(420,333),(420,304),(461,304)]);res(485,304,'R6','');t(545,294,'3.3M',14,a='center');l([(509,304),(546,304),(546,354)])
 l([(466,334),(466,322),(502,322)]);t(471,334,'5',13);t(506,326,'PROT',13,True)
 l([(466,374),(466,418)]);t(474,404,'2',13);g(466,426)
 # One joined VREF line, from C4 and U2+ down to the divider midpoint.
 l([(307,413),(307,445),(414,445),(414,376),(443,376)])
 dot(381,445);l([(381,445),(381,503)]);t(356,439,'VREF',14,True)
 # Reference divider wired to that same VREF node, without a separate diagram.
 t(430,477,'BIAS',13,True)
 t(316,528,'+V',14,True);l([(342,524),(345,524)]);res(369,524,'R4','100k');l([(393,524),(430,524)]);dot(408,524)
 l([(381,503),(408,503),(408,524)]);res(454,524,'R3','100k');l([(478,524),(547,524),(547,531)]);g(547,539)
 t(35,480,'READING THE DRAWING',13,True)
 t(35,502,'Solid lines are electrical connections.',13)
 t(35,520,'A solid dot joins wires. NC is unused.',13)
 t(35,538,'Matching supply labels connect.',13)
 l([(24,566),(576,566)],width=2)
 t(24,584,'R: ohms  /  C: microfarads  /  GND: 0V  /  PROT: supply after D2',13,True)
 c.restoreState();c.showPage();start()
 t(24,29,'PULSESENSOR  /  ELECTRONIC ASSEMBLY SERIES',13,True)
 l([(24,38),(576,38)],width=2);t(24,70,'BENCH REFERENCE',30,True)
 t(24,94,'Keep this card beside the circuit board.',16)
 t(24,123,'PARTS SCHEDULE',16,True);l([(24,132),(576,132)])
 t(32,151,'MARKING',13,True);t(155,151,'VALUE / TYPE',13,True);t(350,151,'PURPOSE',13,True)
 rows=[('R1','LED current limiter','Limits LED current','led'),('R2','12k ohm','Current-to-voltage load','sense'),('R3, R4','100k ohm each','Reference divider','bias'),('R5','10k ohm','Amplifier input','amp'),('R6','3.3M ohm','Amplifier feedback','amp'),('C1, C3','4.7uF each','Filter network','filter'),('C2','4.7uF','Input coupling','sense'),('C4','2.2uF','Filter to reference','filter'),('C5','2.2uF','Supply bypass','power'),('D1','Green LED','Illumination branch','led'),('D2','Schottky diode','Protected chip supply','power'),('U1','APDS-9008','Sensor chip','sense'),('U2','MCP6001','Operational amplifier','amp'),('J1','3-pin JST SH','Power and output','power')]
 for i,(ref,value,role,col) in enumerate(rows):
  y=174+i*20;c.setFillColor(HexColor(C[col]));c.rect(24,600-y-5,552,19,fill=1,stroke=0);t(32,y,ref,14,True);t(155,y,value,14);t(350,y,role,14)
 t(24,465,'HOW TO FOLLOW THE CIRCUIT',15,True)
 t(24,486,'U1 and R2 feed the capacitors. Follow the solid line to U2.',14)
 t(24,505,'R6 returns OUT to the - input. VREF sets the + input midpoint.',14)
 t(24,524,'The color tints match the functional areas on the PCB.',14)
 t(24,543,'J1 pins:  1 GND (-)     2 +V     3 OUT',15,True)
 l([(24,559),(576,559)],width=2)
 t(24,579,'OPEN HARDWARE  /  pulsesensor.com',14,True)
 c.restoreState();c.showPage();c.save()
 if bleed:
  rd=PdfReader(path);wr=PdfWriter()
  for p in rd.pages:p.trimbox=RectangleObject([9,9,297,297]);p.bleedbox=RectangleObject([0,0,306,306]);wr.add_page(p)
  with path.open('wb') as f:wr.write(f)
for name,b in [('full-color-full-schematic-retail-purchase-card.pdf',0),('full-color-full-schematic-retail-purchase-card-bleed.pdf',9)]:make(O/name,b)
print('Created full-color full schematic retail purchase card.')
