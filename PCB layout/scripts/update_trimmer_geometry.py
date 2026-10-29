"""Apply the user-measured RV1 geometry without rebuilding other components.

The measured third pin is provisionally pad 2, NOT a confirmed wiper.
Does not alter project preferences or remove GUI lock files.
"""
from pathlib import Path
import shutil, json
import pcbnew as pcb
import build_design as d

ROOT=d.ROOT

def main():
    raise SystemExit('Historical P1 helper retired: current P2 uses fixed R7=120 ohm. Use build_design.py for the current design.')
    backup=ROOT/'current_mirror-backups/before_P1_2026-10-29'
    backup.mkdir(parents=True,exist_ok=True)
    for name in ('current_mirror.kicad_pcb','current_mirror.kicad_sch','current_mirror.kicad_pro','components.json','reports/design_sha256.json'):
        dest=backup/Path(name).name
        if not dest.exists(): shutil.copy2(ROOT/name,dest)

    file=ROOT/'current_mirror.kicad_pcb'
    tree=d.parse(file.read_text(encoding='utf-8'))
    old=next(f for f in d.children(tree,'footprint') if any(d.val(x[1])=='Reference' and d.val(x[2])=='RV1' for x in d.children(f,'property')))
    scratch=ROOT/'reports/rv1_geometry_scratch.kicad_pcb'
    board=pcb.BOARD(); f=d.trimmer_footprint(board); board.Add(f)
    ref,value,lib,fp,nets,(x,y,angle),sch=next(pt for pt in d.PARTS if pt[0]=='RV1')
    f.SetReference(ref); f.SetValue(value); f.SetPath(pcb.KIID_PATH('/'+d.uid('schematic')+'/'+d.uid(ref)))
    f.Reference().SetTextSize(d.pos(1,1)); f.Reference().SetTextThickness(d.mm(.15))
    f.SetPosition(d.pos(x,y)); f.Value().SetVisible(False)
    for name in set(nets.values()): board.Add(pcb.NETINFO_ITEM(board,'/'+name))
    for pad in f.Pads(): pad.SetNet(board.FindNet('/'+nets[pad.GetNumber()]))
    pcb.SaveBoard(str(scratch),board)
    new=d.children(d.parse(scratch.read_text(encoding='utf-8')),'footprint')[0]
    scratch.unlink()
    d.child(new,'uuid')[1]=d.child(old,'uuid')[1]
    tree[tree.index(old)]=new
    for text in d.children(tree,'gr_text'):
        if d.val(text[1])=='P0 - NOT FOR FABRICATION': text[1]=d.q('P1 - VERIFY RV1 WIPER')
        if d.val(text[1])=='RV1 SPACE RESERVED': text[1]=d.q('RV1 PINOUT UNVERIFIED')
    file.write_text(d.dump(tree),encoding='utf-8')
    d.write_project()  # Existing .kicad_pro is preserved, including user preferences.
    d.write_schematic()
    d.save_local_footprints()
    d.verify_source()
    report={
        'revision':'P1','date':'2026-10-29','status':'MEASURED GEOMETRY FITTED; WIPER IDENTIFICATION REQUIRED',
        'body_diameter_mm':9,'across_pair_mm':8,'third_pin_offset_from_body_centre_mm':5,
        'footprint':fp,'body_centre_on_board_mm':[x,y],
        'pad_centres_relative_to_body_mm':d.TRIMMER_PINS,
        'provisional_pad_roles':nets,
        'important':'Pad 2 at the offset third hole is NOT a confirmed physical wiper. Verify before fabrication; swap physical pad roles if needed.',
        'drill_mm':1.0,'copper_pad_size_mm':2.4,'drill_status':'assumed from thin pins; confirm physical fit',
        'view':'KiCad component-side view. Bottom/pin-side view mirrors left and right; the symmetric hole pattern is unchanged.',
        'body_height':'unknown; no guessed 3D model added',
        'backup':str(backup.relative_to(ROOT)),
    }
    (ROOT/'reports/trimmer_geometry_2026-10-29.json').write_text(json.dumps(report,indent=2))
    print('Applied measured RV1 geometry. Run routing and CAD checks next.',flush=True)

if __name__=='__main__':main()
