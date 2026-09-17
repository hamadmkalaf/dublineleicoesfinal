# -*- coding: utf-8 -*-
"""O plano de sinalizacao num documento so: cada arte ao lado do seu ponto.

Consolida tres fontes que ate agora viviam separadas:

  - a proposta de arte           saidas/pranchas_sinalizacao/  (as pecas desenhadas)
  - a Rota do Eleitor            saidas/rota_do_eleitor_v2.html (o percurso externo)
  - a Sinalizacao do Hall 2      saidas/sinalizacao_hall2_v2.html (o interno)

Cada peca aparece com a arte de verdade a esquerda -- o mesmo desenho que vai
para a grafica, reduzido -- e, a direita, o recorte da planta com o ponto
marcado, mais o que ela diz, o modelo, a quantidade e a fixacao.

    python3 scripts/pranchas/gera_plano_consolidado.py
"""
import json, pathlib, re

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
PRANCHAS = REPO / 'saidas' / 'pranchas_sinalizacao' / 'project'
SAIDA = REPO / 'saidas' / 'plano_sinalizacao_consolidado.html'

S = json.loads((REPO / 'saidas' / 'sinalizacao_v2.json').read_text(encoding='utf-8'))
R = json.loads((REPO / 'saidas' / 'ring3_montagem.json').read_text(encoding='utf-8'))
P = json.loads((REPO / 'data' / 'prancheta_hall2.json').read_text(encoding='utf-8'))
ART = json.loads((REPO / 'saidas' / 'artes_sinalizacao' / 'indice.json').read_text(encoding='utf-8'))

COR = {'A': '#33507E', 'B': '#E8C63A', 'C': '#DE7343'}
TINTA = {'A': '#33507E', 'B': '#7D6004', 'C': '#9C4118'}
MARINHO, OFFW, AMARELO = '#042B5A', '#F0F0E8', '#F8C030'
PAREDE = {'A': 'oeste', 'B': 'norte', 'C': 'leste'}
PORTA = {'A': 'S4', 'B': 'S5', 'C': 'S6'}
portas = {p['letra']: p for p in S['portas']}
artes = {a['arquivo']: a for a in ART['pecas']}

LX, LY = P['salao']['largura'], P['salao']['altura']
PORTAS_SUL = {'A': (19.1, 25.03), 'B': (25.32, 31.25), 'C': (31.54, 37.47)}


# --------------------------------------------------------------- a arte, inline
def arte(nome_prancha: str, larg_px: float, alt_px: float, alvo_px: float = 430.0) -> str:
    """O corpo da prancha, reduzido. E o mesmo desenho que vai para a grafica."""
    s = (PRANCHAS / nome_prancha).read_text(encoding='utf-8')
    i, j = s.index('<x-dc>') + 6, s.index('</x-dc>')
    corpo = re.sub(r'<helmet>.*?</helmet>', '', s[i:j], flags=re.S).strip()
    k = alvo_px / larg_px
    return (f'<div class="arte" style="width:{alvo_px:.0f}px;height:{alt_px*k:.0f}px">'
            f'<div style="width:{larg_px:.0f}px;height:{alt_px:.0f}px;transform:scale({k:.4f});'
            f'transform-origin:top left">{corpo}</div></div>')


# ------------------------------------------------------------ plantas de apoio
def mini_ring(destaque: str = '') -> str:
    """Planta do Ring 3. destaque: 'entrada' ou 'zona-A'|'zona-B'|'zona-C'."""
    E, ox, oy = 7.0, 26, 30
    rw, rd = R['ring']['largura'], R['ring']['profundidade']
    prof, off, cor_ = R['ring']['prof_raias'], R['ring']['offset_x'], R['ring']['corredor']
    X = lambda m: ox + m * E
    Y = lambda m: oy + m * E
    o = [f'<svg viewBox="0 0 {rw*E+52:.0f} {rd*E+72:.0f}" class="mapa" role="img" '
         f'aria-label="Planta do Ring 3 com o ponto desta peça marcado">']
    o.append(f'<rect x="{X(0):.0f}" y="{oy-16:.0f}" width="{rw*E:.0f}" height="16" fill="#E4E8EA"/>')
    o.append(f'<line x1="{X(0)-12:.0f}" y1="{oy-16:.0f}" x2="{X(rw)+12:.0f}" y2="{oy-16:.0f}" stroke="{MARINHO}" stroke-width="2.4"/>')
    o.append(f'<text x="{X(rw/2):.0f}" y="{oy-22:.0f}" text-anchor="middle" class="rot">HALL 2</text>')
    o.append(f'<rect x="{X(0):.0f}" y="{Y(0):.0f}" width="{rw*E:.0f}" height="{rd*E:.0f}" fill="#FFF" stroke="#9AA3AB" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="{X(rw-cor_):.1f}" y="{Y(0):.0f}" width="{cor_*E:.1f}" height="{rd*E:.0f}" fill="#DCE3E7"/>')
    o.append(f'<rect x="{X(0):.0f}" y="{Y(rd-cor_):.1f}" width="{rw*E:.0f}" height="{cor_*E:.1f}" fill="#DCE3E7"/>')
    for L in ('A', 'B', 'C'):
        z = R['zonas'][L]
        x0, x1 = z['x0'] - off, z['x1'] - off
        aceso = destaque == f'zona-{L}'
        o.append(f'<rect x="{X(x0):.1f}" y="{Y(0):.0f}" width="{(x1-x0)*E:.1f}" height="{prof*E:.0f}" '
                 f'fill="{COR[L]}" fill-opacity="{0.55 if aceso else 0.13}" stroke="{COR[L]}" stroke-width="{2 if aceso else 1}"/>')
        o.append(f'<text x="{X((x0+x1)/2):.0f}" y="{Y(prof/2)+5:.0f}" text-anchor="middle" '
                 f'style="font:800 15px Archivo,sans-serif" fill="{TINTA[L]}">{L}</text>')
        bx = (z['boca_x0'] + z['boca_x1']) / 2 - off
        if aceso:
            o.append(f'<circle cx="{X(bx):.1f}" cy="{Y(prof)+7:.0f}" r="8" fill="{MARINHO}"/>')
            o.append(f'<text x="{X(bx):.1f}" y="{Y(prof)+10:.0f}" text-anchor="middle" style="font:800 8px Nunito Sans,sans-serif" fill="#FFF">P4</text>')
    o.append(f'<polyline points="{X(rw-cor_/2):.0f},{Y(0):.0f} {X(rw-cor_/2):.0f},{Y(rd-cor_/2):.0f} {X(2):.0f},{Y(rd-cor_/2):.0f}" '
             f'fill="none" stroke="{MARINHO}" stroke-width="2" stroke-dasharray="4 3" opacity=".8"/>')
    if destaque == 'entrada':
        o.append(f'<circle cx="{X(rw-cor_/2):.0f}" cy="{Y(1.6):.0f}" r="9" fill="{MARINHO}"/>')
        o.append(f'<text x="{X(rw-cor_/2):.0f}" y="{Y(1.6)+3:.0f}" text-anchor="middle" style="font:800 8px Nunito Sans,sans-serif" fill="#FFF">P3</text>')
    o.append(f'<text x="{X(rw/2):.0f}" y="{Y(rd)+16:.0f}" text-anchor="middle" class="rot">RING 3 · 44 × 35 m · lê C, depois B, depois A</text>')
    o.append('</svg>')
    return '\n'.join(o)


