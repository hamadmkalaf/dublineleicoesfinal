#!/bin/bash
# Publica SÓ dados/rotas.json (+ carimbo de versão em sw.js e versao.json) num branch de publicação,
# sem reconstruir o índice nem o pacote da equipe — não precisa da senha da equipe.
# Uso (depois de `python3 scripts/app_construir.py --grava`, que gera app/dist/dados/rotas.json com a amostra;
# rotas.json não depende da lista):
#   bash scripts/app_publicar_rotas.sh gh-pages . v2 v3     # raiz, v2/ e v3/ do gh-pages
#   bash scripts/app_publicar_rotas.sh gh-pages2 .          # raiz do gh-pages2
# Criado em 04/10/2026 para a correção dos grupos da parede oeste (docs/app/contexto.md §2f).
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
BRANCH="${1:?branch de publicação (gh-pages ou gh-pages2)}"; shift
DIRS="${*:-.}"
ROTAS="$RAIZ/app/dist/dados/rotas.json"
[ -f "$ROTAS" ] || { echo "falta $ROTAS: rode python3 scripts/app_construir.py --grava"; exit 1; }
TS="$(date -u +%Y-%m-%dT%H:%M:%S+00:00)"
TMP="$(mktemp -d)"; trap 'git -C "$RAIZ" worktree remove --force "$TMP/wt" 2>/dev/null; rm -rf "$TMP"' EXIT
git -C "$RAIZ" fetch origin "$BRANCH"
git -C "$RAIZ" worktree add -q --detach "$TMP/wt" "origin/$BRANCH"
cd "$TMP/wt"
for d in $DIRS; do
  cp "$ROTAS" "$d/dados/rotas.json"
  sed -i "s|^const VERSAO = \".*\";|const VERSAO = \"$TS\";|" "$d/sw.js"
  grep -q "const VERSAO = \"$TS\"" "$d/sw.js"
  python3 - "$d/dados/versao.json" "$TS" <<'PY'
import json, sys
p, ts = sys.argv[1:]
v = json.load(open(p, encoding="utf-8")); v["construido_em"] = ts; v["rotas"] = "parede oeste na ordem de 23/09 (correção de 04/10)"
json.dump(v, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
PY
done
git add -A && git status --short
git -c user.name="${GIT_AUTHOR_NAME:-$(git -C "$RAIZ" config user.name || echo publicador)}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-$(git -C "$RAIZ" config user.email || echo publicador@localhost)}" \
    commit -q -m "Corrige rotas.json: grupos da parede oeste na ordem de 23/09 (A1/A4 e A2/A5 trocados); versão $TS"
git push origin "HEAD:refs/heads/$BRANCH"
echo "publicado em $BRANCH ($DIRS) @ $TS"
