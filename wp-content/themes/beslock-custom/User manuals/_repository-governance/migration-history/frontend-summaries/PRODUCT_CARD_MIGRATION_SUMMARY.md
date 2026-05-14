# Product Card Migration Summary

## Scope

First production-safe BEM migration slice for the BESLOCK product-card.

This slice keeps the current WooCommerce runtime intact and introduces the new
component API in parallel with the legacy DOM contract.

## Files Touched

- `wp-content/themes/beslock-custom/template-parts/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
- `wp-content/themes/beslock-custom/inc/woocommerce/product-hooks.php`
- `wp-content/themes/beslock-custom/assets/css/components/product-card.css`
- `wp-content/themes/beslock-custom/assets/js/components/product-card.js`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`
- `wp-content/themes/beslock-custom/inc/woocommerce/enqueue-assets.php`

## Dependencies

- WooCommerce loop override still enters via `woocommerce/content-product.php`
- existing template compatibility still enters via `template-parts/product-card.php`
- centralized asset loading now comes from `inc/core/enqueue.php`
- badge eligibility now lives in `inc/woocommerce/product-hooks.php`
- visual behavior still depends on existing legacy CSS in `main.css` and `style.css`

## What Changed

- added reusable partial at `template-parts/cards/product-card.php`
- introduced parallel BEM API:
  - `bes-product-card`
  - `bes-product-card__image`
  - `bes-product-card__content`
  - `bes-product-card__title`
  - `bes-product-card__price`
  - `bes-product-card__actions`
- kept legacy classes in place:
  - `product-card`
  - `product-card__*`
  - `pc-card`
  - `pc-actions`
  - `pc-btn-main`
  - `pc-btn-cart`
- moved badge decision out of the template body into WooCommerce hook-layer helper functions
- moved component enqueue ownership to the centralized enqueue pipeline

## Remaining Legacy Debt

- card visuals are still heavily influenced by `assets/css/main.css` and `style.css`
- legacy `pc-*` action classes still exist and remain required for safety
- product-card JS behavior is only lightly modularized in this slice
- old related CSS/JS files still exist:
  - `product-card-alt.css`
  - `product-card-fade.css`
  - `product-card-alt.js`
  - `product-card-fade.js`
  - `product-rotator.js`
- badge styling still has duplicate legacy rules outside the component file

## Next Migration Candidates

1. consolidate product-card action/button styling and remove `pc-*` aliases
2. fold alternate-image and rotator behavior into the component module
3. reduce duplicated product-card CSS from `main.css` and `style.css`
4. normalize product-card variants as explicit modifiers
5. move related-products and portfolio grids onto the same reusable cards surface