"""Mesarios do 2o turno: quem volta, e quais funcoes faltam preencher.

Consolida tres planilhas de 12/10/2026, cada uma referencia para uma parte:

1. ``Mesarios_Secoes_Atualizadas`` -- vale SO a aba ``Por secao`` colunas M-W
   (comparecimento efetivo dos 28 BUs de 04/10) e a aba ``Ranking``. O resto
   dela (presenca com "0006/2026" e "-") esta superado pelo arquivo 2.
2. ``Mesarios_Comparecimento_confirmado`` -- vale ``Resumo``, ``Mesarios``
   (presenca consolidada x boletins), ``Presenca por secao`` e ``Por secao``
   colunas A-L. E a BASE do arquivo gerado: as abas dele seguem com as
   formulas e a formatacao originais.
3. ``Confirmacao_2turno_Forms`` -- respostas do formulario "Estara disponivel
   no segundo turno, dia 25/10/26?". Anonimo: so traz o nome digitado.

As duas abas ``Por secao`` tem o mesmo layout de linhas (secoes nas linhas
2-29, total na 30, notas e limiares de 32 a 38), entao as colunas M-W do
arquivo 1 sao enxertadas no arquivo 2 com as formulas intactas, e a aba
``Ranking`` (que le ``'Por secao'!V``) continua valendo.

Regras
------
* Cruzamento resposta -> designado pelo nome sem acento e em maiusculas; o que
  nao casa exato passa por ``EQUIVALENCIAS`` (tabela explicita, revisada a
  mao -- nada de casamento aproximado automatico). Sobra vai para revisao.
* Quem respondeu mais de uma vez: vale a ULTIMA resposta (maior ID).
* Lotacao integral (4 funcoes) nas urnas de faixa efetiva Alto ou Medio
  (col. W do arquivo 1). Nas Baixo a meta e ``META_BAIXO`` -- PREMISSA
  operacional, nao regra legal.
* Ordem de prioridade das funcoes ao preencher: ``ORDEM_PRIORIDADE`` --
  tambem premissa (Presidente primeiro, 2o Mesario por ultimo).

Uso
---
    python3 scripts/mesarios_2turno.py           # confere e imprime
    python3 scripts/mesarios_2turno.py --grava   # + grava o .xlsx consolidado

Sai com codigo 1 se alguma conferencia falhar.
"""
import os
import sys
import unicodedata
from collections import Counter, defaultdict
from copy import copy

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "saidas", "mesarios")
ENTRADA = os.path.join(PASTA, "entrada")
ARQ_SECOES = os.path.join(ENTRADA, "2026.10.12_Mesarios_Secoes_Atualizadas.xlsx")
ARQ_PRESENCA = os.path.join(ENTRADA, "2026.10.12_Mesarios_Comparecimento_confirmado.xlsx")
ARQ_FORMS = os.path.join(ENTRADA, "2026.10.12_Confirmacao_2turno_Forms_1-75.xlsx")
ARQ_SAIDA = os.path.join(PASTA, "2026.10.12_Mesarios_2turno_consolidado.xlsx")

# --------------------------------------------------------------------------
# Premissas
# --------------------------------------------------------------------------
FUNCOES = ["Presidente", "1º Mesário", "2º Mesário", "1º Secretário"]
ORDEM_PRIORIDADE = ["Presidente", "1º Mesário", "1º Secretário", "2º Mesário"]
FAIXAS_INTEGRAIS = ("Alto", "Médio")
META_INTEGRAL = 4
META_BAIXO = 3

CONFIRMADO, NAO_VOLTA, SEM_RESPOSTA, VAGO = "Confirmado", "Não volta", "Sem resposta", "VAGO"

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

# Linhas da aba 'Por secao' (iguais nos dois arquivos)
LIN_SECAO_1, LIN_SECAO_N, LIN_TOTAL, LIN_ULTIMA = 2, 29, 30, 38

AZUL = "FF1F3864"
VERDE, AMARELO, VERMELHO, CINZA = "FFC6EFCE", "FFFFEB9C", "FFFFC7CE", "FFD9D9D9"
COR_FAIXA = {"Alto": "FFFF9999", "Médio": "FFFFE699", "Baixo": "FFC6E0B4"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.upper().split())


def linhas(ws, inicio=2):
    return [r for r in ws.iter_rows(min_row=inicio, values_only=True) if any(v is not None for v in r)]


