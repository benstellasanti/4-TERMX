# Principios de diseño — 4-TERMX

Estos principios orientan la evolución del repositorio y sus automatizaciones.

## 1. Evidencia antes que inferencia

Distinguir lo observado de lo declarado y de lo inferido. Si no hay evidencia suficiente, usar valores desconocidos o nulos en lugar de inventar un motivo, actor o causalidad.

## 2. Estado observado y estado deseado son distintos

`system-manifest.json` describe lo detectado en el entorno. `desired-state.json` expresa la intención declarada. No deben tratarse como fuentes intercambiables.

## 3. No administrado no significa prescindible

Una dependencia ausente del estado deseado debe revisarse, no eliminarse automáticamente. El uso real, las dependencias transitivas y el contexto deben evaluarse antes de tomar una decisión.

## 4. Automatización segura y reversible

La automatización debe validar su contexto, preservar los cambios locales y detenerse cuando no puede resolver un conflicto con seguridad. La sincronización no debe recurrir a un push forzado como solución automática.

## 5. Fuente de verdad y proyecciones

GitHub es la fuente versionada de los archivos del proyecto. Los Canvas y la copia del README en Documents/4-TERMX son proyecciones para consulta en Obsidian, no un segundo repositorio Git.

## 6. Generado significa reproducible

Los mapas, Canvas y bloques de inventario deben derivarse de sus fuentes y generadores. Los bloques generados se modifican actualizando el generador, no editando manualmente su resultado.

## 7. Seguridad por defecto

No almacenar credenciales ni claves privadas. Los workflows deben tener permisos limitados, y los scripts deben explicar sus efectos y detenerse ante condiciones inseguras.

## 8. Trazabilidad práctica

Los cambios importantes deben poder relacionarse con su objetivo, archivos, validaciones y commit. La documentación debe ayudar tanto a una persona como a una IA a reconstruir el contexto sin depender de memoria informal.

## 9. Cambios pequeños y verificables

Preferir cambios acotados, con pruebas y documentación proporcionales al riesgo. No afirmar que una validación pasó si no se ejecutó.

## 10. Documentar límites

Explicar qué detecta el sistema, qué no puede confirmar y qué requiere revisión humana. Una observación histórica no equivale a una prueba perfecta del pasado.
