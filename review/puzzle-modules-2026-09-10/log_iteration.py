from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09';shutil.copy2(r/'comparison.png',s/'sheet-23.png')
m=json.loads((s/'sources.json').read_text());title='Puzzle module background iteration';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
a={'number':60,'title':title,'note':'New vector appearance study; color-10 and CAD retained. Six functional regions replace trace overlays.','sources':{}}
for role,name in [('back','puzzle-01-back.png'),('vector','puzzle-01-back.svg'),('comparison','comparison.png'),('source','build_puzzle.py')]:
 p=r/name;a['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(a);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
snippet='<article><h2>Sheet 23 — puzzle module background</h2><a href="sheet-23.png"><img src="sheet-23.png"></a></article>';p=s/'index.html';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';entry='\n## Puzzle module alternative — 2026-09-10\n\n[Sheet 23](sheet-23.png) compares accepted color-10 with interlocking solid-color functional areas. [Vector study and revision record](../puzzle-modules-2026-09-10/README.md). No hardware changes.\n'
if entry not in p.read_text():p.write_text(p.read_text()+entry)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Puzzle module study</title><style>body{max-width:1400px;margin:30px auto;background:#f2f1ed;font:18px system-ui;color:#152b34}img{width:100%}</style><h1>Puzzle module background study</h1><p>Six interlocking functional regions. Component positions and optical geometry preserved.</p><img src="comparison.png"><p><a href="puzzle-01-back.svg">Editable vector proof</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p><h2>First fit, preserved before guide-remnant cleanup</h2><img src="iterations/01-first-fit/back.png">')
