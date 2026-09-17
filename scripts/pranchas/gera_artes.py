# -*- coding: utf-8 -*-
"""Converte cada prancha .dc.html na ARTE em tamanho real: HTML + PDF + PNG.

As pranchas do canvas estao a 1 px = 2 mm, boas para ver na tela e comparar
entre si.  A grafica precisa de outra coisa: a peca na medida fisica.  Este
script pega o corpo de cada prancha e o embrulha num HTML autonomo cujo @page
tem o tamanho real da peca, com um transform que leva o px da prancha ao
milimetro do impresso.  Imprimir esse HTML (ou o PDF que sai dele) da a peca
no tamanho certo.

    python3 scripts/pranchas/gera_artes.py            # so os HTML
    python3 scripts/pranchas/gera_artes.py --render   # HTML + PDF + PNG

Saida: saidas/artes_sinalizacao/
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
PRANCHAS = REPO / 'saidas' / 'pranchas_sinalizacao' / 'project'
OUT = REPO / 'saidas' / 'artes_sinalizacao'

PX_MM = 25.4 / 96.0        # 1 px CSS = 0,2646 mm
ESCALA_PRANCHA = 2.0       # a prancha desenha 1 px para cada 2 mm da peca

# peca -> (arquivo da prancha, largura_mm, altura_mm, quantidade, onde vai)
PECAS = [
    ('P0-consulta',      'P0-Consulta.dc.html',   2000, 1000, 1,
     'Calçada da Merrion Road, no gradil do RDS, 20–30 m antes do portão'),
    ('P0-tabela-mestra', 'P0-Mestra.dc.html',     2000, 1000, 2,
     'Gradil da Merrion Road, ao lado do ponto de consulta'),
    ('P1-portao',        'P1-Portao.dc.html',     2000, 1000, 1,
     'Nas grades do portão de eleitores, uma folha de cada lado do vão'),
    ('P2-parede-leste',  'P2-ParedeLeste.dc.html', 1800, 1200, 3,
     'Vãos entre as 4 saídas de emergência da lateral leste, a 10,75 · 22,50 · 33,90 m do canto norte'),
    ('P3-entrada-ring3', 'P3-EntradaRing.dc.html', 2000, 1000, 1,
     'CCB do corredor de chegada do Ring 3, logo depois do canto nordeste'),
    ('P4-boca-zona-A',   'P4-ZonaA.dc.html',      2000, 1000, 1,
     'CCB de fechamento imediatamente antes da boca da zona A, virada para o trecho de fundo'),
    ('P4-boca-zona-B',   'P4-ZonaB.dc.html',      2000, 1000, 1,
     'CCB de fechamento imediatamente antes da boca da zona B'),
    ('P4-boca-zona-C',   'P4-ZonaC.dc.html',      2000, 1000, 1,
     'CCB de fechamento imediatamente antes da boca da zona C'),
    ('P5-vinil-porta-A', 'P5-VinilA.dc.html',     1200,  700, 1,
     'Por dentro do vidro da fachada sul, sobre o vão da S4'),
    ('P5-vinil-porta-B', 'P5-VinilB.dc.html',     1200,  700, 1,
     'Por dentro do vidro da fachada sul, sobre o vão da S5'),
    ('P5-vinil-porta-C', 'P5-VinilC.dc.html',     1200,  700, 1,
     'Por dentro do vidro da fachada sul, sobre o vão da S6'),
    ('P5-preferencial',  'P5-Preferencial.dc.html', 2000, 1000, 1,
     'Gradil branco de pedestres do apron, junto à porta S7'),
    ('P6-painel-porta-A', 'P6-PainelA.dc.html',    850, 2000, 1,
     'Logo depois da porta S4, dentro do salão, do lado oposto à curva do eleitor'),
    ('P6-painel-porta-B', 'P6-PainelB.dc.html',    850, 2000, 1,
     'Logo depois da porta S5 — a porta cujo destino não se vê da entrada'),
    ('P6-painel-porta-C', 'P6-PainelC.dc.html',    850, 2000, 1,
     'Logo depois da porta S6, dentro do salão'),
    ('P6-bloco-A3',      'P6-BlocoA3.dc.html',     600, 1600, 1,
     'Boca do corredor do bloco A3 (MRV 22), a 4,6 m da parede oeste'),
    ('P6-bloco-C4',      'P6-BlocoC4.dc.html',     600, 1600, 1,
     'Boca do corredor do bloco C4, a 4,6 m da parede leste'),
    ('P7-saida',         'P7-Saida.dc.html',       594,  420, 2,
     'Dentro do salão, sobre cada vão de saída (S2 e S8)'),
]

MOLDE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{titulo}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap');
  @page {{ size: {w_mm}mm {h_mm}mm; margin: 0; }}
  html, body {{ margin: 0; padding: 0; background: #FFFFFF; }}
  /* A peca fisica: {w_mm} x {h_mm} mm.  A arte foi desenhada a {esc} mm por px. */
  .peca {{ width: {w_mm}mm; height: {h_mm}mm; overflow: hidden; position: relative; }}
  .arte {{ position: absolute; top: 0; left: 0;
           width: {w_px}px; height: {h_px}px;
           transform: scale({fator}); transform-origin: top left; }}
  @media screen {{ body {{ background: #DDE1E5; padding: 0; }}
                   .peca {{ margin: 0 auto; box-shadow: 0 0 0 1px #9AA3AB; background: #FFF; }} }}
</style>
</head>
<body>
<div class="peca"><div class="arte">
{corpo}
</div></div>
</body>
</html>
"""