def mini_hall(destaque: str = '') -> str:
    """Planta do Hall 2. destaque: 'porta-A|B|C', 'bloco-A3', 'bloco-C4', 'saidas'."""
    E, ox, oy = 6.2, 20, 22
    X = lambda m: ox + m * E
    Y = lambda m: oy + (LY - m) * E
    o = [f'<svg viewBox="0 0 {LX*E+40:.0f} {LY*E+58:.0f}" class="mapa" role="img" '
         f'aria-label="Planta do Hall 2 com o ponto desta peça marcado">']
    o.append(f'<rect x="{X(0):.0f}" y="{Y(LY):.0f}" width="{LX*E:.0f}" height="{LY*E:.0f}" fill="#FFF" stroke="{MARINHO}" stroke-width="1.6"/>')
    for L in ('A', 'B', 'C'):
        p = portas[L]
        for b in p['blocos']:
            bx, by = b['pos_banner']
            aceso = destaque == f'bloco-{b["id"][-2:]}'
            o.append(f'<circle cx="{X(bx):.1f}" cy="{Y(by):.1f}" r="{7 if aceso else 4}" fill="{COR[L]}" '
                     f'stroke="{MARINHO}" stroke-width="{1.6 if aceso else 0}"/>')
            for c in b['coord']:
                mx, my = (1.4, c) if p['parede'] == 'oeste' else ((c, LY - 1.4) if p['parede'] == 'norte' else (LX - 1.4, c))
                o.append(f'<rect x="{X(mx)-4:.1f}" y="{Y(my)-4:.1f}" width="8" height="8" fill="{COR[L]}" fill-opacity=".45"/>')
    for L, (a, b) in PORTAS_SUL.items():
        aceso = destaque == f'porta-{L}'
        o.append(f'<line x1="{X(a):.1f}" y1="{Y(0):.0f}" x2="{X(b):.1f}" y2="{Y(0):.0f}" stroke="{COR[L]}" stroke-width="{6 if aceso else 3.4}"/>')
        o.append(f'<text x="{X((a+b)/2):.1f}" y="{Y(0)+14:.0f}" text-anchor="middle" style="font:800 9px Nunito Sans,sans-serif" fill="{TINTA[L]}">{PORTA[L]}·{L}</text>')
        if aceso:
            o.append(f'<rect x="{X((a+b)/2)-8:.1f}" y="{Y(3.4):.1f}" width="16" height="16" fill="{COR[L]}" stroke="{MARINHO}" stroke-width="1.4"/>')
            o.append(f'<text x="{X((a+b)/2):.1f}" y="{Y(3.4)+11:.1f}" text-anchor="middle" style="font:800 8px Nunito Sans,sans-serif" fill="{"#FFF" if L=="A" else MARINHO}">P6</text>')
    for nome, x in (('S2', 14.5), ('S8', 41.0)):
        aceso = destaque == 'saidas'
        o.append(f'<line x1="{X(x-1.2):.1f}" y1="{Y(0):.0f}" x2="{X(x+1.2):.1f}" y2="{Y(0):.0f}" stroke="{MARINHO}" stroke-width="{5 if aceso else 2.6}"/>')
        o.append(f'<text x="{X(x):.1f}" y="{Y(0)+14:.0f}" text-anchor="middle" style="font:700 9px Nunito Sans,sans-serif" fill="{MARINHO}">{nome}</text>')
    o.append(f'<text x="{X(LX/2):.0f}" y="{Y(0)+30:.0f}" text-anchor="middle" class="rot">FACHADA SUL · PARA O APRON E O RING 3</text>')
    o.append('</svg>')
    return '\n'.join(o)


