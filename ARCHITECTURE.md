# BESLOCK Architecture Audit

## Purpose

This document captures the current runtime architecture of BESLOCK on branch `Refac_hero_Beslock`, the main structural problems detected during the restoration/bootstrap phase, and the target consolidation direction.

The goal is to define boundaries before refactoring. This document does not authorize aggressive cleanup by itself.

## Current Runtime Baseline

Validated locally against the Docker stack:

- Home responds on `http://localhost:8080/`.
- Product pages respond on `http://localhost:8080/producto/<slug>/`.
- Add to cart works from product pages.
- Cart works on `http://localhost:8080/carrito/`.
- Checkout is not broken, but its canonical local route is `http://localhost:8080/finalizar-compra/`.
- `http://localhost:8080/checkout/` returns `404` because WooCommerce is configured with the localized checkout page slug `finalizar-compra`.
- phpMyAdmin works on `http://localhost:8081/`.
- The restored production child theme is active: `wp-content/themes/beslock-custom`.
- WooCommerce is active.

## Top-Level Architecture

The project currently has four major concerns living in parallel:

1. Infrastructure and bootstrap
2. Runtime WordPress content and plugins
3. Theme UI and product presentation
4. Product catalog sync/import/export tooling

Those concerns are not cleanly separated yet.

## Infrastructure Boundary

Infrastructure currently lives at repository root:

- `docker-compose.yml`
- `docker/`
- `.env`
- `database/`
- `data/`

### Current behavior

- Docker provisions `mysql`, `wordpress`, `phpmyadmin`, and `wpcli`.
- The SQL dump is imported through MySQL init bootstrap.
- `docker/bootstrap-wordpress.sh` runs a WordPress post-import normalization step.
- Bootstrap performs search-replace from production URL to local URL.
- Bootstrap updates `home` and `siteurl`.
- Bootstrap normalizes the legacy plugin slug `portfolio-product-sync/portfolio-product-sync.php` to `beslock-product-sync/beslock-product-sync.php` in `active_plugins`.

### Infrastructure contract

Infrastructure should own only:

- Local environment startup
- Database bootstrap/import
- Environment-specific URL normalization
- Environment configuration

Infrastructure should not own business logic, product transformation rules, or theme-specific admin tooling.

## Data Boundary

### Current product data files

There are currently multiple product JSON files in the repository:

