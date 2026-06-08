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

add_action( 'template_redirect', function() {
  if ( ! function_exists( 'is_cart' ) || ! is_cart() ) {
    return;
  }

  if ( empty( $_GET['remove_item'] ) || ! function_exists( 'WC' ) || ! WC()->cart || ! WC()->cart->is_empty() ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
    return;
  }

  wp_safe_redirect( wc_get_cart_url() );
  exit;
}, 20 );

function beslock_normalize_location_label( $value ) {
  $value = trim( wp_strip_all_tags( (string) $value ) );
  $value = function_exists( 'remove_accents' ) ? remove_accents( $value ) : $value;
  $value = strtolower( $value );

  return preg_replace( '/\s+/', ' ', $value );
}

function beslock_get_colombia_state_code_for_label( $department ) {
  $normalized_department = beslock_normalize_location_label( $department );

  if ( '' === $normalized_department ) {
    return '';
  }

  $aliases = array(
    'amazonas'                  => 'CO-AMA',
    'antioquia'                 => 'CO-ANT',
    'arauca'                    => 'CO-ARA',
    'atlantico'                 => 'CO-ATL',
    'bogota'                    => 'CO-DC',
    'bogota d.c.'               => 'CO-DC',
    'bogota dc'                 => 'CO-DC',
    'bolivar'                   => 'CO-BOL',
    'boyaca'                    => 'CO-BOY',
    'caldas'                    => 'CO-CAL',
    'caqueta'                   => 'CO-CAQ',
    'casanare'                  => 'CO-CAS',
    'cauca'                     => 'CO-CAU',
    'cesar'                     => 'CO-CES',
    'choco'                     => 'CO-CHO',
    'cordoba'                   => 'CO-COR',
    'cundinamarca'              => 'CO-CUN',
    'guainia'                   => 'CO-GUA',
    'guaviare'                  => 'CO-GUV',
    'huila'                     => 'CO-HUI',
    'la guajira'                => 'CO-LAG',
    'magdalena'                 => 'CO-MAG',
    'meta'                      => 'CO-MET',
    'narino'                    => 'CO-NAR',
    'norte de santander'        => 'CO-NSA',
    'putumayo'                  => 'CO-PUT',
    'quindio'                   => 'CO-QUI',
    'risaralda'                 => 'CO-RIS',
    'san andres y providencia'  => 'CO-SAP',
    'san andres, providencia y santa catalina' => 'CO-SAP',
    'santander'                 => 'CO-SAN',
    'sucre'                     => 'CO-SUC',
    'tolima'                    => 'CO-TOL',
    'valle del cauca'           => 'CO-VAC',
    'vaupes'                    => 'CO-VAU',
    'vichada'                   => 'CO-VID',
  );

  if ( isset( $aliases[ $normalized_department ] ) ) {
    return $aliases[ $normalized_department ];
  }

  if ( function_exists( 'WC' ) && WC()->countries ) {
    $states = WC()->countries->get_states( 'CO' );

    if ( is_array( $states ) ) {
      foreach ( $states as $state_code => $state_label ) {
        if ( beslock_normalize_location_label( $state_label ) === $normalized_department ) {
          return $state_code;
        }
      }
    }
  }

  return '';
}

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

function beslock_get_shipping_city_fallback_options() {
  return array(
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
  );
}

