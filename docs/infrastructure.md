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

### Captura temporal de operaciones pkg

Las operaciones mutables de `pkg` se interceptan mediante un wrapper ubicado en:

    ~/.local/bin/pkg

El wrapper registra prospectivamente las operaciones de instalación, eliminación,
reinstalación y actualización en:

    ~/.infra-pkg-operations.log

El registro contiene:

- `occurred_at`: momento en que comenzó la operación.
- `action`: operación solicitada.
- `command`: comando ejecutado.

`infra-sync.py` utiliza este registro como evidencia adicional para correlacionar
los cambios observados en el estado del sistema.

El historial distingue:

- `occurred_at`: momento de la operación capturado por el wrapper.
- `detected_at`: momento en que `infra-sync.py` detectó el cambio.
- `occurred_at_source`: fuente de la evidencia temporal.

Una operación `pkg update` no se utiliza como explicación directa de una instalación,
eliminación o actualización de paquetes, porque solo actualiza los índices de paquetes.

### Cursor de procesamiento

Las operaciones ya procesadas no se vuelven a utilizar en reconciliaciones posteriores.

El cursor persistente se encuentra en:

    infrastructure/history/pkg-operation-cursor.json

El archivo de operaciones original no se elimina después de procesarlo. El cursor
permite conservar la evidencia bruta y, al mismo tiempo, evitar reprocesamientos.

### Limitaciones actuales

La captura temporal es prospectiva: operaciones realizadas antes de instalar el
wrapper pueden no tener `occurred_at` verificable.

El sistema tampoco inventa:

- `actor`
- `reason`

Cuando estos datos no existen en una fuente confiable permanecen como `unknown` o
`null`.

La correlación actual está implementada para `pkg`. Los gestores `pip`, `npm` y
`gem` continúan siendo observados mediante comparación de estado, pero todavía no
tienen captura prospectiva equivalente.

## Auditoría IA

Para responder qué puedo limpiar, un agente debe cruzar estado actual, estado deseado, historial y dependencias reales. Un paquete ausente del estado deseado no implica automáticamente que sea seguro eliminarlo.

## Seguridad

Nunca almacenar aquí claves privadas, tokens, contraseñas, .termux_authinfo, valores de entorno ni contenido de ~/.ssh/.
