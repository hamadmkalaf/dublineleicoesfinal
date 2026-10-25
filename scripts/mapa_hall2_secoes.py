#!/usr/bin/env python3
"""Planta do Hall 2 com as seções de cada mesa -> mapa/hall2_secoes.html.

Lê (não escreve) data/grupos_mesas.json, data/prancheta_hall2.json e
data/decisoes.json. Rotula por grupo de mesas e por seção, nunca por número de
mesa. Uso: python3 scripts/mapa_hall2_secoes.py
"""
import html
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "mapa" / "hall2_secoes.html"

grupos = json.load(open(RAIZ / "data/grupos_mesas.json"))["grupos"]
prancheta = json.load(open(RAIZ / "data/prancheta_hall2.json"))
decisoes = json.load(open(RAIZ / "data/decisoes.json"))

LARG, ALT = prancheta["salao"]["largura"], prancheta["salao"]["altura"]
X_LESTE = 47.3            # borda da faixa protegida de 3 m da fachada leste
S = 15                    # px por metro
ML, MT, MR, MB = 72, 30, 40, 78
W, H = ML + LARG * S + MR, MT + ALT * S + MB
MEIA_MESA, FUNDO, FRENTE = 0.85, 0.9, 1.7   # mesa de 1,7 m, 0,9 m a 1,7 m da parede

CLASSE = {k: v["hex"] for k, v in decisoes["classes"]["cores"].items()}
ROT_CLASSE = {k: v["rotulo"] for k, v in decisoes["classes"]["cores"].items()}


def px(x):
    return ML + x * S


def py(y):
    return MT + (ALT - y) * S


def ret(x1, y1, x2, y2, **attrs):
    a = " ".join(f'{k.rstrip("_").replace("_", "-")}="{v}"' for k, v in attrs.items())
    return (f'<rect x="{px(min(x1, x2)):.1f}" y="{py(max(y1, y2)):.1f}" '
            f'width="{abs(x2 - x1) * S:.1f}" height="{abs(y2 - y1) * S:.1f}" {a}/>')


def txt(x, y, s, **attrs):
    a = " ".join(f'{k.rstrip("_").replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<text x="{x:.1f}" y="{y:.1f}" {a}>{html.escape(str(s))}</text>'


# ---------- dados por mesa e conferência ----------
mesas, secoes = [], {}
for g in grupos:
    for i, coord in enumerate(g["coord"]):
        sec = g["por_mesa"][i]
        m = {"grupo": g["id"], "zona": g["entrada"], "parede": g["parede"],
             "porta": g["porta"], "coord": coord, "secoes": sec, "classe": g["classe"]}
        mesas.append(m)
        for s in sec:
            assert s not in secoes, f"seção {s} repetida"
            secoes[s] = m
assert len(mesas) == 28, len(mesas)
assert len(secoes) == 51, len(secoes)
aptos = {z: sum(g["aptos"] for g in grupos if g["entrada"] == z) for z in "ABC"}
esperado = {e["id"]: e["esperado"] for e in decisoes["entradas"]}
assert sum(aptos.values()) == 16794, aptos

# ---------- planta ----------
svg = []
contorno = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in prancheta["salao"]["contorno"])
svg.append(f'<polygon points="{contorno}" class="piso"/>')

# zonas protegidas e áreas sem mesa
svg.append(ret(X_LESTE, 0, LARG, ALT, class_="protegida"))
svg.append(txt(px(48.8), py(ALT / 2), "FAIXA LIVRE 3 m · EMERGÊNCIA L1–L4",
               class_="t-faixa", transform=f"rotate(90 {px(48.8):.1f} {py(ALT / 2):.1f})"))
svg.append(ret(0, 38.5, 7.8, ALT, class_="apoio"))
svg.append(txt(px(3.9), py(41.75), "sala de apoio", class_="t-area", text_anchor="middle"))
for z in decisoes["zonas_protegidas"]:
    if z["tipo"] == "recuo_porta" and z["porta"] in ("N2", "O2"):
        x1, y1, x2, y2 = z["rect"]
        svg.append(ret(x1, y1, x2, y2, class_="recuo"))

# serpentinas internas das três mesas grandes
for s in decisoes["serpenteados"]:
    x1, y1, x2, y2 = s["rect"]
    svg.append(ret(x1, y1, x2, y2, class_="serp"))
    cx, cy = px((x1 + x2) / 2), py((y1 + y2) / 2)
    svg.append(txt(cx, cy + 3, "fila 20", class_="t-serp", text_anchor="middle"))

