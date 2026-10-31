"""Verify Gerber flashes/tracks, outline and Excellon hits against saved PCB.

No CAD modifications. Produces fabrication-package validation and hash records.
"""
from pathlib import Path
import ast,re,json,math,hashlib,collections

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'fabrication/machine_files'
ns={'re':re,'json':json}
for node in ast.parse((ROOT/'scripts/build_design.py').read_text(encoding='utf-8')).body:
    if isinstance(node,ast.FunctionDef) and node.name in ('parse','children','child','val'):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<pcb parser>','exec'),ns)
parse,children,child,val=(ns[n] for n in ('parse','children','child','val'))

def point(p):return tuple(map(float,p[1:3]))
def keyed(items):return collections.Counter(tuple(round(v,3) if isinstance(v,float) else v for v in item) for item in items)

def gerber(path):
    text=path.read_text();assert '%MOMM*%' in text and '%FSLAX46Y46*%' in text
    assert '%LPC*%' not in text,'Unexpected clear polarity'
    apertures={int(n):(shape,tuple(map(float,size.split('X')))) for n,shape,size in re.findall(r'%ADD(\d+)([CRO]),([\d.X]+)\*%',text)}
    aperture=None;x=y=0;flashes=[];segments=[];regions=[];region=None;mode='G01'
    for line in text.splitlines():
        if line=='G36*':region={'points':[],'radii':[]};continue
        if line=='G37*':
            assert region and len(region['radii'])==4
            pts=region['points'];assert math.dist(pts[0],pts[-1])<1e-6
            x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
            assert max(region['radii'])-min(region['radii'])<1e-6
            regions.append(((x0+x1)/2,(y0+y1)/2,x1-x0,y1-y0,region['radii'][0]));region=None;continue
        if line in ('G01*','G02*','G03*'):mode=line[:-1];continue
        a=re.fullmatch(r'D(\d+)\*',line)
        if a:aperture=int(a[1]);continue
        m=re.fullmatch(r'(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?D0([123])\*',line)
        if not m:continue
        prev=(x,y)
        if m[1] is not None:x=int(m[1])/1e6
        if m[2] is not None:y=int(m[2])/1e6
        if region is not None:
            region['points'].append((x,y))
            if m[5]=='1' and mode in ('G02','G03'):region['radii'].append(math.hypot(int(m[3] or 0)/1e6,int(m[4] or 0)/1e6))
            continue
        shape,size=apertures[aperture]
        if m[5]=='3':flashes.append((x,y,shape,*size))
        elif m[5]=='1':
            assert mode=='G01'
            segments.append((*prev,x,y,shape,*size))
    return flashes,segments,regions

