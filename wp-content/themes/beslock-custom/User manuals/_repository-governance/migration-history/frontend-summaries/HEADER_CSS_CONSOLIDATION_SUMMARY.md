# Header CSS Consolidation Summary

## Scope
First safe CSS ownership cleanup slice for the Header and Drawer surfaces under additive coexistence. This pass preserved the existing runtime contract, selectors, classes, IDs, WooCommerce/Kadence compatibility, and visual output.

## Files Touched
- `wp-content/themes/beslock-custom/assets/css/layout/header.css`
- `wp-content/themes/beslock-custom/assets/css/components/header.css`
- `wp-content/themes/beslock-custom/assets/css/menu-products-mobile.css`
- `wp-content/themes/beslock-custom/assets/css/main.css`
- `wp-content/themes/beslock-custom/assets/css/header-state.css`

## CSS Ownership Moved
### `assets/css/layout/header.css`
Now owns layout/runtime structure for header and drawer surfaces:
- fixed header shell and header bar positioning hooks
- drawer root positioning and pointer-event gating
- backdrop positioning hooks
- drawer panel positioning, width, display state, z-index, mobile full-width rules
- products panel structural positioning and scroll container behavior
- `.is-open`, `.products-open`, `.products-opening`, `.products-closing` layout/state hooks
- drawer menu hidden / close button visible behavior during products state

### `assets/css/components/header.css`
Now owns component visuals/behavior glue for header and drawer surfaces:
- sticky header transition and scrolled-state visual glue
- header logo transition glue
- cart icon cleanup and cart badge styling
- cart badge fallback specificity rules
- drawer header visual treatment
- drawer logo sizing/alignment
- drawer close button styling
- drawer backdrop color transition and visible state
- drawer panel visual surface
- products panel transition, hidden, visible, opening, open, and closing states
- document scroll lock rules for `html.has-drawer-open` and `body.drawer-no-scroll`

## Duplicated Rules Removed
### From `assets/css/menu-products-mobile.css`
Removed ownership that now lives in the header layout/component surfaces:
- drawer root/backdrop/panel structure
- drawer open state panel/backdrop behavior
- products panel hidden/visible/open/closing state blocks
- products-open menu/close visibility blocks
- drawer width expansion during products-open
- header/drawer scroll lock ownership
- drawer header / close button visual styling that duplicated the new component owner

### From `assets/css/main.css`
Removed duplicated header cart ownership after moving it into `components/header.css`:
- cart badge geometry and color block
- cart icon cleanup block
- cart icon pseudo-element suppression
- cart icon glyph alignment block
- cart badge desktop size fallback block
- cart badge extra-specificity fallback block

### `assets/css/header-state.css`
Neutralized into a deprecated comment-only legacy file so accidental re-enqueue cannot reintroduce sticky header ownership.

## Selectors Preserved For Compatibility
The following runtime selectors/classes/IDs were intentionally preserved:
- `.header--scrolled`
- `.is-open`
- `.products-open`
- `.products-opening`
- `.products-closing`
- `.backdrop-visible`
- `html.has-drawer-open`
- `body.drawer-no-scroll`
- `#mobileDrawer`
- `#productsToggle`
- `#productsPanel`
- `#drawerBackdrop`
- existing `.header__*`, `.mobile-drawer__*`, `.mobile-products-panel`, `.products-chevron`, `.drawer-header`, `.drawer__logo` selectors
- `data-js` hooks used by the consolidated header and drawer runtimes

## Visual Parity Validation
Validated against the local Docker WordPress/WooCommerce environment:
- Product page: sticky header still enters `.header--scrolled`
- Product page: cart badge remains visible with `18px x 18px` green badge styling
- Cart page: cart icon and badge remain visible
- Checkout page: cart remains visible and header hook is intact
- Drawer: open state still shows panel and backdrop, and still applies `html.has-drawer-open` / `body.drawer-no-scroll`
- Products subpanel: still opens with hidden main menu and visible close action once initialization settles
- Escape close: still closes drawer, unlocks scroll, and restores products panel hidden state

## Remaining CSS Debt
- `assets/css/main.css` still owns broader legacy header layout and logo rules outside this first safe slice
- `assets/css/wc-scope-fix.css` remains a real WooCommerce/Kadence compatibility layer and was intentionally not reduced in this pass
- `assets/css/menu-products-mobile.css` still owns drawer variables and menu/product-list visual skin
- `assets/css/models-mobile.css` still participates in products-panel visibility through `.models--hidden`, `.models--visible`, and `#productsPanel` state rules

## Future Safe Cleanup Candidates
- classify and trim remaining header layout/logo duplication still living in `assets/css/main.css`
- document `wc-scope-fix.css` as compatibility ownership vs cleanup target before removing anything from it
- evaluate whether products-panel state ownership can be simplified between `components/header.css` and `models-mobile.css`
- continue shrinking `menu-products-mobile.css` once menu-item visual ownership has a canonical home
