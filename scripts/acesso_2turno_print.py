#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marca o plano de acesso do 2º turno sobre o print do Google Maps
(mapa/acesso_2turno_print_base.png, 1163 × 828, satélite, Ballsbridge).

As posições são pixels lidos à mão sobre ESSE print; outro print exige
outra leitura. O que vale como fonte do plano é scripts/acesso_2turno.py;
este só desenha.

    python3 scripts/acesso_2turno_print.py      # grava mapa/acesso_2turno_print.png

Depende de Pillow (pip install pillow).
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "mapa" / "acesso_2turno_print_base.png"
SAIDA = RAIZ / "mapa" / "acesso_2turno_print.png"
Z = 2  # desenha em 2× e reduz, para linhas suaves

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTE_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

VERMELHO = (200, 40, 40)
AMBAR = (235, 150, 20)
VERDE_RDS = (20, 120, 100)
AZUL = (30, 110, 210)
ROXO = (140, 60, 200)
DART = (40, 140, 60)
BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)

# ── pixels (na imagem original) ─────────────────────────────────────────────
BALLSBRIDGE = (585, 322)
P1 = (655, 383)                 # portão da Merrion Road (pedestres)
SERP = (705, 410)               # Merrion Rd × Serpentine Ave (travessia 1)
MERRION = [BALLSBRIDGE, (805, 515), (930, 655), (985, 735), (1060, 828)]
NUTLEY = [(880, 828), (985, 735)]
PEMBROKE = [BALLSBRIDGE, (560, 290)]
NORTHUMBERLAND = [(560, 290), (500, 190), (455, 100), (430, 40)]
PEMBROKE_RESTO = [(560, 290), (500, 247), (430, 200)]
SHELBOURNE = [(588, 318), (592, 235), (596, 150)]
ANGLESEA = [(505, 642), (525, 615), (538, 575), (545, 520), (550, 460), (556, 400), (575, 338)]
ANGLESEA_GATE = (550, 460)
DONNYBROOK = (500, 646)
N11 = [(640, 828), (590, 740), (545, 690), DONNYBROOK]
MOREHAMPTON = [DONNYBROOK, (430, 585), (330, 520), (230, 440), (130, 330)]
SIMMONSCOURT = [(712, 420), (650, 500), (600, 570), (548, 600)]
SIMMONS_GATE = (660, 490)
SERPENTINE_AVE = [(800, 358), SERP]
DART_L = (612, 132)
DART_S = (800, 358)
DART_SP = (1015, 645)
DART_LINHA = [(590, 60), DART_L, (700, 240), DART_S, (900, 490), DART_SP, (1100, 760)]
LANSDOWNE_A_PE = [DART_L, (596, 150), (592, 235), (588, 318)]


def P(p):
    return (p[0] * Z, p[1] * Z)


def linha(d, pts, cor, larg, tracejo=None):
    pts = [P(p) for p in pts]
    if not tracejo:
        d.line(pts, fill=cor, width=larg * Z, joint="curve")
        return
    on, off = tracejo
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L == 0:
            continue
        ux, uy = dx / L, dy / L
        s = 0.0
        while s < L:
            e = min(s + on * Z, L)
            d.line([(a[0] + ux * s, a[1] + uy * s), (a[0] + ux * e, a[1] + uy * e)], fill=cor, width=larg * Z)
            s += (on + off) * Z


def seta(d, a, b, cor, tam=9):
    """Ponta de seta em b, vinda de a."""
    a, b = P(a), P(b)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    t = tam * Z
    p1 = (b[0] - t * math.cos(ang - 0.5), b[1] - t * math.sin(ang - 0.5))
    p2 = (b[0] - t * math.cos(ang + 0.5), b[1] - t * math.sin(ang + 0.5))
    d.polygon([b, p1, p2], fill=cor)


def setas_ao_longo(d, pts, cor, passo=70):
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L // passo))
        for i in range(1, n + 1):
            f = i / (n + 1)
            m = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            seta(d, a, m, cor, 8)


def deslocar(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def rotulo(d, xy, texto, cor_fundo, cor_texto=BRANCO, tam=13, ancora="la"):
    f = ImageFont.truetype(FONTE, tam * Z)
    x, y = P(xy)
    box = d.textbbox((x, y), texto, font=f, anchor=ancora)
    pad = 4 * Z
    d.rounded_rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad), radius=4 * Z, fill=cor_fundo, outline=BRANCO, width=1 * Z)
    d.text((x, y), texto, font=f, fill=cor_texto, anchor=ancora)


