from pathlib import Path
import json,hashlib,html,math,shutil
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parent;S=R.parent/'design-contact-sheets-2026-09-09';old=R.parent/'sendoff-candidate-2026-09-09';manifest=json.loads((S/'sources.json').read_text());assert len(manifest['designs'])==27,'Append once; preserve existing revisions'
items=[]
def add(title,front,back,native,note):items.append(dict(number=28+len(items),title=title,front=str(front) if front else None,back=str(back) if back else None,native=str(native) if native else None,note=note))
a=R.parent/'appearance-study-2026-09-09'
add('Corrected component teaching concept',None,a/'component-teaching-concept.png',None,'Generated concept; full functions; internal testing note removed')
add('Native feasibility study',None,a/'visual-log/07-native-current/native-review.png',None,'Earlier fixed-layout study; not the rerouted candidate')
notes={'layout-03':'Routing incomplete','layout-06':'Complete route; bias courtyard collision','layout-07':'Black-mask appearance proof','layout-08':'Bias collision resolved','layout-09':'Filter courtyard collision','layout-10':'Filter spacing resolved','layout-74':'Ground island found','layout-76':'Ground stitching fixed continuity','layout-77':'Single stitch insufficient; rejected','layout-78':'Rotated LED/input resistors; incomplete route','layout-79':'Selected copper layout','art-01':'First native educational artwork','art-02':'Fragmented copper guides; superseded','art-03':'Logical guides and LED arrow','art-04':'Narrower full-height lettering','art-05':'Labels too far from parts; rejected','art-06':'Labels restored near parts','art-07':'D1 reference separated from signal guide','art-08':'Stronger strokes and polarity clearance','candidate-01':'Matched project; first verification run','candidate-02':'Failed metadata helper checkpoint','candidate-03':'Failed metadata helper checkpoint'}
for n,note in notes.items():
 f=old/'visual-log'/(n+'.png');folder=old/n
 native=next((p for p in [folder/'PulseSensor-JST-Educational.kicad_pcb',folder/'routing-incomplete.kicad_pcb',folder/'placement-only.kicad_pcb'] if p.exists()),None)
 add(n,None,f,native,note+'; milestone back view')
add('Candidate 05 — previous selected design',old/'final-visuals/front.png',old/'final-visuals/back.png',old/'candidate-05/PulseSensor-JST-Educational.kicad_pcb','Verified electrical candidate; original 0.80 mm front x-height')
add('Mono 06 — larger front / polarity draft',R/'mono-06/front.png',R/'mono-06/back.png',R/'mono-06/PulseSensor-JST-Educational.kicad_pcb','1.35 mm front x-height; rounded heart; minus mark later widened')
add('Color 07 — first power-net print proof',None,R/'color-07/back.png',R/'color-07/PulseSensor-JST-Educational.kicad_pcb','CAD vector positioning proof; not photorealistic')
add('Mono 08 — selected monochrome',R/'mono-08/front.png',R/'mono-08/back.png',R/'mono-08/PulseSensor-JST-Educational.kicad_pcb','Larger front, rounded tip and clear + / minus marks')
add('Color 09 — selected PCBWay UV iteration',R/'color-09/front.png',R/'color-09/back.png',R/'color-09/PulseSensor-JST-Educational.kicad_pcb','Front: KiCad render. Back: CAD vector color-positioning proof')
# Neutral letterboxing only; do not redraw the source views.
font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
newpages=[]
for page in range(math.ceil(len(items)/3)):
 num=10+page;im=Image.new('RGB',(2600,3500),'#f2f1ed');d=ImageDraw.Draw(im);d.text((65,38),'PulseSensor · design iteration trail',font=font(54),fill='#151817');d.text((65,107),f'Sheet {num:02d} · Append-only revisions · DEVELOPMENT / REVIEW',font=font(29),fill='#444944')
 for row,it in enumerate(items[page*3:page*3+3]):
  y=185+row*1080;d.text((65,y),f"{it['number']:02d}  {it['title']}",font=font(40),fill='#171b18');d.text((65,y+52),it['note'],font=font(25),fill='#4b514b')
  for col,role in enumerate(['front','back']):
   x=65+1260*col;d.text((x,y+95),'OPTICAL / FRONT' if role=='front' else 'CIRCUIT / BACK',font=font(27),fill='#202920');d.rectangle((x,y+140,x+1200,y+1005),fill='#d9dedc')
   if it[role]:
    p=Path(it[role]);assert p.exists(),p;pic=ImageOps.contain(Image.open(p).convert('RGBA'),(1200,865),Image.Resampling.LANCZOS);im.paste(pic,(x+(1200-pic.width)//2,y+140+(865-pic.height)//2),pic)
   else:d.text((x+75,y+450),'No separate view retained for this face',font=font(34),fill='#566056')
  d.line((65,y+1040,2535,y+1040),fill='#c3c8c1',width=2)
 d.text((65,3450),'Enlarged visual proofs, not actual-size printing. Exact image and native hashes: sources.json',font=font(24),fill='#4b514b');f=S/f'sheet-{num:02d}.png';assert not f.exists();im.save(f,optimize=True);newpages.append(f.name)
for it in items:
 it['sources']={}
 for role in ['front','back','native']:
  if it[role]:
   p=Path(it[role]);it['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest['designs']+=items;manifest['append_2026_09_09']={'new_sheets':newpages,'notes':'Prior sheets 01–09 unchanged. The full routing-attempt ledger remains in sendoff-candidate visual-log. Some source images are local retained checkpoints.','selected_monochrome':'mono-08','selected_color':'color-09'}
(S/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
with (S/'README.md').open('a') as f:
 f.write('\n## Added artwork, routing and power/color revisions\n\nOriginal sheets 01–09 remain unchanged. This appendix adds corrected teaching artwork, retained native routing/artwork milestones, and the enlarged-front / color-print candidates. Metadata-helper failures are explicitly labeled. All partial routing checkpoints remain linked in the local visual ledger.\n\n')
 for name in newpages:f.write(f'[{name}]({name})\n\n')
 f.write('[Current review](../power-color-2026-09-09/review.html) · [All routing attempts and native revision history](../sendoff-candidate-2026-09-09/visual-log/index.html)\n')
allpages=[f'sheet-{i:02d}.png' for i in range(1,10)]+newpages
page='<!doctype html><meta charset="utf-8"><title>PulseSensor contact sheets</title><style>body{font:18px system-ui;background:#172126;color:#eee;margin:35px}a{color:#7ddcca}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}img{width:100%}article{padding:16px;background:#26343b}</style><h1>PulseSensor visual contact sheets</h1><p>Original sheets preserved; new revisions appended. Click a sheet to inspect at full resolution.</p><p><a href="../power-color-2026-09-09/review.html">Current monochrome and color review</a> · <a href="sources.json">Exact source index</a> · <a href="../sendoff-candidate-2026-09-09/visual-log/index.html">Every routing attempt</a></p><main>'+''.join(f'<article><h2>Sheet {i+1:02d}</h2><a href="{n}"><img loading="lazy" src="{n}"></a></article>' for i,n in enumerate(allpages))+'</main>'
(S/'index.html').write_text(page)
(R/'contact-sheet-append.json').write_text(json.dumps({'design_count':len(manifest['designs']),'added_design_count':len(items),'new_sheets':newpages},indent=2))
print('Added',len(items),'designs;',len(newpages),'sheets. Last sheet:',newpages[-1])
