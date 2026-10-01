# App "Onde eu voto?" — Dublin, Eleições 2026

Site estático (PWA) em duas páginas: **eleitor** (nome → seção, fila, porta, parede, grupo e
o caminho Ring 3 → Hall 2; em homônimo, pede o título) e **equipe** (busca por nome, homônimos
lado a lado com título e seção; funciona sem internet). Construído com a lista real do TRE de
29/09/2026 (só nome, inscrição, seção e marcas de turno). Contexto, decisões e modelo de ameaça em
[`../docs/app/contexto.md`](../docs/app/contexto.md).

```
pip install -r app/requirements.txt          # e poppler-utils (pdftotext) no sistema

# 1. a lista do TRE (PDF) fica em data/eleitores/, fora do git:
python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf"          # confere
python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf" --grava  # data/eleitores/eleitores.csv

# 2. construir o site (sem --grava só confere; sem lista usa a amostra sintética):
python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "seis palavras da senha do dia"

# 3. publicar app/dist/ no branch gh-pages deste repositório (GitHub Pages; ver contexto.md §5):
bash scripts/app_publicar.sh

# testes
python3 -m pytest -q app/testes
APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
APP_SENHA_EQUIPE="teste amostra" NODE_PATH=/opt/node22/lib/node_modules node app/testes/ponta_a_ponta.mjs
```

| Pasta | O que é |
|---|---|
| `public/` | o site, sem build de frontend: `index.html` (eleitor), `equipe/`, `comum.js`, `estilo.css`, `sw.js`, `manifest.webmanifest`, `dados/config.json` |
| `dist/` | saída de `app_construir.py` = `public/` + `dados/rotas.json`, `indice_publico.json`, `equipe.enc`, `versao.json`. É o que se publica. Não versionado |
| `testes/` | amostra sintética, vetores Python × JS, pytest e teste de ponta a ponta no Chromium |
