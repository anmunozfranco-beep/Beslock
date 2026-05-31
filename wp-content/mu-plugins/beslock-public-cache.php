<?php
/**
 * Plugin Name: Beslock Public Cache Optimizer
 * Description: Loads the Beslock public cache module early when mu-plugins are deployed.
 * Version: 1.1.0
 * Author: Beslock
 */

if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

$beslock_public_cache_module = WP_CONTENT_DIR . '/themes/beslock-custom/inc/performance/public-cache.php';

if ( file_exists( $beslock_public_cache_module ) ) {
  require_once $beslock_public_cache_module;
}
