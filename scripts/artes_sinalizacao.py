#!/usr/bin/env python3
"""Gera as artes de sinalização que saem de dados, não de desenho à mão.

  * `P0-Consulta` — "não sabe sua seção?", com o QR estático para o site do
    TSE (`data/qr_tse.svg`, de `scripts/qr_tse.py`). Desde 22/09.
  * `P4-ZonaA/B/C` — a boca de cada zona do Ring 3: corpo branco, a cor da
    porta só no bloco da letra, as seções em células com borda. Desde 22/09.
  * `P5-Preferencial` e `P5-VinilPref` — a entrada preferencial, com os cinco
    pictogramas brasileiros de `scripts/_pictogramas.py`. Desde 22/09 a
    P5-Preferencial é empilhada como a placa de referência do Posto: fundo
    azul, moldura branca, título em caixa branca, pictogramas brancos, e sem a
    faixa institucional.
  * `P6-Bloco<ID>` — uma placa alta por grupo de mesas, **os dezesseis**:
    A1–A5, B1–B5 e C1–C6. Desde 22/09 as seções saem **agrupadas por mesa**,
    com uma seta para o lado da mesa: a placa fica entre as duas mesas do par,
    de frente para o salão, e a seta diz de que lado fica a fila de cada seção.

O código do grupo é o título da placa: quem está no par C3 lê "C3" no alto do
banner, na mesma letra e no mesmo número que o painel da porta C usa na lista.

Fonte: `data/grupos_mesas.json`, **lido, nunca escrito** por aqui — a
correspondência seção → porta das P4 vem por `tabela_mestra.por_porta()`.

    python3 scripts/artes_sinalizacao.py            confere e não escreve nada
    python3 scripts/artes_sinalizacao.py --grava    regrava as peças

Sem `--grava` sai com código 1 se alguma peça divergir do que ele geraria.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _pictogramas import picto_linha  # noqa: E402
from paleta import (AZUL, BRANCO, CINZA, CREME, GRAFITE, IMPORT_FONTE,  # noqa: E402
                    MARINHO, OFFWHITE, OURO, PAREDE, PREFERENCIAL, VERDE, ZONA)
from paleta import FONTE as FONTE_CSS  # noqa: E402
from tabela_mestra import por_porta  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "data" / "grupos_mesas.json"
QR = RAIZ / "data" / "qr_tse.svg"
PECAS = RAIZ / "mapa" / "sinalizacao"

# Montserrat é a fonte da campanha e cobre display e texto. Os dois nomes
# ficam por compatibilidade com o resto do módulo.
ARCHIVO = FONTE_CSS
NUNITO = FONTE_CSS
TINTA = MARINHO
CORES = ZONA

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
    @import url('{IMPORT_FONTE}');
    body {{ margin: 0; background: #F2EFE2; }}
    a {{ color: {AZUL}; }} a:hover {{ color: {MARINHO}; }}
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

def _molde(corpo, larg, alt):
    return MOLDE.format(corpo=corpo, larg=larg, alt=alt, AZUL=AZUL, MARINHO=MARINHO,
                        IMPORT_FONTE=IMPORT_FONTE)


# A bandeirinha do logotipo: onda de cima ouro, do meio azul, de baixo verde --
# as três medidas no vetor oficial, não estimadas.
ONDAS = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true" style="display:block">'
    '<path d="M-1 4.6 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="' + OURO + '" stroke-width="6.3" stroke-linecap="butt"/>'
    '<path d="M-1 12.2 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="' + AZUL + '" stroke-width="6.3" stroke-linecap="butt"/>'
    '<path d="M-1 19.799999999999997 q 6.5 -2.0 13 0 t 13 0" fill="none" stroke="' + VERDE + '" stroke-width="6.3" stroke-linecap="butt"/></svg>')


def cabecalho(alto, pal, ano, onda, pad, g1, g2, hashtag):
    regua = 4 if alto > 90 else 3
    """A tarja de identidade do topo, nas duas escalas já usadas pelo plano."""
    # Sobre a faixa off-white o lockup sai inteiro, com as cores dele.
    direita = ('<div style="font-family: ' + ARCHIVO + '; font-weight: 700; font-size: 14.0px;'
               f' letter-spacing: 0.02em; color: {GRAFITE};">'
               f'<span style="color: {VERDE}">#</span>VOTO'
               f'<span style="color: {AZUL}">NA</span>DEMOCRACIA</div>') if hashtag else "    "
    justif = "space-between" if hashtag else "flex-start"
    return f"""  <div style="height: {alto}px; flex-shrink: 0; background: {OFFWHITE}; border-bottom: {regua}px solid {MARINHO}; display: flex; align-items: center; justify-content: {justif}; padding: 0 {pad}px; box-sizing: border-box; overflow: hidden;">
    <div style="display: flex; flex-direction: column; align-items: flex-start; gap: {g1}px; line-height: 1;">
      <div style="display: flex; align-items: center; gap: {g2}px;">
        <span style="font-family: {ARCHIVO}; font-weight: 800; font-size: {pal}px; letter-spacing: 0.01em; color: {GRAFITE};">EL</span>
        {ONDAS.format(s=onda)}
        <span style="font-family: {ARCHIVO}; font-weight: 800; font-size: {pal}px; letter-spacing: 0.01em; color: {GRAFITE};">IÇÕES</span>
      </div>
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: {ano}px; letter-spacing: -0.01em; color: {OURO};">2026</div>
    </div>
    {direita}
  </div>"""


CAB_BANNER = cabecalho(70, 13.0, 25.2, 9.6, 18, 0.9, 0.8, True)
CAB_ALTO = cabecalho(115, 21.4, 41.4, 15.8, 30, 1.4, 1.3, False)


def preferencial():
    """Empilhada como a placa de referência entregue pelo Posto em 22/09: fundo
    azul da referência, moldura branca arredondada, o título numa caixa branca
    e os cinco pictogramas em branco. Sem a faixa institucional — decisão de
    22/09 — e em Montserrat, a fonte da campanha, no lugar da fonte da placa
    vendida. O canvas continua o fence banner de 2080 × 820 mm."""
    corpo = f"""<div style="width: 1040.0px; height: 410.0px; box-sizing: border-box; background: {PREFERENCIAL}; padding: 14px; display: flex; overflow: hidden;">
  <div style="flex-grow: 1; border: 6px solid {BRANCO}; border-radius: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; padding: 16px 30px;">
    <div style="background: {BRANCO}; border-radius: 12px; padding: 12px 40px 14px;">
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 54px; line-height: 1; color: {PREFERENCIAL}; letter-spacing: -0.005em; white-space: nowrap;">ATENDIMENTO PREFERENCIAL</div>
    </div>
    {picto_linha(altura=165, vao=24, tinta=BRANCO, sufixo="pref")}
  </div>
