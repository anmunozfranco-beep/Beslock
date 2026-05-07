<?php
/**
 * BESLOCK local Docker sample config.
 *
 * The official WordPress image can generate wp-config.php automatically from
 * environment variables. This file documents the expected local values and can
 * be copied if you ever need to bootstrap a custom config manually.
 */

define( 'DB_NAME', getenv( 'WORDPRESS_DB_NAME' ) ?: 'beslock' );
define( 'DB_USER', getenv( 'WORDPRESS_DB_USER' ) ?: 'beslock' );
define( 'DB_PASSWORD', getenv( 'WORDPRESS_DB_PASSWORD' ) ?: 'beslock' );
define( 'DB_HOST', getenv( 'WORDPRESS_DB_HOST' ) ?: 'mysql' );
define( 'DB_CHARSET', 'utf8mb4' );
define( 'DB_COLLATE', '' );

define( 'AUTH_KEY',         'put your unique phrase here' );
define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );
define( 'LOGGED_IN_KEY',    'put your unique phrase here' );
define( 'NONCE_KEY',        'put your unique phrase here' );
define( 'AUTH_SALT',        'put your unique phrase here' );
define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );
define( 'LOGGED_IN_SALT',   'put your unique phrase here' );
define( 'NONCE_SALT',       'put your unique phrase here' );

$table_prefix = getenv( 'WORDPRESS_TABLE_PREFIX' ) ?: 'wptq_';

define( 'WP_DEBUG', false );
define( 'WP_CACHE', false );

if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

require_once ABSPATH . 'wp-settings.php';