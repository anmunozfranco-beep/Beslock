<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * Load a theme module if it exists.
 */
function beslock_require_theme_file( $relative_path ) {
  $path = get_stylesheet_directory() . '/' . ltrim( $relative_path, '/' );

  if ( file_exists( $path ) ) {
    require_once $path;
  }
}

/**
 * Register the child theme stylesheet early so later modules can depend on it.
 */
function beslock_enqueue_main_style() {
  $style_path = get_stylesheet_directory() . '/style.css';
  $version    = file_exists( $style_path ) ? filemtime( $style_path ) : null;

  wp_register_style(
    'beslock-main-style',
    get_stylesheet_uri(),
    array(),
    $version
  );

  wp_enqueue_style( 'beslock-main-style' );
}
add_action( 'wp_enqueue_scripts', 'beslock_enqueue_main_style', 1 );

$beslock_public_modules = array(
  'inc/performance/public-cache.php',
  'inc/core/setup.php',
  'inc/core/enqueue.php',
  'inc/features/hero-telemetry.php',
  'inc/legal-pages.php',
  'inc/header-widget.php',
  'inc/cleanup-kadence.php',
  'inc/woocommerce/setup.php',
  'inc/woocommerce/product-features.php',
  'inc/woocommerce/product-interactions.php',
  'inc/woocommerce/support-installation.php',
  'inc/woocommerce/product-hooks.php',
  'inc/woocommerce/cart.php',
  'inc/woocommerce/checkout.php',
  'inc/woocommerce/order-lookup.php',
  'inc/woocommerce/enqueue-assets.php',
);

foreach ( $beslock_public_modules as $beslock_module ) {
  beslock_require_theme_file( $beslock_module );
}

if ( is_admin() || ( defined( 'WP_CLI' ) && WP_CLI ) ) {
  beslock_require_theme_file( 'inc/admin/importer.php' );
  beslock_require_theme_file( 'inc/admin/tools.php' );
}
