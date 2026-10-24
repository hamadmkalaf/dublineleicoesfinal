#!/usr/bin/env python3
"""O mapa "O Hall 2" em alta resolução, com as mesas ampliadas.

É o slide 3 de ``saidas/onde_voce_vota.pptx`` redesenhado como **SVG vetorial**
(escala livre, fonte Montserrat embutida) e rasterizado em PNG de 7500 x 5150 px.
Sai dos mesmos dados do deck (``separadores_fila``, ``mapa_publico``): nada de
geometria é digitado aqui, exceto o que é só apresentação.

**Mesas ampliadas, de propósito.** Cada mesa é desenhada com ``LARG_DESENHO`` de
largura (a real é 0,9 m) para caber o número da seção em corpo legível, com as
seções empilhadas, uma por linha. A **posição** (centro na parede) e a **profundidade**
(4,1 m) são as da planta. O mínimo entre centros vizinhos é 2,4 m, então 2,2 m
não sobrepõe nenhuma; ``confere()`` reprova se um dia sobrepuser. A folha diz isso
no rodapé.

    python3 scripts/mapa_hall_alta.py            confere (sem gravar)
    python3 scripts/mapa_hall_alta.py --grava    grava as duas versões (SVG e PNG) em saidas/

O PNG usa o Chromium do Playwright (``PLAYWRIGHT_BROWSERS_PATH``); sem ele só o
SVG é gravado.
"""
import base64
import glob
import os
import subprocess
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapa_publico as MP
import separadores_fila as SF

RAIZ = MP.RAIZ
# variante -> (largura desenhada da mesa em m, corpo com 2 seções, corpo com 1 seção)
#   padrão  : mesas mais largas, números maiores, 0,2 m de folga entre vizinhas
#   pares   : mesas mais estreitas, 0,6 m de folga entre vizinhas (4 vezes a do padrão)
VARIANTES = {"": (2.2, 17.5, 22), "_pares": (1.8, 14.5, 20)}
SAIDAS = RAIZ / "saidas"
caminho = lambda var, ext: SAIDAS / f"hall2_alta_resolucao{var}.{ext}"
FONTES = RAIZ / "data" / "fontes"