- `data/products.json`
- `wp-content/themes/beslock-custom/data/products.json`
- `wp-content/themes/beslock-custom/products.json`
- `wp-content/themes/beslock-custom/repo_portfolio/products.json`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json`

There is also a SQLite artifact:

- `wp-content/themes/beslock-custom/repo_portfolio/products.sqlite`

### Current consumers

- `wp-content/plugins/beslock-product-sync/beslock-product-sync.php` reads `ABSPATH . 'data/products.json'`.
- `wp-content/plugins/beslock-portfolio-exporter/beslock-portfolio-exporter.php` prefers root `data/products.json`, then theme `data/products.json`, then `repo_portfolio/products.json`.
- `wp-content/plugins/short-des-exporter/short-des-exporter.php` reads `wp-content/themes/beslock-custom/repo_portfolio/products.json` directly.
- `wp-content/themes/beslock-custom/scripts/carga_portfolio_data.php` reads `wp-content/themes/beslock-custom/data/products.json`.
- Several theme helper scripts also read `wp-content/themes/beslock-custom/data/products.json`.

### Architectural conclusion

The repository currently has no single enforced source of truth for catalog data.

### Proposed source of truth

The official source of truth for catalog content should be:

- `data/products.json`

Reasoning:

- It is outside the theme, so it is not coupled to presentation.
- It is already used by the modernized `beslock-product-sync` plugin.
- It aligns with local bootstrap and repository-level workflows.
- It is the safest future boundary for imports, exports, QA diffs, and automation.

### Proposed data ownership model

- `data/products.json`: canonical editable catalog source.
- `wp-content/themes/beslock-custom/repo_portfolio/`: legacy/export compatibility zone only.
- `wp-content/themes/beslock-custom/data/`: transitional legacy input zone to be retired.
- `wp-content/themes/beslock-custom/products.json`: likely legacy duplicate, not a canonical source.

## Theme Boundary

The active runtime theme is:

- `wp-content/themes/beslock-custom`

### What the theme should own

- Templates and template parts
- Frontend CSS/JS assets
- Theme-level WooCommerce presentation hooks
- Visual composition for home, product, cart, checkout, and marketing pages

### What the theme currently also owns, but should not own long term

- Import admin tools
- Export admin tools
- Product data helper scripts
- Import logs and debug artifacts
- Data duplication under theme-local folders

### Current theme structure risks

- `functions.php` is acting as both runtime bootstrap and tools registry.
- Theme admin pages register data/import tooling that overlaps plugin responsibilities.
- The theme contains historical scripts under `scripts/`, operational logs under `import_logs/`, and debug artifacts under `debug/`.
- Theme-local data files make presentation code responsible for product persistence concerns.

## Plugin Boundary

### Current plugin roles

`beslock-product-sync`

- Intended modern sync/import plugin.
- Reads root `data/products.json`.
- Best candidate to become the only supported product ingestion path.

`beslock-portfolio-exporter`

- Exports WooCommerce products to `repo_portfolio/products.json` and optionally `products.sqlite`.
- Also contains import functionality and image-related operations.
- Currently mixes export, import, recovery, and media-assignment responsibilities.

`short-des-exporter`

- Reads `repo_portfolio/products.json` directly.
- Updates WooCommerce excerpts with SQL-style direct database operations.
- Hard-coupled to theme path structure.

`portfolio-product-sync`

- Legacy plugin slug still handled during bootstrap.
- Exists only for backward compatibility with historical database/plugin state.

### Plugin direction

Long term, plugins should own domain behavior and automation, while the theme only owns presentation.

Proposed plugin responsibility split:

- `beslock-product-sync`: canonical importer from `data/products.json` into WooCommerce.
- `beslock-portfolio-exporter`: optional exporter/recovery tool only, with no competing import path.
- `short-des-exporter`: either absorb into the canonical sync pipeline or keep only as a temporary compatibility bridge.

## WooCommerce and Kadence Dependencies

### Current dependencies

- Kadence parent theme is required as the base parent theme.
- `beslock-custom` is the active child theme.
- WooCommerce is required for product runtime.

### Current behavior

- The child theme customizes WooCommerce presentation heavily.
- The child theme dequeues or overrides parts of Kadence styling.
- The child theme includes WooCommerce hooks for shop/cart/product behavior.
- Shop behavior is intentionally redirected toward the front page products section.

### Important runtime detail

The current localized page structure matters:

- Cart page slug: `carrito`
- Checkout page slug: `finalizar-compra`
- Account page slug: `mi-cuenta`

Any refactor must preserve these runtime routes or add explicit redirect compatibility.

## Frontend Asset Pipeline

### Current state

The live enqueue pipeline is centered on:

- `wp-content/themes/beslock-custom/functions.php`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

There is also a legacy duplicate file still present:

- `wp-content/themes/beslock-custom/inc/enqueue-assets.php`

### Observed issue

The theme historically had duplicate enqueue logic and duplicate `main.js` loading. That was stabilized during restoration, but the structure is still fragmented.

### Direction

The theme should converge on one authoritative asset pipeline:

- one entrypoint for theme asset registration
- one place for conditional page-specific enqueues
- no duplicated fallback pipelines living in parallel

## Current Sync and Import Topology

The catalog pipeline is currently fragmented:

1. Root `data/products.json` feeds `beslock-product-sync`.
2. Theme `data/products.json` feeds `carga_portfolio_data.php` and related helper scripts.
3. `beslock-portfolio-exporter` can write `repo_portfolio/products.json` from the WooCommerce database.
4. `short-des-exporter` consumes `repo_portfolio/products.json` to update excerpts.

This creates multiple competing flows:

- source JSON to WooCommerce
- WooCommerce back to export JSON
- export JSON back into WooCommerce excerpts
- theme-local JSON importing in parallel

This is the main architectural problem in the repository.

## Logs, Debug, and Operational Artifacts

The theme currently contains operational artifacts:

- `wp-content/themes/beslock-custom/import_logs/`
- `wp-content/themes/beslock-custom/debug/`
- backup data under `repo_portfolio/`

These artifacts are useful for recovery and audit today, but they should not remain first-class runtime concerns inside the theme forever.

### Proposed ownership

- Keep them for now during consolidation.
- Treat them as legacy operational evidence.
- Move active logs to a non-theme operational path in a later phase.
- Retain only the minimum compatibility surface needed by runtime tools.

## Target Architecture

### Root

Root should own repository-level concerns:

- infrastructure
- environment bootstrap
- canonical shared data
- project documentation

### Theme

The theme should own only presentation:

- templates
- assets
- theme hook orchestration
- view-layer WooCommerce customizations

### Plugins

Plugins should own application/domain behaviors:

- product synchronization
- export/recovery workflows
- admin tooling that manipulates catalog data
- excerpt synchronization if still needed

### Proposed catalog flow

Target flow:

1. Edit `data/products.json`.
2. Run one canonical sync/import mechanism.
3. Persist runtime products in WooCommerce.
4. Use exporter only for backup/recovery or explicit snapshots.
5. Remove theme-local import logic from the critical path.

## Compatibility Constraints

These constraints must be preserved during consolidation:

- Do not break the current Docker bootstrap workflow.
- Do not commit SQL dumps.
- Do not remove `repo_portfolio` until all consumers are migrated.
- Do not remove theme-local scripts before documenting which admin flows still depend on them.
- Do not assume `/checkout/` is canonical; the live local checkout slug is `/finalizar-compra/`.
- Do not break current product permalinks under `/producto/<slug>/`.

## Consolidation Decisions

### Accepted working decisions

- Canonical catalog source: `data/products.json`
- Canonical checkout route in local runtime: `/finalizar-compra/`
- Theme remains active and stable during documentation-first consolidation.
- `repo_portfolio` remains as a compatibility/export zone for now.

### Deferred decisions

- Whether `short-des-exporter` should be deleted or absorbed.
- Whether `beslock-portfolio-exporter` should keep import capabilities.
- Whether theme helper scripts should become CLI tools or plugin-admin tools.
- Whether SQLite export is worth preserving.

## Immediate Architectural Risks

- Multiple competing product import paths can drift catalog state.
- Excerpt sync depends on a theme-local export file instead of the canonical source.
- Theme contains operational scripts and logs that obscure its runtime responsibility.
- Legacy plugin compatibility still exists in bootstrap, indicating historical data drift.
- Route assumptions around checkout can cause false-positive debugging if English slugs are used.

## Recommended Principle for Next Changes

Consolidate behavior first, then remove files.

That means:

- document consumers
- redirect all live consumers toward canonical sources
- validate runtime after each consolidation step
- only then retire duplicates and legacy artifacts