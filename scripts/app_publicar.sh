#!/usr/bin/env bash
# Publica app/dist/ no branch gh-pages deste repositório (GitHub Pages).
#
#   python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "..."
#   bash scripts/app_publicar.sh                 # raiz do site
#   bash scripts/app_publicar.sh --subpasta v2   # em …/dublineleicoesfinal/v2/, sem tocar na raiz
#   bash scripts/app_publicar.sh --subpasta v3   # v3 (nº no caderno, fila, admin) em …/v3/
# O estado vivo da fila (v3) NÃO é publicado por aqui: mora em fila.json no branch órfão `fila`.
#
# O branch gh-pages é ÓRFÃO e contém só o conteúdo de app/dist/ (+ .nojekyll): nenhum dado
# pessoal legível (hashes + pacote cifrado) e nenhum histórico do repositório. Cada publicação
# é um commit novo sobre o gh-pages anterior. Depois da primeira publicação, ativar o Pages em
# Settings → Pages → "Deploy from a branch" → gh-pages / (root).
set -euo pipefail
SUBPASTA=""
while [ $# -gt 0 ]; do
  case "$1" in
    --subpasta) SUBPASTA="${2:?nome da subpasta}"; shift 2 ;;
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
git -C "$RAIZ" fetch origin gh-pages 2>/dev/null || true
git -C "$RAIZ" worktree add --detach "$TMP/wt" >/dev/null 2>&1 || git -C "$RAIZ" worktree add --detach "$TMP/wt" HEAD
cd "$TMP/wt"
if git -C "$RAIZ" show-ref --verify --quiet refs/remotes/origin/gh-pages; then
  git checkout -q -B gh-pages origin/gh-pages
else
  git checkout -q --orphan gh-pages
fi
if [ -n "$SUBPASTA" ]; then
  rm -rf "./$SUBPASTA"
  mkdir -p "./$SUBPASTA"
  cp -r "$DIST"/. "./$SUBPASTA/"
else
  git rm -rfq . >/dev/null 2>&1 || true
  find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp -r "$DIST"/. .
fi
touch .nojekyll
git add -A
git -c user.name="${GIT_AUTHOR_NAME:-$(git -C "$RAIZ" config user.name || echo publicador)}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-$(git -C "$RAIZ" config user.email || echo publicador@localhost)}" \
    commit -q -m "Publica app/dist${SUBPASTA:+ em $SUBPASTA/} (versão $VERSAO)" || { echo "nada mudou em app/dist/"; exit 0; }
git push -u origin gh-pages
cd "$RAIZ"
git worktree remove --force "$TMP/wt"
echo "publicado: gh-pages${SUBPASTA:+/$SUBPASTA} @ $VERSAO"
