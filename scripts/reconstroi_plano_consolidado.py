import json, pathlib, re, subprocess, sys

RAIZ = pathlib.Path('/home/user/dublineleicoesfinal')
SALVO = pathlib.Path('/root/.claude/projects/-home-user/abd9f807-97d4-58c7-83b8-49fb53253f81/'
                     'tool-results/artifact-6d192c67-1789698169-9c01.html')
BASE = '7fb6c79'          # o commit de onde saiu o artefato publicado
SAIDA = pathlib.Path(sys.argv[1])

h = SALVO.read_text(encoding='utf-8')
n0 = len(h)


def corpo(texto):
    """O <div> da arte dentro de um .dc.html, sem o invólucro da plataforma."""
    i = texto.index('<div style="width: ')
    j = texto.rindex('</div>\n</x-dc>')
    return texto[i:j + 6]


def antigo(nome):
    return corpo(subprocess.run(['git', '-C', str(RAIZ), 'show', f'{BASE}:mapa/sinalizacao/{nome}.dc.html'],
                                capture_output=True, text=True, check=True).stdout)


def novo(nome):
    return corpo((RAIZ / 'mapa/sinalizacao' / f'{nome}.dc.html').read_text(encoding='utf-8'))


# ---------------------------------------------------------------- 1. as artes trocadas
for nome in ('P0-Mestra', 'P1-Portao', 'P2-ParedeLeste', 'P3-EntradaRing', 'P5-Preferencial'):
    velho = antigo(nome)
    assert h.count(velho) == 1, (nome, h.count(velho))
    h = h.replace(velho, novo(nome))
print('artes trocadas: 5')

# ---------------------------------------------------------------- 2. CSS novo
CSS = """
  .mestra { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:0 20px; margin:20px 0 6px }
  @media (max-width:700px) { .mestra { grid-template-columns:1fr; gap:18px 0 } }
  .mcab { font-family:var(--disp); font-weight:800; font-size:14.5px; letter-spacing:.05em; padding:7px 11px }
  .mlista { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:3px; margin-top:5px }
  .mcel { font-family:var(--disp); font-weight:700; font-size:15.5px; text-align:center; padding:4px 2px;
          font-variant-numeric:tabular-nums }
  .galeria { display:grid; grid-template-columns:repeat(auto-fill,122px); gap:16px; margin:22px 0 20px;
             justify-content:space-between }
  .gart { width:122px; height:287px; overflow:hidden; border:1px solid var(--rule-soft); background:#FFF;
          box-shadow:0 1px 3px rgba(0,0,0,.09) }
  .gart > div { transform:scale(0.287); transform-origin:top left }
"""
h = h.replace('  :focus-visible { outline:2px solid var(--a-ink); outline-offset:3px }\n',
              '  :focus-visible { outline:2px solid var(--a-ink); outline-offset:3px }\n' + CSS, 1)

# ---------------------------------------------------------------- 3. a tabela da página, por porta
grupos = json.loads((RAIZ / 'data/grupos_mesas.json').read_text(encoding='utf-8'))['grupos']
porta_de = {s: g['entrada'] for g in grupos for s in g['secoes']}
CORES = {'A': ('#33507E', '#FFFFFF'), 'B': ('#E8C63A', '#3F3F3F'), 'C': ('#DE7343', '#3F3F3F')}
PAREDE = {'A': 'parede oeste · S4', 'B': 'parede norte · S5', 'C': 'parede leste · S6'}

blocos = []
for p in 'ABC':
    fundo, tinta = CORES[p]
    secoes = sorted(s for s, q in porta_de.items() if q == p)
    cels = ''.join(f'<div class="mcel" style="background:{fundo};color:{tinta}">{s:04d}</div>'
                   for s in secoes)
    blocos.append(
        f'<div><div class="mcab" style="background:{fundo};color:{tinta}">PORTA {p} · '
        f'{len(secoes)} SEÇÕES</div><div class="mlista">{cels}</div>'
        f'<p class="cap">{PAREDE[p]}</p></div>')
nova_mestra = '<div class="mestra">' + ''.join(blocos) + '</div>'

