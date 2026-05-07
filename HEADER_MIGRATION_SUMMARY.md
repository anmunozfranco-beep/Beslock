# Header Migration Summary

## Scope

First safe consolidation slice for the BESLOCK Header component.

This pass was additive only:

- no intended visual redesign
- no hard removal of legacy selectors/classes
- no Kadence compatibility changes
- no cart, checkout, or product-page flow redesign

## Runtime Ownership Changes

Canonical header render now lives in:

- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`

Compatibility wrappers now delegate to those partials:

- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`

Canonical header behavior now lives in:

- `wp-content/themes/beslock-custom/assets/js/components/header.js`

Canonical mobile drawer behavior now lives in:

- `wp-content/themes/beslock-custom/assets/js/components/mobile-drawer.js`

`wp-content/themes/beslock-custom/assets/js/models-mobile.js` was reduced to a passive enhancer so it no longer competes for drawer/products-panel state ownership.

## Inline JS Removed

Removed header-related inline ownership from:

- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/footer.php`

Removed inline owners included:

- logo height measurement / `--site-logo-height` sync
- sticky header fallback logic
- fallback drawer open/close logic
- emergency cart/header visibility restore logic

## Enqueue Changes

`wp-content/themes/beslock-custom/inc/core/enqueue.php` now loads:

- `assets/css/layout/header.css`
- `assets/css/components/header.css`
- `assets/js/components/header.js`
- `assets/js/components/mobile-drawer.js`

It no longer enqueues the old active header state owners:

- `assets/js/header-state.js`
- `assets/js/menu-products-mobile.js`
- `assets/css/header-state.css`

`assets/js/models-mobile.js` now depends on the new drawer component path instead of the removed legacy drawer owner.

## Compatibility Preserved

The new partials and runtime preserve legacy contracts required by current CSS and WooCommerce/Kadence behavior:

- legacy classes such as `.header`, `.header__bar`, `.header__logo`, `.header__icon--cart`
- legacy drawer ids/classes such as `#mobileDrawer`, `#closeDrawer`, `#productsToggle`, `#productsPanel`, `#drawerBackdrop`
- legacy drawer state classes such as `.is-open`, `.backdrop-visible`, `.products-open`, `.products-opening`, `.products-closing`
- `window.beslock.drawer` API
- `window.beslock.header` API
- `--site-logo-height` runtime contract

## Validation Performed

PHP syntax validation passed for:

- `header.php`
- `footer.php`
- `templates/menu-simple.php`
- `template-parts/header/site-header.php`
- `template-parts/header/mobile-drawer.php`

Editor diagnostics returned no errors for all touched PHP, JS, and CSS files.

Browser/runtime validation on `http://localhost:8080` confirmed:

- home renders header hooks and new component assets
- product page renders header and cart correctly
- cart page renders header and cart count correctly
- checkout page renders header and cart correctly
- `.header--scrolled` toggles after scroll on product page
- drawer open/close works on mobile viewport
- scroll lock/unlock works on mobile viewport
- products panel opens inside the drawer
- close button remains usable with products panel open
- `Escape` closes the drawer and resets products panel state

Additional validation note:

- clicking the center of the backdrop while the products panel is open is not a meaningful check because the products panel covers that area at mobile width; close control and `Escape` validation were used instead

## Files Touched

- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/footer.php`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`
- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`
- `wp-content/themes/beslock-custom/assets/js/components/header.js`
- `wp-content/themes/beslock-custom/assets/js/components/mobile-drawer.js`
- `wp-content/themes/beslock-custom/assets/js/main.js`
- `wp-content/themes/beslock-custom/assets/js/models-mobile.js`
- `wp-content/themes/beslock-custom/assets/css/layout/header.css`
- `wp-content/themes/beslock-custom/assets/css/components/header.css`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

## Remaining Debt

- `assets/js/main.js` still contains dead legacy `headerBehaviorsInit()` and `mobileMenuInit()` code text; it is no longer called, but it should be removed in a later safe cleanup slice
- header styling remains distributed across `assets/css/main.css`, `assets/css/wc-scope-fix.css`, and `assets/css/menu-products-mobile.css`
- the products panel still depends on a legacy CSS state contract instead of a fully component-owned state model
- `assets/js/header-state.js`, `assets/js/menu-products-mobile.js`, and `assets/css/header-state.css` remain in the repository as debt even though they are no longer enqueued

## Outcome

The first header migration slice is complete and stable enough to continue with later cleanup passes.

Render ownership, sticky state ownership, drawer ownership, and template inline JS ownership are now separated into additive component surfaces without intentionally changing the restored production UI.