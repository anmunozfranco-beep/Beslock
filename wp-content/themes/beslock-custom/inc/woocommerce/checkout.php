<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * Wompi's current payment flow relies on WooCommerce's classic checkout
 * redirect to the order-pay receipt page, where the Wompi widget is opened.
 */
function beslock_force_classic_checkout_for_wompi( $content ) {
  if ( is_admin() || ! function_exists( 'wc_get_page_id' ) ) {
    return $content;
  }

  $checkout_page_id = (int) wc_get_page_id( 'checkout' );
  if ( $checkout_page_id <= 0 || ! is_page( $checkout_page_id ) ) {
    return $content;
  }

  if ( has_shortcode( $content, 'woocommerce_checkout' ) ) {
    return $content;
  }

  if ( false === strpos( $content, 'woocommerce/checkout' ) ) {
    return $content;
  }

  return '[woocommerce_checkout]';
}
add_filter( 'the_content', 'beslock_force_classic_checkout_for_wompi', 8 );

function beslock_is_checkout_form_page() {
  $is_checkout_ajax = function_exists( 'wp_doing_ajax' )
    && wp_doing_ajax()
    && isset( $_REQUEST['wc-ajax'] )
    && 'update_order_review' === sanitize_text_field( wp_unslash( $_REQUEST['wc-ajax'] ) );

  if ( $is_checkout_ajax ) {
    return true;
  }

  if ( is_admin() || ! function_exists( 'is_checkout' ) || ! is_checkout() ) {
    return false;
  }

  if ( function_exists( 'is_order_received_page' ) && is_order_received_page() ) {
    return false;
  }

  return true;
}

function beslock_checkout_is_missing_shipping_confirmation() {
  if ( is_admin() || ! function_exists( 'WC' ) || ! WC()->cart ) {
    return false;
  }

  if ( WC()->cart->is_empty() ) {
    return false;
  }

  if ( function_exists( 'is_order_received_page' ) && is_order_received_page() ) {
    return false;
  }

  if ( function_exists( 'is_wc_endpoint_url' ) && is_wc_endpoint_url( 'order-pay' ) ) {
    return false;
  }

  return function_exists( 'beslock_cart_requires_shipping_address_confirmation' ) && beslock_cart_requires_shipping_address_confirmation();
}

function beslock_checkout_shipping_confirmation_notice() {
  return __( 'Actualiza y confirma la dirección de envío en el carrito antes de continuar con el pago.', 'beslock-custom' );
}

function beslock_redirect_checkout_without_confirmed_shipping() {
  if ( ! function_exists( 'is_checkout' ) || ! is_checkout() || ! beslock_checkout_is_missing_shipping_confirmation() ) {
    return;
  }

  $has_notice = function_exists( 'wc_has_notice' ) && wc_has_notice( beslock_checkout_shipping_confirmation_notice(), 'error' );

  if ( function_exists( 'wc_add_notice' ) && ! $has_notice ) {
    wc_add_notice( beslock_checkout_shipping_confirmation_notice(), 'error' );
  }

  wp_safe_redirect( wc_get_cart_url() );
  exit;
}
add_action( 'template_redirect', 'beslock_redirect_checkout_without_confirmed_shipping', 8 );

function beslock_validate_checkout_shipping_confirmation() {
  if ( ! beslock_checkout_is_missing_shipping_confirmation() || ! function_exists( 'wc_add_notice' ) ) {
    return;
  }

  wc_add_notice( beslock_checkout_shipping_confirmation_notice(), 'error' );
}
add_action( 'woocommerce_checkout_process', 'beslock_validate_checkout_shipping_confirmation', 8 );

function beslock_classic_checkout_hooks() {
  if ( ! beslock_is_checkout_form_page() ) {
    return;
  }

  remove_action( 'woocommerce_checkout_order_review', 'woocommerce_checkout_payment', 20 );
  add_action( 'woocommerce_checkout_after_customer_details', 'woocommerce_checkout_payment', 30 );
}
add_action( 'wp', 'beslock_classic_checkout_hooks' );

function beslock_checkout_gateway_description( $description, $payment_id ) {
  if ( 'wompi' !== $payment_id ) {
    return $description;
  }

  return 'Paga de forma segura con Wompi.';
}
add_filter( 'woocommerce_gateway_description', 'beslock_checkout_gateway_description', 10, 2 );

