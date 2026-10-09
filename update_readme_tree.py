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
CANVAS_DIR = ROOT / "docs" / "canvas"
SVG_TO_CANVAS = ROOT / "docs" / "svg2canvas.py"
START = "<!-- FILE-MANIFEST:START -->"
END = "<!-- FILE-MANIFEST:END -->"
EXCLUDED_PREFIXES = (".git/", ".ssh/", ".termux_authinfo", ".local/", "storage/", "4termx-security-backup/")
EXCLUDED_NAMES = {"__pycache__", ".cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
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
    # Raíz y configuración
    "README.md": "Guía principal: propósito, requisitos, inicio rápido, comandos y documentación.",
    ".gitignore": "Excluye secretos, credenciales y artefactos locales de Git.",
    ".gitconfig": "Configuración Git versionada para el entorno del proyecto.",
    ".zshrc": "Inicialización de Zsh y reconciliación automática de infraestructura.",
    ".termux/termux.properties": "Preferencias de interfaz y comportamiento de Termux.",
    ".github/workflows/update-tree.yml": "Workflow que regenera mapas, Canvas e inventario documental.",
    "update_readme_tree.py": "Genera el mapa estructural, grafos DOT/SVG, Canvas y manifiesto del README.",
    "sync-repo.sh": "Punto de entrada para sincronizar el repositorio desde Termux.",

    # Documentación
    "docs/infrastructure.md": "Manual del manifiesto, historial, wrappers, notas y auditoría de infraestructura.",
    "docs/repository-map.md": "Mapa textual de la estructura del repositorio, generado automáticamente.",
    "docs/repository-structure.dot": "Fuente Graphviz del grafo jerárquico de archivos y directorios.",
    "docs/repository-structure.svg": "Visualización SVG de la estructura del repositorio.",
    "docs/repository-architecture.dot": "Fuente Graphviz de las relaciones funcionales principales.",
    "docs/repository-architecture.svg": "Visualización SVG de la arquitectura y automatización.",
    "docs/svg2canvas.py": "Convierte diagramas SVG en archivos Canvas compatibles con Obsidian.",
    "docs/conocimiento-4-termx.md": "Registro progresivo de hechos confirmados y conocimiento técnico del proyecto.",
    "docs/pendientes-evolucion.md": "Registro priorizado de mejoras y metodología de evolución pendiente.",
    "docs/canvas/repository-architecture.canvas": "Diagrama de arquitectura para explorar en Obsidian.",
    "docs/canvas/repository-structure.canvas": "Diagrama estructural para explorar en Obsidian.",

    # Sincronización y comandos
    "scripts/bajada": "Integra cambios de GitHub en Termux con rebase seguro y sincronización a Obsidian.",
    "scripts/subida": "Valida, prepara y publica cambios locales sin force push.",
    "scripts/install-sync-commands.sh": "Instala los comandos bajada y subida en el PATH de Termux.",
    "scripts/sync-canvas-to-obsidian.py": "Copia README y Canvas a Documents/4-TERMX y retira Canvas obsoletos.",
    "scripts/infra-git-sync.sh": "Reconcilia la infraestructura y sincroniza sus cambios con GitHub.",
    "scripts/infra-sync.sh": "Lanza el motor de reconciliación de infraestructura.",

    # Infraestructura como datos
    "infrastructure/system-manifest.json": "Instantánea observada de paquetes, runtimes y metadatos del entorno.",
    "infrastructure/desired-state.json": "Clasificación declarada de dependencias requeridas, opcionales y temporales.",
    "infrastructure/history/infrastructure-history.jsonl": "Historial estructurado de cambios de infraestructura detectados.",
    "infrastructure/history/package-operation-cursor.json": "Cursor para evitar reprocesar operaciones capturadas.",
    "infrastructure/history/pkg-operation-cursor.json": "Cursor de compatibilidad con el registro histórico de operaciones.",

    # Herramientas de auditoría y captura
    "scripts/infra-sync.py": "Detecta cambios entre instantáneas y reconcilia evidencia de operaciones.",
    "scripts/infra-audit.py": "Compara el estado observado con el estado deseado sin desinstalar paquetes.",
    "scripts/infra-note.py": "Registra explícitamente la razón, el actor y el alcance de una dependencia.",
    "scripts/infra-wrapper.sh": "Captura operaciones de gestores de paquetes en un registro JSONL.",
    "scripts/install-infra-wrappers.sh": "Instala wrappers de captura para los gestores disponibles.",
    "scripts/update_readme_tree.py": "Alias documental del generador, si existe en una futura estructura.",
    "CHANGELOG.md": "Historial cronológico de cambios publicados.",
    "CONTRIBUTING.md": "Normas para proponer, probar y documentar cambios.",
    "SECURITY.md": "Canal y pautas para reportar vulnerabilidades de forma responsable.",
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
    """Devuelve una descripción específica o una alternativa transparente."""
    if rel in DESCRIPTIONS:
        return DESCRIPTIONS[rel]
    if rel.startswith(".github/workflows/"):
        return "Workflow de automatización de GitHub Actions."
    if rel.startswith("docs/canvas/"):
        return "Diagrama Canvas de Obsidian generado desde la documentación visual."
    if rel.startswith("docs/"):
        return "Documento de referencia del proyecto; consultar su contenido para el detalle."
    if rel.startswith("infrastructure/history/"):
        return "Dato de historial o cursor utilizado por la reconciliación de infraestructura."
    if rel.startswith("infrastructure/"):
        return "Manifiesto de infraestructura; consultar el esquema y la documentación asociada."
    if rel.startswith("scripts/"):
        return "Script operativo; revisar su ayuda y código antes de ejecutarlo."
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
    if rel.startswith("."):
        return "Archivo de configuración del entorno o del control de versiones."
    return f"Archivo {file_type(Path(rel))}; descripción específica pendiente de documentar."

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
        parts = path.relative_to(ROOT).parts
        if rel.startswith(EXCLUDED_PREFIXES):
            continue
        if any(part in EXCLUDED_NAMES for part in parts):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if rel == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            continue
        if not include_generated and (
            rel in GENERATED_GRAPH_FILES or rel.startswith("docs/canvas/")
        ):
            continue
        result.append((rel, path.stat().st_size))
    return sorted(result)

def convert_svgs_to_canvas():
    """Regenera un Canvas homólogo por cada SVG de documentación."""
    if not SVG_TO_CANVAS.exists():
        raise FileNotFoundError(f"No existe el conversor: {SVG_TO_CANVAS}")

    CANVAS_DIR.mkdir(parents=True, exist_ok=True)
    svg_files = sorted((ROOT / "docs").glob("*.svg"))
    for svg in svg_files:
        output = CANVAS_DIR / f"{svg.stem}.canvas"
        subprocess.run(
            [
                "python",
                str(SVG_TO_CANVAS),
                str(svg),
                "-o",
                str(output),
                "--layout",
                "auto",
            ],
            check=True,
        )
        print(f"Canvas actualizado: {output.relative_to(ROOT)}")

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
    convert_svgs_to_canvas()

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
