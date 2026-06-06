<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

// WooCommerce theme support and gallery tweaks
if ( class_exists( 'WooCommerce' ) && WC() ) {
  add_action( 'after_setup_theme', function() {
    if ( ! current_theme_supports( 'woocommerce' ) ) {
      add_theme_support( 'woocommerce' );
    }
  }, 11 );

  add_action( 'after_setup_theme', function() {
    if ( function_exists( 'remove_theme_support' ) ) {
      remove_theme_support( 'wc-product-gallery-zoom' );
      remove_theme_support( 'wc-product-gallery-lightbox' );
      remove_theme_support( 'wc-product-gallery-slider' );
    }
  }, 20 );

  // Remove default WooCommerce empty cart message to avoid duplication
  add_action( 'init', function() {
    if ( function_exists( 'remove_action' ) ) {
      // wc_empty_cart_message is added by WooCommerce; remove it so theme template controls output
      remove_action( 'woocommerce_cart_is_empty', 'wc_empty_cart_message', 10 );
    }
  } );

  if ( ! function_exists( 'beslock_is_shipping_costs_updated_notice' ) ) {
    function beslock_is_shipping_costs_updated_notice( $message ) {
      $message = wp_strip_all_tags( (string) $message );
      $message = html_entity_decode( $message, ENT_QUOTES, get_bloginfo( 'charset' ) );
      $message = trim( preg_replace( '/\s+/', ' ', $message ) );
      $message = function_exists( 'remove_accents' ) ? remove_accents( $message ) : $message;
      $message = strtolower( rtrim( $message, ". \t\n\r\0\x0B" ) );

      $blocked_messages = array(
        __( 'Shipping costs updated.', 'woocommerce' ),
        'Shipping costs updated.',
        'Costes de envío actualizados.',
        'Costos de envío actualizados.',
      );

      foreach ( $blocked_messages as $blocked_message ) {
        $blocked_message = function_exists( 'remove_accents' ) ? remove_accents( $blocked_message ) : $blocked_message;
        $blocked_message = strtolower( rtrim( trim( $blocked_message ), ". \t\n\r\0\x0B" ) );

        if ( $message === $blocked_message ) {
          return true;
        }
      }

      return false;
    }
  }

  add_filter( 'woocommerce_add_notice', function( $message ) {
    return beslock_is_shipping_costs_updated_notice( $message ) ? '' : $message;
  } );

  if ( ! function_exists( 'beslock_remove_shipping_costs_updated_notice' ) ) {
    function beslock_remove_shipping_costs_updated_notice() {
      if ( ! function_exists( 'wc_get_notices' ) || ! function_exists( 'wc_set_notices' ) ) {
        return;
      }

      $notices = wc_get_notices();

      if ( ! is_array( $notices ) || empty( $notices['notice'] ) || ! is_array( $notices['notice'] ) ) {
        return;
      }

      $notices['notice'] = array_values(
        array_filter(
          $notices['notice'],
          function( $notice ) {
            $message = is_array( $notice ) && isset( $notice['notice'] ) ? $notice['notice'] : $notice;
            return ! beslock_is_shipping_costs_updated_notice( $message );
          }
        )
      );

      if ( empty( $notices['notice'] ) ) {
        unset( $notices['notice'] );
      }

      wc_set_notices( array_filter( $notices ) );
    }
  }

  add_action( 'woocommerce_calculated_shipping', 'beslock_remove_shipping_costs_updated_notice', 20 );
  add_action( 'woocommerce_before_cart', 'beslock_remove_shipping_costs_updated_notice', 1 );
  add_action( 'woocommerce_cart_is_empty', 'beslock_remove_shipping_costs_updated_notice', 1 );
  add_action( 'woocommerce_before_checkout_form_cart_notices', 'beslock_remove_shipping_costs_updated_notice', 1 );
  add_action( 'woocommerce_before_checkout_form', 'beslock_remove_shipping_costs_updated_notice', 1 );

  add_action( 'woocommerce_cart_is_empty', function() {
    if ( ! function_exists( 'wc_get_notices' ) || ! function_exists( 'wc_set_notices' ) ) {
      return;
    }

    $notices = wc_get_notices();

    if ( ! is_array( $notices ) || empty( $notices['success'] ) ) {
      return;
    }

    unset( $notices['success'] );
    wc_set_notices( array_filter( $notices ) );
  }, 1 );
}
