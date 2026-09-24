"""Os cinco pictogramas do atendimento preferencial brasileiro, em vetor.

Redesenhados a partir da placa de referência entregue pelo Posto em 21/09:
**idoso com bengala · gestante · adulto com criança de colo · pessoa com
muleta · laço de peças do espectro autista**, nessa ordem. A versão anterior
trazia uma pessoa em cadeira de rodas no lugar da muleta; foi corrigida.

São vetor e não a imagem de referência por dois motivos. A referência é um
**JPEG de 950 px com marca d'água de banco de imagens** — não um vetor, apesar
do rótulo "EPS/CDR" que ela anuncia —, e ampliada para os 2080 mm do fence
banner sairia borrada; e a arte de um banco de imagens não pode ser
reproduzida sem a licença. Os cinco símbolos em si são de uso corrente e não
têm dono; o que se redesenha aqui são eles, na tipologia e na tinta do plano,
não o layout da placa vendida.

`picto_linha(altura, vao, tinta, sufixo)` devolve o bloco HTML da fileira. O
`sufixo` entra no id do pattern do laço, para que duas fileiras na mesma página
— o artefato consolidado põe todas as peças juntas — não colidam.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from paleta import MARINHO  # noqa: E402

TINTA = MARINHO
LACO = ("M33 96 C38 83 45 71 50 60 C55 49 68 48 68 36 C68 25 60 18 50 18 "
        "C40 18 32 25 32 36 C32 48 45 49 50 60 C55 71 62 83 67 96")
# As quatro cores do próprio símbolo do espectro autista. Não são a paleta do
# plano e por isso ficam de fora da conferência de `scripts/paleta.py`.
PECAS_LACO = ("#3B7DC4", "#E03C3C", "#F2C230", "#6FB9E8")


def _svg(lado, corpo):
    return (f'<svg width="{lado}" height="{lado}" viewBox="0 0 100 100" '
            f'aria-hidden="true" style="display:block; flex-shrink:0">{corpo}</svg>')


def _idoso(lado, tinta):
    """Idoso apoiado em bengala."""
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M60 52 C55 46 48 47 46 52" stroke-width="6"/>'
        '<path d="M60 52 L66 92" stroke-width="6"/>'
        f'<circle cx="38" cy="12" r="9" fill="{tinta}" stroke="none"/>'
        '<path d="M38 21 C40 34 42 44 44 52" stroke-width="15"/>'
        '<path d="M44 52 L34 72 L30 92" stroke-width="12"/>'
        '<path d="M44 52 L50 72 L52 92" stroke-width="12"/>'
        '<path d="M40 32 L58 52" stroke-width="9"/></g>'))


def _gestante(lado, tinta):
    return _svg(lado, (
        f'<g fill="{tinta}" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="40" cy="12" r="9" stroke="none"/>'
        '<path d="M40 21 L38 48" stroke-width="14" fill="none"/>'
        '<ellipse cx="53" cy="41" rx="13" ry="14" stroke="none"/>'
        '<polygon points="30,46 50,46 59,76 23,76" stroke="none"/>'
        '<path d="M33 76 L31 92" stroke-width="10" fill="none"/>'
        '<path d="M48 76 L50 92" stroke-width="10" fill="none"/></g>'))


def _colo(lado, tinta):
    """Adulto com criança de colo, o bebê atravessado nos braços."""
    return _svg(lado, (
        f'<g fill="{tinta}" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="36" cy="12" r="9" stroke="none"/>'
        '<path d="M36 21 L36 46" stroke-width="15" fill="none"/>'
        '<path d="M29 33 C32 47 46 51 60 45" stroke-width="9" fill="none"/>'
        '<ellipse cx="52" cy="36" rx="13" ry="7" transform="rotate(-10 52 36)" stroke="none"/>'
        '<circle cx="65" cy="31" r="6.5" stroke="none"/>'
        '<polygon points="27,46 46,46 55,76 19,76" stroke="none"/>'
        '<path d="M29 76 L27 92" stroke-width="10" fill="none"/>'
        '<path d="M45 76 L47 92" stroke-width="10" fill="none"/></g>'))


def _muleta(lado, tinta):
    """Pessoa apoiada em muleta axilar."""
    return _svg(lado, (
        f'<g fill="none" stroke="{tinta}" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M52 30 L64 30" stroke-width="4.5"/>'
        '<path d="M55 32 L59 58" stroke-width="3.5"/>'
        '<path d="M62 32 L60 58" stroke-width="3.5"/>'
        '<path d="M54 47 L63 45" stroke-width="3.5"/>'
        '<path d="M59.5 58 L61 92" stroke-width="5"/>'
        f'<circle cx="34" cy="12" r="9" fill="{tinta}" stroke="none"/>'
        '<path d="M34 21 C35 32 37 42 40 50" stroke-width="14"/>'
        '<path d="M40 50 L31 70 L27 92" stroke-width="11"/>'
        '<path d="M40 50 L46 70 L46 92" stroke-width="11"/>'
        '<path d="M37 30 L53 42" stroke-width="8"/></g>'))


def _laco(lado, tinta, sufixo):
    pid = f"pz-{sufixo}"
    a, b, c, d = PECAS_LACO
    return _svg(lado, (
        f'<defs><pattern id="{pid}" width="11" height="11" patternUnits="userSpaceOnUse">'
        f'<rect width="11" height="11" fill="{a}"/>'
        f'<rect width="5.5" height="5.5" fill="{b}"/>'
        f'<rect x="5.5" y="5.5" width="5.5" height="5.5" fill="{c}"/>'
        f'<rect x="5.5" width="5.5" height="5.5" fill="{d}"/>'
        '<path d="M5.5 0V11M0 5.5H11" stroke="#FFFFFF" stroke-width="1.2"/>'
        '</pattern></defs><g fill="none" stroke-linecap="round">'
        f'<path d="{LACO}" stroke="{tinta}" stroke-width="13"/>'
        f'<path d="{LACO}" stroke="url(#{pid})" stroke-width="9.6"/></g>'))


def picto_linha(altura=165, vao=20, tinta=TINTA, sufixo="pref"):
    figuras = [
        _idoso(altura, tinta),
        _gestante(altura, tinta),
        _colo(altura, tinta),
        _muleta(altura, tinta),
        _laco(altura, tinta, sufixo),
    ]
    return (f'<div style="display: flex; align-items: flex-end; justify-content: center;'
            f' gap: {vao}px;">' + "".join(figuras) + "</div>")
