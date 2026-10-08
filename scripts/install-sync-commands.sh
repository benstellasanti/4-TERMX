#!/data/data/com.termux/files/usr/bin/bash
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PREFIX_BIN="${PREFIX:-/data/data/com.termux/files/usr}/bin"

[ -d "$PREFIX_BIN" ] || { echo "[ERROR] No existe $PREFIX_BIN"; exit 1; }

chmod +x "$ROOT/scripts/bajada" "$ROOT/scripts/subida"
ln -sfn "$ROOT/scripts/bajada" "$PREFIX_BIN/bajada"
ln -sfn "$ROOT/scripts/subida" "$PREFIX_BIN/subida"

echo "[OK] Comandos instalados:"
echo "     bajada -> $ROOT/scripts/bajada"
echo "     subida -> $ROOT/scripts/subida"
echo
echo "Prueba con:"
echo "     bajada"
echo "     subida"
