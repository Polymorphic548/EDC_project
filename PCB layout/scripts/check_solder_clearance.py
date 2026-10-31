"""Check P6 solder-land geometry, lead fit and rules in both isolated copies.

Native KiCad DRC separately checks actual routed copper clearance/connectivity.
"""
from pathlib import Path
import json, math
import pcbnew as p
import build_design as d

ROOT=d.ROOT

def main():
    b=p.LoadBoard(str(ROOT/'dual_current_mirror.kicad_pcb'))
    footprints={f.GetReference():f for f in b.GetFootprints()}
    result={}
    for copy,offset in [('A',0),('B',100)]:
        lands={}
        for prefix,numbers in [('J',range(1,5)),('Q',range(1,3))]:
            for number in numbers:
                ref=prefix+str(number+offset)
                pads=sorted(footprints[ref].Pads(),key=lambda pad:int(pad.GetNumber()))
                sizes=[(p.ToMM(pad.GetSize().x),p.ToMM(pad.GetSize().y)) for pad in pads]
                expected=(2.4,1.7) if prefix=='J' else (1.7,2.4)
                assert all(all(abs(a-c)<1e-5 for a,c in zip(size,expected)) for size in sizes),ref
                drill=1.0 if prefix=='J' else .8
                # Preserve the actual stock transistor drill (0.8 mm).
                assert all(abs(p.ToMM(pad.GetDrillSize().x)-drill)<1e-5 for pad in pads),ref
                distances=[math.dist((p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)),
                                     (p.ToMM(c.GetPosition().x),p.ToMM(c.GetPosition().y)))
                           for a,c in zip(pads,pads[1:])]
                assert all(abs(distance-2.54)<1e-5 for distance in distances),ref
                assert pads[0].GetShape()==(p.PAD_SHAPE_RECT if prefix=='J' else p.PAD_SHAPE_OVAL)
                assert all(pad.GetShape()==p.PAD_SHAPE_OVAL for pad in pads[1:])
                lands[ref]={'pin_pitch_mm':2.54,'land_size_local_mm':list(expected),
                            'adjacent_land_gap_mm':.84,'drill_mm':drill,
                            'minimum_annular_copper_mm':round((1.7-drill)/2,3)}
        # The two neighbouring diode pairs highlighted in the review drawing.
        gaps={}
        for left,right in [(('D3','2'),('D1','2')),(('D1','1'),('D2','2'))]:
            def pad_at(item):
                base,pin=item;ref='D'+str(int(base[1:])+offset)
                return next(pad for pad in footprints[ref].Pads() if pad.GetNumber()==pin)
            a,c=pad_at(left),pad_at(right)
            distance=math.dist((p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)),
                               (p.ToMM(c.GetPosition().x),p.ToMM(c.GetPosition().y)))
            gap=distance-(p.ToMM(a.GetSize().x)+p.ToMM(c.GetSize().x))/2
            assert gap>=1.5,(copy,left,right,gap)
            gaps[left[0]+'.'+left[1]+' to '+right[0]+'.'+right[1]]=round(gap,3)
        result[copy]={'headers_and_transistors':lands,'neighbouring_diode_pad_gaps_mm':gaps}
    for name in ['current_mirror','dual_current_mirror']:
        pro=json.loads((ROOT/(name+'.kicad_pro')).read_text())
        assert pro['board']['design_settings']['rules']['min_clearance']==.8
        assert all(cls['clearance']>=.8 for cls in pro['net_settings']['classes'])
    report={'result':'PASS','revision':'P6-restored','minimum_configured_copper_clearance_mm':.8,
            'track_width_mm':.6,'copies':result,
            'note':'Pin spacing and drills preserved; pad lands elongated perpendicular to pin row. No solder mask. Careful soldering still required.'}
    (ROOT/'reports/solder_clearance.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
