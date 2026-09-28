"""Constrói o app "Onde eu voto?" a partir da lista nominal e das decisões do Hall 2.

    python3 scripts/app_construir.py                       # só confere, não escreve nada (código 1 se quebrar)
    python3 scripts/app_construir.py --grava               # escreve app/dist/ com a amostra sintética
    python3 scripts/app_construir.py --grava --lista data/eleitores/eleitores.csv --senha-equipe "seis palavras ..."

Lê (nunca escreve): data/decisoes.json, data/grupos_mesas.json, mapa/sinalizacao/P0-Mestra.dc.html.
Escreve em app/dist/:
  - tudo de app/public/ (o site, sem build de frontend);
  - dados/rotas.json          seção -> mesa, letra, porta, parede, grupo, passos do caminho (público, sem dado pessoal);
  - dados/indice_publico.json hash PBKDF2(chave do nome | 2º fator) -> seção(ões);
  - dados/equipe.enc          lista completa (nome, nascimento, título, seção) cifrada com AES-256-GCM;
  - dados/versao.json         carimbo da construção, para o service worker perceber a atualização.

A senha da equipe vem de --senha-equipe ou da variável APP_SENHA_EQUIPE. Sem nenhuma das
duas, o script sorteia uma frase de seis palavras e a imprime UMA vez: anote-a.
"""

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import zlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app_normaliza import (  # noqa: E402
    ITERACOES_PUBLICO, SAL_PUBLICO, TAMANHO_HASH, chaves_nome, hash_publico,
    normaliza_data, normaliza_inscricao, normaliza_nome, normaliza_secao,
)

RAIZ = Path(__file__).resolve().parent.parent
DECISOES = RAIZ / "data" / "decisoes.json"
GRUPOS = RAIZ / "data" / "grupos_mesas.json"
MESTRA = RAIZ / "mapa" / "sinalizacao" / "P0-Mestra.dc.html"
PUBLICO = RAIZ / "app" / "public"
DIST = RAIZ / "app" / "dist"
AMOSTRA = RAIZ / "app" / "testes" / "amostra_eleitores.csv"

ITERACOES_EQUIPE = 600_000

PAREDE_LADO = {"oeste": "à esquerda", "norte": "em frente, do outro lado do salão", "leste": "à direita"}
ORDINAL = ["1º", "2º", "3º", "4º", "5º", "6º"]
PALAVRAS_SENHA = (
    "urna cabine fila porta parede zona letra placa apron portao corredor raia cartorio "
    "mesario secao titulo ring hall calcada painel grupo lista senha dublin merrion ballsbridge "
    "outubro turno voto democracia eleitor apto passo fita ccb vinil banner mapa rota"
).split()


