"""Gera saidas/editor.html — a prancheta manipulavel, em escala.

O editor serve para *estudar posicao*: arrastar uma mesa, girar de 90 em 90,
medir distancia entre dois pontos, e ver o que isso faz com os corredores.
Ele nao recalcula nada e nao decide nada — os numeros continuam saindo da
cadeia (passos 3 e 4), e o que sai daqui e um cenario, que so vira desenho
quando alguem o grava em cenarios/ e roda a cadeia de novo.

    python3 scripts/gera_editor.py

O que ele le, e por que:

  data/prancheta_hall2.json  a geometria medida: salao, modulo, as 18 portas e
                             as duas posicoes iniciais do circuito (cenarios A
                             e B), que sao a base sobre a qual os cenarios
                             gravam alteracoes.
  data/decisoes.json         a decisao em vigor: as 28 mesas com secoes,
                             esperado, classe, parede, entrada, numero
                             eleitor; o papel de cada porta; as zonas
                             protegidas e os serpenteados de 16/09.
  cenarios/*.json            a biblioteca de cenarios publicados.

O bloco `decisoes` que vai embutido na pagina vem do decisoes.json e **nao**
da copia congelada dentro do prancheta_hall2.json: aquela copia e de antes de
15/09 e ainda traz a atribuicao mesa -> entrada por cota do Ring 3. O mesmo
vale para as zonas: as do prancheta_hall2.json sao as antigas, e as que valem
sao decisoes.zonas_protegidas mais decisoes.serpenteados.
"""
import glob
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _camel(d):
    """O bloco de decisoes na forma que o template espera."""
    return dict(
        decididoEm=d["decididoEm"],
        atualizadoEm=d.get("atualizadoEm"),
        numeracao=d["numeracao"],
        numeracaoEleitor=d["numeracao_eleitor"],
        cenarioTrabalho=d["cenario_trabalho"],
        comparecimento={k: d["comparecimento"][k]
                        for k in ("base", "rotulo", "total", "aptos")},
        classes=d["classes"],
        portas=d["portas"],
        saidas=d["saidas"],
        nomenclaturaPortas=d["nomenclatura_portas"],
        entradas=d["entradas"],
        mesas={str(m["mrv"]): m for m in d["mesas"]},
    )


def _zonas(d):
    """As zonas que o desenho reserva: as protegidas e os serpenteados.

    O editor pinta as duas com a mesma hachura — o rotulo diz qual e qual.
    Sao as mesmas em A e em B, porque saem da decisao e nao do arranjo.
    """
    return [{"rect": z["rect"], "rotulo": z["rotulo"]}
            for z in d["zonas_protegidas"] + d["serpenteados"]]


def cenarios_publicados():
    saida = []
    for cam in sorted(glob.glob(os.path.join(RAIZ, "cenarios", "*.json"))):
        c = json.load(open(cam, encoding="utf-8"))
        c.setdefault("id", os.path.splitext(os.path.basename(cam))[0])
        saida.append(c)
    return saida


def monta():
    p = json.load(open(os.path.join(RAIZ, "data", "prancheta_hall2.json"),
                       encoding="utf-8"))
    d = json.load(open(os.path.join(RAIZ, "data", "decisoes.json"),
                       encoding="utf-8"))
    zonas = _zonas(d)
    return dict(
        salao=p["salao"], modulo=p["modulo"], portas=p["portas"],
        cenarios={cen: dict(zonas=zonas, vaos=p["cenarios"][cen]["vaos"],
                            mrvs=p["cenarios"][cen]["mrvs"])
                  for cen in ("A", "B")},
        decisoes=_camel(d),
        cenariosSalvos=cenarios_publicados(),
    )


def main():
    dados = monta()
    modelo = open(os.path.join(RAIZ, "scripts", "editor_template.html"),
                  encoding="utf-8").read()
    html = modelo.replace("@@dados@@", json.dumps(dados, ensure_ascii=False))
    if "@@" in html:
        raise SystemExit("placeholder nao substituido: " + html.split("@@")[1])
    cam = os.path.join(RAIZ, "saidas", "editor.html")
    open(cam, "w", encoding="utf-8").write(html)
    print("gravado", cam, os.path.getsize(cam), "bytes",
          f"— {len(dados['decisoes']['mesas'])} mesas, "
          f"{len(dados['cenariosSalvos'])} cenário(s) publicado(s)")


if __name__ == "__main__":
    main()
