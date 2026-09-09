from pathlib import Path
import shutil,json,hashlib,zipfile
r=Path(__file__).resolve().parent
for name,zipname in [('mono-08','PulseSensor-Mono08-Review.zip'),('color-10','PulseSensor-Color10-PCBWay-Review.zip')]:
 p=r/(name+'-package');src=r/name
 assert (p/'SOURCE/PulseSensor-JST-Educational.kicad_pcb').read_bytes()==(src/'PulseSensor-JST-Educational.kicad_pcb').read_bytes()
 for fn in ['README.md','SUPPLIERS.md']:shutil.copy2(r/fn,p/fn)
 shutil.copy2(r/'verification.json',p/'VALIDATION/verification.json')
 erc=json.loads((p/'VALIDATION/erc.json').read_text());assert not any(s.get('violations') for s in erc.get('sheets',[]))
 shutil.copy2(r/'mono-08/front.png',p/'REVIEW/intended-optical-front.png');shutil.copy2(src/'back.png',p/'REVIEW/back.png')
 if name=='color-10':
  uv=p/'UV_PRINT';uv.mkdir(exist_ok=True)
  for n in ['F-color-print.pdf','F-color-print.png','F-color-print.svg','back-positioning.svg','back.png','net-path-source.json','print-clearance.json']:shutil.copy2(src/n,uv/n)
  shutil.copy2(src/'front.png',p/'REVIEW/native-mixed-mask-render-limitation.png')
  (uv/'READ-FIRST.txt').write_text('REVIEW ONLY — supplier process proof and release approval pending.\nF is circuit BACK. B is optical FRONT.\nPrint only F with supplied F-color-print artwork. PDF page and SVG/PNG art square: 15.875 x 15.875 mm. Center 100,100 in native CAD. Gerber/drill/CPL origin remains 92.0625,107.9375.\nF-color-print has no component bodies; back.png and back-positioning.svg are ALIGNMENT REFERENCES ONLY, NOT PRINT FILES.\nThe ordinary F silkscreen Gerber is a position reference. Replace its white print with supplied UV artwork: do not add a second white overprint. B silkscreen remains conventional white.\nRequested F mask: white plus dark UV background. Requested B mask: black. Confirm mixed-side mask/process compatibility before manufacture. Do not change optical openings.\nNo ink on solder openings. No copper exposure. Confirm registration, smallest printable UV features and RGB color conversion via supplier proof.\nIntended optical front shares mono-08 B geometry and mask; the retained native mixed-mask preview does not correctly display the requested black optical mask.\n')
 else:shutil.copy2(src/'artwork-clearance.json',p/'VALIDATION/artwork-clearance.json')
 manifest={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file() and f.name!='SHA256.json'}
 (p/'SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
 with zipfile.ZipFile(r/zipname,'w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(p.rglob('*')):
   if f.is_file():z.write(f,Path(name+'-REVIEW')/f.relative_to(p))
 with zipfile.ZipFile(r/zipname) as z:assert z.testzip() is None
 print(zipname,len(manifest),'files; source identity and ERC passed; ZIP verified')
(r/'contact-sheet-append.json').write_text(json.dumps({'design_count':57,'added_design_count':30,'new_sheets':[f'sheet-{n:02d}.png' for n in range(10,21)],'selected_monochrome':'mono-08','selected_color':'color-10'},indent=2)+'\n')
