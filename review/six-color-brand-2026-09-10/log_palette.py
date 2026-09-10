from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageOps
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09'
im=Image.new('RGB',(3600,1570),'#ffffff');d=ImageDraw.Draw(im);font=lambda z:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',z)
d.text((65,42),'PulseSensor / Six-color brand / board + card',font=font(62),fill='#000000')
d.text((65,126),'Sheet 30 · Color-only iteration · White · black · PulseSensor red · LED green · gray · beige',font=font(35),fill='#333333')
assets=[('BOARD BACK / SIX-COLOR-07',r/'six-color-07-back.png'),('CARD / FULL SCHEMATIC',r/'output/card-1.png'),('CARD / PARTS SCHEDULE',r/'output/card-2.png')]
for i,(title,p) in enumerate(assets):
 x=65+i*1170;d.text((x,207),title,font=font(34),fill='#000000');pic=ImageOps.contain(Image.open(p).convert('RGBA'),(1105,1105),Image.Resampling.LANCZOS);im.paste(pic,(x,280),pic)
for i,(name,col) in enumerate(json.loads((r/'palette.json').read_text())['board_palette'].items()):
 x=65+i*580;d.rounded_rectangle((x,1433,x+42,1475),5,fill=col,outline='#000000',width=1);d.text((x+58,1437),name+' '+col.upper(),font=font(28),fill='#000000')
d.text((65,1510),'Identical geometry, typography, schematic, component placement and dotted module boundaries. Earlier versions preserved.',font=font(30),fill='#333333')
im.save(r/'six-color-overview.png');im.save(s/'sheet-30.png')
m=json.loads((s/'sources.json').read_text());title='Six-color brand board and retail card';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
a={'number':67,'title':title,'note':'Colors only; Layout retained; board label fills adapt to dark and light regions.','sources':{}}
for role,p in [('board',r/'six-color-07-back.svg'),('card',r/'output/pdf/six-color-retail-purchase-card.pdf'),('palette',r/'palette.json'),('overview',r/'six-color-overview.png')]:a['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(a);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
snippet='<article><h2>Sheet 30 — Six-color brand trial</h2><a href="sheet-30.png"><img src="sheet-30.png"></a></article>';p=s/'index.html';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';entry='\n## Six-color brand trial — 2026-09-10\n\n[Sheet 30](sheet-30.png) shows white, black, red, green, gray and beige on the board and both purchase-card faces. [Palette evidence, print PDFs and color-only checks](../six-color-brand-2026-09-10/README.md). All earlier geometry and text preserved.\n'
if entry not in p.read_text():p.write_text(p.read_text()+entry)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Six-color brand trial</title><style>body{max-width:1800px;margin:30px auto;padding:20px;font:18px system-ui}img{width:100%}a{color:#c8493f}</style><h1>Six-color brand trial</h1><p>Six-color palette with contrasting lettering. Color-only revisions of the board and purchase card.</p><img src="six-color-overview.png"><h2>Board before / after</h2><img src="board-comparison.png"><p><a href="output/pdf/six-color-retail-purchase-card.pdf">Card PDF</a> · <a href="six-color-07-back.svg">Board vector</a> · <a href="palette.json">Palette evidence</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p>')
print('Appended contact sheet 30 and artifact 67.')
