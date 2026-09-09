"""Build a reversible native silkscreen study from the submitted JST board.
Run with KiCad's bundled Python. Electrical items are never edited.
"""
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
import pcbnew as k

ROOT = Path(__file__).resolve().parent
REBUILD = Path('/Users/PulsesensorCorp/.codex/worktrees/2f83/PulseSensor Amped Hardware/PulseSensor-Amped-Rebuild')
SOURCE = REBUILD / 'output/pcbway-release-candidates-RC3-R1-FINAL/PulseSensor-Amped-B-PCBWay-EVT-RC3-R1-FINAL/SOURCE_SUPPORT/PulseSensor-Amped-B-JST.kicad_pcb'
ART = Path('/Users/PulsesensorCorp/Documents/Codex/Imported PulseSensor Projects 2026-07-13/PulseSensor Amped Hardware/Public-Online-Audit/KiCad-Public-3D-View-JSTSH-Variant/PulseSensorAmped_Public_Online_3D_View_JSTSH_Variant.kicad_pcb')
OUT = ROOT / 'native'
OUT.mkdir(exist_ok=True)
# Preserve existing native outputs before any rebuild, including rendered views.
# Full local history may contain superseded internal concepts; do not publish it.
if (OUT/'PulseSensor-JST-Educational-Study.kicad_pcb').exists():
    snapshot=ROOT/'visual-log'/'native-snapshots'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copytree(OUT,snapshot)
    shutil.copy2(__file__,snapshot/'builder-at-next-run.py')
board = k.LoadBoard(str(SOURCE))
def xy(v): return [v.x, v.y]
def electrical(b):
    return {
        'footprints': sorted([{'ref': f.GetReference(), 'value': f.GetValue(), 'pos': xy(f.GetPosition()), 'angle': f.GetOrientationDegrees(), 'layer': f.GetLayer(), 'pads': sorted([(p.GetNumber(), p.GetNetname(), xy(p.GetPosition()), xy(p.GetSize()), xy(p.GetDrillSize()), p.GetLayerSet().FmtHex()) for p in f.Pads()])} for f in b.GetFootprints()], key=lambda f:f['ref']),
        'tracks': sorted([(t.GetClass(), t.GetNetname(), xy(t.GetStart()), xy(t.GetEnd()), t.GetWidth(k.F_Cu) if isinstance(t,k.PCB_VIA) else t.GetWidth(), t.GetLayer(), t.GetDrillValue() if isinstance(t,k.PCB_VIA) else 0) for t in b.GetTracks()]),
        'zones': [(z.GetNetname(),z.GetLayer(),z.GetNumCorners()) for z in b.Zones()],
        'edges': [(d.GetShapeStr(), xy(d.GetStart()), xy(d.GetEnd()), d.GetWidth()) for d in b.GetDrawings() if d.GetLayer()==k.Edge_Cuts]
    }
before=electrical(board)
for d in list(board.GetDrawings()):
    if d.GetLayer() in (k.F_SilkS,k.B_SilkS): d.SetLayer(k.Dwgs_User)
