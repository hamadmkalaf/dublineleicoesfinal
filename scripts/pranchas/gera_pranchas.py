# -*- coding: utf-8 -*-
"""As pecas externas da sinalizacao: P0, P1, P2, P3, P4, P5 e a saida P7.

Escala das pranchas: 1 px = 2 mm.  Um fence banner de 2080 x 820 mm vira
1040 x 410 px, e uma letra de 400 mm vira 200 px -- o que se ve na tela e a
proporcao real da peca.

Formatos: os do catalogo do fornecedor (Helloprint IE, cotacoes de 18/09/2026
em Orcamentos/Sinalizacao).  Peca fora de formato de catalogo custa mais e
demora mais.
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comum import (PALETA, CARVAO, CARVAO_SUAVE, OSSO, OSSO_ESCURO, COR, TEXTO,
                   PAREDE, PORTA, SANS, DISP, faixa, estilo_pagina)

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / 'saidas' / 'pranchas_sinalizacao'
(OUT / 'project').mkdir(parents=True, exist_ok=True)

S = json.loads((REPO / 'saidas' / 'sinalizacao_v2.json').read_text(encoding='utf-8'))
R = json.loads((REPO / 'saidas' / 'ring3_montagem.json').read_text(encoding='utf-8'))

MM = 0.5
def mm(v): return round(v * MM, 1)

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
""" + estilo_pagina() + "\n"

RODAPE = """</x-dc>
<script data-dc-script data-props='{"$preview":{"width":%d,"height":%d}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
"""


def peca(nome, larg_mm, alt_mm, corpo, fundo=OSSO, faixa_frac=0.17):
    w, h = mm(larg_mm), mm(alt_mm)
    fh = round(h * faixa_frac)
    html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: {fundo}; display: flex; flex-direction: column; overflow: hidden;">
{faixa(fh, w)}
{corpo}
</div>
""" + RODAPE % (w, h)
    (OUT / 'project' / nome).write_text(html, encoding='utf-8')


# ------------------------------------------------------- a tabela mestra
def tabela_mestra(cols, alt_px, larg_px):
    """As 51 linhas seção -> porta, dimensionadas para CABER em alt_px.

    O corpo da letra sai da altura disponível; fixá-lo fazia a tabela
    transbordar e o overflow:hidden comia metade das seções, em silêncio.
    """
    itens = sorted(mestra.items())
    por = -(-len(itens) // cols)
    linha_px = alt_px / por
    dig = max(11, round(linha_px * 0.62))
    chip = max(9, round(linha_px * 0.50))
    gap = max(2, round(linha_px * 0.12))
    col_px = larg_px / cols
    if dig * 2.6 + chip * 1.7 > col_px:
        dig = max(11, round((col_px - chip * 1.7) / 2.6))
    colunas = [itens[i*por:(i+1)*por] for i in range(cols)]
    out = [f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); '
           f'gap: 0 {max(10, round(col_px*0.10))}px; flex-grow: 1; overflow: hidden;">']
    for col in colunas:
        out.append('<div style="display: flex; flex-direction: column; justify-content: flex-start;">')
        for sec, p in col:
            out.append(
                f'<div style="display: flex; align-items: center; gap: {max(4, gap)}px; '
                f'border-bottom: 1px solid {OSSO_ESCURO}; padding: {gap//2}px 0;">'
                f'<span style="font-family: {DISP}; font-weight: 700; font-size: {dig}px; '
                f'color: {CARVAO}; font-variant-numeric: tabular-nums;">{sec}</span>'
                f'<span style="flex-grow: 1;"></span>'
                f'<span style="min-width: {round(chip*1.5)}px; text-align: center; background: {COR[p]}; '
                f'color: {TEXTO[p]}; font-family: {DISP}; font-weight: 800; font-size: {chip}px; '
                f'line-height: {round(chip*1.35)}px; padding: 0 5px;">{p}</span>'
                f'</div>')
        out.append('</div>')
    out.append('</div>')
    return '\n'.join(out)


# =========================================================== peças externas
# Todas em fence banner 2080 x 820 mm: o formato do fornecedor feito para
# amarrar em grade e em CCB, com tie wraps.  Substitui o banner 2000 x 1000
# genérico que estava aqui antes.
FB_L, FB_A = 2080, 820

# ------------------------------------------------------------ P0 consulta
corpo = f"""  <div style="flex-grow: 1; display: flex; align-items: center; gap: 34px; padding: 0 44px;">
    <div style="flex-grow: 1;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 82px; line-height: 0.94; color: {CARVAO}; letter-spacing: -0.02em;">NÃO SABE<br>SUA SEÇÃO?</div>
      <div style="display: inline-block; margin-top: 16px; background: {PALETA['verde']}; color: #FFFFFF; font-family: {DISP}; font-weight: 700; font-size: 38px; padding: 12px 24px;">CONSULTE AQUI, ANTES DE ENTRAR</div>
    </div>
    <div style="width: 150px; height: 150px; flex-shrink: 0; border: 6px solid {PALETA['azul']}; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: {SANS}; font-weight: 700; font-size: 17px; color: {PALETA['azul']}; text-align: center; line-height: 1.15;">QR<br>e-Título</div>
  </div>
