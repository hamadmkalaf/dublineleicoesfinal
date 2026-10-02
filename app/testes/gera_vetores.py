"""Gera app/testes/vetores_nome.json: casos de normalização e hash calculados em Python,
que o teste em JavaScript (normaliza.test.mjs) tem de reproduzir byte a byte."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from app_normaliza import chaves_nome, hash_publico, normaliza_data, normaliza_inscricao, normaliza_nome, titulo_parcial

NOMES = [
    "Ana Cristina Evaristo", "LETÍCIA GONÇALVES DE LIMA", "Tizzani Viana D'Andrea Nery", "josé  da   silva",
    "Maria das Dores e Souza", "João Müller-Schmidt", "Ângela Ção", "O'Brien, Séamus", "MARIA APARECIDA SILVA",
    "Thomas Mailleux Sant Ana", "  Pedro   ", "de la Cruz", "Zoë Dâmaso", "Luís Inácio", "X Æ A-12",
    "Katia Cirlene Pereira de Brito Falcao", "Ñandu Peña", "François D’Alembert", "", "E",
    "ALYSSON HENRIQUE DE CAMPOS FORNERO ABREU DE LIMA", "ERIKA MARIA PIRAGIBE DE ALMEIDA E CAMPOS MAIA",
    # 02/10: sinais do português, com e sem acento, têm de cair na MESMA chave (til, cedilha, agudo, circunflexo,
    # grave, trema, ordinal, apóstrofo curvo), em maiúsculas e minúsculas, e também já decompostos (NFD)
    "Conceição Gonçalves Assunção", "CONCEICAO GONCALVES ASSUNCAO", "conceição gonçalves assunção",
    "José Antônio Araújo Côrtes", "JOSE ANTONIO ARAUJO CORTES", "Luís Ângelo Müller Peña", "LUIS ANGELO MULLER PENA",
    "Thaís Raíssa Jaçanã", "THAIS RAISSA JACANA", "Sebastião Façanha D’Ávila", "SEBASTIAO FACANHA DAVILA",
    "Mª da Conceição Sant'Ana", "ma conceicao santana", "Ágata Übel-Çek", "AGATA UBEL CEK",
    "João Gonçalves",  # "João Gonçalves" em NFD (como alguns teclados mandam)
    "JOAO GONCALVES",
]
DATAS = ["1967-10-23", "23/10/1967", "1967-10-23T00:00:00", "23.10.1967", "23101967", "1967-13-01", "31/02/1990", "", "abc"]
TITULOS = ["123456789012", "1234 5678 9012", "1234.5678.9012", "5301982801", 5301982801, "0000 0000 0001", "", None]
vetores = {
    "nomes": [{"entrada": n, "normalizado": normaliza_nome(n), "chaves": chaves_nome(n)} for n in NOMES],
    "datas": [{"entrada": d, "normalizada": normaliza_data(d)} for d in DATAS],
    "titulos": [{"entrada": t, "normalizado": normaliza_inscricao(t), "parcial": titulo_parcial(t)} for t in TITULOS],
    # hash só do nome (consulta normal) e nome|título (desempate de homônimos)
    "hashes": [{"chave": normaliza_nome(n), "fator": "", "hash": hash_publico(normaliza_nome(n))} for n in NOMES[:4]]
            + [{"chave": normaliza_nome(n), "fator": "5678", "hash": hash_publico(normaliza_nome(n), "5678")} for n in NOMES[:3]],
}
Path(__file__).with_name("vetores_nome.json").write_text(json.dumps(vetores, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(NOMES)} nomes, {len(DATAS)} datas, {len(TITULOS)} títulos, {len(vetores['hashes'])} hashes")
