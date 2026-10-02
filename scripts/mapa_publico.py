#!/usr/bin/env python3
"""O mapa simplificado de apresentacao: da Merrion Road ate a mesa.

E a unica peca do projeto feita para **sair do projeto** -- vai para a internet
e para o briefing das equipes. Por isso ela nao mostra a barreira, a fita, os
grupos de mesa, os serpenteados nem as zonas protegidas: nada disso e decisao do
eleitor. Mostra o que ele precisa decidir, e so isso.

O que a folha tem:

  1. **O caminho** -- portao B na Merrion Road, a lateral leste do Hall 2, a
     entrada do Ring 3 pelo canto nordeste, as tres zonas e as tres portas.
  2. **O Hall 2** -- as 28 mesas rotuladas **so pelas secoes que votam nelas**,
     as portas A, B e C, as duas saidas, a entrada preferencial, e as avenidas:
     a de cada entrada, da porta ate a parede, e a de cada parede, da avenida
     ate a mesa.
  3. **Sua secao, sua porta** -- as 51 secoes em tres colunas.

Nenhum numero e digitado aqui. A geometria do salao sai de
``data/prancheta_hall2.json`` e ``cenarios/paredes-abc-20260915.json``, as
secoes de ``data/decisoes.json``, as cores de ``data/paleta.json`` e o Ring 3
de ``data/ring3_montagem.json`` -- copia da saida de ``ring3_montagem.py``, que
vive em hamadmkalaf/eleicoes2026.

O traco entre o portao e o apron **e esquematico**: o Hall 2, o apron e o Ring 3
estao em escala e em posicao relativa medida; a Merrion Road e o portao estao
no lugar certo em relacao ao salao, sem cota. A folha diz isso.

    python3 scripts/mapa_publico.py            confere e sai com codigo 1 se
                                               a folha estiver desatualizada
    python3 scripts/mapa_publico.py --grava    grava mapa/mapa_publico.html
"""
import json
import math
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import separadores_fila as SF          # geometria das avenidas e das mesas

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "mapa" / "mapa_publico.html"

P = json.loads((RAIZ / "data" / "paleta.json").read_text(encoding="utf-8"))
RING = json.loads((RAIZ / "data" / "ring3_montagem.json").read_text(encoding="utf-8"))

ZONA = {k: P["zona"][k]["hex"] for k in "ABC"}
TINTA = {k: P["zona"][k]["tinta"] for k in "ABC"}
PORTA = {k: P["zona"][k]["porta"] for k in "ABC"}
PAREDE = {k: P["zona"][k]["parede"] for k in "ABC"}
MARINHO = P["neutros"]["marinho"]["hex"]
CREME = P["neutros"]["creme"]["hex"]
REGUA = P["neutros"]["regua"]["hex"]
CINZA = P["neutros"]["cinza"]["hex"]
GRAFITE = P["identidade"]["grafite"]["hex"]
VERDE = P["identidade"]["verde"]["hex"]
PREF = P["preferencial"]["hex"]
FONTE_IMPORT = P["fonte"]["import"]
FONTE_CSS = P["fonte"]["css"]

br = lambda v: f"{v:.2f}".replace(".", ",")
br1 = lambda v: f"{v:.1f}".replace(".", ",")
APRON = 14.0          # sobrescrito em monta(), a partir da prancheta
sec = lambda n: f"{int(n):04d}"        # a secao e sempre lida com quatro digitos


# --------------------------------------------------------------------------
# Onde o Ring 3 encosta no Hall 2
# --------------------------------------------------------------------------
def encaixe(planta, dec):
    """Deslocamento em x entre a coordenada do Ring e a do salao, e o apron.

    Nao e digitado: sai de cada porta de entrada. O eixo da porta no Ring
    (``portas_eixo``) e o eixo dela na planta do salao tem de dar o mesmo
    deslocamento nas tres -- se um dia nao derem, o encaixe mudou e isto para.
    """
    eixo_hall = {}
    for p in planta["portas"]:
        papel = dec["sinalizacao_portas"].get(p["id"], {})
        if papel.get("papel") == "entrada":
            eixo_hall[papel["entrada"]] = (p["x1"] + p["x2"]) / 2
    desl = {k: round(eixo_hall[k] - RING["portas_eixo"][k], 3) for k in "ABC"}
    assert len(set(desl.values())) == 1, f"o Ring nao encaixa no salao: {desl}"
    return desl["A"], planta["decisoes"]["ring3"]["apron"]


