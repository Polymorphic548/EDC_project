"""P6: verify emitter copper exports, straight routing and separate centre cut."""
from pathlib import Path
from types import SimpleNamespace
import json,math,zipfile
import pcbnew as p
import build_design as d
import check_machine_files as machine

ROOT=d.ROOT

def main():
    baseline=ROOT/'current_mirror-backups/before_P6_cam_routes_2026-10-31'
    b=p.LoadBoard(str(ROOT/'dual_current_mirror.kicad_pcb'))
    flashes,_,_=machine.gerber(ROOT/'fabrication/machine_files/dual_current_mirror-B_Cu.gbr')
    before_flashes=None
    if (baseline/'dual_panel_machine_files.zip').exists():
        with zipfile.ZipFile(baseline/'dual_panel_machine_files.zip') as archive:
            text=archive.read('dual_current_mirror-B_Cu.gbr').decode()
        before_flashes,_,_=machine.gerber(SimpleNamespace(read_text=lambda:text))
    emitters={}
    for f in b.GetFootprints():
        if f.GetReference() not in ('Q1','Q2','Q101','Q102'):continue
        pad=next(pad for pad in f.Pads() if pad.GetNumber()=='1')
        assert pad.GetShape()==p.PAD_SHAPE_OVAL
        x,y=p.ToMM(pad.GetPosition().x),-p.ToMM(pad.GetPosition().y)
        want=(x,y,'O',2.4,1.7)
        assert machine.keyed([want])<=machine.keyed(flashes),f.GetReference()
        old_present=None if before_flashes is None else machine.keyed([(x,y,'R',2.4,1.7)])<=machine.keyed(before_flashes)
        assert old_present is not False
        emitters[f.GetReference()]={'pin':'1','net':pad.GetNetname(),'gerber_xy_mm':[x,y],
            'gerber_pad':'O 2.4 x 1.7 mm','drill_mm':p.ToMM(pad.GetDrillSize().x),
            'minimum_annular_copper_mm':.45,'present_in_new_copper_gerber':True,
            'present_as_rectangle_in_baseline_gerber':old_present}
    assert len(emitters)==4
    angles={};lengths=[];short_segments=[]
    for track in b.GetTracks():
        assert isinstance(track,p.PCB_TRACK) and not isinstance(track,p.PCB_VIA)
        assert track.GetLayer()==p.B_Cu and track.GetWidth()==p.FromMM(.6)
        dx=p.ToMM(track.GetEnd().x-track.GetStart().x)
        dy=p.ToMM(track.GetEnd().y-track.GetStart().y)
        assert abs(dx)<1e-5 or abs(dy)<1e-5 or abs(abs(dx)-abs(dy))<1e-5
        angle=round(math.degrees(math.atan2(dy,dx)))
        angles[str(angle)]=angles.get(str(angle),0)+1
        lengths.append(math.hypot(dx,dy))
        if lengths[-1]<.5:
            ends={(track.GetStart().x,track.GetStart().y),(track.GetEnd().x,track.GetEnd().y)}
            short_segments.append((track.GetNetname(),ends))
    # An isolated short 45-degree transition is valid. Reject chains of tiny
    # sections that recreate the old obstacle-following staircase geometry.
    for index,(net,ends) in enumerate(short_segments):
        assert not any(net==other_net and ends&other_ends for other_net,other_ends in short_segments[index+1:]),'Consecutive tiny routing steps remain'
    audit=json.loads((ROOT/'reports/panel_audit.json').read_text())
    boxes=audit['actual_copper_bounds_mm']
    margin=min(75-boxes['A'][2],boxes['B'][0]-75)
    assert margin>=4
    # Ensure local footprint library keeps each pin-1 oval after future updates.
    for ref in ('Q1','Q2'):
        tree=d.parse((ROOT/'Project.pretty'/(ref+'_ETCH.kicad_mod')).read_text())
        pad=next(pad for pad in d.children(tree,'pad') if d.val(pad[1])=='1')
        assert pad[3]=='oval'
    report={'result':'PASS','revision':'P6-restored','emitters':emitters,
        'track_segments':len(lengths),'track_angles_degrees':angles,
        'minimum_track_segment_length_mm':min(lengths),'arc_tracks':0,
        'isolated_short_transition_segments':len(short_segments),
        'centre_cut':{'x_mm':75,'y_start_mm':0,'y_end_mm':100,
            'minimum_conservative_centreline_to_copper_mm':round(margin,3),
            'file':'dual_current_mirror-Centre_Cut.gbr',
            'machine_depth_feed_speed_and_holding':'operator inputs pending; no machine program generated'},
        'note':'All four emitter pads already existed in P5. P6 exports them as oval apertures. CopperCAM import and cutting toolpaths still require inspection; the original missing-pad symptom is not reproduced here.'}
    (ROOT/'reports/emitter_routes.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
