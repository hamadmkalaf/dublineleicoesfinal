# Monta o traçado da maratona de 2026 no grafo OSM ligando, na ordem do mapa oficial
# (IL_DM26_ROUTE_MAP_Updated.pdf), as ruas listadas em "Road Closures" (13/10/2026).
# Uso: python3 -I 2_percurso.py <esta pasta> ways.pkl percurso.json
import sys, json, re, math
sys.path.insert(0,sys.argv[1])
from grafo import *
ways,pos=carrega(sys.argv[2])
und=grafo_nao_dirigido(ways)
# ancoras do percurso, na ordem; (regex do nome, lat, lon aproximados)
A=[('^Leeson Street Lower$',53.3326,-6.2534),('^Leeson Street Lower$',53.3355,-6.2565),
('^St\\. Stephen\'s Green$',53.3370,-6.2600),('^Cuffe Street$',53.3377,-6.2645),('^Kevin Street Lower$',53.3380,-6.2675),
('^Kevin Street Upper$',53.3385,-6.2710),('^Patrick Street$',53.3400,-6.2717),('^Nicholas Street$',53.3425,-6.2716),
('^High Street$',53.3430,-6.2735),('^Bridge Street Upper$',53.3437,-6.2755),('^Bridge Street Lower$',53.3447,-6.2760),
('^Merchant\'s Quay$',53.3451,-6.2735),('^O\'Donovan Rossa Bridge$',53.3455,-6.2720),('^Inns Quay$',53.3460,-6.2745),
('^Arran Quay$',53.3465,-6.2785),('^Ellis Quay$',53.3470,-6.2825),('^Blackhall Place$',53.3485,-6.2820),
('^Stoneybatter$',53.3505,-6.2825),('^Manor Street$',53.3520,-6.2845),('^Aughrim Street$',53.3540,-6.2880),
('^North Circular Road$',53.3555,-6.2950),('^North Road$',53.3580,-6.3050),('^Spa Road$',53.3570,-6.3070),
('^Lords Walk$',53.3560,-6.3090),('^Chesterfield Avenue$',53.3600,-6.3200),('^Chesterfield Avenue$',53.3680,-6.3450),
('^Castleknock Road$',53.3710,-6.3470),('^College Road$',53.3700,-6.3560),('^Tower Road$',53.3600,-6.3580),('^Knockmaroon (Road|Hill)$',53.3580,-6.3530),
('^Upper Glen Road$',53.3520,-6.3430),('^Chapelizod Gate$',53.3470,-6.3370),('^Chapelizod Road$',53.3470,-6.3300),("^Saint Laurence's Road$",53.3450,-6.3400),
('^Sarsfield Road$',53.3425,-6.3300),('^Inchicore Road$',53.3420,-6.3130),('^South Circular Road$',53.3396,-6.3077),('^South Circular Road$',53.3387,-6.2999),('^South Circular Road$',53.3357,-6.2962),
('^Dolphin\'s Barn$',53.3325,-6.2920),('^Crumlin Road$',53.3280,-6.3050),('^Drimnagh Road$',53.3245,-6.3220),
('^Walkinstown Road$',53.3210,-6.3300),('^Cromwellsfort Road$',53.3170,-6.3260),('^Kimmage Road West$',53.3130,-6.3060),
('^Fortfield Road$',53.3080,-6.3010),('^Fortfield Road$',53.3036,-6.2992),('^Templeogue Road$',53.3023,-6.2965),('^Templeogue Road$',53.3067,-6.2893),('^Terenure Road East$',53.3110,-6.2790),
('^Orwell Road$',53.3090,-6.2680),('^Orwell Park$',53.3085,-6.2640),('^Dartry Road$',53.3110,-6.2615),
('^Milltown Road$',53.3092,-6.2497),('^Milltown Road$',53.3135,-6.2469),('^Milltown Road$',53.3185,-6.2425),('^Clonskeagh Road$',53.3160,-6.2405),('^Clonskeagh Road$',53.3100,-6.2385),('^Roebuck Road$',53.3030,-6.2280),
("^Foster's Avenue$",53.3010,-6.2140),("^Foster's Avenue$",53.3020,-6.2095),('^Nutley Lane$',53.3160,-6.2180),
('^Merrion Road$',53.3200,-6.2150),('^Merrion Road$',53.3270,-6.2260),('^Pembroke Road$',53.3300,-6.2330),
('^Northumberland Road$',53.3340,-6.2380),('^Northumberland Road$',53.3368,-6.2405),('^Warrington Place$',53.3368,-6.2420),('^Mount Street Upper$',53.3376,-6.2460)]
byname={}
def ancora(rx,la,lo):
    r=re.compile(rx); best=None
    for wid,w in ways.items():
        if not w['drive'] or not r.search(w['name']): continue
        for n,a,b in w['nodes']:
            d=hav((la,lo),(a,b))
            if best is None or d<best[0]: best=(d,n,w['name'])
    return best
anc=[]
for rx,la,lo in A:
    b=ancora(rx,la,lo)
    if b is None or b[0]>400: print('ANCORA RUIM',rx,b); 
    anc.append(b[1]); 
course=[]  # list of (node, wayid)
for a,b in zip(anc,anc[1:]):
    c,p=dijkstra(und,[a],{b},peso=1)
    if p is None: print('sem caminho',a,b); continue
    if course: course.pop()
    course+=p
nodes=[n for n,w in course]
tot=sum(hav(pos[a],pos[b]) for a,b in zip(nodes,nodes[1:]))
print('percurso m',round(tot), 'nos',len(nodes))
names=[]
for n,w in course:
    nm=ways[w]['name'] if w else ''
    if not names or names[-1]!=nm: names.append(nm)
print(' > '.join(names))
json.dump({'course':[(n,w) for n,w in course],'pos':{n:pos[n] for n in nodes}},open(sys.argv[3],'w'))