def ponto(d, xy, cor, r=7, txt=None, tam=11):
    x, y = P(xy)
    R = r * Z
    d.ellipse((x - R, y - R, x + R, y + R), fill=BRANCO, outline=cor, width=3 * Z)
    if txt:
        f = ImageFont.truetype(FONTE, tam * Z)
        d.text((x, y), txt, font=f, fill=cor, anchor="mm")


def main():
    im = Image.open(BASE).convert("RGB")
    W, H = im.size
    im = im.resize((W * Z, H * Z), Image.LANCZOS)
    d = ImageDraw.Draw(im, "RGBA")

    # 1. DART (fundo)
    linha(d, DART_LINHA, DART, 3, (10, 6))

    # 2. Vias fechadas (não percurso)
    for pts in (SHELBOURNE, PEMBROKE_RESTO):
        linha(d, pts, VERMELHO, 5, (12, 6))

    # 3. Percurso da maratona: halo + linha + setas
    percurso = NUTLEY + MERRION[::-1][1:] + PEMBROKE[1:] + NORTHUMBERLAND[1:]
    linha(d, percurso, (200, 40, 40, 70), 22)
    linha(d, percurso, VERMELHO, 7)
    setas_ao_longo(d, percurso, BRANCO, 80)

    # 4. Merrion Road só outbound (Serpentine → Merrion Gates): âmbar ao lado
    outbound = [SERP, (805, 515), (930, 655), (985, 735), (1060, 828)]
    linha(d, deslocar(outbound, -9, 9), AMBAR, 4)
    setas_ao_longo(d, deslocar(outbound, -9, 9), AMBAR, 90)

    # 5. Anglesea Road: tráfego do RDS
    linha(d, ANGLESEA, VERDE_RDS, 9)
    # sem saída para a Merrion em Ballsbridge
    x, y = P((575, 338))
    d.line([(x - 9 * Z, y - 9 * Z), (x + 9 * Z, y + 9 * Z)], fill=VERMELHO, width=4 * Z)
    d.line([(x - 9 * Z, y + 9 * Z), (x + 9 * Z, y - 9 * Z)], fill=VERMELHO, width=4 * Z)

    # 6. Rotas de carro: N11 (V1) e Morehampton (V2) → Donnybrook → Anglesea
    linha(d, N11, VERDE_RDS, 6)
    setas_ao_longo(d, N11, BRANCO, 60)
    linha(d, MOREHAMPTON[::-1], VERDE_RDS, 6)
    setas_ao_longo(d, MOREHAMPTON[::-1], BRANCO, 70)
    # V4 (a confirmar): Simmonscourt → Merrion outbound
    linha(d, SIMMONSCOURT[::-1], VERDE_RDS, 4, (8, 6))

    # 7. Rotas a pé
    linha(d, SERPENTINE_AVE, AZUL, 5, (9, 5))          # A1
    linha(d, [SERP, P1], AZUL, 5, (9, 5))
    linha(d, LANSDOWNE_A_PE, AZUL, 5, (9, 5))          # A2
    linha(d, [(588, 318), P1], AZUL, 5, (9, 5))
    linha(d, [DONNYBROOK, (525, 615), (538, 575), (545, 520), ANGLESEA_GATE], AZUL, 3, (6, 5))  # A3 (sobre a Anglesea)

    # 8. Pontos
    ponto(d, ANGLESEA_GATE, VERDE_RDS, 11, "V", 12)
    ponto(d, P1, AZUL, 11, "P1", 10)
    ponto(d, SERP, AZUL, 9, "1", 11)
    ponto(d, BALLSBRIDGE, AZUL, 9, "2", 11)
    ponto(d, SIMMONS_GATE, VERDE_RDS, 7)
    for s in (DART_L, DART_S, DART_SP):
        ponto(d, s, DART, 7)
    ponto(d, DONNYBROOK, VERDE_RDS, 7)

    # 9. Rótulos
    rotulo(d, (562, 452), "ANGLESEA GATE · veículos, táxi, preferencial", VERDE_RDS, ancora="ra")
    rotulo(d, (668, 372), "P1 · portão Merrion Rd · só pedestres", AZUL)
    rotulo(d, (716, 418), "Travessia 1 (pedir à Garda)", AZUL)
    rotulo(d, (596, 300), "Travessia 2 · Ballsbridge", AZUL, ancora="la")
    rotulo(d, (590, 348), "sem saída p/ Merrion", VERMELHO, tam=11, ancora="ra")
    rotulo(d, (860, 588), "MERRION ROAD · percurso · fechada 10h →", VERMELHO)
    rotulo(d, (850, 470), "só outbound (sul) a partir da Serpentine Ave", AMBAR, PRETO, 11)
    rotulo(d, (870, 772), "NUTLEY LANE · fechada", VERMELHO, tam=11, ancora="rd")
    rotulo(d, (870, 798), "← corredores vêm da N11 / Nutley Lane", VERMELHO, tam=11, ancora="rd")
    rotulo(d, (608, 215), "SHELBOURNE RD · fechada", VERMELHO, tam=11)
    rotulo(d, (470, 110), "NORTHUMBERLAND RD · percurso", VERMELHO, tam=11)
    rotulo(d, (496, 660), "DONNYBROOK · entrada e saída de veículos", VERDE_RDS, ancora="ra")
    rotulo(d, (600, 775), "N11 · aberta · V1 do sul", VERDE_RDS, tam=11, ancora="ra")
    rotulo(d, (300, 470), "MOREHAMPTON · V2 do centro", VERDE_RDS, tam=11)
    rotulo(d, (668, 500), "V4 · Simmonscourt (a confirmar)", VERDE_RDS, tam=11)
    rotulo(d, (624, 120), "DART Lansdowne Rd · A2", DART, tam=11)
    rotulo(d, (812, 346), "DART Sandymount · A1", DART, tam=11)
    rotulo(d, (1027, 633), "DART Sydney Parade", DART, tam=11)
    rotulo(d, (1160, 822), "→ Merrion Gates: inbound desviado p/ Strand Rd, não chega ao RDS", AMBAR, PRETO, 11, ancora="rd")

    # 10. Legenda
    f = ImageFont.truetype(FONTE_R, 12 * Z)
    fb = ImageFont.truetype(FONTE, 13 * Z)
    x0, y0 = 8 * Z, 8 * Z
    d.rounded_rectangle((x0, y0, x0 + 430 * Z, y0 + 226 * Z), radius=6 * Z, fill=(255, 255, 255, 235), outline=(60, 60, 60), width=1 * Z)
    d.text((x0 + 10 * Z, y0 + 8 * Z), "Acesso ao RDS · 2º turno 25/10/2026 · Maratona", font=fb, fill=PRETO)
    itens = [
        (VERMELHO, None, "percurso da maratona / via fechada a partir das 10h"),
        (AMBAR, None, "Merrion Rd só outbound, da Serpentine Ave ao sul"),
        (VERDE_RDS, None, "Anglesea Rd e rotas de carro V1 / V2 (saída = V3)"),
        (AZUL, (9, 5), "rotas a pé A1 / A2 / A3 · travessias 1 e 2"),
        (DART, (10, 6), "linha do DART (funciona normalmente)"),
    ]
    yy = y0 + 34 * Z
    for cor, tr, txt in itens:
        seg = [(x0 / Z + 12, yy / Z + 7), (x0 / Z + 48, yy / Z + 7)]
        linha(d, seg, cor, 5, tr)
        d.text((x0 + 56 * Z, yy), txt, font=f, fill=PRETO)
        yy += 22 * Z
    d.text((x0 + 10 * Z, yy + 4 * Z), "Votação 8h–17h. Corredores no RDS ≈10h45–15h40 (estimativa).\n"
           "Veículos: só Anglesea Gate, via N11 ou Morehampton/Donnybrook.\n"
           "Pedestres: portão Merrion Rd (P1). Táxi: «RDS Anglesea Road Gate».\n"
           "Posições aproximadas, lidas sobre o print.", font=f, fill=(60, 60, 60), spacing=3 * Z)

    im = im.resize((W, H), Image.LANCZOS)
    im.save(SAIDA, optimize=True)
    print("gravado", SAIDA)


if __name__ == "__main__":
    main()
