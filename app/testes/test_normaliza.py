"""pytest: regras de normalização, leitor do PDF do TRE e conferência do build (python3 -m pytest app/testes)."""
import json, os, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from app_normaliza import chave_caderno, chaves_nome, hash_publico, normaliza_data, normaliza_inscricao, normaliza_nome, normaliza_secao, numero_caderno, titulo_parcial  # noqa: E402
from app_importar_eleitores import e_relatorio_de_mesarios, parse_texto_tre  # noqa: E402


def garante_dist_amostra():
    """app/dist/ construído com a AMOSTRA e a senha de teste (reconstrói se faltar ou se for um build real)."""
    versao = RAIZ / "app/dist/dados/versao.json"
    if not versao.exists() or not json.loads(versao.read_text(encoding="utf-8")).get("amostra_sintetica"):
        subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--grava", "--senha-equipe", "teste amostra"], check=True, capture_output=True)


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


def test_nome_com_e_sem_acento_mesma_chave():
    """02/10: til, cedilha, agudo, circunflexo, grave, trema e ordinal nunca mudam a chave (com ou sem, maiúsculo ou não, NFC ou NFD)."""
    pares = [
        ("Conceição Gonçalves Assunção", "CONCEICAO GONCALVES ASSUNCAO"),
        ("José Antônio Araújo Côrtes", "jose antonio araujo cortes"),
        ("Luís Ângelo Müller Peña", "LUIS ANGELO MULLER PENA"),
        ("Thaís Raíssa Jaçanã", "THAIS RAISSA JACANA"),
        ("Sebastião Façanha D’Ávila", "SEBASTIAO FACANHA DAVILA"),
        ("Mª da Conceição Sant'Ana", "ma conceicao santana"),
        ("João Gonçalves", "JOAO GONCALVES"),  # NFD
        ("À Côrte Èdith Ïris Òscar Ùrsula Ÿves", "A CORTE EDITH IRIS OSCAR URSULA YVES"),
    ]
    for com, sem in pares:
        assert normaliza_nome(com) == normaliza_nome(sem) == sem.upper(), com
        assert chaves_nome(com) == chaves_nome(sem), com


def test_vetores_js_iguais():
    subprocess.run([sys.executable, str(RAIZ / "app/testes/gera_vetores.py")], check=True)
    subprocess.run(["node", str(RAIZ / "app/testes/normaliza.test.mjs")], check=True)


def test_cripto_js_puro_igual_webcrypto():
    """A criptografia em JavaScript puro (página em http://, sem crypto.subtle) dá o mesmo resultado que o WebCrypto."""
    garante_dist_amostra()
    subprocess.run(["node", str(RAIZ / "app/testes/cripto.test.mjs")], check=True, env={**os.environ, "APP_SENHA_EQUIPE": "teste amostra"})


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
    garante_dist_amostra()
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
    garante_dist_amostra()
    rotas = json.loads((RAIZ / "app/dist/dados/rotas.json").read_text(encoding="utf-8"))["secoes"]
    proibido = re.compile(r"\b(leste|oeste|nordeste|sudeste|noroeste|sudoeste|apron|boca|bocas|cabe[cç]a|S[0-9])\b", re.I)
    for r in rotas.values():
        assert r["passos"][0]["texto"].startswith(f"Lembre-se disso: sua porta de entrada é {r['letra']}")
        for p in r["passos"]:
            texto = f"{p['onde']} {p['texto']}"
            assert not proibido.search(texto), texto


def test_indice_v2_da_amostra():
    """Índice da amostra: nome único -> [seção]; homônimo -> "H" + entradas nome|título; marca VT."""
    garante_dist_amostra()
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


def decifra_pacote_amostra():
    import base64, hashlib, zlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    garante_dist_amostra()
    pac = json.loads((RAIZ / "app/dist/dados/equipe.enc").read_text(encoding="utf-8"))
    chave = hashlib.pbkdf2_hmac("sha256", b"teste amostra", base64.b64decode(pac["sal"]), pac["iteracoes"], 32)
    claro = zlib.decompress(AESGCM(chave).decrypt(base64.b64decode(pac["iv"]), base64.b64decode(pac["dados"]), None))
    return json.loads(claro), claro.decode("utf-8")


def test_pacote_da_equipe_tem_titulo_completo_e_parcial():
    """02/10: a equipe volta a ver o título inteiro ("tc", 12 dígitos); o parcial ("t") continua, e só ele vai ao índice público."""
    dados, claro = decifra_pacote_amostra()
    assert dados["titulo"] == {"digitos": "5-8", "tamanho": 4}
    assert dados["titulo_equipe"] == "completo"
    assert all(len(e["t"]) == 4 and e["t"].isdigit() for e in dados["eleitores"])
    assert all(len(e["tc"]) == 12 and e["tc"].isdigit() and e["tc"][4:8] == e["t"] for e in dados["eleitores"])
    tizzani = next(e for e in dados["eleitores"] if e["n"] == "TIZZANI VIANA DANDREA NERY")
    assert tizzani["t"] == "5678" and tizzani["tc"].endswith("5678" + tizzani["tc"][8:]) and tizzani["s"] == "3889"
    publico = (RAIZ / "app/dist/dados/indice_publico.json").read_text(encoding="utf-8")
    assert "111111111111" in claro and "111111111111" not in publico, "o título completo só existe no pacote cifrado"
    versao = json.loads((RAIZ / "app/dist/dados/versao.json").read_text(encoding="utf-8"))
    assert versao["titulo_equipe"] == "completo"


