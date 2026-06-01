<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

// WooCommerce cart/shop related logic
if ( class_exists( 'WooCommerce' ) && WC() ) {
  // Redirect the WooCommerce Shop page to the front-page products portfolio section.
  add_action( 'template_redirect', function() {
    if ( function_exists( 'is_shop' ) && is_shop() ) {
      wp_safe_redirect( home_url( '/' ) . '#productos', 301 );
      exit;
    }
  }, 5 );

  // Ensure WooCommerce canonical URLs that expect a shop page don't break.
  add_filter( 'woocommerce_get_shop_page_id', function( $page_id ) {
    return 0;
  } );
}

function beslock_render_header_cart_count( $count = null ) {
  if ( null === $count ) {
    $count = ( class_exists( 'WooCommerce' ) && WC()->cart ) ? (int) WC()->cart->get_cart_contents_count() : 0;
  }

  $count = max( 0, (int) $count );
  $classes = array( 'header__cart-count' );

  if ( 0 === $count ) {
    $classes[] = 'is-empty';
  }

  return sprintf(
    '<span class="%1$s" aria-hidden="true">%2$s</span>',
    esc_attr( implode( ' ', $classes ) ),
    esc_html( (string) $count )
  );
}

add_filter( 'woocommerce_add_to_cart_fragments', function( $fragments ) {
  if ( function_exists( 'beslock_render_header_cart_count' ) ) {
    $fragments['.header__icon--cart .header__cart-count'] = beslock_render_header_cart_count();
  }

  return $fragments;
} );

add_filter( 'wc_add_to_cart_message_html', '__return_empty_string', 10 );

function beslock_get_shipping_area_options() {
  return apply_filters(
    'beslock_shipping_area_options',
    array(
      'Bogotá'   => array(
        'Usaquén',
        'Chapinero',
        'Santa Fe',
        'San Cristóbal',
        'Usme',
        'Tunjuelito',
        'Bosa',
        'Kennedy',
        'Fontibón',
        'Engativá',
        'Suba',
        'Barrios Unidos',
        'Teusaquillo',
        'Los Mártires',
        'Antonio Nariño',
        'Puente Aranda',
        'La Candelaria',
        'Rafael Uribe Uribe',
        'Ciudad Bolívar',
        'Sumapaz',
      ),
      'Medellín' => array(
        'Comuna 1 - Popular',
        'Comuna 2 - Santa Cruz',
        'Comuna 3 - Manrique',
        'Comuna 4 - Aranjuez',
        'Comuna 5 - Castilla',
        'Comuna 6 - Doce de Octubre',
        'Comuna 7 - Robledo',
        'Comuna 8 - Villa Hermosa',
        'Comuna 9 - Buenos Aires',
        'Comuna 10 - La Candelaria',
        'Comuna 11 - Laureles-Estadio',
        'Comuna 12 - La América',
        'Comuna 13 - San Javier',
        'Comuna 14 - El Poblado',
        'Comuna 15 - Guayabal',
        'Comuna 16 - Belén',
        'Corregimiento - San Sebastián de Palmitas',
        'Corregimiento - San Cristóbal',
        'Corregimiento - Altavista',
        'Corregimiento - San Antonio de Prado',
        'Corregimiento - Santa Elena',
      ),
    )
  );
}

function beslock_get_shipping_city_options() {
  return apply_filters(
    'beslock_shipping_city_options',
    array(
      'CO-DC'  => array( 'Bogotá' ),
      'CO-ANT' => array( 'Medellín', 'Bello', 'Envigado', 'Itagüí', 'Sabaneta', 'Rionegro' ),
      'CO-ATL' => array( 'Barranquilla', 'Soledad' ),
      'CO-BOL' => array( 'Cartagena' ),
      'CO-BOY' => array( 'Tunja', 'Duitama', 'Sogamoso' ),
      'CO-CAL' => array( 'Manizales' ),
      'CO-CAU' => array( 'Popayán' ),
      'CO-CES' => array( 'Valledupar' ),
      'CO-COR' => array( 'Montería' ),
      'CO-CUN' => array( 'Chía', 'Cajicá', 'Funza', 'Mosquera', 'Soacha', 'Zipaquirá' ),
      'CO-HUI' => array( 'Neiva' ),
      'CO-LAG' => array( 'Riohacha' ),
      'CO-MAG' => array( 'Santa Marta' ),
      'CO-MET' => array( 'Villavicencio' ),
      'CO-NAR' => array( 'Pasto' ),
      'CO-NSA' => array( 'Cúcuta' ),
      'CO-QUI' => array( 'Armenia' ),
      'CO-RIS' => array( 'Pereira', 'Dosquebradas' ),
      'CO-SAN' => array( 'Bucaramanga', 'Floridablanca', 'Girón', 'Piedecuesta' ),
      'CO-SUC' => array( 'Sincelejo' ),
      'CO-TOL' => array( 'Ibagué' ),
      'CO-VAC' => array( 'Cali', 'Buenaventura', 'Jamundí', 'Palmira', 'Tuluá', 'Yumbo' ),
    )
  );
}

