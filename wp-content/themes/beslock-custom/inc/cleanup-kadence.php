<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * Keep the parent archive hero out of WooCommerce archive contexts while
 * preserving Kadence output for non-commerce archives.
 */
add_action( 'kadence_entry_archive_hero', 'beslock_kadence_archive_hero_buffer_start', 0 );
function beslock_kadence_archive_hero_buffer_start() {
  if ( ! function_exists( 'is_shop' ) ) {
    return;
  }

  ob_start();
}

add_action( 'kadence_entry_archive_hero', 'beslock_kadence_archive_hero_buffer_end', 9999 );
function beslock_kadence_archive_hero_buffer_end() {
  if ( ! function_exists( 'is_shop' ) ) {
    return;
  }

  $content = ob_get_clean();

  if ( is_shop() || is_product_category() || is_product_tag() ) {
    return;
  }

  echo $content;
}
