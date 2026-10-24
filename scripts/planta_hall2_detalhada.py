"""Planta do Hall 2 em alta resolucao, com as 28 MRVs desenhadas por inteiro.

Cada MRV e o modulo de 4,10 x 0,90 m da prancheta: mesa-cavalete dos mesarios
(1,70 x 0,80 m), mesa redonda de 0,90 m do eleitor com a urna, a vaga do
eleitor (0,90 m) e a passagem (0,60 m). Sobre ele a planta traz as portas
(entradas, saidas, emergencia, fechadas), as tres avenidas (azul A, amarela B,
vermelha C), a pequena avenida da parede norte, a barreira da opcao Definitiva
e a fita, e um PONTO em cada lugar em que vai um banner.

Le a geometria de ``separadores_fila.py`` (a mesma das avenidas e dos banners
ja aprovados) e nao altera nenhum dado. Sem ``--grava`` so confere.

    python3 scripts/planta_hall2_detalhada.py           # confere
    python3 scripts/planta_hall2_detalhada.py --grava         # SVG, em portugues e em ingles
    python3 scripts/planta_hall2_detalhada.py --grava --png   # SVG + PNG a 2x (node + Chromium)
"""
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import separadores_fila as sf  # noqa: E402

RAIZ, SAIDAS = sf.RAIZ, sf.SAIDAS
FONTE = "Montserrat, 'Liberation Sans', Helvetica, Arial, sans-serif"

S = 52.0                      # px por metro
ME, MT = 290, 250             # margens: oeste (rotulos de porta) e norte (titulo)
MS, MD = 250, 300             # margem sul (portas + apron) e leste (rotulos)
PAINEL = 800                  # coluna da legenda e do modulo ampliado
GAP = 40

# Modulo da prancheta (data/prancheta_hall2.json -> modulo): mesa 1,70 x 0,80,
# urna 0,90, eleitor 0,90, passagem 0,60 = 4,10 m de profundidade.
U_MESA, U_URNA, U_ELEI, U_PASS = 1.70, sf.U_URNA, 0.90, 0.60
V_MESA = 0.80
LARG_MOD = 0.90
INFO_X, INFO_Y = sf.PONTO_INFO          # ponto de informacao (m), fonte unica em separadores_fila
N_MESARIOS = 4                # premissa: 109 nomeados / 28 MRVs = 3,9
ASSENTO = 0.75

TINTA, CINZA, LEVE = "#16202b", "#5b6470", "#8a94a6"
MADEIRA, MADEIRA_ESC = "#D2A86A", "#7a5527"
COR_PORTA = {"saida": "#3b4654", "preferencial": "#1e8449", "emergencia": sf.COR_EMERGENCIA,
             "fechada": "#b9bfc9", "livre": "#b9bfc9"}
ROTULO_PORTA = {"entrada": "entrada", "saida": "saída", "preferencial": "preferencial",
                "emergencia": "emergência", "fechada": "fechada no dia", "livre": "livre (desobstruída)"}


def virg(v, n=2):
    return f"{v:.{n}f}".replace(".", ",")


# --------------------------------------------------------------------------
# O modulo da MRV, em coordenadas locais: u = do encosto da parede para dentro,
# v = do eixo para o lado em que sentam os mesarios. Tudo em metros; a escala
# entra aqui, uma vez, para o mesmo codigo servir a planta e ao modulo ampliado.
# --------------------------------------------------------------------------
# Ordem do modulo, da parede para dentro (decisao de 30/09): mesa redonda da urna
# encostada na parede, vaga do eleitor, mesa-cavalete dos mesarios, passagem.
# O eleitor fica de costas para a parede e para a mesa redonda, de frente para os mesarios.
U_ELEI0 = U_URNA                  # a vaga do eleitor comeca depois da mesa redonda
U_TREST0 = U_URNA + U_ELEI        # a mesa-cavalete comeca depois da vaga
U_PASS0 = U_TREST0 + U_MESA       # e a passagem depois da mesa-cavalete


def modulo_svg(k, mostra_fundo=True):
    o = []
    add = o.append
    P = U_URNA + U_ELEI + U_MESA + U_PASS

    def R(u0, v0, u1, v1, **kw):
        a = " ".join(f'{n.replace("_", "-")}="{v}"' for n, v in kw.items())
        add(f'<rect x="{u0*k:.2f}" y="{v0*k:.2f}" width="{(u1-u0)*k:.2f}" '
            f'height="{(v1-v0)*k:.2f}" {a}/>')

    if mostra_fundo:
        R(0, -LARG_MOD / 2, P, LARG_MOD / 2, fill="#fff", fill_opacity=".55",
          stroke=LEVE, stroke_width=1, stroke_dasharray="5 4")
    # zona do assento dos mesarios (0,75 m)
    R(U_TREST0, V_MESA / 2, U_TREST0 + U_MESA, V_MESA / 2 + ASSENTO, fill="none", stroke=LEVE,
      stroke_width=1, stroke_dasharray="2 3")
    # passagem (hachurada)
    R(U_PASS0, -LARG_MOD / 2, P, LARG_MOD / 2, fill="url(#hach)", stroke="none")
    # vaga do eleitor
    R(U_ELEI0, -LARG_MOD / 2, U_ELEI0 + U_ELEI, LARG_MOD / 2, fill="#eef3f8", fill_opacity=".8",
      stroke="#9fb1c4", stroke_width=1, stroke_dasharray="3 3")

    # mesa-cavalete: tampo + dois cavaletes em A (as pernas saem do tampo)
    for uc in (U_TREST0 + 0.20, U_TREST0 + U_MESA - 0.20):
        R(uc - 0.035, -V_MESA / 2 - 0.07, uc + 0.035, V_MESA / 2 + 0.07,
          fill=MADEIRA_ESC, rx=1)
    R(U_TREST0, -V_MESA / 2, U_TREST0 + U_MESA, V_MESA / 2, fill=MADEIRA,
      stroke=MADEIRA_ESC, stroke_width=1.6, rx=2)
    for i in (1, 2, 3):                      # veio da madeira
        yv = -V_MESA / 2 + i * V_MESA / 4
        add(f'<line x1="{(U_TREST0+0.06)*k:.2f}" y1="{yv*k:.2f}" '
            f'x2="{(U_TREST0+U_MESA-0.06)*k:.2f}" y2="{yv*k:.2f}" stroke="{MADEIRA_ESC}" '
            f'stroke-opacity=".22" stroke-width="1"/>')

    # mesarios sentados, do lado v > 0
    passo = U_MESA / N_MESARIOS
    for i in range(N_MESARIOS):
        uc = U_TREST0 + passo * (i + .5)
        R(uc - 0.17, V_MESA / 2 + 0.07, uc + 0.17, V_MESA / 2 + 0.43,
          fill="#6d7a89", stroke=TINTA, stroke_width=1, rx=3)          # cadeira
        add(f'<circle cx="{uc*k:.2f}" cy="{(V_MESA/2+0.25)*k:.2f}" r="{0.145*k:.2f}" '
            f'fill="#2c3e50" stroke="#fff" stroke-width="1.2"/>')        # mesario

    # mesa redonda de 0,90 m, com a urna em cima, encostada na parede
    cu, r = U_URNA / 2, 0.45
    add(f'<circle cx="{cu*k:.2f}" cy="0" r="{r*k:.2f}" fill="#f4f1ea" stroke="{TINTA}" '
        f'stroke-width="2"/>')
    add(f'<circle cx="{cu*k:.2f}" cy="0" r="{(r-0.06)*k:.2f}" fill="none" stroke="{LEVE}" '
        f'stroke-width=".8"/>')
    R(cu - 0.17, -0.13, cu + 0.17, 0.13, fill="#1d2733", rx=2)           # urna
    R(cu - 0.04, -0.085, cu + 0.12, 0.085, fill="#8fd9bf", rx=1)          # visor, para o lado do eleitor
    R(cu - 0.13, -0.085, cu - 0.06, 0.085, fill="#3b4a5a", rx=1)          # teclado

    # eleitor em pe: de costas para a parede (e para a mesa redonda), de frente para
    # os mesarios (sentido +u)
    ue = U_ELEI0 + U_ELEI / 2
    add(f'<ellipse cx="{ue*k:.2f}" cy="0" rx="{0.12*k:.2f}" ry="{0.25*k:.2f}" '
        f'fill="#4a6fa5" stroke="#fff" stroke-width="1.2"/>')
    add(f'<circle cx="{(ue+0.04)*k:.2f}" cy="0" r="{0.105*k:.2f}" fill="#e9c9a5" '
        f'stroke="{TINTA}" stroke-width=".8"/>')
    return "\n".join(o)


