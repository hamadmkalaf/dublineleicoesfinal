"""Gera mapa/linhas_maratona.html a partir de shapes_linhas.json, geometrias_mapa.json e nom_rds.json.
uso: python3 -I scripts/transporte_mapa_linhas.py <pasta com os json> mapa/linhas_maratona.html
"""
import json, math, sys, html
S=sys.argv[1]; OUT=sys.argv[2]
shapes=json.load(open(f'{S}/shapes_linhas.json')); geo=json.load(open(f'{S}/geometrias_mapa.json'))
rds=json.load(open(f'{S}/nom_rds.json'))[0]['geojson']['coordinates'][0]
LAT0,LAT1,LON0,LON1=53.303,53.346,-6.262,-6.198
K=20000; CX=math.cos(math.radians(53.325))
def P(la,lo): return (round((lo-LON0)*CX*K,1), round((LAT1-la)*K,1))
W=round((LON1-LON0)*CX*K); H=round((LAT1-LAT0)*K)
def path(pts, close=False):
    d=' '.join(('M' if i==0 else 'L')+f'{x},{y}' for i,(x,y) in enumerate(P(la,lo) for la,lo in pts))
    return d+(' Z' if close else '')
def segs(key): return shapes[key]['segmentos']
def multipath(key): return ' '.join(path(s) for s in segs(key))

g=[]
# --- malha: todas as shapes em cinza
malha=' '.join(multipath(k) for k in shapes)
g.append(f'<path class="malha" d="{malha}"/>')
# --- RDS
g.append(f'<path class="rds" d="{path([(la,lo) for lo,la in rds],True)}"/>')
ar=[(53.3267,-6.2310),(53.3267,-6.2274),(53.3249,-6.2274),(53.3249,-6.2310)]
g.append(f'<path class="rds" d="{path(ar,True)}"/>')
# --- maratona
g.append(f'<path class="maratona-halo" d="{path(geo["maratona"]["pts"])}"/>')
g.append(f'<path class="maratona" d="{path(geo["maratona"]["pts"])}"/>')
# --- corredor de desvio 14/11/44 (halo) + eixo E1/E2/39A
g.append(f'<path class="corredor" d="{path(geo["corredor_donnybrook"]["pts"])}"/>')
g.append(f'<path class="linha eixo" d="{multipath("E1|0")}"/>')
# 44 normal (Appian Way/Ranelagh) e 11/14 normais ficam na malha; 11B terminal
# --- 4 normal, 7/7A normal
g.append(f'<path class="linha l4" d="{multipath("4|0")}"/>')
g.append(f'<path class="linha l7" d="{multipath("7|0")}"/>')
# --- desvio 4/7/7A
g.append(f'<path class="linha desvio" d="{path(geo["desvio_4_7_7A"]["pts"])}"/>')
# --- caminhadas
for k,cls in (('caminhada_774','cam'),('caminhada_416','cam cam2'),('caminhada_sandymount_dart','cam cam3')):
    g.append(f'<path class="{cls}" d="{path(geo[k]["pts"])}"/>')
# --- pontos
pts=[
 ('g',53.32578,-6.23124,'Portão Anglesea Road','gate'),
 ('m',53.32830,-6.22920,'Portão Merrion Road (não usar)','gate2'),
 ('774',53.321612,-6.2355,'774 Donnybrook (Garda) · 11 min','stop e'),
 ('758',53.3226869,-6.2376774,'758 Victoria Avenue · 12 min','stop e'),
 ('759',53.320349,-6.233346,'759 Donnybrook Stadium · 13 min','stop e'),
 ('771',53.31588,-6.227781,'771 Teresian School (terminal 39A após 11h) · 16 min','stop e2'),
 ('416',53.3286399,-6.2293696,'416/485 RDS Ballsbridge · 6 min (linha 4 só até ~10h)','stop o'),
 ('smt',53.327928,-6.2210505,'DART Sandymount — FECHADA 24–26/10','dart'),
 ('ldr',53.3337709,-6.2287109,'DART Lansdowne Road — FECHADA 24–26/10','dart'),
 ('sg',53.33276,-6.21521,'Sandymount (desvio 4/7/7A após 11h) · 21 min, cruza o percurso','stop d'),
]
for id_,la,lo,label,cls in pts:
    x,y=P(la,lo)
    short={'g':'portão Anglesea','m':'portão Merrion','774':'774','758':'758','759':'759','771':'771','416':'416/485 RDS','smt':'DART Sandymount (fechada)','ldr':'DART Lansdowne Rd (fechada)','sg':'Sandymount'}[id_]
    dx,dy={'g':(12,22),'m':(12,18),'774':(-30,-12),'758':(-34,-12),'759':(10,16),'771':(10,16),'416':(12,-8),'smt':(12,16),'ldr':(12,-8),'sg':(10,18)}[id_]
    g.append(f'<g class="pt {cls}" id="pt-{id_}"><circle cx="{x}" cy="{y}" r="7"/><title>{html.escape(label)}</title><text class="ptl" x="{x+dx}" y="{y+dy}">{html.escape(short)}</text></g>')
