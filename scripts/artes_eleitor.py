#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Artes para o eleitor — Eleições 2026, Posto de Dublin.

Gera quatro peças quadradas de 1080 x 1080 (post de feed) em saidas/artes/,
mais um index.html de conferência. Só biblioteca padrão; nada acessa a rede na
geração (as fontes são buscadas apenas na hora de ver o HTML).

O conteúdo vem, sem exceção, de fonte já versionada aqui:

  · datas, horário, local, aptos e seções ....... CLAUDE.md e saidas/dados.json
  · o percurso em cinco passos ................. slide 9 do briefing de 23/09
    ("Da calçada até a urna"), Apresentações/2026.9.23_Equipe Embaixada_Briefing.pptx
  · a tabela seção -> porta (51 seções) ......... mapa/sinalizacao/P1-Portao.dc.html
  · cores, tipografia e a regra da letra ........ mapa/sinalizacao/Main.dc.html
  · portas da fachada sul (S4..S7) .............. data/prancheta_hall2.json

REGRA QUE NÃO SE QUEBRA (Main.dc.html, 17/09): a LETRA identifica a fila; a cor
é apoio. Em nenhuma peça a cor aparece sozinha — para um deuteranope, o amarelo
de B e a abóbora de C só diferem em claridade.

O LOGOTIPO DESENHADO AQUI É MARCAÇÃO DE LUGAR, como nas peças de sinalização:
mostra onde a arte oficial entra e quanto espaço ocupa. A arte em vetor tem de
vir do TSE, com a fonte da campanha e a autorização de uso da marca por posto no
exterior. Não publicar sem trocar.

Uso:
    python3 scripts/artes_eleitor.py            # escreve saidas/artes/
    python3 scripts/artes_eleitor.py --confere  # só confere, não escreve
