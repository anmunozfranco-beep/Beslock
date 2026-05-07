<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

/**
 * Legacy bridge file.
 *
 * Product-card assets now load from the centralized frontend pipeline in
 * `inc/core/enqueue.php`. This file remains as a compatibility include so the
 * theme bootstrap does not change shape during the migration.
 */
add_action( 'wp_enqueue_scripts', function() {
  return;
}, 20 );