</div>"""
    return _molde(corpo=corpo, larg=1040, alt=410)


def vinil_preferencial():
    corpo = f"""<div style="width: 600.0px; height: 350.0px; box-sizing: border-box; background: #DDE4E2; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px;">
  <div style="font-family: {NUNITO}; font-weight: 800; font-size: 46px; color: {TINTA}; letter-spacing: 0.02em;">PREFERENCIAL</div>
  {picto_linha(altura=104, vao=12, sufixo="vinil")}
</div>"""
    return _molde(corpo=corpo, larg=600, alt=350)


def consulta():
    """P0 — "não sabe sua seção?" com o QR estático do TSE (nível H). Vai em
    dois pontos, um de cada lado do portão da Merrion Road, cada um ao lado de
    uma P0-Mestra."""
    qr = QR.read_text(encoding="utf-8").strip()
    assert qr.startswith("<svg") and 'viewBox="0 0 ' in qr, "data/qr_tse.svg: rode scripts/qr_tse.py --grava"
    qr = qr.replace('<svg ', '<svg width="210" height="210" style="display:block" aria-label="QR para a consulta de seção no site do TSE" ', 1)
    qr = qr.replace('stroke="#000"', f'stroke="{MARINHO}"')
    corpo = f"""<div style="width: 1040.0px; height: 410.0px; box-sizing: border-box; background: {CREME}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_BANNER}

  <div style="flex-grow: 1; display: flex; align-items: center; gap: 30px; padding: 0 40px 0 44px;">
    <div style="flex-grow: 1;">
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 82px; line-height: 0.94; color: {TINTA}; letter-spacing: -0.02em;">NÃO SABE<br>SUA SEÇÃO?</div>
      <div style="display: inline-block; margin-top: 16px; background: {VERDE}; color: {BRANCO}; font-family: {ARCHIVO}; font-weight: 700; font-size: 34px; padding: 12px 24px;">CONSULTE AQUI, ANTES DE ENTRAR</div>
    </div>
    <div style="flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 6px;">
      <div style="background: {BRANCO}; padding: 6px; line-height: 0;">{qr}</div>
      <div style="font-family: {ARCHIVO}; font-weight: 700; font-size: 16px; color: {TINTA}; text-align: center; line-height: 1.2;">SITE DO TSE<br><span style="font-weight: 600; font-size: 14px;">sua seção e seu local de votação</span></div>
    </div>
  </div>