"""

import html
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "saidas", "artes")

# ---------------------------------------------------------------- identidade
# Main.dc.html, "cores das fitas" — a cor da porta é a cor da fita comprada.
MARINHO = "#042B5A"   # tipografia e régua da faixa
OFFWHITE = "#F0F0E8"  # faixa institucional e fundo de lista
CAMPANHA = "#F8C030"  # amarelo da campanha: SÓ dentro do lockup
BRANCO = "#FFFFFF"
CINZA = "#5A6270"
CINZA_CLARO = "#C9CFD4"

ZONAS = {
    "A": {"cor": "#33507E", "sobre": BRANCO,  "porta": "S4", "parede": "oeste"},
    "B": {"cor": "#E8C63A", "sobre": MARINHO, "porta": "S5", "parede": "norte"},
    "C": {"cor": "#DE7343", "sobre": MARINHO, "porta": "S6", "parede": "leste"},
}

SANS = ("Archivo, 'Nunito Sans', 'Liberation Sans', 'DejaVu Sans', "
        "'Helvetica Neue', Arial, sans-serif")

L = 1080          # lado da peça
MARGEM = 76
CAB = 132         # altura da faixa institucional
RODAPE = 92

# ------------------------------------------------------------------- helpers


def esc(t):
    return html.escape(str(t), quote=True)


def txt(x, y, s, tam=32, peso=600, cor=None, anc="start", esp=0, ll=None,
        maiusc=False, op=1.0):
    cor = cor or MARINHO
    est = [
        "font-family:%s" % SANS,
        "font-size:%gpx" % tam,
        "font-weight:%d" % peso,
        "fill:%s" % cor,
    ]
    if esp:
        est.append("letter-spacing:%gpx" % esp)
    if maiusc:
        est.append("text-transform:uppercase")
    if op != 1.0:
        est.append("opacity:%g" % op)
    extra = ' dominant-baseline="%s"' % ll if ll else ""
    return ('<text x="%g" y="%g" text-anchor="%s" style="%s"%s>%s</text>'
            % (x, y, anc, ";".join(est), extra, esc(s)))


def rect(x, y, w, h, fill, r=0, stroke=None, sw=0, op=1.0):
    s = '<rect x="%g" y="%g" width="%g" height="%g" fill="%s"' % (x, y, w, h, fill)
    if r:
        s += ' rx="%g"' % r
    if stroke:
        s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if op != 1.0:
        s += ' opacity="%g"' % op
    return s + "/>"


def circulo(cx, cy, r, fill, stroke=None, sw=0):
    s = '<circle cx="%g" cy="%g" r="%g" fill="%s"' % (cx, cy, r, fill)
    if stroke:
        s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    return s + "/>"


def passo(cx, cy, n, r=27, fundo=MARINHO, tinta=BRANCO):
    """Bolota numerada dos cinco passos do percurso."""
    return (circulo(cx, cy, r, fundo)
            + txt(cx, cy + r * 0.36, n, tam=r * 1.18, peso=800, cor=tinta,
                  anc="middle"))


def lockup(x, y, escala=1.0, tinta=MARINHO):
    """Marcação de lugar do logotipo oficial. TROCAR PELA ARTE DO TSE."""
    e = escala
    g = ['<g transform="translate(%g,%g) scale(%g)">' % (x, y, e)]
    g.append(txt(0, 0, "ELEIÇÕES", tam=31, peso=800, cor=tinta, esp=1.6))
    g.append(txt(0, 36, "2026", tam=40, peso=800, cor=CAMPANHA, esp=0.6))
    g.append(txt(96, 34, "#VOTONADEMOCRACIA", tam=13.5, peso=700, cor=tinta,
                 esp=1.2, op=0.85))
    g.append("</g>")
    return "".join(g)


def moldura(titulo_faixa, rodape_esq, rodape_dir, corpo, fundo=BRANCO):
    """Faixa institucional off-white com régua marinha + rodapé marinho."""
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'viewBox="0 0 %d %d">' % (L, L, L, L)]
    p.append(rect(0, 0, L, L, fundo))
    p.append(rect(0, 0, L, CAB, OFFWHITE))
    p.append(rect(0, CAB - 7, L, 7, MARINHO))
    p.append(lockup(MARGEM, 48))
    p.append(txt(L - MARGEM, 62, titulo_faixa, tam=17, peso=700, cor=MARINHO,
                 anc="end", esp=2.4))
    p.append(txt(L - MARGEM, 90, "Embaixada do Brasil em Dublin", tam=15,
                 peso=500, cor=CINZA, anc="end"))
    p.append(corpo)
    p.append(rect(0, L - RODAPE, L, RODAPE, MARINHO))
    p.append(txt(MARGEM, L - RODAPE + 38, rodape_esq, tam=19, peso=700,
                 cor=BRANCO))
    p.append(txt(MARGEM, L - RODAPE + 66, rodape_dir, tam=16, peso=400,
                 cor="#AFC3DA"))
    p.append("</svg>")
    return "".join(p)


# ----------------------------------------------------- dados: seção -> porta

def tabela_mestra():
    """Lê as 51 seções e a porta de cada uma da peça P1-Portao."""
    caminho = os.path.join(RAIZ, "mapa", "sinalizacao", "P1-Portao.dc.html")
    bruto = open(caminho, encoding="utf-8").read()
    bruto = re.sub(r"<script.*?</script>", " ", bruto, flags=re.S)
    bruto = re.sub(r"<style.*?</style>", " ", bruto, flags=re.S)
    plano = html.unescape(re.sub(r"<[^>]+>", " ", bruto))
    pares = re.findall(r"\b(\d{4})\s+([ABC])\b", plano)
    mestra = {}
    for secao, porta in pares:
        mestra[secao] = porta
    return mestra


def confere(mestra):
    """Sai com código 1 se a tabela não fechar com os fatos do CLAUDE.md."""
    erros = []
    if len(mestra) != 51:
        erros.append("a tabela mestra tem %d seções, e não 51" % len(mestra))
    conta = {"A": 0, "B": 0, "C": 0}
    for porta in mestra.values():
        conta[porta] += 1
    for letra, peca in (("A", "P4-ZonaA"), ("B", "P4-ZonaB"), ("C", "P4-ZonaC")):
        caminho = os.path.join(RAIZ, "mapa", "sinalizacao", peca + ".dc.html")
        plano = html.unescape(re.sub(r"<[^>]+>", " ",
                                     open(caminho, encoding="utf-8").read()))
        na_boca = set(re.findall(r"\b\d{4}\b", plano)) - {"2026"}
        na_mestra = {s for s, p in mestra.items() if p == letra}
        if na_boca != na_mestra:
            erros.append("a boca da zona %s e a tabela mestra discordam: %s"
                         % (letra, sorted(na_boca ^ na_mestra)))
    print("Tabela mestra: %d seções · A %d · B %d · C %d"
          % (len(mestra), conta["A"], conta["B"], conta["C"]))
    if erros:
        for e in erros:
            print("  QUEBRA: " + e)
        return 1
    print("  as três bocas de zona batem com a tabela mestra")
    return 0


# ------------------------------------------------------------------- arte 1

def arte_1():
    """Quando, onde, e o que levar."""
    p = []
    y = CAB + 82
    p.append(txt(MARGEM, y, "DOMINGO", tam=26, peso=700, cor=CINZA, esp=6))
    p.append(txt(MARGEM, y + 108, "4 de outubro", tam=104, peso=800,
                 cor=MARINHO, esp=-2.5))
    p.append(txt(MARGEM, y + 178, "8h às 17h · horário de Dublin", tam=40,
                 peso=600, cor=MARINHO))

    # bloco do local
    by = y + 226
    p.append(rect(MARGEM, by, L - 2 * MARGEM, 124, OFFWHITE, r=6))
    p.append(rect(MARGEM, by, 10, 124, MARINHO))
    p.append(txt(MARGEM + 38, by + 44, "RDS · HALL 2", tam=30, peso=800,
                 cor=MARINHO, esp=1))
    p.append(txt(MARGEM + 38, by + 84, "Merrion Road, Ballsbridge, Dublin 4",
                 tam=26, peso=500, cor=CINZA))

    # três lembretes
    ly = by + 176
    itens = [
        ("Documento oficial brasileiro com foto",
         "e-Título, passaporte, RG, CNH ou carteira profissional."),
        ("Saiba o número da sua seção antes de sair de casa",
         "São quatro dígitos, como no e-Título. É o que organiza toda a fila."),
        ("Se houver 2º turno: domingo, 25 de outubro",
         "Mesmo local, mesmo horário."),
    ]
    for i, (chave, linha) in enumerate(itens):
        yy = ly + i * 104
        p.append(circulo(MARGEM + 17, yy + 6, 17, MARINHO))
        p.append(txt(MARGEM + 17, yy + 14, "✓", tam=21, peso=800, cor=BRANCO,
                     anc="middle"))
        p.append(txt(MARGEM + 54, yy + 14, chave, tam=29, peso=700,
                     cor=MARINHO))
        p.append(txt(MARGEM + 54, yy + 50, linha, tam=23, peso=400, cor=CINZA))

    return moldura(
        "ELEIÇÕES 2026 · 1º TURNO",
        "16.794 eleitores aptos · 51 seções · 28 urnas",
        "Não sabe a sua seção? Há uma mesa de consulta na calçada, antes do portão.",
        "".join(p))


# ------------------------------------------------------------------- arte 2

def arte_2():
    """O percurso, da calçada até a urna — o mapa simplificado do slide 9."""
    p = []
    y = CAB + 74
    p.append(txt(MARGEM, y, "O PERCURSO", tam=22, peso=700, cor=CINZA, esp=6))
    p.append(txt(MARGEM, y + 62, "Da calçada até a urna", tam=62, peso=800,
                 cor=MARINHO, esp=-1.4))

    # ---- quadro do esquema
    qx, qy, qw, qh = MARGEM, y + 92, L - 2 * MARGEM, 372
    p.append(rect(qx, qy, qw, qh, OFFWHITE, r=6))

    # Merrion Road, no topo
    p.append(rect(qx, qy, qw, 46, CINZA_CLARO))
    p.append(txt(qx + 20, qy + 30, "MERRION ROAD", tam=19, peso=700,
                 cor=MARINHO, esp=3))
    p.append(rect(qx + 96, qy + 34, 96, 24, MARINHO, r=3))
    p.append(txt(qx + 144, qy + 51, "PORTÃO", tam=14, peso=800, cor=BRANCO,
                 anc="middle", esp=1))

    # Hall 2
    hx, hy, hw, hh = qx + 42, qy + 74, qw - 160, 92
    p.append(rect(hx, hy, hw, hh, BRANCO, r=4, stroke=MARINHO, sw=3))
    p.append(txt(hx + 20, hy + 38, "HALL 2", tam=28, peso=800, cor=MARINHO))
    p.append(txt(hx + 20, hy + 64, "o salão de votação · 28 urnas nas paredes",
                 tam=18, peso=400, cor=CINZA))

    # portas na fachada sul (S4 A · S5 B · S6 C · S7 preferencial)
    largura_porta, passo_porta = 74, 92
    x0 = hx + hw - 40 - passo_porta * 3 - largura_porta
    portas = [("A", ZONAS["A"]), ("B", ZONAS["B"]), ("C", ZONAS["C"])]
    xs = {}
    for i, (letra, z) in enumerate(portas):
        px = x0 + i * passo_porta
        xs[letra] = px + largura_porta / 2
        p.append(rect(px, hy + hh - 14, largura_porta, 28, z["cor"], r=3))
        p.append(txt(px + largura_porta / 2, hy + hh + 8, letra, tam=22,
                     peso=800, cor=z["sobre"], anc="middle"))
    pref_x = x0 + 3 * passo_porta
    p.append(rect(pref_x, hy + hh - 14, largura_porta, 28, MARINHO, r=3))
    p.append(txt(pref_x + largura_porta / 2, hy + hh + 7, "PREF", tam=15,
                 peso=800, cor=BRANCO, anc="middle"))

    # apron
    ay = hy + hh + 18
    p.append(txt(hx + 20, ay + 24, "apron · 14,0 m · travessia", tam=17,
                 peso=500, cor=CINZA))

    # Ring 3, com as três zonas
    ry = ay + 34
    rh = qy + qh - ry - 22
    p.append(rect(hx, ry, hw, rh, BRANCO, r=4, stroke=MARINHO, sw=3))
    p.append(txt(hx + 20, ry + 30, "RING 3 · pátio de fila, ao ar livre",
                 tam=19, peso=700, cor=MARINHO))
    zy, zh, zw = ry + 44, rh - 58, 74
    for letra, z in portas:
        zx = xs[letra] - zw / 2
        p.append(rect(zx, zy, zw, zh, z["cor"], r=3, op=0.92))
        p.append(txt(xs[letra], zy + zh / 2 + 13, letra, tam=38, peso=800,
                     cor=z["sobre"], anc="middle"))

    # caminho: portão -> lateral leste -> canto nordeste do Ring 3
    cx = qx + qw - 30
    p.append('<path d="M %g %g H %g V %g H %g" fill="none" stroke="%s" '
             'stroke-width="5" stroke-dasharray="11 9" stroke-linecap="round"/>'
             % (qx + 144, qy + 64, cx, ry + 24, hx + hw, MARINHO))
    # a fila sobe: da zona, pelo apron, até a porta
    for letra in "ABC":
        p.append('<path d="M %g %g V %g" fill="none" stroke="%s" '
                 'stroke-width="4" stroke-linecap="round" opacity="0.55"/>'
                 % (xs[letra], zy - 6, hy + hh + 16, MARINHO))

    # bolotas dos cinco passos
    p.append(passo(qx + 252, qy + 48, 1, r=19))
    p.append(passo(cx, qy + 150, 2, r=19))
    p.append(passo(hx + hw + 14, ry + 24, 3, r=19))
    p.append(passo(xs["A"] - 70, zy + zh / 2, 4, r=19))
    p.append(passo(xs["A"] - 70, hy + hh, 5, r=19))

    # ---- os cinco passos, em texto
    ly = qy + qh + 36
    linhas = [
        ("Entre pelo portão, na Merrion Road",
         "Antes do portão, a mesa de consulta: quem não sabe a seção descobre ali."),
        ("Contorne o Hall 2 pela lateral leste",
         "O caminho desemboca entre o salão e o pátio."),
        ("Entre no Ring 3 pelo canto nordeste",
         "O corredor distribui: C primeiro, B depois, A no fim."),
        ("Procure a sua letra e entre na fila",
         "As três zonas têm o mesmo tamanho. Entra-se pelo fundo."),
        ("Atravesse o apron e entre pela sua porta",
         "Da porta até a urna é sempre a mesma letra."),
    ]
    for i, (chave, sub) in enumerate(linhas):
        yy = ly + i * 54
        p.append(passo(MARGEM + 20, yy, i + 1, r=19))
        p.append(txt(MARGEM + 54, yy - 3, chave, tam=25, peso=700, cor=MARINHO))
        p.append(txt(MARGEM + 54, yy + 23, sub, tam=18, peso=400, cor=CINZA))

    return moldura(
        "COMO CHEGAR ATÉ A SUA URNA",
        "Esquema do percurso — não está em escala",
        "Preferencial: a porta à direita da C, sem fila.",
        "".join(p))


# ------------------------------------------------------------------- arte 3

def arte_3(mestra):
    """A sua seção diz a sua letra — as 51 seções, por porta."""
    p = []
    y = CAB + 70
    p.append(txt(MARGEM, y, "ANTES DE SAIR DE CASA", tam=22, peso=700,
                 cor=CINZA, esp=5))
    p.append(txt(MARGEM, y + 58, "A sua seção diz", tam=58, peso=800,
                 cor=MARINHO, esp=-1.4))
    p.append(txt(MARGEM, y + 116, "a sua letra", tam=58, peso=800,
                 cor=MARINHO, esp=-1.4))
    p.append(txt(MARGEM, y + 158, "Procure os seus quatro dígitos. A letra ao "
                 "lado é a sua fila,", tam=22, peso=400, cor=CINZA))
    p.append(txt(MARGEM, y + 186, "a sua porta e a sua parede — do pátio até "
                 "a urna.", tam=22, peso=400, cor=CINZA))

    cy = y + 218
    ch = L - RODAPE - cy - 78
    cw = (L - 2 * MARGEM - 2 * 22) / 3
    for i, letra in enumerate("ABC"):
        z = ZONAS[letra]
        cx = MARGEM + i * (cw + 22)
        p.append(rect(cx, cy, cw, ch, OFFWHITE, r=6))
        p.append(rect(cx, cy, cw, 96, z["cor"], r=6))
        p.append(rect(cx, cy + 74, cw, 22, z["cor"]))
        p.append(txt(cx + 22, cy + 66, letra, tam=62, peso=800, cor=z["sobre"]))
        p.append(txt(cx + cw - 22, cy + 44, "PORTA " + letra, tam=20, peso=800,
                     cor=z["sobre"], anc="end", esp=1))
        p.append(txt(cx + cw - 22, cy + 72, "parede " + z["parede"], tam=18,
                     peso=500, cor=z["sobre"], anc="end", op=0.85))

        secoes = sorted(s for s, porta in mestra.items() if porta == letra)
        col = 2
        por_col = (len(secoes) + col - 1) // col
        for j, s in enumerate(secoes):
            c, lin = j // por_col, j % por_col
            p.append(txt(cx + 26 + c * (cw / 2 - 12), cy + 140 + lin * 34, s,
                         tam=27, peso=600, cor=MARINHO))
        p.append(txt(cx + cw / 2, cy + ch - 20,
                     "%d seções" % len(secoes), tam=18, peso=600, cor=CINZA,
                     anc="middle"))

    p.append(txt(L / 2, L - RODAPE - 40,
                 "As mesas não têm número: cada uma traz as seções que votam nela.",
                 tam=23, peso=600, cor=MARINHO, anc="middle"))

    return moldura(
        "SEÇÃO → PORTA → PAREDE",
        "51 seções · 28 urnas · 3 portas",
        "A letra é o que vale. A cor é só apoio.",
        "".join(p))


# ------------------------------------------------------------------- arte 4

def arte_4():
    """Preferencial, celular, comprovante — e a hora de ir."""
    p = []
    y = CAB + 74
    p.append(txt(MARGEM, y, "NO DIA", tam=22, peso=700, cor=CINZA, esp=6))
    p.append(txt(MARGEM, y + 62, "O que você precisa", tam=56, peso=800,
                 cor=MARINHO, esp=-1.4))
    p.append(txt(MARGEM, y + 118, "saber na hora", tam=56, peso=800,
                 cor=MARINHO, esp=-1.4))

    # preferencial, em destaque
    by = y + 156
    p.append(rect(MARGEM, by, L - 2 * MARGEM, 150, MARINHO, r=6))
    p.append(txt(MARGEM + 34, by + 48, "ATENDIMENTO PREFERENCIAL", tam=25,
                 peso=800, cor=BRANCO, esp=2))
    p.append(txt(MARGEM + 34, by + 88,
                 "Idoso, gestante, lactante, pessoa com deficiência",
                 tam=25, peso=500, cor="#CFE0F2"))
    p.append(txt(MARGEM + 34, by + 122,
                 "e quem os acompanha: entram sem fila, pela porta à direita da C.",
                 tam=25, peso=500, cor="#CFE0F2"))

    # quatro lembretes
    ly = by + 196
    itens = [
        ("Leve o documento na mão",
         "Documento oficial brasileiro com foto. O mesário confere — e só ele."),
        ("A maior fila do dia é na abertura",
         "Se puder escolher, evite as duas primeiras horas."),
        ("O celular fica na mesa dos celulares",
         "Você o recolhe ao sair da cabine, antes de pegar o comprovante."),
        ("Saída pela mesma faixa da parede",
         "Quem votou não atravessa a fila de quem está entrando."),
    ]
    for i, (chave, sub) in enumerate(itens):
        yy = ly + i * 96
        p.append(rect(MARGEM, yy - 26, 6, 66, MARINHO))
        p.append(txt(MARGEM + 26, yy, chave, tam=29, peso=700, cor=MARINHO))
        p.append(txt(MARGEM + 26, yy + 32, sub, tam=22, peso=400, cor=CINZA))

    return moldura(
        "ELEITOR · 4 DE OUTUBRO",
        "Voluntário orienta, não decide",
        "Quem confere documento e identifica o eleitor é o mesário, sempre.",
        "".join(p))


# ---------------------------------------------------------------------- main

PECAS = [
    ("01-quando-e-onde", "Quando, onde e o que levar", arte_1),
    ("02-percurso", "Da calçada até a urna", arte_2),
    ("03-secao-porta", "A sua seção diz a sua letra", arte_3),
    ("04-no-dia", "O que saber na hora", arte_4),
]


def main(argv):
    so_confere = "--confere" in argv
    mestra = tabela_mestra()
    codigo = confere(mestra)
    if so_confere:
        return codigo
    if codigo:
        print("  não gravei nada: a conferência quebrou")
        return codigo

    os.makedirs(SAIDA, exist_ok=True)
    cartoes = []
    for chave, titulo, fn in PECAS:
        svg = fn(mestra) if fn is arte_3 else fn()
        caminho = os.path.join(SAIDA, chave + ".svg")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(svg)
        print("  %s.svg · %s" % (chave, titulo))
        cartoes.append('<figure><img src="%s.svg" alt="%s"><figcaption>'
                       '<b>%s</b> · %s.svg</figcaption></figure>'
                       % (chave, esc(titulo), esc(titulo), chave))

    indice = """<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Artes para o eleitor · Eleições 2026 · Dublin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap">
