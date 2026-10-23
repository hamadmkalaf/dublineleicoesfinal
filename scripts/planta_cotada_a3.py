"""Prancha A3 da montagem final do Hall 2, cotada, com a fita por trecho.

Gera ``saidas/montagem_hall2_A3.svg``, em milimetros de papel (420 x 297), pronto
para converter em PDF A3 paisagem. A geometria e a de ``montagem_hall2.py`` -- o desenho definitivo de
17/09 com os ajustes D1-D4 aprovados em 23/10 -- e os desenhos reaproveitam as
mesmas funcoes; so a escala (milimetros de papel por metro de salao) e o estilo
de impressao mudam aqui.

    python3 scripts/planta_cotada_a3.py
"""
import html
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montagem_hall2 as mh  # noqa: E402
import separadores_fila as sf  # noqa: E402

RAIZ = sf.RAIZ
BASE = os.path.join(RAIZ, "saidas", "montagem_hall2_A3")

ESCALA = 190                 # 1:190 -- o salao (50,30 x 44,40 m) cabe com as cotas
K = 1000.0 / ESCALA          # mm de papel por metro
OX, OY = 24.0, 33.0          # canto noroeste do salao na folha, em mm
LARG, ALT = 50.30, 44.40

COR = {"A": "#33507E", "B": "#E8C63A", "C": "#DE7343", "P": "#1e8449",
       "tinta": "#16202b", "cinza": "#5b6672", "claro": "#c7ced6", "alerta": "#b8321f"}

CSS = """
text{font-family:'DejaVu Sans','Liberation Sans',sans-serif;fill:#16202b}
.piso{fill:#ffffff;stroke:none}
.parede{fill:none;stroke:#16202b;stroke-width:.9;stroke-linejoin:round}
.prot{stroke:#b8321f;stroke-width:.2;stroke-dasharray:.8 .5;opacity:.7}
.hatch{stroke:#b8321f;stroke-width:.35;opacity:.45}
.apoio{fill:#eef1f4;stroke:#c7ced6;stroke-width:.2}
.porta{fill:none;stroke-width:1.6}
.porta.entradaA{stroke:#33507E}.porta.entradaB{stroke:#E8C63A}.porta.entradaC{stroke:#DE7343}
.porta.saida{stroke:#16202b}.porta.emergencia{stroke:#b8321f}.porta.preferencial{stroke:#1e8449}
.porta.fechada,.porta.livre{stroke:#a9b2bc}
.lbl-porta{font-size:2.3px;font-weight:700}
.lbl-s{font-size:1.9px;fill:#5b6672}
.escala{fill:none;stroke:#16202b;stroke-width:.3}
.mod{stroke:#16202b;stroke-width:.15}
.mod.zA{fill:#33507E}.mod.zB{fill:#E8C63A}.mod.zC{fill:#DE7343}
.mod.alta{stroke:#b8321f;stroke-width:.5}
.lbl-mod{font-size:1.9px;font-weight:700}
.tA{fill:#fff}.tB{fill:#16202b}.tC{fill:#16202b}.tP{fill:#fff}
.fita{fill:none;stroke-width:.55}
.fA{stroke:#33507E}.fB{stroke:#d1ad1c}.fC{stroke:#DE7343}.fP{stroke:#1e8449}
.fita.fecho{stroke-width:.8}
.fita-branca-base{fill:none;stroke:#16202b;stroke-width:.85}
.fita-branca{fill:none;stroke:#fff;stroke-width:.4}
.tique{fill:none;stroke:#5b6672;stroke-width:.2}
.zebra-base{fill:none;stroke:#16202b;stroke-width:.9}
.zebra{fill:none;stroke:#fff;stroke-width:.9;stroke-dasharray:.5 .5}
.galao{fill:none;stroke-width:.4}
.galao-saida{fill:none;stroke:#8a94a0;stroke-width:.35}
.cinta-base{fill:none;stroke:#16202b;stroke-width:1.1;stroke-linejoin:round;stroke-linecap:round}
.cinta{fill:none;stroke-width:.5;stroke-linejoin:round;stroke-linecap:round}
.cA{stroke:#33507E}.cB{stroke:#E8C63A}.cC{stroke:#DE7343}.cR{stroke:#b8321f}
.poste{fill:#16202b}
.xb{stroke:#16202b;stroke-width:.2}
.xb.zA,.pull.zA,.vinil.zA{fill:#33507E}.xb.zB,.pull.zB,.vinil.zB{fill:#E8C63A}
.xb.zC,.pull.zC,.vinil.zC{fill:#DE7343}.vinil.zP{fill:#1e8449}
.pull{stroke:#16202b;stroke-width:.25}.vinil{stroke:#16202b;stroke-width:.2}
.lbl-vinil{font-size:2.2px;font-weight:800}.lbl-xb{font-size:1.8px;font-weight:700}
.correx{fill:#16202b}
.cota{fill:none;stroke:#16202b;stroke-width:.18}
.ext{fill:none;stroke:#8a94a0;stroke-width:.12;stroke-dasharray:.6 .4}
.v{font-size:2.15px;font-weight:700}
.vl{font-size:1.65px;fill:#5b6672}
.halo{paint-order:stroke;stroke:#fff;stroke-width:.7px;stroke-linejoin:round}
.tag{fill:#16202b}.tagt{font-size:1.75px;font-weight:700;fill:#fff}
.h1{font-size:5.2px;font-weight:700}.h2{font-size:3.1px;font-weight:700}
.t{font-size:2.15px}.tb{font-size:2.15px;font-weight:700}.tm{font-size:1.85px;fill:#5b6672}
.lin{stroke:#c7ced6;stroke-width:.15}
"""


