#!/usr/bin/env python3
"""A paleta do plano, e a conferência de que nenhuma peça saiu dela.

As quatro cores da identidade foram **medidas no logotipo vetorizado** entregue
pelo Posto em 21/09, pixel a pixel. Antes disso as peças usavam quatro
quase-acertos — `#F2CE3A` no lugar do ouro, `#4888A8` no lugar do azul,
`#588018` no lugar do verde — e uma tarja `#5A6E6E` que não existe na marca.

As cores de zona são outra coisa: são **cor de rolo de fita já em estoque**.
Mudar uma delas muda uma compra, então elas não se ajustam à identidade — o
amarelo da zona B (`#E8C63A`) e o ouro da marca (`#E5AE0F`) convivem de
propósito, e é por isso que a tarja da B nunca encosta no logotipo.

    python3 scripts/paleta.py            confere e sai com código 1 se houver
                                         cor fora da paleta em mapa/sinalizacao/
    python3 scripts/paleta.py --grava    aplica as substituições (21/09 e 22/09)

Desde 22/09 a zona C é vermelha (`#C8102E`, rolo a comprar), não laranja.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "data" / "paleta.json"
PECAS = RAIZ / "mapa" / "sinalizacao"

_p = json.loads(FONTE.read_text(encoding="utf-8"))

GRAFITE = _p["identidade"]["grafite"]["hex"]
OURO = _p["identidade"]["ouro"]["hex"]
AZUL = _p["identidade"]["azul"]["hex"]
VERDE = _p["identidade"]["verde"]["hex"]
CREME = _p["neutros"]["creme"]["hex"]
REGUA = _p["neutros"]["regua"]["hex"]
CINZA = _p["neutros"]["cinza"]["hex"]
OFFWHITE = _p["neutros"]["offwhite"]["hex"]
MARINHO = _p["neutros"]["marinho"]["hex"]
BRANCO = _p["neutros"]["branco"]["hex"]
ZONA = {k: (v["hex"], v["tinta"]) for k, v in _p["zona"].items() if len(k) == 1}
FONTE = _p["fonte"]["css"]
IMPORT_FONTE = _p["fonte"]["import"]
PAREDE = {k: v["parede"] for k, v in _p["zona"].items() if len(k) == 1}
PORTA = {k: v["porta"] for k, v in _p["zona"].items() if len(k) == 1}

PREFERENCIAL = _p["preferencial"]["hex"]

# Cada rodada de conferência deixa a sua lista (21/09: identidade medida;
# 22/09: a zona C de laranja a vermelho). Todas continuam valendo.
SUBSTITUICOES = {k.upper(): v.upper()
                 for chave, lista in _p.items() if chave.startswith("substituicoes_")
                 for k, v in lista.items() if k.startswith("#")}

# O que pode aparecer numa peça sem ser erro. Fora a paleta em si: as cores do
# laço do espectro autista, que são do símbolo e não do plano, e os tons
# derivados usados como texto sobre fundo claro da própria cor.
PERMITIDAS = {c.upper() for c in (
    GRAFITE, OURO, AZUL, VERDE, CREME, REGUA, CINZA, BRANCO,
    *[h for h, _ in ZONA.values()],
    *_p["laco_tea"]["hexes"],
    MARINHO, OFFWHITE, PREFERENCIAL,
    "#8A6608", "#5C4A12",            # ouro escurecido, para ler sobre ouro claro
    "#042B5A", "#0B6E9E",            # azuis escurecidos da prancha do sistema
    "#5A6270", "#6B737C", "#7A828C", "#9AA3AB", "#C9CFD4",   # cinzas de planta
    "#DCE3E7", "#DDE4E2", "#E4E8EA", "#F0F0E8", "#FFF4D6", "#333A42",
)}


# Sobre a tarja grafite a hashtag sai toda branca. O lock-up colorido tem o #
# em verde e o NA em azul, mas sobre grafite isso dá 2,5:1 e 2,6:1 -- reprova
# para texto pequeno. A versão colorida vale sobre fundo claro, e é a que a
# prancha do sistema (Main) e a página consolidada usam.
# A faixa institucional. A prancha do sistema (Main, 17/09) decidiu: off-white
# com régua marinha, e o amarelo da campanha só dentro do lockup -- porque uma
# faixa amarela no topo de toda peça passaria a dizer "porta B" a 30 metros,
# inclusive nas peças de A e de C. As peças nunca receberam essa decisão e
# seguiram com uma tarja escura. Estas regras aplicam a decisão.
# A fonte da campanha é Montserrat. Archivo e Nunito Sans eram marcação de
# lugar. Montserrat é mais larga no mesmo corpo, então a troca mexe em medida,
# não só em estilo -- as peças foram remedidas com a fonte real instalada.
TIPOGRAFIA = [
    (re.compile(r"@import url\('https://fonts\.googleapis\.com/css2\?[^']*'\)"),
     lambda m: f"@import url('{IMPORT_FONTE}')"),
    (re.compile(r"font-family: 'Archivo', 'Nunito Sans', sans-serif"),
     lambda m: f"font-family: {FONTE}"),
    (re.compile(r"font-family: 'Nunito Sans', system-ui, sans-serif"),
     lambda m: f"font-family: {FONTE}"),
    (re.compile(r"font:(\s*\d+\s+[\d.]+px) (?:Nunito Sans|Archivo),\s*sans-serif"),
     lambda m: f"font:{m.group(1)} Montserrat, sans-serif"),
    (re.compile(r"font:(\s*\d+\s+[\d.]+px) '(?:Nunito Sans|Archivo)',\s*sans-serif"),
     lambda m: f"font:{m.group(1)} 'Montserrat', sans-serif"),
    # os mapas declaram a fonte como atributo de SVG, não como propriedade CSS
    (re.compile(r'font-family="\'(?:Archivo\', \'Nunito Sans|Nunito Sans)\', (?:sans-serif|system-ui, sans-serif)"'),
     lambda m: 'font-family="\'Montserrat\', system-ui, sans-serif"'),
]

FAIXA = [
    # o fundo da tarja e a régua
    (re.compile(r'(height: (\d+)px; flex-shrink: 0; )background: #404041;'),
     lambda m: f'{m.group(1)}background: {OFFWHITE}; '
               f'border-bottom: {4 if int(m.group(2)) > 90 else 3}px solid {MARINHO};'),
    # a palavra ELEIÇÕES deixa de ser reversa e volta ao grafite do logotipo
    (re.compile(r'(letter-spacing: 0\.01em; )color: #FFFFFF;(">(?:EL|IÇÕES)</span>)'),
     lambda m: f'{m.group(1)}color: @LOCKUP@;{m.group(2)}'),
    # a hashtag volta ao lockup colorido, que sobre claro tem contraste
    (re.compile(r'(letter-spacing: 0\.02em; )color: #FFFFFF;(">)#VOTONADEMOCRACIA'),
     lambda m: f'{m.group(1)}color: @LOCKUP@;{m.group(2)}'
               f'<span style="color: {VERDE}">#</span>VOTO'
               f'<span style="color: {AZUL}">NA</span>DEMOCRACIA'),
]


def corpo(html):
    """(início, fim) do corpo da peça: tudo do fim da faixa institucional para
    baixo. O grafite só é legítimo acima disso, dentro do lockup."""
    m = re.search(r'<div style="height: \d+px; flex-shrink: 0; background: ', html)
    if not m:
        return 0, len(html)
    prof, i = 0, m.start()
    for t in re.finditer(r"<div\b|</div>", html[i:]):
        prof += 1 if t.group().startswith("<div") else -1
        if prof == 0:
            return i + t.end(), len(html)
    return 0, len(html)


def tipografia(html):
    """Grafite vira marinho, mas só no corpo — o lockup guarda o dele."""
    i, f = corpo(html)
    return html[:i] + html[i:f].replace(GRAFITE, MARINHO)


def hexes(texto):
    return {m.upper() for m in re.findall(r"#[0-9A-Fa-f]{6}", texto)}


def main():
    grava = "--grava" in sys.argv[1:]
    trocou = fora = 0
    for caminho in sorted(PECAS.glob("*.dc.html")):
        html = caminho.read_text(encoding="utf-8")
        # A faixa primeiro: ela precisa ver o grafite antes de a tipografia
        # virar marinho. O que é do logotipo sai marcado com @LOCKUP@ e volta
        # ao grafite no fim, para a troca geral não o alcançar.
        novo = html
        for padrao, troca in FAIXA:
            novo = padrao.sub(troca, novo)
        for padrao, troca in TIPOGRAFIA:
            novo = padrao.sub(troca, novo)
        for velho, nvo in SUBSTITUICOES.items():
            novo = re.sub(re.escape(velho), nvo, novo, flags=re.IGNORECASE)
        novo = novo.replace("@LOCKUP@", GRAFITE)
        novo = tipografia(novo)
        if novo != html:
            trocou += 1
            if grava:
                caminho.write_text(novo, encoding="utf-8")
            else:
                print(f"{caminho.name:<22} usa cor superada: "
                      f"{sorted(hexes(html) & set(SUBSTITUICOES))}")
        alvo = novo if grava else html
        i, f = corpo(alvo)
        if GRAFITE in alvo[i:f]:
            fora += 1
            print(f"{caminho.name:<22} grafite fora do lockup: a tipografia do corpo é marinho")
        for velha in _p["fonte"]["superadas"]:
            if velha in alvo:
                fora += 1
                print(f"{caminho.name:<22} usa fonte superada: {velha}")
                break
        estranhas = sorted(hexes(alvo) - PERMITIDAS - set(SUBSTITUICOES))
        if estranhas:
            fora += 1
            print(f"{caminho.name:<22} fora da paleta: {estranhas}")

    if grava:
        print(f"{trocou} peças regravadas com a paleta oficial")
        return 1 if fora else 0
    if trocou or fora:
        print(f"{trocou} peças com cor superada, {fora} com cor fora da paleta; "
              f"rode com --grava", file=sys.stderr)
        return 1
    print("paleta em dia em todas as peças")
    return 0


if __name__ == "__main__":
    sys.exit(main())