# Reuse the existing photo-reconstructed artwork, never another board's parts.
art=k.LoadBoard(str(ART))
for d in art.GetDrawings():
    if d.GetLayer()==k.F_SilkS:
        clone=d.Duplicate()
        clone.Flip(k.VECTOR2I(k.FromMM(100),k.FromMM(100)),False)
        if isinstance(clone,k.PCB_SHAPE):
            # Knock ink out around the actual fixed optical aperture and sensor.
            cuts=k.SHAPE_POLY_SET()
            cuts.NewOutline()
            for i in range(96):
                a=2*math.pi*i/96
                cuts.Append(k.FromMM(100+1.16*math.cos(a)),k.FromMM(99.6063+1.16*math.sin(a)))
            cuts.NewOutline()
            for x,y in [(98.9127,100.9669),(101.1127,100.9669),(101.1127,102.7669),(98.9127,102.7669)]:
                cuts.Append(k.FromMM(x),k.FromMM(y))
            for f in board.GetFootprints():
                for graphic in f.GraphicalItems():
                    if graphic.GetLayer()!=k.B_SilkS:continue
                    box=graphic.GetBoundingBox();cuts.NewOutline()
                    for x,y in [(box.GetLeft()/1e6-.1,box.GetTop()/1e6-.1),(box.GetRight()/1e6+.1,box.GetTop()/1e6-.1),(box.GetRight()/1e6+.1,box.GetBottom()/1e6+.1),(box.GetLeft()/1e6-.1,box.GetBottom()/1e6+.1)]:cuts.Append(k.FromMM(x),k.FromMM(y))
            poly=clone.GetPolyShape();poly.BooleanSubtract(cuts);poly.Fracture()
            for index in range(poly.OutlineCount()):
                part=k.SHAPE_POLY_SET();part.AddOutline(poly.COutline(index))
                shape=k.PCB_SHAPE(board);shape.SetShape(k.SHAPE_T_POLY);shape.SetLayer(k.B_SilkS);shape.SetFilled(True);shape.SetWidth(0);shape.SetPolyShape(part);board.Add(shape)
            continue
        if isinstance(clone,k.PCB_TEXT):
            clone.SetTextAngle(k.EDA_ANGLE(-d.GetTextAngle().AsDegrees(),k.DEGREES_T))
        board.Add(clone)

def text(s,x,y,size=.5):
    t=k.PCB_TEXT(board);t.SetText(s);t.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)))
    t.SetTextSize(k.VECTOR2I(k.FromMM(size),k.FromMM(size)))
    t.SetTextThickness(k.FromMM(.1));t.SetLayer(k.F_SilkS);board.Add(t)
    return t

# Place compact two-line labels in real free space around each component.
body_boxes=[]
for f in board.GetFootprints():
    if f.GetLayer()!=k.F_Cu:continue
    boxes=[p.GetBoundingBox() for p in f.Pads()]
    if boxes:body_boxes.append((min(b.GetLeft() for b in boxes)/1e6-.1,min(b.GetTop() for b in boxes)/1e6-.1,max(b.GetRight() for b in boxes)/1e6+.1,max(b.GetBottom() for b in boxes)/1e6+.1))
for t in board.GetTracks():
    if isinstance(t,k.PCB_VIA):
        x,y=[n/1e6 for n in xy(t.GetPosition())];body_boxes.append((x-.28,y-.28,x+.28,y+.28))
for f in board.GetFootprints():
    for graphic in f.GraphicalItems():
        if graphic.GetLayer()!=k.F_SilkS:continue
        b=graphic.GetBoundingBox();body_boxes.append((b.GetLeft()/1e6-.08,b.GetTop()/1e6-.08,b.GetRight()/1e6+.08,b.GetBottom()/1e6+.08))
placed=[]
def fits(t):
    box=t.GetBoundingBox();a,b,c,d=box.GetLeft()/1e6,box.GetTop()/1e6,box.GetRight()/1e6,box.GetBottom()/1e6
    if any(math.hypot(x-100,y-100)>7.75 for x in (a,c) for y in (b,d)):return False
    return all(c+.02<aa or a-.02>cc or d+.02<bb or b-.02>dd for aa,bb,cc,dd in body_boxes+placed)
roles={'U2':'AMP','D2':'PROTECT','C1':'FILTER','C5':'PWR','R1':'LED I','R2':'SENSE','C2':'COUPLE','D1':'LIGHT','R4':'BIAS','R5':'GAIN','C4':'FILTER','R3':'BIAS','C3':'COUPLE','R6':'FB','J1':'OUT'}
for ref in ['U2','D1','J1','R1','R2','C2','C3','C1','C5','D2','R6','R4','R5','C4','R3']:
    f=next(f for f in board.GetFootprints() if f.GetReference()==ref)
    x,y=[v/1e6 for v in xy(f.GetPosition())]
    t=text(ref,x,y,.45)
    options=sorted(((x+dx*.2,y+dy*.2) for dx in range(-24,25) for dy in range(-24,25)),key=lambda p:math.dist(p,(x,y)))
    found=False
    for wording in [ref]:
        t.SetText(wording)
        for px,py in options:
            t.SetPosition(k.VECTOR2I(k.FromMM(px),k.FromMM(py)))
            if fits(t):found=True;break
        if found:break
    if not found:raise RuntimeError('No free text position for '+ref)
    print(ref,k.ToMM(t.GetPosition()),k.ToMM(t.GetBoundingBox().GetSize()))
    b=t.GetBoundingBox();placed.append((b.GetLeft()/1e6,b.GetTop()/1e6,b.GetRight()/1e6,b.GetBottom()/1e6))

