#!/usr/bin/env python3
"""Generate the automatic manifest and two static repository graphs."""
from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
MAP_MD = ROOT / "docs" / "repository-map.md"
GRAPH_STRUCTURE_DOT = ROOT / "docs" / "repository-structure.dot"
GRAPH_STRUCTURE_SVG = ROOT / "docs" / "repository-structure.svg"
GRAPH_ARCH_DOT = ROOT / "docs" / "repository-architecture.dot"
GRAPH_ARCH_SVG = ROOT / "docs" / "repository-architecture.svg"
START = "<!-- FILE-MANIFEST:START -->"
END = "<!-- FILE-MANIFEST:END -->"
EXCLUDED_PREFIXES = (".git/", ".ssh/", ".termux_authinfo")
GENERATED_GRAPH_FILES = {
    "docs/repository-structure.dot",
    "docs/repository-structure.svg",
    "docs/repository-architecture.dot",
    "docs/repository-architecture.svg",
}

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
    "update_readme_tree.py": "Generador automático del manifiesto y los dos grafos.",
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

def files_in_repo(include_generated=False):
    result = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(EXCLUDED_PREFIXES):
            continue
        if not include_generated and rel in GENERATED_GRAPH_FILES:
            continue
        result.append((rel, path.stat().st_size))
    return sorted(result)

def dot_escape(value):
    return value.replace("\\", "\\\\").replace('"', '\\"')

def node_id(rel):
    return "n_" + "".join(ch if ch.isalnum() else "_" for ch in rel)

def build_structure_dot(files):
    dirs = set()
    for rel, _ in files:
        parts = rel.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))

    lines = [
        "digraph RepositoryStructure {",
        '  graph [rankdir=TB, bgcolor="white", pad="0.25", nodesep="0.28", ranksep="0.55", splines=ortho, label="4-TERMX — Estructura real", labelloc=t, fontsize=20];',
        '  node [fontname="Arial", fontsize=10, style="filled", color="#555555"];',
        '  edge [color="#777777", arrowsize=0.6];',
        '  root [label="4-TERMX", shape=box, style="filled,bold", fontsize=15];',
    ]
    all_dirs = sorted(dirs, key=lambda x: (x.count("/"), x))
    for d in all_dirs:
        lines.append(f'  {node_id(d)} [label="{dot_escape(d.split("/")[-1])}", shape=box, fillcolor="#eeeeee"];')
    for rel, _ in files:
        parent = "/".join(rel.split("/")[:-1])
        shape = "box" if "." not in rel.split("/")[-1] else "note"
        label = rel.split("/")[-1]
        lines.append(f'  {node_id(rel)} [label="{dot_escape(label)}", shape={shape}, fillcolor="white"];')
        source = node_id(parent) if parent else "root"
        lines.append(f"  {source} -> {node_id(rel)};")
    for d in all_dirs:
        parent = "/".join(d.split("/")[:-1])
        source = node_id(parent) if parent else "root"
        lines.append(f"  {source} -> {node_id(d)};")
    lines.append("}")
    return "\n".join(lines) + "\n"

