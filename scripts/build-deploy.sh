#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

output_dir="${1:-deploy/current}"

case "$output_dir" in
  deploy/*|./deploy/*) ;;
  *)
    echo "Error: el destino debe estar dentro de deploy/." >&2
    exit 1
    ;;
esac

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "Error: hay cambios versionados sin commit. Haz commit o stash antes de generar el deploy." >&2
  exit 1
fi

tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/beslock-deploy.XXXXXX")"
trap 'rm -rf "$tmp_dir"' EXIT

rm -rf "$output_dir"
mkdir -p "$output_dir"

git archive --format=tar --worktree-attributes HEAD | tar -x -C "$tmp_dir"
find "$tmp_dir" -mindepth 1 -depth -type d -empty -exec rmdir {} +
rsync -a --delete "$tmp_dir"/ "$output_dir"/

cat > "$output_dir/FTP_DEPLOY_NOTES.txt" <<'EOF'
BESLOCK FileZilla deploy

Usa este mismo deploy unificado.

1. Sube siempre:
   wp-content/themes/beslock-custom/

2. Solo si vas a replicar la capa SEO backstage:
   wp-content/plugins/beslock-seo-config/

Nota:
- Los datos y manuales que usa el SEO ya viajan dentro del theme.
- No necesitas un segundo paquete paralelo dentro de deploy/.
EOF

file_count="$(find "$output_dir" -type f | wc -l | tr -d ' ')"
deploy_head="$(git rev-parse --short HEAD)"

cat <<EOF
Deploy generado correctamente.
Origen: HEAD ${deploy_head}
Destino: ${output_dir}
Archivos: ${file_count}

Usa esta carpeta como origen en FileZilla:
${repo_root}/${output_dir}
EOF