def mini_rua(destaque: str = 'P0') -> str:
    """A calçada da Merrion Road, o portão e o caminho até o apron."""
    o = ['<svg viewBox="0 0 430 150" class="mapa" role="img" aria-label="Calçada da Merrion Road, portão de eleitores e caminho até o Hall 2">']
    o.append(f'<rect x="0" y="16" width="430" height="20" fill="#E4E8EA"/>')
    o.append(f'<text x="8" y="12" class="rot">MERRION ROAD · calçada e gradil</text>')
    o.append(f'<line x1="8" y1="40" x2="250" y2="40" stroke="{MARINHO}" stroke-width="2" opacity=".55"/>')
    o.append(f'<line x1="286" y1="40" x2="420" y2="40" stroke="{MARINHO}" stroke-width="2" opacity=".55"/>')
    o.append(f'<line x1="250" y1="31" x2="250" y2="49" stroke="{MARINHO}" stroke-width="2.6"/>')
    o.append(f'<line x1="286" y1="31" x2="286" y2="49" stroke="{MARINHO}" stroke-width="2.6"/>')
    acesoP = destaque == 'P1'
    o.append(f'<circle cx="268" cy="40" r="{10 if acesoP else 6}" fill="{MARINHO if acesoP else "#9AA3AB"}"/>')
    o.append(f'<text x="268" y="43" text-anchor="middle" style="font:800 8px Nunito Sans,sans-serif" fill="#FFF">P1</text>')
    aceso0 = destaque == 'P0'
    o.append(f'<rect x="120" y="{22 if aceso0 else 24}" width="{92 if aceso0 else 80}" height="{26 if aceso0 else 22}" rx="3" '
             f'fill="{"#FFF" if aceso0 else "#F4F6F5"}" stroke="{MARINHO}" stroke-width="{2 if aceso0 else 1}"/>')
    o.append(f'<text x="{166 if aceso0 else 160}" y="{39 if aceso0 else 38}" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="{MARINHO}">P0</text>')
    o.append(f'<rect x="300" y="66" width="118" height="70" fill="#FFF" stroke="{MARINHO}" stroke-width="1.6"/>')
    o.append(f'<text x="359" y="104" text-anchor="middle" style="font:800 12px Archivo,sans-serif" fill="{MARINHO}">HALL 2</text>')
    o.append(f'<polyline points="268,48 268,58 294,58 294,72" fill="none" stroke="{MARINHO}" stroke-width="2" stroke-dasharray="4 3"/>')
    o.append(f'<text x="150" y="104" style="font:600 10px Nunito Sans,sans-serif" fill="#5A6270">quem chega sem saber a seção</text>')
    o.append(f'<text x="150" y="118" style="font:600 10px Nunito Sans,sans-serif" fill="#5A6270">só se resolve no P0, fora do RDS</text>')
    o.append('</svg>')
    return '\n'.join(o)


def mini_parede_leste() -> str:
    """Elevação da lateral leste: 4 saídas de emergência, 3 tabelas mestras."""
    o = ['<svg viewBox="0 0 430 130" class="mapa" role="img" aria-label="Elevação da lateral leste do Hall 2 com as três tabelas mestras entre as saídas de emergência">']
    o.append(f'<rect x="14" y="26" width="402" height="62" fill="#E4E8EA" stroke="#9AA3AB"/>')
    for c in S['parede_leste']['saidas_emergencia']:
        x = 14 + 402 * c / S['parede_leste']['comprimento']
        o.append(f'<rect x="{x-11:.0f}" y="56" width="22" height="32" fill="#C86A5E" fill-opacity=".55" stroke="#A8352A"/>')
    for i, c in enumerate(S['parede_leste']['paineis'], 1):
        x = 14 + 402 * c / S['parede_leste']['comprimento']
        o.append(f'<rect x="{x-14:.0f}" y="46" width="28" height="19" fill="{OFFW}" stroke="{MARINHO}" stroke-width="2"/>')
        o.append(f'<text x="{x:.0f}" y="42" text-anchor="middle" style="font:800 9px Nunito Sans,sans-serif" fill="{MARINHO}">P2·{i}</text>')
        o.append(f'<text x="{x:.0f}" y="102" text-anchor="middle" style="font:600 8.5px Nunito Sans,sans-serif" fill="#5A6270">{c:.2f} m</text>'.replace('.', ','))
    o.append(f'<text x="14" y="20" class="rot">canto norte (portão)</text>')
    o.append(f'<text x="416" y="20" text-anchor="end" class="rot">canto sul (apron · Ring 3)</text>')
    o.append(f'<text x="215" y="120" text-anchor="middle" style="font:600 10px Nunito Sans,sans-serif" fill="#5A6270">44 m de fila parada — por isso a tabela se repete três vezes</text>')
    o.append('</svg>')
    return '\n'.join(o)


