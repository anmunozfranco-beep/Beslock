<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

function beslock_get_legal_page_slug_from_request() {
  $request_path = isset( $_SERVER['REQUEST_URI'] ) ? wp_parse_url( sanitize_text_field( wp_unslash( $_SERVER['REQUEST_URI'] ) ), PHP_URL_PATH ) : '';
  $home_path    = wp_parse_url( home_url( '/' ), PHP_URL_PATH );

  $request_path = '/' . trim( (string) $request_path, '/' ) . '/';
  $home_path    = '/' . trim( (string) $home_path, '/' ) . '/';

  if ( '/' !== $home_path && 0 === strpos( $request_path, $home_path ) ) {
    $request_path = '/' . ltrim( substr( $request_path, strlen( $home_path ) ), '/' );
  }

  $slug = trim( $request_path, '/' );

  if ( in_array( $slug, array( 'terminos-y-condiciones', 'politica-de-privacidad' ), true ) ) {
    return $slug;
  }

  return '';
}

function beslock_is_legal_page_request() {
  return '' !== beslock_get_legal_page_slug_from_request();
}

add_action(
  'wp_enqueue_scripts',
  function() {
    if ( ! beslock_is_legal_page_request() ) {
      return;
    }

    $css_path = get_stylesheet_directory() . '/assets/css/legal-pages.css';

    if ( file_exists( $css_path ) ) {
      wp_enqueue_style(
        'beslock-legal-pages',
        get_stylesheet_directory_uri() . '/assets/css/legal-pages.css',
        array( 'beslock-main-style', 'beslock-extra-style' ),
        filemtime( $css_path )
      );
    }
  },
  30
);

add_action(
  'template_redirect',
  function() {
    $slug = beslock_get_legal_page_slug_from_request();

    if ( '' === $slug ) {
      return;
    }

    status_header( 200 );
    nocache_headers();

    get_header();

    $template = get_stylesheet_directory() . '/template-parts/legal/' . $slug . '.php';
    if ( file_exists( $template ) ) {
      include $template;
    }

    get_footer();
    exit;
  }
);
