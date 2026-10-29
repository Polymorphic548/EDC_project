"""Rebuild the provisional project with KiCad 10's bundled Python. No GUI required."""
from pathlib import Path
import json, re, uuid, math, sys, struct
import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[1]
INSTALL = Path(sys.executable).resolve().parents[1]
SHARE = INSTALL / 'share/kicad'
NAME = 'current_mirror'
NS = uuid.UUID('bb1a8583-3b3d-4b90-a3b8-e8d541ee27d1')
def uid(s): return str(uuid.uuid5(NS, s))
def q(s): return json.dumps(str(s))
def mm(v): return pcb.FromMM(v)
def pos(x,y): return pcb.VECTOR2I(mm(x),mm(y))

RFP = 'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal'
DFP = 'Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal'
QFP = 'Package_TO_SOT_THT:TO-92_Inline_Wide'
TPFP = 'TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm'
TRIMMER_FP = 'RV1_D9_P8_Offset5_PINOUT_UNVERIFIED'
TRIMMER_PINS = {'1':(-4.0,0.0), '3':(4.0,0.0), '2':(0.0,5.0)}
# These are provisional pad roles, NOT an identification of the actual wiper.
# Pin-view measurements are symmetric about x=0; the board top view may swap
# left/right. Identify the real wiper and check orientation before fabrication.
# ref, value, symbol, footprint, pin-to-net map, board x/y/angle, schematic x/y
PARTS = [
 ('J1','12V INPUT','Connector_Generic:Conn_01x02','Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',{'1':'VIN','2':'GND'},(8,10,0),(25.4,40.64)),
 ('R1','1R (LT F1)','Device:R',RFP,{'1':'VIN','2':'PROT_A'},(16,10,0),(50.8,40.64)),
 ('D4','1N4007','Device:D','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',{'1':'VCC','2':'PROT_A'},(38,10,180),(76.2,40.64)),
 ('C1','100n / >=25V','Device:C','Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm',{'1':'VCC','2':'GND'},(70,13,0),(101.6,40.64)),
 ('R2','620R (LT Rs)','Device:R',RFP,{'1':'VCC','2':'VA'},(29,24,270),(25.4,76.2)),
 ('D3','BZX55C5V1','Device:D_Zener',DFP,{'1':'VA','2':'ZD_A'},(29,35,270),(50.8,76.2)),
 ('D1','1N4148','Device:D',DFP,{'1':'D12','2':'ZD_A'},(29,53,90),(76.2,76.2)),
 ('D2','1N4148','Device:D',DFP,{'1':'GND','2':'D12'},(29,64,90),(101.6,76.2)),
 ('R3','1k (LT R1a)','Device:R',RFP,{'1':'VA','2':'TRIM_TOP'},(43,20,270),(139.7,40.64)),
 ('RV1','500R TRIM / set ~119.8R','Device:R_Potentiometer','Project:'+TRIMMER_FP,{'1':'TRIM_TOP','2':'BASE','3':'BASE'},(49,38,0),(139.7,76.2)),
 ('Q1','2N3904','Transistor_BJT:Q_NPN_EBC',QFP,{'1':'E1','2':'BASE','3':'BASE'},(45,50,0),(177.8,40.64)),
 ('Q2','2N3904','Transistor_BJT:Q_NPN_EBC',QFP,{'1':'E2','2':'BASE','3':'OUT'},(59,50,0),(215.9,40.64)),
 ('R4','22R (LT Re1)','Device:R',RFP,{'1':'E1','2':'GND'},(45,58,270),(177.8,76.2)),
 ('R5','22R (LT Re2)','Device:R',RFP,{'1':'E2','2':'GND'},(59,58,270),(215.9,76.2)),
 ('R6','1k (LT Rload)','Device:R',RFP,{'1':'VCC','2':'OUT'},(64,25,270),(241.3,40.64)),
 ('TP1','GND','Connector:TestPoint',TPFP,{'1':'GND'},(75,60,0),(25.4,114.3)),
 ('TP2','VIN','Connector:TestPoint',TPFP,{'1':'VIN'},(8,20,0),(50.8,114.3)),
 ('TP3','VCC / LOAD+','Connector:TestPoint',TPFP,{'1':'VCC'},(53,10,0),(76.2,114.3)),
 ('TP4','VA','Connector:TestPoint',TPFP,{'1':'VA'},(20,32,0),(101.6,114.3)),
 ('TP5','BASE','Connector:TestPoint',TPFP,{'1':'BASE'},(73,49,0),(139.7,114.3)),
 ('TP6','OUT / LOAD-','Connector:TestPoint',TPFP,{'1':'OUT'},(73,38,0),(177.8,114.3)),
]
# Publish the etching-oriented pad changes as project-local footprints, rather
# than silently changing copies of the stock library footprints.
STOCK_FOOTPRINTS={part[0]:part[3] for part in PARTS}
PARTS=[(*part[:3], 'Project:'+(TRIMMER_FP if part[0]=='RV1' else part[0]+'_ETCH'), *part[4:]) for part in PARTS]

