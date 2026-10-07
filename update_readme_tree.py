#!/usr/bin/env python3
"""Generate the automatic repository manifest and Markmap sources."""
from pathlib import Path
import html
import os
import subprocess

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
MAP_MD = ROOT / "docs" / "repository-map.md"
MAP_HTML = ROOT / "docs" / "repository-map.html"
START = "<!-- FILE-MANIFEST:START -->"
END = "<!-- FILE-MANIFEST:END -->"
EXCLUDED_PREFIXES = (".git/", ".ssh/", ".termux_authinfo")

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
    "sync-repo.sh": "Sincronización del repositorio desde Termux.",
    "update_readme_tree.py": "Generador automático del manifiesto y Repository Map.",
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
        return "Lógica central del agente."
    if rel.startswith("agente/tools/"):
        return "Herramienta del agente."
    if rel.startswith("codex_local/"):
        return "Componente local de Codex."
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
        if rel.startswith(EXCLUDED_PREFIXES):
            continue
        result.append((rel, path.stat().st_size))
    return sorted(result)

def build_tree_markdown(files):
    lines = [
        "# 🌳 4-TERMX — Repository Map",
        "",
        "> Generado automáticamente por GitHub Actions a partir de la estructura real del repositorio.",
        "> Los directorios y archivos excluidos por seguridad no aparecen en este mapa.",
        "",
        "## 🧭 Mapa",
        "",
        "# 4-TERMX",
    ]
    tree = {}
    for rel, _ in files:
        node = tree
        parts = rel.split("/")
        for index, part in enumerate(parts):
            if index == len(parts) - 1:
                node[part] = None
            else:
                node = node.setdefault(part, {})
    def emit(node, depth):
        for name in sorted(node):
            value = node[name]
            if value is None:
                lines.append(f"- {name}")
            else:
                prefix = "#" * min(depth + 2, 6)
                lines.append(f"{prefix} {name}")
                emit(value, depth + 1)
    emit(tree, 0)
    lines += [
        "",
        "## 🔗 Vista interactiva",
        "",
        "Abrir repository-map.html para explorar el mismo árbol con Markmap (zoom, desplazamiento y expandir/contraer ramas).",
        "",
    ]
    return "\n".join(lines)

def build_tree_html(markdown):
    payload = html.escape(markdown, quote=False)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>4-TERMX — Repository Map</title>
<style>html,body,#mindmap{{width:100%;height:100%;margin:0}}</style>
</head>
<body>
<svg id="mindmap"></svg>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18.12"></script>
<script type="text/template">
{payload}
</script>
</body>
</html>
"""

def build_manifest(files):
    total = sum(size for _, size in files)
    lines = [
        START,
        "## 📦 File Manifest Table",
        "",
        "> **Generado automáticamente por GitHub Actions.** Representa los archivos visibles del repositorio; secretos y material SSH están excluidos.",
        "",
        "| Estado | Archivo | Tipo | Tamaño | Función |",
        "|---|---|---|---:|---|",
    ]
    changed = dict(changed_files())
    for rel, size in files:
        status = changed.get(rel, "—")
        link = "[<code>" + rel + "</code>](./" + rel + ")"
        lines.append(f"| {status} | {link} | {file_type(Path(rel))} | {size_text(size)} | {description(rel)} |")

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
    files = files_in_repo()
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    map_markdown = build_tree_markdown(files)
    MAP_MD.write_text(map_markdown, encoding="utf-8")
    MAP_HTML.write_text(build_tree_html(map_markdown), encoding="utf-8")

    content = README.read_text(encoding="utf-8")
    manifest = build_manifest(files)
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        content = before.rstrip() + "\n\n" + manifest + after
    else:
        content = content.rstrip() + "\n\n" + manifest + "\n"
    README.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    main()
