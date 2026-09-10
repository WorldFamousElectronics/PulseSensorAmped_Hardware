from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parent;s=r.parent/'design-contact-sheets-2026-09-09';shutil.copy2(r/'comparison.png',s/'sheet-24.png')
m=json.loads((s/'sources.json').read_text());title='Dotted module outline iteration';m['designs']=[x for x in m['designs'] if x.get('title')!=title]
a={'number':61,'title':title,'note':'New vector appearance study; color-10 and CAD retained. Puzzle tabs removed; black dots mark region boundaries.','sources':{}}
for role,name in [('back','modules-02-back.png'),('vector','modules-02-back.svg'),('comparison','comparison.png'),('source','build_modules.py')]:
 p=r/name;a['sources'][role]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m['designs'].append(a);(s/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
snippet='<article><h2>Sheet 24 — dotted module outlines</h2><a href="sheet-24.png"><img src="sheet-24.png"></a></article>';p=s/'index.html';p.write_text(p.read_text().replace(snippet,'').replace('</main>',snippet+'</main>'))
p=s/'README.md';entry='\n## Dotted module alternative — 2026-09-10\n\n[Sheet 24](sheet-24.png) compares accepted color-10 with straight solid-color functional areas with black dotted boundaries. [Vector study and revision record](../module-outlines-2026-09-10/README.md). No hardware changes.\n'
if entry not in p.read_text():p.write_text(p.read_text()+entry)
(r/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Dotted module study</title><style>body{max-width:1400px;margin:30px auto;background:#f2f1ed;font:18px system-ui;color:#152b34}img{width:100%}</style><h1>Dotted module background study</h1><p>Six colored regions with dotted black boundaries. Component positions and optical geometry preserved.</p><img src="comparison.png"><p><a href="modules-02-back.svg">Editable vector proof</a> · <a href="../design-contact-sheets-2026-09-09/index.html">Visual history</a></p>')
