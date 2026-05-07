# LEGACY RUNTIME Audit Summary

## Scope

Safe audit slice focused on legacy and dormant frontend runtime surfaces.

This pass did not delete assets, change enqueue order, or remove Woo/Kadence
fallbacks. It only classified the current surfaces and marked dormant owners so
the active BESLOCK architecture is explicit.

## Active Canonical Owners

### Product-card runtime and presentation

- `wp-content/themes/beslock-custom/assets/css/components/product-card.css`
- `wp-content/themes/beslock-custom/assets/js/components/product-card.js`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

These are the active owners for card hover state, badge rendering bridge,
alternate-image visibility, rotator frame states, CTA structure, and current
homepage card presentation.

### Storefront and recommendations layout

- `wp-content/themes/beslock-custom/assets/css/layout/storefront.css`
- `wp-content/themes/beslock-custom/assets/css/layout/recommendations.css`

### Homepage surfaces

- `wp-content/themes/beslock-custom/assets/css/components/hero.css`
- `wp-content/themes/beslock-custom/assets/css/components/discover.css`
- `wp-content/themes/beslock-custom/assets/css/layout/homepage.css`
- `wp-content/themes/beslock-custom/assets/css/layout/footer.css`

## Classification

### Active canonical owner

- `inc/core/enqueue.php`: active modular enqueue pipeline.
- `assets/css/components/product-card.css`: active product-card visual/runtime owner.
- `assets/js/components/product-card.js`: active product-card runtime owner.
- `assets/css/main.css`: active compatibility layer still loaded everywhere.
- `style.css`: active baseline stylesheet and low-level fallback layer.

### Dormant compatibility bridge

- `style.css` product-card baseline selectors.
  These still load, but canonical ownership has moved into the component file.
- `assets/css/main.css` legacy product-card CTA/button bridge selectors.
  Still loaded and preserved as Woo/Kadence fallback debt.
- `inc/woocommerce/enqueue-assets.php`.
  This is already a no-op compatibility include and does not enqueue product-card assets.
- `assets/js/product-badge-inject.js`.
  Not enqueued in the active runtime, but kept as a documented fallback because
  historical badge injection existed for dynamic loops.

### Inactive runtime asset

- `assets/css/product-card-alt.css`
- `assets/css/product-rotator.css`
- `assets/js/product-card-alt.js`
- `assets/js/product-rotator.js`
- `assets/js/product-card-fade.js`
- `inc/enqueue-assets.php`

These are not part of the active bootstrap from `functions.php` and were not
observed loading on homepage, cart, or single-product during this audit.

### Unresolved legacy dependency

- `functions.php::beslock_enqueue_assets()` remains active alongside `inc/core/enqueue.php`.
  It still bootstraps `style.css`, `main.css`, `main.js`, and a legacy
  `product-gallery-reel.js` handle.
- `inc/core/enqueue.php` also enqueues `product-gallery-reel.css/js`.
  The JS asset was observed loading twice on homepage, cart, and single-product.
- `footer.php` still carries a disabled product-gallery-reel fallback note.

This is not dormant. It is an active duplicated compatibility path and should
be treated as unsafe to remove without single-product gallery validation.

### Woo-sensitive or Kadence-sensitive surface

- `functions.php` late enqueue/dequeue hooks for `wc-scope-fix.css` and Kadence styles.
- single-product image/layout safety rails in `assets/css/main.css`.
- cart-empty overrides in `assets/css/main.css` and `assets/css/beslock-cart-empty.css`.
- `product-gallery-reel.css/js` load paths.

These remain explicitly unsafe deletion candidates until Woo/Kadence behavior is
validated page-by-page after any change.

### Future safe deletion candidate

- `inc/enqueue-assets.php`, once the dormant status is reconfirmed after the
  active bootstrap is simplified.
- `assets/css/product-card-alt.css`
- `assets/css/product-rotator.css`
- `assets/js/product-card-alt.js`
- `assets/js/product-rotator.js`
- `assets/js/product-card-fade.js`
- `assets/js/product-badge-inject.js`, but only after dynamic loop/AJAX badge
  scenarios are audited.

### Unsafe deletion candidate

- `functions.php::beslock_enqueue_assets()` as a whole.
- `product-gallery-reel.css/js` and related single-product hooks.
- `wc-scope-fix.css` load path.
- `style.css` and `main.css` compatibility selectors that still cover Woo/Kadence surfaces.

## Active Load Observations

### Homepage

Loaded:

- `style.css`
- `assets/css/main.css`
- `assets/css/components/product-card.css`
- `assets/js/main.js`
- `assets/js/components/product-card.js`
- `assets/js/product-gallery-reel.js` twice

Not loaded:

- `product-card-alt.css`
- `product-rotator.css`
- `product-card-fade.css`
- `product-rotator.js`

### Empty-cart recommendations

Loaded:

- `style.css`
- `assets/css/main.css`
- `assets/css/beslock-cart-empty.css`
- `assets/css/components/product-card.css`
- `assets/js/main.js`
- `assets/js/components/product-card.js`
- `assets/js/product-gallery-reel.js` twice

Not loaded:

- `product-card-alt.css`
- `product-rotator.css`
- `product-card-fade.css`
- `product-rotator.js`

### Single product

Loaded:

- `style.css`
- `assets/css/main.css`
- `assets/css/components/product-card.css`
- `assets/js/main.js`
- `assets/js/components/product-card.js`
- `assets/js/product-gallery-reel.js` twice

Not loaded:

- `product-card-alt.css`
- `product-rotator.css`
- `product-card-fade.css`
- `product-rotator.js`

## Compatibility Bridges Preserved Intentionally

- product-card legacy selector aliases inside `components/product-card.css`
  such as `.product-image-rotator`, `.product-frame`, `.product-img`,
  `.product-card__desc`, and `alt-visible`.
- cart-empty recommendation overrides in `main.css`.
- Woo single-product safety rails in `main.css`.
- Kadence dequeue logic and `wc-scope-fix.css` bootstrap.

## Validation

### Audit validation

- Confirmed `functions.php` requires `inc/core/enqueue.php` and does not require `inc/enqueue-assets.php`.
- Confirmed `inc/woocommerce/enqueue-assets.php` is a no-op compatibility bridge.
- Confirmed dormant product-card legacy assets are present in the repo but not loaded in the active audited pages.
- Confirmed `product-gallery-reel.js` is still an active duplicated load path.

### Runtime validation

- Homepage still renders storefront cards.
- Empty-cart recommendations still render.
- Add-to-cart still works on homepage.
- Cart empty state still renders the recommendation surface.
- Checkout still renders.
- Single product still renders gallery, price, and add-to-cart.
- Mobile homepage still renders product cards and action spacing.
- Header/drawer runtime remained untouched in this slice.

## Result

The active BESLOCK architecture is now easier to read:

- the real product-card owner is explicit
- dormant legacy assets are marked as such instead of looking ambiguous
- inactive enqueue surfaces are distinguished from active compatibility paths
- the main unresolved runtime debt is now clearly the duplicated gallery/bootstrap path, not the older dormant product-card files

## Next Safe Candidates

1. Audit `functions.php::beslock_enqueue_assets()` handle-by-handle against `inc/core/enqueue.php` before changing any bootstrap behavior.
2. Prove whether `product-gallery-reel.js` is needed outside single-product, then collapse the duplicate load path.
3. Continue thinning `main.css` only where selectors are clearly compatibility-only and already superseded by explicit owners.