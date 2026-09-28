"""pytest: regras de normalização e conferência do build (python3 -m pytest app/testes)."""
import json, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from app_normaliza import chaves_nome, normaliza_data, normaliza_inscricao, normaliza_nome, normaliza_secao  # noqa: E402


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


def test_vetores_js_iguais():
    subprocess.run([sys.executable, str(RAIZ / "app/testes/gera_vetores.py")], check=True)
    subprocess.run(["node", str(RAIZ / "app/testes/normaliza.test.mjs")], check=True)


def test_build_confere_amostra():
    r = subprocess.run([sys.executable, str(RAIZ / "scripts/app_construir.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "51 seções · A 18 · B 16 · C 17" in r.stdout


def test_build_rejeita_secao_estranha(tmp_path):
    csv = tmp_path / "lista.csv"
    csv.write_text("NUM_INSCRICAO;NOM_ELEITOR;DAT_NASC;NUM_SECAO\n123456789012;FULANO DE TAL;1980-01-01;9999\n", encoding="utf-8")
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
