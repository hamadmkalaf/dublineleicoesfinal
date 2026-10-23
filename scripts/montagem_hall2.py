"""Instrucoes de montagem do Hall 2, etapa por etapa, com uma planta por etapa.

Gera ``mapa/montagem_hall2.html``: o roteiro da vespera (24/10/2026, para o
2o turno de 25/10) em oito etapas, cada uma com a planta do salao em escala.
Em cada planta o trabalho das etapas anteriores aparece esmaecido e o da etapa
corrente em cor -- quem monta ve o que ja deveria estar no chao e o que entra
agora.

A geometria e a do desenho definitivo de 17/09 (``separadores_fila.py``), lida
do mesmo lugar: ``data/prancheta_hall2.json``, ``data/decisoes.json``,
``data/grupos_mesas.json`` e ``cenarios/paredes-abc-20260915.json``. Nenhum
deles e escrito. ``AVENIDAS`` e ``BANDA_PAREDE`` sao importados, nao copiados.

Ajustes de campo (D1-D4)
------------------------
Desenhar o chao trecho a trecho mostrou quatro pontos em que o desenho de 17/09
pede duas fitas no mesmo lugar. A conferencia de ``separadores_fila.py`` so
prova que as tres avenidas nao se cruzam entre si; estes cruzamentos sao de
outros elementos com as avenidas e com os ramais, e ela nao os ve. Os ajustes
abaixo estao em ``AJUSTES`` e foram aprovados pelo Posto em 23/10/2026 para a
montagem do 2o turno; o desenho definitivo de 17/09 nao foi alterado.

D1  Cantos norte. A avenida C vai ate y = 39,5 e passa por cima do ramal da
    2a mesa de B4; o ramal da 2a mesa de C6 cruza os dois de B5. A avenida C
    passa a acabar em 36,2 e B4-2, B5-1 e B5-2 recebem o corredor nordeste.
    No canto noroeste, a avenida A acaba em 36,7 e o ramal de B1-1 comeca
    em 37,4.
D2  O canal verde da S7 (10 m) corta os ramais de C1 e C2: passa a 6 m.
D3  As bocas brancas de S2 e S8 (8 m) cortam a avenida A e o modulo de C1:
    passam a 3 m. O "trilho sul da perna A" repete o trilho interno da
    avenida A e fecharia a boca: sai.
D4  Os serpenteados encostam no modulo e nao deixam os 1,50 m da linha de
    espera. Decisao de 23/10: manter como em 17/09.

    python3 scripts/montagem_hall2.py
"""
import html
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import separadores_fila as sf  # noqa: E402

RAIZ = sf.RAIZ
SAIDA = os.path.join(RAIZ, "mapa", "montagem_hall2.html")

# --------------------------------------------------------------------------
# Ajustes de campo aprovados em 23/10 (D1-D3). D4 nao muda a geometria.
# --------------------------------------------------------------------------
AJUSTES = {
    "topo_A": 36.70,        # D1: avenida A acaba logo acima do ramal de A5-2
    "topo_C": 36.20,        # D1: avenida C acaba logo acima do ramal de C6-2
    "corredor_NE": (36.20, 37.40),   # faixa livre de B entre C e os ramais
    "inicio_curto": 37.40,  # D1: boca dos ramais curtos da parede norte
    "canal_S7": 6.00,       # D2: canal verde da preferencial
    "boca_saida": 3.00,     # D3: guias brancas de S2 e S8
}
# Ramais da parede norte que comecam no corredor, e nao no distribuidor.
CURTOS_NORTE = {11.86, 35.43, 37.83, 41.73}

ESPERA = {"oeste": 5.60, "norte": 38.80, "leste": 41.70}   # linha zebrada
FRENTE = {"oeste": 4.10, "norte": 40.30, "leste": 43.20}   # frente do modulo
BOCA = {"oeste": 11.00, "norte": 35.40, "leste": 36.50}    # boca do ramal

# Posicoes das pecas de sinalizacao (P5/P6/P7). Os x-banners seguem a regra de
# 17/09 (4,60 m da linha das mesas; 8,60 m nas vermelhas; leste a partir de
# 47,30). C1 e isolada e baixa: no eixo, o banner ficaria no caminho entre a
# linha de espera e a mesa, entao vai para o vao entre C1 e C2.
PAINEIS = [  # pull-up 1000 x 2000, no vao morto entre as barreiras
    {"id": "Painel A", "zona": "A", "x": 25.90, "y": 3.00, "face": "oeste"},
    {"id": "Painel B", "zona": "B", "x": 30.90, "y": 3.00, "face": "oeste"},
    {"id": "Painel C", "zona": "C", "x": 32.60, "y": 6.80, "face": "leste"},
]
VINIS = [("A", "S4", 22.07), ("B", "S5", 28.29), ("C", "S6", 34.51)]

# Rotas de saida: as bandas trazem para fora (regra de 17/09).
SAI_OESTE = [(9.00, 37.05), (9.00, 1.80), (13.85, 1.80), (13.85, -0.6)]
SAI_NOROESTE = [(24.00, 35.00), (14.60, 35.00), (14.60, 37.05), (9.00, 37.05)]
SAI_LESTE = [(29.90, 35.00), (32.80, 35.00), (32.80, 36.80), (38.20, 36.80),
             (38.20, 8.30), (40.60, 8.30), (42.72, 3.00), (42.72, -0.6)]

# Rotas do teste da etapa 8 -- um eleitor de cada porta.
TESTES = [
    {"id": "A", "secao": "3313", "grupo": "A3", "cor": "A",
     "ida": [(23.43, -0.8), (23.43, 4.90), (12.50, 4.90), (12.50, 22.40),
             (8.60, 22.40), (4.40, 22.40)],
     "volta": [(4.40, 21.40), (9.00, 21.40), (9.00, 1.80), (13.85, 1.80),
               (13.85, -0.8)]},
    {"id": "B", "secao": "3832", "grupo": "B5", "cor": "B",
     "ida": [(28.30, -0.8), (28.30, 35.00), (32.80, 35.00), (32.80, 36.80),
             (41.73, 36.80), (41.73, 40.00)],
     "volta": [(40.70, 40.00), (40.10, 36.95), (38.20, 36.95), (38.20, 8.30),
               (40.60, 8.30), (42.72, 3.00), (42.72, -0.8)]},
    {"id": "C", "secao": "3442", "grupo": "C1", "cor": "C",
     "ida": [(33.50, -0.8), (33.50, 3.20), (35.00, 5.20), (35.00, 7.15),
             (43.00, 7.15)],
     "volta": [(42.40, 6.30), (42.72, 3.00), (42.72, -0.8)]},
    {"id": "P", "secao": "0519", "grupo": "C3", "cor": "P",
     "ida": [(38.72, -0.8), (38.72, 6.00), (38.20, 8.30), (38.20, 15.85),
             (43.00, 15.85)],
     "volta": []},
]


# --------------------------------------------------------------------------
# Dados
# --------------------------------------------------------------------------
def carrega():
    planta, dec, cen = sf.carrega()
    mesas = sf.monta_mesas(planta, dec, cen)
    with open(os.path.join(RAIZ, "data", "grupos_mesas.json"), encoding="utf-8") as f:
        grupos = json.load(f)["grupos"]
    return planta, dec, mesas, grupos


def eixo(m):
    """Coordenada do eixo da mesa ao longo da sua parede."""
    return m["x"] if m["parede"] == "norte" else m["y"]


def br(v, nd=2):
    return f"{v:.{nd}f}".replace(".", ",")


def sec4(n):
    return str(n).zfill(4)


def banner_pos(g):
    c = sum(g["coord"]) / len(g["coord"])
    if g["classe"] == "alta":
        rec = 8.60
    else:
        rec = 4.60
    if g["id"] == "C1":
        c = 8.35
    if g["parede"] == "oeste":
        return (rec, c)
    if g["parede"] == "norte":
        return (c, 44.40 - rec)
    return (47.30 - rec, c)


# --------------------------------------------------------------------------
# Geometria do chao, ja com os ajustes D1-D3
# --------------------------------------------------------------------------
def ramal(m):
    """(boca, espera) do canal de uma mesa nao vermelha, no eixo da mesa."""
    p = m["parede"]
    if p == "norte":
        ini = AJUSTES["inicio_curto"] if m["x"] in CURTOS_NORTE else BOCA["norte"]
        return ini, ESPERA["norte"]
    return BOCA[p], ESPERA[p]


def serp(dec, mrv):
    return next(s for s in dec["serpenteados"] if s["mrv"] == mrv)


def gaps_linha(mesas, parede, dec, larg=1.10):
    """Intervalos (ao longo da parede) em que a linha da boca fica aberta."""
    out = []
    for m in mesas:
        if m["parede"] != parede:
            continue
        if m["classe"] == "alta":
            s = serp(dec, m["mrv"])
            x1, y1, x2, y2 = s["rect"]
            out.append((x1, x2) if parede == "norte" else (y1, y2))
        else:
            e = eixo(m)
            out.append((e - larg / 2, e + larg / 2))
    return sorted(out)


def linha_com_vaos(a, b, vaos):
    """Segmentos de [a, b] tirando os vaos."""
    segs, cur = [], a
    for v1, v2 in vaos:
        if v2 <= a or v1 >= b:
            continue
        if v1 > cur:
            segs.append((cur, v1))
        cur = max(cur, v2)
    if cur < b:
        segs.append((cur, b))
    return segs


