<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! function_exists( 'beslock_is_installation_service_product' ) ) {
  function beslock_is_installation_service_product( $product ) {
    if ( is_numeric( $product ) && function_exists( 'wc_get_product' ) ) {
      $product = wc_get_product( absint( $product ) );
    }

    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return false;
    }

    return 0 === strpos( (string) $product->get_sku(), 'BESLOCK-INST-' );
  }
}

add_action( 'template_redirect', function() {
  if ( is_admin() || wp_doing_ajax() || ! function_exists( 'is_product' ) || ! is_product() || ! function_exists( 'wc_get_product' ) ) {
    return;
  }

  $queried_product = wc_get_product( get_queried_object_id() );

  if ( ! beslock_is_installation_service_product( $queried_product ) ) {
    return;
  }

  global $wp_query;

  if ( is_object( $wp_query ) && method_exists( $wp_query, 'set_404' ) ) {
    $wp_query->set_404();
  }

  status_header( 404 );
  nocache_headers();

  $template_404 = get_query_template( '404' );

  if ( $template_404 ) {
    include $template_404;
  }

  exit;
}, 8 );
