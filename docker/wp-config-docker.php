<?php

define( 'DB_NAME', getenv( 'WORDPRESS_DB_NAME' ) ?: 'beslock' );
define( 'DB_USER', getenv( 'WORDPRESS_DB_USER' ) ?: 'beslock' );
define( 'DB_PASSWORD', getenv( 'WORDPRESS_DB_PASSWORD' ) ?: 'beslock' );
define( 'DB_HOST', getenv( 'WORDPRESS_DB_HOST' ) ?: 'mysql' );
define( 'DB_CHARSET', 'utf8mb4' );
define( 'DB_COLLATE', '' );

define( 'AUTH_KEY',         'npqwytn2ygha68t22b7i1jzpfia7ujw4tbgiwkurkqpqr0renf2b6pazcbu2hmy9' );
define( 'SECURE_AUTH_KEY',  'td0c4ml1hyng3bsovgqzzw89luowt5nokafhe9ycmg64m6d6ueicfu63yaaypz7b' );
define( 'LOGGED_IN_KEY',    'n0e1rgblwr15xuj5iu5grjvgvrc8goj7lchokgfx0qbd9ptiibksdbtf7pk7lwcf' );
define( 'NONCE_KEY',        'kk5vfaavnmky4exoirnwtueqg5ubedi6nubwgk7jehtygse3ls04qoahksh5coe9' );
define( 'AUTH_SALT',        'gsflmahfsgelxjisoypg3wbqeiu2h3cees3chnldcshgsiiccabkvah3ygntxoqd' );
define( 'SECURE_AUTH_SALT', 'xnvgtvm8httneyhbckn6pltldewao1fkg7yy2d7odw19vsprtcxrss6fhzzrcuix' );
define( 'LOGGED_IN_SALT',   'trjzbhkscis705fe6s5ecl3bxolepcrdzqi79ua3qm5ubi5wsypt3d34pqax7rcg' );
define( 'NONCE_SALT',       'vmpkftv7x9qziaszfojgq47z6fa3johpxztyirfcn8pujhhgn2kxv2jhhmhdgnor' );

define( 'RSSSL_KEY', 'yksG0732Rx8zCO076WHcY8tpKnmVAYffBR4f6pIbQzK8MCNXuJ7rhDmbyKWbcr6W' );

$table_prefix = getenv( 'WORDPRESS_TABLE_PREFIX' ) ?: 'wptq_';

define( 'WP_DEBUG', false );
define( 'WP_CACHE', false );
define( 'DONOTCACHEPAGE', true );
define( 'FORCE_SSL_ADMIN', false );
define( 'FS_METHOD', 'direct' );

$local_url = getenv( 'WORDPRESS_LOCAL_URL' ) ?: 'http://localhost:8080';
define( 'WP_HOME', $local_url );
define( 'WP_SITEURL', $local_url );

if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

require_once ABSPATH . 'wp-settings.php';