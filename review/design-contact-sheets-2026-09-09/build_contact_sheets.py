"""Faithful paired contact sheets: resize/pad existing renders, never redraw boards."""
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

OUT = Path(__file__).resolve().parent
OLD = Path('/Users/PulsesensorCorp/Documents/Codex/Imported PulseSensor Projects 2026-07-13/PulseSensor Amped Hardware')
NEW = Path('/Users/PulsesensorCorp/.codex/worktrees/2f83/PulseSensor Amped Hardware')
RC = 'PulseSensor-Amped-Rebuild/output/pcbway-release-candidates-RC3-R1-FINAL/PulseSensor-Amped-B-PCBWay-EVT-RC3-R1-FINAL'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
def font(n): return ImageFont.truetype(FONT, n)
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
items = []
def add(title, root, front, back, native, note):
    items.append(dict(number=len(items)+1,title=title,root=str(root),front=front,back=back,native=native,note=note))
def native_in(folder):
    return next((str(p.relative_to(OLD)) for p in sorted((OLD/folder).glob('*.kicad_pcb'))), None)
def public(title, suffix):
    p='Public-Online-Audit/KiCad-Public-3D-View'+suffix
    add(title,OLD,p+'/renders/front.png',p+'/renders/back.png',native_in(p),'Earlier DEVELOPMENT reference; not the submitted RC3 board')

add('Submitted PCBWay baseline · RC3 B',NEW,RC+'/REVIEW/PulseSensor-Amped-B-3D-B.png',RC+'/REVIEW/PulseSensor-Amped-B-3D-F.png',RC+'/SOURCE_SUPPORT/PulseSensor-Amped-B-JST.kicad_pcb','Submitted ZIP hash verified; CAD render, not an as-built photograph')
public('Textbook overlay','-JSTSH-Textbook-Overlay-Variant')
p='PCBWay-Fresh-Spin-2026-07-31-Isolated'
add('Counterclockwise perimeter overlay',OLD,None,p+'/Review/CCW_Overlay_3D_bottom.png',p+'/02-counterclockwise-overlay/PulseSensorAmped_Fresh_CCW_Overlay.kicad_pcb','Forensic visual reference; not fabrication-ready')
for title, folder, prefix in [
    ('DesignSpark remake','KiCad-DesignSpark-Remake','PulseSensorAmped_DesignSpark_Remake'),
    ('Original JST-SH','KiCad-Original-JSTSH','PulseSensorAmped_Original_JSTSH'),
    ('Original JST-SH · 16 mm inboard','KiCad-Original-JSTSH-16mm-inboard','PulseSensorAmped_Original_JSTSH_16mm_inboard')]:
    f=folder+'/Review/'+prefix+'_3d_front.png'; b=folder+'/Review/'+prefix+'_3d_back.png'
    add(title,OLD,f if (OLD/f).exists() else None,b if (OLD/b).exists() else None,native_in(folder),'Earlier DEVELOPMENT reference; missing views are not substituted')
public('Public cable preview','')
public('Public JST-SH preview','-JSTSH-Variant')
public('Readable back experiment','-JSTSH-Readable-Back-Experiment')
public('Routing-aware experiment','-JSTSH-Routing-Aware-Experiment')
public('Readable candidate','-JSTSH-Readable-Production-Candidate')
public('Spaced back variant','-JSTSH-Spaced-Back-Variant')
public('Spacious education variant','-JSTSH-Spacious-Education-Variant')
public('Educational candidate','-JSTSH-Educational-Production-Candidate')
for folder,title in [('iteration-00-fixed-optical-stack','Iteration 00 · optical stack'),('iteration-01-connector-label-pass','Iteration 01 · connector labels'),('iteration-02-side-pin-cues','Iteration 02 · side pin cues'),('iteration-03-visible-ground-cue','Iteration 03 · ground cue')]:
    p='Public-Online-Audit/Readable-Production-Design-Loops/'+folder
    add(title,OLD,p+'/renders/front.png',p+'/renders/back.png',native_in(p),'Earlier DEVELOPMENT reference; native source path if present')
for v in range(1,10):
    stem='pulsesensor_back_educational_layout_mockup'+('' if v==1 else '_v'+str(v)) if v<=3 else 'pulsesensor_back_clockwise_puzzle_flow_mockup_v'+str(v)
    p='Public-Online-Audit/Educational-SVG-Mockups/'+stem
    add('Educational SVG concept · v'+str(v),OLD,None,p+'.svg.png',p+'.svg','Back-only illustration; not a native board or fabrication output')

for number, roles in [(3,['front']),(5,['front','back']),(6,['front','back'])]:
    for role in roles:
        items[number-1][role]=str(OUT/'rendered-missing-views'/f'{number:02d}-{role}.png')
    items[number-1]['note']='Existing native design; missing face views rendered with KiCad, source unchanged'
items[4]['note']='Fresh native bare-board views; component models absent in this source'
items[5]['note']='Fresh native face views; incomplete model coverage (optical sensor not shown)'
heads={str(root):git(root,'rev-parse','HEAD') for root in [OLD,NEW]}
for item in items:
    root=Path(item['root']); item['source_checkout_commit']=heads[str(root)]
    item['sources']={}
    for role in ['front','back','native']:
        name=item[role]
        if name:
            p=root/name
            if not p.exists(): raise FileNotFoundError(p)
            srcroot=OUT.parents[1] if Path(name).is_absolute() else root
            rel=str(p.relative_to(srcroot))
            item['sources'][role]={'path':str(p),'repo_relative_path':rel,'sha256':digest(p),'git_status':git(srcroot,'status','--short','--untracked-files=all','--',rel) or 'clean or ignored (see tracked flag)','tracked':bool(git(srcroot,'ls-files','--',rel))}