def mini_fachada(letra: str = '') -> str:
    """A cortina de vidro da fachada sul, com os vãos das três entradas."""
    o = ['<svg viewBox="0 0 430 110" class="mapa" role="img" aria-label="Fachada sul do Hall 2 com os vãos das três entradas e a porta preferencial">']
    o.append(f'<rect x="10" y="22" width="410" height="58" fill="#DCE6EC" stroke="#9AA3AB"/>')
    for L, (a, b) in PORTAS_SUL.items():
        x0 = 10 + 410 * (a - 12) / 30.0
        x1 = 10 + 410 * (b - 12) / 30.0
        aceso = letra == L
        o.append(f'<rect x="{x0:.0f}" y="30" width="{x1-x0:.0f}" height="50" fill="#FFF" stroke="{COR[L]}" stroke-width="{3 if aceso else 1.4}"/>')
        if aceso:
            o.append(f'<rect x="{(x0+x1)/2-13:.0f}" y="36" width="26" height="26" fill="{COR[L]}"/>')
            o.append(f'<text x="{(x0+x1)/2:.0f}" y="56" text-anchor="middle" style="font:800 18px Archivo,sans-serif" fill="{"#FFF" if L=="A" else MARINHO}">{L}</text>')
        o.append(f'<text x="{(x0+x1)/2:.0f}" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="{TINTA[L]}">{PORTA[L]} · {L}</text>')
    if letra == 'S7':
        o.append(f'<rect x="392" y="40" width="10" height="40" fill="{MARINHO}"/>')
        o.append(f'<text x="397" y="94" text-anchor="middle" style="font:800 10px Nunito Sans,sans-serif" fill="{MARINHO}">S7</text>')
    o.append(f'<text x="10" y="16" class="rot">FACHADA SUL · vista de quem chega do Ring 3</text>')
    o.append('</svg>')
    return '\n'.join(o)


# ------------------------------------------------------------------- as fichas
# (chave da arte, prancha, larg_px, alt_px, ponto, titulo, planta)
FICHAS = [
    ('P0-consulta', 'P0-Consulta.dc.html', 1000, 500, 'P0',
     'Descubra sua seção', mini_rua('P0'),
     'É o único ponto do plano em que “não sei minha seção” tem solução. Fica '
     '<strong>fora do RDS</strong>, na calçada, porque depois do portão nenhuma peça resolve isso: '
     'não há regra numérica (as seções 33xx estão nas três portas) nem atalho por condado '
     '(Cork e Limerick caem em duas portas cada).'),
    ('P0-tabela-mestra', 'P0-Mestra.dc.html', 1000, 500, 'P0',
     'Tabela mestra na calçada', mini_rua('P0'),
     'As 51 seções com a letra da porta. Duas peças: uma ao lado da mesa de consulta, outra no '
     'trecho onde a fila da calçada se forma. Quem sai daqui sai com a letra anotada.'),
    ('P1-portao', 'P1-Portao.dc.html', 1000, 500, 'P1',
     'Portão de eleitores', mini_rua('P1'),
     'Uma folha de cada lado do vão: de um lado a chamada e a seta para o Hall 2, do outro a '
     'tabela mestra outra vez. Do portão em diante, toda peça pressupõe a seção conhecida.'),
    ('P2-parede-leste', 'P2-ParedeLeste.dc.html', 900, 600, 'P2',
     'Lateral leste do Hall 2', mini_parede_leste(),
     'São 44 m de fila parada entre o portão e o apron — o trecho em que o eleitor mais tempo '
     'tem para ler. Três peças nos vãos <strong>entre</strong> as saídas de emergência, nunca sobre elas, '
     'penduradas nas folhas de aço das portas de serviço com ganchos magnéticos.'),
    ('P3-entrada-ring3', 'P3-EntradaRing.dc.html', 1000, 500, 'P3',
     'Entrada do Ring 3', mini_ring('entrada'),
     'O eleitor entra pelo canto nordeste e desce o corredor de 3,0 m. A peça diz a ordem em que '
     'as bocas aparecem — <strong>C, depois B, depois A</strong> — para ele saber quantas deixar passar.'),
    ('P4-boca-zona-C', 'P4-ZonaC.dc.html', 1000, 500, 'P4',
     'Boca da zona C', mini_ring('zona-C'),
     'A primeira boca do percurso. Fica na CCB imediatamente <em>antes</em> da abertura, virada para o '
     'trecho de fundo, para ser lida em movimento a 10–15 m.'),
    ('P4-boca-zona-B', 'P4-ZonaB.dc.html', 1000, 500, 'P4',
     'Boca da zona B', mini_ring('zona-B'),
     'A segunda. Quem não achou a seção na C segue em frente e lê esta.'),
    ('P4-boca-zona-A', 'P4-ZonaA.dc.html', 1000, 500, 'P4',
     'Boca da zona A', mini_ring('zona-A'),
     'A última. Quem passou dela sem encontrar volta pelo mesmo corredor, e é caso para o operador '
     'do trecho de fundo, não para a boca. <strong>A boca da zona A fica 2,91 m a oeste do eixo da porta A</strong> '
     '— a única das três que não descarrega na própria porta.'),
    ('P5-vinil-porta-A', 'P5-VinilA.dc.html', 600, 350, 'P5',
     'Letra da porta A no vidro', mini_fachada('A'),
     'Vinil recortado por dentro da cortina de vidro, letra de 300 mm: é lido a 60 m, lá do Ring 3. '
     'Confirma de longe a letra que o eleitor já traz na mão.'),
    ('P5-vinil-porta-B', 'P5-VinilB.dc.html', 600, 350, 'P5',
     'Letra da porta B no vidro', mini_fachada('B'), ''),
    ('P5-vinil-porta-C', 'P5-VinilC.dc.html', 600, 350, 'P5',
     'Letra da porta C no vidro', mini_fachada('C'), ''),
    ('P5-preferencial', 'P5-Preferencial.dc.html', 1000, 500, 'P5',
     'Entrada preferencial', mini_fachada('S7'),
     'No gradil branco do apron, junto à S7. O vão da S7 tem <strong>1,27 m</strong> — serve um fluxo '
     'preferencial pequeno e não absorve fila grande; medir antes de imprimir.'),
    ('P6-painel-porta-A', 'P6-PainelA.dc.html', 425, 1000, 'P6',
     'Painel da porta A', mini_hall('porta-A'),
     'Logo depois da entrada, do lado oposto à curva do eleitor. Sem número de mesa, o <strong>bloco</strong> é a '
     'menor unidade nomeável: o painel espelha a ordem física dos blocos da parede, que é a ordem '
     'em que o eleitor vai andar.'),
    ('P6-painel-porta-B', 'P6-PainelB.dc.html', 425, 1000, 'P6',
     'Painel da porta B', mini_hall('porta-B'),
     '<strong>A porta B é a única cujo destino não se vê da entrada</strong>: são ~40 m de travessia pelo miolo '
     'até a parede norte. Se sobrar orçamento, o primeiro reforço do plano é um segundo painel da B '
     'no meio do salão.'),
    ('P6-painel-porta-C', 'P6-PainelC.dc.html', 425, 1000, 'P6',
     'Painel da porta C', mini_hall('porta-C'), ''),
    ('P6-bloco-A3', 'P6-BlocoA3.dc.html', 300, 800, 'P6',
     'Banner de bloco — A3', mini_hall('bloco-A3'),
     'Um por grupo de mesas, na boca do corredor, a 4,6 m da parede: 5 na oeste, 5 na norte, 6 na leste. '
     'É a <strong>peça crítica</strong> do plano interno — é ela que fecha a busca. Este é o bloco da MRV 22 '
     '(3313 + 3889), uma das três mesas de maior carga.'),
    ('P6-bloco-C4', 'P6-BlocoC4.dc.html', 300, 800, 'P6',
     'Banner de bloco — C4', mini_hall('bloco-C4'),
     'Um par de quatro seções, para comparar com o bloco isolado acima. Nenhum banner traz número '
     'de mesa: só as seções daquele corredor.'),
    ('P7-saida', 'P7-Saida.dc.html', 297, 210, 'P7',
     'Saídas S2 e S8', mini_hall('saidas'),
     'Sobre cada vão de saída, por dentro. Bilíngue, porque a saída é o único ponto do salão em que '
     'quem não fala português pode precisar da peça sozinho.'),
]