def fita_elementos(mesas, dec):
    """Toda a fita do chao: lista de (cor, polilinha, tipo)."""
    av = sf.AVENIDAS
    el = []
    tA, tC = AJUSTES["topo_A"], AJUSTES["topo_C"]
    vO = gaps_linha(mesas, "oeste", dec)
    vL = gaps_linha(mesas, "leste", dec)
    vN = gaps_linha(mesas, "norte", dec)
    # Avenida A: o trilho interno abre nas bocas da parede oeste
    ai = av["A"]["trilho_interno"]
    el.append(("A", [ai[0], ai[1], ai[2]], "avenida"))
    for y1, y2 in linha_com_vaos(3.40, tA, vO):
        el.append(("A", [(11.00, y1), (11.00, y2)], "avenida"))
    ae = av["A"]["trilho_externo"]
    el.append(("A", [ae[0], ae[1], ae[2], (14.00, tA)], "avenida"))
    el.append(("A", [(11.00, tA), (14.00, tA)], "fecho"))
    # Avenida B: barreira inteira, a fita so marca o eixo (galoes)
    # Avenida C: o trilho externo abre nas bocas da parede leste
    ci = av["C"]["trilho_interno"]
    el.append(("C", [ci[0], ci[1], ci[2], (33.50, tC)], "avenida"))
    ce = av["C"]["trilho_externo"]
    el.append(("C", [ce[0], ce[1], ce[2]], "avenida"))
    for y1, y2 in linha_com_vaos(5.20, tC, vL):
        el.append(("C", [(36.50, y1), (36.50, y2)], "avenida"))
    el.append(("C", [(33.50, tC), (36.50, tC)], "fecho"))
    # Distribuidor da parede norte (o T), so entre as avenidas A e C
    for x1, x2 in linha_com_vaos(15.21, 26.80, vN):
        el.append(("B", [(x1, 35.40), (x2, 35.40)], "distribuidor"))
    for x1, x2 in linha_com_vaos(29.80, 32.10, vN):
        el.append(("B", [(x1, 35.40), (x2, 35.40)], "distribuidor"))
    # Corredor nordeste: borda norte, aberta nas bocas curtas
    yN = AJUSTES["corredor_NE"][1]
    vNE = [(x - 0.55, x + 0.55) for x in sorted(CURTOS_NORTE) if x > 30]
    for x1, x2 in linha_com_vaos(32.10, 42.30, vNE):
        el.append(("B", [(x1, yN), (x2, yN)], "distribuidor"))
    # Ramais das 25 mesas nao vermelhas
    for m in mesas:
        if m["classe"] == "alta":
            continue
        ini, esp = ramal(m)
        e = eixo(m)
        for s_ in (-0.55, 0.55):
            if m["parede"] == "norte":
                el.append((m["entrada"], [(e + s_, ini), (e + s_, esp)], "ramal"))
            else:
                el.append((m["entrada"], [(ini, e + s_), (esp, e + s_)], "ramal"))
    # Acesso das vermelhas: as cintas externas do serpenteado seguem em fita
    for s in dec["serpenteados"]:
        x1, y1, x2, y2 = s["rect"]
        m = next(x for x in mesas if x["mrv"] == s["mrv"])
        if s["parede"] == "oeste":
            for y in (y1, y2):
                el.append(("A", [(x2, y), (11.00, y)], "ramal"))
        elif s["parede"] == "leste":
            for y in (y1, y2):
                el.append(("C", [(36.50, y), (x1, y)], "ramal"))
        else:
            for x in (x1, x2):
                el.append(("B", [(x, 35.40), (x, y1)], "ramal"))
    # D2: canal verde da preferencial
    for x in (38.09 - 0.60, 39.36 + 0.60):
        el.append(("P", [(x, 0.0), (x, AJUSTES["canal_S7"])], "preferencial"))
    # D3: guias brancas das saidas
    for x1, x2 in ((13.25, 14.45), (42.12, 43.32)):
        for x in (x1 - 0.60, x2 + 0.60):
            el.append(("S", [(x, 0.0), (x, AJUSTES["boca_saida"])], "saida"))
    return el


def zebras(mesas, dec):
    out = []
    for m in mesas:
        e = eixo(m)
        p = m["parede"]
        pos = ESPERA[p]
        if m["classe"] == "alta":           # D4: na saida do serpenteado
            pos = FRENTE[p] + (0.15 if p == "oeste" else -0.15)
        if p == "norte":
            out.append([(e - 0.55, pos), (e + 0.55, pos)])
        else:
            out.append([(pos, e - 0.55), (pos, e + 0.55)])
    return out


def marcas_fila(mesas):
    """Tiques de 0,65 m dentro de cada canal, da linha de espera para fora."""
    out = []
    for m in mesas:
        if m["classe"] == "alta":
            continue
        ini, esp = ramal(m)
        e = eixo(m)
        L = abs(ini - esp)
        n = int(round((L - 0.10) / sf.PASSO_FILA))
        sgn = 1 if ini > esp else -1
        for i in range(1, n + 1):
            d = esp + sgn * i * sf.PASSO_FILA
            if (d - ini) * sgn > -0.05:
                break
            if m["parede"] == "norte":
                out.append(((e - 0.55, d), (e - 0.30, d)))
            else:
                out.append(((d, e - 0.55), (d, e - 0.30)))
    return out


def eixos_avenida():
    """Polilinha do eixo de cada avenida, para os galoes."""
    return {
        "A": [(23.43, 0.0), (23.43, 4.90), (12.50, 4.90), (12.50, AJUSTES["topo_A"])],
        "B": [(28.30, 0.0), (28.30, 35.40)],
        "C": [(33.50, 0.0), (33.50, 3.20), (35.00, 5.20), (35.00, AJUSTES["topo_C"])],
    }


def pontos_ao_longo(pts, passo, ini=2.5):
    """Pontos e direcao a cada `passo` metros de uma polilinha."""
    out, d0 = [], ini
    acum = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if seg == 0:
            continue
        ux, uy = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
        while d0 <= acum + seg:
            t = d0 - acum
            out.append(((a[0] + ux * t, a[1] + uy * t), (ux, uy)))
            d0 += passo
        acum += seg
    return out


def barreiras(dec):
    """Trechos de unifila do desenho definitivo, com os serpenteados."""
    av = sf.AVENIDAS
    out = []
    for aid in ("A", "C"):
        for lado in ("interno", "externo"):
            out.append((aid, sf._recorta(av[aid][f"trilho_{lado}"], sf.BOCA_PROF),
                        f"boca {aid} · {lado}"))
    for lado in ("interno", "externo"):
        out.append(("B", av["B"][f"trilho_{lado}"], f"avenida B · {lado}"))
    for s in dec["serpenteados"]:
        for t in sf.serpenteado_trilhos(s):
            out.append(("R", t, f"serpenteado {s['mrv']}"))
    return out


def postes_de(t):
    L = sf.comp(t)
    n = sf.postes(L)
    pts = []
    for i in range(n):
        d = 0 if n == 1 else i / (n - 1) * L
        rest = d
        for j in range(len(t) - 1):
            seg = math.dist(t[j], t[j + 1])
            if rest <= seg + 1e-9 or j == len(t) - 2:
                u = 0 if seg == 0 else min(1, rest / seg)
                pts.append((t[j][0] + (t[j + 1][0] - t[j][0]) * u,
                            t[j][1] + (t[j + 1][1] - t[j][1]) * u))
                break
            rest -= seg
    return pts


def pontos_controle():
    """Os piquetes da etapa 2, com a referencia fisica de onde medir."""
    tA, tC = AJUSTES["topo_A"], AJUSTES["topo_C"]
    return [
        ("A1", 21.83, 0.00, "S4: 2,73 m do batente oeste"),
        ("A2", 21.83, 3.40, "3,40 m para dentro a partir de A1"),
        ("A3", 11.00, 3.40, "11,00 m da parede oeste"),
        ("A4", 11.00, tA, "fim da avenida A (D1)"),
        ("A5", 25.03, 0.00, "S4: batente leste (alvenaria S4|S5)"),
        ("A6", 25.03, 6.40, "6,40 m para dentro a partir de A5"),
        ("A7", 14.00, 6.40, "14,00 m da parede oeste"),
        ("A8", 14.00, tA, "fim da avenida A (D1)"),
        ("B1", 26.80, 0.00, "S5: 1,48 m do batente oeste"),
        ("B2", 26.80, 35.40, "9,00 m da parede norte"),
        ("B3", 29.80, 0.00, "S5: 1,45 m do batente leste"),
        ("B4", 29.80, 35.40, "9,00 m da parede norte"),
        ("C1", 32.00, 0.00, "S6: 0,46 m do batente oeste"),
        ("C2", 32.00, 3.20, "3,20 m para dentro a partir de C1"),
        ("C3", 33.50, 5.20, "diagonal de 2,50 m a partir de C2"),
        ("C4", 33.50, tC, "fim da avenida C (D1)"),
        ("C5", 35.00, 0.00, "S6: 2,47 m do batente leste"),
        ("C6", 35.00, 3.20, "3,20 m para dentro a partir de C5"),
        ("C7", 36.50, 5.20, "10,80 m da linha das mesas leste"),
        ("C8", 36.50, tC, "fim da avenida C (D1)"),
        ("N1", 32.10, 37.40, "7,00 m da parede norte"),
        ("N2", 42.30, 37.40, "7,00 m da parede norte"),
        ("L1", 47.30, 3.00, "3,00 m da fachada leste"),
        ("L2", 47.30, 41.40, "3,00 m da fachada leste"),
    ]


# --------------------------------------------------------------------------
# SVG
# --------------------------------------------------------------------------
class Planta:
    """Desenha um recorte do salao. Coordenadas da prancheta: x para leste,
    y para o norte, origem no canto sudoeste da linha da fachada sul."""

    def __init__(self, uid, x0=-1.6, y0=-2.6, x1=52.2, y1=45.8, S=13.0):
        self.uid, self.x0, self.y0, self.x1, self.y1, self.S = uid, x0, y0, x1, y1, S
        self.W = (x1 - x0) * S
        self.H = (y1 - y0) * S
        self.out = []

    def p(self, x, y):
        return ((x - self.x0) * self.S, (self.y1 - y) * self.S)

    def pts(self, ps):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*q) for q in ps))

    def add(self, s):
        self.out.append(s)

    def line(self, ps, cls, extra=""):
        self.add(f'<polyline class="{cls}" points="{self.pts(ps)}"{extra}/>')

    def rect(self, x1, y1, x2, y2, cls, extra=""):
        a, b = self.p(min(x1, x2), max(y1, y2))
        w, h = abs(x2 - x1) * self.S, abs(y2 - y1) * self.S
        self.add(f'<rect class="{cls}" x="{a:.1f}" y="{b:.1f}" width="{w:.1f}" '
                 f'height="{h:.1f}"{extra}/>')

    def text(self, x, y, s, cls, anchor="middle", rot=0, dy=0):
        a, b = self.p(x, y)
        tr = f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ""
        self.add(f'<text class="{cls}" x="{a:.1f}" y="{b + dy:.1f}" '
                 f'text-anchor="{anchor}"{tr}>{html.escape(s)}</text>')

    def circle(self, x, y, r, cls):
        a, b = self.p(x, y)
        self.add(f'<circle class="{cls}" cx="{a:.1f}" cy="{b:.1f}" r="{r:.1f}"/>')

    def svg(self, titulo):
        u = self.uid
        defs = (
            f'<defs><pattern id="h-{u}" width="6" height="6" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" '
            f'class="hatch"/></pattern>'
            f'<marker id="m-{u}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" '
            f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'class="arrowhead"/></marker></defs>')
        return (f'<svg class="planta" viewBox="0 0 {self.W:.0f} {self.H:.0f}" role="img" '
                f'aria-label="{html.escape(titulo)}" xmlns="http://www.w3.org/2000/svg">'
                f'{defs}{"".join(self.out)}</svg>')


