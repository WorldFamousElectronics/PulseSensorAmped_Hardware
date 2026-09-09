from pathlib import Path
import json,sys,shutil,hashlib,xml.etree.ElementTree as ET,wx
app=wx.App(False)
import pcbnew as k
R=Path(__file__).parent;out=R/'candidate-01'
if out.exists():raise RuntimeError('Use a new candidate revision')
out.mkdir();src=R/'art-08';name='PulseSensor-JST-Educational'
for n in [name+'.kicad_pcb',name+'.kicad_pro',name+'.kicad_dru','PulseSensor_Amped.kicad_sym','fp-lib-table','sym-lib-table','label-plan.json','type-catalog.json','guide-plan.json','wordmark.json']:
 shutil.copy2(src/n,out/n)
for n in ['3dmodels','PulseSensor_Amped.pretty']:shutil.copytree(src/n,out/n)
sch=Path('/Users/PulsesensorCorp/.codex/worktrees/2f83/PulseSensor Amped Hardware/PulseSensor-Amped-Rebuild/kicad/PulseSensor-Amped-B-JST.kicad_sch')
shutil.copy2(sch,out/(name+'.kicad_sch'))
# KiCad local-label hierarchy adds / to these same nets. Align board aliases to
# the recovered matching schematic; the pin-to-net partition is unchanged.
b=k.LoadBoard(str(out/(name+'.kicad_pcb')))
for net in b.GetNetsByNetcode().values():
 if net.GetNetname() and not net.GetNetname().startswith('/'):net.SetNetname('/'+net.GetNetname())
k.SaveBoard(str(out/(name+'.kicad_pcb')),b)
shutil.copy2(__file__,out/'finalize_candidate.py')
print('CANDIDATE',out)
