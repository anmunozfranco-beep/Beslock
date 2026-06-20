<?php

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Beslock_SEO_Config {

	const OPTION_LAST_SYNC        = 'beslock_seo_config_last_sync';
	const OPTION_VERSION          = 'beslock_seo_config_version';
	const OPTION_SOURCE_HASH      = 'beslock_seo_config_source_hash';
	const OPTION_LAST_MAINTENANCE = 'beslock_seo_config_last_maintenance';
	const CRON_HOOK               = 'beslock_seo_config_daily_sync';
	const TOOLS_PAGE_SLUG         = 'beslock-seo-config';
	const PLUGIN_SITESEO_FREE     = 'siteseo/siteseo.php';
	const PLUGIN_SITESEO_PRO      = 'siteseo-pro/siteseo-pro.php';
	const META_TITLE              = '_beslock_seo_title';
	const META_DESCRIPTION        = '_beslock_seo_description';
	const META_OG_TITLE           = '_beslock_seo_og_title';
	const META_OG_DESCRIPTION     = '_beslock_seo_og_description';
	const META_TWITTER_TITLE      = '_beslock_seo_twitter_title';
	const META_TWITTER_DESCRIPTION = '_beslock_seo_twitter_description';
	const META_IMAGE_URL          = '_beslock_seo_image_url';
	const META_IMAGE_ALT          = '_beslock_seo_image_alt';
	const META_PAYLOAD            = '_beslock_seo_payload';
	const META_FOCUS_KEYWORDS     = '_beslock_seo_focus_keywords';
	const META_FORCE_NOINDEX      = '_beslock_seo_force_noindex';
	const TERM_META_TITLE         = '_beslock_seo_title';
	const TERM_META_DESCRIPTION   = '_beslock_seo_description';
	const TERM_META_FORCE_NOINDEX = '_beslock_seo_force_noindex';

	private static $request_meta = null;
	private static $catalog_cache = null;
	private static $sitemap_excluded_ids = array();

	public static function boot() {
		add_action( 'init', array( __CLASS__, 'ensure_schedule' ) );
		add_action( 'wp', array( __CLASS__, 'maybe_disable_siteseo_organization_schema' ), 20 );
		add_action( self::CRON_HOOK, array( __CLASS__, 'run_cron_sync' ) );
		add_action( 'admin_init', array( __CLASS__, 'maybe_sync_after_deploy' ) );
		add_action( 'admin_menu', array( __CLASS__, 'register_tools_page' ) );
		add_filter( 'pre_get_document_title', array( __CLASS__, 'filter_document_title' ), 20 );
		add_action( 'wp_head', array( __CLASS__, 'output_meta_tags' ), 1 );
		add_action( 'wp_head', array( __CLASS__, 'output_json_ld' ), 99 );
		add_filter( 'wp_robots', array( __CLASS__, 'filter_wp_robots' ), 20 );
		add_filter( 'wp_sitemaps_add_provider', array( __CLASS__, 'filter_sitemap_provider' ), 10, 2 );
		add_filter( 'wp_sitemaps_taxonomies', array( __CLASS__, 'filter_sitemap_taxonomies' ) );
		add_filter( 'wp_sitemaps_taxonomies_query_args', array( __CLASS__, 'filter_sitemap_taxonomies_query_args' ), 10, 2 );
		add_filter( 'wp_sitemaps_posts_query_args', array( __CLASS__, 'filter_sitemap_posts_query_args' ), 10, 2 );
	}

	public static function activate() {
		self::ensure_schedule();
		self::sync_catalog( 'activation' );
	}

	public static function deactivate() {
		wp_clear_scheduled_hook( self::CRON_HOOK );
	}

	public static function ensure_schedule() {
		if ( ! wp_next_scheduled( self::CRON_HOOK ) ) {
			wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', self::CRON_HOOK );
		}
	}

	public static function run_cron_sync() {
		self::sync_catalog( 'cron' );
	}

	public static function maybe_sync_after_deploy() {
		if ( ! is_admin() || ! current_user_can( 'manage_options' ) ) {
			return;
		}

		$current_version = defined( 'BESLOCK_SEO_CONFIG_VERSION' ) ? BESLOCK_SEO_CONFIG_VERSION : '0.0.0';
		$saved_version   = (string) get_option( self::OPTION_VERSION, '' );
		$current_hash    = self::compute_source_hash();
		$saved_hash      = (string) get_option( self::OPTION_SOURCE_HASH, '' );

		if ( $saved_version !== $current_version || ( $current_hash && $current_hash !== $saved_hash ) ) {
			self::sync_catalog( 'admin-version-check' );
		}
	}

	public static function register_tools_page() {
		add_management_page(
			__( 'BESLOCK SEO', 'beslock' ),
			__( 'BESLOCK SEO', 'beslock' ),
			'manage_options',
			self::TOOLS_PAGE_SLUG,
			array( __CLASS__, 'render_tools_page' )
		);
	}

	public static function render_tools_page() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( esc_html__( 'No tienes permisos para acceder a esta herramienta.', 'beslock' ) );
		}

		$sync_notice        = null;
		$maintenance_notice = null;

		if ( isset( $_POST['beslock_siteseo_rebuild_now'] ) ) {
			check_admin_referer( 'beslock_siteseo_rebuild_action', 'beslock_siteseo_rebuild_nonce' );
			$maintenance_notice = self::run_siteseo_free_rebuild();
		}

		if ( isset( $_POST['beslock_seo_sync_now'] ) ) {
			check_admin_referer( 'beslock_seo_sync_action', 'beslock_seo_sync_nonce' );
			$sync_notice = self::sync_catalog( 'manual-tools-sync' );
		}

		$last_sync         = get_option( self::OPTION_LAST_SYNC, array() );
		$last_maintenance  = get_option( self::OPTION_LAST_MAINTENANCE, array() );
		$catalog           = self::load_catalog();
		$sources           = self::get_source_paths();
		$site_title        = self::get_site_name();
		$product_map       = ! empty( $catalog['products'] ) && is_array( $catalog['products'] ) ? $catalog['products'] : array();
		$plugin_statuses   = self::get_plugin_statuses();
		$meta_owner_label  = self::get_meta_owner_label();

		echo '<div class="wrap">';
		echo '<h1>' . esc_html__( 'BESLOCK SEO', 'beslock' ) . '</h1>';
		echo '<p>' . esc_html__( 'Sincroniza titulos, meta descriptions, Open Graph, Twitter Cards, schema, alt de imagenes y compatibilidad con SITESEO a partir de las fuentes internas de productos y manuales. Tambien permite ejecutar una reconstruccion limpia de SITESEO Free sin depender de ajustes manuales en base de datos.', 'beslock' ) . '</p>';

		if ( is_array( $maintenance_notice ) ) {
			$status_class = empty( $maintenance_notice['errors'] ) ? 'notice notice-success' : 'notice notice-warning';
			echo '<div class="' . esc_attr( $status_class ) . '"><p>' . esc_html( self::format_maintenance_notice( $maintenance_notice ) ) . '</p></div>';
		}

		if ( is_array( $sync_notice ) ) {
			$status_class = empty( $sync_notice['errors'] ) ? 'notice notice-success' : 'notice notice-warning';
			echo '<div class="' . esc_attr( $status_class ) . '"><p>' . esc_html( self::format_sync_notice( $sync_notice ) ) . '</p></div>';
		}

		echo '<table class="widefat striped" style="max-width:1100px">';
		echo '<tbody>';
		echo '<tr><th style="width:280px">' . esc_html__( 'Marca detectada', 'beslock' ) . '</th><td>' . esc_html( $site_title ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Productos con fuente SEO', 'beslock' ) . '</th><td>' . intval( count( $product_map ) ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Ciudades detectadas', 'beslock' ) . '</th><td>' . esc_html( implode( ', ', self::get_available_cities( $catalog ) ) ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Motor que gobierna metadatos', 'beslock' ) . '</th><td>' . esc_html( $meta_owner_label ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Ultima sincronizacion', 'beslock' ) . '</th><td>' . esc_html( ! empty( $last_sync['timestamp'] ) ? $last_sync['timestamp'] : 'Aun no registrada' ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Motivo ultimo sync', 'beslock' ) . '</th><td>' . esc_html( ! empty( $last_sync['reason'] ) ? $last_sync['reason'] : 'N/D' ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Ultimo mantenimiento SITESEO', 'beslock' ) . '</th><td>' . esc_html( ! empty( $last_maintenance['timestamp'] ) ? $last_maintenance['timestamp'] : 'Aun no registrado' ) . '</td></tr>';
		echo '<tr><th>' . esc_html__( 'Hash de fuentes', 'beslock' ) . '</th><td><code>' . esc_html( ! empty( $last_sync['source_hash'] ) ? $last_sync['source_hash'] : 'N/D' ) . '</code></td></tr>';
		echo '</tbody>';
		echo '</table>';

		echo '<h2 style="margin-top:24px">' . esc_html__( 'Estado de plugins SEO', 'beslock' ) . '</h2>';
		echo '<table class="widefat striped" style="max-width:900px"><tbody>';
		foreach ( $plugin_statuses as $status ) {
			echo '<tr><th style="width:280px">' . esc_html( $status['label'] ) . '</th><td>' . esc_html( self::format_plugin_status( $status ) ) . '</td></tr>';
		}
		echo '</tbody></table>';

		echo '<h2 style="margin-top:24px">' . esc_html__( 'Fuentes usadas', 'beslock' ) . '</h2>';
		echo '<ul style="list-style:disc;padding-left:20px">';
		foreach ( $sources as $label => $path ) {
			echo '<li><strong>' . esc_html( $label ) . ':</strong> <code>' . esc_html( $path ) . '</code></li>';
		}
		echo '</ul>';

		echo '<h2 style="margin-top:24px">' . esc_html__( 'Operaciones', 'beslock' ) . '</h2>';
		echo '<form method="post" style="margin-top:12px;padding:16px;border:1px solid #dcdcde;background:#fff;max-width:900px">';
		wp_nonce_field( 'beslock_siteseo_rebuild_action', 'beslock_siteseo_rebuild_nonce' );
		echo '<h3 style="margin-top:0">' . esc_html__( 'Reconstruccion limpia de SITESEO Free', 'beslock' ) . '</h3>';
		echo '<p>' . esc_html__( 'Crea un snapshot JSON en uploads, desactiva SITESEO Free y SITESEO PRO si estuvieran activos, limpia residuos heredados de opciones y metadatos, instala SITESEO Free desde WordPress.org si no estuviera presente, lo activa y vuelve a sembrar la configuracion SEO desde las fuentes internas.', 'beslock' ) . '</p>';
		echo '<p><button type="submit" name="beslock_siteseo_rebuild_now" class="button button-primary">' . esc_html__( 'Ejecutar limpieza + instalar/activar SITESEO Free', 'beslock' ) . '</button></p>';
		echo '</form>';

		echo '<form method="post" style="margin-top:24px">';
		wp_nonce_field( 'beslock_seo_sync_action', 'beslock_seo_sync_nonce' );
		echo '<p><button type="submit" name="beslock_seo_sync_now" class="button">' . esc_html__( 'Sincronizar SEO ahora', 'beslock' ) . '</button></p>';
		echo '</form>';

		if ( ! empty( $last_sync['summary'] ) && is_array( $last_sync['summary'] ) ) {
			echo '<h2>' . esc_html__( 'Ultimo resumen tecnico', 'beslock' ) . '</h2>';
			echo '<table class="widefat striped" style="max-width:900px"><tbody>';
			foreach ( $last_sync['summary'] as $key => $value ) {
				if ( is_array( $value ) ) {
					$value = implode( ', ', $value );
				}
				echo '<tr><th style="width:280px">' . esc_html( (string) $key ) . '</th><td>' . esc_html( (string) $value ) . '</td></tr>';
			}
			echo '</tbody></table>';
		}

		if ( ! empty( $last_maintenance['summary'] ) && is_array( $last_maintenance['summary'] ) ) {
			echo '<h2>' . esc_html__( 'Ultimo mantenimiento SITESEO', 'beslock' ) . '</h2>';
			echo '<table class="widefat striped" style="max-width:900px"><tbody>';
			foreach ( $last_maintenance['summary'] as $key => $value ) {
				if ( is_array( $value ) ) {
					$value = implode( ', ', $value );
				}
				echo '<tr><th style="width:280px">' . esc_html( (string) $key ) . '</th><td>' . esc_html( (string) $value ) . '</td></tr>';
			}
			echo '</tbody></table>';
		}

		echo '</div>';
	}

	private static function format_sync_notice( $summary ) {
		$parts = array(
			sprintf(
				/* translators: 1: synced products, 2: pages, 3: terms, 4: attachments */
				__( 'SEO sincronizado. Productos: %1$d, paginas: %2$d, terminos: %3$d, imagenes: %4$d.', 'beslock' ),
				intval( $summary['products_synced'] ),
				intval( $summary['pages_synced'] ),
				intval( $summary['terms_synced'] ),
				intval( $summary['attachments_synced'] )
			),
		);

		if ( ! empty( $summary['errors'] ) && is_array( $summary['errors'] ) ) {
			$parts[] = __( 'Advertencias:', 'beslock' ) . ' ' . implode( ' | ', array_map( 'sanitize_text_field', $summary['errors'] ) );
		}

		return implode( ' ', $parts );
	}

	private static function format_maintenance_notice( $summary ) {
		$parts = array(
			sprintf(
				/* translators: 1: deleted options, 2: deleted post meta rows, 3: deleted term meta rows */
				__( 'Mantenimiento SITESEO completado. Opciones eliminadas: %1$d, post meta: %2$d, term meta: %3$d.', 'beslock' ),
				intval( $summary['options_deleted'] ),
				intval( $summary['postmeta_deleted'] ),
				intval( $summary['termmeta_deleted'] )
			),
		);

		if ( ! empty( $summary['siteseo_free_activated'] ) ) {
			if ( ! empty( $summary['siteseo_free_installed'] ) ) {
				$parts[] = __( 'SITESEO Free se instaló desde WordPress.org y quedó activo.', 'beslock' );
			} else {
				$parts[] = __( 'SITESEO Free quedo activo.', 'beslock' );
			}
		}

		if ( ! empty( $summary['sync_summary']['products_synced'] ) || ! empty( $summary['sync_summary']['pages_synced'] ) ) {
			$parts[] = sprintf(
				/* translators: 1: products synced, 2: pages synced, 3: terms synced */
				__( 'Resiembra ejecutada. Productos: %1$d, paginas: %2$d, terminos: %3$d.', 'beslock' ),
				intval( $summary['sync_summary']['products_synced'] ),
				intval( $summary['sync_summary']['pages_synced'] ),
				intval( $summary['sync_summary']['terms_synced'] )
			);
		}

		if ( ! empty( $summary['snapshot_path'] ) ) {
			$parts[] = sprintf(
				/* translators: %s: snapshot path */
				__( 'Snapshot: %s.', 'beslock' ),
				$summary['snapshot_path']
			);
		}

		if ( ! empty( $summary['errors'] ) && is_array( $summary['errors'] ) ) {
			$parts[] = __( 'Advertencias:', 'beslock' ) . ' ' . implode( ' | ', array_map( 'sanitize_text_field', $summary['errors'] ) );
		}

		return implode( ' ', $parts );
	}

	public static function sync_catalog( $reason = 'manual' ) {
		$catalog = self::load_catalog( true );
		$summary = array(
			'reason'             => $reason,
			'products_synced'    => 0,
			'pages_synced'       => 0,
			'terms_synced'       => 0,
			'attachments_synced' => 0,
			'siteseo_options'    => 0,
			'errors'             => array(),
		);

		if ( empty( $catalog['products'] ) || ! is_array( $catalog['products'] ) ) {
			$summary['errors'][] = 'No se encontraron productos validos en las fuentes SEO.';
			self::store_sync_summary( $summary );
			return $summary;
		}

		foreach ( $catalog['products'] as $slug => $product_record ) {
			$post_id = self::find_product_post_id( $slug, ! empty( $product_record['sku'] ) ? $product_record['sku'] : '' );

			if ( ! $post_id ) {
				$summary['errors'][] = sprintf( 'Producto no encontrado en WordPress: %s', $slug );
				continue;
			}

			$product_meta = self::build_product_meta( $product_record, $post_id, $catalog );
			self::update_post_seo_payload( $post_id, $product_meta );
			self::sync_post_to_siteseo( $post_id, $product_meta );
			$summary['products_synced']++;
			$summary['attachments_synced'] += self::sync_product_attachment_alts( $post_id, $product_record );
		}

		$summary['pages_synced'] += self::sync_core_pages( $catalog );
		$summary['pages_synced'] += self::sync_low_value_posts();
		$summary['terms_synced'] += self::sync_product_terms( $catalog );
		$summary['siteseo_options'] += self::sync_siteseo_global_options( $catalog );

		self::store_sync_summary( $summary );
		self::$request_meta         = null;
		self::$sitemap_excluded_ids = array();

		return $summary;
	}

	private static function store_sync_summary( $summary ) {
		$summary['timestamp']   = current_time( 'mysql' );
		$summary['version']     = defined( 'BESLOCK_SEO_CONFIG_VERSION' ) ? BESLOCK_SEO_CONFIG_VERSION : '0.0.0';
		$summary['source_hash'] = self::compute_source_hash();
		$summary['summary']     = array(
			'products_synced'    => intval( $summary['products_synced'] ),
			'pages_synced'       => intval( $summary['pages_synced'] ),
			'terms_synced'       => intval( $summary['terms_synced'] ),
			'attachments_synced' => intval( $summary['attachments_synced'] ),
			'siteseo_options'    => intval( $summary['siteseo_options'] ),
			'errors'             => ! empty( $summary['errors'] ) ? $summary['errors'] : array(),
		);

		update_option( self::OPTION_LAST_SYNC, $summary, false );
		update_option( self::OPTION_VERSION, $summary['version'], false );
		update_option( self::OPTION_SOURCE_HASH, $summary['source_hash'], false );
	}

	private static function store_maintenance_summary( $summary ) {
		$summary['timestamp'] = current_time( 'mysql' );
		$summary['version']   = defined( 'BESLOCK_SEO_CONFIG_VERSION' ) ? BESLOCK_SEO_CONFIG_VERSION : '0.0.0';
		$summary['summary']   = array(
			'snapshot_created'         => ! empty( $summary['snapshot_created'] ) ? 'Si' : 'No',
			'snapshot_path'            => ! empty( $summary['snapshot_path'] ) ? $summary['snapshot_path'] : 'N/D',
			'plugins_deactivated'      => ! empty( $summary['plugins_deactivated'] ) ? $summary['plugins_deactivated'] : array( 'Ninguno' ),
			'options_deleted'          => intval( $summary['options_deleted'] ),
			'postmeta_deleted'         => intval( $summary['postmeta_deleted'] ),
			'termmeta_deleted'         => intval( $summary['termmeta_deleted'] ),
			'siteseo_free_installed'   => ! empty( $summary['siteseo_free_installed'] ) ? 'Si' : 'No',
			'siteseo_free_activated'   => ! empty( $summary['siteseo_free_activated'] ) ? 'Si' : 'No',
			'products_resynced'        => ! empty( $summary['sync_summary']['products_synced'] ) ? intval( $summary['sync_summary']['products_synced'] ) : 0,
			'pages_resynced'           => ! empty( $summary['sync_summary']['pages_synced'] ) ? intval( $summary['sync_summary']['pages_synced'] ) : 0,
			'terms_resynced'           => ! empty( $summary['sync_summary']['terms_synced'] ) ? intval( $summary['sync_summary']['terms_synced'] ) : 0,
			'attachments_resynced'     => ! empty( $summary['sync_summary']['attachments_synced'] ) ? intval( $summary['sync_summary']['attachments_synced'] ) : 0,
			'siteseo_options_resynced' => ! empty( $summary['sync_summary']['siteseo_options'] ) ? intval( $summary['sync_summary']['siteseo_options'] ) : 0,
			'errors'                   => ! empty( $summary['errors'] ) ? $summary['errors'] : array(),
		);

		update_option( self::OPTION_LAST_MAINTENANCE, $summary, false );
	}

	private static function run_siteseo_free_rebuild() {
		$summary = array(
			'reason'                 => 'siteseo-free-rebuild',
			'snapshot_created'       => false,
			'snapshot_path'          => '',
			'snapshot_url'           => '',
			'plugins_deactivated'    => array(),
			'options_deleted'        => 0,
			'postmeta_deleted'       => 0,
			'termmeta_deleted'       => 0,
			'siteseo_free_installed' => false,
			'siteseo_free_activated' => false,
			'plugin_status_before'   => self::get_plugin_statuses(),
			'plugin_status_after'    => array(),
			'sync_summary'           => array(),
			'errors'                 => array(),
		);

		$snapshot = self::create_siteseo_snapshot();
		if ( ! empty( $snapshot['created'] ) ) {
			$summary['snapshot_created'] = true;
			$summary['snapshot_path']    = $snapshot['path'];
			$summary['snapshot_url']     = $snapshot['url'];
		}
		if ( ! empty( $snapshot['errors'] ) ) {
			$summary['errors'] = array_merge( $summary['errors'], $snapshot['errors'] );
		}

		$clean_summary = self::clean_siteseo_environment();
		$summary['plugins_deactivated'] = ! empty( $clean_summary['plugins_deactivated'] ) ? $clean_summary['plugins_deactivated'] : array();
		$summary['options_deleted']     = ! empty( $clean_summary['options_deleted'] ) ? intval( $clean_summary['options_deleted'] ) : 0;
		$summary['postmeta_deleted']    = ! empty( $clean_summary['postmeta_deleted'] ) ? intval( $clean_summary['postmeta_deleted'] ) : 0;
		$summary['termmeta_deleted']    = ! empty( $clean_summary['termmeta_deleted'] ) ? intval( $clean_summary['termmeta_deleted'] ) : 0;
		if ( ! empty( $clean_summary['errors'] ) ) {
			$summary['errors'] = array_merge( $summary['errors'], $clean_summary['errors'] );
		}

		$activation = self::activate_siteseo_free();
		$summary['siteseo_free_installed'] = ! empty( $activation['installed'] );
		$summary['siteseo_free_activated'] = ! empty( $activation['activated'] );
		if ( ! empty( $activation['errors'] ) ) {
			$summary['errors'] = array_merge( $summary['errors'], $activation['errors'] );
		}

		if ( $summary['siteseo_free_activated'] ) {
			$summary['sync_summary'] = self::sync_catalog( 'siteseo-free-rebuild' );
			if ( ! empty( $summary['sync_summary']['errors'] ) ) {
				$summary['errors'] = array_merge( $summary['errors'], $summary['sync_summary']['errors'] );
			}
		}

		$summary['plugin_status_after'] = self::get_plugin_statuses();
		$summary['errors']              = array_values( array_unique( array_filter( array_map( 'sanitize_text_field', $summary['errors'] ) ) ) );

		self::store_maintenance_summary( $summary );

		return $summary;
	}

	private static function create_siteseo_snapshot() {
		$upload_dir = wp_upload_dir();
		$summary    = array(
			'created' => false,
			'path'    => '',
			'url'     => '',
			'errors'  => array(),
		);

		if ( ! empty( $upload_dir['error'] ) ) {
			$summary['errors'][] = 'No se pudo resolver el directorio de uploads para guardar el snapshot.';
			return $summary;
		}

		$target_dir = trailingslashit( $upload_dir['basedir'] ) . 'beslock-seo-config';
		if ( ! wp_mkdir_p( $target_dir ) ) {
			$summary['errors'][] = 'No se pudo crear el directorio de snapshots SEO.';
			return $summary;
		}

		$filename = 'siteseo-snapshot-' . current_time( 'Ymd-His' ) . '.json';
		$path     = trailingslashit( $target_dir ) . $filename;
		$url      = trailingslashit( $upload_dir['baseurl'] ) . 'beslock-seo-config/' . $filename;
		$payload  = array(
			'generated_at'      => current_time( 'mysql' ),
			'site_url'          => home_url( '/' ),
			'plugin_statuses'   => self::get_plugin_statuses(),
			'option_names'      => self::get_siteseo_option_names(),
			'options'           => self::get_siteseo_options_snapshot(),
			'postmeta_counts'   => self::get_siteseo_postmeta_counts(),
			'termmeta_counts'   => self::get_siteseo_termmeta_counts(),
			'last_sync'         => get_option( self::OPTION_LAST_SYNC, array() ),
			'last_maintenance'  => get_option( self::OPTION_LAST_MAINTENANCE, array() ),
		);

		$json = wp_json_encode( $payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		if ( ! $json || false === file_put_contents( $path, $json ) ) {
			$summary['errors'][] = 'No se pudo escribir el snapshot JSON de SITESEO.';
			return $summary;
		}

		$summary['created'] = true;
		$summary['path']    = $path;
		$summary['url']     = $url;

		return $summary;
	}

	private static function clean_siteseo_environment() {
		global $wpdb;

		self::load_plugin_api();

		$summary = array(
			'plugins_deactivated' => array(),
			'options_deleted'     => 0,
			'postmeta_deleted'    => 0,
			'termmeta_deleted'    => 0,
			'errors'              => array(),
		);

		$plugin_labels = array(
			self::PLUGIN_SITESEO_FREE => 'SITESEO Free',
			self::PLUGIN_SITESEO_PRO  => 'SITESEO PRO',
		);

		foreach ( $plugin_labels as $plugin_file => $plugin_label ) {
			if ( function_exists( 'is_plugin_active' ) && is_plugin_active( $plugin_file ) ) {
				deactivate_plugins( $plugin_file, true );
				$summary['plugins_deactivated'][] = $plugin_label;
			}
		}

		foreach ( self::get_siteseo_option_names() as $option_name ) {
			if ( delete_option( $option_name ) ) {
				$summary['options_deleted']++;
			}
		}

		$postmeta_deleted = $wpdb->query(
			$wpdb->prepare(
				"DELETE FROM {$wpdb->postmeta} WHERE meta_key LIKE %s OR meta_key = %s",
				$wpdb->esc_like( '_siteseo' ) . '%',
				'siteseo_analysis_target_kw'
			)
		);
		if ( false === $postmeta_deleted ) {
			$summary['errors'][] = 'No se pudieron limpiar todos los post meta heredados de SITESEO.';
		} else {
			$summary['postmeta_deleted'] = intval( $postmeta_deleted );
		}

		$termmeta_deleted = $wpdb->query(
			$wpdb->prepare(
				"DELETE FROM {$wpdb->termmeta} WHERE meta_key LIKE %s",
				$wpdb->esc_like( '_siteseo' ) . '%'
			)
		);
		if ( false === $termmeta_deleted ) {
			$summary['errors'][] = 'No se pudieron limpiar todos los term meta heredados de SITESEO.';
		} else {
			$summary['termmeta_deleted'] = intval( $termmeta_deleted );
		}

		self::$request_meta         = null;
		self::$catalog_cache        = null;
		self::$sitemap_excluded_ids = array();

		return $summary;
	}

	private static function activate_siteseo_free() {
		self::load_plugin_api();

		$summary = array(
			'activated' => false,
			'installed' => false,
			'errors'    => array(),
		);

		$plugin_path = trailingslashit( WP_PLUGIN_DIR ) . self::PLUGIN_SITESEO_FREE;
		if ( ! file_exists( $plugin_path ) ) {
			$install_summary = self::install_siteseo_free();
			$summary['installed'] = ! empty( $install_summary['installed'] );
			if ( ! empty( $install_summary['errors'] ) ) {
				$summary['errors'] = array_merge( $summary['errors'], $install_summary['errors'] );
				return $summary;
			}
		}

		if ( function_exists( 'is_plugin_active' ) && is_plugin_active( self::PLUGIN_SITESEO_FREE ) ) {
			$summary['activated'] = true;
			return $summary;
		}

		$result = activate_plugin( self::PLUGIN_SITESEO_FREE, '', false, false );
		if ( is_wp_error( $result ) ) {
			$summary['errors'][] = $result->get_error_message();
			return $summary;
		}

		$summary['activated'] = true;

		return $summary;
	}

	private static function install_siteseo_free() {
		self::load_plugin_install_api();

		$summary = array(
			'installed' => false,
			'errors'    => array(),
		);

		if ( ! current_user_can( 'install_plugins' ) ) {
			$summary['errors'][] = 'El usuario actual no tiene permisos para instalar plugins.';
			return $summary;
		}

		$plugin_path = trailingslashit( WP_PLUGIN_DIR ) . self::PLUGIN_SITESEO_FREE;
		if ( file_exists( $plugin_path ) ) {
			$summary['installed'] = true;
			return $summary;
		}

		$api = plugins_api(
			'plugin_information',
			array(
				'slug'   => 'siteseo',
				'fields' => array(
					'sections' => false,
				),
			)
		);

		if ( is_wp_error( $api ) ) {
			$summary['errors'] = array_merge( $summary['errors'], self::extract_wp_error_messages( $api ) );
			return $summary;
		}

		if ( empty( $api->download_link ) ) {
			$summary['errors'][] = 'No se pudo obtener el paquete oficial de SITESEO Free.';
			return $summary;
		}

		$skin     = new Automatic_Upgrader_Skin();
		$upgrader = new Plugin_Upgrader( $skin );
		$result   = $upgrader->install( $api->download_link );

		if ( is_wp_error( $result ) ) {
			$summary['errors'] = array_merge( $summary['errors'], self::extract_wp_error_messages( $result ) );
		}

		if ( method_exists( $skin, 'get_errors' ) ) {
			$skin_errors = $skin->get_errors();
			if ( is_wp_error( $skin_errors ) && $skin_errors->has_errors() ) {
				$summary['errors'] = array_merge( $summary['errors'], self::extract_wp_error_messages( $skin_errors ) );
			}
		}

		if ( ! $result || ! file_exists( $plugin_path ) ) {
			if ( empty( $summary['errors'] ) ) {
				$summary['errors'][] = 'La instalacion automatica de SITESEO Free no dejó el plugin disponible en wp-content/plugins.';
			}
			return $summary;
		}

		wp_clean_plugins_cache( true );
		$summary['installed'] = true;

		return $summary;
	}

	private static function load_plugin_api() {
		if ( ! function_exists( 'is_plugin_active' ) || ! function_exists( 'activate_plugin' ) ) {
			require_once ABSPATH . 'wp-admin/includes/plugin.php';
		}
	}

	private static function load_plugin_install_api() {
		self::load_plugin_api();

		if ( ! function_exists( 'plugins_api' ) ) {
			require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
		}
		if ( ! class_exists( 'Plugin_Upgrader' ) ) {
			require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
		}
		if ( ! function_exists( 'request_filesystem_credentials' ) ) {
			require_once ABSPATH . 'wp-admin/includes/file.php';
		}
	}

	private static function extract_wp_error_messages( $error ) {
		if ( ! is_wp_error( $error ) ) {
			return array();
		}

		$messages = array();
		foreach ( $error->get_error_messages() as $message ) {
			$message = sanitize_text_field( $message );
			if ( '' !== $message ) {
				$messages[] = $message;
			}
		}

		return array_values( array_unique( $messages ) );
	}

	private static function get_plugin_statuses() {
		self::load_plugin_api();

		$statuses = array(
			array(
				'label'     => 'BESLOCK SEO Config',
				'basename'  => plugin_basename( BESLOCK_SEO_CONFIG_FILE ),
				'installed' => file_exists( BESLOCK_SEO_CONFIG_FILE ),
				'active'    => function_exists( 'is_plugin_active' ) ? is_plugin_active( plugin_basename( BESLOCK_SEO_CONFIG_FILE ) ) : true,
			),
			array(
				'label'     => 'SITESEO Free',
				'basename'  => self::PLUGIN_SITESEO_FREE,
				'installed' => file_exists( trailingslashit( WP_PLUGIN_DIR ) . self::PLUGIN_SITESEO_FREE ),
				'active'    => function_exists( 'is_plugin_active' ) ? is_plugin_active( self::PLUGIN_SITESEO_FREE ) : self::is_siteseo_active(),
			),
			array(
				'label'     => 'SITESEO PRO',
				'basename'  => self::PLUGIN_SITESEO_PRO,
				'installed' => file_exists( trailingslashit( WP_PLUGIN_DIR ) . self::PLUGIN_SITESEO_PRO ),
				'active'    => function_exists( 'is_plugin_active' ) ? is_plugin_active( self::PLUGIN_SITESEO_PRO ) : defined( 'SITESEO_PRO_VERSION' ),
			),
		);

		return $statuses;
	}

	private static function format_plugin_status( $status ) {
		$parts = array();
		$parts[] = ! empty( $status['installed'] ) ? 'Instalado' : 'No instalado';
		$parts[] = ! empty( $status['active'] ) ? 'Activo' : 'Inactivo';

		return implode( ' | ', $parts );
	}

	private static function get_meta_owner_label() {
		if ( defined( 'WPSEO_VERSION' ) ) {
			return 'Yoast SEO';
		}

		if ( defined( 'RANK_MATH_VERSION' ) ) {
			return 'Rank Math';
		}

		if ( defined( 'AIOSEO_VERSION' ) ) {
			return 'All in One SEO';
		}

		if ( self::is_siteseo_active() ) {
			return defined( 'SITESEO_PRO_VERSION' ) ? 'SITESEO PRO' : 'SITESEO Free';
		}

		return 'BESLOCK SEO Config';
	}

	private static function get_siteseo_option_names() {
		global $wpdb;

		$names = $wpdb->get_col(
			$wpdb->prepare(
				"SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s OR option_name LIKE %s OR option_name LIKE %s OR option_name LIKE %s OR option_name LIKE %s OR option_name = %s ORDER BY option_name ASC",
				$wpdb->esc_like( 'siteseo' ) . '%',
				$wpdb->esc_like( '_transient_siteseo' ) . '%',
				$wpdb->esc_like( '_transient_timeout_siteseo' ) . '%',
				$wpdb->esc_like( '_site_transient_siteseo' ) . '%',
				$wpdb->esc_like( '_site_transient_timeout_siteseo' ) . '%',
				'external_updates-siteseo-pro'
			)
		);

		return is_array( $names ) ? array_values( array_unique( array_filter( $names ) ) ) : array();
	}

	private static function get_siteseo_options_snapshot() {
		$options = array();

		foreach ( self::get_siteseo_option_names() as $option_name ) {
			$options[ $option_name ] = get_option( $option_name );
		}

		return $options;
	}

	private static function get_siteseo_postmeta_counts() {
		global $wpdb;

		$rows = $wpdb->get_results(
			$wpdb->prepare(
				"SELECT meta_key, COUNT(*) AS total FROM {$wpdb->postmeta} WHERE meta_key LIKE %s OR meta_key = %s GROUP BY meta_key ORDER BY total DESC, meta_key ASC",
				$wpdb->esc_like( '_siteseo' ) . '%',
				'siteseo_analysis_target_kw'
			),
			ARRAY_A
		);

		return is_array( $rows ) ? $rows : array();
	}

	private static function get_siteseo_termmeta_counts() {
		global $wpdb;

		$rows = $wpdb->get_results(
			$wpdb->prepare(
				"SELECT meta_key, COUNT(*) AS total FROM {$wpdb->termmeta} WHERE meta_key LIKE %s GROUP BY meta_key ORDER BY total DESC, meta_key ASC",
				$wpdb->esc_like( '_siteseo' ) . '%'
			),
			ARRAY_A
		);

		return is_array( $rows ) ? $rows : array();
	}

	private static function load_catalog( $force = false ) {
		if ( ! $force && null !== self::$catalog_cache ) {
			return self::$catalog_cache;
		}

		$theme_dir          = trailingslashit( WP_CONTENT_DIR ) . 'themes/beslock-custom';
		$products_path      = $theme_dir . '/data/products.json';
		$manual_index_path  = $theme_dir . '/assets/manuals/index.json';
		$pricing_csv_path   = $theme_dir . '/data/woocommerce-pricing-import.csv';
		$runtime_products   = self::read_json_file( $products_path );
		$manual_index_data  = self::read_json_file( $manual_index_path );
		$manual_index_items = ! empty( $manual_index_data['products'] ) && is_array( $manual_index_data['products'] ) ? $manual_index_data['products'] : array();
		$manual_index_map   = array();
		$catalog_products   = array();

		foreach ( $manual_index_items as $manual_index_item ) {
			$slug = ! empty( $manual_index_item['slug'] ) ? sanitize_title( $manual_index_item['slug'] ) : '';
			if ( $slug ) {
				$manual_index_map[ $slug ] = $manual_index_item;
			}
		}

		if ( is_array( $runtime_products ) ) {
			foreach ( $runtime_products as $runtime_product ) {
				if ( ! is_array( $runtime_product ) ) {
					continue;
				}

				$slug = ! empty( $runtime_product['slug'] ) ? sanitize_title( $runtime_product['slug'] ) : '';
				if ( ! $slug ) {
					continue;
				}

				$manual_index_item  = isset( $manual_index_map[ $slug ] ) ? $manual_index_map[ $slug ] : array();
				$manual_product_raw = array();

				if ( ! empty( $manual_index_item['product_json'] ) ) {
					$manual_product_path = $theme_dir . '/assets/manuals/' . ltrim( $manual_index_item['product_json'], '/' );
					$manual_product_raw  = self::read_json_file( $manual_product_path );
				}

				$catalog_products[ $slug ] = self::normalize_product_record( $runtime_product, $manual_index_item, $manual_product_raw );
			}
		}

		self::$catalog_cache = array(
			'products'        => $catalog_products,
			'available_cities' => self::extract_available_cities( $pricing_csv_path ),
			'sources'         => self::get_source_paths(),
		);

		return self::$catalog_cache;
	}

	private static function normalize_product_record( $runtime_product, $manual_index_item, $manual_product_raw ) {
		$product_raw        = ! empty( $manual_product_raw['product'] ) && is_array( $manual_product_raw['product'] ) ? $manual_product_raw['product'] : array();
		$profile_raw        = ! empty( $product_raw['profile'] ) && is_array( $product_raw['profile'] ) ? $product_raw['profile'] : array();
		$identity_raw       = ! empty( $profile_raw['identity'] ) && is_array( $profile_raw['identity'] ) ? $profile_raw['identity'] : array();
		$commercial_raw     = ! empty( $profile_raw['commercial'] ) && is_array( $profile_raw['commercial'] ) ? $profile_raw['commercial'] : array();
		$positioning_raw    = ! empty( $profile_raw['positioning'] ) && is_array( $profile_raw['positioning'] ) ? $profile_raw['positioning'] : array();
		$slug               = ! empty( $runtime_product['slug'] ) ? sanitize_title( $runtime_product['slug'] ) : '';
		$title              = self::normalize_text( self::coalesce( array(
			! empty( $runtime_product['title'] ) ? $runtime_product['title'] : '',
			! empty( $manual_index_item['display_name'] ) ? $manual_index_item['display_name'] : '',
			! empty( $product_raw['display_name'] ) ? $product_raw['display_name'] : '',
		) ) );
		$short_description  = self::normalize_text( self::coalesce( array(
			! empty( $runtime_product['short_description'] ) ? $runtime_product['short_description'] : '',
			! empty( $commercial_raw['short_description'] ) ? $commercial_raw['short_description'] : '',
			! empty( $manual_index_item['short_description'] ) ? $manual_index_item['short_description'] : '',
		) ) );
		$product_type       = self::normalize_text( self::coalesce( array(
			! empty( $identity_raw['product_type'] ) ? $identity_raw['product_type'] : '',
			self::extract_runtime_feature_value( $runtime_product, 'Tipo' ),
		) ) );
		$key_value          = self::normalize_text( ! empty( $commercial_raw['key_value_proposition'] ) ? $commercial_raw['key_value_proposition'] : '' );
		$product_intent     = self::normalize_text( self::coalesce( array(
			! empty( $manual_index_item['product_intent'] ) ? $manual_index_item['product_intent'] : '',
			! empty( $positioning_raw['summary'] ) ? $positioning_raw['summary'] : '',
		) ) );
		$commercial_positioning = self::normalize_text( self::coalesce( array(
			! empty( $manual_index_item['commercial_positioning'] ) ? $manual_index_item['commercial_positioning'] : '',
			! empty( $commercial_raw['commercial_positioning'] ) ? $commercial_raw['commercial_positioning'] : '',
		) ) );
		$target_environment = ! empty( $manual_index_item['target_environment'] ) && is_array( $manual_index_item['target_environment'] ) ? $manual_index_item['target_environment'] : array();
		$seo_keywords       = ! empty( $manual_index_item['seo_keywords'] ) && is_array( $manual_index_item['seo_keywords'] ) ? $manual_index_item['seo_keywords'] : array();
		$value_bullets      = ! empty( $commercial_raw['value_bullets'] ) && is_array( $commercial_raw['value_bullets'] ) ? $commercial_raw['value_bullets'] : array();
		$features           = ! empty( $runtime_product['features'] ) && is_array( $runtime_product['features'] ) ? $runtime_product['features'] : array();

		return array(
			'slug'                  => $slug,
			'title'                 => $title,
			'sku'                   => self::normalize_text( ! empty( $runtime_product['sku'] ) ? $runtime_product['sku'] : '' ),
			'short_description'     => $short_description,
			'badge'                 => self::normalize_text( ! empty( $runtime_product['badge'] ) ? $runtime_product['badge'] : '' ),
			'product_type'          => $product_type,
			'key_value_proposition' => $key_value,
			'product_intent'        => $product_intent,
			'commercial_positioning'=> $commercial_positioning,
			'target_environment'    => array_values( array_filter( array_map( array( __CLASS__, 'normalize_text' ), $target_environment ) ) ),
			'seo_keywords'          => self::normalize_keywords( $seo_keywords ),
			'value_bullets'         => array_values( array_filter( array_map( array( __CLASS__, 'normalize_text' ), $value_bullets ) ) ),
			'features'              => $features,
			'images'                => ! empty( $runtime_product['images'] ) && is_array( $runtime_product['images'] ) ? $runtime_product['images'] : array(),
			'gallery'               => ! empty( $runtime_product['gallery'] ) && is_array( $runtime_product['gallery'] ) ? $runtime_product['gallery'] : array(),
			'hero_image'            => ! empty( $manual_index_item['hero_image'] ) ? ltrim( $manual_index_item['hero_image'], '/' ) : '',
		);
	}

	private static function get_source_paths() {
		$theme_dir = trailingslashit( WP_CONTENT_DIR ) . 'themes/beslock-custom';

		return array(
			'products.json'          => $theme_dir . '/data/products.json',
			'manuals/index.json'     => $theme_dir . '/assets/manuals/index.json',
			'manuals/products/'      => $theme_dir . '/assets/manuals/products',
			'woocommerce CSV'        => $theme_dir . '/data/woocommerce-pricing-import.csv',
		);
	}

	private static function compute_source_hash() {
		$paths = self::get_source_paths();
		$hash_input = array();

		foreach ( $paths as $path ) {
			if ( is_dir( $path ) ) {
				$files = glob( trailingslashit( $path ) . '*.json' );
				if ( is_array( $files ) ) {
					foreach ( $files as $file ) {
						$hash_input[] = $file . '|' . @filemtime( $file ) . '|' . @filesize( $file );
					}
				}
				continue;
			}

			if ( file_exists( $path ) ) {
				$hash_input[] = $path . '|' . @filemtime( $path ) . '|' . @filesize( $path );
			}
		}

		return ! empty( $hash_input ) ? md5( implode( "\n", $hash_input ) ) : '';
	}

	private static function read_json_file( $path ) {
		if ( ! file_exists( $path ) || ! is_readable( $path ) ) {
			return array();
		}

		$raw = file_get_contents( $path );
		if ( false === $raw || '' === trim( $raw ) ) {
			return array();
		}

		$decoded = json_decode( $raw, true );

		return is_array( $decoded ) ? $decoded : array();
	}

	private static function extract_available_cities( $csv_path ) {
		$default = array( 'Bogotá', 'Medellín', 'Cali', 'Barranquilla' );

		if ( ! file_exists( $csv_path ) || ! is_readable( $csv_path ) ) {
			return $default;
		}

		$handle = fopen( $csv_path, 'r' );
		if ( ! $handle ) {
			return $default;
		}

		$header = fgetcsv( $handle );
		if ( ! is_array( $header ) ) {
			fclose( $handle );
			return $default;
		}

		$header = array_map( 'trim', $header );
		$city_index = array_search( 'available_cities', $header, true );
		$cities = array();

		if ( false !== $city_index ) {
			while ( false !== ( $row = fgetcsv( $handle ) ) ) {
				if ( empty( $row[ $city_index ] ) ) {
					continue;
				}

				$row_cities = explode( '|', (string) $row[ $city_index ] );
				foreach ( $row_cities as $city ) {
					$city = self::normalize_text( $city );
					if ( $city ) {
						$cities[ mb_strtolower( $city ) ] = $city;
					}
				}
			}
		}

		fclose( $handle );

		return ! empty( $cities ) ? array_values( $cities ) : $default;
	}

	private static function get_available_cities( $catalog = null ) {
		if ( is_array( $catalog ) && ! empty( $catalog['available_cities'] ) ) {
			return $catalog['available_cities'];
		}

		$catalog = self::load_catalog();

		return ! empty( $catalog['available_cities'] ) ? $catalog['available_cities'] : array( 'Bogotá', 'Medellín', 'Cali', 'Barranquilla' );
	}

	private static function find_product_post_id( $slug, $sku = '' ) {
		$product = get_page_by_path( $slug, OBJECT, 'product' );

		if ( $product && ! empty( $product->ID ) ) {
			return intval( $product->ID );
		}

		if ( $sku ) {
			$matched = get_posts(
				array(
					'post_type'      => 'product',
					'post_status'    => array( 'publish', 'private', 'draft' ),
					'posts_per_page' => 1,
					'meta_key'       => '_sku',
					'meta_value'     => $sku,
					'fields'         => 'ids',
				)
			);

			if ( ! empty( $matched[0] ) ) {
				return intval( $matched[0] );
			}
		}

		return 0;
	}

	private static function build_product_meta( $product_record, $post_id, $catalog ) {
		$image_context = self::resolve_product_image_context( $post_id, $product_record );
		$title_context = self::normalize_text( $product_record['product_type'] );
		$environment   = self::format_environment_list( ! empty( $product_record['target_environment'] ) ? $product_record['target_environment'] : array(), 2 );
		$title_parts   = array( $product_record['title'] );

		if ( $title_context ) {
			$title_parts[] = $title_context . ( $environment ? ' para ' . $environment : '' );
		} elseif ( $environment ) {
			$title_parts[] = 'Cerradura inteligente para ' . $environment;
		}

		$title_parts[] = 'BESLOCK';
		$title_candidate  = implode( ' | ', array_filter( $title_parts ) );
		if ( $environment && mb_strlen( $title_candidate ) > 68 ) {
			$title_candidate = implode(
				' | ',
				array_filter(
					array(
						$product_record['title'],
						$title_context ? $title_context : 'Cerradura inteligente',
						'BESLOCK',
					)
				)
			);
		}

		$meta_title       = self::trim_text( $title_candidate, 68 );
		$description_seed = self::coalesce(
			array(
				! empty( $product_record['short_description'] ) ? $product_record['short_description'] : '',
				! empty( $product_record['key_value_proposition'] ) ? $product_record['key_value_proposition'] : '',
				! empty( $product_record['product_intent'] ) ? $product_record['product_intent'] : '',
			)
		);
		$description      = self::normalize_text( $product_record['title'] . ' de BESLOCK. ' . $description_seed );
		$city_suffix      = ' Disponible en Colombia.';
		$full_city_suffix = ' Disponible en Colombia con instalación en ' . self::format_cities( self::get_available_cities( $catalog ) ) . '.';

		if ( mb_strlen( $description . $full_city_suffix ) <= 158 ) {
			$description .= $full_city_suffix;
		} else {
			$description .= $city_suffix;
		}

		$description = self::trim_text( $description, 158 );

		$payload = array(
			'slug'               => $product_record['slug'],
			'title'              => $product_record['title'],
			'sku'                => $product_record['sku'],
			'product_type'       => $product_record['product_type'],
			'short_description'  => $product_record['short_description'],
			'key_value_proposition' => $product_record['key_value_proposition'],
			'target_environment' => ! empty( $product_record['target_environment'] ) ? $product_record['target_environment'] : array(),
			'seo_keywords'       => ! empty( $product_record['seo_keywords'] ) ? $product_record['seo_keywords'] : array(),
			'features'           => ! empty( $product_record['features'] ) ? $product_record['features'] : array(),
		);

		return array(
			'title'               => $meta_title,
			'description'         => $description,
			'og_title'            => $meta_title,
			'og_description'      => $description,
			'twitter_title'       => $meta_title,
			'twitter_description' => $description,
			'image'               => $image_context,
			'focus_keywords'      => self::build_focus_keywords( $product_record ),
			'payload'             => $payload,
			'force_noindex'       => self::is_hidden_product( $post_id ),
		);
	}

	private static function build_focus_keywords( $product_record ) {
		$keywords = array();

		if ( ! empty( $product_record['title'] ) ) {
			$keywords[] = $product_record['title'];
		}
		if ( ! empty( $product_record['sku'] ) ) {
			$keywords[] = $product_record['sku'];
		}
		if ( ! empty( $product_record['seo_keywords'] ) && is_array( $product_record['seo_keywords'] ) ) {
			$keywords = array_merge( $keywords, $product_record['seo_keywords'] );
		}

		$normalized = array();
		foreach ( $keywords as $keyword ) {
			$keyword = self::normalize_text( $keyword );
			if ( ! $keyword ) {
				continue;
			}
			$normalized[ mb_strtolower( $keyword ) ] = $keyword;
		}

		return implode( ', ', array_slice( array_values( $normalized ), 0, 8 ) );
	}

	private static function sync_core_pages( $catalog ) {
		$count = 0;

		$front_page_id = intval( get_option( 'page_on_front' ) );
		if ( $front_page_id > 0 ) {
			$image_context = self::resolve_post_image_context( $front_page_id );
			$meta = array(
				'title'               => 'Cerraduras inteligentes en Colombia | BESLOCK',
				'description'         => 'Descubre cerraduras inteligentes BESLOCK en Colombia. Soluciones de acceso digital para hogar, oficinas y alquileres con instalación y soporte.',
				'og_title'            => 'Cerraduras inteligentes en Colombia | BESLOCK',
				'og_description'      => 'Descubre cerraduras inteligentes BESLOCK en Colombia. Soluciones de acceso digital para hogar, oficinas y alquileres con instalación y soporte.',
				'twitter_title'       => 'Cerraduras inteligentes en Colombia | BESLOCK',
				'twitter_description' => 'Descubre cerraduras inteligentes BESLOCK en Colombia. Soluciones de acceso digital para hogar, oficinas y alquileres con instalación y soporte.',
				'image'               => $image_context,
				'focus_keywords'      => 'cerraduras inteligentes, cerraduras inteligentes en Colombia, BESLOCK',
				'payload'             => array( 'context' => 'home' ),
				'force_noindex'       => false,
			);
			self::update_post_seo_payload( $front_page_id, $meta );
			self::sync_post_to_siteseo( $front_page_id, $meta );
			$count++;
		}

		$shop_page_id = self::get_wc_page_id( 'shop' );
		if ( $shop_page_id > 0 ) {
			$image_context = self::resolve_post_image_context( $shop_page_id );
			$meta = array(
				'title'               => 'Tienda de cerraduras inteligentes | BESLOCK Colombia',
				'description'         => 'Explora la tienda BESLOCK y encuentra cerraduras inteligentes para puertas principales, oficinas, Airbnb y proyectos residenciales en Colombia.',
				'og_title'            => 'Tienda de cerraduras inteligentes | BESLOCK Colombia',
				'og_description'      => 'Explora la tienda BESLOCK y encuentra cerraduras inteligentes para puertas principales, oficinas, Airbnb y proyectos residenciales en Colombia.',
				'twitter_title'       => 'Tienda de cerraduras inteligentes | BESLOCK Colombia',
				'twitter_description' => 'Explora la tienda BESLOCK y encuentra cerraduras inteligentes para puertas principales, oficinas, Airbnb y proyectos residenciales en Colombia.',
				'image'               => $image_context,
				'focus_keywords'      => 'tienda de cerraduras inteligentes, cerraduras inteligentes Colombia, BESLOCK tienda',
				'payload'             => array( 'context' => 'shop' ),
				'force_noindex'       => false,
			);
			self::update_post_seo_payload( $shop_page_id, $meta );
			self::sync_post_to_siteseo( $shop_page_id, $meta );
			$count++;
		}

		$noindex_page_keys = array( 'cart', 'checkout', 'myaccount' );
		foreach ( $noindex_page_keys as $page_key ) {
			$page_id = self::get_wc_page_id( $page_key );
			if ( $page_id > 0 ) {
				update_post_meta( $page_id, self::META_FORCE_NOINDEX, '1' );
				update_post_meta( $page_id, '_siteseo_robots_index', '1' );
				$count++;
			}
		}

		return $count;
	}

	private static function sync_low_value_posts() {
		$count = 0;
		$targets = array(
			'post' => array( 'hello-world', 'test-post' ),
			'page' => array( 'sample-page' ),
		);

		foreach ( $targets as $post_type => $slugs ) {
			foreach ( $slugs as $slug ) {
				$post = get_page_by_path( $slug, OBJECT, $post_type );
				if ( ! $post || empty( $post->ID ) ) {
					continue;
				}
				update_post_meta( $post->ID, self::META_FORCE_NOINDEX, '1' );
				update_post_meta( $post->ID, '_siteseo_robots_index', '1' );
				$count++;
			}
		}

		return $count;
	}

	private static function sync_product_terms( $catalog ) {
		$count = 0;

		$product_categories = get_terms(
			array(
				'taxonomy'   => 'product_cat',
				'hide_empty' => false,
			)
		);

		if ( ! is_wp_error( $product_categories ) ) {
			foreach ( $product_categories as $term ) {
				$meta = self::build_term_meta( $term, $catalog );
				self::update_term_seo_payload( $term->term_id, $meta );
				self::sync_term_to_siteseo( $term->term_id, $meta );
				$count++;
			}
		}

		$product_tags = get_terms(
			array(
				'taxonomy'   => 'product_tag',
				'hide_empty' => false,
			)
		);

		if ( ! is_wp_error( $product_tags ) ) {
			foreach ( $product_tags as $term ) {
				$meta = array(
					'title'               => self::trim_text( $term->name . ' | BESLOCK', 68 ),
					'description'         => self::trim_text( 'Etiqueta de producto BESLOCK: ' . $term->name . '.', 158 ),
					'og_title'            => self::trim_text( $term->name . ' | BESLOCK', 68 ),
					'og_description'      => self::trim_text( 'Etiqueta de producto BESLOCK: ' . $term->name . '.', 158 ),
					'twitter_title'       => self::trim_text( $term->name . ' | BESLOCK', 68 ),
					'twitter_description' => self::trim_text( 'Etiqueta de producto BESLOCK: ' . $term->name . '.', 158 ),
					'image'               => self::resolve_term_image_context( $term->term_id ),
					'force_noindex'       => true,
				);
				self::update_term_seo_payload( $term->term_id, $meta );
				self::sync_term_to_siteseo( $term->term_id, $meta );
				$count++;
			}
		}

		return $count;
	}

	private static function build_term_meta( $term, $catalog ) {
		$linked_products = self::get_linked_term_products( $term->term_id );
		$environments    = array();

		foreach ( $linked_products as $product_post_id ) {
			$product_payload = get_post_meta( $product_post_id, self::META_PAYLOAD, true );
			if ( ! empty( $product_payload['target_environment'] ) && is_array( $product_payload['target_environment'] ) ) {
				$environments = array_merge( $environments, $product_payload['target_environment'] );
			}
		}

		$environments = array_values( array_unique( array_filter( array_map( array( __CLASS__, 'normalize_text' ), $environments ) ) ) );
		$environment  = self::format_environment_list( $environments, 2 );
		$title        = self::trim_text( $term->name . ' | Cerraduras inteligentes BESLOCK', 68 );
		$description  = 'Explora ' . self::normalize_text( $term->name ) . ' de BESLOCK';
		$description .= $environment ? ' para ' . $environment : ' para hogar, oficinas y rentas';
		$description .= ' en Colombia. Modelos con huella, clave, tarjeta y app según referencia.';
		$description  = self::trim_text( $description, 158 );
		$noindex      = self::should_noindex_term( $term );

		return array(
			'title'               => $title,
			'description'         => $description,
			'og_title'            => $title,
			'og_description'      => $description,
			'twitter_title'       => $title,
			'twitter_description' => $description,
			'image'               => self::resolve_term_image_context( $term->term_id ),
			'force_noindex'       => $noindex,
		);
	}

	private static function should_noindex_term( $term ) {
		if ( ! $term || empty( $term->taxonomy ) ) {
			return false;
		}

		if ( 'product_tag' === $term->taxonomy ) {
			return true;
		}

		$slug = sanitize_title( $term->slug );

		if ( in_array( $slug, array( 'sin-categorizar', 'uncategorized' ), true ) ) {
			return true;
		}

		return false;
	}

	private static function get_linked_term_products( $term_id ) {
		$products = get_posts(
			array(
				'post_type'      => 'product',
				'post_status'    => 'publish',
				'posts_per_page' => 8,
				'fields'         => 'ids',
				'tax_query'      => array(
					array(
						'taxonomy' => 'product_cat',
						'field'    => 'term_id',
						'terms'    => array( intval( $term_id ) ),
					),
				),
			)
		);

		return is_array( $products ) ? $products : array();
	}

	private static function update_post_seo_payload( $post_id, $meta ) {
		update_post_meta( $post_id, self::META_TITLE, $meta['title'] );
		update_post_meta( $post_id, self::META_DESCRIPTION, $meta['description'] );
		update_post_meta( $post_id, self::META_OG_TITLE, $meta['og_title'] );
		update_post_meta( $post_id, self::META_OG_DESCRIPTION, $meta['og_description'] );
		update_post_meta( $post_id, self::META_TWITTER_TITLE, $meta['twitter_title'] );
		update_post_meta( $post_id, self::META_TWITTER_DESCRIPTION, $meta['twitter_description'] );
		update_post_meta( $post_id, self::META_FOCUS_KEYWORDS, $meta['focus_keywords'] );
		update_post_meta( $post_id, self::META_PAYLOAD, $meta['payload'] );
		update_post_meta( $post_id, self::META_FORCE_NOINDEX, ! empty( $meta['force_noindex'] ) ? '1' : '' );

		if ( ! empty( $meta['image']['url'] ) ) {
			update_post_meta( $post_id, self::META_IMAGE_URL, esc_url_raw( $meta['image']['url'] ) );
		}

		if ( ! empty( $meta['image']['alt'] ) ) {
			update_post_meta( $post_id, self::META_IMAGE_ALT, $meta['image']['alt'] );
		}
	}

	private static function update_term_seo_payload( $term_id, $meta ) {
		update_term_meta( $term_id, self::TERM_META_TITLE, $meta['title'] );
		update_term_meta( $term_id, self::TERM_META_DESCRIPTION, $meta['description'] );
		update_term_meta( $term_id, self::TERM_META_FORCE_NOINDEX, ! empty( $meta['force_noindex'] ) ? '1' : '' );
	}

	private static function sync_post_to_siteseo( $post_id, $meta ) {
		update_post_meta( $post_id, '_siteseo_titles_title', $meta['title'] );
		update_post_meta( $post_id, '_siteseo_titles_desc', $meta['description'] );
		update_post_meta( $post_id, '_siteseo_social_fb_title', $meta['og_title'] );
		update_post_meta( $post_id, '_siteseo_social_fb_desc', $meta['og_description'] );
		update_post_meta( $post_id, '_siteseo_social_twitter_title', $meta['twitter_title'] );
		update_post_meta( $post_id, '_siteseo_social_twitter_desc', $meta['twitter_description'] );
		update_post_meta( $post_id, '_siteseo_analysis_target_kw', $meta['focus_keywords'] );

		if ( ! empty( $meta['force_noindex'] ) ) {
			update_post_meta( $post_id, '_siteseo_robots_index', '1' );
		} else {
			delete_post_meta( $post_id, '_siteseo_robots_index' );
		}

		self::sync_post_social_image_to_siteseo( $post_id, $meta );
	}

	private static function sync_term_to_siteseo( $term_id, $meta ) {
		update_term_meta( $term_id, '_siteseo_titles_title', $meta['title'] );
		update_term_meta( $term_id, '_siteseo_titles_desc', $meta['description'] );
		update_term_meta( $term_id, '_siteseo_social_fb_title', $meta['og_title'] );
		update_term_meta( $term_id, '_siteseo_social_fb_desc', $meta['og_description'] );
		update_term_meta( $term_id, '_siteseo_social_twitter_title', $meta['twitter_title'] );
		update_term_meta( $term_id, '_siteseo_social_twitter_desc', $meta['twitter_description'] );

		if ( ! empty( $meta['force_noindex'] ) ) {
			update_term_meta( $term_id, '_siteseo_robots_index', '1' );
		} else {
			delete_term_meta( $term_id, '_siteseo_robots_index' );
		}

		self::sync_term_social_image_to_siteseo( $term_id, $meta );
	}

	private static function sync_post_social_image_to_siteseo( $post_id, $meta ) {
		if ( empty( $meta['image']['url'] ) ) {
			return;
		}

		update_post_meta( $post_id, '_siteseo_social_fb_img', esc_url_raw( $meta['image']['url'] ) );
		update_post_meta( $post_id, '_siteseo_social_twitter_img', esc_url_raw( $meta['image']['url'] ) );

		if ( ! empty( $meta['image']['attachment_id'] ) ) {
			update_post_meta( $post_id, '_siteseo_social_fb_img_attachment_id', intval( $meta['image']['attachment_id'] ) );
			update_post_meta( $post_id, '_siteseo_social_twitter_img_attachment_id', intval( $meta['image']['attachment_id'] ) );
		}

		if ( ! empty( $meta['image']['width'] ) ) {
			update_post_meta( $post_id, '_siteseo_social_fb_img_width', intval( $meta['image']['width'] ) );
			update_post_meta( $post_id, '_siteseo_social_twitter_img_width', intval( $meta['image']['width'] ) );
		}

		if ( ! empty( $meta['image']['height'] ) ) {
			update_post_meta( $post_id, '_siteseo_social_fb_img_height', intval( $meta['image']['height'] ) );
			update_post_meta( $post_id, '_siteseo_social_twitter_img_height', intval( $meta['image']['height'] ) );
		}
	}

	private static function sync_term_social_image_to_siteseo( $term_id, $meta ) {
		if ( empty( $meta['image']['url'] ) ) {
			return;
		}

		update_term_meta( $term_id, '_siteseo_social_fb_img', esc_url_raw( $meta['image']['url'] ) );
		update_term_meta( $term_id, '_siteseo_social_twitter_img', esc_url_raw( $meta['image']['url'] ) );

		if ( ! empty( $meta['image']['attachment_id'] ) ) {
			update_term_meta( $term_id, '_siteseo_social_fb_img_attachment_id', intval( $meta['image']['attachment_id'] ) );
			update_term_meta( $term_id, '_siteseo_social_twitter_img_attachment_id', intval( $meta['image']['attachment_id'] ) );
		}

		if ( ! empty( $meta['image']['width'] ) ) {
			update_term_meta( $term_id, '_siteseo_social_fb_img_width', intval( $meta['image']['width'] ) );
			update_term_meta( $term_id, '_siteseo_social_twitter_img_width', intval( $meta['image']['width'] ) );
		}

		if ( ! empty( $meta['image']['height'] ) ) {
			update_term_meta( $term_id, '_siteseo_social_fb_img_height', intval( $meta['image']['height'] ) );
			update_term_meta( $term_id, '_siteseo_social_twitter_img_height', intval( $meta['image']['height'] ) );
		}
	}

	private static function sync_siteseo_global_options( $catalog ) {
		$count           = 0;
		$default_image   = self::resolve_site_default_image_context();
		$toggles         = get_option( 'siteseo_toggle', array() );
		$titles_options  = get_option( 'siteseo_titles_option_name', array() );
		$social_options  = get_option( 'siteseo_social_option_name', array() );
		$sitemap_options = get_option( 'siteseo_xml_sitemap_option_name', array() );
		$advanced_options = get_option( 'siteseo_advanced_option_name', array() );

		$toggles['toggle-titles']          = true;
		$toggles['toggle-social']          = true;
		$toggles['toggle-xml-sitemap']     = true;
		$toggles['toggle-advanced']        = true;
		$toggles['toggle-instant-indexing']= true;

		$titles_options['titles_sep']                           = '|';
		$titles_options['titles_archives_author_noindex']       = true;
		$titles_options['titles_archives_date_noindex']         = true;
		$titles_options['titles_archives_search_title_noindex'] = true;
		$titles_options['titles_paged_noindex']                 = true;
		$titles_options['titles_attachments_noindex']           = true;
		$titles_options['titles_nositelinkssearchbox']          = false;
		$titles_options['titles_tax_titles']['product_tag']['noindex'] = true;
		$titles_options['titles_tax_titles']['post_tag']['noindex']    = true;

		$social_options['social_facebook_og']            = true;
		$social_options['social_twitter_card']           = true;
		$social_options['social_twitter_card_img_size']  = 'Large';
		$social_options['social_knowledge_type']         = 'Organization';
		$social_options['social_knowledge_name']         = self::get_site_name();
		$social_options['social_knowledge_contact_type'] = 'Customer support';
		$social_options['social_accounts_additional']    = array();

		if ( ! empty( $default_image['url'] ) ) {
			$social_options['social_knowledge_img']  = esc_url_raw( $default_image['url'] );
			$social_options['social_twitter_card_img'] = esc_url_raw( $default_image['url'] );
		}

		$sitemap_options['xml_sitemap_general_enable']                   = true;
		$sitemap_options['xml_sitemap_img_enable']                       = true;
		$sitemap_options['xml_sitemap_author_enable']                    = false;
		$sitemap_options['xml_sitemap_post_types_list']['post']['include']    = true;
		$sitemap_options['xml_sitemap_post_types_list']['page']['include']    = true;
		$sitemap_options['xml_sitemap_post_types_list']['product']['include'] = true;
		$sitemap_options['xml_sitemap_taxonomies_list']['category']['include']    = true;
		$sitemap_options['xml_sitemap_taxonomies_list']['product_cat']['include'] = true;
		$sitemap_options['xml_sitemap_taxonomies_list']['product_tag']['include'] = false;

		$advanced_options['advanced_attachments']        = true;
		$advanced_options['appearance_universal_metabox'] = true;

		update_option( 'siteseo_toggle', $toggles, false );
		update_option( 'siteseo_titles_option_name', $titles_options, false );
		update_option( 'siteseo_social_option_name', $social_options, false );
		update_option( 'siteseo_xml_sitemap_option_name', $sitemap_options, false );
		update_option( 'siteseo_advanced_option_name', $advanced_options, false );
		$count++;

		return $count;
	}

	private static function sync_product_attachment_alts( $post_id, $product_record ) {
		$updated = 0;
		$attachment_ids = array();
		$thumbnail_id   = intval( get_post_thumbnail_id( $post_id ) );
		$gallery_raw    = (string) get_post_meta( $post_id, '_product_image_gallery', true );

		if ( $thumbnail_id > 0 ) {
			$attachment_ids[] = $thumbnail_id;
		}

		if ( $gallery_raw ) {
			$attachment_ids = array_merge( $attachment_ids, array_map( 'intval', explode( ',', $gallery_raw ) ) );
		}

		$attachment_ids = array_values( array_unique( array_filter( $attachment_ids ) ) );

		foreach ( $attachment_ids as $index => $attachment_id ) {
			$current_alt = (string) get_post_meta( $attachment_id, '_wp_attachment_image_alt', true );
			if ( ! self::should_replace_attachment_alt( $current_alt, $attachment_id, $product_record ) ) {
				continue;
			}

			$new_alt = self::build_attachment_alt( $product_record, $index );
			if ( ! $new_alt ) {
				continue;
			}

			update_post_meta( $attachment_id, '_wp_attachment_image_alt', $new_alt );
			$updated++;
		}

		return $updated;
	}

	private static function should_replace_attachment_alt( $current_alt, $attachment_id, $product_record ) {
		$current_alt = self::normalize_text( $current_alt );

		if ( '' === $current_alt ) {
			return true;
		}

		$attachment_title = self::normalize_text( get_the_title( $attachment_id ) );
		$current_slug     = sanitize_title( $current_alt );
		$title_slug       = sanitize_title( $attachment_title );
		$product_slug     = ! empty( $product_record['slug'] ) ? sanitize_title( $product_record['slug'] ) : '';

		if ( $current_slug && $current_slug === $title_slug ) {
			return true;
		}

		if ( $product_slug && 0 === strpos( $current_slug, $product_slug ) ) {
			return true;
		}

		if ( preg_match( '/^featured-\d+$/', $current_slug ) ) {
			return true;
		}

		return false;
	}

	private static function build_attachment_alt( $product_record, $index ) {
		$title        = ! empty( $product_record['title'] ) ? $product_record['title'] : '';
		$product_type = ! empty( $product_record['product_type'] ) ? mb_strtolower( self::normalize_text( $product_record['product_type'] ) ) : 'cerradura inteligente';

		if ( 0 === intval( $index ) ) {
			return trim( $title . ' de BESLOCK, ' . $product_type );
		}

		return trim( $title . ' de BESLOCK, imagen del producto ' . ( intval( $index ) + 1 ) );
	}

	private static function resolve_product_image_context( $post_id, $product_record ) {
		$image_context = self::resolve_post_image_context( $post_id );

		if ( ! empty( $image_context['url'] ) ) {
			return $image_context;
		}

		if ( ! empty( $product_record['hero_image'] ) ) {
			$manual_url = content_url( '/themes/beslock-custom/assets/manuals/' . ltrim( $product_record['hero_image'], '/' ) );
			$manual_path = trailingslashit( WP_CONTENT_DIR ) . 'themes/beslock-custom/assets/manuals/' . ltrim( $product_record['hero_image'], '/' );

			if ( file_exists( $manual_path ) ) {
				return array(
					'url'           => $manual_url,
					'alt'           => ! empty( $product_record['title'] ) ? $product_record['title'] . ' de BESLOCK' : self::get_site_name(),
					'attachment_id' => 0,
					'width'         => 0,
					'height'        => 0,
				);
			}
		}

		return self::resolve_site_default_image_context();
	}

	private static function resolve_post_image_context( $post_id, $fallback_to_site_default = true ) {
		$attachment_id = intval( get_post_thumbnail_id( $post_id ) );

		if ( $attachment_id > 0 ) {
			return self::build_attachment_context( $attachment_id );
		}

		return $fallback_to_site_default ? self::resolve_site_default_image_context() : array();
	}

	private static function resolve_term_image_context( $term_id ) {
		$products = self::get_linked_term_products( $term_id );

		if ( ! empty( $products[0] ) ) {
			return self::resolve_post_image_context( intval( $products[0] ) );
		}

		return self::resolve_site_default_image_context();
	}

	private static function resolve_site_default_image_context() {
		$logo_id = intval( get_theme_mod( 'custom_logo' ) );
		if ( $logo_id > 0 ) {
			return self::build_attachment_context( $logo_id );
		}

		$site_icon_id = intval( get_option( 'site_icon' ) );
		if ( $site_icon_id > 0 ) {
			return self::build_attachment_context( $site_icon_id );
		}

		$products = get_posts(
			array(
				'post_type'      => 'product',
				'post_status'    => 'publish',
				'posts_per_page' => 1,
				'fields'         => 'ids',
				'orderby'        => 'ID',
				'order'          => 'ASC',
			)
		);

		if ( ! empty( $products[0] ) ) {
			$product_image = self::resolve_post_image_context( intval( $products[0] ), false );
			if ( ! empty( $product_image['url'] ) ) {
				return $product_image;
			}
		}

		$site_icon_url = get_site_icon_url( 512 );
		if ( $site_icon_url ) {
			return array(
				'url'           => $site_icon_url,
				'alt'           => self::get_site_name(),
				'attachment_id' => 0,
				'width'         => 512,
				'height'        => 512,
			);
		}

		return array();
	}

	private static function build_attachment_context( $attachment_id ) {
		$url = wp_get_attachment_image_url( $attachment_id, 'full' );
		if ( ! $url ) {
			return array();
		}

		$meta = wp_get_attachment_metadata( $attachment_id );

		return array(
			'url'           => $url,
			'alt'           => self::normalize_text( get_post_meta( $attachment_id, '_wp_attachment_image_alt', true ) ),
			'attachment_id' => $attachment_id,
			'width'         => ! empty( $meta['width'] ) ? intval( $meta['width'] ) : 0,
			'height'        => ! empty( $meta['height'] ) ? intval( $meta['height'] ) : 0,
		);
	}

	public static function filter_document_title( $title ) {
		if ( self::is_external_seo_active() ) {
			return $title;
		}

		$meta = self::get_request_meta();

		return ! empty( $meta['title'] ) ? $meta['title'] : $title;
	}

	public static function output_meta_tags() {
		if ( self::is_external_seo_active() ) {
			return;
		}

		$meta = self::get_request_meta();
		if ( empty( $meta ) || ! is_array( $meta ) ) {
			return;
		}

		$resolved_title = ! empty( $meta['og_title'] ) ? $meta['og_title'] : ( ! empty( $meta['title'] ) ? $meta['title'] : wp_get_document_title() );

		if ( ! empty( $meta['description'] ) ) {
			echo '<meta name="description" content="' . esc_attr( $meta['description'] ) . '">' . "\n";
		}

		$og_type = ! empty( $meta['og_type'] ) ? $meta['og_type'] : ( is_front_page() ? 'website' : 'article' );

		echo '<meta property="og:locale" content="es_CO">' . "\n";
		echo '<meta property="og:site_name" content="' . esc_attr( self::get_site_name() ) . '">' . "\n";
		echo '<meta property="og:type" content="' . esc_attr( $og_type ) . '">' . "\n";
		echo '<meta property="og:title" content="' . esc_attr( $resolved_title ) . '">' . "\n";

		if ( ! empty( $meta['og_description'] ) ) {
			echo '<meta property="og:description" content="' . esc_attr( $meta['og_description'] ) . '">' . "\n";
		}

		echo '<meta property="og:url" content="' . esc_url( self::get_request_url() ) . '">' . "\n";

		if ( ! empty( $meta['image']['url'] ) ) {
			echo '<meta property="og:image" content="' . esc_url( $meta['image']['url'] ) . '">' . "\n";
			if ( ! empty( $meta['image']['alt'] ) ) {
				echo '<meta property="og:image:alt" content="' . esc_attr( $meta['image']['alt'] ) . '">' . "\n";
			}
			if ( ! empty( $meta['image']['width'] ) ) {
				echo '<meta property="og:image:width" content="' . intval( $meta['image']['width'] ) . '">' . "\n";
			}
			if ( ! empty( $meta['image']['height'] ) ) {
				echo '<meta property="og:image:height" content="' . intval( $meta['image']['height'] ) . '">' . "\n";
			}
		}

		echo '<meta name="twitter:card" content="' . esc_attr( ! empty( $meta['image']['url'] ) ? 'summary_large_image' : 'summary' ) . '">' . "\n";
		echo '<meta name="twitter:title" content="' . esc_attr( ! empty( $meta['twitter_title'] ) ? $meta['twitter_title'] : $resolved_title ) . '">' . "\n";

		if ( ! empty( $meta['twitter_description'] ) ) {
			echo '<meta name="twitter:description" content="' . esc_attr( $meta['twitter_description'] ) . '">' . "\n";
		}

		if ( ! empty( $meta['image']['url'] ) ) {
			echo '<meta name="twitter:image" content="' . esc_url( $meta['image']['url'] ) . '">' . "\n";
		}
	}

	public static function output_json_ld() {
		if ( self::is_other_external_seo_active() ) {
			return;
		}

		if ( self::should_noindex_current_request() ) {
			return;
		}

		$schema_graph = array();

		if ( is_front_page() ) {
			$schema_graph[] = self::build_organization_schema();
			$schema_graph[] = self::build_website_schema();
		}

		if ( function_exists( 'is_product' ) && is_product() ) {
			$product_schema = self::build_product_schema( get_queried_object_id() );
			if ( ! empty( $product_schema ) ) {
				$schema_graph[] = $product_schema;
			}
			$schema_graph[] = self::build_breadcrumb_schema();
		} elseif ( self::should_render_breadcrumb_schema() ) {
			$schema_graph[] = self::build_breadcrumb_schema();
		}

		$schema_graph = array_values( array_filter( $schema_graph ) );
		if ( empty( $schema_graph ) ) {
			return;
		}

		echo '<script type="application/ld+json">' . wp_json_encode(
			array(
				'@context' => 'https://schema.org',
				'@graph'   => $schema_graph,
			),
			JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
		) . '</script>' . "\n";
	}

	public static function maybe_disable_siteseo_organization_schema() {
		if ( ! self::is_siteseo_active() ) {
			return;
		}

		remove_action( 'wp_head', '\SiteSEO\SocialMetas::add_social_graph', 1 );
	}

	private static function should_render_breadcrumb_schema() {
		if ( is_front_page() ) {
			return false;
		}

		if ( function_exists( 'is_shop' ) && is_shop() ) {
			return true;
		}

		if ( is_tax( 'product_cat' ) || is_tax( 'product_tag' ) ) {
			return true;
		}

		if ( is_page() ) {
			return true;
		}

		return false;
	}

	private static function build_organization_schema() {
		$default_image = self::resolve_site_default_image_context();

		$schema = array(
			'@type' => 'Organization',
			'@id'   => trailingslashit( home_url( '/' ) ) . '#organization',
			'name'  => self::get_site_name(),
			'url'   => home_url( '/' ),
			'email' => 'ventas@beslock.com.co',
			'contactPoint' => array(
				array(
					'@type'             => 'ContactPoint',
					'contactType'       => 'sales',
					'email'             => 'ventas@beslock.com.co',
					'areaServed'        => 'CO',
					'availableLanguage' => array( 'es-CO', 'es' ),
				),
			),
		);

		if ( ! empty( $default_image['url'] ) ) {
			$schema['logo'] = $default_image['url'];
		}

		return $schema;
	}

	private static function build_website_schema() {
		return array(
			'@type'           => 'WebSite',
			'@id'             => trailingslashit( home_url( '/' ) ) . '#website',
			'url'             => home_url( '/' ),
			'name'            => self::get_site_name(),
			'inLanguage'      => 'es-CO',
			'potentialAction' => array(
				'@type'       => 'SearchAction',
				'target'      => home_url( '/?s={search_term_string}' ),
				'query-input' => 'required name=search_term_string',
			),
		);
	}

	private static function build_product_schema( $post_id ) {
		$post = get_post( $post_id );
		if ( ! $post ) {
			return array();
		}

		$payload    = get_post_meta( $post_id, self::META_PAYLOAD, true );
		$image_meta = self::get_request_meta();
		$product    = function_exists( 'wc_get_product' ) ? wc_get_product( $post_id ) : null;
		$image_urls = array();

		if ( ! empty( $image_meta['image']['url'] ) ) {
			$image_urls[] = $image_meta['image']['url'];
		}

		if ( $product && method_exists( $product, 'get_gallery_image_ids' ) ) {
			foreach ( $product->get_gallery_image_ids() as $attachment_id ) {
				$url = wp_get_attachment_image_url( $attachment_id, 'full' );
				if ( $url ) {
					$image_urls[] = $url;
				}
			}
		}

		$image_urls = array_values( array_unique( array_filter( $image_urls ) ) );

		$schema = array(
			'@type'       => 'Product',
			'@id'         => trailingslashit( get_permalink( $post_id ) ) . '#product',
			'name'        => get_the_title( $post_id ),
			'url'         => get_permalink( $post_id ),
			'description' => ! empty( $image_meta['description'] ) ? $image_meta['description'] : self::normalize_text( get_the_excerpt( $post_id ) ),
			'brand'       => array(
				'@type' => 'Brand',
				'name'  => self::get_site_name(),
			),
		);

		if ( ! empty( $payload['sku'] ) ) {
			$schema['sku'] = $payload['sku'];
		}

		if ( ! empty( $image_urls ) ) {
			$schema['image'] = $image_urls;
		}

		if ( ! empty( $payload['product_type'] ) ) {
			$schema['category'] = $payload['product_type'];
		}

		if ( ! empty( $payload['features'] ) && is_array( $payload['features'] ) ) {
			$properties = array();
			foreach ( $payload['features'] as $feature ) {
				if ( empty( $feature['label'] ) || empty( $feature['value'] ) ) {
					continue;
				}
				$properties[] = array(
					'@type' => 'PropertyValue',
					'name'  => self::normalize_text( $feature['label'] ),
					'value' => self::normalize_text( $feature['value'] ),
				);
			}
			if ( ! empty( $properties ) ) {
				$schema['additionalProperty'] = $properties;
			}
		}

		if ( $product ) {
			$offers = array(
				'@type'         => 'Offer',
				'url'           => get_permalink( $post_id ),
				'priceCurrency' => function_exists( 'get_woocommerce_currency' ) ? get_woocommerce_currency() : 'COP',
				'availability'  => self::schema_availability( $product ),
				'seller'        => array(
					'@type' => 'Organization',
					'name'  => self::get_site_name(),
				),
			);

			$price = method_exists( $product, 'get_price' ) ? $product->get_price() : '';
			if ( '' !== $price && null !== $price ) {
				$offers['price'] = self::normalize_price( $price );
			}

			$schema['offers'] = $offers;

			if ( method_exists( $product, 'get_review_count' ) && intval( $product->get_review_count() ) > 0 && method_exists( $product, 'get_average_rating' ) ) {
				$schema['aggregateRating'] = array(
					'@type'       => 'AggregateRating',
					'ratingValue' => (string) $product->get_average_rating(),
					'reviewCount' => intval( $product->get_review_count() ),
				);
			}
		}

		return $schema;
	}

	private static function build_breadcrumb_schema() {
		$items = array();
		$position = 1;

		$items[] = array(
			'@type'    => 'ListItem',
			'position' => $position++,
			'name'     => self::get_site_name(),
			'item'     => home_url( '/' ),
		);

		$shop_url = self::get_wc_page_url( 'shop' );
		$shop_id  = self::get_wc_page_id( 'shop' );
		$shop_name = $shop_id > 0 ? get_the_title( $shop_id ) : 'Tienda';

		if ( function_exists( 'is_shop' ) && is_shop() ) {
			$items[] = array(
				'@type'    => 'ListItem',
				'position' => $position++,
				'name'     => $shop_name,
				'item'     => $shop_url,
			);
		} elseif ( is_tax( 'product_cat' ) || is_tax( 'product_tag' ) || ( function_exists( 'is_product' ) && is_product() ) ) {
			$items[] = array(
				'@type'    => 'ListItem',
				'position' => $position++,
				'name'     => $shop_name,
				'item'     => $shop_url,
			);
		}

		if ( is_tax( 'product_cat' ) || is_tax( 'product_tag' ) ) {
			$term = get_queried_object();
			if ( $term && ! empty( $term->term_id ) ) {
				$ancestors = array_reverse( get_ancestors( $term->term_id, $term->taxonomy ) );
				foreach ( $ancestors as $ancestor_id ) {
					$ancestor = get_term( $ancestor_id, $term->taxonomy );
					if ( $ancestor && ! is_wp_error( $ancestor ) ) {
						$items[] = array(
							'@type'    => 'ListItem',
							'position' => $position++,
							'name'     => $ancestor->name,
							'item'     => get_term_link( $ancestor ),
						);
					}
				}
				$items[] = array(
					'@type'    => 'ListItem',
					'position' => $position++,
					'name'     => $term->name,
					'item'     => get_term_link( $term ),
				);
			}
		} elseif ( function_exists( 'is_product' ) && is_product() ) {
			$terms = get_the_terms( get_queried_object_id(), 'product_cat' );
			if ( is_array( $terms ) && ! empty( $terms ) ) {
				$primary_term = null;
				foreach ( $terms as $term ) {
					if ( 'sin-categorizar' !== sanitize_title( $term->slug ) ) {
						$primary_term = $term;
						break;
					}
				}
				if ( ! $primary_term ) {
					$primary_term = reset( $terms );
				}
				if ( $primary_term ) {
					$ancestors = array_reverse( get_ancestors( $primary_term->term_id, 'product_cat' ) );
					foreach ( $ancestors as $ancestor_id ) {
						$ancestor = get_term( $ancestor_id, 'product_cat' );
						if ( $ancestor && ! is_wp_error( $ancestor ) ) {
							$items[] = array(
								'@type'    => 'ListItem',
								'position' => $position++,
								'name'     => $ancestor->name,
								'item'     => get_term_link( $ancestor ),
							);
						}
					}
					$items[] = array(
						'@type'    => 'ListItem',
						'position' => $position++,
						'name'     => $primary_term->name,
						'item'     => get_term_link( $primary_term ),
					);
				}
			}

			$items[] = array(
				'@type'    => 'ListItem',
				'position' => $position++,
				'name'     => get_the_title( get_queried_object_id() ),
				'item'     => get_permalink( get_queried_object_id() ),
			);
		} elseif ( is_page() ) {
			$post_id = get_queried_object_id();
			$ancestors = array_reverse( get_post_ancestors( $post_id ) );
			foreach ( $ancestors as $ancestor_id ) {
				$items[] = array(
					'@type'    => 'ListItem',
					'position' => $position++,
					'name'     => get_the_title( $ancestor_id ),
					'item'     => get_permalink( $ancestor_id ),
				);
			}
			$items[] = array(
				'@type'    => 'ListItem',
				'position' => $position++,
				'name'     => get_the_title( $post_id ),
				'item'     => get_permalink( $post_id ),
			);
		}

		if ( count( $items ) < 2 ) {
			return array();
		}

		return array(
			'@type'           => 'BreadcrumbList',
			'@id'             => trailingslashit( self::get_request_url() ) . '#breadcrumb',
			'itemListElement' => $items,
		);
	}

	public static function filter_wp_robots( $robots ) {
		if ( ! is_array( $robots ) ) {
			$robots = array();
		}

		$robots['max-image-preview'] = 'large';

		if ( self::should_noindex_current_request() ) {
			unset( $robots['index'] );
			$robots['noindex'] = true;
			$robots['follow']  = true;
		}

		return $robots;
	}

	private static function should_noindex_current_request() {
		if ( is_search() || is_author() || is_date() || is_attachment() ) {
			return true;
		}

		if ( is_paged() && ! is_singular() ) {
			return true;
		}

		if ( function_exists( 'is_cart' ) && is_cart() ) {
			return true;
		}

		if ( function_exists( 'is_checkout' ) && is_checkout() ) {
			return true;
		}

		if ( function_exists( 'is_account_page' ) && is_account_page() ) {
			return true;
		}

		if ( is_tax( 'product_tag' ) ) {
			return true;
		}

		if ( is_tax( 'product_cat' ) ) {
			$term = get_queried_object();
			if ( $term && self::should_noindex_term( $term ) ) {
				return true;
			}
		}

		if ( is_singular() ) {
			$post_id = get_queried_object_id();
			if ( $post_id && self::should_noindex_post( $post_id ) ) {
				return true;
			}
		}

		return false;
	}

	private static function should_noindex_post( $post_id ) {
		if ( ! $post_id ) {
			return false;
		}

		if ( get_post_meta( $post_id, self::META_FORCE_NOINDEX, true ) ) {
			return true;
		}

		$post = get_post( $post_id );
		if ( ! $post ) {
			return false;
		}

		if ( in_array( sanitize_title( $post->post_name ), array( 'hello-world', 'test-post', 'sample-page' ), true ) ) {
			return true;
		}

		if ( 'product' === $post->post_type && self::is_hidden_product( $post_id ) ) {
			return true;
		}

		return false;
	}

	private static function is_hidden_product( $post_id ) {
		$post = get_post( $post_id );
		if ( ! $post || 'product' !== $post->post_type ) {
			return false;
		}

		if ( 0 === strpos( sanitize_title( $post->post_name ), 'instalacion-beslock-' ) ) {
			return true;
		}

		if ( function_exists( 'wc_get_product' ) ) {
			$product = wc_get_product( $post_id );
			if ( $product && method_exists( $product, 'get_catalog_visibility' ) ) {
				return 'hidden' === $product->get_catalog_visibility();
			}
		}

		return false;
	}

	public static function filter_sitemap_provider( $provider, $name ) {
		if ( 'users' === $name ) {
			return false;
		}

		return $provider;
	}

	public static function filter_sitemap_taxonomies( $taxonomies ) {
		if ( isset( $taxonomies['product_tag'] ) ) {
			unset( $taxonomies['product_tag'] );
		}

		return $taxonomies;
	}

	public static function filter_sitemap_taxonomies_query_args( $args, $taxonomy ) {
		$excluded_slugs = array();

		if ( 'product_cat' === $taxonomy ) {
			$excluded_slugs[] = 'sin-categorizar';
		}

		if ( 'category' === $taxonomy ) {
			$excluded_slugs[] = 'uncategorized';
		}

		if ( empty( $excluded_slugs ) ) {
			return $args;
		}

		$excluded_ids = array();
		foreach ( $excluded_slugs as $slug ) {
			$term = get_term_by( 'slug', $slug, $taxonomy );
			if ( $term && ! is_wp_error( $term ) ) {
				$excluded_ids[] = intval( $term->term_id );
			}
		}

		if ( empty( $excluded_ids ) ) {
			return $args;
		}

		if ( empty( $args['exclude'] ) || ! is_array( $args['exclude'] ) ) {
			$args['exclude'] = array();
		}

		$args['exclude'] = array_values( array_unique( array_merge( $args['exclude'], $excluded_ids ) ) );

		return $args;
	}

	public static function filter_sitemap_posts_query_args( $args, $post_type ) {
		$excluded_ids = self::get_sitemap_excluded_ids( $post_type );
		if ( empty( $excluded_ids ) ) {
			return $args;
		}

		if ( empty( $args['post__not_in'] ) || ! is_array( $args['post__not_in'] ) ) {
			$args['post__not_in'] = array();
		}

		$args['post__not_in'] = array_values( array_unique( array_merge( $args['post__not_in'], $excluded_ids ) ) );

		return $args;
	}

	private static function get_sitemap_excluded_ids( $post_type ) {
		if ( isset( self::$sitemap_excluded_ids[ $post_type ] ) ) {
			return self::$sitemap_excluded_ids[ $post_type ];
		}

		$excluded = array();

		if ( 'post' === $post_type ) {
			foreach ( array( 'hello-world', 'test-post' ) as $slug ) {
				$post = get_page_by_path( $slug, OBJECT, 'post' );
				if ( $post && ! empty( $post->ID ) ) {
					$excluded[] = intval( $post->ID );
				}
			}
		}

		if ( 'page' === $post_type ) {
			foreach ( array( 'sample-page' ) as $slug ) {
				$page = get_page_by_path( $slug, OBJECT, 'page' );
				if ( $page && ! empty( $page->ID ) ) {
					$excluded[] = intval( $page->ID );
				}
			}

			foreach ( array( 'cart', 'checkout', 'myaccount' ) as $key ) {
				$page_id = self::get_wc_page_id( $key );
				if ( $page_id > 0 ) {
					$excluded[] = $page_id;
				}
			}
		}

		if ( 'product' === $post_type ) {
			$product_ids = get_posts(
				array(
					'post_type'      => 'product',
					'post_status'    => 'publish',
					'posts_per_page' => -1,
					'fields'         => 'ids',
				)
			);

			foreach ( $product_ids as $product_id ) {
				if ( self::should_noindex_post( intval( $product_id ) ) ) {
					$excluded[] = intval( $product_id );
				}
			}
		}

		self::$sitemap_excluded_ids[ $post_type ] = array_values( array_unique( array_filter( array_map( 'intval', $excluded ) ) ) );

		return self::$sitemap_excluded_ids[ $post_type ];
	}

	private static function get_request_meta() {
		if ( null !== self::$request_meta ) {
			return self::$request_meta;
		}

		$meta = array();

		if ( is_front_page() ) {
			$front_page_id = intval( get_option( 'page_on_front' ) );
			$meta = $front_page_id ? self::get_post_meta_payload( $front_page_id ) : array();
			$meta['og_type'] = 'website';
		} elseif ( function_exists( 'is_shop' ) && is_shop() ) {
			$shop_id = self::get_wc_page_id( 'shop' );
			$meta = $shop_id ? self::get_post_meta_payload( $shop_id ) : array();
			$meta['og_type'] = 'website';
		} elseif ( function_exists( 'is_product' ) && is_product() ) {
			$meta = self::get_post_meta_payload( get_queried_object_id() );
			$meta['og_type'] = 'product';
		} elseif ( is_tax( 'product_cat' ) || is_tax( 'product_tag' ) ) {
			$term = get_queried_object();
			if ( $term && ! empty( $term->term_id ) ) {
				$meta = self::get_term_meta_payload( $term->term_id );
			}
			$meta['og_type'] = 'website';
		} elseif ( is_singular() ) {
			$meta = self::get_post_meta_payload( get_queried_object_id() );
			if ( empty( $meta['description'] ) ) {
				$post = get_post( get_queried_object_id() );
				if ( $post && ! self::should_noindex_post( $post->ID ) ) {
					$fallback_source = has_excerpt( $post ) ? get_the_excerpt( $post ) : $post->post_content;
					$fallback_source = preg_replace( '/\[[^\]]+\]/', ' ', (string) $fallback_source );
					$fallback_description = self::normalize_text( wp_strip_all_tags( $fallback_source ) );
					if ( $fallback_description ) {
						$meta['description'] = self::trim_text( $fallback_description, 158 );
					}
				}
			}
			$meta['og_type'] = 'article';
		} elseif ( is_search() ) {
			$query = get_search_query();
			$title = self::trim_text( 'Resultados de busqueda para "' . $query . '" | ' . self::get_site_name(), 68 );
			$meta = array(
				'title'               => $title,
				'og_title'            => $title,
				'twitter_title'       => $title,
				'og_type'             => 'website',
				'twitter_description' => '',
				'description'         => '',
				'og_description'      => '',
				'image'               => self::resolve_site_default_image_context(),
			);
		}

		self::$request_meta = $meta;

		return self::$request_meta;
	}

	private static function get_post_meta_payload( $post_id ) {
		$image_url = (string) get_post_meta( $post_id, self::META_IMAGE_URL, true );
		$image_alt = (string) get_post_meta( $post_id, self::META_IMAGE_ALT, true );
		$image     = self::resolve_post_image_context( $post_id );

		if ( $image_url ) {
			$image['url'] = $image_url;
		}
		if ( $image_alt ) {
			$image['alt'] = $image_alt;
		}

		return array(
			'title'               => (string) get_post_meta( $post_id, self::META_TITLE, true ),
			'description'         => (string) get_post_meta( $post_id, self::META_DESCRIPTION, true ),
			'og_title'            => (string) get_post_meta( $post_id, self::META_OG_TITLE, true ),
			'og_description'      => (string) get_post_meta( $post_id, self::META_OG_DESCRIPTION, true ),
			'twitter_title'       => (string) get_post_meta( $post_id, self::META_TWITTER_TITLE, true ),
			'twitter_description' => (string) get_post_meta( $post_id, self::META_TWITTER_DESCRIPTION, true ),
			'image'               => $image,
			'payload'             => get_post_meta( $post_id, self::META_PAYLOAD, true ),
		);
	}

	private static function get_term_meta_payload( $term_id ) {
		return array(
			'title'               => (string) get_term_meta( $term_id, self::TERM_META_TITLE, true ),
			'description'         => (string) get_term_meta( $term_id, self::TERM_META_DESCRIPTION, true ),
			'og_title'            => (string) get_term_meta( $term_id, '_siteseo_social_fb_title', true ),
			'og_description'      => (string) get_term_meta( $term_id, '_siteseo_social_fb_desc', true ),
			'twitter_title'       => (string) get_term_meta( $term_id, '_siteseo_social_twitter_title', true ),
			'twitter_description' => (string) get_term_meta( $term_id, '_siteseo_social_twitter_desc', true ),
			'image'               => self::resolve_term_image_context( $term_id ),
		);
	}

	private static function get_request_url() {
		$request_uri = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
		$request_uri = strtok( $request_uri, '#' );

		return home_url( $request_uri );
	}

	private static function schema_availability( $product ) {
		if ( ! $product || ! method_exists( $product, 'is_in_stock' ) ) {
			return 'https://schema.org/InStock';
		}

		return $product->is_in_stock() ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock';
	}

	private static function normalize_price( $price ) {
		$price = str_replace( ',', '.', (string) $price );
		return preg_replace( '/[^0-9.]/', '', $price );
	}

	private static function is_external_seo_active() {
		return self::is_siteseo_active() || self::is_other_external_seo_active();
	}

	private static function is_siteseo_active() {
		return defined( 'SITESEO_VERSION' );
	}

	private static function is_other_external_seo_active() {
		return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' );
	}

	private static function extract_runtime_feature_value( $runtime_product, $label ) {
		if ( empty( $runtime_product['features'] ) || ! is_array( $runtime_product['features'] ) ) {
			return '';
		}

		foreach ( $runtime_product['features'] as $feature ) {
			if ( empty( $feature['label'] ) || empty( $feature['value'] ) ) {
				continue;
			}
			if ( mb_strtolower( self::normalize_text( $feature['label'] ) ) === mb_strtolower( self::normalize_text( $label ) ) ) {
				return self::normalize_text( $feature['value'] );
			}
		}

		return '';
	}

	private static function normalize_keywords( $keywords ) {
		$normalized = array();

		if ( ! is_array( $keywords ) ) {
			return $normalized;
		}

		foreach ( $keywords as $keyword ) {
			$keyword = self::normalize_text( $keyword );
			if ( ! $keyword ) {
				continue;
			}
			$normalized[ mb_strtolower( $keyword ) ] = $keyword;
		}

		return array_values( $normalized );
	}

	private static function get_site_name() {
		$blogname = get_option( 'blogname' );

		return $blogname ? strtoupper( (string) $blogname ) : 'BESLOCK';
	}

	private static function get_wc_page_id( $page_key ) {
		$page_id = function_exists( 'wc_get_page_id' ) ? intval( wc_get_page_id( $page_key ) ) : 0;

		if ( $page_id > 0 ) {
			return $page_id;
		}

		$option_map = array(
			'shop'      => 'woocommerce_shop_page_id',
			'cart'      => 'woocommerce_cart_page_id',
			'checkout'  => 'woocommerce_checkout_page_id',
			'myaccount' => 'woocommerce_myaccount_page_id',
		);

		if ( isset( $option_map[ $page_key ] ) ) {
			return intval( get_option( $option_map[ $page_key ] ) );
		}

		return 0;
	}

	private static function get_wc_page_url( $page_key ) {
		$page_id = self::get_wc_page_id( $page_key );

		if ( $page_id > 0 ) {
			$url = get_permalink( $page_id );
			if ( $url ) {
				return $url;
			}
		}

		if ( function_exists( 'wc_get_page_permalink' ) ) {
			$url = wc_get_page_permalink( $page_key );
			if ( $url ) {
				return $url;
			}
		}

		return home_url( '/' );
	}

	private static function coalesce( $values ) {
		foreach ( $values as $value ) {
			$value = self::normalize_text( $value );
			if ( '' !== $value ) {
				return $value;
			}
		}

		return '';
	}

	private static function normalize_text( $value ) {
		$value = is_scalar( $value ) ? (string) $value : '';
		$value = wp_strip_all_tags( html_entity_decode( $value, ENT_QUOTES, 'UTF-8' ) );
		$value = preg_replace( '/\s+/u', ' ', $value );

		return trim( (string) $value );
	}

	private static function trim_text( $text, $max_length ) {
		$text = self::normalize_text( $text );
		if ( '' === $text ) {
			return '';
		}

		if ( mb_strlen( $text ) <= $max_length ) {
			return $text;
		}

		$trimmed = mb_substr( $text, 0, $max_length - 1 );
		$trimmed = preg_replace( '/\s+\S*$/u', '', $trimmed );

		return rtrim( $trimmed, " \t\n\r\0\x0B,.;:-" ) . '…';
	}

	private static function format_environment_list( $items, $limit = 2 ) {
		$items = array_values( array_filter( array_map( array( __CLASS__, 'normalize_text' ), (array) $items ) ) );
		$items = array_slice( array_unique( $items ), 0, max( 1, intval( $limit ) ) );

		if ( empty( $items ) ) {
			return '';
		}

		if ( 1 === count( $items ) ) {
			return mb_strtolower( $items[0] );
		}

		$last = array_pop( $items );

		return mb_strtolower( implode( ', ', $items ) . ' y ' . $last );
	}

	private static function format_cities( $cities ) {
		$cities = array_values( array_filter( array_map( array( __CLASS__, 'normalize_text' ), (array) $cities ) ) );

		if ( empty( $cities ) ) {
			return 'Colombia';
		}

		if ( 1 === count( $cities ) ) {
			return $cities[0];
		}

		$last = array_pop( $cities );

		return implode( ', ', $cities ) . ' y ' . $last;
	}
}