def build_architecture_dot(files):
    paths = [rel for rel, _ in files]
    lines = [
        "digraph RepositoryArchitecture {",
        '  graph [rankdir=TB, bgcolor="white", pad="0.3", nodesep="0.45", ranksep="0.65", splines=ortho, label="4-TERMX — Arquitectura / relaciones", labelloc=t, fontsize=20];',
        '  node [fontname="Arial", fontsize=10, style="rounded,filled", color="#555555", fillcolor="white"];',
        '  edge [color="#777777", arrowsize=0.65];',
        '  root [label="4-TERMX", shape=box, fillcolor="#eeeeee", fontsize=15];',
    ]

    top_dirs = sorted({p.split("/")[0] for p in paths if "/" in p})
    root_files = sorted(p for p in paths if "/" not in p)
    for d in top_dirs:
        lines.append(f'  dir_{node_id(d)} [label="{dot_escape(d)}", shape=box, fillcolor="#eeeeee"];')
        lines.append(f"  root -> dir_{node_id(d)};")
    for f in root_files:
        lines.append(f'  file_{node_id(f)} [label="{dot_escape(f)}", shape=note];')
        lines.append(f"  root -> file_{node_id(f)};")

    workflow = next((p for p in paths if p == ".github/workflows/update-tree.yml"), None)
    generator = "update_readme_tree.py" if "update_readme_tree.py" in paths else None
    readme = "README.md" if "README.md" in paths else None

    if workflow:
        lines.append('  workflow [label="update-tree.yml\\nGitHub Actions", shape=box, fillcolor="#f3f3f3"];')
        lines.append(f"  dir_{node_id('.github')} -> workflow;")
    if generator:
        lines.append('  generator [label="update_readme_tree.py\\ndescubre + genera", shape=box, fillcolor="#f3f3f3"];')
        lines.append("  root -> generator;")
    if readme:
        lines.append('  readme [label="README.md", shape=note, fillcolor="white"];')
        lines.append("  root -> readme;")

    docs = [p for p in paths if p.startswith("docs/")]
    if docs:
        lines.append('  docs [label="docs", shape=box, fillcolor="#eeeeee"];')
        lines.append("  root -> docs;")
        for p in docs:
            lines.append(f'  doc_{node_id(p)} [label="{dot_escape(p.split("/")[-1])}", shape=note];')
            lines.append(f"  docs -> doc_{node_id(p)};")

    if generator and workflow:
        lines.append('  workflow -> generator [label="ejecuta"];')
    if generator and readme:
        lines.append('  generator -> readme [label="actualiza"];')
    if generator and docs:
        for p in docs:
            if "repository-" in p:
                lines.append(f'  generator -> doc_{node_id(p)} [label="genera"];')
    lines.append('  github [label="GitHub", shape=box, fillcolor="#eeeeee"];')
    lines.append('  actions [label="GitHub Actions", shape=box, fillcolor="#eeeeee"];')
    lines.append('  root -> github [style=dashed, label="repositorio"];')
    lines.append("  github -> actions [style=dashed];")
    if workflow:
        lines.append('  actions -> workflow [style=dashed, label="workflow"];')
    lines.append("}")
    return "\n".join(lines) + "\n"

def render_graph(dot_path, svg_path):
    subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)], check=True)

def build_tree_markdown(files):
    lines = [
        "# 🌳 4-TERMX — Repository Map",
        "",
        "> Generado automáticamente por GitHub Actions a partir de la estructura real del repositorio.",
        "> Los directorios son ramas y los archivos son hojas.",
        "",
        "## 🧭 Mapa estructural",
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
        "## 🗺️ Grafos estáticos",
        "",
        "- repository-structure.svg: estructura completa, directorios como ramas y archivos como hojas.",
        "- repository-architecture.svg: relaciones funcionales entre GitHub, Actions, workflow, generador, README y docs/.",
        "",
        "> Ambos SVG y sus fuentes DOT se regeneran automáticamente cuando cambia el repositorio.",
        "",
    ]
    return "\n".join(lines)

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
    files = files_in_repo(include_generated=False)
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)

    MAP_MD.write_text(build_tree_markdown(files), encoding="utf-8")
    GRAPH_STRUCTURE_DOT.write_text(build_structure_dot(files), encoding="utf-8")
    GRAPH_ARCH_DOT.write_text(build_architecture_dot(files), encoding="utf-8")
    render_graph(GRAPH_STRUCTURE_DOT, GRAPH_STRUCTURE_SVG)
    render_graph(GRAPH_ARCH_DOT, GRAPH_ARCH_SVG)

    manifest_files = files_in_repo(include_generated=True)
    content = README.read_text(encoding="utf-8")
    manifest = build_manifest(manifest_files)
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        content = before.rstrip() + "\n\n" + manifest + after
    else:
        content = content.rstrip() + "\n\n" + manifest + "\n"
    README.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    main()
