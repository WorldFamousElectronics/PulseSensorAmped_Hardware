from pathlib import Path
import json,sys,math,hashlib,xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
R=Path(__file__).resolve().parent;OUT=R/'output';OUT.mkdir(exist_ok=True)
for n,f in [('Regular','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
C={'paper':'#f6f2e9','ink':'#102d38','soft':'#53666d','red':'#b73843','amber':'#925708','cyan':'#006b7b','violet':'#6342a8','line':'#cdd6d3','panel':'#fffdf8'}
board=R.parent/'power-color-2026-09-09/color-10/back.png'
font_sizes=[]
def draw_pdf(dest,bleed=0):
 W=288+bleed*2;c=canvas.Canvas(str(dest),pagesize=(W,W));c.setTitle('PulseSensor | Meet your circuit');c.setAuthor('World Famous Electronics LLC');c.setSubject('Two-sided 4 x 4 inch JST board circuit guide')
 def start():
  c.setFillColor(HexColor(C['paper']));c.rect(0,0,W,W,fill=1,stroke=0);c.saveState();c.translate(bleed,bleed)
 def text(x,y,s,size=9,bold=False,color='ink',align='left'):
  c.setFillColor(HexColor(C.get(color,color)));c.setFont('Bold' if bold else 'Regular',size);font_sizes.append(size)
  fn=c.drawString if align=='left' else c.drawCentredString if align=='center' else c.drawRightString;fn(x,288-y,s)
 def line(points,color='ink',width=.75,dash=None):
  c.setStrokeColor(HexColor(C.get(color,color)));c.setLineWidth(width);c.setDash(dash or []);p=c.beginPath();p.moveTo(points[0][0],288-points[0][1]);[p.lineTo(x,288-y) for x,y in points[1:]];c.drawPath(p);c.setDash([])
 def rect(x,y,w,h,color='panel',radius=7):
  c.setFillColor(HexColor(C.get(color,color)));c.roundRect(x,288-y-h,w,h,radius,fill=1,stroke=0)
 def dot(x,y,color='ink',r=1.5):c.setFillColor(HexColor(C[color]));c.circle(x,288-y,r,fill=1,stroke=0)
 def badge(x,y,n,col):
  c.setFillColor(HexColor(C[col]));c.circle(x,288-y,7,stroke=0,fill=1);text(x,y+2.5,str(n),8,True,'#ffffff','center')
 def ground(x,y):
  line([(x,y-5),(x,y)],'cyan');line([(x-5,y),(x+5,y)],'cyan');line([(x-3.4,y+2.4),(x+3.4,y+2.4)],'cyan');line([(x-1.5,y+4.8),(x+1.5,y+4.8)],'cyan')
 def resistor(x,y,ref,value='',vertical=False,col='ink'):
  if vertical:
   line([(x,y-11),(x,y-7)],col);line([(x,y+7),(x,y+11)],col);pts=[(x-3,y-7),(x+3,y-7),(x+3,y+7),(x-3,y+7),(x-3,y-7)];line(pts,col)
   text(x+5,y-1,ref,6.5,True);text(x+5,y+6,value,6.5,color='soft')
  else:
   line([(x-13,y),(x-8,y)],col);line([(x+8,y),(x+13,y)],col);line([(x-8,y-3),(x+8,y-3),(x+8,y+3),(x-8,y+3),(x-8,y-3)],col)
   text(x,y-8,ref,6.5,True,align='center')
   if value:text(x,y+12,value,6.5,color='soft',align='center')
 def cap(x,y,ref,value='',vertical=False,col='violet'):
  if vertical:
   line([(x,y-12),(x,y-2)],col);line([(x,y+2),(x,y+12)],col);line([(x-5,y-2),(x+5,y-2)],col);line([(x-5,y+2),(x+5,y+2)],col);text(x+7,y,ref,6.5,True);text(x+7,y+8,value,6.5,color='soft')
  else:
   line([(x-11,y),(x-2,y)],col);line([(x+2,y),(x+11,y)],col);line([(x-2,y-5),(x-2,y+5)],col);line([(x+2,y-5),(x+2,y+5)],col);text(x,y-9,ref,6.5,True,align='center');text(x,y+14,value,6.5,color='soft',align='center')
 def diode(x,y,name,led=False):
  line([(x-14,y),(x-6,y)],'amber');line([(x+6,y),(x+14,y)],'amber');line([(x-6,y-5),(x+4,y),(x-6,y+5),(x-6,y-5)],'amber');line([(x+5,y-6),(x+5,y+6)],'amber');text(x,y-10,name,6.5,True,align='center')
  if led:
   for a in [0,5]:line([(x-3+a,y-7),(x+1+a,y-12),(x-1+a,y-11)],'amber',.6)
 # FACE A — hardware only; no biological or sensing-science illustration.
 start();text(16,16,'PULSESENSOR  /  OPEN HARDWARE',7,True,color='soft')
 text(16,40,'Meet your circuit.',22,True)
 text(16,58,'Match the labels. Follow the connections.',9)
 c.drawImage(ImageReader(str(board)),14,288-213,144,144,mask='auto')
 text(170,75,'PARTS LIST / BOM',8,True,color='soft')
 text(170,88,'REF',6.8,True);text(211,88,'PART / VALUE',6.8,True)
 bom=[('R1','LED limit'),('R2','12k ohm'),('R3, R4','100k ohm'),('R5','10k ohm'),('R6','3.3M ohm'),('C1-C3','4.7 uF'),('C4, C5','2.2 uF'),('D1','Green LED'),('D2','Schottky diode'),('U1','APDS-9008'),('U2','MCP6001'),('J1','3-pin JST SH')]
 for i,(ref,value) in enumerate(bom):
  y=101+i*10.3
  if i%2==0:rect(166,y-7.5,110,10.3,'#e9ece5',1)
  text(170,y,ref,7.1,True);text(211,y,value,7.1)
 text(16,222,'U1 is on the other PCB face.',7,True)
 text(16,232,'k = thousand   M = million   uF = microfarads',7,True)
 # Print-friendly color key uses darkened versions of the PCB colors.
 for x,y,label,col in [(16,244,'+ supply','red'),(82,244,'Ground (-)','cyan'),(161,244,'Signal','violet'),(219,244,'PROT / LED','amber')]:
  dot(x+2,y-2,col,2);text(x+8,y,label,6.8,True,col)
 rect(14,251,260,17,'ink',4);text(22,262,'TL;DR  Power in. Filter + amplify. Signal out.',8.8,True,'#ffffff')
 text(16,278,'PCB BACK, ENLARGED  /  JST EDITION',6.5,True,color='soft');text(272,278,'pulsesensor.com',7,True,color='violet',align='right')
 c.restoreState();c.showPage()
 # FACE B
 start();text(16,16,'PULSESENSOR  /  FOLLOW THE CONNECTIONS',7,True,color='soft');text(16,37,'Same parts. Different view.',17,True)
 rect(12,46,264,61);text(20,56,'1  POWER + LED',7,True,color='amber')
 # LED branch: +V → LED → resistor → GND, independent of signal chain.
 text(26,73,'+V',7,True,'red');line([(43,70),(68,70)],'red');diode(82,70,'D1',True);line([(96,70),(122,70)],'amber');resistor(135,70,'R1',col='amber');line([(148,70),(190,70),(190,77)],'amber');ground(190,82);text(159,65,'LED current',6.5,color='amber')
 text(26,98,'+V',7,True,'red');line([(43,95),(60,95)],'red');diode(74,95,'D2');line([(88,95),(105,95)],'amber');text(109,97,'PROT to U1 & U2',7,True,'amber')
 text(241,60,'+V',7,True,'red',align='center');line([(241,62),(241,65)],'red');cap(241,77,'C5','2.2uF',True,'red');line([(241,89),(241,94)],'cyan');ground(241,99)
 # Sensor, filter and amplifier chain.
 rect(12,111,264,101);text(20,121,'2  INPUT',7,True,'cyan');text(90,121,'3  FILTER',7,True,'violet');text(202,121,'4  AMPLIFY',7,True,'violet')
 rect(20,134,35,33,'#e1eff0',3);text(37.5,145,'U1',8,True,'cyan','center');text(37.5,155,'LIGHT',6.5,True,'cyan','center');text(37.5,163,'SENSOR',6.5,True,'cyan','center')
 text(38,130,'PROT',6.5,True,'amber','center');line([(38,131),(38,134)],'amber');line([(38,167),(38,184)],'cyan');ground(38,189)
 line([(55,151),(66,151)],'cyan');dot(64,151,'cyan');line([(64,151),(64,164)],'cyan');resistor(64,175,'R2','12k',True,'cyan');line([(64,186),(64,189)],'cyan');ground(64,194)
 cap(79,151,'C2','4.7uF');line([(66,151),(68,151)],'violet');line([(90,151),(112,151)],'violet');dot(100,151,'violet');cap(123,151,'C3','4.7uF');line([(134,151),(153,151)],'violet');dot(145,151,'violet');resistor(169,151,'R5','10k',False,'violet');line([(153,151),(156,151)],'violet');line([(182,151),(204,151)],'violet')
 cap(100,179,'C1','4.7uF',True);line([(100,151),(100,167)],'violet');line([(100,191),(100,194)],'cyan');ground(100,199)
 cap(145,179,'C4','2.2uF',True);line([(145,151),(145,167)],'violet');line([(145,191),(145,204),(194,204),(194,170),(204,170)],'violet');text(161,202,'VREF',6.5,True,'violet')
 # Op-amp signal inputs and feedback, with explicit power labels.
 line([(204,142),(204,180),(233,161),(204,142)],'violet');text(207,154,'-',8,True,'violet');text(207,172,'+',8,True,'violet');text(218,163,'U2',7,True,'violet','center')
 line([(233,161),(265,161)],'violet');dot(247,161,'violet');text(258,151,'OUT',7,True,'violet','center');text(258,174,'J1.3',6.5,color='soft',align='center')
 line([(247,161),(247,131),(239,131)],'violet');resistor(226,131,'','',False,'violet');text(225,142,'R6',6.5,True,align='center');text(252,136,'3.3M',6.5,color='soft',align='center');line([(213,131),(190,131),(190,151)],'violet');dot(190,151,'violet')
 text(224,191,'U2 power:',6.5,color='soft',align='center');text(224,201,'PROT / GND',6.5,True,'amber',align='center')
 # Reference divider. All VREF labels refer to same circuit node.
 rect(12,217,264,28);text(20,228,'BIAS',7,True,'violet');text(48,241,'+V',7,True,'red');line([(61,238),(68,238)],'red');resistor(81,238,'R4','',False,'violet');line([(94,238),(119,238)],'violet');dot(107,238,'violet');text(107,229,'VREF',6.5,True,'violet','center');resistor(132,238,'R3','',False,'violet');line([(145,238),(163,238)],'cyan');ground(168,238);line([(163,238),(168,238)],'cyan');text(185,230,'R3 = R4 = 100k',6.5,True);text(185,241,'Sets the signal midpoint.',6.5,color='soft')
 # Legend with standard symbol meaning and connector pin map.
 text(16,255,'R = resistor',7,True);text(99,255,'C = capacitor',7,True);text(193,255,'U = chip',7,True)
 text(16,266,'J1: 1 GND (-)   2 +V   3 OUT',7,True,'cyan');text(272,266,'Matching labels connect.',6.5,color='soft',align='right')
 text(16,278,'PROT = protected supply after D2',6.5,True,color='soft')
 c.restoreState();c.showPage();c.save()
 if bleed:
  reader=PdfReader(dest);writer=PdfWriter()
  for p in reader.pages:p.trimbox=RectangleObject([bleed,bleed,bleed+288,bleed+288]);p.bleedbox=RectangleObject([0,0,W,W]);writer.add_page(p)
  with dest.open('wb') as f:writer.write(f)
for dest,b in [('PulseSensor-4x4-card.pdf',0),('PulseSensor-4x4-card-bleed.pdf',9)]:draw_pdf(OUT/dest,b)
(R/'layout-metrics.json').write_text(json.dumps({'trim_inches':[4,4],'bleed_inches':.125,'faces':2,'smallest_type_pt':min(font_sizes),'body_type_pt':'7.5-10','board_image_source':str(board),'illustration':'None; hardware-only per user correction'},indent=2))
print('Created two-face 4-inch card and 0.125-inch bleed PDF.')
