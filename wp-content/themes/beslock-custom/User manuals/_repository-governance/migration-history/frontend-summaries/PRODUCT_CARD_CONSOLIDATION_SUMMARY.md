# Product Card Consolidation Summary

Date: 2026-05-07

## Goal

Advance the BESLOCK product-card from the first additive BEM slice into a consolidated component phase without removing compatibility wrappers, without redesigning the UI, and without affecting checkout, header, or cart flows.

## Files Touched

- `wp-content/themes/beslock-custom/assets/js/components/product-card.js`
- `wp-content/themes/beslock-custom/assets/css/components/product-card.css`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`
- `wp-content/themes/beslock-custom/assets/css/main.css`
- `wp-content/themes/beslock-custom/style.css`

## What Was Consolidated

### Component JS ownership

`assets/js/components/product-card.js` now owns the product-card interaction surface for both the new BEM API and temporary legacy selectors.

It now initializes:

- component ready state
- add-to-cart link hardening (`rel="nofollow"`)
- card hover state class (`bes-product-card--hover`)
- legacy/image rotator wrappers
- legacy alternate-image containers (`.product-card__image.has-alt`)
- reduced-motion-safe media behavior

This replaces the need for the product-card component to depend on the legacy product rotator script at runtime.

### Component CSS ownership

`assets/css/components/product-card.css` now covers the full card surface that was still split across legacy files:

- card hover elevation state
- image container normalization
- CTA group layout for `.product-card__actions`, `.bes-product-card__actions`, and `.pc-actions`
- CTA button layout for both `bes-product-card__button*` and `pc-*`
- compact button text spacing
- rotator frame stacking and fades
- alternate image overlay handling
- WooCommerce card sizing parity
- reduced motion handling

## CSS Removed

The following duplicated rules were removed because the component stylesheet now covers them:

- duplicated isolated `pc-actions` block from `wp-content/themes/beslock-custom/assets/css/main.css`
- duplicated isolated `pc-actions` block from `wp-content/themes/beslock-custom/style.css`

The removed blocks included:

- `.pc-actions *`
- `.pc-actions`
- `.pc-btn-main`
- `.pc-btn-cart`
- related mobile width override for `.pc-actions`

## Legacy Asset Enqueues Removed

The centralized enqueue pipeline no longer loads these product-card-specific legacy assets:

- `assets/css/product-rotator.css`
- `assets/js/product-rotator.js`
- `assets/css/product-card-alt.css`
- `assets/css/product-card-fade.css`

The active runtime now relies on:

- `assets/css/components/product-card.css`
- `assets/js/components/product-card.js`

## Compatibility Maintained

Compatibility was intentionally preserved during this phase:

- `pc-actions`, `pc-btn-main`, and `pc-btn-cart` remain in the DOM
- `bes-product-card*` API remains active in parallel
- reusable partial and wrapper structure remain unchanged
- `template-parts/product-card.php` wrapper remains intact
- WooCommerce loop integration remains unchanged
- centralized asset ownership remains in `inc/core/enqueue.php`
- `inc/woocommerce/enqueue-assets.php` remains a no-op compatibility bridge

## Runtime Validations

### Homepage grid

Validated at `http://localhost:8080/`.

- 6 product cards rendered
- product-card component CSS loaded
- legacy rotator CSS not loaded
- legacy alt-image CSS not loaded
- legacy rotator JS not loaded
- CTA actions computed as `position: static`
- CTA text line-height normalized to `17.6px`
- all sampled cards kept bottom CTA alignment stable
- no description/actions overlap detected
- varying description heights remained stable

### Empty cart cards

Validated at `http://localhost:8080/carrito/` before and after add-to-cart roundtrip.

- empty-cart recommendations rendered correctly
- 4 product cards rendered in empty-cart state
- CTA line-height remained `17.6px`
- actions stayed in normal flow (`position: static`)
- legacy rotator/alt/fade assets were not loaded

### Add-to-cart behavior

Validated by clicking the first product-card cart CTA from the homepage.

- home add-to-cart request resolved through `/?add-to-cart=240`
- cart counter updated to `1`
- cart page rendered 1 cart row for `e-Shield`
- cart was then cleared and revalidated back to empty-cart state

### Single product / related products

Validated at `http://localhost:8080/producto/e-shield/`.

- single product add-to-cart button remained `Agregar al carrito`
- current local dataset still exposes no related-products product-card surface on tested page
- no product-card runtime regression observed on single-product route

### Mobile viewport

Validated on the homepage with the available browser runtime.

- no horizontal overflow detected
- actions remained `position: static`
- compact CTA line-height remained active
- no text/actions overlap detected

## Remaining Technical Debt

The component is now the active source of truth, but these cleanup items still remain for a later safe phase:

- `template-parts/cards/product-card.php` still outputs `pc-actions`, `pc-btn-main`, and `pc-btn-cart` for compatibility
- `assets/css/main.css` still contains many older `.product-card__actions`, `.product-card__image`, and `.product-card:hover` rules that are no longer authoritative but have not yet been fully removed
- `style.css` still contains multiple legacy `.product-card__actions` and `.product-card__image` overrides outside the removed `pc-actions` block
- orphaned legacy asset files still exist in the repository even though they are no longer enqueued:
  - `assets/css/product-rotator.css`
  - `assets/js/product-rotator.js`
  - `assets/css/product-card-alt.css`
  - `assets/css/product-card-fade.css`
  - `assets/js/product-card-alt.js`
  - `assets/js/product-card-fade.js`
- `wp-content/themes/beslock-custom/inc/enqueue-assets.php` still contains stale product-card enqueue logic but is not part of the active theme bootstrap
- `assets/css/components/badge.css` still contains hover coupling for `.product-card:hover .product-card__badge` and should be reviewed against the consolidated component surface

## Next Safe Removal Candidates

The next low-risk consolidation steps are:

1. remove dead legacy product-card rules from `assets/css/main.css` that duplicate card hover, image, and action layout already covered by the component
2. remove equivalent dead legacy product-card rules from `style.css`
3. drop `pc-*` classes from the product-card partial once no external JS/CSS still depends on them
4. delete orphaned rotator/alt/fade asset files after confirming no other template renders those legacy selectors
5. audit `assets/css/components/badge.css` so badge hover behavior is fully owned by the product-card component surface

## Outcome

The product-card component is now the first BESLOCK frontend component whose active runtime behavior and primary styling live in the dedicated component files, while temporary legacy class compatibility is still preserved.