def br(v, nd=2):
    return f"{v:.{nd}f}".replace(".", ",")


def X(x):
    return OX + x * K


def Y(y):
    return OY + (ALT - y) * K


class Folha:
    def __init__(self):
        self.o = []

    def add(self, s):
        self.o.append(s)

    def ln(self, pts, cls):
        self.add(f'<polyline class="{cls}" points="' +
                 " ".join(f"{a:.2f},{b:.2f}" for a, b in pts) + '"/>')

    def tx(self, x, y, s, cls, anchor="middle", rot=0):
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        self.add(f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}"{tr}>'
                 f'{html.escape(s)}</text>')

    def rc(self, x, y, w, h, cls="", style=""):
        st = f' style="{style}"' if style else ""
        self.add(f'<rect class="{cls}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
                 f'height="{h:.2f}"{st}/>')


# --------------------------------------------------------------------------
# Cotas
# --------------------------------------------------------------------------
def cadeia_h(F, xs, ym, livre=None, ext_ate=None, acima=True, halo=False):
    """Cadeia de cotas horizontal na altura ym (mm), pelos x (m) dados."""
    F.ln([(X(xs[0]), ym), (X(xs[-1]), ym)], "cota")
    for x in xs:
        F.ln([(X(x) - .7, ym + .7), (X(x) + .7, ym - .7)], "cota")
        if ext_ate is not None:
            F.ln([(X(x), ym), (X(x), ext_ate)], "ext")
    for i, (a, b) in enumerate(zip(xs, xs[1:])):
        cx = (X(a) + X(b)) / 2
        dy = -0.9 if acima else 2.7
        F.tx(cx, ym + dy, br(b - a), "v" + (" halo" if halo else ""))
        if livre and livre[i]:
            F.tx(cx, ym + dy + (-2.1 if acima else 2.1), f"({livre[i]})",
                 "vl" + (" halo" if halo else ""))


def cadeia_v(F, ys, xm, livre=None, ext_ate=None, esquerda=True, halo=False):
    F.ln([(xm, Y(ys[0])), (xm, Y(ys[-1]))], "cota")
    for y in ys:
        F.ln([(xm - .7, Y(y) + .7), (xm + .7, Y(y) - .7)], "cota")
        if ext_ate is not None:
            F.ln([(xm, Y(y)), (ext_ate, Y(y))], "ext")
    for i, (a, b) in enumerate(zip(ys, ys[1:])):
        cy = (Y(a) + Y(b)) / 2
        anc = "end" if esquerda else "start"
        dx = -1.0 if esquerda else 1.0
        F.tx(xm + dx, cy + .2, br(b - a), "v" + (" halo" if halo else ""), anchor=anc)
        if livre and livre[i]:
            F.tx(xm + dx, cy + 2.2, f"({livre[i]})", "vl" + (" halo" if halo else ""),
                 anchor=anc)


def livres(eixos, ini_borda=True, fim_borda=True):
    """Espaco livre entre modulos (0,90 m de largura) para cada trecho."""
    out = []
    n = len(eixos)
    for i in range(n - 1):
        a, b = eixos[i], eixos[i + 1]
        first = i == 0 and ini_borda
        last = i == n - 2 and fim_borda
        if first:
            out.append(br(b - a - 0.45))
        elif last:
            out.append(br(b - a - 0.45))
        else:
            out.append(br(b - a - 0.90))
    return out


