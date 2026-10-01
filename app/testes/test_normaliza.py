"""pytest: regras de normalização, leitor do PDF do TRE e conferência do build (python3 -m pytest app/testes)."""
import json, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from app_normaliza import chaves_nome, hash_publico, normaliza_data, normaliza_inscricao, normaliza_nome, normaliza_secao, titulo_parcial  # noqa: E402
from app_importar_eleitores import parse_texto_tre  # noqa: E402


def test_nome_sem_acento_apostrofo_particulas():
    assert normaliza_nome("Letícia Gonçalves de Lima") == "LETICIA GONCALVES LIMA"
    assert normaliza_nome("Tizzani Viana D'Andrea Nery") == "TIZZANI VIANA DANDREA NERY"
    assert normaliza_nome("Maria das Dores e Souza") == "MARIA DORES SOUZA"
    assert normaliza_nome("  josé  da   silva ") == "JOSE SILVA"
    assert normaliza_nome(None) == "" and normaliza_nome("de") == ""


def test_chaves_completa_e_curta():
    assert chaves_nome("Ana Cristina Evaristo") == ["ANA CRISTINA EVARISTO", "ANA EVARISTO"]
    assert chaves_nome("Ana Evaristo") == ["ANA EVARISTO"]
    assert chaves_nome("Ana de Evaristo") == ["ANA EVARISTO"]


def test_data_secao_inscricao():
    assert normaliza_data("23/10/1967") == normaliza_data("1967-10-23") == "1967-10-23"
    assert normaliza_data("31/02/1990") == "" and normaliza_data("") == ""
    assert normaliza_secao(511) == "0511" and normaliza_secao("3313.0") == "3313"
    assert normaliza_inscricao(5301982801) == "005301982801"
    assert normaliza_inscricao("1234 5678 9012") == "123456789012"


def test_titulo_parcial_digitos_5_a_8():
    assert titulo_parcial("123456789012") == "5678"
    assert titulo_parcial("1234 5678 9012") == "5678"
    assert titulo_parcial(5301982801) == "0198"       # planilha do TSE sem zeros à esquerda
    assert titulo_parcial("5678") == "5678"            # já parcial
    assert titulo_parcial("12") == "" and titulo_parcial("") == "" and titulo_parcial(None) == ""


def test_hash_so_nome_e_nome_titulo():
    so_nome = hash_publico("MARIA APARECIDA SILVA")
    com_titulo = hash_publico("MARIA APARECIDA SILVA", "111111111111")
    assert so_nome != com_titulo and len(so_nome) == 16
    assert hash_publico("MARIA APARECIDA SILVA", "") == so_nome


TEXTO_TRE = """\
                                 TRIBUNAL REGIONAL ELEITORAL DO DISTRITO FEDERAL
                                                  ELEIÇÕES 2026 - EXTERIOR

 Local 1: ROYAL DUBLIN SOCIETY - HALL 2 (16794 eleitores alocados)
  SEÇÃO              INSCRIÇÃO             NOME DO ELEITOR                            1º TURNO     2º TURNO

    0511            212451310167           ADALBERTO SALLES MOLLICA                     OK             OK

                                           ALYSSON HENRIQUE DE CAMPOS FORNERO ABREU
    0511            102366140540                                                        OK             OK
                                           DE LIMA

    0513            107990870531           THAIS SANTANA DA SILVA                          VT              VT

    0513            063878561392           CHRISTOPHER DINIZ LIMA E SILVA            OK              VT

Documento oficial gerado em 29/09/2026 às 18:14                                    Página 1 de 470
                                 TRIBUNAL REGIONAL ELEITORAL DO DISTRITO FEDERAL
                                                  ELEIÇÕES 2026 - EXTERIOR

  SEÇÃO              INSCRIÇÃO             NOME DO ELEITOR                           1º TURNO      2º TURNO

    3862            146139720302           YURI GONCALVES CERQUEIRA CHAVES           OK           OK
"""


def test_leitor_pdf_tre():
    regs = parse_texto_tre(TEXTO_TRE)
    assert regs == [
        ["0511", "212451310167", "ADALBERTO SALLES MOLLICA", "OK", "OK"],
        ["0511", "102366140540", "ALYSSON HENRIQUE DE CAMPOS FORNERO ABREU DE LIMA", "OK", "OK"],
        ["0513", "107990870531", "THAIS SANTANA DA SILVA", "VT", "VT"],
        ["0513", "063878561392", "CHRISTOPHER DINIZ LIMA E SILVA", "OK", "VT"],
        ["3862", "146139720302", "YURI GONCALVES CERQUEIRA CHAVES", "OK", "OK"],
    ]


def test_vetores_js_iguais():
    subprocess.run([sys.executable, str(RAIZ / "app/testes/gera_vetores.py")], check=True)
    subprocess.run(["node", str(RAIZ / "app/testes/normaliza.test.mjs")], check=True)


def test_build_confere_amostra():
    r = subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "51 seções · A 18 · B 16 · C 17" in r.stdout
    assert "consulta por nome, título desempata" in r.stdout
    assert "com homônimos (pedem o título)" in r.stdout


def test_build_rejeita_secao_estranha(tmp_path):
    csv = tmp_path / "lista.csv"
    csv.write_text("NUM_INSCRICAO;NOM_ELEITOR;NUM_SECAO;TURNO1;TURNO2\n123456789012;FULANO DE TAL;9999;OK;OK\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--lista", str(csv)], capture_output=True, text=True)
    assert r.returncode == 1 and "9999" in r.stdout


