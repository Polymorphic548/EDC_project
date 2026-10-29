"""Conservative one-copper-layer grid routing; no vias or automatic rule exclusions.

This is a small project-specific router, not a replacement for KiCad DRC.
Run after build_design.py, then validate using kicad-cli pcb drc.
"""
from pathlib import Path
import heapq, math, json, random, time
import numpy as np
import pcbnew as pcb
import build_design as design

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'current_mirror.kicad_pcb'
STEP=.25
WIDTH=.6
CLEAR=.4
NX,NY=337,289

def xy(p): return (pcb.ToMM(p.x),pcb.ToMM(p.y))
def cell(p): return tuple(round(v/STEP) for v in p)
def dilate(mask,point,radius):
    x,y=point; r=math.ceil(radius/STEP)
    x0,x1=max(0,x-r),min(NX,x+r+1); y0,y1=max(0,y-r),min(NY,y+r+1)
    xs=np.arange(x0,x1)[:,None]; ys=np.arange(y0,y1)[None,:]
    mask[x0:x1,y0:y1] |= (xs-x)**2+(ys-y)**2 <= (radius/STEP)**2

def astar(start,goal,blocked):
    if blocked[start] or blocked[goal]: return None
    # Four-way moves make clear, printable 90-degree paths.
    heap=[(abs(start[0]-goal[0])+abs(start[1]-goal[1]),0,start)]
    prev={}; best={start:0}; popped=0
    while heap:
        _,g,u=heapq.heappop(heap)
        if best.get(u)!=g: continue
        if u==goal:
            path=[u]
            while u!=start: u=prev[u]; path.append(u)
            return path[::-1]
        popped+=1
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            v=(u[0]+dx,u[1]+dy)
            if not (0<=v[0]<NX and 0<=v[1]<NY) or blocked[v]: continue
            ng=g+1
            if ng<best.get(v,10**9):
                best[v]=ng; prev[v]=u
                h=abs(v[0]-goal[0])+abs(v[1]-goal[1])
                heapq.heappush(heap,(ng+h,ng,v))
    return None

def simplify(path):
    if len(path)<3:return path
    out=[path[0]]
    for a,b,c in zip(path,path[1:],path[2:]):
        if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]): out.append(b)
    out.append(path[-1]); return out

def main():
    # Avoid KiCad 10 SWIG track-removal lifetime faults: strip serialized
    # segments before loading, rather than deleting C++ track objects in Python.
    tree=design.parse(FILE.read_text(encoding='utf-8'))
    tree=[x for x in tree if not (isinstance(x,list) and x and x[0] in ('segment','via','arc'))]
    scratch=ROOT/'reports/router_input.kicad_pcb'
    scratch.write_text(design.dump(tree),encoding='utf-8')
    b=pcb.LoadBoard(str(scratch))
    scratch.unlink()
    pads=[]; nets={}
    for f in b.GetFootprints():
        for p in f.Pads():
            item={'net':p.GetNetname(),'point':xy(p.GetPosition()),'size':xy(p.GetSize()),'shape':p.GetShape(),'angle':p.GetOrientationDegrees(),'ref':f.GetReference(),'pin':p.GetNumber()}
            pads.append(item); nets.setdefault(p.GetNetname(),[]).append(item)
    static={}
    X=np.arange(NX)[:,None]*STEP; Y=np.arange(NY)[None,:]*STEP
    for net in nets:
        mask=np.broadcast_to((X<4)|(X>80)|(Y<4)|(Y>69),(NX,NY)).copy()
        for p in pads:
            if p['net']==net:continue
            px,py=p['point']; w,h=p['size']; a=math.radians(p['angle'])
            dx=(X-px)*math.cos(a)+(Y-py)*math.sin(a)
            dy=-(X-px)*math.sin(a)+(Y-py)*math.cos(a)
            extra=WIDTH/2+CLEAR+.09
            if p['shape']==pcb.PAD_SHAPE_CIRCLE:
                mask |= (X-px)**2+(Y-py)**2 <= (w/2+extra)**2
            else:
                # Rounded Minkowski expansion of rectangular pads.
                mask |= np.maximum(np.abs(dx)-w/2,0)**2+np.maximum(np.abs(dy)-h/2,0)**2 <= extra**2
        static[net]=mask
    # Electrical pad pairs, minimum spanning tree per net.
    edges={}
    for net,ps in nets.items():
        reached=[0]; pending=set(range(1,len(ps))); es=[]
        while pending:
            dist,i,j=min((math.dist(ps[i]['point'],ps[j]['point']),i,j) for i in reached for j in pending)
            es.append((ps[i],ps[j])); reached.append(j); pending.remove(j)
        edges[net]=es
    seedorder=['/'+n for n in ['PROT_A','ZD_A','D12','TRIM_TOP','E1','E2','BASE','VA','OUT','VIN','VCC','GND']]
    bestcount=-1; best=None
    for attempt in range(50):
        order=seedorder.copy()
        if attempt:
            rng=random.Random(97+attempt)
            rng.shuffle(order)
        routed=[]; copper={n:np.zeros((NX,NY),dtype=bool) for n in nets}; count=0; failed=None
        for net in order:
            blocked=static[net].copy()
            for other,mask in copper.items():
                if other!=net:blocked|=mask
            for a,c in edges[net]:
                path=astar(cell(a['point']),cell(c['point']),blocked)
                if path is None: failed=(net,a['ref']+'.'+a['pin'],c['ref']+'.'+c['pin']); break
                routed.append((net,a,c,path)); count+=1
                for p in path: dilate(copper[net],p,WIDTH+CLEAR+.11)
            if failed:break
        if count>bestcount:
            bestcount=count; best=routed
            print(f'Routing attempt {attempt}: {count}/{sum(map(len,edges.values()))} connections; blocked={failed}',flush=True)
        if not failed: break
    if failed:
        raise RuntimeError(f'No complete single-layer route; best={bestcount}. Adjust placement before continuing.')
    for net,a,c,path in routed:
        points=[a['point']]+[(x*STEP,y*STEP) for x,y in simplify(path)]+[c['point']]
        for u,v in zip(points,points[1:]):
            if math.dist(u,v)<.0001:continue
            t=pcb.PCB_TRACK(b); t.SetStart(pcb.VECTOR2I(pcb.FromMM(u[0]),pcb.FromMM(u[1]))); t.SetEnd(pcb.VECTOR2I(pcb.FromMM(v[0]),pcb.FromMM(v[1]))); t.SetWidth(pcb.FromMM(WIDTH)); t.SetLayer(pcb.B_Cu); t.SetNetCode(b.FindNet(net).GetNetCode()); b.Add(t)
    pcb.SaveBoard(str(FILE),b)
    report={'status':'ROUTED - FIXED R7 120 OHM, NO TRIMMER','revision':'P2','layer':'B.Cu only','track_width_mm':WIDTH,'design_clearance_mm':CLEAR,'vias':0,'wire_jumpers':0,'pad_pair_routes':len(routed),'grid_mm':STEP,'routing_attempt':attempt,'note':'KiCad DRC must be run separately; this report is not a fabrication release.'}
    (ROOT/'reports/routing.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report),flush=True)

if __name__=='__main__': main()
