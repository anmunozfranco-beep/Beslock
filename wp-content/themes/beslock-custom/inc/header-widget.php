<?php
/**
 * LEGACY COMPAT SHIM.
 *
 * CANONICAL OWNER IN FUNCTIONS.PHP.
 *
 * This file intentionally preserves include compatibility without redefining
 * the public header helper contract. The active implementations live in
 * functions.php.
 */

if ( function_exists( 'beslock_header_helper_audit_log' ) ) {
  beslock_header_helper_audit_log(
    'HEADER_HELPER_AUDIT',
    'inc/header-widget.php loaded as legacy compat shim',
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
      '[HEADER_HELPER_AUDIT] inc/header-widget.php loaded before canonical owner %s',
      wp_json_encode( array( 'file' => __FILE__ ) )
    )
  );
}