</div>"""
    return _molde(corpo=corpo, larg=1040, alt=410)


# A boca de cada zona: corpo branco, a cor da porta só no bloco da letra, e as
# seções em células com borda de 3 px (6 mm no impresso) — decisão de 22/09.
# O dígito de 40 px dá 80 mm, o mínimo da tabela de leitura a 15 m; o bloco
# da letra tem 240 px para que as seis células caibam com o dígito tabular.
P4_COLUNAS = 6


def p4(porta, secoes):
    fundo, tinta = CORES[porta]
    celulas = "".join(
        f'<div style="background: {BRANCO}; text-align: center; padding: 3px 4px 5px;">'
        f'<span style="font-family: {ARCHIVO}; font-weight: 700; font-size: 40px; line-height: 1.05;'
        f' color: {TINTA}; font-variant-numeric: tabular-nums;">{s:04d}</span></div>'
        for s in secoes
    )
    vazias = (-len(secoes)) % P4_COLUNAS
    celulas += f'<div style="background: {BRANCO};"></div>' * vazias
    corpo = f"""<div style="width: 1040.0px; height: 410.0px; box-sizing: border-box; background: {BRANCO}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_BANNER}

  <div style="flex-grow: 1; background: {BRANCO}; display: flex; gap: 30px; padding: 0 36px 0 0;">
    <div style="width: 240px; flex-shrink: 0; background: {fundo}; color: {tinta}; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 14px 0 16px;">
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 190px; line-height: 0.80; letter-spacing: -0.04em;">{porta}</div>
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 25px; letter-spacing: 0.04em; margin-top: 6px;">PORTA {porta}</div>
    </div>
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 9px; justify-content: center; padding: 14px 0 16px; color: {TINTA};">
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 23px; letter-spacing: 0.03em; white-space: nowrap;">SUA SEÇÃO ESTÁ AQUI? ENTRE.</div>
      <div style="display: grid; grid-template-columns: repeat({P4_COLUNAS}, minmax(0, 1fr)); gap: 3px; background: {TINTA}; padding: 3px;">{celulas}</div>
      <div style="font-family: {ARCHIVO}; font-weight: 700; font-size: 21px; border-top: 3px solid {TINTA}; padding-top: 8px; margin-top: 2px;">Não está aqui? Siga em frente pelo corredor.</div>
    </div>
  </div>