function beslock_checkout_fields( $fields ) {
  if ( isset( $fields['billing']['billing_first_name'] ) ) {
    $fields['billing']['billing_first_name']['label'] = 'Nombre';
    $fields['billing']['billing_first_name']['class'] = array( 'form-row-first', 'beslock-classic-contact-field' );
  }

  if ( isset( $fields['billing']['billing_last_name'] ) ) {
    $fields['billing']['billing_last_name']['label'] = 'Apellido';
    $fields['billing']['billing_last_name']['class'] = array( 'form-row-last', 'beslock-classic-contact-field' );
  }

  if ( isset( $fields['billing']['billing_phone'] ) ) {
    $fields['billing']['billing_phone']['label']    = 'Celular';
    $fields['billing']['billing_phone']['required'] = true;
    $fields['billing']['billing_phone']['class']    = array( 'form-row-first', 'beslock-classic-contact-field' );
  }

  if ( isset( $fields['billing']['billing_email'] ) ) {
    $fields['billing']['billing_email']['label'] = 'Correo electrónico';
    $fields['billing']['billing_email']['class'] = array( 'form-row-last', 'beslock-classic-contact-field' );
  }

  foreach ( array( 'billing_company', 'billing_country', 'billing_address_1', 'billing_address_2', 'billing_city', 'billing_state', 'billing_postcode' ) as $field_key ) {
    if ( isset( $fields['billing'][ $field_key ] ) ) {
      $fields['billing'][ $field_key ]['required'] = false;
      $fields['billing'][ $field_key ]['class']    = array( 'form-row-wide', 'beslock-classic-address-field' );
    }
  }

  if ( isset( $fields['order']['order_comments'] ) ) {
    $fields['order']['order_comments']['label']       = 'Añadir una nota a tu pedido';
    $fields['order']['order_comments']['placeholder'] = '';
    $fields['order']['order_comments']['class']       = array( 'form-row-wide', 'beslock-classic-note-field' );
  }

  return $fields;
}
add_filter( 'woocommerce_checkout_fields', 'beslock_checkout_fields', 20 );

function beslock_checkout_get_shipping_value( $field_key ) {
  if ( ! function_exists( 'WC' ) || ! WC()->customer ) {
    return '';
  }

  $customer = WC()->customer;
  $values   = array(
    'country'    => $customer->get_shipping_country() ? $customer->get_shipping_country() : 'CO',
    'state'      => $customer->get_shipping_state(),
    'city'       => $customer->get_shipping_city(),
    'address_1'  => function_exists( 'beslock_get_shipping_session_value' ) ? beslock_get_shipping_session_value( 'beslock_shipping_address_1', $customer->get_shipping_address_1() ) : $customer->get_shipping_address_1(),
    'address_2'  => function_exists( 'beslock_get_shipping_session_value' ) ? beslock_get_shipping_session_value( 'beslock_shipping_area', $customer->get_shipping_address_2() ) : $customer->get_shipping_address_2(),
    'postcode'   => $customer->get_shipping_postcode(),
  );

  return isset( $values[ $field_key ] ) ? $values[ $field_key ] : '';
}

function beslock_checkout_default_field_value( $value, $input ) {
  if ( ! beslock_is_checkout_form_page() ) {
    return $value;
  }

  $field_map = array(
    'billing_country'    => 'country',
    'shipping_country'   => 'country',
    'billing_state'      => 'state',
    'shipping_state'     => 'state',
    'billing_city'       => 'city',
    'shipping_city'      => 'city',
    'billing_address_1'  => 'address_1',
    'shipping_address_1' => 'address_1',
    'billing_address_2'  => 'address_2',
    'shipping_address_2' => 'address_2',
    'billing_postcode'   => 'postcode',
    'shipping_postcode'  => 'postcode',
  );

  if ( ! isset( $field_map[ $input ] ) ) {
    return $value;
  }

  if (
    'country' !== $field_map[ $input ] &&
    function_exists( 'beslock_cart_has_confirmed_shipping_address' ) &&
    ! beslock_cart_has_confirmed_shipping_address()
  ) {
    return '';
  }

  $shipping_value = beslock_checkout_get_shipping_value( $field_map[ $input ] );

  return '' !== trim( (string) $shipping_value ) ? $shipping_value : $value;
}
add_filter( 'woocommerce_checkout_get_value', 'beslock_checkout_default_field_value', 20, 2 );

