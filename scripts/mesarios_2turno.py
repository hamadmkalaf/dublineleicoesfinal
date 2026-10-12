"""Mesarios do 2o turno: expectativa de comparecimento e funcoes a preencher.

Le tres planilhas de 12/10/2026, cada uma referencia para uma parte:

1. ``Mesarios_Secoes_Atualizadas`` -- so a aba ``Por secao``: aptos e
   comparecimento efetivo dos 28 BUs de 04/10, posicao e faixa efetiva.
2. ``Mesarios_Comparecimento_confirmado`` -- aba ``Mesarios``: secao, funcao,
   nome, e-mail, titulo e a presenca consolidada do 1o turno.
3. ``Confirmacao_2turno_Forms`` -- respostas do formulario "Estara disponivel
   no segundo turno, dia 25/10/26?". Anonimo: so traz o nome digitado.

e grava uma planilha de 4 abas, ligadas por formula:

    Expectativa          secao, nome e expectativa de comparecimento
    Mesarios             a base editavel (112 linhas: 111 + a vaga da 3862)
    Funcoes a preencher  o que nao "Deve comparecer", por prioridade da secao
    Por secao            aptos, efetivo, posicao e faixa efetiva (BUs)

Para atualizar, muda-se a coluna "Resposta 2o turno" da aba Mesarios; as
outras tres acompanham.

Regra de expectativa (definida pelo Posto em 12/10)
---------------------------------------------------
* respondeu SIM .................................. Deve comparecer
* respondeu NAO .................................. Nao deve comparecer
* nao respondeu e esteve no 1o turno ............. Confirmar
* nao respondeu e faltou ao 1o turno ............. Nao deve comparecer

Cruzamento resposta -> designado pelo nome sem acento e em maiusculas; o que
nao casa exato passa por ``EQUIVALENCIAS`` (tabela explicita, revisada a mao).
Quem respondeu mais de uma vez: vale a ULTIMA resposta (maior ID).

Uso
---
    python3 scripts/mesarios_2turno.py           # confere e imprime
    python3 scripts/mesarios_2turno.py --grava   # + grava o .xlsx

Sai com codigo 1 se alguma conferencia falhar. Precisa de openpyxl.
"""
import os
import sys
import unicodedata
from collections import Counter, defaultdict

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "saidas", "mesarios")
ENTRADA = os.path.join(PASTA, "entrada")
ARQ_SECOES = os.path.join(ENTRADA, "2026.10.12_Mesarios_Secoes_Atualizadas.xlsx")
ARQ_PRESENCA = os.path.join(ENTRADA, "2026.10.12_Mesarios_Comparecimento_confirmado.xlsx")
ARQ_FORMS = os.path.join(ENTRADA, "2026.10.12_Confirmacao_2turno_Forms_1-75.xlsx")
ARQ_SAIDA = os.path.join(PASTA, "2026.10.12_Mesarios_2turno_consolidado.xlsx")

FUNCOES = ["Presidente", "1º Mesário", "2º Mesário", "1º Secretário"]
# Ordem de preenchimento dentro de uma secao -- premissa operacional
PRIORIDADE_FUNCAO = {"Presidente": 1, "1º Mesário": 2, "1º Secretário": 3, "2º Mesário": 4}

DEVE, CONFIRMAR, NAO_DEVE, VAGO = "Deve comparecer", "Confirmar", "Não deve comparecer", "Vago"
ACAO = {CONFIRMAR: "Contatar para confirmar presença",
        NAO_DEVE: "Recrutar substituto",
        VAGO: "Recrutar mesário (função vaga)"}
NOME_VAGO = "— VAGO —"

# Nome como digitado no formulario (normalizado) -> nome na lista Elo
# (normalizado). Cada linha foi conferida a mao contra secao e funcao.
EQUIVALENCIAS = {
    "DANIELA CARETTE": "DANIELA LIMA DE MELO CARETTE",
    "EDIONES DINIZ": "EDIONES DINIZ SAVARIS",
    "ROGETIO GOES": "ROGERIO LINHARES GOES",  # erro de digitacao no form
    "NASTASSJA LOSADA": "NASTASSJA VERONICA LOUSADA GOMES",
    "INGRID MACHADO": "INGRID MACHADO DOS REIS",
    "LINCOLN GUEDES": "LINCOLN CUBAS GUEDES",
    "JAQUELINE TEIXEIRA": "JAQUELINE APARECIDA TEIXEIRA",
    "FERNANDA HERMANSON LOPES": "FERNANDA LIMA HERMANSON CARVALHO LOPES",
    "MARIANA GASPARETTI MCMANUS": "MARIANA JURANDIR GASPARETTI",
    "CAIO ROSSITER": "CAIO CESAR ROSSITER",
    "DIEGO MENDANHA": "DIEGO MENDANHA DA SILVA MAIA",
}