function beslock_get_shipping_neighborhood_options() {
  $grouped_options = function_exists( 'beslock_get_shipping_neighborhood_area_options' ) ? beslock_get_shipping_neighborhood_area_options() : array();
  $city_options    = array();

  foreach ( $grouped_options as $city_label => $area_groups ) {
    $city_options[ $city_label ] = array();

    foreach ( $area_groups as $neighborhoods ) {
      foreach ( $neighborhoods as $neighborhood ) {
        if ( ! in_array( $neighborhood, $city_options[ $city_label ], true ) ) {
          $city_options[ $city_label ][] = $neighborhood;
        }
      }
    }
  }

  return apply_filters(
    'beslock_shipping_neighborhood_options',
    $city_options
  );
}

function beslock_get_shipping_neighborhood_area_options() {
  return apply_filters(
    'beslock_shipping_neighborhood_area_options',
    array(
      'Bogotá'   => array(
        'Chapinero'   => array(
          'Chicó',
          'Chapinero Central',
          'Rosales',
        ),
        'Usaquén'     => array(
          'Cedritos',
          'Santa Bárbara',
          'Usaquén',
        ),
        'Fontibón'    => array(
          'Modelia',
          'Ciudad Salitre',
        ),
        'Kennedy'     => array(
          'Kennedy Central',
        ),
        'Suba'        => array(
          'Colina Campestre',
        ),
        'Teusaquillo' => array(
          'Ciudad Salitre',
        ),
      ),
      'Medellín' => array(
        'Comuna 7 - Robledo'          => array(
          'Robledo',
        ),
        'Comuna 9 - Buenos Aires'     => array(
          'Buenos Aires',
        ),
        'Comuna 10 - La Candelaria'   => array(
          'La Candelaria',
        ),
        'Comuna 11 - Laureles-Estadio' => array(
          'Laureles',
          'Conquistadores',
        ),
        'Comuna 12 - La América'      => array(
          'Santa Mónica',
        ),
        'Comuna 14 - El Poblado'      => array(
          'El Poblado',
          'Manila',
          'Castropol',
        ),
        'Comuna 16 - Belén'           => array(
          'Belén',
        ),
      ),
      'Cali'     => array(
        '' => array(
          'Granada',
          'San Fernando',
          'Ciudad Jardín',
          'El Peñón',
          'Versalles',
          'Pance',
        ),
      ),
    )
  );
}

function beslock_shipping_neighborhood_matches_area( $city, $locality, $neighborhood ) {
  if ( '' === $locality || '' === $neighborhood ) {
    return true;
  }

  if ( in_array( $locality, array( 'No aplica' ), true ) || in_array( $neighborhood, array( 'No aparece en la lista' ), true ) ) {
    return true;
  }

  $area_options = beslock_get_shipping_neighborhood_area_options();

  if ( empty( $area_options[ $city ] ) || ! is_array( $area_options[ $city ] ) ) {
    return true;
  }

  $matching_areas = array();

  foreach ( $area_options[ $city ] as $area_label => $neighborhoods ) {
    if ( '' === $area_label || ! is_array( $neighborhoods ) ) {
      continue;
    }

    if ( in_array( $neighborhood, $neighborhoods, true ) ) {
      $matching_areas[] = $area_label;
    }
  }

  if ( empty( $matching_areas ) ) {
    return true;
  }

  return in_array( $locality, $matching_areas, true );
}

