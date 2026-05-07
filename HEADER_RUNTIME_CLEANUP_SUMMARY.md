# Header Runtime Cleanup Summary

## Scope

This pass cleaned residual header and drawer runtime ownership after the first safe header consolidation slice.

Goals for this phase were:

- keep the current UI and runtime parity
- remove dead or duplicated header/drawer ownership
- keep legacy selectors and compatibility classes intact
- progressively thin `main.js` into orchestration-only code

## Ownership Classification

### Active canonical ownership

Header sticky state is now owned by:

- `wp-content/themes/beslock-custom/assets/js/components/header.js`

Drawer state is now owned by:

- `wp-content/themes/beslock-custom/assets/js/components/mobile-drawer.js`

Shared orchestration still owned by `main.js`:

- section reveal init
- lazy images init
- logo TM init
- hero fallback init
- products-panel bridge that still relies on the legacy drawer CSS contract

### Compatibility bridges

These files are now explicit compatibility bridges instead of runtime owners:

- `wp-content/themes/beslock-custom/assets/js/header-state.js`
- `wp-content/themes/beslock-custom/assets/js/menu-products-mobile.js`

Each bridge now only exposes a deprecation marker under `window.beslock.legacy` and intentionally registers no listeners, observers, or state transitions.

### Dead runtime removed

Removed from `wp-content/themes/beslock-custom/assets/js/main.js`:

- dead sticky owner `headerBehaviorsInit()`
- dead drawer owner `mobileMenuInit()`
- orphan sticky helpers:
  - reload scroll-restoration helper
  - logo click override
  - drawer close fallback from the header block
- orphan drawer helpers:
  - per-element stored handler logic
  - dead focus-trap implementation for the old drawer path
  - stale escape handler wiring via `document._beslockEscHandler`
  - stale touch-swipe drawer handlers
  - stale link-close handler set for the legacy drawer owner
- noop compatibility function `revealObserverInit()`

### Remaining bridge logic in `main.js`

`productsPanelInit()` remains in `main.js`, but it no longer owns the drawer itself.

It now only:

- toggles products-panel visibility classes and aria state
- toggles `.products-open`, `.products-opening`, and `.products-closing`
- respects the current legacy CSS animation contract
- avoids reopening/closing the drawer, backdrop, or body scroll lock directly

## Files Touched

- `wp-content/themes/beslock-custom/assets/js/main.js`
- `wp-content/themes/beslock-custom/assets/js/menu-products-mobile.js`
- `wp-content/themes/beslock-custom/assets/js/header-state.js`
- `HEADER_RUNTIME_CLEANUP_SUMMARY.md`

## Listeners Removed

From the dead sticky block in `main.js`:

- 1 scroll listener
- 1 resize listener
- 1 pageshow listener
- 1 beforeunload listener
- 1 logo click override

From the dead drawer block in `main.js`:

- 1 toggle button click listener
- 1 close button click listener
- 1 backdrop click listener
- 1 document escape listener
- per-link close listeners for drawer links
- 3 swipe listeners on the drawer panel (`touchstart`, `touchmove`, `touchend`)

From legacy scripts converted to bridges:

- full legacy drawer listener tree in `menu-products-mobile.js`
- full legacy sticky listener tree in `header-state.js`
- legacy MutationObserver usage in `menu-products-mobile.js`

## Source-Level Cleanup Measurements

Confirmed removed from `main.js` by source search:

- `headerBehaviorsInit`
- `mobileMenuInit`
- `document._beslockEscHandler`
- `window.__beslock_menu_initialized`
- `closeDrawerIfOpen`
- `setScrollRestorationManualIfReload`
- `productsBack`
- `productsClose`
- `menuContent`

Redundant DOM queries removed from `main.js` included:

- header lookup for legacy sticky ownership
- logo anchor lookup for legacy click override
- legacy drawer element lookups for menu button, close button, backdrop, and drawer root
- unused products back/close/menuContent lookups

## Compatibility Preserved

This cleanup intentionally preserved:

- the existing visual behavior
- legacy classes such as `.header--scrolled`, `.is-open`, `.backdrop-visible`, `.products-open`
- existing ids and compatibility selectors
- WooCommerce and Kadence compatibility
- cart visibility behavior
- mobile drawer scroll-lock behavior
- escape-to-close behavior
- products subpanel animation contract

## Validation Performed

Editor diagnostics returned no errors for:

- `assets/js/main.js`
- `assets/js/menu-products-mobile.js`
- `assets/js/header-state.js`

Runtime validation confirmed:

- homepage loads only canonical header/drawer scripts
- legacy `header-state.js` is not loaded
- legacy `menu-products-mobile.js` is not loaded
- product page sticky transition still works
- product page cart remains visible
- cart page still renders header and cart count correctly
- checkout page still renders header/cart correctly
- mobile drawer open/close still works
- body scroll locking still works
- products subpanel still opens correctly
- products subpanel resets when the drawer closes
- `Escape` still closes the drawer and resets products state

## Remaining Technical Debt

- `productsPanelInit()` still lives in `main.js` because the products subpanel still depends on a legacy CSS state contract
- root-level `wp-content/themes/beslock-custom/inc/enqueue-assets.php` remains in the repository as a dormant legacy enqueue surface even though the active bootstrap uses `inc/core/enqueue.php` and a noop WooCommerce bridge
- the CSS side of header and drawer behavior is still distributed across multiple legacy files
- legacy bridge files remain in the repository to preserve path stability during the migration

## Future Safe Cleanup Candidates

- move the products-panel bridge from `main.js` into a dedicated component once the CSS contract is safe to componentize
- remove dormant legacy PHP enqueue surfaces after confirming nothing outside the current bootstrap includes them
- shrink dead comments and migration-era compatibility notes once the header migration is complete
- consolidate remaining header/drawer CSS ownership after runtime parity is preserved across all surfaces
