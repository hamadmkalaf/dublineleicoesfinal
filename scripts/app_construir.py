"""Constrói o app "Onde eu voto?" a partir da lista nominal e das decisões do Hall 2.

    python3 scripts/app_construir.py                       # só confere, não escreve nada (código 1 se quebrar)
    python3 scripts/app_construir.py --grava               # escreve app/dist/ com a amostra sintética
    python3 scripts/app_construir.py --grava --lista data/eleitores/eleitores_v2.csv --senha-equipe "seis palavras ..."
    python3 scripts/app_construir.py --grava --lista data/eleitores/eleitores_v2.csv.enc --senha-equipe "..."   # lista cifrada do git

Lê (nunca escreve): data/decisoes.json, data/grupos_mesas.json, mapa/sinalizacao/P0-Mestra.dc.html,
app/public/dados/config.json (turno_n).
Escreve em app/dist/:
  - tudo de app/public/ (o site, sem build de frontend);
  - dados/rotas.json          seção -> mesa, letra, porta, parede, grupo, passos do caminho (público, sem dado pessoal);
  - dados/indice_publico.json consulta por NOME (desenho de 01/10/2026, lista do TRE sem nascimento):
                                hash(chave do nome) -> [seção] quando a chave é de uma pessoa só;
                                hash(chave do nome) -> "H" quando há homônimos, e então
                                hash(chave do nome | título de 12 dígitos) -> [seção] para cada um deles.
                              A seção vem acompanhada da marca de turno quando ela não é "OK" (ex.: VT).
  - dados/equipe.enc          lista completa (nome, título, seção, marcas 1º/2º turno) cifrada com AES-256-GCM; leva
                              também posição alfabética na seção da lista e "número no caderno" (p/c, v3), que a
                              página NÃO exibe (02/10: a lista é por mesa; o caderno físico é por seção);
  - dados/versao.json         carimbo da construção, para o service worker perceber a atualização.
Em dados/rotas.json vai também um bloco "zonas" (urnas, aptos e esperado por zona A/B/C), que a
estimativa de espera da fila (v3) usa junto com os parâmetros de config.json ("fila").
O estado vivo da fila (lotação por zona, status ligado/desligado) NÃO sai do build: mora em
fila.json num branch próprio do repositório, escrito pela equipe/admin pela API do GitHub
(ver docs/app/contexto.md §2d).

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
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app_normaliza import (  # noqa: E402
    CADERNO_BLOCO, ITERACOES_PUBLICO, SAL_PUBLICO, TAMANHO_HASH, TITULO_JANELA, chave_caderno, chaves_nome,
    hash_publico, normaliza_inscricao, normaliza_nome, normaliza_secao, numero_caderno, titulo_parcial,
)

TITULO = {"digitos": f"{TITULO_JANELA[0]}-{TITULO_JANELA[1]}", "tamanho": 4}
COLUNA_PARCIAL = f"TITULO_{TITULO_JANELA[0]}_{TITULO_JANELA[1]}"

RAIZ = Path(__file__).resolve().parent.parent
DECISOES = RAIZ / "data" / "decisoes.json"
GRUPOS = RAIZ / "data" / "grupos_mesas.json"
MESTRA = RAIZ / "mapa" / "sinalizacao" / "P0-Mestra.dc.html"
PUBLICO = RAIZ / "app" / "public"
CONFIG = PUBLICO / "dados" / "config.json"
DIST = RAIZ / "app" / "dist"
AMOSTRA = RAIZ / "app" / "testes" / "amostra_eleitores.csv"

ITERACOES_EQUIPE = 600_000

# Orientação sempre na direção em que o eleitor caminha: ele entra no Hall pelas portas da
# fachada sul, olhando para o fundo do salão. Oeste = esquerda, norte = fundo, leste = direita.
# Nos textos ao eleitor não se usam pontos cardeais, "apron", "boca" nem "cabeça" (decisão de 01/10).
ROTULO_PAREDE = {"oeste": "da esquerda", "norte": "do fundo", "leste": "da direita"}
ORDINAL = ["1º", "2º", "3º", "4º", "5º", "6º"]
PALAVRAS_SENHA = (
    "urna cabine fila porta parede zona letra placa patio portao corredor raia cartorio "
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
                "parede_rotulo": ROTULO_PAREDE[m["parede"]],
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


def monta_zonas(dec):
    """Resumo por zona do Ring 3 (A/B/C): urnas, aptos e comparecimento esperado, para a estimativa de espera."""
    zonas = {}
    for ent in dec["entradas"]:
        mesas = [m for m in dec["mesas"] if m["entrada"] == ent["id"]]
        zonas[ent["id"]] = {
            "urnas": len(mesas),
            "aptos": sum(m["aptos"] for m in mesas),
            "esperado": ent["esperado"],
            "porta": ent["porta"],
            "parede": ent["parede"],
        }
    return zonas


def passos(letra, porta, parede, grupo, n_grupo, secoes_grupo):
    """Texto do caminho, na perspectiva de quem caminha (textos ditados em 01/10/2026).

    Sem números de porta da prancheta (S4, S7…): o eleitor só lê "porta A/B/C". O parâmetro
    `porta` fica na assinatura para os dados da rota, mas não entra em nenhuma frase.
    """
    ordem = {"C": "a primeira que você encontra", "B": "a segunda", "A": "a última, no fim do trecho de fundo"}[letra]
    rotulo = ROTULO_PAREDE[parede]
    return [
        {"onde": "Portão · Merrion Road", "texto": f"Lembre-se disso: sua porta de entrada é {letra}. Pegue a fila {letra} em frente ao Hall 2."},
        {"onde": "Ring 3 · pátio de fila", "texto": f"As filas serão formadas em frente ao Hall 2, no espaço chamado Ring 3. Entre no corredor e caminhe até o fundo. Chegando ao fundo, a fila {letra} será {ordem}."},
        {"onde": "Frente da fila · pátio", "texto": f"Quando liberado, atravesse o pátio até a porta de entrada {letra} (identificada com um adesivo no vidro)."},
        {"onde": f"Hall 2 · parede {rotulo}", "texto": f"Sua mesa fica na parede {rotulo}{', em frente a você' if parede == 'norte' else ''}. Procure o painel {letra} e siga até o grupo {grupo}, o {ORDINAL[n_grupo]} corredor a partir da porta. Na placa alta: “grupo {grupo} · seções {' '.join(secoes_grupo)}”."},
        {"onde": "Mesa", "texto": "Apresente o documento com foto ao mesário e diga a ele a sua seção, a que aparece no e-Título. Não encontrou sua seção no grupo? Pergunte ao mesário."},
        {"onde": "Saída", "texto": "Saia pelas portas com a placa SAÍDA; elas levam de volta à Merrion Road."},
    ]


def le_lista(caminho, senha=None):
    """CSV canônico em claro, ou cifrado (.enc, ver app_cifra_lista.py) com a senha da equipe."""
    import io

    if str(caminho).endswith(".enc"):
        from app_cifra_lista import le_csv_cifrado

        texto = le_csv_cifrado(caminho, senha)
    else:
        texto = Path(caminho).read_text(encoding="utf-8")
    sep = ";" if texto[:4096].count(";") >= texto[:4096].count(",") else ","
    return list(csv.DictReader(io.StringIO(texto, newline=""), delimiter=sep))


def prepara_eleitores(linhas):
    """Normaliza cada linha. A consulta é só por nome; o título PARCIAL (dígitos 5-8) desempata homônimos.

    Aceita o CSV com NUM_INSCRICAO de 12 dígitos (título completo) e o v2 (coluna TITULO_5_8).
    O índice público só conhece o parcial ("t"). O completo ("tc", quando existe) vai apenas ao
    pacote cifrado da equipe (decisão de 02/10/2026: a equipe volta a ver o título inteiro).
    """
    eleitores = []
    for r in linhas:
        nome = normaliza_nome(r.get("NOM_ELEITOR"))
        if not nome:
            continue
        completo = normaliza_inscricao(r.get("NUM_INSCRICAO")) if not r.get(COLUNA_PARCIAL) else ""
        bruto = r.get(COLUNA_PARCIAL) if r.get(COLUNA_PARCIAL) else completo
        eleitores.append({
            "n": nome,
            "nome_original": (r.get("NOM_ELEITOR") or "").strip(),
            "t": titulo_parcial(bruto),
            "tc": completo if len(completo) == 12 else "",
            "s": normaliza_secao(r.get("NUM_SECAO")),
            "t1": (r.get("TURNO1") or "").strip().upper(),
            "t2": (r.get("TURNO2") or "").strip().upper(),
        })
    return eleitores


def numera_caderno(eleitores):
    """Atribui a cada eleitor a posição alfabética na sua seção ("p") e o número no caderno ("c").

    Ordena por chave_caderno(nome impresso) e, em empate, pelo título parcial. A seção é a da
    lista (por mesa, agregadas somadas). Regra em app_normaliza.numero_caderno (v3, 01/10/2026).
    """
    por_secao = defaultdict(list)
    for e in eleitores:
        por_secao[e["s"]].append(e)
    for secao, pessoas in por_secao.items():
        pessoas.sort(key=lambda e: (chave_caderno(e["nome_original"] or e["n"]), e["t"]))
        for i, e in enumerate(pessoas, start=1):
            e["p"] = i
            e["c"] = numero_caderno(i)
    return eleitores


def marca_turno(e, turno):
    """Marca da lista para o turno em construção, só quando NÃO é 'OK' (vazia = sem marca)."""
    m = e["t1"] if turno == 1 else e["t2"]
    return "" if m in ("", "OK") else m


def monta_indice(eleitores, turno):
    """Índice público por nome.

    Cada eleitor entra pelas chaves de `chaves_nome` (nome completo e, se houver, primeiro +
    último). Chave de uma pessoa só: hash(chave) -> [seção] (+ marca de turno se não for OK).
    Chave de mais de uma: hash(chave) -> "H", e hash(chave|título parcial) -> [seção] para cada pessoa.
    Se duas pessoas da mesma chave têm o mesmo título parcial (colisão), a entrada vira "P":
    o app não consegue separá-las e manda ao P0.
    """
    por_chave = defaultdict(list)
    for e in eleitores:
        for chave in chaves_nome(e["n"]):
            por_chave[chave].append(e)
    pedidos = []  # (chave, fator, valor) — o hash é calculado em paralelo, é a parte lenta do build
    homonimos = 0
    sem_titulo = 0
    colisoes = 0
    for chave, pessoas in por_chave.items():
        if len(pessoas) == 1:
            pedidos.append((chave, "", valor_indice(pessoas[0], turno)))
            continue
        homonimos += 1
        pedidos.append((chave, "", "H"))
        repetidos = {t for t, n in Counter(e["t"] for e in pessoas).items() if n > 1}
        vistos = set()
        for e in pessoas:
            if not e["t"]:
                sem_titulo += 1
                continue
            if e["t"] in repetidos:
                if e["t"] not in vistos:
                    pedidos.append((chave, e["t"], "P"))
                    vistos.add(e["t"])
                    colisoes += 1
                continue
            pedidos.append((chave, e["t"], valor_indice(e, turno)))
    if sem_titulo:
        raise SystemExit(f"{sem_titulo} homônimos sem número de título: não há como desempatá-los")
    with ProcessPoolExecutor() as pool:
        hashes = list(pool.map(_hash_par, [(c, f) for c, f, _ in pedidos], chunksize=64))
    itens = {h: v for h, (_, _, v) in zip(hashes, pedidos)}
    if len(itens) != len(pedidos):
        raise SystemExit("colisão de hash no índice público (não deveria acontecer): confira a lista")
    nomes_repetidos = sum(1 for v in Counter(e["n"] for e in eleitores).values() if v > 1)
    return {
        "v": 2,
        "kdf": "PBKDF2-SHA256",
        "iteracoes": ITERACOES_PUBLICO,
        "sal": SAL_PUBLICO.decode("ascii"),
        "bytes": TAMANHO_HASH,
        "fator": "nome",
        "desempate": "titulo",
        "titulo": TITULO,
        "turno": turno,
        "n": len(eleitores),
        "itens": dict(sorted(itens.items())),
    }, {"chaves": len(por_chave), "ambiguas": homonimos, "nomes_completos_repetidos": nomes_repetidos, "colisoes": colisoes}


def _hash_par(par):
    return hash_publico(*par)


def valor_indice(e, turno):
    m = marca_turno(e, turno)
    return [e["s"], m] if m else [e["s"]]


def titulo_equipe(eleitores):
    """"completo" se todos os eleitores têm o título de 12 dígitos; senão "parcial" (só os dígitos 5-8)."""
    return "completo" if eleitores and all(e.get("tc") for e in eleitores) else "parcial"


def cifra_equipe(eleitores, turno, senha):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    registros = [{"n": e["n"], "o": e["nome_original"], "t": e["t"], "tc": e.get("tc", ""), "s": e["s"], "t1": e["t1"], "t2": e["t2"],
                  "p": e.get("p"), "c": e.get("c")} for e in eleitores]
    claro = zlib.compress(json.dumps({"fator": "nome", "titulo": TITULO, "titulo_equipe": titulo_equipe(eleitores), "turno": turno,
                                      "caderno": {"bloco": CADERNO_BLOCO}, "eleitores": registros}, ensure_ascii=False).encode("utf-8"), 9)
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
    sem_titulo = sum(1 for e in eleitores if len(e["t"]) != 4)
    if sem_titulo:
        erros.append(f"{sem_titulo} eleitores sem título parcial de 4 dígitos")
    return erros


def senha_sorteada():
    return " ".join(secrets.choice(PALAVRAS_SENHA) for _ in range(6))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lista", type=Path, default=AMOSTRA, help="CSV nominal (padrão: amostra sintética)")
    ap.add_argument("--grava", action="store_true", help="escreve app/dist/; sem isso só confere")
    ap.add_argument("--senha-equipe", default=os.environ.get("APP_SENHA_EQUIPE"))
    ap.add_argument("--turno", type=int, choices=(1, 2), help="turno em construção (padrão: turno_n de config.json)")
    args = ap.parse_args()

    config = carrega(CONFIG)
    turno = args.turno or int(config.get("turno_n", 1))
    dec, grupos = carrega(DECISOES), carrega(GRUPOS)
    rotas = monta_rotas(dec, grupos)
    linhas = le_lista(args.lista, args.senha_equipe)
    eleitores = numera_caderno(prepara_eleitores(linhas))
    zonas = monta_zonas(dec)
    erros = confere(rotas, eleitores, dec)
    if sorted(zonas) != ["A", "B", "C"] or sum(z["urnas"] for z in zonas.values()) != 28:
        erros.append(f"zonas do Ring 3: {zonas}")

    print(f"lista: {args.lista.relative_to(RAIZ) if args.lista.is_relative_to(RAIZ) else args.lista} · {len(eleitores)} eleitores · consulta por nome, título desempata · turno {turno}")
    print(f"rotas: {len(rotas)} seções · " + " · ".join(f"{l} {n}" for l, n in sorted(Counter(r['letra'] for r in rotas.values()).items())))
    por_secao = Counter(e["s"] for e in eleitores)
    vazias = [s for s in rotas if por_secao[s] == 0]
    agregadas = {normaliza_secao(m["agregada"]) for m in dec["mesas"] if m.get("agregada")}
    if vazias and set(vazias) <= agregadas:
        print(f"lista por mesa: as {len(vazias)} seções agregadas não aparecem (já estão somadas na principal)")
    elif vazias:
        print(f"aviso: {len(vazias)} seções sem nenhum eleitor na lista: {' '.join(vazias)}")
    marcas = Counter(marca_turno(e, turno) for e in eleitores)
    fora = {m: n for m, n in marcas.items() if m}
    if fora:
        print(f"marcas no turno {turno} diferentes de OK: " + " · ".join(f"{m} {n}" for m, n in fora.items()) + " (o app avisa esses eleitores)")
    for e in erros:
        print("ERRO:", e)
    if erros:
        sys.exit(1)

    indice, resumo = monta_indice(eleitores, turno)
    maior = max(e["p"] for e in eleitores) if eleitores else 0
    print(f"caderno: posição alfabética por seção; maior seção com {maior} eleitores · número = posição, ou posição − {CADERNO_BLOCO} acima de {CADERNO_BLOCO}")
    print(f"zonas do Ring 3: " + " · ".join(f"{l} {z['urnas']} urnas / {z['esperado']} esperados" for l, z in zonas.items()))
    if titulo_equipe(eleitores) == "completo":
        print("pacote da equipe: título COMPLETO (12 dígitos); o índice público segue só com os dígitos 5-8")
    else:
        print(f"AVISO: a lista só tem o título parcial ({sum(1 for e in eleitores if not e.get('tc'))} eleitores sem os 12 dígitos): "
              "a equipe verá só os dígitos 5-8. Reimporte o PDF do TRE com app_importar_eleitores.py (padrão: título completo).")
    print(f"índice público: {resumo['chaves']} chaves de nome, {resumo['ambiguas']} com homônimos (pedem o título), "
          f"{resumo['nomes_completos_repetidos']} nomes completos repetidos · {len(indice['itens'])} entradas · "
          f"título parcial (dígitos {TITULO['digitos']}): {resumo['colisoes']} colisões (mandam ao P0)")
    if not args.grava:
        print("conferência ok; nada gravado (use --grava)")
        return

    senha = args.senha_equipe
    if not senha:
        senha = senha_sorteada()
        print(f"\nSENHA DA EQUIPE (sorteada agora, não fica gravada em lugar nenhum):\n    {senha}\n")
    pacote = cifra_equipe(eleitores, turno, senha)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUBLICO, DIST)
    dados = DIST / "dados"
    dados.mkdir(exist_ok=True)
    (dados / "rotas.json").write_text(json.dumps({"atualizado": dec["atualizadoEm"], "zonas": zonas, "secoes": rotas}, ensure_ascii=False, indent=1), encoding="utf-8")
    (dados / "indice_publico.json").write_text(json.dumps(indice, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (dados / "equipe.enc").write_text(json.dumps(pacote, separators=(",", ":")), encoding="utf-8")
    versao = {
        "construido_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "eleitores": len(eleitores),
        "fator": "nome",
        "titulo": TITULO,
        "titulo_equipe": titulo_equipe(eleitores),
        "turno": turno,
        "app": config.get("versao_app", ""),
        "caderno": {"bloco": CADERNO_BLOCO},
        "homonimos": resumo["ambiguas"],
        "colisoes_titulo": resumo["colisoes"],
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