def parse(s):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s)
    stack=[]; root=None
    for t in tokens:
        if t=='(':
            a=[]
            if stack: stack[-1].append(a)
            stack.append(a)
        elif t==')':
            root=stack.pop()
        else: stack[-1].append(t)
    return root
def dump(a): return '('+' '.join(dump(x) if isinstance(x,list) else x for x in a)+')'
def children(a,k): return [x for x in a if isinstance(x,list) and x and x[0]==k]
def child(a,k): return next(iter(children(a,k)),None)
def val(t): return json.loads(t) if t.startswith('"') else t

def library_symbol(libid):
    lib,name=libid.split(':')
    tree=parse((SHARE/'symbols'/f'{lib}.kicad_sym').read_text(encoding='utf-8'))
    sym=next(x for x in children(tree,'symbol') if val(x[1])==name)
    assert not child(sym,'extends'), libid
    sym[1]=q(libid)
    return sym

def write_schematic():
    libs={p[2]:library_symbol(p[2]) for p in PARTS}
    rootid=uid('schematic')
    out=[f'(kicad_sch (version 20250114) (generator "pcb_layout_script") (uuid {rootid}) (paper "A4")',
         '(title_block (title "5 mA diode-compensated current mirror") (rev "P1 - VERIFY RV1 WIPER") (comment 1 "Exact LTspice connectivity; added power connector and voltage test points"))',
         '(lib_symbols '+' '.join(dump(s) for s in libs.values())+')']
    for ref,value,lib,fp,nets,board,(x,y) in PARTS:
        sid=uid(ref)
        out.append(f'(symbol (lib_id {q(lib)}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {sid})')
        for prop,pv,px,py,hide in [('Reference',ref,x+5.08,y-5.08,False),('Value',value,x+5.08,y-2.54,False),('Footprint',fp,x,y,True)]:
            out.append(f'(property {q(prop)} {q(pv)} (at {px} {py} 0) (effects (font (size 1.0 1.0)) (justify left) {"(hide yes)" if hide else ""}))')
        pins=[]
        for sub in children(libs[lib],'symbol'): pins+=children(sub,'pin')
        for pin in pins:
            n=val(child(pin,'number')[1]); at=child(pin,'at'); dx,dy,angle=map(float,at[1:4]); px,py=x+dx,y-dy
            out.append(f'(pin {q(n)} (uuid {uid(ref+"-pin-"+n)}))')
            # Stubs point away from symbol body; labels sit at the outer end.
        out.append(f'(instances (project "{NAME}" (path "/{rootid}" (reference {q(ref)}) (unit 1)))))')
        for pin in pins:
            n=val(child(pin,'number')[1]); at=child(pin,'at'); dx,dy,angle=map(float,at[1:4]); px,py=x+dx,y-dy
            a=math.radians(angle); ex=round(px-5.08*math.cos(a),4); ey=round(py+5.08*math.sin(a),4)
            out.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {uid(ref+"wire"+n)}))')
            out.append(f'(label {q(nets[n])} (at {ex} {ey} 0) (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid {uid(ref+"label"+n)}))')
    notes=[(20,20,'SUPPLY: J1 -> R1 -> D4 -> VCC. R1 is a resistor, not a fuse.'),
           (20,145,'RV1: 500 ohm; ~119.8 ohm nominal setting. Pad 2 + 3 tied; actual wiper identification PENDING.'),
           (20,153,'P1 PROVISIONAL: RV1 measured geometry fitted; verify actual wiper/pin mapping before fabrication.'),
           (20,161,'Measure V(TP3)-V(TP6) across R6: approximately 5 V means approximately 5 mA (nominal 1k load).'),
           (20,169,'LT names: R1=F1, R2=Rs, R3=R1a, R4=Re1, R5=Re2, R6=Rload, D3=Dz.'),
           (20,177,'All resistors 1/4 W. Labels with matching names are electrically connected.')]
    for x,y,t in notes: out.append(f'(text {q(t)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid(t)}))')
    out.append(')')
    (ROOT/f'{NAME}.kicad_sch').write_text('\n'.join(out),encoding='utf-8')

