<?php
/**
 * Catalog generator service.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class IPCG_Generator {

	/**
	 * @var IPCG_Parser
	 */
	private $parser;

	/**
	 * @param IPCG_Parser|null $parser Parser dependency.
	 */
	public function __construct( ?IPCG_Parser $parser = null ) {
		$this->parser = $parser ? $parser : new IPCG_Parser();
	}

	/**
	 * Generates products_thrut.json from live WooCommerce products.
	 *
	 * @return array|WP_Error
	 */
	public function generate_catalog() {
		if ( ! function_exists( 'wc_get_product' ) ) {
			return new WP_Error( 'ipcg_missing_woocommerce', __( 'WooCommerce functions are unavailable.', 'info-prod-catlg-generator' ) );
		}

		$debug_rows = $this->collect_debug_inventory();
		$warnings   = array();

		$product_ids = get_posts(
			array(
				'post_type'      => 'product',
				'post_status'    => array( 'publish' ),
				'posts_per_page' => -1,
				'fields'         => 'ids',
				'orderby'        => 'ID',
				'order'          => 'ASC',
				'no_found_rows'  => true,
			)
		);

		$catalog         = array();
		$seen_slugs      = array();
		$duplicate_slugs = array();

		foreach ( $product_ids as $product_id ) {
			$product = wc_get_product( (int) $product_id );
			if ( ! $product instanceof WC_Product ) {
				continue;
			}

			if ( $product->is_type( 'variation' ) ) {
				continue;
			}

			$status = (string) $product->get_status();
			if ( 'publish' !== $status ) {
				continue;
			}

			$slug = (string) $product->get_slug();
			if ( '' === $slug ) {
				$warnings[] = sprintf( 'Product ID %d skipped: empty slug.', (int) $product->get_id() );
				continue;
			}

			if ( $this->is_placeholder_product( $product, $slug ) ) {
				$warnings[] = sprintf(
					'Skipped placeholder product artifact: slug=%1$s ID=%2$d.',
					$slug,
					(int) $product->get_id()
				);
				continue;
			}

			if ( isset( $seen_slugs[ $slug ] ) ) {
				$duplicate_slugs[] = $slug;
				$warnings[]        = sprintf( 'Duplicate slug detected and skipped: %s (product ID %d).', $slug, (int) $product->get_id() );
				continue;
			}

			$seen_slugs[ $slug ] = true;

			$catalog[] = array(
				'product_id'        => (int) $product->get_id(),
				'slug'              => $slug,
				'sku'               => (string) $product->get_sku(),
				'name'              => $this->normalize_text( (string) $product->get_name() ),
				'price'             => (string) $product->get_price(),
				'short_description' => $this->extract_short_description_from_canonical_render( $product ),
				'description'       => $this->normalize_text( wp_strip_all_tags( (string) $product->get_description() ) ),
				'categories'        => $this->get_term_names( (int) $product->get_id(), 'product_cat' ),
				'tags'              => $this->get_term_names( (int) $product->get_id(), 'product_tag' ),
				'status'            => $status,
			);
		}

		$written = $this->write_json_file( $catalog );
		if ( is_wp_error( $written ) ) {
			return $written;
		}

		$unique_slug_count = count( array_unique( wp_list_pluck( $catalog, 'slug' ) ) );
		$exported_count    = count( $catalog );

		if ( $exported_count !== $unique_slug_count ) {
			$warnings[] = sprintf(
				'Validation warning: exported products (%d) differ from unique slugs (%d).',
				$exported_count,
				$unique_slug_count
			);
		}

		return array(
			'count'                => $exported_count,
			'unique_slug_count'    => $unique_slug_count,
			'duplicate_slug_count' => count( array_unique( $duplicate_slugs ) ),
			'duplicate_slugs'      => array_values( array_unique( $duplicate_slugs ) ),
			'exported_slugs'       => array_values( wp_list_pluck( $catalog, 'slug' ) ),
			'debug_rows'           => $debug_rows,
			'warnings'             => $warnings,
			'path'                 => $written,
		);
	}

	/**
	 * Build debug inventory to diagnose over-export issues.
	 *
	 * @return array<int,array<string,mixed>>
	 */
	private function collect_debug_inventory() {
		$ids = get_posts(
			array(
				'post_type'      => array( 'product', 'product_variation' ),
				'post_status'    => 'any',
				'posts_per_page' => -1,
				'fields'         => 'ids',
				'orderby'        => 'ID',
				'order'          => 'ASC',
				'no_found_rows'  => true,
			)
		);

		$rows = array();

		foreach ( $ids as $id ) {
			$post = get_post( (int) $id );
			if ( ! $post instanceof WP_Post ) {
				continue;
			}

			$product = wc_get_product( (int) $id );
			$rows[]  = array(
				'id'           => (int) $id,
				'post_type'    => (string) $post->post_type,
				'product_type' => $product instanceof WC_Product ? (string) $product->get_type() : 'n/a',
				'slug'         => (string) $post->post_name,
				'status'       => (string) $post->post_status,
				'parent_id'    => (int) $post->post_parent,
			);
		}

		return $rows;
	}

	/**
	 * Identify known placeholder product artifacts created by broken imports.
	 *
	 * @param WC_Product $product Product instance.
	 * @param string     $slug Product slug.
	 * @return bool
	 */
	private function is_placeholder_product( WC_Product $product, $slug ) {
		$post = get_post( (int) $product->get_id() );
		if ( ! $post instanceof WP_Post ) {
			return false;
		}

		$title = trim( (string) $post->post_title );
		$sku   = trim( (string) $product->get_sku() );

		if ( '' !== $sku ) {
			return false;
		}

		return (bool) preg_match( '/^product(?:-[0-9]+)?$/', $slug ) && 'Product' === $title;
	}

	/**
	 * Renders canonical WooCommerce loop template and extracts product-card description text.
	 *
	 * Canonical chain:
	 * woocommerce/content-product.php -> template-parts/product-card.php -> template-parts/cards/product-card.php
	 *
	 * @param WC_Product $product Product instance.
	 * @return string
	 */
	private function extract_short_description_from_canonical_render( WC_Product $wc_product ) {
		global $post, $product;

		$previous_post    = $post;
		$previous_product = $product;
		$previous_context = get_query_var( 'beslock_context', null );

		$post = get_post( $wc_product->get_id() );
		if ( $post instanceof WP_Post ) {
			setup_postdata( $post );
		}

		$product = $wc_product;
		set_query_var(
			'beslock_context',
			array(
				'show_description' => true,
			)
		);

		ob_start();
		wc_get_template_part( 'content', 'product' );
		$html        = ob_get_clean();
		$description = $this->parser->extract_short_description( (string) $html );

		if ( '' === $description ) {
			ob_start();
			get_template_part(
				'template-parts/product-card',
				null,
				array(
					'product'          => $wc_product,
					'show_description' => true,
				)
			);
			$fallback_html = ob_get_clean();
			$description   = $this->parser->extract_short_description( (string) $fallback_html );
		}

		$product = $previous_product;
		if ( null === $previous_context ) {
			set_query_var( 'beslock_context', array() );
		} else {
			set_query_var( 'beslock_context', $previous_context );
		}
		$post = $previous_post;
		if ( $previous_post instanceof WP_Post ) {
			setup_postdata( $previous_post );
		} else {
			wp_reset_postdata();
		}

		return $description;
	}

	/**
	 * Gets term names for a product taxonomy.
	 *
	 * @param int    $product_id Product ID.
	 * @param string $taxonomy Taxonomy name.
	 * @return array
	 */
	private function get_term_names( $product_id, $taxonomy ) {
		$terms = wp_get_post_terms( $product_id, $taxonomy, array( 'fields' => 'names' ) );
		if ( is_wp_error( $terms ) || ! is_array( $terms ) ) {
			return array();
		}

		$normalized = array();
		foreach ( $terms as $term_name ) {
			$normalized[] = $this->normalize_text( (string) $term_name );
		}
		return $normalized;
	}

	/**
	 * Writes JSON data to target output file.
	 *
	 * @param array $catalog Export payload.
	 * @return string|WP_Error
	 */
	private function write_json_file( array $catalog ) {
		$target = $this->get_output_path();
		$dir    = dirname( $target );

		if ( ! is_dir( $dir ) ) {
			if ( ! wp_mkdir_p( $dir ) ) {
				return new WP_Error( 'ipcg_output_dir', sprintf( __( 'Cannot create output directory: %s', 'info-prod-catlg-generator' ), $dir ) );
			}
		}

		$json = wp_json_encode( $catalog, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		if ( false === $json ) {
			return new WP_Error( 'ipcg_json_encode', __( 'Failed to encode JSON payload.', 'info-prod-catlg-generator' ) );
		}

		$result = file_put_contents( $target, $json . PHP_EOL, LOCK_EX );
		if ( false === $result ) {
			return new WP_Error( 'ipcg_write_failed', sprintf( __( 'Cannot write output file: %s', 'info-prod-catlg-generator' ), $target ) );
		}

		return $target;
	}

	/**
	 * Returns output path using centralized helper.
	 *
	 * @return string
	 */
	public function get_output_path() {
		return IPCG_Utils::get_products_json_path();
	}

	/**
	 * @param string $text Input text.
	 * @return string
	 */
	private function normalize_text( $text ) {
		$normalized = preg_replace( '/\s+/u', ' ', (string) $text );
		return trim( (string) $normalized );
	}
}
