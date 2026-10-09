# 4-TERMX — Entorno de desarrollo móvil en Termux

[![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Android-2ea44f?logo=android&logoColor=white)](https://termux.dev/)
[![Shell](https://img.shields.io/badge/shell-Zsh-informational?logo=zsh&logoColor=white)](https://www.zsh.org/)
[![Automation](https://img.shields.io/badge/automation-GitHub%20Actions-blue?logo=githubactions&logoColor=white)](./.github/workflows/update-tree.yml)

**4-TERMX** reúne configuración, automatización y documentación para mantener un entorno de trabajo reproducible en Termux/Android. Incluye sincronización Git segura, documentación visual del repositorio y un sistema de observación de infraestructura mediante manifiestos e historial estructurado.

> El repositorio está diseñado para registrar y auditar cambios. No elimina paquetes automáticamente ni debe tratarse como una copia de seguridad de credenciales.

## Contenido

- [Qué incluye](#qué-incluye)
- [Requisitos](#requisitos)
- [Inicio rápido](#inicio-rápido)
- [Comandos habituales](#comandos-habituales)
- [Infraestructura como datos](#infraestructura-como-datos)
- [Documentación y mapas](#documentación-y-mapas)
- [Seguridad y límites](#seguridad-y-límites)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Estado y evolución](#estado-y-evolución)

## Qué incluye

- **Sincronización Git con controles:** `scripts/bajada` integra cambios desde GitHub; `scripts/subida` prepara y publica cambios locales. Ambos comprueban el estado del repositorio y se detienen ante conflictos en vez de forzar un push.
- **Vista para Obsidian:** `scripts/sync-canvas-to-obsidian.py` copia el README y los Canvas de documentación al directorio compartido de Android.
- **Infraestructura como datos:** manifiesto del estado observado, estado deseado, historial de cambios y auditoría de paquetes.
- **Documentación generada:** GitHub Actions actualiza el inventario y los mapas del repositorio cuando corresponde.

## Requisitos

- Android con [Termux](https://termux.dev/) instalado.
- Git y Python disponibles en Termux.
- Acceso configurado al repositorio de GitHub para las operaciones remotas.
- Para regenerar los grafos localmente: Python, Graphviz (`dot`) y las dependencias que use el conversor SVG/Canvas.

Los comandos y rutas se orientan al entorno Termux. No ejecutes scripts de configuración en otro sistema sin revisar primero sus rutas y requisitos.

## Inicio rápido

Desde la raíz local del repositorio:

```bash
git status
git pull --rebase origin main
bash scripts/bajada
```

La última orden ejecuta la bajada segura y sincroniza el README y los archivos Canvas hacia:

```text
~/storage/shared/Documents/4-TERMX/
```

Para publicar cambios locales, revisa primero qué se modificará:

```bash
git status --short
git diff
bash scripts/subida
```

No ejecutes `git push --force` como parte de este flujo. Si el script se detiene por un conflicto, revisa `git status` y resuelve la situación antes de continuar.

## Comandos habituales

| Objetivo | Comando |
|---|---|
| Descargar e integrar cambios | `bash scripts/bajada` |
| Publicar cambios locales | `bash scripts/subida` |
| Sincronizar README y Canvas a Obsidian | `python scripts/sync-canvas-to-obsidian.py` |
| Actualizar el manifiesto local | `python scripts/infra-sync.py` |
| Auditar estado observado frente al deseado | `python scripts/infra-audit.py` |
| Registrar la razón de una dependencia | `python scripts/infra-note.py --help` |

Ejecuta los comandos desde la raíz del repositorio. Consulta la documentación de cada script y comprueba sus opciones antes de automatizarlo.

## Infraestructura como datos

El sistema distingue entre lo observado y lo declarado:

- `infrastructure/system-manifest.json`: estado observado del entorno.
- `infrastructure/desired-state.json`: clasificación deseada de dependencias.
- `infrastructure/history/infrastructure-history.jsonl`: eventos de cambios detectados.
- `scripts/infra-sync.py`: reconciliación del estado.
- `scripts/infra-audit.py`: comparación con el estado deseado.
- `scripts/infra-note.py`: registro de actor, motivo y clasificación cuando se conocen.

Si no hay evidencia suficiente, el sistema no inventa la intención: puede registrar actor desconocido y motivo nulo. Un paquete clasificado como `unmanaged` no es automáticamente seguro de eliminar. La auditoría informa; no desinstala paquetes.

Guía completa: [docs/infrastructure.md](./docs/infrastructure.md).

## Documentación y mapas

- [Mapa del repositorio](./docs/repository-map.md)
- [Estructura del repositorio (SVG)](./docs/repository-structure.svg) · [fuente DOT](./docs/repository-structure.dot)
- [Arquitectura y relaciones (SVG)](./docs/repository-architecture.svg) · [fuente DOT](./docs/repository-architecture.dot)
- [Conocimiento del proyecto](./docs/conocimiento-4-termx.md)
- [Pendientes de evolución](./docs/pendientes-evolucion.md)
- [Workflow de generación documental](./.github/workflows/update-tree.yml)

Los mapas, el inventario y los Canvas relacionados son artefactos generados. Para cambiar su lógica, modifica el generador o la fuente correspondiente; evita editar manualmente los bloques generados.

## Seguridad y límites

- No guardes contraseñas, tokens, claves privadas, archivos `.env` reales ni contenido de `~/.ssh/` en el repositorio.
- Revisa `git diff` y `git status` antes de publicar cambios.
- La captura de operaciones es prospectiva: los cambios anteriores a instalar los wrappers pueden no tener una marca temporal fiable.
- El historial representa observaciones y evidencias disponibles; no demuestra causalidad absoluta.
- No elimines dependencias solo porque no aparezcan en el estado deseado.
- Los scripts de sincronización no sustituyen una copia de seguridad.

## Estructura del repositorio

```text
.github/workflows/   Automatización de documentación
.termux/             Configuración específica de Termux
docs/                Guías, mapas, fuentes visuales y Canvas
infrastructure/      Manifiestos y registros de estado
scripts/              Sincronización, auditoría y utilidades
.zshrc                Configuración de inicio de Zsh
.gitignore            Exclusiones de Git y protección básica
README.md             Guía principal del proyecto
```

El inventario detallado generado automáticamente se mantiene al final de este README.

## Estado y evolución

El proyecto continúa en evolución. Las mejoras planificadas están documentadas en [docs/pendientes-evolucion.md](./docs/pendientes-evolucion.md). Las tareas pendientes describen trabajo futuro y no implican necesariamente que una función existente esté rota.

---

<!-- FILE-MANIFEST:START -->
## 📦 File Manifest Table

> **Generado automáticamente por GitHub Actions.** Representa los archivos visibles del repositorio; secretos y material SSH están excluidos.

| Estado | Archivo | Tipo | Tamaño | Función |
|---|---|---|---:|---|
| — | [<code>.gitconfig</code>](./.gitconfig) | Configuración | 64 B | Archivo Configuración del proyecto. |
| — | [<code>.github/workflows/update-tree.yml</code>](./.github/workflows/update-tree.yml) | GitHub Actions | 1.5 KB | Workflow de automatización de GitHub Actions. |
| — | [<code>.gitignore</code>](./.gitignore) | Configuración | 398 B | Archivo Configuración del proyecto. |
| — | [<code>.termux/termux.properties</code>](./.termux/termux.properties) | Archivo | 5.9 KB | Archivo Archivo del proyecto. |
| — | [<code>.zshrc</code>](./.zshrc) | Configuración | 319 B | Archivo Configuración del proyecto. |
| — | [<code>README.md</code>](./README.md) | Markdown | 16.5 KB | Documentación central del entorno Termux. |
| — | [<code>docs/canvas/repository-architecture.canvas</code>](./docs/canvas/repository-architecture.canvas) | Archivo | 8.4 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/canvas/repository-structure.canvas</code>](./docs/canvas/repository-structure.canvas) | Archivo | 12.2 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/conocimiento-4-termx.md</code>](./docs/conocimiento-4-termx.md) | Markdown | 2.4 KB | Archivo Markdown del proyecto. |
| — | [<code>docs/infrastructure.md</code>](./docs/infrastructure.md) | Markdown | 4.7 KB | Archivo Markdown del proyecto. |
| — | [<code>docs/pendientes-evolucion.md</code>](./docs/pendientes-evolucion.md) | Markdown | 7.5 KB | Archivo Markdown del proyecto. |
| — | [<code>docs/repository-architecture.dot</code>](./docs/repository-architecture.dot) | Archivo | 2.7 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-architecture.svg</code>](./docs/repository-architecture.svg) | Archivo | 21.3 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-map.md</code>](./docs/repository-map.md) | Markdown | 1.2 KB | Archivo Markdown del proyecto. |
| — | [<code>docs/repository-structure.dot</code>](./docs/repository-structure.dot) | Archivo | 4.8 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-structure.svg</code>](./docs/repository-structure.svg) | Archivo | 29.7 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/svg2canvas.py</code>](./docs/svg2canvas.py) | Python | 12.4 KB | Archivo Python del proyecto. |
| — | [<code>infrastructure/desired-state.json</code>](./infrastructure/desired-state.json) | JSON | 597 B | Archivo JSON del proyecto. |
| — | [<code>infrastructure/history/infrastructure-history.jsonl</code>](./infrastructure/history/infrastructure-history.jsonl) | Archivo | 2.6 KB | Archivo Archivo del proyecto. |
| — | [<code>infrastructure/history/package-operation-cursor.json</code>](./infrastructure/history/package-operation-cursor.json) | JSON | 54 B | Archivo JSON del proyecto. |
| — | [<code>infrastructure/history/pkg-operation-cursor.json</code>](./infrastructure/history/pkg-operation-cursor.json) | JSON | 54 B | Archivo JSON del proyecto. |
| — | [<code>infrastructure/system-manifest.json</code>](./infrastructure/system-manifest.json) | JSON | 4.2 KB | Archivo JSON del proyecto. |
| — | [<code>scripts/bajada</code>](./scripts/bajada) | Archivo | 4.6 KB | Archivo Archivo del proyecto. |
| — | [<code>scripts/infra-audit.py</code>](./scripts/infra-audit.py) | Python | 2.2 KB | Archivo Python del proyecto. |
| — | [<code>scripts/infra-git-sync.sh</code>](./scripts/infra-git-sync.sh) | Shell | 463 B | Archivo Shell del proyecto. |
| — | [<code>scripts/infra-note.py</code>](./scripts/infra-note.py) | Python | 1.1 KB | Archivo Python del proyecto. |
| — | [<code>scripts/infra-sync.py</code>](./scripts/infra-sync.py) | Python | 13.8 KB | Archivo Python del proyecto. |
| — | [<code>scripts/infra-sync.sh</code>](./scripts/infra-sync.sh) | Shell | 181 B | Archivo Shell del proyecto. |
| — | [<code>scripts/infra-wrapper.sh</code>](./scripts/infra-wrapper.sh) | Shell | 884 B | Archivo Shell del proyecto. |
| — | [<code>scripts/install-infra-wrappers.sh</code>](./scripts/install-infra-wrappers.sh) | Shell | 840 B | Archivo Shell del proyecto. |
| — | [<code>scripts/install-sync-commands.sh</code>](./scripts/install-sync-commands.sh) | Shell | 584 B | Archivo Shell del proyecto. |
| — | [<code>scripts/subida</code>](./scripts/subida) | Archivo | 4.2 KB | Archivo Archivo del proyecto. |
| — | [<code>scripts/sync-canvas-to-obsidian.py</code>](./scripts/sync-canvas-to-obsidian.py) | Python | 1.8 KB | Archivo Python del proyecto. |
| — | [<code>sync-repo.sh</code>](./sync-repo.sh) | Shell | 1.1 KB | Sincronización del repositorio desde Termux. |
| — | [<code>update_readme_tree.py</code>](./update_readme_tree.py) | Python | 13.6 KB | Generador automático del manifiesto y los dos grafos. |

### 📂 Bloques colapsables por componente

<details>
<summary>📁 <strong>.github</strong> — 1 archivos / 1.5 KB</summary>

- [<code>.github/workflows/update-tree.yml</code>](./.github/workflows/update-tree.yml) — **1.5 KB** — Workflow de automatización de GitHub Actions.

</details>

<details>
<summary>📁 <strong>.termux</strong> — 1 archivos / 5.9 KB</summary>

- [<code>.termux/termux.properties</code>](./.termux/termux.properties) — **5.9 KB** — Archivo Archivo del proyecto.

</details>

<details>
<summary>📁 <strong>docs</strong> — 11 archivos / 107.1 KB</summary>

- [<code>docs/canvas/repository-architecture.canvas</code>](./docs/canvas/repository-architecture.canvas) — **8.4 KB** — Archivo Archivo del proyecto.
- [<code>docs/canvas/repository-structure.canvas</code>](./docs/canvas/repository-structure.canvas) — **12.2 KB** — Archivo Archivo del proyecto.
- [<code>docs/conocimiento-4-termx.md</code>](./docs/conocimiento-4-termx.md) — **2.4 KB** — Archivo Markdown del proyecto.
- [<code>docs/infrastructure.md</code>](./docs/infrastructure.md) — **4.7 KB** — Archivo Markdown del proyecto.
- [<code>docs/pendientes-evolucion.md</code>](./docs/pendientes-evolucion.md) — **7.5 KB** — Archivo Markdown del proyecto.
- [<code>docs/repository-architecture.dot</code>](./docs/repository-architecture.dot) — **2.7 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-architecture.svg</code>](./docs/repository-architecture.svg) — **21.3 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-map.md</code>](./docs/repository-map.md) — **1.2 KB** — Archivo Markdown del proyecto.
- [<code>docs/repository-structure.dot</code>](./docs/repository-structure.dot) — **4.8 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-structure.svg</code>](./docs/repository-structure.svg) — **29.7 KB** — Archivo Archivo del proyecto.
- [<code>docs/svg2canvas.py</code>](./docs/svg2canvas.py) — **12.4 KB** — Archivo Python del proyecto.

</details>

<details>
<summary>📁 <strong>infrastructure</strong> — 5 archivos / 7.5 KB</summary>

- [<code>infrastructure/desired-state.json</code>](./infrastructure/desired-state.json) — **597 B** — Archivo JSON del proyecto.
- [<code>infrastructure/history/infrastructure-history.jsonl</code>](./infrastructure/history/infrastructure-history.jsonl) — **2.6 KB** — Archivo Archivo del proyecto.
- [<code>infrastructure/history/package-operation-cursor.json</code>](./infrastructure/history/package-operation-cursor.json) — **54 B** — Archivo JSON del proyecto.
- [<code>infrastructure/history/pkg-operation-cursor.json</code>](./infrastructure/history/pkg-operation-cursor.json) — **54 B** — Archivo JSON del proyecto.
- [<code>infrastructure/system-manifest.json</code>](./infrastructure/system-manifest.json) — **4.2 KB** — Archivo JSON del proyecto.

</details>

<details>
<summary>📁 <strong>raíz</strong> — 6 archivos / 32.0 KB</summary>

- [<code>.gitconfig</code>](./.gitconfig) — **64 B** — Archivo Configuración del proyecto.
- [<code>.gitignore</code>](./.gitignore) — **398 B** — Archivo Configuración del proyecto.
- [<code>.zshrc</code>](./.zshrc) — **319 B** — Archivo Configuración del proyecto.
- [<code>README.md</code>](./README.md) — **16.5 KB** — Documentación central del entorno Termux.
- [<code>sync-repo.sh</code>](./sync-repo.sh) — **1.1 KB** — Sincronización del repositorio desde Termux.
- [<code>update_readme_tree.py</code>](./update_readme_tree.py) — **13.6 KB** — Generador automático del manifiesto y los dos grafos.

</details>

<details>
<summary>📁 <strong>scripts</strong> — 11 archivos / 30.6 KB</summary>

- [<code>scripts/bajada</code>](./scripts/bajada) — **4.6 KB** — Archivo Archivo del proyecto.
- [<code>scripts/infra-audit.py</code>](./scripts/infra-audit.py) — **2.2 KB** — Archivo Python del proyecto.
- [<code>scripts/infra-git-sync.sh</code>](./scripts/infra-git-sync.sh) — **463 B** — Archivo Shell del proyecto.
- [<code>scripts/infra-note.py</code>](./scripts/infra-note.py) — **1.1 KB** — Archivo Python del proyecto.
- [<code>scripts/infra-sync.py</code>](./scripts/infra-sync.py) — **13.8 KB** — Archivo Python del proyecto.
- [<code>scripts/infra-sync.sh</code>](./scripts/infra-sync.sh) — **181 B** — Archivo Shell del proyecto.
- [<code>scripts/infra-wrapper.sh</code>](./scripts/infra-wrapper.sh) — **884 B** — Archivo Shell del proyecto.
- [<code>scripts/install-infra-wrappers.sh</code>](./scripts/install-infra-wrappers.sh) — **840 B** — Archivo Shell del proyecto.
- [<code>scripts/install-sync-commands.sh</code>](./scripts/install-sync-commands.sh) — **584 B** — Archivo Shell del proyecto.
- [<code>scripts/subida</code>](./scripts/subida) — **4.2 KB** — Archivo Archivo del proyecto.
- [<code>scripts/sync-canvas-to-obsidian.py</code>](./scripts/sync-canvas-to-obsidian.py) — **1.8 KB** — Archivo Python del proyecto.

</details>

**Total actual:** 35 archivos — **184.7 KB**

_Este bloque es mantenido por Actions. No editar manualmente entre los marcadores._
<!-- FILE-MANIFEST:END -->
