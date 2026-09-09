from pathlib import Path
import subprocess,json,shutil,hashlib,csv
R=Path(__file__).parent;src=R/'mono-08';board=src/'PulseSensor-JST-Educational.kicad_pcb';out=R/'mono-08-package'
if out.exists():raise RuntimeError('Output exists; choose another revision')
for d in ('FAB','ASSEMBLY/PASTE_GERBERS','SOURCE','REVIEW','VALIDATION'):(out/d).mkdir(parents=True,exist_ok=True)
cli='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli';commands=[]
def run(args):
 result=subprocess.run([cli]+[str(a) for a in args],capture_output=True,text=True);commands.append({'argv':args,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
 if result.returncode:raise RuntimeError(result.stderr or result.stdout)
run(['pcb','export','gerbers','--no-x2','--subtract-soldermask','--check-zones','--use-drill-file-origin','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','-o',str(out/'FAB'),str(board)])
run(['pcb','export','drill','--format','excellon','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',str(out/'FAB/DRILL_REPORT.txt'),'-o',str(out/'FAB'),str(board)])
run(['pcb','export','ipcd356','-o',str(out/'FAB/PulseSensor-JST-Educational.d356'),str(board)])
run(['pcb','export','gerbers','--no-x2','--check-zones','--use-drill-file-origin','--layers','F.Paste,B.Paste','-o',str(out/'ASSEMBLY/PASTE_GERBERS'),str(board)])
run(['pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--use-drill-file-origin','-o',str(out/'ASSEMBLY/CPL.csv'),str(board)])
run(['sch','export','netlist','--format','kicadxml','-o',str(out/'VALIDATION/netlist.xml'),str(board.with_suffix('.kicad_sch'))])
run(['sch','export','pdf','-o',str(out/'REVIEW/schematic.pdf'),str(board.with_suffix('.kicad_sch'))])
run(['sch','erc','--format','json','-o',str(out/'VALIDATION/erc.json'),str(board.with_suffix('.kicad_sch'))])
for p in src.iterdir():
 if p.suffix in ('.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym') or p.name in ('fp-lib-table','sym-lib-table'):shutil.copy2(p,out/'SOURCE'/p.name)
for d in ('3dmodels','PulseSensor_Amped.pretty'):shutil.copytree(src/d,out/'SOURCE'/d)
shutil.copy2(src/'drc-final.json',out/'VALIDATION/drc.json')
# Retain the exact existing component selections. New placement data is above.
old=Path('/Users/PulsesensorCorp/.codex/worktrees/2f83/PulseSensor Amped Hardware/PulseSensor-Amped-Rebuild/output/pcbway-release-candidates-RC3-R1-FINAL/PulseSensor-Amped-B-PCBWay-EVT-RC3-R1-FINAL/ASSEMBLY')
for oldname,newname in [('PulseSensor-Amped-B-BOM.csv','BOM-controlled-components.csv'),('PulseSensor-Amped-B-R1-POPULATION-MATRIX.csv','R1-controlled-population.csv')]:shutil.copy2(old/oldname,out/'ASSEMBLY'/newname)
(out/'VALIDATION/export-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('EXPORTED',out)
