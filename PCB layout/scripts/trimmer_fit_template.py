"""Generate a dimensioned, 1:1 mechanical fit print; never a copper mask."""
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
MM=72/25.4
doc=fitz.open(); page=doc.new_page(width=210*MM,height=297*MM)
def pt(x,y): return fitz.Point(x*MM,y*MM)
def line(x1,y1,x2,y2):page.draw_line(pt(x1,y1),pt(x2,y2),width=.5)
def label(x,y,s,size=9):page.insert_text(pt(x,y),s,fontsize=size)
label(20,20,'RV1 mechanical fit check - P1',14)
label(20,28,'Print at ACTUAL SIZE / 100%. This is NOT a copper mask.')
label(20,35,'Measured geometry only; wiper and physical pin roles are UNVERIFIED.')
cx,cy=55,70
page.draw_circle(pt(cx,cy),4.5*MM,width=.6)
line(cx-6,cy,cx+6,cy);line(cx,cy-6,cx,cy+7)
for x,y,name in [(-4,0,'A'),(4,0,'B'),(0,5,'C')]:
    page.draw_circle(pt(cx+x,cy+y),.5*MM,width=.5)
    label(cx+x-1,cy+y-2,name,8)
line(cx-4,cy-9,cx+4,cy-9)
for x in (cx-4,cx+4):line(x,cy-10,x,cy-6)
label(cx-3,cy-11,'8 mm',8)
line(cx+10,cy,cx+10,cy+5)
line(cx+8,cy,cx+11,cy);line(cx+8,cy+5,cx+11,cy+5)
label(cx+12,cy+3,'5 mm',8)
label(20,94,'Body: diameter 9 mm. Hole centres: A=(-4,0), B=(+4,0), C=(0,+5) mm.')
label(20,102,'Hole diameter shown: 1.0 mm, assumed; check against the real leads.')
label(20,110,'Component-side view. A bottom view mirrors A/B; the hole pattern is symmetric.')
label(20,118,'A/B/C are physical locations, not a manufacturer pinout or wiper identification.')
label(20,126,'Current CAD mapping (PROVISIONAL): A=pad 1, B=pad 3, C=pad 2.')
label(20,134,'Do not fabricate before checking the wiper and matching physical pad roles.')
line(20,154,70,154);line(20,152,20,156);line(70,152,70,156)
label(20,163,'Calibration line: exactly 50 mm. Measure this after printing.')
file=ROOT/'previews/trimmer_fit_check.pdf';doc.save(file);doc.close()
print('Saved:',file)