# --------------------------------------------------------------------------
# Leitura
# --------------------------------------------------------------------------
def le():
    v1 = openpyxl.load_workbook(ARQ_SECOES, data_only=True)
    v2 = openpyxl.load_workbook(ARQ_PRESENCA, data_only=True)
    v3 = openpyxl.load_workbook(ARQ_FORMS, data_only=True)

    cab = [c.value for c in v2["Mesarios"][1]]
    ix = {k: cab.index(k) for k in ("Seção", "Função", "E-mail", "Nome", "Presença consolidada")}
    mesarios = []
    for lin, r in enumerate(v2["Mesarios"].iter_rows(min_row=2, values_only=True), start=2):
        if r[0] is None:
            continue
        mesarios.append({
            "linha": lin, "secao": r[ix["Seção"]], "funcao": r[ix["Função"]],
            "email": r[ix["E-mail"]], "nome": r[ix["Nome"]],
            "presenca_1t": r[ix["Presença consolidada"]], "chave": norm(r[ix["Nome"]]),
        })

    ps1 = v1["Por secao"]
    cab1 = [c.value for c in ps1[1]]
    efetivo = {}
    for r in ps1.iter_rows(min_row=LIN_SECAO_1, max_row=LIN_SECAO_N, values_only=True):
        efetivo[r[0]] = {"aptos_bu": r[cab1.index("Aptos (BU)")],
                         "efetivo": r[cab1.index("Comparecimento efetivo (BU)")],
                         "posicao": r[cab1.index("Posição (efetivo)")],
                         "faixa": r[cab1.index("Faixa efetiva")]}
    ranking = [r for r in linhas(v1["Ranking"]) if isinstance(r[0], int)]

    respostas = []
    for r in linhas(v3.active):
        respostas.append({"id": r[0], "inicio": r[1], "fim": r[2], "nome": (r[6] or "").strip(),
                          "resposta": r[7], "chave": norm(r[6])})

    secoes_ps2 = [r[0] for r in v2["Por secao"].iter_rows(min_row=LIN_SECAO_1, max_row=LIN_SECAO_N, values_only=True)]
    secoes_ps1 = [r[0] for r in ps1.iter_rows(min_row=LIN_SECAO_1, max_row=LIN_SECAO_N, values_only=True)]
    total_efetivo_ps1 = ps1.cell(LIN_TOTAL, cab1.index("Comparecimento efetivo (BU)") + 1).value
    return mesarios, efetivo, ranking, respostas, secoes_ps1, secoes_ps2, total_efetivo_ps1


# --------------------------------------------------------------------------
# Cruzamento
# --------------------------------------------------------------------------
def cruza(mesarios, respostas):
    por_nome = {m["chave"]: m for m in mesarios}
    for r in respostas:
        alvo = r["chave"] if r["chave"] in por_nome else EQUIVALENCIAS.get(r["chave"])
        r["mesario"] = por_nome.get(alvo)
        r["casamento"] = ("exato" if r["chave"] in por_nome else
                          "equivalência" if r["mesario"] else "sem correspondência")

    por_pessoa = defaultdict(list)
    for r in respostas:
        if r["mesario"]:
            por_pessoa[r["mesario"]["chave"]].append(r)

    for m in mesarios:
        rs = sorted(por_pessoa.get(m["chave"], []), key=lambda r: r["id"])
        m["respostas"] = rs
        obs = []
        if not rs:
            m["status"] = SEM_RESPOSTA
        else:
            ultima = rs[-1]
            m["status"] = CONFIRMADO if norm(ultima["resposta"]) == "SIM" else NAO_VOLTA
            for r in rs:
                r["considerada"] = r is ultima
            if len({norm(r["resposta"]) for r in rs}) > 1:
                obs.append("Respostas conflitantes (" + " → ".join(
                    f"ID {r['id']} {r['resposta']}" for r in rs) + "); vale a última — confirmar por contato")
            elif len(rs) > 1:
                obs.append(f"Respondeu {len(rs)} vezes, mesma resposta")
        if m["status"] == CONFIRMADO and m["presenca_1t"] != "SIM":
            obs.append("Confirmou o 2º turno, mas foi AUSENTE no 1º turno")
        m["obs"] = "; ".join(obs)
    for r in respostas:
        r.setdefault("considerada", False)
        r["obs"] = ""
        if r["mesario"] and len(r["mesario"]["respostas"]) > 1:
            r["obs"] = "Duplicada — considerada" if r["considerada"] else "Duplicada — superada pela resposta seguinte"
            if len({norm(x["resposta"]) for x in r["mesario"]["respostas"]}) > 1:
                r["obs"] = "CONFLITO — " + ("considerada (última)" if r["considerada"] else "superada")
        if not r["mesario"]:
            r["obs"] = "Não corresponde a nenhum dos 111 designados — revisão manual"
    return respostas


