# 4-TERMX — Manifiesto de Infraestructura

## Modelo

- infrastructure/system-manifest.json: estado observado actual.
- infrastructure/desired-state.json: intención declarada.
- infrastructure/history/infrastructure-history.jsonl: historial de cambios.
- scripts/infra-sync.py: motor de reconciliación.
- scripts/infra-audit.py: auditoría de estado contra intención.
- scripts/infra-note.py: registro explícito de razón/actor.
- scripts/install-infra-wrappers.sh: instalación de capturadores prospectivos.
- scripts/infra-git-sync.sh: reconciliación + commit + pull/rebase + push explícitos.

## Detección

Se comparan paquetes pkg/dpkg, Python/pip, npm global y gems de Ruby cuando existen. También se registran versiones de runtimes, arquitectura, metadatos básicos y nombres de perfiles SSH sin registrar claves.

Si una persona o agente instala algo manualmente y no declara el motivo, el sistema registra el hecho con actor=unknown, reason=null, confidence=detected y evidencia de observación. No inventa explicaciones.

## Captura prospectiva

Los wrappers se instalan en:

    ~/.local/bin/

El registro unificado queda en:

    ~/.infra-package-operations.jsonl

La instalación se realiza con:

    $HOME/scripts/install-infra-wrappers.sh

Después de instalar wrappers en una sesión Zsh existente puede ser necesario ejecutar:

    rehash

Se capturan operaciones mutables de pkg, pip, pip3, npm y gem.

La instalación conserva occurred_at, manager, action y command. infra-sync.py cruza esa evidencia con el cambio real del manifest y correlaciona el paquete cuando aparece explícitamente en el comando.

pkg update no se utiliza como explicación directa de un cambio de paquete.

## Razón y actor

Cuando se conoce la intención, se puede registrar:

    $HOME/scripts/infra-note.py pkg figlet "prueba temporal de detección" --scope temporary

Ejemplo:

    $HOME/scripts/infra-note.py pip requests "dependencia requerida por proyecto X" --actor user --scope required

El registro queda en:

    ~/.infra-notes.jsonl

Durante la reconciliación, una nota coincidente por gestor/paquete y cercana temporalmente puede enriquecer el evento con reason, actor, reason_source y actor_source.

Si no existe evidencia suficiente, los campos permanecen null o unknown.

## Auditoría

    $HOME/scripts/infra-audit.py
    $HOME/scripts/infra-audit.py --json

Clasificaciones:

- required: declarado necesario.
- optional: declarado opcional.
- temporary: declarado temporal y candidato a revisión.
- unmanaged: instalado pero no declarado en desired-state.

unmanaged no significa safe-to-remove. La auditoría no elimina paquetes automáticamente.

## Reconciliación

La reconciliación automática de inicio de shell solo observa y actualiza datos locales:

    $HOME/scripts/infra-sync.sh --quiet --no-git

No hace commits automáticamente. Esto evita generar commits por cada apertura de Zsh.

La sincronización con GitHub es una acción explícita:

    $HOME/scripts/infra-git-sync.sh

Ese script reconcilia, crea commit si corresponde, hace pull --rebase y finalmente push.

## Historial y cursor

Las operaciones procesadas se controlan con:

    infrastructure/history/package-operation-cursor.json

El log bruto no se elimina. El cursor evita reprocesamientos.

Existe compatibilidad de lectura con el antiguo:

    ~/.infra-pkg-operations.log

y su cursor histórico.

## Estructura de un evento

Los eventos actuales usan schema 1.2 y distinguen:

- occurred_at: cuándo comenzó la operación capturada.
- detected_at: cuándo fue detectado el cambio.
- occurred_at_source: fuente temporal.
- actor: quién la declaró, si existe evidencia.
- reason: por qué ocurrió, si existe evidencia.
- confidence: nivel de respaldo de esos datos.
- evidence: método y comando observado.

## Auditoría IA

Un agente debe cruzar estado actual, estado deseado, historial, notas de intención, operación capturada y evidencia de uso/dependencias cuando exista.

Regla crítica: un paquete ausente de desired-state.json no implica automáticamente que sea seguro eliminarlo.

## Limitaciones

La captura temporal es prospectiva. Operaciones realizadas antes de instalar los wrappers pueden no tener occurred_at.

La correlación por paquete mejora la precisión cuando el comando contiene nombres explícitos. Las operaciones globales como upgrade pueden afectar múltiples paquetes y se consideran evidencia común para los cambios observados.

No se debe usar el historial como prueba de causalidad absoluta: representa observaciones y evidencias disponibles, no una reconstrucción perfecta del pasado.

## Seguridad

Nunca almacenar aquí claves privadas, tokens, contraseñas, .termux_authinfo, valores de entorno ni contenido de ~/.ssh/.
