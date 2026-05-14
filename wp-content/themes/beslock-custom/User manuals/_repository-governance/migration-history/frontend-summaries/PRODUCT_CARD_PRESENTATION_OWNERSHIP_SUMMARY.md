# Product Card Presentation Ownership

## Goal

Move the remaining product-card presentation ownership out of storefront-scoped selectors in `assets/css/main.css` and into `assets/css/components/product-card.css` without redesigning the card or changing runtime behavior.

## What Moved

- Canonical component ownership now includes the effective homepage presentation values for:
  - content bottom padding
  - title spacing
  - price spacing and letter spacing
  - actions top spacing and internal gap
  - legacy `.product-card__btn--link` sizing
  - final cart CTA sizing via `a:last-child`
- Added a compatibility alias for legacy `.product-card__desc` inside the component stylesheet while keeping `.product-card__description` as the canonical render class.
- Removed duplicated presentation overrides from `assets/css/main.css` that were still winning through storefront scope or late cascade order.

## Validation

Homepage storefront card computed values remained aligned with the pre-migration baseline:

- title margin-bottom: `6px`
- title font-size: `18px`
- price margin-bottom: `14px`
- price font-size: `20px`
- content padding-bottom: `28.8px`
- actions margin-top: `10px`
- actions gap: `10px`
- primary CTA height: `48px`
- primary CTA left padding: `14px`
- cart CTA width: `52px`
- cart CTA height: `46px`

Cross-surface checks completed:

- homepage add-to-cart still increments the cart count
- empty-cart recommendations still render and keep cart-only spacing overrides
- single product page still renders gallery, price, and add-to-cart CTA
- checkout still renders its checkout surface

## Remaining Debt

- Cart-empty recommendation presentation still intentionally relies on cart-only overrides in `assets/css/main.css`.
- Legacy inactive files such as `assets/css/product-card-alt.css` and `assets/css/product-rotator.css` remain untouched in this slice.