def desenha_base(P, planta, dec, destaque_protegidas=False):
    c = planta["salao"]["contorno"]
    P.line(c + [c[0]], "piso")
    P.line(c + [c[0]], "parede")
    h = f"url(#h-{P.uid})"
    cls = "prot forte" if destaque_protegidas else "prot"
    for z in dec["zonas_protegidas"]:
        x1, y1, x2, y2 = z["rect"]
        if z["tipo"] == "sala_apoio":
            P.rect(x1, y1, x2, y2, "apoio")
            P.text((x1 + x2) / 2, (y1 + y2) / 2, "apoio", "lbl-s", dy=3)
            continue
        P.rect(x1, y1, x2, y2, cls, f' fill="{h}"')
    for pt in planta["portas"]:
        papel = dec["sinalizacao_portas"].get(pt["id"], {}).get("papel", "livre")
        if pt["id"] in ("S4", "S5", "S6"):
            papel = "entrada" + {"S4": "A", "S5": "B", "S6": "C"}[pt["id"]]
        if pt["id"] == "S7":
            papel = "preferencial"
        P.line([(pt["x1"], pt["y1"]), (pt["x2"], pt["y2"])], f"porta {papel}")
        mx, my = (pt["x1"] + pt["x2"]) / 2, (pt["y1"] + pt["y2"]) / 2
        if pt["face"] == "sul":
            P.text(mx, my - 1.55, pt["id"], "lbl-porta")
        elif pt["face"] == "leste":
            P.text(mx + 1.0, my, pt["id"], "lbl-porta", rot=90)
        elif pt["face"] == "norte":
            P.text(mx, my + 0.55, pt["id"], "lbl-porta")
        else:
            P.text(mx - 0.75, my, pt["id"], "lbl-porta", rot=-90)
    # escala e norte
    P.line([(0.0, -1.95), (10.0, -1.95)], "escala")
    for x in (0.0, 5.0, 10.0):
        P.line([(x, -1.75), (x, -2.15)], "escala")
    P.text(10.4, -1.95, "10 m", "lbl-s", anchor="start", dy=3)


def desenha_mesas(P, mesas, planta, rotulo=True):
    Pm, L = planta["modulo"]["prof"], planta["modulo"]["larg"] / 2
    for m in mesas:
        e = eixo(m)
        if m["parede"] == "oeste":
            r = (0, e - L, Pm, e + L)
        elif m["parede"] == "leste":
            r = (47.3 - Pm, e - L, 47.3, e + L)
        else:
            r = (e - L, 44.4 - Pm, e + L, 44.4)
        cls = f"mod z{m['entrada']}" + (" alta" if m["classe"] == "alta" else "")
        P.rect(*r, cls)
        if rotulo:
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            rot = -90 if m["parede"] == "norte" else 0
            P.text(cx, cy, m["grupo"], f"lbl-mod t{m['entrada']}", rot=rot, dy=3)


def desenha_controle(P, mesas):
    for pid, x, y, _ in pontos_controle():
        P.line([(x - 0.45, y), (x + 0.45, y)], "piq")
        P.line([(x, y - 0.45), (x, y + 0.45)], "piq")
        dx = -0.6 if pid in ("A1", "B1", "C1", "C5", "A5", "B3") else 0.6
        anchor = "end" if dx < 0 else "start"
        if pid.startswith("L"):
            dx, anchor = -0.6, "end"
        P.text(x + dx, y + 0.35, pid, "lbl-piq", anchor=anchor)
    for m in mesas:
        e = eixo(m)
        if m["parede"] == "oeste":
            P.line([(0.0, e), (FRENTE["oeste"], e)], "giz")
        elif m["parede"] == "leste":
            P.line([(FRENTE["leste"], e), (47.30, e)], "giz")
        else:
            P.line([(e, FRENTE["norte"]), (e, 44.40)], "giz")
    P.line([(47.30, 0.0), (47.30, 44.4)], "giz forte")
    P.line([(FRENTE["oeste"], 7.5), (FRENTE["oeste"], 36.8)], "giz")
    P.line([(FRENTE["leste"], 6.5), (FRENTE["leste"], 36.2)], "giz")
    P.line([(11.2, FRENTE["norte"]), (42.4, FRENTE["norte"])], "giz")
    P.text(47.9, 22.0, "linha das mesas · 3,00 m da fachada", "lbl-s", rot=90)


def desenha_fita(P, mesas, dec):
    for cor, ps, tipo in fita_elementos(mesas, dec):
        if cor == "S":
            P.line(ps, "fita-branca-base")
            P.line(ps, "fita-branca")
        else:
            P.line(ps, f"fita f{cor}" + (" fecho" if tipo == "fecho" else ""))
    for a, b in marcas_fila(mesas):
        m = [a, b]
        P.line(m, "tique")
    for z in zebras(mesas, dec):
        P.line(z, "zebra-base")
        P.line(z, "zebra")
    for aid, ps in eixos_avenida().items():
        for (x, y), (ux, uy) in pontos_ao_longo(ps, sf.PASSO_GALAO):
            desenha_galao(P, x, y, ux, uy, f"galao f{aid}")
    for (x, y), (ux, uy) in pontos_ao_longo(
            [(32.80, 36.80), (41.0, 36.80)], 2.6, ini=1.2):
        desenha_galao(P, x, y, ux, uy, "galao fB")
    for rota in (SAI_OESTE, SAI_NOROESTE, SAI_LESTE):
        for (x, y), (ux, uy) in pontos_ao_longo(rota, 4.0, ini=1.5):
            desenha_galao(P, x, y, ux, uy, "galao-saida")


def desenha_galao(P, x, y, ux, uy, cls, t=0.55):
    px_, py_ = -uy, ux
    a = (x - ux * t * 0.6 + px_ * t, y - uy * t * 0.6 + py_ * t)
    b = (x + ux * t * 0.4, y + uy * t * 0.4)
    c = (x - ux * t * 0.6 - px_ * t, y - uy * t * 0.6 - py_ * t)
    P.line([a, b, c], cls)


def desenha_barreiras(P, dec):
    for zona, t, _ in barreiras(dec):
        P.line(t, "cinta-base")
        P.line(t, f"cinta c{zona}")
        for q in postes_de(t):
            P.circle(q[0], q[1], 2.3, "poste")


def desenha_sinal(P, grupos):
    for g in grupos:
        x, y = banner_pos(g)
        if g["parede"] == "norte":
            P.rect(x - 0.45, y - 0.22, x + 0.45, y + 0.22, f"xb z{g['entrada']}")
            P.text(x, y - 0.75, g["id"], "lbl-xb", dy=3)
        else:
            P.rect(x - 0.22, y - 0.45, x + 0.22, y + 0.45, f"xb z{g['entrada']}")
            off = 0.75 if g["parede"] == "oeste" else -0.75
            P.text(x + off, y, g["id"], "lbl-xb",
                   anchor="start" if off > 0 else "end", dy=3)
    for pn in PAINEIS:
        x, y = pn["x"], pn["y"]
        if pn["face"] in ("oeste", "leste"):
            P.rect(x - 0.18, y - 0.55, x + 0.18, y + 0.55, f"pull z{pn['zona']}")
        P.text(x, y + 1.15, pn["id"].replace("Painel ", "P"), "lbl-xb", dy=3)
    for letra, _, x in VINIS:
        P.rect(x - 0.6, -1.25, x + 0.6, -0.15, f"vinil z{letra}")
        P.text(x, -0.70, letra, f"lbl-vinil t{letra}", dy=3)
    P.rect(38.12, -1.25, 39.32, -0.15, "vinil zP")
    P.text(38.72, -0.70, "P", "lbl-vinil tP", dy=3)
    for x in (13.85, 42.72):
        P.rect(x - 0.7, 0.25, x + 0.7, 0.95, "correx")


def desenha_testes(P):
    for t in TESTES:
        P.line(t["ida"], f"rota r{t['cor']}", f' marker-end="url(#m-{P.uid})"')
        if t["volta"]:
            P.line(t["volta"], "rota rS", f' marker-end="url(#m-{P.uid})"')
        x, y = t["ida"][-1]
        P.circle(x, y, 4.2, f"alvo r{t['cor']}")


def planta_etapa(uid, fase, planta, dec, mesas, grupos):
    """fase: 1 reconhecimento ... 8 teste. 0 = planta final completa."""
    P = Planta(uid)
    desenha_base(P, planta, dec, destaque_protegidas=(fase == 1))
    camadas = [
        (2, lambda: desenha_controle(P, mesas)),
        (3, lambda: desenha_mesas(P, mesas, planta)),
        (5, lambda: desenha_fita(P, mesas, dec)),
        (6, lambda: desenha_barreiras(P, dec)),
        (7, lambda: desenha_sinal(P, grupos)),
        (8, lambda: desenha_testes(P)),
    ]
    for f, fn in camadas:
        if fase == 0:
            if f in (2, 8):
                continue
            fn()
            continue
        if f > fase:
            continue
        if f == 2 and fase > 3:
            continue          # os piquetes somem sob as mesas e a fita
        P.add('<g class="ghost">' if f < fase else '<g class="atual">')
        fn()
        P.add('</g>')
    return P.svg(f"Planta do Hall 2 — etapa {fase}")


def planta_bocas(planta, dec, mesas, grupos):
    """Zoom da fachada sul: portas, bocas, painéis, verde e branco."""
    P = Planta("bocas", x0=9.5, y0=-2.2, x1=45.5, y1=12.5, S=21.0)
    desenha_base(P, planta, dec)
    desenha_mesas(P, mesas, planta)
    desenha_fita(P, mesas, dec)
    desenha_barreiras(P, dec)
    desenha_sinal(P, grupos)
    for x1, x2, txt in ((19.23, 25.03, "boca A · 6 m de barreira"),
                        (32.0, 36.5, "boca C · 6 m"), (26.8, 29.8, "avenida B · barreira inteira")):
        P.text((x1 + x2) / 2, 8.6, txt, "lbl-s")
    P.text(38.72, 6.6, "verde · 6 m (D2)", "lbl-s")
    P.text(13.85, 3.5, "branco · 3 m (D3)", "lbl-s")
    P.text(42.72, 3.5, "branco · 3 m (D3)", "lbl-s")
    return P.svg("Fachada sul: bocas, painéis e sinalização das portas")


def planta_nordeste(planta, dec, mesas, ajustado):
    """Canto nordeste antes e depois do ajuste D1."""
    P = Planta("ne" + ("1" if ajustado else "0"), x0=30.0, y0=29.5, x1=48.2, y1=45.0, S=22.0)
    desenha_base(P, planta, dec)
    desenha_mesas(P, mesas, planta)
    if ajustado:
        desenha_fita(P, mesas, dec)
        P.rect(32.10, AJUSTES["corredor_NE"][0], 42.30, AJUSTES["corredor_NE"][1],
               "corredor")
        P.text(37.9, 36.75, "corredor B", "lbl-s", dy=3)
    else:
        av = sf.AVENIDAS["C"]
        for t in (av["trilho_interno"], av["trilho_externo"]):
            P.line([q for q in t if q[1] > 29], "fita fC")
        P.line([(32.0, 35.40), (42.3, 35.40)], "fita fB")
        for m in mesas:
            if m["classe"] == "alta" or not (m["parede"] == "leste" and m["y"] > 30
                                             or m["parede"] == "norte" and m["x"] > 30):
                continue
            e = eixo(m)
            for s_ in (-0.55, 0.55):
                if m["parede"] == "norte":
                    P.line([(e + s_, 35.40), (e + s_, 38.80)], "fita fB")
                else:
                    P.line([(36.50, e + s_), (41.70, e + s_)], "fita fC")
        for r in ((34.88, 35.40, 35.98, 38.80), (37.28, 35.40, 38.38, 36.10),
                  (41.18, 35.40, 42.28, 36.10)):
            P.rect(*r, "conflito")
        P.text(35.43, 39.2, "B4 × avenida C", "lbl-conf", dy=3)
        P.text(39.8, 34.3, "C6 × B5", "lbl-conf", dy=3)
    return P.svg("Canto nordeste " + ("com o ajuste D1" if ajustado else "no desenho de 17/09"))


