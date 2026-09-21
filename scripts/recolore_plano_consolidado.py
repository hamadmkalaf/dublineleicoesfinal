import json, pathlib, re, subprocess, sys
sys.path.insert(0, 'scripts')
from paleta import AZUL, GRAFITE, MARINHO, OFFWHITE, OURO, VERDE, ZONA

RAIZ = pathlib.Path('/home/user/dublineleicoesfinal')
BASE = '3fb8534'          # o commit de que saiu a versão 3 publicada
ENTRADA = RAIZ / 'mapa' / 'plano_sinalizacao.html'
SAIDA = pathlib.Path(sys.argv[1])
h = ENTRADA.read_text(encoding='utf-8')
n0 = len(h)


def corpo(t):
    return t[t.index('<div style="width: '):t.rindex('</div>\n</x-dc>') + 6]


def antigo(n):
    return corpo(subprocess.run(['git', '-C', str(RAIZ), 'show', f'{BASE}:mapa/sinalizacao/{n}.dc.html'],
                                capture_output=True, text=True, check=True).stdout)


def novo(n):
    return corpo((RAIZ / 'mapa/sinalizacao' / f'{n}.dc.html').read_text(encoding='utf-8'))


grupos = json.loads((RAIZ / 'data/grupos_mesas.json').read_text(encoding='utf-8'))['grupos']
pecas = ['P0-Consulta', 'P0-Mestra', 'P1-Portao', 'P2-ParedeLeste', 'P3-EntradaRing',
         'P4-ZonaA', 'P4-ZonaB', 'P4-ZonaC', 'P5-VinilA', 'P5-VinilB', 'P5-VinilC',
         'P5-Preferencial', 'P5-VinilPref', 'P6-PainelA', 'P6-PainelB', 'P6-PainelC',
         'P7-Saida'] + [f"P6-Bloco{g['id']}" for g in grupos]
trocadas = 0
for n in pecas:
    v = antigo(n)
    if h.count(v) != 1:
        raise SystemExit(f'{n}: {h.count(v)} ocorrências, esperava 1')
    h = h.replace(v, novo(n))
    trocadas += 1
print(f'artes trocadas: {trocadas}')

# a tabela da própria página, com a tinta nova das portas
porta_de = {s: g['entrada'] for g in grupos for s in g['secoes']}
PAREDE = {'A': 'parede oeste · S4', 'B': 'parede norte · S5', 'C': 'parede leste · S6'}
blocos = []
for p in 'ABC':
    fundo, tinta = ZONA[p]
    ss = sorted(s for s, q in porta_de.items() if q == p)
    cels = ''.join(f'<div class="mcel" style="background:{fundo};color:{tinta}">{s:04d}</div>' for s in ss)
    blocos.append(f'<div><div class="mcab" style="background:{fundo};color:{tinta}">PORTA {p} · '
                  f'{len(ss)} SEÇÕES</div><div class="mlista">{cels}</div>'
                  f'<p class="cap">{PAREDE[p]}</p></div>')
i = h.index('<div class="mestra">')
j = h.index('</div></div>\n</section>', i) + len('</div></div>')
h = h[:i] + '<div class="mestra">' + ''.join(blocos) + '</div>' + h[j:]
print('tabela da página recolorida')

# a paleta da página: tinta marinha, acentos oficiais
for velho, nvo in [('--tinta:#3F3F3F;', f'--tinta:{MARINHO};'),
                   ('--ground:#F0F0E8;', f'--ground:{OFFWHITE};'),
                   ('--b-ink:#7D6004;', f'--b-ink:{MARINHO};'),
                   ('--c-ink:#9C4118;', f'--c-ink:{MARINHO};')]:
    if velho not in h:
        raise SystemExit(f'CSS sem alvo: {velho}')
    h = h.replace(velho, nvo, 1)

CSS = f"""
  .pal {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:20px 0 6px }}
  .sw {{ border:1px solid var(--rule) }}
  .sw i {{ display:block; height:56px }}
  .sw b {{ display:block; font-family:ui-monospace,Menlo,monospace; font-size:12px; padding:7px 10px 0 }}
  .sw span {{ display:block; font-size:13px; color:var(--muted); padding:1px 10px 9px }}
"""
h = h.replace('  :focus-visible { outline:2px solid var(--a-ink); outline-offset:3px }\n',
              '  :focus-visible { outline:2px solid var(--a-ink); outline-offset:3px }\n' + CSS, 1)


