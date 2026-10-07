#!/usr/bin/env python3
"""Generate the automatic File Manifest section of README.md."""
from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
START = "<!-- FILE-MANIFEST:START -->"
END = "<!-- FILE-MANIFEST:END -->"

TYPE_MAP = {
    ".py": "Python", ".sh": "Shell", ".md": "Markdown",
    ".yml": "GitHub Actions", ".yaml": "GitHub Actions",
    ".txt": "Texto", ".json": "JSON", ".toml": "TOML",
    ".c": "C", ".js": "JavaScript", ".ts": "TypeScript",
}

DESCRIPTIONS = {
    "README.md": "Documentación central del entorno Termux.",
    "CHANGELOG.md": "Historial de cambios del proyecto.",
    "MENU_IA.md": "Menú y documentación de herramientas de IA.",
    "RAG.md": "Documentación del flujo RAG.",
    "rag.py": "Implementación principal de RAG.",
    "rag_local.py": "Implementación local de RAG.",
    "rag_simple.py": "Implementación simplificada de RAG.",
    "sync-menu.sh": "Menú de sincronización y operaciones Git.",
    "update_readme_tree.py": "Generador automático del File Manifest del README.",
}

def size_text(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"

def file_type(path):
    if path.name.startswith("."):
        return "Configuración"
    return TYPE_MAP.get(path.suffix.lower(), "Archivo")

def description(rel):
    if rel in DESCRIPTIONS:
        return DESCRIPTIONS[rel]
    if rel.startswith(".github/workflows/"):
        return "Workflow de automatización de GitHub Actions."
    if rel.startswith("agente/core/"):
        return "Lógica central del agente, modelos, memoria, configuración o pruebas."
    if rel.startswith("agente/tools/"):
        return "Herramienta del agente para archivos, sistema o servicios."
    if rel.startswith("codex_local/"):
        return "Componente local de Codex: configuración, ejecución, herramientas o pruebas."
    if rel.startswith("pxe-winpe/scripts/"):
        return "Script operativo del flujo PXE/WinPE."
    if rel.startswith("pxe-winpe/config/"):
        return "Configuración del flujo PXE/WinPE."
    if rel.startswith("pxe-winpe/"):
        return "Componente del entorno PXE/WinPE."
    return f"Archivo {file_type(Path(rel))} del proyecto."

def changed_files():
    before = os.getenv("GITHUB_EVENT_BEFORE", "")
    current = os.getenv("GITHUB_SHA", "")
    if not before or not current or before == "0" * 40:
        return []
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-status", before, current],
            text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return []
    labels = {"A": "🆕 Nuevo", "M": "✏️ Modificado", "D": "🗑️ Eliminado", "R": "🔄 Renombrado"}
    result = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            result.append((labels.get(parts[0][0], parts[0]), parts[-1]))
    return result

def files_in_repo():
    result = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.split("/")[0] == ".git":
            continue
        result.append((rel, path.stat().st_size))
    return sorted(result)

def build_manifest():
    files = files_in_repo()
    total = sum(size for _, size in files)
    lines = [
        START,
        "## 📦 File Manifest Table",
        "",
        "> **Generado automáticamente por GitHub Actions.** Esta tabla representa el estado actual de los archivos rastreados del repositorio.",
        "",
        "| Estado | Archivo | Tipo | Tamaño | Función |",
        "|---|---|---|---:|---|",
    ]

    changed = dict(changed_files())
    for rel, size in files:
        status = changed.get(rel, "—")
        link = "[<code>" + rel + "</code>](./" + rel + ")"
        lines.append(
            f"| {status} | {link} | {file_type(Path(rel))} | "
            f"{size_text(size)} | {description(rel)} |"
        )

    lines += ["", "### 📂 Bloques colapsables por componente", ""]
    groups = {}
    for rel, size in files:
        group = rel.split("/", 1)[0] if "/" in rel else "raíz"
        groups.setdefault(group, []).append((rel, size))

    for group, entries in sorted(groups.items()):
        group_total = sum(size for _, size in entries)
        lines += [
            "<details>",
            f"<summary>📁 <strong>{group}</strong> — {len(entries)} archivos / {size_text(group_total)}</summary>",
            "",
        ]
        for rel, size in entries:
            link = "[<code>" + rel + "</code>](./" + rel + ")"
            lines.append(f"- {link} — **{size_text(size)}** — {description(rel)}")
        lines += ["", "</details>", ""]

    recent = changed_files()
    if recent:
        lines += ["### 🆕 Cambios detectados por la última ejecución", ""]
        for status, rel in recent:
            lines.append(f"- **{status}** <code>{rel}</code>")
        lines.append("")

    lines += [
        f"**Total actual:** {len(files)} archivos — **{size_text(total)}**",
        "",
        "_Este bloque es mantenido por Actions. No editar manualmente entre los marcadores._",
        END,
    ]
    return "\n".join(lines)

def main():
    content = README.read_text(encoding="utf-8")
    manifest = build_manifest()
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        content = before.rstrip() + "\n\n" + manifest + after
    else:
        content = content.rstrip() + "\n\n" + manifest + "\n"
    README.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    main()
