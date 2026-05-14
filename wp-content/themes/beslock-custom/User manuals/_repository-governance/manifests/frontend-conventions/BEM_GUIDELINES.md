# BESLOCK BEM Guidelines

## Purpose

This document defines the official frontend naming and modularization rules for BESLOCK.

These guidelines are designed to coexist with the restored theme during migration.

They do not require deleting legacy classes immediately.

## Core Principles

- preserve current visuals unless a change is explicitly approved
- keep WooCommerce and Kadence compatibility intact
- prefer additive migration over destructive rewrite
- one component, one block, one responsibility
- templates render, CSS styles, JS behaves, PHP glue integrates

## Official Naming Convention

### Block

Format:

- `.block-name`

Rules:

- block names are lowercase
- words are separated with hyphens
- block names describe responsibility, not location

Examples adapted to BESLOCK:

- `.site-header`
- `.hero-banner`
- `.product-card`
- `.product-gallery`
- `.mobile-drawer`
- `.cart-summary`
- `.cta-section`

### Element

Format:

- `.block-name__element-name`

Rules:

- elements must belong to a block
- elements cannot be reused outside the block contract by name alone
- do not style naked child structure when an element name is possible

Examples:

- `.site-header__logo`
- `.site-header__menu-button`
- `.product-card__image`
- `.product-card__price`
- `.product-gallery__slide`
- `.cart-summary__total`
- `.mobile-drawer__backdrop`

### Modifier

Format:

- `.block-name--modifier`
- `.block-name__element-name--modifier`

Rules:

- modifiers change presentation or state variant
- modifiers must never replace the base block or element class

Examples:

- `.site-header--compact`
- `.product-card--featured`
- `.product-card--fade`
- `.product-gallery__slide--active`
- `.cta-section--discover`

## State Classes

### JS-driven states

Use state classes with `is-` and `has-` prefixes.

Rules:

- JS state classes are global state signals, not BEM modifiers
- use them only for runtime state, never for static visual variation
- prefer attaching them to the owning block root

Examples:

- `.is-open`
- `.is-active`
- `.is-hidden`
- `.is-loading`
- `.has-error`
- `.has-items`

### When to use modifier vs state

Use modifier when:

- the variant is structural or design-defined
- the class should exist in server-rendered markup or static templates

Use state class when:

- JS toggles it at runtime
- the state is ephemeral or interactive

Example:

- `.product-card--featured` is a modifier
- `.is-active` on `.product-tabs__panel` is a runtime state

## JS Hook Naming

### Official JS hook prefix

Use `js-` prefixed classes for JavaScript hooks only.

Rules:

- JS hooks must not carry visual styling
- if a DOM node needs both style and behavior, give it both classes
- prefer data attributes when a hook is semantically stateful or configured

Examples:

- `.js-header-toggle`
- `.js-mobile-drawer`
- `.js-product-tabs`
- `.js-qty-control`

Recommended alternative for behavior targets:

- `data-js="header-toggle"`
- `data-js="product-tabs"`
- `data-js="mobile-drawer"`

### BESLOCK rule

For new code, prefer:

- BEM class for styling
- `data-js` for behavior targeting

Example:

```html
<button class="site-header__menu-button" data-js="drawer-toggle">
```

## Responsive Strategy

### Official rule

Use mobile-first CSS.

Rules:

- base styles target mobile first
- add enhancements progressively with `min-width` breakpoints
- avoid desktop-first overrides unless dealing with legacy compatibility only

### Breakpoint philosophy

Recommended working scale:

- base: mobile default
- `min-width: 768px` for tablet
- `min-width: 1024px` for desktop
- `min-width: 1280px` for wide desktop only when needed

### Responsive ownership

- component responsive rules live with the component when the behavior is local
- layout responsive rules live in `assets/css/layout/`
- utility breakpoints must remain rare and predictable

## Spacing Philosophy

### Official rule

Use a tokenized spacing system.

Recommended scale:

- `--space-2`: 0.125rem
- `--space-4`: 0.25rem
- `--space-8`: 0.5rem
- `--space-12`: 0.75rem
- `--space-16`: 1rem
- `--space-20`: 1.25rem
- `--space-24`: 1.5rem
- `--space-32`: 2rem
- `--space-40`: 2.5rem
- `--space-48`: 3rem

### Rules

- spacing belongs to the component boundary first
- use margin for relationships between siblings
- use padding for internal breathing room
- avoid arbitrary pixel values in new modules when a token exists

### Exception rule

If exact legacy geometry must be preserved during migration, keep the current value but annotate it as a candidate token in the migration ticket or follow-up phase.

