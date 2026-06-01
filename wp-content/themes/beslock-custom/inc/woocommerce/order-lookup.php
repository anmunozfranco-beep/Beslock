<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

function beslock_is_order_lookup_request() {
  if ( is_admin() ) {
    return false;
  }

  if ( get_query_var( 'beslock_order_lookup' ) ) {
    return true;
  }

  $request_uri = isset( $_SERVER['REQUEST_URI'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '';
  $path        = trim( (string) wp_parse_url( $request_uri, PHP_URL_PATH ), '/' );

  return 'consulta-pedido' === $path;
}

add_action( 'init', function() {
  add_rewrite_rule( '^consulta-pedido/?$', 'index.php?beslock_order_lookup=1', 'top' );
} );

add_filter( 'query_vars', function( $vars ) {
  $vars[] = 'beslock_order_lookup';
  return $vars;
} );

add_action( 'after_switch_theme', function() {
  flush_rewrite_rules();
} );

add_action( 'wp_enqueue_scripts', function() {
  if ( ! beslock_is_order_lookup_request() ) {
    return;
  }

  $css_path = get_stylesheet_directory() . '/assets/css/order-lookup.css';
  if ( file_exists( $css_path ) ) {
    wp_enqueue_style(
      'beslock-order-lookup',
      get_stylesheet_directory_uri() . '/assets/css/order-lookup.css',
      array( 'beslock-main-style', 'beslock-wc-scope-fix' ),
      filemtime( $css_path )
    );
  }
}, 32 );

add_filter( 'pre_get_document_title', function( $title ) {
  if ( beslock_is_order_lookup_request() ) {
    return __( 'Consulta tu pedido - beslock', 'beslock-custom' );
  }

  return $title;
} );

add_action( 'template_redirect', function() {
  if ( ! beslock_is_order_lookup_request() ) {
    return;
  }

  global $wp_query;
  if ( $wp_query ) {
    $wp_query->is_404  = false;
    $wp_query->is_page = true;
  }

  status_header( 200 );
  nocache_headers();
  beslock_render_order_lookup_page();
  exit;
}, 1 );

function beslock_get_first_order_meta_value( WC_Order $order, array $keys ) {
  foreach ( $keys as $key ) {
    $value = $order->get_meta( $key, true );
    if ( is_scalar( $value ) && '' !== trim( (string) $value ) ) {
      return sanitize_text_field( (string) $value );
    }
  }

  return '';
}

function beslock_get_order_tracking_data( WC_Order $order ) {
  $carrier = beslock_get_first_order_meta_value(
    $order,
    array(
      '_shipping_carrier',
      'shipping_carrier',
      '_carrier',
      'carrier',
      '_tracking_provider',
      '_wc_shipment_tracking_provider',
      '_aftership_tracking_provider_name',
    )
  );

  $tracking_number = beslock_get_first_order_meta_value(
    $order,
    array(
      '_tracking_number',
      'tracking_number',
      '_wc_shipment_tracking_number',
      '_aftership_tracking_number',
      '_tracking_code',
      'guia',
      '_guia',
    )
  );

  $shipment_items = $order->get_meta( '_wc_shipment_tracking_items', true );
  if ( is_array( $shipment_items ) && ! empty( $shipment_items ) ) {
    $first_item = reset( $shipment_items );
    if ( is_array( $first_item ) ) {
      if ( '' === $carrier && ! empty( $first_item['tracking_provider'] ) ) {
        $carrier = sanitize_text_field( (string) $first_item['tracking_provider'] );
      }
      if ( '' === $tracking_number && ! empty( $first_item['tracking_number'] ) ) {
        $tracking_number = sanitize_text_field( (string) $first_item['tracking_number'] );
      }
    }
  }

  return array(
    'carrier'         => $carrier,
    'tracking_number' => $tracking_number,
  );
}

function beslock_get_order_preparation_status( WC_Order $order ) {
  switch ( $order->get_status() ) {
    case 'processing':
      return __( 'En preparación', 'beslock-custom' );
    case 'completed':
      return __( 'Completado', 'beslock-custom' );
    case 'on-hold':
      return __( 'En revisión', 'beslock-custom' );
    case 'pending':
      return __( 'Pendiente de confirmación', 'beslock-custom' );
    case 'cancelled':
      return __( 'Cancelado', 'beslock-custom' );
    case 'refunded':
      return __( 'Reembolsado', 'beslock-custom' );
    case 'failed':
      return __( 'No confirmado', 'beslock-custom' );
    default:
      return wc_get_order_status_name( $order->get_status() );
  }
}

function beslock_get_order_payment_status( WC_Order $order ) {
  if ( $order->is_paid() ) {
    return __( 'Pago confirmado', 'beslock-custom' );
  }

  switch ( $order->get_status() ) {
    case 'failed':
      return __( 'Pago no confirmado', 'beslock-custom' );
    case 'cancelled':
      return __( 'Pedido cancelado', 'beslock-custom' );
    default:
      return __( 'Pendiente de pago', 'beslock-custom' );
  }
}

function beslock_get_order_timeline_events( WC_Order $order, $order_date, array $tracking ) {
  $status   = $order->get_status();
  $is_paid  = $order->is_paid();
  $is_issue = in_array( $status, array( 'cancelled', 'failed', 'refunded' ), true );

  $payment_state = $is_paid ? 'complete' : 'current';
  if ( $is_issue ) {
    $payment_state = 'issue';
  }

  $preparation_state = 'pending';
  if ( $is_issue ) {
    $preparation_state = 'issue';
  } elseif ( 'completed' === $status ) {
    $preparation_state = 'complete';
  } elseif ( in_array( $status, array( 'processing', 'on-hold' ), true ) || $is_paid ) {
    $preparation_state = 'current';
  }

  $shipping_detail = __( 'Guía aún no disponible', 'beslock-custom' );
  if ( $tracking['carrier'] && $tracking['tracking_number'] ) {
    $shipping_detail = sprintf(
      /* translators: 1: carrier name, 2: tracking number */
      __( '%1$s · Guía %2$s', 'beslock-custom' ),
      $tracking['carrier'],
      $tracking['tracking_number']
    );
  } elseif ( $tracking['carrier'] ) {
    $shipping_detail = sprintf(
      /* translators: %s: carrier name */
      __( '%s · guía pendiente', 'beslock-custom' ),
      $tracking['carrier']
    );
  } elseif ( $tracking['tracking_number'] ) {
    $shipping_detail = sprintf(
      /* translators: %s: tracking number */
      __( 'Guía %s', 'beslock-custom' ),
      $tracking['tracking_number']
    );
  }

  $shipping_state = 'pending';
  if ( $is_issue ) {
    $shipping_state = 'issue';
  } elseif ( $tracking['carrier'] || $tracking['tracking_number'] || 'completed' === $status ) {
    $shipping_state = 'complete';
  }

  return array(
    array(
      'title'  => __( 'Pedido recibido', 'beslock-custom' ),
      'detail' => $order_date,
      'state'  => 'complete',
    ),
    array(
      'title'  => __( 'Pago', 'beslock-custom' ),
      'detail' => beslock_get_order_payment_status( $order ),
      'state'  => $payment_state,
    ),
    array(
      'title'  => __( 'Preparación', 'beslock-custom' ),
      'detail' => beslock_get_order_preparation_status( $order ),
      'state'  => $preparation_state,
    ),
    array(
      'title'  => __( 'Envío', 'beslock-custom' ),
      'detail' => $shipping_detail,
      'state'  => $shipping_state,
    ),
  );
}

function beslock_get_order_timeline_progress( array $events ) {
  $last_active_index = 0;
  foreach ( $events as $index => $event ) {
    if ( isset( $event['state'] ) && 'pending' !== $event['state'] ) {
      $last_active_index = (int) $index;
    }
  }

  $max_index = max( count( $events ) - 1, 1 );
  return max( 0, min( 1, $last_active_index / $max_index ) );
}

function beslock_find_order_for_lookup( $order_input, $email ) {
  if ( ! function_exists( 'wc_get_order' ) ) {
    return null;
  }

  $order_id = absint( preg_replace( '/\D+/', '', (string) $order_input ) );
  if ( ! $order_id || ! is_email( $email ) ) {
    return null;
  }

  $order = wc_get_order( $order_id );
  if ( ! $order instanceof WC_Order ) {
    return null;
  }

  $billing_email = strtolower( trim( (string) $order->get_billing_email() ) );
  $lookup_email  = strtolower( trim( (string) $email ) );

  if ( '' === $billing_email || $billing_email !== $lookup_email ) {
    return null;
  }

  return $order;
}

function beslock_get_order_lookup_state() {
  $state = array(
    'submitted' => false,
    'order'     => null,
    'error'     => '',
    'not_found' => false,
    'values'    => array(
      'order' => '',
      'email' => '',
    ),
  );

  $is_post = isset( $_SERVER['REQUEST_METHOD'] ) && 'POST' === strtoupper( sanitize_text_field( wp_unslash( $_SERVER['REQUEST_METHOD'] ) ) );
  if ( ! $is_post ) {
    return $state;
  }

  $state['submitted'] = true;
  $order_input        = isset( $_POST['beslock_order_number'] ) ? sanitize_text_field( wp_unslash( $_POST['beslock_order_number'] ) ) : '';
  $email              = isset( $_POST['beslock_order_email'] ) ? sanitize_email( wp_unslash( $_POST['beslock_order_email'] ) ) : '';

  $state['values']['order'] = $order_input;
  $state['values']['email'] = $email;

  if ( '' === trim( $order_input ) || ! is_email( $email ) ) {
    $state['error'] = __( 'Ingresa el número de pedido y un correo válido.', 'beslock-custom' );
    return $state;
  }

  $order = beslock_find_order_for_lookup( $order_input, $email );
  if ( ! $order ) {
    $state['not_found'] = true;
    return $state;
  }

  $state['order'] = $order;
  return $state;
}

function beslock_render_order_lookup_form( array $state ) {
  ?>
  <form class="beslock-order-lookup__form" method="post" action="<?php echo esc_url( home_url( '/consulta-pedido/' ) ); ?>" data-js="order-lookup-form" novalidate>
    <label class="beslock-order-lookup__field">
      <span>Número de pedido</span>
      <input type="text" name="beslock_order_number" inputmode="numeric" autocomplete="off" value="<?php echo esc_attr( $state['values']['order'] ); ?>" data-js="order-lookup-order" />
    </label>
    <label class="beslock-order-lookup__field">
      <span>Correo electrónico</span>
      <input type="email" name="beslock_order_email" autocomplete="email" value="<?php echo esc_attr( $state['values']['email'] ); ?>" data-js="order-lookup-email" />
    </label>
    <p class="beslock-order-lookup__error" data-js="order-lookup-error" <?php echo $state['error'] ? '' : 'hidden'; ?>><?php echo esc_html( $state['error'] ); ?></p>
    <button type="submit" class="beslock-order-lookup__submit">Consultar</button>
  </form>
  <?php
}

function beslock_render_order_lookup_result( WC_Order $order ) {
  $date_created = $order->get_date_created();
  $order_date   = $date_created ? wc_format_datetime( $date_created, 'j \d\e F \d\e Y' ) : __( 'No disponible', 'beslock-custom' );
  $tracking     = beslock_get_order_tracking_data( $order );
  $items        = $order->get_items();
  $events       = beslock_get_order_timeline_events( $order, $order_date, $tracking );
  $progress     = beslock_get_order_timeline_progress( $events );
  ?>
  <section class="beslock-order-lookup__result" aria-label="<?php esc_attr_e( 'Estado del pedido', 'beslock-custom' ); ?>">
    <div class="beslock-order-lookup__result-header">
      <p class="beslock-order-lookup__status-pill"><?php echo esc_html( wc_get_order_status_name( $order->get_status() ) ); ?></p>
      <h2>Estado de tu compra</h2>
    </div>

    <ol class="beslock-order-lookup__timeline" style="--timeline-progress: <?php echo esc_attr( number_format( $progress, 3, '.', '' ) ); ?>;">
      <?php foreach ( $events as $event ) : ?>
        <li class="beslock-order-lookup__timeline-item beslock-order-lookup__timeline-item--<?php echo esc_attr( sanitize_html_class( $event['state'] ) ); ?>">
          <span class="beslock-order-lookup__timeline-node" aria-hidden="true"></span>
          <span class="beslock-order-lookup__timeline-title"><?php echo esc_html( $event['title'] ); ?></span>
          <span class="beslock-order-lookup__timeline-detail"><?php echo esc_html( $event['detail'] ); ?></span>
        </li>
      <?php endforeach; ?>
    </ol>

    <div class="beslock-order-lookup__products">
      <h3>Producto comprado</h3>
      <ul>
        <?php foreach ( $items as $item ) : ?>
          <li>
            <span><?php echo esc_html( $item->get_name() ); ?></span>
            <strong>x<?php echo esc_html( (string) $item->get_quantity() ); ?></strong>
          </li>
        <?php endforeach; ?>
      </ul>
    </div>
  </section>
  <?php
}

function beslock_render_order_lookup_page() {
  $state = beslock_get_order_lookup_state();

  get_header();
  ?>
  <main id="main-content" class="beslock-order-lookup" aria-labelledby="beslock-order-lookup-title">
    <div class="beslock-order-lookup__shell">
      <div class="beslock-order-lookup__layout">
        <section class="beslock-order-lookup__panel" aria-label="<?php esc_attr_e( 'Formulario de consulta', 'beslock-custom' ); ?>">
          <h1 id="beslock-order-lookup-title">Consulta tu pedido</h1>
          <?php beslock_render_order_lookup_form( $state ); ?>
        </section>

        <?php if ( $state['submitted'] && $state['order'] instanceof WC_Order ) : ?>
          <?php beslock_render_order_lookup_result( $state['order'] ); ?>
        <?php elseif ( $state['submitted'] ) : ?>
          <section class="beslock-order-lookup__result beslock-order-lookup__result--empty" aria-live="polite">
            <p class="beslock-order-lookup__status-pill beslock-order-lookup__status-pill--neutral">Sin coincidencia</p>
            <h2>No encontramos un pedido con esos datos.</h2>
            <p>Verifica que el número de pedido y el correo sean exactamente los usados en la compra.</p>
          </section>
        <?php else : ?>
          <section class="beslock-order-lookup__result beslock-order-lookup__result--empty">
            <p class="beslock-order-lookup__status-pill beslock-order-lookup__status-pill--neutral">Consulta segura</p>
            <h2>Solo mostramos la información necesaria.</h2>
            <p>No se exponen dirección completa, teléfono, documento ni información sensible de pago.</p>
          </section>
        <?php endif; ?>
      </div>
    </div>
  </main>
  <?php
  get_footer();
}
