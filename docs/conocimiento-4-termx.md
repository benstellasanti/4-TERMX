# 4-TERMX — Conocimiento y descubrimiento del repositorio

> Documento vivo de referencia. Se actualiza a medida que investigamos el repositorio, para evitar repetir consultas y conservar el conocimiento adquirido.

## 1. Punto de partida

Fecha de inicio: 2026-10-07.

Este documento parte de la premisa de que el lector **desconoce 4-TERMX**. La finalidad es explicar progresivamente qué es, qué contiene, cómo se relacionan sus componentes, cómo se utiliza y cómo conservar su trazabilidad.

## 2. Primera evidencia confirmada

El repositorio contiene un mapa estructural documentado en `docs/repository-map.md`.

Ese mapa indica que la estructura actual incluye:

- `.github/`: automatización mediante GitHub Actions.
- `.termux/`: configuración y archivos propios de Termux.
- `docs/`: documentación del proyecto.
- `infrastructure/`: estado deseado e información histórica de infraestructura.
- `scripts/`: scripts de auditoría, sincronización, notas y mantenimiento.

Dentro de `infrastructure/history/` existen actualmente tres archivos:

- `infrastructure-history.jsonl`
- `pkg-operation-cursor.json`
- `system-manifest.json`

## 3. Visualizaciones existentes

El mapa documenta dos visualizaciones:

- `repository-structure.svg`: estructura completa del repositorio.
- `repository-architecture.svg`: relaciones funcionales entre GitHub, Actions, workflow, generador, README y `docs/`.

Según el propio mapa, estas visualizaciones y sus fuentes DOT se regeneran automáticamente cuando cambia el repositorio.

## 4. Cómo continuaremos la investigación

Cada descubrimiento relevante se incorporará a este documento, procurando distinguir entre:

1. **Hecho confirmado:** información observada directamente en el repositorio.
2. **Interpretación:** explicación de lo que significa ese hecho.
3. **Uso:** cómo utilizar ese componente.
4. **Evidencia:** archivo, registro o mecanismo que permite comprobarlo.

No se incorporarán afirmaciones sobre el funcionamiento que no hayan sido verificadas.

## 5. Próximo punto de investigación

La primera pregunta funcional será:

> **¿Qué es 4-TERMX y qué problema resuelve?**

Después se documentarán, en orden, su estructura, arquitectura, componentes, flujo de ejecución, auditoría, sincronización, historial, evidencias y procedimiento de evolución.

---

## Fuentes iniciales

- `docs/repository-map.md` — mapa estructural actual del repositorio.
