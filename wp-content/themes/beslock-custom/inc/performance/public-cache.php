<?php
/**
 * Public cache controls for anonymous Beslock pages.
 *
 * This module is intentionally loadable from the active theme and from a
 * mu-plugin. The mu-plugin gets the earliest hooks when available; the theme
 * fallback keeps production deploys safe when only beslock-custom is uploaded.
 */

if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

if ( defined( 'BESLOCK_PUBLIC_CACHE_OPTIMIZER_LOADED' ) ) {
  return;
}

define( 'BESLOCK_PUBLIC_CACHE_OPTIMIZER_LOADED', true );

function beslock_public_cache_request_uri() {
  return isset( $_SERVER['REQUEST_URI'] ) ? (string) stripslashes( $_SERVER['REQUEST_URI'] ) : '/';
}

function beslock_public_cache_path() {
  $path = parse_url( beslock_public_cache_request_uri(), PHP_URL_PATH );
  $path = is_string( $path ) && $path !== '' ? $path : '/';

  return '/' . ltrim( strtolower( rawurldecode( $path ) ), '/' );
}

function beslock_public_cache_has_cookie_prefix( array $prefixes ) {
  if ( empty( $_COOKIE ) ) {
    return false;
  }

  foreach ( array_keys( $_COOKIE ) as $cookie_name ) {
    foreach ( $prefixes as $prefix ) {
      if ( strpos( (string) $cookie_name, $prefix ) === 0 ) {
        return true;
      }
    }
  }

  return false;
}

function beslock_public_cache_is_eligible_request() {
  $method = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( (string) $_SERVER['REQUEST_METHOD'] ) : 'GET';
  if ( ! in_array( $method, array( 'GET', 'HEAD' ), true ) ) {
    return false;
  }

  if ( ( function_exists( 'is_admin' ) && is_admin() ) || ( defined( 'DOING_AJAX' ) && DOING_AJAX ) || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
    return false;
  }

  $uri  = beslock_public_cache_request_uri();
  $path = beslock_public_cache_path();

  if ( parse_url( $uri, PHP_URL_QUERY ) ) {
    return false;
  }

  $blocked_paths = array(
    '/cart',
    '/carrito',
    '/checkout',
    '/finalizar-compra',
    '/mi-cuenta',
    '/my-account',
    '/pago',
    '/wc-api',
    '/wp-admin',
    '/wp-cron.php',
    '/wp-json',
    '/wp-login.php',
    '/wp-comments-post.php',
    '/xmlrpc.php',
  );

  foreach ( $blocked_paths as $blocked_path ) {
    if ( strpos( $path, $blocked_path ) === 0 ) {
      return false;
    }
  }

  $blocked_fragments = array(
    '/feed/',
    '/sitemap',
    'add-to-cart',
    'preview=true',
    'wc-ajax',
  );

  foreach ( $blocked_fragments as $fragment ) {
    if ( strpos( $uri, $fragment ) !== false ) {
      return false;
    }
  }

  if ( beslock_public_cache_has_cookie_prefix(
    array(
      'comment_author_',
      'woocommerce_cart_hash',
      'woocommerce_items_in_cart',
      'wordpress_logged_in_',
      'wp-postpass_',
      'wp_woocommerce_session_',
    )
  ) ) {
    return false;
  }

  if ( function_exists( 'is_user_logged_in' ) && is_user_logged_in() ) {
    return false;
  }

  return true;
}

function beslock_public_cache_prepare_php_session() {
  if ( ! beslock_public_cache_is_eligible_request() || headers_sent() ) {
    return;
  }

  if ( function_exists( 'session_status' ) && PHP_SESSION_NONE !== session_status() ) {
    return;
  }

  if ( function_exists( 'session_cache_limiter' ) ) {
    session_cache_limiter( '' );
  }

  @ini_set( 'session.use_cookies', '0' );
  @ini_set( 'session.use_only_cookies', '0' );
  @ini_set( 'session.use_trans_sid', '0' );
}
beslock_public_cache_prepare_php_session();

function beslock_public_cache_disable_session_plugins( $plugins ) {
  if ( ! beslock_public_cache_is_eligible_request() || ! is_array( $plugins ) ) {
    return $plugins;
  }

  return array_values( array_diff( $plugins, array( 'captcha-code-authentication/wpCaptcha.php' ) ) );
}
add_filter( 'option_active_plugins', 'beslock_public_cache_disable_session_plugins', 1 );