def monta_urnas(mesarios, efetivo):
    grade = defaultdict(dict)
    for m in mesarios:
        grade[m["secao"]][m["funcao"]] = m
    urnas = []
    for secao, e in sorted(efetivo.items(), key=lambda kv: kv[1]["posicao"]):
        meta = META_INTEGRAL if e["faixa"] in FAIXAS_INTEGRAIS else META_BAIXO
        status = {f: (grade[secao][f]["status"] if f in grade[secao] else VAGO) for f in FUNCOES}
        conf = sum(s == CONFIRMADO for s in status.values())
        abertas = [f for f in ORDEM_PRIORIDADE if status[f] != CONFIRMADO]
        precisa = max(0, meta - conf)
        urnas.append({"secao": secao, **e, "meta": meta, "status": status, "grade": grade[secao],
                      "confirmados": conf, "deficit": precisa,
                      "necessarias": abertas[:precisa], "desejaveis": abertas[precisa:]})
    return urnas


# --------------------------------------------------------------------------
# Conferencias
# --------------------------------------------------------------------------
def confere(mesarios, efetivo, ranking, respostas, urnas, secoes_ps1, secoes_ps2, total_ps1):
    falhas = []

    def ok(cond, msg):
        if not cond:
            falhas.append(msg)

    st = Counter(m["status"] for m in mesarios)
    ok(len(mesarios) == 111, f"esperava 111 designados, li {len(mesarios)}")
    ok(len({(m['secao'], m['funcao']) for m in mesarios}) == len(mesarios), "chave seção|função repetida")
    ok(len({m['chave'] for m in mesarios}) == len(mesarios), "nome repetido entre designados")
    ok(secoes_ps1 == secoes_ps2, "as duas abas 'Por secao' não têm as seções na mesma ordem — enxerto M–W inválido")
    ok(set(secoes_ps2) == {m["secao"] for m in mesarios}, "seções de Mesarios ≠ seções de Por secao")
    ok(len(urnas) == 28 and sum(len(u["status"]) for u in urnas) == 112, "grade urna × função ≠ 28 × 4")
    ok(sum(st.values()) == len(mesarios), "confirmados + não volta + sem resposta ≠ designados")
    vagos = sum(s == VAGO for u in urnas for s in u["status"].values())
    ok(vagos + len(mesarios) == 112, "vagos + designados ≠ 112")
    ok(sum(e["efetivo"] for e in efetivo.values()) == total_ps1 == 8417,
       f"comparecimento efetivo não fecha em 8.417 ({total_ps1})")
    ok(sorted(r[0] for r in ranking) == list(range(1, 29)), "Ranking não tem as posições 1–28")
    ok({r[1] for r in ranking} == set(efetivo), "seções do Ranking ≠ seções de Por secao")
    casadas = sum(1 for r in respostas if r["mesario"])
    ok(casadas + sum(1 for r in respostas if not r["mesario"]) == len(respostas), "respostas perdidas no cruzamento")
    ok(sum(len(m["respostas"]) for m in mesarios) == casadas, "respostas casadas não batem com as atribuídas")
    usadas = {EQUIVALENCIAS.get(r["chave"]) for r in respostas if r["casamento"] == "equivalência"}
    ok(usadas == set(EQUIVALENCIAS.values()), "EQUIVALENCIAS tem entrada que não foi usada (nome mudou?)")
    return falhas


# --------------------------------------------------------------------------
# Relatorio
# --------------------------------------------------------------------------
def numeros(mesarios, respostas, urnas):
    st = Counter(m["status"] for m in mesarios)
    integ = [u for u in urnas if u["meta"] == META_INTEGRAL]
    baixo = [u for u in urnas if u["meta"] != META_INTEGRAL]
    return {
        "respostas": len(respostas),
        "ids_faltando": sorted(set(range(1, max(r["id"] for r in respostas) + 1)) - {r["id"] for r in respostas}),
        "resp_sim": sum(norm(r["resposta"]) == "SIM" for r in respostas),
        "resp_nao": sum(norm(r["resposta"]) != "SIM" for r in respostas),
        "exato": sum(r["casamento"] == "exato" for r in respostas),
        "equiv": sum(r["casamento"] == "equivalência" for r in respostas),
        "sem_corresp": [r for r in respostas if not r["mesario"]],
        "duplicados": [m for m in mesarios if len(m["respostas"]) > 1],
        "conflitos": [m for m in mesarios if len({norm(r["resposta"]) for r in m["respostas"]}) > 1],
        "st": st,
        "conf_presentes": sum(m["status"] == CONFIRMADO and m["presenca_1t"] == "SIM" for m in mesarios),
        "conf_ausentes": [m for m in mesarios if m["status"] == CONFIRMADO and m["presenca_1t"] != "SIM"],
        "nao_presentes": sum(m["status"] == NAO_VOLTA and m["presenca_1t"] == "SIM" for m in mesarios),
        "sr_presentes": sum(m["status"] == SEM_RESPOSTA and m["presenca_1t"] == "SIM" for m in mesarios),
        "vagos": sum(s == VAGO for u in urnas for s in u["status"].values()),
        "a_preencher": sum(4 - u["confirmados"] for u in urnas),
        "meta_total": sum(u["meta"] for u in urnas),
        "deficit": sum(u["deficit"] for u in urnas),
        "integ": integ, "baixo": baixo,
        "deficit_integ": sum(u["deficit"] for u in integ),
        "deficit_baixo": sum(u["deficit"] for u in baixo),
        "completas": [u for u in urnas if u["confirmados"] == 4],
        "na_meta": [u for u in urnas if u["deficit"] == 0],
        "sem_presidente": [u for u in urnas if u["status"]["Presidente"] != CONFIRMADO],
        "deficit_contato": sum(1 for u in urnas for f in u["necessarias"] if u["status"][f] == SEM_RESPOSTA),
        "deficit_recruta": sum(1 for u in urnas for f in u["necessarias"] if u["status"][f] in (NAO_VOLTA, VAGO)),
    }


