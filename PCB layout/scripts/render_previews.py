"""Optional PNG review images and draft stamps; requires PyMuPDF, not pcbnew.

Run only after exporting fresh native PDF plots. Does not change design files.
"""
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'previews'
for name in ('assembly_top','copper_review'):
    file=PRE/(name+'.pdf')
    doc=fitz.open(file); page=doc[0]
    # Outside board bounds, so geometry remains exactly at its native 1:1 scale.
    page.insert_text((10,222),'P1 DRAFT - VERIFY RV1 WIPER',fontsize=10,color=(.7,0,0))
    page.insert_text((10,236),'RV1: 9mm body, 8/5mm pins. Board: 78 x 67 mm.',fontsize=8,color=(.3,.3,.3))
    if name=='copper_review':
        page.insert_text((10,249),'Top-coordinate review only; mask orientation is unconfirmed.',fontsize=7,color=(.3,.3,.3))
    # Save atomically; no implicit scaling or mirroring.
    tmp=file.with_suffix('.tmp.pdf'); doc.save(tmp); doc.close(); tmp.replace(file)
    doc=fitz.open(file)
    doc[0].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(0,0,245,255)).save(PRE/(name+'.png'))
    doc.close()
doc=fitz.open(PRE/'schematic.pdf')
doc[0].get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(PRE/'schematic.png')
print('Saved stamped PDF and PNG review previews. No fabrication mask released.')
