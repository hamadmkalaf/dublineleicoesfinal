"""Gera uma lista nominal SINTÉTICA para testar o app sem dado pessoal real.

    python3 scripts/app_gera_amostra.py            # escreve app/testes/amostra_eleitores.csv
    python3 scripts/app_gera_amostra.py --n 2000   # outro tamanho

Nomes inventados por combinação aleatória com semente fixa (o arquivo é reproduzível).
As seções são as 51 reais de Dublin (`data/decisoes.json`), com peso proporcional aos
aptos, para que o build exercite todas as portas e grupos. Inclui homônimos propositais, resolvidos pelo título (a lista real não tem nascimento):
  - "MARIA APARECIDA SILVA" ×3, seções diferentes, títulos 1111..., 2222..., 3333...;
  - "JOAO CARLOS SOUZA" ×2, seções 3313 e 0511, títulos 4444... e 5555....
Marcas de turno como na relação do TRE: a maioria OK/OK; alguns VT (voto em trânsito, premissa)
num turno ou nos dois. O eleitor fixo "ANA VT TESTE" é VT no 1º turno.
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
    def marcas():
        r = rnd.random()
        if r < 0.004:
            return "VT", "VT"
        if r < 0.006:
            return "VT", "OK"
        if r < 0.008:
            return "OK", "VT"
        return "OK", "OK"

    def linha(secao, insc, nome, mae=None, t1="OK", t2="OK", nasc=None):
        return {"NUM_LOCAL": "1015", "NUM_SECAO": secao, "NUM_INSCRICAO": insc,
                "DAT_NASC": nasc or data_aleatoria(rnd).isoformat(), "NOM_ELEITOR": nome,
                "NOM_MAE": mae or nome_aleatorio(rnd), "TURNO1": t1, "TURNO2": t2}

    for _ in range(n):
        t1, t2 = marcas()
        linhas.append(linha(rnd.choices(lista, pesos)[0], inscricao(rnd), nome_aleatorio(rnd), t1=t1, t2=t2))
    # homônimos propositais, desempatados pelo título
    secoes_maria = ["0511", "3313", "3862"]
    for i, sec in enumerate(secoes_maria, start=1):
        linhas.append(linha(sec, str(i) * 12, "MARIA APARECIDA SILVA"))
    linhas.append(linha("3313", "4" * 12, "JOAO CARLOS SOUZA"))
    linhas.append(linha("0511", "5" * 12, "JOAO CARLOS SOUZA"))
    # eleitores fixos, usados pelos testes de ponta a ponta
    linhas.append(linha("3889", "123456789012", "TIZZANI VIANA D'ANDREA NERY", mae="NEUZA VIANA D'ANDREA", nasc="1975-03-16"))
    linhas.append(linha("3315", "987654321098", "ANA VT TESTE", t1="VT", t2="OK"))
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
        w = csv.DictWriter(f, fieldnames=["NUM_INSCRICAO", "NOM_ELEITOR", "DAT_NASC", "NUM_SECAO", "NOM_MAE", "NUM_LOCAL", "TURNO1", "TURNO2"],
                           delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} eleitores sintéticos em {args.destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
