#!/usr/bin/env python3
"""Mantém `data/grupos_mesas.json` alinhado ao arranjo do Hall 2.

O arquivo nasceu de `saidas/sinalizacao_v2.json` (branch de origem, não
transferido) e desde então ninguém o regerava: a coordenada de cada grupo
(`coord`) é a posição das suas mesas na parede, e ela sai do cenário de
trabalho. Este script refaz **só** o que depende do arranjo — `coord` e, por
conferência, `por_mesa`, `secoes`, `mrvs`, `parede`, `entrada`, `porta` — e
deixa os ids, o `tipo` e a ordem dos grupos como estão.

Lê, sem escrever: `data/decisoes.json`, `data/prancheta_hall2.json` e
`cenarios/<cenario_trabalho>.json`.

    python3 scripts/grupos_mesas.py            confere e sai com código 1 se divergir
    python3 scripts/grupos_mesas.py --grava    regrava data/grupos_mesas.json
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ALVO = RAIZ / "data" / "grupos_mesas.json"

ENTRADA = {"oeste": "A", "norte": "B", "leste": "C"}
PORTA = {"A": "S4", "B": "S5", "C": "S6"}


def carrega(*p):
    return json.loads((RAIZ / pathlib.Path(*p)).read_text(encoding="utf-8"))


def posicoes(planta, cenario):
    pos = {m["n"]: {k: m[k] for k in ("x", "y", "rot", "lado")}
           for m in planta["cenarios"][cenario["base"]]["mrvs"]}
    for a in cenario["alteracoes"]:
        pos[a["n"]].update({k: a[k] for k in ("x", "y", "rot", "lado")})
    return pos


def coordenada(m, pos):
    """A coordenada ao longo da parede: y nas paredes oeste e leste, x na norte."""
    p = pos[m["mrv"]]
    return p["x"] if m["parede"] == "norte" else p["y"]


def main():
    grava = "--grava" in sys.argv[1:]
    decisoes = carrega("data", "decisoes.json")
    planta = carrega("data", "prancheta_hall2.json")
    cenario = carrega("cenarios", decisoes["cenario_trabalho"]["id"] + ".json")
    pos = posicoes(planta, cenario)
    mesas = {m["mrv"]: m for m in decisoes["mesas"]}

    dados = json.loads(ALVO.read_text(encoding="utf-8"))
    novo = json.loads(json.dumps(dados))
    vistos = set()
    for g in novo["grupos"]:
        ms = [mesas[n] for n in g["mrvs"]]
        paredes = {m["parede"] for m in ms}
        if len(paredes) != 1:
            raise SystemExit(f"grupo {g['id']}: mesas em paredes diferentes {paredes}")
        parede = paredes.pop()
        g["parede"] = parede
        g["entrada"] = ENTRADA[parede]
        g["porta"] = PORTA[g["entrada"]]
        g["coord"] = [coordenada(m, pos) for m in ms]
        g["por_mesa"] = [sorted(s for s in (m["principal"], m["agregada"]) if s) for m in ms]
        g["secoes"] = sorted(s for grupo in g["por_mesa"] for s in grupo)
        g["aptos"] = sum(m["aptos"] for m in ms)
        g["esperado"] = sum(m["esperado"] for m in ms)
        vistos.update(g["mrvs"])
    if vistos != set(mesas):
        raise SystemExit(f"grupos cobrem {len(vistos)} mesas, não 28: faltam {sorted(set(mesas) - vistos)}")
    todas = sorted(s for g in novo["grupos"] for s in g["secoes"])
    if len(todas) != 51 or len(set(todas)) != 51:
        raise SystemExit(f"{len(todas)} seções nos grupos, esperadas 51 sem repetição")

    # os códigos crescem ao longo da parede: y na oeste e na leste (sul → norte), x na norte
    for parede in ("oeste", "norte", "leste"):
        gs = sorted((g for g in novo["grupos"] if g["parede"] == parede), key=lambda g: min(g["coord"]))
        ids = [g["id"] for g in gs]
        if ids != sorted(ids):
            raise SystemExit(f"parede {parede}: a ordem física {ids} não segue os códigos")

    texto = json.dumps(novo, ensure_ascii=False, indent=1)
    atual = ALVO.read_text(encoding="utf-8")
    if texto == atual:
        print("grupos_mesas.json em dia com o cenário", cenario["id"])
        return 0
    mudou = [g["id"] for g, h in zip(dados["grupos"], novo["grupos"]) if g != h]
    if grava:
        ALVO.write_text(texto, encoding="utf-8")
        print(f"regravado data/grupos_mesas.json · grupos alterados: {', '.join(mudou)}")
        return 0
    print(f"data/grupos_mesas.json difere do cenário {cenario['id']} nos grupos "
          f"{', '.join(mudou)}; rode com --grava", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