function beslock_public_cache_disable_network_session_plugins( $plugins ) {
  if ( ! beslock_public_cache_is_eligible_request() || ! is_array( $plugins ) ) {
    return $plugins;
  }

  unset( $plugins['captcha-code-authentication/wpCaptcha.php'] );

  return $plugins;
}
add_filter( 'site_option_active_sitewide_plugins', 'beslock_public_cache_disable_network_session_plugins', 1 );

function beslock_public_cache_allow_woocommerce_static_view_cookie_policy( $enabled, $name = '' ) {
  if ( ! beslock_public_cache_is_eligible_request() ) {
    return $enabled;
  }

  $blocked_names = array(
    'tk_ai',
    'woocommerce_geo_hash',
    'woocommerce_recently_viewed',
  );

  if ( in_array( (string) $name, $blocked_names, true ) || strpos( (string) $name, 'wp_woocommerce_session_' ) === 0 ) {
    return false;
  }

  return $enabled;
}
add_filter( 'woocommerce_set_cookie_enabled', 'beslock_public_cache_allow_woocommerce_static_view_cookie_policy', 10, 2 );

function beslock_public_cache_headers( $headers ) {
  if ( ! beslock_public_cache_is_eligible_request() ) {
    return $headers;
  }

  unset( $headers['Cache-Control'], $headers['Pragma'], $headers['Expires'] );

  $headers['Cache-Control']                = 'public, max-age=300, s-maxage=14400, stale-while-revalidate=86400';
  $headers['CDN-Cache-Control']            = 'public, max-age=14400, stale-while-revalidate=86400';
  $headers['Cloudflare-CDN-Cache-Control'] = 'public, max-age=14400, stale-while-revalidate=86400';
  $headers['X-Beslock-Cache-Eligible']     = 'public-html';

  return $headers;
}
add_filter( 'wp_headers', 'beslock_public_cache_headers', PHP_INT_MAX );

function beslock_public_cache_disable_nocache_headers( $headers ) {
  if ( beslock_public_cache_is_eligible_request() ) {
    return array();
  }

  return $headers;
}
add_filter( 'nocache_headers', 'beslock_public_cache_disable_nocache_headers', PHP_INT_MAX );

function beslock_public_cache_remove_public_set_cookie_headers() {
  if ( ! beslock_public_cache_is_eligible_request() || headers_sent() ) {
    return;
  }

  $headers_to_keep = array();

  foreach ( headers_list() as $header ) {
    if ( stripos( $header, 'Set-Cookie:' ) !== 0 ) {
      continue;
    }

    if ( preg_match( '/^Set-Cookie:\s*(PHPSESSID|tk_ai|woocommerce_geo_hash|woocommerce_recently_viewed|wp_woocommerce_session_[^=]*)=/i', $header ) ) {
      continue;
    }

    $headers_to_keep[] = $header;
  }

  header_remove( 'Set-Cookie' );

  foreach ( $headers_to_keep as $header ) {
    header( $header, false );
  }

  if ( function_exists( 'session_status' ) && PHP_SESSION_ACTIVE === session_status() ) {
    session_write_close();
  }
}

function beslock_public_cache_send_headers() {
  if ( ! beslock_public_cache_is_eligible_request() || headers_sent() ) {
    return;
  }

  beslock_public_cache_remove_public_set_cookie_headers();

  header_remove( 'Pragma' );
  header_remove( 'Expires' );
  header_remove( 'Cache-Control' );

  header( 'Cache-Control: public, max-age=300, s-maxage=14400, stale-while-revalidate=86400', true );
  header( 'CDN-Cache-Control: public, max-age=14400, stale-while-revalidate=86400', true );
  header( 'Cloudflare-CDN-Cache-Control: public, max-age=14400, stale-while-revalidate=86400', true );
  header( 'X-Beslock-Cache-Eligible: public-html', true );
}
add_action( 'send_headers', 'beslock_public_cache_send_headers', PHP_INT_MAX );
add_action( 'template_redirect', 'beslock_public_cache_send_headers', PHP_INT_MAX );
