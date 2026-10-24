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
# Desde a versão publicada em 25/09 (v10): P1-Portão e o fence banner P5-Preferencial
# saíram do plano, os vinis viraram window stickers e a peça do fim da avenida B foi
# renomeada ao virar roll-up. O adesivo preferencial é a foto real do arquivo
# (mapa/assets/p5-preferencial.jpg), não um .dc.html, e por isso não está aqui.
ARQUIVO = {
    "P0-consulta": "P0-Consulta", "P0-tabela-mestra": "P0-Mestra",
    "P2-parede-leste": "P2-ParedeLeste", "P3-entrada-ring3": "P3-EntradaRing",
    "P4-boca-zona-A": "P4-ZonaA", "P4-boca-zona-B": "P4-ZonaB", "P4-boca-zona-C": "P4-ZonaC",
    "P5-WindowSticker_A": "P5-VinilA", "P5-WindowSticker_B": "P5-VinilB",
    "P5-WindowSticker_C": "P5-VinilC",
    "P6-painel-porta-A": "P6-PainelA", "P6-painel-porta-B": "P6-PainelB", "P6-painel-porta-C": "P6-PainelC",
    "P6-Painel_FimAvenidaB": "P4-FimAvenidaB",
    "P7-saida": "P7-Saida",
}
# a página publicada a partir de 25/09 tem orçamento e contagem de peças escritos à mão
# (window sticker sem preço, P1 e P5-Preferencial fora); numeros() não passa por cima
MARCA_25_09 = "Revisão de <strong>25/09/2026</strong>"

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
         '<li><s>Decidir o cruzamento da zona A.</s> <strong>Resolvido em 22/09:</strong> a boca da A passou para o extremo oeste e a saída fica no extremo leste, a 2,91 m do eixo da S4, no batente do vão; o cruzamento do apron fica com o orientador R5/A2. Falta <strong>confirmar com o RDS que os quatro painéis do gradil da face norte podem ser abertos</strong> — o corredor de chegada e as saídas C, B e A, cotadas do canto nordeste na folha de montagem.</li>',
         # a revisão de 02/10 reescreve o fim desta frase (decisão de 24/09)
         '<li><s>Decidir o cruzamento da zona A.</s> <strong>Resolvido em 22/09:</strong>'),
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
FICHA_FIM_B = """<section class="ficha">
  <div class="fc-arte">
    <div class="arte" style="width:430px;height:170px"><div style="width:1040px;height:410px;transform:scale(0.4135);transform-origin:top left">
CORPO_AQUI
</div></div>
    <p class="cap">2080 × 820 mm · arquivo <code>P4-fim-avenida-B</code></p>
  </div>
  <div class="fc-local">
    <h3><span class="pt">P4</span>Fim da avenida B</h3>
    <div class="ondemapa">MAPA_AQUI</div>
    <p class="onde"><strong>Onde:</strong> Na boca da pequena avenida da parede norte, onde a barreira da avenida B termina — no fim dos 33,6 m que sobem da porta S5, virada para quem chega, a 1,80 m do distribuidor.</p>
    <p class="texto">Peça nova em 23/09. A avenida B é a única que não corre rente à sua parede: ela sobe perpendicular e termina em <strong>T</strong>, e nesse metro quadrado todo o comparecimento da porta B — 3.832 esperados — tem de escolher um lado. A peça existe para que a escolha se faça <em>andando</em>, e não parado no T, que era o ponto mais frágil do traçado inteiro. Em <strong>23/09 (v2)</strong> o último par de unifilas da avenida B saiu e esse 1,80 m virou a <strong>pequena avenida</strong> da parede norte: a peça passa a ser lida na boca dela, e a escolha de lado acontece de fato em movimento, dentro de uma faixa transversal, e não num metro quadrado. À esquerda, na direção da porta A, ficam B1, B2 e B3; à direita, na direção da porta C, B4 e B5. O corte é por mesa, não por grupo: o par <strong>B3 fica escarranchado no vão da avenida</strong>, com uma mesa de cada lado do eixo, então ele sai à esquerda com a ressalva escrita no rodapé de que está bem em frente. Os subtítulos dizem "na direção da porta A" e "na direção da porta C" porque é o que não muda com a direção para onde o eleitor está virado.</p>
    <dl class="specs"><div class="sp"><dt>Medida</dt><dd>2080 × 820 mm</dd></div><div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div><div class="sp"><dt>Modelo</dt><dd>Fence banner 2080 × 820 mm</dd></div><div class="sp"><dt>Corpo</dt><dd>seções 58 mm · lido a 10 m</dd></div><div class="sp"><dt>Fixação</dt><dd>amarrada na última unifila da avenida B com tie wraps</dd></div></dl>
  </div>
</section>
"""

