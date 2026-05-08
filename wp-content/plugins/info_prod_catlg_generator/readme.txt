=== Info Product Catalog Generator ===
Contributors: beslock
Tags: woocommerce, export, catalog, json
Requires at least: 6.0
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Generates a normalized catalog JSON from live WooCommerce products and extracts short descriptions from canonical product-card render output.

== Description ==

This plugin exports WooCommerce products to a portable snapshot JSON file at:
  plugins_ZIP/products_thrut.json

The short_description field is extracted from the canonical rendered card markup:
.product-card__description.bes-product-card__description

It does not export image URLs, gallery fields, or attachment metadata.

== Installation ==

1. Upload the ZIP through WordPress Admin > Plugins > Add New.
2. Activate "Info Product Catalog Generator".
3. Go to Tools > Info Product Catalog Generator.
4. Click "Generate JSON".

== Changelog ==

= 1.0.0 =
* Initial standalone plugin release.