def test_lista_so_parcial_marca_pacote_como_parcial():
    from app_construir import prepara_eleitores, titulo_equipe
    parcial = prepara_eleitores([{"NOM_ELEITOR": "FULANO DE TAL", "TITULO_5_8": "1234", "NUM_SECAO": "0511"}])
    completo = prepara_eleitores([{"NOM_ELEITOR": "FULANO DE TAL", "NUM_INSCRICAO": "000012340001", "NUM_SECAO": "0511"}])
    assert parcial[0]["t"] == "1234" and parcial[0]["tc"] == "" and titulo_equipe(parcial) == "parcial"
    assert completo[0]["t"] == "1234" and completo[0]["tc"] == "000012340001" and titulo_equipe(completo) == "completo"


def test_importador_rejeita_relatorio_de_mesarios():
    """O PDF "Relatório de Mesários por Situação" (Elo/Convoca+) não é a relação de eleitores (enviado por engano em 02/10)."""
    assert e_relatorio_de_mesarios("   Justiça Eleitoral\n   Elo - Cadastro Eleitoral | Convoca+\n   Relatório de Mesários por Situação\n")
    assert not e_relatorio_de_mesarios(TEXTO_TRE)


def test_textos_ao_eleitor_sem_secao_especifica():
    """02/10: o eleitor não vê 'sua seção'; vê porta e grupo, e a nota manda conferir no e-Título / TSE."""
    garante_dist_amostra()
    cfg = json.loads((RAIZ / "app/public/dados/config.json").read_text(encoding="utf-8"))
    assert "e-Título" in cfg["nota_secao"] and "TSE" in cfg["nota_secao"]
    rotas = json.loads((RAIZ / "app/dist/dados/rotas.json").read_text(encoding="utf-8"))["secoes"]
    assert "e-Título" in rotas["3889"]["passos"][4]["texto"]
    html = (RAIZ / "app/public/index.html").read_text(encoding="utf-8")
    assert "seção ${OEV.esc(rota.secao)}" not in html and "grupo ${OEV.esc(rota.grupo)}" in html
    js = (RAIZ / "app/public/comum.js").read_text(encoding="utf-8")
    assert '<div class="rotulo">seção</div>' not in js and "seu grupo de mesas" in js and "nota-secao" in js


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


def test_lista_cifrada_ida_e_volta(tmp_path):
    """CSV cifrado com app_cifra_lista: volta idêntico com a senha, falha com senha errada, sem nome em claro."""
    from app_cifra_lista import cifra_bytes, decifra_bytes, le_csv_cifrado
    csv_claro = (RAIZ / "app/testes/amostra_eleitores.csv").read_bytes()
    pacote = cifra_bytes(csv_claro, "teste amostra")
    assert decifra_bytes(pacote, "teste amostra") == csv_claro
    assert b"TIZZANI" not in json.dumps(pacote).encode()
    enc = tmp_path / "amostra.csv.enc"
    enc.write_text(json.dumps(pacote), encoding="utf-8")
    assert "TIZZANI VIANA D'ANDREA NERY" in le_csv_cifrado(enc, "teste amostra")
    import pytest
    with pytest.raises(SystemExit):
        le_csv_cifrado(enc, "senha errada")
    r = subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py"), "--lista", str(enc), "--senha-equipe", "teste amostra"], capture_output=True, text=True)
    assert r.returncode == 0 and "1007 eleitores" in r.stdout, r.stdout + r.stderr


# ---- v3 (01/10/2026): número no caderno e zonas para a estimativa de espera ----

def test_numero_caderno_regra_dos_200():
    """Posição até 200 -> ela mesma; acima de 200 -> menos 200 (exemplo do usuário: 256º -> 56)."""
    assert numero_caderno(1) == 1 and numero_caderno(199) == 199 and numero_caderno(200) == 200
    assert numero_caderno(201) == 1 and numero_caderno(256) == 56
    assert numero_caderno(0) is None and numero_caderno(None) is None


def test_chave_caderno_mantem_particulas():
    """Ordem alfabética do nome impresso: sem acento, maiúsculas, partículas contam (ao contrário de normaliza_nome)."""
    assert chave_caderno("Maria da Silva") == "MARIA DA SILVA"
    assert chave_caderno("  josé  gonçalves ") == "JOSE GONCALVES"
    assert chave_caderno("MARIA DA SILVA") < chave_caderno("MARIA DANTAS")