# --- rótulos de rua (posição e rotação à mão)
labels=[
 ('Merrion Road',53.3238,-6.2208,-40),('Anglesea Road',53.3236,-6.2328,-52),('Donnybrook Road',53.3192,-6.2318,-33),
 ('Stillorgan Road · N11',53.3100,-6.2235,-32),('Nutley Lane',53.3145,-6.2160,-75),('Pembroke Road',53.3322,-6.2370,-40),
 ('Northumberland Road',53.3360,-6.2422,-55),('Strand Road',53.3245,-6.2082,-60),('Leeson Street',53.3312,-6.2515,-40),
 ('Morehampton Road',53.3268,-6.2445,-40),('Sandymount',53.3330,-6.2150,0),('Ballsbridge',53.3300,-6.2335,0),
 ('Donnybrook',53.3222,-6.2395,0),('RDS',53.3272,-6.2272,0),('UCD',53.3075,-6.2240,0),('Ringsend',53.3410,-6.2290,0),
 ('Merrion Gates',53.3190,-6.2060,0),('Ranelagh',53.3260,-6.2560,0),
]
for t,la,lo,rot in labels:
    x,y=P(la,lo)
    cls='rua' if rot else 'lugar'
    g.append(f'<text class="{cls}" x="{x}" y="{y}" transform="rotate({rot} {x} {y})">{html.escape(t)}</text>')
# anotações de linhas
ann=[('E1 · E2 · 39A (e 14, 11, 44 no desvio)',53.3135,-6.2335,-33,'eixo'),('4 (até ~10h) · 7 · 7A (não rodam no dia)',53.3128,-6.2060,-48,'l4'),
     ('desvio 4 · 7 · 7A por Strand Road',53.3300,-6.2060,-62,'desvio'),('percurso da maratona',53.3212,-6.2172,-40,'mar'),
     ('11 min a pé',53.3238,-6.2345,-55,'camt')]
for t,la,lo,rot,cls in ann:
    x,y=P(la,lo); g.append(f'<text class="ann {cls}" x="{x}" y="{y}" transform="rotate({rot} {x} {y})">{html.escape(t)}</text>')
# escala 500 m
x0,y0=P(53.3045,-6.2600); x1,_=P(53.3045,-6.2600+500/(111320*CX))
g.append(f'<g class="escala"><line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}"/><text x="{x0}" y="{y0-6}">500 m</text></g>')
svg='\n'.join(g)