def carrega(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def tabela_mestra():
    """Pares (seção, letra) da peça P0-Mestra, para conferir contra decisoes.json."""
    html = MESTRA.read_text(encoding="utf-8")
    pares = re.findall(r">(\d{4})</span>.*?>([ABC])</span>", html, flags=re.S)
    return {s: l for s, l in pares}


def monta_rotas(dec, grupos):
    """Um registro por seção: onde está a mesa e como chegar lá."""
    entradas = {e["id"]: e for e in dec["entradas"]}
    grupos_por_secao = {}
    ordem_na_parede = {}
    for g in grupos["grupos"]:
        letra = g["entrada"]
        ordem_na_parede.setdefault(letra, []).append(g["id"])
        for i, s in enumerate(g["secoes"]):
            grupos_por_secao[normaliza_secao(s)] = (g, i)
    rotas = {}
    for m in dec["mesas"]:
        letra = m["entrada"]
        ent = entradas[letra]
        secoes_mesa = [normaliza_secao(m["principal"])] + ([normaliza_secao(m["agregada"])] if m.get("agregada") else [])
        for s in secoes_mesa:
            g, _ = grupos_por_secao[s]
            if g["entrada"] != letra or g["porta"] != m["porta"] or g["parede"] != m["parede"]:
                raise SystemExit(f"seção {s}: grupo {g['id']} ({g['entrada']}/{g['porta']}/{g['parede']}) "
                                 f"não bate com a mesa MRV {m['mrv']} ({letra}/{m['porta']}/{m['parede']})")
            n_grupo = ordem_na_parede[letra].index(g["id"])
            i_mesa = next(i for i, par in enumerate(g["por_mesa"]) if int(s) in par)
            rotas[s] = {
                "secao": s,
                "papel": "principal" if s == normaliza_secao(m["principal"]) else "agregada",
                "secoes_da_mesa": secoes_mesa,
                "mrv": m["mrv"],
                "letra": letra,
                "porta": m["porta"],
                "parede": m["parede"],
                "cor": ent["cor"],
                "grupo": g["id"],
                "secoes_do_grupo": [normaliza_secao(x) for x in g["secoes"]],
                "ordem_grupo": n_grupo + 1,
                "coord_grupo": g["coord"][i_mesa],
                "grupos_na_parede": len(ordem_na_parede[letra]),
                "serpenteado": any(sp["mrv"] == m["mrv"] for sp in dec.get("serpenteados", [])),
                "passos": passos(letra, m["porta"], m["parede"], g["id"], n_grupo, [normaliza_secao(x) for x in g["secoes"]]),
            }
    return dict(sorted(rotas.items()))


def passos(letra, porta, parede, grupo, n_grupo, secoes_grupo):
    """Texto do caminho, no vocabulário das peças de sinalização P1–P7."""
    if letra == "C":
        ring = "Entre no Ring 3 pelo canto nordeste e desça o corredor. A boca da zona C é a PRIMEIRA que você alcança."
    elif letra == "B":
        ring = "Entre no Ring 3 pelo canto nordeste e desça o corredor. Passe a boca C; a zona B é a SEGUNDA, no centro."
    else:
        ring = "Entre no Ring 3 pelo canto nordeste e desça o corredor. Passe as bocas C e B; a zona A é a ÚLTIMA, no fim do trecho de fundo."
    return [
        {"onde": "Portão · Merrion Road", "texto": f"Sua letra é {letra}. Anote: você vai procurá-la três vezes no caminho. Siga a fila pela lateral leste do Hall 2."},
        {"onde": "Ring 3 · pátio de fila", "texto": f"{ring} Confira a placa da boca: sua seção está listada nela."},
        {"onde": "Cabeça da fila · apron", "texto": f"Da cabeça da zona {letra}, atravesse os 14 m do apron até a porta {porta}, com a letra {letra} no vidro."},
        {"onde": f"Hall 2 · parede {parede}", "texto": f"Sua mesa fica na parede {parede}, {PAREDE_LADO[parede]}. Procure o painel {letra} e siga até o grupo {grupo}, o {ORDINAL[n_grupo]} corredor a partir da porta. Na placa alta: “grupo {grupo} · seções {' '.join(secoes_grupo)}”."},
        {"onde": "Mesa", "texto": "Apresente o documento com foto ao mesário. Não encontrou a sua seção? Procure um mesário: sua seção está em outra porta."},
        {"onde": "Saída", "texto": "Saia pelas portas S2 ou S8 (placa SAÍDA → Merrion Road)."},
    ]


def le_lista(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)
        sep = ";" if amostra.count(";") >= amostra.count(",") else ","
        return list(csv.DictReader(f, delimiter=sep))


def prepara_eleitores(linhas):
    """Normaliza cada linha e descobre qual 2º fator a lista permite (nascimento ou mãe)."""
    eleitores = []
    com_nasc = com_mae = 0
    for r in linhas:
        nome = normaliza_nome(r.get("NOM_ELEITOR"))
        if not nome:
            continue
        nasc = normaliza_data(r.get("DAT_NASC"))
        mae = normaliza_nome(r.get("NOM_MAE"))
        com_nasc += bool(nasc)
        com_mae += bool(mae)
        eleitores.append({
            "n": nome,
            "nome_original": (r.get("NOM_ELEITOR") or "").strip(),
            "d": nasc,
            "m": mae,
            "t": normaliza_inscricao(r.get("NUM_INSCRICAO")),
            "s": normaliza_secao(r.get("NUM_SECAO")),
        })
    n = len(eleitores)
    if n and com_nasc >= 0.98 * n:
        fator = "nascimento"
    elif n and com_mae >= 0.98 * n:
        fator = "mae"
    else:
        raise SystemExit(f"a lista não tem 2º fator utilizável: nascimento em {com_nasc}/{n}, nome da mãe em {com_mae}/{n}")
    return eleitores, fator


def monta_indice(eleitores, fator):
    itens = defaultdict(set)
    for e in eleitores:
        segundo = e["d"] if fator == "nascimento" else e["m"]
        if not segundo:
            continue
        for chave in chaves_nome(e["n"]):
            itens[hash_publico(chave, segundo)].add(e["s"])
    ambiguos = sum(1 for v in itens.values() if len(v) > 1)
    return {
        "v": 1,
        "kdf": "PBKDF2-SHA256",
        "iteracoes": ITERACOES_PUBLICO,
        "sal": SAL_PUBLICO.decode("ascii"),
        "bytes": TAMANHO_HASH,
        "fator": fator,
        "n": len(eleitores),
        "itens": {h: sorted(v) for h, v in sorted(itens.items())},
    }, ambiguos


def cifra_equipe(eleitores, fator, senha):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    registros = [{"n": e["n"], "o": e["nome_original"], "d": e["d"], "m": e["m"], "t": e["t"], "s": e["s"]} for e in eleitores]
    claro = zlib.compress(json.dumps({"fator": fator, "eleitores": registros}, ensure_ascii=False).encode("utf-8"), 9)
    sal = secrets.token_bytes(16)
    iv = secrets.token_bytes(12)
    chave = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES_EQUIPE, 32)
    cifrado = AESGCM(chave).encrypt(iv, claro, None)
    b64 = lambda b: base64.b64encode(b).decode("ascii")
    return {"v": 1, "kdf": "PBKDF2-SHA256", "iteracoes": ITERACOES_EQUIPE, "sal": b64(sal), "iv": b64(iv),
            "cifra": "AES-256-GCM", "compressao": "deflate", "n": len(registros), "dados": b64(cifrado)}