"""
peca('P0-Consulta.dc.html', FB_L, FB_A, corpo)

# ------------------------------------------------------- tabelas mestras
for nome, sub in (('P0-Mestra.dc.html', 'Anote a letra. Você vai procurá-la três vezes no caminho.'),
                  ('P1-Portao.dc.html', 'A letra é a sua fila, do portão até a urna.')):
    corpo = f"""  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 14px 40px 18px; gap: 8px;">
    <div style="display: flex; align-items: baseline; gap: 18px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 40px; color: {CARVAO}; letter-spacing: -0.015em; white-space: nowrap;">SUA SEÇÃO <span style="color: {PALETA['laranja']}">→</span> SUA PORTA</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 19px; color: {CARVAO_SUAVE};">{sub}</div>
    </div>
{tabela_mestra(cols=6, alt_px=250, larg_px=960)}
  </div>
"""
    peca(nome, FB_L, FB_A, corpo)

# ------------------------------------ P2 parede leste (PVC 2000 x 1000 mm)
corpo = f"""  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 14px 36px 18px; gap: 8px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 42px; color: {CARVAO}; white-space: nowrap;">SUA SEÇÃO <span style="color: {PALETA['laranja']}">→</span> SUA PORTA</div>
{tabela_mestra(cols=6, alt_px=300, larg_px=928)}
    <div style="display: flex; align-items: center; gap: 14px; background: {PALETA['ardosia']}; color: #FFFFFF; padding: 10px 20px; font-family: {DISP}; font-weight: 700; font-size: 28px;">
      <span>A FILA SEGUE ADIANTE</span>
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
    </div>
  </div>
"""
peca('P2-ParedeLeste.dc.html', 2000, 1000, corpo, faixa_frac=0.15)

# ------------------------------------------------------- P3 entrada do Ring
corpo = f"""  <div style="flex-grow: 1; display: flex; padding: 12px 36px 16px; gap: 26px;">
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 34px; color: {CARVAO}; white-space: nowrap;">SUA SEÇÃO <span style="color: {PALETA['laranja']}">→</span> SUA PORTA</div>
{tabela_mestra(cols=5, alt_px=250, larg_px=680)}
    </div>
    <div style="width: 258px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: center; gap: 12px; border-left: 4px solid {OSSO_ESCURO}; padding-left: 24px;">
      <div style="font-family: {SANS}; font-weight: 800; font-size: 19px; color: {PALETA['verde']}; letter-spacing: 0.06em;">SIGA O CORREDOR</div>
      <div style="display: flex; flex-direction: column; gap: 9px;">
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 54px; text-align: center; background: {COR['C']}; color: {TEXTO['C']}; font-family: {DISP}; font-weight: 800; font-size: 38px; line-height: 54px;">C</span><span style="font-family: {SANS}; font-weight: 700; font-size: 21px; color: {CARVAO};">primeiro</span></div>
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 54px; text-align: center; background: {COR['B']}; color: {TEXTO['B']}; font-family: {DISP}; font-weight: 800; font-size: 38px; line-height: 54px;">B</span><span style="font-family: {SANS}; font-weight: 700; font-size: 21px; color: {CARVAO};">depois</span></div>
        <div style="display: flex; align-items: center; gap: 12px;"><span style="width: 54px; text-align: center; background: {COR['A']}; color: {TEXTO['A']}; font-family: {DISP}; font-weight: 800; font-size: 38px; line-height: 54px;">A</span><span style="font-family: {SANS}; font-weight: 700; font-size: 21px; color: {CARVAO};">no fim</span></div>
      </div>
    </div>
  </div>
