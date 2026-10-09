# Arquitectura de 4-TERMX

## Propósito

4-TERMX mantiene configuración y automatizaciones para un entorno Termux en Android. El repositorio versionado en GitHub es la fuente de verdad para los archivos del proyecto; la carpeta compartida de Android es una proyección para consulta en Obsidian.

## Componentes

| Componente | Responsabilidad | Entradas principales | Salidas principales |
|---|---|---|---|
| `.github/workflows/validate.yml` | Ejecutar pruebas y validaciones con permisos de solo lectura | Código, pruebas y manifiestos JSON | Resultado de validación en GitHub Actions |
| `.github/workflows/update-tree.yml` | Validar y regenerar documentación en GitHub Actions | Archivos versionados | README actualizado, mapa, DOT/SVG y Canvas |
| `update_readme_tree.py` | Descubrir archivos y generar artefactos documentales | Árbol del repositorio y README | Inventario, mapa y grafos |
| `scripts/bajada` | Integrar cambios remotos en el clon Termux | Rama local y `origin/main` | Árbol local actualizado y copia de Obsidian |
| `scripts/subida` | Publicar cambios locales de forma controlada | Cambios locales revisados | Commit y push normal a GitHub |
| `scripts/sync-canvas-to-obsidian.py` | Copiar README y Canvas a almacenamiento compartido | README y `docs/canvas/` | `Documents/4-TERMX/` |
| `scripts/infra-sync.py` | Observar y reconciliar el estado de infraestructura | Inventario de gestores y registros de operación | Manifiesto e historial |
| `scripts/infra-audit.py` | Comparar lo observado con lo declarado | Manifiesto y estado deseado | Hallazgos de auditoría |
| `scripts/infra-note.py` | Registrar intención conocida | Gestor, paquete, motivo y alcance | Nota local estructurada |

## Flujos principales

### Documentación automática

1. Un cambio llega a la rama `main`.
2. `validate.yml` ejecuta pruebas unitarias y validaciones estáticas con permisos de solo lectura.
3. `update-tree.yml` vuelve a validar antes de generar documentación y dispone de permisos de escritura solo para publicar artefactos generados.
4. El generador descubre los archivos que deben documentarse.
5. Graphviz genera las visualizaciones SVG desde sus fuentes DOT.
6. El conversor crea los Canvas asociados.
7. El generador actualiza el mapa y el bloque de inventario del README.
8. Si hay cambios generados, el workflow los versiona con un commit de bot.

### GitHub a Termux y Obsidian

1. `bajada` comprueba que se ejecuta dentro del repositorio y en la rama esperada.
2. Consulta el remoto y evalúa si hay cambios, cambios locales o divergencia.
3. Integra mediante rebase cuando es seguro; ante conflictos se detiene para intervención.
4. Después de integrar, copia el README y los Canvas a `~/storage/shared/Documents/4-TERMX/`.

### Termux a GitHub

1. `subida` revisa cambios, errores de whitespace y estado remoto.
2. Prepara cambios locales excluyendo el almacenamiento local `storage/`.
3. Crea un commit si hay cambios y aplica rebase cuando sea necesario.
4. Solo realiza push normal cuando el historial puede avanzar de forma segura.
5. No utiliza force push como mecanismo de recuperación.

### Infraestructura como datos

- **Observado:** `infrastructure/system-manifest.json`.
- **Deseado:** `infrastructure/desired-state.json`.
- **Histórico:** `infrastructure/history/infrastructure-history.jsonl`.
- **Intención local:** notas de razón/actor en el entorno Termux.
- **Auditoría:** comparación del estado observado con la clasificación declarada.

Un elemento no clasificado no debe eliminarse automáticamente. El historial conserva la evidencia disponible, pero no prueba por sí solo la causalidad absoluta.

## Límites y precauciones

- El estado y los registros locales de Termux pueden contener información que no debe versionarse.
- La copia en Documents es una proyección para Obsidian, no un clon Git independiente.
- Los cambios de estructura requieren revisar las rutas relativas y los workflows.
- Las pruebas automáticas de sintaxis no sustituyen pruebas funcionales en Termux.
- La política de sincronización preserva conflictos para revisión humana; no promete resolver automáticamente toda divergencia.

## Fuentes de implementación

- [Workflow de documentación](../.github/workflows/update-tree.yml)
- [Generador de mapas e inventario](../update_readme_tree.py)
- [Sincronización segura](../scripts/bajada) · [subida](../scripts/subida)
- [Infraestructura como datos](./infrastructure.md)
- [Principios de diseño](./design-principles.md)
