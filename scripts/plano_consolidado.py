#!/usr/bin/env python3
"""Mantém `mapa/plano_sinalizacao.html` — o plano consolidado, peça por peça —
alinhado às peças de `mapa/sinalizacao/` e às decisões vigentes.

A página embute a arte de cada peça, reduzida, ao lado da ficha do ponto em
que ela é instalada. As artes são as mesmas dos `.dc.html`: este script troca
cada corpo embutido pelo corpo atual do arquivo correspondente (as 17 fichas
pela legenda `arquivo <code>…</code>`, as 16 placas de grupo pelo código no
alto do banner) e aplica as revisões de texto de cada rodada — quantidades,
orçamento, mapas, paleta, pendências e rodapé.

Substitui `reconstroi_plano_consolidado.py` e `atualiza_plano_consolidado.py`,
que estavam presos a um commit-base e a um caminho de outra sessão.

    python3 scripts/plano_consolidado.py            confere e sai com 1 se divergir
    python3 scripts/plano_consolidado.py --grava    regrava a página

As revisões de texto são idempotentes: cada uma se aplica se o texto antigo
estiver na página, e é ignorada se o novo já estiver.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "mapa" / "plano_sinalizacao.html"
PECAS = RAIZ / "mapa" / "sinalizacao"
GRUPOS = RAIZ / "data" / "grupos_mesas.json"

# a legenda "arquivo <code>…</code>" de cada ficha → a peça
ARQUIVO = {
    "P0-consulta": "P0-Consulta", "P0-tabela-mestra": "P0-Mestra", "P1-portao": "P1-Portao",
    "P2-parede-leste": "P2-ParedeLeste", "P3-entrada-ring3": "P3-EntradaRing",
    "P4-boca-zona-A": "P4-ZonaA", "P4-boca-zona-B": "P4-ZonaB", "P4-boca-zona-C": "P4-ZonaC",
    "P5-vinil-porta-A": "P5-VinilA", "P5-vinil-porta-B": "P5-VinilB", "P5-vinil-porta-C": "P5-VinilC",
    "P5-preferencial": "P5-Preferencial", "P5-vinil-preferencial": "P5-VinilPref",
    "P6-painel-porta-A": "P6-PainelA", "P6-painel-porta-B": "P6-PainelB", "P6-painel-porta-C": "P6-PainelC",
    "P4-fim-corredor-C": "P4-FimCorredorC",
    "P7-saida": "P7-Saida",
}

ABRE = '<div style="width: '


def fim_do_div(texto, i):
    """Índice logo depois do </div> que fecha o <div> aberto em `i`."""
    prof = 0
    for m in re.finditer(r"<div\b|</div>", texto[i:]):
        prof += 1 if m.group().startswith("<div") else -1
        if prof == 0:
            return i + m.end()
    raise SystemExit("div sem fechamento")


def corpo(nome):
    t = (PECAS / f"{nome}.dc.html").read_text(encoding="utf-8")
    i = t.index(ABRE)
    return t[i:fim_do_div(t, i)]


def troca_artes(h):
    """As 17 fichas: cada arte embutida vira o corpo atual da sua peça."""
    for legenda, nome in ARQUIVO.items():
        cap = f"arquivo <code>{legenda}</code>"
        j = h.index(cap)
        # o corpo é o último <div style="width: … aberto dentro do invólucro .arte antes da legenda
        a = h.rindex('<div class="arte" style=', 0, j)
        i = h.index(ABRE, a)              # o invólucro escreve "width:" sem espaço; o corpo, "width: "
        f = fim_do_div(h, i)
        h = h[:i] + corpo(nome) + h[f:]
    return h


def troca_galeria(h):
    """As 16 placas de grupo, identificadas pelo código no alto do banner."""
    grupos = [g["id"] for g in json.loads(GRUPOS.read_text(encoding="utf-8"))["grupos"]]
    pos = 0
    vistos = []
    while True:
        a = h.find('<div class="gart">', pos)
        if a < 0:
            break
        i = h.index(ABRE, a)
        f = fim_do_div(h, i)
        m = re.search(r'font-size: 104px; line-height: 0\.86; letter-spacing: -0\.03em;">([ABC]\d)</div>', h[i:f])
        gid = m.group(1)
        novo = corpo(f"P6-Bloco{gid}")
        h = h[:i] + novo + h[f:]
        vistos.append(gid)
        pos = i + len(novo)
    if vistos != grupos:
        raise SystemExit(f"galeria com {vistos}, esperava {grupos}")
    return h


def secao(h, marca):
    """(início, fim) da <section class="ficha"> que contém `marca`."""
    j = h.index(marca)
    a = h.rindex('<section class="ficha">', 0, j)
    f = h.index("</section>", j) + len("</section>")
    return a, f


def revisa(h, trocas, onde=None):
    """Aplica (velho, novo[, marca]) de forma idempotente, no trecho `onde`.

    `marca` é um fragmento cuja presença já basta para pular a troca. Serve
    para a revisão de uma rodada cujo texto uma rodada posterior reescreveu em
    parte: sem ela, a regra antiga não acha nem o velho nem o novo e aborta.
    """
    a, f = onde if onde else (0, len(h))
    trecho = h[a:f]
    for velho, novo, *resto in trocas:
        if (resto[0] if resto else novo) in trecho:
            continue
        if trecho.count(velho) != 1:
            raise SystemExit(f"revisão sem alvo único ({trecho.count(velho)}): {velho[:70]}")
        trecho = trecho.replace(velho, novo)
    return h[:a] + trecho + h[f:]


# ---------------------------------------------------------------- revisão de 22/09
CIRCULOS_OESTE = {  # x-banners A3, A4 e A5 nos mapas do Hall 2 (cy antigo → novo, escala 6,194 px/m)
    "153.9": "144.5", "124.5": "115.1", "85.4": "76.1"}
QUADRADOS_OESTE = {  # as cinco mesas de A3, A4 e A5 (y antigo → novo)
    "149.9": "140.5", "132.6": "123.2", "108.4": "99.0", "93.5": "84.1", "69.3": "60.0"}


def revisao_22_09(h):
    # cores: a zona C passou de laranja a vermelho; a tinta sobre ela, a branco
    # (o laranja citado como história, entre <code>, fica)
    h = re.sub(r"(?<!<code>)#DE7343", "#C8102E", h).replace("#9C4118", "#8A0B20")
    h = h.replace("background:#C8102E;color:#042B5A", "background:#C8102E;color:#FFFFFF")

    # cabeçalho e orçamento: o P0-Consulta passou a duas peças (+1 fence banner)
    h = revisa(h, [
        ('O quarto vinil. da S7. entrou em 21/09 e herda essa incerteza.',
         'O quarto vinil. da S7. entrou em 21/09 e herda essa incerteza. O segundo P0-Consulta entrou em 22/09: é o 11º fence banner. a € 32.40 pelo unitário da cotação.'),
    ])

    # a ficha do P0-Consulta: duas peças, uma de cada lado do portão, com o QR do TSE
    h = revisa(h, [
        ('<p class="onde"><strong>Onde:</strong> Calçada da Merrion Road, no gradil do RDS, 20–30 m antes do portão.</p>',
         '<p class="onde"><strong>Onde:</strong> Calçada da Merrion Road, no gradil do RDS — <strong>duas peças, uma de cada lado do portão</strong> de eleitores, cada uma ao lado de uma tabela mestra.</p>'),
        ('nem atalho por condado (Cork e Limerick caem em duas portas cada).</p>',
         'nem atalho por condado (Cork e Limerick caem em duas portas cada). Desde 22/09 são <strong>duas</strong>, uma de cada lado do portão, cada uma emparelhada com uma tabela mestra: quem descobre a seção no QR lê a porta na peça ao lado. O QR é <strong>estático e aponta direto para a consulta por nome no site do TSE</strong> (nível de correção H), gerado por <code>scripts/qr_tse.py</code> — não para o e-Título nem para um encurtador de terceiro.</p>'),
        ('<div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div>', '<div class="sp"><dt>Quantidade</dt><dd>2 peças</dd></div>'),
    ], secao(h, "arquivo <code>P0-consulta</code>"))
    h = revisa(h, [
        ('<p class="onde"><strong>Onde:</strong> Gradil da Merrion Road, ao lado do ponto de consulta.</p>',
         '<p class="onde"><strong>Onde:</strong> Gradil da Merrion Road, uma de cada lado do portão, cada uma ao lado de um ponto de consulta.</p>'),
        ('Duas peças: uma ao lado da mesa de consulta, outra no trecho onde a fila da calçada se forma.',
         'Duas peças, uma de cada lado do portão, cada uma emparelhada com um P0-Consulta (22/09).'),
    ], secao(h, "arquivo <code>P0-tabela-mestra</code>"))
    # o mapa da calçada, nas três fichas que o usam: o segundo par do outro lado do portão
    velho_p0 = ('<rect x="120" y="22" width="92" height="26" rx="3" fill="#FFF" stroke="#3F3F3F" stroke-width="2"/>\n'
                '<text x="166" y="39" text-anchor="middle" style="font:800 10px Montserrat,sans-serif" fill="#3F3F3F">P0</text>')
    novo_p0 = velho_p0 + ('\n<rect x="300" y="22" width="92" height="26" rx="3" fill="#FFF" stroke="#3F3F3F" stroke-width="2"/>\n'
                          '<text x="346" y="39" text-anchor="middle" style="font:800 10px Montserrat,sans-serif" fill="#3F3F3F">P0</text>')
    if novo_p0 not in h:
        assert h.count(velho_p0) == 2, h.count(velho_p0)
        h = h.replace(velho_p0, novo_p0)
    # na ficha do P1 o P0 aparece esmaecido, na mesma posição
    velho_p1 = ('<rect x="120" y="24" width="80" height="22" rx="3" fill="#F4F6F5" stroke="#3F3F3F" stroke-width="1"/>\n'
                '<text x="160" y="38" text-anchor="middle" style="font:800 10px Montserrat,sans-serif" fill="#3F3F3F">P0</text>')
    novo_p1 = velho_p1 + ('\n<rect x="306" y="24" width="80" height="22" rx="3" fill="#F4F6F5" stroke="#3F3F3F" stroke-width="1"/>\n'
                          '<text x="346" y="38" text-anchor="middle" style="font:800 10px Montserrat,sans-serif" fill="#3F3F3F">P0</text>')
    if novo_p1 not in h:
        assert h.count(velho_p1) == 1, h.count(velho_p1)
        h = h.replace(velho_p1, novo_p1)

    # as bocas do Ring 3: a A a oeste, as saídas na face norte
    S = 308 / 44.0
    aberturas = "".join(
        f'\n<line x1="{26 + xa * S:.1f}" y1="30" x2="{26 + xb * S:.1f}" y2="30" stroke="#FFF" stroke-width="4"/>'
        f'\n<line x1="{26 + xa * S:.1f}" y1="30" x2="{26 + xb * S:.1f}" y2="30" stroke="{cor}" stroke-width="3"/>'
        for xa, xb, cor in ((10.87, 12.87, "#33507E"), (19.5, 21.5, "#E8C63A"), (28.13, 30.13, "#C8102E")))
    velho_ring = '<rect x="26" y="254.0" width="308" height="21.0" fill="#DCE3E7"/>'
    if velho_ring + aberturas not in h:
        assert h.count(velho_ring) == 4, h.count(velho_ring)
        h = h.replace(velho_ring, velho_ring + aberturas)
    h = revisa(h, [
        ('<circle cx="106.0" cy="261" r="8" fill="#3F3F3F"/>\n<text x="106.0" y="264"',
         '<circle cx="36.0" cy="261" r="8" fill="#3F3F3F"/>\n<text x="36.0" y="264"'),
        ('<p class="onde"><strong>Onde:</strong> CCB de fechamento imediatamente antes da boca da zona A, virada para o trecho de fundo.</p>',
         '<p class="onde"><strong>Onde:</strong> CCB de fechamento imediatamente antes da boca da zona A, no <strong>extremo oeste</strong> do trecho de fundo (desde 22/09), virada para quem chega.</p>'),
        ('<strong>A boca da zona A fica 2,91 m a oeste do eixo da porta A</strong> — a única das três que não descarrega na própria porta.</p>',
         'Desde 22/09 a boca de entrada da A fica no <strong>extremo oeste</strong>: com 23 raias, a raia de cima anda no sentido contrário ao da boca, e só assim a fila sai no extremo leste, junto à S4. <strong>A saída da A fica a 2,91 m do eixo da porta, no batente oeste do vão</strong> — a única das três que atravessa o apron em diagonal; C e B saem dentro do vão da própria porta.</p>'),
    ], secao(h, "arquivo <code>P4-boca-zona-A</code>"))
    h = revisa(h, [
        ('<p class="texto">A primeira boca do percurso. Fica na CCB imediatamente <em>antes</em> da abertura, virada para o trecho de fundo, para ser lida em movimento a 10–15 m.</p>',
         '<p class="texto">A primeira boca do percurso. Fica na CCB imediatamente <em>antes</em> da abertura, virada para o trecho de fundo, para ser lida em movimento a 10–15 m. Desde 22/09 as três peças têm o corpo branco e a cor da porta só no bloco da letra; as seções vão em células com borda, dígito de 80 mm.</p>'),
    ], secao(h, "arquivo <code>P4-boca-zona-C</code>"))

    # o Hall 2: as mesas A3, A4 e A5 andaram 1,50 m para o norte (prancheta de 22/09)
    for velho, novo in QUADRADOS_OESTE.items():
        h = h.replace(f'<rect x="24.7" y="{velho}" width="8" height="8" fill="#33507E"',
                      f'<rect x="24.7" y="{novo}" width="8" height="8" fill="#33507E"')
    for velho, novo in CIRCULOS_OESTE.items():
        h = h.replace(f'<circle cx="48.5" cy="{velho}" r="4" fill="#33507E"',
                      f'<circle cx="48.5" cy="{novo}" r="4" fill="#33507E"')
        h = h.replace(f'<circle cx="48.5" cy="{velho}" r="6" fill="#33507E" stroke="#3F3F3F" stroke-width="1.4"/><text x="62.0" y="{float(velho) + 3.4:.1f}"',
                      f'<circle cx="48.5" cy="{novo}" r="6" fill="#33507E" stroke="#3F3F3F" stroke-width="1.4"/><text x="62.0" y="{float(novo) + 3.4:.1f}"')
    h = revisa(h, [
        ('<p class="cap">Onde cada uma fica: na boca do seu corredor, <strong>a 4,6 m da parede</strong> —\n  cinco na oeste, cinco na norte, seis na leste.</p>',
         '<p class="cap">Onde cada uma fica: na boca do seu corredor, <strong>a 4,6 m da parede</strong> —\n  cinco na oeste, cinco na norte, seis na leste. Desde 22/09 cada placa lista as seções <strong>por mesa</strong>, com uma seta para o lado da mesa: a placa fica entre as duas mesas do par, e a seta diz de que lado é a fila de cada seção. Nos grupos de uma mesa só (A3, B2, C5, C1) não há seta.</p>'),
        ('<div class="sp"><dt>Corpo</dt><dd>dígitos 160–260 mm · lido a 25 m · quanto menor o grupo, maior o número</dd></div>',
         '<div class="sp"><dt>Corpo</dt><dd>dígitos 160–260 mm · lido a 25 m · quanto menor o grupo, maior o número · seções por mesa, com seta para o lado da mesa</dd></div>'),
    ])

    # o preferencial: empilhado como a referência do Posto, sem faixa institucional
    h = revisa(h, [
        ('O vão da S7 tem <strong>1,27 m</strong>',
         'Desde 22/09 a peça é a placa de referência do Posto refeita em vetor e em Montserrat: fundo azul <code>#1E3674</code>, moldura branca, o título numa caixa branca e os cinco pictogramas em branco — sem a faixa institucional, por decisão do Posto. O vão da S7 tem <strong>1,27 m</strong>'),
    ], secao(h, "arquivo <code>P5-preferencial</code>"))

    # a paleta
    h = revisa(h, [
        ('<div class="sw"><i style="background:#C8102E"></i><b>#C8102E</b><span>Porta C · leste — rolo laranja em estoque · marinho, 4,4:1</span></div>',
         '<div class="sw"><i style="background:#C8102E"></i><b>#C8102E</b><span>Porta C · leste — <strong>vermelho, rolo a comprar</strong> (era o laranja <code>#DE7343</code> até 22/09) · texto branco, 5,9:1</span></div>\n    <div class="sw"><i style="background:#1E3674"></i><b>#1E3674</b><span>Azul da placa preferencial — medido na referência do Posto de 22/09; só na P5-Preferencial</span></div>'),
        ('<p class="texto">As três cores de porta <strong>não se ajustam à identidade</strong>: são cor de rolo\n  de fita já comprada. Mexer numa delas é mexer numa compra. É por isso que o amarelo da porta B e o\n  ouro da marca convivem sendo dois amarelos — e por isso a tarja da B nunca encosta no logotipo.</p>',
         '<p class="texto">As cores de porta <strong>não se ajustam à identidade</strong>: são cor de rolo\n  de fita. Mexer numa delas é mexer numa compra. É por isso que o amarelo da porta B e o\n  ouro da marca convivem sendo dois amarelos — e por isso a tarja da B nunca encosta no logotipo.\n  <strong>Em 22/09 o Posto trocou o laranja da C por vermelho:</strong> o rolo vermelho ainda não existe, então\n  <code>#C8102E</code> é proposta até a compra — quando o rolo chegar, o hex se ajusta a ele. Com isso a\n  tinta sobre a C passou a branco (marinho sobre o vermelho dá 2,4:1), e no layout final dos separadores as\n  mesas de alta carga deixaram o vermelho e viraram roxas, para que vermelho signifique só “zona C”.</p>'),
    ])

    # pendências
    h = revisa(h, [
        ('<li>Confirmar os três hexes contra o rolo de fita — foram lidos da foto do estoque, não medidos.</li>',
         '<li>Confirmar os hexes de A e B contra o rolo de fita — foram lidos da foto do estoque, não medidos. O vermelho da C (<code>#C8102E</code>) é proposta: o rolo ainda não foi comprado, e o hex final é o do rolo.</li>'),
        ('<li>Medir em campo: a profundidade da sala de apoio (7,80 m é suposição), o vão da S7 e o recorte do canto sudoeste, que tem duas leituras no repositório.</li>',
         '<li>Medir em campo: o vão da S7 e o recorte do canto sudoeste, que tem duas leituras no repositório. <s>A profundidade da sala de apoio</s> saiu da lista em 22/09: é um recuo para dentro da parede oeste, fora do piso do salão.</li>'),
        ('<li>Decidir o cruzamento da zona A: aceitar os 2,91 m de desvio até a porta, com orientador, ou deslocar o Ring 3 para leste.</li>',
         '<li><s>Decidir o cruzamento da zona A.</s> <strong>Resolvido em 22/09:</strong> a boca da A passou para o extremo oeste e a saída fica no extremo leste, a 2,91 m do eixo da S4, no batente do vão; o cruzamento do apron fica com o orientador R5/A2. Falta <strong>confirmar com o RDS que os quatro painéis do gradil da face norte podem ser abertos</strong> — o corredor de chegada e as saídas C, B e A, cotadas do canto nordeste na folha de montagem.</li>'),
    ])

    # rodapé
    h = revisa(h, [
        ('<footer>\n  Revisão de <strong>21/09/2026</strong>, na segunda rodada: paleta medida no logotipo vetorizado,',
         '<footer>\n  Revisão de <strong>22/09/2026</strong>, na terceira rodada: zona C vermelha (rolo a comprar), P0-Consulta em dois\n  pontos com o QR estático do site do TSE, bocas do Ring com o corpo branco, preferencial empilhada como a referência\n  do Posto, as dezesseis placas por mesa com setas, e os mapas com a boca da A a oeste, as saídas da face norte e a\n  parede oeste 1,50 m ao norte. Antes, em 21/09: paleta medida no logotipo vetorizado,', 'zona C vermelha (rolo a comprar), P0-Consulta em dois'),
        ('<code>scripts/tabela_mestra.py</code> monta a tabela seção → porta das quatro peças\n  de triagem, e <code>scripts/artes_sinalizacao.py</code> monta a entrada preferencial e as dezesseis\n  placas de grupo, e <code>scripts/paleta.py</code> reprova',
         '<code>scripts/tabela_mestra.py</code> monta a tabela seção → porta das quatro peças\n  de triagem, <code>scripts/artes_sinalizacao.py</code> monta o P0-Consulta (com o QR de\n  <code>scripts/qr_tse.py</code>), as três bocas do Ring, a entrada preferencial e as dezesseis\n  placas de grupo, <code>scripts/plano_consolidado.py</code> embute tudo nesta página, e <code>scripts/paleta.py</code> reprova'),
    ])
    return h


# ---------------------------------------------------------------- revisão de 23/09
FICHA_FIM_C = """<section class="ficha">
  <div class="fc-arte">
    <div class="arte" style="width:430px;height:170px"><div style="width:1040px;height:410px;transform:scale(0.4135);transform-origin:top left">
