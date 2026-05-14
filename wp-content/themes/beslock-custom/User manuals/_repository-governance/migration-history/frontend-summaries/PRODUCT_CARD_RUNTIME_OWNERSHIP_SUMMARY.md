# PRODUCT CARD Runtime Ownership Summary

## Scope

Next safe decomposition slice focused on separating product-card runtime ownership from storefront-specific ownership.

This pass did **not** redesign cards, change CTA hierarchy, alter storefront UX, or rewrite Woo templates.

The slice only moved active runtime visual bridges that were still coupled to storefront/recommendation wrappers into the canonical product-card component owner.

## Files Touched

- `wp-content/themes/beslock-custom/assets/css/components/product-card.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`

## Audit Classification

### Canonical product-card ownership

- card hover visual state via `.bes-product-card--hover`
- card root transition and shadow behavior
- image container structure
- rotator container and frame states
- alternate-image visibility states
- CTA alignment and button slot structure
- badge runtime visual behavior
- reduced-motion runtime fallbacks
- product-card JS initialization via `data-js="product-card"`

### Runtime visual ownership

- overflow visibility needed by badge/image runtime behavior
- image contain/positioning bridge for runtime card media
- content column flow for cards rendered through the product-card partial
- rotator width/min-width bridge for cards rendered through the product-card partial

### Storefront-only ownership left out of this slice

- storefront grid/layout ownership in `assets/css/layout/storefront.css`
- storefront spacing/layout wrappers

### Recommendation-only ownership left out of this slice

- recommendation layout ownership in `assets/css/layout/recommendations.css`
- empty-cart wrapper/grid structure

### Compatibility bridges preserved

- legacy `.product-card*` selectors still coexist with `.bes-product-card*`
- legacy `alt-visible` class still coexists with `bes-product-card__image--alt-visible`
- legacy rotator frame classes (`visible`, `is-active`) still coexist with `product-card__frame--active`
- older legacy asset files remain in the repo untouched as non-active compatibility surfaces

### Unsafe mixed ownership left in place

- storefront-scoped `.products-portfolio .product-card*` typography and CTA tuning in `main.css`
- Woo-sensitive sizing bridges in `main.css`
- older `style.css` product-card bridges
- any selector that still mixes product-card visuals with Woo/Kadence layout assumptions

### Woo-sensitive ownership left in place

- single-product image/layout safety rails
- cart and checkout rendering surfaces
- native Woo loops and their wrapper markup
- Kadence compatibility selectors

### Legacy hover/runtime ownership status

- `assets/js/components/product-card.js` is the active runtime owner
- `assets/css/product-rotator.css` and `assets/css/product-card-alt.css` are legacy/dead in the active homepage load path
- `inc/enqueue-assets.php` still references old product-card runtime assets, but the active load path is `inc/core/enqueue.php`

## Ownership Transferred

`assets/css/components/product-card.css` now owns the active runtime bridges that were still expressed through storefront/recommendation selectors in `main.css`:

- `[data-js="product-card"]`
- `[data-js="product-card"] .product-card__image`
- `[data-js="product-card"] .bes-product-card__image`
- `[data-js="product-card"] .product-card__image > img:not(.product-card__badge)`
- `[data-js="product-card"] .bes-product-card__image > img:not(.product-card__badge)`
- `[data-js="product-card"] .product-card__content`
- `[data-js="product-card"] .bes-product-card__content`
- `[data-js="product-card"] .product-card__image-rotator`
- `[data-js="product-card"] .bes-product-card .product-card__image-rotator`

This makes runtime ownership independent from `products-portfolio` and recommendation wrappers for cards rendered through the canonical component partial.

## Storefront/Runtime Separation

Before this slice, active runtime bridges still depended on selectors like:

- `.products-portfolio .product-card`
- `.products-portfolio .product-card__image`
- `.beslock-cart__recommendations .product-card`
- `.beslock-cart__recommendations .product-card__image`

After this slice, the active runtime bridges depend on the component anchor instead:

- `[data-js="product-card"]`

This keeps storefront and recommendations as context/layout owners while the card component owns its own runtime visual requirements.

## Selectors Removed From `main.css`

- `.products-portfolio .product-card`
- `.products-portfolio .product-card__image`
- `.beslock-cart__recommendations .product-card`
- `.beslock-cart__recommendations .product-card__image`
- `.products-portfolio .product-card__image > img:not(.product-card__badge)`
- `.beslock-cart__recommendations .product-card__image > img:not(.product-card__badge)`

## Validation

### Static validation

- No CSS errors in `components/product-card.css`.
- No CSS errors in `main.css` after removal.

### Runtime validation

- Homepage storefront: product-card component JS loads.
- Homepage storefront: product-card component CSS loads.
- Homepage storefront: cards initialize with `data-bes-product-card-ready="true"`.
- Homepage storefront: hover adds `.bes-product-card--hover`.
- Homepage storefront: card and image overflow remain `visible`.
- Homepage storefront: CTA container still computes to `display:flex` with the same gap.
- Empty-cart recommendations: cards initialize and hover with the same component runtime behavior.
- Empty-cart recommendations: overflow and CTA alignment remain intact.
- Mobile homepage: drawer state and scroll lock remain intact while product-card actions still render.
- Product page: quantity and add-to-cart remain present.
- Add-to-cart: cart indicator increments after adding `e-Shield`.
- Cart page with items: cart form, rows, and checkout CTA still render.
- Checkout page: Woo block checkout form still renders.

### Dataset gap

The current local dataset does **not** expose active `.product-card__image.has-alt` or `.product-card__image-rotator` surfaces on the tested homepage cards.

Because of that, alternate-image behavior and rotator transitions were validated by active asset ownership and DOM/runtime presence, but not by a visible live card instance in the current dataset.

## Remaining Mixed Ownership

- storefront-scoped `.products-portfolio .product-card__title/price/desc/actions` rules in `main.css`
- high-specificity `body .products-portfolio .product-card *` storefront tuning in `main.css`
- older `style.css` card image/badge bridges
- dormant legacy assets still referenced in `inc/enqueue-assets.php`
- Woo-sensitive max-width and layout bridges in `components/product-card.css` and `main.css`

## Future Cleanup Candidates

1. Audit the storefront-scoped typography/CTA tuning blocks in `main.css` and decide which belong to product-card component ownership versus storefront compatibility.
2. Remove or quarantine dead legacy runtime assets referenced only from `inc/enqueue-assets.php` once that enqueue path is confirmed inactive everywhere.
3. Revalidate alternate-image and rotator behavior against a dataset that actually renders `has-alt` or rotator frames before removing the last compatibility bridges.
4. Audit `style.css` product-card runtime bridges so the component stylesheet becomes the only active runtime visual owner.