# --------------------------------------------------------------------------
# Peça 1 — o caminho
# --------------------------------------------------------------------------
def svg_caminho(planta, dec):
    dx, apron = encaixe(planta, dec)
    RW, RD = RING["ring"]
    COR, PROF, UTIL = RING["corredor"], RD - RING["corredor"], RW - RING["corredor"]
    # coordenadas do salao: y = 0 e a fachada sul, +y para o norte, +x para leste.
    # o Ring vive em y negativo; ring_y cresce para o sul.
    rx = lambda x: x + dx
    ry = lambda y: -apron - y
    LARG, ALT = planta["salao"]["largura"], planta["salao"]["altura"]

    # a Merrion Road e o portao: posicao relativa certa, sem cota
    RUA_X, RUA_W = 60.0, 9.0
    PORTAO_Y = 33.0
    CALCADA = RUA_X - 1.6

    x0, x1 = -3.0, RUA_X + RUA_W + 1.0
    y0, y1 = ry(RD) - 7.0, ALT + 9.0
    S, M = 8.8, 8
    W = (x1 - x0) * S + 2 * M
    H = (y1 - y0) * S + 2 * M
    X = lambda x: M + (x - x0) * S
    Y = lambda y: M + (y1 - y) * S

    o = []
    a = o.append
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="mapa" role="img" '
      f'aria-label="Planta do percurso: o portão B na Merrion Road, a lateral leste do Hall 2, '
      f'o apron, o pátio do Ring 3 com as três zonas A, B e C, e as três portas do salão.">')
    a('<defs><marker id="pc" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="5.4" '
      'markerHeight="5.4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>'
      '</marker></defs>')

    # rua e calçada
    a(f'<rect x="{X(RUA_X):.1f}" y="{Y(y1):.1f}" width="{RUA_W*S:.1f}" height="{(y1-y0)*S:.1f}" '
      f'fill="var(--asfalto)"/>')
    a(f'<line x1="{X(RUA_X+RUA_W/2):.1f}" y1="{Y(y1):.1f}" x2="{X(RUA_X+RUA_W/2):.1f}" '
      f'y2="{Y(y0):.1f}" stroke="var(--faixa)" stroke-width="2" stroke-dasharray="14 12"/>')
    a(f'<text class="rua" x="{X(RUA_X+RUA_W/2):.1f}" y="{Y(ALT-4):.1f}" text-anchor="middle" '
      f'transform="rotate(-90 {X(RUA_X+RUA_W/2):.1f} {Y(ALT-4):.1f})">MERRION ROAD</text>')
    a(f'<line x1="{X(CALCADA):.1f}" y1="{Y(y1-2):.1f}" x2="{X(CALCADA):.1f}" y2="{Y(y0+2):.1f}" '
      f'stroke="var(--regua)" stroke-width="3"/>')

    # o salão
    cont = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in planta["salao"]["contorno"])
    a(f'<polygon points="{cont}" fill="var(--piso)" stroke="var(--tinta)" stroke-width="2.2"/>')
    a(f'<text class="rot" x="{X(LARG/2):.1f}" y="{Y(ALT/2):.1f}" text-anchor="middle">HALL 2</text>')
    a(f'<text class="rotp" x="{X(LARG/2):.1f}" y="{Y(ALT/2)+16:.1f}" text-anchor="middle">'
      f'o salão de votação</text>')

    # apron
    a(f'<rect x="{X(rx(0)):.1f}" y="{Y(0):.1f}" width="{RW*S:.1f}" height="{apron*S:.1f}" '
      f'fill="var(--apron)"/>')
    a(f'<text class="peq" x="{X(rx(3.0)):.1f}" y="{Y(-apron/2)+3:.1f}" text-anchor="start">'
      f'apron · {br1(apron)} m</text>')

    # o Ring 3
    a(f'<rect x="{X(rx(0)):.1f}" y="{Y(ry(0)):.1f}" width="{RW*S:.1f}" height="{RD*S:.1f}" '
      f'fill="var(--patio)" stroke="var(--tinta)" stroke-width="1.6" stroke-dasharray="7 5"/>')
    # corredor de chegada e trecho de fundo
    a(f'<rect x="{X(rx(UTIL)):.1f}" y="{Y(ry(0)):.1f}" width="{COR*S:.1f}" height="{RD*S:.1f}" '
      f'fill="var(--circ)"/>')
    a(f'<rect x="{X(rx(0)):.1f}" y="{Y(ry(PROF)):.1f}" width="{UTIL*S:.1f}" height="{COR*S:.1f}" '
      f'fill="var(--circ)"/>')
    a(f'<text class="peq" x="{X(rx(UTIL+COR/2)):.1f}" y="{Y(ry(PROF/2)):.1f}" text-anchor="middle" '
      f'transform="rotate(-90 {X(rx(UTIL+COR/2)):.1f} {Y(ry(PROF/2)):.1f})">corredor de chegada</text>')
    a(f'<text class="peq" x="{X(rx(UTIL/2)):.1f}" y="{Y(ry(PROF+COR/2))+3.5:.1f}" '
      f'text-anchor="middle">o corredor distribui as três filas: C, depois B, depois A</text>')

    # as três zonas
    for k in "ABC":
        za, zb = RING["x0"][k], RING["x0"][k] + RING["larguras"][k]
        a(f'<rect x="{X(rx(za)):.1f}" y="{Y(ry(0)):.1f}" width="{(zb-za)*S:.1f}" '
          f'height="{PROF*S:.1f}" fill="{ZONA[k]}" fill-opacity=".22" stroke="{ZONA[k]}" '
          f'stroke-width="1.4"/>')
        a(f'<text class="zona" x="{X(rx((za+zb)/2)):.1f}" y="{Y(ry(PROF/2)):.1f}" '
          f'text-anchor="middle" fill="var(--z{k.lower()}t)">{k}</text>')
        a(f'<text class="peq" x="{X(rx((za+zb)/2)):.1f}" y="{Y(ry(PROF/2))+17:.1f}" '
          f'text-anchor="middle">fila da porta {k}</text>')
        # a boca, no trecho de fundo
        ba, bb = RING["bocas_fundo"][k]["x"]
        a(f'<line x1="{X(rx(ba)):.1f}" y1="{Y(ry(PROF)):.1f}" x2="{X(rx(bb)):.1f}" '
          f'y2="{Y(ry(PROF)):.1f}" stroke="{ZONA[k]}" stroke-width="5"/>')
        # a saída da zona, e a travessia do apron até a porta
        sa, sb = RING["saidas_norte"][k]
        a(f'<line x1="{X(rx(sa)):.1f}" y1="{Y(ry(0)):.1f}" x2="{X(rx(sb)):.1f}" '
          f'y2="{Y(ry(0)):.1f}" stroke="{ZONA[k]}" stroke-width="5"/>')
        a(f'<line x1="{X(rx((sa+sb)/2)):.1f}" y1="{Y(ry(0))-2:.1f}" '
          f'x2="{X(RING["portas_eixo"][k]+dx):.1f}" y2="{Y(0)+4:.1f}" stroke="{ZONA[k]}" '
          f'stroke-width="2.6" marker-end="url(#pc)"/>')

    # as portas do salão, na fachada sul
    for p in planta["portas"]:
        s = dec["sinalizacao_portas"].get(p["id"], {})
        if s.get("papel") == "entrada":
            k = s["entrada"]
            a(f'<line x1="{X(p["x1"]):.1f}" y1="{Y(0):.1f}" x2="{X(p["x2"]):.1f}" y2="{Y(0):.1f}" '
              f'stroke="{ZONA[k]}" stroke-width="7"/>')
            a(f'<text class="porta" x="{X((p["x1"]+p["x2"])/2):.1f}" y="{Y(0)-7:.1f}" '
              f'text-anchor="middle" fill="var(--z{k.lower()}t)">{k}</text>')
        elif s.get("papel") == "preferencial":
            a(f'<line x1="{X(p["x1"]):.1f}" y1="{Y(0):.1f}" x2="{X(p["x2"]):.1f}" y2="{Y(0):.1f}" '
              f'stroke="{PREF}" stroke-width="7"/>')
            a(f'<text class="peq" x="{X(p["x2"])+6:.1f}" y="{Y(0)-9:.1f}" '
              f'text-anchor="start" fill="{PREF}">preferencial</text>')
        elif s.get("papel") == "saida":
            a(f'<line x1="{X(p["x1"]):.1f}" y1="{Y(0):.1f}" x2="{X(p["x2"]):.1f}" y2="{Y(0):.1f}" '
              f'stroke="var(--saida)" stroke-width="7"/>')
            a(f'<text class="peq" x="{X((p["x1"]+p["x2"])/2):.1f}" y="{Y(0)+15:.1f}" '
              f'text-anchor="middle">saída</text>')

    # o percurso de chegada, do portão ao canto nordeste do Ring
    cx = LARG + 4.0
    rota = [(CALCADA, PORTAO_Y), (cx, PORTAO_Y), (cx, ry(0) + 1.5),
            (rx(UTIL + COR / 2), ry(0) + 1.5), (rx(UTIL + COR / 2), ry(2.5))]
    pts = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in rota)
    a(f'<polyline points="{pts}" fill="none" stroke="var(--rota)" stroke-width="3.4" '
      f'stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="11 7" '
      f'marker-end="url(#pc)"/>')

    # o portão e os passos
    a(f'<circle cx="{X(CALCADA):.1f}" cy="{Y(PORTAO_Y):.1f}" r="7" fill="var(--rota)"/>')
    zbc = rx(RING["x0"]["B"] + RING["larguras"]["B"] / 2)
    passos = [(CALCADA - 11.8, PORTAO_Y, "1"),
              (cx + 2.4, PORTAO_Y - 20, "2"),
              (rx(RW) + 2.6, ry(9), "3"),
              (zbc, ry(25.5), "4"),
              (RING["portas_eixo"]["B"] + dx, -3.4, "5")]
    for px, py, n in passos:
        a(f'<circle cx="{X(px):.1f}" cy="{Y(py):.1f}" r="9.5" fill="var(--rota)"/>')
        a(f'<text class="passo" x="{X(px):.1f}" y="{Y(py)+3.8:.1f}" text-anchor="middle">{n}</text>')
    a(f'<text class="portao" x="{X(CALCADA)-14:.1f}" y="{Y(PORTAO_Y)+4:.1f}" text-anchor="end">'
      f'PORTÃO B</text>')
    a(f'<text class="peq" x="{X(CALCADA)-14:.1f}" y="{Y(PORTAO_Y)+18:.1f}" text-anchor="end">'
      f'entrada do eleitor</text>')
    a(f'<text class="peq" x="{X(cx)-9:.1f}" y="{Y(12):.1f}" transform="rotate(-90 '
      f'{X(cx)-9:.1f} {Y(12):.1f})" text-anchor="middle">lateral leste do Hall 2</text>')
    a(f'<text class="peq" x="{X(LARG/2):.1f}" y="{Y(ALT/2)+32:.1f}" text-anchor="middle">'
      f'as 28 mesas ficam nas paredes — ver o mapa do salão abaixo</text>')

    # norte
    a(f'<g transform="translate({X(x0+3.4):.1f} {Y(y1-4.5):.1f})">'
      f'<line x1="0" y1="14" x2="0" y2="-9" stroke="var(--tinta)" stroke-width="1.8" '
      f'marker-end="url(#pc)"/>'
      f'<text class="peq" x="0" y="26" text-anchor="middle">N</text></g>')
    # escala
    ex, ey = x0 + 2.0, y0 + 3.0
    a(f'<line x1="{X(ex):.1f}" y1="{Y(ey):.1f}" x2="{X(ex+20):.1f}" y2="{Y(ey):.1f}" '
      f'stroke="var(--tinta)" stroke-width="2"/>')
    for m in (0, 10, 20):
        a(f'<line x1="{X(ex+m):.1f}" y1="{Y(ey)-4:.1f}" x2="{X(ex+m):.1f}" y2="{Y(ey)+4:.1f}" '
          f'stroke="var(--tinta)" stroke-width="1.4"/>')
    a(f'<text class="peq" x="{X(ex+20)+7:.1f}" y="{Y(ey)+4:.1f}">20 m</text>')
    a('</svg>')
    return "\n".join(o)