W, H = 1500, 1030
S = 17.8                     # unidades de SVG por metro
MX, MY = 50, 125             # canto noroeste do salão
ESCALA_PX = 5                # 1500 x 1030 -> 7500 x 5150
TXT_B = "#9A7C00"            # amarelo do rolo não se lê em texto (igual ao deck)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def fonte_css():
    faces = []
    for peso in (400, 700, 900):
        f = FONTES / f"montserrat-latin-{peso}-normal.woff2"
        b64 = base64.b64encode(f.read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'Montserrat';font-weight:{peso};"
                     f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "".join(faces)


def confere(mesas, LARG_DESENHO):
    """Nenhuma mesa ampliada encosta na vizinha da mesma parede."""
    for par in ("oeste", "norte", "leste"):
        eixo = "x" if par == "norte" else "y"
        cs = sorted(m[eixo] for m in mesas if m["parede"] == par)
        for a, b in zip(cs, cs[1:]):
            assert b - a >= LARG_DESENHO + 0.1, f"mesas ampliadas se tocam na parede {par}: {a}/{b}"


def monta(var=""):
    LARG_DESENHO, FS2, FS1 = VARIANTES[var]
    planta, dec, cen = SF.carrega()
    mesas = SF.monta_mesas(planta, dec, cen)
    confere(mesas, LARG_DESENHO)
    LARG, ALT = planta["salao"]["largura"], planta["salao"]["altura"]
    PROFM = planta["modulo"]["prof"]
    X = lambda x: MX + x * S
    Y = lambda y: MY + (ALT - y) * S
    ZONA, TINTA_Z = MP.ZONA, MP.TINTA
    txt_z = {"A": MP.ZONA["A"], "B": TXT_B, "C": MP.ZONA["C"]}

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'role="img" aria-label="Planta do Hall 2 com as 28 mesas, cada uma rotulada pelas seções que '
      f'votam nela, as portas A, B e C, as saídas e as avenidas.">')
    a(f'<style>{fonte_css()} text{{font-family:Montserrat,sans-serif}}</style>')
    a('<defs><marker id="ph" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="5" '
      'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>'
      '</marker></defs>')
    a(f'<rect width="{W}" height="{H}" fill="{MP.CREME}"/>')

    # ---- cabeçalho ----
    a(f'<text x="{MX}" y="48" font-size="15" font-weight="700" letter-spacing="3" '
      f'fill="{MP.VERDE}">DENTRO DO SALÃO</text>')
    a(f'<text x="{MX}" y="100" font-size="50" font-weight="700" fill="{MP.MARINHO}">O Hall 2</text>')
    sub = ("As mesas não têm número: cada uma traz as seções que votam nela, que é o "
           "que você tem na mão.")
    for i, ln in enumerate(textwrap.wrap(sub, 62)):
        a(f'<text x="290" y="{66 + i*22}" font-size="16" fill="{MP.CINZA}">{esc(ln)}</text>')

    # ---- o salão ----
    a(f'<rect x="{X(0):.1f}" y="{Y(ALT):.1f}" width="{LARG*S:.1f}" height="{ALT*S:.1f}" '
      f'fill="#FFFFFF" stroke="{MP.MARINHO}" stroke-width="3"/>')

    # ---- as faixas das paredes ----
    for par, k in (("oeste", "A"), ("norte", "B"), ("leste", "C")):
        banda = SF.BANDA_PAREDE[par]
        ys = [m["y"] for m in mesas if m["parede"] == par]
        xs = [m["x"] for m in mesas if m["parede"] == par]
        if par == "oeste":
            r = (PROFM, min(ys) - 1.4, banda, max(ys) + 1.4)
        elif par == "leste":
            r = (47.3 - banda, min(ys) - 1.4, 47.3 - PROFM, max(ys) + 1.4)
        else:
            r = (min(xs) - 1.4, ALT - banda, max(xs) + 1.4, ALT - PROFM)
        a(f'<rect x="{X(r[0]):.1f}" y="{Y(r[3]):.1f}" width="{(r[2]-r[0])*S:.1f}" '
          f'height="{(r[3]-r[1])*S:.1f}" fill="{ZONA[k]}" fill-opacity=".12"/>')

    # ---- as avenidas de entrada ----
    for k, av in SF.AVENIDAS.items():
        pol = av["trilho_interno"] + list(reversed(av["trilho_externo"]))
        pts = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in pol)
        a(f'<polygon points="{pts}" fill="{ZONA[k]}" fill-opacity=".24"/>')
        exi = (av["trilho_interno"][0][0] + av["trilho_externo"][0][0]) / 2
        a(f'<line x1="{X(exi):.1f}" y1="{Y(1.0):.1f}" x2="{X(exi):.1f}" y2="{Y(7.5):.1f}" '
          f'stroke="{ZONA[k]}" stroke-width="4" marker-end="url(#ph)"/>')
    xa, xb = SF.X_AVENIDA_NORTE
    a(f'<rect x="{X(xa):.1f}" y="{Y(SF.Y_BANDA_NORTE):.1f}" width="{(xb-xa)*S:.1f}" '
      f'height="{SF.AVENIDA_NORTE*S:.1f}" fill="{ZONA["B"]}" fill-opacity=".30"/>')

    # ---- as 28 mesas, ampliadas ----
    for m in mesas:
        k = m["entrada"]
        if m["parede"] == "norte":
            x1, x2 = m["x"] - LARG_DESENHO / 2, m["x"] + LARG_DESENHO / 2
            y1, y2 = m["y"] - PROFM, m["y"]
        else:
            xs = sorted([m["x"], m["x"] + m["dx"] * PROFM])
            x1, x2 = xs
            y1, y2 = m["y"] - LARG_DESENHO / 2, m["y"] + LARG_DESENHO / 2
        a(f'<rect x="{X(x1):.1f}" y="{Y(y2):.1f}" width="{(x2-x1)*S:.1f}" height="{(y2-y1)*S:.1f}" '
          f'rx="2" fill="{ZONA[k]}" stroke="{MP.MARINHO}" stroke-width="1.2"/>')
        cx, cy = X((x1 + x2) / 2), Y((y1 + y2) / 2)
        linhas = [MP.sec(s) for s in m["secoes"]]
        fs = FS2 if len(linhas) > 1 else FS1
        ld = fs * 1.06
        giro = f' transform="rotate(-90 {cx:.1f} {cy:.1f})"' if m["parede"] == "norte" else ""
        a(f'<g{giro} font-size="{fs}" font-weight="900" fill="{TINTA_Z[k]}" text-anchor="middle" '
          f'style="font-variant-numeric:tabular-nums">')
        y0 = cy + fs * 0.36 - (len(linhas) - 1) * ld / 2
        for i, t in enumerate(linhas):
            a(f'<text x="{cx:.1f}" y="{y0 + i*ld:.1f}">{t}</text>')
        a('</g>')

    # ---- as portas ----
    for p in planta["portas"]:
        sin = dec["sinalizacao_portas"].get(p["id"], {})
        papel = sin.get("papel")
        if papel not in ("entrada", "saida", "preferencial"):
            continue
        cor = ZONA[sin["entrada"]] if papel == "entrada" else (
            MP.PREF if papel == "preferencial" else MP.GRAFITE)
        a(f'<line x1="{X(p["x1"]):.1f}" y1="{Y(0):.1f}" x2="{X(p["x2"]):.1f}" y2="{Y(0):.1f}" '
          f'stroke="{cor}" stroke-width="9"/>')
        cxp = X((p["x1"] + p["x2"]) / 2)
        if papel == "entrada":
            a(f'<text x="{cxp:.1f}" y="{Y(0)+36:.1f}" text-anchor="middle" font-size="30" '
              f'font-weight="900" fill="{txt_z[sin["entrada"]]}">{sin["entrada"]}</text>')
            a(f'<text x="{cxp:.1f}" y="{Y(0)+54:.1f}" text-anchor="middle" font-size="13" '
              f'fill="{MP.CINZA}">entrada</text>')
        else:
            rotu = "preferencial" if papel == "preferencial" else "saída"
            corr = MP.PREF if papel == "preferencial" else MP.CINZA
            a(f'<text x="{cxp:.1f}" y="{Y(0)+30:.1f}" text-anchor="middle" font-size="13" '
              f'font-weight="700" fill="{corr}">{rotu}</text>')

    # ---- legenda ----
    lx = X(LARG) + 60
    a(f'<text x="{lx}" y="{MY+14}" font-size="18" font-weight="700" letter-spacing="2.5" '
      f'fill="{MP.MARINHO}">COMO LER</text>')
    ly = MY + 52
    itens = [(ZONA["A"], "Porta A → parede oeste"), (ZONA["B"], "Porta B → parede norte"),
             (ZONA["C"], "Porta C → parede leste"), (MP.PREF, "Entrada preferencial, sem fila"),
             (MP.GRAFITE, "Saída — pela mesma faixa da parede")]
    for cor, txt in itens:
        a(f'<rect x="{lx}" y="{ly-17}" width="22" height="22" rx="5" fill="{cor}"/>')
        a(f'<text x="{lx+36}" y="{ly}" font-size="17" fill="{MP.MARINHO}">{esc(txt)}</text>')
        ly += 44
    ly += 18
    paras = ["Da porta, a avenida da sua cor leva até a parede. Da avenida da parede, um passo "
             "até a sua seção.",
             "Quem votou volta pela mesma faixa da parede e sai pela fachada sul — ninguém "
             "atravessa a avenida de quem está entrando.",
             "A faixa mais escura na frente da parede norte é a pequena avenida de 1,80 m: é ali "
             "que a fila da porta B escolhe o lado, andando.",
             "As mesas estão desenhadas mais largas que a real para caber o número; a posição "
             "na parede é a da planta."]
    for t in paras:
        for ln in textwrap.wrap(t, 46):
            a(f'<text x="{lx}" y="{ly}" font-size="15" fill="{MP.CINZA}">{esc(ln)}</text>')
            ly += 22
        ly += 12

    a(f'<text x="{MX}" y="{H-14}" font-size="13" fill="{MP.CINZA}">Planta em escala · fachada sul '
      f'embaixo, como quem chega do Ring 3 · mesas ampliadas ({MP.br1(LARG_DESENHO)} m desenhados '
      f'em vez de {MP.br1(planta["modulo"]["larg"])} m) para o número caber</text>')
    a('</svg>')
    return "\n".join(o)