def test_rotas_batem_com_decisoes():
    if not (RAIZ / "app/dist/dados/rotas.json").exists():
        subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--grava", "--senha-equipe", "teste amostra"], check=True, capture_output=True)
    rotas = json.loads((RAIZ / "app/dist/dados/rotas.json").read_text(encoding="utf-8"))["secoes"]
    dec = json.loads((RAIZ / "data/decisoes.json").read_text(encoding="utf-8"))
    for m in dec["mesas"]:
        for s in [m["principal"]] + ([m["agregada"]] if m.get("agregada") else []):
            r = rotas[f"{s:04d}"]
            assert (r["letra"], r["porta"], r["parede"], r["mrv"]) == (m["entrada"], m["porta"], m["parede"], m["mrv"])
    assert rotas["3313"]["grupo"] == "A3" and rotas["3315"]["grupo"] == "B2" and rotas["3322"]["grupo"] == "C5"
    assert {r["parede_rotulo"] for r in rotas.values()} == {"da esquerda", "do fundo", "da direita"}
    assert rotas["3313"]["parede_rotulo"] == "da esquerda" and rotas["3322"]["parede_rotulo"] == "da direita"


def test_passos_na_perspectiva_do_eleitor():
    """Textos ao eleitor: sem pontos cardeais leste/oeste, sem 'apron', 'boca' nem 'cabeça' (decisão de 01/10)."""
    import re
    if not (RAIZ / "app/dist/dados/rotas.json").exists():
        subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--grava", "--senha-equipe", "teste amostra"], check=True, capture_output=True)
    rotas = json.loads((RAIZ / "app/dist/dados/rotas.json").read_text(encoding="utf-8"))["secoes"]
    proibido = re.compile(r"\b(leste|oeste|nordeste|sudeste|noroeste|sudoeste|apron|boca|bocas|cabe[cç]a|S[0-9])\b", re.I)
    for r in rotas.values():
        assert r["passos"][0]["texto"].startswith(f"Lembre-se disso: sua porta de entrada é {r['letra']}")
        for p in r["passos"]:
            texto = f"{p['onde']} {p['texto']}"
            assert not proibido.search(texto), texto


def test_indice_v2_da_amostra():
    """Índice da amostra: nome único -> [seção]; homônimo -> "H" + entradas nome|título; marca VT."""
    if not (RAIZ / "app/dist/dados/indice_publico.json").exists():
        subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--grava", "--senha-equipe", "teste amostra"], check=True, capture_output=True)
    idx = json.loads((RAIZ / "app/dist/dados/indice_publico.json").read_text(encoding="utf-8"))
    assert idx["v"] == 2 and idx["fator"] == "nome" and idx["turno"] == 1
    itens = idx["itens"]
    assert idx["titulo"] == {"digitos": "5-8", "tamanho": 4}
    assert itens[hash_publico("TIZZANI VIANA DANDREA NERY")] == ["3889"]
    assert itens[hash_publico("MARIA APARECIDA SILVA")] == "H"
    assert itens[hash_publico("MARIA APARECIDA SILVA", "1111")] == ["0511"]
    assert itens[hash_publico("MARIA APARECIDA SILVA", "3333")] == ["3862"]
    assert hash_publico("MARIA APARECIDA SILVA", "111111111111") not in itens, "o título completo não é chave do índice"
    assert itens[hash_publico("ANA VT TESTE")] == ["3315", "VT"]
    assert "111111111111" not in json.dumps(itens)


def test_pacote_da_equipe_so_tem_titulo_parcial():
    """Decifra o pacote da amostra (senha de teste) e confere que nenhum título tem mais de 4 dígitos."""
    import base64, hashlib, zlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    if not (RAIZ / "app/dist/dados/equipe.enc").exists():
        subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--grava", "--senha-equipe", "teste amostra"], check=True, capture_output=True)
    pac = json.loads((RAIZ / "app/dist/dados/equipe.enc").read_text(encoding="utf-8"))
    chave = hashlib.pbkdf2_hmac("sha256", b"teste amostra", base64.b64decode(pac["sal"]), pac["iteracoes"], 32)
    claro = zlib.decompress(AESGCM(chave).decrypt(base64.b64decode(pac["iv"]), base64.b64decode(pac["dados"]), None))
    dados = json.loads(claro)
    assert dados["titulo"] == {"digitos": "5-8", "tamanho": 4}
    assert all(len(e["t"]) == 4 and e["t"].isdigit() for e in dados["eleitores"])
    assert "123456789012" not in claro.decode("utf-8")


def test_colisao_de_titulo_parcial_vira_P(tmp_path):
    """Duas pessoas com o mesmo nome e os mesmos dígitos 5-8 não se separam: entrada "P" (manda ao P0)."""
    from app_construir import monta_indice, prepara_eleitores
    linhas = [
        {"NOM_ELEITOR": "FULANO DE TAL", "NUM_INSCRICAO": "000012340001", "NUM_SECAO": "0511", "TURNO1": "OK", "TURNO2": "OK"},
        {"NOM_ELEITOR": "FULANO DE TAL", "NUM_INSCRICAO": "999912349999", "NUM_SECAO": "3313", "TURNO1": "OK", "TURNO2": "OK"},
        {"NOM_ELEITOR": "FULANO DE TAL", "NUM_INSCRICAO": "000056780001", "NUM_SECAO": "3862", "TURNO1": "OK", "TURNO2": "OK"},
    ]
    idx, resumo = monta_indice(prepara_eleitores(linhas), 1)
    assert resumo["colisoes"] == 1
    assert idx["itens"][hash_publico("FULANO TAL", "1234")] == "P"
    assert idx["itens"][hash_publico("FULANO TAL", "5678")] == ["3862"]