def relatorio(n, urnas):
    st = n["st"]
    print("Mesários do 2º turno (25/10/2026) — consolidação de 12/10/2026\n")
    print(f"Formulário: {n['respostas']} respostas (IDs ausentes: {n['ids_faltando']}) — "
          f"{n['resp_sim']} SIM, {n['resp_nao']} NÃO")
    print(f"  casadas: {n['exato']} exato + {n['equiv']} por equivalência; "
          f"sem correspondência: {', '.join(r['nome'] for r in n['sem_corresp']) or '—'}")
    print(f"  responderam mais de uma vez: {', '.join(m['nome'] for m in n['duplicados'])}")
    print(f"  conflito SIM/NÃO: {', '.join(m['nome'] for m in n['conflitos']) or '—'} (vale a última)")
    print(f"\n111 designados: {st[CONFIRMADO]} confirmados · {st[NAO_VOLTA]} não voltam · "
          f"{st[SEM_RESPOSTA]} sem resposta")
    print(f"  confirmados que estiveram no 1º turno: {n['conf_presentes']}; "
          f"ausentes no 1º turno: {', '.join(m['nome'] for m in n['conf_ausentes']) or '—'}")
    print(f"\n112 funções (28 × 4, {n['vagos']} vaga desde o 1º turno): "
          f"{st[CONFIRMADO]} preenchidas, {n['a_preencher']} abertas")
    print(f"Meta (Alto+Médio = {META_INTEGRAL}, Baixo = {META_BAIXO}, premissa): {n['meta_total']} funções; "
          f"déficit {n['deficit']} = {n['deficit_integ']} nas {len(n['integ'])} prioritárias + "
          f"{n['deficit_baixo']} nas {len(n['baixo'])} Baixo")
    print(f"  do déficit: {n['deficit_contato']} são de designado sem resposta (contatar) e "
          f"{n['deficit_recruta']} exigem substituto (não volta ou vaga)")
    print(f"Urnas sem Presidente confirmado: {len(n['sem_presidente'])}\n")
    print(f"{'Pos':>3} {'Seção':>5} {'Efet.':>5} {'Faixa':<6} {'Meta':>4} "
          + " ".join(f"{f[:6]:<6}" for f in FUNCOES) + "  Conf  Déf")
    abrev = {CONFIRMADO: "ok", NAO_VOLTA: "NÃO", SEM_RESPOSTA: "s/r", VAGO: "VAGO"}
    for u in urnas:
        print(f"{u['posicao']:>3} {u['secao']:>5} {u['efetivo']:>5} {u['faixa']:<6} {u['meta']:>4} "
              + " ".join(f"{abrev[u['status'][f]]:<6}" for f in FUNCOES)
              + f"  {u['confirmados']:>4}  {u['deficit']:>3}")


# --------------------------------------------------------------------------
# Gravacao
# --------------------------------------------------------------------------
def copia_celula(orig, dest):
    dest.value = orig.value
    if orig.has_style:
        dest.font, dest.fill, dest.border = copy(orig.font), copy(orig.fill), copy(orig.border)
        dest.alignment, dest.number_format = copy(orig.alignment), orig.number_format
        dest.protection = copy(orig.protection)


def cabecalho(ws, titulos, larguras):
    fonte = Font(bold=True, color="FFFFFFFF")
    fundo = PatternFill("solid", fgColor=AZUL)
    for i, (t, w) in enumerate(zip(titulos, larguras), start=1):
        c = ws.cell(1, i, t)
        c.font, c.fill = fonte, fundo
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C2"
    ws.row_dimensions[1].height = 32


def regras_status(ws, faixa):
    for valor, cor in ((CONFIRMADO, VERDE), (SEM_RESPOSTA, AMARELO), (NAO_VOLTA, VERMELHO), (VAGO, CINZA)):
        col = faixa.split(":")[0].rstrip("0123456789")
        lin = faixa.split(":")[0][len(col):]
        ws.conditional_formatting.add(faixa, FormulaRule(
            formula=[f'{col}{lin}="{valor}"'], fill=PatternFill("solid", bgColor=cor)))


