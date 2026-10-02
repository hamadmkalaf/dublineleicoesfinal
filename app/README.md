# App "Onde eu voto?" — Dublin, Eleições 2026

Site estático (PWA) em três páginas: **eleitor** (nome → **porta e grupo de mesas**, parede e o
caminho Ring 3 → Hall 2 — sem a seção específica, que o eleitor confere no e-Título (02/10); em homônimo, pede o título; v3: tempo estimado de espera quando o
status de fila está ativado), **equipe** (busca por nome, homônimos lado a lado com o **título completo** e a seção da lista; painel para informar quão cheia está cada zona do Ring 3; funciona sem
internet) e **administrador** (v3: liga/desliga o status de fila; guarda a chave de publicação). Construído com a lista real do TRE de
29/09/2026 (só nome, inscrição, seção e marcas de turno). Contexto, decisões e modelo de ameaça em
[`../docs/app/contexto.md`](../docs/app/contexto.md).

```
pip install -r app/requirements.txt          # e poppler-utils (pdftotext) no sistema

# 1. a lista do TRE (PDF) fica em data/eleitores/, fora do git:
python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf"          # confere
python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf" --grava  # data/eleitores/eleitores.csv (título completo; --titulo-parcial dá o v2)

# 1b. guardar a lista v2 no git, cifrada com a senha da equipe (único arquivo de data/eleitores/ que entra):
python3 scripts/app_cifra_lista.py cifrar data/eleitores/eleitores.csv --senha "seis palavras da senha do dia"
python3 scripts/app_cifra_lista.py decifrar data/eleitores/eleitores.csv.enc --senha "..."   # em outra máquina

# 2. construir o site (sem --grava só confere; sem lista usa a amostra sintética; aceita o .enc):
python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv.enc --grava --senha-equipe "seis palavras da senha do dia"   # o eleitores_v2.csv.enc ainda funciona, mas a equipe só vê 4 dígitos

# 3. publicar app/dist/ no branch gh-pages deste repositório (GitHub Pages; ver contexto.md §5):
bash scripts/app_publicar.sh --subpasta v3      # …/dublineleicoesfinal/v3/ ; sem --subpasta publica na raiz
bash scripts/app_publicar.sh --branch gh-pages2 # branch gh-pages2 = só a v3 (02/10); o Pages serve UM branch: apontar em Settings → Pages

# 3b. (v3) estado vivo da fila: fila.json no branch órfão `fila` deste repositório. Já existe; a equipe e o
#     admin gravam nele pela API do GitHub com um fine-grained PAT (só este repositório, Contents: read/write),
#     colado uma vez em cada aparelho (admin/ ou equipe/) e guardado cifrado com a senha. Ver docs/app/contexto.md §2d.

# testes
python3 -m pytest -q app/testes
APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
APP_SENHA_EQUIPE="teste amostra" NODE_PATH=/opt/node22/lib/node_modules node app/testes/ponta_a_ponta.mjs
node app/testes/cripto.test.mjs                 # criptografia em JavaScript puro (página em http://) × WebCrypto
APP_SENHA_EQUIPE="teste amostra" NODE_PATH=/opt/node22/lib/node_modules node app/testes/insegura.mjs   # as 3 páginas num http://IP, sem crypto.subtle
```

| Pasta | O que é |
|---|---|
| `public/` | o site, sem build de frontend: `index.html` (eleitor), `equipe/`, `admin/` (v3), `comum.js`, `estilo.css`, `sw.js`, `manifest.webmanifest`, `dados/config.json` (textos, parâmetros da fila, hash da senha do admin) |
| `dist/` | saída de `app_construir.py` = `public/` + `dados/rotas.json` (com `zonas`), `indice_publico.json`, `equipe.enc` (com `p`/`c` do caderno), `versao.json`. É o que se publica. Não versionado |
| branch `fila` | só `fila.json` (lotação por zona, status ativado); escrito pela equipe/admin, lido pelo eleitor. Sem dado pessoal |
| `testes/` | amostra sintética, vetores Python × JS, pytest e teste de ponta a ponta no Chromium |
| `../data/eleitores/*.csv.enc` | a lista cifrada (AES-256-GCM, senha da equipe): `eleitores_v2.csv.enc` só com os dígitos 5-8 (01/10); `eleitores.csv.enc` com o título completo, a gerar da relação do TRE (02/10). O CSV em claro não entra no git |
