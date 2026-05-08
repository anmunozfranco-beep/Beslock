<?php
/**
 * Shared path helpers for generator plugin.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class IPCG_Utils {

	/**
	 * Resolve plugins_ZIP directory in wp-content.
	 * Auto-creates if missing.
	 *
	 * @return string
	 */
	public static function get_plugins_zip_dir() {
		$path = wp_normalize_path( trailingslashit( WP_CONTENT_DIR ) . 'plugins_ZIP' );
		
		if ( ! is_dir( $path ) ) {
			wp_mkdir_p( $path );
		}
		
		return $path;
	}

	/**
	 * Shared JSON snapshot path at wp-content/plugins_ZIP/products_thrut.json
	 *
	 * @return string
	 */
	public static function get_products_json_path() {
		$default = wp_normalize_path( trailingslashit( self::get_plugins_zip_dir() ) . 'products_thrut.json' );
		return (string) apply_filters( 'ipcg_output_path', $default );
	}
}