def detalhe_par():
    """Um par de mesas da parede oeste em escala grande, com as cotas."""
    S = 46.0
    x0, y0, x1, y1 = -0.9, -1.6, 15.2, 6.4
    W, H = (x1 - x0) * S, (y1 - y0) * S

    def p(x, y):
        return ((x - x0) * S, (y1 - y) * S)

    o = []

    def ln(ps, cls):
        o.append(f'<polyline class="{cls}" points="' +
                 " ".join(f"{a:.1f},{b:.1f}" for a, b in (p(*q) for q in ps)) + '"/>')

    def rc(xa, ya, xb, yb, cls):
        a, b = p(xa, max(ya, yb))
        o.append(f'<rect class="{cls}" x="{a:.1f}" y="{b:.1f}" width="{abs(xb - xa) * S:.1f}" '
                 f'height="{abs(yb - ya) * S:.1f}"/>')

    def tx(x, y, s, cls, anchor="middle", dy=0):
        a, b = p(x, y)
        o.append(f'<text class="{cls}" x="{a:.1f}" y="{b + dy:.1f}" text-anchor="{anchor}">'
                 f'{html.escape(s)}</text>')

    def cota(xa, xb, y, s):
        ln([(xa, y), (xb, y)], "cota")
        ln([(xa, y - 0.12), (xa, y + 0.12)], "cota")
        ln([(xb, y - 0.12), (xb, y + 0.12)], "cota")
        tx((xa + xb) / 2, y + 0.18, s, "lbl-cota")

    def cotav(x, ya, yb, s):
        ln([(x, ya), (x, yb)], "cota")
        ln([(x - 0.12, ya), (x + 0.12, ya)], "cota")
        ln([(x - 0.12, yb), (x + 0.12, yb)], "cota")
        a, b = p(x + 0.2, (ya + yb) / 2)
        o.append(f'<text class="lbl-cota" x="{a:.1f}" y="{b + 4:.1f}" '
                 f'text-anchor="start">{html.escape(s)}</text>')

    e1, e2 = 1.0, 4.9               # dois eixos de um par (3,90 m)
    rc(-0.35, -1.0, 0.0, 6.2, "parede-det")
    rc(11.0, -1.0, 14.0, 6.2, "avenida-det")
    tx(12.5, 2.9, "AVENIDA A · 3,00 m", "lbl-av")
    for e in (e1, e2):
        rc(0, e - 0.45, 4.1, e + 0.45, "mod zA")
        tx(2.05, e, "módulo · 4,10 m", "lbl-mod tA", dy=4)
        for s_ in (-0.55, 0.55):
            ln([(5.6, e + s_), (11.0, e + s_)], "fita fA")
        for i in range(1, 9):
            d = 5.6 + i * 0.65
            if d > 10.95:
                break
            ln([(d, e - 0.55), (d, e - 0.30)], "tique")
        ln([(5.6, e - 0.55), (5.6, e + 0.55)], "zebra-base")
        ln([(5.6, e - 0.55), (5.6, e + 0.55)], "zebra")
        rc(7.0, e + 0.62, 8.2, e + 0.95, "papel")
    rc(4.38, 2.95 - 0.12, 4.82, 2.95 + 0.12, "xb zA")
    tx(4.6, 3.35, "x-banner do grupo", "lbl-s")
    tx(7.6, e2 + 1.25, "papel plastificado, fora da pisada", "lbl-s")
    cota(0.0, 4.1, -0.55, "4,10")
    cota(4.1, 5.6, -1.0, "1,50 · sigilo")
    cota(5.6, 11.0, -0.55, "5,40 · canal com marcas a cada 0,65")
    cota(0.0, 4.6, 5.9, "4,60 até o x-banner")
    cotav(6.4, e1 + 0.55, e2 - 0.55, "2,80 entre canais")
    cotav(1.4, e1 + 0.45, e2 - 0.45, "3,00 livres")
    cotav(10.4, e1 - 0.55, e1 + 0.55, "1,10")
    tx(5.65, e1 - 0.95, "linha de espera · zebrado", "lbl-s")
    tx(0.2, -1.45, "parede oeste", "lbl-s", anchor="start")
    return (f'<svg class="planta" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
            f'aria-label="Detalhe de um par de mesas da parede oeste" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(o)}</svg>')


# --------------------------------------------------------------------------
# Tabelas
# --------------------------------------------------------------------------
def tabela_mesas(mesas, grupos):
    ref = {"oeste": "canto do recorte (y 7,00)", "norte": "parede oeste (x 0)",
           "leste": "fachada sul (y 0)"}
    base = {"oeste": 7.0, "norte": 0.0, "leste": 0.0}
    linhas = []
    for parede, zona in (("oeste", "A"), ("norte", "B"), ("leste", "C")):
        ms = sorted((m for m in mesas if m["parede"] == parede), key=eixo)
        linhas.append(f'<tr class="sep"><th colspan="7">Zona {zona} · parede {parede} · '
                      f'medir a partir de: {ref[parede]}</th></tr>')
        prev = None
        for m in ms:
            e = eixo(m)
            gap = "" if prev is None else br(e - prev)
            prev = e
            ini, esp = (None, None) if m["classe"] == "alta" else ramal(m)
            canal = "serpenteado" if ini is None else f"{br(esp)} → {br(ini)}"
            secs = " · ".join(sec4(s) for s in m["secoes"])
            flag = ' <span class="tag">vermelha</span>' if m["classe"] == "alta" else ""
            linhas.append(
                f'<tr><td>{m["grupo"]}</td><td>{secs}{flag}</td>'
                f'<td class="n">{br(e)}</td><td class="n">{br(e - base[parede])}</td>'
                f'<td class="n">{gap}</td><td class="n">{br(FRENTE[parede])}</td>'
                f'<td class="n">{canal}</td></tr>')
    return ('<table class="dados"><thead><tr><th>Grupo</th><th>Seções da mesa</th>'
            '<th>Eixo (m)</th><th>Medida na parede</th><th>Até o eixo anterior</th>'
            '<th>Frente do módulo</th><th>Canal: espera → boca</th></tr></thead><tbody>'
            + "".join(linhas) + "</tbody></table>")


def tabela_controle():
    rows = "".join(
        f'<tr><td><b>{pid}</b></td><td class="n">{br(x)}</td><td class="n">{br(y)}</td>'
        f'<td>{html.escape(ref)}</td></tr>' for pid, x, y, ref in pontos_controle())
    return ('<table class="dados"><thead><tr><th>Ponto</th><th>x (m)</th><th>y (m)</th>'
            '<th>Como achar no salão</th></tr></thead><tbody>' + rows + "</tbody></table>")


def tabela_banners(grupos):
    rows = []
    for g in grupos:
        x, y = banner_pos(g)
        secs = " ".join(sec4(s) for s in sorted(g["secoes"]))
        nota = {"alta": "atrás do serpenteado (8,60 m)",
                }.get(g["classe"], "boca do corredor do par (4,60 m)")
        if g["tipo"] == "isolada" and g["classe"] != "alta":
            nota = "no vão entre C1 e C2, fora do caminho da mesa"
        rows.append(f'<tr><td><b>{g["id"]}</b></td><td>{secs}</td>'
                    f'<td class="n">{br(x)} · {br(y)}</td><td>{nota}</td></tr>')
    return ('<table class="dados"><thead><tr><th>Grupo</th><th>Seções impressas</th>'
            '<th>x · y (m)</th><th>Onde</th></tr></thead><tbody>' + "".join(rows)
            + "</tbody></table>")


def _por_cor(mesas, dec):
    import planta_cotada_a3 as pc   # importa este modulo: so em tempo de execucao
    out = {}
    for g in pc.trechos(mesas, dec).values():
        out[g["cor"]] = out.get(g["cor"], 0.0) + g["m"]
    return out


def total_fita(mesas, dec):
    return sum(_por_cor(mesas, dec).values()) * (1 + sf.RETOQUE)


def linhas_fita(mesas, dec):
    uso = {"A": "avenida A, 9 canais, marcas, galões", "B": "distribuidor, corredor NE, 9 canais, marcas, galões",
           "C": "avenida C, 10 canais, marcas, galões", "Z": "28 linhas de espera",
           "P": "canal da S7 (D2)", "S": "guias de S2/S8 (D3) e galões de saída"}
    nomes = [("A", "Fita azul (zona A)"), ("B", "Fita amarela (zona B)"), ("C", "Fita laranja (zona C)"),
             ("Z", "Fita zebrada preto-e-branco"), ("P", "Fita verde"), ("S", "Fita branca")]
    pc = _por_cor(mesas, dec)
    out = []
    for c, n in nomes:
        v = pc.get(c, 0.0) * (1 + sf.RETOQUE)
        out.append(f'<tr><td>{n}</td><td class="n">{br(v, 0)} m · {math.ceil(v / sf.ROLO)} rolo(s)</td>'
                   f'<td>{uso[c]}</td></tr>')
    return "".join(out)


def resumo_material(dec):
    bar = barreiras(dec)
    n = sum(sf.postes(sf.comp(t)) for _, t, _ in bar)
    return n