def passo_m(i):
    return U_TREST0 + U_MESA / N_MESARIOS * (i + .5)


def grupo_modulo(x, y, ang, lado, k, corpo):
    """Coloca o modulo: (x, y) em px e o ponto de encosto; ang = sentido de u na tela."""
    return (f'<g transform="translate({x:.2f} {y:.2f}) rotate({ang:.3f}) '
            f'scale(1 {-lado})">{corpo}</g>')


# --------------------------------------------------------------------------
def carrega_tudo():
    planta, dec, cen = sf.carrega()
    mesas = sf.monta_mesas(planta, dec, cen)
    base = {m["n"]: dict(m) for m in planta["cenarios"][cen["base"]]["mrvs"]}
    for alt in cen["alteracoes"]:
        base[alt["n"]].update(alt)
    for m in mesas:
        m["lado"] = base[m["mrv"]]["lado"]
    with open(os.path.join(RAIZ, "data", "grupos_mesas.json"), encoding="utf-8") as f:
        grupos = json.load(f)["grupos"]
    itens = sf.catalogo(planta, dec, mesas)
    op = sf.opcoes(itens, mesas)[2]        # a Definitiva
    return planta, dec, mesas, grupos, itens, op


def posicao_banner(g):
    """Ponto do x-banner de um grupo (mesma regra de separadores_fila.svg_plano)."""
    eixo = sum(g["coord"]) / len(g["coord"])
    rec = 8.60 if g["classe"] == "alta" else 4.60
    if g["parede"] == "oeste":
        return rec, eixo
    if g["parede"] == "norte":
        return eixo, 44.4 - rec
    return 47.3 - rec, eixo


def postes_ao_longo(t):
    Lt = sf.comp(t)
    n = sf.postes(Lt)
    res = []
    for i in range(n):
        d = (0 if n == 1 else i / (n - 1)) * Lt
        rest = d
        for j in range(len(t) - 1):
            seg = math.dist(t[j], t[j + 1])
            if rest <= seg or j == len(t) - 2:
                u = 0 if seg == 0 else rest / seg
                res.append((t[j][0] + (t[j + 1][0] - t[j][0]) * u,
                            t[j][1] + (t[j + 1][1] - t[j][1]) * u))
                break
            rest -= seg
    return res


def eixo_avenida(aid):
    """Linha de centro de cada avenida, para as setas de sentido."""
    av = sf.AVENIDAS[aid]
    i, e = av["trilho_interno"], av["trilho_externo"]
    n = min(len(i), len(e))
    return [((i[j][0] + e[j][0]) / 2, (i[j][1] + e[j][1]) / 2) for j in range(n)] \
        if aid != "A" else [(23.43, 0.0), (23.43, 4.90), (12.50, 4.90), (12.50, 40.0)]


