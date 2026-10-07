#!/data/data/com.termux/files/usr/bin/bash
set -u

MANAGER="${INFRA_MANAGER:?INFRA_MANAGER is required}"
REAL_COMMAND="${INFRA_REAL_COMMAND:?INFRA_REAL_COMMAND is required}"
LOG="${HOME}/.infra-package-operations.jsonl"

case "${1:-}" in
  install|reinstall|remove|uninstall|upgrade|update|full-upgrade|dist-upgrade|uninstall)
    STARTED_AT="$(date --iso-8601=seconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')"
    printf '%s\n' "$(python - "$MANAGER" "$1" "$*" "$REAL_COMMAND" "$STARTED_AT" <<'PY'
import json,sys
manager,action,command,real_command,occurred_at=sys.argv[1:]
print(json.dumps({
  "schema_version":"1.0",
  "occurred_at":occurred_at,
  "manager":manager,
  "action":action,
  "command":command,
  "real_command":real_command
}, ensure_ascii=False, sort_keys=True))
PY
)" >> "$LOG"
    exec "$REAL_COMMAND" "$@"
    ;;
  *)
    exec "$REAL_COMMAND" "$@"
    ;;
esac
