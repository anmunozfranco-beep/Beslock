<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( ! function_exists( 'beslock_get_support_installation_product_options' ) ) {
  function beslock_get_support_installation_product_options() {
    static $options = null;

    if ( null !== $options ) {
      return $options;
    }

    $options   = array();
    $data_file = trailingslashit( get_stylesheet_directory() ) . 'data/products.json';

    if ( is_readable( $data_file ) ) {
      $products_data = json_decode( file_get_contents( $data_file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

      if ( is_array( $products_data ) ) {
        foreach ( $products_data as $product_data ) {
          $slug = ! empty( $product_data['slug'] ) ? sanitize_title( $product_data['slug'] ) : '';

          if ( '' === $slug ) {
            continue;
          }

          $product_post = get_page_by_path( $slug, OBJECT, 'product' );

          if ( ! $product_post || 'publish' !== get_post_status( $product_post ) ) {
            continue;
          }

          $options[] = array(
            'slug'       => $slug,
            'title'      => ! empty( $product_data['title'] ) ? sanitize_text_field( $product_data['title'] ) : get_the_title( $product_post ),
            'product_id' => absint( $product_post->ID ),
          );
        }
      }
    }

    if ( empty( $options ) && function_exists( 'wc_get_products' ) ) {
      $products = wc_get_products(
        array(
          'status'  => 'publish',
          'limit'   => -1,
          'orderby' => 'menu_order',
          'order'   => 'ASC',
        )
      );

      foreach ( $products as $product ) {
        if ( ! $product || ! is_a( $product, 'WC_Product' ) || 0 === strpos( (string) $product->get_sku(), 'BESLOCK-INST-' ) ) {
          continue;
        }

        $options[] = array(
          'slug'       => $product->get_slug(),
          'title'      => $product->get_name(),
          'product_id' => absint( $product->get_id() ),
        );
      }
    }

    return $options;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_product_by_slug' ) ) {
  function beslock_get_support_installation_product_by_slug( $slug ) {
    $slug = sanitize_title( $slug );

    if ( '' === $slug || ! function_exists( 'wc_get_product' ) ) {
      return null;
    }

    foreach ( beslock_get_support_installation_product_options() as $product_option ) {
      if ( $slug === $product_option['slug'] && ! empty( $product_option['product_id'] ) ) {
        return wc_get_product( absint( $product_option['product_id'] ) );
      }
    }

    return null;
  }
}

if ( ! function_exists( 'beslock_support_installation_send_error' ) ) {
  function beslock_support_installation_send_error( $message ) {
    wp_send_json_error(
      array(
        'message' => $message,
      ),
      400
    );
  }
}

if ( ! function_exists( 'beslock_support_installation_format_price' ) ) {
  function beslock_support_installation_format_price( $amount ) {
    if ( function_exists( 'wc_price' ) ) {
      return html_entity_decode( wp_strip_all_tags( wc_price( $amount ) ), ENT_QUOTES, get_bloginfo( 'charset' ) );
    }

    return (string) $amount;
  }
}

if ( ! function_exists( 'beslock_support_installation_default_message' ) ) {
  function beslock_support_installation_default_message() {
    return __( 'Quisiera saber si pueden prestar el servicio de instalación según la ciudad indicada', 'beslock-custom' );
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_from_request' ) ) {
  function beslock_get_support_installation_order_from_request() {
    if ( ! function_exists( 'wc_get_order' ) ) {
      beslock_support_installation_send_error( __( 'No pudimos validar el pedido en este momento.', 'beslock-custom' ) );
    }

    $order_number = isset( $_POST['order_number'] ) ? sanitize_text_field( wp_unslash( $_POST['order_number'] ) ) : '';
    $email        = isset( $_POST['order_email'] ) ? sanitize_email( wp_unslash( $_POST['order_email'] ) ) : '';
    $order_id     = absint( preg_replace( '/\D+/', '', $order_number ) );

    if ( $order_id <= 0 ) {
      beslock_support_installation_send_error( __( 'Ingresa el número de pedido.', 'beslock-custom' ) );
    }

    if ( '' === trim( $email ) || ! is_email( $email ) ) {
      beslock_support_installation_send_error( __( 'Ingresa el correo electrónico asociado al pedido.', 'beslock-custom' ) );
    }

    $order = wc_get_order( $order_id );

    if ( ! $order ) {
      beslock_support_installation_send_error( __( 'No encontramos ese pedido. Revisa el número o usa la opción sin pedido.', 'beslock-custom' ) );
    }

    $order_email = sanitize_email( $order->get_billing_email() );

    if ( '' === $order_email || strtolower( $email ) !== strtolower( $order_email ) ) {
      beslock_support_installation_send_error( __( 'El correo no coincide con el pedido indicado.', 'beslock-custom' ) );
    }

    return $order;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_contact_name' ) ) {
  function beslock_get_support_installation_order_contact_name( $order ) {
    $name = trim( (string) $order->get_shipping_first_name() . ' ' . (string) $order->get_shipping_last_name() );

    if ( '' === $name ) {
      $name = trim( (string) $order->get_billing_first_name() . ' ' . (string) $order->get_billing_last_name() );
    }

    return $name;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_address' ) ) {
  function beslock_get_support_installation_order_address( $order ) {
    $line_1 = trim( (string) ( $order->get_shipping_address_1() ?: $order->get_billing_address_1() ) );
    $line_2 = trim( (string) ( $order->get_shipping_address_2() ?: $order->get_billing_address_2() ) );

    return trim( implode( ', ', array_filter( array( $line_1, $line_2 ) ) ) );
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_city' ) ) {
  function beslock_get_support_installation_order_city( $order ) {
    return trim( (string) ( $order->get_shipping_city() ?: $order->get_billing_city() ) );
  }
}

if ( ! function_exists( 'beslock_get_support_installation_product_source_by_slug' ) ) {
  function beslock_get_support_installation_product_source_by_slug( $slug ) {
    static $products = null;

    $slug = sanitize_title( $slug );

    if ( null === $products ) {
      $products  = array();
      $data_file = trailingslashit( get_stylesheet_directory() ) . 'data/products.json';

      if ( is_readable( $data_file ) ) {
        $products_data = json_decode( file_get_contents( $data_file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

        if ( is_array( $products_data ) ) {
          foreach ( $products_data as $product_data ) {
            if ( ! empty( $product_data['slug'] ) ) {
              $products[ sanitize_title( $product_data['slug'] ) ] = $product_data;
            }
          }
        }
      }
    }

    return isset( $products[ $slug ] ) && is_array( $products[ $slug ] ) ? $products[ $slug ] : array();
  }
}

if ( ! function_exists( 'beslock_get_support_installation_type_source_by_sku' ) ) {
  function beslock_get_support_installation_type_source_by_sku( $sku ) {
    static $types = null;

    $sku = sanitize_text_field( (string) $sku );

    if ( null === $types ) {
      $types       = array();
      $source_file = trailingslashit( get_stylesheet_directory() ) . 'data/product-pricing-source.json';

      if ( is_readable( $source_file ) ) {
        $source = json_decode( file_get_contents( $source_file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

        if ( is_array( $source ) && ! empty( $source['installation_types'] ) && is_array( $source['installation_types'] ) ) {
          foreach ( $source['installation_types'] as $type ) {
            if ( ! empty( $type['sku'] ) ) {
              $types[ sanitize_text_field( $type['sku'] ) ] = is_array( $type ) ? $type : array();
            }
          }
        }
      }
    }

    return isset( $types[ $sku ] ) ? $types[ $sku ] : array();
  }
}

if ( ! function_exists( 'beslock_ensure_support_installation_product' ) ) {
  function beslock_ensure_support_installation_product( $item ) {
    if ( ! function_exists( 'wc_get_product_id_by_sku' ) || ! class_exists( 'WC_Product_Simple' ) ) {
      return 0;
    }

    $item = is_array( $item ) ? $item : array();
    $sku  = ! empty( $item['installation_sku'] ) ? sanitize_text_field( $item['installation_sku'] ) : '';

    if ( '' === $sku ) {
      return 0;
    }

    $product_id = absint( wc_get_product_id_by_sku( $sku ) );

    if ( $product_id > 0 ) {
      return $product_id;
    }

    $type_source = beslock_get_support_installation_type_source_by_sku( $sku );
    $price       = ! empty( $item['price'] ) ? (float) wc_format_decimal( $item['price'] ) : 0.0;

    if ( $price <= 0 && isset( $type_source['price'] ) ) {
      $price = (float) wc_format_decimal( $type_source['price'] );
    }

    if ( $price <= 0 ) {
      return 0;
    }

    $name = ! empty( $type_source['name'] )
      ? sanitize_text_field( $type_source['name'] )
      : __( 'Instalación BESLOCK', 'beslock-custom' );

    $description = ! empty( $type_source['description'] )
      ? sanitize_textarea_field( $type_source['description'] )
      : __( 'Servicio de instalación BESLOCK para ciudades habilitadas.', 'beslock-custom' );

    $product = new WC_Product_Simple();
    $product->set_name( $name );
    $product->set_slug( sanitize_title( $name ) );
    $product->set_sku( $sku );
    $product->set_status( 'publish' );
    $product->set_catalog_visibility( 'hidden' );
    $product->set_virtual( true );
    $product->set_sold_individually( false );
    $product->set_reviews_allowed( false );
    $product->set_tax_status( 'none' );
    $product->set_regular_price( (string) $price );
    $product->set_price( (string) $price );
    $product->set_short_description( $description );
    $product->set_description( $description );

    $product_id = absint( $product->save() );

    if ( $product_id <= 0 ) {
      return 0;
    }

    update_post_meta( $product_id, '_beslock_installation_generated', 'yes' );
    update_post_meta( $product_id, '_beslock_installation_price', $price );

    if ( ! empty( $type_source['id'] ) ) {
      update_post_meta( $product_id, '_beslock_installation_type', sanitize_text_field( $type_source['id'] ) );
    }

    if ( ! empty( $type_source['applies_to'] ) && is_array( $type_source['applies_to'] ) ) {
      update_post_meta( $product_id, '_beslock_installation_applies_to', implode( '|', array_map( 'sanitize_title', $type_source['applies_to'] ) ) );
    }

    return $product_id;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_data_for_product' ) ) {
  function beslock_get_support_installation_data_for_product( $product ) {
    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
      return array();
    }

    $sku = (string) $product->get_sku();

    if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
      return array();
    }

    $product_id        = absint( $product->get_id() );
    $installation_sku  = get_post_meta( $product_id, '_beslock_installation_sku', true );
    $installation_type = get_post_meta( $product_id, '_beslock_installation_type', true );
    $price             = get_post_meta( $product_id, '_beslock_installation_price', true );

    if ( '' === (string) $installation_sku || '' === (string) $price || '' === (string) $installation_type ) {
      $source = beslock_get_support_installation_product_source_by_slug( $product->get_slug() );

      if ( '' === (string) $installation_sku && isset( $source['installation_product_sku'] ) ) {
        $installation_sku = $source['installation_product_sku'];
      }

      if ( '' === (string) $installation_type && isset( $source['installation_type'] ) ) {
        $installation_type = $source['installation_type'];
      }

      if ( '' === (string) $price && isset( $source['installation_price'] ) ) {
        $price = $source['installation_price'];
      }
    }

    $price = (float) wc_format_decimal( $price );

    if ( '' === (string) $installation_sku || $price <= 0 ) {
      return array();
    }

    return array(
      'sku'   => sanitize_text_field( $installation_sku ),
      'type'  => sanitize_text_field( $installation_type ),
      'price' => $price,
    );
  }
}

if ( ! function_exists( 'beslock_support_installation_is_city_directly_available' ) ) {
  function beslock_support_installation_is_city_directly_available( $city ) {
    if ( function_exists( 'beslock_is_cart_installation_city_available' ) ) {
      return beslock_is_cart_installation_city_available( $city );
    }

    $city_key = function_exists( 'remove_accents' )
      ? strtolower( remove_accents( trim( (string) $city ) ) )
      : strtolower( trim( (string) $city ) );

    return in_array( $city_key, array( 'bogota', 'medellin', 'cali', 'barranquilla' ), true );
  }
}

if ( ! function_exists( 'beslock_order_has_support_installation_purchased' ) ) {
  function beslock_order_has_support_installation_purchased( $order ) {
    foreach ( $order->get_fees() as $fee ) {
      if ( false !== stripos( $fee->get_name(), 'Instalación BESLOCK' ) && (float) $fee->get_total() > 0 ) {
        return true;
      }
    }

    foreach ( $order->get_items() as $item ) {
      $product = $item->get_product();
      $sku     = $product ? (string) $product->get_sku() : '';

      if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
        return true;
      }
    }

    return false;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_quote' ) ) {
  function beslock_get_support_installation_order_quote( $order ) {
    $quote = array(
      'items' => array(),
      'total' => 0.0,
    );

    foreach ( $order->get_items() as $item ) {
      $product = $item->get_product();
      $data    = beslock_get_support_installation_data_for_product( $product );

      if ( empty( $data ) ) {
        continue;
      }

      $quantity = max( 1, (int) $item->get_quantity() );
      $total    = $data['price'] * $quantity;

      $quote['items'][] = array(
        'name'                   => $item->get_name(),
        'quantity'               => $quantity,
        'installation_sku'       => $data['sku'],
        'installation_product_id' => function_exists( 'wc_get_product_id_by_sku' ) ? absint( wc_get_product_id_by_sku( $data['sku'] ) ) : 0,
        'price'                  => $data['price'],
        'price_html'             => beslock_support_installation_format_price( $data['price'] ),
        'total'                  => $total,
        'total_html'             => beslock_support_installation_format_price( $total ),
      );
      $quote['total'] += $total;
    }

    $quote['total_html'] = beslock_support_installation_format_price( $quote['total'] );

    return $quote;
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_installation_state' ) ) {
  function beslock_get_support_installation_order_installation_state( $order ) {
    $city       = beslock_get_support_installation_order_city( $order );
    $purchased  = beslock_order_has_support_installation_purchased( $order );
    $quote      = beslock_get_support_installation_order_quote( $order );
    $direct     = beslock_support_installation_is_city_directly_available( $city );
    $can_buy    = ! $purchased && $direct && ! empty( $quote['items'] ) && $quote['total'] > 0;

    return array(
      'purchased'           => $purchased,
      'direct_available'    => $direct,
      'can_purchase'        => $can_buy,
      'total'               => $quote['total'],
      'total_html'          => $quote['total_html'],
      'items'               => $quote['items'],
      'customer_note'       => trim( (string) $order->get_customer_note() ),
    );
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_payload' ) ) {
  function beslock_get_support_installation_order_payload( $order ) {
    return array(
      'name'         => beslock_get_support_installation_order_contact_name( $order ),
      'phone'        => trim( (string) $order->get_billing_phone() ),
      'city'         => beslock_get_support_installation_order_city( $order ),
      'address'      => beslock_get_support_installation_order_address( $order ),
      'installation' => beslock_get_support_installation_order_installation_state( $order ),
    );
  }
}

if ( ! function_exists( 'beslock_get_support_installation_order_lookup_message' ) ) {
  function beslock_get_support_installation_order_lookup_message( $payload ) {
    $installation = isset( $payload['installation'] ) && is_array( $payload['installation'] )
      ? $payload['installation']
      : array();

    if ( empty( $installation['purchased'] ) && empty( $installation['direct_available'] ) ) {
      return __( 'Pedido confirmado sin instalacion por cobertura geografica', 'beslock-custom' );
    }

    if ( ! empty( $installation['can_purchase'] ) ) {
      return __( 'Pedido confirmado. Puedes comprar la instalación para este pedido.', 'beslock-custom' );
    }

    if ( ! empty( $installation['purchased'] ) ) {
      return __( 'Pedido confirmado. Revisa los datos de instalación antes de programar.', 'beslock-custom' );
    }

    return __( 'Pedido confirmado.', 'beslock-custom' );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_order_lookup' ) ) {
  function beslock_handle_support_installation_order_lookup() {
    $order   = beslock_get_support_installation_order_from_request();
    $payload = beslock_get_support_installation_order_payload( $order );

    wp_send_json_success(
      array(
        'message' => beslock_get_support_installation_order_lookup_message( $payload ),
        'order'   => $payload,
      )
    );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_purchase_request' ) ) {
  function beslock_handle_support_installation_purchase_request() {
    if ( ! function_exists( 'WC' ) || ! function_exists( 'wc_get_product' ) ) {
      beslock_support_installation_send_error( __( 'No pudimos iniciar la compra de instalación en este momento.', 'beslock-custom' ) );
    }

    if ( null === WC()->cart && function_exists( 'wc_load_cart' ) ) {
      wc_load_cart();
    }

    if ( ! WC()->cart ) {
      beslock_support_installation_send_error( __( 'No pudimos preparar el carrito de instalación.', 'beslock-custom' ) );
    }

    $order        = beslock_get_support_installation_order_from_request();
    $installation = beslock_get_support_installation_order_installation_state( $order );

    if ( ! empty( $installation['purchased'] ) ) {
      beslock_support_installation_send_error( __( 'Este pedido ya tiene instalación adquirida. Puedes programarla desde esta misma pantalla.', 'beslock-custom' ) );
    }

    if ( empty( $installation['direct_available'] ) ) {
      beslock_support_installation_send_error( __( 'Para esta ciudad debemos consultar la cobertura antes de ofrecer la compra directa de instalación.', 'beslock-custom' ) );
    }

    if ( empty( $installation['can_purchase'] ) || empty( $installation['items'] ) ) {
      beslock_support_installation_send_error( __( 'No encontramos un valor de instalación disponible para los productos de este pedido.', 'beslock-custom' ) );
    }

    $order_id = absint( $order->get_id() );

    foreach ( WC()->cart->get_cart() as $cart_item_key => $cart_item ) {
      if ( ! empty( $cart_item['beslock_installation_parent_order_id'] ) && absint( $cart_item['beslock_installation_parent_order_id'] ) === $order_id ) {
        WC()->cart->remove_cart_item( $cart_item_key );
      }
    }

    $city    = beslock_get_support_installation_order_city( $order );
    $address = beslock_get_support_installation_order_address( $order );

    foreach ( $installation['items'] as $item ) {
      $installation_product_id = ! empty( $item['installation_product_id'] ) ? absint( $item['installation_product_id'] ) : 0;
      $quantity                = ! empty( $item['quantity'] ) ? max( 1, absint( $item['quantity'] ) ) : 1;

      if ( $installation_product_id <= 0 ) {
        $installation_product_id = beslock_ensure_support_installation_product( $item );
      }

      if ( $installation_product_id <= 0 ) {
        beslock_support_installation_send_error( __( 'No pudimos preparar el producto de instalación asociado a este pedido.', 'beslock-custom' ) );
      }

      $installation_product = wc_get_product( $installation_product_id );

      if ( ! $installation_product || ! $installation_product->is_purchasable() ) {
        beslock_support_installation_send_error( __( 'La instalación no está disponible para compra en este momento.', 'beslock-custom' ) );
      }

      WC()->cart->add_to_cart(
        $installation_product_id,
        $quantity,
        0,
        array(),
        array(
          'beslock_installation_parent_order_id'     => $order_id,
          'beslock_installation_parent_order_number' => $order->get_order_number(),
          'beslock_installation_city'                => $city,
          'beslock_installation_address'             => $address,
          'beslock_installation_source_product'      => ! empty( $item['name'] ) ? sanitize_text_field( $item['name'] ) : '',
        )
      );
    }

    WC()->cart->calculate_totals();

    wp_send_json_success(
      array(
        'message'  => __( 'Instalación agregada al carrito.', 'beslock-custom' ),
        'redirect' => wc_get_cart_url(),
      )
    );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_info_request' ) ) {
  function beslock_handle_support_installation_info_request() {
    $order        = beslock_get_support_installation_order_from_request();
    $installation = beslock_get_support_installation_order_installation_state( $order );
    $city         = beslock_get_support_installation_order_city( $order );
    $message      = isset( $_POST['installation_info_message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['installation_info_message'] ) ) : '';

    if ( '' === trim( $message ) ) {
      $message = beslock_support_installation_default_message();
    }

    if ( ! empty( $installation['purchased'] ) ) {
      beslock_support_installation_send_error( __( 'Este pedido ya tiene instalación adquirida. Puedes programarla desde esta misma pantalla.', 'beslock-custom' ) );
    }

    if ( ! empty( $installation['direct_available'] ) ) {
      beslock_support_installation_send_error( __( 'Para esta ciudad el servicio está disponible para compra directa.', 'beslock-custom' ) );
    }

    $order->update_meta_data( '_beslock_installation_info_requested', 'yes' );
    $order->update_meta_data( '_beslock_installation_info_requested_at', current_time( 'mysql' ) );
    $order->update_meta_data( '_beslock_installation_info_message', $message );

    $note = sprintf(
      /* translators: 1: city, 2: customer message. */
      __( "Solicitud de información de instalación recibida desde el sitio. Ciudad del pedido: %1\$s. El equipo debe validar cobertura e informar si es posible prestar el servicio.\n\nObservaciones o solicitudes: %2\$s", 'beslock-custom' ),
      '' !== $city ? $city : __( 'sin ciudad registrada', 'beslock-custom' ),
      $message
    );

    $order->add_order_note( $note );
    $order->save();

    wp_send_json_success(
      array(
        'message' => __( 'Solicitud recibida. Nuestro equipo humano estará contactándose para coordinar la instalación o informarte la disponibilidad del servicio.', 'beslock-custom' ),
      )
    );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_order_request' ) ) {
  function beslock_handle_support_installation_order_request() {
    $order        = beslock_get_support_installation_order_from_request();
    $installation = beslock_get_support_installation_order_installation_state( $order );
    $address      = isset( $_POST['installation_address'] ) ? sanitize_text_field( wp_unslash( $_POST['installation_address'] ) ) : '';
    $date         = isset( $_POST['installation_requested_date'] ) ? sanitize_text_field( wp_unslash( $_POST['installation_requested_date'] ) ) : '';
    $time         = isset( $_POST['installation_requested_time'] ) ? sanitize_text_field( wp_unslash( $_POST['installation_requested_time'] ) ) : '';

    if ( empty( $installation['purchased'] ) ) {
      beslock_support_installation_send_error( __( 'La instalación aún no fue adquirida para este pedido.', 'beslock-custom' ) );
    }

    if ( '' === trim( $address ) ) {
      beslock_support_installation_send_error( __( 'Ingresa la dirección de instalación.', 'beslock-custom' ) );
    }

    if ( '' === trim( $date ) || ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $date ) ) {
      beslock_support_installation_send_error( __( 'Ingresa una fecha tentativa para la instalación.', 'beslock-custom' ) );
    }

    if ( '' === trim( $time ) || ! preg_match( '/^\d{2}:\d{2}$/', $time ) ) {
      beslock_support_installation_send_error( __( 'Ingresa una hora tentativa para la instalación.', 'beslock-custom' ) );
    }

    $city = beslock_get_support_installation_order_city( $order );

    $order->update_meta_data( '_beslock_installation_schedule_requested', 'yes' );
    $order->update_meta_data( '_beslock_installation_address_override', $address );
    $order->update_meta_data( '_beslock_installation_requested_date', $date );
    $order->update_meta_data( '_beslock_installation_requested_time', $time );

    $note = sprintf(
      /* translators: 1: address, 2: city, 3: requested date, 4: requested time. */
      __( 'Solicitud de programación de instalación recibida desde el sitio. Dirección indicada: %1$s. Ciudad del pedido: %2$s. Fecha tentativa: %3$s. Hora tentativa: %4$s.', 'beslock-custom' ),
      $address,
      '' !== $city ? $city : __( 'sin ciudad registrada', 'beslock-custom' ),
      $date,
      $time
    );

    $order->add_order_note( $note );
    $order->save();

    wp_send_json_success(
      array(
        'message' => __( 'Solicitud recibida. Nuestro equipo humano estará contactándose para coordinar la instalación.', 'beslock-custom' ),
      )
    );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_no_order_request' ) ) {
  function beslock_handle_support_installation_no_order_request() {
    $name    = isset( $_POST['contact_name'] ) ? sanitize_text_field( wp_unslash( $_POST['contact_name'] ) ) : '';
    $email   = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
    $city    = isset( $_POST['city'] ) ? sanitize_text_field( wp_unslash( $_POST['city'] ) ) : '';
    $address = isset( $_POST['installation_address'] ) ? sanitize_text_field( wp_unslash( $_POST['installation_address'] ) ) : '';
    $message = isset( $_POST['installation_message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['installation_message'] ) ) : '';
    $slug    = isset( $_POST['product_model'] ) ? sanitize_title( wp_unslash( $_POST['product_model'] ) ) : '';

    if ( '' === trim( $message ) ) {
      $message = beslock_support_installation_default_message();
    }

    if ( '' === trim( $name ) ) {
      beslock_support_installation_send_error( __( 'Ingresa tu nombre.', 'beslock-custom' ) );
    }

    if ( '' === trim( $email ) || ! is_email( $email ) ) {
      beslock_support_installation_send_error( __( 'Ingresa un correo electrónico válido.', 'beslock-custom' ) );
    }

    if ( '' === trim( $city ) ) {
      beslock_support_installation_send_error( __( 'Ingresa la ciudad de instalación.', 'beslock-custom' ) );
    }

    if ( '' === trim( $address ) ) {
      beslock_support_installation_send_error( __( 'Ingresa la dirección de instalación.', 'beslock-custom' ) );
    }

    $product = beslock_get_support_installation_product_by_slug( $slug );

    if ( ! $product ) {
      beslock_support_installation_send_error( __( 'Selecciona el modelo BESLOCK relacionado con la solicitud.', 'beslock-custom' ) );
    }

    $content = sprintf(
      /* translators: 1: product name, 2: city, 3: customer message. */
      __( "Consulta de instalación para %1\$s en %2\$s.\n\n%3\$s", 'beslock-custom' ),
      $product->get_name(),
      $city,
      $message
    );

    $comment_id = wp_new_comment(
      wp_slash(
        array(
          'comment_post_ID'      => absint( $product->get_id() ),
          'comment_content'      => $content,
          'comment_author'       => $name,
          'comment_author_email' => $email,
          'comment_approved'     => 0,
        )
      ),
      true
    );

    if ( is_wp_error( $comment_id ) ) {
      beslock_support_installation_send_error( __( 'No pudimos enviar la solicitud. Verifica los datos e inténtalo de nuevo.', 'beslock-custom' ) );
    }

    update_comment_meta( $comment_id, 'interaction_type', 'question' );
    update_comment_meta( $comment_id, 'beslock_installation_request_type', 'no_order' );
    update_comment_meta( $comment_id, 'beslock_installation_city', $city );
    update_comment_meta( $comment_id, 'beslock_installation_address_private', $address );
    update_comment_meta( $comment_id, 'beslock_installation_message_private', $message );
    update_comment_meta( $comment_id, 'beslock_installation_product_model', $product->get_name() );

    wp_send_json_success(
      array(
        'commentId' => absint( $comment_id ),
        'message'   => __( 'Solicitud enviada. Quedó como consulta pendiente del modelo seleccionado y será revisada antes de publicarse.', 'beslock-custom' ),
      )
    );
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_request' ) ) {
  function beslock_handle_support_installation_request() {
    if ( ! check_ajax_referer( 'beslock_support_installation', 'nonce', false ) ) {
      beslock_support_installation_send_error( __( 'No pudimos validar la sesión. Recarga la página e inténtalo nuevamente.', 'beslock-custom' ) );
    }

    $request_type = isset( $_POST['beslock_installation_request_type'] ) ? sanitize_key( wp_unslash( $_POST['beslock_installation_request_type'] ) ) : 'order';
    $step         = isset( $_POST['beslock_installation_step'] ) ? sanitize_key( wp_unslash( $_POST['beslock_installation_step'] ) ) : 'submit';

    if ( 'no_order' === $request_type ) {
      beslock_handle_support_installation_no_order_request();
    }

    if ( 'lookup_order' === $step ) {
      beslock_handle_support_installation_order_lookup();
    }

    if ( 'purchase_installation' === $step ) {
      beslock_handle_support_installation_purchase_request();
    }

    if ( 'request_installation_info' === $step ) {
      beslock_handle_support_installation_info_request();
    }

    beslock_handle_support_installation_order_request();
  }
}

if ( ! function_exists( 'beslock_handle_support_installation_nonce_request' ) ) {
  function beslock_handle_support_installation_nonce_request() {
    wp_send_json_success(
      array(
        'nonce' => wp_create_nonce( 'beslock_support_installation' ),
      )
    );
  }
}

add_action( 'wp_ajax_beslock_support_installation_request', 'beslock_handle_support_installation_request' );
add_action( 'wp_ajax_nopriv_beslock_support_installation_request', 'beslock_handle_support_installation_request' );
add_action( 'wp_ajax_beslock_support_installation_nonce', 'beslock_handle_support_installation_nonce_request' );
add_action( 'wp_ajax_nopriv_beslock_support_installation_nonce', 'beslock_handle_support_installation_nonce_request' );

add_filter( 'woocommerce_get_item_data', function( $item_data, $cart_item ) {
  if ( empty( $cart_item['beslock_installation_parent_order_number'] ) ) {
    return $item_data;
  }

  $item_data[] = array(
    'key'   => __( 'Pedido asociado', 'beslock-custom' ),
    'value' => sanitize_text_field( $cart_item['beslock_installation_parent_order_number'] ),
  );

  if ( ! empty( $cart_item['beslock_installation_city'] ) ) {
    $item_data[] = array(
      'key'   => __( 'Ciudad de instalación', 'beslock-custom' ),
      'value' => sanitize_text_field( $cart_item['beslock_installation_city'] ),
    );
  }

  return $item_data;
}, 10, 2 );

add_action( 'woocommerce_checkout_create_order_line_item', function( $item, $cart_item_key, $values ) {
  if ( empty( $values['beslock_installation_parent_order_id'] ) ) {
    return;
  }

  $item->add_meta_data( __( 'Pedido asociado', 'beslock-custom' ), sanitize_text_field( $values['beslock_installation_parent_order_number'] ?? '' ), true );
  $item->add_meta_data( __( 'Ciudad de instalación', 'beslock-custom' ), sanitize_text_field( $values['beslock_installation_city'] ?? '' ), true );
  $item->add_meta_data( __( 'Dirección de instalación', 'beslock-custom' ), sanitize_text_field( $values['beslock_installation_address'] ?? '' ), true );
}, 10, 3 );
