"""Record explicit opaque RGBA metadata after the color-09 renderer check."""
from pathlib import Path
import shutil
r=Path(__file__).resolve().parent
if (r/'color-10').exists():raise RuntimeError('Preserve existing revision; choose a new destination')
shutil.copytree(r/'color-09',r/'color-10')
p=r/'color-10/PulseSensor-JST-Educational.kicad_pcb'
p.write_text(p.read_text().replace('(color "White")','(color "#FFFFFFFF")'))
# KiCad still applies the F-mask display color to both sides. See README;
# intended B-side appearance is documented using the identical mono-08 face.