# Add functional words only where a real free patch remains.
for word,x,y in [('LED',100,97.5),('AMP',100,96.8),('OUT',104,104),('SENSE',95,102),('FILTER',102,97.3)]:
    t=text(word,x,y,.45);found=False
    opts=sorted(((x+dx*.15,y+dy*.15) for dx in range(-12,13) for dy in range(-12,13)),key=lambda p:math.dist(p,(x,y)))
    for px,py in opts:
        t.SetPosition(k.VECTOR2I(k.FromMM(px),k.FromMM(py)))
        if fits(t):found=True;break
    if found:
        b=t.GetBoundingBox();placed.append((b.GetLeft()/1e6,b.GetTop()/1e6,b.GetRight()/1e6,b.GetBottom()/1e6))
    else:t.SetLayer(k.Dwgs_User)

# Reproduce actual routed signal-net centerlines in white dashed silk.
# Clip every stroke against all exposed pads and component bodies.
obstacles=list(body_boxes)
for f in board.GetFootprints():
    if f.GetLayer()!=k.F_Cu: continue
    pads=list(f.Pads())
    boxes=[p.GetBoundingBox() for p in pads]
    if boxes:
        obstacles.append((min(b.GetLeft() for b in boxes)/1e6-.18,min(b.GetTop() for b in boxes)/1e6-.18,max(b.GetRight() for b in boxes)/1e6+.18,max(b.GetBottom() for b in boxes)/1e6+.18))
for f in board.GetFootprints():
    for p in f.Pads():
        if p.IsOnLayer(k.F_Mask):
            b=p.GetBoundingBox();obstacles.append((b.GetLeft()/1e6-.18,b.GetTop()/1e6-.18,b.GetRight()/1e6+.18,b.GetBottom()/1e6+.18))
for d in board.GetDrawings():
    if d.GetLayer()==k.F_SilkS and isinstance(d,k.PCB_TEXT):
        b=d.GetBoundingBox();obstacles.append((b.GetLeft()/1e6-.12,b.GetTop()/1e6-.12,b.GetRight()/1e6+.12,b.GetBottom()/1e6+.12))
def free(x,y):return all(not(a<=x<=c and b<=y<=d) for a,b,c,d in obstacles) and math.hypot(x-100,y-100)<7.65
def line(a,b,width=.1):
    d=k.PCB_SHAPE(board);d.SetShape(k.SHAPE_T_SEGMENT);d.SetStart(k.VECTOR2I(k.FromMM(a[0]),k.FromMM(a[1])));d.SetEnd(k.VECTOR2I(k.FromMM(b[0]),k.FromMM(b[1])));d.SetWidth(k.FromMM(width));d.SetLayer(k.F_SilkS);board.Add(d)
selected={'U1_IOUT','FILTER_STAGE_1','FILTER_STAGE_2','AMP_INVERTING','SIGNAL','LED_K'}
# Leave a visible break at crossings of different projected nets.
crossings=[]
tracks=[t for t in board.GetTracks() if not isinstance(t,k.PCB_VIA) and t.GetNetname() in selected]
for i,t in enumerate(tracks):
    a=[v/1e6 for v in xy(t.GetStart())];b=[v/1e6 for v in xy(t.GetEnd())]
    for u in tracks[i+1:]:
        if u.GetNetname()==t.GetNetname():continue
        c=[v/1e6 for v in xy(u.GetStart())];d=[v/1e6 for v in xy(u.GetEnd())]
        r=(b[0]-a[0],b[1]-a[1]);v=(d[0]-c[0],d[1]-c[1]);den=r[0]*v[1]-r[1]*v[0]
        if abs(den)<1e-8:continue
        q=(c[0]-a[0],c[1]-a[1]);f=(q[0]*v[1]-q[1]*v[0])/den;g=(q[0]*r[1]-q[1]*r[0])/den
        if 0<=f<=1 and 0<=g<=1:crossings.append((a[0]+f*r[0],a[1]+f*r[1]))