# Informado pelo Posto em 12/10, por fora do formulario. Os tres Presidentes
# das urnas Alto estiveram no 1o turno e confirmaram o 2o por contato direto.
# O boletim de identificacao nao registrava Jair; a presenca dele e corrigida.
CORRECOES_PRESENCA = {"JAIR DE ASSUNCAO CORREIA FILHO": "SIM"}
CONFIRMACOES_DIRETAS = {"MAIRA FABIOLA FABIANI", "JAIR DE ASSUNCAO CORREIA FILHO",
                        "VANESSA ROCHA BARBOSA BARBALHO"}

AZUL = "FF1F3864"
COR_EXPECTATIVA = {DEVE: "FFC6EFCE", CONFIRMAR: "FFFFEB9C", NAO_DEVE: "FFFFC7CE", VAGO: "FFD9D9D9"}
COR_FAIXA = {"Alto": "FFFF9999", "Médio": "FFFFE699", "Baixo": "FFC6E0B4"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.upper().split())


def sim_nao(v):
    return "SIM" if norm(v) == "SIM" else "NÃO"


def expectativa(presenca, resposta):
    """A regra do Posto. ``resposta`` e "SIM", "NÃO" ou None."""
    if presenca is None:
        return VAGO
    if resposta == "SIM":
        return DEVE
    if resposta == "NÃO":
        return NAO_DEVE
    return CONFIRMAR if presenca == "SIM" else NAO_DEVE


# --------------------------------------------------------------------------
# Leitura e cruzamento
# --------------------------------------------------------------------------
def le():
    v1 = openpyxl.load_workbook(ARQ_SECOES, data_only=True)
    v2 = openpyxl.load_workbook(ARQ_PRESENCA, data_only=True)
    v3 = openpyxl.load_workbook(ARQ_FORMS, data_only=True)

    ws = v2["Mesarios"]
    cab = [c.value for c in ws[1]]
    ix = {k: cab.index(k) for k in ("Seção", "Função", "E-mail", "Nome",
                                    "Título de eleitor", "Presença consolidada")}
    mesarios = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        chave = norm(r[ix["Nome"]])
        presenca = CORRECOES_PRESENCA.get(chave, sim_nao(r[ix["Presença consolidada"]]))
        mesarios.append({"secao": r[ix["Seção"]], "funcao": r[ix["Função"]], "nome": r[ix["Nome"]],
                         "email": r[ix["E-mail"]], "titulo": r[ix["Título de eleitor"]],
                         "presenca": presenca, "chave": chave})

    ps = v1["Por secao"]
    cab1 = [c.value for c in ps[1]]
    secoes = []
    for r in ps.iter_rows(min_row=2, max_row=29, values_only=True):
        secoes.append({"secao": r[0], "aptos": r[cab1.index("Aptos (BU)")],
                       "efetivo": r[cab1.index("Comparecimento efetivo (BU)")],
                       "posicao": r[cab1.index("Posição (efetivo)")],
                       "faixa": r[cab1.index("Faixa efetiva")]})
    secoes.sort(key=lambda s: s["posicao"])

    respostas = [{"id": r[0], "nome": (r[6] or "").strip(), "resposta": sim_nao(r[7]), "chave": norm(r[6])}
                 for r in v3.active.iter_rows(min_row=2, values_only=True) if r[0] is not None]
    return mesarios, secoes, respostas


def cruza(mesarios, respostas):
    por_nome = {m["chave"]: m for m in mesarios}
    for r in respostas:
        alvo = r["chave"] if r["chave"] in por_nome else EQUIVALENCIAS.get(r["chave"])
        r["mesario"] = por_nome.get(alvo)
        r["casamento"] = ("exato" if r["chave"] in por_nome else
                          "equivalência" if r["mesario"] else "sem correspondência")
    for m in mesarios:
        rs = sorted((r for r in respostas if r["mesario"] is m), key=lambda r: r["id"])
        m["respostas"] = rs
        m["resposta"] = rs[-1]["resposta"] if rs else None
        m["ids"] = ", ".join(str(r["id"]) for r in rs)
        if m["chave"] in CONFIRMACOES_DIRETAS:
            m["resposta"] = "SIM"
            m["ids"] = ", ".join(filter(None, [m["ids"], "contato direto"]))
        m["expectativa"] = expectativa(m["presenca"], m["resposta"])


