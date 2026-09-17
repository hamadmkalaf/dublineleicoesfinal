# -*- coding: utf-8 -*-
"""Gera as pranchas .dc.html da proposta de sinalizacao a partir dos dados do repo.

Escala das pecas: 1 px = 2 mm.  Um banner de 2,0 x 1,0 m vira 1000 x 500 px, e
uma letra de 400 mm vira 200 px -- o que se ve na tela e a proporcao real.
"""
import json, os, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / 'saidas' / 'pranchas_sinalizacao'
(OUT / 'project').mkdir(parents=True, exist_ok=True)

S = json.loads((REPO / 'saidas' / 'sinalizacao_v2.json').read_text(encoding='utf-8'))
R = json.loads((REPO / 'saidas' / 'ring3_montagem.json').read_text(encoding='utf-8'))

MM = 0.5                      # px por mm
def mm(v): return round(v * MM, 1)

# --- paleta, de docs/identidade_visual.md -----------------------------------
AMARELO = '#F8C030'
OURO    = '#E6B00F'
MARINHO = '#042B5A'
OFFW    = '#F0F0E8'
# As tres fitas compradas pelo Posto (foto de 17/09). O texto de cada campo
# segue a luminancia do fundo: branco no azul, marinho no amarelo e na abobora.
COR   = {'A': '#33507E', 'B': '#E8C63A', 'C': '#DE7343'}
TEXTO = {'A': '#FFFFFF', 'B': '#042B5A', 'C': '#042B5A'}
REGUA = {'A': 'rgba(255,255,255,0.5)', 'B': 'rgba(4,43,90,0.35)', 'C': 'rgba(4,43,90,0.35)'}
FAIXA = OFFW   # a faixa institucional deixou de ser amarela: amarelo agora e a porta B
PAREDE = {'A': 'oeste', 'B': 'norte', 'C': 'leste'}
PORTA  = {'A': 'S4', 'B': 'S5', 'C': 'S6'}
FLAG   = ('#E6B00F', '#398CB0', '#5F8722')

mestra = {str(l['secao']).zfill(4): l['porta'] for l in S['mestra']}
portas = {p['letra']: p for p in S['portas']}

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

SANS = "'Nunito Sans', system-ui, sans-serif"
DISP = "'Archivo', 'Nunito Sans', sans-serif"


def faixa(larg_px, alt_px, nota=''):
    """Faixa institucional: o lugar do logotipo oficial, que ainda nao temos em vetor."""
    h = alt_px
    esc = h / 90.0
    ondas = ''.join(
        f'<path d="M0 {6+i*11} q 9 -5 18 0 t 18 0 t 18 0" fill="none" '
        f'stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
        for i, c in enumerate(FLAG))
    return f"""  <div style="height: {h}px; flex-shrink: 0; background: {FAIXA}; border-bottom: 3px solid {MARINHO}; display: flex; align-items: center; justify-content: space-between; padding: 0 {round(h*0.34)}px; box-sizing: border-box;">
    <div style="display: flex; align-items: center; gap: {round(h*0.2)}px;">
      <svg width="{round(54*esc)}" height="{round(54*esc)}" viewBox="0 0 54 54" aria-hidden="true"><circle cx="27" cy="27" r="25" fill="none" stroke="{MARINHO}" stroke-width="3.4"/><path d="M27 6 a21 21 0 0 1 0 42" fill="{MARINHO}"/><rect x="24" y="24" width="15" height="15" fill="{FAIXA}"/></svg>
      <div style="font-family: {DISP}; font-weight: 700; font-size: {round(15*esc)}px; line-height: 1.02; color: {MARINHO}; letter-spacing: -0.01em;">Justiça<br>Eleitoral</div>
    </div>
    <div style="display: flex; align-items: center; gap: {round(h*0.16)}px;">
      <svg width="{round(56*esc)}" height="{round(40*esc)}" viewBox="0 0 56 40" aria-hidden="true">{ondas}</svg>
      <div style="text-align: left;">
        <div style="font-family: {DISP}; font-weight: 700; font-size: {round(15*esc)}px; letter-spacing: 0.10em; color: {MARINHO}; line-height: 1;">ELEIÇÕES</div>
        <div style="font-family: {DISP}; font-weight: 800; font-size: {round(25*esc)}px; letter-spacing: -0.01em; color: {MARINHO}; line-height: 0.96;">2026</div>
      </div>
    </div>
  </div>
"""