# --------------------------------------------------------------------------
def svg_planta(planta, dec, mesas, grupos, itens, op):
    LARG, ALT = planta["salao"]["largura"], planta["salao"]["altura"]
    W = ME + LARG * S + MD + GAP + PAINEL
    H = MT + ALT * S + MS
    px = lambda x, y: (ME + x * S, MT + (ALT - y) * S)
    pts = lambda seq: " ".join(f"{px(*p)[0]:.1f},{px(*p)[1]:.1f}" for p in seq)
    o = []
    add = o.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
        f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="{FONTE}">')
    add(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#fbfaf8"/>')
    add('<defs>'
        f'<pattern id="prot" width="9" height="9" patternTransform="rotate(45)" '
        f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="9" '
        f'stroke="{sf.COR_AVISO}" stroke-width="1.3" stroke-opacity=".26"/></pattern>'
        f'<pattern id="hach" width="7" height="7" patternTransform="rotate(45)" '
        f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" stroke="#8a94a6" '
        f'stroke-width="1.4" stroke-opacity=".55"/></pattern>'
        f'<pattern id="fech" width="8" height="8" patternTransform="rotate(-45)" '
        f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="8" stroke="#8a94a6" '
        f'stroke-width="3"/></pattern>'
        '<marker id="seta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" '
        'markerHeight="5.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>'
        '</marker></defs>')

    # ---- titulo ----
    add(f'<text x="{ME}" y="62" font-size="44" font-weight="800" fill="{TINTA}">'
        f'Hall 2 · planta de votação com as 28 MRVs</text>')
    add(f'<text x="{ME}" y="96" font-size="21" fill="{CINZA}">RDS Ballsbridge, Dublin · '
        f'1º turno, 04/10/2026 · cenário Paredes_ABC · arranjo e avenidas de 23/09 (v2) · módulo revisto em 30/09 · '
        f'escala 1 m = {S:.0f} px</text>')
    add(f'<text x="{ME}" y="124" font-size="21" fill="{CINZA}">Módulo da MRV, da parede para dentro: mesa redonda ⌀ 0,90 m com a urna · '
        f'vaga do eleitor 0,90 m, de costas para a parede · mesa-cavalete dos mesários 1,70 × 0,80 m · '
        f'passagem 0,60 m = 4,10 m</text>')

    # ---- piso e paredes ----
    cont = pts(planta["salao"]["contorno"])
    add(f'<polygon points="{cont}" fill="#ffffff"/>')

    # bandas de fila de cada parede
    for x1, y1, x2, y2 in ((0, 0, sf.BANDA_PAREDE["oeste"], ALT),
                           (0, ALT - sf.BANDA_PAREDE["norte"], LARG, ALT),
                           (47.3 - sf.BANDA_PAREDE["leste"], 0, 47.3, ALT)):
        a, b = px(x1, y2)
        add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(x2-x1)*S:.1f}" height="{(y2-y1)*S:.1f}" '
            f'fill="{TINTA}" fill-opacity=".03"/>')
    # o recorte sudoeste fica fora do piso
    rc = planta["salao"]["recorte"]
    a, b = px(rc[0], rc[3])
    add(f'<rect x="{a-2:.1f}" y="{b:.1f}" width="{(rc[2]-rc[0])*S+2:.1f}" '
        f'height="{(rc[3]-rc[1])*S+2:.1f}" fill="#fbfaf8"/>')

    # zonas protegidas
    rot_zona = {"faixa_emergencia": "faixa de emergência · 3 m livres",
                "recuo_porta": None}
    for z in dec["zonas_protegidas"]:
        x1, y1, x2, y2 = z["rect"]
        a, b = px(x1, y2)
        add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(x2-x1)*S:.1f}" height="{(y2-y1)*S:.1f}" '
            f'fill="url(#prot)" stroke="{sf.COR_AVISO}" stroke-opacity=".4" '
            f'stroke-dasharray="4 4"/>')

    # ---- avenidas: corredores tingidos, fita, setas ----
    for aid, av in sf.AVENIDAS.items():
        poly = list(av["trilho_interno"]) + list(reversed(av["trilho_externo"]))
        add(f'<polygon points="{pts(poly)}" fill="{av["hex"]}" fill-opacity=".17" stroke="none"/>')
    xa, xb = sf.X_AVENIDA_NORTE
    a, b = px(xa, sf.Y_BANDA_NORTE)
    add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(xb-xa)*S:.1f}" '
        f'height="{sf.AVENIDA_NORTE*S:.1f}" fill="{sf.CORES_ZONA["B"]}" fill-opacity=".30"/>')

    ativos = set(op["itens"])
    for aid, av in sf.AVENIDAS.items():
        for lado in ("interno", "externo"):
            if f"avenida_{aid}_{lado[:3]}" in ativos:
                continue
            add(f'<polyline points="{pts(av["trilho_"+lado])}" fill="none" stroke="{av["hex"]}" '
                f'stroke-width="3.4" stroke-dasharray="14 8" stroke-linejoin="round" '
                f'stroke-opacity=".9"/>')
    for ponto in (sf.DISTRIBUIDOR_NORTE, sf.AVENIDA_NORTE_SUL):
        add(f'<polyline points="{pts(ponto)}" fill="none" stroke="#d98600" stroke-width="3.4" '
            f'stroke-dasharray="14 8"/>')

    # pequena avenida: duas setas, cada uma para o seu lado
    ym = sf.Y_BANDA_NORTE - sf.AVENIDA_NORTE / 2
    for xd, xp in ((27.5, 13.0), (29.1, 35.6)):
        a, b = px(xd, ym)
        c, d = px(xp, ym)
        add(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="#d98600" '
            f'stroke-width="4" marker-end="url(#seta)"/>')

    # saida: campo livre, setas convergindo em S2 e S8
    for (x0, y0), (x1, y1) in (((6.0, 9.0), (13.85, 0.6)), ((20.0, 30.0), (13.85, 0.6)),
                               ((36.0, 30.0), (42.7, 0.6)), ((44.0, 9.0), (42.7, 0.6))):
        a, b = px(x0, y0)
        c, d = px(x1, y1)
        add(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="#8a94a6" '
            f'stroke-width="2.4" stroke-dasharray="3 8" marker-end="url(#seta)" opacity=".8"/>')

    # ---- ramais, marcas de 0,65 m e linha de espera ----
    serp = {s["mrv"] for s in dec["serpenteados"]}
    for m in mesas:
        dx, dy = m["dx"], m["dy"]
        perp = (-dy, dx)
        banda = sf.BANDA_PAREDE[m["parede"]]
        u_espera = 4.10 + sf.RECUO_MESA
        alta = m["mrv"] in serp
        if alta:
            continue          # o serpenteado ocupa o lugar do canal
        ponto = lambda u, v: (m["x"] + dx * u + perp[0] * v, m["y"] + dy * u + perp[1] * v)
        meia = sf.LARG_CANAL / 2
        for sg in (1, -1):
            add(f'<line x1="{px(*ponto(banda, sg*meia))[0]:.1f}" '
                f'y1="{px(*ponto(banda, sg*meia))[1]:.1f}" '
                f'x2="{px(*ponto(u_espera, sg*meia))[0]:.1f}" '
                f'y2="{px(*ponto(u_espera, sg*meia))[1]:.1f}" stroke="{m["hex_entrada"]}" '
                f'stroke-width="2.6" stroke-dasharray="9 6" stroke-opacity=".85"/>')
        n = int((banda - u_espera) / sf.PASSO_FILA)
        for i in range(1, n + 1):
            u = u_espera + i * sf.PASSO_FILA
            p1, p2 = ponto(u, -meia), ponto(u, -meia + .2)
            add(f'<line x1="{px(*p1)[0]:.1f}" y1="{px(*p1)[1]:.1f}" x2="{px(*p2)[0]:.1f}" '
                f'y2="{px(*p2)[1]:.1f}" stroke="{m["hex_entrada"]}" stroke-width="2" '
                f'stroke-opacity=".45"/>')
        e1, e2 = ponto(u_espera, -meia - .2), ponto(u_espera, meia + .2)
        add(f'<line x1="{px(*e1)[0]:.1f}" y1="{px(*e1)[1]:.1f}" x2="{px(*e2)[0]:.1f}" '
            f'y2="{px(*e2)[1]:.1f}" stroke="#fff" stroke-width="7"/>')
        add(f'<line x1="{px(*e1)[0]:.1f}" y1="{px(*e1)[1]:.1f}" x2="{px(*e2)[0]:.1f}" '
            f'y2="{px(*e2)[1]:.1f}" stroke="{TINTA}" stroke-width="7" stroke-dasharray="5 5"/>')

    # ---- barreira (Definitiva) ----
    for k in op["itens"]:
        it = itens[k]
        for t in it["trilhos"]:
            add(f'<polyline points="{pts(t)}" fill="none" stroke="{TINTA}" stroke-width="8" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
            add(f'<polyline points="{pts(t)}" fill="none" stroke="{it["hex"]}" stroke-width="4" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
            for p in postes_ao_longo(t):
                a, b = px(*p)
                add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4.6" fill="{TINTA}"/>'
                    f'<circle cx="{a:.1f}" cy="{b:.1f}" r="1.7" fill="#fff"/>')

    # ---- ponto de informacao: mesa-cavalete junto ao R1 ----
    # Fora do recuo de emergencia do R1 (x 7,80-10,80 m, y 0-7,00 m, sem mesa e sem fila)
    # e fora do vao da S1 (ate x = 11,45 m); termina na ombreira oeste da S2 (13,25 m).
    # Mesarios/atendentes do lado da parede, eleitor do lado do salao.
    ix0, ix1, iy0, iy1 = INFO_X[0], INFO_X[1], INFO_Y[0], INFO_Y[1]
    a, b = px(ix0, iy1)
    for xl in (ix0 + 0.20, ix1 - 0.20):
        c, d = px(xl, iy1 + 0.07)
        add(f'<rect x="{c-0.035*S:.1f}" y="{d:.1f}" width="{0.07*S:.1f}" '
            f'height="{(iy1-iy0+0.14)*S:.1f}" fill="{MADEIRA_ESC}" rx="1"/>')
    add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(ix1-ix0)*S:.1f}" height="{(iy1-iy0)*S:.1f}" '
        f'fill="{MADEIRA}" stroke="{MADEIRA_ESC}" stroke-width="1.6" rx="2"/>')
    for xc in (ix0 + 0.45, ix1 - 0.45):
        c, d = px(xc, iy0 - 0.25)
        add(f'<rect x="{c-0.17*S:.1f}" y="{d-0.18*S:.1f}" width="{0.34*S:.1f}" '
            f'height="{0.36*S:.1f}" rx="3" fill="#6d7a89" stroke="{TINTA}" stroke-width="1"/>'
            f'<circle cx="{c:.1f}" cy="{d:.1f}" r="{0.145*S:.1f}" fill="#2c3e50" '
            f'stroke="#fff" stroke-width="1.2"/>')
    c, d = px((ix0 + ix1) / 2, (iy0 + iy1) / 2)
    add(f'<circle cx="{c:.1f}" cy="{d:.1f}" r="15" fill="#0B5C8A" stroke="#fff" '
        f'stroke-width="2.4"/><text x="{c:.1f}" y="{d+6:.1f}" font-size="19" '
        f'font-weight="800" fill="#fff" text-anchor="middle" font-style="italic">i</text>')
    c, d = px(ix1 + 0.25, (iy0 + iy1) / 2)
    halo = 'stroke="#fff" stroke-width="5" paint-order="stroke" stroke-linejoin="round"'
    add(f'<text x="{c:.1f}" y="{d-2:.1f}" font-size="14" font-weight="800" fill="#0B5C8A" '
        f'{halo}>PONTO DE INFORMAÇÃO</text>'
        f'<text x="{c:.1f}" y="{d+13:.1f}" font-size="11" fill="{CINZA}" {halo}>mesa-cavalete '
        f'1,70 × 0,80 m · junto ao R1</text>')

    # ---- as 28 MRVs ----
    etiquetas = []
    for m in mesas:
        ang = math.degrees(math.atan2(-m["dy"], m["dx"]))
        x, y = px(m["x"], m["y"])
        add(grupo_modulo(x, y, ang, m["lado"], S, modulo_svg(S)))
        # selo da MRV sobre a mesa-cavalete, na cor da classe de comparecimento
        bx, by = px(m["x"] + m["dx"] * (U_TREST0 + U_MESA / 2), m["y"] + m["dy"] * (U_TREST0 + U_MESA / 2))
        claro = m["cor"] in ("#d4a017",)
        add(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="15" fill="{m["cor"]}" stroke="#fff" '
            f'stroke-width="2.4"/>'
            f'<text x="{bx:.1f}" y="{by+5.4:.1f}" font-size="15" font-weight="800" '
            f'fill="{TINTA if claro else "#fff"}" text-anchor="middle">{m["mrv"]}</text>')
        # rotulo de grupo e de secao numa linha so, do lado oposto ao dos mesarios:
        # e ali que a folga de 1,50 m entre unidades comporta o texto
        perp = (-m["dy"], m["dx"])
        ax_, ay_ = px(m["x"] + m["dx"] * 2.05, m["y"] + m["dy"] * 2.05)
        nvx, nvy = -m["lado"] * perp[0], m["lado"] * perp[1]    # lado oposto, na tela
        etiquetas.append((m, ax_, ay_, nvx, nvy))

    for m, ax_, ay_, nvx, nvy in etiquetas:
        sec = " · ".join(str(s) for s in m["secoes"])
        corpo = (f'<tspan font-size="14" font-weight="800" fill="{TINTA}">{m["grupo"]}</tspan>'
                 f'<tspan font-size="11" fill="{CINZA}" dx="6">{sec}</tspan>')
        meio = LARG_MOD / 2 * S
        if m["parede"] == "norte":
            xb = ax_ + (meio + 17 if nvx > 0 else -(meio + 6))
            add(f'<text x="{xb:.1f}" y="{ay_:.1f}" text-anchor="middle" '
                f'transform="rotate(-90 {xb:.1f} {ay_:.1f})">{corpo}</text>')
        else:
            yb = ay_ + (meio + 17 if nvy > 0 else -(meio + 6))
            add(f'<text x="{ax_:.1f}" y="{yb:.1f}" text-anchor="middle">{corpo}</text>')

    # ---- paredes por cima do piso ----
    add(f'<polygon points="{cont}" fill="none" stroke="{TINTA}" stroke-width="9" '
        f'stroke-linejoin="miter"/>')

    # ---- portas ----
    for p in planta["portas"]:
        sin = dec["sinalizacao_portas"].get(p["id"], {})
        papel = sin.get("papel", "livre")
        cor = sf.CORES_ZONA.get(sin.get("entrada"), "#8a94a6") if papel == "entrada" \
            else COR_PORTA[papel]
        a1, b1 = px(p["x1"], p["y1"])
        a2, b2 = px(p["x2"], p["y2"])
        add(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#fbfaf8" '
            f'stroke-width="13"/>')
        if papel == "fechada":
            add(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" '
                f'stroke="url(#fech)" stroke-width="10"/>')
        else:
            add(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="{cor}" '
                f'stroke-width="10"/>')
        mx, my = (a1 + a2) / 2, (b1 + b2) / 2
        fc = p["face"]
        ox_, oy_ = {"sul": (0, 1), "norte": (0, -1), "leste": (1, 0), "oeste": (-1, 0),
                    "recorte_v": (-1, 0)}[fc]
        nome = p["id"]
        if papel == "entrada":
            seg = f'entrada {sin["entrada"]}'
        else:
            seg = ROTULO_PORTA[papel]
        det = f'{virg(p["larg"])} m'
        # seta de sentido (so onde ha fluxo de eleitor)
        if papel in ("entrada", "saida", "preferencial"):
            de, para = (1.9, 0.25) if papel != "saida" else (0.25, 1.9)
            # 1,9 m do lado de fora: seta de fora para dentro (entrada) ou o contrario
            a = (mx + ox_ * de * S, my + oy_ * de * S)
            c = (mx + ox_ * para * S, my + oy_ * para * S)
            add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{c[0]:.1f}" y2="{c[1]:.1f}" '
                f'stroke="{cor}" stroke-width="6" marker-end="url(#seta)"/>')
        gap_txt = (2.35 if ox_ == 0 and oy_ > 0 else 0.95) * S
        tx_, ty_ = mx + ox_ * gap_txt, my + oy_ * gap_txt
        anc = "middle" if ox_ == 0 else ("start" if ox_ > 0 else "end")
        if ox_ == 0:
            yb = ty_ + (13 if oy_ > 0 else -50)
            add(f'<text x="{tx_:.1f}" y="{yb+10:.1f}" font-size="22" font-weight="800" '
                f'fill="{cor if papel in ("entrada", "saida", "preferencial", "emergencia") else CINZA}" text-anchor="{anc}">{nome}</text>'
                f'<text x="{tx_:.1f}" y="{yb+25:.1f}" font-size="11.5" fill="{CINZA}" '
                f'text-anchor="{anc}">{seg} · {det}</text>')
        else:
            add(f'<text x="{tx_:.1f}" y="{ty_-2:.1f}" font-size="20" font-weight="800" '
                f'fill="{cor if papel in ("entrada", "saida", "preferencial", "emergencia") else CINZA}" text-anchor="{anc}">{nome}</text>'
                f'<text x="{tx_:.1f}" y="{ty_+13:.1f}" font-size="11.5" fill="{CINZA}" '
                f'text-anchor="{anc}">{seg} · {det}</text>')

    # ---- BANNERS: pontos ----
    def ponto_banner(x, y, rot, cor, txtcor, r=15):
        a, b = px(x, y)
        add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r+6}" fill="#fff" fill-opacity=".9" '
            f'stroke="{TINTA}" stroke-width="1.6"/>'
            f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r}" fill="{cor}"/>'
            f'<text x="{a:.1f}" y="{b+4.6:.1f}" font-size="13.5" font-weight="800" '
            f'fill="{txtcor}" text-anchor="middle">{rot}</text>')

    for g in grupos:
        bx, by = posicao_banner(g)
        cor = sf.CORES_ZONA[g["entrada"]]
        ponto_banner(bx, by, g["id"], cor, TINTA if g["entrada"] == "B" else "#fff")

    # painel de porta P6 (pull-up), no eixo da avenida, logo depois da porta
    for aid, av in sf.AVENIDAS.items():
        e = eixo_avenida(aid)
        a, b = px(e[0][0], 2.7)
        add(f'<rect x="{a-19:.1f}" y="{b-19:.1f}" width="38" height="38" fill="{av["hex"]}" '
            f'stroke="#fff" stroke-width="3"/><rect x="{a-19:.1f}" y="{b-19:.1f}" width="38" '
            f'height="38" fill="none" stroke="{TINTA}" stroke-width="1.4"/>'
            f'<text x="{a:.1f}" y="{b+5:.1f}" font-size="14" font-weight="800" '
            f'fill="{TINTA if aid=="B" else "#fff"}" text-anchor="middle">P6</text>')

    # fence banner da boca da pequena avenida
    a, b = px(28.3, ym)
    add(f'<polygon points="{a:.1f},{b-24:.1f} {a+24:.1f},{b:.1f} {a:.1f},{b+24:.1f} '
        f'{a-24:.1f},{b:.1f}" fill="{sf.CORES_ZONA["B"]}" stroke="#fff" stroke-width="3"/>'
        f'<polygon points="{a:.1f},{b-24:.1f} {a+24:.1f},{b:.1f} {a:.1f},{b+24:.1f} '
        f'{a-24:.1f},{b:.1f}" fill="none" stroke="{TINTA}" stroke-width="1.4"/>'
        f'<text x="{a:.1f}" y="{b+5:.1f}" font-size="13" font-weight="800" fill="{TINTA}" '
        f'text-anchor="middle">P4</text>')

    # ---- rotulos das avenidas ----
    def rotulo_ave(x, y, txt, cor, sub):
        a, b = px(x, y)
        add(f'<g transform="rotate(-90 {a:.1f} {b:.1f})">'
            f'<rect x="{a-110:.1f}" y="{b-19:.1f}" width="220" height="38" rx="6" fill="#fff" '
            f'fill-opacity=".92" stroke="{cor}" stroke-width="2"/>'
            f'<text x="{a:.1f}" y="{b-2:.1f}" font-size="15" font-weight="800" fill="{TINTA}" '
            f'text-anchor="middle">{txt}</text>'
            f'<text x="{a:.1f}" y="{b+12:.1f}" font-size="10.5" fill="{CINZA}" '
            f'text-anchor="middle">{sub}</text></g>')
    rotulo_ave(12.5, 22.0, "AVENIDA A · AZUL", sf.CORES_ZONA["A"], "S4 → parede oeste · 3,00 m")
    rotulo_ave(28.3, 17.0, "AVENIDA B · AMARELA", "#b48f00", "S5 → parede norte · 3,00 m")
    rotulo_ave(35.0, 22.0, "AVENIDA C · VERMELHA", sf.CORES_ZONA["C"], "S6 → parede leste · 3,00 m")
    a, b = px(20.0, ym)
    add(f'<text x="{a:.1f}" y="{b+5:.1f}" font-size="14" font-weight="800" fill="#8a6a00" '
        f'text-anchor="middle">pequena avenida · 1,80 m</text>')
    a, b = px(37.5, ym)
    add(f'<text x="{a:.1f}" y="{b+5:.1f}" font-size="14" font-weight="800" fill="#8a6a00" '
        f'text-anchor="middle">pequena avenida</text>')

    # ---- apron ----
    a, b = px(24.0, 0)
    add(f'<text x="{a:.1f}" y="{b+MS-34:.1f}" font-size="15" font-weight="700" fill="{CINZA}" '
        f'letter-spacing="2" text-anchor="middle">FACHADA SUL ↓ APRON (14 m) E RING 3</text>')

    # ---- norte, escala ----
    nx, ny = ME + LARG * S + 95, MT + 10
    add(f'<polygon points="{nx},{ny} {nx+13},{ny+46} {nx},{ny+36} {nx-13},{ny+46}" fill="{TINTA}"/>'
        f'<text x="{nx}" y="{ny-8}" font-size="18" font-weight="800" fill="{TINTA}" '
        f'text-anchor="middle">N</text>')
    sx, sy = ME, MT + ALT * S + MS - 12
    add(f'<line x1="{sx}" y1="{sy}" x2="{sx+10*S:.0f}" y2="{sy}" stroke="{TINTA}" '
        f'stroke-width="4"/>')
    for i in range(11):
        add(f'<line x1="{sx+i*S:.0f}" y1="{sy-6}" x2="{sx+i*S:.0f}" y2="{sy+6}" stroke="{TINTA}" '
            f'stroke-width="2"/>')
    add(f'<text x="{sx+10*S+14:.0f}" y="{sy+5}" font-size="14" fill="{CINZA}">10 m</text>')
    add(f'<text x="{sx}" y="{sy-14}" font-size="12" fill="{LEVE}">Hall 2 · {virg(LARG,1)} × '
        f'{virg(ALT,1)} m</text>')

    # ---- painel direito ----
    px0 = ME + LARG * S + MD + GAP
    painel(add, px0, MT, mesas, grupos)
    add('</svg>')
    return "\n".join(o)


