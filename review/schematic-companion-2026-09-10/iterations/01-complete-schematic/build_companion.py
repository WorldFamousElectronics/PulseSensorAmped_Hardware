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
C=dict(paper='#f6f2e9',ink='#102d38',soft='#53666d',red='#b73843',amber='#925708',cyan='#006b7b',violet='#6342a8',panel='#fffdf8')
def make(path,bleed):
 w=288+2*bleed;c=canvas.Canvas(str(path),pagesize=(w,w));c.setTitle('PulseSensor | Complete circuit companion');c.setAuthor('World Famous Electronics LLC')
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
  if vert:
   l([(x,y-20),(x,y-12),(x-5,y-12),(x-5,y+12),(x+5,y+12),(x+5,y-12),(x,y-12)],col);l([(x,y+12),(x,y+20)],col);t(x+11,y-1,ref,14,True);t(x+11,y+15,val,14,col='soft')
  else:
   l([(x-24,y),(x-15,y),(x-15,y-5),(x+15,y-5),(x+15,y+5),(x-15,y+5),(x-15,y),(x+15,y),(x+24,y)],col) if False else None
   l([(x-24,y),(x-15,y)],col);l([(x+15,y),(x+24,y)],col);l([(x-15,y-5),(x+15,y-5),(x+15,y+5),(x-15,y+5),(x-15,y-5)],col);t(x,y-12,ref,14,True,a='center');t(x,y+23,val,14,col='soft',a='center')
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
  t(x-15,y+20,'2',12,col='soft');t(x+14,y+20,'1',12,col='soft');t(x,y-27,ref,14,True,a='center')
 def head(x,y,label,col):t(x,y,label,15,True,col)
 start();t(24,30,'PULSESENSOR  /  OPEN HARDWARE  /  CARD 02',14,True,'soft');t(24,66,'The whole circuit.',34,True);t(24,88,'Same label = same wire, even between separate boxes.',15)
 box(24,102,264,126);head(38,122,'1  CONNECT + DECOUPLE','red')
 # Actual connector with every pin; C5 connected across incoming supply.
 l([(40,140),(88,140),(88,210),(40,210),(40,140)]);t(64,157,'J1',16,True,a='center')
 for y,n,lab,col in [(168,'1','GND','cyan'),(186,'2','+V','red'),(204,'3','OUT','violet')]:t(74,y-3,n,12);l([(88,y),(110,y)],col);t(115,y+4,lab,14,True,col)
 t(226,144,'+V',14,True,'red',a='center');l([(226,148),(226,154)],'red');cap(226,174,'C5','2.2uF',True);l([(226,194),(226,203)],'cyan');g(226,211)
 box(300,102,276,126);head(314,122,'2  POWER + LED','amber')
 t(313,162,'+V',14,True,'red');l([(338,158),(345,158)],'red');diode(370,158,'D1',True);l([(395,158),(416,158)],'amber');res(440,158,'R1','LED limit','amber');l([(464,158),(540,158),(540,170)],'amber');g(540,178)
 t(313,212,'+V',14,True,'red');l([(338,208),(345,208)],'red');diode(370,208,'D2');l([(395,208),(435,208)],'amber');t(441,212,'PROT',14,True,'amber')
 box(24,240,300,154);head(38,262,'3  SENSOR + CURRENT LOAD','cyan')
 # U1 complete package, including all intentional no-connects.
 l([(77,291),(149,291),(149,357),(77,357),(77,291)],'cyan');t(113,308,'U1',17,True,a='center');t(113,326,'APDS-',14,a='center');t(113,343,'9008',14,a='center')
 t(111,279,'PROT',14,True,'amber',a='center');l([(111,281),(111,291)],'amber');t(117,289,'1',12)
 l([(111,357),(111,373)],'cyan');t(117,370,'4',12);g(111,380)
 for y,n in [(303,'2'),(325,'3'),(347,'5')]:l([(61,y),(77,y)],'soft');l([(57,y-4),(65,y+4)],'soft');l([(57,y+4),(65,y-4)],'soft');t(78,y-3,n,12)
 t(38,379,'NC',13,col='soft');l([(149,319),(238,319)],'cyan');t(151,315,'6',12);t(179,307,'IOUT',14,True,'violet');dot(216,319,'cyan');l([(216,319),(216,334)],'cyan');res(216,354,'R2','12k','cyan',True);g(216,382)
 box(336,240,240,154);head(350,262,'4  MAKE A MIDPOINT','violet')
 t(352,316,'+V',14,True,'red');l([(380,312),(387,312)],'red');res(411,312,'R4','100k','violet');l([(435,312),(452,312)],'violet');dot(447,312);res(476,312,'R3','100k','violet');l([(500,312),(551,312),(551,340)],'cyan');g(551,348)
 l([(447,312),(447,356)],'violet');t(447,375,'VREF',14,True,'violet',a='center')
 box(24,406,302,152);head(38,427,'5  FILTER','violet')
 t(38,455,'IOUT',14,True,'violet');l([(74,451),(79,451)],'violet');cap(99,451,'C2','4.7uF');l([(119,451),(166,451)],'violet');cap(186,451,'C3','4.7uF');l([(206,451),(292,451)],'violet');t(294,455,'B',14,True,'violet')
 dot(142,451);l([(142,451),(142,487)],'violet');cap(142,507,'C1','4.7uF',True);l([(142,527),(142,533)],'cyan');g(142,541)
 dot(238,451);l([(238,451),(238,487)],'violet');cap(238,507,'C4','2.2uF',True);t(238,547,'VREF',14,True,'violet',a='center');l([(238,527),(238,533)],'violet')
 box(338,406,238,152);head(352,427,'6  AMPLIFY','violet')
 # R6 feeds OUT back to the inverting input. All five U2 pins drawn.
 t(351,489,'B',14,True,'violet');l([(362,485),(366,485)],'violet');res(390,485,'R5','10k','violet');l([(414,485),(454,485)],'violet');dot(432,485)
 l([(432,485),(432,451),(438,451)],'violet');res(462,451,'R6','3.3M','violet');l([(486,451),(553,451),(553,498)],'violet')
 l([(454,475),(454,525),(496,500),(454,475)],'violet');t(458,490,'-',15,True);t(458,516,'+',15,True);t(474,505,'U2',14,True,a='center');t(445,482,'4',12);t(445,514,'3',12)
 l([(496,500),(560,500)],'violet');l([(553,498),(553,500)],'violet');dot(553,500);t(503,495,'1',12);t(552,522,'OUT',14,True,'violet',a='center')
 l([(438,516),(454,516)],'violet');t(433,540,'VREF',14,True,'violet',a='right');l([(433,536),(438,536),(438,516)],'violet')
 l([(476,488),(476,478)],'amber');t(482,479,'5',12);t(510,479,'PROT',13,True,'amber',a='center')
 l([(476,512),(476,537)],'cyan');t(482,531,'2',12);g(476,545)
 t(24,579,'GND = 0V    PROT = supply after D2    NC = intentionally unconnected',14,True,'soft')
 c.restoreState();c.showPage();start()
 t(24,30,'PULSESENSOR  /  SCHEMATIC READING GUIDE',14,True,'soft');t(24,67,'You can read this.',34,True)
 t(24,93,'Start with J1. Then follow the matching labels.',17)
 box(24,111,552,88,'ink');t(40,136,'TL;DR',15,True,'#ffffff');t(40,160,'J1 brings in power and carries OUT back.',20,True,'#ffffff');t(40,183,'U1 + R2 feed the filter. U2 amplifies the result.',17,False,'#ffffff')
 items=[('1','CONNECT + DECOUPLE','J1 is the cable connector. C5 helps steady','the incoming supply. Pins: 1 GND, 2 +V, 3 OUT.'),('2','POWER + LED','D1 is the LED; R1 limits its current. D2 feeds','the protected supply, PROT, to U1 and U2.'),('3','SENSOR + CURRENT LOAD','U1 is the sensor chip. R2 turns its output','current into a voltage at the IOUT connection.'),('4','MAKE A MIDPOINT','R4 and R3 divide +V in half to make VREF.','This reference gives the signal a midpoint.'),('5','FILTER','C2 and C3 are in the signal path. C1 and C4','connect it to GND and VREF, shaping the response.'),('6','AMPLIFY','U2 is an op-amp. R6 returns OUT to its - input;','R5 and R6 set the gain. Its + input uses VREF.')]
 for i,(n,h,a,b) in enumerate(items):
  y=222+i*43;t(27,y,n,19,True,'violet');t(50,y,h,14,True);t(50,y+17,a,15);t(50,y+33,b,15)
 box(24,488,552,70);t(38,510,'THE SYMBOL KEY',14,True)
 t(38,531,'R  resistor',15,True);t(170,531,'C  capacitor',15,True);t(320,531,'D  diode / LED',15,True);t(485,531,'U  chip',15,True)
 t(38,550,'Dot = wires join. Small pin numbers match the chip or connector.',14)
 t(24,579,'Match R1, C2, U2... to the PCB + BOM on card 01.',15,True,'violet')
 c.restoreState();c.showPage();c.save()
 if bleed:
  rd=PdfReader(path);wr=PdfWriter()
  for p in rd.pages:p.trimbox=RectangleObject([9,9,297,297]);p.bleedbox=RectangleObject([0,0,306,306]);wr.add_page(p)
  with path.open('wb') as f:wr.write(f)
for name,b in [('PulseSensor-complete-schematic-4x4.pdf',0),('PulseSensor-complete-schematic-4x4-bleed.pdf',9)]:make(O/name,b)
print('Created companion schematic card, two faces.')
