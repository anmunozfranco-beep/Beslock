=== Info Product Catalog Loader ===
Contributors: beslock
Requires at least: 6.0
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Loads and updates WooCommerce products from a portable JSON snapshot and imports local WEBP images in a second independent step.

== Description ==

This plugin provides two admin actions under Tools > Info Product Catalog Loader:

1. Cargar datos de productos
- Reads products JSON from:
  plugins_ZIP/products_thrut.json
- Creates missing products and updates matched products.
- Matching key: slug (post_name).

2. Cargar imágenes
- Reads image files from:
  {active-theme}/assets/images (resolved at runtime via get_stylesheet_directory())
- Featured image rule: slug_.webp
- Gallery rule: slug_*.webp excluding slug_.webp
- Reuses existing attachments when possible and avoids duplicate gallery entries.

Supported product fields:
- product_id
- slug
- sku
- name
- price
- short_description
- description
- categories
- tags
- status

Unsupported fields are ignored by design, including external image URLs and attachment metadata from JSON.

== Installation ==

1. Upload the plugin ZIP in WordPress admin.
2. Activate the plugin.
3. Go to Tools > Info Product Catalog Loader.

== Changelog ==

= 1.0.0 =
- Initial release.
