from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09';im=Image.new('RGB',(2600,1590),'#f2f1ed');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((65,40),'PulseSensor · 4 × 4 inch hardware postcard',font=font(54),fill='#152b34');d.text((65,111),'Sheet 21 · Packaging insert · PCB + schematic + reference BOM · Both faces shown enlarged',font=font(28),fill='#53666d')
for col,(name,p) in enumerate([('FACE A / PCB + PARTS',r/'output/card-1.png'),('FACE B / SCHEMATIC',r/'output/card-2.png')]):
 x=65+1260*col;d.text((x,178),name,font=font(30),fill='#152b34');pic=ImageOps.contain(Image.open(p).convert('RGB'),(1200,1200),Image.Resampling.LANCZOS);im.paste(pic,(x,230))
d.text((65,1495),'Hardware-only. Exact PCB artwork; vector schematic and text. Board back milestone preserved; front art deferred.',font=font(26),fill='#53666d')
im.save(s/'sheet-21.png',optimize=True);im.save(r/'output/postcard-preview.png',optimize=True)
m=json.loads((s/'sources.json').read_text());m['designs']=[it for it in m['designs'] if it.get('title')!='4-inch hardware postcard with BOM']
item={'number':58,'title':'4-inch hardware postcard with BOM','note':'Two packaging faces, not PCB faces. Native PCB artwork unchanged.','sources':{}}
for role,p in [('face_a',r/'output/card-1.png'),('face_b',r/'output/card-2.png'),('pdf',r/'output/PulseSensor-4x4-card.pdf'),('editable_source',r/'build_postcard.py')]:item['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(item);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
p=s/'index.html';p.write_text(p.read_text().replace('<article><h2>Sheet 21 — hardware postcard + BOM</h2><a href="sheet-21.png"><img src="sheet-21.png"></a></article>','').replace('</main>','<article><h2>Sheet 21 — hardware postcard + BOM</h2><a href="sheet-21.png"><img src="sheet-21.png"></a></article></main>'))
with (s/'README.md').open('a') as f:f.write('\n## Packaging postcard milestone — 2026-09-10\n\n[Sheet 21](sheet-21.png) shows both 4-inch insert faces: PCB/reference BOM and matching schematic. [Print files and source](../postcard-insert-2026-09-10/README.md). The color-10 board back is accepted as a major milestone; front board graphics are deferred. No hardware geometry changed.\n')
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>PulseSensor hardware insert</title><style>body{font:18px/1.5 system-ui;max-width:1250px;margin:30px auto;padding:20px;background:#f6f2e9;color:#102d38}img{width:100%}a{color:#6342a8}</style><h1>PulseSensor hardware insert</h1><p>Two 4 × 4 inch faces: PCB, schematic, reference BOM and TL;DR.</p><img src="output/postcard-preview.png"><p><a href="output/PulseSensor-4x4-card.pdf">4-inch PDF</a> · <a href="output/PulseSensor-4x4-card-bleed.pdf">PDF with bleed</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p>')
print('Appended postcard to sheet 21; 58 indexed designs/artifacts.')
