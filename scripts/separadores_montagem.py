#!/usr/bin/env python3
"""Mapa de montagem da fita no Hall 2 -- cada trecho cotado em metros.

Para a equipe que cola a fita no chao: onde comeca e onde acaba cada trecho,
quanto mede, a distancia entre as duas fitas de cada avenida, os vaos dos
ramais, e a distancia da fita ate a mesa.

Le a MESMA geometria de ``scripts/separadores_fila.py`` (AVENIDAS,
BANDA_PAREDE, DISTRIBUIDOR_NORTE, BOCA_PROF, LARG_CANAL, RECUO_MESA,
PASSO_FILA, CORES_ZONA) -- nao redefine nada, para que o mapa nunca divirja do
desenho definitivo de 17/09. Mudou a geometria la, basta rodar isto de novo.

Sistema de medidas: x a partir da parede oeste (x = 0), y a partir da linha das
portas da fachada sul (y = 0), como em ``data/prancheta_hall2.json``.

    python3 scripts/separadores_montagem.py           # lista de corte no terminal
    python3 scripts/separadores_montagem.py --grava   # + SVG, HTML, JSON e Markdown
"""
import datetime as _dt
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import separadores_fila as sf  # noqa: E402

RAIZ = sf.RAIZ
SAIDAS = sf.SAIDAS
DOCS = os.path.join(RAIZ, "docs", "separadores")

NOME_COR = {"A": "azul", "B": "amarelo", "C": "laranja"}
NOME_PAREDE_ELEITOR = {"oeste": "da esquerda", "norte": "do fundo", "leste": "da direita"}
# Quanto de cada trilho e barreira (unifila) e nao fita, pela alocacao
# definitiva de 17/09: as bocas de A e C (6 m por trilho) e a avenida B inteira.
BARREIRA_POR_AVENIDA = {"A": sf.BOCA_PROF, "B": math.inf, "C": sf.BOCA_PROF}
# Em que trilho de cada avenida ficam as aberturas dos ramais (o "pente").
TRILHO_DISTRIBUI = {"A": "trilho_interno", "C": "trilho_externo"}
MIN_PECA = 0.05        # pedacos de fita menores que isto nao se colam


def virg(v, nd=2):
    return f"{v:.{nd}f}".replace(".", ",")


def pt(p):
    return f"({virg(p[0])}; {virg(p[1])})"


# --------------------------------------------------------------------------
# A lista de corte
# --------------------------------------------------------------------------
def _funde(vaos):
    vaos = sorted(vaos)
    saida = []
    for a, b in vaos:
        if saida and a <= saida[-1][1] + 1e-9:
            saida[-1] = (saida[-1][0], max(saida[-1][1], b))
        else:
            saida.append((a, b))
    return saida


def pecas(ini, fim, vaos):
    """Os pedacos continuos de [ini, fim] que sobram depois de abrir os vaos."""
    saida, cursor = [], ini
    for a, b in _funde(vaos):
        if b <= ini or a >= fim:
            continue
        if a > cursor:
            saida.append((cursor, min(a, fim)))
        cursor = max(cursor, b)
    if cursor < fim:
        saida.append((cursor, fim))
    return [(a, b) for a, b in saida if b - a >= MIN_PECA]


def vaos_ramais(mesas, parede):
    """Os vaos de 1,10 m que cada ramal abre no trilho de distribuicao da parede."""
    meia = sf.LARG_CANAL / 2
    vaos = []
    for m in mesas:
        if m["parede"] != parede:
            continue
        eixo = m["y"] if parede in ("oeste", "leste") else m["x"]
        vaos.append((eixo - meia, eixo + meia))
    return vaos


def trilho(aid, lado, pts, mesas):
    """Um trilho de avenida, segmento a segmento, com barreira/fita e pedacos."""
    limite = BARREIRA_POR_AVENIDA[aid]
    percorrido = 0.0
    segs = []
    distribui = TRILHO_DISTRIBUI.get(aid) == lado
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        L = math.dist(a, b)
        barr = max(0.0, min(L, limite - percorrido))
        seg = {"n": i + 1, "de": a, "ate": b, "m": round(L, 2),
               "barreira_m": round(barr, 2), "fita_m": round(L - barr, 2),
               "vertical": abs(a[0] - b[0]) < 1e-9,
               "horizontal": abs(a[1] - b[1]) < 1e-9}
        if barr and barr < L:
            u = barr / L
            seg["fim_barreira"] = (round(a[0] + (b[0] - a[0]) * u, 2),
                                   round(a[1] + (b[1] - a[1]) * u, 2))
        # o ultimo segmento do trilho de distribuicao leva os vaos dos ramais
        if distribui and i == len(pts) - 2 and seg["vertical"]:
            parede = sf.AVENIDAS[aid]["parede"]
            y0, y1 = sorted((a[1], b[1]))
            ps = pecas(y0, y1, vaos_ramais(mesas, parede))
            seg["pecas"] = [{"de": (a[0], round(p, 2)), "ate": (a[0], round(q, 2)),
                             "m": round(q - p, 2)} for p, q in ps]
            seg["fita_m"] = round(sum(q - p for p, q in ps) - barr, 2)
            seg["vaos"] = [{"de": round(p, 2), "ate": round(q, 2)}
                           for p, q in _funde(vaos_ramais(mesas, parede))
                           if q > y0 and p < y1]
        segs.append(seg)
        percorrido += L
    return {"lado": lado, "segmentos": segs,
            "m": round(sum(s["m"] for s in segs), 2),
            "barreira_m": round(sum(s["barreira_m"] for s in segs), 2),
            "fita_m": round(sum(s["fita_m"] for s in segs), 2)}


def distribuidor(mesas):
    """O T da parede norte: a linha y = 35,40, com os vaos dos 9 ramais e a boca de B."""
    (x0, y), (x1, _) = sf.DISTRIBUIDOR_NORTE
    boca = (sf.AVENIDAS["B"]["trilho_interno"][-1][0], sf.AVENIDAS["B"]["trilho_externo"][-1][0])
    vaos = vaos_ramais(mesas, "norte") + [boca]
    ps = pecas(x0, x1, vaos)
    return {"y": y, "de": x0, "ate": x1, "boca_B": boca,
            "pecas": [{"de": (round(p, 2), y), "ate": (round(q, 2), y), "m": round(q - p, 2)}
                      for p, q in ps],
            "vaos": [{"de": round(p, 2), "ate": round(q, 2)} for p, q in _funde(vaos)],
            "fita_m": round(sum(q - p for p, q in ps), 2)}


def portas_por_id(planta):
    return {p["id"]: p for p in planta["portas"]}


def bocas(planta):
    """Onde cada trilho comeca na porta, medido dos batentes."""
    P = portas_por_id(planta)
    saida = []
    for aid, av in sf.AVENIDAS.items():
        porta = P[av["porta"]]
        xi, xe = av["trilho_interno"][0][0], av["trilho_externo"][0][0]
        saida.append({
            "avenida": aid, "porta": av["porta"], "batente_oeste": porta["x1"],
            "batente_leste": porta["x2"], "vao_porta": round(porta["x2"] - porta["x1"], 2),
            "trilho_interno_x": xi, "trilho_externo_x": xe,
            "interno_do_batente_oeste": round(xi - porta["x1"], 2),
            "externo_do_batente_leste": round(porta["x2"] - xe, 2),
            "largura": round(xe - xi, 2),
        })
    return saida


