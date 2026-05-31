#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://beslock.com.co"
PASSES=2
SLEEP_SECONDS=1
TIMEOUT_SECONDS=60

usage() {
  cat <<'USAGE'
Warm Beslock public Cloudflare cache after a purge.

Warms public pages, product pages, manual JSON files, manual images,
and hero reel assets so first visitors after a purge are not the ones
paying the full cold-cache cost.

Usage:
  warm_cloudflare_cache.sh [--base-url URL] [--passes N] [--sleep SECONDS] [--timeout SECONDS]

Examples:
  ./wp-content/themes/beslock-custom/scripts/warm_cloudflare_cache.sh
  ./wp-content/themes/beslock-custom/scripts/warm_cloudflare_cache.sh --passes 3
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --passes)
      PASSES="${2:-}"
      shift 2
      ;;
    --sleep)
      SLEEP_SECONDS="${2:-}"
      shift 2
      ;;
    --timeout)
      TIMEOUT_SECONDS="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

BASE_URL="${BASE_URL%/}"
THEME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRODUCTS_JSON="$THEME_DIR/data/products.json"
MANUALS_DIR="$THEME_DIR/dist/manuals"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required." >&2
  exit 1
fi

if ! [[ "$PASSES" =~ ^[0-9]+$ ]] || [ "$PASSES" -lt 1 ]; then
  echo "--passes must be a positive integer." >&2
  exit 1
fi

if ! [[ "$SLEEP_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "--sleep must be a non-negative integer." >&2
  exit 1
fi

if ! [[ "$TIMEOUT_SECONDS" =~ ^[0-9]+$ ]] || [ "$TIMEOUT_SECONDS" -lt 1 ]; then
  echo "--timeout must be a positive integer." >&2
  exit 1
fi

read_product_slugs() {
  if command -v jq >/dev/null 2>&1 && [ -f "$PRODUCTS_JSON" ]; then
    jq -r '.[].slug // empty' "$PRODUCTS_JSON"
    return
  fi

  cat <<'SLUGS'
e-flex
e-nova
e-orbit
e-prime
e-shield
e-touch
SLUGS
}

URLS=("$BASE_URL/")

while IFS= read -r slug; do
  [ -n "$slug" ] || continue
  URLS+=("$BASE_URL/producto/$slug/")
done < <(read_product_slugs)

URLS+=(
  "$BASE_URL/wp-content/themes/beslock-custom/dist/manuals/index.json"
  "$BASE_URL/wp-content/themes/beslock-custom/dist/manuals/export_summary.json"
)

if [ -d "$THEME_DIR/assets/images/Clips_hero" ]; then
  while IFS= read -r hero_asset; do
    relative_path="${hero_asset#"$THEME_DIR"/}"
    URLS+=("$BASE_URL/wp-content/themes/beslock-custom/$relative_path")
  done < <(find "$THEME_DIR/assets/images/Clips_hero" -maxdepth 2 -type f \( -name '*.mp4' -o -name '*.webp' \) | sort)
fi

if [ -d "$THEME_DIR/assets/images/Hero_develp/images_hero" ]; then
  while IFS= read -r hero_image; do
    relative_path="${hero_image#"$THEME_DIR"/}"
    URLS+=("$BASE_URL/wp-content/themes/beslock-custom/$relative_path")
  done < <(find "$THEME_DIR/assets/images/Hero_develp/images_hero" -type f \( -iname '*.webp' -o -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) | sort)
fi

if [ -d "$MANUALS_DIR/products" ]; then
  while IFS= read -r product_json; do
    name="$(basename "$product_json")"
    URLS+=("$BASE_URL/wp-content/themes/beslock-custom/dist/manuals/products/$name")
  done < <(find "$MANUALS_DIR/products" -maxdepth 1 -type f -name '*.json' | sort)
fi

if [ -d "$MANUALS_DIR/assets" ]; then
  while IFS= read -r manual_asset; do
    relative_path="${manual_asset#"$THEME_DIR"/}"
    URLS+=("$BASE_URL/wp-content/themes/beslock-custom/$relative_path")
  done < <(find "$MANUALS_DIR/assets" -type f \( -iname '*.webp' -o -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) | sort)
fi

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

printf 'Warming %s URLs on %s (%s passes)\n' "${#URLS[@]}" "$BASE_URL" "$PASSES"
printf 'Expected pattern after purge: first pass MISS, next pass HIT.\n\n'

overall_status=0

for pass in $(seq 1 "$PASSES"); do
  printf 'Pass %s/%s\n' "$pass" "$PASSES"

  for url in "${URLS[@]}"; do
    headers_file="$(mktemp)"
    body_file="$(mktemp)"

    metrics="$(
      curl \
        --silent \
        --show-error \
        --location \
        --max-time "$TIMEOUT_SECONDS" \
        --user-agent "$USER_AGENT" \
        --dump-header "$headers_file" \
        --output "$body_file" \
        --write-out 'http=%{http_code} cf=%header{cf-cache-status} time=%{time_total} size=%{size_download}' \
        "$url" || true
    )"

    rm -f "$headers_file" "$body_file"

    http_code="$(printf '%s' "$metrics" | sed -n 's/.*http=\([0-9][0-9][0-9]\).*/\1/p')"
    cf_status="$(printf '%s' "$metrics" | sed -n 's/.*cf=\([^ ]*\).*/\1/p')"
    total_time="$(printf '%s' "$metrics" | sed -n 's/.*time=\([^ ]*\).*/\1/p')"

    if [ -z "$http_code" ] || [ "$http_code" -lt 200 ] || [ "$http_code" -ge 400 ]; then
      overall_status=1
      printf '  FAIL %-72s http=%s cf=%s time=%s\n' "$url" "${http_code:-n/a}" "${cf_status:-n/a}" "${total_time:-n/a}"
      continue
    fi

    if [ "$pass" -gt 1 ] && [ "${cf_status:-}" != "HIT" ]; then
      overall_status=1
      printf '  WARN %-72s http=%s cf=%s time=%s\n' "$url" "$http_code" "${cf_status:-n/a}" "$total_time"
      continue
    fi

    printf '  OK   %-72s http=%s cf=%s time=%s\n' "$url" "$http_code" "${cf_status:-n/a}" "$total_time"
  done

  if [ "$pass" -lt "$PASSES" ]; then
    sleep "$SLEEP_SECONDS"
  fi

  printf '\n'
done

if [ "$overall_status" -ne 0 ]; then
  echo "Cache warm completed with warnings. Re-run once before investigating if this was immediately after purge." >&2
  exit "$overall_status"
fi

echo "Cache warm completed successfully."