function beslock_get_shipping_session_value( $key, $fallback = '' ) {
  if ( function_exists( 'WC' ) && WC()->session ) {
    $value = WC()->session->get( $key );

    if ( is_string( $value ) && '' !== $value ) {
      return $value;
    }
  }

  return $fallback;
}

function beslock_get_shipping_placeholder_values() {
  return apply_filters(
    'beslock_shipping_placeholder_values',
    array(
      'No aplica',
      'No aplica en mi ciudad',
      'No aparece en la lista',
    )
  );
}

function beslock_is_shipping_placeholder_value( $value ) {
  $value = trim( wp_strip_all_tags( (string) $value ) );

  if ( '' === $value ) {
    return true;
  }

  $normalized_value = function_exists( 'remove_accents' ) ? remove_accents( $value ) : $value;
  $normalized_value = strtolower( $normalized_value );

  foreach ( beslock_get_shipping_placeholder_values() as $placeholder ) {
    $normalized_placeholder = function_exists( 'remove_accents' ) ? remove_accents( $placeholder ) : $placeholder;
    $normalized_placeholder = strtolower( trim( wp_strip_all_tags( (string) $normalized_placeholder ) ) );

    if ( $normalized_value === $normalized_placeholder ) {
      return true;
    }
  }

  return false;
}

function beslock_clean_shipping_destination_part( $value ) {
  $value = trim( wp_strip_all_tags( (string) $value ) );

  if ( beslock_is_shipping_placeholder_value( $value ) ) {
    return '';
  }

  return $value;
}

function beslock_get_clean_shipping_area_parts( $locality, $neighborhood ) {
  $parts = array(
    beslock_clean_shipping_destination_part( $locality ),
    beslock_clean_shipping_destination_part( $neighborhood ),
  );

  return array_values( array_filter( $parts ) );
}

function beslock_get_clean_shipping_area( $locality, $neighborhood ) {
  return implode( ' / ', beslock_get_clean_shipping_area_parts( $locality, $neighborhood ) );
}

function beslock_format_cart_shipping_destination( $destination = array() ) {
  if ( ! function_exists( 'WC' ) || ! WC()->customer ) {
    return '';
  }

  $destination = is_array( $destination ) ? $destination : array();
  $country     = ! empty( $destination['country'] ) ? $destination['country'] : WC()->customer->get_shipping_country();
  $state       = ! empty( $destination['state'] ) ? $destination['state'] : WC()->customer->get_shipping_state();
  $city        = ! empty( $destination['city'] ) ? $destination['city'] : WC()->customer->get_shipping_city();
  $address_1   = ! empty( $destination['address_1'] ) ? $destination['address_1'] : WC()->customer->get_shipping_address_1();

  $address_1    = beslock_get_shipping_session_value( 'beslock_shipping_address_1', $address_1 );
  $locality     = beslock_get_shipping_session_value( 'beslock_shipping_locality', WC()->customer->get_meta( 'beslock_shipping_locality' ) );
  $neighborhood = beslock_get_shipping_session_value( 'beslock_shipping_neighborhood', WC()->customer->get_meta( 'beslock_shipping_neighborhood' ) );
  $state_label  = $state;

  if ( $country && $state && function_exists( 'WC' ) && WC()->countries ) {
    $states = WC()->countries->get_states( $country );

    if ( is_array( $states ) && isset( $states[ $state ] ) ) {
      $state_label = $states[ $state ];
    }
  }

  $parts = array_merge(
    array( beslock_clean_shipping_destination_part( $address_1 ) ),
    beslock_get_clean_shipping_area_parts( $locality, $neighborhood ),
    array(
      beslock_clean_shipping_destination_part( $city ),
      beslock_clean_shipping_destination_part( $state_label ),
    )
  );

  $parts        = array_values( array_filter( $parts ) );
  $unique_parts = array();

  foreach ( $parts as $part ) {
    $key = strtolower( function_exists( 'remove_accents' ) ? remove_accents( $part ) : $part );

    if ( ! isset( $unique_parts[ $key ] ) ) {
      $unique_parts[ $key ] = $part;
    }
  }

  return implode( ', ', array_values( $unique_parts ) );
}

