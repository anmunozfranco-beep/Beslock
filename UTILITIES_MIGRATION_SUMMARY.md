# UTILITIES Migration Summary

## Scope

Next safe `main.css` decomposition slice focused on shared UI primitives and utility ownership.

This slice intentionally moved only canonical reusable helpers that are safe to own outside `main.css`:

- shared button primitives
- shared container/layout helpers
- shared section spacing helpers
- shared reveal/visibility state helpers

The slice did **not** move WooCommerce-specific overrides, page-specific layout, or unclear legacy bridges.

## Files Touched

- `wp-content/themes/beslock-custom/assets/css/utilities/buttons.css`
- `wp-content/themes/beslock-custom/assets/css/utilities/layout-helpers.css`
- `wp-content/themes/beslock-custom/assets/css/utilities/utilities.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

## Audit Classification

### Canonical utility ownership

- `.btn`
- `.btn, .beslock-btn, .discover__btn`
- shared button interactive states for `.btn`, `.beslock-btn`, `.discover__btn`
- `.u-container, .container`
- `.section`
- `.section--lined`
- `.section--lined::before`
- `.section-reveal`
- `.section-reveal.is-active`
- reduced-motion reveal fallback

### Component-specific ownership kept out of this slice

- `.hero__cta`
- all `product-card*` selectors
- header/drawer selectors
- discover/hero/footer component blocks

### Layout ownership kept in main.css

- single-product image/summary grid rules
- hero slide feature positioning
- page-specific responsive layouts

### WooCommerce dependency kept in main.css

- single-product safety rails
- Woo product-card and product-page overrides
- cart/checkout rendering-specific styles

### Compatibility bridges preserved

- product-card CTA/cart legacy bridges
- header offset and stacking variables
- theme-specific component selectors not yet fully classified

### Unsafe legacy dependency deferred

- generic-looking grid/flex rules that are actually tied to page sections
- global spacing helpers that still sit inside page-specific blocks
- Woo/Kadence safety overrides around `.u-container` consumers in `wc-scope-fix.css`

## Extracted Utility Layers

### `assets/css/utilities/buttons.css`

Owns canonical shared button primitives:

- base `.btn`
- pill-style shared button surface for `.btn`, `.beslock-btn`, `.discover__btn`
- shared interactive hover/focus/active states for those selectors

### `assets/css/utilities/layout-helpers.css`

Owns reusable layout primitives:

- `.u-container, .container`
- `.section`
- `.section--lined`
- `.section--lined::before`

### `assets/css/utilities/utilities.css`

Owns generic state helpers:

- `.section-reveal`
- `.section-reveal.is-active`
- reduced-motion fallback for reveal transitions

## Selectors Removed From `main.css`

- `.btn`
- early `.u-container` block
- `.u-container, .container`
- `.section`
- `.section--lined`
- `.section--lined::before`
- `.btn, .beslock-btn, .discover__btn`
- shared button hover/focus/active block for `.btn`, `.beslock-btn`, `.discover__btn`
- `.section-reveal`
- `.section-reveal.is-active`
- reduced-motion `section-reveal` override

## Bridges Preserved In `main.css`

- `product-card` CTA/cart/image/badge compatibility
- `hero__cta`
- hero/fallback/video transitions
- single-product layout + image safety rails
- header/footer visual behavior not yet migrated
- page-specific flex/grid/layout sections

## Enqueue Changes

`inc/core/enqueue.php` now loads these utility layers after `main.css` via `beslock-extra-style` dependency:

- `beslock-utilities-buttons`
- `beslock-utilities-layout-helpers`
- `beslock-utilities`

This keeps `main.css` operational while the canonical ownership moves into explicit utility surfaces.

## Validation

### Static validation

- No CSS errors in the new utility files.
- No CSS errors in `main.css` after removal.
- No PHP errors in `inc/core/enqueue.php` after enqueue changes.

### Runtime validation

- Homepage: utility stylesheets loaded after `main.css`.
- Homepage desktop: sticky header still reaches `.header--scrolled`.
- Homepage desktop: `.section-reveal` still activates on scroll.
- Homepage: product cards still render and CTA buttons keep `display:flex` and `text-decoration:none`.
- Homepage mobile: drawer still opens, backdrop still closes it, and scroll lock still applies.
- Product page: quantity controls and add-to-cart remain present.
- Cart page: cart row, coupon control, and checkout CTA remain present.
- Checkout page: checkout content still renders and contact-information surface remains present.

## Remaining `main.css` Ownership

`main.css` still owns:

- page-specific hero/discover/footer surfaces
- product-card compatibility not yet fully migrated
- single-product layout and Woo safety rails
- legacy component/layout bridges with uncertain dependency chains
- page-specific flex/grid blocks that are not true utilities

## Next Cleanup Candidates

1. Finish the remaining `product-card` spacing/grid fallback audit later in the file.
2. Split page-level hero/discover/footer surfaces into canonical component/layout owners.
3. Audit generic-looking flex/grid blocks section-by-section before moving any more layout helpers.
4. Delay Woo single-product safety rail cleanup until page parity is explicitly revalidated selector-by-selector.