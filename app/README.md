# App "Onde eu voto?" — Dublin, Eleições 2026

Site estático (PWA) em duas páginas: **eleitor** (nome + data de nascimento → seção, fila,
porta, parede, grupo e o caminho Ring 3 → Hall 2) e **equipe** (busca por nome, com título
e seção; funciona sem internet). Contexto, decisões e modelo de ameaça em
[`../docs/app/contexto.md`](../docs/app/contexto.md).

```
pip install -r app/requirements.txt

# 1. quando a lista chegar (.xlsx, .csv ou .pdf com texto):
python3 scripts/app_importar_eleitores.py lista.xlsx --local 1015          # confere
python3 scripts/app_importar_eleitores.py lista.xlsx --local 1015 --grava  # data/eleitores/eleitores.csv (fora do git)

# 2. construir o site (sem --grava só confere; sem lista usa a amostra sintética):
python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "seis palavras da senha do dia"

# 3. publicar app/dist/ no GitHub Pages (ver contexto.md §5)

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