stroke_count=0
for t in list(board.GetTracks()):
    if isinstance(t,k.PCB_VIA) or t.GetNetname() not in selected:continue
    a=[n/1e6 for n in xy(t.GetStart())];b=[n/1e6 for n in xy(t.GetEnd())]
    length=math.dist(a,b)
    if length<.12:continue
    n=max(1,int(length/.32))
    for i in range(n):
        p=[a[j]+(b[j]-a[j])*i/n for j in (0,1)]
        q=[a[j]+(b[j]-a[j])*min(1,(i+.48)/n) for j in (0,1)]
        if all(free(p[0]+(q[0]-p[0])*u,p[1]+(q[1]-p[1])*u) and all(math.dist((p[0]+(q[0]-p[0])*u,p[1]+(q[1]-p[1])*u),cross)>.22 for cross in crossings) for u in (0,.5,1)):
            line(p,q);stroke_count+=1

# A conventional-current arrow on the actual LED cathode route (toward R1).
for a,b in [((96.3,99.6),(95.9,99.6)),((95.9,99.6),(96.08,99.43)),((95.9,99.6),(96.08,99.77))]:
    if all(free(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u) for u in (0,.5,1)):line(a,b)

# Full explanatory schematic in native CAD on User.1, outside the physical PCB.
# It provides readable context without pretending paragraph text fits on 16 mm.
def note(s,x,y,size=.9):
    t=text(s,x,y,size);t.SetLayer(k.User_1);t.SetTextThickness(k.FromMM(.12));return t
def wire(points):
    for a,b in zip(points,points[1:]):
        d=k.PCB_SHAPE(board);d.SetShape(k.SHAPE_T_SEGMENT);d.SetStart(k.VECTOR2I(k.FromMM(a[0]),k.FromMM(a[1])));d.SetEnd(k.VECTOR2I(k.FromMM(b[0]),k.FromMM(b[1])));d.SetWidth(k.FromMM(.15));d.SetLayer(k.User_1);board.Add(d)
def resistor(ref,x,y,vertical=False):
    if vertical:
        wire([(x,y-3),(x,y-1.5),(x-.7,y-1.5),(x-.7,y+1.5),(x+.7,y+1.5),(x+.7,y-1.5),(x,y-1.5)]);wire([(x,y+1.5),(x,y+3)]);note(ref,x+4.3,y,.7)
    else:
        wire([(x-3,y),(x-1.5,y),(x-1.5,y-.7),(x+1.5,y-.7),(x+1.5,y+.7),(x-1.5,y+.7),(x-1.5,y)]);wire([(x+1.5,y),(x+3,y)]);note(ref,x,y-2,.7)
def cap(ref,x,y,vertical=False):
    if vertical:
        wire([(x,y-3),(x,y-.5)]);wire([(x-1.1,y-.5),(x+1.1,y-.5)]);wire([(x-1.1,y+.5),(x+1.1,y+.5)]);wire([(x,y+.5),(x,y+3)]);note(ref,x+4.3,y,.7)
    else:
        wire([(x-3,y),(x-.5,y)]);wire([(x-.5,y-1.1),(x-.5,y+1.1)]);wire([(x+.5,y-1.1),(x+.5,y+1.1)]);wire([(x+.5,y),(x+3,y)]);note(ref,x,y-2,.7)
def ground(x,y):
    wire([(x,y),(x,y+1)]);wire([(x-1.1,y+1),(x+1.1,y+1)]);wire([(x-.7,y+1.5),(x+.7,y+1.5)]);wire([(x-.3,y+2),(x+.3,y+2)])
