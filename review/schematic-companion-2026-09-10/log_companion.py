from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09'
im=Image.new('RGB',(2600,1590),'#f2f1ed');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((65,40),'PulseSensor · Complete schematic companion',font=font(54),fill='#152b34')
d.text((65,111),'Sheet 22 · Separate 4 × 4 inch postcard · Packaging faces, not PCB faces',font=font(28),fill='#53666d')
for col,(name,p) in enumerate([('FACE A / COMPLETE SCHEMATIC',r/'output/card-1.png'),('FACE B / READING GUIDE',r/'output/card-2.png')]):
 x=65+1260*col;d.text((x,178),name,font=font(30),fill='#152b34');pic=ImageOps.contain(Image.open(p).convert('RGB'),(1200,1200),Image.Resampling.LANCZOS);im.paste(pic,(x,230))
d.text((65,1495),'All 16 parts · Explicit chip / connector pins · Matching wire labels · Complements card 01 PCB + BOM',font=font(26),fill='#53666d')
im.save(s/'sheet-22.png',optimize=True);im.save(r/'output/companion-preview.png',optimize=True)
m=json.loads((s/'sources.json').read_text());title='Complete schematic companion postcard';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
item={'number':59,'title':title,'note':'Separate packaging card; complete circuit and reading guide. Original PCB/BOM card retained.','sources':{}}
for role,p in [('face_a',r/'output/card-1.png'),('face_b',r/'output/card-2.png'),('pdf',r/'output/pdf/PulseSensor-complete-schematic-4x4.pdf'),('editable_source',r/'build_companion.py')]:item['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(item);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
p=s/'index.html';snippet='<article><h2>Sheet 22 — complete schematic companion postcard</h2><a href="sheet-22.png"><img src="sheet-22.png"></a></article>';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';section='\n## Complete schematic companion — 2026-09-10\n\n[Sheet 22](sheet-22.png) adds a separate 4-inch card with the complete circuit and a six-part reading guide. [Print files, source and preserved draft](../schematic-companion-2026-09-10/README.md). The first PCB/BOM card and all hardware remain unchanged.\n'
if section not in p.read_text():p.write_text(p.read_text()+section)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Complete schematic companion</title><style>body{font:18px/1.5 system-ui;max-width:1250px;margin:30px auto;padding:20px;background:#f6f2e9;color:#102d38}img{width:100%}a{color:#6342a8}</style><h1>Complete schematic companion</h1><p>A separate 4 × 4 inch postcard to accompany the PCB and BOM card.</p><img src="output/companion-preview.png"><p><a href="output/pdf/PulseSensor-complete-schematic-4x4.pdf">4-inch PDF</a> · <a href="output/pdf/PulseSensor-complete-schematic-4x4-bleed.pdf">PDF with bleed</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p><h2>First layout proof, preserved</h2><img src="iterations/01-complete-schematic/face-a.png"><img src="iterations/01-complete-schematic/face-b.png">')
print('Appended sheet 22 and artifact 59; earlier sheets preserved.')
