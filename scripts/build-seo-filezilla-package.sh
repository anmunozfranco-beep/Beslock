#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

output_dir="${1:-deploy/seo-filezilla}"

case "$output_dir" in
  deploy/*|./deploy/*) ;;
  *)
    echo "Error: el destino debe estar dentro de deploy/." >&2
    exit 1
    ;;
esac

required_paths=(
  "wp-content/plugins/beslock-seo-config"
  "wp-content/themes/beslock-custom/data/products.json"
  "wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv"
  "wp-content/themes/beslock-custom/assets/manuals/index.json"
  "wp-content/themes/beslock-custom/assets/manuals/products"
)

for path in "${required_paths[@]}"; do
  if [ ! -e "$path" ]; then
    echo "Error: falta la ruta requerida: $path" >&2
    exit 1
  fi
done

rm -rf "$output_dir"
mkdir -p "$output_dir/wp-content/plugins"
mkdir -p "$output_dir/wp-content/themes/beslock-custom/data"
mkdir -p "$output_dir/wp-content/themes/beslock-custom/assets"
mkdir -p "$output_dir/packages"

rsync -a "wp-content/plugins/beslock-seo-config" "$output_dir/wp-content/plugins/"
rsync -a "wp-content/themes/beslock-custom/data/products.json" "$output_dir/wp-content/themes/beslock-custom/data/"
rsync -a "wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv" "$output_dir/wp-content/themes/beslock-custom/data/"
rsync -a "wp-content/themes/beslock-custom/assets/manuals" "$output_dir/wp-content/themes/beslock-custom/assets/"

doc_source="docs/SEO_FILEZILLA_PRODUCTION_MIGRATION.md"
if [ -f "$doc_source" ]; then
  cp "$doc_source" "$output_dir/SEO_FILEZILLA_PRODUCTION_MIGRATION.md"
fi

generated_at="$(date '+%Y-%m-%d %H:%M:%S %Z')"
git_head="$(git rev-parse --short HEAD 2>/dev/null || echo 'sin-git')"
dirty_marker=""
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  dirty_marker=" (working tree con cambios versionados)"
fi

cat > "$output_dir/README.md" <<EOF
# Paquete SEO para FileZilla

Generado: ${generated_at}
Base Git: ${git_head}${dirty_marker}

Este paquete contiene solo lo necesario para reproducir la capa SEO backstage en producción.

## Qué subir

- \`wp-content/plugins/beslock-seo-config/\`
- \`wp-content/themes/beslock-custom/data/products.json\`
- \`wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv\`
- \`wp-content/themes/beslock-custom/assets/manuals/\`

## Orden recomendado

1. Respaldar base de datos y \`wp-content/\`.
2. Subir estas rutas con FileZilla respetando la misma estructura.
3. Activar \`BESLOCK SEO Config\` en WordPress si aún no está activo.
4. Ir a \`Herramientas > BESLOCK SEO\`.
5. Ejecutar \`Ejecutar limpieza + instalar/activar SITESEO Free\`.
6. Verificar que \`SITESEO Free\` quede activo y que el último sync no reporte errores críticos.

## Notas

- Si el hosting no permite instalación automática desde WordPress.org, sube manualmente el plugin oficial \`siteseo/\` a \`wp-content/plugins/\` y repite el paso 5.
- Este paquete no incluye \`wp-content/uploads/beslock-seo-config/\`; esos snapshots se regeneran en producción.
- Si producción no tiene la última versión del theme base, usa además \`deploy/current/wp-content/themes/beslock-custom/\`.
EOF

(
  cd "$output_dir"
  find wp-content -type f | sort | while IFS= read -r relative_path; do
    shasum -a 256 "$relative_path"
  done
) > "$output_dir/checksums.sha256"

if command -v zip >/dev/null 2>&1; then
  (
    cd "$repo_root/wp-content/plugins"
    zip -qr "$repo_root/$output_dir/packages/beslock-seo-config.zip" "beslock-seo-config"
  )
fi

file_count="$(find "$output_dir/wp-content" -type f | wc -l | tr -d ' ')"

cat <<EOF
Paquete SEO para FileZilla generado correctamente.
Destino: ${repo_root}/${output_dir}
Archivos incluidos: ${file_count}

Sube esta estructura:
${repo_root}/${output_dir}/wp-content/
EOF
