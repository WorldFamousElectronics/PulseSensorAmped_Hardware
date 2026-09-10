from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09'
im=Image.new('RGB',(2600,1590),'#f2f1ed');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((65,40),'PulseSensor · Full-color full schematic retail purchase card',font=font(45),fill='#152b34')
d.text((65,111),'Sheet 25 · 1960s assembly-guide treatment · Packaging faces, not PCB faces',font=font(28),fill='#53666d')
for col,(name,p) in enumerate([('FACE A / CONTINUOUS SCHEMATIC',r/'output/card-1.png'),('FACE B / PARTS SCHEDULE',r/'output/card-2.png')]):
 x=65+1260*col;d.text((x,178),name,font=font(30),fill='#152b34');pic=ImageOps.contain(Image.open(p).convert('RGB'),(1200,1200),Image.Resampling.LANCZOS);im.paste(pic,(x,230))
d.text((65,1495),'Continuous signal path · Six color tints · Black vector schematic · Parts schedule on reverse',font=font(26),fill='#53666d')
im.save(s/'sheet-25.png',optimize=True);im.save(r/'output/retail-card-preview.png',optimize=True)
m=json.loads((s/'sources.json').read_text());title='Full-color full schematic retail purchase card';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
item={'number':62,'title':title,'note':'Separate packaging card; continuous circuit and parts schedule. Original PCB/BOM card retained.','sources':{}}
for role,p in [('face_a',r/'output/card-1.png'),('face_b',r/'output/card-2.png'),('pdf',r/'output/pdf/full-color-full-schematic-retail-purchase-card.pdf'),('editable_source',r/'build_card.py')]:item['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(item);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
p=s/'index.html';snippet='<article><h2>Sheet 25 — full-color retail schematic card</h2><a href="sheet-25.png"><img src="sheet-25.png"></a></article>';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';section='\n## Full-color full schematic retail purchase card — 2026-09-10\n\n[Sheet 25](sheet-25.png) adds a separate 4-inch card with the complete circuit and a parts schedule. [Print files, source and preserved draft](../full-color-retail-card-2026-09-10/README.md). The first PCB/BOM card and all hardware remain unchanged.\n'
if section not in p.read_text():p.write_text(p.read_text()+section)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Full-color full schematic retail purchase card</title><style>body{font:18px/1.5 system-ui;max-width:1250px;margin:30px auto;padding:20px;background:#f6f2e9;color:#102d38}img{width:100%}a{color:#6342a8}</style><h1>Full-color full schematic retail purchase card</h1><p>A separate 4 × 4 inch postcard to accompany the PCB and BOM card.</p><img src="output/retail-card-preview.png"><p><a href="output/pdf/full-color-full-schematic-retail-purchase-card.pdf">4-inch PDF</a> · <a href="output/pdf/full-color-full-schematic-retail-purchase-card-bleed.pdf">PDF with bleed</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p><h2>First layout proof, preserved</h2><img src="iterations/01-layout/face-a.png"><img src="iterations/01-layout/face-b.png">')
print('Appended sheet 25 and artifact 62; earlier sheets preserved.')