# --------------------------------------------------------------------------
# Fita por trecho
# --------------------------------------------------------------------------
def trechos(mesas, dec):
    """Agrupa a fita de ``fita_elementos`` em trechos nomeados, com metros."""
    grupos = {}

    def soma(cod, nome, cor, ps):
        g = grupos.setdefault(cod, {"nome": nome, "cor": cor, "m": 0.0, "pts": []})
        g["m"] += sf.comp(ps)
        g["pts"].append(ps)

    for cor, ps, tipo in mh.fita_elementos(mesas, dec):
        xs = {round(p[0], 2) for p in ps}
        ys = {round(p[1], 2) for p in ps}
        if tipo == "fecho":
            soma(f"{cor}-fecho", f"Fecho da avenida {cor}", cor, ps)
        elif tipo == "avenida" and cor == "A":
            if xs & {11.0, 21.83}:
                soma("T1", "Avenida A · linha do lado da parede", "A", ps)
            else:
                soma("T2", "Avenida A · linha do lado do campo", "A", ps)
        elif tipo == "avenida" and cor == "C":
            if xs & {32.0, 33.5}:
                soma("T4", "Avenida C · linha do lado do campo", "C", ps)
            else:
                soma("T5", "Avenida C · linha do lado da parede", "C", ps)
        elif tipo == "distribuidor":
            if ys == {37.4}:
                soma("T8", "Borda do corredor nordeste (y 37,40)", "B", ps)
            else:
                soma("T7", "Distribuidor norte (y 35,40)", "B", ps)
        elif tipo == "ramal":
            cod, nome = {"A": ("T9", "Canais da parede oeste"),
                         "B": ("T10", "Canais da parede norte"),
                         "C": ("T11", "Canais da parede leste")}[cor]
            soma(cod, nome, cor, ps)
        elif tipo == "preferencial":
            soma("T15", "Canal da preferencial S7 · 2 × 6,00", "P", ps)
        elif tipo == "saida":
            soma("T16", "Guias de S2 e S8 · 4 × 3,00", "S", ps)
    for cod, nome in (("A-fecho", "T3"), ("C-fecho", "T6")):
        if cod in grupos:
            grupos[nome] = grupos.pop(cod)
    # Sempre fita, fora do traçado: zebrado, marcas, galoes
    grupos["T12"] = {"nome": "Linhas de espera · 28 × 1,10", "cor": "Z",
                     "m": 28 * sf.LARG_CANAL, "pts": []}
    marcas = {"A": 0, "B": 0, "C": 0}
    for m in mesas:
        if m["classe"] == "alta":
            continue
        ini, esp = mh.ramal(m)
        n = sum(1 for i in range(1, 20)
                if abs(i * sf.PASSO_FILA) < abs(ini - esp) - 0.05)
        marcas[m["entrada"]] += n
    gal = {}
    for aid, ps in mh.eixos_avenida().items():
        gal[aid] = len(mh.pontos_ao_longo(ps, sf.PASSO_GALAO))
    gal["B"] += len(mh.pontos_ao_longo([(32.80, 36.80), (41.0, 36.80)], 2.6, ini=1.2))
    saida = sum(len(mh.pontos_ao_longo(r, 4.0, ini=1.5))
                for r in (mh.SAI_OESTE, mh.SAI_NOROESTE, mh.SAI_LESTE))
    for z in "ABC":
        grupos[f"T13{z}"] = {"nome": f"Marcas de fila (0,25 a cada 0,65) · {marcas[z]} un",
                             "cor": z, "m": marcas[z] * 0.25, "pts": []}
        grupos[f"T14{z}"] = {"nome": f"Galões no eixo · {gal[z]} un", "cor": z,
                             "m": gal[z] * sf.GALAO, "pts": []}
    grupos["T17"] = {"nome": f"Galões brancos de saída · {saida} un", "cor": "S",
                     "m": saida * sf.GALAO, "pts": []}
    return grupos


# Onde vai a etiqueta de cada trecho na planta (m), ao lado da linha.
TAGS = {"T1": (9.9, 26.0), "T2": (15.1, 26.0), "T3": (12.5, 37.5), "T4": (32.4, 26.0),
        "T5": (37.6, 24.1), "T6": (35.0, 35.4), "T7": (22.0, 34.6), "T8": (40.0, 38.15),
        "T9": (7.6, 13.2), "T10": (27.6, 37.6), "T11": (39.4, 12.4), "T15": (38.72, 3.8),
        "T16": (13.85, 4.1)}


