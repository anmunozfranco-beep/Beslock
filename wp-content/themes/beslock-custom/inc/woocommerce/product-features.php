<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * Product feature hooks: register callbacks that prepare data and delegate
 * rendering to template parts to keep markup out of logic files.
 */

error_log( 'Loaded OK: inc/woocommerce/product-features.php' );

if ( ! function_exists( 'beslock_get_manual_product_catalog' ) ) {
  function beslock_get_manual_product_catalog() {
    static $catalog = null;

    if ( null !== $catalog ) {
      return $catalog;
    }

    $catalog = array();
    $catalog_path = get_stylesheet_directory() . '/data/product-manual-features.php';

    if ( ! file_exists( $catalog_path ) || ! is_readable( $catalog_path ) ) {
      return $catalog;
    }

    $loaded_catalog = require $catalog_path;
    if ( ! is_array( $loaded_catalog ) ) {
      return $catalog;
    }

    foreach ( $loaded_catalog as $slug => $item ) {
      if ( empty( $slug ) || ! is_array( $item ) ) {
        continue;
      }

      $catalog[ sanitize_title( (string) $slug ) ] = $item;
    }

    return $catalog;
  }
}

if ( ! function_exists( 'beslock_get_manual_product_item' ) ) {
  function beslock_get_manual_product_item( $product ) {
    if ( is_numeric( $product ) && function_exists( 'wc_get_product' ) ) {
      $product = wc_get_product( intval( $product ) );
    }

    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return array();
    }

    $catalog = beslock_get_manual_product_catalog();
    $slug = sanitize_title( (string) $product->get_slug() );

    if ( empty( $catalog[ $slug ] ) || ! is_array( $catalog[ $slug ] ) ) {
      return array();
    }

    return $catalog[ $slug ];
  }
}

if ( ! function_exists( 'beslock_normalize_product_feature_list' ) ) {
  function beslock_normalize_product_feature_list( $features ) {
    if ( is_string( $features ) ) {
      $features = maybe_unserialize( $features );
    }

    if ( ! is_array( $features ) ) {
      return array();
    }

    $normalized_features = array();

    foreach ( $features as $feature ) {
      $feature = trim( wp_strip_all_tags( (string) $feature ) );

      if ( '' === $feature ) {
        continue;
      }

      $normalized_features[] = $feature;
    }

    return array_values( array_unique( $normalized_features ) );
  }
}

if ( ! function_exists( 'beslock_normalize_product_feature_rows' ) ) {
  function beslock_normalize_product_feature_rows( $features ) {
    if ( is_string( $features ) ) {
      $features = maybe_unserialize( $features );
    }

    if ( ! is_array( $features ) ) {
      return array();
    }

    $normalized_rows = array();

    foreach ( $features as $feature ) {
      if ( is_array( $feature ) ) {
        $label = trim( wp_strip_all_tags( (string) ( $feature['label'] ?? '' ) ) );
        $value = trim( wp_strip_all_tags( (string) ( $feature['value'] ?? '' ) ) );

        if ( '' === $label || '' === $value ) {
          continue;
        }

        $normalized_rows[] = array(
          'label' => $label,
          'value' => $value,
        );
        continue;
      }

      $feature = trim( wp_strip_all_tags( (string) $feature ) );
      if ( '' === $feature ) {
        continue;
      }

      $feature_parts = preg_split( '/:\s+/u', $feature, 2 );
      if ( ! is_array( $feature_parts ) || 2 !== count( $feature_parts ) ) {
        $feature_parts = preg_split( '/\s+[—-]\s+/u', $feature, 2 );
      }

      if ( is_array( $feature_parts ) && 2 === count( $feature_parts ) ) {
        $normalized_rows[] = array(
          'label' => trim( $feature_parts[0] ),
          'value' => trim( $feature_parts[1] ),
        );
        continue;
      }

      $normalized_rows[] = array(
        'label' => __( 'Detalle', 'beslock' ),
        'value' => $feature,
      );
    }

    return $normalized_rows;
  }
}

if ( ! function_exists( 'beslock_get_product_features_list' ) ) {
  function beslock_get_product_features_list( $product ) {
    if ( is_numeric( $product ) && function_exists( 'wc_get_product' ) ) {
      $product = wc_get_product( intval( $product ) );
    }

    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return array();
    }

    $manual_item = beslock_get_manual_product_item( $product );
    if ( ! empty( $manual_item['feature_rows'] ) ) {
      return beslock_normalize_product_feature_rows( $manual_item['feature_rows'] );
    }

    if ( ! empty( $manual_item['features'] ) ) {
      return beslock_normalize_product_feature_rows( $manual_item['features'] );
    }

    $features = beslock_normalize_product_feature_rows(
      get_post_meta( $product->get_id(), 'beslock_features', true )
    );

    if ( ! empty( $features ) ) {
      return $features;
    }

    return array();
  }
}

