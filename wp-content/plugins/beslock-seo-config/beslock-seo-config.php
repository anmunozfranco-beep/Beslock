<?php
/*
Plugin Name: BESLOCK SEO Config
Description: Sincroniza SEO backstage para BESLOCK desde el catalogo y manuales, con reglas tecnicas reproducibles para WordPress y WooCommerce.
Version: 0.2.0
Author: BESLOCK
*/

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BESLOCK_SEO_CONFIG_VERSION', '0.2.0' );
define( 'BESLOCK_SEO_CONFIG_FILE', __FILE__ );
define( 'BESLOCK_SEO_CONFIG_DIR', plugin_dir_path( __FILE__ ) );

require_once BESLOCK_SEO_CONFIG_DIR . 'includes/class-beslock-seo-config.php';

Beslock_SEO_Config::boot();

register_activation_hook( __FILE__, array( 'Beslock_SEO_Config', 'activate' ) );
register_deactivation_hook( __FILE__, array( 'Beslock_SEO_Config', 'deactivate' ) );
