# HOMEPAGE SURFACE Migration Summary

## Scope

Next safe `main.css` decomposition slice focused on homepage surfaces and page-level component ownership.

This slice moved only homepage selectors that are now clearly backed by the active homepage markup and can be owned safely outside `main.css`:

- the active `beslock-hero` carousel surface
- the `discover` CTA block
- the real `site-footer` surface used by `footer.php`
- a minimal homepage-only spacing rule for homepage section rhythm

This slice did **not** move WooCommerce grids, cart-empty product recommendations, drawer/sticky runtime contracts, or the older compatibility `hero*` bridge blocks that still need a later audit.

## Files Touched

- `wp-content/themes/beslock-custom/assets/css/components/hero.css`
- `wp-content/themes/beslock-custom/assets/css/components/discover.css`
- `wp-content/themes/beslock-custom/assets/css/layout/footer.css`
- `wp-content/themes/beslock-custom/assets/css/layout/homepage.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

## Audit Classification

### Canonical component ownership now extracted

- `.beslock-hero`
- `.beslock-loader*`
- `.hero-viewport`
- `.hero-slides`
- `.hero-slide*`
- `.slide-inner`
- `.slide-video`
- `.slide-overlay*`
- `.slide-dim`
- `.slide-content`
- `.hero__title`
- `.hero__subtitle`
- `.hero-dots`
- `.hero-dot*`
- `slide-title-in` / `slide-subtitle-in` keyframes
- `.discover*`

### Canonical layout ownership now extracted

- `.site-footer`
- `.footer-logo`
- `.site-footer .u-container`
- `.site-footer .footer-copy`
- homepage-only spacing for `.products-portfolio` and `.discover`

### Compatibility intentionally kept in `main.css`

- legacy `.hero`, `.hero__video`, `.hero__fallback`, `.hero__content` lineage
- feature-wrapper positioning bridges around the hero slide content
- product-card and WooCommerce grid/layout fallbacks
- cart-empty recommendation styling using `.products-portfolio__grid`
- single-product and Woo safety rails

### Unsafe for this slice

- lower mixed hero feature/responsive blocks not yet proven redundant
- any `products-portfolio__grid` rule that also affects empty-cart recommendations
- any selector coupled to drawer, sticky header, or JS state classes

## Enqueue Changes

`inc/core/enqueue.php` now loads these owners after `main.css`:

- `beslock-homepage-layout`
- `beslock-footer-layout`
- `beslock-hero-component`
- `beslock-discover-component`

This keeps `main.css` operational as a compatibility layer while the canonical homepage owners now live in explicit modular stylesheets.

## Selectors Removed From `main.css`

- full `discover` block
- `site-footer` visual block
- `footer-logo` block
- `.site-footer .u-container`
- `.site-footer .footer-copy`
- appended `HERO BESLOCK STYLES` block for the active hero carousel
- homepage spacing rule for `.discover`

## What Stayed In `main.css`

- product-card portfolio layout and product-card fallback blocks
- legacy hero compatibility rules
- mixed section bridges that still touch product-card or Woo surfaces
- any rule that could affect cart, checkout, single-product, or drawer behavior

## Validation

### Static validation

- No CSS errors in the extracted stylesheet files.
- No CSS errors in `main.css` after block removal.
- No PHP errors in `inc/core/enqueue.php` after enqueue additions.

### Runtime validation

- Homepage desktop: the extracted `hero`, `discover`, `footer`, and `homepage` stylesheets all load after `main.css`.
- Homepage desktop: `.beslock-hero`, `.discover`, `.products-portfolio`, `.site-footer`, and six hero dots still render.
- Homepage desktop: hero remains black, discover remains white, footer padding remains intact.
- Homepage mobile: drawer still opens, `has-drawer-open` and `drawer-no-scroll` still apply, and footer still renders.
- Product page: title, quantity control, add-to-cart button, and footer remain present.
- Cart empty state: recommendation cards still render and footer remains present.

## Result

This slice makes homepage ownership more explicit without widening into risky Woo or runtime surfaces:

- `main.css` no longer owns the active homepage hero carousel block
- `discover` now has a dedicated component owner
- `site-footer` now has a dedicated layout owner
- homepage spacing moved into a dedicated layout file, but only for the proven safe selectors

## Next Safe Candidates

1. Audit the remaining hero feature-wrapper and responsive bridge rules to see which ones still belong to the active `beslock-hero` DOM.
2. Separate homepage product-grid spacing from cart-empty recommendation rules before moving any `.products-portfolio__grid` ownership.
3. Leave Woo/single-product safety rails untouched until they are audited page-by-page again.