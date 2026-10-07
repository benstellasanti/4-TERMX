#!/bin/sh
# -----------------------------------------------------------------------------
# Script Comunitario de Sincronización Robusta para Git / Termux
# -----------------------------------------------------------------------------

echo "==> 1. Verificando estado del repositorio..."
git status -s

echo "==> 2. Descargando cambios remotos (Fetch)..."
git fetch origin main

echo "==> 3. Integrando cambios si los hay (Rebase/Merge)..."
git pull origin main --rebase || {
    echo "⚠️ Hubo un conflicto al fusionar. Por favor revísalo manualmente."
    exit 1
}

echo "==> 4. Añadiendo cambios locales..."
git add -A

# Verifica si hay cambios pendientes por commitear
if git diff-index --cached --quiet HEAD --; then
    echo "✨ No hay cambios locales nuevos que sincronizar."
else
    echo "==> 5. Guardando cambios locales automáticamente..."
    git commit -m "sync: actualización automática desde Termux - $(date +'%Y-%m-%d %H:%M:%S')"
fi

echo "==> 6. Subiendo cambios a GitHub (Push)..."
git push origin main

echo "¡Sincronización completada con éxito! 🚀"