i = h.index('<div class="mestra">')
j = h.index('</div></div>\n</section>', i) + len('</div></div>')
antes = h[i:j]
assert antes.count('class="mrow"') == 51
h = h[:i] + nova_mestra + h[j:]
h = h.replace(
    'As 51 seções em ordem crescente. É o conteúdo literal de P0, P1, P2 e P3 — quatro pontos,\n'
    '  sete cópias — e a mesma lista que reaparece recortada nas bocas do Ring 3 e nos painéis de porta.',
    'As 51 seções <strong>agrupadas pela porta</strong>, e dentro de cada porta em ordem crescente. '
    'É o conteúdo literal de P0, P1, P2 e P3 — quatro pontos, sete cópias — e a mesma lista que '
    'reaparece recortada nas bocas do Ring 3 e nos painéis de porta. Desde 21/09 a cor do fundo '
    'é a cor da porta: quem achou o número já está olhando para a resposta.')
print('tabela da página regrupada')

# ---------------------------------------------------------------- 4. a planta com as 16 placas
def planta_16():
    k = h.index('P6-bloco-A3')
    a = h.rindex('<div class="ondemapa">', 0, k)
    b = h.index('</svg></div>', a) + len('</svg>')
    svg = h[a + len('<div class="ondemapa">'):b]
    svg = re.sub(r'<circle[^>]*/>', '', svg)          # fora os marcadores do A3
    svg = svg.replace('<rect x="225.9" y="276.2" width="16" height="16" fill="#DE7343" '
                      'stroke="#3F3F3F" stroke-width="1.4"/>\n', '')
    svg = svg.replace('<text x="233.9" y="287.2" text-anchor="middle" '
                      'style="font:800 8px Nunito Sans,sans-serif" fill="#3F3F3F">P6</text>\n', '')
    marcas = []
    for g in grupos:
        p, c = g['entrada'], sum(g['coord']) / len(g['coord'])
        if p == 'B':
            x, y = 19.8 + 6.211 * c, 50.5
            tx, ty, anc = x, 72, 'middle'
        elif p == 'A':
            x, y = 48.5, 297.28 - 6.202 * c
            tx, ty, anc = 62, y + 3.4, 'start'
        else:
            x, y = 303.3, 297.28 - 6.202 * c
            tx, ty, anc = 290, y + 3.4, 'end'
        fundo = CORES[p][0]
        marcas.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{fundo}" stroke="#3F3F3F" stroke-width="1.4"/>'
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}" '
            f'style="font:800 10px Nunito Sans,sans-serif" fill="#3F3F3F">{g["id"]}</text>')
    return svg.replace('</svg>', ''.join(marcas) + '</svg>').replace(
        'Planta do Hall 2 com o ponto desta peça marcado',
        'Planta do Hall 2 com os dezesseis grupos de mesas marcados')


galeria = []
for g in grupos:
    galeria.append(f'<div class="gart">{novo("P6-Bloco" + g["id"])}</div>')

SECAO_BLOCOS = f"""<section class="bloco">
  <h2>As dezesseis placas de grupo</h2>
  <p class="lede">Uma por par de mesas, do A1 ao C6. Até 20/09 existiam duas — A3 e C4, as dos grupos
  maiores —, e os outros catorze corredores não tinham peça nenhuma. <strong>O código do grupo é o
  título da placa:</strong> quem está no par C3 lê <code>C3</code> no alto, o mesmo código que o painel
  da porta C usa na sua lista. É o que fecha porta → grupo → seção com o mesmo rótulo nos dois pontos.
  Nenhuma traz número de mesa: só as seções daquele corredor. É a <strong>peça crítica</strong> do
  plano interno — é ela que fecha a busca.</p>
  <div class="ondemapa">{planta_16()}</div>
  <p class="cap">Onde cada uma fica: na boca do seu corredor, <strong>a 4,6 m da parede</strong> —
  cinco na oeste, cinco na norte, seis na leste.</p>
  <div class="galeria">{''.join(galeria)}</div>
  <dl class="specs"><div class="sp"><dt>Medida</dt><dd>850 × 2000 mm</dd></div><div class="sp"><dt>Quantidade</dt><dd>16 peças</dd></div><div class="sp"><dt>Modelo</dt><dd>Pull-up 850 × 2000 mm</dd></div><div class="sp"><dt>Corpo</dt><dd>dígitos 160–260 mm · lido a 25 m · quanto menor o grupo, maior o número</dd></div><div class="sp"><dt>Altura útil</dt><dd>conteúdo no terço superior: o primeiro número cai a ~1.400 mm do chão</dd></div><div class="sp"><dt>Orçamento</dt><dd>já previstas na cotação de 18/09 — € 398 as dezesseis</dd></div></dl>
</section>

"""

