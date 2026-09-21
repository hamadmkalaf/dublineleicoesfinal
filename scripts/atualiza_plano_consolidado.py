import json, pathlib, re, subprocess, sys
sys.path.insert(0, 'scripts')
from paleta import FONTE, IMPORT_FONTE

RAIZ = pathlib.Path('/home/user/dublineleicoesfinal')
BASE = '1edcfcc'        # o commit de que saiu a versão 4 publicada
h = (RAIZ / 'mapa' / 'plano_sinalizacao.html').read_text(encoding='utf-8')
n0 = len(h)
corpo = lambda t: t[t.index('<div style="width: '):t.rindex('</div>\n</x-dc>') + 6]
sh = lambda n: corpo(subprocess.run(['git', '-C', str(RAIZ), 'show', f'{BASE}:mapa/sinalizacao/{n}.dc.html'],
                                    capture_output=True, text=True, check=True).stdout)
agora = lambda n: corpo((RAIZ / 'mapa/sinalizacao' / f'{n}.dc.html').read_text(encoding='utf-8'))

grupos = json.loads((RAIZ / 'data/grupos_mesas.json').read_text(encoding='utf-8'))['grupos']
pecas = ['P0-Consulta', 'P0-Mestra', 'P1-Portao', 'P2-ParedeLeste', 'P3-EntradaRing',
         'P4-ZonaA', 'P4-ZonaB', 'P4-ZonaC', 'P5-VinilA', 'P5-VinilB', 'P5-VinilC',
         'P5-Preferencial', 'P5-VinilPref', 'P6-PainelA', 'P6-PainelB', 'P6-PainelC',
         'P7-Saida'] + [f"P6-Bloco{g['id']}" for g in grupos]
for n in pecas:
    v = sh(n)
    assert h.count(v) == 1, (n, h.count(v))
    h = h.replace(v, agora(n))
print(f'artes trocadas: {len(pecas)}')

# a tipografia da própria página
trocas = [
    ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800'
     '&family=Nunito+Sans:wght@400;600;700;900&display=swap">',
     f'<link rel="stylesheet" href="{IMPORT_FONTE}">'),
    ("--sans:'Nunito Sans',system-ui,sans-serif; --disp:'Archivo','Nunito Sans',sans-serif;",
     f"--sans:{FONTE}; --disp:{FONTE};"),
    (".rot { font:700 9.5px 'Nunito Sans',sans-serif;", ".rot { font:700 9.5px 'Montserrat',sans-serif;"),
]
for velho, nvo in trocas:
    assert h.count(velho) == 1, ('sem alvo único', velho[:60], h.count(velho))
    h = h.replace(velho, nvo)
# os mapas de posição da própria página declaram a fonte no shorthand `font:`
h, n = re.subn(r'font:(\d+ [\d.,]+px) (?:Nunito Sans|Archivo),sans-serif',
               lambda m: f'font:{m.group(1)} Montserrat,sans-serif', h)
# e um rótulo trazia `8,5px`, com vírgula: shorthand inválido, o navegador
# descartava a declaração inteira e o texto saía no corpo padrão
h, v = re.subn(r'font:(\d+) (\d+),(\d+)px Montserrat', r'font:\1 \2.\3px Montserrat', h)
print(f'tipografia da página trocada ({n} rótulos de mapa, {v} corpo inválido corrigido)')

# a porta do preferencial, na prosa da ficha
velho_onde = ('<p class="onde"><strong>Onde:</strong> Gradil branco de pedestres do apron, '
              'junto à porta S7.</p>')
novo_onde = ('<p class="onde"><strong>Onde:</strong> Gradil branco de pedestres do apron, junto à '
             '<strong>S7 — a porta à direita da C</strong>.</p>')
assert h.count(velho_onde) == 1
h = h.replace(velho_onde, novo_onde)
velho_txt = ('<p class="texto">No gradil branco do apron, junto à S7. O vão da S7 tem '
             '<strong>1,27 m</strong>')
novo_txt = ('<p class="texto">O preferencial <strong>não entra por qualquer porta</strong>: entra '
            'pela <strong>S7</strong>, a primeira à direita da porta C. A peça passou a dizer isso em '
            '21/09 — até então dizia “qualquer porta”, e a tabela da Rota do Eleitor ainda diz. '
            'O vão da S7 tem <strong>1,27 m</strong>')
assert h.count(velho_txt) == 1
h = h.replace(velho_txt, novo_txt)
print('porta do preferencial corrigida na ficha')

# a pendência da compra de fita, e as duas que saíram da lista
velho_pend = ('<li>Trazer o logotipo Eleições 2026 em vetor do TSE — o desenho destas peças é marcação '
              'de lugar — e obter a autorização de uso da marca para posto no exterior.</li>')
novo_pend = ('<li><s>Trazer o logotipo Eleições 2026 em vetor do TSE e obter a autorização de uso da '
             'marca para posto no exterior.</s> <strong>Resolvido em 21/09:</strong> o vetor chegou, a '
             'autorização foi concedida e a fonte da campanha é <strong>Montserrat</strong> — as 36 '
             'peças foram remedidas com ela instalada, porque é mais larga que a anterior no mesmo '
             'corpo. O que ainda é reprodução, e não arquivo oficial, é o desenho do lockup.</li>'
             '<li><strong>Decidir se a compra de fita é refeita.</strong> As três cores de porta não '
             'são escolha de projeto: são o rolo que está em mãos, e a peça impressa persegue a fita. '
             'Refazer a compra resolveria duas coisas de uma vez — a briga entre o amarelo da porta B '
             'e o ouro da marca, e o fato de que, para um deuteranope, B e C têm <strong>1,9:1</strong> '
             'entre si e só a letra as separa. Quem decidir precisa dos metros por cor antes: a conta '
             'de fita é por cor de rolo, não por metro total.</li>')
assert h.count(velho_pend) == 1
h = h.replace(velho_pend, novo_pend)
print('pendências atualizadas')

h = h.replace('faixa institucional off-white como a prancha do sistema já mandava, e os\n'
              '  cinco pictogramas do preferencial no conjunto da referência do Posto',
              'faixa institucional off-white como a prancha do sistema já mandava, tipografia\n'
              '  <strong>Montserrat</strong> — a fonte da campanha —, e os cinco pictogramas do\n'
              '  preferencial no conjunto da referência do Posto')
pathlib.Path(sys.argv[1]).write_text(h, encoding='utf-8')
print(f'{n0} -> {len(h)} bytes')
