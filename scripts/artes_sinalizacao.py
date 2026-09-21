#!/usr/bin/env python3
"""Gera as artes de sinalização que saem de dados, não de desenho à mão.

  * `P5-Preferencial` e `P5-VinilPref` — a entrada preferencial, com os cinco
    pictogramas brasileiros de `scripts/_pictogramas.py`.
  * `P6-Bloco<ID>` — uma placa alta por grupo de mesas, **os dezesseis**:
    A1–A5, B1–B5 e C1–C6. Antes existiam só duas, A3 e C4.

O código do grupo é o título da placa: quem está no par C3 lê "C3" no alto do
banner, na mesma letra e no mesmo número que o painel da porta C usa na lista.

Fonte: `data/grupos_mesas.json`, **lido, nunca escrito** por aqui.

    python3 scripts/artes_sinalizacao.py            confere e não escreve nada
    python3 scripts/artes_sinalizacao.py --grava    regrava as peças

Sem `--grava` sai com código 1 se alguma peça divergir do que ele geraria.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _pictogramas import picto_linha  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "data" / "grupos_mesas.json"
PECAS = RAIZ / "mapa" / "sinalizacao"

ARCHIVO = "'Archivo', 'Nunito Sans', sans-serif"
NUNITO = "'Nunito Sans', system-ui, sans-serif"
CREME = "#F2EFE2"
TINTA = "#3F3F3F"
CINZA = "#6B6B6B"

CORES = {
    "A": ("#33507E", "#FFFFFF"),
    "B": ("#E8C63A", "#3F3F3F"),
    "C": ("#DE7343", "#3F3F3F"),
}
PAREDE = {"A": "parede oeste", "B": "parede norte", "C": "parede leste"}

MOLDE = """<!doctype html>
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
    body {{ margin: 0; background: #F2EFE2; }}
    a {{ color: #5A8CAA; }} a:hover {{ color: #3F3F3F; }}
  </style>
</helmet>
{corpo}
</x-dc>
<script data-dc-script data-props='{{"$preview":{{"width":{larg},"height":{alt}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""

ONDAS = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true" style="display:block">'
         '<path d="M-1 4.6 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="#E8B800" stroke-width="6.3" stroke-linecap="butt"/>'
         '<path d="M-1 12.2 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="#4888A8" stroke-width="6.3" stroke-linecap="butt"/>'
         '<path d="M-1 19.799999999999997 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="#588018" stroke-width="6.3" stroke-linecap="butt"/></svg>')


def cabecalho(alto, pal, ano, onda, pad, g1, g2, hashtag):
    """A tarja de identidade do topo, nas duas escalas já usadas pelo plano."""
    direita = ('<div style="font-family: ' + ARCHIVO + '; font-weight: 700; font-size: 14.0px;'
               ' letter-spacing: 0.02em; color: #FFFFFF;">#VOTO<span style="color: #5A8CAA">NA</span>'
               'DEMOCRACIA</div>') if hashtag else "    "
    justif = "space-between" if hashtag else "flex-start"
    return f"""  <div style="height: {alto}px; flex-shrink: 0; background: #5A6E6E; display: flex; align-items: center; justify-content: {justif}; padding: 0 {pad}px; box-sizing: border-box; overflow: hidden;">
    <div style="display: flex; flex-direction: column; align-items: flex-start; gap: {g1}px; line-height: 1;">
      <div style="display: flex; align-items: center; gap: {g2}px;">
        <span style="font-family: {ARCHIVO}; font-weight: 800; font-size: {pal}px; letter-spacing: 0.01em; color: #FFFFFF;">EL</span>
        {ONDAS.format(s=onda)}
        <span style="font-family: {ARCHIVO}; font-weight: 800; font-size: {pal}px; letter-spacing: 0.01em; color: #FFFFFF;">IÇÕES</span>
      </div>
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: {ano}px; letter-spacing: -0.01em; color: #F2CE3A;">2026</div>
    </div>
    {direita}
  </div>"""


CAB_BANNER = cabecalho(70, 13.0, 25.2, 9.6, 18, 0.9, 0.8, True)
CAB_ALTO = cabecalho(115, 21.4, 41.4, 15.8, 30, 1.4, 1.3, False)


def preferencial():
    corpo = f"""<div style="width: 1040.0px; height: 410.0px; box-sizing: border-box; background: {CREME}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_BANNER}

  <div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding: 12px 40px 16px;">
    <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 58px; line-height: 1; color: {TINTA}; letter-spacing: -0.01em;">ATENDIMENTO PREFERENCIAL</div>
    <div style="width: 100%; height: 4px; background: {TINTA};"></div>
    {picto_linha(altura=158, vao=18, sufixo="pref")}
    <div style="font-family: {NUNITO}; font-weight: 600; font-size: 23px; color: {CINZA}; white-space: nowrap;">Idoso · colo · gestante · PcD · TEA — <strong style="color: #648232">qualquer porta, sem fila</strong></div>
  </div>

</div>"""
    return MOLDE.format(corpo=corpo, larg=1040, alt=410)


def vinil_preferencial():
    corpo = f"""<div style="width: 600.0px; height: 350.0px; box-sizing: border-box; background: #DDE4E2; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px;">
  <div style="font-family: {NUNITO}; font-weight: 800; font-size: 46px; color: {TINTA}; letter-spacing: 0.02em;">PREFERENCIAL</div>
  {picto_linha(altura=104, vao=12, sufixo="vinil")}
</div>"""
    return MOLDE.format(corpo=corpo, larg=600, alt=350)


# O corpo da placa fica encostado no topo, não centrado: o pull-up tem 2000 mm e
# o terço de baixo some atrás da fila. Assim o primeiro número cai por volta de
# 1.400 mm do chão, acima da cabeça de quem está na frente.
# Quanto menos seções no grupo, maior o dígito: a placa tem 725 px de corpo e
# no máximo quatro números, então sobra altura para gastar em legibilidade.
# 80 px no canvas de 425 px equivalem a 160 mm no pull-up de 850 mm.
DIGITO = {1: 130, 2: 112, 3: 96, 4: 80}


def banner_bloco(grupo):
    porta = grupo["entrada"]
    fundo, tinta = CORES[porta]
    secoes = sorted(grupo["secoes"])
    tam = DIGITO[len(secoes)]
    numeros = "".join(
        f'<div style="font-family: {ARCHIVO}; font-weight: 800; font-size: {tam}px;'
        f' line-height: 1.12; color: {TINTA}; font-variant-numeric: tabular-nums;">{s:04d}</div>'
        for s in secoes
    )
    corpo = f"""<div style="width: 425.0px; height: 1000.0px; box-sizing: border-box; background: {CREME}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_ALTO}
  <div style="background: {fundo}; color: {tinta}; padding: 14px 20px 16px; display: flex; align-items: center; justify-content: space-between;">
    <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 104px; line-height: 0.86; letter-spacing: -0.03em;">{grupo["id"]}</div>
    <div style="font-family: {NUNITO}; font-weight: 700; font-size: 22px; text-align: right; line-height: 1.25;">PORTA {porta}<br><span style="opacity: 0.85; font-weight: 600;">{PAREDE[porta]}</span></div>
  </div>
  <div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 4px; padding: 30px 16px 16px;">
    <div style="font-family: {NUNITO}; font-weight: 700; font-size: 17px; letter-spacing: 0.08em; color: {CINZA}; margin-bottom: 10px;">SEÇÕES DESTE CORREDOR</div>
    {numeros}
  </div>
  <div style="height: 10px; background: {fundo}; flex-shrink: 0;"></div>

</div>"""
    return MOLDE.format(corpo=corpo, larg=425, alt=1000)


def pecas():
    grupos = json.loads(FONTE.read_text(encoding="utf-8"))["grupos"]
    saida = {"P5-Preferencial": preferencial(), "P5-VinilPref": vinil_preferencial()}
    for g in grupos:
        saida[f"P6-Bloco{g['id']}"] = banner_bloco(g)
    return saida


def main():
    grava = "--grava" in sys.argv[1:]
    divergiu = False
    for nome, html in pecas().items():
        caminho = PECAS / f"{nome}.dc.html"
        atual = caminho.read_text(encoding="utf-8") if caminho.exists() else None
        if atual == html:
            marca = "igual"
        else:
            divergiu = True
            marca = ("regravada" if atual is not None else "nova") if grava else "DIVERGENTE"
            if grava:
                caminho.write_text(html, encoding="utf-8")
        print(f"{nome:<18} {marca}")
    if divergiu and not grava:
        print("as peças estão fora do que este gerador produz; rode com --grava", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