def corpo_da_prancha(caminho: pathlib.Path) -> str:
    """Tira o conteudo desenhavel de uma prancha .dc.html: o que esta entre
    <x-dc> e </x-dc>, menos o <helmet> (que so carrega regras de pagina)."""
    s = caminho.read_text(encoding='utf-8')
    i, j = s.index('<x-dc>') + len('<x-dc>'), s.index('</x-dc>')
    corpo = s[i:j]
    corpo = re.sub(r'<helmet>.*?</helmet>', '', corpo, flags=re.S)
    return corpo.strip()


def main(render: bool) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    indice = []
    for slug, arquivo, w_mm, h_mm, qtd, onde in PECAS:
        origem = PRANCHAS / arquivo
        if not origem.exists():
            raise SystemExit(f'falta {origem} — rode antes scripts/pranchas/gera_pranchas.py')
        w_px, h_px = w_mm / ESCALA_PRANCHA, h_mm / ESCALA_PRANCHA
        # de px da prancha para mm da peca: 1 px -> 2 mm -> 2/0,2646 px de impressao
        fator = ESCALA_PRANCHA / PX_MM
        html = MOLDE.format(titulo=slug, w_mm=w_mm, h_mm=h_mm, w_px=w_px, h_px=h_px,
                            fator=round(fator, 6), esc=ESCALA_PRANCHA,
                            corpo=corpo_da_prancha(origem))
        (OUT / f'{slug}.html').write_text(html, encoding='utf-8')
        indice.append({'arquivo': slug, 'largura_mm': w_mm, 'altura_mm': h_mm,
                       'quantidade': qtd, 'onde': onde, 'prancha': arquivo})
        print(f'  {slug:20s} {w_mm:5d} × {h_mm:4d} mm   ×{qtd}')

    (OUT / 'indice.json').write_text(
        json.dumps({'gerado_por': 'scripts/pranchas/gera_artes.py',
                    'escala': '1 px da prancha = 2 mm da peça',
                    'pecas': indice}, ensure_ascii=False, indent=1) + '\n',
        encoding='utf-8')
    print(f'\n{len(indice)} artes em {OUT.relative_to(REPO)}/')

    if render:
        renderiza(indice)


def renderiza(indice) -> None:
    import os
    from playwright.sync_api import sync_playwright
    # o Chromium do ambiente pode nao ser o que a versao do playwright espera;
    # CHROMIUM permite apontar o binario existente.
    exe = os.environ.get('CHROMIUM')
    cortes = []
    print('\nrenderizando PDF e PNG...')
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pag = nav.new_page()
        for p in indice:
            caminho = (OUT / f"{p['arquivo']}.html").as_uri()
            pag.goto(caminho, wait_until='networkidle')
            # A peca corta o que passa da borda (overflow:hidden).  Sem esta
            # conferencia, uma arte cortada pela metade vai para a grafica em
            # silencio -- foi o que aconteceu com o P2 antes de 4 colunas.
            corte = pag.evaluate('''() => {
                const r = document.querySelector('.arte > div');
                if (!r) return null;
                return {h: r.scrollHeight, ch: r.clientHeight,
                        w: r.scrollWidth,  cw: r.clientWidth};
            }''')
            if corte and (corte['h'] > corte['ch'] + 1 or corte['w'] > corte['cw'] + 1):
                cortes.append(f"{p['arquivo']}: conteudo {corte['w']}x{corte['h']} px "
                              f"na peca de {corte['cw']}x{corte['ch']} px")
            pag.pdf(path=str(OUT / f"{p['arquivo']}.pdf"),
                    width=f"{p['largura_mm']}mm", height=f"{p['altura_mm']}mm",
                    print_background=True, margin={'top': '0', 'bottom': '0',
                                                   'left': '0', 'right': '0'})
            # PNG de conferencia: 4 px por mm, o bastante para ler na tela
            alvo = pag.locator('.peca')
            pag.set_viewport_size({'width': max(400, round(p['largura_mm'] * 0.42)),
                                   'height': max(400, round(p['altura_mm'] * 0.42))})
            alvo.screenshot(path=str(OUT / f"{p['arquivo']}.png"), scale='css')
            print(f"  {p['arquivo']}: pdf + png")
        nav.close()
    if cortes:
        print('\nARTE CORTADA -- nao mande para a grafica assim:')
        for c in cortes:
            print('  ' + c)
        raise SystemExit(1)
    print('\nnenhuma arte cortada')


if __name__ == '__main__':
    main('--render' in sys.argv)
