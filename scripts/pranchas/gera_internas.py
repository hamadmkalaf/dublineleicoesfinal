# -*- coding: utf-8 -*-
"""Pecas internas do Hall 2 (P6, P7) e as duas plantas de posicionamento."""
import json, pathlib, math

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / 'saidas' / 'pranchas_sinalizacao' / 'project'

S = json.loads((REPO / 'saidas' / 'sinalizacao_v2.json').read_text(encoding='utf-8'))
R = json.loads((REPO / 'saidas' / 'ring3_montagem.json').read_text(encoding='utf-8'))
P = json.loads((REPO / 'data' / 'prancheta_hall2.json').read_text(encoding='utf-8'))

MM = 0.5
def mm(v): return round(v * MM, 1)

AMARELO='#F8C030'; MARINHO='#042B5A'; OFFW='#F0F0E8'
COR={'A':'#0B6E9E','B':'#B04E0A','C':'#4A7C1E'}
PAREDE={'A':'oeste','B':'norte','C':'leste'}
PORTA={'A':'S4','B':'S5','C':'S6'}
FLAG=('#E6B00F','#398CB0','#5F8722')
SANS="'Nunito Sans', system-ui, sans-serif"
DISP="'Archivo', 'Nunito Sans', sans-serif"
portas={p['letra']:p for p in S['portas']}

