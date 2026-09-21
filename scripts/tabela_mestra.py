#!/usr/bin/env python3
"""Gera a tabela mestra "sua seção -> sua porta" das peças P0, P1, P2 e P3.

A tabela deixou de ser uma lista única em ordem de seção e passou a ser
agrupada pela porta: bloco A, bloco B, bloco C, e dentro de cada bloco as
seções em ordem crescente. O rótulo da porta sai uma vez, no cabeçalho do
bloco, em vez de repetir-se em 51 pastilhas -- e a largura que sobra vira
dígito maior.

A fonte da correspondência seção -> porta é `data/grupos_mesas.json`, que é
lido, nunca escrito por aqui.

    python3 scripts/tabela_mestra.py            confere e não escreve nada
    python3 scripts/tabela_mestra.py --grava    regrava as quatro peças

Sem `--grava` o script compara o que está nos arquivos com o que geraria e
sai com código 1 na divergência, de modo a servir de teste.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "data" / "grupos_mesas.json"
PECAS = RAIZ / "mapa" / "sinalizacao"

# As três cores de porta, iguais às do resto do plano de sinalização.
CORES = {
    "A": ("#33507E", "#FFFFFF"),
    "B": ("#E8C63A", "#3F3F3F"),
    "C": ("#DE7343", "#3F3F3F"),
}
REGUA = "#E4DFCC"
COLUNAS_POR_BLOCO = 3

ARCHIVO = "'Archivo', 'Nunito Sans', sans-serif"

# Uma escala por peça: a P0 e a P1 são banners de gradil lidos de perto, a P2
# divide a altura com a tarja de rodapé e a P3 divide a largura com o painel
# "siga o corredor". Medidas em px do canvas de 1040x410 (1 px = 2 mm).
ESCALAS = {
    "P0-Mestra": dict(num=26, alt=30, cab=30, cab_fonte=20, vao=18, vao_int=12, vao_cab=6),
    "P1-Portao": dict(num=26, alt=30, cab=30, cab_fonte=20, vao=18, vao_int=12, vao_cab=6),
    "P2-ParedeLeste": dict(num=26, alt=31, cab=32, cab_fonte=20, vao=15, vao_int=10, vao_cab=5),
    "P3-EntradaRing": dict(num=22, alt=26, cab=28, cab_fonte=17, vao=12, vao_int=8, vao_cab=5),
}


def por_porta():
    """Seções de cada porta, em ordem crescente, a partir de grupos_mesas.json."""
    dados = json.loads(FONTE.read_text(encoding="utf-8"))
    mapa = {}
    for grupo in dados["grupos"]:
        for secao in grupo["secoes"]:
            anterior = mapa.setdefault(secao, grupo["entrada"])
            if anterior != grupo["entrada"]:
                raise SystemExit(f"seção {secao} em duas portas: {anterior} e {grupo['entrada']}")
    return {p: sorted(s for s, porta in mapa.items() if porta == p) for p in "ABC"}


def reparte(secoes, colunas):
    """Distribui as seções em colunas de altura igual, lendo de cima para baixo."""
    n = len(secoes)
    base, resto = divmod(n, colunas)
    saida, i = [], 0
    for c in range(colunas):
        tam = base + (1 if c < resto else 0)
        saida.append(secoes[i:i + tam])
        i += tam
    return saida


def bloco(porta, secoes, e):
    fundo, tinta = CORES[porta]
    cabecalho = (
        f'<div style="display: flex; align-items: center; height: {e["cab"]}px; flex-shrink: 0;'
        f' background: {fundo}; color: {tinta}; padding: 0 9px; box-sizing: border-box;">'
        f'<span style="font-family: {ARCHIVO}; font-weight: 800; font-size: {e["cab_fonte"]}px;'
        f' letter-spacing: 0.04em;">PORTA {porta}</span></div>'
    )
    colunas = []
    for coluna in reparte(secoes, COLUNAS_POR_BLOCO):
        linhas = "".join(
            f'<div style="border-bottom: 1px solid {REGUA}; padding: 1px 0;">'
            f'<span style="font-family: {ARCHIVO}; font-weight: 700; font-size: {e["num"]}px;'
            f' line-height: {e["alt"]}px; color: #3F3F3F; font-variant-numeric: tabular-nums;">'
            f"{secao:04d}</span></div>"
            for secao in coluna
        )
        colunas.append(f'<div style="display: flex; flex-direction: column;">{linhas}</div>')
    grade = (
        f'<div style="display: grid; grid-template-columns: repeat({COLUNAS_POR_BLOCO},'
        f' minmax(0, 1fr)); gap: 0 {e["vao_int"]}px;">' + "".join(colunas) + "</div>"
    )
    return (
        f'<div style="display: flex; flex-direction: column; gap: {e["vao_cab"]}px;">'
        f"{cabecalho}{grade}</div>"
    )


def tabela(peca, portas):
    e = ESCALAS[peca]
    blocos = "".join(bloco(p, portas[p], e) for p in "ABC")
    return (
        f'<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));'
        f' gap: 0 {e["vao"]}px; flex-grow: 1; overflow: hidden;">\n{blocos}\n</div>'
    )


def recorta(html):
    """Devolve (início, fim) do div da tabela: o primeiro grid de colunas da peça."""
    i = html.index('<div style="display: grid; grid-template-columns: repeat(')
    profundidade, j = 0, i
    for m in re.finditer(r"<div\b|</div>", html[i:]):
        j = i + m.end()
        profundidade += 1 if m.group().startswith("<div") else -1
        if profundidade == 0:
            return i, j
    raise SystemExit("div da tabela sem fechamento")


def main():
    grava = "--grava" in sys.argv[1:]
    portas = por_porta()
    total = sum(len(s) for s in portas.values())
    if total != 51:
        raise SystemExit(f"esperadas 51 seções, vieram {total}")

    divergiu = False
    for peca in ESCALAS:
        caminho = PECAS / f"{peca}.dc.html"
        html = caminho.read_text(encoding="utf-8")
        i, j = recorta(html)
        novo = html[:i] + tabela(peca, portas) + html[j:]
        marca = "igual"
        if novo != html:
            divergiu = True
            marca = "regravada" if grava else "DIVERGENTE"
            if grava:
                caminho.write_text(novo, encoding="utf-8")
        print(f"{peca:<16} {marca}")

    print("porta A {} · porta B {} · porta C {} · {} seções".format(
        *(len(portas[p]) for p in "ABC"), total))
    if divergiu and not grava:
        print("as peças estão fora do que este gerador produz; rode com --grava", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
