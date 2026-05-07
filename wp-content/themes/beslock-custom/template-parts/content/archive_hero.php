<?php
/**
 * Child theme override: archive hero
 *
 * LEGACY BRIDGE — canonical parent rendering still lives in Kadence, but this
 * child override is the active suppression surface for Woo archive hero output.
 * PRESERVED FOR BACKWARD COMPATIBILITY with parent-theme archive contexts.
 *
 * Purpose: completely disable the Kadence archive/hero output for the
 * Shop page and product archives (product categories and tags) by short-circuiting
 * the template. For all other contexts this file defers to the parent theme's
 * `template-parts/content/archive_hero.php` to preserve default behavior.
 *
 * Placement: `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
 */

defined( 'ABSPATH' ) || exit;

// If this is the Shop or a product taxonomy archive, do not render the hero.
if ( function_exists( 'is_shop' ) && ( is_shop() || is_product_category() || is_product_tag() ) ) {
    // Intentionally empty: suppress Kadence hero for Shop and product archive pages.
    return;
}

// PRESERVED LEGACY DELEGATOR — non-Woo archive contexts still fall through to
// the parent template so child and parent behavior remain aligned.
// Otherwise, include the parent's template so behavior is identical to Kadence.
$parent_template = get_template_directory() . '/template-parts/content/archive_hero.php';
if ( file_exists( $parent_template ) ) {
    include $parent_template; // phpcs:ignore WordPressVIPMinimum.Files.IncludingFile
}
