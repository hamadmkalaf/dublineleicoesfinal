"""Os cinco pictogramas do atendimento preferencial brasileiro, em vetor.

Redesenhados a partir da placa padrão "ATENDIMENTO PREFERENCIAL" (idoso,
adulto com criança de colo, gestante, pessoa em cadeira de rodas e o laço de
peças do espectro autista). São vetor, e não a imagem de referência, porque a
imagem tem ~570 px de largura: ampliada para os 2080 mm do fence banner daria
cerca de 7 px/cm, e a placa sairia borrada da gráfica.

`picto_linha(altura, vao, tinta, sufixo)` devolve o bloco HTML da fileira. O
`sufixo` entra no id do pattern do laço, para que duas fileiras na mesma página
— o artefato consolidado põe todas as peças juntas — não colidam.
"""

TINTA = "#3F3F3F"
LACO = "M33 96 C38 83 45 71 50 60 C55 49 68 48 68 36 C68 25 60 18 50 18 C40 18 32 25 32 36 C32 48 45 49 50 60 C55 71 62 83 67 96"


def _svg(lado, corpo):
    return (f'<svg width="{lado}" height="{lado}" viewBox="0 0 100 100" '
            f'aria-hidden="true" style="display:block; flex-shrink:0">{corpo}</svg>')


def _idoso(lado, tinta):
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M64 55 L70 93" stroke-width="6"/>'
        '<path d="M64 55 C58 47 49 48 47 54" stroke-width="6"/>'
        f'<circle cx="28" cy="13" r="9" fill="{tinta}" stroke="none"/>'
        '<path d="M29 20 C32 33 38 42 47 48" stroke-width="15"/>'
        '<path d="M47 48 L30 68 L24 92" stroke-width="12"/>'
        '<path d="M47 48 L53 70 L54 92" stroke-width="12"/>'
        '<path d="M35 32 L62 54" stroke-width="10"/></g>'))


def _colo(lado, tinta):
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="28" cy="13" r="9" fill="{tinta}" stroke="none"/>'
        '<path d="M28 20 L28 58" stroke-width="16"/>'
        '<path d="M25 58 L20 92" stroke-width="12"/>'
        '<path d="M32 58 L41 91" stroke-width="12"/>'
        '<path d="M29 32 L24 47 L54 44" stroke-width="9"/>'
        f'<circle cx="59" cy="28" r="8.5" fill="{tinta}" stroke="none"/>'
        '<path d="M58 35 L61 43" stroke-width="13"/></g>'))


def _gestante(lado, tinta):
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="31" cy="13" r="9" fill="{tinta}" stroke="none"/>'
        '<path d="M31 20 L30 60" stroke-width="15"/>'
        f'<ellipse cx="43" cy="43" rx="14" ry="15" fill="{tinta}" stroke="none"/>'
        '<path d="M27 60 L21 92" stroke-width="12"/>'
        '<path d="M34 60 L45 91" stroke-width="12"/></g>'))


def _cadeirante(lado, tinta):
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="52" cy="76" r="18" stroke-width="5.5"/>'
        f'<circle cx="30" cy="11" r="8.5" fill="{tinta}" stroke="none"/>'
        '<path d="M30 18 L31 50 L57 52" stroke-width="11"/>'
        '<path d="M34 25 L52 34" stroke-width="7.5"/>'
        '<path d="M60 54 L67 74" stroke-width="8.5"/>'
        '<path d="M67 74 L79 78" stroke-width="7"/></g>'))


def _laco(lado, tinta, sufixo):
    pid = f"pz-{sufixo}"
    return _svg(lado, (
        f'<defs><pattern id="{pid}" width="11" height="11" patternUnits="userSpaceOnUse">'
        '<rect width="11" height="11" fill="#3B7DC4"/>'
        '<rect width="5.5" height="5.5" fill="#E03C3C"/>'
        '<rect x="5.5" y="5.5" width="5.5" height="5.5" fill="#F2C230"/>'
        '<rect x="5.5" width="5.5" height="5.5" fill="#6FB9E8"/>'
        '<path d="M5.5 0V11M0 5.5H11" stroke="#FFFFFF" stroke-width="1.2"/>'
        '</pattern></defs><g fill="none" stroke-linecap="round">'
        f'<path d="{LACO}" stroke="{tinta}" stroke-width="13"/>'
        f'<path d="{LACO}" stroke="url(#{pid})" stroke-width="9.6"/></g>'))


def picto_linha(altura=165, vao=20, tinta=TINTA, sufixo="pref"):
    figuras = [
        _idoso(altura, tinta),
        _colo(altura, tinta),
        _gestante(altura, tinta),
        _cadeirante(altura, tinta),
        _laco(altura, tinta, sufixo),
    ]
    return (f'<div style="display: flex; align-items: flex-end; justify-content: center;'
            f' gap: {vao}px;">' + "".join(figuras) + "</div>")
