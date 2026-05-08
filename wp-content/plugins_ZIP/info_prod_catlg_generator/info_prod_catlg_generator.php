<?php
/**
 * Plugin Name: Info Product Catalog Generator
 * Plugin URI: https://beslock.local
 * Description: Generates a normalized WooCommerce product catalog JSON using canonical product-card rendering for short description extraction.
 * Version: 1.0.0
 * Author: Beslock
 * License: GPL-2.0-or-later
 * Text Domain: info-prod-catlg-generator
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( 'IPCG_VERSION' ) ) {
	define( 'IPCG_VERSION', '1.0.0' );
}

if ( ! defined( 'IPCG_PLUGIN_FILE' ) ) {
	define( 'IPCG_PLUGIN_FILE', __FILE__ );
}

if ( ! defined( 'IPCG_PLUGIN_DIR' ) ) {
	define( 'IPCG_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
}

require_once IPCG_PLUGIN_DIR . 'includes/class-ipcg-utils.php';
require_once IPCG_PLUGIN_DIR . 'includes/class-ipcg-parser.php';
require_once IPCG_PLUGIN_DIR . 'includes/class-ipcg-generator.php';
require_once IPCG_PLUGIN_DIR . 'includes/class-ipcg-admin.php';

register_activation_hook( IPCG_PLUGIN_FILE, 'ipcg_activate_plugin' );

/**
 * Basic activation check to ensure WooCommerce context exists before use.
 */
function ipcg_activate_plugin() {
	if ( ! class_exists( 'WooCommerce' ) ) {
		deactivate_plugins( plugin_basename( IPCG_PLUGIN_FILE ) );
		wp_die( esc_html__( 'Info Product Catalog Generator requires WooCommerce to be active.', 'info-prod-catlg-generator' ) );
	}
}

add_action( 'plugins_loaded', 'ipcg_bootstrap_plugin' );

/**
 * Bootstraps plugin services.
 */
function ipcg_bootstrap_plugin() {
	if ( is_admin() ) {
		new IPCG_Admin();
	}
}
