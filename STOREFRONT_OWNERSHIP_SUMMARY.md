# STOREFRONT Ownership Summary

## Scope

Next safe `main.css` decomposition slice focused on storefront ownership and recommendation separation.

This slice treats `products-portfolio` as the canonical BESLOCK storefront/catalog surface, not as a homepage-only decorative block.

The goal of this pass was to separate:

- canonical storefront layout ownership
- reusable recommendation layout ownership
- homepage-only spacing ownership

without changing card design, CTA hierarchy, WooCommerce runtime behavior, or header/drawer ownership.

## Files Touched

- `wp-content/themes/beslock-custom/assets/css/layout/storefront.css`
- `wp-content/themes/beslock-custom/assets/css/layout/recommendations.css`
- `wp-content/themes/beslock-custom/assets/css/layout/homepage.css`
- `wp-content/themes/beslock-custom/assets/css/beslock-cart-empty.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- `wp-content/themes/beslock-custom/woocommerce/cart/cart-empty.php`

## Audit Classification

### Canonical storefront ownership

- `.products-portfolio`
- additive `.storefront`
- additive `.storefront-grid`
- storefront section spacing/layout for the site’s practical catalog surface
- storefront grid flex/wrap behavior used by the homepage catalog experience

### Reusable recommendation ownership

- `.beslock-cart__recommendations`
- additive `.recommendations-surface`
- additive `.recommendations-grid`
- recommendation wrapper spacing/layout for empty-cart product reuse
- reusable grid structure for recommendation cards without reclassifying them as storefront

### Homepage-only decorative ownership

- `.discover` spacing remains in `assets/css/layout/homepage.css`

### Product-card ownership kept out of this slice

- `.products-portfolio .product-card__title`
- `.products-portfolio .product-card__price`
- `.products-portfolio .product-card__desc`
- `.products-portfolio .product-card__actions`
- `.products-portfolio .product-card__btn*`
- product-card sizing/hover/CTA/icon rules already owned by `components/product-card.css` plus compatibility bridges in `main.css`

### Layout ownership transferred

- storefront wrapper spacing moved into `assets/css/layout/storefront.css`
- storefront grid layout moved into `assets/css/layout/storefront.css`
- recommendation wrapper layout moved into `assets/css/layout/recommendations.css`
- recommendation grid layout moved into `assets/css/layout/recommendations.css`

### Compatibility bridges preserved

- `.products-portfolio` remains on both storefront and recommendation grids as a legacy alias where needed
- product-card overflow/image bridges scoped to `.products-portfolio` and `.beslock-cart__recommendations` stay in `main.css`
- storefront-scoped product-card tuning blocks stay in `main.css`
- WooCommerce/Kadence-sensitive card sizing bridges stay in `main.css` and `components/product-card.css`

### Unsafe mixed ownership left in `main.css`

- storefront-scoped product-card typography and CTA sizing blocks
- shared `.product-card` sizing that still affects storefront and Woo contexts together
- mixed storefront/recommendation card bridges touching image overflow and badge behavior

### Woo-sensitive ownership left in place

- non-empty cart layout
- checkout block styling/runtime
- single-product safety rails
- native Woo cross-sells loop output
- Kadence/Woo compatibility selectors

## Why No `catalog-grid.css`

This slice did **not** create `assets/css/layout/catalog-grid.css`.

Reason:

- the storefront grid and recommendation grid do not currently share the same computed layout
- storefront computes to flex-wrap catalog rows
- empty-cart recommendations compute to a Woo-specific grid layout

Creating a fake shared grid owner here would have mixed two behaviors that are currently distinct and working.

## Ownership Changes

### Storefront ownership transferred

`assets/css/layout/storefront.css` now owns:

- `.products-portfolio`
- `.storefront`
- `.products-portfolio.storefront .products-portfolio__grid`
- `.storefront-grid`

### Recommendation ownership separated

`assets/css/layout/recommendations.css` now owns:

- `.beslock-cart__recommendations`
- `.recommendations-surface`
- `.recommendations-grid`

### Template markup made explicit

The catalog and recommendation surfaces now carry additive class names so layout ownership is explicit and future slices do not need to infer intent from `products-portfolio__grid` alone.

- storefront template adds `.storefront` and `.storefront-grid`
- empty-cart template adds `.recommendations-surface` and `.recommendations-grid`

## Removed From Legacy Owners

### Removed from `main.css`

- early `.products-portfolio__grid` grid block
- `.woocommerce .products-portfolio__grid` duplicate grid block
- late `.products-portfolio__grid` flex/wrap block
- duplicate `.products-portfolio` margin-top block

### Removed from `homepage.css`

- `.products-portfolio` spacing, because storefront is not homepage-only

### Removed from `beslock-cart-empty.css`

- `.beslock-cart__recommendations` layout block, now owned by `recommendations.css`

## Enqueue Changes

`inc/core/enqueue.php` now loads after `main.css`:

- `beslock-storefront-layout`
- `beslock-recommendations-layout`

This keeps the new layout owners explicit and later in the cascade than `main.css`.

## Validation

### Static validation

- No CSS errors in the new layout files.
- No CSS errors in `main.css` after selector removal.
- No PHP errors in the touched templates or enqueue file.

### Runtime validation

- Homepage desktop: `.products-portfolio storefront` and `.storefront-grid` render and load with the new storefront owner.
- Homepage desktop: storefront grid still computes to `display:flex`, `flex-wrap:wrap`, `gap:32px`.
- Homepage desktop: card width and CTA alignment remain intact.
- Homepage mobile: drawer still opens and `drawer-no-scroll` / `has-drawer-open` still apply.
- Empty-cart recommendations: recommendation wrapper and recommendation grid render with new additive classes.
- Empty-cart recommendations: wrapper still computes to grid, inner recommendation grid still computes to grid, CTA alignment remains intact.
- Product page: quantity control and add-to-cart button remain present.
- Add-to-cart: adding `e-Shield` still increments the cart indicator.
- Cart page with items: cart form, cart rows, and checkout CTA still render.
- Checkout page: loads the Woo block checkout surface (`wc-block-components-form wc-block-checkout__form`) with contact, shipping, and payment sections.
- Footer remains present on homepage, cart, product, and checkout.

## Remaining `main.css` Debt

- storefront-scoped product-card refinements still mixed with component ownership
- shared `.product-card` sizing that still affects Woo and storefront contexts together
- overflow/image compatibility bridges shared between storefront and recommendations
- unresolved interactions with `product-rotator.css` and `product-card-alt.css` on storefront cards
- older Woo-sensitive catalog bridges not yet isolated into explicit owners

## Future Cleanup Candidates

1. Audit the storefront-scoped `.product-card*` blocks in `main.css` and determine which belong in `components/product-card.css` versus a storefront compatibility layer.
2. Audit `product-rotator.css` and `product-card-alt.css` to determine whether their `products-portfolio` selectors are storefront ownership or card behavior ownership.
3. Keep native Woo loops like cross-sells separate until their markup is intentionally normalized.
4. Revisit shared card sizing only after storefront and recommendation card-slot requirements are proven identical.