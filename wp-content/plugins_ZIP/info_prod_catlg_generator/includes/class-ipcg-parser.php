<?php
/**
 * HTML parser for canonical product-card extraction.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class IPCG_Parser {

	/**
	 * Extracts the product-card short description text from rendered HTML.
	 *
	 * @param string $html Rendered product card HTML.
	 * @return string
	 */
	public function extract_short_description( $html ) {
		if ( ! is_string( $html ) || '' === trim( $html ) ) {
			return '';
		}

		$internal_errors = libxml_use_internal_errors( true );
		$dom             = new DOMDocument();
		$encoded         = mb_convert_encoding( $html, 'HTML-ENTITIES', 'UTF-8' );
		$loaded          = $dom->loadHTML( '<html><body>' . $encoded . '</body></html>' );

		if ( ! $loaded ) {
			libxml_clear_errors();
			libxml_use_internal_errors( $internal_errors );
			return '';
		}

		$xpath = new DOMXPath( $dom );
		$query = "//*[contains(concat(' ', normalize-space(@class), ' '), ' product-card__description ') and contains(concat(' ', normalize-space(@class), ' '), ' bes-product-card__description ')]";
		$nodes = $xpath->query( $query );

		libxml_clear_errors();
		libxml_use_internal_errors( $internal_errors );

		if ( ! $nodes instanceof DOMNodeList || 0 === $nodes->length ) {
			return '';
		}

		$text = trim( wp_strip_all_tags( $nodes->item( 0 )->textContent ) );
		return $this->normalize_text( $text );
	}

	/**
	 * Normalizes whitespace while preserving UTF-8 text.
	 *
	 * @param string $text Input text.
	 * @return string
	 */
	private function normalize_text( $text ) {
		$normalized = preg_replace( '/\s+/u', ' ', (string) $text );
		return trim( (string) $normalized );
	}
}
