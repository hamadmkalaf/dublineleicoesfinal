"""Gera uma lista nominal SINTÉTICA para testar o app sem dado pessoal real.

    python3 scripts/app_gera_amostra.py            # escreve app/testes/amostra_eleitores.csv
    python3 scripts/app_gera_amostra.py --n 2000   # outro tamanho

Nomes inventados por combinação aleatória com semente fixa (o arquivo é reproduzível).
As seções são as 51 reais de Dublin (`data/decisoes.json`), com peso proporcional aos
aptos, para que o build exercite todas as portas e grupos. Inclui homônimos propositais:
  - "MARIA APARECIDA SILVA" ×3 com datas diferentes (resolvido pela data);
  - "JOAO CARLOS SOUZA" ×2 com a MESMA data e seções diferentes (caso que manda ao P0).
"""

import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "app" / "testes" / "amostra_eleitores.csv"

PRIMEIROS = [
    "ANA", "BRUNO", "CARLA", "DIEGO", "ELISA", "FABIO", "GABRIELA", "HUGO", "ISABELA",
    "JOAO", "KARINA", "LUCAS", "MARIA", "NATALIA", "OTAVIO", "PAULA", "RAFAEL", "SOFIA",
    "THIAGO", "VANESSA", "WAGNER", "LETICIA", "MARCOS", "JULIANA", "PEDRO", "BEATRIZ",
    "FELIPE", "CAMILA", "RODRIGO", "LARISSA",
]
MEIOS = [
    "", "", "", "CRISTINA", "CARLOS", "APARECIDA", "HENRIQUE", "LUIZA", "EDUARDO",
    "FERNANDA", "AUGUSTO", "HELENA", "VITOR", "REGINA", "ALESSANDRO", "DE FATIMA",
]
SOBRENOMES = [
    "SILVA", "SANTOS", "OLIVEIRA", "SOUZA", "PEREIRA", "LIMA", "COSTA", "FERREIRA",
    "RODRIGUES", "ALMEIDA", "NASCIMENTO", "ARAUJO", "CARVALHO", "GOMES", "MARTINS",
    "ROCHA", "RIBEIRO", "BARBOSA", "MOREIRA", "DIAS", "GONÇALVES", "D'ANDREA", "MÜLLER",
    "O'BRIEN", "SANT ANA",
]
CONECTIVOS = ["", "", "DE", "DA", "DOS", "DO"]


def nome_aleatorio(rnd):
    partes = [rnd.choice(PRIMEIROS)]
    meio = rnd.choice(MEIOS)
    if meio:
        partes.append(meio)
    c = rnd.choice(CONECTIVOS)
    if c:
        partes.append(c)
    partes.append(rnd.choice(SOBRENOMES))
    if rnd.random() < 0.4:
        partes.append(rnd.choice(SOBRENOMES))
    return " ".join(partes)


def data_aleatoria(rnd):
    inicio = date(1940, 1, 1)
    return inicio + timedelta(days=rnd.randrange((date(2008, 10, 4) - inicio).days))


def inscricao(rnd):
    return "".join(rnd.choice("0123456789") for _ in range(12))


def secoes_com_peso():
    dec = json.loads((RAIZ / "data" / "decisoes.json").read_text(encoding="utf-8"))
    pesos = []
    for m in dec["mesas"]:
        pesos.append((f"{m['principal']:04d}", m["aptos_principal"]))
        if m.get("agregada"):
            pesos.append((f"{m['agregada']:04d}", m["aptos_agregada"]))
    return pesos


def gera(n, semente=2026):
    rnd = random.Random(semente)
    secoes = secoes_com_peso()
    lista = [s for s, _ in secoes]
    pesos = [p for _, p in secoes]
    linhas = []
    for _ in range(n):
        linhas.append({
            "NUM_LOCAL": "1015",
            "NUM_SECAO": rnd.choices(lista, pesos)[0],
            "NUM_INSCRICAO": inscricao(rnd),
            "DAT_NASC": data_aleatoria(rnd).isoformat(),
            "NOM_ELEITOR": nome_aleatorio(rnd),
            "NOM_MAE": nome_aleatorio(rnd),
        })
    # homônimos propositais
    for d in ("1970-05-05", "1981-11-30", "1995-02-14"):
        linhas.append({"NUM_LOCAL": "1015", "NUM_SECAO": rnd.choice(lista), "NUM_INSCRICAO": inscricao(rnd),
                       "DAT_NASC": d, "NOM_ELEITOR": "MARIA APARECIDA SILVA", "NOM_MAE": nome_aleatorio(rnd)})
    for s in ("3313", "0511"):
        linhas.append({"NUM_LOCAL": "1015", "NUM_SECAO": s, "NUM_INSCRICAO": inscricao(rnd),
                       "DAT_NASC": "1988-08-08", "NOM_ELEITOR": "JOAO CARLOS SOUZA", "NOM_MAE": nome_aleatorio(rnd)})
    # um eleitor fixo, usado pelos testes de ponta a ponta
    linhas.append({"NUM_LOCAL": "1015", "NUM_SECAO": "3889", "NUM_INSCRICAO": "123456789012",
                   "DAT_NASC": "1975-03-16", "NOM_ELEITOR": "TIZZANI VIANA D'ANDREA NERY", "NOM_MAE": "NEUZA VIANA D'ANDREA"})
    linhas.sort(key=lambda r: (r["NUM_SECAO"], r["NOM_ELEITOR"]))
    return linhas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--destino", type=Path, default=DESTINO)
    args = ap.parse_args()
    linhas = gera(args.n)
    args.destino.parent.mkdir(parents=True, exist_ok=True)
    with open(args.destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["NUM_INSCRICAO", "NOM_ELEITOR", "DAT_NASC", "NUM_SECAO", "NOM_MAE", "NUM_LOCAL"],
                           delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} eleitores sintéticos em {args.destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