def confere(rotas, eleitores, dec):
    erros = []
    if len(rotas) != 51:
        erros.append(f"rotas cobrem {len(rotas)} seções, esperava 51")
    mestra = tabela_mestra()
    if len(mestra) != 51:
        erros.append(f"tabela mestra P0 lida com {len(mestra)} linhas, esperava 51")
    for s, r in rotas.items():
        if mestra.get(s) != r["letra"]:
            erros.append(f"seção {s}: decisoes.json diz {r['letra']}, P0-Mestra diz {mestra.get(s)}")
    letras = Counter(r["letra"] for r in rotas.values())
    if letras != {"A": 18, "B": 16, "C": 17}:
        erros.append(f"seções por letra {dict(letras)}, esperava A 18 / B 16 / C 17")
    desconhecidas = Counter(e["s"] for e in eleitores if e["s"] not in rotas)
    if desconhecidas:
        erros.append(f"eleitores em seções que não são de Dublin: {dict(desconhecidas)}")
    sem_titulo = sum(1 for e in eleitores if not e["t"])
    if sem_titulo:
        erros.append(f"{sem_titulo} eleitores sem número de inscrição")
    return erros


def senha_sorteada():
    return " ".join(secrets.choice(PALAVRAS_SENHA) for _ in range(6))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lista", type=Path, default=AMOSTRA, help="CSV nominal (padrão: amostra sintética)")
    ap.add_argument("--grava", action="store_true", help="escreve app/dist/; sem isso só confere")
    ap.add_argument("--senha-equipe", default=os.environ.get("APP_SENHA_EQUIPE"))
    args = ap.parse_args()

    dec, grupos = carrega(DECISOES), carrega(GRUPOS)
    rotas = monta_rotas(dec, grupos)
    linhas = le_lista(args.lista)
    eleitores, fator = prepara_eleitores(linhas)
    erros = confere(rotas, eleitores, dec)

    print(f"lista: {args.lista.relative_to(RAIZ) if args.lista.is_relative_to(RAIZ) else args.lista} · {len(eleitores)} eleitores · 2º fator: {fator}")
    print(f"rotas: {len(rotas)} seções · " + " · ".join(f"{l} {n}" for l, n in sorted(Counter(r['letra'] for r in rotas.values()).items())))
    por_secao = Counter(e["s"] for e in eleitores)
    vazias = [s for s in rotas if por_secao[s] == 0]
    if vazias:
        print(f"aviso: {len(vazias)} seções sem nenhum eleitor na lista: {' '.join(vazias)}")
    for e in erros:
        print("ERRO:", e)
    if erros:
        sys.exit(1)

    indice, ambiguos = monta_indice(eleitores, fator)
    print(f"índice público: {len(indice['itens'])} chaves, {ambiguos} com mais de uma seção (mandam ao P0)")
    if not args.grava:
        print("conferência ok; nada gravado (use --grava)")
        return

    senha = args.senha_equipe
    if not senha:
        senha = senha_sorteada()
        print(f"\nSENHA DA EQUIPE (sorteada agora, não fica gravada em lugar nenhum):\n    {senha}\n")
    pacote = cifra_equipe(eleitores, fator, senha)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUBLICO, DIST)
    dados = DIST / "dados"
    dados.mkdir(exist_ok=True)
    (dados / "rotas.json").write_text(json.dumps({"atualizado": dec["atualizadoEm"], "secoes": rotas}, ensure_ascii=False, indent=1), encoding="utf-8")
    (dados / "indice_publico.json").write_text(json.dumps(indice, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (dados / "equipe.enc").write_text(json.dumps(pacote, separators=(",", ":")), encoding="utf-8")
    versao = {
        "construido_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "eleitores": len(eleitores),
        "fator": fator,
        "lista": args.lista.name,
        "amostra_sintetica": args.lista.resolve() == AMOSTRA.resolve(),
        "indice_sha256": hashlib.sha256((dados / "indice_publico.json").read_bytes()).hexdigest()[:16],
    }
    (dados / "versao.json").write_text(json.dumps(versao, ensure_ascii=False, indent=1), encoding="utf-8")
    sw = DIST / "sw.js"
    sw.write_text(sw.read_text(encoding="utf-8").replace("__VERSAO__", versao["construido_em"]), encoding="utf-8")
    for nome in ("rotas.json", "indice_publico.json", "equipe.enc"):
        print(f"  {nome:22s} {(dados / nome).stat().st_size / 1024:7.0f} kB")
    print(f"gravado em {DIST.relative_to(RAIZ)}/ · versão {versao['construido_em']}")


if __name__ == "__main__":
    main()