add_filter( 'woocommerce_get_country_locale', function( $locale ) {
  if ( isset( $locale['CO']['city'] ) ) {
    $locale['CO']['city']['label'] = __( 'Ciudad / municipio', 'beslock-custom' );
  }

  if ( isset( $locale['CO']['state'] ) ) {
    $locale['CO']['state']['label'] = __( 'Departamento', 'beslock-custom' );
  }

  return $locale;
} );

add_filter( 'woocommerce_cart_shipping_method_full_label', function( $label, $method ) {
  if ( isset( $method->method_id ) && 'free_shipping' === $method->method_id ) {
    return esc_html__( 'Envío gratis', 'beslock-custom' );
  }

  return str_replace(
    array( 'Free shipping', 'Free Shipping' ),
    esc_html__( 'Envío gratis', 'beslock-custom' ),
    $label
  );
}, 20, 2 );

add_filter( 'woocommerce_cart_calculate_shipping_address', function( $address ) {
  if ( empty( $_POST['calc_shipping'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Missing
    return $address;
  }

  $address_1    = isset( $_POST['calc_shipping_address_1'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_address_1'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
  $locality     = isset( $_POST['calc_shipping_locality'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_locality'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
  $neighborhood = isset( $_POST['calc_shipping_neighborhood'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_neighborhood'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing

  if ( '' === $address_1 ) {
    throw new Exception( __( 'Ingresa la dirección completa para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( empty( $address['state'] ) ) {
    throw new Exception( __( 'Selecciona el departamento para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( empty( $address['city'] ) ) {
    throw new Exception( __( 'Selecciona la ciudad o municipio para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( '' === $locality && '' === $neighborhood ) {
    throw new Exception( __( 'Selecciona una localidad/comuna o ingresa un barrio para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( function_exists( 'beslock_shipping_neighborhood_matches_area' ) && ! beslock_shipping_neighborhood_matches_area( $address['city'], $locality, $neighborhood ) ) {
    throw new Exception( __( 'El barrio seleccionado no corresponde a la localidad/comuna elegida. Ajusta esa combinación para calcular la entrega.', 'beslock-custom' ) );
  }

  $resolved_postcode = apply_filters(
    'beslock_resolve_shipping_postcode',
    '',
    array(
      'country'      => isset( $address['country'] ) ? $address['country'] : '',
      'state'        => isset( $address['state'] ) ? $address['state'] : '',
      'city'         => isset( $address['city'] ) ? $address['city'] : '',
      'locality'     => $locality,
      'neighborhood' => $neighborhood,
      'address_1'    => $address_1,
    )
  );

  if ( is_string( $resolved_postcode ) && '' !== $resolved_postcode ) {
    $address['postcode'] = wc_format_postcode( $resolved_postcode, $address['country'] );
  }

  return $address;
} );

add_action( 'woocommerce_calculated_shipping', function() {
  if ( ! function_exists( 'WC' ) || ! WC()->customer || empty( $_POST['calc_shipping'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Missing
    return;
  }

  $address_1    = isset( $_POST['calc_shipping_address_1'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_address_1'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
  $locality     = isset( $_POST['calc_shipping_locality'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_locality'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
  $neighborhood = isset( $_POST['calc_shipping_neighborhood'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_neighborhood'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
  $area         = function_exists( 'beslock_get_clean_shipping_area' ) ? beslock_get_clean_shipping_area( $locality, $neighborhood ) : trim( $locality . ( '' !== $locality && '' !== $neighborhood ? ' / ' : '' ) . $neighborhood );

  WC()->customer->set_shipping_address_1( $address_1 );
  WC()->customer->set_shipping_address_2( $area );
  WC()->customer->update_meta_data( 'beslock_shipping_area', $area );
  WC()->customer->update_meta_data( 'beslock_shipping_locality', $locality );
  WC()->customer->update_meta_data( 'beslock_shipping_neighborhood', $neighborhood );

  if ( ! WC()->customer->get_billing_first_name() ) {
    WC()->customer->set_billing_address_1( $address_1 );
    WC()->customer->set_billing_address_2( $area );
  }

  if ( WC()->session ) {
    WC()->session->set( 'beslock_shipping_address_1', $address_1 );
    WC()->session->set( 'beslock_shipping_area', $area );
    WC()->session->set( 'beslock_shipping_locality', $locality );
    WC()->session->set( 'beslock_shipping_neighborhood', $neighborhood );
  }

  WC()->customer->save();
}, 20 );
