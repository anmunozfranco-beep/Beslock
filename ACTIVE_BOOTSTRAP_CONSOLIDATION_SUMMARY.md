# ACTIVE BOOTSTRAP Consolidation Summary

## Scope

Safe architectural slice focused on the active enqueue/bootstrap runtime.

This pass did not remove the compatibility bootstrap, did not redesign JS
ownership, and did not alter WooCommerce gallery behavior. It only clarified the
canonical owner and removed one proven duplicate active load path.

## Canonical Enqueue Owner

### Frontend modular owner

- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

This is the canonical active enqueue surface for the modern frontend runtime,
including modular CSS owners, header/mobile drawer JS, canonical product-card
runtime, and the current gallery reel handle.

## Active Compatibility Bootstrap Paths

### Early base bootstrap

- `wp-content/themes/beslock-custom/functions.php`
  - `beslock_enqueue_main_style()` at priority `1`
  - `beslock_enqueue_assets()` at default priority `10`

This remains active as a compatibility bootstrap for shared base handles and
legacy runtime continuity.

### Active Woo/Kadence-sensitive hooks

- `functions.php` late `wc-scope-fix.css` enqueue hook
- `functions.php` late Kadence style dequeue hook
- `inc/core/enqueue.php` matching `wc-scope-fix.css` and late style cleanup hooks

These are still Woo/Kadence-sensitive and were not consolidated in this slice.

## Active Runtime Classification

### Canonical active owner

- `inc/core/enqueue.php`
- `assets/js/components/product-card.js`
- `assets/css/components/product-card.css`
- `assets/js/components/header.js`
- `assets/js/components/mobile-drawer.js`

### Compatibility bootstrap

- `functions.php::beslock_enqueue_assets()`
- `functions.php::beslock_enqueue_main_style()`

### Duplicate active path found during audit

- `assets/js/product-gallery-reel.js`
  - handle `beslock-gallery-reel` from `functions.php`
  - handle `beslock-product-gallery-reel-js` from `inc/core/enqueue.php`

This script was observed loading twice on homepage and single-product before the
consolidation guard in this slice.

### Woo-sensitive runtime

- `assets/js/product-gallery-reel.js`
- `assets/js/product-gallery-init.js`
- `assets/js/fix-placeholder.js`
- `assets/js/product-quantity-controls.js`
- `wc-scope-fix.css` enqueue path

### Globally loaded runtime

- `assets/js/main.js`
- `assets/js/components/header.js`
- `assets/js/components/mobile-drawer.js`
- `assets/js/components/product-card.js`
- `assets/js/product-gallery-reel.js` from the canonical path

### Single-product-only runtime in behavior

- `assets/js/product-gallery-reel.js`
  - only initializes `.product-page__gallery`
- `assets/js/product-gallery-init.js`
  - only runs when `.single-product` exists
- `assets/js/product-quantity-controls.js`
  - product quantity controls

## Duplicate Initialization Findings

### product-gallery-reel.js

Before this slice:

- the same file loaded twice through different handles
- homepage loaded the script twice even with `0` `.product-page__gallery` roots
- single product loaded the script twice while only producing one visible reel UI

Runtime details:

- the script already avoided duplicate DOM UI through `data-beslockInit="1"`
- it did **not** have a global idempotence guard
- duplicate execution could still create duplicate global `load` listeners,
  duplicate `MutationObserver` instances, and duplicate mobile excerpt resize handlers

### Consolidation applied

- `functions.php` now skips its compatibility enqueue when the canonical handle
  `beslock-product-gallery-reel-js` is already enqueued
- `assets/js/product-gallery-reel.js` now exits early if a prior execution has
  already initialized the runtime globally

This preserves behavior while reducing accidental duplicate listeners and script tags.

## Safe Consolidation Applied

### Handle ownership normalization

- canonical owner kept in `inc/core/enqueue.php`
- compatibility bootstrap in `functions.php` reduced to fallback-only behavior

### Runtime idempotence protection

- `window.__beslockProductGalleryReelInit` guard added to
  `assets/js/product-gallery-reel.js`

## Unresolved Risks

- `functions.php` and `inc/core/enqueue.php` still overlap on base handles such as
  `beslock-main-style`, `beslock-extra-style`, and `beslock-main-js`
- `product-gallery-reel.js` is still loaded globally by the canonical owner even
  though its behavior is effectively single-product-only
- `product-gallery-init.js` remains present in the repo and can still interact
  with Woo gallery timing if it becomes enqueued elsewhere later
- Woo/Kadence late enqueue/dequeue hooks are still duplicated across active surfaces

## Safe Future Consolidation Candidates

1. Audit `beslock-main-js` and `beslock-extra-style` ownership to determine
   whether `functions.php::beslock_enqueue_assets()` can shrink further without
   destabilizing Woo/Kadence pages.
2. Prove `product-gallery-reel.js` is only needed on single-product, then scope
   the canonical enqueue path accordingly.
3. Consolidate duplicate Woo/Kadence enqueue hooks only after validating style
   ordering and checkout/cart stability.

## Validation

### Runtime validation

- Homepage still renders storefront cards and add-to-cart works.
- Single product still renders one gallery UI with one reel root, one counter,
  and two dots.
- Cart still renders.
- Checkout still renders with active cart contents.
- Mobile drawer still opens and keeps body scroll lock.

### Duplicate loading validation

Before the change:

- homepage DOM contained two `product-gallery-reel.js` script URLs
- single-product DOM contained two `product-gallery-reel.js` script URLs

After the change, the active architecture is protected in two places:

- duplicate enqueue is blocked from the compatibility bootstrap when the
  canonical handle already exists
- duplicate runtime execution is blocked by the global JS guard

## Result

The active bootstrap is now clearer and safer without widening the migration:

- `inc/core/enqueue.php` is the explicit canonical owner for the reel runtime
- `functions.php` remains active, but its gallery reel path is now fallback-only
- duplicate reel execution is prevented even if an overlapping path reappears