MARCADOR_S6 = ('<rect x="225.9" y="276.2" width="16" height="16" fill="#C8102E" stroke="#3F3F3F" stroke-width="1.4"/>\n'
               '<text x="233.9" y="287.2" text-anchor="middle" style="font:800 8px Montserrat,sans-serif" fill="#3F3F3F">P6</text>')
# A boca da pequena avenida em coordenada da planta do plano: o eixo da avenida B
# (x = 28,30 m) e o fim da barreira dela (y = 33,60 m desde 23/09 (v2), era 35,40 m),
# pela escala do mapa — 6,20 px/m, origem em (20, 297).
MARCADOR_T_V1 = ('<rect x="187.6" y="69.7" width="16" height="16" fill="#E8C63A" stroke="#3F3F3F" stroke-width="1.4"/>\n'
                   '<text x="195.6" y="80.7" text-anchor="middle" style="font:800 8px Montserrat,sans-serif" fill="#3F3F3F">P4</text>')
MARCADOR_T = ('<rect x="187.6" y="80.9" width="16" height="16" fill="#E8C63A" stroke="#3F3F3F" stroke-width="1.4"/>\n'
              '<text x="195.6" y="91.9" text-anchor="middle" style="font:800 8px Montserrat,sans-serif" fill="#3F3F3F">P4</text>')


# O que a versão descartada da peça (fim do corredor C) deixou escrito no plano.
MIGRA_C_PARA_B = [
    ("O segundo P0-Consulta entrou em 22/09 e o fim do corredor C em 23/09: são o 11º e o 12º fence banner.",
     "O segundo P0-Consulta entrou em 22/09 e o fim da avenida B em 23/09: são o 11º e o 12º fence banner."),
    ("painéis de porta gerados de dados, e a peça nova do fim do corredor C. Antes, em <strong>22/09</strong>:",
     "painéis de porta gerados de dados, e a peça nova do fim da avenida B. O recuo das avenidas, pedido e desenhado no\n  mesmo dia, foi revisto à vista da planta e não entrou: a geometria continua a de 22/09. Antes, em <strong>22/09</strong>:"),
]


