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

exec docker-entrypoint.sh "$@"