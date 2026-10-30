"""Raster review images and 1:1 PDF orientation labels outside the blank area."""
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
MM=72/25.4
for name in ('dual_panel_assembly','dual_panel_copper_review'):
    file=ROOT/'previews'/(name+'.pdf');doc=fitz.open(file);page=doc[0]
    page.insert_text((10,304),'P4: 150 x 100 mm - TWO ISOLATED COPIES',fontsize=11,color=(.6,0,0))
    page.insert_text((10,320),'Review drawing. 5mm gap; 5.5mm side / 11mm top-bottom margins. Not a copper mask.',fontsize=8)
    tmp=file.with_suffix('.tmp.pdf');doc.save(tmp);doc.close();tmp.replace(file)
    doc=fitz.open(file);doc[0].get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(0,0,450,338)).save(file.with_suffix('.png'));doc.close()
doc=fitz.open(ROOT/'previews/dual_panel_schematic.pdf')
doc[0].get_pixmap(matrix=fitz.Matrix(1,1),clip=fitz.Rect(0,0,1650,680)).save(ROOT/'previews/dual_panel_schematic.png');doc.close()
for orientation in ('unmirrored','mirrored'):
    file=ROOT/'fabrication'/('dual_panel_BCu_'+orientation+'_1to1.pdf')
    source=fitz.open(file);original=source[0]
    # KiCad mirrors about the A4 page centre. Normalize both orientation
    # variants to the SAME 150x100mm rectangle at the page's top left,
    # translating vector content only (source/destination sizes are equal).
    width,height=150*MM,100*MM
    left=original.rect.width-width if orientation=='mirrored' else 0
    clip=fitz.Rect(left,0,left+width,height)
    doc=fitz.open();page=doc.new_page(width=original.rect.width,height=original.rect.height)
    page.show_pdf_page(fitz.Rect(0,0,width,height),source,0,clip=clip)
    # All annotations are BELOW the 150x100mm copper blank, never inside it.
    page.insert_text((10,304),'P4 B.Cu ONLY - '+orientation.upper()+' - SCALE 1:1',fontsize=10)
    page.insert_text((10,320),'Confirm mask polarity and orientation with college staff. Print ACTUAL SIZE / 100%.',fontsize=8)
    page.draw_line((10,340),(10+50*MM,340),width=.6)
    page.draw_line((10,337),(10,343),width=.6);page.draw_line((10+50*MM,337),(10+50*MM,343),width=.6)
    page.insert_text((10,355),'Calibration line = exactly 50mm. Board bounds: 150 x 100mm. No outline plotted.',fontsize=8)
    tmp=file.with_suffix('.tmp.pdf');doc.save(tmp);doc.close();source.close();tmp.replace(file)
print('Panel review PNG/PDF and two clearly labeled 1:1 copper-only orientation variants saved.')
