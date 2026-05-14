# BESLOCK Component Migration Plan

## Goal

This plan defines the safest frontend migration order for BESLOCK toward a modular BEM architecture.

This phase does not migrate everything.

This phase defines the order, scope, risks, and validation gates.

## Guardrails

- no visual redesign in this phase
- no mass CSS rewrite
- no WooCommerce rewrite
- no Kadence compatibility breakage
- no template deletion until replacement ownership is verified
- no legacy file deletion until consumers are migrated

## Runtime Baseline To Protect

Validated current flows:

- home works
- product page works
- add to cart works
- cart works
- checkout works at `/finalizar-compra/`
- mobile home render works

Every migration slice must preserve these.

## Migration Principles

1. isolate one component at a time
2. separate ownership before deleting legacy
3. move behavior out of templates before restructuring markup aggressively
4. prefer compatibility layers over hard replacements
5. finish one component end to end before widening scope

## Current Priority Order

## Phase 0: Frontend Freeze And Mapping

Objective:

- lock the architecture direction before implementation churn

Actions:

- keep current frontend runtime unchanged
- use this plan plus `FRONTEND_ARCHITECTURE.md` and `BEM_GUIDELINES.md` as the source of migration rules
- confirm which legacy classes must temporarily coexist with BEM classes

Exit criteria:

- architecture approved
- naming approved
- migration order approved

## Phase 1: Pipeline Consolidation Without Visual Change

Objective:

- reduce frontend ownership confusion before touching component markup

Targets:

- `functions.php`
- `inc/core/enqueue.php`
- `inc/woocommerce/enqueue-assets.php`

Actions:

- document one authoritative frontend enqueue surface
- stop adding new inline scripts in templates
- define future target folders for CSS and JS without moving everything yet
- identify duplicated asset registrations and overlapping behavior modules

Important note:

This phase may still leave legacy files in place.

The goal is clarity, not destruction.

Validation:

- home
- product page
- add to cart
- cart
- checkout
- mobile home

## Phase 2: Header Component First

Why first:

- highest cross-cutting debt
- currently split across template, CSS, JS, and inline fallbacks
- affects every page and mobile drawer behavior

Current issues to solve:

- inline JS in `header.php`
- inline JS in `footer.php`
- overlap between `main.js` and `header-state.js`
- emergency runtime restore logic in footer
- logo measurement/state logic spread across template and JS

Desired outcome:

- one header block
- one header behavior module
- no inline header behavior in templates
- drawer and sticky state owned by explicit modules

Safe migration steps:

1. define canonical header block and element names
2. introduce `data-js` hooks without removing legacy classes
3. move inline header logic into header-related JS module
4. keep markup stable while reducing duplicate behavior
5. remove template inline scripts only after parity validation

Validation:

- header visible on home/product/cart/checkout
- menu button works on mobile
- cart icon remains visible
- no regression in sticky behavior

## Phase 3: Product Card Component

Why second:

- already partially BEM
- reused in several storefront contexts
- currently mixes BEM and legacy class systems
- template still contains hardcoded badge logic

Current issues to solve:

- `.product-card` coexists with `pc-card` style aliases
- actions use legacy names such as `pc-actions`, `pc-btn-main`, `pc-btn-cart`
- badge logic is hardcoded in the template
- styles are split across product-card and variant files

Desired outcome:

- one block contract for product-card
- server-side badge decision moved out of the template body
- variants expressed as modifiers, not parallel pseudo-components

Safe migration steps:

1. define final block API for product-card
2. keep legacy classes as bridge classes temporarily
3. move badge decision to PHP integration layer or filtered data source
4. collapse action/button naming into element/modifier rules gradually
5. consolidate style ownership after markup compatibility is stable

Validation:

- home product grid
- empty-cart upsell/product recommendations if applicable
- product links
- add-to-cart links
- mobile card render

## Phase 4: Product Gallery And Product Tabs

Why third:

- this is the highest WooCommerce/Kadence compatibility risk surface after the header
- current implementation relies on aggressive CSS overrides and duplicated tab behavior

Current issues to solve:

- inline tabs script in `woocommerce/single-product.php`
- separate `product-tabs.js` module already exists
- WooCommerce gallery styling depends on deep selectors and `!important`
- gallery behavior and layout are not yet isolated as a clear component

Desired outcome:

- one product-tabs behavior source
- one product-gallery ownership surface
- WooCommerce compatibility styles contained in a dedicated bridge layer

Safe migration steps:

1. keep current markup structure stable
2. remove duplicate inline tab behavior only after JS module parity is verified
3. identify gallery markup contract that must remain WooCommerce-compatible
4. isolate compatibility CSS from component CSS
5. progressively reduce selector depth where safe

Validation:

- product image gallery
- gallery navigation
- tabs switching
- add-to-cart area
- mobile product page

## Phase 5: Mobile Drawer / Navigation Surface

Why fourth:

- central to mobile-first architecture
- currently split between primary JS and fallback JS
- strong need for one interaction model

Current issues to solve:

- fallback drawer code in `footer.php`
- menu behavior overlap with `main.js`
- unclear distinction between navigation render and drawer behavior ownership

Desired outcome:

- one drawer block
- one navigation render surface
- one JS owner for open/close/focus/escape/backdrop logic

Safe migration steps:

1. define drawer markup contract
2. introduce `data-js` hooks on existing markup
3. move duplicated fallback logic into one owned module
4. remove fallback inline scripts only after parity verification

Validation:

- menu open/close
- backdrop close
- keyboard escape
- scroll lock behavior
- mobile navigation links still work

## Phase 6: Cart UI Components

Why fifth:

- cart runtime is already stable
- cart UI is a strong candidate for clearer render/styling separation
- most cart business logic is already owned by WooCommerce and integration hooks

Targets:

- cart summary
- cart totals
- cross-sells block
- empty-cart presentation

Desired outcome:

- cart-related BEM blocks around WooCommerce render structure
- keep WooCommerce business behavior intact
- style composition separated from backend glue

Validation:

- line items
- quantity controls
- totals
- shipping UI
- proceed to checkout link

## Phase 7: Hero And CTA Sections

Why sixth:

- lower compatibility risk than deep WooCommerce internals
- good candidates to normalize BEM and folder conventions
- useful for establishing section/component standards across the homepage

Targets:

- hero
- discover / CTA section
- home section wrappers

Desired outcome:

- section-level blocks in `template-parts/sections/`
- hero-specific block under `template-parts/hero/`
- clear separation between section layout and reusable child components

Validation:

- home desktop
- home mobile
- hero interactions
- CTA spacing and alignment

## Legacy Management Strategy

### Allowed during migration

- duplicate classes on the same node
- compatibility CSS bridge files
- WooCommerce-specific override layer while component CSS is being introduced
- temporary coexistence of old and new JS hook surfaces

### Not allowed during migration

- deleting legacy selectors before new selectors own the same surface
- removing inline logic before equivalent module behavior is verified
- renaming class APIs across many templates in one sweep
- mixing visual redesign with architectural migration

## Recommended Target Structure

### CSS

`assets/css/core/`

- tokens
- reset
- typography
- primitives

`assets/css/layout/`

- wrappers
- grid
- section shells

`assets/css/components/`

- header
- hero
- product-card
- product-gallery
- product-tabs
- mobile-drawer
- cart-summary
- cta-section

`assets/css/utilities/`

- explicit low-level helpers only

`assets/css/woocommerce/`

- WooCommerce bridge and compatibility styles

### JS

`assets/js/core/`

- boot
- dom helpers
- event helpers
- viewport helpers

`assets/js/components/`

- header
- mobile-drawer
- product-card
- product-gallery
- product-tabs
- quantity-controls
- hero

`assets/js/woocommerce/`

- WooCommerce-specific enhancements only

### Template Parts

`template-parts/hero/`

- hero render pieces

`template-parts/cards/`

- product-card and other card patterns

`template-parts/drawers/`

- mobile drawer pieces

`template-parts/sections/`

- page section blocks such as discover/CTA

`template-parts/navigation/`

- nav fragments and menu structures

## Validation Checklist For Every Migration Slice

- home renders correctly
- product page renders correctly
- add to cart works
- cart works
- checkout renders correctly at `/finalizar-compra/`
- mobile home still shows menu button, cart icon, and product cards
- no visual regression introduced unintentionally

## Non-Goals For The Next Phase

- rewriting all WooCommerce templates
- collapsing all CSS into new folders immediately
- deleting legacy CSS files wholesale
- changing the design system visually
- replacing WooCommerce/Kadence assumptions in one move

## Immediate Next Implementation Recommendation

Start with a small, reversible header consolidation slice.

That slice should:

1. formalize the header block contract
2. add `data-js` hooks without changing the visual layer
3. move inline header behavior into owned JS
4. validate all pages and mobile
5. only then remove redundant inline header scripts