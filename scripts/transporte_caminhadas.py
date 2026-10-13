import json, sys, urllib.request, time
G=(53.32578,-6.23124); M=(53.32830,-6.22920)
stops = {
 '774':('Donnybrook (Garda Station)',53.321612,-6.2355),
 '758':('Victoria Avenue',53.3226869,-6.2376774),
 '759':('Donnybrook Stadium',53.320349,-6.233346),
 '773':('Donnybrook Stadium (sentido cidade)',53.319916,-6.233273),
 '757':('Donnybrook Village',53.324081,-6.239586),
 '775':('Donnybrook Village (sentido cidade)',53.3234897,-6.2390854),
 '776':('Morehampton Terrace',53.325479,-6.241736),
 '760':('Donnybrook Depot',53.31833,-6.230562),
 '772':('Donnybrook Depot (sentido cidade)',53.318485,-6.231321),
 '761':('Teresian School (sentido UCD)',53.3161,-6.227487),
 '771':('Teresian School (terminal 39A pos-11h)',53.31588,-6.227781),
 '883':('Eglinton Road',53.317685,-6.241036),
 '416':('RDS Ballsbridge (sentido Blackrock)',53.3286399,-6.2293696),
 '485':('RDS Ballsbridge (sentido cidade)',53.328252,-6.228635),
 '417':('Merrion Road (Embaixada)',53.3277,-6.22597),
 '855':('Sandford Road (11/44)',None,None),
 '884':('Norwood Park (11/44)',None,None),
 '7739':('Park Avenue, Sandymount (47/C1/C2)',None,None),
 '7740':('Park Avenue, Sandymount (47/C1/C2)',None,None),
 '753':('Waterloo Road',None,None),
 '7333':('Mespil Hotel',None,None),
 '2808':('Sandymount Station (ponto onibus)',53.326811,-6.223065),
 'DART-SMT':('Estacao DART Sandymount',53.327928,-6.2210505),
 'DART-LDR':('Estacao DART Lansdowne Road',53.3337709,-6.2287109),
 '2798':('Pembroke Road',53.331999,-6.235882),
}
# completa coordenadas a partir do json do gtfs
d=json.load(open(sys.argv[1]))
for e in d['linhas']:
    p=e['parada_mais_proxima']
    if p['codigo'] in stops and stops[p['codigo']][1] is None:
        stops[p['codigo']]=(stops[p['codigo']][0],p['lat'],p['lon'])
out={}
for code,(name,lat,lon) in stops.items():
    if lat is None: print('sem coord',code); continue
    row={'nome':name,'lat':lat,'lon':lon}
    for tag,dest in (('anglesea',G),('merrion',M)):
        url=f"https://routing.openstreetmap.de/routed-foot/route/v1/foot/{lon},{lat};{dest[1]},{dest[0]}?overview=false"
        req=urllib.request.Request(url,headers={'User-Agent':'eleicoes-dublin-logistica/1.0 (hamadmkalaf@gmail.com)'})
        try:
            r=json.load(urllib.request.urlopen(req,timeout=40))['routes'][0]
            row[tag+'_m']=round(r['distance']); row[tag+'_min']=round(r['distance']/80,1)  # 80 m/min = 4,8 km/h
        except Exception as ex:
            row[tag+'_m']=None; row[tag+'_err']=str(ex)
        time.sleep(0.5)
    out[code]=row
    print(f"{code:9} {name[:40]:40} Anglesea {row.get('anglesea_m')} m ({row.get('anglesea_min')} min) | Merrion {row.get('merrion_m')} m ({row.get('merrion_min')} min)")
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