def text(board,s,x,y,size=1,layer=pcb.F_SilkS):
    t=pcb.PCB_TEXT(board); t.SetText(s); t.SetPosition(pos(x,y)); t.SetTextSize(pos(size,size)); t.SetTextThickness(mm(.15)); t.SetLayer(layer); board.Add(t)

def trimmer_footprint(board):
    """Measured geometry; pad numbering is provisional until wiper is tested."""
    f=pcb.FOOTPRINT(board); f.SetFPID(pcb.LIB_ID('Project',TRIMMER_FP)); f.SetAttributes(pcb.FP_THROUGH_HOLE)
    f.SetLibDescription('User-measured 9mm body, 8mm across pair, third pin offset 5mm. WIPER AND PAD ROLES UNVERIFIED. Drill 1.0mm assumed.')
    layers=pcb.LSET()
    for layer in (pcb.F_Cu,pcb.B_Cu,pcb.F_Mask,pcb.B_Mask): layers.AddLayer(layer)
    for number,(x,y) in TRIMMER_PINS.items():
        pad=pcb.PAD(f); pad.SetNumber(number); pad.SetAttribute(pcb.PAD_ATTRIB_PTH)
        pad.SetShape(pcb.PAD_SHAPE_RECT if number=='1' else pcb.PAD_SHAPE_CIRCLE)
        pad.SetSize(pos(2.4,2.4)); pad.SetDrillSize(pos(1,1)); pad.SetLayerSet(layers); pad.SetPosition(pos(x,y)); f.Add(pad)
    circle=pcb.PCB_SHAPE(); circle.SetShape(pcb.SHAPE_T_CIRCLE); circle.SetStart(pos(0,0)); circle.SetEnd(pos(4.5,0)); circle.SetLayer(pcb.F_Fab); circle.SetWidth(mm(.1)); f.Add(circle)
    for a,c in [((-5.5,-5),(5.5,-5)),((5.5,-5),(5.5,6.5)),((5.5,6.5),(-5.5,6.5)),((-5.5,6.5),(-5.5,-5))]:
        edge=pcb.PCB_SHAPE(); edge.SetShape(pcb.SHAPE_T_SEGMENT); edge.SetStart(pos(*a)); edge.SetEnd(pos(*c)); edge.SetLayer(pcb.F_CrtYd); edge.SetWidth(mm(.05)); f.Add(edge)
    # Existing reservation remains 40..58 by 31..45 in board coordinates.
    for a,c in [((-9,-7),(9,-7)),((9,-7),(9,7)),((9,7),(-9,7)),((-9,7),(-9,-7))]:
        edge=pcb.PCB_SHAPE(); edge.SetShape(pcb.SHAPE_T_SEGMENT); edge.SetStart(pos(*a)); edge.SetEnd(pos(*c)); edge.SetLayer(pcb.Dwgs_User); edge.SetWidth(mm(.2)); f.Add(edge)
    f.Reference().SetPosition(pos(0,-6.4)); f.Value().SetVisible(False)
    return f

