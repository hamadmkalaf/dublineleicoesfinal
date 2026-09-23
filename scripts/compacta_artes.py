#!/usr/bin/env python3
"""Reescreve os PDFs de saidas/artes_sinalizacao/ em forma compacta, no lugar,
sem tocar no conteúdo da página.

    python3 scripts/compacta_artes.py            reescreve e confere
    python3 scripts/compacta_artes.py --confere  só confere: sai com código 1 se
                                                 algum PDF ainda estiver na forma
                                                 que o Chromium grava

O que muda, e por quê:

1. **Fontes fundidas.** O Chromium embute um subconjunto da Montserrat por trecho
   de texto — sete objetos de fonte para três pesos numa placa de grupo, cada um
   com 12 KB de tabelas de hinting e métricas para 3 a 12 glifos usados. Como o
   Skia preserva os IDs de glifo do TTF original, os subconjuntos do mesmo peso
   são substituíveis por um só: aqui ele é recortado de novo do TTF instalado
   (só os glifos usados, IDs preservados, sem hinting) e todos os descritores
   daquele peso passam a apontar para o mesmo stream. Antes de trocar, cada
   glifo usado é comparado contorno a contorno com o do TTF do sistema; se
   diferir, a fonte não é tocada.
2. **PDF 1.5 com object streams e xref stream** (`garbage=4`, `use_objstms=1`):
   ~12% menor e sem a tabela xref clássica, dezenas de linhas quase iguais.

Resultado típico: uma placa de 850 × 2000 cai de 38 KB para ~10 KB. A conferência
renderiza cada página antes e depois e exige o mesmo raster: a compactação não
pode mudar a arte. Precisa de PyMuPDF e fontTools (`pip install pymupdf fonttools`).
"""
import io
import json
import sys
from pathlib import Path

import pymupdf
from fontTools import subset
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "saidas" / "artes_sinalizacao"
# peso CSS → peso do fontconfig (escala própria: 400 = 80, 700 = 200, 800 = 205)
PESOS = {"Thin": 0, "ExtraLight": 40, "Light": 50, "Regular": 80, "Medium": 100,
         "SemiBold": 180, "Bold": 200, "ExtraBold": 205, "Black": 210}


def compacto(caminho):
    return b"\nxref\n" not in caminho.read_bytes()


def raster(caminho, zoom=0.25):
    with pymupdf.open(caminho) as d:
        return d[0].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).samples


def ttf_do_sistema(peso):
    """O TTF instalado do peso pedido, pelo fontconfig — o mesmo que o Chromium usou."""
    import subprocess
    saida = subprocess.run(["fc-list", f":family=Montserrat:weight={peso}", "file"],
                           capture_output=True, text=True, check=True).stdout
    caminhos = [l.strip().rstrip(":") for l in saida.splitlines() if l.strip()]
    if len(caminhos) != 1:
        raise RuntimeError(f"Montserrat peso {peso}: esperava 1 TTF no sistema, achei {caminhos}")
    return caminhos[0]


def glifos_usados(raw):
    """O subconjunto e os IDs (GID) dos glifos com contorno — os nomes de glifo do
    subconjunto são genéricos, então a comparação com o original é por GID."""
    f = TTFont(io.BytesIO(raw))
    g = f["glyf"]
    return f, {i for i, n in enumerate(f.getGlyphOrder()) if g[n].numberOfContours != 0}


def funde_fontes(doc):
    """Um stream de fonte por peso. Devolve quantos objetos de fonte foram dispensados."""
    descritores = {}
    for x in range(1, doc.xref_length()):
        if doc.xref_get_key(x, "Type")[1] != "/FontDescriptor":
            continue
        nome = doc.xref_get_key(x, "FontName")[1]          # /AAAAAA+Montserrat-ExtraBold
        ff = doc.xref_get_key(x, "FontFile2")
        if ff[0] != "xref":
            continue
        descritores.setdefault(nome.split("+", 1)[-1], []).append((x, int(ff[1].split()[0])))
    dispensados = 0
    for face, lista in descritores.items():
        familia, _, estilo = face.partition("-")
        if familia != "Montserrat" or estilo not in PESOS:
            continue
        original = TTFont(ttf_do_sistema(PESOS[estilo]))
        ordem = original.getGlyphOrder()
        usados = set()
        for _, fx in lista:
            sub, gids = glifos_usados(doc.xref_stream(fx))
            sub_ordem = sub.getGlyphOrder()
            for i in gids:   # mesmo contorno no subconjunto e no original, ou nada feito
                a = sub["glyf"][sub_ordem[i]].getCoordinates(sub["glyf"])
                b = original["glyf"][ordem[i]].getCoordinates(original["glyf"])
                if a != b:
                    raise RuntimeError(f"{face}: glifo {i} difere do TTF do sistema")
            usados |= gids
        opcoes = subset.Options(retain_gids=True, hinting=False, notdef_outline=True,
                                drop_tables=["STAT", "GPOS", "GSUB", "GDEF", "DSIG", "name"] ,
                                name_IDs=[], glyph_names=False, recalc_bounds=True)
        s = subset.Subsetter(opcoes)
        s.populate(gids=sorted(usados))
        s.subset(original)
        buf = io.BytesIO()
        original.save(buf)
        dados = buf.getvalue()
        novo = doc.get_new_xref()
        doc.update_object(novo, f"<</Length1 {len(dados)}>>")
        doc.update_stream(novo, dados)
        for dx, _ in lista:
            doc.xref_set_key(dx, "FontFile2", f"{novo} 0 R")
        dispensados += len(lista) - 1
    return dispensados


def main():
    confere = "--confere" in sys.argv[1:]
    pdfs = sorted(SAIDA.glob("*.pdf"))
    if not pdfs:
        print("nenhum PDF em saidas/artes_sinalizacao/; rode node scripts/exporta_artes.mjs", file=sys.stderr)
        return 1
    pendentes = [p for p in pdfs if not compacto(p)]
    if confere:
        for p in pendentes:
            print(f"{p.name}: forma do Chromium, não compactado")
        print(f"{len(pdfs) - len(pendentes)}/{len(pdfs)} compactos")
        return 1 if pendentes else 0
    tamanhos = {}
    for p in pendentes:
        antes = raster(p)
        tmp = p.with_suffix(".tmp.pdf")
        with pymupdf.open(p) as d:
            n = funde_fontes(d)
            d.save(tmp, garbage=4, deflate=True, use_objstms=1)
        if raster(tmp) != antes:
            tmp.unlink()
            print(f"{p.name}: o raster mudou na compactação; mantido o original", file=sys.stderr)
            return 1
        a, b = p.stat().st_size, tmp.stat().st_size
        tmp.replace(p)
        tamanhos[p.name] = b
        print(f"{p.name:<52} {a:>7} → {b:>6} B  ({n} fontes fundidas)")
    manifesto = SAIDA / "manifesto.json"
    if manifesto.exists() and tamanhos:
        m = json.loads(manifesto.read_text(encoding="utf-8"))
        for item in m["artes"]:
            if item["arquivo"] in tamanhos:
                item["bytes"] = tamanhos[item["arquivo"]]
        manifesto.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(pendentes)} compactados, {len(pdfs) - len(pendentes)} já estavam")
    return 0


if __name__ == "__main__":
    sys.exit(main())
