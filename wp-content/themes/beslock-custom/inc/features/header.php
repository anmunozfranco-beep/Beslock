<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * LEGACY COMPAT SHIM.
 *
 * CANONICAL OWNER IN FUNCTIONS.PHP.
 *
 * This file intentionally remains load-safe for existing includes while the
 * header helper contract is owned only by functions.php.
 */
if ( function_exists( 'beslock_header_helper_audit_log' ) ) {
  beslock_header_helper_audit_log(
    'HEADER_HELPER_AUDIT',
    'inc/features/header.php loaded as legacy compat shim',
    array(
      'file' => __FILE__,
      'canonical_owner_loaded' => function_exists( 'beslock_get_header_widget_html' )
        && function_exists( 'beslock_header_widget_shortcode' )
        && function_exists( 'beslock_render_header_widget' ),
    )
  );
} else {
  error_log(
    sprintf(
      '[HEADER_HELPER_AUDIT] inc/features/header.php loaded before canonical owner %s',
      wp_json_encode( array( 'file' => __FILE__ ) )
    )
  );
}