function beslock_checkout_cart_item_class( $class, $cart_item, $cart_item_key ) {
  if ( ! beslock_is_checkout_form_page() || empty( $cart_item['data'] ) || ! is_a( $cart_item['data'], 'WC_Product' ) ) {
    return $class;
  }

  $sku = (string) $cart_item['data']->get_sku();

  if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
    $class .= ' beslock-checkout-item--installation';
  }

  return $class;
}
add_filter( 'woocommerce_cart_item_class', 'beslock_checkout_cart_item_class', 20, 3 );

function beslock_checkout_cart_item_name( $name, $cart_item, $cart_item_key ) {
  if ( ! beslock_is_checkout_form_page() || empty( $cart_item['data'] ) || ! is_a( $cart_item['data'], 'WC_Product' ) ) {
    return $name;
  }

  $product   = $cart_item['data'];
  $sku       = (string) $product->get_sku();

  if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
    $installation_order_number = ! empty( $cart_item['beslock_installation_parent_order_number'] ) ? sanitize_text_field( $cart_item['beslock_installation_parent_order_number'] ) : '';
    $installation_city         = ! empty( $cart_item['beslock_installation_city'] ) ? sanitize_text_field( $cart_item['beslock_installation_city'] ) : '';
    $installation_meta         = '';

    if ( '' !== $installation_order_number || '' !== $installation_city ) {
      ob_start();
      ?>
      <span class="beslock-classic-summary-installation-meta">
        <?php if ( '' !== $installation_order_number ) : ?>
          <span class="beslock-classic-summary-installation-meta__item">
            <span class="beslock-classic-summary-installation-meta__label"><?php esc_html_e( 'Pedido asociado:', 'beslock-custom' ); ?></span>
            <span class="beslock-classic-summary-installation-meta__value"><?php echo esc_html( $installation_order_number ); ?></span>
          </span>
        <?php endif; ?>

        <?php if ( '' !== $installation_city ) : ?>
          <span class="beslock-classic-summary-installation-meta__item">
            <span class="beslock-classic-summary-installation-meta__label"><?php esc_html_e( 'Ciudad de instalación:', 'beslock-custom' ); ?></span>
            <span class="beslock-classic-summary-installation-meta__value"><?php echo esc_html( $installation_city ); ?></span>
          </span>
        <?php endif; ?>
      </span>
      <?php
      $installation_meta = ob_get_clean();
    }

    return sprintf(
      '<span class="beslock-classic-summary-product beslock-classic-summary-product--installation"><span class="beslock-classic-summary-product__name">%1$s</span>%2$s</span>',
      esc_html__( 'Servicio de instalación', 'beslock-custom' ),
      $installation_meta
    );
  }

  $thumbnail = $product->get_image(
    'woocommerce_thumbnail',
    array(
      'class' => 'beslock-classic-summary-product__image',
      'alt'   => $product->get_name(),
    )
  );

  return sprintf(
    '<span class="beslock-classic-summary-product"><span class="beslock-classic-summary-product__media">%1$s</span><span class="beslock-classic-summary-product__name">%2$s</span></span>',
    $thumbnail,
    esc_html( $product->get_name() )
  );
}
add_filter( 'woocommerce_cart_item_name', 'beslock_checkout_cart_item_name', 20, 3 );

function beslock_checkout_cart_item_quantity( $quantity_html, $cart_item, $cart_item_key ) {
  if ( ! beslock_is_checkout_form_page() || empty( $cart_item['quantity'] ) ) {
    return $quantity_html;
  }

  if ( ! empty( $cart_item['data'] ) && is_a( $cart_item['data'], 'WC_Product' ) ) {
    $sku = (string) $cart_item['data']->get_sku();

    if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
      return '';
    }
  }

  return '<span class="beslock-classic-summary-qty">' . esc_html( (string) $cart_item['quantity'] ) . '</span>';
}
add_filter( 'woocommerce_checkout_cart_item_quantity', 'beslock_checkout_cart_item_quantity', 20, 3 );

function beslock_checkout_hide_installation_cart_item_data( $item_data, $cart_item ) {
  if ( ! beslock_is_checkout_form_page() || empty( $cart_item['data'] ) || ! is_a( $cart_item['data'], 'WC_Product' ) ) {
    return $item_data;
  }

  $sku = (string) $cart_item['data']->get_sku();

  if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
    return array();
  }

  return $item_data;
}
add_filter( 'woocommerce_get_item_data', 'beslock_checkout_hide_installation_cart_item_data', 20, 2 );
