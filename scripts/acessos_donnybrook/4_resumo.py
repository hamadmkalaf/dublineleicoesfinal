# Resume a saída de 3_acessos.py por origem e faixa de horário.
# Uso: python3 -I 4_resumo.py saida.json
import json,sys
R=json.load(open(sys.argv[1]))
CURTO={'Morehampton Road (de Leeson St Upper)':'Morehampton','Marlborough Road (de Ranelagh/Sandford)':'Marlborough','Herbert Park (de Ballsbridge)':'Herbert Park',
'Anglesea Road (de Ballsbridge)':'Anglesea','Ailesbury Road (da Merrion Rd)':'Ailesbury','Stillorgan Road / N11 (de UCD)':'N11','Beaver Row (de Clonskeagh)':'Beaver Row',
'Eglinton Road (de Milltown/Ranelagh)':'Eglinton','Belmont Avenue (de Sandford Rd)':'Belmont'}
CHAVE={'Strand Road','Beach Road','Booterstown Avenue','Woodbine Road','Rock Road','Charlemont Street','Grand Parade','Sussex Road','Leeson Street Upper','Leeson Street Lower','Ranelagh Road','Ranelagh','Shelbourne Road','Grand Canal Street Upper','Northumberland Road','Pembroke Road','Baggot Street Lower','Waterloo Road','Harcourt Street','Camden Street Upper','Rathmines Road Lower','Rathmines Road Upper','M50','N31','Stillorgan Road','Clonskeagh Road','Milltown Road','Merrion Road','Sean Moore Road','East Link Bridge','Tom Clarke Bridge','Dundrum Road','Mount Merrion Avenue','Taney Road','Churchtown Road Upper','Bird Avenue','Rathgar Road','Terenure Road North','Highfield Road','Dartry Road','Orwell Road','Kimmage Road Lower','Harold\'s Cross Road','Clanbrassil Street Upper','Leinster Road','Grove Road','Rathmines Road','Sandford Road','Belmont Avenue','Anglesea Road','Herbert Park','Morehampton Road','Eglinton Road','Mespil Road','Haddington Road','Lansdowne Road','Pembroke Street','Tritonville Road','Sydney Parade Avenue','Ailesbury Road','Merrion Gates','Nutley Lane','Simmonscourt Road','Booterstown','Rock Road','Seafort Avenue','Gilford Road','Sandymount Road','Beach Road','Londonbridge Road','Bath Avenue','South Lotts Road','Ringsend Road','Pearse Street','Westland Row','Lombard Street East','Cardiff Lane','Sir John Rogerson\'s Quay','Samuel Beckett Bridge','Matt Talbot Memorial Bridge','Talbot Memorial Bridge','East Wall Road','Port Tunnel','Dublin Port Tunnel'}
def hh(t): return 'normal' if t is None else f"{int(t)}h{int(round((t%1)*60)):02d}"
def corredor(via):
    c=[x for x in via if x in CHAVE]
    out=[]
    for x in c:
        if not out or out[-1]!=x: out.append(x)
    return ' > '.join(out[-6:])
por={}
for r in R: por.setdefault((r['regiao'],r['origem']),[]).append(r)
for (reg,o),lst in por.items():
    lst.sort(key=lambda r:-1 if r['hora'] is None else r['hora'])
    print(f"\n## {reg} · {o}")
    grupos=[]
    for r in lst:
        p=r['portas']
        if not p: key=('—','','') 
        else:
            k=min(p,key=lambda g:p[g]['min']); key=(CURTO[k],corredor(p[k]['via']))
        if grupos and grupos[-1][0]==key and r['hora'] is not None and grupos[-1][1][0]['hora'] is not None: grupos[-1][1].append(r)
        else: grupos.append((key,[r]))
    for key,rs in grupos:
        a=hh(rs[0]['hora']); b=hh(rs[-1]['hora']+0.25) if rs[-1]['hora'] is not None else ''
        mins=[min(x['min'] for x in r['portas'].values()) for r in rs if r['portas']]
        p=rs[len(rs)//2]['portas']; b0=min(x['min'] for x in p.values()) if p else 0
        alt=sorted(((CURTO[g],v['min']) for g,v in p.items() if CURTO[g]!=key[0] and v['min']<=b0+6),key=lambda x:x[1])
        alts=', '.join(f"{g} {m:.0f}" for g,m in alt[:4])
        print(f"  {a}{'–'+b if b else ''}: {key[0]} {min(mins):.0f}–{max(mins):.0f} min · {key[1]}" + (f"  | alt: {alts}" if alts else ''))
