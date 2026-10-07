#!/data/data/com.termux/files/usr/bin/bash
set -eu

BIN="$HOME/.local/bin"
mkdir -p "$BIN"

install_wrapper() {
  name="$1"
  manager="$2"
  real="$3"
  cat > "$BIN/$name" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
export INFRA_MANAGER="$manager"
export INFRA_REAL_COMMAND="$real"
exec "$HOME/scripts/infra-wrapper.sh" "\$@"
EOF
  chmod 700 "$BIN/$name"
}

install_wrapper pkg pkg /data/data/com.termux/files/usr/bin/pkg
install_wrapper pip pip /data/data/com.termux/files/usr/bin/pip
install_wrapper pip3 pip /data/data/com.termux/files/usr/bin/pip
install_wrapper npm npm /data/data/com.termux/files/usr/bin/npm
install_wrapper gem gem /data/data/com.termux/files/usr/bin/gem

echo "Wrappers instalados en $BIN"
echo "Ejecuta 'rehash' en zsh si algún comando ya estaba cacheado."
