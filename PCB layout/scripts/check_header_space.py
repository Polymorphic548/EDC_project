"""Audit restored P6 header positions and retained cutting setup/thickness."""
from pathlib import Path
import json,math
import pcbnew as p
import build_design as d

ROOT=d.ROOT

def main():
    b=p.LoadBoard(str(ROOT/'dual_current_mirror.kicad_pcb'))
    refs={f.GetReference():f for f in b.GetFootprints()}
    headers={}
    for ref,x in [('J2',30.5),('J4',50.5),('J102',102.5),('J104',122.5)]:
        f=refs[ref]
        assert abs(p.ToMM(f.GetPosition().x)-x)<1e-5
        assert abs(p.ToMM(f.GetPosition().y)-19)<1e-5
        pads=list(f.Pads());left=min(p.ToMM(pad.GetPosition().x) for pad in pads)-1.2
        right=max(p.ToMM(pad.GetPosition().x) for pad in pads)+1.2
        pad_top=19-.85
        # Clip each straight centreline to the header's horizontal land span.
        # Only centreline pieces wholly above the pad lands count as passing
        # tracks; short joining stubs within the lands are not free-space rails.
        gaps=[]
        for track in b.GetTracks():
            x0,y0=p.ToMM(track.GetStart().x),p.ToMM(track.GetStart().y)
            x1,y1=p.ToMM(track.GetEnd().x),p.ToMM(track.GetEnd().y)
            if abs(x1-x0)<1e-8:
                if not left<=x0<=right:continue
                low,high=0.,1.
            else:
                a,c=sorted(((left-x0)/(x1-x0),(right-x0)/(x1-x0)))
                low,high=max(0.,a),min(1.,c)
                if low>high:continue
            ys=[y0+(y1-y0)*t for t in (low,high)]
            if max(ys)<pad_top-.01:
                gaps.append(pad_top-max(ys)-p.ToMM(track.GetWidth())/2)
        assert gaps,ref
        gap=min(gaps)
        assert gap>=.8-1e-5,(ref,gap)
        headers[ref]={'anchor_mm':[x,19],'restored_to_P6':True,
            'minimum_vertical_gap_from_pad_top_to_passing_track_mm':round(gap,3)}
    for name in ['current_mirror','dual_current_mirror']:
        board=p.LoadBoard(str(ROOT/(name+'.kicad_pcb')))
        assert abs(p.ToMM(board.GetDesignSettings().GetBoardThickness())-1.7)<1e-5
    setup=json.loads((ROOT/'centre_cut_setup.json').read_text())
    assert setup['user_reported_board_thickness_mm']==1.7
    assert setup['user_reported_cutter_diameter_mm']==.8
    assert setup['user_reported_maximum_depth_per_pass_mm']==.4
    assert setup['nominal_depths_below_top_surface_to_board_bottom_mm']==[.4,.8,1.2,1.6,1.7]
    report={'result':'PASS','revision':'P8-rectangles','headers':headers,'physical_board_thickness_mm':1.7,
        'centre_cut_setup':'User-reported dimensions recorded; machine program pending missing operator settings.'}
    (ROOT/'reports/header_space.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