# letras de zona ao fundo
for z, x, y in (("A", 11.5, 22), ("B", 25.5, 33.5), ("C", 39.5, 22)):
    svg.append(txt(px(x), py(y), z, class_=f"letra z{z}", text_anchor="middle"))

# portas
for p in prancheta["portas"]:
    x1, y1, x2, y2 = p["x1"], p["y1"], p["x2"], p["y2"]
    pid = p["id"]
    papel = decisoes["portas"].get(pid, {}).get("papel")
    if pid == "S7":
        cls, rot = "pref", "S7 · preferencial"
    elif papel == "entrada":
        z = decisoes["portas"][pid]["entrada"]
        cls, rot = f"ent z{z}", f"{pid} · entrada {z}"
    elif papel == "saida":
        cls, rot = "saida", f"{pid} · saída"
    elif p["estado"] == "fechada":
        cls, rot = "fechada", f"{pid} fechada"
    elif p["estado"] == "emergencia":
        cls, rot = "emerg", pid
    else:
        cls, rot = "livre", pid
    svg.append(f'<line x1="{px(x1):.1f}" y1="{py(y1):.1f}" x2="{px(x2):.1f}" '
               f'y2="{py(y2):.1f}" class="porta {cls}"/>')
    if p["face"] == "sul":
        mx = px((x1 + x2) / 2)
        if papel == "entrada":
            svg.append(txt(mx, py(0) + 22, pid, class_=f"t-ent z{z}", text_anchor="middle"))
            svg.append(txt(mx, py(0) + 37, f"entrada {z}", class_=f"t-ent2 z{z}", text_anchor="middle"))
        else:
            dy = 20 if pid == "S7" else 34
            svg.append(txt(mx, py(0) + dy, rot, class_=f"t-porta {cls}", text_anchor="middle"))
    elif p["face"] == "leste":
        svg.append(txt(px(LARG) + 5, py((y1 + y2) / 2) + 4, rot, class_="t-porta emerg"))
    elif p["face"] == "norte":
        svg.append(txt(px((x1 + x2) / 2), py(ALT) - 7, rot, class_="t-porta livre", text_anchor="middle"))
    elif p["face"] == "oeste":
        svg.append(txt(px(0) - 5, py((y1 + y2) / 2) + 4, rot, class_="t-porta livre",
                       text_anchor="end"))
svg.append(txt(px(25.15), py(0) + 62, "FACHADA SUL  ·  APRON 14 m  ·  RING 3 (pátio de fila)",
               class_="t-sul", text_anchor="middle"))

# mesas
for idx, m in enumerate(mesas):
    c, z, par = m["coord"], m["zona"], m["parede"]
    attrs = f'class="mesa z{z}" data-i="{idx}" tabindex="0" role="button" ' \
            f'aria-label="Grupo {m["grupo"]}, seções {" e ".join(map(str, m["secoes"]))}"'
    if par == "oeste":
        r = ret(FUNDO, c - MEIA_MESA, FRENTE, c + MEIA_MESA, class_="tampo")
        lx, ly, anc, dy = px(2.0), py(c), "start", 0
    elif par == "norte":
        r = ret(c - MEIA_MESA, ALT - FRENTE, c + MEIA_MESA, ALT - FUNDO, class_="tampo")
        lx, ly, anc, dy = px(c), py(ALT - 2.0), "middle", 1
    else:
        r = ret(X_LESTE - FRENTE, c - MEIA_MESA, X_LESTE - FUNDO, c + MEIA_MESA, class_="tampo")
        lx, ly, anc, dy = px(X_LESTE - 2.0), py(c), "end", 0
    secs = m["secoes"]
    linhas = []
    if dy:   # parede norte: rótulo abaixo da mesa
        base = ly + 11
    else:
        base = ly + 4 - (len(secs) - 1) * 6.5
    for k, s in enumerate(secs):
        linhas.append(txt(lx, base + k * 13, s, class_="t-sec" if k == 0 else "t-sec ag",
                          text_anchor=anc))
    dot = {"oeste": (px(FUNDO) - 0.1, py(c)), "norte": (px(c), py(ALT - FUNDO) + 0.1),
           "leste": (px(X_LESTE - FUNDO) + 0.1, py(c))}[par]
    svg.append(f'<g {attrs}>{r}<circle cx="{dot[0]:.1f}" cy="{dot[1]:.1f}" r="3.2" '
               f'fill="{CLASSE[m["classe"]]}" class="cls"/>{"".join(linhas)}</g>')