# --------------------------------------------------------------------------
# Pagina
# --------------------------------------------------------------------------
CSS = r"""
:root{
  /* Layout: um caderno de obra — coluna de texto à esquerda, planta grande à direita, uma etapa por bloco. */
  --papel:#eef1f4; --folha:#ffffff; --tinta:#16202b; --suave:#566271; --linha:#cfd6de;
  --piso:#f7f8fa; --parede:#16202b; --fantasma:#9aa4b0;
  --zA:#33507E; --zB:#E8C63A; --zC:#DE7343; --zP:#1e8449; --zS:#ffffff;
  --tA:#ffffff; --tB:#16202b; --tC:#16202b;
  --alerta:#b8321f; --alerta-fundo:#fbe9e5; --ok:#1e7a45; --ok-fundo:#e3f2e9;
  --nota-fundo:#f3efe0;
  --f-titulo:"Barlow Condensed","Arial Narrow",sans-serif;
  --f-texto:"IBM Plex Sans",system-ui,sans-serif;
  --f-dado:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --papel:#10161d; --folha:#18212b; --tinta:#e6ebf0; --suave:#9aa7b5; --linha:#2d3a48;
  --piso:#1d2833; --parede:#d7dee6; --fantasma:#4b5866;
  --zA:#5b7cb3; --tA:#ffffff;
  --alerta:#ff8a72; --alerta-fundo:#3a1f1a; --ok:#6fd39a; --ok-fundo:#18301f;
  --nota-fundo:#2b2818; color-scheme:dark}}
:root[data-theme="dark"]{
  --papel:#10161d; --folha:#18212b; --tinta:#e6ebf0; --suave:#9aa7b5; --linha:#2d3a48;
  --piso:#1d2833; --parede:#d7dee6; --fantasma:#4b5866;
  --zA:#5b7cb3; --tA:#ffffff;
  --alerta:#ff8a72; --alerta-fundo:#3a1f1a; --ok:#6fd39a; --ok-fundo:#18301f;
  --nota-fundo:#2b2818; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--papel);color:var(--tinta);font-family:var(--f-texto);font-size:15px;line-height:1.55;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:1180px;margin:0 auto;padding-block:28px 64px;display:flex;flex-direction:column;gap:34px}
h1,h2,h3{font-family:var(--f-titulo);font-weight:700;line-height:1.1;text-wrap:balance;margin:0}
h1{font-size:clamp(34px,5vw,54px);letter-spacing:.005em}
h2{font-size:30px}
h3{font-size:19px;letter-spacing:.04em;text-transform:uppercase}
p{margin:0;max-width:68ch}
.eyebrow{font-family:var(--f-dado);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--suave)}
header{display:flex;flex-direction:column;gap:14px;padding-bottom:22px;border-bottom:3px solid var(--tinta)}
.zebra-faixa{height:10px;background:repeating-linear-gradient(90deg,var(--tinta) 0 18px,var(--papel) 18px 36px);border:1px solid var(--tinta)}
.lead{font-size:18px;max-width:72ch}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:var(--f-dado);font-size:12px;padding:3px 9px;border:1px solid var(--linha);border-radius:3px;background:var(--folha)}
.bloco{background:var(--folha);border:1px solid var(--linha);padding:22px;display:flex;flex-direction:column;gap:16px}
.duas{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px}
@media (max-width:860px){.duas{grid-template-columns:minmax(0,1fr)}}
.regras{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:0;padding:0;list-style:none}
.regras li{border-top:3px solid var(--tinta);padding-top:8px;display:flex;flex-direction:column;gap:4px}
.regras b{font-family:var(--f-titulo);font-size:19px}
.etapa{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:24px;background:var(--folha);border:1px solid var(--linha);padding:22px}
@media (max-width:960px){.etapa{grid-template-columns:minmax(0,1fr)}}
.etapa-cab{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.num{font-family:var(--f-titulo);font-size:58px;line-height:.8;font-weight:800}
.hora{font-family:var(--f-dado);font-size:12.5px;color:var(--suave)}
.texto{display:flex;flex-direction:column;gap:14px;min-width:0}
ol.passos{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:7px;counter-reset:p}
ol.passos li{counter-increment:p}
ol.passos label{display:grid;grid-template-columns:22px 26px minmax(0,1fr);gap:4px;align-items:start;cursor:pointer}
ol.passos label::before{content:counter(p) ".";grid-column:2;grid-row:1;font-family:var(--f-dado);font-size:12.5px;color:var(--suave);padding-top:2px}
ol.passos input{grid-column:1;grid-row:1;margin:3px 0 0;width:16px;height:16px;accent-color:var(--tinta)}
ol.passos span{grid-column:3}
ol.passos input:checked ~ span{color:var(--suave);text-decoration:line-through;text-decoration-thickness:1px}
input:focus-visible,button:focus-visible{outline:2px solid var(--zA);outline-offset:2px}
.pronto{background:var(--ok-fundo);border-left:4px solid var(--ok);padding:10px 12px;font-size:14px}
.pronto b{color:var(--ok)}
.cuidado{background:var(--alerta-fundo);border-left:4px solid var(--alerta);padding:10px 12px;font-size:14px}
.cuidado b{color:var(--alerta)}
.parada{font-family:var(--f-dado);font-size:12px;letter-spacing:.08em;text-transform:uppercase;background:var(--tinta);color:var(--papel);padding:2px 8px;align-self:flex-start}
.fig{display:flex;flex-direction:column;gap:8px;min-width:0}
.fig-scroll{overflow-x:auto;border:1px solid var(--linha);background:var(--piso)}
.fig-scroll svg{display:block;width:100%;min-width:560px;height:auto}
figcaption{font-size:13px;color:var(--suave)}
.legenda{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--suave)}
.legenda i{display:inline-block;width:18px;height:4px;vertical-align:middle;margin-right:5px}
.tabwrap{overflow-x:auto}
table.dados{border-collapse:collapse;width:100%;font-size:13.5px;font-variant-numeric:tabular-nums}
table.dados th,table.dados td{border-bottom:1px solid var(--linha);padding:5px 8px;text-align:left;vertical-align:top}
table.dados thead th{font-family:var(--f-dado);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--suave);font-weight:500}
table.dados td.n{font-family:var(--f-dado);font-size:12.5px;white-space:nowrap}
table.dados tr.sep th{background:var(--papel);font-family:var(--f-titulo);font-size:15px;letter-spacing:.03em}
.tag{font-family:var(--f-dado);font-size:10.5px;color:var(--alerta);border:1px solid var(--alerta);padding:0 4px;margin-left:4px}
.decisao{display:grid;grid-template-columns:minmax(0,1fr);align-content:start;gap:10px;border-top:3px solid var(--alerta);padding-top:12px}
.decisao h3{color:var(--alerta)}
.decisoes{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}
.nota{background:var(--nota-fundo);padding:12px 14px;font-size:14px}
.agenda{display:grid;grid-template-columns:minmax(0,1fr);gap:0;border-top:1px solid var(--linha)}
.agenda div{display:grid;grid-template-columns:110px 36px minmax(0,1fr) 140px;gap:10px;padding:7px 0;border-bottom:1px solid var(--linha);align-items:baseline}
.agenda .t{font-family:var(--f-dado);font-size:12.5px}
.agenda .e{font-family:var(--f-titulo);font-size:20px;font-weight:800}
.agenda .q{font-size:13px;color:var(--suave)}
@media (max-width:620px){.agenda div{grid-template-columns:90px 30px minmax(0,1fr)}.agenda .q{grid-column:3}}
.barra-acoes{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
button{font:inherit;font-size:13px;padding:6px 12px;border:1px solid var(--tinta);background:var(--folha);color:var(--tinta);cursor:pointer}
code{font-family:var(--f-dado);font-size:.9em}
/* planta */
.planta text{font-family:var(--f-texto)}
.piso{fill:var(--folha);stroke:none}
.parede{fill:none;stroke:var(--parede);stroke-width:3.2;stroke-linejoin:round}
.prot{stroke:var(--alerta);stroke-width:.8;stroke-dasharray:3 2;opacity:.55}
.prot.forte{opacity:1;stroke-width:1.6}
.hatch{stroke:var(--alerta);stroke-width:1.4;opacity:.55}
.apoio{fill:var(--papel);stroke:var(--linha)}
.porta{fill:none;stroke-width:6.5;stroke-linecap:butt}
.porta.entradaA{stroke:var(--zA)} .porta.entradaB{stroke:var(--zB)} .porta.entradaC{stroke:var(--zC)}
.porta.saida{stroke:var(--tinta)} .porta.emergencia{stroke:var(--alerta)} .porta.preferencial{stroke:var(--zP)}
.porta.fechada,.porta.livre{stroke:var(--fantasma)}
.lbl-porta{font-size:10.5px;font-weight:700;fill:var(--tinta)}
.lbl-s{font-size:9.5px;fill:var(--suave)}
.escala{fill:none;stroke:var(--tinta);stroke-width:1.2}
.mod{stroke:var(--tinta);stroke-width:.7}
.mod.zA{fill:var(--zA)} .mod.zB{fill:var(--zB)} .mod.zC{fill:var(--zC)}
.mod.alta{stroke:var(--alerta);stroke-width:2.2}
.lbl-mod{font-size:8.5px;font-weight:700}
.tA{fill:var(--tA)} .tB{fill:var(--tB)} .tC{fill:var(--tC)} .tP{fill:#ffffff}
.piq{fill:none;stroke:var(--alerta);stroke-width:1.6}
.lbl-piq{font-family:var(--f-dado)!important;font-size:9px;fill:var(--alerta);font-weight:600}
.giz{fill:none;stroke:var(--suave);stroke-width:.9;stroke-dasharray:4 3}
.giz.forte{stroke:var(--alerta);stroke-width:1.4}
.fita{fill:none;stroke-width:2.2;stroke-linecap:butt}
.fA{stroke:var(--zA)} .fB{stroke:var(--zB)} .fC{stroke:var(--zC)} .fP{stroke:var(--zP)}
.fita.fecho{stroke-width:3.2}
.fita-branca-base{fill:none;stroke:var(--tinta);stroke-width:3.6}
.fita-branca{fill:none;stroke:#ffffff;stroke-width:1.8}
.tique{fill:none;stroke:var(--suave);stroke-width:1}
.zebra-base{fill:none;stroke:var(--tinta);stroke-width:3.6}
.zebra{fill:none;stroke:#ffffff;stroke-width:3.6;stroke-dasharray:2.2 2.2}
.galao{fill:none;stroke-width:1.8;stroke-linejoin:miter}
.galao-saida{fill:none;stroke:var(--suave);stroke-width:1.5}
.cinta-base{fill:none;stroke:var(--tinta);stroke-width:4.6;stroke-linejoin:round;stroke-linecap:round}
.cinta{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.cA{stroke:var(--zA)} .cB{stroke:var(--zB)} .cC{stroke:var(--zC)} .cR{stroke:var(--alerta)}
.poste{fill:var(--tinta)}
.xb{stroke:var(--tinta);stroke-width:.9}
.xb.zA,.pull.zA,.vinil.zA{fill:var(--zA)} .xb.zB,.pull.zB,.vinil.zB{fill:var(--zB)} .xb.zC,.pull.zC,.vinil.zC{fill:var(--zC)} .vinil.zP{fill:var(--zP)}
.pull{stroke:var(--tinta);stroke-width:1.2}
.vinil{stroke:var(--tinta);stroke-width:.8}
.lbl-vinil{font-size:10px;font-weight:800}
.lbl-xb{font-size:9px;font-weight:700;fill:var(--tinta)}
.correx{fill:var(--tinta)}
.rota{fill:none;stroke-width:2.6;stroke-dasharray:6 3}
.rA{stroke:var(--zA)} .rB{stroke:#b8930e} .rC{stroke:var(--zC)} .rP{stroke:var(--zP)} .rS{stroke:var(--suave)}
.alvo{fill:none;stroke-width:2}
.arrowhead{fill:var(--tinta)}
.conflito{fill:var(--alerta);opacity:.55}
.lbl-conf{font-size:10px;font-weight:700;fill:var(--alerta)}
.corredor{fill:var(--zB);opacity:.22}
.ghost{opacity:.3;filter:grayscale(1)}
.cota{fill:none;stroke:var(--suave);stroke-width:1}
.lbl-cota{font-size:11px;fill:var(--tinta);font-family:var(--f-dado)!important}
.lbl-av{font-size:12px;font-weight:700;fill:var(--suave);letter-spacing:.06em}
.parede-det{fill:var(--parede)}
.avenida-det{fill:var(--papel);stroke:var(--linha)}
.papel{fill:var(--folha);stroke:var(--tinta);stroke-width:.8}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

LEGENDA_PLANTA = """
<div class="legenda">
 <span><i style="background:var(--zA)"></i>zona A · azul</span>
 <span><i style="background:var(--zB)"></i>zona B · amarelo</span>
 <span><i style="background:var(--zC)"></i>zona C · laranja</span>
 <span><i style="background:var(--zP)"></i>preferencial · verde</span>
 <span><i style="background:repeating-linear-gradient(90deg,var(--tinta) 0 3px,#fff 3px 6px);border:1px solid var(--tinta)"></i>linha de espera · zebrado</span>
 <span><i style="background:var(--alerta)"></i>zona protegida · não ocupar</span>