# tira as duas fichas antigas de bloco e põe a seção nova no lugar
k = h.index('P6-bloco-A3')
ini = h.rindex('<section class="ficha">', 0, k)
k2 = h.index('P6-bloco-C4')
fim = h.index('</section>', h.index('</dl>', k2)) + len('</section>')
h = h[:ini] + h[fim:]
# a seção nova entra logo depois do bloco das fichas, antes de "Seção → porta"
h = h.replace('<section class="bloco">\n  <h2>Seção → porta</h2>', SECAO_BLOCOS + '<section class="bloco">\n  <h2>Seção → porta</h2>', 1)
print('galeria das 16 montada')

# ---------------------------------------------------------------- 5. o vinil da porta S7
FACHADA = """<svg viewBox="0 0 430 110" class="mapa" role="img" aria-label="Fachada sul do Hall 2 com os vãos das três entradas e a porta preferencial S7 destacada">
<rect x="10" y="22" width="410" height="58" fill="#DCE6EC" stroke="#9AA3AB"/>
<rect x="107" y="30" width="81" height="50" fill="#FFF" stroke="#33507E" stroke-width="1.4"/>
<text x="148" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="#33507E">S4 &#183; A</text>
<rect x="192" y="30" width="81" height="50" fill="#FFF" stroke="#E8C63A" stroke-width="1.4"/>
<text x="233" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="#7D6004">S5 &#183; B</text>
<rect x="277" y="30" width="81" height="50" fill="#FFF" stroke="#DE7343" stroke-width="1.4"/>
<text x="318" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="#9C4118">S6 &#183; C</text>
<rect x="390" y="28" width="14" height="54" fill="#FFF" stroke="#648232" stroke-width="3"/>
<circle cx="397" cy="42" r="3.2" fill="#648232"/>
<path d="M397 46 L397 55 M392 49 L402 49 M397 55 L393 63 M397 55 L401 63" stroke="#648232" stroke-width="2" fill="none" stroke-linecap="round"/>
<text x="397" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="#648232">S7</text>
<text x="10" y="16" class="rot">FACHADA SUL &#183; vista de quem chega do Ring 3</text>
</svg>"""
FICHA_VINIL = f"""<section class="ficha">
  <div class="fc-arte">
    <div class="arte" style="width:430px;height:251px"><div style="width:600px;height:350px;transform:scale(0.7167);transform-origin:top left">{novo('P5-VinilPref')}</div></div>
    <p class="cap">1200 × 700 mm · arquivo <code>P5-vinil-preferencial</code></p>
  </div>
  <div class="fc-local">
    <h3><span class="pt">P5</span>Porta preferencial no vidro</h3>
    <div class="ondemapa">{FACHADA}</div>
    <p class="onde"><strong>Onde:</strong> Por dentro do vidro da fachada sul, sobre o vão da <strong>S7</strong>.</p>
    <p class="texto">A S7 é a porta preferencial e era a única das quatro sem peça no vidro — A, B e C já
    tinham a sua letra. Sem ela, a porta que mais precisa ser achada de longe é a única que não se anuncia.
    Leva os mesmos cinco pictogramas do banner, para que a pessoa reconheça a mesma coisa duas vezes.</p>
    <dl class="specs"><div class="sp"><dt>Medida</dt><dd>1200 × 700 mm</dd></div><div class="sp"><dt>Quantidade</dt><dd>1 peça</dd></div><div class="sp"><dt>Modelo</dt><dd>Vinil recortado por porta</dd></div><div class="sp"><dt>Corpo</dt><dd>pictogramas de 200 mm · o vão da S7 tem 1,27 m</dd></div><div class="sp"><dt>Fixação</dt><dd>colado no vidro; sai sem resíduo</dd></div></dl>
  </div>
</section>"""

k = h.index('P5-preferencial</code>')
fim_pref = h.index('</section>', h.index('</dl>', k)) + len('</section>')
h = h[:fim_pref] + FICHA_VINIL + h[fim_pref:]
print('ficha do vinil S7 inserida')