# --------------------------------------------------------------------------
# Peça 2 — o Hall 2
# --------------------------------------------------------------------------
def svg_hall(planta, dec, mesas):
    LARG, ALT = planta["salao"]["largura"], planta["salao"]["altura"]
    PROFM, LARGM = planta["modulo"]["prof"], planta["modulo"]["larg"]
    S, M = 21.0, 34
    W, H = LARG * S + 2 * M, ALT * S + 2 * M + 58
    X = lambda x: M + x * S
    Y = lambda y: M + (ALT - y) * S

    o = []
    a = o.append
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="mapa mapa--hall" role="img" '
      f'aria-label="Planta simplificada do Hall 2: as 28 mesas encostadas nas paredes oeste, norte '
      f'e leste, cada uma rotulada pelas seções que votam nela; as portas A, B e C na fachada sul, '
      f'a entrada preferencial, as duas saídas, e as avenidas que levam de cada porta à sua parede '
      f'e da avenida a cada mesa.">')
    a('<defs><marker id="ph" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="5" '
      'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>'
      '</marker></defs>')
    cont = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in planta["salao"]["contorno"])
    a(f'<polygon points="{cont}" fill="var(--piso)" stroke="var(--tinta)" stroke-width="2.4"/>')

    # ---- as avenidas da parede: da avenida de entrada até a boca de cada mesa ----
    faixa = {}
    for par, k in (("oeste", "A"), ("norte", "B"), ("leste", "C")):
        banda = SF.BANDA_PAREDE[par]
        ys = [m["y"] if par == "norte" else m["y"] for m in mesas if m["parede"] == par]
        xs = [m["x"] for m in mesas if m["parede"] == par]
        if par == "oeste":
            r = (PROFM, min(ys) - 1.4, banda, max(ys) + 1.4)
        elif par == "leste":
            r = (47.3 - banda, min(ys) - 1.4, 47.3 - PROFM, max(ys) + 1.4)
        else:
            r = (min(xs) - 1.4, ALT - banda, max(xs) + 1.4, ALT - PROFM)
        faixa[par] = r
        a(f'<rect x="{X(r[0]):.1f}" y="{Y(r[3]):.1f}" width="{(r[2]-r[0])*S:.1f}" '
          f'height="{(r[3]-r[1])*S:.1f}" fill="{ZONA[k]}" fill-opacity=".10"/>')

    # ---- as avenidas de entrada: a faixa entre os dois trilhos ----
    for k, av in SF.AVENIDAS.items():
        pol = av["trilho_interno"] + list(reversed(av["trilho_externo"]))
        pts = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in pol)
        a(f'<polygon points="{pts}" fill="{ZONA[k]}" fill-opacity=".22"/>')
        # a seta de sentido, no eixo, perto da porta
        p0 = av["trilho_interno"][0]
        p1 = av["trilho_externo"][0]
        exi = (p0[0] + p1[0]) / 2
        a(f'<line x1="{X(exi):.1f}" y1="{Y(1.2):.1f}" x2="{X(exi):.1f}" y2="{Y(7.5):.1f}" '
          f'stroke="{ZONA[k]}" stroke-width="3" marker-end="url(#ph)"/>')
    # a pequena avenida da parede norte
    a(f'<rect x="{X(SF.X_AVENIDA_NORTE[0]):.1f}" y="{Y(SF.Y_BANDA_NORTE):.1f}" '
      f'width="{(SF.X_AVENIDA_NORTE[1]-SF.X_AVENIDA_NORTE[0])*S:.1f}" '
      f'height="{SF.AVENIDA_NORTE*S:.1f}" fill="{ZONA["B"]}" fill-opacity=".22"/>')
    for de, para in ((26.4, 15.0), (30.2, 34.0)):
        ym = SF.Y_BANDA_NORTE - SF.AVENIDA_NORTE / 2
        a(f'<line x1="{X(de):.1f}" y1="{Y(ym):.1f}" x2="{X(para):.1f}" y2="{Y(ym):.1f}" '
          f'stroke="{ZONA["B"]}" stroke-width="3" marker-end="url(#ph)"/>')

    # ---- as 28 mesas, rotuladas só pelas seções ----
    for m in mesas:
        k = m["entrada"]
        dxm, dym = m["dx"], m["dy"]
        pxm, pym = -dym, dxm
        L = LARGM / 2
        cantos = [(m["x"] + pxm * L, m["y"] + pym * L),
                  (m["x"] - pxm * L, m["y"] - pym * L),
                  (m["x"] - pxm * L + dxm * PROFM, m["y"] - pym * L + dym * PROFM),
                  (m["x"] + pxm * L + dxm * PROFM, m["y"] + pym * L + dym * PROFM)]
        pts = " ".join(f"{X(cx):.1f},{Y(cy):.1f}" for cx, cy in cantos)
        a(f'<rect x="0" y="0" width="0" height="0" fill="none"/>'
          if False else
          f'<polygon points="{pts}" fill="{ZONA[k]}" stroke="var(--tinta)" stroke-width=".8" '
          f'rx="2"/>')
        # a seta curta que liga a avenida da parede à boca da mesa
        bx = m["x"] + dxm * (PROFM + 1.9)
        by = m["y"] + dym * (PROFM + 1.9)
        a(f'<line x1="{X(bx):.1f}" y1="{Y(by):.1f}" '
          f'x2="{X(m["x"] + dxm*(PROFM+0.35)):.1f}" y2="{Y(m["y"] + dym*(PROFM+0.35)):.1f}" '
          f'stroke="{ZONA[k]}" stroke-width="1.6" marker-end="url(#ph)" opacity=".85"/>')
        rot = " ".join(sec(s) for s in m["secoes"])
        gx, gy = X(m["x"] + dxm * PROFM / 2), Y(m["y"] + dym * PROFM / 2)
        giro = -90 if m["parede"] == "norte" else 0
        tr = f' transform="rotate({giro} {gx:.1f} {gy:.1f})"' if giro else ""
        a(f'<text class="mesa" x="{gx:.1f}" y="{gy+3.6:.1f}" text-anchor="middle" '
          f'fill="{TINTA[k]}"{tr}>{rot}</text>')

    # ---- as portas ----
    for p in planta["portas"]:
        s = dec["sinalizacao_portas"].get(p["id"], {})
        papel = s.get("papel")
        if papel not in ("entrada", "saida", "preferencial"):
            continue
        cor = ZONA[s["entrada"]] if papel == "entrada" else (
            PREF if papel == "preferencial" else "var(--saida)")
        a(f'<line x1="{X(p["x1"]):.1f}" y1="{Y(p["y1"]):.1f}" x2="{X(p["x2"]):.1f}" '
          f'y2="{Y(p["y2"]):.1f}" stroke="{cor}" stroke-width="9" stroke-linecap="butt"/>')
        cxp = (p["x1"] + p["x2"]) / 2
        if papel == "entrada":
            a(f'<text class="portaH" x="{X(cxp):.1f}" y="{Y(0)+26:.1f}" text-anchor="middle" '
              f'fill="var(--z{s["entrada"].lower()}t)">{s["entrada"]}</text>')
            a(f'<text class="peq" x="{X(cxp):.1f}" y="{Y(0)+40:.1f}" text-anchor="middle">'
              f'entrada</text>')
        elif papel == "preferencial":
            a(f'<text class="peq2" x="{X(cxp):.1f}" y="{Y(0)+26:.1f}" text-anchor="middle" '
              f'fill="{cor}">preferencial</text>')
        else:
            a(f'<text class="peq2" x="{X(cxp):.1f}" y="{Y(0)+26:.1f}" text-anchor="middle" '
              f'fill="var(--saida)">saída</text>')

    # ---- a volta: quem votou sai pela banda da sua parede ----
    for (x_de, y_de), (x_para, y_para) in (((6.0, 12.0), (13.85, 2.4)),
                                           ((43.0, 12.0), (42.7, 2.4))):
        a(f'<line x1="{X(x_de):.1f}" y1="{Y(y_de):.1f}" x2="{X(x_para):.1f}" y2="{Y(y_para):.1f}" '
          f'stroke="var(--saida)" stroke-width="2" stroke-dasharray="3 5" '
          f'marker-end="url(#ph)" opacity=".85"/>')

    a(f'<text class="peq" x="{X(LARG/2):.1f}" y="{H-14:.1f}" text-anchor="middle">'
      f'planta em escala · fachada sul embaixo, como quem chega do Ring 3</text>')
    a('</svg>')
    return "\n".join(o)


