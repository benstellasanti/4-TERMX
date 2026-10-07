# 4-TERMX — Manifiesto de Infraestructura

## Modelo

- system-manifest.json: estado observado actual.
- desired-state.json: intención declarada.
- infrastructure-history.jsonl: historial de cambios detectados.
- infra-sync.py: motor de reconciliación.

## Detección

Se comparan paquetes pkg/dpkg, Python/pip, npm global y gems de Ruby cuando existen. También se registran versiones de runtimes, arquitectura, metadatos básicos y nombres de perfiles SSH sin registrar claves.

Si una persona o agente instala algo manualmente y no declara el motivo, el sistema registra el hecho con actor unknown, source reconciliation, confidence detected y reason null. No inventa explicaciones.

## Automatización

Primera ejecución segura:

    $HOME/scripts/infra-sync.sh --no-git

Ejecución normal:

    $HOME/scripts/infra-sync.sh

La ejecución normal crea un commit solo cuando existe una observación inicial o un cambio detectado.

## Auditoría IA

Para responder qué puedo limpiar, un agente debe cruzar estado actual, estado deseado, historial y dependencias reales. Un paquete ausente del estado deseado no implica automáticamente que sea seguro eliminarlo.

## Seguridad

Nunca almacenar aquí claves privadas, tokens, contraseñas, .termux_authinfo, valores de entorno ni contenido de ~/.ssh/.