</div>"""
    return _molde(corpo=corpo, larg=1040, alt=410)


# O corpo da placa fica encostado no topo, não centrado: o pull-up tem 2000 mm e
# o terço de baixo some atrás da fila. Assim o primeiro número cai por volta de
# 1.400 mm do chão, acima da cabeça de quem está na frente.
# Quanto menos seções no grupo, maior o dígito: a placa tem 725 px de corpo e
# no máximo quatro números, então sobra altura para gastar em legibilidade.
# 80 px no canvas de 425 px equivalem a 160 mm no pull-up de 850 mm.
DIGITO = {1: 130, 2: 112, 3: 96, 4: 80}


def seta(tam, cor, direcao):
    """Uma seta do tamanho do dígito, na cor da porta, apontando para a mesa."""
    lado = round(tam * 0.62)
    d = "M12 50 H88 M56 18 L88 50 L56 82" if direcao == "dir" else "M88 50 H12 M44 18 L12 50 L44 82"
    return (f'<svg width="{lado}" height="{lado}" viewBox="0 0 100 100" aria-hidden="true" style="display:block; flex-shrink:0">'
            f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def lados(grupo):
    """As mesas do par na ordem esquerda → direita para quem lê a placa, que
    fica entre as duas mesas, de frente para o salão: na parede oeste a mesa
    de menor y fica à esquerda (sul); na norte, a de menor x (oeste); na
    leste, a de maior y (norte). `coord` e `por_mesa` andam juntos."""
    pares = list(zip(grupo["coord"], grupo["por_mesa"]))
    pares.sort(key=lambda p: p[0], reverse=(grupo["parede"] == "leste"))
    return [secoes for _, secoes in pares]


def banner_bloco(grupo):
    porta = grupo["entrada"]
    fundo, tinta = CORES[porta]
    secoes = sorted(grupo["secoes"])
    tam = DIGITO[len(secoes)]
    mesas = lados(grupo)
    numero = (f'<div style="font-family: {ARCHIVO}; font-weight: 800; font-size: {tam}px;'
              f' line-height: 1.12; color: {TINTA}; font-variant-numeric: tabular-nums;">{{s:04d}}</div>')
    if len(mesas) == 1:
        # mesa isolada: a fila é uma só, não há lado a apontar
        numeros = "".join(numero.format(s=s) for s in mesas[0])
    else:
        # esquerda: seta e número; direita: número e seta. As duas mesas
        # separadas por um vão maior, para se lerem como dois grupos.
        esq, dir_ = mesas
        linhas = [f'<div style="display: flex; align-items: center; gap: 14px; align-self: flex-start;">'
                  f'{seta(tam, fundo, "esq")}{numero.format(s=s)}</div>' for s in esq]
        linhas.append('<div style="height: 26px; flex-shrink: 0;"></div>')
        linhas += [f'<div style="display: flex; align-items: center; gap: 14px; align-self: flex-end;">'
                   f'{numero.format(s=s)}{seta(tam, fundo, "dir")}</div>' for s in dir_]
        numeros = "".join(linhas)
    corpo = f"""<div style="width: 425.0px; height: 1000.0px; box-sizing: border-box; background: {CREME}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_ALTO}
  <div style="background: {fundo}; color: {tinta}; padding: 14px 20px 16px; display: flex; align-items: center; justify-content: space-between;">
    <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 104px; line-height: 0.86; letter-spacing: -0.03em;">{grupo["id"]}</div>
    <div style="font-family: {NUNITO}; font-weight: 700; font-size: 22px; text-align: right; line-height: 1.25;">PORTA {porta}<br><span style="opacity: 0.85; font-weight: 600;">{"parede " + PAREDE[porta]}</span></div>
  </div>
  <div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 4px; padding: 30px 24px 16px;">
    <div style="font-family: {NUNITO}; font-weight: 700; font-size: 17px; letter-spacing: 0.08em; color: {CINZA}; margin-bottom: 10px;">SEÇÕES DESTE CORREDOR</div>
    {numeros}
  </div>
  <div style="height: 10px; background: {fundo}; flex-shrink: 0;"></div>

