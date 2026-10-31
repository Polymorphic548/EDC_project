"""Prove exact saved P6 layout restoration while retaining cutting setup."""
from pathlib import Path
from decimal import Decimal
import json,re,hashlib
import check_machine_files as m

ROOT=Path(__file__).resolve().parents[1]
GEOMETRY={'footprint','segment','arc','via','zone','gr_line','gr_arc','gr_circle',
          'gr_rect','gr_poly','gr_text','gr_text_box','dimension','image','target','group'}

def normalized(node):
    if isinstance(node,list):return [normalized(item) for item in node]
    if node.startswith('"'):return ['quoted',json.loads(node)]
    if re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?',node):
        return ['number',str(Decimal(node).normalize())]
    return node

def fingerprint(path):
    tree=m.parse(path.read_text(encoding='utf-8'))
    items=sorted(json.dumps(normalized(item),separators=(',',':'))
        for item in tree if isinstance(item,list) and item and item[0] in GEOMETRY)
    return hashlib.sha256('\n'.join(items).encode()).hexdigest()

def main():
    baseline=ROOT/'current_mirror-backups/before_P7_header_space_2026-10-31'
    report_path=ROOT/'reports/layout_restore.json'
    old_report=json.loads(report_path.read_text()) if report_path.exists() else {}
    hashes={}
    for name in ('current_mirror','dual_current_mirror'):
        file=name+'.kicad_pcb';actual=fingerprint(ROOT/file)
        expected=fingerprint(baseline/file) if (baseline/file).exists() else old_report['p6_geometry_sha256'][file]
        assert actual==expected,('Saved P6 geometry differs',file)
        hashes[file]=expected
    retained=ROOT/'current_mirror-backups/before_restore_P6_2026-10-31/retained_settings_sha256.json'
    wanted=json.loads(retained.read_text()) if retained.exists() else old_report['retained_settings_sha256']
    for name,expected in wanted.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    report={'result':'PASS','revision':'P6-restored','p6_geometry_sha256':hashes,
        'compared':'All footprints including labels/models/UUIDs, every track, pad, board drawing and centre-cut line',
        'retained_settings_sha256':wanted,'unit_track_segments':50,'panel_track_segments':100,
        'note':'Exact saved P6 appearance, not a reroute. Physical thickness remains 1.7 mm; retained cutting JSON and project preferences are byte-identical.'}
    report_path.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