# ---------------------------------------------------------------- 6. números e textos
trocas = [
    ('<div class="fact"><dt>Peças externas</dt><dd>16</dd></div>',
     '<div class="fact"><dt>Peças externas</dt><dd>17</dd></div>'),
    ('<div class="fact"><dt>Orçamento</dt><dd>€ 1140</dd></div>',
     '<div class="fact"><dt>Orçamento</dt><dd>€ 1170</dd></div>'),
    ('<p class="lede">16 peças externas e 21 internas.',
     '<p class="lede">17 peças externas e 21 internas.'),
    ('<tr><td>Vinil recortado por porta</td><td class="n">3</td><td class="n">€ 30</td><td class="n">€ 90</td></tr>',
     '<tr><td>Vinil recortado por porta</td><td class="n">4</td><td class="n">€ 30</td><td class="n">€ 120</td></tr>'),
    ('<tfoot><tr><td>Total sem IVA</td><td class="n">38</td><td></td>\n<td class="n">€ 1139.57</td></tr>',
     '<tfoot><tr><td>Total sem IVA</td><td class="n">39</td><td></td>\n<td class="n">€ 1169.57</td></tr>'),
    ('<tr><td>IVA 23%</td><td></td><td></td><td class="n">€ 262.10</td></tr>',
     '<tr><td>IVA 23%</td><td></td><td></td><td class="n">€ 269.00</td></tr>'),
    ('<tr><td>Total a pagar</td><td></td><td></td><td class="n">€ 1401.67</td></tr>',
     '<tr><td>Total a pagar</td><td></td><td></td><td class="n">€ 1438.57</td></tr>'),
    ('Quatro linhas — PVC. vinil. correx e fixação — ainda são premissa: a cotação não as precificou.',
     'Quatro linhas — PVC. vinil. correx e fixação — ainda são premissa: a cotação não as precificou. '
     'O quarto vinil. da S7. entrou em 21/09 e herda essa incerteza. As dezesseis placas de grupo. ao '
     'contrário. já estavam na cotação de 18/09: o que faltava eram as artes.'),
    ('<li>Cotar as quatro linhas que continuam premissa: os 3 banners PVC da parede leste, os 3 vinis das portas, as 2 placas correx de saída e a fixação.</li>',
     '<li>Cotar as quatro linhas que continuam premissa: os 3 banners PVC da parede leste, os <strong>4</strong> vinis das portas — a S7 entrou em 21/09 —, as 2 placas correx de saída e a fixação.</li>'),
]
for velho, nvo in trocas:
    assert h.count(velho) == 1, ('troca sem alvo único', velho[:60], h.count(velho))
    h = h.replace(velho, nvo)

RODAPE_VELHO = h[h.index('<footer>'):h.index('</footer>') + len('</footer>')]
RODAPE = """<footer>
  Revisão de <strong>21/09/2026</strong>. As artes desta página são a fonte versionada de
  <code>mapa/sinalizacao/</code> no repositório <code>dublineleicoesfinal</code>, embutida aqui tal como
  sai dos geradores: <code>scripts/tabela_mestra.py</code> monta a tabela seção → porta das quatro peças
  de triagem, e <code>scripts/artes_sinalizacao.py</code> monta a entrada preferencial e as dezesseis
  placas de grupo. Os dois leem <code>data/grupos_mesas.json</code> e, sem <code>--grava</code>, saem com
  código 1 se as peças divergirem — as 51 seções aparecem exatamente uma vez, a união das dezesseis
  placas é exatamente a tabela mestra, e o código de cada placa aparece na lista do painel da sua porta.
</footer>"""
h = h.replace(RODAPE_VELHO, RODAPE)
print('números, ressalvas e rodapé atualizados')

# As caixas de escala das miniaturas não batem com o tamanho real da arte: uma
# arte de 1040 x 410 dentro de uma caixa declarada de 1000 x 500 perde 40 px à
# direita -- some a hashtag do cabeçalho -- e ganha uma faixa branca embaixo.
# Recalcula cada cartão a partir do tamanho real, mantendo a largura de coluna.
PADRAO = re.compile(
    r'<div class="arte" style="width:(\d+)px;height:\d+px">'
    r'<div style="width:\d+px;height:\d+px;transform:scale\([\d.]+\);transform-origin:top left">'
    r'(<div style="width: ([\d.]+)px; height: ([\d.]+)px)')


def conserta(m):
    larg = int(m.group(1))
    aw, ah = float(m.group(3)), float(m.group(4))
    esc = larg / aw
    return (f'<div class="arte" style="width:{larg}px;height:{round(ah * esc)}px">'
            f'<div style="width:{aw:g}px;height:{ah:g}px;transform:scale({esc:.4f});'
            f'transform-origin:top left">{m.group(2)}')


h, n = PADRAO.subn(conserta, h)
print(f'miniaturas recalculadas: {n}')

SAIDA.write_text(h, encoding='utf-8')
print(f'{n0} -> {len(h)} bytes')