def sw(hexa, nome, onde):
    return (f'<div class="sw"><i style="background:{hexa}"></i>'
            f'<b>{hexa}</b><span>{nome} — {onde}</span></div>')


SECAO = f"""<section class="bloco">
  <h2>A paleta, medida e não lembrada</h2>
  <p class="lede">As quatro cores da identidade foram lidas pixel a pixel no logotipo vetorizado que o
  Posto entregou em 21/09. Até então <strong>as quatro estavam erradas em todas as 36 peças</strong> —
  sempre por pouco, nunca certo: <code>#F2CE3A</code> no lugar do ouro, <code>#4888A8</code> e
  <code>#5A8CAA</code> no do azul, <code>#588018</code> e <code>#648232</code> no do verde.</p>
  <div class="pal">
    {sw(GRAFITE, 'Grafite', 'a palavra ELEIÇÕES; só dentro do lockup')}
    {sw(OURO, 'Ouro', 'o 2026 e a onda de cima; só dentro do lockup')}
    {sw(AZUL, 'Azul', 'a onda do meio e o NA da hashtag')}
    {sw(VERDE, 'Verde', 'a onda de baixo, o # e o acento de ação')}
  </div>
  <p class="texto">A faixa do topo era uma tarja escura <code>#5A6E6E</code> que não existe na marca.
  A prancha do sistema já mandava outra coisa desde 17/09 — <em>“a faixa virou off-white com régua
  marinha; o amarelo agora só significa porta B”</em> —, e a razão está escrita lá: uma faixa amarela
  no alto diria “porta B” a 30 m <strong>em toda peça</strong>, inclusive nas de A e de C. As peças só
  não tinham recebido a decisão.</p>
  <div class="pal">
    {sw(OFFWHITE, 'Off-white', 'a faixa institucional')}
    {sw(MARINHO, 'Marinho', 'toda a tipografia do plano e a régua da faixa')}
    {sw(ZONA['A'][0], 'Porta A · oeste', 'rolo azul em estoque · texto branco, 8,1:1')}
    {sw(ZONA['B'][0], 'Porta B · norte', 'rolo amarelo em estoque · marinho, 8,4:1')}
    {sw(ZONA['C'][0], 'Porta C · leste', 'rolo laranja em estoque · marinho, 4,4:1')}
  </div>
  <p class="texto">As três cores de porta <strong>não se ajustam à identidade</strong>: são cor de rolo
  de fita já comprada. Mexer numa delas é mexer numa compra. É por isso que o amarelo da porta B e o
  ouro da marca convivem sendo dois amarelos — e por isso a tarja da B nunca encosta no logotipo.</p>
</section>

"""
h = h.replace('<section class="bloco">\n  <h2>Onde o orçamento vai</h2>',
              SECAO + '<section class="bloco">\n  <h2>Onde o orçamento vai</h2>', 1)
print('seção da paleta inserida')

h = h.replace('Revisão de <strong>21/09/2026</strong>.',
              'Revisão de <strong>21/09/2026</strong>, na segunda rodada: paleta medida no logotipo '
              'vetorizado, faixa institucional off-white como a prancha do sistema já mandava, e os '
              'cinco pictogramas do preferencial no conjunto da referência do Posto — idoso, gestante, '
              'criança de colo, muleta e o laço do espectro autista.')
h = h.replace('<code>scripts/artes_sinalizacao.py</code> monta a entrada preferencial e as dezesseis\n'
              '  placas de grupo.',
              '<code>scripts/artes_sinalizacao.py</code> monta a entrada preferencial e as dezesseis\n'
              '  placas de grupo, e <code>scripts/paleta.py</code> reprova qualquer peça que use cor de\n'
              '  fora de <code>data/paleta.json</code>.')
SAIDA.write_text(h, encoding='utf-8')
print(f'{n0} -> {len(h)} bytes')
