# Para cada origem e cada horário (15 em 15 min), o caminho de carro mais rápido até a
# Donnybrook Road passando por cada uma das portas de chegada, com os fechamentos de
# fechamentos.py. Premissas: percurso fechado não se cruza; N11 aberta salvo o corredor de
# ônibus, sem entrada lateral no trecho Foster's Ave–Nutley Lane; velocidades de fluxo livre.
# Uso: python3 -I 3_acessos.py <esta pasta> ways.pkl percurso.json origens.json saida.json <horas, -1 = dia normal>
import sys,json,pickle,collections,math,re
sys.path.insert(0,sys.argv[1])
from grafo import *; from fechamentos import *
ways,pos=carrega(sys.argv[2]); P=json.load(open(sys.argv[3])); ORIG=json.load(open(sys.argv[4]))
adj=grafo_carro(ways)
# janela de cada aresta do percurso (sem nome herda a anterior)
course=[(int(n),w) for n,w in P['course']]
edges=[]; last=None
for (a,w),(b,_) in zip(course,course[1:]):
    nm=ways[w]['name'] if w else ''
    if re.search(ABERTAS_NO_PERCURSO,nm): edges.append((a,b,None,nm)); last=None; continue
    j=janela(nm,PERCURSO) if nm else None
    if j is None: j=last
    if j is None and nm: print('SEM JANELA',nm)
    edges.append((a,b,j,nm)); last=j
n11=set(n for w in ways.values() if w['name']=='Stillorgan Road' for n,_,_ in w['nodes'])
ini,fim=course[0][0],course[-1][0]
locais=[]
for wid,w in ways.items():
    if not w['drive']: continue
    j=janela(w['name'],LOCAIS)
    if not j: continue
    la=sum(n[1] for n in w['nodes'])/len(w['nodes']); lo=sum(n[2] for n in w['nodes'])/len(w['nodes'])
    if BBOX_LOCAIS[0]<la<BBOX_LOCAIS[1] and BBOX_LOCAIS[2]<lo<BBOX_LOCAIS[3]:
        ns=[n for n,_,_ in w['nodes']]
        for a,b in zip(ns,ns[1:]): locais.append((a,b,j))
N11_TRECHO=set(n for n in n11 if 53.3030<=pos[n][0]<=53.3142)
LATERAIS=[]
for wid,w in ways.items():
    if not w['drive'] or w['name']=='Stillorgan Road': continue
    ns=[n for n,_,_ in w['nodes']]
    for a,b in zip(ns,ns[1:]):
        if a in N11_TRECHO or b in N11_TRECHO: LATERAIS.append((a,b))
def bloqueio(t):
    if t is None: return frozenset(),frozenset()
    nos=set(); ar=set()
    if 9.25<=t<17:
        for a,b in LATERAIS: ar.add((a,b)); ar.add((b,a))
    for a,b,j,nm in edges:
        if j and j[0]<=t<j[1]:
            for x in (a,b):
                if x not in n11 and x not in (ini,fim): nos.add(x)
            ar.add((a,b)); ar.add((b,a))
    for a,b,j in locais:
        if j[0]<=t<j[1]: ar.add((a,b)); ar.add((b,a))
    return frozenset(nos),frozenset(ar)
DR=set(n for w in ways.values() if w['name']=='Donnybrook Road' and w['hw']!='service' for n,_,_ in w['nodes'])
# no de partida: no mais proximo, com saida, fora de nos bloqueados
allnodes=[n for n in adj if adj[n]]
def mais_proximo(la,lo,proib):
    best=None
    for n in allnodes:
        if n in proib: continue
        p=pos[n]
        if abs(p[0]-la)>0.01 or abs(p[1]-lo)>0.016: continue
        d=hav((la,lo),p)
        if best is None or d<best[0]: best=(d,n)
    return best[1]
def dijkstra_full(src,proib,arp):
    dist={src:0}; prev={}; pq=[(0,src)]
    while pq:
        c,u=heapq.heappop(pq)
        if c>dist[u]: continue
        for v,d,s,w in adj.get(u,()):
            if v in proib or (u,v) in arp: continue
            nc=c+s
            if nc<dist.get(v,1e18): dist[v]=nc; prev[v]=(u,w); heapq.heappush(pq,(nc,v))
    return dist,prev
def resumo(prev,alvo,src):
    seq=[]; u=alvo; m=0
    while u!=src:
        if u not in prev: break
        p,w=prev[u]; seq.append((w,hav(pos[p],pos[u]))); u=p
    seq.reverse()
    # agrega por nome (ou ref) com metragem
    out=[]
    for w,d in seq:
        nm=ways[w]['name'] or ways[w]['ref'] or '(sem nome)'
        if out and out[-1][0]==nm: out[-1][1]+=d
        else: out.append([nm,d])
    km=sum(d for _,d in out)/1000
    principais=[nm for nm,d in out if d>=250]
    return km,principais