<style>
 body{margin:0;background:#E9E6DC;color:#042B5A;
      font:16px/1.5 Archivo,'Liberation Sans',system-ui,sans-serif;padding:40px 24px 80px}
 h1{font-size:30px;margin:0 0 6px} p.lead{margin:0 0 32px;max-width:70ch;color:#5A6270}
 .g{display:grid;gap:32px;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));
    max-width:1400px;margin:0 auto}
 figure{margin:0} img{width:100%%;display:block;border:1px solid #C9CFD4}
 figcaption{margin-top:10px;font-size:14px;color:#5A6270}
 .aviso{max-width:70ch;margin:0 auto 32px;background:#FFF4D6;border-left:6px solid #F8C030;
        padding:14px 18px;font-size:15px}
</style>
<h1>Artes para o eleitor</h1>
<p class="lead">Quatro peças de 1080 × 1080 para o feed. Geradas por
<code>scripts/artes_eleitor.py</code> a partir do briefing de 23/09, do sistema
visual de sinalização e da tabela mestra seção → porta.</p>
<div class="aviso"><b>Antes de publicar:</b> o logotipo destas peças é marcação de
lugar. A arte oficial em vetor tem de vir do TSE, com a fonte da campanha e a
autorização de uso da marca por posto no exterior.</div>
<div class="g">%s</div>
</html>""" % "\n".join(cartoes)
    with open(os.path.join(SAIDA, "index.html"), "w", encoding="utf-8") as f:
        f.write(indice)
    print("  index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
