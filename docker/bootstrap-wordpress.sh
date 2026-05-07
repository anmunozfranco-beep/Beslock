#!/bin/sh
set -eu

path="/var/www/html"
max_attempts=60
attempt=1

until wp core is-installed --allow-root --path="$path" >/dev/null 2>&1; do
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "WordPress bootstrap timed out waiting for imported database tables."
    exit 1
  fi

  attempt=$((attempt + 1))
  sleep 5
done

wp search-replace \
  "${WORDPRESS_PRODUCTION_URL}" \
  "${WORDPRESS_LOCAL_URL}" \
  --all-tables \
  --skip-columns=guid \
  --allow-root \
  --path="$path"

wp option update home "${WORDPRESS_LOCAL_URL}" --allow-root --path="$path"
wp option update siteurl "${WORDPRESS_LOCAL_URL}" --allow-root --path="$path"

wp eval '
$active = get_option("active_plugins", []);
$legacy = "portfolio-product-sync/portfolio-product-sync.php";
$current = "beslock-product-sync/beslock-product-sync.php";
$changed = false;

$legacy_index = array_search($legacy, $active, true);
if ($legacy_index !== false) {
  unset($active[$legacy_index]);
  $changed = true;
}

if (file_exists(WP_PLUGIN_DIR . "/beslock-product-sync/beslock-product-sync.php") && ! in_array($current, $active, true)) {
  $active[] = $current;
  $changed = true;
}

if ($changed) {
  update_option("active_plugins", array_values($active));
}
' --allow-root --path="$path" >/dev/null 2>&1 || true

if wp plugin is-installed beslock-product-sync --allow-root --path="$path" >/dev/null 2>&1; then
  wp plugin activate beslock-product-sync --allow-root --path="$path" >/dev/null 2>&1 || true
fi

wp cache flush --allow-root --path="$path" >/dev/null 2>&1 || true