def ramais(mesas, planta, dec):
    """Os 28 ramais: eixo, comprimento, linha de espera, marcas, serpenteado."""
    P = planta["modulo"]["prof"]
    serp = {s["mrv"]: s for s in dec["serpenteados"]}
    saida = []
    por_parede = {}
    for m in mesas:
        por_parede.setdefault(m["parede"], []).append(m)
    for parede, lista in por_parede.items():
        banda = sf.BANDA_PAREDE[parede]
        comprimento = banda - P                      # trilho -> frente do modulo
        fila = comprimento - sf.RECUO_MESA           # trilho -> linha de espera
        n_marcas = int(round(fila / sf.PASSO_FILA))
        eixo_de = lambda m: m["y"] if parede in ("oeste", "leste") else m["x"]
        lista = sorted(lista, key=eixo_de)
        for i, m in enumerate(lista):
            eixo = eixo_de(m)
            viz = []
            if i > 0:
                viz.append(round(eixo - eixo_de(lista[i - 1]) - sf.LARG_CANAL, 2))
            if i < len(lista) - 1:
                viz.append(round(eixo_de(lista[i + 1]) - eixo - sf.LARG_CANAL, 2))
            s = serp.get(m["mrv"])
            r = {
                "eleitor": m["eleitor"], "mrv": m["mrv"], "grupo": m["grupo"],
                "secoes": m["secoes"], "parede": parede, "entrada": m["entrada"],
                "classe": m["classe"], "esperado": m["esperado"],
                "eixo": round(eixo, 2),
                "eixo_da_parede_norte": round(planta["salao"]["altura"] - eixo, 2)
                if parede in ("oeste", "leste") else None,
                "eixo_da_parede_oeste": round(eixo, 2) if parede == "norte" else None,
                "largura": sf.LARG_CANAL,
                "espaco_ate_vizinho": viz,
                "trilho_ate_frente_modulo": round(comprimento, 2),
                "trilho_ate_linha_espera": round(fila, 2),
                "linha_espera_da_mesa": sf.RECUO_MESA,
                "marcas": n_marcas,
                "frente": sf.frente(m, planta), "boca": sf.boca_avenida(m, planta),
            }
            if s:
                # o serpenteado (unifila) ocupa da frente do modulo ate `prof`;
                # o ramal de fita vai do trilho ate a borda do serpenteado
                r["serpenteado"] = {"rect": s["rect"], "profundidade": s["profundidade"],
                                    "raias": s["raias"], "passo_raia": s["passo_raia"],
                                    "pessoas": s["pessoas"]}
                r["fita_ate_serpenteado"] = round(comprimento - s["profundidade"], 2)
            saida.append(r)
    return sorted(saida, key=lambda r: r["eleitor"])


def fita_por_cor(avenidas, dist, rams):
    """Metros de fita a colar, pelo que esta neste mapa (avenidas, ramais, espera)."""
    por = {"A": 0.0, "B": 0.0, "C": 0.0, "espera": 0.0}
    for aid, av in avenidas.items():
        por[aid] += av["trilho_interno"]["fita_m"] + av["trilho_externo"]["fita_m"]
    por["B"] += dist["fita_m"]
    for r in rams:
        L = r.get("fita_ate_serpenteado", r["trilho_ate_frente_modulo"])
        por[r["entrada"]] += 2 * L + r["marcas"] * 0.25
        por["espera"] += sf.LARG_CANAL
    return {k: round(v, 1) for k, v in por.items()}


def monta():
    planta, dec, cen = sf.carrega()
    mesas = sf.monta_mesas(planta, dec, cen)
    avenidas = {}
    for aid, av in sf.AVENIDAS.items():
        avenidas[aid] = {
            "porta": av["porta"], "parede": av["parede"], "hex": av["hex"],
            "cor": NOME_COR[aid],
            "trilho_interno": trilho(aid, "trilho_interno", av["trilho_interno"], mesas),
            "trilho_externo": trilho(aid, "trilho_externo", av["trilho_externo"], mesas),
        }
    dist = distribuidor(mesas)
    rams = ramais(mesas, planta, dec)
    dados = {
        "gerado_em": _dt.date.today().isoformat(),
        "origem": "scripts/separadores_fila.py (desenho definitivo de 17/09, cenário Paredes_ABC)",
        "sistema": "x da parede oeste, y da linha das portas da fachada sul; metros",
        "premissas": {"largura_avenida_m": sf.LARG_AVENIDA, "largura_canal_m": sf.LARG_CANAL,
                      "linha_espera_m": sf.RECUO_MESA, "passo_fila_m": sf.PASSO_FILA,
                      "boca_barreira_m": sf.BOCA_PROF, "banda_por_parede_m": sf.BANDA_PAREDE,
                      "modulo_m": planta["modulo"]["prof"]},
        "bocas": bocas(planta),
        "avenidas": avenidas,
        "distribuidor_norte": dist,
        "ramais": rams,
    }
    dados["fita_por_cor"] = fita_por_cor(avenidas, dist, rams)
    return planta, dec, mesas, dados


# --------------------------------------------------------------------------
# Conferencias de campo: o que a geometria fechada deixa em aberto
# --------------------------------------------------------------------------
def conferencias(dados, mesas):
    """Conflitos que o mapa expoe e que a conferencia de 17/09 nao cobre.

    `separadores_fila.confere()` prova que as avenidas nao se cruzam entre si
    nem invadem zona protegida. Nao olha para o que acontece onde um trilho
    entra na banda de OUTRA parede. Isto olha.
    """
    achados = []
    ALT = 44.4
    y_banda_norte = ALT - sf.BANDA_PAREDE["norte"]
    for aid in ("A", "C"):
        av = dados["avenidas"][aid]
        lado_dist = TRILHO_DISTRIBUI[aid]
        lado_outro = "trilho_externo" if lado_dist == "trilho_interno" else "trilho_interno"
        seg_dist = av[lado_dist]["segmentos"][-1]
        topo_dist = seg_dist["pecas"][-1]["ate"][1]          # onde o trilho com vaos acaba de fato
        topo_outro = av[lado_outro]["segmentos"][-1]["ate"][1]
        topo = max(topo_dist, topo_outro)
        if topo <= y_banda_norte + 1e-9:
            continue
        xs = sorted((seg_dist["de"][0], av[lado_outro]["segmentos"][-1]["ate"][0]))
        dentro = [m for m in mesas if m["parede"] == "norte" and xs[0] < m["x"] < xs[1]]
        # ate onde o trilho precisa ir: o fim do ultimo vao de ramal, ou a borda da banda
        ultimo_vao = seg_dist["vaos"][-1]["ate"]
        fim_sugerido = round(min(ultimo_vao, topo_dist) if ultimo_vao <= topo else y_banda_norte, 2)
        achados.append({
            "avenida": aid, "trilho_com_vaos": lado_dist.replace("trilho_", ""),
            "topo_trilho_com_vaos": round(topo_dist, 2), "topo_outro_trilho": round(topo_outro, 2),
            "entra_na_banda_norte_m": round(topo - y_banda_norte, 2),
            "fim_sugerido": fim_sugerido,
            "mesas_norte_dentro": [f"{m['grupo']} (eleitor {m['eleitor']}, x = {virg(m['x'])})"
                                   for m in dentro],
            "economia_fita_m": round(max(0, topo_dist - fim_sugerido) + max(0, topo_outro - fim_sugerido), 1),
        })
    return achados


# --------------------------------------------------------------------------
# O desenho
# --------------------------------------------------------------------------
S = 20.0                       # px por metro
MX, MY = 64, 112               # margem esquerda, margem de topo (titulo)
MB = 96                        # margem inferior (cotas da porta)
LEG = 142                      # faixa da legenda


