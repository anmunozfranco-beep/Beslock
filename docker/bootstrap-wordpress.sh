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
wp cache flush --allow-root --path="$path" >/dev/null 2>&1 || true