W,H=2600,3500
for page in range(9):
    sheet=Image.new('RGB',(W,H),'#f2f1ed'); d=ImageDraw.Draw(sheet)
    d.text((65,38),'PulseSensor · existing design review',font=font(54),fill='#151817')
    d.text((65,107),f'Sheet {page+1:02d} / 09  ·  Paired optical/front + circuit/back  ·  DEVELOPMENT REFERENCES',font=font(29),fill='#444944')
    for row,item in enumerate(items[page*3:page*3+3]):
        top=185+row*1080
        d.text((65,top),f"{item['number']:02d}  {item['title']}",font=font(42),fill='#171b18')
        d.text((65,top+52),item['note'],font=font(24),fill='#4b514b')
        for col,(role,label) in enumerate([('front','OPTICAL / FRONT'),('back','CIRCUIT / BACK')]):
            x=65+col*1260
            d.text((x,top+95),label,font=font(27),fill='#202920')
            box=(x,top+140,x+1200,top+1005)
            d.rectangle(box,fill='#e2e4e0')
            if item[role]:
                im=Image.open(Path(item['root'])/item[role]).convert('RGBA')
                im=ImageOps.contain(im,(1200,865),Image.Resampling.LANCZOS)
                # Preserve transparency using a neutral background; no crop, recolor or geometry edits.
                sheet.paste(im,(x+(1200-im.width)//2,top+140+(865-im.height)//2),im)
            else:
                d.text((x+70,top+450),'No existing view in this source set',font=font(36),fill='#566056')
                d.text((x+70,top+510),'Back-only concept; no optical/front drawing',font=font(27),fill='#566056')
        d.line((65,top+1040,2535,top+1040),fill='#c3c8c1',width=2)
    d.text((65,3450),'Faithful existing renders; large screen views are not actual-size print proofs. Source index: README.md + sources.json',font=font(23),fill='#4b514b')
    sheet.save(OUT/f'sheet-{page+1:02d}.png',optimize=True)

(OUT/'sources.json').write_text(json.dumps({'classification':'DEVELOPMENT / visual review only','render_method':'Pillow contain resize and neutral padding; no crop, recoloring, redrawing or board editing','source_repositories':'WorldFamousElectronics/PulseSensorAmped_Hardware','submitted_zip_sha256':'0afda167b52ab0b0251cf22f91fd92fefa5dcf5e74f67b36446e7ec775acf792','designs':items},indent=2)+'\n')
lines=['# PulseSensor design contact sheets — 2026-09-09','','DEVELOPMENT / visual reference review only. No board design changes or fabrication release.','','27 numbered designs, paired front/back. Missing views are labeled; no different board is substituted. The nine SVG concepts are back-only illustrations. Existing renders are resized and padded faithfully, with no crop, recoloring, or reconstruction. Render colors may differ from intended manufacturing colors.','','## Contact sheets','']
for page in range(9):
    lines += [f'### Sheet {page+1:02d}: designs {page*3+1:02d}–{page*3+3:02d}',f'![Sheet {page+1:02d}](sheet-{page+1:02d}.png)','']
lines += ['## Source index','','Exact local source paths, SHA-256 hashes, source checkout revisions, tracked flags, and per-file dirty status are in [sources.json](sources.json). A checkout revision alone does not identify dirty or ignored artifacts: use the recorded file hash. Source files remain untouched.','','| No. | Design | Source folder / native file |','| --- | --- | --- |']
for i in items:
    lines.append(f"| {i['number']:02d} | {i['title']} | `{i['native'] or i['back'] or 'no native located'}` |")
lines += ['','## Submitted baseline and reuse boundaries','','Design 01 uses the render files and native supporting PCB from the submitted RC3 B archive. The local archive SHA-256 was recomputed as `0afda167b52ab0b0251cf22f91fd92fefa5dcf5e74f67b36446e7ec775acf792`; native PCB bytes were compared directly with its ZIP member. PCB SHA-256: `b439dcff82c4553731ac35ebcd27276899f8dfbbfcd35f2351d8101497eb4ad4`. This establishes archive identity, not as-built equivalence. The original manufacturing Gerbers, BOM and CPL control, rather than the supporting native file.','','The submitted RC3 design has optical/front on KiCad B and circuit/back on KiCad F. Earlier versions use different conventions; the paired labels here follow their existing optical/front and circuit/back renders.','','Textbook, educational-candidate, and counterclockwise versions demonstrate actual educational silkscreen graphics in native boards. These are block/flow illustrations, not a full component-symbol schematic. They are visual references on older electrical layouts. Their pin maps, geometry, topology and values must not replace the RC3 working baseline. The July counterclockwise folder explicitly declares itself non-authoritative and not for fabrication.','','The old white heart and website geometry is photo-reconstructed artwork, not a recovered original silkscreen export (see `Original-Review/original_logo_source_audit.md` in the source checkout). No new artwork or board changes were made for this review.','','## Reproduce','','Run `build_contact_sheets.py` using Python with Pillow. It reads the approved WFE source checkout paths defined at the top and writes only this review directory. The source hashes record the exact visual inputs used. No email content or supplier correspondence is included.','']
lines += ['## Render QA and limitations','','All nine sheets were visually reviewed. Five missing/incorrectly named face views were rendered from unchanged existing native boards using KiCad; exact commands and before/after source-hash checks are in `rendered-missing-views/render-evidence.json`. Design 05 has no component models; design 06 has incomplete optical-sensor model coverage. These are source limitations, not assembly instructions. Design 04 also has incomplete legacy model coverage. No missing parts were invented. All native sources remain byte-for-byte unchanged.','']
(OUT/'README.md').write_text('\n'.join(lines))
print(f'Created {len(items)} paired entries, 9 sheets, README and hashed source index in {OUT}')
