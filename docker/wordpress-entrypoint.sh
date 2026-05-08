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

# Ensure a usable `wp-config.php` exists. Some setups mount a volume over
# `/var/www/html` which can hide bind-mounted files; in that case copy the
# provided `wp-config-docker.php` into place at container start if missing.
if [ ! -f /var/www/html/wp-config.php ]; then
  if [ -f /var/www/html/wp-config-docker.php ]; then
    cp /var/www/html/wp-config-docker.php /var/www/html/wp-config.php 2>/dev/null || true
    chown www-data:www-data /var/www/html/wp-config.php 2>/dev/null || true
  elif [ -f /usr/src/wordpress/wp-config-docker.php ]; then
    cp /usr/src/wordpress/wp-config-docker.php /var/www/html/wp-config.php 2>/dev/null || true
    chown www-data:www-data /var/www/html/wp-config.php 2>/dev/null || true
  fi
fi

exec docker-entrypoint.sh "$@"