def revisao_23_09(h):
    """A peça nova do fim da avenida B, os painéis de porta que passaram a sair
    de dados, e o orçamento com o 12º fence banner."""
    # A primeira versão desta peça foi feita para o fim do corredor C. O Posto
    # corrigiu o pedido no mesmo dia -- era a avenida B -, então a ficha da C
    # sai se estiver presente. Vale como migração de quem gerou o plano antes
    # da correção, e é inócua depois.
    if "P4-fim-corredor-C" in h:
        a, f = secao(h, "arquivo <code>P4-fim-corredor-C</code>")
        h = h[:a].rstrip("\n") + "\n" + h[f:].lstrip("\n")
    # As duas frases que citavam a peça descartada. `replace` simples, e não
    # `revisa`, porque tem de ser inócuo quando o plano é remontado do estado
    # de 22/09, em que nenhuma das duas existe.
    for velho, novo in MIGRA_C_PARA_B:
        h = h.replace(velho, novo)

    # a ficha entra logo depois da do painel da porta B, que é a peça de porta
    # imediatamente antes no percurso; o mapa é o da porta C, com o marcador
    # movido da S6 para o T da avenida B
    if "P4-fim-avenida-B" not in h:
        a, f = secao(h, "arquivo <code>P6-painel-porta-C</code>")
        i = h.index('<div class="ondemapa">', a) + len('<div class="ondemapa">')
        mapa = h[i:h.index("</svg>", i) + len("</svg>")]
        assert MARCADOR_S6 in mapa
        mapa = mapa.replace(MARCADOR_S6, MARCADOR_T)
        ficha = FICHA_FIM_B.replace("MAPA_AQUI", mapa).replace("CORPO_AQUI", corpo("P4-FimAvenidaB"))
        _, fb = secao(h, "arquivo <code>P6-painel-porta-B</code>")
        h = h[:fb] + "\n" + ficha + h[fb:]

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
         'O segundo P0-Consulta entrou em 22/09 e o fim da avenida B em 23/09: são o 11º e o 12º fence banner. a € 32.40 pelo unitário da cotação.'),
    ])

    # A frase de 22/09 sobre o 11º fence banner é reinserida pela revisão daquela
    # rodada a cada montagem, e a desta rodada a substitui -- mas só quando ainda
    # não foi aplicada. Nas montagens seguintes as duas convivem, uma dentro da
    # outra. Aqui a mais antiga sai: a nova já diz o que ela dizia.
    h = h.replace(
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner. a € 32.40 "
        "pelo unitário da cotação. O segundo P0-Consulta entrou em 22/09 e o fim "
        "da avenida B", "O segundo P0-Consulta entrou em 22/09 e o fim da avenida B")

    h = revisa(h, [
        ('<footer>\n  Revisão de <strong>22/09/2026</strong>, na terceira rodada:',
         '<footer>\n  Revisão de <strong>23/09/2026</strong>, na quarta rodada: a parede oeste reordenada — as duas duplas de menor\n  comparecimento passaram para a entrada do corredor, e os códigos A1 a A5 foram junto com a posição —, os três\n  painéis de porta gerados de dados, e a peça nova do fim da avenida B. O recuo das avenidas, pedido e desenhado no\n  mesmo dia, foi revisto à vista da planta e não entrou: a geometria continua a de 22/09. Antes, em <strong>22/09</strong>:',
         # a rodada v2 reescreve a frase da geometria dentro deste mesmo rodapé:
         # a marca de idempotência tem de ser só a data da rodada.
         '<footer>\n  Revisão de <strong>23/09/2026</strong>'),
    ])
    return h


# ---------------------------------------------------------------- contagem e orçamento
# Quantidade de peças e orçamento saem por regex e não por par (velho, novo):
# duas rodadas seguidas mexeram nos mesmos números, e um par datado quebra
# assim que a rodada seguinte passa por cima dele.
PECAS_EXTERNAS = 17
# Em 24/09 a P4-FimAvenidaB deixou de ser fence banner e virou o quarto
# pull-up de 1000 x 2000 mm: FENCE_N cai de 12 para 11, e o unitário do
# pull-up 1000 é o da cotação na faixa de 4 unidades (€ 122,99 / 4).
FENCE_N, FENCE_UNIT = 8, 32.40
PULLUP1000_N, PULLUP1000_UNIT = 4, 122.99 / 4
ITENS_TOTAL = 38
SEM_IVA, IVA, COM_IVA = 1138.20, 261.79, 1399.99   # com o window sticker a preço de vinil


# ---------------------------------------------------------------- revisão de 23/09 (v2)
# As duas frases da ficha do P4 antes e depois da pequena avenida. A versão nova
# é a que FICHA_FIM_B já traz, para quem remontar o plano do zero; estas ficam
# aqui para corrigir o HTML que foi gravado em 23/09.
ONDE_V1 = ('<p class="onde"><strong>Onde:</strong> No T da avenida B, no fim dos 35,4 m '
              'que sobem da porta S5, virada para quem chega — a 3 m da banda da parede norte.</p>')
ONDE_V2 = ('<p class="onde"><strong>Onde:</strong> Na boca da pequena avenida da parede '
              'norte, onde a barreira da avenida B termina — no fim dos 33,6 m que sobem da '
              'porta S5, virada para quem chega, a 1,80 m do distribuidor.</p>')
TEXTO_V1 = ('A peça existe para que a escolha se faça <em>andando</em>, e não parado no T, '
               'que é o ponto mais frágil do traçado inteiro.')
TEXTO_V2 = ('A peça existe para que a escolha se faça <em>andando</em>, e não parado no T, '
               'que era o ponto mais frágil do traçado inteiro. Em <strong>23/09 (v2)</strong> o '
               'último par de unifilas da avenida B saiu e esse 1,80 m virou a '
               '<strong>pequena avenida</strong> da parede norte: a peça passa a ser lida na '
               'boca dela, e a escolha de lado acontece de fato em movimento, dentro de uma '
               'faixa transversal, e não num metro quadrado.')