CORPO_AQUI
</div></div>
    <p class="cap">2080 × 820 mm · arquivo <code>P4-fim-corredor-C</code></p>
  </div>
  <div class="fc-local">
    <h3><span class="pt">P4</span>Fim do corredor C</h3>
    <div class="ondemapa">MAPA_AQUI</div>
    <p class="onde"><strong>Onde:</strong> Parede leste, no extremo norte da banda da zona C, virada para quem chega pelo corredor.</p>
    <p class="texto">Peça nova em 23/09. O corredor da parede leste termina ao norte do último grupo, então quem anda até o fim tem <em>todos</em> os grupos atrás de si — não há nada adiante. A peça é a correção desse engano: de um lado a seta e as seções do C6, o grupo do fim da parede; do outro, as catorze seções que ficam para o sul, na ordem em que se volta a encontrá-las. As setas dizem esquerda e direita; os subtítulos dizem norte e sul, que é o que não muda com a direção para onde o eleitor está virado.</p>
    <dl class="specs"><div class="sp"><dt>Medida</dt><dd>2080 × 820 mm</dd></div><div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div><div class="sp"><dt>Modelo</dt><dd>Fence banner 2080 × 820 mm</dd></div><div class="sp"><dt>Corpo</dt><dd>seções 62 mm · lido a 10 m</dd></div><div class="sp"><dt>Fixação</dt><dd>amarrado no trilho externo da avenida C com tie wraps</dd></div></dl>
  </div>
