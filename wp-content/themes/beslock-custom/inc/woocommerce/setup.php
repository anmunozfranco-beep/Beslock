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

  if ( ! function_exists( 'beslock_email_commercial_sender_name' ) ) {
    function beslock_email_commercial_sender_name() {
      return 'BESLOCK® | ZONAS SMART';
    }
  }

  if ( ! function_exists( 'beslock_email_use_commercial_sender_name' ) ) {
    function beslock_email_use_commercial_sender_name( $from_name ) {
      return beslock_email_commercial_sender_name();
    }
  }

  add_filter( 'woocommerce_email_from_name', 'beslock_email_use_commercial_sender_name', 20 );
  add_filter( 'wp_mail_from_name', 'beslock_email_use_commercial_sender_name', 20 );

  if ( ! function_exists( 'beslock_email_order_subject' ) ) {
    function beslock_email_order_subject( $subject, $order = null, $email = null ) {
      if ( ! $order instanceof WC_Order ) {
        return $subject;
      }

      $email_id     = is_object( $email ) && ! empty( $email->id ) ? (string) $email->id : '';
      $order_number = $order->get_order_number();

      $subject_formats = array(
        'customer_processing_order'    => __( 'BESLOCK® | Confirmación de pedido #%s', 'beslock-custom' ),
        'customer_on_hold_order'       => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_completed_order'     => __( 'BESLOCK® | Tu pedido #%s ha sido despachado', 'beslock-custom' ),
        'customer_note'                => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_refunded_order'      => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_cancelled_order'     => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_failed_order'        => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_invoice'             => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
        'customer_pos_completed_order' => __( 'BESLOCK® | Confirmación de pedido #%s', 'beslock-custom' ),
        'customer_pos_refunded_order'  => __( 'BESLOCK® | Actualización de tu pedido #%s', 'beslock-custom' ),
      );

      if ( ! isset( $subject_formats[ $email_id ] ) ) {
        return $subject;
      }

      return sprintf( $subject_formats[ $email_id ], $order_number );
    }
  }

  add_filter( 'woocommerce_email_subject_customer_processing_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_on_hold_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_completed_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_note', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_refunded_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_cancelled_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_failed_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_invoice', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_pos_completed_order', 'beslock_email_order_subject', 20, 3 );
  add_filter( 'woocommerce_email_subject_customer_pos_refunded_order', 'beslock_email_order_subject', 20, 3 );

  if ( ! function_exists( 'beslock_email_account_subject' ) ) {
    function beslock_email_account_subject( $subject ) {
      if ( 'woocommerce_email_subject_customer_reset_password' === current_filter() ) {
        return __( 'BESLOCK® | Restablece tu contraseña', 'beslock-custom' );
      }

      return __( 'BESLOCK® | Tu cuenta BESLOCK', 'beslock-custom' );
    }
  }

  add_filter( 'woocommerce_email_subject_customer_new_account', 'beslock_email_account_subject', 20 );
  add_filter( 'woocommerce_email_subject_customer_reset_password', 'beslock_email_account_subject', 20 );

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
