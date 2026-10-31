"""Two rotated, isolated header-equipped units on a 150 x 100 mm blank.

Run after build_design.py and route_board.py. No routing is shared between units.
The flat panel schematic uses A_/B_ local net labels and +100 reference numbers
for copy B. The reusable unit project remains current_mirror.kicad_pro.
"""
from pathlib import Path
import copy,json,csv,re
import pcbnew as p
import build_design as d

ROOT=d.ROOT
NAME='dual_current_mirror'
ROOT_ID=d.uid('dual-panel-schematic')
COPIES={'A':(2.5,92),'B':(74.5,92)}
def reference(ref,unit):
    if unit=='A':return ref
    m=re.fullmatch(r'([A-Za-z]+)(\d+)',ref);assert m,ref
    return m[1]+str(int(m[2])+100)
def renamed_text(text,unit):
    return re.sub(r'\b(?:'+ '|'.join(re.escape(x[0]) for x in d.PARTS)+r')\b',lambda m:reference(m[0],unit),text)
def transform(pt,unit):
    x,y=pt;tx,ty=COPIES[unit]
    return (y+tx,-x+ty)
def native_pt(pt):return d.pos(*pt)
def mm_pt(pt):return (p.ToMM(pt.x),p.ToMM(pt.y))

def schematic():
    tree=d.parse((ROOT/'current_mirror.kicad_sch').read_text(encoding='utf-8'))
    out=['kicad_sch',['version','20250114'],['generator',d.q('pcb_layout_script')],['uuid',ROOT_ID],['paper',d.q('A2')],
         ['title_block',['title',d.q('Two isolated current mirrors - 150 x 100 mm panel')],['rev',d.q('P5 - SOLDER CLEARANCE')]],copy.deepcopy(d.child(tree,'lib_symbols'))]
    def walk(node,unit,dx,dy):
        if not isinstance(node,list) or not node:return
        if node[0] in ('at','xy') and len(node)>=3:
            node[1]=str(round(float(node[1])+dx,4));node[2]=str(round(float(node[2])+dy,4))
        elif node[0]=='uuid':node[1]=d.uid(unit+'/'+node[1])
        elif node[0]=='label':node[1]=d.q(unit+'_'+d.val(node[1]))
        elif node[0]=='text':node[1]=d.q(renamed_text(d.val(node[1]),unit))
        elif node[0]=='property' and d.val(node[1]) in ('Reference','Value'):
            node[2]=d.q(renamed_text(d.val(node[2]),unit))
        for x in node:
            if isinstance(x,list):walk(x,unit,dx,dy)
    for unit,dx in [('A',0),('B',284.48)]:
        for item in tree:
            if not isinstance(item,list) or item[0] not in ('symbol','wire','label','junction','text','no_connect'):continue
            node=copy.deepcopy(item)
            oldref=None
            if node[0]=='symbol':oldref=next(d.val(x[2]) for x in d.children(node,'property') if d.val(x[1])=='Reference')
            walk(node,unit,dx,15.24)
            if oldref:
                instances=d.child(node,'instances');node.remove(instances)
                node.append(['instances',['project',d.q(NAME),['path',d.q('/'+ROOT_ID),['reference',d.q(reference(oldref,unit))],['unit','1']]]])
            out.append(node)
        title=f'COPY {unit}: '+('Q1 / Q2; J1 power; J2 load; J3/J4 Vbe' if unit=='A' else 'Q101 / Q102; J101 power; J102 load; J103/J104 Vbe')
        out.append(['text',d.q(title),['at',str(20+dx),'15','0'],['effects',['font',['size','1.7','1.7']],['justify','left']],['uuid',d.uid('heading'+unit)]])
    out.append(['text',d.q('A_ and B_ nets are separate, including GND. No copper or power rail is shared between the two copies.'),['at','20','215','0'],['effects',['font',['size','1.5','1.5']],['justify','left']],['uuid',d.uid('isolation-note')]])
    (ROOT/(NAME+'.kicad_sch')).write_text(d.dump(out),encoding='utf-8')