def svg_montagem(planta, dec, mesas, dados):
    LARG, ALT = planta["salao"]["largura"], planta["salao"]["altura"]
    W = MX * 2 + LARG * S + 60
    H = MY + ALT * S + MB + LEG
    px = lambda x, y: (MX + x * S, MY + (ALT - y) * S)
    o = []
    add = o.append
    INK, CINZA, CLARO = "#16202b", "#5b6470", "#8a94a6"

    def t(x, y, txt, size=10, cor=INK, anc="start", peso=400, rot=None, extra=""):
        a, b = px(x, y)
        tr = f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ""
        add(f'<text x="{a:.1f}" y="{b:.1f}" font-size="{size}" fill="{cor}" '
            f'text-anchor="{anc}" font-weight="{peso}"{tr}{extra}>{txt}</text>')

    def linha(p, q, cor, w, extra=""):
        a, b = px(*p)
        c, d = px(*q)
        add(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" '
            f'stroke="{cor}" stroke-width="{w}"{extra}/>')

    def poli(pts, cor, w, extra=""):
        s = " ".join(f"{px(*p)[0]:.1f},{px(*p)[1]:.1f}" for p in pts)
        add(f'<polyline points="{s}" fill="none" stroke="{cor}" stroke-width="{w}"{extra}/>')

    def cota_h(x1, x2, y, txt, acima=True, size=9.5, cor=CINZA, dx_txt=0.0):
        linha((x1, y), (x2, y), cor, 0.9)
        for xx in (x1, x2):
            linha((xx, y - 0.22), (xx, y + 0.22), cor, 0.9)
        t((x1 + x2) / 2 + dx_txt, y + (0.28 if acima else -0.58), txt, size, cor, "middle",
          600, extra=' font-variant-numeric="tabular-nums"')

    def cota_v(y1, y2, x, txt, esq=True, size=9.5, cor=CINZA):
        linha((x, y1), (x, y2), cor, 0.9)
        for yy in (y1, y2):
            linha((x - 0.22, yy), (x + 0.22, yy), cor, 0.9)
        t(x + (-0.28 if esq else 0.28), (y1 + y2) / 2, txt, size, cor, "middle", 600,
          rot=-90, extra=' font-variant-numeric="tabular-nums"')

    def rotulo_seg(p, q, txt, lado=1, size=9.5, cor=INK, peso=700, afast=0.42):
        """Texto paralelo ao segmento, afastado para o lado (+1 = esquerda da marcha)."""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        x, y = mx + nx * lado * afast, my + ny * lado * afast
        ang = -math.degrees(math.atan2(dy, dx))
        if ang > 90 or ang < -90:
            ang += 180
        t(x, y, txt, size, cor, "middle", peso, rot=round(ang, 1) or None,
          extra=' font-variant-numeric="tabular-nums" dominant-baseline="middle"')

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
        f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="Inter, Helvetica, Arial, sans-serif">')
    add(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#fbfaf8"/>')
    add('<defs>'
        '<pattern id="prot" width="7" height="7" patternTransform="rotate(45)" '
        'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" stroke="#c0392b" '
        'stroke-width="1" stroke-opacity=".22"/></pattern>'
        '<marker id="seta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
        'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>'
        '</marker></defs>')

    # ---- titulo ----
    add(f'<text x="{MX}" y="36" font-size="22" font-weight="800" fill="{INK}">'
        f'Montagem da fita no chão · Hall 2</text>')
    add(f'<text x="{MX}" y="58" font-size="12.5" fill="{CINZA}">Avenidas, ramais e linhas de '
        f'espera, cotados em metros. Medidas a partir da parede oeste (x) e da linha das portas '
        f'da fachada sul (y). Geometria do desenho definitivo de 17/09.</text>')
    add(f'<text x="{MX}" y="76" font-size="12.5" fill="{CINZA}">'
        f'<tspan font-weight="700" fill="{INK}">Traço grosso preto = unifila</tspan> (bocas de A e C, '
        f'avenida B inteira, serpenteados). <tspan font-weight="700" fill="{INK}">Traço na cor = '
        f'fita</tspan>. Vãos de {virg(sf.LARG_CANAL)} m só onde entra um ramal.</text>')
    add(f'<text x="{MX}" y="94" font-size="12.5" fill="{CINZA}">Avenida: {virg(sf.LARG_AVENIDA)} m '
        f'entre fitas (A: 3,20 m na boca). Ramal: canal de {virg(sf.LARG_CANAL)} m até a linha de '
        f'espera, a {virg(sf.RECUO_MESA)} m da mesa. Marcas a cada {virg(sf.PASSO_FILA)} m.</text>')

    # ---- salao ----
    cont = " ".join(f"{px(x, y)[0]:.1f},{px(x, y)[1]:.1f}" for x, y in planta["salao"]["contorno"])
    add(f'<polygon points="{cont}" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    for z in dec["zonas_protegidas"]:
        x1, y1, x2, y2 = z["rect"]
        a, b = px(x1, y2)
        sala = z["tipo"] == "sala_apoio"
        add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(x2-x1)*S:.1f}" height="{(y2-y1)*S:.1f}" '
            f'fill="{"#8a94a6" if sala else "url(#prot)"}" fill-opacity="{0.18 if sala else 1}" '
            f'stroke="#c0392b" stroke-opacity=".3" stroke-dasharray="3 3"/>')
        if sala:
            t((x1 + x2) / 2, (y1 + y2) / 2, "sala de apoio", 9.5, CINZA, "middle")
    # bandas
    for x1, y1, x2, y2 in ((0, 0, sf.BANDA_PAREDE["oeste"], ALT),
                           (0, ALT - sf.BANDA_PAREDE["norte"], LARG, ALT),
                           (47.3 - sf.BANDA_PAREDE["leste"], 0, 47.3, ALT)):
        a, b = px(x1, y2)
        add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{(x2-x1)*S:.1f}" height="{(y2-y1)*S:.1f}" '
            f'fill="{INK}" fill-opacity=".03"/>')

    # ---- portas ----
    rotulos_porta = []
    for p in planta["portas"]:
        sin = dec["sinalizacao_portas"].get(p["id"], {})
        papel = sin.get("papel", "livre")
        cor = {"entrada": sf.CORES_ZONA.get(sin.get("entrada"), CLARO), "saida": CINZA,
               "emergencia": "#c0392b", "preferencial": "#1e8449",
               "fechada": "#c9ced6", "livre": "#c9ced6"}[papel]
        linha((p["x1"], p["y1"]), (p["x2"], p["y2"]), cor, 7)
        if papel in ("entrada", "saida", "preferencial") or p["id"] in ("S3", "R1", "N2", "O2"):
            mx, my = (p["x1"] + p["x2"]) / 2, (p["y1"] + p["y2"]) / 2
            halo = ' paint-order="stroke" stroke="#fbfaf8" stroke-width="3"'
            if p["face"] == "sul":
                if papel == "entrada":      # no eixo da boca, entre as duas fitas
                    av_ = sf.AVENIDAS[sin["entrada"]]
                    mx = (av_["trilho_interno"][0][0] + av_["trilho_externo"][0][0]) / 2
                rotulos_porta.append((mx, my + 0.35, p["id"], cor, None, halo))
            elif p["face"] == "norte":
                rotulos_porta.append((mx, my - 0.75, p["id"], cor, None, halo))
            else:
                rotulos_porta.append((mx + (0.45 if p["face"] == "recorte_v" else -0.45), my,
                                      p["id"], cor, -90, halo))

    # ---- modulos ----
    P, L = planta["modulo"]["prof"], planta["modulo"]["larg"] / 2
    for m in mesas:
        dxp, dyp = m["dx"], m["dy"]
        pxp, pyp = -dyp, dxp
        cantos = [(m["x"] + pxp * L, m["y"] + pyp * L), (m["x"] - pxp * L, m["y"] - pyp * L),
                  (m["x"] - pxp * L + dxp * P, m["y"] - pyp * L + dyp * P),
                  (m["x"] + pxp * L + dxp * P, m["y"] + pyp * L + dyp * P)]
        pts = " ".join(f"{px(*c)[0]:.1f},{px(*c)[1]:.1f}" for c in cantos)
        add(f'<polygon points="{pts}" fill="{m["hex_entrada"]}" fill-opacity=".85" '
            f'stroke="{INK}" stroke-width=".6"/>')
        gx, gy = m["x"] + dxp * P / 2, m["y"] + dyp * P / 2
        tc = "#16202b" if m["entrada"] == "B" else "#ffffff"
        t(gx, gy, m["grupo"], 9.5, tc, "middle", 800, rot=(-90 if m["rot"] == 270 else None),
          extra=' dominant-baseline="middle"')

    # ---- ramais: canal, marcas, linha de espera, serpenteado ----
    for r in dados["ramais"]:
        m = next(x for x in mesas if x["eleitor"] == r["eleitor"])
        fx, fy = r["frente"]
        bx, by = r["boca"]
        dx, dy = m["dx"], m["dy"]
        perp = (-dy, dx)
        meia = sf.LARG_CANAL / 2
        # o ramal de fita: do trilho ate a frente do modulo (ou ate o serpenteado)
        fim = r.get("fita_ate_serpenteado", r["trilho_ate_frente_modulo"])
        ex, ey = bx - dx * fim, by - dy * fim
        for sgn in (1, -1):
            linha((bx + perp[0] * meia * sgn, by + perp[1] * meia * sgn),
                  (ex + perp[0] * meia * sgn, ey + perp[1] * meia * sgn),
                  m["hex_entrada"], 1.6)
        # marcas de 0,65 m a partir da linha de espera, para fora
        lx, ly = fx + dx * sf.RECUO_MESA, fy + dy * sf.RECUO_MESA
        if "serpenteado" not in r:
            for i in range(1, r["marcas"] + 1):
                qx, qy = lx + dx * i * sf.PASSO_FILA, ly + dy * i * sf.PASSO_FILA
                linha((qx + perp[0] * meia, qy + perp[1] * meia),
                      (qx + perp[0] * (meia - 0.25), qy + perp[1] * (meia - 0.25)),
                      m["hex_entrada"], 1.2)
        # linha de espera zebrada, a 1,50 m da mesa, em todas as 28 (nas vermelhas
        # ela cai dentro da primeira raia do serpenteado: ver "conferir em campo")
        e1 = (lx + perp[0] * meia, ly + perp[1] * meia)
        e2 = (lx - perp[0] * meia, ly - perp[1] * meia)
        linha(e1, e2, INK, 4)
        linha(e1, e2, "#ffffff", 2.2, ' stroke-dasharray="3 3"')
        if "serpenteado" in r:
            s = r["serpenteado"]
            for tr in sf.serpenteado_trilhos({"rect": s["rect"], "profundidade": s["profundidade"],
                                              "parede": r["parede"], "passo_raia": s["passo_raia"]}):
                poli(tr, INK, 3.2, ' stroke-linecap="round"')
                for p in tr:
                    a, b = px(*p)
                    add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.2" fill="{INK}"/>')

    # ---- distribuidor norte (fita amarela, em pedacos) ----
    dist = dados["distribuidor_norte"]
    cruzam = [sf.AVENIDAS[a][l][-1][0] for a in ("A", "C") for l in ("trilho_interno", "trilho_externo")]
    for pcs in dist["pecas"]:
        linha(pcs["de"], pcs["ate"], sf.CORES_ZONA["B"], 3)
        cx_ = (pcs["de"][0] + pcs["ate"][0]) / 2
        if any(abs(cx_ - x_) < 0.7 for x_ in cruzam):
            cx_ = pcs["de"][0] + 0.65
        t(cx_, dist["y"] + 0.32, virg(pcs["m"]), 8.5,
          "#8a6a00", "middle", 700, extra=' font-variant-numeric="tabular-nums"')

    # ---- avenidas ----
    for aid, av in dados["avenidas"].items():
        cor = av["hex"]
        for lado in ("trilho_interno", "trilho_externo"):
            tr = av[lado]
            for seg in tr["segmentos"]:
                a, b = seg["de"], seg["ate"]
                if "pecas" in seg:
                    # barreira ate fim_barreira, depois fita em pedacos
                    if seg["barreira_m"]:
                        fb = seg.get("fim_barreira", b)
                        linha(a, fb, INK, 5, ' stroke-linecap="round"')
                        linha(a, fb, cor, 2.2, ' stroke-linecap="round"')
                    for pcs in seg["pecas"]:
                        p, q = pcs["de"], pcs["ate"]
                        if seg["barreira_m"] and q[1] <= seg["fim_barreira"][1] + 1e-9:
                            continue
                        p = (p[0], max(p[1], seg.get("fim_barreira", p)[1])) if seg["barreira_m"] else p
                        linha(p, q, cor, 3)
                    continue
                if seg["barreira_m"] >= seg["m"] - 1e-9:
                    linha(a, b, INK, 5, ' stroke-linecap="round"')
                    linha(a, b, cor, 2.2, ' stroke-linecap="round"')
                elif seg["barreira_m"]:
                    fb = seg["fim_barreira"]
                    linha(a, fb, INK, 5, ' stroke-linecap="round"')
                    linha(a, fb, cor, 2.2, ' stroke-linecap="round"')
                    linha(fb, b, cor, 3)
                else:
                    linha(a, b, cor, 3)
        # postes das bocas e da avenida B
        for lado in ("trilho_interno", "trilho_externo"):
            pts = sf.AVENIDAS[aid][lado]
            Lb = min(sf.comp(pts), BARREIRA_POR_AVENIDA[aid])
            n = sf.postes(Lb)
            for i in range(n):
                d = 0 if n == 1 else i / (n - 1) * Lb
                pnt = sf._recorta(pts, d)[-1] if d > 0 else pts[0]
                a, b = px(*pnt)
                add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.4" fill="{INK}"/>')

    # fim da barreira
    for aid in ("A", "C"):
        for lado in ("trilho_interno", "trilho_externo"):
            for seg in dados["avenidas"][aid][lado]["segmentos"]:
                if "fim_barreira" in seg:
                    a, b = px(*seg["fim_barreira"])
                    add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4.5" fill="#fbfaf8" '
                        f'stroke="{INK}" stroke-width="1.6"/>')

    # ---- setas de sentido ----
    def seta(p, q, cor):
        linha(p, q, cor, 2.6, ' marker-end="url(#seta)" opacity=".85"')
    seta((23.43, 0.6), (23.43, 2.6), sf.CORES_ZONA["A"])
    seta((20.5, 4.9), (16.5, 4.9), sf.CORES_ZONA["A"])
    for yy in (9.0, 15.0, 27.0, 33.0):
        seta((12.5, yy), (12.5, yy + 2.2), sf.CORES_ZONA["A"])
    for yy in (6.0, 14.0, 22.0, 30.0):
        seta((28.3, yy), (28.3, yy + 2.2), "#b8960c")
    seta((33.5, 0.7), (33.5, 2.6), sf.CORES_ZONA["C"])
    for yy in (9.0, 15.0, 27.0, 33.0):
        seta((35.0, yy), (35.0, yy + 2.2), sf.CORES_ZONA["C"])

    # ---- rotulos de trecho ----
    A, C = dados["avenidas"]["A"], dados["avenidas"]["C"]
    corA, corC = sf.CORES_ZONA["A"], "#b04a1e"
    corB = "#8a6a00"
    # A interno
    si = A["trilho_interno"]["segmentos"]
    rotulo_seg(si[0]["de"], si[0]["ate"], f'{virg(si[0]["m"])} unifila', -1, 9, corA)
    rotulo_seg(si[1]["de"], si[1]["ate"], f'{virg(si[1]["m"])} = {virg(si[1]["barreira_m"])} unifila '
               f'+ {virg(si[1]["fita_m"])} fita', -1, 9.5, corA)
    for pcs in si[2]["pecas"]:
        rotulo_seg(pcs["de"], pcs["ate"], virg(pcs["m"]), -1, 8.5, corA, 700, 0.36)
    # A externo
    se = A["trilho_externo"]["segmentos"]
    rotulo_seg(se[0]["de"], se[0]["ate"], f'{virg(se[0]["m"])} = 6,00 unifila + 0,40 fita', 1, 8.5, corA, 700, 0.5)
    rotulo_seg(se[1]["de"], se[1]["ate"], f'{virg(se[1]["m"])} fita', 1, 9.5, corA)
    rotulo_seg(se[2]["de"], se[2]["ate"], f'{virg(se[2]["m"])} fita, contínua', 1, 9.5, corA)
    t(12.5, 21.5, f'trilho interno {virg(A["trilho_interno"]["m"])} · externo '
      f'{virg(A["trilho_externo"]["m"])}', 8.5, corA, "middle", 600, rot=-90)
    # B
    for lado, txt_lado in (("trilho_interno", "lado da parede"), ("trilho_externo", "lado do campo")):
        sgm = dados["avenidas"]["B"][lado]["segmentos"][0]
        rotulo_seg(sgm["de"], sgm["ate"], f'{virg(sgm["m"])} unifila · 21 postes · {txt_lado}',
                   1 if lado == "trilho_externo" else -1, 9.5, corB)
    t(28.3, 18.0, "B · toda em unifila", 9, corB, "middle", 700, rot=-90)
    # C interno
    si = C["trilho_interno"]["segmentos"]
    rotulo_seg(si[0]["de"], si[0]["ate"], f'{virg(si[0]["m"])} unifila', 1, 9, corC)
    rotulo_seg(si[1]["de"], si[1]["ate"], f'{virg(si[1]["m"])}', 1, 9, corC, 700, 0.5)
    rotulo_seg(si[2]["de"], si[2]["ate"], f'{virg(si[2]["m"])} = 0,30 unifila + {virg(si[2]["fita_m"])} fita, contínua',
               1, 9.5, corC)
    se = C["trilho_externo"]["segmentos"]
    rotulo_seg(se[0]["de"], se[0]["ate"], f'{virg(se[0]["m"])} unifila', -1, 9, corC)
    rotulo_seg(se[1]["de"], se[1]["ate"], f'{virg(se[1]["m"])}', -1, 9, corC, 700, 0.5)
    for pcs in se[2]["pecas"]:
        if pcs["ate"][1] <= 5.5 + 1e-9:
            continue
        p = (pcs["de"][0], max(pcs["de"][1], 5.5))
        rotulo_seg(p, pcs["ate"], virg(round(pcs["ate"][1] - p[1], 2)), 1, 8.5, corC, 700, 0.36)
    t(35.0, 21.5, f'trilho interno {virg(C["trilho_interno"]["m"])} · externo '
      f'{virg(C["trilho_externo"]["m"])}', 8.5, corC, "middle", 600, rot=-90)
    # distribuidor
    t(14.5, dist["y"] - 0.8, f'distribuidor do T · y = {virg(dist["y"])} · '
      f'{virg(dist["fita_m"])} m em {len(dist["pecas"])} pedaços', 8.5, corB, "start", 700)

    # ---- cotas da porta (abaixo da fachada sul) ----
    B = {b["avenida"]: b for b in dados["bocas"]}
    cota_h(B["A"]["trilho_interno_x"], B["A"]["trilho_externo_x"], -0.9, virg(B["A"]["largura"]), False)
    cota_h(B["A"]["trilho_externo_x"], B["B"]["trilho_interno_x"], -0.9,
           virg(B["B"]["trilho_interno_x"] - B["A"]["trilho_externo_x"]), False)
    cota_h(B["B"]["trilho_interno_x"], B["B"]["trilho_externo_x"], -0.9, virg(B["B"]["largura"]), False)
    cota_h(B["B"]["trilho_externo_x"], B["C"]["trilho_interno_x"], -0.9,
           virg(B["C"]["trilho_interno_x"] - B["B"]["trilho_externo_x"]), False)
    cota_h(B["C"]["trilho_interno_x"], B["C"]["trilho_externo_x"], -0.9, virg(B["C"]["largura"]), False)
    for aid in "ABC":
        b = B[aid]
        if b["interno_do_batente_oeste"] > 0.05:
            cota_h(b["batente_oeste"], b["trilho_interno_x"], -2.1, virg(b["interno_do_batente_oeste"]), False,
                   dx_txt=(0.6 if b["interno_do_batente_oeste"] < 0.8 else 0.0))
        if b["externo_do_batente_leste"] > 0.05:
            cota_h(b["trilho_externo_x"], b["batente_leste"], -2.1, virg(b["externo_do_batente_leste"]), False)
        cota_h(b["batente_oeste"], b["batente_leste"], -3.3, f'{b["porta"]} · vão {virg(b["vao_porta"])}', False)
    t(B["A"]["batente_oeste"] - 0.4, -1.45, "entre fitas", 8.5, CINZA, "end")
    t(B["A"]["batente_oeste"] - 0.4, -2.65, "do batente", 8.5, CINZA, "end")

    # ---- cotas das pernas (A e C) ----
    cota_v(0, 3.40, 10.3, "3,40", True)
    cota_v(3.40, 6.40, 10.3, "3,00", True)
    cota_v(0, 3.20, 31.4, "3,20", True)
    cota_v(3.20, 5.20, 31.4, "2,00", True)
    cota_h(32.0, 33.5, 5.75, "1,50", True, 8.5)
    cota_h(35.0, 36.5, 5.75, "1,50", True, 8.5)
    # topos, medidos da parede norte
    cota_v(36.30, ALT, 14.7, f'{virg(ALT - 36.30)} da parede norte', False, 8.5)
    cota_v(39.50, ALT, 36.72, f'{virg(ALT - 39.50)} da parede norte', False, 8.5)
    cota_v(dist["y"], ALT, 9.3, f'{virg(ALT - dist["y"])} banda norte', True, 8.5)
    # campo entre avenidas
    cota_h(14.0, 26.8, 12.0, f'{virg(12.8)} · campo de reserva de fila', True)
    cota_h(29.8, 33.5, 12.0, virg(3.7), True)

    # ---- cotas da fita a mesa, uma por parede ----
    # oeste, num trecho sem ramal (entre A2 e o serpenteado de A3)
    yy = 20.3
    cota_h(0, P, yy, f'{virg(P)} módulo', True, 8.5)
    cota_h(P, P + sf.RECUO_MESA, yy, virg(sf.RECUO_MESA), True, 8.5)
    cota_h(P + sf.RECUO_MESA, sf.BANDA_PAREDE["oeste"], yy,
           f'{virg(sf.BANDA_PAREDE["oeste"] - P - sf.RECUO_MESA)} fila · 8 marcas', True, 8.5)
    cota_h(0, sf.BANDA_PAREDE["oeste"], yy - 0.9, f'{virg(sf.BANDA_PAREDE["oeste"])} banda oeste', False, 8.5)
    # norte, no recuo N2
    xx = 23.7
    cota_v(ALT - P, ALT, xx, f'{virg(P)} módulo', True, 8.5)
    cota_v(ALT - P - sf.RECUO_MESA, ALT - P, xx, virg(sf.RECUO_MESA), True, 8.5)
    cota_v(dist["y"], ALT - P - sf.RECUO_MESA, xx,
           f'{virg(ALT - P - sf.RECUO_MESA - dist["y"])} · 5 marcas', True, 8)
    # leste, entre C3 e C4
    yy = 17.8
    cota_h(47.3 - P, 47.3, yy, f'{virg(P)} módulo', True, 8.5)
    cota_h(47.3 - P - sf.RECUO_MESA, 47.3 - P, yy, virg(sf.RECUO_MESA), True, 8.5)
    cota_h(36.5, 47.3 - P - sf.RECUO_MESA, yy,
           f'{virg(47.3 - P - sf.RECUO_MESA - 36.5)} fila · 8 marcas', True, 8.5)
    cota_h(36.5, 47.3, yy - 0.9, f'{virg(sf.BANDA_PAREDE["leste"])} banda leste', False, 8.5)
    cota_h(47.3, 50.3, yy, "3,00 L1–L4", True, 8.5)
    # largura do ramal, uma vez por parede
    cota_v(8.03 - 0.55, 8.03 + 0.55, 9.6, "1,10", False, 8.5)
    cota_v(13.45 - 0.55, 13.45 + 0.55, 38.0, "1,10", True, 8.5)
    cota_h(41.73 - 0.55, 41.73 + 0.55, 37.4, "1,10", False, 8.5)

    for mx, my, idp, cor, rot, halo in rotulos_porta:
        t(mx, my, idp, 10, cor, "middle", 800, rot=rot, extra=halo)

    # ---- legenda ----
    ly = MY + ALT * S + MB + 22
    lx = MX
    add(f'<line x1="{lx}" y1="{ly-16}" x2="{W-MX}" y2="{ly-16}" stroke="#dcdde1"/>')
    itens = [
        ("barreira", INK, 5, "", "unifila (traço grosso, postes a 1,80 m)"),
        ("fitaA", sf.CORES_ZONA["A"], 3, "", "fita azul · avenida A e ramais da parede oeste"),
        ("fitaB", sf.CORES_ZONA["B"], 3, "", "fita amarela · distribuidor do T e ramais da parede norte"),
        ("fitaC", sf.CORES_ZONA["C"], 3, "", "fita laranja · avenida C e ramais da parede leste"),
        ("espera", INK, 4, "zebra", "linha de espera · zebrado preto-e-branco, 1,10 m"),
        ("fim", INK, 0, "circ", "fim da barreira, começa a fita"),
        ("prot", "#c0392b", 0, "hatch", "zona protegida: não colar nem enfileirar"),
        ("serp", INK, 3.2, "serp", "serpenteado em unifila: 3 trilhos de 4,20 m, raias de 1,40 m"),
    ]
    col_w = (W - 2 * MX) / 3
    for i, (k, cor, w, tipo, txt) in enumerate(itens):
        cx = lx + (i % 3) * col_w
        cy = ly + (i // 3) * 26
        if tipo == "zebra":
            add(f'<line x1="{cx}" y1="{cy}" x2="{cx+26}" y2="{cy}" stroke="{INK}" stroke-width="4"/>')
            add(f'<line x1="{cx}" y1="{cy}" x2="{cx+26}" y2="{cy}" stroke="#fff" stroke-width="2.2" '
                f'stroke-dasharray="3 3"/>')
        elif tipo == "circ":
            add(f'<circle cx="{cx+13}" cy="{cy}" r="4.5" fill="#fbfaf8" stroke="{INK}" stroke-width="1.6"/>')
        elif tipo == "serp":
            for dy_ in (-5, 0, 5):
                add(f'<line x1="{cx}" y1="{cy+dy_}" x2="{cx+26}" y2="{cy+dy_}" stroke="{INK}" stroke-width="2.4"/>')
        elif tipo == "hatch":
            add(f'<rect x="{cx}" y="{cy-7}" width="26" height="14" fill="url(#prot)" stroke="#c0392b" '
                f'stroke-opacity=".3"/>')
        else:
            add(f'<line x1="{cx}" y1="{cy}" x2="{cx+26}" y2="{cy}" stroke="{cor}" stroke-width="{w}" '
                f'stroke-linecap="round"/>')
            if k == "barreira":
                for dx_ in (0, 13, 26):
                    add(f'<circle cx="{cx+dx_}" cy="{cy}" r="2.4" fill="{INK}"/>')
        add(f'<text x="{cx+34}" y="{cy+4}" font-size="10.5" fill="#31404f">{txt}</text>')
    add(f'<text x="{MX}" y="{H-12}" font-size="9.5" fill="{CLARO}">Gerado por '
        f'scripts/separadores_montagem.py em {dados["gerado_em"]} · escala 1 m = {S:.0f} px · '
        f'cenário Paredes_ABC · lista de corte completa em docs/separadores/montagem_fita_hall2.md</text>')
    add('</svg>')
    return "\n".join(o)


# --------------------------------------------------------------------------
# Lista de corte em texto (terminal e Markdown)
# --------------------------------------------------------------------------
def linhas_segmentos(av):
    out = []
    for lado, nome in (("trilho_interno", "trilho interno (lado da parede)"),
                       ("trilho_externo", "trilho externo (lado do campo)")):
        tr = av[lado]
        out.append((nome, tr))
    return out


def md_lista(dados, achados):
    L = []
    a = L.append
    pr = dados["premissas"]
    a("# Montagem da fita no chão — Hall 2, lista de corte\n")
    a(f"Gerado em {dados['gerado_em']} por `scripts/separadores_montagem.py`, a partir da geometria de "
      "`scripts/separadores_fila.py` (desenho definitivo de 17/09, cenário `Paredes_ABC`). "
      "Mapa cotado: `saidas/montagem_fita_hall2.svg` (e `.png`); página para o celular: "
      "`saidas/montagem_fita_hall2.html`.\n")
    a("**Medidas em metros.** `x` conta da parede oeste; `y` conta da linha das portas da fachada sul "
      "(a mesma origem de `data/prancheta_hall2.json`). Um ponto é `(x; y)`.\n")
    a("## Regras que valem para tudo\n")
    a(f"- Avenida: duas fitas paralelas a **{virg(pr['largura_avenida_m'])} m** uma da outra "
      "(a boca da A tem 3,20 m, porque o trilho externo encosta na alvenaria entre S4 e S5).")
    a(f"- A fita só abre **vão de {virg(pr['largura_canal_m'])} m** onde entra um ramal. Fora isso é contínua.")
    a(f"- O que é **unifila** não leva fita: as bocas de A e C ({virg(pr['boca_barreira_m'])} m de cada trilho, "
      "contados da porta), a avenida B inteira e os três serpenteados. Montar a unifila primeiro; "
      "a fita começa onde o último poste acaba.")
    a(f"- Ramal: canal de {virg(pr['largura_canal_m'])} m, na cor da zona, do trilho da avenida até a frente da mesa. "
      f"Linha de espera **zebrada** a {virg(pr['linha_espera_m'])} m da mesa, atravessando o canal. "
      f"Marcas de 0,25 m a cada {virg(pr['passo_fila_m'])} m, da linha de espera para fora.")
    a("- Rótulo no chão por **grupo e seção**, nunca por número de mesa.\n")

    a("## 1. Na porta: onde cada fita começa\n")
    a("| Avenida | Porta | Trilho interno | Trilho externo | Entre fitas |")
    a("|---|---|---|---|---|")
    for b in dados["bocas"]:
        a(f"| **{b['avenida']}** | {b['porta']} (vão {virg(b['vao_porta'])} m, x {virg(b['batente_oeste'])}–"
          f"{virg(b['batente_leste'])}) | x = {virg(b['trilho_interno_x'])} · "
          f"{_do_batente(b['interno_do_batente_oeste'], 'oeste')} | x = {virg(b['trilho_externo_x'])} · "
          f"{_do_batente(b['externo_do_batente_leste'], 'leste')} | **{virg(b['largura'])} m** |")
    bz = {b["avenida"]: b for b in dados["bocas"]}
    a(f"\nEntre a fita externa de A e a interna de B: "
      f"{virg(bz['B']['trilho_interno_x'] - bz['A']['trilho_externo_x'])} m. "
      f"Entre a externa de B e a interna de C: {virg(bz['C']['trilho_interno_x'] - bz['B']['trilho_externo_x'])} m. "
      "A alvenaria entre portas tem 0,29 m.\n")

    for aid, av in dados["avenidas"].items():
        a(f"## 2.{'ABC'.index(aid) + 1}. Avenida {aid} · {av['cor']} · {av['porta']} → parede {av['parede']}\n")
        for nome, tr in linhas_segmentos(av):
            a(f"**{nome.capitalize()}** — {virg(tr['m'])} m no total: {virg(tr['barreira_m'])} m em unifila, "
              f"{virg(tr['fita_m'])} m em fita.\n")
            a("| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |")
            a("|---|---|---|---:|---:|---:|---|")
            for s in tr["segmentos"]:
                obs = ""
                if "fim_barreira" in s:
                    obs = f"a unifila acaba em {pt(s['fim_barreira'])}; daí em diante, fita"
                if "pecas" in s:
                    obs = (obs + "; " if obs else "") + \
                        f"{len(s['pecas'])} pedaços com {len(s['vaos'])} vãos de {virg(sf.LARG_CANAL)} m (abaixo)"
                a(f"| {s['n']} | {pt(s['de'])} | {pt(s['ate'])} | {virg(s['m'])} | "
                  f"{virg(s['barreira_m']) if s['barreira_m'] else '—'} | "
                  f"{virg(s['fita_m']) if s['fita_m'] else '—'} | {obs} |")
            a("")
            for s in tr["segmentos"]:
                if "pecas" not in s:
                    continue
                a(f"Pedaços do segmento {s['n']} (x = {virg(s['de'][0])}), de sul para norte. "
                  "Cada vão é a boca de um ramal; o primeiro pedaço começa onde a unifila acaba "
                  f"({virg(s['fim_barreira'][1]) if 'fim_barreira' in s else virg(s['de'][1])}).\n")
                a("| Pedaço | y de | y até | m | Vão seguinte (y) |")
                a("|---|---:|---:|---:|---|")
                vaos = s["vaos"]
                for i, pcs in enumerate(s["pecas"]):
                    y0 = pcs["de"][1]
                    if "fim_barreira" in s and y0 < s["fim_barreira"][1]:
                        y0 = s["fim_barreira"][1]
                    comp_ = round(pcs["ate"][1] - y0, 2)
                    v = next((v for v in vaos if abs(v["de"] - pcs["ate"][1]) < 1e-6), None)
                    vtxt = f"{virg(v['de'])}–{virg(v['ate'])}" if v else "fim do trilho"
                    a(f"| {i + 1} | {virg(y0)} | {virg(pcs['ate'][1])} | {virg(comp_)} | {vtxt} |")
                a("")

    d = dados["distribuidor_norte"]
    a(f"## 3. Distribuidor do T (parede norte) · fita amarela · y = {virg(d['y'])}\n")
    a(f"Linha reta de x = {virg(d['de'])} a x = {virg(d['ate'])}, interrompida pela boca da avenida B "
      f"(x {virg(d['boca_B'][0])}–{virg(d['boca_B'][1])}, onde os postes chegam) e pelos 9 vãos dos ramais. "
      f"{virg(d['fita_m'])} m de fita em {len(d['pecas'])} pedaços, de oeste para leste:\n")
    a("| Pedaço | x de | x até | m |")
    a("|---|---:|---:|---:|")
    for i, pcs in enumerate(d["pecas"]):
        a(f"| {i + 1} | {virg(pcs['de'][0])} | {virg(pcs['ate'][0])} | {virg(pcs['m'])} |")
    a("")

    a("## 4. Da fita à mesa, por parede\n")
    a("| Parede | Fita da avenida | → linha de espera | → frente do módulo | → parede | Marcas no canal |")
    a("|---|---|---:|---:|---:|---:|")
    P = pr["modulo_m"]
    for parede, (lbl) in (("oeste", "x = 11,00 (trilho interno de A)"),
                          ("norte", "y = 35,40 (distribuidor do T)"),
                          ("leste", "x = 36,50 (trilho externo de C)")):
        banda = pr["banda_por_parede_m"][parede]
        a(f"| **{parede}** | {lbl} | {virg(banda - P - pr['linha_espera_m'])} m | {virg(banda - P)} m "
          f"| {virg(banda)} m | {int(round((banda - P - pr['linha_espera_m']) / pr['passo_fila_m']))} |")
    a("\nA parede leste é a linha das mesas, x = 47,30; os 3,00 m até a fachada (50,30) são a faixa "
      "protegida das saídas de emergência L1–L4.\n")

    a("## 5. Os 28 ramais\n")
    a("Eixo do canal medido da **parede norte** (paredes oeste e leste) ou da **parede oeste** (parede norte). "
      "\"Espaço\" é a fita contínua entre este ramal e o vizinho, nos dois sentidos.\n")
    a("| Nº | Grupo | Seções | Parede | Eixo `(x; y)` | Eixo, da referência | Espaço até os vizinhos | Canal | Marcas |")
    a("|---:|---|---|---|---|---|---|---:|---:|")
    for r in dados["ramais"]:
        ref = (f"{virg(r['eixo_da_parede_norte'])} m da parede norte" if r["eixo_da_parede_norte"] is not None
               else f"{virg(r['eixo_da_parede_oeste'])} m da parede oeste")
        eixo_xy = (f"({virg(r['boca'][0])}; {virg(r['eixo'])})" if r["parede"] in ("oeste", "leste")
                   else f"({virg(r['eixo'])}; {virg(r['boca'][1])})")
        canal = (f"{virg(r['fita_ate_serpenteado'])} até o serpenteado" if "serpenteado" in r
                 else f"{virg(r['trilho_ate_frente_modulo'])}")
        marcas = "serp." if "serpenteado" in r else str(r["marcas"])
        a(f"| {r['eleitor']} | **{r['grupo']}** | {' · '.join(str(s) for s in r['secoes'])} | {r['parede']} | "
          f"{eixo_xy} | {ref} | {' / '.join(virg(v) for v in r['espaco_ate_vizinho'])} | {canal} | {marcas} |")
    a("\nNos três grupos vermelhos (A3, B2, C5) o serpenteado em unifila — 3 trilhos de 4,20 m, raias de "
      "1,40 m — ocupa os 4,20 m à frente do módulo; o ramal de fita vai do trilho da avenida até a borda "
      "do serpenteado.\n")

    f = dados["fita_por_cor"]
    a("## 6. Fita a colar, pelo que está neste mapa\n")
    a("| Cor | Onde | m |")
    a("|---|---|---:|")
    a(f"| Azul | avenida A (fita), 9 ramais da oeste, marcas | {virg(f['A'], 1)} |")
    a(f"| Amarelo | distribuidor do T, 9 ramais da norte, marcas | {virg(f['B'], 1)} |")
    a(f"| Laranja | avenida C (fita), 10 ramais da leste, marcas | {virg(f['C'], 1)} |")
    a(f"| Zebrado | 28 linhas de espera de 1,10 m | {virg(f['espera'], 1)} |")
    a("\nSão só os trechos cotados aqui, sem os galões de sentido, as setas de saída, o canal verde da "
      "preferencial S7 nem as bocas brancas de S2/S8. A compra de 17/09 (8 rolos; "
      "`docs/separadores/plano_separadores_fila.md` §4) foi dimensionada com margem e continua valendo.\n")

    a("## 7. Conferir em campo antes de colar\n")
    for ac in achados:
        outro = "externo" if ac["trilho_com_vaos"] == "interno" else "interno"
        a(f"- **Topo da avenida {ac['avenida']}.** O trilho {ac['trilho_com_vaos']} (o dos vãos) acaba em "
          f"y = {virg(ac['topo_trilho_com_vaos'])} e o {outro} sobe até y = {virg(ac['topo_outro_trilho'])}: "
          f"{virg(ac['entra_na_banda_norte_m'])} m para dentro da banda norte, que começa em y = 35,40. "
          f"Dali para cima o trecho não serve a nenhum ramal e corta a banda por onde o eleitor de B caminha"
          + (f"; a mesa {', '.join(ac['mesas_norte_dentro'])} fica com a boca do ramal entre as duas fitas"
             if ac["mesas_norte_dentro"] else "")
          + f". Se o Posto encerrar os dois trilhos em y = {virg(ac['fim_sugerido'])}, poupa "
          f"{virg(ac['economia_fita_m'], 1)} m de fita. É mudança no desenho fechado de 17/09: decisão do "
          "Posto, não deste mapa.")
    a("- **Linha de espera dentro do serpenteado.** `data/decisoes.json` põe o serpenteado dos três grupos "
      "vermelhos encostado na frente do módulo (de 4,10 a 8,30 m da parede), então a linha de espera a 1,50 m "
      "cai dentro da primeira raia. Em campo: colar a linha zebrada a 1,50 m da mesa e começar a primeira "
      "raia da unifila depois dela.")
    a("- **O item `trilho_sul_A` do catálogo** (y = 3,40, de x = 11,00 a 25,03) coincide com o trilho interno "
      "de A até x = 21,83; o resto, de 21,83 a 25,03, fecharia a boca da avenida. Não colar além de 21,83. "
      "Ele entra na conta de fita branca de 17/09 (14 m) sem fazer falta na compra.")
    a("- **Fita no piso do RDS**: continua sem confirmação escrita (pendência 1 de `PENDENCIAS.md`).")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# A pagina
# --------------------------------------------------------------------------
def html_pagina(svg, dados, achados):
    md = md_lista(dados, achados)
    # converte as tabelas e listas do markdown num HTML simples (sem dependencia)
    corpo = []
    em_tabela = False
    for ln in md.splitlines():
        if ln.startswith("# "):
            continue
        if ln.startswith("|"):
            celulas = [c.strip() for c in ln.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in celulas):
                continue
            if not em_tabela:
                corpo.append('<div class="rolagem"><table>')
                em_tabela = True
                corpo.append("<tr>" + "".join(f"<th>{_inl(c)}</th>" for c in celulas) + "</tr>")
            else:
                corpo.append("<tr>" + "".join(f"<td>{_inl(c)}</td>" for c in celulas) + "</tr>")
            continue
        if em_tabela:
            corpo.append("</table></div>")
            em_tabela = False
        if ln.startswith("## "):
            corpo.append(f"<h2>{_inl(ln[3:])}</h2>")
        elif ln.startswith("- "):
            corpo.append(f"<ul><li>{_inl(ln[2:])}</li></ul>")
        elif ln.strip():
            corpo.append(f"<p>{_inl(ln)}</p>")
    if em_tabela:
        corpo.append("</table></div>")
    corpo_html = "\n".join(corpo).replace("</ul>\n<ul>", "\n")
    svg_resp = svg.replace('<svg xmlns', '<svg class="mapa-svg" xmlns', 1)
    return f"""<title>Montagem das Avenidas</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
/* Layout: folha de obra — mapa largo que rola na horizontal, lista de corte abaixo em tabelas. */
:root {{
  --fundo: #fbfaf8; --papel: #ffffff; --tinta: #16202b; --tinta-2: #4b5664; --fio: #d9dce2;
  --realce: #33507E; --aviso-fundo: #fff4e5; --aviso-fio: #DE7343;
  --fonte: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --fundo: #14181d; --papel: #1c2229; --tinta: #eef1f4; --tinta-2: #aab3bf; --fio: #333c47;
  --realce: #8fb0e8; --aviso-fundo: #3a2a1c; --aviso-fio: #DE7343; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --fundo: #14181d; --papel: #1c2229; --tinta: #eef1f4; --tinta-2: #aab3bf; --fio: #333c47;
  --realce: #8fb0e8; --aviso-fundo: #3a2a1c; --aviso-fio: #DE7343; color-scheme: dark; }}
body {{ background: var(--fundo); color: var(--tinta); font-family: var(--fonte); font-size: 15px;
  line-height: 1.5; margin: 0; }}
.pagina {{ max-width: 1180px; margin: 0 auto; padding-block: 24px 48px; padding-inline: 16px; }}
.topo {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px; }}
.topo .olho {{ font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--tinta-2); font-weight: 600; }}
h1 {{ font-size: clamp(22px, 3.2vw, 30px); margin: 0; line-height: 1.15; text-wrap: balance; }}
.topo p {{ margin: 0; color: var(--tinta-2); max-width: 70ch; }}
h2 {{ font-size: 19px; margin: 34px 0 10px; text-wrap: balance; }}
p {{ max-width: 75ch; }}
.regras {{ background: var(--papel); border: 1px solid var(--fio); border-left: 4px solid var(--realce);
  padding: 12px 16px; margin: 0 0 18px; }}
.regras ul, .regras li {{ margin: 0; }}
.regras li + li {{ margin-top: 4px; }}
.mapa {{ background: var(--papel); border: 1px solid var(--fio); overflow-x: auto; -webkit-overflow-scrolling: touch; }}
.mapa-svg {{ display: block; min-width: 1194px; width: 1194px; height: auto; }}
.dica {{ font-size: 13px; color: var(--tinta-2); margin: 6px 0 0; }}
.rolagem {{ overflow-x: auto; margin: 8px 0 14px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13.5px; font-variant-numeric: tabular-nums; min-width: 420px; }}
th, td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--fio); vertical-align: top; }}
th {{ font-size: 12px; letter-spacing: .04em; text-transform: uppercase; color: var(--tinta-2); background: var(--papel); }}
td code, p code, li code {{ font-family: var(--mono); font-size: .92em; }}
ul {{ padding-left: 20px; }}
li {{ margin: 4px 0; max-width: 80ch; }}
.aviso {{ background: var(--aviso-fundo); border: 1px solid var(--aviso-fio); padding: 12px 16px; }}
.rodape {{ margin-top: 36px; font-size: 12.5px; color: var(--tinta-2); border-top: 1px solid var(--fio); padding-top: 12px; }}
a {{ color: var(--realce); }}
</style>
<div class="pagina">
  <header class="topo">
    <div class="olho">Eleições 2026 · Posto de Dublin · RDS Hall 2 · montagem</div>
    <h1>Fita no chão do Hall 2: cada trecho em metros</h1>
    <p>Avenidas A, B e C, distribuidor do T, 28 ramais e linhas de espera. Medidas em metros, <code>x</code> da
    parede oeste e <code>y</code> da linha das portas da fachada sul. Geometria do desenho definitivo de 17/09,
    sem alteração. Gerado em {dados['gerado_em']}.</p>
  </header>
  <div class="regras"><ul>
    <li><strong>Unifila primeiro, fita depois.</strong> Traço grosso preto no mapa é unifila (bocas de A e C,
      avenida B inteira, serpenteados). A fita começa no círculo branco, onde o último poste acaba.</li>
    <li><strong>{virg(sf.LARG_AVENIDA)} m entre as duas fitas</strong> de cada avenida; 3,20 m só na boca da A.</li>
    <li><strong>Vão de {virg(sf.LARG_CANAL)} m só onde entra um ramal.</strong> Fora dos vãos a fita é contínua.</li>
    <li><strong>Linha de espera zebrada a {virg(sf.RECUO_MESA)} m da mesa</strong>, atravessando o canal de
      {virg(sf.LARG_CANAL)} m; marcas a cada {virg(sf.PASSO_FILA)} m dela para fora.</li>
  </ul></div>
  <div class="mapa">{svg_resp}</div>
  <p class="dica">No celular, arraste o mapa para o lado e amplie com dois dedos. A lista de corte completa
  está abaixo, trecho a trecho.</p>
  {corpo_html}
  <div class="rodape">Fonte: <code>scripts/separadores_montagem.py</code>, que lê a geometria de
  <code>scripts/separadores_fila.py</code> e os dados de <code>data/decisoes.json</code>,
  <code>data/prancheta_hall2.json</code> e <code>cenarios/paredes-abc-20260915.json</code>.
  Contexto do desenho: <code>docs/separadores/contexto.md</code>.</div>
</div>
"""


def _do_batente(d, lado):
    return f"no batente {lado}" if d < 0.05 else f"{virg(d)} m do batente {lado}"


def _inl(txt):
    """Negrito, codigo e setas do markdown de uma linha, em HTML."""
    import re
    txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"`(.+?)`", r"<code>\1</code>", txt)
    return txt