# --------------------------------------------------------------------------
def painel(add, x0, y0, mesas, grupos):
    y = y0
    add(f'<text x="{x0}" y="{y+4}" font-size="15" font-weight="800" fill="{TINTA}" '
        f'letter-spacing="2.2">O MÓDULO DA MRV · 4,10 × 0,90 m</text>')
    # modulo ampliado, horizontal: parede a esquerda, mesarios para cima
    K = 150.0
    ox, oy = x0 + 40, y + 330
    add(f'<rect x="{ox-22}" y="{oy-140}" width="22" height="280" fill="{TINTA}"/>')
    add(f'<text x="{ox-33}" y="{oy}" font-size="11" fill="{TINTA}" font-weight="700" '
        f'letter-spacing="2" text-anchor="middle" transform="rotate(-90 {ox-33} {oy})">PAREDE</text>')
    add(f'<g transform="translate({ox} {oy}) scale(1 -1)">{modulo_svg(K)}</g>')

    def cota_u(u0, u1, yy, txt):
        a, b = ox + u0 * K, ox + u1 * K
        add(f'<line x1="{a:.0f}" y1="{yy}" x2="{b:.0f}" y2="{yy}" stroke="{LEVE}" stroke-width="1.4"/>'
            f'<line x1="{a:.0f}" y1="{yy-6}" x2="{a:.0f}" y2="{yy+6}" stroke="{LEVE}" stroke-width="1.4"/>'
            f'<line x1="{b:.0f}" y1="{yy-6}" x2="{b:.0f}" y2="{yy+6}" stroke="{LEVE}" stroke-width="1.4"/>'
            f'<text x="{(a+b)/2:.0f}" y="{yy+20}" font-size="13" fill="{CINZA}" '
            f'text-anchor="middle">{txt}</text>')
    yc = oy + 0.45 * K + 30
    cota_u(0, U_URNA, yc, "0,90")
    cota_u(U_ELEI0, U_TREST0, yc, "0,90")
    cota_u(U_TREST0, U_PASS0, yc, "1,70")
    cota_u(U_PASS0, 4.10, yc, "0,60")
    cota_u(0, 4.10, yc + 36, "4,10 m de profundidade")
    xv = ox + 4.10 * K + 30
    add(f'<line x1="{xv:.0f}" y1="{oy-0.45*K:.0f}" x2="{xv:.0f}" y2="{oy+0.45*K:.0f}" '
        f'stroke="{LEVE}" stroke-width="1.4"/>'
        f'<line x1="{xv-6:.0f}" y1="{oy-0.45*K:.0f}" x2="{xv+6:.0f}" y2="{oy-0.45*K:.0f}" stroke="{LEVE}" stroke-width="1.4"/>'
        f'<line x1="{xv-6:.0f}" y1="{oy+0.45*K:.0f}" x2="{xv+6:.0f}" y2="{oy+0.45*K:.0f}" stroke="{LEVE}" stroke-width="1.4"/>'
        f'<text x="{xv+10:.0f}" y="{oy+5:.0f}" font-size="13" fill="{CINZA}">0,90</text>')

    def chama(u, v, yt, t1, t2, dx_txt=8):
        ax, ay = ox + u * K, oy - v * K
        add(f'<line x1="{ax:.0f}" y1="{yt+14:.0f}" x2="{ax:.0f}" y2="{ay:.0f}" stroke="{TINTA}" '
            f'stroke-width="1.2"/><circle cx="{ax:.0f}" cy="{ay:.0f}" r="3.6" fill="{TINTA}"/>'
            f'<text x="{ax+dx_txt:.0f}" y="{yt:.0f}" font-size="14" font-weight="800" '
            f'fill="{TINTA}">{t1}</text>'
            f'<text x="{ax+dx_txt:.0f}" y="{yt+16:.0f}" font-size="12" fill="{CINZA}">{t2}</text>')
    r1, r2 = y + 58, y + 118
    chama(U_URNA / 2, 0.45, r1, "mesa redonda ⌀ 0,90 m", "da urna · encostada na parede")
    chama(passo_m(0), 0.68, r1, f"{N_MESARIOS} mesários sentados",
          "assento 0,75 m · premissa: 109 ÷ 28 ≈ 3,9")
    chama(U_ELEI0 + U_ELEI / 2, 0.40, r2, "vaga do eleitor", "0,90 m · de costas para a parede")
    chama(U_TREST0 + 1.27, 0.40, r2, "mesa-cavalete (trestle)", "1,70 × 0,80 m · dos mesários")
    add(f'<text x="{ox+4.10*K:.0f}" y="{yc+96:.0f}" font-size="12.5" fill="{CINZA}" '
        f'text-anchor="end">hachurado: passagem de 0,60 m, por onde o eleitor entra no módulo</text>')
    y = yc + 140

    # ---- legenda ----
    def titulo(t):
        nonlocal y
        add(f'<line x1="{x0}" y1="{y-16}" x2="{x0+PAINEL-20}" y2="{y-16}" stroke="#dcdde1"/>')
        add(f'<text x="{x0}" y="{y+8}" font-size="15" font-weight="800" fill="{TINTA}" '
            f'letter-spacing="2.2">{t}</text>')
        y += 38

    def linha(simbolo, txt, sub=None, h=30):
        nonlocal y
        add(simbolo.replace("@Y", f"{y-7:.0f}"))
        add(f'<text x="{x0+62}" y="{y}" font-size="14.5" fill="#31404f">{txt}</text>')
        if sub:
            add(f'<text x="{x0+62}" y="{y+16}" font-size="11.5" fill="{LEVE}">{sub}</text>')
            y += 16
        y += h

    def faixa(cor, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="{cor}" '
                f'stroke-width="5"{d}/>')

    titulo("PORTAS")
    linha(f'<line x1="{x0}" y1="@Y" x2="{x0+14}" y2="@Y" stroke="{sf.CORES_ZONA["A"]}" stroke-width="9"/>'
          f'<line x1="{x0+17}" y1="@Y" x2="{x0+31}" y2="@Y" stroke="{sf.CORES_ZONA["B"]}" stroke-width="9"/>'
          f'<line x1="{x0+34}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="{sf.CORES_ZONA["C"]}" stroke-width="9"/>',
          "entradas S4 (A), S5 (B), S6 (C)", "as três contíguas, 0,29 m de alvenaria entre elas · 5,93 m cada")
    linha(faixa(COR_PORTA["saida"]), "saídas S2 e S8", "1,20 m · quem vota sai pela banda da sua parede")
    linha(faixa(COR_PORTA["preferencial"]), "S7 · entrada preferencial", "1,27 m · sem fila")
    linha(faixa(COR_PORTA["emergencia"]), "L1–L4 · saídas de emergência", "leste, faixa protegida de 3 m")
    linha(f'<line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="url(#fech)" stroke-width="9"/>',
          "fechadas no dia (N1, O1) · livres (N2, O2, R1, S1, S3, S9)",
          "as livres ficam desobstruídas, sem mesa e sem fila")

    titulo("AVENIDAS E FITA")
    for aid, nome in (("A", "azul · S4 → parede oeste"), ("B", "amarela · S5 → parede norte"),
                      ("C", "vermelha · S6 → parede leste")):
        hx = sf.AVENIDAS[aid]["hex"]
        linha(f'<rect x="{x0}" y="@Y" width="48" height="16" fill="{hx}" fill-opacity=".30" '
              f'stroke="{hx}" stroke-width="1.6" transform="translate(0 -8)"/>',
              f"avenida {aid} — {nome}", "corredor de 3,00 m, sentido único: da porta à parede", h=26)
    linha(f'<rect x="{x0}" y="@Y" width="48" height="10" fill="{sf.CORES_ZONA["B"]}" '
          f'fill-opacity=".45" transform="translate(0 -5)"/>'
          f'<line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="#d98600" stroke-width="3" '
          f'stroke-dasharray="8 5"/>',
          "pequena avenida da parede norte", "1,80 m, duas bordas de fita: a escolha de lado é andando")
    linha(f'<line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="{TINTA}" stroke-width="8" '
          f'stroke-linecap="round"/><line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" '
          f'stroke="{sf.CORES_ZONA["A"]}" stroke-width="4" stroke-linecap="round"/>'
          f'<circle cx="{x0+2}" cy="@Y" r="4.6" fill="{TINTA}"/><circle cx="{x0+46}" cy="@Y" r="4.6" fill="{TINTA}"/>',
          "unifilas (barreira) · 96 de 100", "bocas de A e C, avenida B e os 3 serpenteados")
    linha(faixa(sf.CORES_ZONA["C"], "9 6"), "fita no chão", "resto das avenidas e 28 ramais de 1,10 m, na cor da entrada")
    linha(f'<line x1="{x0}" y1="@Y" x2="{x0+48}" y2="@Y" stroke="{TINTA}" stroke-width="6" '
          f'stroke-dasharray="5 5"/>', "linha de espera · zebrado",
          "1,50 m à frente do módulo: só passa quem o mesário chamar")

    titulo("BANNERS, PEÇAS E PONTOS")
    linha(f'<circle cx="{x0+22}" cy="@Y" r="16" fill="#fff" stroke="{TINTA}" stroke-width="1.6"/>'
          f'<circle cx="{x0+22}" cy="@Y" r="11" fill="{sf.CORES_ZONA["C"]}"/>',
          "x-banner do grupo de mesas (16: 5 oeste, 5 norte, 6 leste)",
          "a 4,60 m da parede, na boca do corredor do grupo · 8,60 m nos 3 de alta carga")
    linha(f'<rect x="{x0+8}" y="@Y" width="28" height="28" fill="{sf.CORES_ZONA["A"]}" '
          f'transform="translate(0 -14)"/>',
          "P6 · painel de porta (pull-up 1000 × 2000 mm)", "no eixo da avenida, logo depois da porta", h=28)
    linha(f'<polygon points="{x0+22},{y-24} {x0+40},{y-8} {x0+22},{y+8} {x0+4},{y-8}" '
          f'fill="{sf.CORES_ZONA["B"]}" stroke="{TINTA}" stroke-width="1.4"/>',
          "P4-FimAvenidaB · fence banner 2080 × 820 mm",
          "na boca da pequena avenida: B1–B3 à esquerda, B4–B5 à direita")

    linha(f'<rect x="{x0+4}" y="@Y" width="40" height="16" fill="{MADEIRA}" stroke="{MADEIRA_ESC}" '
          f'stroke-width="1.4" rx="2" transform="translate(0 -8)"/>'
          f'<circle cx="{x0+24}" cy="@Y" r="10" fill="#0B5C8A" stroke="#fff" stroke-width="2"/>'
          f'<text x="{x0+24}" y="@Y" dy="4.5" font-size="13" font-weight="800" fill="#fff" '
          f'text-anchor="middle" font-style="italic">i</text>',
          "ponto de informação · mesa-cavalete 1,70 × 0,80 m",
          "junto ao R1, fora do recuo de emergência (7,8–10,8 m) e do vão da S1")

    titulo("MESAS, POR CLASSE DE COMPARECIMENTO")
    for cl, rot, n in (("alta", "alto comparecimento", 3), ("media", "médio", 8),
                       ("baixa", "baixo", 17)):
        c = next(m for m in mesas if m["classe"] == cl)["cor"]
        linha(f'<circle cx="{x0+22}" cy="@Y" r="12" fill="{c}"/>', f"{rot} ({n} MRVs)",
              None, h=26)
    add(f'<text x="{x0}" y="{y+6}" font-size="12.5" fill="{CINZA}">O número no selo é a MRV '
        f'(numeração oficial, uso interno); ao lado, o grupo e as seções.</text>')
    y += 22
    add(f'<text x="{x0}" y="{y+6}" font-size="12.5" fill="{CINZA}">A sinalização para o '
        f'eleitor usa só grupo e seção — nunca o número da mesa.</text>')
    return y


