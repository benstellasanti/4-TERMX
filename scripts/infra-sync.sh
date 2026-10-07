#!/data/data/com.termux/files/usr/bin/sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PYTHON="${PYTHON:-python}"
exec "$PYTHON" "$ROOT/scripts/infra-sync.py" "$@"