</div>"""
    return _molde(corpo=corpo, larg=425, alt=1000)


# --------------------------------------------------------------------------
# Painel da porta e fim do corredor (23/09)
# --------------------------------------------------------------------------
# A ordem em que o eleitor encontra os grupos: na oeste e na leste a avenida
# sobe do sul para o norte, entao e a ordem da coordenada; na norte a avenida
# chega no meio, pelo T, e a lista segue a parede de oeste para leste.
def em_ordem(grupos, porta):
    gs = [g for g in grupos if g["entrada"] == porta]
    return sorted(gs, key=lambda g: min(g["coord"]))


# So as paredes cuja avenida corre RENTE a elas tem "comeco" e "fim": a A e a
# C. Na B a avenida chega perpendicular e desemboca no meio da parede, entao
# nem o primeiro nem o ultimo grupo ficam "no comeco" de coisa nenhuma.
AVENIDA_RENTE = {"A": "oeste", "C": "leste"}
MARCA_PONTA = {
    "primeiro": "LOGO NA ENTRADA DO CORREDOR",
    "ultimo": "NO FIM DO CORREDOR, O MAIS DISTANTE",
}


def painel_porta(porta, grupos):
    """O pull-up de 1000 x 2000 mm que fica na porta, com os grupos da parede.

    Ate 22/09 as tres peças eram escritas a mao, e a reordenacao da parede
    oeste em 23/09 deixou a da porta A errada em quatro linhas. Agora sai de
    `grupos_mesas.json`, como as dezesseis placas.
    """
    fundo, tinta = CORES[porta]
    gs = em_ordem(grupos, porta)
    linhas = []
    for i, g in enumerate(gs):
        marca = ""
        if porta in AVENIDA_RENTE:
            chave = "primeiro" if i == 0 else ("ultimo" if i == len(gs) - 1 else None)
            if chave:
                marca = (f'<div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 13px;'
                         f' letter-spacing: 0.06em; color: {fundo}; margin-top: 3px;">'
                         f'{MARCA_PONTA[chave]}</div>')
        numeros = " · ".join(f"{s:04d}" for s in sorted(g["secoes"]))
        linhas.append(
            f'<div style="display: flex; align-items: baseline; gap: 12px; padding: 10px 0;'
            f' border-bottom: 1px solid #E4DFCC; flex-grow: 1;">'
            f'<span style="font-family: {ARCHIVO}; font-weight: 800; font-size: 17px; color: {CINZA};'
            f' min-width: 34px;">{g["id"]}</span>'
            f'<span style="flex-grow: 1;">'
            f'<span style="font-family: {ARCHIVO}; font-weight: 700; font-size: 26px; color: {TINTA};'
            f' font-variant-numeric: tabular-nums; letter-spacing: -0.01em; white-space: nowrap;">'
            f'{numeros}</span>{marca}</span></div>')
    chamada = ("PROCURE A SUA SEÇÃO · NA ORDEM EM QUE VOCÊ VAI ANDAR"
               if porta in AVENIDA_RENTE else
               "PROCURE A SUA SEÇÃO · DA ESQUERDA PARA A DIREITA NA PAREDE")
    corpo = f"""<div style="width: 500.0px; height: 1000.0px; box-sizing: border-box; background: {CREME}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_ALTO}
  <div style="background: {fundo}; color: {tinta}; padding: 18px 26px 16px; display: flex; align-items: center; gap: 18px;">
    <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 150px; line-height: 0.8; letter-spacing: -0.04em;">{porta}</div>
    <div>
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 34px; letter-spacing: 0.02em;">PORTA {porta}</div>
      <div style="font-family: {ARCHIVO}; font-weight: 600; font-size: 22px; opacity: 0.88;">parede {PAREDE[porta]}</div>
    </div>
  </div>
  <div style="flex-grow: 1; padding: 20px 26px 26px; display: flex; flex-direction: column;">
    <div style="font-family: {ARCHIVO}; font-weight: 700; font-size: 19px; letter-spacing: 0.06em; color: {CINZA}; margin-bottom: 8px;">{chamada}</div>
    <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: stretch;">{"".join(linhas)}</div>
    <div style="font-family: {ARCHIVO}; font-weight: 700; font-size: 21px; color: {TINTA}; border-top: 3px solid {fundo}; padding-top: 12px; margin-top: 10px;">Cada grupo tem uma placa alta na boca do corredor.</div>
  </div>

