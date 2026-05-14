# PRIMARY BOOTSTRAP Consolidation Summary

## Scope

Safe architectural slice focused on the primary active bootstrap overlap between:

- `wp-content/themes/beslock-custom/functions.php`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

This pass did not remove the compatibility bootstrap, did not rewrite WooCommerce
runtime, did not change checkout/cart behavior, and did not touch dormant legacy
assets beyond existing documentation.

## Canonical Enqueue Owner

### Primary runtime/bootstrap owner

- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

This file is now the explicit canonical owner for:

- `beslock-extra-style`
- `beslock-main-js`
- modular component/layout stylesheet loading
- modular frontend script loading
- late `beslock-wc-scope-fix` enqueue
- late Kadence/frontend style cleanup

## Compatibility Bootstrap Paths

### Early base bridge

- `functions.php::beslock_enqueue_main_style()`

This remains the early bridge that guarantees `beslock-main-style` exists before
the modular runtime depends on it.

### Compatibility fallback bridge

- `functions.php::beslock_enqueue_assets()`

This remains active, but now behaves as a guarded fallback bridge instead of a
co-owner for the base runtime handles.

### Late compatibility bridges

- `functions.php` late `beslock-wc-scope-fix` hook at priority `20`
- `functions.php` late Kadence cleanup hook at priority `100`

These now only act as bridge/fallback paths when the canonical owner in
`inc/core/enqueue.php` has not already taken control.

## Active Runtime Classification

### Canonical runtime owner

- `inc/core/enqueue.php`

### Compatibility bootstrap

- `functions.php::beslock_enqueue_main_style()`
- `functions.php::beslock_enqueue_assets()`

### Runtime bridge

- guarded fallback enqueue for `beslock-extra-style`
- guarded fallback enqueue for `beslock-main-js`
- guarded fallback enqueue for `beslock-gallery-reel`
- guarded fallback enqueue for `beslock-wc-scope-fix`
- guarded fallback Kadence cleanup in `functions.php`

### Woo-sensitive runtime

- `beslock-wc-scope-fix`
- `assets/js/product-gallery-reel.js`
- `assets/js/product-gallery-init.js`
- `assets/js/fix-placeholder.js`
- `assets/js/product-quantity-controls.js`
- single-product styles such as `product-page.css` and `product-tabs.css`

### Kadence-sensitive runtime

- `kadence-parent-style` bootstrap/dequeue path
- late `kadence*` style cleanup
- late cleanup of `global-styles`, `classic-theme-styles`, `wp-block-library-theme`, and `wp-block-library`

### Safe consolidation candidates completed in this slice

- base handle ownership for `beslock-extra-style`
- base handle ownership for `beslock-main-js`
- late `beslock-wc-scope-fix` enqueue ownership
- late Kadence cleanup ownership
- fallback registration for `beslock-main-style` now points to `style.css` instead of incorrectly mapping that handle to `assets/css/main.css`

### Unresolved dependency

- `beslock-main-style` is still bootstrapped from `functions.php` and remains a required early dependency for the canonical runtime
- `assets/js/product-gallery-reel.js` still loads globally from the canonical path even though its behavior is effectively single-product-only
- the single-product inline overlay script in `inc/core/enqueue.php` still sits outside the enqueue handle graph

## Duplicate Active Ownership Resolved

Before this slice, both active surfaces still claimed enqueue/bootstrap authority for:

- `beslock-extra-style`
- `beslock-main-js`
- `beslock-wc-scope-fix`
- late Kadence/frontend cleanup behavior

After this slice:

- `inc/core/enqueue.php` remains the canonical owner
- `functions.php` only enqueues those handles when the canonical owner did not already enqueue them
- `functions.php` only runs its late Kadence cleanup when the canonical cleanup hook did not already complete

## Safe Changes Applied

### functions.php

- `beslock_enqueue_assets()` now skips `beslock-extra-style` when already enqueued/done by the canonical runtime
- `beslock_enqueue_assets()` now skips `beslock-main-js` when already enqueued/done by the canonical runtime
- late `beslock-wc-scope-fix` bridge now skips when the canonical late enqueue already ran
- late `beslock-wc-scope-fix` fallback registration restores `beslock-main-style` to the correct `style.css` source
- late Kadence cleanup now exits when the canonical cleanup action already completed

### inc/core/enqueue.php

- explicit ownership comments now mark the file as the canonical active runtime/bootstrap owner
- late Woo scope-fix and Kadence cleanup hooks are documented as canonical owners
- late Kadence cleanup now emits `beslock_core_kadence_cleanup_complete` so the compatibility bridge can stand down safely

## Validation

### Duplicate asset loading behavior

Runtime checks on homepage, single product, cart, and checkout showed:

- `main.js`: `1` script tag and `1` resource load per checked page
- `main.css`: `1` stylesheet link per checked page
- `wc-scope-fix.css`: `1` stylesheet link per checked page
- `product-gallery-reel.js`: `1` script tag and `1` resource load on homepage and single product

### Homepage

- renders `6` product cards
- mobile drawer surface still present
- mobile drawer still opens
- `drawer-no-scroll` and `has-drawer-open` still apply after opening the drawer

### Single product

- `.product-page__gallery` still renders
- gallery controls still expose `2` slide buttons and `1 / 2` count text
- quantity controls remain present
- add-to-cart remains present
- add-to-cart increments cart count from `1` to `2`
- console error and page error checks remained empty during runtime validation

### Cart

- cart row still renders
- checkout link still renders
- totals surface still renders

### Checkout

- checkout surface still renders
- place-order button still renders

## Remaining Bootstrap Overlap

The primary duplicated enqueue authority is now reduced, but the runtime is not
fully singular yet.

Open overlap still worth auditing later:

1. Determine whether `beslock-main-style` can stay permanently as an early bridge in `functions.php` or should gain a more explicit bootstrap contract.
2. Prove whether `product-gallery-reel.js` should stop loading globally and become single-product scoped from the canonical owner.
3. Audit whether the inline single-product overlay script should stay in `wp_head` or move into an explicit runtime handle later.

## Result

This slice moved the primary active bootstrap ownership in the intended direction without widening risk:

- `inc/core/enqueue.php` is the clear canonical owner for active base runtime handles and late cleanup hooks
- `functions.php` remains active, but now behaves as an explicit compatibility/bootstrap bridge for those overlapping surfaces
- duplicated enqueue authority for the main overlapping handles was reduced without breaking WooCommerce or Kadence-sensitive pages