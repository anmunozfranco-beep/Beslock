<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

// General theme setup hooks (non-WooCommerce). Keep minimal to avoid behavioral changes.
if ( ! function_exists( 'beslock_core_setup' ) ) {
  function beslock_core_setup() {
    add_theme_support( 'title-tag' );
  }
  add_action( 'after_setup_theme', 'beslock_core_setup', 10 );
}
