#!/usr/bin/env python3
"""O QR da peça P0-Consulta: estático, direto para a consulta de seção do TSE.

Decisão do Posto de 22/09: o QR aponta para o site do TSE, não para o e-Título.
O SVG recebido nesse dia (`Identidadevisual/consultasecaoeleitoral.svg`) não é
usado na peça: decodificado, ele leva a `https://link.getqr.com/XwlEKkK`, um
encurtador dinâmico de terceiro, cujo destino pode mudar sem que o Posto saiba
e cujo serviço pode expirar antes do dia da eleição. Um QR estático para a URL
do TSE não depende de ninguém.

Nível de correção H (30%): o fence banner fica ao ar livre, num gradil, e a
peça é lida de perto por quem já não sabe a seção — sujeira, dobra e sombra
não podem tirar o código de serviço.

    python3 scripts/qr_tse.py            confere data/qr_tse.svg e sai com 1 se divergir
    python3 scripts/qr_tse.py --grava    regrava data/qr_tse.svg

A URL é a constante `URL`: se o Posto preferir outra página do TSE, muda ali
e regrava.
"""
import io
import pathlib
import sys

import segno

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ALVO = RAIZ / "data" / "qr_tse.svg"
URL = "https://www.tse.jus.br/servicos-eleitorais/titulo-e-local-de-votacao/consulta-por-nome"
NIVEL = "H"


def svg():
    qr = segno.make(URL, error=NIVEL, micro=False)
    buf = io.BytesIO()
    # um <path> só, sem tamanho fixo: a peça dimensiona pelo viewBox; a zona de
    # silêncio de 4 módulos entra no viewBox (border=4)
    qr.save(buf, kind="svg", xmldecl=False, svgclass=None, lineclass=None,
            omitsize=True, dark="#000000", light=None, border=4, scale=1)
    texto = buf.getvalue().decode("utf-8").strip() + "\n"
    return texto, qr


def main():
    grava = "--grava" in sys.argv[1:]
    texto, qr = svg()
    atual = ALVO.read_text(encoding="utf-8") if ALVO.exists() else None
    print(f"QR versão {qr.version}, nível {qr.error}, {qr.symbol_size(border=4)[0]} módulos com a zona de silêncio · {URL}")
    if atual == texto:
        print("data/qr_tse.svg em dia")
        return 0
    if grava:
        ALVO.write_text(texto, encoding="utf-8")
        print("regravado data/qr_tse.svg")
        return 0
    print("data/qr_tse.svg diverge; rode com --grava", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
