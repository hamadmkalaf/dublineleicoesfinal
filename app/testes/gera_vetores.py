"""Gera app/testes/vetores_nome.json: casos de normalização e hash calculados em Python,
que o teste em JavaScript (normaliza.test.mjs) tem de reproduzir byte a byte."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from app_normaliza import chaves_nome, hash_publico, normaliza_data, normaliza_nome

NOMES = [
    "Ana Cristina Evaristo", "LETÍCIA GONÇALVES DE LIMA", "Tizzani Viana D'Andrea Nery", "josé  da   silva",
    "Maria das Dores e Souza", "João Müller-Schmidt", "Ângela Ção", "O'Brien, Séamus", "MARIA APARECIDA SILVA",
    "Thomas Mailleux Sant Ana", "  Pedro   ", "de la Cruz", "Zoë Dâmaso", "Luís Inácio", "X Æ A-12",
    "Katia Cirlene Pereira de Brito Falcao", "Ñandu Peña", "François D’Alembert", "", "E",
]
DATAS = ["1967-10-23", "23/10/1967", "1967-10-23T00:00:00", "23.10.1967", "23101967", "1967-13-01", "31/02/1990", "", "abc"]
vetores = {
    "nomes": [{"entrada": n, "normalizado": normaliza_nome(n), "chaves": chaves_nome(n)} for n in NOMES],
    "datas": [{"entrada": d, "normalizada": normaliza_data(d)} for d in DATAS],
    "hashes": [{"chave": normaliza_nome(n), "fator": "1975-03-16", "hash": hash_publico(normaliza_nome(n), "1975-03-16")} for n in NOMES[:5]],
}
Path(__file__).with_name("vetores_nome.json").write_text(json.dumps(vetores, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(NOMES)} nomes, {len(DATAS)} datas, {len(vetores['hashes'])} hashes")