# --------------------------------------------------------------------------
# Versao em ingles: o desenho e um so; o texto e traduzido na saida. Toda
# mensagem da planta precisa estar aqui -- localiza() para com erro se sobrar
# texto em portugues sem traducao, em vez de entregar uma planta meio traduzida.
# --------------------------------------------------------------------------
EN = {
    "0,90 m · de costas para a parede": "0.90 m · back to the wall",
    "1,20 m · quem vota sai pela banda da sua parede": "1.20 m · voters leave along the band of their own wall",
    "1,27 m · sem fila": "1.27 m · no queue",
    "1,50 m à frente do módulo: só passa quem o mesário chamar": "1.50 m in front of the module: only those called by the poll worker cross",
    "1,70 × 0,80 m · dos mesários": "1.70 × 0.80 m · poll workers'",
    "1,80 m, duas bordas de fita: a escolha de lado é andando": "1.80 m, two tape edges: voters pick a side while walking",
    "4 mesários sentados": "4 poll workers seated",
    "4,10 m de profundidade": "4.10 m deep",
    "A sinalização para o eleitor usa só grupo e seção — nunca o número da mesa.": "Voter signage uses only group and section — never the table number.",
    "AVENIDA A · AZUL": "AVENUE A · BLUE",
    "AVENIDA B · AMARELA": "AVENUE B · YELLOW",
    "AVENIDA C · VERMELHA": "AVENUE C · RED",
    "AVENIDAS E FITA": "AVENUES AND TAPE",
    "BANNERS, PEÇAS E PONTOS": "BANNERS, SIGNS AND POINTS",
    "FACHADA SUL ↓ APRON (14 m) E RING 3": "SOUTH FAÇADE ↓ APRON (14 m) AND RING 3",
    "Hall 2 · planta de votação com as 28 MRVs": "Hall 2 · voting floor plan with the 28 MRVs (polling tables)",
    "L1–L4 · saídas de emergência": "L1–L4 · emergency exits",
    "MESAS, POR CLASSE DE COMPARECIMENTO": "TABLES, BY EXPECTED-TURNOUT CLASS",
    "Módulo da MRV, da parede para dentro: mesa redonda ⌀ 0,90 m com a urna · vaga do eleitor 0,90 m, de costas para a parede · mesa-cavalete dos mesários 1,70 × 0,80 m · passagem 0,60 m = 4,10 m":
        "MRV module, from the wall inwards: round table ⌀ 0.90 m with the voting machine · voter spot 0.90 m, back to the wall · poll workers' trestle table 1.70 × 0.80 m · passage 0.60 m = 4.10 m",
    "O MÓDULO DA MRV · 4,10 × 0,90 m": "THE MRV MODULE · 4.10 × 0.90 m",
    "O número no selo é a MRV (numeração oficial, uso interno); ao lado, o grupo e as seções.":
        "The number in the badge is the MRV (official numbering, internal use); beside it, the group and the sections.",
    "P6 · painel de porta (pull-up 1000 × 2000 mm)": "P6 · door panel (pull-up 1000 × 2000 mm)",
    "P4-FimAvenidaB · fence banner 2080 × 820 mm": "P4-FimAvenidaB · fence banner 2080 × 820 mm",
    "PAREDE": "WALL",
    "PONTO DE INFORMAÇÃO": "INFORMATION POINT",
    "PORTAS": "DOORS",
    "S4 → parede oeste · 3,00 m": "S4 → west wall · 3,00 m",
    "S5 → parede norte · 3,00 m": "S5 → north wall · 3,00 m",
    "S6 → parede leste · 3,00 m": "S6 → east wall · 3,00 m",
    "S7 · entrada preferencial": "S7 · priority entrance",
    "a 4,60 m da parede, na boca do corredor do grupo · 8,60 m nos 3 de alta carga":
        "at 4,60 m from the wall, at the mouth of the group's corridor · 8,60 m for the 3 high-turnout groups",
    "alto comparecimento (3 MRVs)": "high turnout (3 MRVs)",
    "médio (8 MRVs)": "medium (8 MRVs)",
    "baixo (17 MRVs)": "low (17 MRVs)",
    "as livres ficam desobstruídas, sem mesa e sem fila": "the clear ones stay unobstructed: no tables, no queues",
    "as três contíguas, 0,29 m de alvenaria entre elas · 5,93 m cada": "the three are contiguous, 0,29 m of masonry between them · 5,93 m each",
    "assento 0,75 m · premissa: 109 ÷ 28 ≈ 3,9": "seat 0,75 m · assumption: 109 ÷ 28 ≈ 3,9",
    "avenida A — azul · S4 → parede oeste": "avenue A — blue · S4 → west wall",
    "avenida B — amarela · S5 → parede norte": "avenue B — yellow · S5 → north wall",
    "avenida C — vermelha · S6 → parede leste": "avenue C — red · S6 → east wall",
    "bocas de A e C, avenida B e os 3 serpenteados": "mouths of A and C, avenue B and the 3 serpentine queues",
    "corredor de 3,00 m, sentido único: da porta à parede": "3,00 m corridor, one-way: from the door to the wall",
    "da urna · encostada na parede": "voting machine · against the wall",
    "entradas S4 (A), S5 (B), S6 (C)": "entrances S4 (A), S5 (B), S6 (C)",
    "fechadas no dia (N1, O1) · livres (N2, O2, R1, S1, S3, S9)": "closed on the day (N1, O1) · kept clear (N2, O2, R1, S1, S3, S9)",
    "fita no chão": "floor tape",
    "hachurado: passagem de 0,60 m, por onde o eleitor entra no módulo": "hatched: 0,60 m passage, where the voter enters the module",
    "junto ao R1, fora do recuo de emergência (7,8–10,8 m) e do vão da S1": "next to R1, outside the emergency setback (7,8–10,8 m) and the S1 opening",
    "leste, faixa protegida de 3 m": "east side, 3 m protected strip",
    "linha de espera · zebrado": "waiting line · zebra stripes",
    "mesa redonda ⌀ 0,90 m": "round table ⌀ 0,90 m",
    "mesa-cavalete (trestle)": "trestle table",
    "mesa-cavalete 1,70 × 0,80 m · junto ao R1": "trestle table 1,70 × 0,80 m · next to R1",
    "na boca da pequena avenida: B1–B3 à esquerda, B4–B5 à direita": "at the mouth of the small avenue: B1–B3 to the left, B4–B5 to the right",
    "no eixo da avenida, logo depois da porta": "on the avenue axis, right after the door",
    "pequena avenida": "small avenue",
    "pequena avenida da parede norte": "small avenue of the north wall",
    "pequena avenida · 1,80 m": "small avenue · 1,80 m",
    "ponto de informação · mesa-cavalete 1,70 × 0,80 m": "information point · trestle table 1,70 × 0,80 m",
    "resto das avenidas e 28 ramais de 1,10 m, na cor da entrada": "rest of the avenues and the 28 table lanes of 1,10 m, in the entrance colour",
    "saídas S2 e S8": "exits S2 and S8",
    "unifilas (barreira) · 96 de 100": "queue barriers (stanchions) · 96 of 100",
    "vaga do eleitor": "voter spot",
    "x-banner do grupo de mesas (16: 5 oeste, 5 norte, 6 leste)": "x-banner of each table group (16: 5 west, 5 north, 6 east)",
    "RDS Ballsbridge, Dublin · 1º turno, 04/10/2026 · cenário Paredes_ABC · arranjo e avenidas de 23/09 (v2) · módulo revisto em 30/09 · escala 1 m = 52 px":
        "RDS Ballsbridge, Dublin · 1st round, 4 Oct 2026 · Paredes_ABC scenario · layout and avenues of 23 Sep (v2) · module revised 30 Sep · scale 1 m = 52 px",
    "Hall 2 · 50,3 × 44,4 m": "Hall 2 · 50,3 × 44,4 m",
}
EN_PADROES = [
    (r"^entrada ([ABC]) · (.+)$", r"entrance \1 · \2"),
    (r"^saída · (.+)$", r"exit · \1"),
    (r"^preferencial · (.+)$", r"priority · \1"),
    (r"^emergência · (.+)$", r"emergency · \1"),
    (r"^fechada no dia · (.+)$", r"closed on the day · \1"),
    (r"^livre \(desobstruída\) · (.+)$", r"kept clear · \1"),
]
# texto que nao se traduz: codigos de porta, de grupo, de peca, unidades, letras soltas
SEM_TRADUCAO = re.compile(r"^([A-Z]\d|[A-Z]|P\d|i|\d+ m|L1|N[12]|O[12]|S\d|R1)$")