ACHADOS = [
    ('01', 'Não existe regra numérica que leve o eleitor à porta certa',
     'As seções 33xx de Dublin estão espalhadas pelas três portas. Nenhuma peça pode usar faixa de '
     'numeração; toda peça de triagem carrega a lista completa das 51.'),
    ('02', 'Nem o condado serve de atalho',
     'Cork e Limerick caem em duas portas cada. O eleitor do interior só pode ser triado pelo número '
     'da seção — e quem não o sabe precisa do P0, fora do RDS, não de um mesário na porta.'),
    ('03', 'Sem número de mesa, o bloco é a menor unidade nomeável',
     'Ninguém pode ser mandado “à mesa 12”: vai à parede, depois ao bloco, depois à via da sua seção. '
     'Por isso o painel da porta espelha a ordem física dos blocos, e por isso o banner de bloco é a peça crítica.'),
    ('04', 'A porta B é a única cujo destino não se vê da entrada',
     '~40 m de travessia pelo miolo até a parede norte. O primeiro reforço, se sobrar orçamento, é um '
     'segundo painel da B no meio do salão.'),
]

PENDENCIAS = [
    'Confirmar os três hexes contra o rolo de fita — foram lidos da foto do estoque, não medidos.',
    'Trazer o logotipo Eleições 2026 e a marca Justiça Eleitoral em vetor do TSE; o desenho destas '
    'peças é marcação de lugar, e a autorização de uso da marca para posto no exterior ainda não existe.',
    'Confirmar a posição real das portas S4 · S5 · S6 e S7 contra a planta cotada do RDS.',
    'Medir em campo: a profundidade da sala de apoio (7,80 m é suposição), o vão da S7 e o recorte '
    'do canto sudoeste, que tem duas leituras no repositório.',
    'Decidir o cruzamento da zona A: aceitar os 2,91 m de desvio até a porta, com orientador, ou '
    'deslocar o Ring 3 para leste.',
    'Refazer a simulação das vias de fila sobre a Paredes_ABC antes de comprar fita e decalque.',
    'Colar os preços do anexo do Posto na tabela e conferir a faixa de € 1.700–1.900.',
]