"""
peca('P3-EntradaRing.dc.html', FB_L, FB_A, corpo)

# --------------------------------------------------- P4 bocas das zonas
for L in ('A', 'B', 'C'):
    secs = [str(s).zfill(4) for s in sorted(portas[L]['secoes'])]
    regua = 'rgba(255,255,255,0.5)' if L == 'A' else 'rgba(63,63,63,0.3)'
    grade = ''.join(
        f'<span style="font-family: {DISP}; font-weight: 700; font-size: 42px; '
        f'color: {TEXTO[L]}; font-variant-numeric: tabular-nums;">{s}</span>'
        for s in secs)
    corpo = f"""  <div style="flex-grow: 1; background: {COR[L]}; display: flex; padding: 14px 36px 16px; gap: 30px; color: {TEXTO[L]};">
    <div style="width: 230px; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 190px; line-height: 0.80; letter-spacing: -0.04em;">{L}</div>
      <div style="font-family: {SANS}; font-weight: 800; font-size: 25px; letter-spacing: 0.04em; margin-top: 4px;">PORTA {L}</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 19px; opacity: 0.85;">parede {PAREDE[L]} · {PORTA[L]}</div>
    </div>
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 9px; justify-content: center;">
      <div style="font-family: {SANS}; font-weight: 800; font-size: 23px; letter-spacing: 0.03em; white-space: nowrap;">SUA SEÇÃO ESTÁ AQUI? ENTRE.</div>
      <div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 6px 14px;">{grade}</div>
      <div style="font-family: {SANS}; font-weight: 700; font-size: 21px; border-top: 3px solid {regua}; padding-top: 8px; margin-top: 2px;">Não está aqui? Siga em frente pelo corredor.</div>
    </div>
  </div>
"""
    peca(f'P4-Zona{L}.dc.html', FB_L, FB_A, corpo, fundo=COR[L])

# ------------------------------------------------------- P5 vinil no vidro
for L in ('A', 'B', 'C'):
    w, h = mm(1200), mm(700)
    html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: #DDE4E2; display: flex; align-items: center; justify-content: center;">
  <div style="display: flex; align-items: center; gap: 26px;">
    <div style="font-family: {SANS}; font-weight: 800; font-size: 44px; color: {CARVAO}; letter-spacing: 0.02em;">ENTRADA</div>
    <div style="width: 150px; height: 150px; background: {COR[L]}; color: {TEXTO[L]}; font-family: {DISP}; font-weight: 800; font-size: 150px; line-height: 150px; text-align: center;">{L}</div>
  </div>
</div>
""" + RODAPE % (w, h)
    (OUT / 'project' / f'P5-Vinil{L}.dc.html').write_text(html, encoding='utf-8')

# -------------------------------------------------------- P5 preferencial
corpo = f"""  <div style="flex-grow: 1; display: flex; align-items: center; gap: 34px; padding: 0 44px;">
    <svg width="118" height="118" viewBox="0 0 24 24" fill="none" stroke="{PALETA['verde']}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4.6" r="2.1"/><path d="M12 7.5v6m0 0-3 6m3-6 3 6M7.5 10h9"/></svg>
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <div style="font-family: {DISP}; font-weight: 800; font-size: 66px; line-height: 0.96; color: {CARVAO};">ENTRADA PREFERENCIAL</div>
      <div style="font-family: {SANS}; font-weight: 600; font-size: 27px; color: {CARVAO_SUAVE};">Idoso · gestante · PcD · com acompanhante — <strong style="color: {PALETA['verde']}">qualquer porta</strong></div>
    </div>
  </div>
"""
peca('P5-Preferencial.dc.html', FB_L, FB_A, corpo)

# -------------------------------------------------------------- P7 saída
w, h = mm(594), mm(420)
html = CAB + f"""<div style="width: {w}px; height: {h}px; box-sizing: border-box; background: {PALETA['ardosia']}; color: #FFFFFF; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;">
  <div style="display: flex; align-items: center; gap: 12px;">
    <div style="font-family: {DISP}; font-weight: 800; font-size: 68px; line-height: 1;">SAÍDA</div>
    <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
  </div>
  <div style="font-family: {SANS}; font-weight: 600; font-size: 24px; opacity: 0.82;">→ Merrion Road</div>
</div>
""" + RODAPE % (w, h)
(OUT / 'project' / 'P7-Saida.dc.html').write_text(html, encoding='utf-8')

print('peças externas e a saída: ok')
