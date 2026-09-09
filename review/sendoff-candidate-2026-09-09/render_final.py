from pathlib import Path
import subprocess
R=Path(__file__).parent;board=R/'candidate-05/PulseSensor-JST-Educational.kicad_pcb';out=R/'final-visuals';out.mkdir(exist_ok=True);cli='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
views={'back':('top',None),'front':('bottom',None),'left':('left',None),'right':('right',None),'edge-front':('front',None),'edge-back':('back',None),'iso-top-left':('top','-35,0,45'),'iso-top-right':('top','-35,0,-45'),'iso-bottom-left':('bottom','35,0,45'),'iso-bottom-right':('bottom','35,0,-45')}
for name,(side,rotate) in views.items():
 p=out/(name+'.png')
 if p.exists():continue
 args=[cli,'pcb','render','--quality','high','--side',side,'--width','1400','--height','1400','--zoom','.86','--use-board-stackup-colors','-o',str(p)]
 if rotate:args+=['--rotate',rotate]
 r=subprocess.run(args+[str(board)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
 print('Rendered',name,flush=True)