# ------------------------------------------------------------------ montagem
# cada ficha aponta explicitamente para a sua peça em sinalizacao_v2.json:
# casar por prefixo de nome falhava em cinco delas, e em silêncio.
PECA_DE = {
    'P0-consulta': 'Ponto “descubra sua seção”',
    'P0-tabela-mestra': 'Tabela mestra na calçada',
    'P1-portao': 'Portão de entrada do RDS',
    'P2-parede-leste': 'Tabela mestra na parede leste do Hall 2',
    'P3-entrada-ring3': 'Entrada do Ring 3',
    'P4-boca-zona-A': 'Boca da zona A',
    'P4-boca-zona-B': 'Boca da zona B',
    'P4-boca-zona-C': 'Boca da zona C',
    'P5-vinil-porta-A': 'Letra da porta no vidro',
    'P5-vinil-porta-B': 'Letra da porta no vidro',
    'P5-vinil-porta-C': 'Letra da porta no vidro',
    'P5-preferencial': 'Entrada preferencial',
    'P6-painel-porta-A': 'Painel da porta A',
    'P6-painel-porta-B': 'Painel da porta B',
    'P6-painel-porta-C': 'Painel da porta C',
    'P6-bloco-A3': 'Banners de bloco — porta A',
    'P6-bloco-C4': 'Banners de bloco — porta C',
    'P7-saida': 'Saídas S2 e S8',
}
_por_nome = {}
for _p in S['pecas']:
    _por_nome.setdefault(_p['nome'], _p)
for _k, _n in PECA_DE.items():
    if _n not in _por_nome:
        raise SystemExit(f'ficha {_k}: não há peça "{_n}" em sinalizacao_v2.json')