# --------------------------------------------------------------------------
# A folha
# --------------------------------------------------------------------------
def monta():
    global APRON
    planta, dec, cen = SF.carrega()
    APRON = planta["decisoes"]["ring3"]["apron"]
    mesas = SF.monta_mesas(planta, dec, cen)
    por_porta = {k: sorted({s for m in mesas if m["entrada"] == k for s in m["secoes"]})
                 for k in "ABC"}
    total = sum(len(v) for v in por_porta.values())
    assert total == 51, f"as seções não fecham em 51: {total}"

    colunas = []
    for k in "ABC":
        itens = " ".join(f'<span>{sec(s)}</span>' for s in por_porta[k])
        colunas.append(
            f'<div class="col" style="--z:{ZONA[k]};--t:{TINTA[k]}">'
            f'<h3><b>{k}</b> porta {PORTA[k]} · parede {PAREDE[k]}</h3>'
            f'<p class="n">{len(por_porta[k])} seções</p>'
            f'<div class="secs">{itens}</div></div>')

    passos = [
        ("Portão B, na Merrion Road",
         "É por ali que o eleitor entra. Antes do portão há uma mesa de consulta: "
         "quem não sabe o número da sua seção descobre ali, e anota a letra da porta. "
         "Depois do portão, tudo pressupõe a seção conhecida."),
        ("Pela lateral leste do Hall 2",
         "O caminho contorna o salão pelo lado leste e desemboca no apron, a faixa "
         f"pavimentada de {br1(APRON)} m entre o Hall 2 e o pátio."),
        ("Ring 3, pelo canto nordeste",
         "O pátio de fila fica ao ar livre, ao sul do salão. Entra-se pelo canto "
         "nordeste e desce-se pelo corredor de chegada; no fundo, o corredor distribui "
         "para as três zonas: <b>C primeiro, B depois, A no fim</b>."),
        ("A sua zona, a sua fila",
         "Cada zona é a fila de uma porta, e as três têm o mesmo tamanho. Entra-se pela "
         "boca no fundo, sobe-se a fila e sai-se pela abertura da frente — a que fica "
         "em frente à sua porta."),
        ("A porta A, B ou C",
         "Atravessado o apron, cada zona entra pela sua porta. Da porta até a mesa é "
         "sempre a mesma letra: a avenida da sua cor leva à parede, e a avenida da "
         "parede leva à sua seção."),
    ]
    lista = "\n".join(
        f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in passos)


    return TEMPLATE.format(
        fonte_import=FONTE_IMPORT, fonte_css=FONTE_CSS,
        creme=CREME, regua=REGUA, cinza=CINZA, grafite=GRAFITE, marinho=MARINHO,
        verde=VERDE, pref=PREF, za=ZONA["A"], zb=ZONA["B"], zc=ZONA["C"],
        lista=lista, colunas="\n".join(colunas),
        caminho=svg_caminho(planta, dec), hall=svg_hall(planta, dec, mesas),
        lotacao=f"{RING['lotacao']:,}".replace(",", "."),
        zonas=br(RING["larguras"]["A"]), apron=br1(APRON),
        urnas=len(mesas), secoes=total,
        aptos=f"{dec['comparecimento']['aptos']:,}".replace(",", "."),
    )


