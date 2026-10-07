#!/data/data/com.termux/files/usr/bin/bash
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"

"$ROOT/scripts/infra-sync.sh" --no-git

git add infrastructure/system-manifest.json infrastructure/history .gitignore docs scripts
if ! git diff --cached --quiet; then
  git commit -m "infra: reconcile infrastructure state"
fi

git pull --rebase origin main
git push origin main