CAB = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap');
    body { margin: 0; background: #F0F0E8; }
    a { color: #0B6E9E; } a:hover { color: #042B5A; }
  </style>
</helmet>
"""
RODAPE = """</x-dc>
<script data-dc-script data-props='{"$preview":{"width":%d,"height":%d}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
"""

def faixa(alt_px):
    h=alt_px; esc=h/90.0
    ondas=''.join(f'<path d="M0 {6+i*11} q 9 -5 18 0 t 18 0 t 18 0" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>' for i,c in enumerate(FLAG))
    return f"""  <div style="height: {h}px; flex-shrink: 0; background: {AMARELO}; display: flex; align-items: center; justify-content: space-between; padding: 0 {round(h*0.34)}px; box-sizing: border-box;">
    <div style="display: flex; align-items: center; gap: {round(h*0.2)}px;">
      <svg width="{round(54*esc)}" height="{round(54*esc)}" viewBox="0 0 54 54" aria-hidden="true"><circle cx="27" cy="27" r="25" fill="none" stroke="{MARINHO}" stroke-width="3.4"/><path d="M27 6 a21 21 0 0 1 0 42" fill="{MARINHO}"/><rect x="24" y="24" width="15" height="15" fill="{AMARELO}"/></svg>
      <div style="font-family: {DISP}; font-weight: 700; font-size: {round(15*esc)}px; line-height: 1.02; color: {MARINHO};">Justiça<br>Eleitoral</div>
    </div>
    <div style="display: flex; align-items: center; gap: {round(h*0.16)}px;">
      <svg width="{round(56*esc)}" height="{round(40*esc)}" viewBox="0 0 56 40" aria-hidden="true">{ondas}</svg>
      <div><div style="font-family: {DISP}; font-weight: 700; font-size: {round(15*esc)}px; letter-spacing: 0.10em; color: {MARINHO}; line-height: 1;">ELEIÇÕES</div><div style="font-family: {DISP}; font-weight: 800; font-size: {round(25*esc)}px; color: {MARINHO}; line-height: 0.96;">2026</div></div>
    </div>
  </div>
"""

def grava(nome, w, h, corpo, fundo='#FFFFFF'):
    html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: {fundo}; display: flex; flex-direction: column; overflow: hidden;">
{corpo}
</div>
""" + RODAPE % (w, h)
    (OUT / nome).write_text(html, encoding='utf-8')

# --------------------------------------------- P6 painel da porta (pull-up 850x2000)
for L in ('A','B','C'):
    w,h = mm(850), mm(2000)
    blocos = portas[L]['blocos']
    linhas=[]
    for b in blocos:
        secs=' · '.join(str(s).zfill(4) for s in sorted(b['secoes']))
        linhas.append(
            f'<div style="display: flex; align-items: baseline; gap: 12px; padding: 9px 0; border-bottom: 1px solid #DDE1E5;">'
            f'<span style="font-family: {SANS}; font-weight: 700; font-size: 15px; color: #7A828C; min-width: 34px;">{b["id"][-2:]}</span>'
            f'<span style="font-family: {DISP}; font-weight: 700; font-size: 30px; color: {MARINHO}; font-variant-numeric: tabular-nums; letter-spacing: 0.01em;">{secs}</span>'
            f'</div>')
    corpo = faixa(round(h*0.10)) + f"""  <div style="background: {COR[L]}; color: #FFFFFF; padding: 18px 26px 16px; display: flex; align-items: center; gap: 18px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 150px; line-height: 0.8; letter-spacing: -0.04em;">{L}</div>
    <div>
      <div style="font-family: {SANS}; font-weight: 800; font-size: 34px; letter-spacing: 0.02em;">PORTA {L}</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 22px; opacity: 0.88;">parede {PAREDE[L]}</div>
    </div>
  </div>
  <div style="flex-grow: 1; padding: 20px 26px 26px; display: flex; flex-direction: column;">
    <div style="font-family: {SANS}; font-weight: 700; font-size: 19px; letter-spacing: 0.06em; color: #5A6270; margin-bottom: 8px;">PROCURE A SUA SEÇÃO · NA ORDEM EM QUE VOCÊ VAI ANDAR</div>
    {''.join(linhas)}
    <div style="flex-grow: 1;"></div>
    <div style="font-family: {SANS}; font-weight: 700; font-size: 21px; color: {MARINHO}; border-top: 3px solid {COR[L]}; padding-top: 12px;">Cada grupo tem uma placa alta na boca do corredor.</div>
  </div>
"""
    grava(f'P6-Painel{L}.dc.html', w, h, corpo)

# ------------------------------------------- P6 x-banner de bloco (600x1600)
def xbanner(L, b, nome):
    w,h = mm(600), mm(1600)
    secs=[str(s).zfill(4) for s in sorted(b['secoes'])]
    nums=''.join(f'<div style="font-family: {DISP}; font-weight: 800; font-size: 60px; line-height: 1.12; color: {MARINHO}; font-variant-numeric: tabular-nums;">{s}</div>' for s in secs)
    corpo = faixa(round(h*0.09)) + f"""  <div style="background: {COR[L]}; color: #FFFFFF; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 52px; line-height: 1;">{L}</div>
    <div style="font-family: {SANS}; font-weight: 700; font-size: 17px; text-align: right; line-height: 1.2;">parede {PAREDE[L]}<br><span style="opacity: 0.85;">grupo {b['id'][-2:]}</span></div>
  </div>
  <div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 16px;">
    <div style="font-family: {SANS}; font-weight: 700; font-size: 17px; letter-spacing: 0.08em; color: #5A6270; margin-bottom: 10px;">SEÇÕES DESTE CORREDOR</div>
    {nums}
  </div>
  <div style="height: 10px; background: {COR[L]}; flex-shrink: 0;"></div>
"""
    grava(nome, w, h, corpo)

xbanner('A', portas['A']['blocos'][2], 'P6-BlocoA3.dc.html')   # a isolada MRV 22, mesa vermelha
xbanner('C', portas['C']['blocos'][3], 'P6-BlocoC4.dc.html')   # um par de quatro secoes

# --------------------------------------------------------- planta do Ring 3
def planta_ring():
    W,H = 1240, 820
    ES = 22.0                       # px por metro
    rw, rd = R['ring']['largura'], R['ring']['profundidade']
    ox, oy = 60, 150
    def X(m): return ox + m*ES
    def Y(m): return oy + m*ES
    o=[f'<svg viewBox="0 0 {W} {H}" style="width: {W}px; height: {H}px;" role="img" aria-label="Planta do Ring 3 com as bocas das tres zonas e o ponto de cada peca de sinalizacao externa.">']
    # apron + fachada
    o.append(f'<rect x="{X(0):.0f}" y="{oy-100:.0f}" width="{rw*ES:.0f}" height="100" fill="#E4E8EA"/>')
    o.append(f'<line x1="{X(0)-30:.0f}" y1="{oy-100:.0f}" x2="{X(rw)+30:.0f}" y2="{oy-100:.0f}" stroke="{MARINHO}" stroke-width="4"/>')
    o.append(f'<text x="{X(rw/2):.0f}" y="{oy-112:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="13" fill="{MARINHO}" letter-spacing="1.4">FACHADA SUL DO HALL 2</text>')
    o.append(f'<text x="{X(rw/2):.0f}" y="{oy-44:.0f}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#6B737C">apron pavimentado · 14,0 m</text>')
    # cercado
    o.append(f'<rect x="{X(0):.0f}" y="{Y(0):.0f}" width="{rw*ES:.0f}" height="{rd*ES:.0f}" fill="#FFFFFF" stroke="#9AA3AB" stroke-width="2" stroke-dasharray="7 5"/>')
    # zonas
    off = R['ring']['offset_x']
    for L in ('A','B','C'):
        z=R['zonas'][L]
        x0,x1 = z['x0']-off, z['x1']-off
        prof = R['ring']['prof_raias']
        o.append(f'<rect x="{X(x0):.1f}" y="{Y(0):.0f}" width="{(x1-x0)*ES:.1f}" height="{prof*ES:.0f}" fill="{COR[L]}" fill-opacity="0.13" stroke="{COR[L]}" stroke-width="2"/>')
        for i in range(1, R['ring']['raias']):
            yy=Y(prof*i/R['ring']['raias'])
            o.append(f'<line x1="{X(x0):.1f}" y1="{yy:.1f}" x2="{X(x1):.1f}" y2="{yy:.1f}" stroke="{COR[L]}" stroke-width="0.7" opacity="0.4"/>')
        cx=X((x0+x1)/2)
        o.append(f'<text x="{cx:.0f}" y="{Y(prof/2):.0f}" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="52" fill="{COR[L]}">{L}</text>')
        o.append(f'<text x="{cx:.0f}" y="{Y(prof/2)+22:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="600" font-size="12" fill="{COR[L]}">{z["largura"]:.2f} m · {z["lotacao"]} pessoas</text>')
        # boca no lado leste da borda sul
        bx0,bx1 = z['boca_x0']-off, z['boca_x1']-off
        o.append(f'<line x1="{X(bx0):.1f}" y1="{Y(prof):.0f}" x2="{X(bx1):.1f}" y2="{Y(prof):.0f}" stroke="#FFFFFF" stroke-width="6"/>')
        o.append(f'<circle cx="{X((bx0+bx1)/2):.1f}" cy="{Y(prof)+20:.0f}" r="13" fill="{COR[L]}"/>')
        o.append(f'<text x="{X((bx0+bx1)/2):.1f}" y="{Y(prof)+25:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="12" fill="#FFF">P4</text>')
        # porta correspondente
        px=z['porta_x']
        o.append(f'<rect x="{X(px-2.96):.1f}" y="{oy-106:.0f}" width="{5.92*ES:.1f}" height="8" fill="{COR[L]}"/>')
        o.append(f'<text x="{X(px):.1f}" y="{oy-118:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="13" fill="{COR[L]}">{PORTA[L]} · {L}</text>')
        # ligacao boca -> porta
        o.append(f'<path d="M {X((bx0+bx1)/2):.1f} {Y(prof)+34:.0f} L {X((bx0+bx1)/2):.1f} {Y(prof)+48:.0f} L {X(px):.1f} {oy-92:.0f}" fill="none" stroke="{COR[L]}" stroke-width="2" stroke-dasharray="5 4" opacity="0.75"/>')
    # corredor em L
    cor=R['ring']['corredor']
    o.append(f'<rect x="{X(rw-cor):.1f}" y="{Y(0):.0f}" width="{cor*ES:.1f}" height="{rd*ES:.0f}" fill="#DCE3E7"/>')
    o.append(f'<rect x="{X(0):.0f}" y="{Y(rd-cor):.1f}" width="{rw*ES:.0f}" height="{cor*ES:.1f}" fill="#DCE3E7"/>')
    o.append(f'<text x="{X(rw-cor/2):.1f}" y="{Y(rd/2):.0f}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#5A6270" transform="rotate(90 {X(rw-cor/2):.1f} {Y(rd/2):.0f})">corredor de chegada · 3,0 m</text>')
    o.append(f'<text x="{X(rw/2):.0f}" y="{Y(rd-cor/2)+5:.0f}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#5A6270">trecho de fundo · lê C, depois B, depois A</text>')
    # P3 na entrada
    o.append(f'<circle cx="{X(rw-cor/2):.1f}" cy="{Y(1.6):.0f}" r="14" fill="{MARINHO}"/>')
    o.append(f'<text x="{X(rw-cor/2):.1f}" y="{Y(1.6)+5:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="12" fill="#FFF">P3</text>')
    o.append(f'<text x="{X(rw)+8:.0f}" y="{Y(1.6)+5:.0f}" font-family="{SANS}" font-weight="600" font-size="12" fill="{MARINHO}">entrada · canto nordeste</text>')
    # escala
    o.append(f'<line x1="{X(0):.0f}" y1="{Y(rd)+34:.0f}" x2="{X(10):.0f}" y2="{Y(rd)+34:.0f}" stroke="{MARINHO}" stroke-width="2.5"/>')
    o.append(f'<text x="{X(10)+8:.0f}" y="{Y(rd)+38:.0f}" font-family="{SANS}" font-size="12" fill="#5A6270">10 m</text>')
    o.append('</svg>')
    return '\n'.join(o)

corpo = f"""  <div style="padding: 26px 30px 0; display: flex; flex-direction: column; gap: 4px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 30px; color: {MARINHO};">Onde cada peça externa fica — Ring 3</div>
    <div style="font-family: {SANS}; font-weight: 600; font-size: 15px; color: #5A6270; max-width: 76ch;">Montagem confirmada em 16/09: 44 × 35 m, corredor em L de 3,0 m, {R['ring']['raias']} raias por zona. As larguras saem do esperado por entrada de Paredes_ABC. <strong>{R['bom']['ccb']} CCBs</strong> dos 200 em estoque, {R['bom']['fita_m']:.0f} m de fita, lotação {R['bom']['lotacao_total']}.</div>
  </div>
  <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center;">{planta_ring()}</div>
  <div style="padding: 0 30px 22px; font-family: {SANS}; font-size: 14px; color: #5A6270;">A linha tracejada é o caminho da boca até a porta. <strong style="color: {COR['A']};">A zona A descarrega 2,91 m a oeste do eixo da porta A</strong> — o cercado começa a oeste da primeira porta, e três zonas em terços não caem cada uma sob a sua. É o ponto a resolver em campo.</div>
"""
grava('Mapa-Ring3.dc.html', 1300, 1080, corpo, fundo=OFFW)

# ------------------------------------------------------- planta do Hall 2
def planta_hall():
    sal=P['salao']
    LX, LY = sal['largura'], sal['altura']
    ES=19.0; ox,oy=70,70
    W,H = round(LX*ES)+150, round(LY*ES)+150
    def X(m): return ox+m*ES
    def Y(m): return oy+(LY-m)*ES
    o=[f'<svg viewBox="0 0 {W} {H}" style="width: {W}px; height: {H}px;" role="img" aria-label="Planta do Hall 2 com as 28 mesas, os paineis de porta e os x-banners de cada grupo de mesas.">']
    o.append(f'<rect x="{X(0):.0f}" y="{Y(LY):.0f}" width="{LX*ES:.0f}" height="{LY*ES:.0f}" fill="#FFFFFF" stroke="{MARINHO}" stroke-width="2.5"/>')
    for L in ('A','B','C'):
        p=portas[L]
        for b in p['blocos']:
            bx,by = b['pos_banner']
            o.append(f'<circle cx="{X(bx):.1f}" cy="{Y(by):.1f}" r="11" fill="{COR[L]}"/>')
            o.append(f'<text x="{X(bx):.1f}" y="{Y(by)+4:.1f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="10" fill="#FFF">{b["id"][-2:]}</text>')
            for c in b['coord']:
                if p['parede']=='oeste':   mx,my = 1.4, c
                elif p['parede']=='norte': mx,my = c, LY-1.4
                else:                      mx,my = LX-1.4, c
                o.append(f'<rect x="{X(mx)-9:.1f}" y="{Y(my)-9:.1f}" width="18" height="18" fill="{COR[L]}" fill-opacity="0.30" stroke="{COR[L]}" stroke-width="1.4"/>')
    # portas na fachada sul
    for L,(a,bb) in (('A',(19.1,25.03)),('B',(25.32,31.25)),('C',(31.54,37.47))):
        o.append(f'<line x1="{X(a):.1f}" y1="{Y(0):.0f}" x2="{X(bb):.1f}" y2="{Y(0):.0f}" stroke="{COR[L]}" stroke-width="7"/>')
        o.append(f'<text x="{X((a+bb)/2):.1f}" y="{Y(0)+22:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="13" fill="{COR[L]}">{PORTA[L]} · {L}</text>')
        o.append(f'<rect x="{X((a+bb)/2)-10:.1f}" y="{Y(3.2):.1f}" width="20" height="20" fill="{COR[L]}"/>')
        o.append(f'<text x="{X((a+bb)/2):.1f}" y="{Y(3.2)+14:.1f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="10" fill="#FFF">P6</text>')
    o.append(f'<text x="{X(LX/2):.0f}" y="{Y(0)+46:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="12" fill="#5A6270" letter-spacing="1.2">FACHADA SUL · PARA O APRON E O RING 3</text>')
    o.append(f'<line x1="{X(0):.0f}" y1="{Y(LY)-24:.0f}" x2="{X(10):.0f}" y2="{Y(LY)-24:.0f}" stroke="{MARINHO}" stroke-width="2.5"/>')
    o.append(f'<text x="{X(10)+8:.0f}" y="{Y(LY)-20:.0f}" font-family="{SANS}" font-size="12" fill="#5A6270">10 m</text>')
    o.append('</svg>')
    return '\n'.join(o), W, H

svg, sw, sh = planta_hall()
corpo = f"""  <div style="padding: 26px 30px 0; display: flex; flex-direction: column; gap: 4px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 30px; color: {MARINHO};">Onde cada peça interna fica — Hall 2</div>
    <div style="font-family: {SANS}; font-weight: 600; font-size: 15px; color: #5A6270; max-width: 76ch;">Quadrado grande: o painel da porta (P6, pull-up), logo depois de cada entrada. Círculo: o x-banner do grupo de mesas, a 4,6 m da parede, na boca do corredor. As posições saem de <code>saidas/sinalizacao_v2.json</code>, campo <code>pos_banner</code>.</div>
  </div>
  <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center;">{svg}</div>
  <div style="padding: 0 30px 22px; font-family: {SANS}; font-size: 14px; color: #5A6270;">16 x-banners no total: 5 na oeste, 5 na norte, 6 na leste — um por grupo de mesas. Nenhum traz número de mesa: só as seções do grupo.</div>
"""
grava('Mapa-Hall2.dc.html', max(1180, sw+60), sh+230, corpo, fundo=OFFW)
print('internas e plantas: ok')