</div>"""


def passos(eid, itens):
    lis = []
    for i, t in enumerate(itens, 1):
        lis.append(f'<li><label for="{eid}-{i}"><input type="checkbox" id="{eid}-{i}">'
                   f'<span>{t}</span></label></li>')
    return '<ol class="passos">' + "".join(lis) + "</ol>"


def etapa(num, titulo, hora, equipe, objetivo, itens, pronto, figura, legenda,
          cuidado=None, parada=None):
    cuid = f'<div class="cuidado"><b>Atenção.</b> {cuidado}</div>' if cuidado else ""
    par = f'<span class="parada">Ponto de parada · {parada}</span>' if parada else ""
    return f"""
<section class="etapa" id="etapa-{num}">
 <div class="texto">
  <div class="etapa-cab"><span class="num">{num}</span><div><h2>{titulo}</h2>
   <div class="hora">{hora} · {equipe}</div></div></div>
  <p>{objetivo}</p>
  {passos(f"e{num}", itens)}
  {cuid}
  <div class="pronto"><b>Pronto quando:</b> {pronto}</div>
  {par}
 </div>
 <figure class="fig">
  <div class="fig-scroll">{figura}</div>
  <figcaption>{legenda}</figcaption>
 </figure>
</section>"""


def pagina(planta, dec, mesas, grupos):
    fig = {f: planta_etapa(f"e{f}", f, planta, dec, mesas, grupos) for f in (1, 2, 3, 5, 6, 7, 8)}
    final = planta_etapa("final", 0, planta, dec, mesas, grupos)
    n_post = resumo_material(dec)
    ret = sf.RETOQUE

    etapas = []
    etapas.append(etapa(
        1, "Reconhecer e liberar o salão", "08h00–08h30", "coordenação + 2",
        "Conferir que o salão está vazio, limpo e igual à planta antes de medir qualquer coisa. "
        "As zonas protegidas são marcadas primeiro: tudo o que vier depois as contorna.",
        ["Percorrer o salão com o responsável do RDS. Fotografar piso e paredes nas quatro "
         "direções: é o registro do estado inicial para a devolução.",
         "O RDS já autorizou a fita no piso. Combinar com o responsável do dia quem remove "
         "a fita depois da votação e em que prazo.",
         "Testar as portas: <b>S4, S5, S6</b> (entradas), <b>S7</b> (preferencial), "
         "<b>S2, S8</b> (saídas), <b>L1–L4</b> (emergência). <b>O1</b> e <b>N1</b> ficam fechadas.",
         "Conferir duas medidas gerais com trena: largura do salão na fachada sul "
         "(50,30 m) e profundidade na parede oeste (44,40 m). Diferença acima de 10 cm: avisar "
         "a coordenação antes de marcar.",
         "Marcar com fita crepe um X nos cantos de cada zona protegida: faixa leste de 3,00 m "
         "(L1–L4), recuos de S3, S7, R1, O2 e N2.",
         "Varrer e secar o piso nas faixas que vão receber fita (avenidas e bandas). "
         "Fita em piso com pó solta antes do meio-dia."],
        "as zonas protegidas estão visíveis no chão e a remoção da fita está combinada com o RDS.",
        fig[1], "Etapa 1 · zonas protegidas em destaque. Nada é colocado, apoiado ou "
        "estocado nelas durante a montagem, nem caixas vazias.",
        cuidado="a faixa de 3,00 m da fachada leste é a rota das quatro saídas de emergência. "
        "Não serve de depósito nem por uma hora."))

    etapas.append(etapa(
        2, "Marcar as referências no chão", "08h30–09h45", "2 duplas com trena",
        "Antes de mover mobília, os pontos que definem o desenho vão para o chão em fita crepe. "
        "Cada dupla mede a partir de uma referência física (batente de porta ou parede), "
        "nunca encadeando uma medida na anterior.",
        ["Marcar a <b>linha das mesas leste</b> em x = 47,30 m (3,00 m da fachada leste) com fita "
         "crepe contínua. É a única linha que não admite tolerância para dentro da faixa.",
         "Marcar o <b>eixo de cada mesa</b> na base da parede (oeste e norte) ou na linha 47,30 "
         "(leste), com a seção escrita na crepe. Tabela no anexo A.",
         "Marcar a <b>frente do módulo</b> em cada eixo: 4,10 m da parede oeste (x 4,10), "
         "da parede norte (y 40,30) e da linha leste (x 43,20).",
         "Marcar os <b>24 piquetes</b> das avenidas e do corredor nordeste (tabela ao lado). "
         "As avenidas se medem a partir dos batentes das portas S4, S5 e S6.",
         "Conferir os vértices em ângulo reto pela diagonal: num retângulo de 3 × 4 m a diagonal "
         "tem 5,00 m.",
         "Conferência cruzada: a outra dupla remede cinco piquetes escolhidos pela coordenação."],
        "os 28 eixos, as três linhas de frente e os 24 piquetes estão no chão e cinco deles "
        "foram remedidos por outra dupla com diferença de até 5 cm.",
        fig[2] + '<div class="tabwrap">' + tabela_controle() + "</div>",
        "Etapa 2 · em vermelho, os piquetes de fita crepe. Tracejado: linhas de giz ou crepe "
        "para eixos e frentes de módulo.",
        parada="coordenação confere os piquetes antes de entrar mobília"))

    etapas.append(etapa(
        3, "Posicionar mesas, cabines e urnas por pares", "09h45–11h30",
        "3 equipes, uma por parede",
        "As 28 mesas vão para os eixos marcados, uma parede por equipe. A mobília entra antes "
        "da fita porque mesa arrastada sobre fita nova arranca a fita.",
        ["Trazer a mobília pela porta da própria zona: oeste por S4, norte por S5, leste por "
         "S6. Ninguém atravessa a faixa leste carregando mesa.",
         "Montar cada <b>módulo</b> encostado na parede (na leste, encostado na linha 47,30): "
         "0,90 m de largura no eixo, 4,10 m de profundidade.",
         "Montar <b>par por par</b>: as duas mesas de um grupo ficam a 3,90 m de eixo a eixo, "
         "com 3,00 m livres entre elas. Esse corredor recebe o x-banner na etapa 7.",
         "Entre um par e o seguinte, 2,40 m de eixo a eixo (1,50 m livres). Os vãos maiores "
         "são de propósito: O2 na oeste, N2 na norte e as mesas vermelhas.",
         "As três mesas vermelhas (<b>A3</b> 3313·3889, <b>B2</b> 3315·3778, <b>C5</b> "
         "3322·3752) ficam isoladas, com o retângulo do serpenteado livre à frente.",
         "Etiquetar cada mesa no verso, para a equipe, com as <b>seções</b>. Número de mesa "
         "não aparece em nada que o eleitor veja.",
         "Cabos de energia: correr junto à parede, atrás dos módulos, e cobrir com "
         "passa-cabo onde cruzarem passagem. Nenhum cabo atravessa avenida ou faixa leste.",
         "Urnas: seguir o protocolo do Cartório para guarda e instalação. Se só forem "
         "instaladas no dia 25, deixar o lugar delas marcado no módulo."],
        "as 28 mesas estão nos eixos, pares e vãos batem com a tabela e nenhum objeto "
        "está nas zonas protegidas.",
        fig[3] + detalhe_par(),
        "Etapa 3 · módulos por zona, rotulados por grupo. Contorno vermelho: as três mesas "
        "vermelhas. Abaixo, o par em escala: módulo, sigilo, canal e x-banner.",
        cuidado="a equipe da parede leste trabalha com as costas para a faixa de emergência. "
        "Cadeiras e caixas de material ficam do lado do salão, nunca atrás das mesas."))

    etapas.append(f"""
<section class="etapa" id="etapa-4">
 <div class="texto">
  <div class="etapa-cab"><span class="num">4</span><div><h2>Conferir mesas e distâncias</h2>
   <div class="hora">11h30–12h00 · coordenação + 1 dupla</div></div></div>
  <p>É a sua etapa 1, no lugar em que ela funciona: depois das mesas no chão e antes de
   qualquer fita. Corrigir uma mesa agora custa minutos. Depois da fita, custa rolos.</p>
  {passos("e4", [
      "Faixa leste: de x 47,30 a 50,30 livre em todo o comprimento. Medir em cinco pontos.",
      "Eixos: cada mesa no seu eixo da tabela, com até 5 cm de diferença.",
      "Profundidade: frente de cada módulo a 4,10 m da parede (ou da linha leste), com até 5 cm.",
      "Pares: 3,90 m de eixo a eixo dentro do par, 2,40 m entre pares. Conferir com a coluna "
      "<i>até o eixo anterior</i> do anexo A.",
      "Alinhamento: as frentes de uma parede formam uma reta. Esticar linha de giz de ponta a "
      "ponta e ver se algum módulo avança ou recua.",
      "Recuos: O2 (y 19,36–22,43 na oeste), N2 (x 20,66–24,22 na norte), R1, S3 e S7 vazios.",
      "Serpenteados: retângulos livres à frente de A3, B2 e C5 (4,20 × 2,80 m), encostados no módulo (D4).",
      "Conferir que os piquetes de D1 (fim das avenidas A e C, corredor nordeste) estão no chão."])}
  <div class="pronto"><b>Pronto quando:</b> o coordenador assinou a conferência. Só então a
   fita começa.</div>
  <span class="parada">Ponto de parada · nenhuma fita antes da assinatura</span>
 </div>
 <div class="fig">
  <div class="tabwrap">{tabela_mesas(mesas, grupos)}</div>
  <figcaption>Anexo A · as 28 mesas por parede. "Medida na parede" é a trena a partir da
   referência indicada na linha da zona. Nenhuma coluna traz número de mesa.</figcaption>
 </div>
