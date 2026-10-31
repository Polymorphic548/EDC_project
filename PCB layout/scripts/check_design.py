"""Audit the saved board against KiCad's exported schematic netlist."""
from pathlib import Path
import json, csv, hashlib
import pcbnew as p
import build_design as d

ROOT=d.ROOT

def sync_placeholder():
    path=ROOT/'current_mirror.kicad_pcb'; b=p.LoadBoard(str(path))
    for f in b.GetFootprints():
        part=next(item for item in d.PARTS if item[0]==f.GetReference())
        f.SetFPID(p.LIB_ID(*part[3].split(':')))
        if f.GetReference().startswith('TP'): f.SetAttributes(f.GetAttributes() & ~p.FP_EXCLUDE_FROM_BOM)
        if f.GetReference() in ('D1','D2','R3','TP5'): f.SetPosition(d.pos(*part[5][:2]))
        if f.GetReference()=='J1': f.Reference().SetPosition(d.pos(12,17))
        if f.GetReference() in ('D1','D2','D3','C1'):
            for graphic in f.GraphicalItems():
                if graphic.GetLayer()==p.F_SilkS: graphic.SetLayer(p.F_Fab)
        for pad in f.Pads():
            if not pad.GetNetname().startswith('/'):
                pad.GetNet().SetNetname('/'+pad.GetNetname())
        if f.GetReference().startswith('J'):
            for pad in f.Pads():
                pad.SetSize(d.pos(2.4,1.7))
                pad.SetShape(p.PAD_SHAPE_RECT)
        if f.GetReference().startswith('Q'):
            for pad in f.Pads():
                pad.SetSize(d.pos(1.7,2.4))
                pad.SetShape(p.PAD_SHAPE_RECT)
        for pad in f.Pads():
            if pad.GetShape()==p.PAD_SHAPE_ROUNDRECT:pad.SetShape(p.PAD_SHAPE_RECT)
    for t in b.GetDrawings():
        if isinstance(t,p.PCB_TEXT) and t.GetText()=='BOTTOM COPPER ONLY': t.SetLayer(p.B_SilkS); t.SetMirrored(True)
        if isinstance(t,p.PCB_TEXT) and t.GetText()=='BASE': t.SetPosition(d.pos(73,52))
    p.SaveBoard(str(path),b)
    d.save_local_footprints()

def audit():
    b=p.LoadBoard(str(ROOT/'current_mirror.kicad_pcb'))
    sch=d.parse((ROOT/'reports/current_mirror.net').read_text(encoding='utf-8'))
    expected={}
    for net in d.children(d.child(sch,'nets'),'net'):
        name=d.val(d.child(net,'name')[1])
        expected[name]=sorted(d.val(d.child(n,'ref')[1])+'.'+d.val(d.child(n,'pin')[1]) for n in d.children(net,'node'))
    actual={}
    for f in b.GetFootprints():
        for pad in f.Pads(): actual.setdefault(pad.GetNetname(),[]).append(f.GetReference()+'.'+pad.GetNumber())
    actual={n:sorted(v) for n,v in actual.items()}
    assert expected==actual, {'schematic':expected,'board':actual}
    assert all(t.GetLayer()==p.B_Cu and isinstance(t,p.PCB_TRACK) and not isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'Track on wrong layer or via present'
    assert min(p.ToMM(t.GetWidth()) for t in b.GetTracks())>=.6
    assert not any(f.GetReference()=='RV1' for f in b.GetFootprints())
    resistor=next(f for f in b.GetFootprints() if f.GetReference()=='R7')
    assert resistor.GetValue()=='120R (117.6R measured)'
    for f in b.GetFootprints():
        assert f.GetValue()==next(part[1] for part in d.PARTS if part[0]==f.GetReference()),f.GetReference()
    assert {pad.GetNumber():pad.GetNetname() for pad in resistor.Pads()}=={'1':'/TRIM_TOP','2':'/BASE'}
    assert len(list(resistor.Pads()))==2
    assert not any(f.GetReference().startswith('TP') for f in b.GetFootprints())
    for ref,nets in {'J1':{'1':'/VIN','2':'/GND'},'J2':{'1':'/VCC','2':'/OUT'},'J3':{'1':'/BASE','2':'/E1'},'J4':{'1':'/BASE','2':'/E2'}}.items():
        f=next(f for f in b.GetFootprints() if f.GetReference()==ref)
        assert {pad.GetNumber():pad.GetNetname() for pad in f.Pads()}==nets
    report={'result':'PASS','revision':'P8-rectangles','schematic_to_board_pad_nets':'exact match of native KiCad exported netlist','nets':actual,'tracks':len(list(b.GetTracks())),'routed_layers':['B.Cu'],'vias':0,'footprints':len(list(b.GetFootprints())),'headers':'J1 power; J2 Rload; J3 Q1 B-E; J4 Q2 B-E','note':'Single unit CAD audit. Separate panel isolation audit required; no physical performance measurement.'}
    (ROOT/'reports/board_audit.json').write_text(json.dumps(report,indent=2))
    parts=json.loads((ROOT/'components.json').read_text())
    for item in parts:
        item['position_mm']=list(next(pt for pt in d.PARTS if pt[0]==item['reference'])[5])
    (ROOT/'components.json').write_text(json.dumps(parts,indent=2))
    with (ROOT/'BOM.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Reference','Value','Footprint','Status'])
        for item in parts:w.writerow([item['reference'],item['value'],item['footprint'],item['status']])
    source=ROOT.parent/'schematics/diode_comp_mirror_enhanced_v2.asc'
    hashes={str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else '../schematics/'+f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [source,ROOT/'current_mirror.kicad_sch',ROOT/'current_mirror.kicad_pcb',ROOT/'current_mirror.kicad_pro']}
    (ROOT/'reports/design_sha256.json').write_text(json.dumps(hashes,indent=2))
    print('PASS: native schematic netlist matches board; bottom-only tracks; no vias.',flush=True)

if __name__=='__main__':
    import sys
    if '--sync-placeholder' in sys.argv:sync_placeholder()
    else:audit()
