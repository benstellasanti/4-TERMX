HISTSIZE=10000
SAVEHIST=20000
setopt HIST_IGNORE_ALL_DUPS
setopt INC_APPEND_HISTORY
# 4-TERMX Infrastructure Reconciliation
# Detecta cambios de paquetes/runtimes sin exigir registro manual.
if [ -x "$HOME/scripts/infra-sync.sh" ]; then
  ( "$HOME/scripts/infra-sync.sh" --quiet >/dev/null 2>&1 ) &
fi