# O rodapé da rodada de 23/09 dizia que nenhuma geometria tinha mudado. A pequena
# avenida mudou uma, e só uma — é o que a frase passa a dizer.
RODAPE_V1 = ('O recuo das avenidas, pedido e desenhado no\n'
             '  mesmo dia, foi revisto à vista da planta e não entrou: a geometria continua a de 22/09.')
RODAPE_V2 = ('O recuo das avenidas, pedido e desenhado no\n'
             '  mesmo dia, foi revisto à vista da planta e não entrou. Na <strong>segunda rodada do mesmo\n'
             '  dia</strong> saiu o último par de unifilas da avenida B: o 1,80 m que sobrou virou a\n'
             '  <strong>pequena avenida da parede norte</strong>, e a P4 do fim da avenida passou a ser lida\n'
             '  na boca dela. É a única mudança de geometria desde 22/09.')


def revisao_23_09_v2(h):
    """A pequena avenida da parede norte muda onde a P4-FimAvenidaB é lida.

    O último par de unifilas da avenida B saiu, a barreira passa a terminar em
    y = 33,60 m e esse 1,80 m vira uma faixa transversal. A peça continua
    amarrada na última unifila — que é a mesma peça de hardware —, mas ela
    deixa de ficar em cima do T e passa a ficar na boca da avenida pequena.
    """
    if "arquivo <code>P4-fim-avenida-B</code>" not in h:
        return h                      # o plano ainda está no estado de 22/09
    a, f = secao(h, "arquivo <code>P4-fim-avenida-B</code>")
    h = revisa(h, [(ONDE_V1, ONDE_V2), (TEXTO_V1, TEXTO_V2),
                   (MARCADOR_T_V1, MARCADOR_T)], (a, f))
    h = revisa(h, [(RODAPE_V1, RODAPE_V2)])
    return h


# ------------------------------------------------------- revisão de 24/09 (roll-up)
# A boca da pequena avenida fica em pleno salão: não há gradil nem barreira
# rígida para amarrar um fence banner ali, só a unifila, que não aguenta o
# peso. A peça vira roll-up autoportante de 1000 x 2000 mm — o mesmo modelo
# dos três painéis de porta — e o corpo gira de paisagem para retrato, com os
# dois lados empilhados (esquerda em cima, direita embaixo) em vez de lado a
# lado; as setas continuam apontando para o lado real, só o enquadramento gira.
WRAPPER_FIM_B_FENCE = ('<div class="arte" style="width:430px;height:170px">'
                       '<div style="width:1040px;height:410px;transform:scale(0.4135);transform-origin:top left">')
WRAPPER_FIM_B_ROLLUP = ('<div class="arte" style="width:250px;height:500px">'
                        '<div style="width:500px;height:1000px;transform:scale(0.5000);transform-origin:top left">')

CAP_FIM_B_FENCE = '<p class="cap">2080 × 820 mm · arquivo <code>P4-fim-avenida-B</code></p>'
CAP_FIM_B_ROLLUP = '<p class="cap">1000 × 2000 mm · arquivo <code>P4-fim-avenida-B</code></p>'

SPECS_FIM_B_FENCE = ('<dl class="specs"><div class="sp"><dt>Medida</dt><dd>2080 × 820 mm</dd></div>'
                     '<div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div>'
                     '<div class="sp"><dt>Modelo</dt><dd>Fence banner 2080 × 820 mm</dd></div>'
                     '<div class="sp"><dt>Corpo</dt><dd>seções 58 mm · lido a 10 m</dd></div>'
                     '<div class="sp"><dt>Fixação</dt><dd>amarrada na última unifila da avenida B com tie wraps</dd></div></dl>')
SPECS_FIM_B_ROLLUP = ('<dl class="specs"><div class="sp"><dt>Medida</dt><dd>1000 × 2000 mm</dd></div>'
                      '<div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div>'
                      '<div class="sp"><dt>Modelo</dt><dd>Pull-up 1000 × 2000 mm</dd></div>'
                      '<div class="sp"><dt>Corpo</dt><dd>seções 76 mm · lido a 5 m</dd></div>'
                      '<div class="sp"><dt>Fixação</dt><dd>autoportante (cassete) — a boca da avenida não tem gradil para amarrar</dd></div></dl>')