# --------------------------------------------------------------------------
def main():
    grava = "--grava" in sys.argv
    planta, dec, mesas, dados = monta()
    faixas, faltas = sf.confere(dec)
    if faltas:
        print("A geometria base falha na conferência de separadores_fila.py:")
        for f in faltas:
            print("   ", f)
        sys.exit(1)
    achados = conferencias(dados, mesas)

    print("Montagem da fita no Hall 2 — lista de corte (metros; x da parede oeste, y da linha das portas)\n")
    for b in dados["bocas"]:
        print(f"  Avenida {b['avenida']} na {b['porta']}: trilho interno x = {virg(b['trilho_interno_x'])} "
              f"({virg(b['interno_do_batente_oeste'])} do batente oeste), externo x = "
              f"{virg(b['trilho_externo_x'])} ({virg(b['externo_do_batente_leste'])} do batente leste), "
              f"entre fitas {virg(b['largura'])}")
    print()
    for aid, av in dados["avenidas"].items():
        print(f"  Avenida {aid} ({av['cor']}, {av['porta']} → {av['parede']})")
        for nome, tr in linhas_segmentos(av):
            print(f"    {nome}: {virg(tr['m'])} m = {virg(tr['barreira_m'])} unifila + {virg(tr['fita_m'])} fita")
            for s in tr["segmentos"]:
                fb = f"  (unifila até {pt(s['fim_barreira'])})" if "fim_barreira" in s else ""
                print(f"      {s['n']}. {pt(s['de'])} → {pt(s['ate'])}  {virg(s['m']):>6} m{fb}")
                if "pecas" in s:
                    print("         pedaços: " + " · ".join(virg(p["m"]) for p in s["pecas"]))
    d = dados["distribuidor_norte"]
    print(f"\n  Distribuidor do T, y = {virg(d['y'])}: {virg(d['fita_m'])} m de fita amarela em "
          f"{len(d['pecas'])} pedaços: " + " · ".join(virg(p["m"]) for p in d["pecas"]))
    pr = dados["premissas"]
    print("\n  Da fita à mesa: ", end="")
    print(" · ".join(f"{p_}: {virg(b - pr['modulo_m'] - pr['linha_espera_m'])} fila + "
                     f"{virg(pr['linha_espera_m'])} + {virg(pr['modulo_m'])} módulo = {virg(b)}"
                     for p_, b in pr["banda_por_parede_m"].items()))
    f = dados["fita_por_cor"]
    print(f"\n  Fita a colar (só o que está no mapa): azul {virg(f['A'], 1)} · amarelo {virg(f['B'], 1)} · "
          f"laranja {virg(f['C'], 1)} · zebrado {virg(f['espera'], 1)} m")
    if achados:
        print("\n  CONFERIR EM CAMPO:")
        for ac in achados:
            print(f"    avenida {ac['avenida']}: trilho {ac['trilho_com_vaos']} acaba em y = "
                  f"{virg(ac['topo_trilho_com_vaos'])}, o outro em y = {virg(ac['topo_outro_trilho'])} "
                  f"({virg(ac['entra_na_banda_norte_m'])} m dentro da banda norte); sugerido encerrar em "
                  f"y = {virg(ac['fim_sugerido'])}"
                  + (f"; mesa(s) da norte entre os trilhos: {', '.join(ac['mesas_norte_dentro'])}"
                     if ac["mesas_norte_dentro"] else ""))
    if not grava:
        print("\n(sem --grava: nada foi escrito)")
        return

    os.makedirs(SAIDAS, exist_ok=True)
    svg = svg_montagem(planta, dec, mesas, dados)
    escritos = []
    for nome, conteudo in (("montagem_fita_hall2.svg", svg),
                           ("montagem_fita_hall2.html", html_pagina(svg, dados, achados))):
        caminho = os.path.join(SAIDAS, nome)
        with open(caminho, "w", encoding="utf-8") as fh:
            fh.write(conteudo)
        escritos.append(caminho)
    caminho = os.path.join(SAIDAS, "montagem_fita_hall2.json")
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump({**dados, "conferir_em_campo": achados}, fh, ensure_ascii=False, indent=1)
    escritos.append(caminho)
    caminho = os.path.join(DOCS, "montagem_fita_hall2.md")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(md_lista(dados, achados))
    escritos.append(caminho)
    for c in escritos:
        print("escrito", os.path.relpath(c, RAIZ))


if __name__ == "__main__":
    main()