def localiza(svg, lang):
    """Traduz os nos de texto do SVG e acerta a virgula decimal; 'pt' devolve o SVG como esta."""
    if lang == "pt":
        return svg.replace("<svg xmlns=", '<svg lang="pt-BR" xmlns=', 1)
    sobra = set()

    def no(m):
        txt = m.group(1)
        if not re.search(r"[A-Za-zÀ-ú]", txt):
            return f">{txt}<"
        novo = EN.get(txt)
        if novo is None:
            for pad, sub in EN_PADROES:
                if re.match(pad, txt):
                    novo = re.sub(pad, sub, txt)
                    break
        if novo is None:
            if not SEM_TRADUCAO.match(txt) and not re.fullmatch(r"[\d\s·–\-.,A-Za-z⌀×≈÷→]*", txt):
                sobra.add(txt)
            novo = txt
        novo = re.sub(r"(\d),(\d)", r"\1.\2", novo)
        return f">{novo}<"

    saida = re.sub(r">([^<>]+)<", no, svg)
    if sobra:
        raise SystemExit("texto sem tradução:\n  " + "\n  ".join(sorted(sobra)))
    return saida.replace("<svg xmlns=", '<svg lang="en" xmlns=', 1)


# --------------------------------------------------------------------------
def confere(mesas, grupos, planta):
    falhas = []
    if len(mesas) != 28:
        falhas.append(f"esperava 28 MRVs, vieram {len(mesas)}")
    if len(grupos) != 16:
        falhas.append(f"esperava 16 grupos, vieram {len(grupos)}")
    mod = planta["modulo"]
    soma = round(mod["mesa"][0] + mod["urna"] + mod["eleitor"] + mod["passagem"], 2)
    if soma != mod["prof"]:
        falhas.append(f"módulo não fecha: {soma} ≠ {mod['prof']}")
    for g in grupos:
        bx, by = posicao_banner(g)
        if not (0 < bx < 47.3 and 0 < by < 44.4):
            falhas.append(f"banner {g['id']} fora do salão: {bx:.2f}, {by:.2f}")
    for m in mesas:
        if m["lado"] not in (1, -1):
            falhas.append(f"MRV {m['mrv']} sem lado")
    return falhas


def main():
    grava = "--grava" in sys.argv
    planta, dec, mesas, grupos, itens, op = carrega_tudo()
    falhas = confere(mesas, grupos, planta)
    if falhas:
        print("FALHAS:")
        for f in falhas:
            print("  ", f)
        sys.exit(1)
    print(f"{len(mesas)} MRVs · {len(grupos)} banners de grupo · 3 painéis P6 · 1 fence banner P4")
    if not grava:
        print("(sem --grava: nada foi escrito)")
        return
    os.makedirs(SAIDAS, exist_ok=True)
    base = svg_planta(planta, dec, mesas, grupos, itens, op)
    for lang in ("pt", "en"):
        caminho = os.path.join(SAIDAS, f"planta_hall2_detalhada_{lang}.svg")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(localiza(base, lang))
        print("escrito", os.path.relpath(caminho, RAIZ))
        if "--png" in sys.argv:
            png = caminho[:-4] + ".png"
            r = subprocess.run(["node", os.path.join(RAIZ, "scripts", "svg_para_png.js"),
                                caminho, png, "2"])
            print("escrito", os.path.relpath(png, RAIZ) if r.returncode == 0
                  else "PNG não gerado (precisa de node + playwright + Chromium)")

if __name__ == "__main__":
    main()