def peca(nome, larg_mm, alt_mm, corpo, fundo='#FFFFFF', faixa_frac=0.15):
    """Uma peca em escala: faixa institucional no topo, corpo embaixo."""
    w, h = mm(larg_mm), mm(alt_mm)
    fh = round(h * faixa_frac)
    html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: {fundo}; display: flex; flex-direction: column; overflow: hidden;">
{faixa(w, fh)}
{corpo}
</div>
""" + RODAPE % (w, h)
    (OUT / 'project' / nome).write_text(html, encoding='utf-8')
    return {'w': w, 'h': h}


# ---------------------------------------------------------------- P0 consulta
corpo = f"""  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 14px; padding: 0 44px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 75px; line-height: 0.94; color: {MARINHO}; letter-spacing: -0.02em;">NÃO SABE<br>SUA SEÇÃO?</div>
    <div style="font-family: {SANS}; font-weight: 700; font-size: 34px; color: #5A6270;">Don't know your section?</div>
    <div style="display: flex; align-items: center; gap: 22px; margin-top: 8px;">
      <div style="background: {MARINHO}; color: #FFFFFF; font-family: {DISP}; font-weight: 700; font-size: 38px; padding: 14px 26px;">CONSULTE AQUI, ANTES DE ENTRAR</div>
      <div style="width: 96px; height: 96px; border: 5px solid {MARINHO}; display: flex; align-items: center; justify-content: center; font-family: {SANS}; font-weight: 700; font-size: 15px; color: {MARINHO}; text-align: center; line-height: 1.1;">QR<br>e-Título</div>
    </div>
  </div>
"""
peca('P0-Consulta.dc.html', 2000, 1000, corpo)

# ------------------------------------------------------------- tabela mestra
def tabela_mestra(cols=3, dig=40, chip=30, gap=9):
    itens = sorted(mestra.items())
    por = -(-len(itens) // cols)
    colunas = [itens[i*por:(i+1)*por] for i in range(cols)]
    out = [f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 0 34px; flex-grow: 1;">']
    for col in colunas:
        out.append('<div style="display: flex; flex-direction: column; justify-content: space-between;">')
        for sec, p in col:
            out.append(
                f'<div style="display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #D8DCE0; padding: {gap//2}px 0;">'
                f'<span style="font-family: {DISP}; font-weight: 700; font-size: {dig}px; color: {MARINHO}; font-variant-numeric: tabular-nums;">{sec}</span>'
                f'<span style="flex-grow: 1;"></span>'
                f'<span style="min-width: {chip+14}px; text-align: center; background: {COR[p]}; color: {TEXTO[p]}; font-family: {DISP}; font-weight: 800; font-size: {chip}px; line-height: {chip+10}px; padding: 0 8px;">{p}</span>'
                f'</div>')
        out.append('</div>')
    out.append('</div>')
    return '\n'.join(out)

for nome, titulo, sub in (
        ('P0-Mestra.dc.html', 'SUA SEÇÃO → SUA PORTA', 'Anote a letra. Você vai procurá-la três vezes no caminho.'),
        ('P1-Portao.dc.html', 'SUA SEÇÃO → SUA PORTA', 'Section → door · a letra é a sua fila do portão até a urna.')):
    corpo = f"""  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 16px 40px 20px; gap: 10px;">
    <div style="display: flex; align-items: baseline; gap: 18px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 40px; color: {MARINHO}; letter-spacing: -0.01em;">{titulo}</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 19px; color: #5A6270;">{sub}</div>
    </div>
{tabela_mestra()}
  </div>
"""
    peca(nome, 2000, 1000, corpo)

# ------------------------------------------------- P2 parede leste (PVC 1,8 x 1,2)
corpo = f"""  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 16px 34px 20px; gap: 8px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 42px; color: {MARINHO};">SUA SEÇÃO → SUA PORTA</div>
{tabela_mestra(cols=3, dig=42, chip=32, gap=12)}
    <div style="display: flex; align-items: center; gap: 14px; background: {MARINHO}; color: #FFFFFF; padding: 12px 20px; font-family: {DISP}; font-weight: 700; font-size: 30px;">
      <span>A FILA SEGUE ADIANTE</span>
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
    </div>
  </div>
"""
peca('P2-ParedeLeste.dc.html', 1800, 1200, corpo)

# ------------------------------------------------------------ P3 entrada Ring
corpo = f"""  <div style="flex-grow: 1; display: flex; padding: 14px 34px 18px; gap: 26px;">
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 8px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 36px; color: {MARINHO};">SUA SEÇÃO → SUA PORTA</div>
{tabela_mestra(cols=2, dig=34, chip=26, gap=6)}
    </div>
    <div style="width: 300px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: center; gap: 16px; border-left: 4px solid #D8DCE0; padding-left: 26px;">
      <div style="font-family: {SANS}; font-weight: 700; font-size: 20px; color: #5A6270; text-transform: uppercase; letter-spacing: 0.08em;">Siga o corredor</div>
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 58px; text-align: center; background: {COR['C']}; color: {TEXTO['C']}; font-family: {DISP}; font-weight: 800; font-size: 40px; line-height: 58px;">C</span><span style="font-family: {SANS}; font-weight: 600; font-size: 21px; color: {MARINHO};">primeiro</span></div>
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 58px; text-align: center; background: {COR['B']}; color: {TEXTO['B']}; font-family: {DISP}; font-weight: 800; font-size: 40px; line-height: 58px;">B</span><span style="font-family: {SANS}; font-weight: 600; font-size: 21px; color: {MARINHO};">depois</span></div>
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 58px; text-align: center; background: {COR['A']}; color: {TEXTO['A']}; font-family: {DISP}; font-weight: 800; font-size: 40px; line-height: 58px;">A</span><span style="font-family: {SANS}; font-weight: 600; font-size: 21px; color: {MARINHO};">no fim</span></div>
      </div>
    </div>
  </div>