def ancora(g):
    """Ponto (m) onde vai a etiqueta do trecho: meio do trecho mais longo."""
    if not g["pts"]:
        return None
    ps = max(g["pts"], key=sf.comp)
    L = sf.comp(ps)
    alvo, acum = L / 2, 0.0
    for a, b in zip(ps, ps[1:]):
        s = math.dist(a, b)
        if acum + s >= alvo:
            u = (alvo - acum) / s
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        acum += s
    return ps[0]


# --------------------------------------------------------------------------
# A prancha
# --------------------------------------------------------------------------
def prancha():
    planta, dec, mesas, grupos_mesas = mh.carrega()
    F = Folha()
    F.rc(0, 0, 420, 297, style="fill:#fff")

    # planta, desenhada pelas mesmas funcoes da pagina, em mm de papel
    P = mh.Planta("a3", x0=0.0, y0=0.0, x1=LARG, y1=ALT, S=K)
    mh.desenha_base(P, planta, dec)
    mh.desenha_mesas(P, mesas, planta)
    mh.desenha_fita(P, mesas, dec)
    for zona, t, _ in mh.barreiras(dec):
        P.line(t, "cinta-base")
        P.line(t, f"cinta c{zona}")
        for q in mh.postes_de(t):
            P.circle(q[0], q[1], .45, "poste")
    mh.desenha_sinal(P, grupos_mesas)
    defs = (f'<defs><pattern id="h-a3" width="1.4" height="1.4" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.4" class="hatch"/>'
            f'</pattern></defs>')
    F.add(defs)
    F.add(f'<g transform="translate({OX} {OY})">' + "".join(P.out) + "</g>")

    por_parede = {p: sorted(mh.eixo(m) for m in mesas if m["parede"] == p)
                  for p in ("oeste", "norte", "leste")}

    # --- cadeias externas: eixos das mesas ao longo de cada parede ---------
    eo = por_parede["oeste"]
    cadeia_v(F, [7.0] + eo + [ALT], OX - 6.5, livres([7.0] + eo + [ALT]),
             ext_ate=OX)
    F.tx(OX - 6.5, Y(7.0) + 3.2, "canto do recorte", "vl", anchor="middle")
    en = por_parede["norte"]
    cadeia_h(F, [0.0] + en + [LARG], OY - 7.0, livres([0.0] + en + [LARG]), ext_ate=OY)
    el = por_parede["leste"]
    xm = X(LARG) + 7.0
    cadeia_v(F, [0.0] + el + [ALT], xm, livres([0.0] + el + [ALT]), ext_ate=X(47.30),
             esquerda=False)

    # --- cadeia da fachada sul: tudo o que encosta na porta ---------------
    xs_sul = [0.0, 12.65, 15.05, 21.83, 25.03, 26.80, 29.80, 32.00, 35.00, 37.49, 39.96,
              41.52, 43.92, LARG]
    cadeia_h(F, xs_sul, Y(0.0) + 13.0, ext_ate=Y(0.0) + 1.0, acima=False)
    nomes = {(12.65, 15.05): "guia S2", (21.83, 25.03): "boca A", (26.80, 29.80): "aven. B",
             (32.00, 35.00): "boca C", (37.49, 39.96): "verde S7", (41.52, 43.92): "guia S8"}
    for (a, b), n in nomes.items():
        F.tx((X(a) + X(b)) / 2, Y(0.0) + 19.2, n, "vl")

    # --- cadeia transversal no meio do salao (y 17,00, no vao entre pares) ---
    xs_mid = [0.0, 4.10, 5.60, 11.00, 14.00, 26.80, 29.80, 33.50, 36.50, 41.70, 43.20,
              47.30, LARG]
    cadeia_h(F, xs_mid, Y(17.0), halo=True)
    rot = {(0.0, 4.10): "módulo", (4.10, 5.60): "sigilo", (5.60, 11.00): "canal",
           (11.00, 14.00): "aven. A", (26.80, 29.80): "aven. B", (33.50, 36.50): "aven. C",
           (36.50, 41.70): "canal", (41.70, 43.20): "sigilo", (43.20, 47.30): "módulo",
           (47.30, LARG): "faixa emerg.", (14.00, 26.80): "campo / reserva de fila",
           (29.80, 33.50): "campo"}
    for (a, b), n in rot.items():
        F.tx((X(a) + X(b)) / 2, Y(17.0) + 2.6, n, "vl halo")

    # --- cadeia longitudinal (x 23,00): perna da A, distribuidor, norte ----
    cadeia_v(F, [0.0, 3.40, 6.40, 35.40, 38.80, 40.30, ALT], X(23.0), halo=True,
             esquerda=False)
    for y, n in ((1.7, "boca A"), (4.9, "perna A"), (37.1, "canal norte"),
                 (39.55, "sigilo"), (42.35, "módulo")):
        F.tx(X(23.0) + 6.2, Y(y) + .7, n, "vl halo", anchor="start")
    # canto nordeste (D1)
    cadeia_v(F, [35.40, 36.20, 37.40, 38.80], X(32.75), halo=True)
    F.tx(X(32.75) - 6.0, Y(36.8) + .7, "corredor NE", "vl halo", anchor="end")
    F.tx(X(35.0), Y(36.2) + 2.6, "fim da C · 36,20", "vl halo")
    F.tx(X(12.5), Y(36.7) - 1.2, "fim da A · 36,70", "vl halo")
    # perna da avenida C e serpenteados
    F.tx(X(34.4), Y(4.2), "diag. 2,50", "vl halo", anchor="start")
    for s in dec["serpenteados"]:
        x1, y1, x2, y2 = s["rect"]
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        if s["parede"] == "norte":
            F.tx(X(cx), Y(y1) + 2.6, "serp. 2,80 × 4,20", "vl halo")
        else:
            F.tx(X(cx), Y(y2) - 1.0, "serp. 4,20 × 2,80", "vl halo")

    # --- etiquetas dos trechos de fita ------------------------------------
    tr = trechos(mesas, dec)
    for cod, (mx, my) in TAGS.items():
        x, y = X(mx), Y(my)
        F.rc(x - 2.4, y - 1.7, 4.8, 2.5, "tag")
        F.tx(x, y + .05, cod, "tagt")

    # --- coluna da direita: titulo, fita por trecho, barreira, legenda -----
    cx0 = 316.0
    F.tx(cx0, 12.0, "Hall 2 · montagem cotada", "h1", anchor="start")
    F.tx(cx0, 17.6, "2º turno · montagem sáb. 24/10/2026 · votação dom. 25/10", "t",
         anchor="start")
    F.tx(cx0, 21.2, f"Escala 1:{ESCALA} em A3 · medidas em metros · ajustes D1–D4 de 23/10",
         "tm", anchor="start")

    y = 29.0
    F.tx(cx0, y, "Fita por trecho", "h2", anchor="start")
    y += 4.0
    F.tx(cx0, y, "trecho", "tm", anchor="start")
    F.tx(412, y, "metros", "tm", anchor="end")
    y += 1.2
    ordem = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11",
             "T13A", "T13B", "T13C", "T14A", "T14B", "T14C", "T12", "T15", "T16", "T17"]
    por_cor = {}
    for cod in ordem:
        g = tr[cod]
        por_cor[g["cor"]] = por_cor.get(g["cor"], 0) + g["m"]
        y += 3.55
        sw = {"A": COR["A"], "B": "#d1ad1c", "C": COR["C"], "P": COR["P"],
              "S": "#ffffff", "Z": "#16202b"}[g["cor"]]
        F.rc(cx0, y - 2.0, 3.4, 2.2, style=f"fill:{sw};stroke:#16202b;stroke-width:.15")
        if g["cor"] == "Z":
            for i in range(3):
                F.rc(cx0 + .4 + i * 1.1, y - 2.0, .55, 2.2, style="fill:#fff")
        F.tx(cx0 + 4.6, y, cod.rstrip("ABC") if cod.startswith(("T13", "T14")) else cod,
             "tb", anchor="start")
        F.tx(cx0 + 11.5, y, g["nome"], "t", anchor="start")
        F.tx(412, y, br(g["m"], 1), "tb", anchor="end")
        F.ln([(cx0, y + 1.0), (412, y + 1.0)], "lin")

    y += 6.5
    F.tx(cx0, y, "Total por cor (com 10% de retoque · rolos de 50 m)", "tb", anchor="start")
    nome_cor = [("A", "azul"), ("B", "amarelo"), ("C", "laranja"), ("Z", "zebrado"),
                ("P", "verde"), ("S", "branco")]
    tot = 0.0
    for c, n in nome_cor:
        v = por_cor.get(c, 0.0)
        tot += v
        y += 3.4
        F.tx(cx0 + 2, y, n, "t", anchor="start")
        F.tx(cx0 + 40, y, f"{br(v, 1)} m", "t", anchor="end")
        F.tx(cx0 + 66, y, f"{br(v * 1.1, 1)} m", "t", anchor="end")
        F.tx(412, y, f"{math.ceil(v * 1.1 / 50)} rolo(s)", "tb", anchor="end")
    y += 3.6
    F.ln([(cx0, y - 2.4), (412, y - 2.4)], "lin")
    F.tx(cx0 + 2, y, "total", "tb", anchor="start")
    F.tx(cx0 + 40, y, f"{br(tot, 0)} m", "tb", anchor="end")
    F.tx(cx0 + 66, y, f"{br(tot * 1.1, 0)} m", "tb", anchor="end")

    y += 8.0
    F.tx(cx0, y, "Barreira (unifila · postes a 1,80 m)", "h2", anchor="start")
    bar = {}
    for zona, t, nome in mh.barreiras(dec):
        chave = nome.split(" · ")[0] if nome.startswith(("boca", "avenida")) else \
            {"22": "serpenteado A3", "23": "serpenteado B2", "24": "serpenteado C5"}[
                nome.split()[-1]]
        b = bar.setdefault(chave, [0.0, 0, 0])
        b[0] += sf.comp(t)
        b[1] += sf.postes(sf.comp(t))
        b[2] += 1
    ntot = 0
    for chave, (m_, n_, k_) in bar.items():
        y += 3.55
        ntot += n_
        F.tx(cx0 + 2, y, f"{chave} · {k_} cinta(s) de trilho", "t", anchor="start")
        F.tx(cx0 + 66, y, f"{br(m_, 1)} m", "t", anchor="end")
        F.tx(412, y, f"{n_} postes", "tb", anchor="end")
    y += 3.6
    F.ln([(cx0, y - 2.4), (412, y - 2.4)], "lin")
    F.tx(cx0 + 2, y, "total em uso · reserva 2 (+15 se compradas)", "tb", anchor="start")
    F.tx(412, y, f"{ntot} postes", "tb", anchor="end")

    y += 8.0
    F.tx(cx0, y, "Como ler", "h2", anchor="start")
    notas = [
        "Cadeias de fora da planta: eixo a eixo das mesas,",
        "medido ao longo da parede. Entre parênteses: espaço",
        "livre entre módulos (módulo = 0,90 m de largura).",
        "Oeste: medir a partir do canto do recorte (y 7,00).",
        "Leste: as mesas encostam na linha 47,30, a 3,00 m",
        "da fachada; a faixa até a fachada fica livre.",
        "Cadeia da fachada sul: medir a partir da parede oeste",
        "(x 0) ou do batente de porta mais próximo.",
        "Fita: 50 mm. Tiques de fila a cada 0,65 m no canal.",
        "Etiquetas T1–T11 na planta = linhas da tabela.",
        "Nenhuma peça para o eleitor leva número de mesa.",
    ]
    for n in notas:
        y += 2.9
        F.tx(cx0, y, n, "tm", anchor="start")

    # legenda curta embaixo da planta
    ly = 292.0
    itens = [("#33507E", "zona A · azul"), ("#d1ad1c", "zona B · amarelo"),
             ("#DE7343", "zona C · laranja"), ("#1e8449", "preferencial"),
             ("#b8321f", "zona protegida / serpenteado")]
    lx = OX
    for c, n in itens:
        F.rc(lx, ly - 1.7, 4.0, 1.6, style=f"fill:{c}")
        F.tx(lx + 5.0, ly, n, "tm", anchor="start")
        lx += 5.0 + len(n) * 1.05 + 5
    F.tx(lx, ly, "linha preta grossa com pontos = unifila · tracejado zebrado = linha de espera",
         "tm", anchor="start")

    corpo = "".join(F.o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" '
            f'viewBox="0 0 420 297"><style>{CSS}</style>{corpo}</svg>')


def main():
    svg = prancha()
    os.makedirs(os.path.dirname(BASE), exist_ok=True)
    with open(BASE + ".svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("escrito", os.path.relpath(BASE + ".svg", RAIZ))


if __name__ == "__main__":
    main()