note('HOW THE CIRCUIT WORKS',149,85,1.5)
note('Native teaching drawing - common net names connect repeated labels',149,88,.75)
note('LIGHT: conventional current',138,92,1)
note('+V',121,98);wire([(123,98),(128,98)])
wire([(128,97),(128,99),(131,98),(128,97)]);wire([(131,96.8),(131,99.2)]);wire([(131,98),(137,98)])
note('D1 GREEN LED',130,95,.8);resistor('R1 current limit',140,98);wire([(143,98),(151,98)]);ground(151,98)
wire([(134,100.5),(136,100.5),(135.3,100)]);note('current',135,102,.65)
note('SIGNAL: changing light becomes a changing voltage',148,105,1)
note('U1 LIGHT SENSOR',123,111,.8);note('front optical window',123,113,.65)
wire([(124,116),(132,116),(133,116)])
resistor('R2 12k',129,121,True);wire([(129,116),(129,118)]);ground(129,124)
cap('C2 4.7u',136,116);wire([(139,116),(147,116)])
cap('C1 4.7u',142,121,True);wire([(142,116),(142,118)]);ground(142,124)
cap('C3 4.7u',150,116);wire([(153,116),(160,116)])
cap('C4 2.2u',156,121,True);wire([(156,116),(156,118)]);note('VREF',156,125,.7)
resistor('R5 10k',163,116);wire([(166,116),(171,116)])
wire([(171,113),(171,122),(178,117.5),(171,113)]);note('-',172,116,.8);note('+',172,120,.8);note('U2 AMP',175,111,.8)
wire([(169,120),(171,120)]);note('VREF',168,122,.7)
wire([(178,117.5),(183,117.5)]);note('SIGNAL',185,114,.8);note('to J1 pin 3',183,120,.65)
wire([(168,116),(168,108),(172,108)]);resistor('R6 3.3M',175,108);wire([(178,108),(181,108),(181,117.5)])
note('BIAS REFERENCE',131,133,1);note('+V',121,138,.8);wire([(123,138),(126,138)]);resistor('R4 100k',129,138);wire([(132,138),(139,138)]);resistor('R3 100k',142,138);ground(145,138);note('VREF',135,136,.8)
note('SUPPLY',157,133,1);note('+V -> D2 Schottky -> protected supply',166,137,.8);note('Protected supply powers U1 and U2',166,139,.7);note('C5 2.2u: +V to GND, supply smoothing',166,142,.7)
note('J1: pin 1 GND | pin 2 +V | pin 3 SIGNAL',151,148,.9)
note('Dashed board ink follows routed signal nets. Capacitors carry changing signals, not steady DC.',151,152,.7)
note('LED location, optical window, all components and copper remain fixed in this study.',151,155,.7)

dest=OUT/'PulseSensor-JST-Educational-Study.kicad_pcb'
k.SaveBoard(str(dest),board)
assert electrical(k.LoadBoard(str(dest)))==before,'Electrical or placement change'
models=OUT/'3dmodels';models.mkdir(exist_ok=True)
for name in ('NSR05F40NXT5G.wrl','APDS-9008-020.wrl','AM2520ZGC09.wrl'):
    shutil.copy2(SOURCE.parent/'3dmodels'/name,models/name)
for suffix in ('.kicad_pro','.kicad_dru'):
    shutil.copy2(SOURCE.with_suffix(suffix),dest.with_suffix(suffix))
for name in ('fp-lib-table','sym-lib-table','PulseSensor_Amped.kicad_sym'):
    shutil.copy2(SOURCE.parent/name,OUT/name)
shutil.copytree(SOURCE.parent/'PulseSensor_Amped.pretty',OUT/'PulseSensor_Amped.pretty',dirs_exist_ok=True)
evidence={'classification':'DEVELOPMENT','status':'REVISE — artwork study; not fabrication','source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'artwork_source':str(ART),'artwork_sha256':hashlib.sha256(ART.read_bytes()).hexdigest(),'native_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'electrical_and_placement_unchanged':True,'fixed_references':['D1','U1','J1'],'dashed_strokes':stroke_count,'path_nets':sorted(selected),'meaning':'Dashed lines follow existing routed net centerlines, clipped at parts and text. They are not unidirectional DC arrows. Both copper layers are projected onto the back artwork.','minimum_text_mm':.45,'minimum_stroke_mm':.1,'limits':['Original heart is reconstructed','Small text needs actual-size review','Silkscreen clearance and readability still under review','No fabrication outputs authorized or produced']}
(OUT/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps(evidence,indent=2))
