# -*- coding: utf-8 -*-
"""Paleta, logotipo e molde de peca -- o que os tres geradores compartilham.

Antes isto estava copiado nos tres arquivos, e uma correcao de logotipo tinha
de ser feita tres vezes.  Aqui e uma vez so.

As cores sao as da identidade oficial Eleicoes 2026, amostradas da carta de
cores e do logotipo entregues pelo Posto em 17-18/09/2026
(referencias/identidade_visual_tse_2026/).
"""

# ---------------------------------------------------------------- a paleta
# A carta "CORES" traz onze tons em tres familias -- verdes, azuis e quentes --
# "inspirados nas cores vibrantes da nossa bandeira nacional".
PALETA = {
    'ardosia':     '#5A6E6E',   # verde-ardosia escuro
    'verde':       '#648232',
    'verde_claro': '#96B43C',
    'limao':       '#B4C83C',
    'azul_ard':    '#5A6E96',
    'azul_cinza':  '#6E82A0',
    'azul':        '#5A8CAA',
    'azul_claro':  '#78AAC8',
    'laranja':     '#DC963C',
    'ouro':        '#DCB43C',
    'amarelo':     '#E6BE3C',
}

# Do logotipo: a tipografia e carvao, nao marinho, e o "2026" e ouro.
CARVAO = '#3F3F3F'          # "ELEICOES" e todo texto corrido
CARVAO_SUAVE = '#6B6B6B'    # texto secundario
OURO_LOGO = '#E8B800'       # o "2026"
FAIXA_E = ('#E8B800', '#4888A8', '#588018')   # as tres ondas do E estilizado
OSSO = '#F2EFE2'            # o fundo creme das pecas de lista
OSSO_ESCURO = '#E4DFCC'     # rulers e divisoes sobre o osso

# As tres portas: a cor de cada uma e a da FITA DE PISO comprada, nao da
# paleta -- e o chao que o eleitor pisa que manda.  Batem de perto com tres
# tons da paleta, o que mantem o conjunto coerente.
COR = {'A': '#33507E', 'B': '#E8C63A', 'C': '#DE7343'}
TEXTO = {'A': '#FFFFFF', 'B': CARVAO, 'C': CARVAO}
TINTA = {'A': '#33507E', 'B': '#7D6004', 'C': '#9C4118'}   # a cor como TEXTO
PAREDE = {'A': 'oeste', 'B': 'norte', 'C': 'leste'}
PORTA = {'A': 'S4', 'B': 'S5', 'C': 'S6'}

SANS = "'Nunito Sans', system-ui, sans-serif"
DISP = "'Archivo', 'Nunito Sans', sans-serif"


def logotipo(alt_px: float, escuro: bool = True) -> str:
    """O logotipo Eleições 2026, na proporção do original.

    "ELEIÇÕES" em carvão (ou branco, sobre fundo escuro) com o E substituído
    por três ondas — amarelo, azul, verde, a bandeira; "2026" em ouro embaixo,
    maior.  Sem a marca da Justiça Eleitoral: o Posto pediu que saísse.

    É MARCAÇÃO DE LUGAR: mostra onde a arte oficial entra e quanto ocupa.
    A arte em vetor tem de vir do TSE antes de qualquer impressão.
    """
    h = alt_px
    tinta = '#FFFFFF' if escuro else CARVAO
    ouro = '#F2CE3A' if escuro else OURO_LOGO
    # O E: três ondas grossas, na altura de caixa alta da própria letra —
    # no logotipo oficial elas ocupam a caixa inteira de um E e leem-se como
    # a bandeira.  Desenhá-las pequenas abre um buraco em "EL_IÇÕES".
    corpo_px = h * 0.30                 # corpo da palavra ELEIÇÕES
    caixa_px = corpo_px * 0.74          # altura de caixa alta
    larg_px = caixa_px * 1.00           # o bloco do E é tão largo quanto alto
    # Ondas de amplitude baixa e traço grosso: é isso que faz três BARRAS que
    # se leem como um E.  Amplitude alta afina a barra e o bloco vira rabisco.
    ondas = ''.join(
        f'<path d="M-1 {4.6+i*7.6} q 6.5 -2.0 13 0 t 13 0" fill="none" '
        f'stroke="{c}" stroke-width="6.3" stroke-linecap="butt"/>'
        for i, c in enumerate(FAIXA_E))
    return f"""<div style="display: flex; flex-direction: column; align-items: flex-start; gap: {h*0.02:.1f}px; line-height: 1;">
      <div style="display: flex; align-items: center; gap: {corpo_px*0.06:.1f}px;">
        <span style="font-family: {DISP}; font-weight: 800; font-size: {corpo_px:.1f}px; letter-spacing: 0.01em; color: {tinta};">EL</span>
        <svg width="{larg_px:.1f}" height="{caixa_px:.1f}" viewBox="0 0 24 24" aria-hidden="true" style="display:block">{ondas}</svg>
        <span style="font-family: {DISP}; font-weight: 800; font-size: {corpo_px:.1f}px; letter-spacing: 0.01em; color: {tinta};">IÇÕES</span>
      </div>
      <div style="font-family: {DISP}; font-weight: 800; font-size: {h*0.58:.1f}px; letter-spacing: -0.01em; color: {ouro};">2026</div>
    </div>"""


def hashtag(tam_px: float, escuro: bool = False) -> str:
    """#VOTONADEMOCRACIA, com o NA em azul, como no logotipo."""
    tinta = '#FFFFFF' if escuro else CARVAO
    return (f'<div style="font-family: {DISP}; font-weight: 700; font-size: {tam_px:.1f}px; '
            f'letter-spacing: 0.02em; color: {tinta};">#VOTO'
            f'<span style="color: {PALETA["azul"]}">NA</span>DEMOCRACIA</div>')


def faixa(alt_px: float, larg_px: float = 0, fundo: str = None) -> str:
    """A faixa institucional do topo de cada peça.

    Fundo verde-ardósia da paleta, não amarelo: desde 17/09 o amarelo quer
    dizer "porta B", e uma faixa amarela em toda peça diria "B" a 30 m.

    `larg_px` é a largura da peça: numa peça estreita a hashtag não cabe ao
    lado do logotipo e sai, em vez de transbordar a borda.
    """
    h = alt_px
    fundo = fundo or PALETA['ardosia']
    # o logotipo ocupa ~2,6 h de largura; a hashtag pede outros ~9 do seu corpo
    cabe_hashtag = larg_px == 0 or larg_px > h * 2.6 + h * 0.20 * 9 + h * 0.8
    tag = hashtag(h * 0.20, escuro=True) if cabe_hashtag else ''
    return f"""  <div style="height: {h:.0f}px; flex-shrink: 0; background: {fundo}; display: flex; align-items: center; justify-content: {'space-between' if tag else 'flex-start'}; padding: 0 {h*0.26:.0f}px; box-sizing: border-box; overflow: hidden;">
    {logotipo(h * 0.62, escuro=True)}
    {tag}
  </div>
"""


def estilo_pagina() -> str:
    """O <helmet> comum das pranchas."""
    return f"""<helmet>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap');
    body {{ margin: 0; background: {OSSO}; }}
    a {{ color: {PALETA['azul']}; }} a:hover {{ color: {CARVAO}; }}
  </style>
</helmet>"""