if ( ! function_exists( 'beslock_get_product_reviews_list' ) ) {
  function beslock_get_product_reviews_list( $product ) {
    if ( is_numeric( $product ) && function_exists( 'wc_get_product' ) ) {
      $product = wc_get_product( intval( $product ) );
    }

    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return array();
    }

    $reviews = array();
    $comments = get_comments( array(
      'post_id' => $product->get_id(),
      'status' => 'approve',
      'orderby' => 'comment_date_gmt',
      'order' => 'DESC',
    ) );

    if ( is_array( $comments ) ) {
      foreach ( $comments as $comment ) {
        if ( empty( $comment->comment_content ) || in_array( $comment->comment_type, array( 'pingback', 'trackback' ), true ) ) {
          continue;
        }

        $reviews[] = array(
          'author' => trim( wp_strip_all_tags( (string) ( $comment->comment_author ?: __( 'Cliente verificado', 'beslock' ) ) ) ),
          'rating' => min( 5, max( 0, absint( get_comment_meta( $comment->comment_ID, 'rating', true ) ) ) ),
          'text'   => trim( wp_strip_all_tags( (string) $comment->comment_content ) ),
        );
      }
    }

    if ( ! empty( $reviews ) ) {
      return $reviews;
    }

    return array();
  }
}

add_action( 'beslock_product_trust_badges', function() {
  global $product;
  if ( ! $product ) return;
  $pid = intval( $product->get_id() );
  $badges_meta = get_post_meta( $pid, 'beslock_trust_badges', true );
  if ( empty( $badges_meta ) ) return;
  $badges = is_array( $badges_meta ) ? $badges_meta : array_map( 'trim', explode( ',', (string) $badges_meta ) );
  if ( empty( $badges ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'badges', 'badges' => $badges ) );
}, 10 );

add_action( 'beslock_product_confianza', function() {
  global $product;
  if ( ! $product ) return;
  $pid = intval( $product->get_id() );
  $conf = get_post_meta( $pid, 'beslock_confianza', true );
  if ( empty( $conf ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'confianza', 'confianza' => $conf ) );
} );

add_action( 'beslock_product_psb', function() {
  global $post;
  if ( empty( $post ) ) return;
  $pid = intval( $post->ID );
  $problem = get_post_meta( $pid, 'beslock_psb_problem', true );
  $solution = get_post_meta( $pid, 'beslock_psb_solution', true );
  $benefits = get_post_meta( $pid, 'beslock_psb_benefits', true );
  if ( empty( $problem ) && empty( $solution ) && empty( $benefits ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'psb', 'problem' => $problem, 'solution' => $solution, 'benefits' => $benefits ) );
} );

add_action( 'beslock_product_specs', function() {
  global $product;
  if ( ! $product ) return;
  $pid = intval( $product->get_id() );
  $has_attrs = ( ! empty( $product->get_attributes() ) );
  $specs_meta = get_post_meta( $pid, 'beslock_specs', true );
  if ( ! $has_attrs && empty( $specs_meta ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'specs', 'specs' => $specs_meta, 'has_attrs' => $has_attrs, 'product_id' => $pid ) );
} );

add_action( 'beslock_product_demo', function() {
  global $post;
  if ( empty( $post ) ) return;
  $embed = get_post_meta( $post->ID, 'beslock_demo_embed', true );
  if ( empty( $embed ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'demo', 'embed' => $embed ) );
} );

add_action( 'beslock_product_who', function() {
  global $post;
  $who = get_post_meta( $post->ID, 'beslock_who', true );
  if ( empty( $who ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'who', 'who' => $who ) );
} );

add_action( 'beslock_product_faq', function() {
  global $post;
  $faq = get_post_meta( $post->ID, 'beslock_faq', true );
  if ( empty( $faq ) ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'faq', 'faq' => $faq ) );
} );

add_action( 'beslock_product_cta', function() {
  global $product;
  if ( ! $product ) return;
  get_template_part( 'template-parts/product-features', null, array( 'section' => 'cta', 'product_id' => intval( $product->get_id() ) ) );
} );

/**
 * Admin product checkbox: toggle 'beslock_badge' per product
 */
add_action( 'woocommerce_product_options_general_product_data', function() {
  woocommerce_wp_checkbox( array(
    'id' => 'beslock_badge',
    'label' => __( 'Mostrar badge de instalación', 'beslock' ),
    'desc_tip' => true,
    'description' => __( 'Activa el badge "Instalación incluida" en este producto.', 'beslock' ),
  ) );
} );

add_action( 'woocommerce_process_product_meta', function( $post_id ) {
  $value = isset( $_POST['beslock_badge'] ) && $_POST['beslock_badge'] ? 'yes' : 'no';
  update_post_meta( $post_id, 'beslock_badge', $value );
} );
