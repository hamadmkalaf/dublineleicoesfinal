"""Converte a planilha de voluntários (Nome, Pronome, E-mail, Local de trabalho) em JSON
para scripts/gera_carta_docx.js. Uso: python3 scripts/xlsx_para_json.py planilha.xlsx saida.json
Não grave a saída no repositório: contém dados pessoais."""
import json, re, sys, openpyxl

POSS = {"he/his": "his", "she/her": "her", "they/their": "their"}
def limpa(s): return re.sub(r"\s+", " ", str(s or "").replace("\xa0", " ")).strip()
def empregadores(s):
    partes = re.split(r",\s+|\s+e\s+", limpa(s).rstrip(".").strip())
    return [p.strip() for p in partes if p.strip()]

ws = openpyxl.load_workbook(sys.argv[1]).active
saida = []
for nome, pron, email, local in list(ws.iter_rows(values_only=True))[1:]:
    if not limpa(nome): continue
    chave = limpa(pron).lower()
    if chave not in POSS: sys.exit(f"Pronome não reconhecido para {limpa(nome)}: {pron!r}")
    saida.append({"nome": limpa(nome), "pronome_poss": POSS[chave], "email": limpa(email),
                  "empresas": empregadores(local)})
json.dump(saida, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(saida), "voluntários")