</section>""")

    decisoes = f"""
<section class="bloco" id="decisoes">
 <div class="eyebrow">Aprovados em 23/10 · valem para esta montagem</div>
 <h2>Quatro ajustes de chão</h2>
 <p>Desenhar o chão trecho a trecho mostrou quatro pontos em que o desenho de 17/09 põe duas
  fitas no mesmo lugar. A conferência automática do desenho só prova que as três avenidas não se
  cruzam entre si, e por isso não os pegou. Os quatro ajustes abaixo foram aprovados pelo Posto
  em 23/10 e <b>valem no lugar do desenho de 17/09</b> nesses pontos. As figuras e as medidas
  desta página já os aplicam.</p>
 <div class="decisoes">
  <div class="decisao"><h3>D1 · Os cantos norte</h3>
   <p>No desenho, a avenida C sobe até y 39,50 e passa por cima do canal da segunda mesa de
    <b>B4</b> (0518·3306). O canal da segunda mesa de <b>C6</b> (0511·1100) cruza os dois
    canais de <b>B5</b>. São cerca de 1.100 eleitores de B (B4-2 e B5) sem caminho que não
    atravesse a avenida C.</p>
   <p><b>Aprovado:</b> a avenida C acaba em y 36,20 e é fechada ali com fita laranja. Os
    eleitores de B4-2, B5-1 e B5-2 sobem pelo vão entre B4-1 e a avenida C (x 32,1–33,5) e
    seguem pelo <b>corredor nordeste</b>, faixa livre de y 36,20 a 37,40. Os três canais
    passam a começar em 37,40 (1,40 m, duas pessoas). No noroeste, a avenida A acaba em
    36,70 e o canal da primeira mesa de B1 (0512·2855) começa em 37,40.</p></div>
  <div class="decisao"><h3>D2 · O canal verde da S7</h3>
   <p>O canal da preferencial tem 10 m no desenho e corta os canais de <b>C1</b> (3442) e
    <b>C2</b> (3688). <b>Aprovado:</b> 6,00 m de verde, que terminam antes do canal de C1
    (y 6,60). Gasta 8 m de verde a menos.</p></div>
  <div class="decisao"><h3>D3 · As guias brancas de S2 e S8</h3>
   <p>As guias de 8 m cortam a avenida A (S2) e o canal, o sigilo e o módulo de C1 (S8).
    <b>Aprovado:</b> 3,00 m de cada lado da porta. O "trilho sul da perna A" do desenho
    repete o trilho interno da avenida A e, levado até x 25,03, fecharia a boca da A:
    <b>não colar</b>.</p></div>
  <div class="decisao"><h3>D4 · Os serpenteados e o sigilo</h3>
   <p>Os serpenteados de A3, B2 e C5 começam colados no módulo (4,10 m), sem os 1,50 m da
    linha de espera que as outras 25 mesas têm. <b>Aprovado: manter o desenho.</b> O zebrado
    vai na saída do serpenteado, junto ao módulo. Se no dia houver queixa de sigilo, o
    serpenteado de A3 ou de C5 pode recuar 1,50 m (cabe na oeste e na leste); o de B2 não
    tem esse espaço.</p></div>
 </div>
 <div class="duas">
  <figure class="fig"><div class="fig-scroll">{planta_nordeste(planta, dec, mesas, False)}</div>
   <figcaption>Canto nordeste no desenho de 17/09. Em vermelho, onde dois canais, ou um canal
    e a avenida C, ocupam o mesmo chão.</figcaption></figure>
  <figure class="fig"><div class="fig-scroll">{planta_nordeste(planta, dec, mesas, True)}</div>
   <figcaption>Com D1: a avenida C fecha em 36,20 e B ganha o corredor nordeste (em amarelo
    claro), com galões apontando para leste.</figcaption></figure>
 </div>
</section>"""

    etapas.append(decisoes)

    etapas.append(etapa(
        5, "Colar a fita no chão", "12h45–16h15", "4 duplas: azul, amarela, laranja, neutra",
        "Com as mesas no lugar e conferidas, a fita vai do fundo do salão para as portas, para que "
        "ninguém pise em fita recém-colada. Uma dupla por cor: ninguém troca de rolo no meio.",
        ["<b>5a · Avenidas.</b> Azul (A) e laranja (C) entre os piquetes, com as linhas do lado "
         "das mesas abertas em 1,10 m na boca de cada canal. Colar também os fechos: A em 36,70 e "
         "C em 36,20 (D1). A avenida B não leva linha: a barreira inteira faz esse papel.",
         "<b>5b · Distribuidor norte.</b> Amarelo em y 35,40, só entre as avenidas A e C, "
         "aberto na boca de cada canal norte; e a borda do corredor nordeste em y 37,40 (D1).",
         "<b>5c · Canais.</b> Duas linhas a 1,10 m, na cor da zona, da linha de espera até a "
         "boca. Oeste 5,60 → 11,00; leste 41,70 → 36,50; norte 38,80 → 35,40 (ou 37,40 nos "
         "quatro canais curtos). Nas vermelhas, prolongar as cintas externas do serpenteado em "
         "fita até a avenida.",
         "<b>5d · Linha de espera.</b> Zebrado preto-e-branco, 1,10 m, atravessando cada canal "
         "a 1,50 m da mesa. Nunca amarelo, que é a cor da zona B.",
         "<b>5e · Marcas de fila.</b> Tique de 25 cm a cada 0,65 m dentro do canal, a partir da "
         "linha de espera: oito marcas na oeste, sete na leste, cinco na norte.",
         "<b>5f · Galões.</b> Um a cada 5 m no eixo de cada avenida, apontando para dentro. "
         "Galões amarelos no corredor nordeste, apontando para leste.",
         "<b>5g · Verde e branco.</b> Canal da S7 em verde, 6,00 m (D2). Guias de S2 e S8 em "
         "branco, 3,00 m (D3). Galões brancos de saída ao longo das bandas: "
         "B1 a B3-1 e toda a zona A saem por S2; B3-2 a B5 e toda a zona C saem por S8.",
         "Assentar cada trecho com pressão (rolo ou pano), sobretudo nas pontas e nas "
         "emendas. Ponta solta é onde a fita começa a sair.",
         "Guardar sobras por cor na sala de apoio, etiquetadas, para o retoque do meio-dia "
         f"do dia 25 (margem de {ret:.0%} no orçamento de fita)."],
        "todas as linhas estão coladas e assentadas, as bocas dos canais estão abertas na "
        "largura certa e ninguém precisa pisar em fita para chegar a uma mesa.",
        fig[5],
        "Etapa 5 · a fita sobre as mesas já conferidas. Linhas na cor da zona; zebrado nas "
        "linhas de espera; cinza, os galões brancos de saída.",
        cuidado="a avenida A tem só 36 cm de folga entre o trilho interno (x 21,83) e o recuo "
        "S3 (até 21,47). Colar essa linha conferindo o piquete A1 duas vezes."))

    etapas.append(etapa(
        6, "Montar as barreiras", "16h15–17h00", "2 duplas",
        f"As {n_post} unifilas vão onde a fita não segura: as bocas das portas, a avenida B "
        "inteira e os três serpenteados. Barreira depois da fita, porque o poste fica sobre a "
        "linha e a cinta precisa da linha para alinhar.",
        ["<b>Boca A</b>: 6 m de cada trilho a partir de S4, 5 postes em cada. O trilho interno "
         "sobe 3,40 m e vira para oeste.",
         "<b>Boca C</b>: 6 m de cada trilho a partir de S6, 5 postes em cada.",
         "<b>Avenida B</b>: os dois trilhos inteiros, de S5 até o distribuidor (35,40 m), "
         "21 postes em cada.",
         "<b>Serpenteados</b> de A3, B2 e C5: 3 cintas de 4,20 m a 1,40 m de distância, "
         "12 postes em cada.",
         "Postes a 1,80 m: a cinta de 2,00 m só fica esticada assim. Cinta frouxa vira "
         "obstáculo de tropeço.",
         "<b>Vãos de serviço na avenida B</b>: em cada trilho, marcar com fita verde no poste "
         "duas cintas (perto de y 12 e y 24) que a equipe solta para atravessar com um eleitor "
         "preferencial ou numa evacuação. Sem isso, a avenida B é um muro de 35 m.",
         "Guardar a reserva (2 unifilas, mais as 15 adicionais se chegaram) montada e "
         "encostada na sala de apoio.",
         "Mostrar o leiaute final de barreira ao responsável de incêndio do RDS."],
        "nenhuma cinta está frouxa, nenhum poste está em zona protegida e o RDS viu o "
        "leiaute de barreira.",
        fig[6] + planta_bocas(planta, dec, mesas, grupos),
        "Etapa 6 · barreiras com os postes. Abaixo, a fachada sul ampliada: bocas A e C, "
        "avenida B, verde da S7 e guias brancas.",
        parada="responsável de incêndio do RDS vê a barreira"))

    etapas.append(etapa(
        7, "Sinalização: portas, painéis e banners", "17h00–18h00", "2 duplas",
        "A sinalização entra por último porque é a peça mais leve e a que depende da posição "
        "final dos canais. Cada peça diz seções e grupos, nunca número de mesa.",
        ["<b>Vinis</b> A, B e C na face externa do vidro de S4, S5 e S6, letra de 300 mm. "
         "Vinil da preferencial na S7.",
         "<b>Painéis de porta</b> (pull-up 1000 × 2000) no vão entre as barreiras, a cerca de "
         "3 m da porta e do lado oposto à curva: painel A entre as avenidas A e B, de frente "
         "para a A; painel B entre B e C, de frente para a B; painel C a oeste da avenida C, "
         "de frente para ela.",
         "<b>X-banners de grupo</b> (16, 600 × 1600): na boca do corredor de cada par, a "
         "4,60 m da linha das mesas. Nas três vermelhas, a 8,60 m, logo atrás do serpenteado. "
         "C1 fica no vão entre C1 e C2. Posições no anexo B.",
         "Conferir cada banner contra as seções do par à sua frente. É o erro mais caro do dia: "
         "um banner trocado manda o eleitor para a fila errada.",
         "<b>Papel da seção</b>, plastificado, na borda de cada canal, fora da linha de "
         "pisada. Confirma a seção para quem já está no canal.",
         "<b>Correx de saída</b> sobre S2 e S8, pelo lado de dentro."],
        "as 16 + 3 + 4 + 2 peças estão no lugar e cada banner foi conferido contra a mesa "
        "por alguém que não o colocou.",
        fig[7] + '<div class="tabwrap">' + tabela_banners(grupos) + "</div>",
        "Etapa 7 · painéis de porta (PA, PB, PC), x-banners por grupo, vinis nas portas e "
        "correx nas saídas. Anexo B: onde fica cada x-banner.",
        cuidado="os papéis da seção vão na borda do canal. No meio do canal eles somem sob os "
        "pés antes do meio-dia."))

    etapas.append(etapa(
        8, "Testar andando", "18h00–18h45", "4 pessoas que não montaram a zona",
        "Quatro pessoas fazem o caminho de um eleitor com um cartão de seção na mão, cada uma "
        "por uma porta, sem ajuda da equipe que montou aquela zona.",
        ["<b>Seção 3313</b>: entra por S4, segue a azul até o serpenteado de A3, sai pela "
         "banda oeste até S2.",
         "<b>Seção 3832</b>: entra por S5, sobe a avenida B, vira no distribuidor, passa pelo "
         "corredor nordeste até B5 e sai por S8. Testa a decisão D1.",
         "<b>Seção 3442</b>: entra por S6 até C1, a mesa mais perto das portas, e sai por S8. "
         "Testa as decisões D2 e D3.",
         "<b>Preferencial, seção 0519</b>: entra por S7, segue o verde até C3.",
         "Cada pessoa anota onde hesitou, onde pisou em fita e onde precisou perguntar. "
         "Corrigir na hora o que for fita ou banner.",
         "Andar a faixa leste de L4 a L1 e abrir as quatro portas de emergência.",
         "Fotografar cada parede de frente e as três bocas para o registro do 2º turno."],
        "os quatro chegaram à mesa certa sem perguntar e sem pular fita, e as quatro "
        "saídas de emergência abrem.",
        fig[8],
        "Etapa 8 · as quatro rotas de teste (ida em cor, volta em cinza). O círculo marca a "
        "mesa de destino.",
        parada="aceite final da coordenação"))

    agenda = [
        ("antes", "0", "Preparar material e equipes", "coordenação"),
        ("08h00–08h30", "1", "Reconhecer e liberar o salão", "coord. + 2"),
        ("08h30–09h45", "2", "Marcar as referências no chão", "2 duplas"),
        ("09h45–11h30", "3", "Mesas, cabines e urnas por pares", "3 equipes"),
        ("11h30–12h00", "4", "Conferir mesas e decidir D1–D4", "coord. + 1 dupla"),
        ("12h00–12h45", "", "Almoço", ""),
        ("12h45–16h15", "5", "Colar a fita no chão", "4 duplas"),
        ("16h15–17h00", "6", "Montar as barreiras", "2 duplas"),
        ("17h00–18h00", "7", "Sinalização", "2 duplas"),
        ("18h00–18h45", "8", "Testar andando", "4 pessoas"),
        ("18h45–19h15", "", "Fechar: sobras, reserva, fotos, chaves", "coordenação"),
    ]
    agenda_html = "".join(
        f'<div><span class="t">{t}</span><span class="e">{e}</span><span>{d}</span>'
        f'<span class="q">{q}</span></div>' for t, e, d, q in agenda)

    material = """