def test_numera_caderno_por_secao():
    """256 eleitores na 0513 e 3 na 3313: posição alfabética por seção; o 256º da 0513 vira nº 56."""
    from app_construir import numera_caderno, prepara_eleitores
    linhas = [{"NOM_ELEITOR": f"ELEITOR {i:03d} TESTE", "NUM_INSCRICAO": f"{i:012d}", "NUM_SECAO": "0513", "TURNO1": "OK", "TURNO2": "OK"} for i in range(1, 256)]
    linhas.append({"NOM_ELEITOR": "MARIVALDO CLEITON", "NUM_INSCRICAO": "999999999999", "NUM_SECAO": "0513", "TURNO1": "OK", "TURNO2": "OK"})
    linhas += [{"NOM_ELEITOR": n, "NUM_INSCRICAO": f"{i:012d}", "NUM_SECAO": "3313", "TURNO1": "OK", "TURNO2": "OK"}
               for i, n in enumerate(["ZELIA ALVES", "ANA DA COSTA", "ANA COSTA"], start=1)]
    eleitores = numera_caderno(prepara_eleitores(linhas))
    por_nome = {e["n"]: e for e in eleitores}
    m = por_nome["MARIVALDO CLEITON"]
    assert (m["p"], m["c"]) == (256, 56)
    assert (por_nome["ELEITOR 001 TESTE"]["p"], por_nome["ELEITOR 001 TESTE"]["c"]) == (1, 1)
    assert (por_nome["ELEITOR 200 TESTE"]["p"], por_nome["ELEITOR 200 TESTE"]["c"]) == (200, 200)
    assert (por_nome["ELEITOR 201 TESTE"]["p"], por_nome["ELEITOR 201 TESTE"]["c"]) == (201, 1)
    # na 3313: "ANA COSTA" < "ANA DA COSTA" < "ZELIA ALVES" (a partícula DA conta na ordem do caderno)
    assert [e["n"] for e in sorted((e for e in eleitores if e["s"] == "3313"), key=lambda e: e["p"])] == ["ANA COSTA", "ANA COSTA", "ZELIA ALVES"]
    assert por_nome["ZELIA ALVES"]["c"] == 3


def test_pacote_da_equipe_tem_numero_do_caderno():
    import base64, hashlib, zlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    garante_dist_amostra()
    pac = json.loads((RAIZ / "app/dist/dados/equipe.enc").read_text(encoding="utf-8"))
    chave = hashlib.pbkdf2_hmac("sha256", b"teste amostra", base64.b64decode(pac["sal"]), pac["iteracoes"], 32)
    dados = json.loads(zlib.decompress(AESGCM(chave).decrypt(base64.b64decode(pac["iv"]), base64.b64decode(pac["dados"]), None)))
    assert dados["caderno"] == {"bloco": 200}
    assert all(isinstance(e["p"], int) and isinstance(e["c"], int) and 1 <= e["c"] <= e["p"] for e in dados["eleitores"])
    por_secao = {}
    for e in dados["eleitores"]:
        por_secao.setdefault(e["s"], []).append(e)
    for secao, pessoas in por_secao.items():
        pessoas.sort(key=lambda e: e["p"])
        assert [e["p"] for e in pessoas] == list(range(1, len(pessoas) + 1)), secao
        chaves = [chave_caderno(e["o"]) for e in pessoas]
        assert chaves == sorted(chaves), secao


def test_rotas_tem_zonas_e_config_tem_fila_e_admin():
    garante_dist_amostra()
    rotas = json.loads((RAIZ / "app/dist/dados/rotas.json").read_text(encoding="utf-8"))
    assert {l: z["urnas"] for l, z in rotas["zonas"].items()} == {"A": 9, "B": 9, "C": 10}
    assert sum(z["esperado"] for z in rotas["zonas"].values()) == 11499
    cfg = json.loads((RAIZ / "app/public/dados/config.json").read_text(encoding="utf-8"))
    assert cfg["versao_app"] == "v3"
    f = cfg["fila"]
    assert f["url_leitura"].startswith("https://raw.githubusercontent.com/") and f["url_leitura"].endswith(f"/{f['branch']}/{f['arquivo']}")
    assert f["repo"] in f["url_leitura"]
    assert f["lotacao_zona"] == 706 and f["segundos_por_eleitor"] > 0
    import base64, hashlib
    adm = cfg["admin"]
    # a senha real do administrador não aparece em lugar nenhum do git (nem aqui): só o hash PBKDF2, de 32 bytes
    assert adm["kdf"] == "PBKDF2-SHA256" and adm["iteracoes"] >= 200000 and len(adm["sal"]) >= 16
    assert len(base64.urlsafe_b64decode(adm["hash"] + "=" * (-len(adm["hash"]) % 4))) == 32
    dk = hashlib.pbkdf2_hmac("sha256", b"senha errada", adm["sal"].encode(), adm["iteracoes"], 32)
    assert base64.urlsafe_b64encode(dk).decode().rstrip("=") != adm["hash"]
    versao = json.loads((RAIZ / "app/dist/dados/versao.json").read_text(encoding="utf-8"))
    assert versao["app"] == "v3" and versao["caderno"] == {"bloco": 200}
