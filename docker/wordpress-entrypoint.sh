#!/bin/sh
set -eu

# Prevent the official image from seeding default themes and plugins into the
# repository-mounted wp-content directory on first boot.
rm -rf \
  /usr/src/wordpress/wp-content/index.php \
  /usr/src/wordpress/wp-content/plugins/akismet \
  /usr/src/wordpress/wp-content/plugins/hello.php \
  /usr/src/wordpress/wp-content/plugins/index.php \
  /usr/src/wordpress/wp-content/themes/index.php \
  /usr/src/wordpress/wp-content/themes/twentytwentythree \
  /usr/src/wordpress/wp-content/themes/twentytwentyfour \
  /usr/src/wordpress/wp-content/themes/twentytwentyfive

# Keep the effective wp-config in sync with the bind-mounted docker config.
config_target="/var/www/html/wp-config.php"
config_source=""

if [ -f /var/www/html/wp-config-docker.php ]; then
  config_source="/var/www/html/wp-config-docker.php"
elif [ -f /usr/src/wordpress/wp-config-docker.php ]; then
  config_source="/usr/src/wordpress/wp-config-docker.php"
fi

if [ -n "$config_source" ] && { [ ! -f "$config_target" ] || ! cmp -s "$config_source" "$config_target"; }; then
  cp "$config_source" "$config_target" 2>/dev/null || true
  chown www-data:www-data "$config_target" 2>/dev/null || true
fi

exec docker-entrypoint.sh "$@"