def board():
    unit_board=p.LoadBoard(str(ROOT/'current_mirror.kicad_pcb'))
    b=p.BOARD();b.SetCopperLayerCount(2)
    nets={}
    for unit in COPIES:
        for f in unit_board.GetFootprints():
            for pad in f.Pads():
                name='/'+unit+'_'+pad.GetNetname().lstrip('/')
                if name not in nets:
                    n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
    manifest=[]
    angle=p.EDA_ANGLE(90,p.DEGREES_T)
    for unit,(tx,ty) in COPIES.items():
        for original in unit_board.GetFootprints():
            f=p.FOOTPRINT(original);b.Add(f)
            oldref=original.GetReference();newref=reference(oldref,unit)
            f.Rotate(d.pos(0,0),angle);f.Move(d.pos(tx,ty))
            f.SetReference(newref);f.SetValue(renamed_text(original.GetValue(),unit))
            f.SetPath(p.KIID_PATH('/'+ROOT_ID+'/'+d.uid(unit+'/'+d.uid(oldref))))
            for pad in f.Pads():
                oldnet=next(x.GetNetname() for x in original.Pads() if x.GetNumber()==pad.GetNumber())
                pad.SetNet(nets['/'+unit+'_'+oldnet.lstrip('/')])
            manifest.append({'unit':unit,'reference':newref,'unit_reference':oldref,'value':f.GetValue(),'position_mm':mm_pt(f.GetPosition()),'nets':{pad.GetNumber():pad.GetNetname() for pad in f.Pads()}})
        for original in unit_board.GetTracks():
            assert isinstance(original,p.PCB_TRACK) and not isinstance(original,p.PCB_VIA)
            t=p.PCB_TRACK(b);t.SetStart(native_pt(transform(mm_pt(original.GetStart()),unit)));t.SetEnd(native_pt(transform(mm_pt(original.GetEnd()),unit)))
            t.SetWidth(original.GetWidth());t.SetLayer(p.B_Cu);t.SetNet(nets['/'+unit+'_'+original.GetNetname().lstrip('/')]);b.Add(t)
        for original in unit_board.GetDrawings():
            item=p.PCB_TEXT(original) if isinstance(original,p.PCB_TEXT) else p.PCB_SHAPE(original)
            b.Add(item)
            item.Rotate(d.pos(0,0),angle);item.Move(d.pos(tx,ty))
            if item.GetLayer()==p.Edge_Cuts:item.SetLayer(p.Dwgs_User)
            if isinstance(item,p.PCB_TEXT):item.SetText(renamed_text(item.GetText(),unit))
        d.text(b,'COPY '+unit,39 if unit=='A' else 111,7,1.5)
    for a,c in [((0,0),(150,0)),((150,0),(150,100)),((150,100),(0,100)),((0,100),(0,0))]:
        s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(d.pos(*a));s.SetEnd(d.pos(*c));s.SetLayer(p.Edge_Cuts);s.SetWidth(d.mm(.05));b.Add(s)
    # Separation guide is documentation only, never copper or a routed slot.
    guide=p.PCB_SHAPE();guide.SetShape(p.SHAPE_T_SEGMENT);guide.SetStart(d.pos(75,5));guide.SetEnd(d.pos(75,95));guide.SetLayer(p.Dwgs_User);guide.SetWidth(d.mm(.15));b.Add(guide)
    d.text(b,'150 x 100 mm - TWO ISOLATED COPIES',75,96,1.2)
    p.SaveBoard(str(ROOT/(NAME+'.kicad_pcb')),b)
    # Duplicate() can retain UUIDs in some KiCad versions. Give every footprint
    # and child a unique panel identity; schematic paths are kept unchanged.
    tree=d.parse((ROOT/(NAME+'.kicad_pcb')).read_text(encoding='utf-8'))
    def identity(node,ref):
        if not isinstance(node,list) or not node:return
        if node[0]=='uuid':node[1]=d.uid('panel/'+ref+'/'+node[1])
        for x in node:
            if isinstance(x,list):identity(x,ref)
    for fp in d.children(tree,'footprint'):
        ref=next(d.val(x[2]) for x in d.children(fp,'property') if d.val(x[1])=='Reference')
        identity(fp,ref)
    for index,item in enumerate(tree):
        if isinstance(item,list) and item[0]!='footprint':identity(item,'root-'+str(index))
    (ROOT/(NAME+'.kicad_pcb')).write_text(d.dump(tree),encoding='utf-8')
    project_path=ROOT/(NAME+'.kicad_pro')
    pro=json.loads((project_path if project_path.exists() else ROOT/'current_mirror.kicad_pro').read_text())
    pro['board']['design_settings']['rules']['min_clearance']=.8
    for cls in pro['net_settings']['classes']:cls['clearance']=max(.8,cls.get('clearance',0))
    pro.setdefault('meta',{})['filename']=NAME+'.kicad_pro'
    pro['sheets']=[];pro.setdefault('schematic',{})['top_level_sheets']=[]
    (ROOT/(NAME+'.kicad_pro')).write_text(json.dumps(pro,indent=2),encoding='utf-8')
    (ROOT/'panel_components.json').write_text(json.dumps(manifest,indent=2))
    with (ROOT/'panel_BOM.csv').open('w',newline='',encoding='utf-8-sig') as file:
        w=csv.writer(file);w.writerow(['Copy','Reference','Unit reference','Value','Notes'])
        for x in manifest:w.writerow([x['unit'],x['reference'],x['unit_reference'],x['value'],'R7 measurement reported for original part only; measure each assembled copy separately' if x['unit_reference']=='R7' else ''])
    print('Built dual_current_mirror: 150x100mm; two rotated 67x78mm units; 5mm gap.',flush=True)

if __name__=='__main__':schematic();board()