"""
peca('P3-EntradaRing.dc.html', 2000, 1000, corpo)

# ------------------------------------------------------- P4 bocas das zonas
for L in ('A', 'B', 'C'):
    secs = [str(s).zfill(4) for s in sorted(portas[L]['secoes'])]
    z = R['zonas'][L]
    grade = ''.join(
        f'<span style="font-family: {DISP}; font-weight: 700; font-size: 40px; color: {TEXTO[L]}; font-variant-numeric: tabular-nums;">{s}</span>'
        for s in secs)
    ncol = 6
    corpo = f"""  <div style="flex-grow: 1; background: {COR[L]}; display: flex; padding: 18px 34px 20px; gap: 30px; color: {TEXTO[L]};">
    <div style="width: 240px; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 200px; line-height: 0.82; letter-spacing: -0.04em;">{L}</div>
      <div style="font-family: {SANS}; font-weight: 700; font-size: 24px; letter-spacing: 0.04em; margin-top: 6px;">PORTA {L}</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 19px; opacity: 0.86;">parede {PAREDE[L]} · {PORTA[L]}</div>
    </div>
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 10px; justify-content: center;">
      <div style="font-family: {SANS}; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; opacity: 0.9;">ENTRE AQUI SE A SUA SEÇÃO ESTÁ NESTA LISTA</div>
      <div style="display: grid; grid-template-columns: repeat({ncol}, minmax(0, 1fr)); gap: 7px 16px;">{grade}</div>
      <div style="font-family: {SANS}; font-weight: 700; font-size: 21px; border-top: 3px solid {REGUA[L]}; padding-top: 9px; margin-top: 4px;">Não está aqui? Siga em frente pelo corredor.</div>
    </div>
  </div>
"""
    peca(f'P4-Zona{L}.dc.html', 2000, 1000, corpo, fundo=COR[L])

# ------------------------------------------------------------- P5 vinil porta
for L in ('A', 'B', 'C'):
    w, h = mm(1200), mm(700)
    html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: #DCE6EC; display: flex; align-items: center; justify-content: center;">
  <div style="display: flex; align-items: center; gap: 26px;">
    <div style="font-family: {SANS}; font-weight: 700; font-size: 44px; color: {MARINHO}; letter-spacing: 0.02em;">ENTRADA</div>
    <div style="width: 150px; height: 150px; background: {COR[L]}; color: {TEXTO[L]}; font-family: {DISP}; font-weight: 800; font-size: 150px; line-height: 150px; text-align: center;">{L}</div>
  </div>
</div>
""" + RODAPE % (w, h)
    (OUT / 'project' / f'P5-Vinil{L}.dc.html').write_text(html, encoding='utf-8')

# ------------------------------------------------------------ P5 preferencial
corpo = f"""  <div style="flex-grow: 1; display: flex; align-items: center; gap: 34px; padding: 0 40px;">
    <svg width="130" height="130" viewBox="0 0 24 24" fill="none" stroke="{MARINHO}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4.6" r="2.1"/><path d="M12 7.5v6m0 0-3 6m3-6 3 6M7.5 10h9"/></svg>
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 62px; line-height: 0.96; color: {MARINHO};">ENTRADA PREFERENCIAL</div>
      <div style="font-family: {SANS}; font-weight: 700; font-size: 30px; color: #5A6270;">Priority entrance</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 26px; color: {MARINHO};">Idoso · gestante · PcD · com acompanhante — <strong>qualquer porta</strong></div>
    </div>
  </div>
"""
peca('P5-Preferencial.dc.html', 2000, 1000, corpo)

# ------------------------------------------------------------------ P7 saida
w, h = mm(594), mm(420)
html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: {MARINHO}; color: #FFFFFF; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;">
  <div style="display: flex; align-items: center; gap: 16px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 75px; line-height: 1;">SAÍDA</div>
    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
  </div>
  <div style="font-family: {SANS}; font-weight: 700; font-size: 28px; opacity: 0.85;">WAY OUT</div>
  <div style="font-family: {SANS}; font-weight: 600; font-size: 22px; opacity: 0.7;">→ Merrion Road</div>
</div>
""" + RODAPE % (w, h)
(OUT / 'project' / 'P7-Saida.dc.html').write_text(html, encoding='utf-8')

print('pecas externas e saida: ok')