TEXTO_FIM_B_FENCE_INICIO = '<p class="texto">Peça nova em 23/09.'
TEXTO_FIM_B_ROLLUP_INICIO = (
    '<p class="texto"><strong>Desde 24/09</strong> é um roll-up autoportante de 1000 × 2000 mm, não mais um '
    'fence banner: a boca da pequena avenida fica em pleno salão, sem gradil ou barreira rígida para amarrar a '
    'peça — só a unifila, que não aguenta o peso do banner. O corpo virou retrato, com os dois lados empilhados '
    'um sobre o outro em vez de lado a lado; as setas continuam apontando para o lado real de quem lê, só o '
    'enquadramento da peça girou. Peça nova em 23/09.')

ORCAMENTO_FIM_B_FENCE = ('O segundo P0-Consulta entrou em 22/09 e o fim da avenida B em 23/09: são o 11º e o '
                         '12º fence banner. a € 32.40 pelo unitário da cotação.')
ORCAMENTO_FIM_B_ROLLUP = (
    'O segundo P0-Consulta entrou em 22/09: é o 11º fence banner, a € 32.40 pelo unitário da cotação. Em 24/09 '
    'a peça do fim da avenida B deixou de ser fence banner e virou o quarto pull-up de 1000 × 2000 mm — mesmo '
    'modelo dos três painéis de porta —, a € 30.75 pelo unitário da cotação na faixa de 4 unidades.')


