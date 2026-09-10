from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageOps
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09'
im=Image.new('RGB',(3600,1570),'#ffffff');d=ImageDraw.Draw(im);font=lambda z:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',z)
d.text((65,42),'PulseSensor / Green LED / red power / board + card',font=font(62),fill='#000000')
d.text((65,126),'Sheet 28 · Color-only iteration · Coral + lime + orange + sky blue + status green',font=font(35),fill='#333333')
assets=[('BOARD BACK / LED-GREEN / POWER-RED',r/'led-green-power-red-05-back.png'),('CARD / FULL SCHEMATIC',r/'output/card-1.png'),('CARD / PARTS SCHEDULE',r/'output/card-2.png')]
for i,(title,p) in enumerate(assets):
 x=65+i*1170;d.text((x,207),title,font=font(34),fill='#000000');pic=ImageOps.contain(Image.open(p).convert('RGBA'),(1105,1105),Image.Resampling.LANCZOS);im.paste(pic,(x,280),pic)
for i,(name,col) in enumerate(json.loads((r/'palette.json').read_text())['module_mapping'].items()):
 x=65+i*580;d.rounded_rectangle((x,1433,x+42,1475),5,fill=col,outline='#000000',width=1);d.text((x+58,1437),name+' '+col.upper(),font=font(28),fill='#000000')
d.text((65,1510),'Identical geometry, typography, schematic, component placement and dotted module boundaries. Earlier versions preserved.',font=font(30),fill='#333333')
im.save(r/'led-green-power-red-overview.png');im.save(s/'sheet-28.png')
m=json.loads((s/'sources.json').read_text());title='Green LED and red power board and card';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
a={'number':65,'title':title,'note':'Colors only; board SVG geometry and non-color PDF operators verified identical to prior versions.','sources':{}}
for role,p in [('board',r/'led-green-power-red-05-back.svg'),('card',r/'output/pdf/led-green-power-red-retail-purchase-card.pdf'),('palette',r/'palette.json'),('overview',r/'led-green-power-red-overview.png')]:a['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(a);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
snippet='<article><h2>Sheet 28 — PulseSensor WebSerial palette</h2><a href="sheet-28.png"><img src="sheet-28.png"></a></article>';p=s/'index.html';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';entry='\n## WebSerial color iteration — 2026-09-10\n\n[Sheet 28](sheet-28.png) shows matching WebSerial accent colors on the board and both purchase-card faces. [Palette evidence, print PDFs and color-only checks](../led-green-power-red-2026-09-10/README.md). All earlier geometry and text preserved.\n'
if entry not in p.read_text():p.write_text(p.read_text()+entry)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>PulseSensor WebSerial palette</title><style>body{max-width:1800px;margin:30px auto;padding:20px;font:18px system-ui}img{width:100%}a{color:#c8493f}</style><h1>PulseSensor WebSerial palette</h1><p>WebSerial coral, lime, orange, sky blue and status green. Color-only revisions of the board and purchase card.</p><img src="led-green-power-red-overview.png"><h2>Board before / after</h2><img src="board-comparison.png"><p><a href="output/pdf/led-green-power-red-retail-purchase-card.pdf">Card PDF</a> · <a href="led-green-power-red-05-back.svg">Board vector</a> · <a href="palette.json">Palette evidence</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p>')
print('Appended contact sheet 28 and artifact 65.')