def com_vagas(mesarios, secoes):
    """As 112 posicoes (28 x 4), com as funcoes sem designado como VAGO."""
    ocupadas = {(m["secao"], m["funcao"]) for m in mesarios}
    linhas = list(mesarios)
    for s in secoes:
        for f in FUNCOES:
            if (s["secao"], f) not in ocupadas:
                linhas.append({"secao": s["secao"], "funcao": f, "nome": NOME_VAGO, "email": None,
                               "titulo": None, "presenca": None, "resposta": None, "ids": "",
                               "expectativa": VAGO, "respostas": []})
    ordem_f = {f: i for i, f in enumerate(FUNCOES)}
    linhas.sort(key=lambda m: (m["secao"], ordem_f[m["funcao"]]))
    return linhas


# --------------------------------------------------------------------------
# Conferencias e relatorio
# --------------------------------------------------------------------------
def confere(mesarios, linhas, secoes, respostas):
    falhas = []

    def ok(cond, msg):
        if not cond:
            falhas.append(msg)

    ok(len(mesarios) == 111, f"esperava 111 designados, li {len(mesarios)}")
    ok(len(linhas) == 112, f"esperava 112 posições (28 × 4), montei {len(linhas)}")
    ok(len({(m['secao'], m['funcao']) for m in linhas}) == 112, "seção|função repetida")
    ok(len({m['chave'] for m in mesarios}) == len(mesarios), "nome repetido entre designados")
    ok(len(secoes) == 28 and sorted(s["posicao"] for s in secoes) == list(range(1, 29)),
       "Por secao não tem as posições 1–28")
    ok({s["secao"] for s in secoes} == {m["secao"] for m in mesarios}, "seções de Mesarios ≠ Por secao")
    ok(sum(s["efetivo"] for s in secoes) == 8417, "comparecimento efetivo não fecha em 8.417")
    ok(sum(len(m["respostas"]) for m in mesarios) == sum(1 for r in respostas if r["mesario"]),
       "respostas casadas não batem com as atribuídas")
    usadas = {EQUIVALENCIAS[r["chave"]] for r in respostas if r["casamento"] == "equivalência"}
    ok(usadas == set(EQUIVALENCIAS.values()), "EQUIVALENCIAS tem entrada que não foi usada")
    nomes = {m["chave"] for m in mesarios}
    ok(CONFIRMACOES_DIRETAS <= nomes and set(CORRECOES_PRESENCA) <= nomes,
       "confirmação direta ou correção aponta para nome que não está na lista")
    return falhas


def relatorio(mesarios, linhas, respostas):
    exp = Counter(m["expectativa"] for m in linhas)
    print("Mesários do 2º turno (25/10/2026) — expectativa de comparecimento\n")
    print(f"Formulário: {len(respostas)} respostas — "
          f"{sum(r['casamento'] == 'exato' for r in respostas)} casadas exato, "
          f"{sum(r['casamento'] == 'equivalência' for r in respostas)} por equivalência, "
          f"sem correspondência: {', '.join(r['nome'] for r in respostas if not r['mesario']) or '—'}")
    conflito = [m["nome"] for m in mesarios if len({r["resposta"] for r in m["respostas"]}) > 1]
    print(f"Respostas conflitantes (vale a última): {', '.join(conflito) or '—'}")
    print(f"Confirmações diretas: {len(CONFIRMACOES_DIRETAS)} · correções de presença: {len(CORRECOES_PRESENCA)}\n")
    print("112 funções (28 urnas × 4):")
    for e in (DEVE, CONFIRMAR, NAO_DEVE, VAGO):
        print(f"  {e:<22} {exp[e]:>3}")
    print(f"  {'a preencher':<22} {112 - exp[DEVE]:>3}")


# --------------------------------------------------------------------------
# Gravacao
# --------------------------------------------------------------------------
def cabecalho(ws, titulos, larguras):
    for i, (t, w) in enumerate(zip(titulos, larguras), start=1):
        c = ws.cell(1, i, t)
        c.font = Font(bold=True, color="FFFFFFFF")
        c.fill = PatternFill("solid", fgColor=AZUL)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"


def cores(ws, faixa, ref, mapa):
    for valor, cor in mapa.items():
        ws.conditional_formatting.add(faixa, FormulaRule(
            formula=[f'{ref}="{valor}"'], fill=PatternFill("solid", bgColor=cor)))


