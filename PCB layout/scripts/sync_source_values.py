"""P3: synchronize reviewed LTspice values while preserving all PCB geometry."""
from pathlib import Path
import hashlib,json,re,shutil
import pcbnew as pcb
import build_design as d

ROOT=d.ROOT
def routing_geometry(tree):
    # Track UUIDs, net assignments, pads/drills and placements are checked too.
    copper=sorted(d.dump(x) for x in tree if isinstance(x,list) and x and x[0] in ('segment','arc','via','zone'))
    footprints={}
    for f in d.children(tree,'footprint'):
        ref=next(d.val(x[2]) for x in d.children(f,'property') if d.val(x[1])=='Reference')
        footprints[ref]={'at':d.child(f,'at'),'footprint':f[1],'pads':sorted(d.dump(p) for p in d.children(f,'pad'))}
    return {'copper':copper,'footprints':footprints,'outline':sorted(d.dump(x) for x in d.children(tree,'gr_line'))}

def main():
    raise SystemExit('Historical P3 helper retired. Current P4 uses header units and dual-panel generation; see README reproduction steps.')
    source=ROOT.parent/'schematics/diode_comp_mirror_enhanced_v2.asc'
    source_bytes=source.read_bytes(); text=source_bytes.decode('utf-8')
    source_parts={}; current={}
    for line in text.splitlines():
        if line.startswith('SYMBOL '): current={}
        elif line.startswith('SYMATTR '):
            _,key,value=line.split(' ',2); current[key]=value
            if 'InstName' in current and 'Value' in current:source_parts[current['InstName']]=current['Value']
    assert {ref:source_parts[ref] for ref in ('V1','Rs','C1')}=={'V1':'9.8','Rs':'662','C1':'1.33n'}
    assert re.search(r'\.param\s+RV=117\.6(?:\s|$)',text)
    backup=ROOT/'current_mirror-backups/before_P3_source_sync_2026-10-30'
    backup.mkdir(parents=True,exist_ok=True)
    for name in ('current_mirror.kicad_pcb','current_mirror.kicad_sch','current_mirror.kicad_pro','components.json','reports/routing.json'):
        dest=backup/Path(name).name
        if not dest.exists():shutil.copy2(ROOT/name,dest)
    path=ROOT/'current_mirror.kicad_pcb'
    before=routing_geometry(d.parse(path.read_text(encoding='utf-8')))
    board=pcb.LoadBoard(str(path)); changes={}
    for f in board.GetFootprints():
        new=next(p[1] for p in d.PARTS if p[0]==f.GetReference())
        if f.GetValue()!=new:
            changes[f.GetReference()]={'before':f.GetValue(),'after':new}; f.SetValue(new)
    labels={'+12V':'+9.8V','5 mA CURRENT MIRROR':'CURRENT MIRROR','P2 - FIXED R7 120R':'P3 - SOURCE VALUES SYNC'}
    for item in board.GetDrawings():
        if isinstance(item,pcb.PCB_TEXT) and item.GetText() in labels:item.SetText(labels[item.GetText()])
    pcb.SaveBoard(str(path),board)
    assert routing_geometry(d.parse(path.read_text(encoding='utf-8')))==before,'Unexpected layout change'
    d.write_project(); d.write_schematic(); d.verify_source()
    for ref in changes:
        file=ROOT/'Project.pretty'/(ref+'_ETCH.kicad_mod')
        fp=d.parse(file.read_text(encoding='utf-8'))
        prop=next(x for x in d.children(fp,'property') if d.val(x[1])=='Value')
        prop[2]=d.q(changes[ref]['after']); file.write_text(d.dump(fp),encoding='utf-8')
    routing=json.loads((ROOT/'reports/routing.json').read_text())
    routing.update(revision='P3',note='P3 value/label sync only; all original track/pad geometry preserved, no rerouting.')
    (ROOT/'reports/routing.json').write_text(json.dumps(routing,indent=2))
    assert source.read_bytes()==source_bytes
    out=ROOT/'reports/P3_source_sync_2026-10-30';out.mkdir(exist_ok=True)
    report={'revision':'P3','source_sha256':hashlib.sha256(source_bytes).hexdigest(),'changes':changes,'reference_changes':[],
            'routing_pads_placements_outline_preserved':True,'no_rerouting':True,'source_unchanged':True,
            'r7_note':'Retain fixed nominal 120 ohm part; measured 117.6 ohm matches updated LT RV parameter.',
            'simulation_note':'Supplied LTspice log: 4.62459400296mA at 25C; 4.66735195369mA at 75C. Not physical measurements; no new run.'}
    (out/'changes.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