## Utility Rules

### Official rule

Utilities are allowed, but must remain limited and low-specificity.

Use utilities for:

- wrappers and container width
- screen-reader visibility helpers
- one-off layout helpers with obvious generic meaning

Do not use utilities for:

- component-specific styling
- product-specific design exceptions
- JS state

Recommended utility prefixes:

- `.u-container`
- `.u-visually-hidden`
- `.u-text-center`
- `.u-stack-md`

### BESLOCK constraint

If a utility starts accumulating component-specific meaning, convert it into a proper block or element rule.

## CSS Specificity Rules

### Official rule

Keep selectors shallow.

Preferred order:

1. block
2. element
3. modifier
4. state

Avoid by default:

- deep descendant chains
- styling through page ancestry when a block modifier is possible
- `!important`

### `!important` rule

Allowed only for:

- controlled compatibility shims against WooCommerce/Kadence legacy selectors
- temporary migration bridge layers

Not allowed for:

- ordinary component implementation
- new module defaults

## Template Responsibility Rules

Templates may:

- render BEM classes
- render modifier classes from prepared PHP values
- compose template parts

Templates may not:

- embed inline scripts for component behavior
- hardcode catalog-specific business logic when a filter/hook is more appropriate
- mutate layout via emergency browser scripting

## JS Responsibility Rules

JS modules should:

- initialize one component or one explicit behavior surface
- bind through `data-js` or dedicated hook selectors
- toggle `is-*` or `has-*` state classes only where needed

JS modules should not:

- depend on unrelated page structures
- mutate styling that belongs in CSS if a class toggle is sufficient
- duplicate behavior already present in another component module

## Official Folder Ownership

### CSS

`assets/css/core/`

- tokens
- reset
- typography
- global primitives only

`assets/css/layout/`

- wrappers
- page shell
- grid and structural layout

`assets/css/components/`

- one file per BEM block when practical

`assets/css/utilities/`

- explicit opt-in helpers only

`assets/css/woocommerce/`

- compatibility bridge styles and WooCommerce-specific component surfaces

### JS

`assets/js/core/`

- bootstrap and shared helpers

`assets/js/components/`

- block-oriented behavior modules

`assets/js/woocommerce/`

- WooCommerce enhancement modules only

## BESLOCK Real-World Examples

### Header

Preferred:

```html
<header class="site-header site-header--transparent" data-js="site-header">
  <div class="site-header__bar u-container">
    <button class="site-header__menu-button" data-js="drawer-toggle"></button>
    <a class="site-header__logo" href="/"></a>
    <a class="site-header__cart" href="/carrito/"></a>
  </div>
</header>
```

Runtime state:

- `.site-header--transparent` for static design variant
- `.is-compact` or existing `.header--compact` equivalent for JS state only if standardized in migration

### Product Card

Preferred:

```html
<article class="product-card product-card--catalog">
  <div class="product-card__media">
    <img class="product-card__image" alt="">
    <span class="product-card__badge">Instalación incluida</span>
  </div>
  <h3 class="product-card__title"></h3>
  <p class="product-card__price"></p>
  <p class="product-card__description"></p>
  <div class="product-card__actions">
    <a class="product-card__cta button button--primary"></a>
    <button class="product-card__cart-button" data-js="add-to-cart"></button>
  </div>
</article>
```

### Product Tabs

Preferred:

```html
<section class="product-tabs" data-js="product-tabs">
  <div class="product-tabs__nav">
    <button class="product-tabs__tab is-active"></button>
    <button class="product-tabs__tab"></button>
  </div>
  <div class="product-tabs__panel is-active"></div>
  <div class="product-tabs__panel"></div>
</section>
```

### Mobile Drawer

Preferred:

```html
<aside class="mobile-drawer" data-js="mobile-drawer" aria-hidden="true">
  <div class="mobile-drawer__backdrop" data-js="drawer-close"></div>
  <div class="mobile-drawer__panel">
    <button class="mobile-drawer__close" data-js="drawer-close"></button>
    <nav class="mobile-drawer__nav"></nav>
  </div>
</aside>
```

## Migration Compatibility Rule

During migration, a node may temporarily carry both legacy and target classes.

Example:

```html
<div class="product-card pc-card">
```

This is allowed only as a bridge.

The end goal is to remove legacy aliases once the new block owns the component fully.

## Non-Negotiable Rule For This Phase

- do not rewrite the whole theme
- do not remove legacy CSS wholesale
- do not break WooCommerce templates
- do not break Kadence compatibility
- do not change visuals unless a migration task explicitly includes visual QA