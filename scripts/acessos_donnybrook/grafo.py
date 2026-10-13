import pickle, math, heapq, collections
def hav(a,b):
    R=6371000; la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    d=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(d))
SPEED={'motorway':100,'motorway_link':60,'trunk':60,'trunk_link':40,'primary':45,'primary_link':35,
 'secondary':40,'secondary_link':30,'tertiary':35,'tertiary_link':30,'unclassified':30,'residential':25,
 'living_street':10,'road':25,'service':15}
def carrega(p):
    ways=pickle.load(open(p,'rb'))
    pos={}
    for w in ways.values():
        for n,la,lo in w['nodes']: pos[n]=(la,lo)
    return ways,pos
def grafo_carro(ways):
    """arestas dirigidas: adj[u] -> list of (v, seg_m, seg_s, wayid)"""
    adj=collections.defaultdict(list)
    for wid,w in ways.items():
        if not w['drive']: continue
        if w['access'] in ('private','no') or w['motor'] in ('private','no'): continue
        if w['hw']=='service': continue
        ow=w['oneway']; fwd=True; back=True
        if ow in ('yes','1','true') or w['junction'] in ('roundabout','circular') or w['hw'] in ('motorway',) : back=False
        if ow=='-1': fwd=False
        if ow=='no': back=True
        v=SPEED[w['hw']]/3.6
        ns=w['nodes']
        for (a,la,lo),(b,lb,lob) in zip(ns,ns[1:]):
            d=hav((la,lo),(lb,lob))
            if fwd: adj[a].append((b,d,d/v,wid))
            if back: adj[b].append((a,d,d/v,wid))
    return adj
def grafo_nao_dirigido(ways):
    adj=collections.defaultdict(list)
    for wid,w in ways.items():
        if not w['drive']: continue
        if w['hw']=='service': continue
        ns=w['nodes']
        for (a,la,lo),(b,lb,lob) in zip(ns,ns[1:]):
            d=hav((la,lo),(lb,lob)); adj[a].append((b,d,d,wid)); adj[b].append((a,d,d,wid))
    return adj
def dijkstra(adj,src,alvos,proibidos=frozenset(),arestas_proib=frozenset(),peso=2):
    """src: iterable of nodes; alvos: set. retorna (custo, caminho de (no, wayid))"""
    dist={}; prev={}; pq=[]
    for s in src:
        if s in proibidos: continue
        dist[s]=0; heapq.heappush(pq,(0,s))
    while pq:
        c,u=heapq.heappop(pq)
        if c>dist.get(u,1e18): continue
        if u in alvos:
            path=[(u,None)]
            while u in prev:
                p,w=prev[u]; path.append((p,w)); u=p
            path.reverse()
            # path: list of (node, wayid used to leave this node)
            out=[]
            for i in range(len(path)-1): out.append((path[i][0],path[i+1][1]))
            out.append((path[-1][0],None))
            return c,out
        for e in adj.get(u,()):
            v=e[0]
            if v in proibidos or (u,v) in arestas_proib: continue
            nc=c+e[peso]
            if nc<dist.get(v,1e18):
                dist[v]=nc; prev[v]=(u,e[3]); heapq.heappush(pq,(nc,v))
    return None,None