def ficha(chave, prancha, w, h, ponto, titulo, planta, texto):
    a = artes[chave]
    m = S['modelos']
    pj = _por_nome[PECA_DE[chave]]
    modelo, corpo, fixacao = pj['modelo'], pj['corpo'], pj['fixacao']
    alvo = 430 if w >= 900 else (300 if w >= 500 else 250)
    # o x-banner de bloco: a arte é de um exemplar, a quantidade é a da parede
    qtd = (f"{pj['qtd']} peças nesta parede · arte de um exemplar"
           if chave.startswith('P6-bloco')
           else f"{a['quantidade']} peça" + ('s' if a['quantidade'] > 1 else ''))
    specs = [('Medida', f"{a['largura_mm']} × {a['altura_mm']} mm"),
             ('Quantidade', qtd),
             ('Modelo', m[modelo]['nome'] if modelo in m else '—'),
             ('Corpo', corpo or '—'),
             ('Fixação', fixacao or '—')]
    linhas = ''.join(f'<div class="sp"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in specs)
    return f"""<section class="ficha">
  <div class="fc-arte">
    {arte(prancha, w, h, alvo)}
    <p class="cap">{a['largura_mm']} × {a['altura_mm']} mm · arquivo <code>{chave}</code></p>
  </div>
  <div class="fc-local">
    <h3><span class="pt">{ponto}</span>{titulo}</h3>
    <div class="ondemapa">{planta}</div>
    <p class="onde"><strong>Onde:</strong> {a['onde']}.</p>
    {f'<p class="texto">{texto}</p>' if texto else ''}
    <dl class="specs">{linhas}</dl>
  </div>
</section>"""


def tabela_mestra_html():
    itens = sorted((str(l['secao']).zfill(4), l['porta']) for l in S['mestra'])
    cols = 4
    por = -(-len(itens) // cols)
    out = []
    for i in range(cols):
        out.append('<div>')
        for sec, p in itens[i*por:(i+1)*por]:
            out.append(f'<div class="mrow"><span class="sec">{sec}</span><span class="dots"></span>'
                       f'<span class="chip c{p}">{p}</span></div>')
        out.append('</div>')
    return ''.join(out)


def orcamento_html():
    m, o = S['modelos'], S['orcamento']
    linhas = ''.join(
        f'<tr><td>{m[k]["nome"]}</td><td class="n">{v["qtd"]}</td>'
        f'<td class="n">€ {m[k]["preco"]:.0f}</td><td class="n">€ {v["total"]:.0f}</td></tr>'
        for k, v in o['por_modelo'].items())
    return f"""<table class="orc"><thead><tr><th>Modelo</th><th class="n">Qtd</th><th class="n">Unit.</th><th class="n">Total</th></tr></thead>
<tbody>{linhas}</tbody>
<tfoot><tr><td>Total</td><td class="n">{sum(v['qtd'] for v in o['por_modelo'].values())}</td><td></td>
<td class="n">€ {o['total']:.0f}</td></tr>
<tr class="faixa"><td colspan="4">Faixa orçada: € {S['faixa_orcamento'][0]:,} – € {S['faixa_orcamento'][1]:,}</td></tr></tfoot></table>""".replace(',', '.')


ext = sum(p['qtd'] for p in S['pecas'] if p['externo'] and p['modelo'] != 'fixacao')
ins = sum(p['qtd'] for p in S['pecas'] if not p['externo'])

DOC = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plano de Sinalização · Posto de Dublin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap">
<style>
  :root {{
    --tinta:{MARINHO}; --ground:#F0F0E8; --surface:#FFFFFF; --rule:#C9CFD4; --rule-soft:#E2E6E4;
    --muted:#5A6270; --a:{COR['A']}; --b:{COR['B']}; --c:{COR['C']};
    --a-ink:{TINTA['A']}; --b-ink:{TINTA['B']}; --c-ink:{TINTA['C']};
    --sans:'Nunito Sans',system-ui,sans-serif; --disp:'Archivo','Nunito Sans',sans-serif;
  }}
  @media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{
    --tinta:#E6EBEA; --ground:#12181A; --surface:#1B2325; --rule:#36423F; --rule-soft:#28322F;
    --muted:#9AA6A3; --a-ink:#8FA9D6; --b-ink:#E8C63A; --c-ink:#EE9468; }} }}
  :root[data-theme="dark"] {{
    --tinta:#E6EBEA; --ground:#12181A; --surface:#1B2325; --rule:#36423F; --rule-soft:#28322F;
    --muted:#9AA6A3; --a-ink:#8FA9D6; --b-ink:#E8C63A; --c-ink:#EE9468; }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; background:var(--ground); color:var(--tinta); font-family:var(--sans); font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:0 16px 96px }}
  header.mast {{ padding:56px 0 26px; border-bottom:3px solid var(--tinta) }}
  .eyebrow {{ font-size:11.5px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); margin:0 0 12px }}
  h1 {{ font-family:var(--disp); font-weight:800; font-size:clamp(32px,5.4vw,52px); line-height:1.02; letter-spacing:-.025em; margin:0 0 14px; text-wrap:balance }}
  .stand {{ font-size:18.5px; color:var(--muted); max-width:62ch; margin:0 }}
  .facts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(124px,1fr)); gap:1px; background:var(--rule); border:1px solid var(--rule); margin:26px 0 0 }}
  .fact {{ background:var(--ground); padding:12px 14px }}
  .fact dt {{ font-size:10.5px; font-weight:800; letter-spacing:.11em; text-transform:uppercase; color:var(--muted); margin:0 0 4px }}
  .fact dd {{ margin:0; font-family:var(--disp); font-size:21px; font-weight:700; letter-spacing:-.02em }}
  section.bloco {{ padding-top:56px }}
  h2 {{ font-family:var(--disp); font-weight:800; font-size:27px; letter-spacing:-.018em; margin:0 0 8px; text-wrap:balance }}
  .lede {{ font-size:18px; color:var(--muted); max-width:64ch; margin:0 0 22px }}
  .ficha {{ display:grid; grid-template-columns:minmax(0,470px) minmax(0,1fr); gap:34px; align-items:start;
            background:var(--surface); border:1px solid var(--rule); padding:24px; margin:0 0 20px }}
  @media (max-width:820px) {{ .ficha {{ grid-template-columns:1fr; gap:22px }} }}
  .arte {{ overflow:hidden; border:1px solid var(--rule-soft); background:#FFF; box-shadow:0 1px 3px rgba(0,0,0,.09) }}
  .cap {{ font-size:12.5px; color:var(--muted); margin:9px 0 0 }}
  .cap code {{ font-family:ui-monospace,Menlo,monospace; font-size:12px }}
  .fc-local h3 {{ font-family:var(--disp); font-weight:700; font-size:20px; margin:0 0 12px; display:flex; align-items:center; gap:11px; flex-wrap:wrap }}
  .pt {{ font-family:ui-monospace,Menlo,monospace; font-size:12.5px; font-weight:700; background:var(--tinta); color:var(--ground); padding:3px 8px; border-radius:2px }}
  .mapa {{ display:block; width:100%; height:auto; background:var(--surface) }}
  .ondemapa {{ border:1px solid var(--rule-soft); padding:10px; margin:0 0 14px; background:#FBFCFB }}
  @media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) .ondemapa {{ background:#F4F6F5 }} }}
  .rot {{ font:700 9.5px 'Nunito Sans',sans-serif; fill:#5A6270; letter-spacing:.09em }}
  .onde, .texto {{ margin:0 0 12px; font-size:15.5px; max-width:64ch }}
  .onde {{ color:var(--tinta) }} .texto {{ color:var(--muted) }}
  .specs {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1px; background:var(--rule-soft); border:1px solid var(--rule-soft); margin:0 }}
  .sp {{ background:var(--surface); padding:9px 11px }}
  .sp dt {{ font-size:10px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); margin:0 0 3px }}
  .sp dd {{ margin:0; font-size:13.5px; font-weight:600; line-height:1.4 }}
  .achados {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(255px,1fr)); gap:14px; margin:20px 0 }}
  .achado {{ background:var(--surface); border:1px solid var(--rule); border-top:4px solid var(--tinta); padding:16px }}
  .achado .n {{ font-family:ui-monospace,Menlo,monospace; font-size:12px; color:var(--muted); font-weight:700 }}
  .achado h4 {{ font-family:var(--disp); font-size:16px; margin:5px 0 7px; line-height:1.25 }}
  .achado p {{ margin:0; font-size:14.5px; color:var(--muted) }}
  .mestra {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:0 26px; margin:18px 0 }}
  @media (max-width:700px) {{ .mestra {{ grid-template-columns:repeat(2,minmax(0,1fr)) }} }}
  .mrow {{ display:flex; align-items:center; gap:8px; padding:4px 0; border-bottom:1px solid var(--rule-soft) }}
  .sec {{ font-family:ui-monospace,Menlo,monospace; font-weight:700; font-size:14px }}
  .dots {{ flex:1; border-bottom:1px dotted var(--rule); height:.7em }}
  .chip {{ min-width:22px; text-align:center; font-weight:800; font-size:12px; line-height:19px; padding:0 6px; border-radius:2px }}
  .chip.cA {{ background:#e3e8f2; color:var(--a-ink); box-shadow:inset 0 0 0 1px var(--a) }}
  .chip.cB {{ background:#faf2d6; color:var(--b-ink); box-shadow:inset 0 0 0 1px var(--b) }}
  .chip.cC {{ background:#fbe7dc; color:var(--c-ink); box-shadow:inset 0 0 0 1px var(--c) }}
  table.orc {{ border-collapse:collapse; width:100%; max-width:640px; font-size:15px; background:var(--surface); border:1px solid var(--rule) }}
  table.orc th {{ text-align:left; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); padding:10px 13px; border-bottom:1px solid var(--rule) }}
  table.orc td {{ padding:9px 13px; border-bottom:1px solid var(--rule-soft) }}
  table.orc .n {{ text-align:right; font-variant-numeric:tabular-nums }}
  table.orc tfoot td {{ font-weight:800; border-top:2px solid var(--rule); border-bottom:0 }}
  table.orc tfoot .faixa td {{ font-weight:400; color:var(--muted); font-size:13.5px }}
  ol.pend {{ margin:18px 0; padding-left:22px; max-width:70ch }}
  ol.pend li {{ margin:0 0 10px; font-size:15.5px }}
  footer {{ margin-top:64px; padding-top:20px; border-top:1px solid var(--rule); font-size:13.5px; color:var(--muted) }}
  a {{ color:var(--a-ink) }} a:hover {{ color:var(--tinta) }}
  :focus-visible {{ outline:2px solid var(--a-ink); outline-offset:3px }}
</style>
</head>
<body>
<div class="wrap">

<header class="mast">
  <p class="eyebrow">Eleições 2026 · 1º turno · 4 de outubro · RDS Hall 2, Dublin</p>
  <h1>Plano de sinalização, peça por peça</h1>
  <p class="stand">Cada arte ao lado do ponto em que ela é instalada. Consolida a proposta de arte,
  a Rota do Eleitor e o plano interno do Hall 2 num documento só — o que se imprime, onde se prende
  e o que resolve.</p>
  <dl class="facts">
    <div class="fact"><dt>Aptos</dt><dd>16.794</dd></div>
    <div class="fact"><dt>Seções</dt><dd>51</dd></div>
    <div class="fact"><dt>Esperados</dt><dd>11.499</dd></div>
    <div class="fact"><dt>Peças externas</dt><dd>{ext}</dd></div>
    <div class="fact"><dt>Peças internas</dt><dd>{ins}</dd></div>
    <div class="fact"><dt>Orçamento</dt><dd>€ {S['orcamento']['total']:.0f}</dd></div>
  </dl>
</header>

<section class="bloco">
  <h2>A consulta é uma só, e se repete sete vezes</h2>
  <p class="lede">O eleitor precisa saber uma coisa: <strong>a sua seção</strong>. Daí sai a letra da porta,
  e a letra o leva até a mesa. As mesas não têm número em peça nenhuma — desde a revisão de 16/09, a
  menor unidade nomeável dentro do salão é o <strong>bloco</strong> de mesas.</p>
  <div class="achados">
    {''.join(f'<div class="achado"><div class="n">{n}</div><h4>{t}</h4><p>{d}</p></div>' for n, t, d in ACHADOS)}
  </div>
</section>

<section class="bloco">
  <h2>As peças, na ordem em que o eleitor as encontra</h2>
  <p class="lede">A arte à esquerda é o desenho que vai para a gráfica, reduzido. À direita, o recorte da
  planta com o ponto marcado. Os arquivos em tamanho real — HTML, PDF e PNG — estão em
  <code>saidas/artes_sinalizacao/</code> no repositório.</p>
  {''.join(ficha(*f) for f in FICHAS)}
</section>

<section class="bloco">
  <h2>Seção → porta</h2>
  <p class="lede">As 51 seções em ordem crescente. É o conteúdo literal de P0, P1, P2 e P3 — quatro pontos,
  sete cópias — e a mesma lista que reaparece recortada nas bocas do Ring 3 e nos painéis de porta.</p>
  <div class="mestra">{tabela_mestra_html()}</div>
</section>

<section class="bloco">
  <h2>Onde os € 1.700–1.900 vão</h2>
  <p class="lede">{ext} peças externas e {ins} internas. Preços de tabela de gráficas irlandesas,
  inc. IVA — o anexo de preços do Posto ainda não chegou a estas contas.</p>
  {orcamento_html()}
</section>

<section class="bloco">
  <h2>O que falta antes de imprimir</h2>
  <ol class="pend">{''.join(f'<li>{p}</li>' for p in PENDENCIAS)}</ol>
</section>

<footer>
  Gerado por <code>scripts/pranchas/gera_plano_consolidado.py</code> a partir de
  <code>saidas/sinalizacao_v2.json</code>, <code>saidas/ring3_montagem.json</code>,
  <code>data/prancheta_hall2.json</code> e das pranchas de
  <code>saidas/pranchas_sinalizacao/</code>. As 51 seções aparecem exatamente uma vez, os aptos somam
  16.794 e as 28 mesas fecham — o script falha em vez de gravar um plano que não bata com a base do TSE.
</footer>

</div>
</body>
</html>
"""

# validacao: o plano nao vale se a base nao bater
secoes = [str(l['secao']).zfill(4) for l in S['mestra']]
assert len(secoes) == len(set(secoes)) == 51, 'as 51 seções não aparecem exatamente uma vez'
assert sum(m['aptos'] for m in json.loads((REPO / 'data' / 'decisoes.json').read_text(encoding='utf-8'))['mesas']) == 16794
SAIDA.write_text(DOC, encoding='utf-8')
print(f'gravado {SAIDA.relative_to(REPO)} · {len(FICHAS)} fichas · {len(DOC)//1024} KB')
