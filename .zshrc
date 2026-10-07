HISTSIZE=10000
SAVEHIST=20000
setopt HIST_IGNORE_ALL_DUPS
setopt INC_APPEND_HISTORY

# 4-TERMX Infrastructure Reconciliation
# Solo observa y actualiza el estado local; no crea commits al abrir Zsh.
if [ -x "$HOME/scripts/infra-sync.sh" ]; then
  ( "$HOME/scripts/infra-sync.sh" --quiet --no-git >/dev/null 2>&1 ) &
fi
