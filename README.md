---

## 📊 Arquitectura del Flujo de Trabajo

```mermaid
graph TD
    A[PC Windows / VS Code] -->|SSH Port 8022| B(Termux en Android)
    B -->|Zsh + Autosuggestions| C[Entorno Local]
    C -->|Git & SSH Keys| D((GitHub Repository))
    style B fill:#36BCF7,stroke:#333,stroke-width:2px
    style D fill:#3fb950,stroke:#333,stroke-width:2px
