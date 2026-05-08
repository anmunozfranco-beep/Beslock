<?php
/**
 * Admin UI for catalog generation.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class IPCG_Admin {

	/**
	 * @var IPCG_Generator
	 */
	private $generator;

	public function __construct() {
		$this->generator = new IPCG_Generator();
		add_action( 'admin_menu', array( $this, 'register_menu_page' ) );
	}

	/**
	 * Registers Tools submenu page.
	 */
	public function register_menu_page() {
		add_management_page(
			__( 'Info Product Catalog Generator', 'info-prod-catlg-generator' ),
			__( 'Info Product Catalog Generator', 'info-prod-catlg-generator' ),
			'manage_options',
			'info-prod-catlg-generator',
			array( $this, 'render_admin_page' )
		);
	}

	/**
	 * Renders admin page and handles generation action.
	 */
	public function render_admin_page() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( esc_html__( 'Insufficient permissions.', 'info-prod-catlg-generator' ) );
		}

		$notice_type  = '';
		$notice_text  = '';
		$result       = null;
		$debug_output = '';

		if ( isset( $_POST['ipcg_generate_json'] ) ) {
			check_admin_referer( 'ipcg_generate_json_nonce' );
			$result = $this->generator->generate_catalog();

			if ( is_wp_error( $result ) ) {
				$notice_type = 'error';
				$notice_text = $result->get_error_message();
			} else {
				$notice_type = 'success';
				$notice_text = sprintf(
					__( 'Snapshot generated. Exported: %1$d, unique slugs: %2$d. Output: %3$s', 'info-prod-catlg-generator' ),
					(int) $result['count'],
					(int) $result['unique_slug_count'],
					(string) $result['path']
				);

				$debug_lines = array();
				foreach ( $result['debug_rows'] as $row ) {
					$debug_lines[] = sprintf(
						'ID=%1$d | post_type=%2$s | product_type=%3$s | slug=%4$s | status=%5$s | parent_id=%6$d',
						(int) $row['id'],
						(string) $row['post_type'],
						(string) $row['product_type'],
						(string) $row['slug'],
						(string) $row['status'],
						(int) $row['parent_id']
					);
				}
				$debug_output = implode( "\n", $debug_lines );
			}
		}

		$output_path = $this->generator->get_output_path();
		$output_dir  = dirname( $output_path );

		echo '<div class="wrap">';
		echo '<h1>' . esc_html__( 'Info Product Catalog Generator', 'info-prod-catlg-generator' ) . '</h1>';
		echo '<p>' . esc_html__( 'Generate portable products_thrut.json snapshot from published WooCommerce products deduplicated by slug.', 'info-prod-catlg-generator' ) . '</p>';

		if ( '' !== $notice_type ) {
			echo '<div class="notice notice-' . esc_attr( $notice_type ) . '"><p>' . esc_html( $notice_text ) . '</p></div>';
		}

		echo '<table class="widefat striped" style="max-width: 960px; margin-bottom: 16px;">';
		echo '<tbody>';
		echo '<tr><td><strong>' . esc_html__( 'Resolved JSON path', 'info-prod-catlg-generator' ) . '</strong></td><td><code>' . esc_html( $output_path ) . '</code></td></tr>';
		echo '<tr><td>' . esc_html__( 'File exists', 'info-prod-catlg-generator' ) . '</td><td>' . ( file_exists( $output_path ) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>' ) . '</td></tr>';
		echo '<tr><td>' . esc_html__( 'File readable', 'info-prod-catlg-generator' ) . '</td><td>' . ( is_readable( $output_path ) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>' ) . '</td></tr>';
		echo '<tr><td>' . esc_html__( 'Directory writable', 'info-prod-catlg-generator' ) . '</td><td>' . ( is_dir( $output_dir ) && is_writable( $output_dir ) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>' ) . '</td></tr>';

		if ( is_array( $result ) ) {
			echo '<tr><td><strong>' . esc_html__( 'Exported count', 'info-prod-catlg-generator' ) . '</strong></td><td>' . esc_html( (string) $result['count'] ) . '</td></tr>';
			echo '<tr><td><strong>' . esc_html__( 'Unique slugs', 'info-prod-catlg-generator' ) . '</strong></td><td>' . esc_html( (string) $result['unique_slug_count'] ) . '</td></tr>';
			echo '<tr><td><strong>' . esc_html__( 'Duplicate slugs', 'info-prod-catlg-generator' ) . '</strong></td><td>' . esc_html( (string) $result['duplicate_slug_count'] ) . '</td></tr>';
		}
		echo '</tbody>';
		echo '</table>';

		if ( is_array( $result ) && ! empty( $result['warnings'] ) ) {
			echo '<div class="notice notice-warning"><p><strong>' . esc_html__( 'Warnings', 'info-prod-catlg-generator' ) . '</strong></p><ul style="list-style:disc;padding-left:20px;">';
			foreach ( $result['warnings'] as $warning ) {
				echo '<li>' . esc_html( (string) $warning ) . '</li>';
			}
			echo '</ul></div>';
		}

		if ( is_array( $result ) ) {
			echo '<h2>' . esc_html__( 'Exported slugs', 'info-prod-catlg-generator' ) . '</h2>';
			echo '<textarea readonly="readonly" style="width:100%;max-width:980px;min-height:120px;font-family:monospace;">' . esc_textarea( implode( "\n", $result['exported_slugs'] ) ) . '</textarea>';

			echo '<h2>' . esc_html__( 'Debug inventory (pre-export)', 'info-prod-catlg-generator' ) . '</h2>';
			echo '<textarea readonly="readonly" style="width:100%;max-width:980px;min-height:280px;font-family:monospace;">' . esc_textarea( $debug_output ) . '</textarea>';
		}

		echo '<form method="post" style="margin-top:16px;">';
		wp_nonce_field( 'ipcg_generate_json_nonce' );
		echo '<p><button type="submit" name="ipcg_generate_json" class="button button-primary">' . esc_html__( 'Generate JSON', 'info-prod-catlg-generator' ) . '</button></p>';
		echo '</form>';
		echo '</div>';
	}
}
