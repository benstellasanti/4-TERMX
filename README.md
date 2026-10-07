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

## 📊 Arquitectura del Flujo de Trabajo

```mermaid
graph TD
    A[PC Windows / VS Code] -->|SSH Port 8022| B(Termux en Android)
    B -->|Zsh + Autosuggestions| C[Entorno Local]
    C -->|Git & SSH Keys & GitHub Actions| D((GitHub Repository))
    style B fill:#36BCF7,stroke:#333,stroke-width:2px
    style D fill:#3fb950,stroke:#333,stroke-width:2px

<!-- FILE-MANIFEST:START -->
## 📦 File Manifest Table

> **Generado automáticamente por GitHub Actions.** Esta tabla representa el estado actual de los archivos rastreados del repositorio.

| Estado | Archivo | Tipo | Tamaño | Función |
|---|---|---|---:|---|
| — | [<code>.gitconfig</code>](./.gitconfig) | Configuración | 64 B | Archivo Configuración del proyecto. |
| — | [<code>.github/workflows/update-tree.yml</code>](./.github/workflows/update-tree.yml) | GitHub Actions | 975 B | Workflow de automatización de GitHub Actions. |
| — | [<code>.ssh/authorized_keys</code>](./.ssh/authorized_keys) | Archivo | 0 B | Archivo Archivo del proyecto. |
| — | [<code>.ssh/id_ed25519</code>](./.ssh/id_ed25519) | Archivo | 419 B | Archivo Archivo del proyecto. |
| — | [<code>.ssh/id_ed25519.pub</code>](./.ssh/id_ed25519.pub) | Archivo | 106 B | Archivo Archivo del proyecto. |
| — | [<code>.ssh/known_hosts</code>](./.ssh/known_hosts) | Archivo | 828 B | Archivo Archivo del proyecto. |
| — | [<code>.ssh/known_hosts.old</code>](./.ssh/known_hosts.old) | Archivo | 92 B | Archivo Archivo del proyecto. |
| — | [<code>.termux/termux.properties</code>](./.termux/termux.properties) | Archivo | 5.9 KB | Archivo Archivo del proyecto. |
| — | [<code>.termux_authinfo</code>](./.termux_authinfo) | Configuración | 20 B | Archivo Configuración del proyecto. |
| — | [<code>.zshrc</code>](./.zshrc) | Configuración | 84 B | Archivo Configuración del proyecto. |
| — | [<code>README.md</code>](./README.md) | Markdown | 1.4 KB | Documentación central del entorno Termux. |
| — | [<code>sync-repo.sh</code>](./sync-repo.sh) | Shell | 1.1 KB | Archivo Shell del proyecto. |
| — | [<code>update_readme_tree.py</code>](./update_readme_tree.py) | Python | 5.7 KB | Generador automático del File Manifest del README. |

### 📂 Bloques colapsables por componente

<details>
<summary>📁 <strong>.github</strong> — 1 archivos / 975 B</summary>

- [<code>.github/workflows/update-tree.yml</code>](./.github/workflows/update-tree.yml) — **975 B** — Workflow de automatización de GitHub Actions.

</details>

<details>
<summary>📁 <strong>.ssh</strong> — 5 archivos / 1.4 KB</summary>

- [<code>.ssh/authorized_keys</code>](./.ssh/authorized_keys) — **0 B** — Archivo Archivo del proyecto.
- [<code>.ssh/id_ed25519</code>](./.ssh/id_ed25519) — **419 B** — Archivo Archivo del proyecto.
- [<code>.ssh/id_ed25519.pub</code>](./.ssh/id_ed25519.pub) — **106 B** — Archivo Archivo del proyecto.
- [<code>.ssh/known_hosts</code>](./.ssh/known_hosts) — **828 B** — Archivo Archivo del proyecto.
- [<code>.ssh/known_hosts.old</code>](./.ssh/known_hosts.old) — **92 B** — Archivo Archivo del proyecto.

</details>

<details>
<summary>📁 <strong>.termux</strong> — 1 archivos / 5.9 KB</summary>

- [<code>.termux/termux.properties</code>](./.termux/termux.properties) — **5.9 KB** — Archivo Archivo del proyecto.

</details>

<details>
<summary>📁 <strong>raíz</strong> — 6 archivos / 8.3 KB</summary>

- [<code>.gitconfig</code>](./.gitconfig) — **64 B** — Archivo Configuración del proyecto.
- [<code>.termux_authinfo</code>](./.termux_authinfo) — **20 B** — Archivo Configuración del proyecto.
- [<code>.zshrc</code>](./.zshrc) — **84 B** — Archivo Configuración del proyecto.
- [<code>README.md</code>](./README.md) — **1.4 KB** — Documentación central del entorno Termux.
- [<code>sync-repo.sh</code>](./sync-repo.sh) — **1.1 KB** — Archivo Shell del proyecto.
- [<code>update_readme_tree.py</code>](./update_readme_tree.py) — **5.7 KB** — Generador automático del File Manifest del README.

</details>

**Total actual:** 13 archivos — **16.5 KB**

_Este bloque es mantenido por Actions. No editar manualmente entre los marcadores._
<!-- FILE-MANIFEST:END -->
