"""Importa a lista nominal de eleitores (.pdf do TRE, .xlsx ou .csv) para o CSV canônico do app.

    python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf"          # confere
    python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf" --grava  # escreve data/eleitores/eleitores.csv
    python3 scripts/app_importar_eleitores.py lista.xlsx --local 1015                                 # planilha, filtrando um posto

Saída canônica (UTF-8, separador ';'):
    NUM_INSCRICAO;NOM_ELEITOR;DAT_NASC;NUM_SECAO;NOM_MAE;NUM_LOCAL;TURNO1;TURNO2
Esse CSV contém dados pessoais: fica em data/eleitores/, que está no .gitignore. Nunca commitar.

A lista real (TRE-DF, "Relação de eleitores por local de votação", 29/09/2026) é um PDF com
texto: SEÇÃO · INSCRIÇÃO · NOME DO ELEITOR · 1º TURNO · 2º TURNO, sem data de nascimento nem
nome da mãe. A seção é a da MESA (principal), não a seção original: as agregadas já vêm somadas.
O PDF é lido com `pdftotext -layout` (poppler-utils); nomes longos quebram em duas linhas, uma
antes e outra depois da linha do registro, e o leitor junta as duas.

O importador reconhece colunas pelo nome em planilhas, normaliza datas e zeros à esquerda e
confere a contagem contra saidas/dados.json: por seção original quando a lista vem assim, por
mesa (principal + agregada, de data/decisoes.json) quando vem por mesa. Sai com código 1 se a
contagem não bater, se houver seção que não é de Dublin ou se faltar coluna obrigatória.
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app_normaliza import normaliza_data, normaliza_inscricao, normaliza_nome, normaliza_secao  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "saidas" / "dados.json"
DECISOES = RAIZ / "data" / "decisoes.json"
DESTINO = RAIZ / "data" / "eleitores" / "eleitores.csv"

# nome canônico -> nomes aceitos no cabeçalho (comparados já normalizados: maiúsculas, sem acento, sem pontuação)
COLUNAS = {
    "NUM_INSCRICAO": ["NUM INSCRICAO", "NR INSCRICAO", "INSCRICAO", "NR TITULO", "TITULO", "TITULO DE ELEITOR", "NUMERO DO TITULO", "NR TITULO ELEITOR"],
    "NOM_ELEITOR": ["NOM ELEITOR", "NM ELEITOR", "NOME", "NOME DO ELEITOR", "ELEITOR", "NOME ELEITOR"],
    "DAT_NASC": ["DAT NASC", "DT NASCIMENTO", "DATA DE NASCIMENTO", "NASCIMENTO", "DT NASC", "DATA NASC", "DATA NASCIMENTO"],
    "NUM_SECAO": ["NUM SECAO", "NR SECAO", "SECAO", "SECAO ELEITORAL", "N SECAO", "NO SECAO"],
    "NOM_MAE": ["NOM MAE", "NM MAE", "NOME DA MAE", "MAE", "NOME MAE"],
    "NUM_LOCAL": ["NUM LOCAL", "NR LOCAL", "LOCAL", "NR LOCAL VOTACAO", "LOCAL DE VOTACAO", "NUM LOCAL VOTACAO"],
    "TURNO1": ["TURNO1", "1 TURNO", "1O TURNO", "PRIMEIRO TURNO"],
    "TURNO2": ["TURNO2", "2 TURNO", "2O TURNO", "SEGUNDO TURNO"],
}
OBRIGATORIAS = ["NUM_INSCRICAO", "NOM_ELEITOR", "NUM_SECAO"]
SAIDA = ["NUM_INSCRICAO", "NOM_ELEITOR", "DAT_NASC", "NUM_SECAO", "NOM_MAE", "NUM_LOCAL", "TURNO1", "TURNO2"]


def chave_cabecalho(texto):
    return normaliza_nome(str(texto or "").replace("_", " "))


def mapeia_colunas(cabecalho):
    """Índice de cada coluna canônica no cabeçalho lido, ou None se não houver."""
    normalizado = [chave_cabecalho(c) for c in cabecalho]
    mapa = {}
    for canonica, aceitos in COLUNAS.items():
        aceitos_n = [chave_cabecalho(a) for a in aceitos]
        idx = next((i for i, c in enumerate(normalizado) if c in aceitos_n), None)
        mapa[canonica] = idx
    return mapa


def acha_cabecalho(linhas):
    """Primeira linha que contenha pelo menos as colunas obrigatórias."""
    for i, linha in enumerate(linhas[:50]):
        mapa = mapeia_colunas(linha)
        if all(mapa[c] is not None for c in OBRIGATORIAS):
            return i, mapa
    return None, None


# ---------- leitores por formato: devolvem lista de linhas (listas de células) ----------

def le_xlsx(caminho, planilha=None):
    import openpyxl

    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    folhas = [wb[planilha]] if planilha else wb.worksheets
    for ws in folhas:
        linhas = [list(r) for r in ws.iter_rows(values_only=True)]
        i, mapa = acha_cabecalho(linhas)
        if i is not None:
            print(f"planilha '{ws.title}': cabeçalho na linha {i + 1}")
            return linhas
    raise SystemExit("nenhuma planilha tem as colunas obrigatórias (inscrição, nome, seção)")


def le_csv(caminho):
    bruto = Path(caminho).read_bytes()
    for enc in ("utf-8-sig", "latin-1"):
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    sep = ";" if texto[:4096].count(";") >= texto[:4096].count(",") else ","
    return [row for row in csv.reader(texto.splitlines(), delimiter=sep)]


# ---------- PDF do TRE: "Relação de eleitores por local de votação" ----------

REGISTRO_TRE = re.compile(r"^\s*(\d{4})\s+(\d{12})(?:\s+(.*?))?\s*$")
MARCAS_TURNO = {"OK", "VT", "NAO", "NÃO", "X", "-", "--"}
CABECALHOS_TRE = ("TRIBUNAL", "ELEIÇÕES", "ELEICOES", "DOCUMENTO OFICIAL", "SEÇÃO", "SECAO", "LOCAL ", "RELAÇÃO", "RELACAO", "PAÍS", "PAIS")


def texto_do_pdf(caminho):
    """Texto com layout preservado, via pdftotext (poppler-utils)."""
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext não está instalado (pacote poppler-utils); instale-o ou peça a lista em .xlsx/.csv")
    r = subprocess.run(["pdftotext", "-layout", str(caminho), "-"], capture_output=True, check=True)
    texto = r.stdout.decode("utf-8", errors="replace")
    if not texto.strip():
        raise SystemExit("o PDF não tem texto extraível (parece escaneado): peça a lista em .xlsx ou .csv ao Cartório")
    return texto


def parse_texto_tre(texto):
    """Linhas de texto do pdftotext -> registros [SEÇÃO, INSCRIÇÃO, NOME, TURNO1, TURNO2].

    Cada registro é um bloco separado por linha em branco. Nome curto fica na linha do
    registro, entre a inscrição e as marcas de turno. Nome longo quebra: a primeira parte
    vem na linha ANTERIOR e a segunda na linha POSTERIOR do mesmo bloco, e a linha do
    registro fica sem nome. Linhas de cabeçalho e rodapé de página são ignoradas.
    """
    def cabecalho(l):
        u = l.strip().upper()
        return not u or any(u.startswith(c) for c in CABECALHOS_TRE)

    blocos, atual = [], []
    for l in texto.splitlines():
        if l.strip() == "":
            if atual:
                blocos.append(atual)
                atual = []
        else:
            atual.append(l)
    if atual:
        blocos.append(atual)

    registros = []
    for bloco in blocos:
        linhas = [l for l in bloco if not cabecalho(l)]
        idx = next((i for i, l in enumerate(linhas) if REGISTRO_TRE.match(l)), None)
        if idx is None:
            continue
        secao, insc, resto = REGISTRO_TRE.match(linhas[idx]).groups()
        tokens = (resto or "").split()
        marcas = []
        while tokens and tokens[-1].upper() in MARCAS_TURNO and len(marcas) < 2:
            marcas.insert(0, tokens.pop().upper())
        nome = " ".join(tokens)
        if not nome:
            antes = " ".join(l.strip() for l in linhas[:idx])
            depois = " ".join(l.strip() for l in linhas[idx + 1:])
            nome = f"{antes} {depois}".strip()
        t1 = marcas[0] if len(marcas) >= 1 else ""
        t2 = marcas[1] if len(marcas) == 2 else ""
        registros.append([secao, insc, nome, t1, t2])
    return registros


def le_pdf(caminho):
    registros = parse_texto_tre(texto_do_pdf(caminho))
    if not registros:
        raise SystemExit("nenhum registro SEÇÃO/INSCRIÇÃO/NOME reconhecido no PDF: o layout não é o da relação do TRE")
    sem_nome = sum(1 for r in registros if not r[2])
    if sem_nome:
        raise SystemExit(f"{sem_nome} registros sem nome no PDF: confira a extração")
    print(f"PDF do TRE: {len(registros)} registros")
    return [["NUM_SECAO", "NUM_INSCRICAO", "NOM_ELEITOR", "TURNO1", "TURNO2"]] + registros


def le(caminho, planilha=None):
    ext = Path(caminho).suffix.lower()
    if ext in (".xlsx", ".xlsm"):
        return le_xlsx(caminho, planilha)
    if ext in (".csv", ".txt", ".tsv"):
        return le_csv(caminho)
    if ext == ".pdf":
        return le_pdf(caminho)
    raise SystemExit(f"formato não reconhecido: {ext}")


# ---------- normalização e conferência ----------

def converte(linhas, local=None):
    i, mapa = acha_cabecalho(linhas)
    if i is None:
        raise SystemExit("não achei o cabeçalho com inscrição, nome e seção")
    faltam = [c for c in OBRIGATORIAS if mapa[c] is None]
    if faltam:
        raise SystemExit(f"faltam colunas obrigatórias: {faltam}")
    achadas = {c: (linhas[i][idx] if idx is not None else None) for c, idx in mapa.items()}
    print("colunas:", " · ".join(f"{c} ← {v!r}" for c, v in achadas.items() if v is not None))
    for c in ("DAT_NASC", "NOM_MAE"):
        if mapa[c] is None:
            print(f"aviso: sem coluna {c}")

    def cel(row, c):
        idx = mapa[c]
        return row[idx] if idx is not None and idx < len(row) else ""

    saida, vazias, filtradas, sem_nasc, sem_insc = [], 0, 0, 0, 0
    for row in linhas[i + 1:]:
        nome = normaliza_nome(cel(row, "NOM_ELEITOR"))
        if not nome:
            vazias += 1
            continue
        num_local = re.sub(r"\D", "", str(cel(row, "NUM_LOCAL") or ""))
        if local and num_local and num_local.lstrip("0") != str(local).lstrip("0"):
            filtradas += 1
            continue
        nasc = normaliza_data(cel(row, "DAT_NASC"))
        insc = normaliza_inscricao(cel(row, "NUM_INSCRICAO"))
        sem_nasc += not nasc
        sem_insc += not insc
        saida.append({
            "NUM_INSCRICAO": insc,
            "NOM_ELEITOR": str(cel(row, "NOM_ELEITOR")).strip(),
            "DAT_NASC": nasc,
            "NUM_SECAO": normaliza_secao(cel(row, "NUM_SECAO")),
            "NOM_MAE": str(cel(row, "NOM_MAE") or "").strip(),
            "NUM_LOCAL": num_local,
            "TURNO1": str(cel(row, "TURNO1") or "").strip().upper(),
            "TURNO2": str(cel(row, "TURNO2") or "").strip().upper(),
        })
    print(f"linhas: {len(saida)} eleitores · {vazias} vazias · {filtradas} de outros postos"
          + (f" · {sem_nasc} sem nascimento" if sem_nasc else "") + (f" · {sem_insc} sem inscrição" if sem_insc else ""))
    marcas = Counter((e["TURNO1"], e["TURNO2"]) for e in saida)
    if any(k != ("", "") for k in marcas):
        print("marcas de turno (1º/2º): " + " · ".join(f"{a or '?'}/{b or '?'} {n}" for (a, b), n in marcas.most_common()))
    return saida


def confere(saida):
    dados = json.loads(DADOS.read_text(encoding="utf-8"))
    dec = json.loads(DECISOES.read_text(encoding="utf-8"))
    aptos = {normaliza_secao(s["Secao"]): s["Eleitores"] for s in dados["secoes"]}
    mesas = {normaliza_secao(m["principal"]): m for m in dec["mesas"]}
    agregadas = {normaliza_secao(m["agregada"]) for m in dec["mesas"] if m.get("agregada")}
    por_secao = Counter(e["NUM_SECAO"] for e in saida)
    erros = []
    estranhas = {s: n for s, n in por_secao.items() if s not in aptos}
    if estranhas:
        erros.append(f"seções que não são de Dublin: {estranhas}")
    dup = [t for t, n in Counter(e["NUM_INSCRICAO"] for e in saida if e["NUM_INSCRICAO"]).items() if n > 1]
    if dup:
        erros.append(f"{len(dup)} inscrições repetidas (ex.: {dup[:3]})")

    # A lista vem por MESA (só seções principais, agregadas já somadas) ou por SEÇÃO original?
    por_mesa = not any(por_secao.get(s) for s in agregadas)
    if por_mesa:
        print("lista por mesa: só as seções principais aparecem; as agregadas já estão somadas")
        print(f"{'mesa':>5} {'seção':>6} {'agreg.':>6} {'lista':>6} {'aptos':>6}  desvio")
        desvios = 0
        for s in sorted(mesas):
            m = mesas[s]
            n, a = por_secao.get(s, 0), m["aptos"]
            d = (n - a) / a if a else 0
            marca = "  <-- confira" if n != a else ""
            desvios += bool(marca)
            ag = normaliza_secao(m["agregada"]) if m.get("agregada") else "-"
            print(f"{m['mrv']:>5} {s:>6} {ag:>6} {n:>6} {a:>6} {d:+7.1%}{marca}")
        total_aptos = sum(m["aptos"] for m in mesas.values())
        print(f"total {len(saida)} na lista · {total_aptos} aptos nas 28 mesas · {desvios} mesas com desvio")
        if desvios:
            erros.append(f"{desvios} mesas com contagem diferente de decisoes.json")
    else:
        print(f"{'seção':>6} {'lista':>6} {'aptos':>6}  desvio")
        desvios = 0
        for s in sorted(aptos):
            n, a = por_secao.get(s, 0), aptos[s]
            d = (n - a) / a if a else 0
            marca = "  <-- confira" if abs(d) > 0.02 else ""
            desvios += bool(marca)
            print(f"{s:>6} {n:>6} {a:>6} {d:+7.1%}{marca}")
        print(f"total {len(saida)} na lista · {sum(aptos.values())} aptos em dados.json · {desvios} seções com desvio > 2%")
    return erros


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo", type=Path)
    ap.add_argument("--planilha", help="nome da aba, no .xlsx (padrão: a primeira com as colunas)")
    ap.add_argument("--local", help="manter só este NUM_LOCAL (ex.: 1015)")
    ap.add_argument("--grava", action="store_true", help=f"escrever {DESTINO.relative_to(RAIZ)}")
    ap.add_argument("--destino", type=Path, default=DESTINO)
    ap.add_argument("--sem-conferencia", action="store_true", help="não comparar com saidas/dados.json (listas de outro posto)")
    args = ap.parse_args()

    linhas = le(args.arquivo, args.planilha)
    saida = converte(linhas, args.local)
    erros = [] if args.sem_conferencia else confere(saida)
    for e in erros:
        print("ERRO:", e)
    if erros:
        sys.exit(1)
    if not args.grava:
        print("conferência ok; nada gravado (use --grava)")
        return
    args.destino.parent.mkdir(parents=True, exist_ok=True)
    with open(args.destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SAIDA, delimiter=";")
        w.writeheader()
        w.writerows(saida)
    print(f"gravado: {args.destino} ({len(saida)} eleitores). Este arquivo tem dados pessoais e não entra no git.")


if __name__ == "__main__":
    main()