</section>
"""

MARCADOR_S6 = ('<rect x="225.9" y="276.2" width="16" height="16" fill="#C8102E" stroke="#3F3F3F" stroke-width="1.4"/>\n'
               '<text x="233.9" y="287.2" text-anchor="middle" style="font:800 8px Montserrat,sans-serif" fill="#3F3F3F">P6</text>')
MARCADOR_FIM = ('<rect x="295.3" y="58.0" width="16" height="16" fill="#C8102E" stroke="#3F3F3F" stroke-width="1.4"/>\n'
                '<text x="303.3" y="69.0" text-anchor="middle" style="font:800 8px Montserrat,sans-serif" fill="#3F3F3F">P4</text>')


def revisao_23_09(h):
    """A peça nova do fim do corredor C, os painéis de porta que passaram a sair
    de dados, e o orçamento com o 12º fence banner."""
    # a ficha nova entra logo depois da do painel da porta C, que é a última
    # peça de dentro do salão antes da saída; o mapa é o dela, com o marcador
    # movido da porta S6 para o extremo norte da banda leste
    if "P4-fim-corredor-C" not in h:
        a, f = secao(h, "arquivo <code>P6-painel-porta-C</code>")
        i = h.index('<div class="ondemapa">', a) + len('<div class="ondemapa">')
        mapa = h[i:h.index("</svg>", i) + len("</svg>")]
        assert MARCADOR_S6 in mapa
        mapa = mapa.replace(MARCADOR_S6, MARCADOR_FIM)
        ficha = FICHA_FIM_C.replace("MAPA_AQUI", mapa).replace("CORPO_AQUI", corpo("P4-FimCorredorC"))
        h = h[:f] + "\n" + ficha + h[f:]

    # os painéis de porta passam a sair de grupos_mesas.json, e os da A e da C
    # marcam o primeiro e o último grupo do corredor
    h = revisa(h, [
        ('<p class="onde"><strong>Onde:</strong> Logo depois da porta S4, dentro do salão, do lado oposto à curva do eleitor.</p>',
         '<p class="onde"><strong>Onde:</strong> Logo depois da porta S4, dentro do salão, do lado oposto à curva do eleitor.</p>\n'
         '    <p class="texto">Desde 23/09 a lista sai de <code>data/grupos_mesas.json</code>, na ordem em que o eleitor encontra os grupos subindo o corredor, e marca as duas pontas: o <strong>A1</strong> logo na entrada e o <strong>A5</strong> no fim, o mais distante da porta. Foi a reordenação da parede oeste do mesmo dia que obrigou: as quatro duplas trocaram de lugar e a peça escrita à mão ficou errada em quatro linhas.</p>'),
        ('<p class="onde"><strong>Onde:</strong> Logo depois da porta S6, dentro do salão.</p>',
         '<p class="onde"><strong>Onde:</strong> Logo depois da porta S6, dentro do salão.</p>\n'
         '    <p class="texto">Mesma regra da porta A, desde 23/09: a lista sai dos dados, na ordem de caminhada, com o <strong>C1</strong> logo na entrada e o <strong>C6</strong> no fim do corredor.</p>'),
    ])

    # orçamento: mais um fence banner
    h = revisa(h, [
        ('O segundo P0-Consulta entrou em 22/09: é o 11º fence banner. a € 32.40 pelo unitário da cotação.',
         'O segundo P0-Consulta entrou em 22/09 e o fim do corredor C em 23/09: são o 11º e o 12º fence banner. a € 32.40 pelo unitário da cotação.'),
    ])

    h = revisa(h, [
        ('<footer>\n  Revisão de <strong>22/09/2026</strong>, na terceira rodada:',
         '<footer>\n  Revisão de <strong>23/09/2026</strong>, na quarta rodada: a parede oeste reordenada — as duas duplas de menor\n  comparecimento passaram para a entrada do corredor, e os códigos A1 a A5 foram junto com a posição —, os três\n  painéis de porta gerados de dados, e a peça nova do fim do corredor C. Antes, em <strong>22/09</strong>:'),
    ])
    return h


# ---------------------------------------------------------------- contagem e orçamento
# Quantidade de peças e orçamento saem por regex e não por par (velho, novo):
# duas rodadas seguidas mexeram nos mesmos números, e um par datado quebra
# assim que a rodada seguinte passa por cima dele.
PECAS_EXTERNAS = 19
FENCE_N, FENCE_UNIT = 12, 32.40
ITENS_TOTAL = 41
SEM_IVA, IVA, COM_IVA = 1234.37, 283.90, 1518.27


def numeros(h):
    h = re.sub(r'(<div class="fact"><dt>Peças externas</dt><dd>)\d+(</dd>)',
               rf'\g<1>{PECAS_EXTERNAS}\g<2>', h)
    h = re.sub(r'(<div class="fact"><dt>Orçamento</dt><dd>€ )\d+(</dd>)',
               rf'\g<1>{SEM_IVA:.0f}\g<2>', h)
    h = re.sub(r'(<p class="lede">)\d+( peças externas e 21 internas\.)',
               rf'\g<1>{PECAS_EXTERNAS}\g<2>', h)
    h = re.sub(r'(<tr><td>Fence banner 2080 × 820 mm</td><td class="n">)\d+'
               r'(</td><td class="n">€ )[\d.]+(</td><td class="n">€ )[\d.]+(</td></tr>)',
               rf'\g<1>{FENCE_N}\g<2>{FENCE_UNIT:.0f}\g<3>{FENCE_N * FENCE_UNIT:.0f}\g<4>', h)
    h = re.sub(r'(<tfoot><tr><td>Total sem IVA</td><td class="n">)\d+(</td><td></td>\n'
               r'<td class="n">€ )[\d.]+(</td></tr>\n<tr><td>IVA 23%</td><td></td><td></td>'
               r'<td class="n">€ )[\d.]+(</td></tr>\n<tr><td>Total a pagar</td><td></td><td></td>'
               r'<td class="n">€ )[\d.]+(</td></tr>)',
               rf'\g<1>{ITENS_TOTAL}\g<2>{SEM_IVA}\g<3>{IVA}\g<4>{COM_IVA}\g<5>', h)
    return h


def monta():
    h = PAGINA.read_text(encoding="utf-8")
    h = revisao_22_09(h)
    h = revisao_23_09(h)
    h = troca_artes(h)
    h = troca_galeria(h)
    return numeros(h)


def main():
    grava = "--grava" in sys.argv[1:]
    atual = PAGINA.read_text(encoding="utf-8")
    novo = monta()
    if novo == atual:
        print("mapa/plano_sinalizacao.html em dia com as peças")
        return 0
    if grava:
        PAGINA.write_text(novo, encoding="utf-8")
        print(f"regravado mapa/plano_sinalizacao.html ({len(atual)} → {len(novo)} bytes)")
        return 0
    print("mapa/plano_sinalizacao.html difere das peças; rode com --grava", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
