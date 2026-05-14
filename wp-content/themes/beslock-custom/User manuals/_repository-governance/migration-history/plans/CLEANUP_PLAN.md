# BESLOCK Cleanup Plan

## Goal

This plan defines a safe consolidation order for BESLOCK without breaking the restored local runtime.

This is a sequencing document, not an authorization to delete everything immediately.

## Guardrails

- Do not remove active runtime routes.
- Do not remove `repo_portfolio` before every consumer is migrated.
- Do not change the Docker bootstrap contract unless the replacement is validated end to end.
- Do not delete SQL dumps from local developer machines automatically.
- Do not assume historical files are dead until their consumers are confirmed.
- Validate home, product, add-to-cart, cart, and checkout after each functional change.

## Current Known Runtime Facts

- Home works.
- Product pages work.
- Add to cart works.
- Cart works.
- Checkout works at `/finalizar-compra/`.
- `/checkout/` is not the canonical route in the current localized dataset.

## Phase 1: Freeze and Document

Objective: make the current system legible without changing behavior.

Actions:

- Keep `data/products.json`, theme `data/products.json`, and `repo_portfolio/products.json` in place.
- Keep theme `scripts/`, `import_logs/`, `debug/`, and `repo_portfolio/` intact.
- Document every known consumer of product JSON files.
- Document the current WooCommerce slugs and page IDs.
- Document which admin pages belong to the theme versus plugins.

Exit criteria:

- architecture baseline is written
- cleanup order is agreed
- runtime baseline is captured

## Phase 2: Establish One Canonical Catalog Source

Objective: make `data/products.json` the only approved source for catalog content changes.

Actions:

- Declare `data/products.json` as the canonical catalog source in docs and tooling.
- Audit every code path that still reads theme `data/products.json`.
- Add compatibility adapters where needed so old flows can still function while reading the root source.
- Stop introducing manual edits to theme-local product JSON files.

Concrete targets:

- migrate theme helper scripts away from `wp-content/themes/beslock-custom/data/products.json`
- remove new operational dependence on `wp-content/themes/beslock-custom/products.json`
- keep `repo_portfolio/products.json` as export output only

Risks:

- admin tools may silently depend on theme-local paths
- excerpt workflows may still assume export JSON is the working source

Validation:

- sync products from the canonical source
- validate product pages and excerpts after sync
- verify no consumer still requires manual edits in theme-local JSON files

## Phase 3: Collapse Competing Import Paths

Objective: reduce product ingestion to one supported mechanism.

Actions:

- Choose `beslock-product-sync` as the canonical importer.
- Audit `carga_portfolio_data.php` and related theme scripts.
- Decide whether those scripts become:
  - wrappers around the canonical importer
  - one-off migration tools
  - legacy tools to retire after migration
- Remove competing business logic from the theme critical path.

Candidate changes:

- move import logic out of theme admin pages
- keep only one supported product sync button/entrypoint
- stop having both plugin import and theme import paths create/update products independently

Risks:

- hidden admin workflows may still use theme tools
- image assignment and product metadata enrichment may be bundled into the old importer path

Validation:

- perform a clean sync from `data/products.json`
- verify prices, excerpts, gallery, badge, and product availability on the frontend

## Phase 4: Isolate Export and Recovery Responsibilities

Objective: make export tools clearly secondary to the canonical import path.

Actions:

- keep `beslock-portfolio-exporter` only for export, snapshot, recovery, or media assignment if still justified
- decide whether import code inside `beslock-portfolio-exporter` should be removed or explicitly marked legacy
- review whether SQLite export has any real consumer
- define whether backups belong in versioned project structure or a local ignored operational directory

Target state:

- exporter does not compete with the importer
- export files are outputs, not primary working data
- backup artifacts are preserved intentionally, not accidentally

Risks:

- `short-des-exporter` currently depends on export JSON
- operators may still use exporter import buttons out of habit

Validation:

- run export intentionally and confirm outputs are non-canonical snapshots
- confirm normal day-to-day catalog changes do not depend on export artifacts

## Phase 5: Consolidate Excerpt and Metadata Sync

Objective: stop using a separate excerpt pipeline tied to `repo_portfolio/products.json` unless there is a strong business reason.

Actions:

- review `short-des-exporter`
- review theme scripts that manipulate excerpts from theme-local JSON
- decide whether excerpt synchronization becomes part of canonical product sync
- if retained temporarily, point excerpt sync to `data/products.json` or to the canonical importer output instead of `repo_portfolio/products.json`

Preferred outcome:

- one sync path updates title, excerpt, price, gallery, badge, and related product metadata together

Risks:

- direct database update behavior in `short-des-exporter` may hide data mismatches
- excerpt structure may differ between export JSON and canonical JSON

Validation:

- compare frontend product excerpt output before and after consolidation
- verify WooCommerce admin data remains correct

## Phase 6: Reduce Theme Responsibility Surface

Objective: leave `beslock-custom` focused on presentation and WooCommerce UI behavior.

Actions:

- move non-presentational admin tools out of the theme where practical
- reduce `functions.php` to orchestration and theme bootstrap only
- converge on one enqueue pipeline
- keep WooCommerce presentation hooks in theme scope when they are truly view-related

Candidate items to relocate or retire later:

- import/export admin pages registered from the theme
- helper scripts under `scripts/`
- debug artifacts under `debug/`
- historical logs under `import_logs/`

Risks:

- some tools may be actively used during content operations
- moving code too early may break manual support workflows

Validation:

- home and product rendering remain unchanged
- cart and checkout remain stable
- assets are enqueued once and in the expected order

## Phase 7: Remove Legacy and Duplicate Artifacts

Objective: only after consumers are migrated, remove redundant files and paths.

Candidates for eventual removal or archival review:

- `wp-content/themes/beslock-custom/products.json`
- `wp-content/themes/beslock-custom/data/products.json`
- legacy import helpers that duplicate canonical sync
- `portfolio-product-sync` plugin directory if no environment still references it
- `repo_portfolio/products.sqlite` if confirmed unused
- stale backup artifacts such as `products_backup_latest.json.restored` if archived elsewhere
- stale logs from `import_logs/`
- stale debug files from `debug/`

Important rule:

No artifact should be deleted until its ownership and replacement path are explicit.

## Recommended Execution Order

1. Keep runtime stable and document the current system.
2. Declare `data/products.json` as canonical.
3. Redirect legacy readers to the canonical source with compatibility shims.
4. Collapse competing import paths into one supported importer.
5. Reclassify exporter output as backup/export only.
6. Consolidate excerpt sync into the canonical data pipeline.
7. Move non-presentational tools out of the theme.
8. Remove duplicates and legacy artifacts only after validation.

## Suggested Validation Checklist For Every Phase

- Home responds and renders expected hero/products sections.
- Product page renders gallery, price, excerpt, and add-to-cart.
- Add to cart updates cart count.
- Cart renders line items and totals.
- Checkout renders at `/finalizar-compra/`.
- `phpMyAdmin` remains available.
- No unexpected references to production URLs appear in rendered HTML.

## Near-Term Deliverables

The next implementation phase should produce these concrete outputs:

- migration map of every `products.json` consumer
- decision on the future of `short-des-exporter`
- decision on whether `beslock-portfolio-exporter` remains export-only
- plan to replace theme-local import scripts with canonical data adapters
- optional redirect or compatibility handling for `/checkout/` if developer ergonomics require it

## Non-Goals For This Phase

- deleting legacy files immediately
- rewriting the theme from scratch
- replacing WooCommerce
- changing product URL structure
- changing Docker bootstrap away from the current working import approach