def regras_faixa(ws, faixa, ref):
    for valor, cor in COR_FAIXA.items():
        ws.conditional_formatting.add(faixa, FormulaRule(
            formula=[f'{ref}="{valor}"'], fill=PatternFill("solid", bgColor=cor)))


def nota(ws, linha, texto, ncols):
    c = ws.cell(linha, 1, texto)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(italic=True, size=9)
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=ncols)
    ws.row_dimensions[linha].height = 15 * max(1, len(texto) // 160 + 1)


def grava(mesarios, respostas, urnas, n):
    wb = openpyxl.load_workbook(ARQ_PRESENCA)
    src = openpyxl.load_workbook(ARQ_SECOES)

    # --- Por secao: enxerta M-W do arquivo 1 -----------------------------
    ps, ps1 = wb["Por secao"], src["Por secao"]
    for lin in range(1, LIN_ULTIMA + 1):
        for col in range(13, 24):  # M..W
            copia_celula(ps1.cell(lin, col), ps.cell(lin, col))
    for lin in range(LIN_TOTAL + 1, LIN_ULTIMA + 1):  # notas das colunas P-W
        if ps.cell(lin, 1).value is None and ps1.cell(lin, 1).value is not None:
            copia_celula(ps1.cell(lin, 1), ps.cell(lin, 1))
    for letra, dim in ps1.column_dimensions.items():
        if letra >= "M":
            ps.column_dimensions[letra].width = dim.width
    for cf in ps1.conditional_formatting:
        if str(cf.sqref).startswith(("Q", "V")):
            for regra in cf.rules:
                ps.conditional_formatting.add(str(cf.sqref), regra)

    # --- Ranking: copia inteira do arquivo 1 -----------------------------
    rk1 = src["Ranking"]
    rk = wb.create_sheet("Ranking")
    for row in rk1.iter_rows():
        for c in row:
            copia_celula(c, rk.cell(c.row, c.column))
    for letra, dim in rk1.column_dimensions.items():
        rk.column_dimensions[letra].width = dim.width
    rk.freeze_panes = rk1.freeze_panes
    for cf in rk1.conditional_formatting:
        for regra in cf.rules:
            rk.conditional_formatting.add(str(cf.sqref), regra)

    wb["Resumo"].title = "Resumo 1º turno"

    # --- Mesarios: colunas do 2o turno ----------------------------------
    me = wb["Mesarios"]
    base = me.cell(1, 15)  # O1, cabecalho de referencia
    for col, titulo, larg in ((16, "Resposta 2º turno", 16), (17, "ID(s) no formulário", 14),
                              (18, "Observação 2º turno", 60)):
        c = me.cell(1, col, titulo)
        copia_celula(base, c)
        c.value = titulo
        me.column_dimensions[get_column_letter(col)].width = larg
    for m in mesarios:
        me.cell(m["linha"], 16, m["status"])
        me.cell(m["linha"], 17, ", ".join(str(r["id"]) for r in m["respostas"]) or "—")
        me.cell(m["linha"], 18, m["obs"] or None)
    regras_status(me, "P2:P112")

    # --- Vagas por urna (formulas sobre Mesarios!P) ----------------------
    vg = wb.create_sheet("Vagas por urna")
    tit = ["Pos.", "Seção", "Efetivo (BU)", "Faixa efetiva", "Meta"]
    for f in FUNCOES:
        tit += [f, "Status"]
    tit += ["Confirmados", "Abertas (de 4)", "Déficit vs meta", "Alerta"]
    cabecalho(vg, tit, [6, 8, 10, 10, 6] + [36, 13] * 4 + [11, 10, 10, 34])
    lin_meta = len(urnas) + 4
    for i, u in enumerate(urnas, start=2):
        s = f"$B{i}"
        vg.cell(i, 1, u["posicao"])
        vg.cell(i, 2, u["secao"])
        vg.cell(i, 3, f"=INDEX('Por secao'!$Q$2:$Q$29,MATCH({s},'Por secao'!$A$2:$A$29,0))")
        vg.cell(i, 4, f"=INDEX('Por secao'!$W$2:$W$29,MATCH({s},'Por secao'!$A$2:$A$29,0))")
        vg.cell(i, 5, f'=IF(OR(D{i}="Alto",D{i}="Médio"),{META_INTEGRAL},$C${lin_meta})')
        stc = []
        for k, f in enumerate(FUNCOES):
            cn, cs = 6 + 2 * k, 7 + 2 * k
            chave = f'{s}&"|{f}"'
            vg.cell(i, cn, f'=IFERROR(INDEX(Mesarios!$D$2:$D$112,MATCH({chave},Mesarios!$F$2:$F$112,0)),"—")')
            vg.cell(i, cs, f'=IFERROR(INDEX(Mesarios!$P$2:$P$112,MATCH({chave},Mesarios!$F$2:$F$112,0)),"{VAGO}")')
            stc.append(f'{get_column_letter(cs)}{i}')
        vg.cell(i, 14, "=" + "+".join(f'({c}="{CONFIRMADO}")' for c in stc))
        vg.cell(i, 15, f"=4-N{i}")
        vg.cell(i, 16, f"=MAX(0,E{i}-N{i})")
        vg.cell(i, 17, f'=IF(G{i}<>"{CONFIRMADO}","Sem Presidente confirmado","")'
                       f'&IF(AND(G{i}<>"{CONFIRMADO}",P{i}>0)," · ","")'
                       f'&IF(P{i}>0,"Faltam "&P{i}&" para a meta","")')
    t = len(urnas) + 2
    vg.cell(t, 2, "Total")
    vg.cell(t, 3, f"=SUM(C2:C{t-1})")
    vg.cell(t, 5, f"=SUM(E2:E{t-1})")
    for k in range(4):
        cs = get_column_letter(7 + 2 * k)
        vg.cell(t, 7 + 2 * k, f'=COUNTIF({cs}2:{cs}{t-1},"{CONFIRMADO}")')
    for col in (14, 15, 16):
        L = get_column_letter(col)
        vg.cell(t, col, f"=SUM({L}2:{L}{t-1})")
    vg.cell(t, 17, f'=COUNTIF(G2:G{t-1},"<>{CONFIRMADO}")&" urnas sem Presidente confirmado"')
    for c in vg[t]:
        c.font = Font(bold=True)
    vg.cell(lin_meta, 1, "Meta das urnas Baixo (premissa, editável):").font = Font(bold=True)
    vg.cell(lin_meta, 3, META_BAIXO).fill = PatternFill("solid", fgColor=AMARELO)
    nota(vg, lin_meta + 1, (
        "Ordem = posição no Ranking (comparecimento efetivo dos BUs de 04/10, arquivo Seções_Atualizadas). "
        "Lotação integral (4) nas urnas de faixa efetiva Alto ou Médio; nas Baixo, a meta da célula C"
        f"{lin_meta}. Status lido de Mesarios!P (Resposta 2º turno): mudou uma resposta lá, esta aba se "
        "atualiza. Confirmado = respondeu SIM no formulário de 2º turno; Não volta = respondeu NÃO; "
        "Sem resposta = designado(a) que não respondeu; VAGO = função sem designado desde o 1º turno."), 17)
    regras_status(vg, f"G2:G{t-1}")
    for k in range(1, 4):
        L = get_column_letter(7 + 2 * k)
        regras_status(vg, f"{L}2:{L}{t-1}")
    regras_faixa(vg, f"A2:B{t-1}", "$D2")
    regras_faixa(vg, f"D2:E{t-1}", "$D2")
    vg.conditional_formatting.add(f"P2:Q{t-1}", FormulaRule(
        formula=["$P2>0"], fill=PatternFill("solid", bgColor=VERMELHO)))

    # --- Funcoes a preencher (lista plana, retrato de 12/10) -------------
    fp = wb.create_sheet("Funções a preencher")
    cabecalho(fp, ["Pos.", "Seção", "Faixa efetiva", "Função", "Prioridade", "Situação",
                   "Designado(a) no 1º turno", "E-mail", "Presença 1º turno", "Ação"],
              [6, 8, 10, 14, 13, 14, 38, 34, 11, 46])
    i = 2
    for u in urnas:
        for f in ORDEM_PRIORIDADE:
            stt = u["status"][f]
            if stt == CONFIRMADO:
                continue
            m = u["grade"].get(f)
            prio = "Necessária" if f in u["necessarias"] else "Desejável"
            acao = {SEM_RESPOSTA: "Contatar o(a) designado(a); se não confirmar, recrutar substituto",
                    NAO_VOLTA: "Recrutar substituto",
                    VAGO: "Recrutar (função sem designado desde o 1º turno)"}[stt]
            vals = [u["posicao"], u["secao"], u["faixa"], f, prio, stt,
                    m["nome"] if m else "—", m["email"] if m else "—", m["presenca_1t"] if m else "—", acao]
            for j, v in enumerate(vals, start=1):
                fp.cell(i, j, v)
            i += 1
    nota(fp, i + 1, (
        f"Retrato de 12/10/2026, gerado por scripts/mesarios_2turno.py — não se atualiza sozinho (a aba "
        f"'Vagas por urna' sim). Prioridade: em cada urna, as funções abertas que faltam para a meta "
        f"({META_INTEGRAL} nas Alto/Médio, {META_BAIXO} nas Baixo) são 'Necessária', na ordem "
        f"{' > '.join(ORDEM_PRIORIDADE)} (premissa); as demais, 'Desejável'."), 10)
    regras_status(fp, f"F2:F{i-1}")
    regras_faixa(fp, f"A2:C{i-1}", "$C2")
    fp.conditional_formatting.add(f"E2:E{i-1}", FormulaRule(
        formula=['$E2="Necessária"'], fill=PatternFill("solid", bgColor=VERMELHO), font=Font(bold=True)))
    fp.auto_filter.ref = f"A1:J{i-1}"

    # --- Respostas 2o turno ---------------------------------------------
    rs = wb.create_sheet("Respostas 2º turno")
    cabecalho(rs, ["ID", "Conclusão", "Nome informado", "Resposta", "Casamento",
                   "Designado(a) correspondente", "Seção", "Função", "Presença 1º turno",
                   "Considerada", "Observação"],
              [6, 17, 36, 10, 18, 38, 8, 14, 11, 11, 52])
    rs.freeze_panes = "D2"
    for i, r in enumerate(respostas, start=2):
        m = r["mesario"]
        vals = [r["id"], r["fim"], r["nome"], r["resposta"], r["casamento"],
                m["nome"] if m else "—", m["secao"] if m else "—", m["funcao"] if m else "—",
                m["presenca_1t"] if m else "—", "Sim" if r["considerada"] else "Não", r["obs"] or None]
        for j, v in enumerate(vals, start=1):
            c = rs.cell(i, j, v)
            if j == 2:
                c.number_format = "dd/mm/yyyy hh:mm"
    fim = len(respostas) + 1
    rs.conditional_formatting.add(f"A2:K{fim}", FormulaRule(
        formula=['$E2="sem correspondência"'], fill=PatternFill("solid", bgColor=VERMELHO)))
    rs.conditional_formatting.add(f"A2:K{fim}", FormulaRule(
        formula=['LEFT($K2,8)="CONFLITO"'], fill=PatternFill("solid", bgColor=AMARELO)))
    rs.conditional_formatting.add(f"A2:K{fim}", FormulaRule(
        formula=['$J2="Não"'], font=Font(color="FF808080", strike=True)))
    nota(rs, fim + 2, (
        "Fonte: formulário 'CONFIRMAÇÃO DE PARTICIPAÇÃO (MESÁRIOS) — SEGUNDO TURNO DAS ELEIÇÕES DE 2026 "
        "EM DUBLIN', respostas 1–75 (anônimo: só o nome digitado). Casamento 'exato' = mesmo nome sem "
        "acento/caixa; 'equivalência' = nome parcial ou com erro, conferido à mão (tabela EQUIVALENCIAS do "
        "script). Quem respondeu mais de uma vez: vale a última resposta."), 11)

    # --- Resumo 2o turno -------------------------------------------------
    rz = wb.create_sheet("Resumo 2º turno", 0)
    rz.column_dimensions["A"].width = 62
    rz.column_dimensions["B"].width = 16
    rz.column_dimensions["C"].width = 70
    linhas_rz = [
        ("Mesários — 2º turno 25/10/2026 · RDS Hall 2 · consolidação de 12/10/2026", None, None),
        (None, None, None),
        ("Formulário de confirmação", None, None),
        ("Respostas recebidas", n["respostas"], f"IDs 1–75; ausentes no export: {', '.join(map(str, n['ids_faltando']))}"),
        ("  SIM", n["resp_sim"], None),
        ("  NÃO", n["resp_nao"], None),
        ("Casadas por nome exato", n["exato"], None),
        ("Casadas por equivalência (nome parcial/erro)", n["equiv"], "conferidas à mão; ver aba 'Respostas 2º turno'"),
        ("Sem correspondência na lista de 111", len(n["sem_corresp"]),
         "; ".join(f"{r['nome']} ({r['resposta']}, ID {r['id']})" for r in n["sem_corresp"]) + " — revisão manual"),
        ("Pessoas que responderam mais de uma vez", len(n["duplicados"]),
         ", ".join(m["nome"] for m in n["duplicados"])),
        ("  com respostas conflitantes (vale a última)", len(n["conflitos"]),
         ", ".join(m["nome"] for m in n["conflitos"])),
        (None, None, None),
        ("Designados do 1º turno (lista Elo, 111)", None, None),
        ("Confirmados para o 2º turno", f'=COUNTIF(Mesarios!$P$2:$P$112,"{CONFIRMADO}")', None),
        ("Não voltam", f'=COUNTIF(Mesarios!$P$2:$P$112,"{NAO_VOLTA}")', None),
        ("Sem resposta", f'=COUNTIF(Mesarios!$P$2:$P$112,"{SEM_RESPOSTA}")',
         f"{n['sr_presentes']} deles estiveram presentes no 1º turno — contatar primeiro"),
        ("Conferência: soma = 111", "=IF(B14+B15+B16=COUNTA(Mesarios!D2:D112),\"OK\",\"ERRO\")", None),
        ("Confirmados que estiveram presentes no 1º turno",
         f'=COUNTIFS(Mesarios!$P$2:$P$112,"{CONFIRMADO}",Mesarios!$M$2:$M$112,"SIM")', None),
        ("Confirmados que foram AUSENTES no 1º turno",
         f'=COUNTIFS(Mesarios!$P$2:$P$112,"{CONFIRMADO}",Mesarios!$M$2:$M$112,"NAO")',
         ", ".join(m["nome"] for m in n["conf_ausentes"])),
        (None, None, None),
        ("Funções (28 urnas × 4)", None, None),
        ("Funções totais", 112, f"{n['vagos']} sem designado desde o 1º turno (3862, 2º Mesário)"),
        ("Preenchidas (confirmados)", "='Vagas por urna'!N30", None),
        ("Abertas", "='Vagas por urna'!O30", None),
        ("Meta (Alto/Médio = 4, Baixo = meta editável)", "='Vagas por urna'!E30",
         f"{len(n['integ'])} urnas de lotação integral: " + ", ".join(str(u['secao']) for u in n['integ'])),
        ("Déficit vs meta (funções a preencher no mínimo)", "='Vagas por urna'!P30",
         f"no retrato de 12/10: {n['deficit_integ']} nas prioritárias + {n['deficit_baixo']} nas Baixo; "
         f"{n['deficit_contato']} são de designado sem resposta, {n['deficit_recruta']} exigem substituto"),
        ("Urnas sem Presidente confirmado", f'=COUNTIF(\'Vagas por urna\'!G2:G29,"<>{CONFIRMADO}")', None),
        ("Urnas com as 4 funções confirmadas", "=COUNTIF('Vagas por urna'!N2:N29,4)",
         ", ".join(str(u["secao"]) for u in n["completas"])),
        (None, None, None),
        ("Nota", None,
         "Fontes: (1) 2026.10.12_Mesários_Seções_Atualizadas — só 'Por secao' M–W (BUs de 04/10) e "
         "'Ranking'; (2) 2026.10.12_Mesários_Comparecimento confirmado — 'Resumo' (agora 'Resumo 1º "
         "turno'), 'Mesarios', 'Presenca por secao', 'Por secao' A–L, 'Boletins', 'Divergências', 'Fora "
         "da lista'; (3) formulário de confirmação do 2º turno, respostas 1–75. A meta 3 nas urnas Baixo "
         "e a ordem de prioridade das funções são premissas operacionais, não regra legal. Thalison "
         "Miquilini Motta (aba 'Fora da lista') atuou em 3322 sem estar na lista e não respondeu ao "
         "formulário — possível reforço."),
    ]
    for i, (a, b, c) in enumerate(linhas_rz, start=1):
        rz.cell(i, 1, a)
        rz.cell(i, 2, b)
        rz.cell(i, 3, c)
        rz.cell(i, 3).alignment = Alignment(wrap_text=True, vertical="top")
        rz.cell(i, 2).alignment = Alignment(horizontal="right", vertical="top")
        if a and b is None and c is None:
            rz.cell(i, 1).font = Font(bold=True, color=AZUL, size=12 if i > 1 else 13)
    rz.row_dimensions[len(linhas_rz)].height = 130
    rz.cell(len(linhas_rz), 1).alignment = Alignment(vertical="top")

    # Ordem das abas
    ordem = ["Resumo 2º turno", "Vagas por urna", "Funções a preencher", "Respostas 2º turno",
             "Mesarios", "Por secao", "Ranking", "Presenca por secao", "Resumo 1º turno",
             "Boletins", "Divergências", "Fora da lista"]
    wb._sheets = [wb[t] for t in ordem]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_view.tabSelected = ws.title == ordem[0]
    wb.calculation.fullCalcOnLoad = True
    wb.save(ARQ_SAIDA)
    print(f"\ngravado: {os.path.relpath(ARQ_SAIDA, RAIZ)}")


def main():
    mesarios, efetivo, ranking, respostas, s1, s2, tot = le()
    cruza(mesarios, respostas)
    urnas = monta_urnas(mesarios, efetivo)
    n = numeros(mesarios, respostas, urnas)
    relatorio(n, urnas)
    falhas = confere(mesarios, efetivo, ranking, respostas, urnas, s1, s2, tot)
    print("\nConferências: " + ("OK" if not falhas else "FALHARAM"))
    for f in falhas:
        print("  ✗ " + f)
    if falhas:
        sys.exit(1)
    if "--grava" in sys.argv:
        grava(mesarios, respostas, urnas, n)


if __name__ == "__main__":
    main()
