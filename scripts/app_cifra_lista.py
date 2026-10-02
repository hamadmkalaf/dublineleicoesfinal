"""Cifra e decifra o CSV canônico da lista para guardá-lo no repositório.

    python3 scripts/app_cifra_lista.py cifrar  data/eleitores/eleitores.csv  --senha "..."   # -> eleitores.csv.enc (título completo, 02/10)
    python3 scripts/app_cifra_lista.py decifrar data/eleitores/eleitores.csv.enc --senha "..."  # -> eleitores.csv
    (eleitores_v2.csv.enc é o formato anterior, só com os dígitos 5-8 do título)

AES-256-GCM com chave de PBKDF2-SHA256 (600.000 iterações) sobre a senha — o mesmo esquema do
pacote da equipe (app_construir.cifra_equipe). A senha vem de --senha ou de APP_SENHA_EQUIPE.
O .enc pode entrar no git (`.gitignore` abre exceção para data/eleitores/*.enc): ninguém lê
nomes nele sem a senha. O CSV em claro continua fora do git.
`app_construir.py --lista arquivo.enc --senha-equipe "..."` lê o .enc diretamente.
"""

import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import zlib
from pathlib import Path

ITERACOES = 600_000


def cifra_bytes(claro, senha):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    sal, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    chave = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES, 32)
    cifrado = AESGCM(chave).encrypt(iv, zlib.compress(claro, 9), None)
    b64 = lambda b: base64.b64encode(b).decode("ascii")
    return {"v": 1, "kdf": "PBKDF2-SHA256", "iteracoes": ITERACOES, "sal": b64(sal), "iv": b64(iv),
            "cifra": "AES-256-GCM", "compressao": "deflate", "bytes_claros": len(claro), "dados": b64(cifrado)}


def decifra_bytes(pacote, senha):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    chave = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), base64.b64decode(pacote["sal"]), pacote["iteracoes"], 32)
    return zlib.decompress(AESGCM(chave).decrypt(base64.b64decode(pacote["iv"]), base64.b64decode(pacote["dados"]), None))


def le_csv_cifrado(caminho, senha):
    """Texto do CSV a partir do .enc. Lança ValueError com senha errada."""
    if not senha:
        raise SystemExit(f"{caminho} é cifrado: passe a senha (--senha-equipe ou APP_SENHA_EQUIPE)")
    try:
        return decifra_bytes(json.loads(Path(caminho).read_text(encoding="utf-8")), senha).decode("utf-8")
    except Exception as e:  # InvalidTag, JSON ruim…
        raise SystemExit(f"não consegui decifrar {caminho}: senha errada ou arquivo corrompido ({type(e).__name__})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=("cifrar", "decifrar"))
    ap.add_argument("arquivo", type=Path)
    ap.add_argument("--senha", default=os.environ.get("APP_SENHA_EQUIPE"))
    ap.add_argument("--destino", type=Path)
    args = ap.parse_args()
    if not args.senha:
        raise SystemExit("passe --senha ou defina APP_SENHA_EQUIPE")
    if args.acao == "cifrar":
        destino = args.destino or args.arquivo.with_suffix(args.arquivo.suffix + ".enc")
        claro = args.arquivo.read_bytes()
        destino.write_text(json.dumps(cifra_bytes(claro, args.senha), separators=(",", ":")), encoding="utf-8")
        print(f"cifrado: {destino} ({len(claro) / 1024:.0f} kB em claro → {destino.stat().st_size / 1024:.0f} kB). Pode entrar no git.")
    else:
        destino = args.destino or (args.arquivo.with_suffix("") if args.arquivo.suffix == ".enc" else args.arquivo.with_name(args.arquivo.name + ".csv"))
        destino.write_text(le_csv_cifrado(args.arquivo, args.senha), encoding="utf-8")
        print(f"decifrado: {destino}. Este arquivo tem dados pessoais e não entra no git.")


if __name__ == "__main__":
    main()
