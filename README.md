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
* **Conectividad:** Acceso remoto seguro vía SSH desde entornos de escritorio.

---

## 📊 Arquitectura del Flujo de Trabajo

```mermaid
graph TD
    A[PC Windows / VS Code] -->|SSH Port 8022| B(Termux en Android)
    B -->|Zsh + Autosuggestions| C[Entorno Local]
    C -->|Git & SSH Keys| D((GitHub Repository))
    style B fill:#36BCF7,stroke:#333,stroke-width:2px
    style D fill:#3fb950,stroke:#333,stroke-width:2px
