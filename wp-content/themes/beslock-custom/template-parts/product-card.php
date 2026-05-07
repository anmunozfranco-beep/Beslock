<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

global $product;

$context = get_query_var( 'beslock_context', array() );
$show_description = $context['show_description'] ?? false;

if ( isset( $args['product'] ) && $args['product'] instanceof WC_Product ) {
  $product = $args['product'];
}

if ( ! $product instanceof WC_Product ) {
  return;
}

get_template_part(
  'template-parts/cards/product-card',
  null,
  array(
    'product'          => $product,
    'show_description' => $args['show_description'] ?? $show_description,
    'context'          => $context,
  )
);