<table class="dados"><thead><tr><th>Item</th><th>Quantidade</th><th>Usado em</th></tr></thead><tbody>
<tr><td>Fita crepe e marcador permanente</td><td class="n">4 rolos</td><td>etapa 2 · piquetes e eixos</td></tr>
<tr><td>Trenas de 30 a 50 m</td><td class="n">2 (+1 laser)</td><td>etapas 1, 2, 4</td></tr>
<tr><td>Linha de giz</td><td class="n">2</td><td>etapas 2 e 4 · alinhamento das frentes</td></tr>
{FITA_LINHAS}<tr><td>Unifilas (Tensa, cinta de 2 m)</td><td class="n">98 + reserva</td><td>etapa 6</td></tr>
<tr><td>Pull-ups de porta · X-banners · vinis · correx</td><td class="n">3 · 16 · 4 · 2</td><td>etapa 7</td></tr>
<tr><td>Papéis de seção plastificados</td><td class="n">28</td><td>etapa 7 · borda dos canais</td></tr>
<tr><td>Passa-cabos, extensões, abraçadeiras</td><td class="n">conforme o eletricista</td><td>etapa 3</td></tr>
<tr><td>Pano, vassoura, rolo para assentar fita</td><td class="n">2 kits</td><td>etapas 1 e 5</td></tr>
<tr><td>Esta folha impressa em A3, uma por equipe</td><td class="n">6</td><td>todas</td></tr>
</tbody></table>"""
    material = material.replace("{FITA_LINHAS}", linhas_fita(mesas, dec))

    corpo = f"""
<title>Montagem do Hall 2</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{CSS}</style>
<main>
<header>
 <div class="eyebrow">Eleições 2026 · Posto de Dublin · RDS Ballsbridge</div>
 <h1>Montagem do Hall 2 · véspera do 2º turno</h1>
 <div class="zebra-faixa" aria-hidden="true"></div>
 <p class="lead">Sábado, 24/10/2026. Oito etapas para deixar o salão pronto para a votação
  de domingo, das portas S4, S5 e S6 até as 28 mesas. Cada etapa tem uma planta em escala: o que
  já deveria estar pronto aparece em cinza, o que entra agora aparece em cor.</p>
 <div class="chips"><span class="chip">28 mesas · 16 grupos · 51 seções</span>
  <span class="chip">11.499 eleitores esperados</span><span class="chip">{n_post} unifilas</span>
  <span class="chip">≈ {total_fita(mesas, dec):.0f} m de fita em 6 cores</span><span class="chip">salão 50,30 × 44,40 m</span></div>
</header>

<section class="bloco">
 <div class="eyebrow">A lógica da sequência</div>
 <h2>Medir, mobiliar, conferir, colar, barrar, sinalizar, testar</h2>
 <ul class="regras">
  <li><b>Medir antes de mover</b>Os pontos vão para o chão antes da mobília. Mesa posta a olho
   leva o erro para a fita, a barreira e o banner.</li>
  <li><b>Arrastar antes de colar</b>Mesa arrastada sobre fita nova arranca a fita. Tudo o que é
   pesado entra antes.</li>
  <li><b>Fixo antes do móvel</b>Fita colada não se move. Barreira e banner se movem, e se apoiam
   na fita para alinhar.</li>
  <li><b>Conferir antes de colar</b>Uma parada formal entre as mesas e a fita. Errar a mesa ali
   custa minutos; depois custa rolos.</li>
  <li><b>Testar andando</b>Um caminho que funciona no papel pode falhar no chão. Quem não montou
   a zona é quem a testa.</li>
 </ul>
 <div class="nota"><b>Sobre a sua proposta.</b> A conferência de mesas e distâncias está certa e
  virou a etapa 4, mas ela pressupõe mesas já no chão e pontos de referência contra os quais
  conferir: por isso vêm antes a marcação (2) e o posicionamento por pares (3). Os banners
  passaram para depois da fita e das barreiras. As bases ficam exatamente onde a fita passa (boca
  do corredor, borda do canal), atrapalham quem cola, e a posição certa de cada uma só existe
  depois que os canais estão no chão.</div>
</section>

<section class="duas">
 <div class="bloco">
  <div class="eyebrow">Ordem do dia</div>
  <h2>Horário de referência</h2>
  <div class="agenda">{agenda_html}</div>
  <p class="hora">Premissas, a substituir pelo que valeu no 1º turno: acesso ao salão das 8h às
   19h30, equipe de 9 pessoas (coordenação + 8), cerca de 80 m de fita por dupla por hora com os
   piquetes já marcados.</p>
 </div>
 <div class="bloco">
  <div class="eyebrow">Etapa 0 · antes de entrar</div>
  <h2>Material e equipes</h2>
  <div class="tabwrap">{material}</div>
  <p class="hora">Metragem de fita: medida trecho a trecho no traçado desta página (com D1–D4),
   mais {ret:.0%} de retoque, em rolos de 50 m. É menor que a conta de 17/09, que media os canais
   a partir do módulo e incluía trechos que D2 e D3 cortaram. Detalhe por trecho na prancha A3.</p>
 </div>
</section>

<section class="bloco">
 <div class="eyebrow">Onde se quer chegar</div>
 <h2>O salão montado</h2>
 <div class="fig-scroll">{final}</div>
 {LEGENDA_PLANTA}
 <p class="hora">Zona do Ring 3 → porta → parede, a mesma letra em toda a rota: A entra por S4
  e vai à parede oeste, B por S5 à norte, C por S6 à leste. As avenidas levam para dentro; as
  bandas trazem para fora, até S2 e S8. O Ring 3 e o apron têm folha própria
  (<code>mapa/ring3_montagem.html</code>).</p>
</section>

<div class="barra-acoes"><button type="button" id="limpar">Desmarcar todos os passos</button>
 <span class="hora" id="estado">As marcações ficam salvas só neste aparelho.</span></div>

{"".join(etapas)}

<section class="bloco">
 <div class="eyebrow">Fontes</div>
 <p class="hora">Geometria: <code>data/prancheta_hall2.json</code>, cenário Paredes_ABC
  (<code>cenarios/paredes-abc-20260915.json</code>), <code>data/decisoes.json</code>,
  <code>data/grupos_mesas.json</code>; traçado do desenho definitivo de 17/09
  (<code>scripts/separadores_fila.py</code>); peças e cores da sinalização v2 de 17/09. Gerado por
  <code>scripts/montagem_hall2.py</code>, que lê esses arquivos e não escreve em nenhum deles.
  Os horários e o tamanho da equipe são premissas.</p>
</section>
</main>
<script>
(function(){{
  var K="montagem-hall2-passos";
  var caixas=[].slice.call(document.querySelectorAll('ol.passos input'));
  var salvo={{}};
  try{{salvo=JSON.parse(localStorage.getItem(K)||"{{}}")||{{}};}}catch(e){{salvo={{}};}}
  caixas.forEach(function(c){{
    if(salvo[c.id]) c.checked=true;
    c.addEventListener('change',function(){{
      salvo[c.id]=c.checked;
      try{{localStorage.setItem(K,JSON.stringify(salvo));}}catch(e){{}}
    }});
  }});
  document.getElementById('limpar').addEventListener('click',function(){{
    caixas.forEach(function(c){{c.checked=false;}});
    salvo={{}};
    try{{localStorage.removeItem(K);}}catch(e){{}}
    document.getElementById('estado').textContent='Todos os passos desmarcados.';
  }});
}})();
</script>
"""
    return corpo


def main():
    planta, dec, mesas, grupos = carrega()
    html_ = pagina(planta, dec, mesas, grupos)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(html_)
    print("escrito", os.path.relpath(SAIDA, RAIZ), f"({len(html_) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