page=f'''<title>Linhas até o RDS na maratona</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@87.5,400;87.5,600;87.5,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
/* layout: um mapa SVG georreferenciado ocupa a largura; cenários acima, legenda e caminhadas abaixo */
:root{{--bg:#f6f4ee;--fg:#1f2a24;--muted:#5f6b63;--rule:#d9d4c7;--malha:#cfc9bb;--rds:#e4dfd0;
--eixo:#1b7a3d;--corredor:#bfe3c8;--l4:#d9781a;--l7:#b4342d;--mar:#6b3fa0;--marhalo:#d9c8ef;--cam:#1f2a24;--dart:#8a8f8a;--card:#fffdf8}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#161a17;--fg:#ece9df;--muted:#a7aea5;--rule:#333a35;--malha:#3a413c;--rds:#2a3029;
--eixo:#4fc46f;--corredor:#1f4a2b;--l4:#f0973c;--l7:#e8655c;--mar:#b48ae6;--marhalo:#3b2a57;--cam:#ece9df;--dart:#7d837e;--card:#1e2320;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#161a17;--fg:#ece9df;--muted:#a7aea5;--rule:#333a35;--malha:#3a413c;--rds:#2a3029;
--eixo:#4fc46f;--corredor:#1f4a2b;--l4:#f0973c;--l7:#e8655c;--mar:#b48ae6;--marhalo:#3b2a57;--cam:#ece9df;--dart:#7d837e;--card:#1e2320;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:"Source Serif 4",Georgia,serif;padding-block:20px;padding-inline:16px;max-width:1040px;margin:0 auto}}
h1{{font-family:Archivo,"Helvetica Neue",Arial,sans-serif;font-stretch:87.5%;font-weight:700;font-size:1.6rem;margin:0 0 4px;text-wrap:balance}}
.sub{{color:var(--muted);margin:0 0 14px;max-width:65ch;font-size:.95rem}}
.cen{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}}
.cen button{{font-family:Archivo,sans-serif;font-stretch:87.5%;font-weight:600;font-size:.9rem;padding:8px 14px;border:1px solid var(--rule);background:var(--card);color:var(--fg);border-radius:4px;cursor:pointer}}
.cen button[aria-pressed="true"]{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.cen button:focus-visible{{outline:2px solid var(--eixo);outline-offset:2px}}
.nota{{font-family:Archivo,sans-serif;font-stretch:87.5%;font-size:.9rem;color:var(--muted);min-height:2.4em;margin:0 0 10px;max-width:70ch}}
.mapa{{width:100%;max-width:100%;overflow:hidden;border:1px solid var(--rule);background:var(--card)}}
svg{{display:block;width:100%;height:auto}}
.malha{{fill:none;stroke:var(--malha);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.rds{{fill:var(--rds);stroke:var(--rule);stroke-width:1}}
.maratona-halo{{fill:none;stroke:var(--marhalo);stroke-width:16;stroke-linecap:round;stroke-linejoin:round}}
.maratona{{fill:none;stroke:var(--mar);stroke-width:3;stroke-dasharray:10 6;stroke-linejoin:round}}
.corredor{{fill:none;stroke:var(--corredor);stroke-width:14;stroke-linecap:round;stroke-linejoin:round}}
.linha{{fill:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}}
.eixo{{stroke:var(--eixo)}} .l4{{stroke:var(--l4)}} .l7{{stroke:var(--l7);stroke-width:3}} .desvio{{stroke:var(--l4);stroke-dasharray:9 7;stroke-width:3.5}}
.cam{{fill:none;stroke:var(--cam);stroke-width:2.5;stroke-dasharray:2 5;stroke-linecap:round}} .cam2{{stroke-width:1.8}} .cam3{{stroke-width:1.8;opacity:.6}}
.pt circle{{stroke:var(--card);stroke-width:2.5}}
.pt.e circle{{fill:var(--eixo)}} .pt.e2 circle{{fill:var(--eixo);r:5}} .pt.o circle{{fill:var(--l4)}} .pt.d circle{{fill:var(--l4);r:5}}
.pt.gate circle{{fill:var(--fg);r:10;stroke:var(--eixo);stroke-width:4}} .pt.gate2 circle{{fill:none;stroke:var(--fg);stroke-width:2;r:8;stroke-dasharray:3 3}}
.pt.dart circle{{fill:var(--dart);r:8}}
text{{font-family:Archivo,sans-serif;font-stretch:87.5%;fill:var(--fg)}}
.rua{{font-size:11px;fill:var(--muted);letter-spacing:.02em}} .lugar{{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;fill:var(--muted);text-anchor:middle}}
.ann{{font-size:12.5px;font-weight:600;paint-order:stroke;stroke:var(--card);stroke-width:4;stroke-linejoin:round}}
.ann.eixo{{fill:var(--eixo)}} .ann.l4{{fill:var(--l4)}} .ann.desvio{{fill:var(--l4)}} .ann.mar{{fill:var(--mar)}} .ann.camt{{fill:var(--cam)}}
.ptl{{font-size:11px;font-weight:600;paint-order:stroke;stroke:var(--card);stroke-width:3.5;stroke-linejoin:round}} .pt.dart .ptl{{fill:var(--dart)}} svg.normal .pt.dart .ptl{{display:none}}
.escala line{{stroke:var(--fg);stroke-width:2}} .escala text{{font-size:11px}}
/* cenários */
svg.normal .desvio, svg.normal .maratona, svg.normal .maratona-halo, svg.normal .corredor, svg.normal .ann.desvio, svg.normal .ann.mar{{display:none}}
svg.normal .pt.dart circle{{fill:var(--eixo)}}
svg.manha .corredor{{opacity:.55}} svg.manha .l7{{stroke:var(--malha)}} svg.manha .pt.d{{display:none}}
svg.tarde .l4,svg.tarde .l7{{stroke:var(--malha)}} svg.tarde .ann.l4{{fill:var(--muted)}} svg.tarde .pt.o circle{{fill:var(--malha)}}
svg.manha .ann.l4,svg.tarde .ann.l4{{}}
.leg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:6px 20px;margin:14px 0 0;padding:0;list-style:none;font-family:Archivo,sans-serif;font-stretch:87.5%;font-size:.88rem}}
.leg li{{display:flex;align-items:center;gap:10px;min-width:0}} .sw{{flex:none;width:34px;height:0;border-top:4px solid}}
.sw.dash{{border-top-style:dashed}} .sw.dot{{border-top:3px dotted var(--cam)}} .sw.band{{height:10px;background:var(--marhalo);border:0}} .sw.cor{{height:10px;background:var(--corredor);border:0}}
.sw.ring{{width:14px;height:14px;border-radius:50%;background:var(--fg);border:3px solid var(--eixo)}} .sw.pin{{width:12px;height:12px;border-radius:50%;border:0}}
h2{{font-family:Archivo,sans-serif;font-stretch:87.5%;font-size:1.05rem;margin:22px 0 8px}}
table{{border-collapse:collapse;width:100%;font-family:Archivo,sans-serif;font-stretch:87.5%;font-size:.88rem;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);vertical-align:top}} th{{color:var(--muted);font-weight:600;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}}
td.n{{text-align:right;white-space:nowrap}}
.tw{{overflow-x:auto}}
.fonte{{color:var(--muted);font-size:.82rem;margin-top:16px;max-width:75ch}}
@media (prefers-reduced-motion:no-preference){{.linha,.pt circle{{transition:stroke .25s,fill .25s,opacity .25s}}}}
</style>
<h1>Linhas de ônibus até o RDS no dia da maratona</h1>
<p class="sub">Domingo 25/10/2026, 2º turno, 8h–17h. Portão de eleitores na Anglesea Road. Traçados do GTFS da NTA (06/10), desvios do aviso da Dublin Bus (07/10), fechamentos da Garda (18/9) e caminhadas medidas no OpenStreetMap.</p>
<div class="cen" role="group" aria-label="Cenário">
<button type="button" id="b-normal" data-cen="normal" aria-pressed="false">Dia normal</button>
<button type="button" id="b-manha" data-cen="manha" aria-pressed="true">25/10 · até 11h</button>
<button type="button" id="b-tarde" data-cen="tarde" aria-pressed="false">25/10 · a partir de 11h</button>
</div>
<p class="nota" id="nota"></p>
<div class="mapa"><svg class="manha" viewBox="0 0 {W} {H}" role="img" aria-label="Mapa das linhas de ônibus ao redor do RDS, Ballsbridge e Donnybrook">
{svg}
</svg></div>
<ul class="leg">
<li><span class="sw" style="border-color:var(--eixo)"></span>E1 · E2 · 39A pela Donnybrook Road (E2 e 39A só após 11h)</li>
<li><span class="sw cor"></span>Corredor de desvio da 14, 11 e 44 (paradas não confirmadas)</li>
<li><span class="sw" style="border-color:var(--l4)"></span>Linha 4 pela Merrion Road (até o fechamento, 9h40–11h)</li>
<li><span class="sw" style="border-color:var(--l7)"></span>7 e 7A, rota normal: não rodam por aqui em 25/10</li>
<li><span class="sw dash" style="border-color:var(--l4)"></span>Desvio de 4, 7 e 7A por Ringsend, Sandymount e Strand Road</li>
<li><span class="sw band"></span>Percurso da maratona (Merrion Road fechada 9h40–17h30)</li>
<li><span class="sw dot"></span>Caminhada medida até o portão</li>
<li><span class="sw ring"></span>Portão da Anglesea Road (ponto assumido)</li>
<li><span class="sw pin" style="background:var(--eixo)"></span>Paradas 774, 758, 759 confirmadas pela prefeitura</li>
<li><span class="sw pin" style="background:var(--dart)"></span>Estações DART fechadas de 24 a 26/10</li>
<li><span class="sw" style="border-color:var(--malha)"></span>Outras ruas com ônibus (traçados do GTFS)</li>
</ul>
<h2>Caminhada de cada parada ao portão da Anglesea Road</h2>
<div class="tw"><table>
<tr><th>Parada</th><th>Linhas no dia</th><th class="n">Distância</th><th class="n">Tempo a 4,8 km/h</th><th>Cruza o percurso?</th></tr>
<tr><td>774 Donnybrook (Garda Station)</td><td>E1 o dia todo; E2, 39A, 11B após 11h</td><td class="n">884 m</td><td class="n">11 min</td><td>Não</td></tr>
<tr><td>758 Victoria Avenue</td><td>E1 o dia todo; E2, 39A, 11B após 11h</td><td class="n">932 m</td><td class="n">12 min</td><td>Não</td></tr>
<tr><td>759 Donnybrook Stadium</td><td>E1 o dia todo; E2, 39A, 11B após 11h</td><td class="n">1.025 m</td><td class="n">13 min</td><td>Não</td></tr>
<tr><td>771 Teresian School</td><td>39A (terminal após 11h)</td><td class="n">1.256 m</td><td class="n">16 min</td><td>Não</td></tr>
<tr><td>416 / 485 RDS Ballsbridge</td><td>4, só até o fechamento da Merrion Road</td><td class="n">438 m</td><td class="n">6 min</td><td>Está no percurso</td></tr>
<tr><td>Sandymount (desvio de 4/7/7A)</td><td>4, 7, 7A após 11h</td><td class="n">1.664 m</td><td class="n">21 min</td><td>Sim</td></tr>
<tr><td>DART Sandymount</td><td>Sem trens em 25/10</td><td class="n">921 m</td><td class="n">12 min</td><td>Sim</td></tr>
</table></div>
<p class="fonte">O ponto do portão é o meio da testada do RDS Arena na Anglesea Road, premissa até o RDS confirmar. O percurso da maratona e os desvios foram traçados sobre a malha viária do OpenStreetMap a partir das descrições por escrito; os traçados de linha são os do GTFS. Fonte dos dados e método em <code>conflito com maratona/ranking_linhas_rds.md</code>.</p>
<script>
(function(){{
var notas={{normal:"Dia normal: 4, 7 e 7A param na porta do RDS (Merrion Road); E1, E2, 39A e 11B passam por Donnybrook, a 11–13 min a pé do portão da Anglesea.",
manha:"Até 11h em 25/10: só a E1 serve Donnybrook (vinda do sul, até Sussex Road). A 4 roda pela Merrion Road até o fechamento (9h40 pelo organizador, 10h pela Garda, 11h pela Dublin Bus). 7 e 7A já estão desviadas por Strand Road. DART sem trens em Sandymount e Lansdowne Road.",
tarde:"A partir de 11h: E1, E2 e 39A a cada ~15 min por Donnybrook, mais 11B, 14, 11 e 44 no mesmo corredor. 4, 7 e 7A seguem por Ringsend e Strand Road, do outro lado do percurso. Merrion Road fechada até 17h30."}};
var svg=document.querySelector('svg'),nota=document.getElementById('nota'),bs=document.querySelectorAll('.cen button');
function set(c){{svg.setAttribute('class',c);nota.textContent=notas[c];bs.forEach(function(b){{b.setAttribute('aria-pressed',String(b.dataset.cen===c));}});try{{localStorage.setItem('cen',c);}}catch(e){{}}}}
bs.forEach(function(b){{b.addEventListener('click',function(){{set(b.dataset.cen);}});}});
var c='manha';try{{c=localStorage.getItem('cen')||c;}}catch(e){{}} if(!notas[c])c='manha'; set(c);
}})();
</script>
'''
open(OUT,'w').write(page); print('ok',W,H,len(page))
