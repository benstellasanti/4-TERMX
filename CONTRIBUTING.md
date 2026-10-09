# Guía de contribución

Gracias por tu interés en mejorar 4-TERMX. El objetivo es mantener un entorno Termux documentado, auditable y seguro, con cambios pequeños y verificables.

## Antes de modificar

1. Lee el [README](./README.md) y la documentación relevante en `docs/`.
2. Identifica los archivos que participan en el flujo que quieres cambiar.
3. Comprueba si el contenido está generado automáticamente. No edites manualmente el inventario delimitado por `FILE-MANIFEST:START` y `FILE-MANIFEST:END`; modifica `update_readme_tree.py` cuando corresponda.
4. No muevas ni renombres scripts sin revisar las rutas, los wrappers y los workflows que dependen de ellos.

## Flujo recomendado

1. Explica el problema y el resultado esperado.
2. Limita el cambio al alcance necesario.
3. Actualiza la documentación afectada.
4. Ejecuta las validaciones disponibles.
5. Revisa `git diff --check`, `git status` y el diff completo.
6. Describe en el commit qué cambió y por qué.

Para cambios mayores, abre primero un Issue o una propuesta de diseño. No es necesario imponer un flujo pesado a cambios documentales pequeños.

## Validaciones

Según el tipo de cambio:

- Python: comprobar sintaxis y ejecutar las pruebas disponibles.
- JSON: validar el formato y conservar el esquema esperado.
- Shell: revisar sintaxis y rutas de ejecución.
- Documentación: comprobar enlaces relativos y que las instrucciones coincidan con el código.
- Generador: confirmar que los mapas, Canvas y manifiesto se produzcan correctamente.

No declares una prueba como exitosa si no fue ejecutada. Anota las limitaciones de las pruebas que no se pudieron realizar.

## Seguridad y datos locales

- Nunca añadas tokens, contraseñas, claves privadas, archivos `.env` reales ni contenido de `~/.ssh/`.
- No incluyas registros locales que puedan contener datos sensibles.
- No conviertas la auditoría de infraestructura en desinstalación automática.
- No uses `git push --force` para resolver divergencias.
- Las acciones destructivas requieren una decisión explícita y una revisión de sus efectos.

## Estilo de cambios

- Prefiere nombres descriptivos y funciones con responsabilidades claras.
- Mantén separados los hechos observados, las decisiones declaradas y las inferencias.
- Conserva compatibilidad o documenta expresamente los cambios incompatibles.
- Evita añadir dependencias si la función puede resolverse con herramientas ya disponibles.

## Commits

Usa mensajes cortos y descriptivos, por ejemplo:

- `docs: aclarar el flujo de sincronización`
- `fix: validar el destino de Canvas`
- `test: comprobar el generador documental`

La contribución debe poder revisarse mediante su diff, su evidencia de validación y su documentación.