TEMPLATE = """<title>Onde você vota no RDS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonte_import}">
<style>
:root {{
  color-scheme: light;
  --ground:{creme}; --piso:#FFFFFF; --tinta:{marinho}; --regua:{regua};
  --cinza:{cinza};  --grafite:{grafite};
  --apron:#E4E0CF;  --patio:#EDEADB; --circ:#DBD6C2; --asfalto:#D8D3C3;
  --faixa:#FFFFFF;  --rota:{verde};  --saida:{grafite};
  --cartao:#FBFAF4; --sombra:0 1px 0 {regua}, 0 10px 26px rgba(4,43,90,.07);
  --za:{za}; --zb:{zb}; --zc:{zc}; --pref:{pref};
  /* o hex do rolo pinta a faixa; a TINTA de zona é outra coisa, e precisa de
     contraste sobre o fundo de cada tema */
  --zat:{za}; --zbt:#9A7C00; --zct:{zc};
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --ground:#0A1B30; --piso:#132741; --tinta:#F1ECDC; --regua:#284566;
    --cinza:#A9B7C9;  --grafite:#CBD5E1;
    --apron:#1B3452;  --patio:#17304C; --circ:#22405F; --asfalto:#16293F;
    --faixa:#4C6684;  --rota:#8FBF54;  --saida:#CBD5E1;
    --cartao:#122438; --sombra:0 1px 0 #284566, 0 10px 26px rgba(0,0,0,.35);
    --zat:#8FADE0; --zbt:#F2D45C; --zct:#FF8497;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --ground:#0A1B30; --piso:#132741; --tinta:#F1ECDC; --regua:#284566;
  --cinza:#A9B7C9;  --grafite:#CBD5E1;
  --apron:#1B3452;  --patio:#17304C; --circ:#22405F; --asfalto:#16293F;
  --faixa:#4C6684;  --rota:#8FBF54;  --saida:#CBD5E1;
  --cartao:#122438; --sombra:0 1px 0 #284566, 0 10px 26px rgba(0,0,0,.35);
  --zat:#8FADE0; --zbt:#F2D45C; --zct:#FF8497;
}}

* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--tinta);
  font-family:{fonte_css}; font-size:16px; line-height:1.55;
  -webkit-text-size-adjust:100%;
}}
.folha {{ max-width:1080px; margin:0 auto; padding-inline:18px; padding-block:0 56px; }}

header.topo {{ padding-block:38px 26px; border-bottom:3px solid var(--tinta); }}
.olho {{
  margin:0 0 10px; font-size:11.5px; font-weight:700; letter-spacing:.16em;
  text-transform:uppercase; color:var(--cinza);
}}
h1 {{
  margin:0; font-size:clamp(30px,6.4vw,54px); font-weight:900; line-height:1.03;
  letter-spacing:-.022em; text-wrap:balance;
}}
h1 em {{ font-style:normal; color:var(--rota); }}
.chamada {{
  margin:16px 0 0; max-width:62ch; font-size:clamp(15px,2.3vw,18px); font-weight:500;
}}
.carimbo {{
  display:flex; flex-wrap:wrap; gap:10px 30px; margin:22px 0 0; padding:0; list-style:none;
}}
.carimbo li {{ display:flex; flex-direction:column; }}
.carimbo b {{ font-size:22px; font-weight:800; font-variant-numeric:tabular-nums; }}
.carimbo span {{ font-size:11.5px; font-weight:600; letter-spacing:.07em;
  text-transform:uppercase; color:var(--cinza); }}

section {{ padding-block:40px 0; }}
.rotulo {{
  margin:0 0 6px; font-size:11.5px; font-weight:800; letter-spacing:.16em;
  text-transform:uppercase; color:var(--rota);
}}
h2 {{ margin:0 0 6px; font-size:clamp(22px,3.6vw,30px); font-weight:800;
  letter-spacing:-.014em; text-wrap:balance; }}
.sub {{ margin:0 0 22px; max-width:64ch; color:var(--cinza); font-size:15px; }}

ol.passos {{
  counter-reset:p; list-style:none; margin:0 0 26px; padding:0;
  display:grid; gap:14px 22px; grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
}}
ol.passos li {{ counter-increment:p; position:relative; padding-left:42px; }}
ol.passos li::before {{
  counter-reset:none; content:counter(p); position:absolute; left:0; top:1px;
  width:28px; height:28px; border-radius:50%; background:var(--rota); color:#fff;
  font-size:14px; font-weight:800; display:grid; place-items:center;
}}
ol.passos h3 {{ margin:2px 0 3px; font-size:15.5px; font-weight:800; }}
ol.passos p {{ margin:0; font-size:14px; color:var(--cinza); }}

figure {{ margin:0; }}
.quadro {{
  background:var(--cartao); border:1px solid var(--regua); border-radius:10px;
  box-shadow:var(--sombra); padding:14px; overflow-x:auto;
}}
svg.mapa {{ display:block; width:100%; height:auto; min-width:520px; }}
svg.mapa--hall {{ min-width:880px; }}
figcaption {{ margin-top:12px; font-size:13px; color:var(--cinza); max-width:70ch; }}

svg.mapa text {{ font-family:{fonte_css}; }}
svg .rot   {{ font-size:19px; font-weight:900; letter-spacing:.1em; fill:var(--tinta); }}
svg .rotp  {{ font-size:11px; font-weight:600; fill:var(--cinza); }}
svg .rua   {{ font-size:12px; font-weight:800; letter-spacing:.2em; fill:var(--cinza); }}
svg .peq   {{ font-size:10.5px; font-weight:600; fill:var(--cinza); }}
svg .peq2  {{ font-size:11.5px; font-weight:800; }}
svg .zona  {{ font-size:30px; font-weight:900; }}
svg .porta {{ font-size:17px; font-weight:900; }}
svg .portaH{{ font-size:21px; font-weight:900; }}
svg .passo {{ font-size:12px; font-weight:800; fill:#fff; }}
svg .portao{{ font-size:13px; font-weight:900; fill:var(--rota); letter-spacing:.05em; }}
svg .mesa  {{ font-size:10.5px; font-weight:700; font-variant-numeric:tabular-nums;
  letter-spacing:.02em; }}

.colunas {{ display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); }}
.col {{
  background:var(--cartao); border:1px solid var(--regua); border-top:5px solid var(--z);
  border-radius:8px; padding:16px 16px 18px;
}}
.col h3 {{ margin:0; font-size:14.5px; font-weight:700; display:flex; align-items:center; gap:10px; }}
.col h3 b {{
  width:32px; height:32px; border-radius:6px; background:var(--z); color:var(--t);
  display:grid; place-items:center; font-size:19px; font-weight:900; flex:none;
}}
.col .n {{ margin:8px 0 12px; font-size:12px; font-weight:600; color:var(--cinza);
  letter-spacing:.06em; text-transform:uppercase; }}
.secs {{ display:flex; flex-wrap:wrap; gap:6px; }}
.secs span {{
  font-size:13.5px; font-weight:700; font-variant-numeric:tabular-nums;
  padding:3px 7px; border-radius:4px; background:var(--z); color:var(--t);
}}

.aviso {{
  margin-top:22px; padding:14px 16px; border-left:4px solid var(--pref);
  background:var(--cartao); border-radius:0 8px 8px 0; font-size:14.5px;
}}
.aviso b {{ color:var(--pref); }}
footer {{
  margin-top:44px; padding-top:18px; border-top:1px solid var(--regua);
  font-size:12.5px; color:var(--cinza); max-width:74ch;
}}
@media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; transition:none !important; }} }}
</style>

<div class="folha">
<header class="topo">
  <p class="olho">Eleições 2026 · 1º turno · domingo, 4 de outubro · 8h às 17h</p>
  <h1>Onde você vota no <em>RDS</em></h1>
  <p class="chamada">Todas as seções da Irlanda votam num único lugar: o <b>Hall 2 do RDS</b>,
  na Merrion Road, em Ballsbridge. O caminho é o mesmo para todo mundo — muda só uma coisa,
  e é a <b>letra da sua porta</b>. Descubra o número da sua seção antes de sair de casa:
  com ele, a letra está no fim desta página.</p>
  <ul class="carimbo">
    <li><b>{secoes}</b><span>seções</span></li>
    <li><b>{urnas}</b><span>urnas</span></li>
    <li><b>{aptos}</b><span>eleitores aptos</span></li>
    <li><b>3</b><span>portas: A, B e C</span></li>
  </ul>
</header>

<section>
  <p class="rotulo">Passo a passo</p>
  <h2>Da calçada até a urna</h2>
  <p class="sub">Cinco trechos. A letra da sua porta aparece em todos eles — no portão, na
  lateral do salão, na entrada do pátio e na própria porta.</p>
  <ol class="passos">
{lista}
  </ol>
  <figure>
    <div class="quadro">{caminho}</div>
    <figcaption><b>O caminho.</b> O Hall 2, o apron de {apron} m e o pátio do Ring 3 estão em
    escala e na posição relativa medida em planta. O trecho entre o portão e o apron é
    esquemático: indica o lado por onde se anda, não a distância. As três zonas do pátio têm
    {zonas} m cada e comportam {lotacao} pessoas ao todo.</figcaption>
  </figure>
  <p class="aviso"><b>Atendimento preferencial.</b> Idoso, gestante, pessoa com deficiência e
  quem os acompanha entram pela porta preferencial, à direita da porta C, <b>sem fila</b>.</p>
</section>

<section>
  <p class="rotulo">Dentro do salão</p>
  <h2>O Hall 2</h2>
  <p class="sub">As mesas ficam encostadas nas paredes, e cada parede é de uma porta: a porta A
  vota na parede oeste, a B na norte, a C na leste. As mesas não têm número — cada uma traz as
  <b>seções que votam nela</b>, que é o que você tem na mão.</p>
  <figure>
    <div class="quadro">{hall}</div>
    <figcaption><b>O salão.</b> Da porta, a avenida da sua cor leva até a parede; da avenida da
    parede, um passo até a sua seção. Quem votou volta pela mesma faixa da parede e sai pelas
    saídas da fachada sul — ninguém atravessa a avenida de quem está entrando.</figcaption>
  </figure>
</section>

<section>
  <p class="rotulo">Sua seção, sua porta</p>
  <h2>Ache o seu número</h2>
  <p class="sub">As {secoes} seções da Irlanda, repartidas pelas três portas. Anote a letra: você
  vai procurá-la três vezes no caminho.</p>
  <div class="colunas">
{colunas}
  </div>
</section>

<footer>
  <p>Royal Dublin Society, Hall 2 · Merrion Road, Ballsbridge, Dublin 4, D04 AK83. Entrada de
  eleitores pelo portão B, na Merrion Road. Planta do salão e posição das mesas medidas sobre a
  planta oficial do RDS; geometria do pátio gerada do mesmo desenho que produz a folha de
  montagem do Ring 3. Página gerada por <code>scripts/mapa_publico.py</code>.</p>
  <p>Consulte sempre o seu local e a sua seção no site do TSE antes de sair de casa.</p>
</footer>
</div>
"""


def main():
    grava = "--grava" in sys.argv[1:]
    novo = monta()
    atual = PAGINA.read_text(encoding="utf-8") if PAGINA.exists() else ""
    if novo == atual:
        print("mapa/mapa_publico.html em dia")
        return 0
    if grava:
        PAGINA.write_text(novo, encoding="utf-8")
        print(f"gravado mapa/mapa_publico.html ({len(novo)} bytes)")
        return 0
    print("mapa/mapa_publico.html difere do gerador; rode com --grava", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