def acha_chromium():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    # o headless_shell (headless clássico) respeita --window-size; o "new headless" corta embaixo
    for padrao in ("chromium_headless_shell-*/chrome-linux/headless_shell",
                   "chromium_headless_shell-*/chrome-linux/chrome"):
        achados = sorted(glob.glob(os.path.join(base, padrao)))
        if achados:
            return achados[0]
    return None


def rasteriza(svg, png):
    exe = acha_chromium()
    if not exe:
        print("Chromium não encontrado; só o SVG foi gravado", file=sys.stderr)
        return False
    subprocess.run([exe, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={ESCALA_PX}", f"--window-size={W},{H}",
                    f"--screenshot={png}", svg.as_uri()],
                   check=True, capture_output=True, timeout=180)
    return True


def main():
    grava = "--grava" in sys.argv[1:]
    rc = 0
    for var in VARIANTES:
        svg, png = caminho(var, "svg"), caminho(var, "png")
        novo = monta(var)
        atual = svg.read_text(encoding="utf-8") if svg.exists() else ""
        if novo == atual:
            print(f"saidas/{svg.name} em dia")
            continue
        if not grava:
            print(f"saidas/{svg.name} difere do gerador; rode com --grava", file=sys.stderr)
            rc = 1
            continue
        svg.write_text(novo, encoding="utf-8")
        print(f"gravado {svg.name} ({len(novo)} bytes)")
        if rasteriza(svg, png):
            print(f"gravado {png.name}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