def revisao_24_09_rollup(h):
    """A P4-FimAvenidaB deixa de ser fence banner: não há gradil na boca da
    pequena avenida para amarrar a peça, só a unifila, que não aguenta o
    peso. Vira roll-up autoportante de 1000 x 2000 mm, como os três painéis
    de porta, e o corpo gira de paisagem para retrato."""
    if "arquivo <code>P4-fim-avenida-B</code>" not in h:
        return h                      # o plano ainda está no estado de 22/09
    a, f = secao(h, "arquivo <code>P4-fim-avenida-B</code>")
    h = revisa(h, [
        (WRAPPER_FIM_B_FENCE, WRAPPER_FIM_B_ROLLUP),
        (CAP_FIM_B_FENCE, CAP_FIM_B_ROLLUP),
        (SPECS_FIM_B_FENCE, SPECS_FIM_B_ROLLUP),
        (TEXTO_FIM_B_FENCE_INICIO, TEXTO_FIM_B_ROLLUP_INICIO),
    ], (a, f))
    h = revisa(h, [(ORCAMENTO_FIM_B_FENCE, ORCAMENTO_FIM_B_ROLLUP)])

    # A frase de 22/09 (ou a de 23/09, que a envolve) é reinserida pelas
    # revisões daquelas rodadas a cada montagem, porque o marcador delas deixa
    # de bater assim que esta rodada reescreve o rabo da frase — o mesmo
    # problema que a limpeza de 23/09 já resolve uma rodada atrás. Aqui a
    # reinserção sai: a frase desta rodada já diz o que as duas diziam.
    h = h.replace(
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner. a € 32.40 pelo unitário da cotação. "
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner, a € 32.40",
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner, a € 32.40")
    h = h.replace(
        "O segundo P0-Consulta entrou em 22/09 e o fim da avenida B em 23/09: são o 11º e o 12º fence banner. "
        "a € 32.40 pelo unitário da cotação. "
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner, a € 32.40",
        "O segundo P0-Consulta entrou em 22/09: é o 11º fence banner, a € 32.40")
    return h


# ------------------------------------------------------- revisão de 02/10 (21026_final)
# O que mudou depois de 24/09 e toca o plano: as duas decisões de 24/09 de seguir
# sem aguardar o RDS, as cotações de 24 e 25/09 que superam a referência de 18/09,
# e o arquivo de impressão da P4-FimAvenidaB em roll-up (29/09). Nenhuma arte muda.
RDS_GRADIL_V1 = ('Falta <strong>confirmar com o RDS que os quatro painéis do gradil da face norte podem ser '
                 'abertos</strong> — o corredor de chegada e as saídas C, B e A, cotadas do canto nordeste na '
                 'folha de montagem.')
RDS_GRADIL_V2 = ('<strong>Decisão de 24/09:</strong> o Posto abre os quatro painéis do gradil da face norte — o '
                 'corredor de chegada e as saídas C, B e A, cotadas do canto nordeste na folha de montagem — '
                 '<strong>sem aguardar a confirmação do RDS</strong>, dado o histórico de demora do local. O risco '
                 'fica assumido, não eliminado. Vale o mesmo para a fita adesiva no piso do Hall 2.')
COTAR_V1 = ('<li>Cotar as quatro linhas que continuam premissa: os 3 banners PVC da parede leste, os '
            '<strong>4</strong> window stickers das portas (vinis até 24/09) — a S7 entrou em 21/09 —, as 2 '
            'placas correx de saída e a fixação.</li>')
COTAR_V2 = ('<li><strong>Cotações de 24 e 25/09</strong>, lado a lado em '
            '<code>Orçamentos/Sinalização/comparativo_cotacoes_2026-09-24.xlsx</code>: o carrinho Helloprint de '
            '24/09 (€ 2.694,68 sem IVA, € 3.314,46 com IVA, cada arte uma linha de 1) <strong>substitui a '
            'referência de 18/09</strong> que a tabela de orçamento acima ainda usa; a proposta Snap Leeson '
            '1554129 revista em 25/09 dá € 4.145,00 sem IVA na opção Basic — já com o quarto pull-up largo, '
            'que é a P6-Painel_FimAvenidaB, e com <strong>4 adesivos laminados 900 × 900 mm a € 280</strong> '
            '(€ 70 cada), o primeiro preço real do window sticker —, mas perdeu os 3 banners PVC da parede '
            'leste e ainda pede 11 fence banners, contra os 8 do plano desde 25/09. O carrinho Helloprint '
            'também foi montado antes de 25/09 (12 fence banners) e não tem os window stickers 900 × 900 nem '
            'a fixação. <strong>Nenhum fornecedor foi escolhido no repositório</strong> até 02/10.</li>')
PRAZO_V1 = ('<li>Decidir o prazo de entrega. Pela cotação de 18/09, a entrega Saver é grátis e chega em 28/09 — seis '
            'dias antes da eleição —, mas o arquivo tem de subir até 18/09 às 13:30. Standard (+ € 35) chega 23/09 e '
            'Express (+ € 38) chega 22/09. É a decisão mais urgente da lista.</li>')
PRAZO_V2 = ('<li><s>Decidir o prazo de entrega pela cotação de 18/09.</s> As datas daquela cotação passaram. Em '
            '<strong>02/10</strong>, a dois dias da eleição, o repositório não registra pedido feito nem data de '
            'entrega: <strong>confirmar com a gráfica escolhida que as peças chegam até a véspera</strong>. É a '
            'decisão mais urgente da lista.</li>')
FIM_B_ARQ_MARCA = 'Arquivo de impressão (29/09)'
FIM_B_LEGENDA = "arquivo <code>P6-Painel_FimAvenidaB</code>"
FIM_B_TEXTO_FIM = "reformatado para o formato vertical.</p>"
FIM_B_ARQ = ('<p class="texto"><strong>Arquivo de impressão (29/09):</strong> '
             '<code>Artes/impressao/P6-Painel_FimAvenidaB.pdf</code>, vetorial na medida de 1000 × 2000 mm, com a '
             'Montserrat embutida como TrueType (o Chromium a imprimia como Type3, que alguns RIPs recusam), e o '
             'JPG de 8000 × 16000 px sem margem, 203 dpi na medida final. Saem de '
             '<code>scripts/render_arte.py</code> sobre a mesma fonte <code>.dc.html</code> desta peça. '
             'A arte desta ficha passou a ser a do roll-up, em retrato: até 02/10 a página mostrava '
             'ainda o desenho do fence banner.</p>')
RODAPE_0210_MARCA = 'Versão <strong>21026_final</strong>'
RODAPE_0210 = ('\n  <br><br>Versão <strong>21026_final</strong>, de <strong>02/10/2026</strong>, sobre a publicada em '
               '25/09: a ficha da P6-Painel_FimAvenidaB passa a mostrar a arte do roll-up em retrato, com o '
               'arquivo de impressão de 29/09; as aberturas do gradil do Ring 3 e a fita no piso do Hall 2 '
               'entram como decisões de 24/09, com risco assumido; e as cotações de 24 e 25/09 e o prazo da '
               'gráfica entram nas pendências. As decisões de 24 e 25/09 desta página — P1 fora do plano, '
               'window stickers, adesivo preferencial como única peça da S7 — ficam como estavam.\n</footer>')


def revisao_02_10(h):
    """Decisões posteriores a 24/09 que tocam o plano, sem mexer em arte."""
    h = revisa(h, [(RDS_GRADIL_V1, RDS_GRADIL_V2), (COTAR_V1, COTAR_V2), (PRAZO_V1, PRAZO_V2),
                   ('\n</footer>', RODAPE_0210, RODAPE_0210_MARCA)])
    a, f = secao(h, FIM_B_LEGENDA)
    # a arte do roll-up no invólucro de retrato (o corpo vem do .dc.html em troca_artes)
    h = revisa(h, [(WRAPPER_FIM_B_FENCE, WRAPPER_FIM_B_ROLLUP)], (a, f))
    if FIM_B_ARQ_MARCA not in h:
        a, f = secao(h, FIM_B_LEGENDA)
        j = h.index(FIM_B_TEXTO_FIM, a, f) + len(FIM_B_TEXTO_FIM)
        h = h[:j] + FIM_B_ARQ + h[j:]
    return h


def numeros(h):
    if MARCA_25_09 in h:
        return h
    h = re.sub(r'(<div class="fact"><dt>Peças externas</dt><dd>)\d+(</dd>)',
               rf'\g<1>{PECAS_EXTERNAS}\g<2>', h)
    h = re.sub(r'(<div class="fact"><dt>Orçamento</dt><dd>€ )\d+(</dd>)',
               rf'\g<1>{SEM_IVA:.0f}\g<2>', h)
    h = re.sub(r'(<p class="lede">)\d+( peças externas e 21 internas\.)',
               rf'\g<1>{PECAS_EXTERNAS}\g<2>', h)
    h = re.sub(r'(<tr><td>Fence banner 2080 × 820 mm</td><td class="n">)\d+'
               r'(</td><td class="n">€ )[\d.]+(</td><td class="n">€ )[\d.]+(</td></tr>)',
               rf'\g<1>{FENCE_N}\g<2>{FENCE_UNIT:.0f}\g<3>{FENCE_N * FENCE_UNIT:.0f}\g<4>', h)
    h = re.sub(r'(<tr><td>Pull-up 1000 × 2000 mm</td><td class="n">)\d+'
               r'(</td><td class="n">€ )[\d.]+(</td><td class="n">€ )[\d.]+(</td></tr>)',
               rf'\g<1>{PULLUP1000_N}\g<2>{PULLUP1000_UNIT:.0f}\g<3>{PULLUP1000_N * PULLUP1000_UNIT:.0f}\g<4>', h)
    h = re.sub(r'(<tfoot><tr><td>Total sem IVA</td><td class="n">)\d+(</td><td></td>\n'
               r'<td class="n">€ )[\d.]+(</td></tr>\n<tr><td>IVA 23%</td><td></td><td></td>'
               r'<td class="n">€ )[\d.]+(</td></tr>\n<tr><td>Total a pagar</td><td></td><td></td>'
               r'<td class="n">€ )[\d.]+(</td></tr>)',
               rf'\g<1>{ITENS_TOTAL}\g<2>{SEM_IVA}\g<3>{IVA}\g<4>{COM_IVA}\g<5>', h)
    return h


def monta():
    h = PAGINA.read_text(encoding="utf-8")
    # A página publicada em 25/09 foi revista à mão sobre a de 23/09 (v2) e já traz o
    # que as revisões de 22/09 a 24/09 faziam, com textos próprios que elas não reconhecem.
    if MARCA_25_09 not in h:
        h = revisao_22_09(h)
        h = revisao_23_09(h)
        h = revisao_23_09_v2(h)
        h = revisao_24_09_rollup(h)
    h = revisao_02_10(h)
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