function beslock_get_shipping_city_options() {
  static $city_options = null;

  if ( null !== $city_options ) {
    return apply_filters( 'beslock_shipping_city_options', $city_options );
  }

  $city_options  = array();
  $csv_path      = trailingslashit( get_stylesheet_directory() ) . 'worldcities.csv';
  $csv_is_ready  = is_readable( $csv_path );
  $cache_key     = $csv_is_ready ? 'beslock_shipping_city_options_' . filemtime( $csv_path ) : '';

  if ( '' !== $cache_key && function_exists( 'get_transient' ) ) {
    $cached_city_options = get_transient( $cache_key );

    if ( is_array( $cached_city_options ) && ! empty( $cached_city_options ) ) {
      $city_options = $cached_city_options;

      return apply_filters( 'beslock_shipping_city_options', $city_options );
    }
  }

  if ( $csv_is_ready ) {
    $handle = fopen( $csv_path, 'r' ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fopen

    if ( false !== $handle ) {
      $header  = fgetcsv( $handle );
      $columns = is_array( $header ) ? array_flip( $header ) : array();

      $city_index       = isset( $columns['city'] ) ? $columns['city'] : null;
      $city_fallback    = isset( $columns['Ciudad'] ) ? $columns['Ciudad'] : null;
      $iso2_index       = isset( $columns['iso2'] ) ? $columns['iso2'] : null;
      $department_index = isset( $columns['Departamento'] ) ? $columns['Departamento'] : null;

      while ( false !== ( $row = fgetcsv( $handle ) ) ) { // phpcs:ignore WordPress.CodeAnalysis.AssignmentInCondition.FoundInWhileCondition
        if ( null === $city_index || null === $iso2_index || null === $department_index || empty( $row[ $iso2_index ] ) || 'CO' !== $row[ $iso2_index ] ) {
          continue;
        }

        $state_code = beslock_get_colombia_state_code_for_label( isset( $row[ $department_index ] ) ? $row[ $department_index ] : '' );
        $city_label = isset( $row[ $city_index ] ) ? trim( (string) $row[ $city_index ] ) : '';

        if ( '' === $city_label && null !== $city_fallback && isset( $row[ $city_fallback ] ) ) {
          $city_label = trim( (string) $row[ $city_fallback ] );
        }

        if ( '' === $state_code || '' === $city_label ) {
          continue;
        }

        if ( ! isset( $city_options[ $state_code ] ) ) {
          $city_options[ $state_code ] = array();
        }

        $normalized_city = beslock_normalize_location_label( $city_label );

        if ( ! isset( $city_options[ $state_code ][ $normalized_city ] ) ) {
          $city_options[ $state_code ][ $normalized_city ] = $city_label;
        }
      }

      fclose( $handle ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fclose
    }
  }

  if ( empty( $city_options ) ) {
    $city_options = beslock_get_shipping_city_fallback_options();
  } else {
    foreach ( $city_options as $state_code => $cities ) {
      natcasesort( $cities );
      $city_options[ $state_code ] = array_values( $cities );
    }
  }

  if ( '' !== $cache_key && function_exists( 'set_transient' ) && ! empty( $city_options ) ) {
    set_transient( $cache_key, $city_options, WEEK_IN_SECONDS );
  }

  return apply_filters( 'beslock_shipping_city_options', $city_options );
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

function beslock_shipping_city_has_locality_options( $city ) {
  $city         = trim( (string) $city );
  $area_options = beslock_get_shipping_area_options();

  return '' !== $city && ! empty( $area_options[ $city ] ) && is_array( $area_options[ $city ] );
}

function beslock_shipping_city_has_neighborhood_options( $city ) {
  $city         = trim( (string) $city );
  $area_options = beslock_get_shipping_neighborhood_area_options();

  if ( '' === $city || empty( $area_options[ $city ] ) || ! is_array( $area_options[ $city ] ) ) {
    return false;
  }

  foreach ( $area_options[ $city ] as $neighborhoods ) {
    if ( ! empty( $neighborhoods ) && is_array( $neighborhoods ) ) {
      return true;
    }
  }

  return false;
}

function beslock_shipping_city_uses_locality( $city ) {
  $normalized_city = beslock_normalize_location_label( $city );

  return in_array( $normalized_city, array( 'bogota', 'bogota d.c.', 'bogota dc' ), true );
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

function beslock_cart_has_confirmed_shipping_address() {
  if ( ! function_exists( 'WC' ) || ! WC()->customer ) {
    return false;
  }

  if ( WC()->session ) {
    if ( 'yes' === WC()->session->get( 'beslock_shipping_address_confirmed' ) ) {
      return true;
    }

    $session_address = WC()->session->get( 'beslock_shipping_address_1' );
    if ( is_string( $session_address ) && '' !== trim( $session_address ) ) {
      return true;
    }
  }

  return '' !== trim( (string) WC()->customer->get_shipping_address_1() );
}

function beslock_cart_requires_shipping_address_confirmation() {
  if ( ! function_exists( 'WC' ) || ! WC()->cart || WC()->cart->is_empty() ) {
    return false;
  }

  if ( method_exists( WC()->cart, 'needs_shipping' ) && ! WC()->cart->needs_shipping() ) {
    return false;
  }

  return ! beslock_cart_has_confirmed_shipping_address();
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

  if ( function_exists( 'beslock_cart_has_confirmed_shipping_address' ) && ! beslock_cart_has_confirmed_shipping_address() ) {
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

function beslock_get_cart_installation_policy() {
  static $policy = null;

  if ( null !== $policy ) {
    return $policy;
  }

  $policy = array(
    'available_cities' => array( 'Bogotá', 'Medellín', 'Cali', 'Barranquilla' ),
    'consult_target' => 'support-drawer:schedule-installation',
    'unavailable_city_message' => __( 'Consulta la disponibilidad del servicio para tu ubicación en Programar instalación', 'beslock-custom' ),
  );

  $source_file = trailingslashit( get_stylesheet_directory() ) . 'data/product-pricing-source.json';
  if ( is_readable( $source_file ) ) {
    $source = json_decode( file_get_contents( $source_file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

    if ( is_array( $source ) && ! empty( $source['installation_policy'] ) && is_array( $source['installation_policy'] ) ) {
      $source_policy = $source['installation_policy'];

      if ( ! empty( $source_policy['available_cities'] ) && is_array( $source_policy['available_cities'] ) ) {
        $cities = array();

        foreach ( $source_policy['available_cities'] as $city ) {
          if ( is_array( $city ) && ! empty( $city['label'] ) ) {
            $cities[] = sanitize_text_field( $city['label'] );
          } elseif ( is_string( $city ) && '' !== $city ) {
            $cities[] = sanitize_text_field( $city );
          }
        }

        if ( ! empty( $cities ) ) {
          $policy['available_cities'] = array_values( array_unique( $cities ) );
        }
      }

      if ( ! empty( $source_policy['consult_target'] ) && is_string( $source_policy['consult_target'] ) ) {
        $policy['consult_target'] = sanitize_text_field( $source_policy['consult_target'] );
      }

      if ( ! empty( $source_policy['unavailable_city_message'] ) && is_string( $source_policy['unavailable_city_message'] ) ) {
        $policy['unavailable_city_message'] = sanitize_textarea_field( $source_policy['unavailable_city_message'] );
      }
    }
  }

  return apply_filters( 'beslock_cart_installation_policy', $policy );
}

function beslock_normalize_installation_city_key( $city ) {
  $city = function_exists( 'beslock_normalize_location_label' ) ? beslock_normalize_location_label( $city ) : strtolower( trim( (string) $city ) );

  if ( in_array( $city, array( 'bogota d.c.', 'bogota dc' ), true ) ) {
    return 'bogota';
  }

  return $city;
}

function beslock_is_cart_installation_city_available( $city ) {
  $city_key = beslock_normalize_installation_city_key( $city );

  if ( '' === $city_key ) {
    return false;
  }

  $policy = beslock_get_cart_installation_policy();
  foreach ( (array) $policy['available_cities'] as $available_city ) {
    if ( $city_key === beslock_normalize_installation_city_key( $available_city ) ) {
      return true;
    }
  }

  return false;
}

function beslock_get_cart_installation_city() {
  if ( ! function_exists( 'WC' ) || ! WC()->customer ) {
    return '';
  }

  if ( function_exists( 'beslock_cart_has_confirmed_shipping_address' ) && ! beslock_cart_has_confirmed_shipping_address() ) {
    return '';
  }

  $city = WC()->customer->get_shipping_city();

  if ( '' === trim( (string) $city ) ) {
    $city = WC()->customer->get_billing_city();
  }

  return trim( (string) $city );
}

function beslock_get_portfolio_product_data_by_slug( $slug ) {
  static $products = null;

  $slug = sanitize_title( $slug );
  if ( '' === $slug ) {
    return array();
  }

  if ( null === $products ) {
    $products  = array();
    $data_file = trailingslashit( get_stylesheet_directory() ) . 'data/products.json';

    if ( is_readable( $data_file ) ) {
      $data = json_decode( file_get_contents( $data_file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

      if ( is_array( $data ) ) {
        foreach ( $data as $product_data ) {
          if ( ! empty( $product_data['slug'] ) ) {
            $products[ sanitize_title( $product_data['slug'] ) ] = $product_data;
          }
        }
      }
    }
  }

  return isset( $products[ $slug ] ) && is_array( $products[ $slug ] ) ? $products[ $slug ] : array();
}

function beslock_get_cart_item_installation_data( $cart_item ) {
  if ( empty( $cart_item['data'] ) || ! $cart_item['data'] instanceof WC_Product ) {
    return array();
  }

  $product    = $cart_item['data'];
  $product_id = ! empty( $cart_item['product_id'] ) ? absint( $cart_item['product_id'] ) : $product->get_id();
  $sku        = (string) $product->get_sku();

  if ( 0 === strpos( $sku, 'BESLOCK-INST-' ) ) {
    return array();
  }

  $price = get_post_meta( $product_id, '_beslock_installation_price', true );
  $type  = get_post_meta( $product_id, '_beslock_installation_type', true );
  $inst_sku = get_post_meta( $product_id, '_beslock_installation_sku', true );

  if ( '' === (string) $price || '' === (string) $type ) {
    $source = beslock_get_portfolio_product_data_by_slug( $product->get_slug() );

    if ( '' === (string) $price && isset( $source['installation_price'] ) ) {
      $price = $source['installation_price'];
    }

    if ( '' === (string) $type && isset( $source['installation_type'] ) ) {
      $type = $source['installation_type'];
    }

    if ( '' === (string) $inst_sku && isset( $source['installation_product_sku'] ) ) {
      $inst_sku = $source['installation_product_sku'];
    }
  }

  $price = (float) wc_format_decimal( $price );

  if ( $price <= 0 ) {
    return array();
  }

  $quantity = isset( $cart_item['quantity'] ) ? max( 1, (int) $cart_item['quantity'] ) : 1;

  return array(
    'product_id' => $product_id,
    'name'       => $product->get_name(),
    'slug'       => $product->get_slug(),
    'sku'        => $inst_sku,
    'type'       => $type,
    'price'      => $price,
    'quantity'   => $quantity,
    'total'      => $price * $quantity,
  );
}

function beslock_get_cart_installation_quote() {
  $quote = array(
    'has_installable_items' => false,
    'items'                 => array(),
    'total'                 => 0.0,
    'city'                  => beslock_get_cart_installation_city(),
    'is_city_available'     => false,
    'available_cities'      => beslock_get_cart_installation_policy()['available_cities'],
  );

  if ( ! function_exists( 'WC' ) || ! WC()->cart ) {
    return $quote;
  }

  foreach ( WC()->cart->get_cart() as $cart_item ) {
    $item = beslock_get_cart_item_installation_data( $cart_item );

    if ( empty( $item ) ) {
      continue;
    }

    $quote['has_installable_items'] = true;
    $quote['items'][]              = $item;
    $quote['total']               += $item['total'];
  }

  $quote['is_city_available'] = beslock_is_cart_installation_city_available( $quote['city'] );

  return $quote;
}

function beslock_cart_installation_is_selected() {
  return function_exists( 'WC' ) && WC()->session && 'yes' === WC()->session->get( 'beslock_cart_include_installation' );
}

function beslock_set_cart_installation_selected( $selected ) {
  if ( function_exists( 'WC' ) && WC()->session ) {
    WC()->session->set( 'beslock_cart_include_installation', $selected ? 'yes' : 'no' );
  }
}

add_action( 'wp_loaded', function() {
  if ( empty( $_POST['beslock_cart_installation_action'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Missing
    return;
  }

  if ( ! isset( $_POST['beslock_cart_installation_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['beslock_cart_installation_nonce'] ) ), 'beslock-cart-installation' ) ) {
    return;
  }

  $quote    = beslock_get_cart_installation_quote();
  $selected = ! empty( $_POST['beslock_include_installation'] ); // phpcs:ignore WordPress.Security.NonceVerification.Missing

  if ( $selected && ( empty( $quote['has_installable_items'] ) || empty( $quote['is_city_available'] ) || $quote['total'] <= 0 || ! beslock_cart_has_confirmed_shipping_address() ) ) {
    beslock_set_cart_installation_selected( false );
  } else {
    beslock_set_cart_installation_selected( $selected );
  }

  if ( function_exists( 'WC' ) && WC()->cart ) {
    WC()->cart->calculate_totals();
  }

  wp_safe_redirect( wc_get_cart_url() );
  exit;
}, 20 );

add_action( 'woocommerce_cart_calculate_fees', function( $cart ) {
  if ( is_admin() && ! wp_doing_ajax() ) {
    return;
  }

  if ( ! beslock_cart_installation_is_selected() ) {
    return;
  }

  $quote = beslock_get_cart_installation_quote();

  if ( empty( $quote['has_installable_items'] ) || empty( $quote['is_city_available'] ) || $quote['total'] <= 0 || ! beslock_cart_has_confirmed_shipping_address() ) {
    beslock_set_cart_installation_selected( false );
    return;
  }

  $cart->add_fee( __( 'Instalación BESLOCK', 'beslock-custom' ), $quote['total'], false );
}, 30 );

function beslock_render_cart_installation_option() {
  $quote = beslock_get_cart_installation_quote();

  if ( empty( $quote['has_installable_items'] ) || $quote['total'] <= 0 ) {
    return;
  }

  if ( ! beslock_cart_has_confirmed_shipping_address() ) {
    return;
  }

  $is_available = ! empty( $quote['is_city_available'] );
  $is_selected  = $is_available && beslock_cart_installation_is_selected();
  $message_html = '';

  if ( ! $is_available && beslock_cart_installation_is_selected() ) {
    beslock_set_cart_installation_selected( false );
    $is_selected = false;
  }

  if ( $is_available ) {
    $title        = __( 'Instalación disponible', 'beslock-custom' );
    $message_html = esc_html__( 'Instalación disponible para tu ubicación.', 'beslock-custom' );
  } else {
    $schedule_installation_link = sprintf(
      '<a class="beslock-cart-installation__message-link" href="%1$s" target="_self">%2$s</a>',
      esc_url(
        add_query_arg(
          array(
            'drawer'  => 'contact',
            'section' => 'schedule-installation',
          ),
          home_url( '/' )
        )
      ),
      esc_html__( 'Programar instalación', 'beslock-custom' )
    );
    $message_html       = sprintf(
      esc_html__( 'Consulta la disponibilidad del servicio para tu ubicación en %s', 'beslock-custom' ),
      $schedule_installation_link
    );
  }

  ?>
  <tr class="beslock-cart-installation <?php echo $is_available ? 'is-available' : 'is-unavailable'; ?>">
    <th>
      <span><?php esc_html_e( 'Instalación', 'beslock-custom' ); ?></span>
      <?php if ( ! $is_available ) : ?>
        <strong class="beslock-cart-installation__price beslock-cart-installation__price--heading"><?php echo wp_kses_post( wc_price( $quote['total'] ) ); ?></strong>
      <?php endif; ?>
    </th>
    <td data-title="<?php esc_attr_e( 'Instalación', 'beslock-custom' ); ?>">
      <form class="beslock-cart-installation__form" method="post" action="<?php echo esc_url( wc_get_cart_url() ); ?>">
        <input type="hidden" name="beslock_cart_installation_action" value="1">
        <?php wp_nonce_field( 'beslock-cart-installation', 'beslock_cart_installation_nonce' ); ?>
        <?php if ( $is_available ) : ?>
          <label class="beslock-cart-installation__choice">
            <input
              type="checkbox"
              name="beslock_include_installation"
              value="1"
              <?php checked( $is_selected ); ?>
            >
            <span class="beslock-cart-installation__copy">
              <span class="beslock-cart-installation__title">
                <?php echo esc_html( $title ); ?>
              </span>
              <span class="beslock-cart-installation__message">
                <?php echo esc_html( $message_html ); ?>
              </span>
            </span>
            <strong class="beslock-cart-installation__price"><?php echo wp_kses_post( wc_price( $quote['total'] ) ); ?></strong>
          </label>
        <?php else : ?>
          <div class="beslock-cart-installation__choice beslock-cart-installation__choice--readonly">
            <span class="beslock-cart-installation__copy">
              <span class="beslock-cart-installation__message beslock-cart-installation__message--headline">
                <?php
                echo wp_kses(
                  $message_html,
                  array(
                    'a' => array(
                      'class'  => true,
                      'href'   => true,
                      'target' => true,
                    ),
                  )
                );
                ?>
              </span>
            </span>
          </div>
        <?php endif; ?>
        <?php if ( $is_available ) : ?>
          <button type="submit" class="beslock-cart-installation__submit"><?php esc_html_e( 'Actualizar instalación', 'beslock-custom' ); ?></button>
        <?php endif; ?>
        <?php if ( count( (array) $quote['items'] ) > 1 ) : ?>
          <ul class="beslock-cart-installation__items">
            <?php foreach ( $quote['items'] as $item ) : ?>
              <li>
                <span><?php echo esc_html( $item['name'] ); ?></span>
                <span><?php echo wp_kses_post( wc_price( $item['total'] ) ); ?></span>
              </li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>
      </form>
    </td>
  </tr>
  <?php
}

add_filter( 'woocommerce_get_country_locale', function( $locale ) {
  if ( isset( $locale['CO']['city'] ) ) {
    $locale['CO']['city']['label'] = __( 'Ciudad / Municipio', 'beslock-custom' );
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

function beslock_get_free_shipping_rate_id() {
  return 'beslock_free_shipping';
}

add_filter( 'woocommerce_package_rates', function( $rates, $package ) {
  if ( is_admin() && ! wp_doing_ajax() ) {
    return $rates;
  }

  if ( ! class_exists( 'WC_Shipping_Rate' ) ) {
    return $rates;
  }

  $rate_id = beslock_get_free_shipping_rate_id();
  $rate    = new WC_Shipping_Rate(
    $rate_id,
    __( 'Envío gratis', 'beslock-custom' ),
    0,
    array(),
    'beslock_free_shipping'
  );

  return array(
    $rate_id => $rate,
  );
}, 100, 2 );

add_filter( 'woocommerce_shipping_chosen_method', function( $default, $rates, $chosen_method ) {
  $rate_id = beslock_get_free_shipping_rate_id();

  if ( isset( $rates[ $rate_id ] ) ) {
    return $rate_id;
  }

  return $default;
}, 100, 3 );

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
    throw new Exception( __( 'Selecciona la Ciudad/Municipio para calcular la entrega.', 'beslock-custom' ) );
  }

  $clean_locality     = function_exists( 'beslock_clean_shipping_destination_part' ) ? beslock_clean_shipping_destination_part( $locality ) : $locality;
  $clean_neighborhood = function_exists( 'beslock_clean_shipping_destination_part' ) ? beslock_clean_shipping_destination_part( $neighborhood ) : $neighborhood;
  $uses_locality      = function_exists( 'beslock_shipping_city_uses_locality' ) && beslock_shipping_city_uses_locality( $address['city'] );

  if ( ! $uses_locality ) {
    $locality       = '';
    $clean_locality = '';
  }

  if ( ! $uses_locality && '' === $clean_neighborhood ) {
    throw new Exception( __( 'Ingresa el barrio o sector para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( $uses_locality && '' === $clean_locality && '' === $clean_neighborhood ) {
    throw new Exception( __( 'Selecciona la localidad o ingresa el barrio para calcular la entrega.', 'beslock-custom' ) );
  }

  if ( $uses_locality && function_exists( 'beslock_shipping_neighborhood_matches_area' ) && ! beslock_shipping_neighborhood_matches_area( $address['city'], $locality, $neighborhood ) ) {
    throw new Exception( __( 'El barrio seleccionado no corresponde a la localidad elegida. Ajusta esa combinación para calcular la entrega.', 'beslock-custom' ) );
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
  $shipping_city = isset( $_POST['calc_shipping_city'] ) ? wc_clean( wp_unslash( $_POST['calc_shipping_city'] ) ) : WC()->customer->get_shipping_city(); // phpcs:ignore WordPress.Security.NonceVerification.Missing

  if ( function_exists( 'beslock_shipping_city_uses_locality' ) && ! beslock_shipping_city_uses_locality( $shipping_city ) ) {
    $locality = '';
  }

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
    WC()->session->set( 'beslock_shipping_address_confirmed', 'yes' );
    WC()->session->set( 'beslock_shipping_address_1', $address_1 );
    WC()->session->set( 'beslock_shipping_area', $area );
    WC()->session->set( 'beslock_shipping_locality', $locality );
    WC()->session->set( 'beslock_shipping_neighborhood', $neighborhood );
  }

  WC()->customer->save();
}, 20 );
