#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rasteriza as artes de saidas/artes/*.svg em PNG de 1080 x 1080.

Usa o Chromium que já vem no ambiente (o mesmo do Playwright). Passo opcional:
o SVG é o entregável; o PNG existe só para quem vai postar. Se não houver
Chromium, o script diz isso e sai sem erro — as artes continuam válidas.

O Chromium reserva ~82 px de altura para a moldura da janela mesmo em headless,
então a janela é pedida mais alta e a imagem é recortada de volta a 1080.

Uso:
    python3 scripts/artes_png.py
"""

import glob
import os
import struct
import subprocess
import sys
import tempfile
import zlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTES = os.path.join(RAIZ, "saidas", "artes")
LADO = 1080
FOLGA = 120  # altura extra pedida à janela, recortada depois


def acha_chromium():
    for padrao in ("/opt/pw-browsers/chromium*/chrome-linux/chrome",
                   "/usr/bin/chromium", "/usr/bin/chromium-browser",
                   "/usr/bin/google-chrome"):
        achados = sorted(glob.glob(padrao))
        if achados:
            return achados[-1]
    return None


def le_png(caminho):
    d = open(caminho, "rb").read()
    pos, idat = 8, b""
    w = h = ct = None
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ, dados = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", dados[:10])
            if bd != 8:
                raise SystemExit("PNG de %d bits: não trato" % bd)
        elif typ == b"IDAT":
            idat += dados
        pos += 12 + ln
    nch = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    bruto = zlib.decompress(idat)
    stride = w * nch
    linhas, ant, i = [], bytearray(stride), 0
    for _ in range(h):
        f = bruto[i]
        i += 1
        lin = bytearray(bruto[i:i + stride])
        i += stride
        for x in range(stride):
            a = lin[x - nch] if x >= nch else 0
            b = ant[x]
            c = ant[x - nch] if x >= nch else 0
            if f == 1:
                lin[x] = (lin[x] + a) & 255
            elif f == 2:
                lin[x] = (lin[x] + b) & 255
            elif f == 3:
                lin[x] = (lin[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                lin[x] = (lin[x] + (a if (pa <= pb and pa <= pc)
                                    else (b if pb <= pc else c))) & 255
        linhas.append(bytes(lin))
        ant = lin
    return w, h, nch, ct, linhas


def grava_png(caminho, w, h, nch, ct, linhas):
    cru = b"".join(b"\0" + l for l in linhas)
    def bloco(typ, dados):
        return (struct.pack(">I", len(dados)) + typ + dados
                + struct.pack(">I", zlib.crc32(typ + dados) & 0xFFFFFFFF))
    png = (b"\x89PNG\r\n\x1a\n"
           + bloco(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0))
           + bloco(b"IDAT", zlib.compress(cru, 9))
           + bloco(b"IEND", b""))
    open(caminho, "wb").write(png)


def main():
    chrome = acha_chromium()
    if not chrome:
        print("Chromium não encontrado — os SVG continuam válidos, "
              "só não gerei PNG.")
        return 0
    svgs = sorted(glob.glob(os.path.join(ARTES, "*.svg")))
    if not svgs:
        print("Nada em saidas/artes/*.svg — rode antes scripts/artes_eleitor.py")
        return 1
    tmp = tempfile.mkdtemp(prefix="artes-")
    for svg in svgs:
        nome = os.path.splitext(os.path.basename(svg))[0]
        env = os.path.join(tmp, nome + ".html")
        with open(env, "w", encoding="utf-8") as f:
            f.write('<!doctype html><meta charset="utf-8">'
                    '<style>html,body{margin:0;padding:0;background:#fff}'
                    'img{display:block;width:%dpx;height:%dpx}</style>'
                    '<img src="file://%s">' % (LADO, LADO, svg))
        destino = os.path.join(ARTES, nome + ".png")
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             "--window-size=%d,%d" % (LADO, LADO + FOLGA),
             "--screenshot=" + destino, "file://" + env],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        w, h, nch, ct, linhas = le_png(destino)
        if (w, h) != (LADO, LADO):
            linhas = [l[:LADO * nch] for l in linhas[:LADO]]
            faltam = LADO - len(linhas)
            if faltam > 0:
                raise SystemExit("%s saiu com %dx%d: janela pequena demais"
                                 % (nome, w, h))
            grava_png(destino, LADO, LADO, nch, ct, linhas)
        print("  %s.png · %d x %d" % (nome, LADO, LADO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
