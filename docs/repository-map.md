# 🌳 4-TERMX — Repository Map

> Generado automáticamente por GitHub Actions a partir de los archivos del repositorio.
> El árbol refleja rutas relativas; no incluye secretos ni artefactos excluidos.

## 🧭 Mapa estructural

```text
4-TERMX/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   ├── workflows/
│   │   ├── update-tree.yml
│   │   └── validate.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── .termux/
│   └── termux.properties
├── docs/
│   ├── architecture.md
│   ├── conocimiento-4-termx.md
│   ├── design-principles.md
│   ├── infrastructure.md
│   ├── pendientes-evolucion.md
│   ├── repository-map.md
│   └── svg2canvas.py
├── infrastructure/
│   ├── history/
│   │   ├── infrastructure-history.jsonl
│   │   ├── package-operation-cursor.json
│   │   └── pkg-operation-cursor.json
│   ├── desired-state.json
│   └── system-manifest.json
├── scripts/
│   ├── bajada
│   ├── infra-audit.py
│   ├── infra-git-sync.sh
│   ├── infra-note.py
│   ├── infra-sync.py
│   ├── infra-sync.sh
│   ├── infra-wrapper.sh
│   ├── install-infra-wrappers.sh
│   ├── install-sync-commands.sh
│   ├── subida
│   └── sync-canvas-to-obsidian.py
├── tests/
│   └── test_update_readme_tree.py
├── .gitconfig
├── .gitignore
├── .zshrc
├── CONTRIBUTING.md
├── README.md
├── SECURITY.md
├── sync-repo.sh
└── update_readme_tree.py
```

## 🗺️ Grafos estáticos

- [repository-structure.svg](./repository-structure.svg): grafo visual de la estructura de archivos y carpetas.
- [repository-architecture.svg](./repository-architecture.svg): relaciones funcionales entre GitHub Actions, el generador, README y la documentación.
- Los archivos DOT son las fuentes editables de ambos grafos.

> Los mapas SVG, sus fuentes DOT y los Canvas de Obsidian se regeneran desde el workflow del repositorio.
