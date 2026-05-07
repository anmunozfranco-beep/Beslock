# BESLOCK Frontend Architecture Audit

## Purpose

This document defines the current frontend architecture of the active BESLOCK child theme, the current separation of responsibilities, the main risk areas, and the target modular frontend direction.

This phase is documentation-first.

It does not authorize a full rewrite.

## Current Runtime Baseline

Validated against the current local Docker runtime:

- Home renders correctly at `http://localhost:8080/`.
- Product page renders correctly at `http://localhost:8080/producto/e-shield/`.
- Add to cart works from the product page.
- Cart works at `http://localhost:8080/carrito/`.
- Checkout works at `http://localhost:8080/finalizar-compra/`.
- Mobile home render is working with menu button, cart icon, and product cards visible.

This audit assumes the current visual output and user flows must remain stable.

## Frontend Responsibility Split

### Confirmed intended separation

`wp-content/themes/beslock-custom/woocommerce/`

- owns WooCommerce template overrides
- owns markup/render structure for WooCommerce pages and fragments
- should remain focused on HTML/PHP rendering only

`wp-content/themes/beslock-custom/inc/woocommerce/`

- owns hooks, filters, feature toggles, and WooCommerce integration logic
- should remain backend glue and integration orchestration
- should not own presentational markup or inline browser behavior

### Current reality

The separation exists conceptually, but it is not yet strict:

- render logic still leaks into templates through hardcoded rules and inline scripts
- frontend asset concerns are still spread between `functions.php`, `inc/core/enqueue.php`, `inc/woocommerce/enqueue-assets.php`, `header.php`, `footer.php`, and WooCommerce templates
- some WooCommerce logic is duplicated between `functions.php` and `inc/woocommerce/*`

## Current Theme Frontend Map

### Root templates

- `front-page.php`
- `header.php`
- `footer.php`
- `page.php`

### Frontend template directories

`template-parts/`

- partially component-oriented
- currently contains product and content fragments, but structure is still shallow

`templates/`

- contains alternate block-style templates and menu/mobile structures
- currently overlaps conceptually with `template-parts/`

`woocommerce/`

- contains WooCommerce overrides such as:
  - `single-product.php`
  - `content-product.php`
  - `cart/*`

### Assets

`assets/css/`

- contains a partially modular structure:
  - `base/`
  - `components/`
  - `layout/`
  - `pages/`
- also contains many flat feature files at the root of `assets/css/`

`assets/js/`

- contains multiple feature scripts
- lacks a stable top-level module taxonomy such as `core/`, `components/`, `woocommerce/`
- `main.js` still acts as a large multipurpose runtime entry with mixed responsibilities

## Current Enqueue Pipeline

### Active files

- `functions.php`
- `inc/core/enqueue.php`
- `inc/woocommerce/enqueue-assets.php`

### Current behavior

`functions.php`

- registers and enqueues `beslock-main-style`
- enqueues `assets/css/main.css`
- enqueues `assets/js/main.js`
- loads WooCommerce integration modules
- still contains additional WooCommerce logic and admin tooling, so it is not frontend-only

`inc/core/enqueue.php`

- enqueues a large set of CSS and JS files
- loads GSAP and ScrollTrigger from CDN
- enqueues page-sensitive and feature-sensitive scripts
- injects inline CSS and inline behavior through `wp_head`
- effectively acts as the real frontend asset pipeline

`inc/woocommerce/enqueue-assets.php`

- registers/enqueues WooCommerce-related CSS such as product-card assets
- introduces a second presentational enqueue surface for WooCommerce UI

### Architectural issue

There is no single authoritative frontend asset manifest.

The current pipeline is functional, but fragmented.

## Current Frontend Debt Patterns

### 1. Templates contain behavior

Examples:

- `header.php` contains inline JavaScript for logo measurement and CSS variable syncing
- `footer.php` contains multiple inline script blocks for header behavior, drawer fallback, and emergency recovery logic
- `woocommerce/single-product.php` contains inline tab behavior despite the existence of `assets/js/product-tabs.js`

### 2. Templates contain business-ish logic

Examples:

- `template-parts/product-card.php` contains hardcoded badge-product slug logic
- `front-page.php` contains fallback orchestration and dual template-path branching for hero/products/discover sections
- `woocommerce/content-product.php` injects context and forwards rendering to `template-parts/product-card.php`

### 3. CSS is partially modular but still coupled

Observed traits:

- BEM exists in some blocks: `product-card`, `product-page`, `product-tabs`, `header`
- legacy companion classes still coexist: `pc-card`, `pc-actions`, `pc-btn-main`, `pc-btn-cart`
- several CSS files operate as behavior patches or conflict suppressors instead of isolated components
- WooCommerce overrides rely on deep selectors and aggressive `!important`

### 4. JS is partially modular but not responsibility-separated

Observed traits:

- `main.js` mixes utilities, header behavior, mobile drawer, section reveal, and menu logic
- `header-state.js` overlaps conceptually with header logic already present elsewhere
- `product-tabs.js` exists, but the product template still ships its own inline tab logic
- fallback scripts in `footer.php` duplicate behavior already expected from bundled JS

### 5. Asset naming is feature-based, not architecture-based

Examples:

- `product-card-alt.css`
- `product-card-fade.css`
- `product-rotator.css`
- `menu-products-mobile.css`
- `models-mobile.css`

These files are understandable locally, but they do not yet form a scalable component taxonomy.

## Directory Audit By Area

## `/woocommerce`

### Current role

- template/render/markup layer for WooCommerce views

### Findings

- this should remain the primary override layer for WooCommerce HTML structure
- current overrides are acceptable as a render boundary
- problem appears when templates own behavior or hardcoded UI logic

### Key observations

- `single-product.php` contains custom layout and inline tabs script
- `content-product.php` delegates card rendering to a shared template part, which is a good direction
- cart templates are render-heavy as expected, but future componentization should keep them as markup composition only

## `/inc/woocommerce`

### Current role

- hook/filter/integration/backend glue layer

### Findings

- the intended boundary is correct and should be preserved
- current modules are already meaningfully separated by concern:
  - `setup.php`
  - `product-features.php`
  - `product-hooks.php`
  - `cart.php`
  - `enqueue-assets.php`

### Architectural conclusion

This is the correct place for:

- hook registrations
- WooCommerce support declarations
- text filters
- feature flags
- data-to-template preparation
- server-side view decisions

This is not the right place for template markup, inline browser behavior, or CSS rules.

## `/template-parts`

### Current role

- reusable render fragments

### Findings

- this is the best existing base for future component decomposition
- current structure is still transitional and shallow
- some parts are real components, others are page fragments

### Strong candidates already present

- product card
- product features
- hero-related content
- section-based homepage fragments

### Problem

The structure mixes reusable UI with page-specific fragments, and naming is not yet responsibility-driven.

## `/assets/css`

### Current state

- partially modular, partially legacy flat structure
- contains both architecture-friendly directories and ad hoc feature files

### Findings

- `components/` exists but does not yet contain the whole component surface
- `base/variables.css` and `layout/header.css` suggest intent, but the architecture is incomplete
- large frontend behavior still depends on `main.css` and several root-level files
- WooCommerce conflict-mitigation CSS lives as patch-style files, not as a clean layer

### Current CSS categories in practice

- global/base
- per-feature component CSS
- WooCommerce overrides
- responsive/mobile-specific feature CSS
- emergency compatibility CSS

## `/assets/js`

### Current state

- several useful feature files already exist
- top-level JS organization is still flat

### Findings

- some scripts are valid future component modules:
  - `product-tabs.js`
  - `product-quantity-controls.js`
  - `product-rotator.js`
  - `header-state.js`
- `main.js` is too central and should eventually become orchestration only
- duplicate or overlapping behavior still exists between entry scripts and inline scripts

## Reusable Component Candidates

These are the strongest candidates for future modular BEM ownership:

- header
- hero
- product-card
- product gallery
- product tabs
- quantity controls
- mobile drawer
- cart summary UI
- CTA/discover section
- product badge
- navigation/menu surface

## Current High-Risk Frontend Issues

### Inline JS

Current inline JS is one of the main blockers to strict responsibility separation.

Locations observed:

- `header.php`
- `footer.php`
- `woocommerce/single-product.php`
- `inc/core/enqueue.php` through injected head behavior

Why it is risky:

- duplicates bundled behavior
- makes debugging ownership harder
- makes partial component migration harder
- breaks the boundary between template and behavior

### CSS coupling

Examples:

- WooCommerce gallery override selectors are deep and defensive
- `product-widgets.css` behaves like a compatibility battlefield instead of a component stylesheet
- `main.css` still carries global resets, component styles, and layout behavior together

### Asset duplication and overlap

Examples:

- multiple product-card related CSS files
- multiple header behavior surfaces
- product-tabs behavior exists both inline and in a standalone script
- mobile drawer fallback behavior exists outside the main JS module structure

### Template logic leakage

Examples:

- hardcoded badge slugs in `template-parts/product-card.php`
- multi-path section rendering logic in `front-page.php`
- inline interaction behavior in WooCommerce templates

## Current BEM Status

### Already positive

The theme is not starting from zero.

It already contains meaningful BEM-style naming in parts of the frontend:

- `header__*`
- `product-card__*`
- `product-page__*`
- `product-tabs__*`

### What is missing

- a single official naming standard
- a rule for legacy class coexistence
- a canonical component folder layout
- explicit JS hook naming rules
- a formal utility layer and limits for its usage
- a migration strategy that protects WooCommerce/Kadence compatibility

## Target Frontend Architecture

The target architecture should be based on:

- BEM blocks as the primary UI unit
- mobile-first CSS layering
- JS modules attached to component responsibility, not page accidents
- template/render separated from hooks/integration logic
- progressive coexistence with legacy until each component is safely migrated

## Target Directory Structure

### CSS

`assets/css/`

- `core/`
  - tokens, variables, reset, typography, base primitives
- `layout/`
  - wrappers, grid, page scaffolding, structural layout rules
- `components/`
  - isolated BEM blocks such as header, hero, product-card, drawer, gallery, tabs, cart-summary, CTA
- `utilities/`
  - explicit opt-in helpers with low specificity and strong limits
- `woocommerce/`
  - WooCommerce-specific compatibility and component bridge styles

### JS

`assets/js/`

- `core/`
  - boot, dom helpers, event helpers, viewport helpers, state helpers
- `components/`
  - header, drawer, product-card, gallery, tabs, quantity-controls, hero behavior
- `woocommerce/`
  - WooCommerce-specific enhancements and adapters

### Templates

`template-parts/`

- `hero/`
- `cards/`
- `drawers/`
- `sections/`
- `navigation/`

This keeps reusable render fragments grouped by UI responsibility instead of historical location.

## Separation Model Going Forward

### Templates

Templates should own:

- semantic markup
- render structure
- interpolation of already-prepared values
- composition of template parts

Templates should not own:

- inline JS behavior
- hardcoded behavioral business rules
- DOM state recovery logic
- CSS variable mutation logic

### PHP integration modules

`inc/woocommerce/` should own:

- hook registration
- data shaping for templates
- WooCommerce customization glue
- feature toggles
- modifier/state decisions exposed to markup

### CSS

CSS should own:

- presentation
- responsive adaptation
- component variants via modifiers

CSS should not own:

- compatibility band-aids forever
- deep selector warfare as a permanent strategy

### JS

JS should own:

- behavior
- component state
- keyboard/accessibility interactions
- transitions and non-critical UI enhancement

JS should not own:

- layout compensation that belongs in CSS
- behavior duplicated inline in templates

## Component Migration Priorities

These components should migrate first because they offer the highest architectural gain with relatively controlled blast radius.

### 1. Header

Why first:

- currently split between CSS, `main.js`, `header-state.js`, `header.php`, and `footer.php`
- high visibility
- central to mobile drawer, sticky state, cart visibility, and logo sizing behavior

### 2. Product Card

Why first:

- already partially BEM
- reused in home/catalog/cart-empty related flows
- currently split across template logic and multiple CSS/JS variants

### 3. Gallery

Why first:

- WooCommerce conflict surface is high
- current styling relies on defensive overrides
- this is the most likely point of future WooCommerce/Kadence regressions

### 4. Mobile Drawer

Why first:

- behavior duplication currently exists
- strong need for a single ownership model
- core for mobile-first architecture

### 5. Cart UI

Why first:

- current runtime is stable
- cart templates are a clean candidate for compositional improvements without changing business logic

### 6. CTA / Discover Sections

Why first:

- relatively isolated from WooCommerce internals
- good low-risk candidates to establish block-level BEM conventions

## Components That Must Not Be Rewritten First

Avoid starting with:

- full WooCommerce template rewrites
- global reset rewrite
- complete asset pipeline replacement
- Kadence compatibility removal
- wholesale CSS flattening

That would increase risk before the architecture is stabilized.

## Strategic Rule For This Phase

No massive rewrite.

No visual change.

No runtime breakage.

The correct move is:

1. document current boundaries
2. formalize BEM rules
3. define migration order
4. migrate one component at a time behind the current runtime contract