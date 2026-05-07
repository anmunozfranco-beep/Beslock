<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! function_exists( 'beslock_get_product_card_badge_slugs' ) ) {
  function beslock_get_product_card_badge_slugs() {
    $slugs = array( 'e-orbit', 'e-flex', 's-shield', 'e-prime' );

    return apply_filters( 'beslock_product_card_badge_slugs', $slugs );
  }
}

if ( ! function_exists( 'beslock_product_card_has_install_badge' ) ) {
  function beslock_product_card_has_install_badge( $product ) {
    if ( ! $product instanceof WC_Product ) {
      return false;
    }

    return in_array( $product->get_slug(), beslock_get_product_card_badge_slugs(), true );
  }
}

// Product-specific WooCommerce filters and hooks
if ( class_exists( 'WooCommerce' ) && WC() ) {
  // Change single product add-to-cart button text to Spanish
  if ( ! has_filter( 'woocommerce_product_single_add_to_cart_text' ) ) {
    add_filter( 'woocommerce_product_single_add_to_cart_text', function( $text ) {
      return 'Agregar al carrito';
    } );
  }
}
