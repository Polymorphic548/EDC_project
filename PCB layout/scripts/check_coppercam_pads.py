"""P8: require only basic C/R apertures and verify every transistor pad."""
from pathlib import Path
import json,re,collections,math,hashlib
import check_machine_files as m

ROOT=Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'fabrication/machine_files/dual_current_mirror-B_Cu.gbr'
    text=path.read_text()
    apertures=re.findall(r'%ADD\d+([A-Za-z_][^,*]*),',text)
    assert set(apertures)=={'C','R'},apertures
    assert '%AM' not in text and 'G36*' not in text and '%LPC*%' not in text
    flashes,tracks,regions=m.gerber(path)
    assert len(flashes)==76 and not regions and len(tracks)==100
    tree=m.parse((ROOT/'dual_current_mirror.kicad_pcb').read_text())
    shapes=collections.Counter();transistors={}
    for fp in m.children(tree,'footprint'):
        ref=next(m.val(prop[2]) for prop in m.children(fp,'property') if m.val(prop[1])=='Reference')
        at=m.child(fp,'at');fx,fy=map(float,at[1:3]);angle=math.radians(float(at[3]) if len(at)>3 else 0)
        for pad in m.children(fp,'pad'):
            assert pad[3] in ('circle','rect'),(ref,pad[1],pad[3])
            shapes[pad[3]]+=1
            if not ref.startswith('Q'):continue
            assert pad[3]=='rect'
            sx,sy=map(float,m.child(pad,'size')[1:]);assert (sx,sy)==(1.7,2.4)
            assert float(m.child(pad,'drill')[1])==.8
            dx,dy=map(float,m.child(pad,'at')[1:3])
            x=fx+dx*math.cos(angle)+dy*math.sin(angle);y=fy-dx*math.sin(angle)+dy*math.cos(angle)
            assert m.keyed([(x,-y,'R',2.4,1.7)])<=m.keyed(flashes)
            transistors[ref+'.'+m.val(pad[1])]={'gerber_xy_mm':[round(x,6),round(-y,6)],
                'shape':'R','size_mm':[2.4,1.7],'drill_mm':.8,'net':m.val(m.child(pad,'net')[-1])}
    assert len(transistors)==12 and shapes=={'rect':36,'circle':40}
    for path in (ROOT/'Project.pretty').glob('*.kicad_mod'):
        if path.stem.startswith('RV'):continue
        fp=m.parse(path.read_text())
        for pad in m.children(fp,'pad'):
            assert pad[3] in ('circle','rect'),path.name
    baseline=ROOT/'current_mirror-backups/before_P8_rectangles_2026-10-31/retained_settings_sha256.json'
    report_path=ROOT/'reports/coppercam_pads.json'
    previous=json.loads(report_path.read_text()) if report_path.exists() else {}
    retained=json.loads(baseline.read_text()) if baseline.exists() else previous['retained_settings_sha256']
    for name,want in retained.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,name
    report={'result':'PASS - FILE GEOMETRY ONLY','revision':'P8-rectangles','pad_shapes':dict(shapes),
        'converted_oval_pads':20,'converted_rounded_rectangle_pads':8,
        'gerber_standard_aperture_shapes':sorted(set(apertures)),'gerber_pad_flashes':76,
        'gerber_regions':0,'gerber_aperture_macros':0,'transistor_pads':transistors,
        'retained_settings_sha256':retained,
        'CopperCAM_import_confirmation':'PENDING LAB TEST - not reproduced locally',
        'note':'Only pad outline shape changes. P6 placement, routes, dimensions, drills, electrical nets and cutting setup are retained and separately checked.'}
    report_path.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