def nota(ws, linha, texto, ncols):
    c = ws.cell(linha, 1, texto)
    c.font = Font(italic=True, size=9, color="FF595959")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=ncols)
    ws.row_dimensions[linha].height = 15 * (len(texto) // 110 + 1)


def grava(linhas, secoes):
    wb = openpyxl.Workbook()
    ex = wb.active
    ex.title = "Expectativa"
    me = wb.create_sheet("Mesários")
    fp = wb.create_sheet("Funções a preencher")
    ps = wb.create_sheet("Por seção")
    n = len(linhas)
    fim = n + 1
    ME = "'Mesários'"
    MEX = f"{ME}!$I$2:$I${fim}"

    # --- 4. Por secao ----------------------------------------------------
    cabecalho(ps, ["Seção", "Aptos (BU)", "Comparecimento efetivo (BU)", "Posição (efetivo)",
                   "Faixa efetiva"], [9, 11, 15, 11, 11])
    for i, s in enumerate(secoes, start=2):
        for j, k in enumerate(("secao", "aptos", "efetivo", "posicao", "faixa"), start=1):
            ps.cell(i, j, s[k])
        ps.cell(i, 2).number_format = ps.cell(i, 3).number_format = "#,##0"
    cores(ps, f"A2:E{len(secoes) + 1}", "$E2", COR_FAIXA)
    nota(ps, len(secoes) + 3, (
        "Boletins de Urna do 1º turno (04/10/2026), da aba 'Por secao' de 2026.10.12_Mesários_"
        "Seções_Atualizadas. Posição = ordem pelo comparecimento efetivo. Faixa efetiva: as 3 maiores "
        "= Alto; efetivo ≥ 329 = Médio; abaixo = Baixo. A posição define a ordem da aba 'Funções a "
        "preencher'."), 5)

    # --- 2. Mesarios (base) ----------------------------------------------
    cabecalho(me, ["Seção", "Função", "Nome", "E-mail", "Título de eleitor", "Presença 1º turno",
                   "Resposta 2º turno", "ID no formulário", "Expectativa", "Ordem (auxiliar)"],
              [8, 13, 40, 34, 15, 11, 11, 14, 20, 9])
    me.freeze_panes = "D2"
    pos = "'Por seção'!$A$2:$A$29"
    for i, m in enumerate(linhas, start=2):
        vals = [m["secao"], m["funcao"], m["nome"], m["email"], m["titulo"], m["presenca"],
                m["resposta"], m["ids"] or None]
        for j, v in enumerate(vals, start=1):
            me.cell(i, j, v)
        me.cell(i, 5).number_format = "@"
        if m["nome"] == NOME_VAGO:
            me.cell(i, 9, VAGO)
        else:
            me.cell(i, 9, f'=IF(G{i}="SIM","{DEVE}",IF(G{i}="NÃO","{NAO_DEVE}",'
                          f'IF(F{i}="SIM","{CONFIRMAR}","{NAO_DEVE}")))')
        # Ordem = posicao da secao x 10 + prioridade da funcao; vazio se nao ha o que preencher
        prio = PRIORIDADE_FUNCAO[m["funcao"]]
        me.cell(i, 10, f'=IF(I{i}="{DEVE}","",MATCH(A{i},{pos},0)*10+{prio})')
        me.cell(i, 10).font = Font(color="FF808080")
    for col, lista in (("F", '"SIM,NÃO"'), ("G", '"SIM,NÃO"')):
        dv = DataValidation(type="list", formula1=lista, allow_blank=True)
        dv.add(f"{col}2:{col}{fim}")
        me.add_data_validation(dv)
    cores(me, f"I2:I{fim}", "$I2", COR_EXPECTATIVA)
    me.conditional_formatting.add(f"F2:F{fim}", FormulaRule(
        formula=['$F2="NÃO"'], font=Font(color="FFC00000", bold=True)))
    me.auto_filter.ref = f"A1:J{fim}"
    nota(me, fim + 2, (
        "Para atualizar: mude a coluna G (Resposta 2º turno: SIM, NÃO ou vazio). As abas "
        "'Expectativa' e 'Funções a preencher' se recalculam. Presença 1º turno = presença "
        "consolidada (lista Elo × boletins de identificação de 04/10). Resposta 2º turno = última "
        "resposta no formulário de confirmação; 'contato direto' = confirmado por fora do formulário. "
        "Expectativa: SIM → Deve comparecer; NÃO → Não deve comparecer; sem resposta → Confirmar se "
        "esteve no 1º turno, senão Não deve comparecer. A coluna J só ordena a aba 'Funções a preencher'."), 10)

    # --- 1. Expectativa --------------------------------------------------
    cabecalho(ex, ["Seção", "Nome", "Expectativa"], [8, 40, 22])
    for i in range(2, fim + 1):
        ex.cell(i, 1, f"='Mesários'!A{i}")
        ex.cell(i, 2, f"='Mesários'!C{i}")
        ex.cell(i, 3, f"='Mesários'!I{i}")
    cores(ex, f"A2:C{fim}", "$C2", COR_EXPECTATIVA)
    ex.auto_filter.ref = f"A1:C{fim}"
    for k, e in enumerate((DEVE, CONFIRMAR, NAO_DEVE, VAGO)):
        ex.cell(2 + k, 5, e)
        ex.cell(2 + k, 6, f'=COUNTIF({MEX},"{e}")')
    ex.cell(1, 5, "Resumo").font = Font(bold=True)
    ex.cell(6, 5, "Total").font = Font(bold=True)
    ex.cell(6, 6, "=SUM(F2:F5)").font = Font(bold=True)
    cores(ex, "E2:F5", "$E2", COR_EXPECTATIVA)
    ex.column_dimensions["D"].width = 3
    ex.column_dimensions["E"].width = 22
    ex.column_dimensions["F"].width = 7

    # --- 3. Funcoes a preencher ------------------------------------------
    cabecalho(fp, ["Seção", "Função", "Nome do designado", "Sugestão de ação"], [8, 13, 40, 34])
    ORD = f"'Mesários'!$J$2:$J${fim}"
    for k in range(1, n + 1):
        i = k + 1
        lin = f"MATCH(SMALL({ORD},{k}),{ORD},0)"
        fp.cell(i, 1, f'=IFERROR(INDEX({ME}!$A$2:$A${fim},{lin}),"")')
        fp.cell(i, 2, f'=IFERROR(INDEX({ME}!$B$2:$B${fim},{lin}),"")')
        fp.cell(i, 3, f'=IFERROR(INDEX({ME}!$C$2:$C${fim},{lin}),"")')
        fp.cell(i, 4, f'=IFERROR(CHOOSE(MATCH(INDEX({MEX},{lin}),'
                      f'{{"{CONFIRMAR}","{NAO_DEVE}","{VAGO}"}},0),'
                      f'"{ACAO[CONFIRMAR]}","{ACAO[NAO_DEVE]}","{ACAO[VAGO]}"),"")')
    fp.conditional_formatting.add(f"A2:D{fim}", FormulaRule(
        formula=[f'$D2="{ACAO[CONFIRMAR]}"'], fill=PatternFill("solid", bgColor=COR_EXPECTATIVA[CONFIRMAR])))
    fp.conditional_formatting.add(f"A2:D{fim}", FormulaRule(
        formula=[f'$D2="{ACAO[NAO_DEVE]}"'], fill=PatternFill("solid", bgColor=COR_EXPECTATIVA[NAO_DEVE])))
    fp.conditional_formatting.add(f"A2:D{fim}", FormulaRule(
        formula=[f'$D2="{ACAO[VAGO]}"'], fill=PatternFill("solid", bgColor=COR_EXPECTATIVA[VAGO])))
    fp.cell(1, 6, "A preencher").font = Font(bold=True)
    fp.cell(1, 7, f'=COUNT({ORD})').font = Font(bold=True)
    fp.column_dimensions["F"].width = 13
    nota(fp, fim + 2, (
        "Lista as funções cuja expectativa não é 'Deve comparecer', na ordem de prioridade da seção "
        "(aba 'Por seção', comparecimento efetivo do 1º turno) e, dentro da seção, Presidente > "
        "1º Mesário > 1º Secretário > 2º Mesário (premissa). Calculada a partir da aba 'Mesários': "
        "não editar aqui."), 4)

    wb.calculation.fullCalcOnLoad = True
    wb.save(ARQ_SAIDA)
    print(f"\ngravado: {os.path.relpath(ARQ_SAIDA, RAIZ)}")


def main():
    mesarios, secoes, respostas = le()
    cruza(mesarios, respostas)
    linhas = com_vagas(mesarios, secoes)
    relatorio(mesarios, linhas, respostas)
    falhas = confere(mesarios, linhas, secoes, respostas)
    print("\nConferências: " + ("OK" if not falhas else "FALHARAM"))
    for f in falhas:
        print("  ✗ " + f)
    if falhas:
        sys.exit(1)
    if "--grava" in sys.argv:
        grava(linhas, secoes)


if __name__ == "__main__":
    main()
