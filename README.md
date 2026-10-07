# 📱 4-TERMX — Entorno de Desarrollo Móvil

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Termux%20%2F%2F%20Android-blue?style=for-the-badge&logo=android" alt="Termux">
  <img src="https://img.shields.io/badge/Shell-Zsh%20%2B%20Autosuggestions-green?style=for-the-badge&logo=gnu-bash" alt="Zsh">
  <img src="https://img.shields.io/badge/Git-Synced-orange?style=for-the-badge&logo=git" alt="Git">
</p>

> Repositorio personal de configuración, flujos de trabajo y experimentación en **Termux** para transformar un dispositivo Android en una estación de trabajo portátil eficiente.

---

## 🚀 Características del Entorno
* **Shell Optimizado:** Configurado con **Zsh** y autocompletado inteligente (`zsh-autosuggestions`).
* **Historial Persistente:** Gestión avanzada de comandos y persistencia extendida.
* **Control de Versiones:** Sincronización segura mediante claves SSH con GitHub.
* **Automatización:** Actualización en tiempo real del árbol de archivos mediante GitHub Actions.

---

## 🏗️ Infrastructure as Data

El entorno Termux se audita mediante un manifiesto estructurado y un historial de reconciliación:

- `infrastructure/system-manifest.json` — estado observado.
- `infrastructure/desired-state.json` — estado deseado.
- `infrastructure/history/infrastructure-history.jsonl` — cambios detectados.
- `scripts/infra-sync.py` — motor de auditoría.

El sistema detecta instalaciones, eliminaciones y cambios de versión aunque el cambio haya sido realizado manualmente. Cuando no existe información sobre el motivo, registra `actor: unknown` y `reason: null`; no inventa contexto.

La reconciliación se ejecuta automáticamente al iniciar Zsh.

## 🗺️ Repository Maps

El repositorio se representa automáticamente de **dos formas complementarias**:

### 1. 🌳 Estructura del repositorio

Muestra la jerarquía real: **directorios como ramas y archivos como hojas**.

![4-TERMX — Estructura del repositorio](./docs/repository-structure.svg)

[📄 Ver fuente DOT](./docs/repository-structure.dot)

### 2. 🧠 Arquitectura y relaciones

Muestra las relaciones funcionales principales: **GitHub → GitHub Actions → workflow → generador → README/docs**.

![4-TERMX — Arquitectura y relaciones](./docs/repository-architecture.svg)

[📄 Ver fuente DOT](./docs/repository-architecture.dot)

### 🔄 Actualización automática

~~~text
Nuevo archivo/directorio
        │
        ▼
     git push
        │
        ▼
 GitHub Actions
        │
        ├── descubre la estructura actual
        ├── genera el grafo estructural
        ├── genera el grafo de arquitectura
        ├── actualiza README.md
        └── actualiza el File Manifest
        │
        ▼
 Commit automático de documentación
~~~

**Actualización automática:** el workflow se ejecuta en cada push a main y también puede ejecutarse manualmente. Cuando agregues, modifiques o elimines archivos en main, los dos grafos se vuelven a generar a partir del estado real del repositorio.

Graphviz genera los SVG estáticos desde archivos DOT; ambos formatos quedan versionados dentro de docs/.

<!-- FILE-MANIFEST:START -->
## 📦 File Manifest Table

> **Generado automáticamente por GitHub Actions.** Representa los archivos visibles del repositorio; secretos y material SSH están excluidos.

| Estado | Archivo | Tipo | Tamaño | Función |
|---|---|---|---:|---|
| — | [<code>.gitconfig</code>](./.gitconfig) | Configuración | 64 B | Archivo Configuración del proyecto. |
| — | [<code>.github/workflows/update-tree.yml</code>](./.github/workflows/update-tree.yml) | GitHub Actions | 1.5 KB | Workflow de automatización de GitHub Actions. |
| — | [<code>.gitignore</code>](./.gitignore) | Configuración | 279 B | Archivo Configuración del proyecto. |
| — | [<code>.termux/termux.properties</code>](./.termux/termux.properties) | Archivo | 5.9 KB | Archivo Archivo del proyecto. |
| — | [<code>.zshrc</code>](./.zshrc) | Configuración | 84 B | Archivo Configuración del proyecto. |
| — | [<code>README.md</code>](./README.md) | Markdown | 6.5 KB | Documentación central del entorno Termux. |
| — | [<code>docs/repository-architecture.dot</code>](./docs/repository-architecture.dot) | Archivo | 2.1 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-architecture.svg</code>](./docs/repository-architecture.svg) | Archivo | 15.7 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-map.md</code>](./docs/repository-map.md) | Markdown | 740 B | Archivo Markdown del proyecto. |
| — | [<code>docs/repository-structure.dot</code>](./docs/repository-structure.dot) | Archivo | 1.7 KB | Archivo Archivo del proyecto. |
| — | [<code>docs/repository-structure.svg</code>](./docs/repository-structure.svg) | Archivo | 10.3 KB | Archivo Archivo del proyecto. |
| — | [<code>sync-repo.sh</code>](./sync-repo.sh) | Shell | 1.1 KB | Sincronización del repositorio desde Termux. |
| — | [<code>update_readme_tree.py</code>](./update_readme_tree.py) | Python | 12.8 KB | Generador automático del manifiesto y los dos grafos. |

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
<summary>📁 <strong>docs</strong> — 5 archivos / 30.4 KB</summary>

- [<code>docs/repository-architecture.dot</code>](./docs/repository-architecture.dot) — **2.1 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-architecture.svg</code>](./docs/repository-architecture.svg) — **15.7 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-map.md</code>](./docs/repository-map.md) — **740 B** — Archivo Markdown del proyecto.
- [<code>docs/repository-structure.dot</code>](./docs/repository-structure.dot) — **1.7 KB** — Archivo Archivo del proyecto.
- [<code>docs/repository-structure.svg</code>](./docs/repository-structure.svg) — **10.3 KB** — Archivo Archivo del proyecto.

</details>

<details>
<summary>📁 <strong>raíz</strong> — 6 archivos / 20.7 KB</summary>

- [<code>.gitconfig</code>](./.gitconfig) — **64 B** — Archivo Configuración del proyecto.
- [<code>.gitignore</code>](./.gitignore) — **279 B** — Archivo Configuración del proyecto.
- [<code>.zshrc</code>](./.zshrc) — **84 B** — Archivo Configuración del proyecto.
- [<code>README.md</code>](./README.md) — **6.5 KB** — Documentación central del entorno Termux.
- [<code>sync-repo.sh</code>](./sync-repo.sh) — **1.1 KB** — Sincronización del repositorio desde Termux.
- [<code>update_readme_tree.py</code>](./update_readme_tree.py) — **12.8 KB** — Generador automático del manifiesto y los dos grafos.

</details>

**Total actual:** 13 archivos — **58.5 KB**

_Este bloque es mantenido por Actions. No editar manualmente entre los marcadores._
<!-- FILE-MANIFEST:END -->