def build_board():
    b=pcb.BOARD(); b.SetCopperLayerCount(2)
    netobjs={}
    for n in sorted({n for p in PARTS for n in p[4].values()}):
        net=pcb.NETINFO_ITEM(b,'/'+n); b.Add(net); netobjs[n]=net
    for ref,value,lib,fp,nets,(x,y,angle),sch in PARTS:
        if ref=='RV1':
            f=trimmer_footprint(b)
        else:
            libname,fpname=STOCK_FOOTPRINTS[ref].split(':'); f=pcb.FootprintLoad(str(SHARE/'footprints'/f'{libname}.pretty'),fpname); assert f,fp
        b.Add(f); f.SetReference(ref); f.SetValue(value); f.SetFPID(pcb.LIB_ID(*fp.split(':'))); f.SetPath(pcb.KIID_PATH('/'+uid('schematic')+'/'+uid(ref)))
        f.SetPosition(pos(x,y)); f.SetOrientationDegrees(angle)
        f.Reference().SetTextSize(pos(1,1)); f.Reference().SetTextThickness(mm(.15)); f.Value().SetVisible(False)
        if ref.startswith('TP'): f.SetAttributes(f.GetAttributes() & ~pcb.FP_EXCLUDE_FROM_BOM)
        if ref=='J1': f.Reference().SetPosition(pos(12,17))
        if ref in ('D1','D2','D3','C1'):
            for graphic in f.GraphicalItems():
                if graphic.GetLayer()==pcb.F_SilkS: graphic.SetLayer(pcb.F_Fab)
        for p in f.Pads():
            p.SetNet(netobjs[nets[p.GetNumber()]])
            if ref.startswith('R') and ref!='RV1' or ref in ('D1','D2','D3','D4','C1','J1'):
                p.SetSize(pos(2.2,2.2))
                if ref=='J1': p.SetSize(pos(2.0,2.0))
                # Preserve square pin 1 for polarity/numbering.
            if ref.startswith('TP'): p.SetSize(pos(2.8,2.8)); p.SetDrillSize(pos(1,1))
            if ref.startswith('Q'): p.SetSize(pos(2.0,2.0))
    for a,c in [((3,3),(81,3)),((81,3),(81,70)),((81,70),(3,70)),((3,70),(3,3))]:
        s=pcb.PCB_SHAPE(); s.SetShape(pcb.SHAPE_T_SEGMENT); s.SetStart(pos(*a)); s.SetEnd(pos(*c)); s.SetLayer(pcb.Edge_Cuts); s.SetWidth(mm(.05)); b.Add(s)
    text(b,'5 mA CURRENT MIRROR',43,5.7,1.2)
    text(b,'P1 - VERIFY RV1 WIPER',42,68,1.1)
    text(b,'RV1 PINOUT UNVERIFIED',49,33,0.8,pcb.Dwgs_User)
    text(b,'+12V',8,7.5,.85); text(b,'GND',8,16,.85)
    text(b,'GND',75,63,.85); text(b,'OUT',75,41,.85)
    text(b,'VCC',53,13,.85); text(b,'VA',20,35,.85); text(b,'BASE',73,52,.85)
    text(b,'BOTTOM COPPER ONLY',22,67,1,pcb.B_SilkS)
    for graphic in b.GetDrawings():
        if isinstance(graphic,pcb.PCB_TEXT) and graphic.GetLayer()==pcb.B_SilkS: graphic.SetMirrored(True)
    pcb.SaveBoard(str(ROOT/f'{NAME}.kicad_pcb'),b)
    # Keep the provisional footprint editable locally.
    save_local_footprints()

def save_local_footprints():
    fpdir=ROOT/'Project.pretty'; fpdir.mkdir(exist_ok=True)
    tree=parse((ROOT/f'{NAME}.kicad_pcb').read_text(encoding='utf-8'))
    for fs in children(tree,'footprint'):
        name=val(fs[1]).split(':')[-1]
        at=child(fs,'at'); angle=float(at[3]) if at and len(at)>3 else 0
        for item in fs:
            if not isinstance(item,list): continue
            localat=child(item,'at')
            if localat and len(localat)>3:
                localat[3]=str((float(localat[3])-angle)%360)
            if item[0]=='pad': item[:]=[x for x in item if not (isinstance(x,list) and x and x[0]=='net')]
        fs[1]=q(name)
        fs=[x for x in fs if not (isinstance(x,list) and x and x[0] in ('at','path','uuid','sheetname','sheetfile'))]
        fs[2:2]=[['version','20241229'],['generator','"pcb_layout_script"']]
        (fpdir/(name+'.kicad_mod')).write_text(dump(fs),encoding='utf-8')