def main():
    path=ROOT/'dual_current_mirror.kicad_pcb';tree=parse(path.read_text(encoding='utf-8'))
    expected_hits=[];expected_flashes=[];expected_tracks=[];expected_regions=[]
    for fp in children(tree,'footprint'):
        at=child(fp,'at');fx,fy=point(at);angle=math.radians(float(at[3]) if len(at)>3 else 0)
        for pad in children(fp,'pad'):
            dx,dy=point(child(pad,'at'));x=fx+dx*math.cos(angle)+dy*math.sin(angle);y=fy-dx*math.sin(angle)+dy*math.cos(angle)
            drill=child(pad,'drill');assert len(drill)==2
            expected_hits.append((x,-y,float(drill[1])))
            sx,sy=map(float,child(pad,'size')[1:]);shape=pad[3]
            if shape=='circle':expected_flashes.append((x,-y,'C',sx))
            elif shape in ('rect','oval'):
                pa=child(pad,'at')
                orientation=float(pa[3]) if len(pa)>3 else 0
                assert abs(orientation/90-round(orientation/90))<1e-6
                if round(orientation/90)%2:sx,sy=sy,sx
                expected_flashes.append((x,-y,'R' if shape=='rect' else 'O',sx,sy))
            else:
                assert shape=='roundrect' and sx==sy
                radius=min(sx,sy)*float(child(pad,'roundrect_rratio')[1])
                expected_regions.append((x,-y,sx,sy,radius))
    for seg in children(tree,'segment'):
        assert val(child(seg,'layer')[1])=='B.Cu'
        x,y=point(child(seg,'start'));xx,yy=point(child(seg,'end'))
        expected_tracks.append((x,-y,xx,-yy,'C',float(child(seg,'width')[1])))
    assert not children(tree,'via') and not children(tree,'zone')
    copper=OUT/'dual_current_mirror-B_Cu.gbr'
    flashes,tracks,regions=gerber(copper)
    assert keyed(flashes)==keyed(expected_flashes),'Copper pad flashes differ from PCB'
    assert keyed(regions)==keyed(expected_regions),'Rounded rectangle pad regions differ from PCB'
    # Gerber may reverse segment start/end; compare unordered endpoint pairs.
    def canonical(items):
        result=[]
        for x,y,xx,yy,*tail in items:
            a,b=sorted(((round(x,3),round(y,3)),(round(xx,3),round(yy,3))))
            result.append((*a,*b,*tail))
        return keyed(result)
    assert canonical(tracks)==canonical(expected_tracks),'Copper tracks differ from PCB'
    drill=(OUT/'dual_current_mirror.drl').read_text();assert 'METRIC' in drill and 'G90' in drill
    tools={int(n):float(d) for n,d in re.findall(r'^T(\d+)C([\d.]+)$',drill,re.M)}
    selected=None;hits=[]
    for line in drill.splitlines():
        m=re.fullmatch(r'T(\d+)',line)
        if m:selected=int(m[1]);continue
        m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
        if m:hits.append((float(m[1]),float(m[2]),tools[selected]))
    assert keyed(hits)==keyed(expected_hits),'Drill centres/sizes differ from PCB or Gerber registration'
    assert len(hits)==76
    _,outline,outline_regions=gerber(OUT/'dual_current_mirror-Edge_Cuts.gbr');assert not outline_regions
    assert len(outline)==4
    coords={(round(x,3),round(y,3)) for s in outline for x,y in ((s[0],s[1]),(s[2],s[3]))}
    assert coords=={(0,0),(150,0),(150,-100),(0,-100)}
    cut_flashes,cut_tracks,cut_regions=gerber(OUT/'dual_current_mirror-Centre_Cut.gbr')
    assert not cut_flashes and not cut_regions and len(cut_tracks)==1
    x,y,xx,yy,shape,width=cut_tracks[0]
    assert shape=='C' and abs(width-.1)<1e-6
    assert {(x,y),(xx,yy)}=={(75.0,0.0),(75.0,-100.0)}
    cut_shapes=[item for item in children(tree,'gr_line') if val(child(item,'layer')[1])=='User.1']
    assert len(cut_shapes)==1
    assert {point(child(cut_shapes[0],'start')),point(child(cut_shapes[0],'end'))}=={(75.0,0.0),(75.0,100.0)}
    assert (OUT/'centre_cut_setup.json').read_bytes()==(ROOT/'centre_cut_setup.json').read_bytes()
    cut_setup=json.loads((OUT/'centre_cut_setup.json').read_text())
    assert cut_setup['user_reported_board_thickness_mm']==1.7
    assert cut_setup['user_reported_cutter_diameter_mm']==.8
    assert cut_setup['user_reported_maximum_depth_per_pass_mm']==.4
    assert not list(OUT.glob('*F_Cu*')) and not list(OUT.glob('*.gbrjob'))
    # Exporting must not change any source CAD files that were validated earlier.
    recorded=json.loads((ROOT/'reports/panel_sha256.json').read_text())
    for name,want in recorded.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,name
    report={'result':'PASS','panel_size_mm':[150,100],'physical_copper_layers':1,'copper_layer':'B.Cu',
            'units':'mm','origin':'absolute, shared by Gerber and drill','extra_mirroring':False,
            'drill_hits':len(hits),'drill_sizes_and_counts_mm':dict(sorted(collections.Counter(str(d) for x,y,d in hits).items())),
            'copper_pad_features':len(flashes)+len(regions),'copper_pad_flashes':len(flashes),'rounded_pad_regions':len(regions),'copper_track_segments':len(tracks),
            'all_drill_positions_sizes_and_copper_geometry_match_saved_pcb':True,
            'outline':'150 x 100 mm, separate optional file; not copper artwork',
            'centre_cut':'separate straight centreline from (75,0) to (75,-100) mm; operator assigns cut-through toolpath; no tabs encoded',
            'centre_cut_user_setup_mm':{'board_thickness':1.7,'cutter_diameter':.8,'maximum_pass_depth':.4},
            'source_cad_and_existing_print_artifacts_unchanged':True}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2))
    files=[p for p in OUT.iterdir() if p.is_file() and p.name!='SHA256.json']
    (OUT/'SHA256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
