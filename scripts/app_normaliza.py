"""Normalização de nomes, datas e chaves de busca do app "Onde eu voto?".

Este módulo é a referência: `app/public/comum.js` reimplementa as mesmas regras em
JavaScript, e `app/testes/test_normaliza.py` confere que os dois produzem os mesmos
resultados sobre `app/testes/vetores_nome.json`. Mudou aqui, mude lá.

Regras do nome:
  1. decompõe acentos (NFKD) e descarta as marcas combinantes;
  2. maiúsculas; apóstrofos somem sem deixar espaço (D'ANDREA -> DANDREA);
  3. qualquer outro caractere que não seja letra ou dígito vira espaço;
  4. espaços múltiplos viram um só; remove as partículas DE DA DO DOS DAS E.

Chaves indexadas por eleitor: o nome completo normalizado e, quando há três ou mais
palavras, "primeiro último", para tolerar quem omite os nomes do meio.
"""

import base64
import hashlib
import re
import unicodedata
from datetime import date, datetime

PARTICULAS = {"DE", "DA", "DO", "DOS", "DAS", "E"}
APOSTROFOS = "'’`´"

# Sal público e fixo do índice do eleitor. É público por desenho: a proteção vem do
# custo do PBKDF2 (ITERACOES_PUBLICO por tentativa), não do segredo do sal.
SAL_PUBLICO = b"dublin-2026-onde-eu-voto"
ITERACOES_PUBLICO = 50_000
TAMANHO_HASH = 12  # bytes (96 bits) — colisão desprezível para 17 mil chaves


def normaliza_nome(texto):
    """Nome como digitado -> forma canônica em maiúsculas, sem acento nem partículas."""
    if texto is None:
        return ""
    s = unicodedata.normalize("NFKD", str(texto))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.upper()
    for a in APOSTROFOS:
        s = s.replace(a, "")
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    palavras = [p for p in s.split() if p not in PARTICULAS]
    return " ".join(palavras)


def chaves_nome(texto):
    """Lista de chaves a indexar para um nome: completa e, se couber, primeiro+último."""
    completo = normaliza_nome(texto)
    if not completo:
        return []
    chaves = [completo]
    partes = completo.split(" ")
    if len(partes) >= 3:
        curta = f"{partes[0]} {partes[-1]}"
        if curta != completo:
            chaves.append(curta)
    return chaves


def normaliza_data(valor):
    """Data em qualquer forma usual -> 'AAAA-MM-DD'. Devolve '' se não reconhecer."""
    if valor is None or valor == "":
        return ""
    if isinstance(valor, datetime):
        return valor.date().isoformat()
    if isinstance(valor, date):
        return valor.isoformat()
    s = str(valor).strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        a, me, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})", s)
        if not m:
            m = re.match(r"^(\d{2})(\d{2})(\d{4})$", s)
            if not m:
                return ""
        d, me, a = m.groups()
    try:
        return date(int(a), int(me), int(d)).isoformat()
    except ValueError:
        return ""


def normaliza_secao(valor):
    """Seção como vier (int, '511', '0511', '3313.0') -> 4 dígitos com zeros à esquerda."""
    if valor is None or valor == "":
        return ""
    s = re.sub(r"\.0+$", "", str(valor).strip())
    digitos = re.sub(r"\D", "", s)
    if not digitos:
        return ""
    return digitos.zfill(4)


def normaliza_inscricao(valor):
    """Título de eleitor -> 12 dígitos (a planilha do TSE perde os zeros à esquerda)."""
    if valor is None or valor == "":
        return ""
    digitos = re.sub(r"\D", "", re.sub(r"\.0+$", "", str(valor).strip()))
    return digitos.zfill(12) if digitos else ""


def hash_publico(chave_nome, segundo_fator=""):
    """Hash indexado no arquivo público: PBKDF2-SHA256 truncado.

    Material: só a chave do nome (consulta por nome, desenho de 01/10/2026) ou
    'CHAVE|FATOR' quando há um fator de desempate — o título de 12 dígitos, no caso de
    homônimos. O título nunca aparece em claro no índice: só dentro do hash.
    """
    material = (f"{chave_nome}|{segundo_fator}" if segundo_fator else chave_nome).encode("utf-8")
    dk = hashlib.pbkdf2_hmac("sha256", material, SAL_PUBLICO, ITERACOES_PUBLICO, TAMANHO_HASH)
    return base64.urlsafe_b64encode(dk).decode("ascii").rstrip("=")


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(repr(arg), "->", normaliza_nome(arg), chaves_nome(arg))