def verify_source():
    """Extract LTspice connectivity independently from wire geometry + installed symbols."""
    src=ROOT.parent/'schematics/diode_comp_mirror_enhanced_v2.asc'
    lines=src.read_text().splitlines(); wires=[]; flags=[]; syms=[]
    for l in lines:
        a=l.split()
        if not a: continue
        if a[0]=='WIRE': wires.append(tuple(map(int,a[1:])))
        elif a[0]=='FLAG': flags.append((tuple(map(int,a[1:3])),a[3]))
        elif a[0]=='SYMBOL': syms.append({'sym':a[1],'x':int(a[2]),'y':int(a[3]),'rot':a[4]})
        elif a[:2]==['SYMATTR','InstName']: syms[-1]['ref']=a[2]
    symroot=Path.home()/'AppData/Local/LTspice/lib/sym'
    points=set(); terminal={}
    for s in syms:
        pins=[l.split() for l in (symroot/(s['sym']+'.asy')).read_text().splitlines() if l.startswith('PIN ')]
        for i,p in enumerate(pins,1):
            dx,dy=map(int,p[1:3]); r=s['rot']; assert r in ('R0','R180'),r
            if r=='R180': dx,dy=-dx,-dy
            pt=(s['x']+dx,s['y']+dy); points.add(pt); terminal[(s['ref'],str(i))]=pt
    points.update(pt for pt,n in flags)
    for x1,y1,x2,y2 in wires: points.update([(x1,y1),(x2,y2)])
    parent={p:p for p in points}
    def find(p):
        if parent[p]!=p: parent[p]=find(parent[p])
        return parent[p]
    def union(a,b): parent[find(a)]=find(b)
    for x1,y1,x2,y2 in wires:
        on=[p for p in points if min(x1,x2)<=p[0]<=max(x1,x2) and min(y1,y2)<=p[1]<=max(y1,y2) and (x1==x2 or y1==y2)]
        for p in on: union((x1,y1),p)
    named={}
    for pt,name in flags:
        if name in named: union(pt,named[name])
        else: named[name]=pt
    # Expected KiCad pin -> LTspice terminal; diode pin ordering is reversed.
    refs={'R1':'F1','R2':'Rs','R3':'R1a','R4':'Re1','R5':'Re2','R6':'Rload','D3':'Dz'}
    groups={}; expected={}
    for ref,v,lib,fp,nets,*_ in PARTS:
        if ref.startswith(('TP','J')): continue
        for pin,net in nets.items():
            if ref=='RV1' and pin=='3': continue
            lt_pin=({'1':'2','2':'1'}[pin] if ref.startswith('D') else {'1':'3','2':'2','3':'1'}[pin] if ref.startswith('Q') else pin)
            root=find(terminal[(refs.get(ref,ref),lt_pin)])
            groups.setdefault(root,[]).append(f'{ref}.{pin}'); expected.setdefault(root,set()).add(net)
    assert all(len(ns)==1 for ns in expected.values()),expected
    assert len({next(iter(s)) for s in expected.values()})==len(expected),'Unexpected source net split'
    assert next(iter(expected[find(terminal[('V1','1')])]))=='VIN'
    assert next(iter(expected[find(terminal[('V1','2')])]))=='GND'
    report={'result':'PASS','source':src.name,'source_electrical_nets':len(groups),'nets':{next(iter(expected[r])):sorted(pins) for r,pins in groups.items()},'notes':['J1 replaces ideal 12V source V1.','RV1 pin 3 tied to wiper pin 2; the two-terminal resistance is preserved.','Test points add no circuit components.']}
    (ROOT/'reports/source_connectivity.json').write_text(json.dumps(report,indent=2))
    print('Independent LTspice connectivity check: PASS',flush=True)

def write_project():
    pro={'meta':{'filename':NAME+'.kicad_pro','version':3},'board':{'design_settings':{'rules':{'min_clearance':.4,'min_track_width':.6,'min_through_hole_diameter':.7,'min_hole_clearance':.25,'min_copper_edge_clearance':.5}}},'net_settings':{'classes':[{'name':'Default','clearance':.4,'track_width':.6,'via_diameter':1.6,'via_drill':.8,'microvia_diameter':.3,'microvia_drill':.1,'diff_pair_width':.6,'diff_pair_gap':.4,'diff_pair_via_gap':.4,'wire_width':6,'bus_width':12,'line_style':0,'schematic_color':'rgba(0, 0, 0, 0.000)','pcb_color':'rgba(0, 0, 0, 0.000)'}],'meta':{'version':4}}}
    if not (ROOT/f'{NAME}.kicad_pro').exists():
        (ROOT/f'{NAME}.kicad_pro').write_text(json.dumps(pro,indent=2))
    (ROOT/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Project") (type "KiCad") (uri "${KIPRJMOD}/Project.pretty") (options "") (descr "Local etching footprints; RV1 measured geometry, wiper unverified")))\n')
    manifest=[{'reference':r,'value':v,'symbol':lib,'footprint':fp,'stock_footprint_basis':STOCK_FOOTPRINTS[r],'connections':nets,'position_mm':list(bp),'status':'MEASURED GEOMETRY - WIPER/PAD MAPPING UNVERIFIED - NOT FABRICABLE' if r=='RV1' else 'package assumption - confirm physical part'} for r,v,lib,fp,nets,bp,sp in PARTS]
    (ROOT/'components.json').write_text(json.dumps(manifest,indent=2))

if __name__=='__main__':
    verify_source(); write_project(); write_schematic(); build_board()
    print('Generated schematic, board, project, manifest, and source verification.',flush=True)
