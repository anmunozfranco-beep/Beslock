# MAIN CSS Decomposition Summary

## Scope

First safe decomposition slice for `wp-content/themes/beslock-custom/assets/css/main.css`.

This slice intentionally moved only clearly-owned product-card CTA/image/badge rules that were already duplicated by the canonical component stylesheet loaded later in the enqueue order.

## Files Touched

- `wp-content/themes/beslock-custom/assets/css/components/product-card.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`

## Ownership Changes

### Canonical owner reinforced

`wp-content/themes/beslock-custom/assets/css/components/product-card.css` now owns both the modern and compatibility product-card action surfaces:

- `.bes-product-card__button*`
- `.pc-btn-*`
- `.product-card__btn`
- `.product-card__btn--link`
- `.product-card__add-to-cart`
- `.product-card__actions .btn-primary`
- `.product-card__actions .btn-cart`

This keeps legacy selectors alive while consolidating ownership in the component stylesheet already enqueued after `main.css`.

### Removed from main.css

The following duplicated product-card blocks were removed from `main.css`:

- Early debug/legacy `.product-card__btn--link` block, including the temporary red border.
- Repeated `.product-card__actions` centered-layout override block.
- Repeated `.product-card__actions .btn-primary` / `.btn-cart` sizing blocks.
- Repeated product-card link reset block scoped to actions.
- Repeated `.product-card__image` / `img:not(.product-card__badge)` bridge block.
- Repeated `.product-card__badge` animation block and reduced-motion override.

## main.css Ownership Audit

### Canonical elsewhere now

- Header and drawer structure/state: `assets/css/layout/header.css`
- Header and drawer visual/state glue: `assets/css/components/header.css`
- Product-card CTA/image/badge/hover bridge: `assets/css/components/product-card.css`

### Compatibility bridge still intentionally in main.css

- Global tokens in `:root`
- Base reset/body defaults
- `.btn` utility base
- `.u-container` baseline
- Product-card price overlay positioning
- Older Woo/product-card fallback blocks that still need selector-by-selector verification
- Hero, discover, footer, section reveal, and general layout rules

### Waiting for later safe slices

- Remaining product-card blocks later in `main.css` around grid sizing, empty-cart recommendations, and old add-to-cart fallbacks
- Single-product layout rules that may still be acting as Woo/Kadence safety rails
- Global button/base utility extraction into a dedicated utilities stylesheet
- Hero/layout sections that should move only after ownership is mapped and later enqueue order is defined

### Unsafe for this slice

- WooCommerce/Kadence compatibility overrides without page-by-page proof
- Header/body offset and global stacking tokens
- Any selector still coupled to legacy templates outside the canonical product-card partial

## Validation

### Static validation

- CSS diagnostics: no errors in touched files.

### Runtime validation

- Homepage `http://localhost:8080/`: product cards still render with CTA and cart action links.
- Mobile homepage: drawer opens, backdrop becomes visible, and `drawer-no-scroll` / `has-drawer-open` contracts remain intact.
- Desktop homepage: sticky header still reaches `.header--scrolled` after scroll.
- Product page `http://localhost:8080/producto/e-shield/`: quantity controls and add-to-cart remain present.
- Cart `http://localhost:8080/carrito/`: cart row and checkout CTA remain present.
- Checkout `http://localhost:8080/finalizar-compra/`: checkout form still renders.

## Result

This slice made the `product-card` ownership transfer more real instead of nominal:

- duplicated rules were removed from `main.css`
- compatibility selectors were re-homed in the component owner
- no validated runtime regressions were introduced on the required surfaces

## Next Safe Candidates

1. Consolidate the remaining late-file product-card fallbacks that still duplicate card spacing/grid/button behavior.
2. Extract the generic `.btn` and container baseline into a dedicated utilities stylesheet once enqueue order is defined.
3. Audit single-product layout rules separately from shared product-card ownership so Woo safety rails are not removed accidentally.