PORTAS=[('Norte','Morehampton Road (de Leeson St Upper)','Morehampton Road',53.3265,-6.2437),
 ('Norte','Marlborough Road (de Ranelagh/Sandford)','Marlborough Road',53.3235,-6.2440),
 ('Norte/Leste','Herbert Park (de Ballsbridge)','Herbert Park',53.3270,-6.2365),
 ('Leste','Anglesea Road (de Ballsbridge)','Anglesea Road',53.3260,-6.2310),
 ('Leste','Ailesbury Road (da Merrion Rd)','Ailesbury Road',53.3200,-6.2240),
 ('Sul','Stillorgan Road / N11 (de UCD)','Stillorgan Road',53.3172,-6.2283),
 ('Oeste','Beaver Row (de Clonskeagh)','Beaver Row',53.3175,-6.2345),
 ('Oeste','Eglinton Road (de Milltown/Ranelagh)','Eglinton Road',53.3190,-6.2400),
 ('Oeste','Belmont Avenue (de Sandford Rd)','Belmont Avenue',53.3212,-6.2410)]
rev=collections.defaultdict(list)
for u,l in adj.items():
    for v,d,s_,w in l: rev[v].append((u,d,s_,w))
def portas_arestas():
    out=[]
    for reg,rot,nm,la,lo in PORTAS:
        best=None
        for u,l in adj.items():
            pu=pos[u]
            if abs(pu[0]-la)>0.003 or abs(pu[1]-lo)>0.005: continue
            for v,d,s_,w in l:
                if ways[w]['name']!=nm: continue
                pm=((pu[0]+pos[v][0])/2,(pu[1]+pos[v][1])/2); dd=hav(pm,(la,lo))
                if best is None or dd<best[0]-1: best=(dd,[(u,v,s_,w)])
                elif abs(dd-best[0])<1: best[1].append((u,v,s_,w))
        if best is None or best[0]>150: print('PORTA RUIM',rot,best and best[0]); continue
        out.append((reg,rot,best[1]))
    return out
PA=portas_arestas(); print('portas',[(r,len(e)) for _,r,e in PA])
def dij(g,srcs,proib,arp,reverso=False):
    dist={}; prev={}; pq=[]
    for s0 in srcs:
        if s0 in proib: continue
        dist[s0]=0; pq.append((0,s0))
    heapq.heapify(pq)
    while pq:
        c,u=heapq.heappop(pq)
        if c>dist[u]: continue
        for v,d,s_,w in g.get(u,()):
            if v in proib: continue
            if (reverso and (v,u) in arp) or (not reverso and (u,v) in arp): continue
            nc=c+s_
            if nc<dist.get(v,1e18): dist[v]=nc; prev[v]=(u,w); heapq.heappush(pq,(nc,v))
    return dist,prev
def nomes(seq):
    out=[]
    for w,d in seq:
        nm=ways[w]['name'] or ways[w]['ref'] or ''
        if not nm: continue
        if out and out[-1][0]==nm: out[-1][1]+=d
        else: out.append([nm,d])
    return out
TEMPOS=[None if x=="-1" else float(x) for x in sys.argv[6].split(",")]
cache={}
res=[]
for t in TEMPOS:
    proib,arp=bloqueio(t)
    dto,nxt=dij(rev,DR,proib,arp,reverso=True)
    for o in ORIG:
        src=mais_proximo(o['lat'],o['lon'],proib)
        dist,prev=dij(adj,[src],proib,arp)
        portas={}
        for reg,rot,arestas in PA:
            best=None
            for u,v,s_,w in arestas:
                if u in proib or v in proib or (u,v) in arp: continue
                if u in dist and v in dto:
                    c=dist[u]+s_+dto[v]
                    if best is None or c<best[0]: best=(c,u,v,w)
            if not best: continue
            c,u,v,w=best
            seq=[]; x=u
            while x!=src: p,ww=prev[x]; seq.append((ww,hav(pos[p],pos[x]))); x=p
            seq.reverse(); seq.append((w,hav(pos[u],pos[v]))); x=v
            while x not in DR: p,ww=nxt[x]; seq.append((ww,hav(pos[x],pos[p]))); x=p
            ns=nomes(seq); km=sum(d for _,d in ns)/1000
            portas[rot]=dict(regiao_porta=reg,min=round(c/60,1),km=round(km,1),via=[n for n,d in ns if d>=300])
        res.append(dict(regiao=o['regiao'],origem=o['nome'],hora=t,portas=portas))
    print('hora',t,flush=True)
json.dump(res,open(sys.argv[5],'w'),ensure_ascii=False)
