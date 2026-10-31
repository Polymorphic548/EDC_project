"""Verify panel netlist, isolation, layout bounds, headers and native reports."""
from pathlib import Path
import json,hashlib
import pcbnew as p
import build_design as d
import build_dual_panel as panel

ROOT=d.ROOT
def audit():
    b=p.LoadBoard(str(ROOT/'dual_current_mirror.kicad_pcb'))
    unit=p.LoadBoard(str(ROOT/'current_mirror.kicad_pcb'))
    expected={}
    sch=d.parse((ROOT/'reports/dual_current_mirror.net').read_text(encoding='utf-8'))
    for n in d.children(d.child(sch,'nets'),'net'):
        name=d.val(d.child(n,'name')[1])
        expected[name]=sorted(d.val(d.child(x,'ref')[1])+'.'+d.val(d.child(x,'pin')[1]) for x in d.children(n,'node'))
    actual={};groups={'A':[],'B':[]};bounds={}
    by_ref={f.GetReference():f for f in b.GetFootprints()}
    assert len(by_ref)==36
    unit_by_ref={f.GetReference():f for f in unit.GetFootprints()}
    for copy in groups:
        for ref,original in unit_by_ref.items():
            name=panel.reference(ref,copy);f=by_ref[name];groups[copy].append(name)
            assert f.GetValue()==panel.renamed_text(original.GetValue(),copy),name
            target=panel.transform(panel.mm_pt(original.GetPosition()),copy)
            assert all(abs(a-c)<.00001 for a,c in zip(panel.mm_pt(f.GetPosition()),target)),name
            assert abs((f.GetOrientationDegrees()-original.GetOrientationDegrees())%360-90)<.001
            for pad in f.Pads():
                orig=next(x for x in original.Pads() if x.GetNumber()==pad.GetNumber())
                net='/'+copy+'_'+orig.GetNetname().lstrip('/')
                assert pad.GetNetname()==net
                target=panel.transform(panel.mm_pt(orig.GetPosition()),copy)
                assert all(abs(a-c)<.00001 for a,c in zip(panel.mm_pt(pad.GetPosition()),target)),(name,pad.GetNumber())
                actual.setdefault(net,[]).append(name+'.'+pad.GetNumber())
                bb=pad.GetBoundingBox();box=(p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom()))
                bounds.setdefault(copy,[]).append(box)
    assert expected=={n:sorted(v) for n,v in actual.items()}
    assert len(actual)==24 and not set(n for n in actual if n.startswith('/A_'))&set(n for n in actual if n.startswith('/B_'))
    for t in b.GetTracks():
        assert not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu
        assert t.GetWidth()>=p.FromMM(.6)
        copy='A' if t.GetNetname().startswith('/A_') else 'B'
        assert t.GetNetname().startswith('/'+copy+'_')
        bb=t.GetBoundingBox();bounds[copy].append((p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())))
    assert len(list(b.GetTracks()))==2*len(list(unit.GetTracks()))
    assert not list(b.Zones())
    outlines=[x for x in b.GetDrawings() if x.GetLayer()==p.Edge_Cuts]
    assert len(outlines)==4
    points=[panel.mm_pt(x.GetStart()) for x in outlines]+[panel.mm_pt(x.GetEnd()) for x in outlines]
    assert min(x for x,y in points)==0 and max(x for x,y in points)==150
    assert min(y for x,y in points)==0 and max(y for x,y in points)==100
    boxes={c:[min(v[0] for v in bs),min(v[1] for v in bs),max(v[2] for v in bs),max(v[3] for v in bs)] for c,bs in bounds.items()}
    assert boxes['A'][0]>=5.5 and boxes['A'][2]<=72.5
    assert boxes['B'][0]>=77.5 and boxes['B'][2]<=144.5
    assert all(v[1]>=11 and v[3]<=89 for v in boxes.values())
    headers={}
    roles={'J1':{'1':'VIN','2':'GND'},'J2':{'1':'VCC','2':'OUT'},'J3':{'1':'BASE','2':'E1'},'J4':{'1':'BASE','2':'E2'}}
    for copy in groups:
        for ref,role in roles.items():
            f=by_ref[panel.reference(ref,copy)]
            nets={pad.GetNumber():pad.GetNetname() for pad in f.Pads()}
            assert nets=={pin:'/'+copy+'_'+net for pin,net in role.items()}
            assert len(list(f.Pads()))==2
            assert all(abs(p.ToMM(pad.GetDrillSize().x)-1)<.001 for pad in f.Pads())
            headers[f.GetReference()]=nets
    assert not any(ref.startswith(('TP','RV')) for ref in by_ref)
    for filename in ('erc.json','panel_erc.json'):
        data=json.loads((ROOT/'reports'/filename).read_text());assert all(not s['violations'] for s in data['sheets']),filename
    for filename in ('drc.json','panel_drc.json'):
        data=json.loads((ROOT/'reports'/filename).read_text())
        assert not data['violations'] and not data['unconnected_items'] and not data['schematic_parity'],filename
    # Every serialized board UUID must be unique after panel duplication.
    tree=d.parse((ROOT/'dual_current_mirror.kicad_pcb').read_text())
    uuids=[]
    def visit(node):
        if not isinstance(node,list) or not node:return
        if node[0]=='uuid':uuids.append(node[1])
        for x in node:
            if isinstance(x,list):visit(x)
    visit(tree);assert len(uuids)==len(set(uuids))
    report={'result':'PASS','revision':'P8-rectangles','panel_size_mm':[150,100],'unit_size_mm':[67,78],
            'unit_rectangles_mm':{'A':[5.5,11,72.5,89],'B':[77.5,11,144.5,89]},
            'gap_mm':5,'side_margins_mm':5.5,'top_bottom_margins_mm':11,
            'isolated_net_groups':{'A':12,'B':12},'shared_nets':[], 'shared_ground':False,
            'actual_copper_bounds_mm':boxes,'minimum_horizontal_copper_gap_mm':boxes['B'][0]-boxes['A'][2],
            'footprints':36,'male_2pin_headers':8,'headers':headers,'layers':['B.Cu'],'vias':0,'jumpers':0,
            'unit_and_panel_erc_drc_parity':'zero reported violations and unconnected items',
            'note':'PCB-only isolation; a shared external supply or grounded instrument may connect copies externally. No physical performance validation.'}
    (ROOT/'reports/panel_audit.json').write_text(json.dumps(report,indent=2))
    files=['dual_current_mirror.kicad_pcb','dual_current_mirror.kicad_sch','dual_current_mirror.kicad_pro','current_mirror.kicad_pcb','current_mirror.kicad_sch','current_mirror.kicad_pro','fabrication/dual_panel_BCu_unmirrored_1to1.pdf','fabrication/dual_panel_BCu_mirrored_1to1.pdf']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}
    (ROOT/'reports/panel_sha256.json').write_text(json.dumps(hashes,indent=2))
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':audit()
