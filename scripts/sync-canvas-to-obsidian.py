#!/data/data/com.termux/files/usr/bin/python
from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "canvas"

# Destino oficial de Canvas en Termux/Obsidian.
# Se puede sobrescribir con CANVAS_DESTINATION si alguna instalación futura lo requiere.
DESTINATION = Path(
    os.environ.get(
        "CANVAS_DESTINATION",
        str(Path.home() / "storage" / "shared" / "Documents" / "4-TERMX"),
    )
).expanduser()


def main() -> int:
    if not SOURCE.is_dir():
        raise SystemExit(f"ERROR: no existe el origen: {SOURCE}")

    DESTINATION.mkdir(parents=True, exist_ok=True)

    source_files = {p.relative_to(SOURCE) for p in SOURCE.rglob("*.canvas")}

    # README es la referencia textual que acompaña a los Canvas en Obsidian.
    readme_source = ROOT / "README.md"
    readme_target = DESTINATION / "README.md"
    if readme_source.is_file():
        shutil.copy2(readme_source, readme_target)
        print(f"[README] README.md -> {readme_target}")

    for relative in sorted(source_files):
        source = SOURCE / relative
        target = DESTINATION / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        print(f"[Canvas] {relative} -> {target}")

    destination_files = {
        p.relative_to(DESTINATION)
        for p in DESTINATION.rglob("*.canvas")
    }

    for relative in sorted(destination_files - source_files):
        stale = DESTINATION / relative
        stale.unlink()
        print(f"[Canvas] eliminado obsoleto: {stale}")

    print(f"Sincronización Obsidian completada: {len(source_files)} Canvas + README.md.")
    print(f"Destino Obsidian: {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
