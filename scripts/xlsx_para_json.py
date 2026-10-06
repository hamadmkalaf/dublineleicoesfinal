"""Converte a planilha de voluntários (Nome, Pronome, E-mail, Local de trabalho) em JSON
para scripts/gera_carta_docx.js. Uso: python3 scripts/xlsx_para_json.py planilha.xlsx saida.json [--separar "Nome"]... [--pronome "Nome=he/his"]...
  --separar: uma carta por empregador para essa pessoa; --pronome: corrige o pronome da planilha.
Não grave a saída no repositório: contém dados pessoais."""
import json, re, sys, openpyxl

POSS = {"he/his": "his", "she/her": "her", "they/their": "their"}
def limpa(s): return re.sub(r"\s+", " ", str(s or "").replace("\xa0", " ")).strip()
def empregadores(s):
    partes = re.split(r",\s+|\s+e\s+", limpa(s).rstrip(".").strip())
    return [p.strip() for p in partes if p.strip()]

args = sys.argv[3:]
def opcoes(flag): return [args[i + 1] for i, a in enumerate(args) if a == flag]
separar = {limpa(n) for n in opcoes("--separar")}
corrige = dict(o.split("=", 1) for o in opcoes("--pronome"))
corrige = {limpa(k): v for k, v in corrige.items()}
ws = openpyxl.load_workbook(sys.argv[1]).active
saida = []
for nome, pron, email, local in list(ws.iter_rows(values_only=True))[1:]:
    if not limpa(nome): continue
    chave = corrige.get(limpa(nome), limpa(pron)).lower()
    if chave not in POSS: sys.exit(f"Pronome não reconhecido para {limpa(nome)}: {pron!r}")
    saida.append({"nome": limpa(nome), "pronome_poss": POSS[chave], "email": limpa(email),
                  "empresas": empregadores(local),
                  "uma_carta_por_empresa": limpa(nome) in separar})
json.dump(saida, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(saida), "voluntários")