</div>"""
    return _molde(corpo=corpo, larg=500, alt=1000)


def fim_corredor(porta, grupos):
    """A peça do fim do corredor: para quem andou demais e passou do seu grupo.

    O corredor da parede leste termina ao norte do ultimo grupo, entao quem
    chega ao fim tem TODOS os grupos atras de si -- e por isso as duas colunas
    saem desiguais: o ultimo grupo de um lado, os outros cinco do outro. As
    setas dizem esquerda e direita; os subtitulos dizem norte e sul, que e o
    que nao depende de para onde o eleitor esta virado.
    """
    fundo, tinta = CORES[porta]
    gs = em_ordem(grupos, porta)
    esq, dire = [gs[-1]], list(reversed(gs[:-1]))

    def coluna(lista, direcao, titulo, sub):
        alinha = "flex-start" if direcao == "esq" else "flex-end"
        numeros = "".join(
            f'<span style="font-family: {ARCHIVO}; font-weight: 700; font-size: 31px;'
            f' color: {TINTA}; font-variant-numeric: tabular-nums;">{s:04d}</span>'
            for g in lista for s in sorted(g["secoes"]))
        codigos = " · ".join(g["id"] for g in lista)
        cabeca = (f'{seta(64, fundo, direcao)}'
                  f'<div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 26px;'
                  f' letter-spacing: 0.03em; color: {fundo};">{titulo}</div>')
        if direcao != "esq":
            cabeca = (f'<div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 26px;'
                      f' letter-spacing: 0.03em; color: {fundo};">{titulo}</div>'
                      f'{seta(64, fundo, direcao)}')
        return (f'<div style="display: flex; flex-direction: column; align-items: {alinha}; gap: 6px; min-width: 0;">'
                f'<div style="display: flex; align-items: center; gap: 12px;">{cabeca}</div>'
                f'<div style="font-family: {ARCHIVO}; font-weight: 700; font-size: 15px;'
                f' letter-spacing: 0.05em; color: {CINZA};">{sub} · {codigos}</div>'
                f'<div style="display: flex; flex-wrap: wrap; gap: 4px 16px; justify-content: {alinha};">{numeros}</div>'
                f'</div>')

    corpo = f"""<div style="width: 1040.0px; height: 410.0px; box-sizing: border-box; background: {BRANCO}; display: flex; flex-direction: column; overflow: hidden;">
{CAB_BANNER}

  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 14px 30px 16px; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 14px;">
      <div style="background: {fundo}; color: {tinta}; font-family: {ARCHIVO}; font-weight: 800; font-size: 44px; line-height: 1; padding: 8px 16px 10px;">{porta}</div>
      <div style="font-family: {ARCHIVO}; font-weight: 800; font-size: 31px; letter-spacing: 0.02em; color: {TINTA};">FIM DO CORREDOR · PASSOU DA SUA SEÇÃO?</div>
    </div>
    <div style="display: flex; align-items: center; gap: 22px; flex-grow: 1;">
      <div style="width: 232px; flex-shrink: 0;">{coluna(esq, "esq", "AQUI", "fim da parede, ao norte")}</div>
      <div style="width: 3px; align-self: stretch; background: {TINTA};"></div>
      <div style="flex-grow: 1; min-width: 0;">{coluna(dire, "dir", "VOLTE", "para o sul, de volta à porta")}</div>
    </div>
  </div>

</div>"""
    return _molde(corpo=corpo, larg=1040, alt=410)


def pecas():
    grupos = json.loads(FONTE.read_text(encoding="utf-8"))["grupos"]
    saida = {"P0-Consulta": consulta(), "P5-Preferencial": preferencial(),
             "P5-VinilPref": vinil_preferencial()}
    portas = por_porta()
    for porta in "ABC":
        saida[f"P4-Zona{porta}"] = p4(porta, portas[porta])
    for g in grupos:
        saida[f"P6-Bloco{g['id']}"] = banner_bloco(g)
    for porta in "ABC":
        saida[f"P6-Painel{porta}"] = painel_porta(porta, grupos)
    saida["P4-FimCorredorC"] = fim_corredor("C", grupos)
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