# grupos: marcador a 9,6 m da parede (fora das serpentinas), centrado no grupo
for g in grupos:
    c = sum(g["coord"]) / len(g["coord"])
    if g["parede"] == "oeste":
        cx, cy = px(9.6), py(c)
    elif g["parede"] == "norte":
        cx, cy = px(c), py(ALT - 9.6)
    else:
        cx, cy = px(X_LESTE - 9.6), py(c)
    svg.append(f'<g class="grupo z{g["entrada"]}" data-g="{g["id"]}">'
               f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13"/>'
               f'{txt(cx, cy + 4.5, g["id"], text_anchor="middle")}</g>')

# norte e escala
nx, ny = px(LARG) - 4, MT - 12
svg.append(f'<g class="norte"><path d="M{nx:.1f} {ny - 8:.1f} l5 12 l-5 -3 l-5 3 z"/>'
           f'{txt(nx, ny + 16, "N", text_anchor="middle")}</g>')
ex, ey = px(1), py(0) + 62
svg.append(f'<g class="escala"><line x1="{ex:.1f}" y1="{ey:.1f}" x2="{ex + 10 * S:.1f}" y2="{ey:.1f}"/>'
           f'<line x1="{ex:.1f}" y1="{ey - 4:.1f}" x2="{ex:.1f}" y2="{ey + 4:.1f}"/>'
           f'<line x1="{ex + 10 * S:.1f}" y1="{ey - 4:.1f}" x2="{ex + 10 * S:.1f}" y2="{ey + 4:.1f}"/>'
           f'{txt(ex + 5 * S, ey - 6, "10 m", text_anchor="middle")}</g>')

SVG = (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-labelledby="svg-t">'
       f'<title id="svg-t">Planta do Hall 2 com as seções de cada mesa</title>'
       f'<defs><pattern id="hach" width="6" height="6" patternUnits="userSpaceOnUse" '
       f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" class="hach"/></pattern></defs>'
       f'{"".join(svg)}</svg>')

# ---------- índice por zona ----------
NOME_PAREDE = {"A": "parede oeste", "B": "parede norte", "C": "parede leste"}
PORTA = {"A": "S4", "B": "S5", "C": "S6"}
colunas = []
for z in "ABC":
    linhas = []
    for g in [g for g in grupos if g["entrada"] == z]:
        secs = " · ".join(str(s) for s in sorted(g["secoes"]))
        linhas.append(f'<li data-g="{g["id"]}"><b class="chip z{z}">{g["id"]}</b>'
                      f'<span class="secs">{secs}</span></li>')
    colunas.append(
        f'<section class="zona z{z}"><header><span class="letra-z">{z}</span>'
        f'<div><strong>Porta {PORTA[z]} → {NOME_PAREDE[z]}</strong>'
        f'<small>{sum(len(g["coord"]) for g in grupos if g["entrada"] == z)} urnas · '
        f'{aptos[z]:,} aptos · {esperado[z]:,} esperados</small></div></header>'
        f'<ul>{"".join(linhas)}</ul></section>'.replace(",", "."))

ordenadas = "".join(
    f'<button type="button" class="s z{secoes[s]["zona"]}" data-s="{s}">'
    f'<span>{s}</span><em>{secoes[s]["grupo"]}</em></button>'
    for s in sorted(secoes))

DADOS = json.dumps({
    "mesas": [{k: m[k] for k in ("grupo", "zona", "parede", "porta", "secoes")} for m in mesas],
    "parede": NOME_PAREDE,
}, ensure_ascii=False)

pagina = (Path(__file__).with_name("mapa_hall2_secoes.tpl.html").read_text()
          .replace("{{SVG}}", SVG).replace("{{COLUNAS}}", "".join(colunas))
          .replace("{{ORDENADAS}}", ordenadas).replace("{{DADOS}}", DADOS)
          .replace("{{CLASSES}}", "".join(
              f'<span><i style="background:{CLASSE[k]}"></i>{ROT_CLASSE[k]}</span>'
              for k in ("alta", "media", "baixa"))))
SAIDA.write_text(pagina)
print(f"{SAIDA.relative_to(RAIZ)}: 28 mesas, 51 seções, aptos {aptos}")
