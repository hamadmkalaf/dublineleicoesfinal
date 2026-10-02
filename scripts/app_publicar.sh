#!/usr/bin/env bash
# Publica app/dist/ no branch gh-pages deste repositório (GitHub Pages).
#
#   python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "..."
#   bash scripts/app_publicar.sh                 # raiz do site (= o domínio dublineleicoes2026.com.br); preserva CNAME e v2/, v3/
#   bash scripts/app_publicar.sh --subpasta v2   # em …/dublineleicoesfinal/v2/, sem tocar na raiz
#   bash scripts/app_publicar.sh --subpasta v3   # v3 (nº no caderno, fila, admin) em …/v3/
#   bash scripts/app_publicar.sh --branch gh-pages2   # mesma coisa, noutro branch de publicação (02/10: gh-pages2 = só a v3)
# O estado vivo da fila (v3) NÃO é publicado por aqui: mora em fila.json no branch órfão `fila`.
#
# O branch de publicação (gh-pages por padrão) é ÓRFÃO e contém só o conteúdo de app/dist/ (+ .nojekyll
# e CNAME): nenhum dado pessoal legível (hashes + pacote cifrado) e nenhum histórico do repositório. Cada
# publicação é um commit novo sobre o anterior. O GitHub Pages serve UM branch por repositório: depois de
# publicar, apontar Settings → Pages → "Deploy from a branch" → <branch> / (root), e marcar "Enforce HTTPS".
set -euo pipefail
SUBPASTA=""
BRANCH="gh-pages"
while [ $# -gt 0 ]; do
  case "$1" in
    --subpasta) SUBPASTA="${2:?nome da subpasta}"; shift 2 ;;
    --branch) BRANCH="${2:?nome do branch}"; shift 2 ;;
    *) echo "argumento desconhecido: $1"; exit 2 ;;
  esac
done
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$RAIZ/app/dist"
[ -f "$DIST/dados/versao.json" ] || { echo "app/dist/ não existe ou está incompleto: rode app_construir.py --grava"; exit 1; }
if grep -q '"amostra_sintetica": true' "$DIST/dados/versao.json"; then
  echo "app/dist/ foi construído com a AMOSTRA sintética; reconstrua com --lista data/eleitores/eleitores.csv"; exit 1
fi
VERSAO="$(python3 -c "import json;print(json.load(open('$DIST/dados/versao.json'))['construido_em'])")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git -C "$RAIZ" fetch origin "$BRANCH" 2>/dev/null || true
git -C "$RAIZ" worktree add --detach "$TMP/wt" >/dev/null 2>&1 || git -C "$RAIZ" worktree add --detach "$TMP/wt" HEAD
cd "$TMP/wt"
if git -C "$RAIZ" show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git checkout -q -B "$BRANCH" "origin/$BRANCH"
else
  git checkout -q --orphan "$BRANCH"
  git rm -rfq --cached . 2>/dev/null || true
  find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  # branch novo: herda o CNAME do gh-pages, para o domínio seguir quando o Pages for apontado para ele
  git -C "$RAIZ" show origin/gh-pages:CNAME > CNAME 2>/dev/null || rm -f CNAME
fi
if [ -n "$SUBPASTA" ]; then
  rm -rf "./$SUBPASTA"
  mkdir -p "./$SUBPASTA"
  cp -r "$DIST"/. "./$SUBPASTA/"
else
  # raiz: substitui o app, mas preserva o CNAME (domínio próprio) e as versões antigas em v2/, v3/…
  find . -mindepth 1 -maxdepth 1 ! -name .git ! -name CNAME ! -name 'v[0-9]*' -exec rm -rf {} +
  cp -r "$DIST"/. .
fi
touch .nojekyll
git add -A
git -c user.name="${GIT_AUTHOR_NAME:-$(git -C "$RAIZ" config user.name || echo publicador)}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-$(git -C "$RAIZ" config user.email || echo publicador@localhost)}" \
    commit -q -m "Publica app/dist${SUBPASTA:+ em $SUBPASTA/} (versão $VERSAO)" || { echo "nada mudou em app/dist/"; exit 0; }
git push -u origin "$BRANCH"
cd "$RAIZ"
git worktree remove --force "$TMP/wt"
echo "publicado: $BRANCH${SUBPASTA:+/$SUBPASTA} @ $VERSAO"
