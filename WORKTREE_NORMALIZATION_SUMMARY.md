# WORKTREE NORMALIZATION Summary

## Scope

Controlled audit of the BESLOCK theme worktree after the frontend migration
foundation and the bootstrap ownership consolidation.

This pass does not delete files, does not reset the repository, and does not
change runtime behavior. It only classifies the current repository state and
normalizes understanding of what is active, dormant, local-only, ignored, or
ambiguous.

## Current Worktree State

### Git state now

- Runtime visibility risk from local excludes was reduced in this slice by
	removing the excludes that hid `template-parts/` and `templates/`.
- The remaining local visibility review item in `.git/info/exclude` is the
	broad `assets/images/` exclusion.
- Current visible worktree noise outside the scope of this slice is generated
	artifact drift such as `debug/enqueued-styles.log`.

### Previous critical normalization finding

`.git/info/exclude` currently ignores:

- `wp-content/themes/beslock-custom/template-parts/`
- `wp-content/themes/beslock-custom/templates/`

Those paths contain active, versioned frontend source and should not be hidden
from future git adds in a local-only exclude file.

This is not breaking current tracking because the files are already committed,
but it is a real worktree normalization hazard for future edits and new files.

### Previously excluded active files

These files were hidden by local exclude rules before the exclude
normalization cleanup and were the reason for removing the dangerous local
exclude patterns:

- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`
- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/product-features.php`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`
- `wp-content/themes/beslock-custom/templates/models-mobile.php`

### Canonical but currently untracked

No canonical runtime assets appear to be currently untracked in the live
worktree. The risk is not missing tracked files; the risk is local exclude
policy hiding active source from future adds and reviews.

## Exclude Normalization Result

### Removed local excludes

The following local-only excludes were removed from `.git/info/exclude` in this
slice because they hid runtime-critical theme source:

- `wp-content/themes/beslock-custom/template-parts/`
- `wp-content/themes/beslock-custom/templates/`

### Preserved local excludes

These local excludes were intentionally preserved because they still represent
generated artifacts, local environment data, or an unresolved review item:

- `wp-config.php`
- `wp-content/uploads/`
- `.DS_Store`
- `wp-content/themes/beslock-custom/assets/images/` as `REVIEW / RUNTIME CRITICAL`, not yet removed in this slice

### Git visibility result

- `git ls-files -ci --exclude-standard` no longer reports the six recovered runtime surfaces.
- `git check-ignore` no longer matches the six critical runtime files targeted by this slice.
- `git status` for those six files is now clean, which means they are visible to git without adding runtime noise.

## Recovered Runtime Surfaces

These runtime-critical surfaces are now visible again to normal git operations:

- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`
- `wp-content/themes/beslock-custom/template-parts/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/product-features.php`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`
- `wp-content/themes/beslock-custom/templates/models-mobile.php`

### Additional runtime-related paths now visible in status scans

After removing the dangerous excludes, git status also surfaces additional
template files under the same recovered paths when they are not currently
tracked:

- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/discover.php`
- `wp-content/themes/beslock-custom/templates/blocks/hero.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`

## Remaining Local-Only Generated Artifacts

These artifacts remain outside the intended commit scope for this slice and
should stay treated as generated or local-only until repository-level ignore
policy is normalized:

- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*.log`
- `wp-content/themes/beslock-custom/repo_portfolio/products.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json.restored`
- `wp-content/uploads/`
- database exports covered by `database/.gitignore`

## Visibility & Ignore Policy Audit

This section isolates visibility normalization from runtime ownership. The goal
is to ensure active runtime surfaces remain visible to Git, VS Code, and
Copilot, while generated artifacts and local-only outputs are separated cleanly.

### Audit sources checked

- repository `.gitignore` files: only `database/.gitignore` was found
- local repository excludes: `.git/info/exclude`
- additional git exclude source: no `core.excludesfile` value was returned
- VS Code workspace settings: no versioned `.vscode/settings.json` was found
- VS Code workspace files: no `*.code-workspace` file was found
- Copilot ignore settings: no `.copilotignore` or other `.copilot*` ignore file was found

### Exclude classification

| Source | Pattern | Classification | Status | Rationale |
| --- | --- | --- | --- | --- |
| `.git/info/exclude` | `wp-config.php` | local-only config | KEEP | local environment config should stay out of normal tracking |
| `.git/info/exclude` | `wp-content/uploads/` | generated artifact | GENERATED | runtime media uploads are environment data, not authored theme source |
| `.git/info/exclude` | `.DS_Store` | generated artifact | GENERATED | OS metadata |
| `.git/info/exclude` | `wp-content/themes/beslock-custom/assets/images/` | runtime asset surface | REVIEW / RUNTIME CRITICAL | active theme images are referenced by header, footer, and importer tooling; hiding the whole path risks future invisible runtime assets |
| `.git/info/exclude` | `wp-content/themes/beslock-custom/template-parts/` | active runtime surface | REMOVE / RUNTIME CRITICAL | hides active templates and render partials from normal git adds |
| `.git/info/exclude` | `wp-content/themes/beslock-custom/templates/` | active runtime surface | REMOVE / RUNTIME CRITICAL | hides active runtime templates from normal git adds |
| `database/.gitignore` | `*.sql` | generated artifact | KEEP / GENERATED | local database export files |
| `database/.gitignore` | `*.sql.gz` | generated artifact | KEEP / GENERATED | compressed database export files |

### Previously hidden active surfaces

The following surfaces were hidden before local exclude normalization and are
now recovered:

- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`
- `wp-content/themes/beslock-custom/template-parts/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/product-features.php`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`
- `wp-content/themes/beslock-custom/templates/models-mobile.php`

### Dangerous hidden runtime surfaces

- `wp-content/themes/beslock-custom/template-parts/` is dangerous to hide because it contains active render partials for the header, drawer, product card, product features, and archive suppression logic.
- `wp-content/themes/beslock-custom/templates/` is dangerous to hide because it contains active runtime templates used by the current header and drawer flow.
- `wp-content/themes/beslock-custom/assets/images/` is dangerous to hide as a whole because active runtime references already exist for theme media such as logos and hero poster assets, and importer tooling also reads from this path.

### Intentionally excluded generated artifacts

- `wp-config.php`
- `wp-content/uploads/`
- `.DS_Store`
- `database/*.sql`
- `database/*.sql.gz`

### Generated artifacts detected in the current worktree

- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*.log`
- `wp-content/themes/beslock-custom/repo_portfolio/products.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json.restored`

### Safe-to-ignore paths

These are safe ignore candidates because they are generated or local-only and
are not part of the canonical runtime graph:

- `wp-content/themes/beslock-custom/debug/*.log`
- `wp-content/themes/beslock-custom/import_logs/*.log`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/*.restored`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json`
- `.DS_Store`
- `wp-content/uploads/`

### Real runtime files that must remain visible

- `template-parts/header/site-header.php`
- `template-parts/header/mobile-drawer.php`
- `template-parts/product-card.php`
- `template-parts/product-features.php`
- `templates/menu-simple.php`
- `templates/models-mobile.php`
- `template-parts/content/archive_hero.php`
- `assets/css/menu-products-mobile.css`
- active theme image assets under `assets/images/` when they are referenced by templates or importer tooling

### Recommended future ignore policy

Future `.gitignore` normalization should distinguish generated artifacts from
runtime surfaces. Recommended direction only, not applied in this slice:

```gitignore
.DS_Store
wp-content/themes/beslock-custom/debug/*.log
wp-content/themes/beslock-custom/import_logs/*.log
!wp-content/themes/beslock-custom/import_logs/.gitkeep
wp-content/themes/beslock-custom/repo_portfolio/*.sqlite
wp-content/themes/beslock-custom/repo_portfolio/*.restored
wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json
wp-content/uploads/
database/*.sql
database/*.sql.gz
```

Do not carry forward ignore rules for:

- `wp-content/themes/beslock-custom/template-parts/`
- `wp-content/themes/beslock-custom/templates/`
- broad `wp-content/themes/beslock-custom/assets/images/` exclusion without a narrower authored/generated split

### Visibility confirmations requested in this slice

- `site-header.php`, `mobile-drawer.php`, `product-card.php`, `product-features.php`, `menu-simple.php`, and `models-mobile.php` are no longer hidden by local `.git/info/exclude` rules after this slice.
- `menu-products-mobile.css` participates in the active runtime via `inc/core/enqueue.php`; it is not only a preserved legacy file.
- `product-gallery-init.js` is an archive candidate confirmed for the active runtime graph. It has no active enqueue path and now serves only as a preserved recovery/debug fallback.
- `assets/css/pages/single-product.css` is an archive candidate confirmed for the active runtime graph. It has no active enqueue path and is preserved only as a recovery snapshot.
- `assets/css/base/variables.css` is an archive candidate confirmed. No active enqueue or import reference was found.

## Assets Visibility Audit

This section isolates the remaining shadow media surface under
`wp-content/themes/beslock-custom/assets/images/`.

### Audit outcome

- The broad local exclude for `wp-content/themes/beslock-custom/assets/images/` is no longer sustainable as a default visibility policy.
- The path contains multiple runtime-critical and tooling-critical media surfaces, not just optional local assets.
- The exclude should remain classified as `REVIEW / RUNTIME CRITICAL` until a narrower authored/generated split exists.

### Runtime media ownership

| Path or subpath | Classification | Real ownership / usage |
| --- | --- | --- |
| `assets/images/logo-green.png` | RUNTIME CRITICAL | active in `template-parts/header/site-header.php`, `template-parts/header/mobile-drawer.php`, `template-parts/header/header-widget.php`, and hero loader markup |
| `assets/images/logo-white.png` | RUNTIME CRITICAL | active in `footer.php` |
| `assets/images/discover.png` | RUNTIME CRITICAL | active in `templates/blocks/discover.php` |
| `assets/images/instal.png` | RUNTIME CRITICAL | active badge asset in `template-parts/cards/product-card.php`; also referenced by dormant `product-badge-inject.js` |
| `assets/images/products/*.webp` | RUNTIME CRITICAL + TOOLING CRITICAL | active in `templates/models-mobile.php`; also used by placeholder-fix tooling |
| `assets/images/Hero_develp/clips_hero/*.mp4` | RUNTIME CRITICAL | active homepage hero video sources in `templates/blocks/hero.php` |
| `assets/images/Hero_develp/images_hero/*.png` | RUNTIME CRITICAL | active homepage hero overlay images in `templates/blocks/hero.php` |
| `assets/images/Hero_develp/images_hero/images_hero_d/*.png` | RUNTIME CRITICAL | active responsive hero overlay sources in `templates/blocks/hero.php` when desktop variants exist |
| `assets/images/Icons/*.svg` | RUNTIME CRITICAL | active feature icons in `templates/blocks/hero.php` |

### Tooling media dependencies

| Path or subpath | Classification | Tooling dependency |
| --- | --- | --- |
| `assets/images/e-flex_.webp`, `e-nova_.webp`, `e-orbit_.webp`, `e-prime_.webp`, `e-shield_.webp`, `e-touch_.webp` | TOOLING CRITICAL | referenced by `data/products.json` as primary product image source for importer flows |
| `assets/images/e-nova_s.webp`, `e-shield_e.webp`, `e-touch_c.webp` | TOOLING CRITICAL | referenced by `data/products.json` as gallery image sources for importer flows |
| `assets/images/products/*.webp` | TOOLING CRITICAL | read by `scripts/carga_portfolio_data.php`, `scripts/fix-placeholder-images.php`, and menu/mobile card generation |
| `assets/images/` root as search dir | TOOLING CRITICAL | importer and placeholder-fix tooling scan this directory as fallback source for product media |
| `assets/images/hero-poster.webp` | PRESERVED LEGACY / OPTIONAL RUNTIME | checked by `header.php` and `header-noheader.php`, but not present in current image inventory |

### WooCommerce media ownership notes

- Current WooCommerce single-product runtime primarily uses attachment IDs and `_product_image_gallery` metadata after import, not direct filesystem paths under `assets/images/`.
- `data/products.json` still maps product image filenames to theme assets, so importer workflows depend on `assets/images/` to seed or repair Woo attachments.
- `templates/blocks/product-card.php` contains theme-file fallback logic for image normalization, but the current canonical product-card runtime prefers Woo attachments when available.

### Hero and overlay media participation

- `Hero_develp/clips_hero/*.mp4` is active runtime media; the hero template currently references only the base `.mp4` files, not the `.480`, `.720`, or `.webm` variants.
- `Hero_develp/images_hero/*.png` and `Hero_develp/images_hero/images_hero_d/*.png` are active runtime overlay assets.
- `Hero_develp/images_hero/psd_files/*.psd` are not part of the runtime graph and behave as preserved source/design artifacts.
- `Hero_develp/clips_hero/*.bak` files are not part of the active runtime graph and behave as preserved backup artifacts.

### Media classification by subpath

| Subpath | Primary classification | Notes |
| --- | --- | --- |
| `assets/images/products/` | RUNTIME CRITICAL + TOOLING CRITICAL | must remain visible because mobile drawer/runtime and importer tooling both depend on it |
| `assets/images/Hero_develp/clips_hero/` | RUNTIME CRITICAL with preserved legacy variants | base `.mp4` files are active; `.480`, `.720`, `.webm`, `.bak` are not active in the current template |
| `assets/images/Hero_develp/images_hero/` | RUNTIME CRITICAL | active hero overlays |
| `assets/images/Hero_develp/images_hero/images_hero_d/` | RUNTIME CRITICAL | active desktop hero overlay variants |
| `assets/images/Hero_develp/images_hero/psd_files/` | FUTURE ARCHIVE CANDIDATE | design-source artifacts, not runtime |
| `assets/images/Icons/` | RUNTIME CRITICAL with one candidate artifact | SVG icons are active; the screenshot file is a candidate artifact |
| `assets/images/` root product files with underscore/gallery naming | TOOLING CRITICAL / PRESERVED LEGACY | still required by importer data and repair flows |
| `assets/images/` root logos and discover asset | RUNTIME CRITICAL | directly rendered in active templates |

### Candidate media artifacts inside assets/images

| Path | Classification | Reason |
| --- | --- | --- |
| `assets/images/Hero_develp/images_hero/psd_files/*.psd` | FUTURE ARCHIVE CANDIDATE | source design files, not runtime |
| `assets/images/Hero_develp/clips_hero/*.mp4.bak` | PRESERVED LEGACY / FUTURE ARCHIVE CANDIDATE | backup copies, not active hero sources |
| `assets/images/Icons/Screenshot 2026-04-27 at 18.11.41.png` | FUTURE ARCHIVE CANDIDATE | no active reference found |
| `assets/images/Favicon_Beslock.png` | FUTURE ARCHIVE CANDIDATE | no active reference found in audited runtime/tooling surfaces |
| `assets/images/Layout-product.jpeg` | FUTURE ARCHIVE CANDIDATE | no active reference found in audited runtime/tooling surfaces |
| `assets/images/hero.mp4` | FUTURE ARCHIVE CANDIDATE | no active reference found; hero runtime uses `Hero_develp/clips_hero/*.mp4` |
| `assets/images/e-orbit_.png` | PRESERVED LEGACY / DUPLICATE CANDIDATE | no active reference found; webp variant is the one referenced by tooling data |

### Safe Future Media Ignore Strategy

Future media visibility normalization should split authored runtime media from
design backups and local artifacts instead of excluding `assets/images/`
wholesale.

Recommended direction only, not applied in this slice:

- keep `assets/images/` visible by default
- if needed later, ignore only clearly non-runtime subpaths or file patterns such as:
	`assets/images/Hero_develp/images_hero/psd_files/`
	`assets/images/Hero_develp/clips_hero/*.bak`
	isolated design screenshots with no runtime references
- do not ignore:
	`assets/images/products/`
	`assets/images/Hero_develp/clips_hero/*.mp4`
	`assets/images/Hero_develp/images_hero/`
	`assets/images/Hero_develp/images_hero/images_hero_d/`
	`assets/images/Icons/*.svg`
	root runtime assets like logos, `discover.png`, `instal.png`, and tooling-owned product image files referenced by `data/products.json`

### Conclusion for the broad local exclude

- `assets/images/` should stay classified as `REVIEW / RUNTIME CRITICAL`.
- The broad exclude is currently hiding real runtime media and importer-owned media, so it is not a sustainable long-term visibility policy.
- Any future cleanup should be path-specific and proof-based, not directory-wide.

## Canonical Path Audit

This section isolates hardcoded path ownership in tooling, importer/exporter,
data readers/writers, and media resolution logic.

### Audit outcome

- The repository currently runs two path-resolution models in parallel.
- The canonical plugin path model already reads root `data/products.json`.
- Theme-local tooling still assumes that catalog data, media source paths,
	script entrypoints, and some generated outputs live under
	`wp-content/themes/beslock-custom`.
- There is no shared path-resolution layer. Path discovery is duplicated across
	theme scripts, theme admin tooling, and custom plugins.

### Hardcoded path families detected

| Path family | Classification | Current usage |
| --- | --- | --- |
| `get_stylesheet_directory() . '/data/products.json'` | theme-relative data path | importer and helper scripts under `wp-content/themes/beslock-custom/scripts/` |
| `get_stylesheet_directory() . '/assets/images/'` and `/assets/images/products/` | theme-relative media root | importer helpers, placeholder-fix tooling, image assignment helpers |
| `get_stylesheet_directory() . '/scripts/*.php'` | theme-relative tooling entrypoint | theme admin menu registration in `functions.php` |
| `get_stylesheet_directory() . '/import_logs'` | theme-relative generated output | importer log output in `carga_portfolio_data.php` |
| `WP_CONTENT_DIR . '/themes/beslock-custom'` | hardcoded active theme path | custom plugins, exporter, image import, backup/undo flows |
| `WP_CONTENT_DIR . '/themes/beslock-custom/repo_portfolio'` | hardcoded export/compatibility path | exporter JSON/SQLite/backup outputs and short-des exporter input |
| `ABSPATH . 'data/products.json'` | repo-root canonical data path | `beslock-product-sync` and importer selection in `beslock-portfolio-exporter` |
| `__DIR__ . '/../../../../wp-load.php'` and walk-up chains | bootstrap path heuristic | CLI/eval scripts that assume current file depth relative to WordPress root |
| `dirname( dirname( dirname( __FILE__ ) ) ) . '/data/products.json'` | fallback repo-root heuristic | exporter plugin fallback when `ABSPATH` is unavailable |

### Tooling and script path dependency map

| Surface | Current read path(s) | Current write path(s) | Path ownership assumption |
| --- | --- | --- | --- |
| `scripts/carga_portfolio_data.php` | theme `data/products.json`; theme `assets/images/products/`; theme `assets/images/` | theme `import_logs/`; `dirname( data_file )/products.updated.json`; uploads fallback for logs | theme owns data root, media root, and preferred tooling output root |
| `scripts/fix-placeholder-images.php` | theme `assets/images/products/`; theme `assets/images/`; bootstrap via `__DIR__/../../../../wp-load.php` | uploads backup JSON under `uploads/beslock-backups/` | theme owns media source root; WordPress root is found by file depth heuristic |
| `scripts/set_post_excerpts_from_products.php` | theme `data/products.json`; walk-up `wp-load.php` discovery | overwrites same theme `data/products.json`; attempts git add/commit | theme owns editable data source |
| `scripts/apply_products_short_descriptions.php` | theme `data/products.json`; walk-up `wp-load.php` discovery | writes WP `post_excerpt`; option log only | theme owns canonical read source |
| `scripts/run_carga_dry.php` | `require_once get_stylesheet_directory() . '/scripts/carga_portfolio_data.php'` | none | importer must live inside active theme |
| `scripts/CSV_portfolio_generator.php` | WP product DB; optional importer function from theme script include chain | theme `data/products_portfolio.csv` | exporter output belongs inside theme `data/` |
| `functions.php` admin tooling | theme `scripts/carga_portfolio_data.php`; theme `scripts/fix-placeholder-images.php`; theme `assets/images` | admin-triggered media imports from theme assets | tooling registry is theme-owned |
| `plugins/beslock-product-sync` | root `data/products.json` | WooCommerce DB only | canonical data is repo-owned |
| `plugins/beslock-portfolio-exporter` export | WooCommerce DB; existing `repo_portfolio/products.json` for merge | `repo_portfolio/products.json`; `repo_portfolio/products.sqlite` | export compatibility zone is theme-owned |
| `plugins/beslock-portfolio-exporter` import | prefers root `data/products.json`, then theme `data/products.json`, then `repo_portfolio/products.json` | theme `repo_portfolio/products_backup_latest.json`; theme `import_logs/` | mixed ownership: canonical read may be repo-root, but writes remain theme-owned |
| `plugins/beslock-portfolio-exporter` images | theme `assets/images` | uploads / attachment assignment | media source root is theme-owned |
| `plugins/short-des-exporter` | theme `repo_portfolio/products.json` | uploads `short-des-exporter.log`; direct DB updates | excerpt sync is hard-coupled to theme export artifact |

### Duplicated path resolution logic

- `products.json` resolution is duplicated across at least three models:
	root-only (`beslock-product-sync`), root-then-theme-then-repo fallback
	(`beslock-portfolio-exporter`), and theme-only (`scripts/*`).
- media lookup under `assets/images/products/` plus `assets/images/` is
	duplicated in `carga_portfolio_data.php`, `fix-placeholder-images.php`,
	`functions.php` image tooling, and the exporter image-import flow.
- WordPress bootstrap discovery is duplicated with incompatible heuristics:
	fixed relative `__DIR__` jumps and walk-up loops for `wp-load.php`.
- log/output ownership is duplicated between theme-local `import_logs/`,
	theme-local `data/`, uploads, and temporary fallback directories.

### Implicit ownership assumptions detected

- active theme path equals tooling root
- active theme path equals canonical data root
- theme `assets/images/` equals authoritative media source root for importer and repair flows
- theme `repo_portfolio/` equals exporter compatibility/output root
- script physical location determines how WordPress bootstrap should be found
- a consumer can safely infer repo root from `ABSPATH` or from plugin/script depth without a shared contract

### Scripts that would break today if data moves out of the theme

These surfaces still read theme-local `data/products.json` directly and would
break immediately if that file stops existing without a compatibility bridge:

- `wp-content/themes/beslock-custom/scripts/carga_portfolio_data.php`
- `wp-content/themes/beslock-custom/scripts/set_post_excerpts_from_products.php`
- `wp-content/themes/beslock-custom/scripts/apply_products_short_descriptions.php`
- `wp-content/themes/beslock-custom/scripts/CSV_portfolio_generator.php` for CSV output placement expectations
- `wp-content/themes/beslock-custom/scripts/run_carga_dry.php` indirectly, because it loads the importer script that still reads theme-local data
- theme admin pages registered in `functions.php` that include those scripts

These surfaces would not break on the read path because they already prefer or
require repo-root data, but they still contain hardcoded ownership elsewhere:

- `wp-content/plugins/beslock-product-sync/beslock-product-sync.php`
- `wp-content/plugins/beslock-portfolio-exporter/beslock-portfolio-exporter.php`

These surfaces remain coupled to theme-local export artifacts rather than the
canonical data root:

- `wp-content/plugins/short-des-exporter/short-des-exporter.php`
- `wp-content/plugins/beslock-portfolio-exporter/beslock-portfolio-exporter.php` backup/export/undo paths

## Runtime vs Data Ownership

This section separates what should remain runtime-theme-owned from what should
become repo-owned canonical data.

### Ownership split

| Root concern | Should own it long term | Current actual owner | Notes |
| --- | --- | --- | --- |
| frontend templates and render assets | runtime theme root | theme root | keep theme-owned |
| WooCommerce presentation and template overrides | runtime theme root | theme root | keep theme-owned |
| canonical catalog source (`products.json`) | canonical data root | split between repo root and theme root | currently inconsistent |
| importer orchestration | tooling root or canonical sync plugin | split between theme scripts and plugins | should stop depending on theme path |
| exporter outputs and recovery artifacts | generated/export root | theme `repo_portfolio/` | compatibility zone only |
| source media used to seed attachments | media root | theme `assets/images/` | should remain distinct from canonical JSON root |
| temporary logs and backups | generated/export root or uploads | theme `import_logs/`, uploads, temp dir | currently mixed |

### Where each canonical root should resolve from

| Proposed root | Responsibility | Should resolve from |
| --- | --- | --- |
| runtime theme root | templates, partials, frontend CSS/JS, runtime image URLs | active child theme path via WordPress theme APIs |
| repo root | repository-level docs, canonical data folder, shared tooling contracts | `ABSPATH` in the current monorepo layout, with one explicit fallback contract only |
| canonical data root | editable catalog source such as `products.json` | repo root `data/` |
| tooling root | importer/exporter scripts, sync helpers, admin tooling contracts | explicit tooling layer, not inferred from theme path |
| media root | authored source media used to seed or repair attachments | runtime theme assets until media ownership is split later |
| generated/export root | exporter JSON, SQLite, backups, dry-run outputs, logs | explicit output root separate from runtime theme presentation surfaces |

### Specific ownership decisions for the future layer

- `products.json` should live in root `data/products.json` as the canonical editable catalog source.
- the importer should read from the canonical data root, not from theme-local `data/`.
- the exporter should write to a declared generated/export root; for compatibility it can still target `repo_portfolio/`, but that should be treated as output-only, not as source-of-truth.
- `assets/images` should resolve from a media root contract distinct from the canonical data root. The canonical JSON may reference media filenames, but should not imply that data ownership lives inside the theme.

## Tooling Path Dependencies

This section groups current consumers by the root they depend on.

### Runtime theme path dependencies

- `functions.php` admin tooling includes theme-local scripts by absolute theme-relative path.
- `scripts/run_carga_dry.php` requires the importer from the active theme path.
- `plugins/beslock-portfolio-exporter` hardcodes `WP_CONTENT_DIR . '/themes/beslock-custom'` for export, import backup/undo, and image import helpers.
- `plugins/short-des-exporter` hardcodes `WP_CONTENT_DIR . '/themes/beslock-custom/repo_portfolio/products.json'`.

### Canonical data path dependencies

- `plugins/beslock-product-sync` already depends only on `ABSPATH . 'data/products.json'`.
- `plugins/beslock-portfolio-exporter` already prefers root `data/products.json` on import.
- theme helper scripts do not yet consume the canonical data root directly.

### Tooling bootstrap dependencies

- `scripts/fix-placeholder-images.php` depends on fixed relative location to `wp-load.php`.
- `scripts/set_post_excerpts_from_products.php` and `scripts/apply_products_short_descriptions.php` depend on walk-up discovery of `wp-load.php`.
- `scripts/run_carga_dry.php` assumes the repository root and WordPress root are reachable from the script's current depth.

### Media source path dependencies

- importer and repair flows assume source media live under theme `assets/images/products/` and theme `assets/images/`.
- exporter image import assumes the same theme-local media root.
- current media resolution logic is filename-based and attachment-oriented, but the filesystem search roots are still theme-owned.

### Generated/export path dependencies

- `plugins/beslock-portfolio-exporter` writes to `repo_portfolio/products.json`, `repo_portfolio/products.sqlite`, and `repo_portfolio/products_backup_latest.json`.
- `plugins/short-des-exporter` consumes `repo_portfolio/products.json` as if it were a stable input contract.
- `carga_portfolio_data.php` writes theme-local import logs and `products.updated.json` beside the data file.
- `CSV_portfolio_generator.php` writes `products_portfolio.csv` into theme `data/`.

## Future Path Resolution Strategy

This section proposes a canonical path resolution layer without implementing it.

### Proposed Canonical Path Resolution Layer

One explicit resolver should define and return these roots:

- runtime theme root
- runtime theme URI root
- repo root
- canonical data root
- tooling root
- media root
- generated/export root
- logs root

### Resolver behavior the future layer should provide

- resolve canonical data reads independently from the active theme path
- resolve generated/export writes independently from canonical data reads
- resolve media source lookup independently from runtime template URLs
- expose a single compatibility fallback order during migration instead of repeating fallback chains in each script
- expose one bootstrap contract for CLI/admin tooling instead of repeated `wp-load.php` heuristics

### Recommended fallback policy during migration

- canonical data read order should be explicit and centralized
- current compatibility order can be preserved temporarily as:
	root `data/products.json` -> theme `data/products.json` -> `repo_portfolio/products.json`
- exporter outputs should keep current location until consumers are migrated, but that path should be labeled output-only
- media source resolution should continue to point at theme `assets/images/` until media ownership is migrated separately

### Migration risks

| Risk | Why it matters now |
| --- | --- |
| theme-local tooling silently diverges from repo-root canonical data | different importers can operate on different product sets or descriptions |
| exporter and excerpt sync still treat `repo_portfolio` as stable input | moving outputs or reclassifying them too early will break compatibility consumers |
| media lookup is still theme-owned | moving data without preserving media root contracts will break importer image assignment |
| bootstrap path heuristics are brittle | moving scripts or changing folder depth can break CLI tooling before any functional logic runs |
| generated outputs are mixed with authored theme surfaces | future ignore or cleanup work can accidentally hide or delete active tooling artifacts |

### Recommended future implementation order

1. Introduce a read-only path resolver that only reports roots and fallback order, with no behavior change.
2. Switch theme helper scripts to consume the resolver for canonical data reads while preserving current fallback order.
3. Normalize generated/export writes behind the same resolver, still targeting current paths.
4. Migrate admin tooling registration in `functions.php` away from hardcoded theme script includes toward a tooling entry layer.
5. Migrate `short-des-exporter` off direct `repo_portfolio/products.json` reads.
6. Only after all consumers are path-normalized, remove theme-local `data/products.json` assumptions.

## Surface Ownership Registry

This registry converts the audit into an explicit ownership map for the most
important ambiguous or high-value surfaces.

| Surface | Canonical owner | Bridge / delegator | Dormant fallback | Future archive candidate | Preserved legacy |
| --- | --- | --- | --- | --- | --- |
| `site-header.php` | `template-parts/header/site-header.php` | `header.php` | none identified | no | no |
| `mobile-drawer.php` | `template-parts/header/mobile-drawer.php` | `templates/menu-simple.php` | none identified | no | no |
| `product-card.php` | `template-parts/product-card.php` -> `template-parts/cards/product-card.php` | `woocommerce/content-product.php`, `templates/blocks/product-card.php` | none identified | no | `templates/blocks/product-card.php` |
| `product-features.php` | `template-parts/product-features.php` | `inc/woocommerce/product-features.php` | none identified | no | no |
| `menu-simple.php` | `templates/menu-simple.php` | `header.php` | none identified | no | no |
| `models-mobile.php` | `templates/models-mobile.php` | `template-parts/header/mobile-drawer.php` | none identified | no | no |
| `archive_hero.php` | `template-parts/content/archive_hero.php` for Woo archive suppression | parent Kadence `template-parts/content/archive_hero.php` for non-Woo contexts | none identified | no | yes |
| `header.php` | `header.php` as active shell; canonical header markup still lives in `template-parts/header/site-header.php` | none | none identified | no | yes |
| `menu-products-mobile.css` | `assets/css/menu-products-mobile.css` enqueued from `inc/core/enqueue.php` | none | older duplicate reference remains in `inc/enqueue-assets.php` | no | yes |
| `product-gallery-init.js` | none in active runtime; canonical gallery runtime is `assets/js/product-gallery-reel.js` | none | `assets/js/product-gallery-init.js` | yes | yes |
| `variables.css` | none identified | none | none | yes | yes |
| `single-product.css` | none in active runtime; canonical single-product stack is `product-page.css`, `product-tabs.css`, `product-widgets.css`, `wc-scope-fix.css` | none | `assets/css/pages/single-product.css` | yes | yes |
| `debug.php` | none in active runtime | none | `inc/debug/debug.php` as manual troubleshooting helper | yes | yes |
| `products.json` | `data/products.json` for tooling/import workflows | theme-root `products.json` acts only as a duplicate surface today | none identified | yes for theme-root `products.json` | yes for `data/products.json` |

### Registry notes

- `products.json` appears in two roles: `data/products.json` is the canonical tooling data source, while theme-root `products.json` behaves as a duplicate surface and archive candidate.
- Inline ownership comments were added only to files that support comment syntax without changing behavior. JSON files were intentionally left untouched.

## Classification Tables

### Canonical frontend source

| Path group | Classification | Runtime relevance | Commit relevance |
| --- | --- | --- | --- |
| `wp-content/themes/beslock-custom/functions.php` | compatibility bridge + bootstrap entry | active | must remain versioned |
| `wp-content/themes/beslock-custom/inc/core/enqueue.php` | canonical frontend enqueue owner | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/components/header.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/components/hero.css` | canonical frontend source | active homepage owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/components/discover.css` | canonical frontend source | active homepage owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/components/product-card.css` | canonical frontend source | active product-card owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/layout/header.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/layout/homepage.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/layout/storefront.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/layout/recommendations.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/layout/footer.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/utilities/buttons.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/utilities/layout-helpers.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/utilities/utilities.css` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/main.css` | compatibility layer with active ownership debt | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/menu-products-mobile.css` | active frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/models-mobile.css` | active frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/beslock-cart-empty.css` | active Woo override | active cart-empty owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/product-page.css` | active Woo override | active single-product owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/product-tabs.css` | active Woo override | active single-product owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/product-widgets.css` | active Woo override | active single-product owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/css/wc-scope-fix.css` | active Woo compatibility | active bridge | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/main.js` | canonical frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/components/header.js` | canonical frontend source | active header owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/components/mobile-drawer.js` | canonical frontend source | active drawer owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/components/product-card.js` | canonical frontend source | active product-card owner | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/models-mobile.js` | active frontend source | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/fix-placeholder.js` | active Woo-sensitive runtime | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/product-tabs.js` | active Woo-sensitive runtime | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/product-quantity-controls.js` | active Woo-sensitive runtime | active | must remain versioned |
| `wp-content/themes/beslock-custom/assets/js/product-gallery-reel.js` | active Woo-sensitive runtime | active canonical reel runtime | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/product-card.php` | canonical frontend source | active card render owner | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/cards/product-card.php` | canonical frontend source | active card render leaf partial | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/product-features.php` | canonical frontend source | active Woo feature partial | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/header/site-header.php` | canonical frontend source | active header markup | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php` | canonical frontend source | active drawer markup | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/header/header-widget.php` | active header partial | active via `functions.php`, `inc/header-widget.php`, `inc/features/header.php` | must remain versioned |
| `wp-content/themes/beslock-custom/templates/menu-simple.php` | active frontend source | active header include | must remain versioned |
| `wp-content/themes/beslock-custom/templates/models-mobile.php` | active frontend source | active drawer include | must remain versioned |
| `wp-content/themes/beslock-custom/templates/blocks/hero.php` | active homepage source | active fallback/homepage owner | must remain versioned |
| `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php` | active storefront source | active fallback/homepage owner | must remain versioned |
| `wp-content/themes/beslock-custom/templates/blocks/discover.php` | active homepage source | active fallback/homepage owner | must remain versioned |
| `wp-content/themes/beslock-custom/front-page.php`, `header.php`, `footer.php`, `page.php`, `index.php`, `woocommerce/**/*.php` | canonical template/Woo override source | active | must remain versioned |
| `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php` | indirect canonical template override | active on Woo archive suppression path | must remain versioned |

### Compatibility bridge

| Path | Classification | Notes |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/functions.php` | compatibility bootstrap | early `beslock-main-style` owner plus guarded fallback enqueues |
| `wp-content/themes/beslock-custom/style.css` | compatibility bridge | active baseline fallback layer |
| `wp-content/themes/beslock-custom/assets/css/main.css` | compatibility bridge | still globally loaded and still covers Woo/Kadence debt |
| `wp-content/themes/beslock-custom/inc/woocommerce/enqueue-assets.php` | compatibility bridge | no-op compatibility include |
| `wp-content/themes/beslock-custom/header.php` | compatibility bridge | active child header shell that composes canonical Beslock header and drawer/menu partials |
| `wp-content/themes/beslock-custom/page.php` and `index.php` | compatibility bridge | active delegates that preserve parent Kadence loop behavior while child theme owns selected surfaces |
| `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php` | compatibility bridge | looks legacy because it defers to parent, but actively suppresses Woo archive hero output |
| `wp-content/themes/beslock-custom/ACTIVE_BOOTSTRAP_CONSOLIDATION_SUMMARY.md` and related migration summaries | migration documentation | valuable architectural trace, not runtime |

### Dormant legacy asset

| Path | Classification | Evidence |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/inc/enqueue-assets.php` | dormant legacy enqueue surface | not included from `functions.php`; retains older pipeline |
| `wp-content/themes/beslock-custom/assets/css/product-rotator.css` | dormant legacy asset | only referenced from dormant `inc/enqueue-assets.php` |
| `wp-content/themes/beslock-custom/assets/js/product-rotator.js` | dormant legacy asset | only referenced from dormant `inc/enqueue-assets.php` |
| `wp-content/themes/beslock-custom/assets/css/product-card-alt.css` | dormant legacy asset | only referenced from dormant `inc/enqueue-assets.php` |
| `wp-content/themes/beslock-custom/assets/js/product-card-alt.js` | dormant legacy asset | no active enqueue references found |
| `wp-content/themes/beslock-custom/assets/css/product-card-fade.css` | dormant legacy asset | only referenced from dormant `inc/enqueue-assets.php` |
| `wp-content/themes/beslock-custom/assets/js/product-card-fade.js` | dormant legacy asset | no active enqueue references found |
| `wp-content/themes/beslock-custom/assets/js/product-badge-inject.js` | dormant legacy asset | active badge path is server-rendered; no active enqueue reference |
| `wp-content/themes/beslock-custom/assets/js/product-gallery-init.js` | dormant legacy asset / unresolved dependency | present, Woo-sensitive, but no active enqueue reference |
| `wp-content/themes/beslock-custom/templates/blocks/product-card.php` | runtime inactive but intentionally preserved | wrapper/delegation layer for older portfolio-array flow, superseded by `template-parts/product-card.php` |

### Duplicated surface or legacy shim

| Path | Classification | Notes |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/assets/css/header-state.css` | duplicated surface / legacy shim | only referenced from dormant `inc/enqueue-assets.php` and `HEADER-FIX.md` |
| `wp-content/themes/beslock-custom/assets/js/header-state.js` | duplicated surface / legacy shim | only referenced from dormant `inc/enqueue-assets.php` and `HEADER-FIX.md` |
| `wp-content/themes/beslock-custom/assets/js/menu-products-mobile.js` | duplicated surface | only referenced from dormant `inc/enqueue-assets.php`; active drawer runtime is `components/mobile-drawer.js` |
| `wp-content/themes/beslock-custom/products.json` | duplicated data surface | no active script references found; `scripts/*` use `data/products.json` instead |

### Debug artifact or temporary runtime artifact

| Path | Classification | Notes |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/debug/enqueued-styles.log` | debug artifact | generated runtime inspection output |
| `wp-content/themes/beslock-custom/import_logs/*.log` | temporary runtime artifact | importer execution logs |
| `wp-content/themes/beslock-custom/import_logs/.gitkeep` | folder-retention helper | keep only if logs directory must exist in repo |
| `wp-content/themes/beslock-custom/repo_portfolio/products.sqlite` | temporary/local data artifact | not part of frontend runtime |
| `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json` | temporary/local data artifact | not part of frontend runtime |
| `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json.restored` | temporary/local data artifact | not part of frontend runtime |

### Script/data source outside frontend runtime

| Path | Classification | Notes |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/data/products.json` | should-be-versioned data source | consumed by importer/excerpt scripts |
| `wp-content/themes/beslock-custom/scripts/*.php` | tooling source | not frontend runtime, but first-party operational scripts |
| `wp-content/themes/beslock-custom/docs/*.md` | migration/implementation docs | useful, but not runtime |
| `wp-content/themes/beslock-custom/HEADER-FIX.md` | documentation artifact | documents legacy header shim state for `header-state.*` |
| `database/.gitignore` | generated/transient support file | only repo-level `.gitignore` found during this audit; scoped to database artifacts, not theme source |
| root `*.md` migration and architecture docs | migration documentation | should remain versioned if the repo keeps architectural trace in-tree |

### Plugin/vendor noise

| Path group | Classification | Notes |
| --- | --- | --- |
| `wp-content/plugins/woocommerce/` | plugin/vendor noise | upstream plugin copy, not theme source |
| `wp-content/themes/kadence/` | vendor/theme dependency noise | parent theme copy, not child-theme source |
| third-party plugins such as `complianz-*`, `loginizer`, `really-simple-ssl`, `siteseo-pro`, `google-listings-and-ads`, `fileorganizer` | plugin/vendor noise | environment-level, not theme architecture |
| custom local plugins `wp-content/plugins/beslock-portfolio-exporter/`, `wp-content/plugins/short-des-exporter/`, `wp-content/plugins/beslock-product-sync/` | unresolved ambiguity | first-party naming suggests they may deserve their own repo or explicit versioning policy |

### Unresolved ambiguity / orphan candidates

| Path | Classification | Why ambiguous |
| --- | --- | --- |
| `wp-content/themes/beslock-custom/assets/css/components/badge.css` | unresolved ambiguity | no active enqueue or template reference found |
| `wp-content/themes/beslock-custom/assets/css/pages/single-product.css` | unresolved ambiguity | no active enqueue reference found; may be superseded by `product-page.css` |
| `wp-content/themes/beslock-custom/assets/css/base/variables.css` | orphan candidate | no active enqueue or import reference found in audited runtime or docs |
| `wp-content/themes/beslock-custom/header-noheader.php` | unresolved ambiguity | present but no active reference found in audited runtime paths |
| `wp-content/themes/beslock-custom/inc/cleanup-kadence.php` | unresolved ambiguity | active `inc/integrations/kadence-cleanup.php` also exists; naming overlap suggests older surface |
| `wp-content/themes/beslock-custom/inc/debug.php` and `inc/debug/debug.php` | debug/runtime artifact candidates | present as tooling/debug helpers, but no audited include path references them |

## Ownership Cross-Map

### By controlling PHP surface

| Controlling surface | Owns directly | Indirect participants | Notes |
| --- | --- | --- | --- |
| `functions.php` | `style.css`, guarded fallbacks, late Kadence/Woo bridges | `header-widget.php`, Woo setup includes, `inc/core/enqueue.php` | active compatibility entrypoint, not the main modular owner anymore |
| `inc/core/enqueue.php` | canonical active CSS/JS runtime handles | `menu-products-mobile.css`, `models-mobile.css`, product page assets, `wc-scope-fix.css` | primary enqueue owner for current frontend runtime |
| `header.php` | child header shell | `template-parts/header/site-header.php`, `templates/menu-simple.php` | looks thin, but is active and dangerous to remove |
| `template-parts/header/mobile-drawer.php` | canonical drawer markup | `templates/models-mobile.php`, `assets/js/components/mobile-drawer.js`, `assets/js/models-mobile.js` | active source currently hidden by local exclude |
| `front-page.php` | homepage composition routing | `templates/blocks/hero.php`, `templates/blocks/products-portfolio.php`, `templates/blocks/discover.php` | fallback routing means missing `template-parts/{hero,products,discover}.php` is intentional today |
| `woocommerce/content-product.php` | loop-item render routing | `template-parts/product-card.php`, `template-parts/cards/product-card.php` | canonical card render path |
| `template-parts/content/archive_hero.php` | Woo archive hero suppression | parent Kadence archive hero template for non-Woo contexts | legacy-looking file with active indirect behavior |

### By asset ownership layer

| Layer | Canonical active assets | Deferred / inactive neighbors | Notes |
| --- | --- | --- | --- |
| `assets/css/components/` | `header.css`, `hero.css`, `discover.css`, `product-card.css` | `badge.css` | `badge.css` contains real styles but is not yet part of the active stylesheet graph |
| `assets/css/layout/` | `header.css`, `homepage.css`, `storefront.css`, `recommendations.css`, `footer.css` | none found | canonical modular layout layer |
| `assets/css/utilities/` | `buttons.css`, `layout-helpers.css`, `utilities.css` | none found | canonical utility layer |
| `assets/css/` root | `main.css`, `menu-products-mobile.css`, `models-mobile.css`, `product-page.css`, `product-tabs.css`, `product-widgets.css`, `wc-scope-fix.css`, `beslock-cart-empty.css` | `product-rotator.css`, `product-card-alt.css`, `product-card-fade.css`, `header-state.css`, `pages/single-product.css`, `base/variables.css` | mixed active bridge layer plus preserved debt |
| `assets/js/components/` | `header.js`, `mobile-drawer.js`, `product-card.js` | none found | canonical modular JS layer |
| `assets/js/` root | `main.js`, `models-mobile.js`, `fix-placeholder.js`, `product-tabs.js`, `product-quantity-controls.js`, `product-gallery-reel.js` | `menu-products-mobile.js`, `header-state.js`, `product-rotator.js`, `product-card-alt.js`, `product-card-fade.js`, `product-gallery-init.js`, `product-badge-inject.js` | active root scripts coexist with preserved legacy scripts |

### Migration summary relationships

| Summary artifact | Relationship to current ownership map |
| --- | --- |
| `LEGACY_RUNTIME_AUDIT_SUMMARY.md` | historical basis for classifying `inc/enqueue-assets.php` and dormant asset surfaces |
| `PRODUCT_CARD_RUNTIME_OWNERSHIP_SUMMARY.md` and `PRODUCT_CARD_PRESENTATION_OWNERSHIP_SUMMARY.md` | explain why `template-parts/product-card.php` and `assets/css/components/product-card.css` are canonical owners |
| `ACTIVE_BOOTSTRAP_CONSOLIDATION_SUMMARY.md` and `PRIMARY_BOOTSTRAP_CONSOLIDATION_SUMMARY.md` | explain why `inc/core/enqueue.php` is now the canonical runtime owner and `functions.php` is fallback-only for overlaps |
| `HEADER_RUNTIME_CLEANUP_SUMMARY.md` and `HEADER_CSS_CONSOLIDATION_SUMMARY.md` | explain why header runtime moved away from `header-state.*` toward `header.php`, `site-header.php`, and modular header assets |
| `HOMEPAGE_SURFACE_MIGRATION_SUMMARY.md` and `STOREFRONT_OWNERSHIP_SUMMARY.md` | explain why homepage/storefront ownership lives in `templates/blocks/*` and modular layout/component CSS |

## Runtime Ownership Relevance

### Actively referenced from enqueue/bootstrap

Active bootstrap references were verified in:

- `wp-content/themes/beslock-custom/functions.php`
- `wp-content/themes/beslock-custom/inc/core/enqueue.php`

The active runtime currently references these frontend surfaces directly:

- `style.css`
- `assets/css/main.css`
- `assets/css/utilities/*.css`
- `assets/css/layout/{homepage,storefront,recommendations,footer,header}.css`
- `assets/css/components/{header,hero,discover,product-card}.css`
- `assets/css/{beslock-cart-empty,menu-products-mobile,models-mobile,product-widgets,product-page,product-tabs,wc-scope-fix}.css`
- `assets/js/main.js`
- `assets/js/components/{header,mobile-drawer,product-card}.js`
- `assets/js/{fix-placeholder,models-mobile,product-tabs,product-quantity-controls,product-gallery-reel}.js`

### Actively referenced from templates and Woo overrides

Verified active template/render chain includes:

- `woocommerce/content-product.php` -> `template-parts/product-card.php` -> `template-parts/cards/product-card.php`
- `header.php` -> `template-parts/header/site-header.php`
- `template-parts/header/mobile-drawer.php` -> `templates/models-mobile.php`
- `front-page.php` -> fallback chain to `templates/blocks/{hero,products-portfolio,discover}.php`
- `inc/woocommerce/product-features.php` -> `template-parts/product-features.php`
- `header.php` -> `templates/menu-simple.php`
- `template-parts/content/archive_hero.php` -> parent Kadence archive hero for non-shop contexts only

### Looks legacy but still participates indirectly

- `template-parts/content/archive_hero.php` looks like a parent-theme defer file, but it is the active mechanism suppressing Kadence hero output on shop and product taxonomies.
- `header.php`, `page.php`, and `index.php` look thin or parent-oriented, but they are active compatibility shells that keep Kadence behavior intact where the child theme has not taken full ownership.
- `menu-products-mobile.css` looks like an older mobile menu surface by name, but it is still actively enqueued from `inc/core/enqueue.php` and supports the current drawer/templates flow.
- `templates/blocks/product-card.php` looks like an active card template by name, but today it is only a preserved compatibility wrapper and not the canonical render owner.

### Intentionally dormant but preserved

These files are retained because they still document or preserve older runtime
surfaces even though the active enqueue path no longer owns them:

- `inc/enqueue-assets.php`
- `assets/css/product-rotator.css`
- `assets/js/product-rotator.js`
- `assets/css/product-card-alt.css`
- `assets/js/product-card-alt.js`
- `assets/css/product-card-fade.css`
- `assets/js/product-card-fade.js`
- `assets/js/product-badge-inject.js`
- `assets/js/product-gallery-init.js`
- `inc/cleanup-kadence.php`

### Dangerous to remove without a proof pass

- `template-parts/header/site-header.php`
- `template-parts/header/mobile-drawer.php`
- `template-parts/product-card.php`
- `template-parts/product-features.php`
- `templates/menu-simple.php`
- `templates/models-mobile.php`
- `template-parts/content/archive_hero.php`
- `assets/css/menu-products-mobile.css`
- `assets/css/models-mobile.css`
- `assets/js/models-mobile.js`
- `data/products.json`

## Commit Relevance

### Must remain versioned

- all active theme PHP templates and Woo overrides
- all active assets enqueued from `functions.php` or `inc/core/enqueue.php`
- all active template partials in `template-parts/` and `templates/blocks/`
- migration summaries that document committed architectural slices
- `data/products.json` and `scripts/*.php` if importer workflows are part of the repo’s intended tooling surface

### Should likely remain versioned, but grouped as tooling/docs rather than frontend runtime

- root architecture and migration planning docs
- `wp-content/themes/beslock-custom/docs/*.md`
- `wp-content/themes/beslock-custom/scripts/*.php`
- `wp-content/themes/beslock-custom/HEADER-FIX.md`

### Should likely be ignored or removed from worktree later, not versioned as frontend source

- `.DS_Store`
- `debug/enqueued-styles.log`
- `import_logs/*.log`
- `repo_portfolio/products.sqlite`
- `repo_portfolio/products_backup_latest.json`
- `repo_portfolio/products_backup_latest.json.restored`
- vendor/plugin copies such as `wp-content/plugins/woocommerce/` and `wp-content/themes/kadence/`

### Should-be-ignored but keep available locally

- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*.log`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- restored or backup JSON/database artifacts under `repo_portfolio/`

## Recommended Gitignore Additions

These are recommended repository-level ignores for a future normalization-only
commit. They are recommendations only; not applied in this audit.

```gitignore
.DS_Store
wp-content/themes/beslock-custom/debug/*.log
wp-content/themes/beslock-custom/import_logs/*.log
!wp-content/themes/beslock-custom/import_logs/.gitkeep
wp-content/themes/beslock-custom/repo_portfolio/*.sqlite
wp-content/themes/beslock-custom/repo_portfolio/*.restored
wp-content/themes/kadence/
wp-content/plugins/woocommerce/
```

### Important non-gitignore recommendation

Do not keep these paths in `.git/info/exclude`:

- `wp-content/themes/beslock-custom/template-parts/`
- `wp-content/themes/beslock-custom/templates/`

Those should be visible to normal git operations because they are active,
versioned theme source.

### Ignore pattern audit notes

- No `.copilotignore` or other `.copilot*` ignore file was found in the repository.
- The only versioned `.gitignore` found during this audit is `database/.gitignore`; it does not govern active theme source ownership.
- Current accidental hiding of active theme files is coming from local `.git/info/exclude`, not from repository-level ignore policy.

## Safe Future Cleanup Candidates

These are candidates for later proof-based cleanup, not immediate deletion:

1. `assets/css/header-state.css` and `assets/js/header-state.js`
2. `assets/js/menu-products-mobile.js`
3. `assets/css/components/badge.css`
4. `assets/css/pages/single-product.css`
5. `products.json` at the theme root
6. `inc/cleanup-kadence.php` if `inc/integrations/kadence-cleanup.php` remains the real owner
7. `assets/css/base/variables.css`
8. dormant legacy product-card/media assets after one more runtime proof pass

## Files That Are Currently Ambiguous

Highest-value ambiguities to resolve before more migration work:

1. Whether `assets/css/pages/single-product.css` has any live dependency outside the audited enqueue path.
2. Whether `assets/css/components/badge.css` is dead or simply unqueued canonical work.
3. Whether theme-root `products.json` should be deleted later or kept as a human-editable source distinct from `data/products.json`.
4. Whether custom local plugins are part of the repository scope or should live in separate repos/worktrees.
5. Whether `wp-content/themes/beslock-custom/docs/*.md` should stay in-theme or move to a repo-level docs convention.
6. Whether `assets/css/base/variables.css` is abandoned scaffolding or a planned future import source.

## Safe Commit Grouping Strategy

### Docs only

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- non-functional inline ownership comments in ambiguous files

### Ignore policy

- future repository-level `.gitignore` additions for logs, sqlite artifacts, and restored backup artifacts
- onboarding or local setup note clarifying that `template-parts/` and `templates/` must not be excluded locally

### Dormant cleanup

- proof-based retirement of `header-state.*`
- proof-based retirement of `menu-products-mobile.js`
- proof-based decision on `product-gallery-init.js`
- proof-based decision on theme-root `products.json`

### Runtime cleanup

- any consolidation of duplicate single-product styling surfaces
- any consolidation of duplicate header runtime surfaces
- any change affecting enqueue graphs or active templates

### Future archival

- `assets/css/base/variables.css`
- `assets/css/pages/single-product.css`
- `assets/js/product-gallery-init.js`
- theme-root `products.json`

### Commit now

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- repository-level ignore policy updates only
- developer note or onboarding note clarifying that `template-parts/` and `templates/` must not be hidden in local excludes

### Wait until next slice

- any runtime-affecting decision on `badge.css`
- any runtime-affecting decision on `pages/single-product.css`
- retirement of `header-state.*`
- retirement of `menu-products-mobile.js`
- consolidation of Kadence cleanup helpers

### Keep untracked temporarily

- importer logs
- debug logs
- local sqlite/export backups
- local vendor/theme/plugin copies used only for the local WordPress environment

### Future archive candidate

- `assets/js/menu-products-mobile.js`
- `assets/css/header-state.css`
- `assets/js/header-state.js`
- `assets/css/product-rotator.css`
- `assets/js/product-rotator.js`
- `assets/css/product-card-alt.css`
- `assets/js/product-card-alt.js`
- `assets/css/product-card-fade.css`
- `assets/js/product-card-fade.js`
- `assets/js/product-gallery-init.js`
- `assets/css/base/variables.css`

## Proposed Clean Staged Commit Plan

### Commit plan for normalization, not runtime behavior

If a normalization-only commit is created later, the clean scope should be:

1. repository ignore policy only
2. optional documentation-only normalization summary

That commit should include:

- `.gitignore` updates for logs, `.DS_Store`, and local database artifacts
- removal of the local-only exclude for `template-parts/` and `templates/` from developer setup notes or repo onboarding docs
- `WORKTREE_NORMALIZATION_SUMMARY.md`

That commit should exclude:

- plugin directories
- parent theme copies
- runtime logs
- importer output files
- unrelated infrastructure files unless they are part of the ignore-policy change itself
- any dormant asset retirement

## Next Coherent Frontend Commit

The next coherent frontend commit should not be another broad migration slice.
Based on the audit, the safest next focused frontend commit would be:

### Option A: theme source normalization

- formalize ignore policy
- remove local exclude dependence for active `template-parts/` and `templates/`
- classify or quarantine `header-state.*`, `menu-products-mobile.js`, `badge.css`, and `pages/single-product.css`

### Option B: small runtime cleanup slice

- prove and retire one dormant runtime surface only
- good candidates: `header-state.*` or `menu-products-mobile.js`

## What Should Remain Intentionally Untracked

Until a repo policy says otherwise, these should remain intentionally untracked
or locally ignored:

- importer log outputs
- debug logs
- local sqlite/export backup artifacts
- local vendor/plugin/theme copies not authored as part of the child theme
- generated debug output even when produced by first-party tooling

## Immediate Commit / Manual Validation / Archive Lists

### Files safe for immediate commit

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
- `wp-content/themes/beslock-custom/assets/css/base/variables.css`
- `wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
- `wp-content/themes/beslock-custom/inc/debug/debug.php`

### Files requiring manual validation before any future cleanup decision

- `wp-content/themes/beslock-custom/assets/css/menu-products-mobile.css`
- `wp-content/themes/beslock-custom/templates/menu-simple.php`
- `wp-content/themes/beslock-custom/templates/models-mobile.php`
- `wp-content/themes/beslock-custom/template-parts/header/mobile-drawer.php`
- `wp-content/themes/beslock-custom/template-parts/header/site-header.php`
- `wp-content/themes/beslock-custom/template-parts/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/product-features.php`
- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/data/products.json`

### Files that look like real archive candidates

- `wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
- `wp-content/themes/beslock-custom/assets/css/base/variables.css`
- `wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
- `wp-content/themes/beslock-custom/products.json`
- `wp-content/themes/beslock-custom/assets/js/menu-products-mobile.js`

## Path Resolution Layer Spec

This section defines a centralized, explicit path-resolution architecture for
canonical data, tooling, runtime theme assets, media roots, and generated
outputs.

This is a design-only slice. No code paths, includes, active routes, or
runtime behavior are changed here.

### Design goals

- decouple canonical data ownership from the active theme path
- stop inferring repository structure from duplicated `dirname()` or `__DIR__`
	chains
- keep runtime-owned theme surfaces separate from tooling-owned and
	generated-output surfaces
- give importer, exporter, sync tooling, and plugins one shared contract for
	path discovery
- preserve current behavior during migration by centralizing fallback order
	rather than changing current active paths immediately

### Proposed helper API

These helper names are recommended for a future implementation. They are not
implemented in this slice.

| Helper | Responsibility |
| --- | --- |
| `beslock_get_repo_root()` | resolve the canonical repository root |
| `beslock_get_runtime_theme_root()` | resolve the active child theme filesystem root |
| `beslock_get_runtime_theme_uri_root()` | resolve the active child theme URI root |
| `beslock_get_data_root()` | resolve the canonical data root under the repo |
| `beslock_get_products_json_path()` | resolve the canonical `products.json` path using centralized fallback policy |
| `beslock_get_tooling_root()` | resolve the shared tooling root for future utilities and bridges |
| `beslock_get_media_root()` | resolve the authored source media root used by importer and repair flows |
| `beslock_get_generated_root()` | resolve the generated/export output root |
| `beslock_get_logs_root()` | resolve the log output root |
| `beslock_get_backup_root()` | resolve the backup/undo artifact root |
| `beslock_get_export_json_path()` | resolve the exporter JSON output path |
| `beslock_get_export_sqlite_path()` | resolve the exporter SQLite output path |
| `beslock_get_products_csv_path()` | resolve the CSV output path for generator flows |
| `beslock_get_wp_bootstrap_path()` | resolve the WordPress bootstrap path for CLI/eval tooling |
| `beslock_get_media_search_roots()` | return ordered media lookup roots for importer/exporter image discovery |

### Expected helper contract

- helpers should resolve paths only; they should not perform importer/exporter
	work directly
- helpers should return normalized absolute filesystem paths, except for the
	theme URI helper
- helpers should be safe to call from theme context, plugin context, admin
	tooling, and CLI tooling
- helpers should encapsulate fallback order so that individual scripts do not
	repeat path heuristics
- helpers should log or expose resolution failure context without mutating
	runtime behavior

## Canonical Roots

This section defines the root map the future layer should expose.

### Canonical roots map

| Root | Intended owner | Proposed source | Purpose |
| --- | --- | --- | --- |
| canonical repo root | repo-owned | repository root | shared boundary for canonical data and repo-level utilities |
| canonical data root | repo-owned | `data/` under repo root | source-of-truth catalog data |
| runtime theme root | runtime-owned | active child theme root | templates, partials, CSS/JS, runtime image URL composition |
| runtime theme URI root | runtime-owned | active child theme URI | frontend asset and image URLs |
| media root | runtime-owned source media with tooling consumers | theme `assets/images/` for now | authored media used to seed/repair attachments |
| tooling root | tooling-owned | future explicit tooling layer | shared utilities and orchestration entrypoints |
| generated/export root | tooling-owned generated output | explicit output root; temporarily theme `repo_portfolio/` for compatibility | exporter JSON/SQLite outputs |
| logs root | tooling-owned generated output | explicit log root; temporarily theme `import_logs/` or uploads fallback | importer/exporter logs |
| backup root | tooling-owned generated output | explicit backup root; temporarily `repo_portfolio/` and uploads backup zones | undo payloads and repair backups |

### Root ownership split

#### Runtime-owned surfaces

- theme templates and template parts
- active frontend CSS and JS
- runtime theme image URLs
- WooCommerce presentation overrides
- media assets that must remain available for active render output

#### Canonical repo-owned surfaces

- editable catalog data
- repo-level tooling contracts
- future shared utilities for path resolution
- migration documentation and repository-level process docs

#### Tooling-owned generated surfaces

- export JSON and SQLite artifacts
- importer and exporter logs
- backup payloads
- CSV exports and temporary updated-data artifacts

## Fallback Resolution Strategy

This section defines the safe fallback chain for the future layer.

### Canonical data fallback chain

During coexistence, centralized resolution should preserve the current safe
order without leaving that logic duplicated in each consumer.

Recommended canonical data chain:

1. repo-root canonical path
2. theme-local compatibility path
3. legacy export/compatibility path
4. fail-safe logging and explicit error result

Concrete target order for `products.json`:

1. `repo-root/data/products.json`
2. `wp-content/themes/beslock-custom/data/products.json`
3. `wp-content/themes/beslock-custom/repo_portfolio/products.json`
4. structured failure with logging

### Media resolution fallback chain

Recommended media chain during migration:

1. canonical media root primary path
2. canonical media secondary search roots
3. legacy compatibility path if still declared by the resolver
4. attachment reuse / existing-media lookup
5. structured failure with logging

For the current repository, this means preserving the existing filesystem
search order behind one helper:

1. `assets/images/products/`
2. `assets/images/`
3. existing attachment lookup
4. failure log entry

### WordPress bootstrap fallback chain

Recommended bootstrap chain for CLI/tooling:

1. explicit WordPress root from known environment constant or configuration
2. repository-aware bootstrap path resolution
3. compatibility fallback for current relative-depth assumptions
4. structured failure with log context

This design avoids keeping separate `wp-load.php` heuristics in each script.

### Generated output fallback chain

Recommended output chain:

1. explicit generated/export root
2. explicit logs root or backup root depending on artifact class
3. uploads fallback only when compatibility requires it
4. temporary system fallback only for non-canonical log output
5. structured warning when canonical write target is unavailable

## Ownership Transition Plan

This section defines how ownership should evolve while old and new path models
coexist.

### Consumers by root they should use

| Consumer | Root it should use long term | Transitional note |
| --- | --- | --- |
| importer | canonical data root + media root + logs root | today still split across theme scripts and plugin logic |
| exporter | generated/export root + canonical data root for reference | should stop treating export artifacts as source-of-truth |
| sync scripts | canonical data root | should stop reading theme-local `data/products.json` directly |
| short description tooling | canonical data root or canonical importer output | should stop depending on `repo_portfolio/products.json` |
| WooCommerce image assignment | media root + attachment lookup | should not infer canonical data ownership from theme paths |
| CSV generators | generated/export root or dedicated CSV output path | should stop writing into theme `data/` by default |
| logs | logs root | should stop mixing theme-local logs with fallback-only outputs |
| backups | backup root | should stop sharing ownership with export compatibility files |

### What should stay in the theme

- runtime templates and partials
- active enqueue-owned CSS and JS
- runtime image URL composition
- WooCommerce presentation-specific code
- temporary compatibility shells that are still part of the render graph

### What should move to plugin-owned or tooling-owned layers later

- importer orchestration and shared data readers
- exporter orchestration and undo/backup handling
- short-description synchronization flows
- shared path helpers
- CLI-oriented utility wrappers and bootstrap helpers

### What should move to repo-root utilities later

- canonical data readers and validators
- shared tooling configuration
- migration-safe path contracts that are not presentation-specific
- repo-aware wrappers used by both theme-side and plugin-side tooling

### Coexistence policy during migration

- keep current active paths valid
- introduce the resolver first as a read-only abstraction
- migrate consumers one by one to the resolver while preserving current
	fallback order
- mark theme-local data and export artifacts as compatibility surfaces, not
	canonical ownership surfaces
- retire legacy paths only after every active consumer is on the centralized
	layer

## Future Tooling Migration Strategy

This section turns the ownership plan into implementation phases for a future
functional slice.

### Migration phases

#### Phase 1: contract-first resolver

- add the centralized helper API
- make no path changes yet
- expose root discovery and fallback order only

#### Phase 2: reader normalization

- repoint importer, sync scripts, and CSV generators to the resolver for data
	reads
- preserve current theme and legacy fallback behavior

#### Phase 3: output normalization

- repoint logs, backups, CSV outputs, and exporter outputs to resolver-owned
	generated roots
- keep current destination paths as compatibility targets when needed

#### Phase 4: tooling ownership cleanup

- remove theme-specific bootstrap assumptions from CLI tooling
- move shared orchestration out of `functions.php` and theme-local script
	includes

#### Phase 5: legacy path retirement

- stop reading theme-local `data/products.json`
- stop using `repo_portfolio/products.json` as an input contract
- keep only explicit compatibility bridges that still have active consumers

### Highest migration risk surfaces

- `wp-content/themes/beslock-custom/scripts/carga_portfolio_data.php`
- `wp-content/themes/beslock-custom/scripts/fix-placeholder-images.php`
- `wp-content/themes/beslock-custom/scripts/set_post_excerpts_from_products.php`
- `wp-content/themes/beslock-custom/scripts/apply_products_short_descriptions.php`
- `wp-content/themes/beslock-custom/scripts/run_carga_dry.php`
- `wp-content/plugins/beslock-portfolio-exporter/beslock-portfolio-exporter.php`
- `wp-content/plugins/short-des-exporter/short-des-exporter.php`
- theme admin tooling registered from `functions.php`

### Implementation risks to account for

| Risk | Why it is high-risk |
| --- | --- |
| `wp-load.php` bootstrap | current tooling mixes fixed-depth and walk-up heuristics; centralization can break CLI entry unexpectedly if not staged |
| CLI tooling context | scripts may run from repo root, WordPress root, or eval-file context; resolver must not assume one execution cwd |
| plugin context | plugins may execute before theme-specific assumptions are safe; repo and theme roots must be resolvable independently |
| theme context | runtime theme APIs are valid here, but canonical data should not be inferred from theme ownership |
| relative path assumptions | duplicated `dirname()` chains are fragile and hide ownership errors |
| media resolution | importer/exporter image flows still depend on theme media layout and filename conventions |
| export ownership | `repo_portfolio` is still treated as both output and compatibility input by some consumers |

### Recommended implementation order

1. implement the helper API only, with no consumer rewiring yet
2. switch canonical data readers to the helper API while preserving current fallback order
3. switch media lookup callers to shared media-root helpers
4. centralize log, backup, CSV, and export output path resolution
5. migrate plugin and CLI bootstrap callers off custom `wp-load.php` heuristics
6. retire direct reads from theme-local data and legacy export artifacts only after all consumers are centralized

## Consumer → Helper Matrix

This matrix translates the path-resolution design into an explicit
consumer-to-helper-to-root mapping.

| Consumer | Current path assumptions | Current root ownership | Proposed helper | Proposed canonical root | Required fallback chain | Migration risk | Migration phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts/carga_portfolio_data.php` | theme `data/products.json`; theme `assets/images/products/`; theme `assets/images/`; theme `import_logs/` | theme-owned data/tooling/media mix | `beslock_get_products_json_path()`, `beslock_get_media_search_roots()`, `beslock_get_logs_root()` | canonical data root, media root, logs root | repo data -> theme data -> repo_portfolio; products media -> root media -> attachment reuse -> fail-safe log | CRITICAL | Phase 2 |
| `scripts/fix-placeholder-images.php` | theme media roots; relative `wp-load.php`; uploads backup | theme-owned media, duplicated bootstrap, uploads backup | `beslock_get_media_search_roots()`, `beslock_get_wp_bootstrap_path()`, `beslock_get_backup_root()` | media root, bootstrap path, backup root | explicit bootstrap -> repo-aware bootstrap -> current relative fallback; products media -> root media -> fail-safe log | CRITICAL | Phase 3 |
| `scripts/CSV_portfolio_generator.php` | theme `data/` as CSV write target; optional importer coupling | theme-owned tooling output | `beslock_get_products_csv_path()`, `beslock_get_generated_root()` | generated/export root | generated root -> current theme data fallback -> fail-safe log | HIGH | Phase 3 |
| `scripts/apply_products_short_descriptions.php` | theme `data/products.json`; walk-up bootstrap | theme-owned data reader | `beslock_get_products_json_path()`, `beslock_get_wp_bootstrap_path()` | canonical data root | repo data -> theme data -> repo_portfolio -> fail-safe log | HIGH | Phase 2 |
| `scripts/set_post_excerpts_from_products.php` | theme `data/products.json`; walk-up bootstrap; in-script git assumptions | theme-owned data writer | `beslock_get_products_json_path()`, `beslock_get_wp_bootstrap_path()` | canonical data root | repo data -> theme data -> repo_portfolio -> fail-safe log | CRITICAL | Phase 2 |
| `scripts/run_carga_dry.php` | importer script must live in active theme; relative WordPress root | theme-owned tooling entry | `beslock_get_tooling_root()`, `beslock_get_wp_bootstrap_path()` | tooling root, bootstrap path | explicit tooling path -> current theme script fallback | HIGH | Phase 4 |
| `plugins/beslock-portfolio-exporter.php` export | hardcoded `WP_CONTENT_DIR/themes/beslock-custom`; `repo_portfolio` writes; theme import logs | theme-owned export/backup/log paths | `beslock_get_generated_root()`, `beslock_get_export_json_path()`, `beslock_get_export_sqlite_path()`, `beslock_get_logs_root()`, `beslock_get_backup_root()` | generated/export root, logs root, backup root | generated root -> current repo_portfolio compatibility path -> fail-safe log | CRITICAL | Phase 3 |
| `plugins/beslock-portfolio-exporter.php` import | root data preferred, then theme data, then repo_portfolio; theme media root | mixed canonical read + theme-owned outputs/media | `beslock_get_products_json_path()`, `beslock_get_media_search_roots()`, `beslock_get_backup_root()`, `beslock_get_logs_root()` | canonical data root, media root, backup root, logs root | repo data -> theme data -> repo_portfolio -> fail-safe log | CRITICAL | Phase 2 |
| `plugins/beslock-product-sync.php` | `ABSPATH . 'data/products.json'` | repo-owned canonical data | `beslock_get_products_json_path()` | canonical data root | repo data -> explicit fail-safe only | LOW | Phase 2 |
| `plugins/short-des-exporter.php` | hardcoded theme `repo_portfolio/products.json`; uploads log | legacy export artifact as input | `beslock_get_products_json_path()`, `beslock_get_logs_root()` | canonical data root, logs root | repo data -> theme data -> repo_portfolio -> fail-safe log | CRITICAL | Phase 4 |
| `templates/models-mobile.php` | theme `assets/images/products/` path + URI | runtime theme-owned media | `beslock_get_media_root()`, `beslock_get_runtime_theme_uri_root()` | media root, runtime theme URI root | current products media root only; no legacy non-products fallback needed | MEDIUM | Phase 3 |
| `templates/blocks/hero.php` | theme `assets/images/Hero_develp/*`; theme icon dir; direct URI/path composition | runtime theme-owned media | `beslock_get_media_root()`, `beslock_get_runtime_theme_uri_root()` | media root, runtime theme URI root | current hero media root only; preserve direct theme runtime fallback | MEDIUM | Phase 3 |
| `template-parts/content/archive_hero.php` | parent template via `get_template_directory()` | runtime parent-theme bridge | `beslock_get_runtime_theme_root()` only if documented later; no data helper needed | runtime theme/parent bridge | no migration until path layer is stable; preserve current parent fallback | HIGH | Phase 5 |
| `template-parts/cards/product-card.php` | badge asset via `get_template_directory()` and `get_template_directory_uri()` | runtime theme asset | `beslock_get_media_root()`, `beslock_get_runtime_theme_uri_root()` | media root, runtime theme URI root | current badge path only; preserve parent/theme fallback semantics | MEDIUM | Phase 3 |

## Tooling Ownership Matrix

This matrix classifies who should own each consumer long term.

| Consumer | Should remain theme-owned | Should migrate to tooling layer | Should migrate to plugin | Should migrate to repo utilities | Notes |
| --- | --- | --- | --- | --- | --- |
| `scripts/carga_portfolio_data.php` | no | yes | partial | yes | orchestration should leave the theme; shared readers should become repo utilities |
| `scripts/fix-placeholder-images.php` | no | yes | partial | yes | repair tooling should not depend on theme-local bootstrap logic |
| `scripts/CSV_portfolio_generator.php` | no | yes | possible | yes | CSV output is tooling concern, not runtime theme concern |
| `scripts/apply_products_short_descriptions.php` | no | yes | possible | yes | data sync helper should use canonical data utilities |
| `scripts/set_post_excerpts_from_products.php` | no | yes | possible | yes | should stop owning git/data logic inside theme scripts |
| `scripts/run_carga_dry.php` | no | yes | no | yes | runner wrapper belongs in tooling utilities |
| `plugins/beslock-portfolio-exporter.php` | no | partial | yes | partial | plugin is the right long-term home, but shared path/data utilities should be externalized |
| `plugins/beslock-product-sync.php` | no | no | yes | partial | canonical importer stays plugin-owned; data/path resolution can be shared utility code |
| `plugins/short-des-exporter.php` | no | partial | yes | partial | either merge into canonical sync plugin or keep as compatibility plugin |
| `templates/models-mobile.php` | yes | no | no | no | runtime-owned render surface |
| `templates/blocks/hero.php` | yes | no | no | no | runtime-owned render surface |
| `template-parts/content/archive_hero.php` | yes | no | no | no | runtime-owned bridge to parent theme |
| `template-parts/cards/product-card.php` | yes | no | no | no | runtime-owned product card leaf partial |

## Migration Risk Table

This table orders consumers by migration risk and complexity.

| Consumer | Risk | Why |
| --- | --- | --- |
| `scripts/carga_portfolio_data.php` | CRITICAL | mixes canonical data read, media lookup, logs, admin UI, image import, and Woo assignment assumptions |
| `scripts/fix-placeholder-images.php` | CRITICAL | mixes relative bootstrap logic, media lookup duplication, and backup semantics |
| `scripts/set_post_excerpts_from_products.php` | CRITICAL | writes canonical-like data, depends on theme path, and embeds git behavior |
| `plugins/beslock-portfolio-exporter.php` | CRITICAL | mixes import, export, backup, logs, media import, and compatibility fallbacks |
| `plugins/short-des-exporter.php` | CRITICAL | directly consumes legacy export artifact as input contract |
| `scripts/CSV_portfolio_generator.php` | HIGH | generated output path is theme-owned and coupled to importer availability |
| `scripts/apply_products_short_descriptions.php` | HIGH | theme-local data reader plus duplicated bootstrap heuristic |
| `scripts/run_carga_dry.php` | HIGH | wrapper hardcodes theme script location and repo/WordPress root assumptions |
| `template-parts/content/archive_hero.php` | HIGH | parent-theme fallback bridge is runtime-sensitive even though not tooling-owned |
| `templates/models-mobile.php` | MEDIUM | direct media path assumptions but limited blast radius |
| `templates/blocks/hero.php` | MEDIUM | direct media path assumptions but still purely runtime-owned |
| `template-parts/cards/product-card.php` | MEDIUM | small media dependency for badge asset, otherwise low path complexity |
| `plugins/beslock-product-sync.php` | LOW | already aligned to canonical repo-root data model |

## Bootstrap Dependency Matrix

This matrix isolates duplicated bootstrap logic and context sensitivity.

| Consumer | Bootstrap assumption | Duplicated bootstrap logic | Proposed helper | Risk |
| --- | --- | --- | --- | --- |
| `scripts/fix-placeholder-images.php` | fixed relative path to `wp-load.php` | yes | `beslock_get_wp_bootstrap_path()` | CRITICAL |
| `scripts/set_post_excerpts_from_products.php` | walk-up search for `wp-load.php` | yes | `beslock_get_wp_bootstrap_path()` | CRITICAL |
| `scripts/apply_products_short_descriptions.php` | walk-up search for `wp-load.php` | yes | `beslock_get_wp_bootstrap_path()` | HIGH |
| `scripts/run_carga_dry.php` | repo-root `chdir()` plus fixed relative bootstrap path | yes | `beslock_get_wp_bootstrap_path()` | HIGH |
| theme admin tooling in `functions.php` | assumes scripts are includable from active theme path | yes | `beslock_get_tooling_root()` | HIGH |
| plugins under normal WordPress load | WordPress already bootstrapped | no | none needed first; may later consume helper for consistency | LOW |
| runtime templates | WordPress runtime already bootstrapped | no | none needed | LOW |

## Media Resolution Dependency Matrix

This matrix isolates duplicated media lookup and runtime media path composition.

| Consumer | Media dependencies | Duplicated media lookup logic | Proposed helper | Generated output dependency |
| --- | --- | --- | --- | --- |
| `scripts/carga_portfolio_data.php` | `assets/images/products/`, `assets/images/`, filename-based attachment matching | yes | `beslock_get_media_search_roots()` | `import_logs/`, `products.updated.json` |
| `scripts/fix-placeholder-images.php` | `assets/images/products/`, `assets/images/`, slug-based glob patterns | yes | `beslock_get_media_search_roots()` | uploads backup JSON |
| `plugins/beslock-portfolio-exporter.php` import/images | theme `assets/images`, slug-based import lookup | yes | `beslock_get_media_search_roots()` | `repo_portfolio`, `import_logs/` |
| `templates/models-mobile.php` | `assets/images/products/` direct scan + URI composition | no, but direct runtime path composition exists | `beslock_get_media_root()` | none |
| `templates/blocks/hero.php` | `assets/images/Hero_develp/*`, `assets/images/icons/`, filemtime checks | no, but direct runtime path composition exists | `beslock_get_media_root()` | none |
| `template-parts/cards/product-card.php` | `assets/images/instal.png` | no | `beslock_get_media_root()` | none |

## Consumer → Reads

| Consumer | Reads |
| --- | --- |
| `scripts/carga_portfolio_data.php` | theme `data/products.json`, theme media roots, existing attachments, Woo products |
| `scripts/fix-placeholder-images.php` | Woo product attachments, theme media roots, `wp-load.php` bootstrap |
| `scripts/CSV_portfolio_generator.php` | Woo products, importer function availability |
| `scripts/apply_products_short_descriptions.php` | theme `data/products.json`, Woo products |
| `scripts/set_post_excerpts_from_products.php` | theme `data/products.json`, Woo products |
| `scripts/run_carga_dry.php` | importer script path, WordPress bootstrap |
| `plugins/beslock-portfolio-exporter.php` | Woo products, root/theme/repo `products.json`, theme media roots, current backups |
| `plugins/beslock-product-sync.php` | root `data/products.json` |
| `plugins/short-des-exporter.php` | theme `repo_portfolio/products.json`, Woo DB |
| `templates/models-mobile.php` | theme `assets/images/products/` |
| `templates/blocks/hero.php` | theme hero media and icon paths |
| `template-parts/content/archive_hero.php` | parent theme archive hero path |
| `template-parts/cards/product-card.php` | runtime badge asset path, Woo product object |

## Consumer → Writes

| Consumer | Writes |
| --- | --- |
| `scripts/carga_portfolio_data.php` | Woo products/meta, theme/import fallback logs, `products.updated.json`, options |
| `scripts/fix-placeholder-images.php` | uploads backup JSON, Woo thumbnails/gallery |
| `scripts/CSV_portfolio_generator.php` | theme `data/products_portfolio.csv` |
| `scripts/apply_products_short_descriptions.php` | Woo `post_excerpt`, option log |
| `scripts/set_post_excerpts_from_products.php` | theme `data/products.json`, optional git add/commit |
| `scripts/run_carga_dry.php` | stdout JSON only |
| `plugins/beslock-portfolio-exporter.php` | `repo_portfolio/products.json`, `repo_portfolio/products.sqlite`, `repo_portfolio/products_backup_latest.json`, `import_logs/*.log`, Woo products/meta |
| `plugins/beslock-product-sync.php` | Woo products and sync state only |
| `plugins/short-des-exporter.php` | Woo `post_excerpt`, uploads log |
| runtime templates | none |

## Consumer → Generated Outputs

| Consumer | Generated outputs |
| --- | --- |
| `scripts/carga_portfolio_data.php` | import logs, `products.updated.json` |
| `scripts/fix-placeholder-images.php` | uploads backup JSON |
| `scripts/CSV_portfolio_generator.php` | `products_portfolio.csv` |
| `scripts/run_carga_dry.php` | stdout JSON report |
| `plugins/beslock-portfolio-exporter.php` | exporter JSON, SQLite, backups, import logs |
| `plugins/short-des-exporter.php` | uploads log |
| runtime templates | none |

## Duplicated Logic Hotspots

### Duplicated path logic

- theme-local `data/products.json` resolution across multiple theme scripts
- mixed root/theme/repo fallback handling in exporter/importer surfaces
- direct theme path composition in runtime templates for media access

### Duplicated bootstrap logic

- fixed relative `wp-load.php` lookup in `fix-placeholder-images.php`
- walk-up bootstrap discovery in `set_post_excerpts_from_products.php` and `apply_products_short_descriptions.php`
- wrapper-specific repo-root bootstrap in `run_carga_dry.php`

### Duplicated media lookup logic

- repeated `assets/images/products/` then `assets/images/` search patterns in importer and repair flows
- repeated slug/glob conventions for underscore and secondary webp variants

### Duplicated export handling

- `repo_portfolio/products.json` treated both as output artifact and fallback input
- backup, undo, and excerpt tooling all assume exporter compatibility artifacts are stable contracts

## Untracked Inventory

This section classifies the current untracked set after visibility recovery.

### Current untracked set

At the time of this audit, the current untracked inventory is:

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/discover.php`
- `wp-content/themes/beslock-custom/templates/blocks/hero.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`

### Untracked inventory notes

- The current untracked set is dominated by authored theme/runtime source, not by generated artifacts.
- No `import_logs`, `repo_portfolio/*.sqlite`, `repo_portfolio/*.restored`, uploads, or cache artifacts are currently untracked in the live set.
- Generated artifact drift still exists in the worktree, but in the current snapshot it appears as tracked-modified noise such as `debug/enqueued-styles.log`, not as untracked files.

## Untracked Ownership Classification

This table assigns one primary classification to each current untracked file.

| Path | Primary classification | Ownership summary | Recommended disposition |
| --- | --- | --- | --- |
| `WORKTREE_NORMALIZATION_SUMMARY.md` | TOOLING | repository-level normalization documentation | commit now |
| `template-parts/cards/product-card.php` | RUNTIME CRITICAL | active card leaf partial in the canonical Woo product-card render chain | validate first, then track |
| `template-parts/content/archive_hero.php` | RUNTIME CRITICAL | active Woo archive suppression bridge; preserved legacy behavior toward Kadence parent | validate first, then track |
| `template-parts/header/header-widget.php` | RUNTIME CRITICAL | active reusable header partial with runtime logo/cart behavior | validate first, then track |
| `templates/blocks/discover.php` | RUNTIME CRITICAL | active homepage fallback block and direct runtime media consumer | validate first, then track |
| `templates/blocks/hero.php` | MEDIA RUNTIME | active homepage hero surface with direct theme media dependencies | validate first, then track |
| `templates/blocks/product-card.php` | PRESERVED LEGACY | compatibility wrapper for older portfolio-array flow; not the canonical active card owner | validate manually before any tracking decision |
| `templates/blocks/products-portfolio.php` | RUNTIME CRITICAL | active storefront/homepage fallback block using Woo loop rendering | validate first, then track |

### Secondary classification tags

| Path | Secondary tags |
| --- | --- |
| `WORKTREE_NORMALIZATION_SUMMARY.md` | docs-only, non-runtime |
| `template-parts/cards/product-card.php` | canonical frontend source |
| `template-parts/content/archive_hero.php` | preserved legacy, runtime bridge |
| `template-parts/header/header-widget.php` | canonical frontend source |
| `templates/blocks/discover.php` | canonical frontend source, media runtime |
| `templates/blocks/hero.php` | canonical frontend source, media runtime |
| `templates/blocks/product-card.php` | preserved legacy, future archive candidate |
| `templates/blocks/products-portfolio.php` | canonical frontend source |

### Categories not present in the current untracked set

- `CANONICAL DATA`: none currently untracked
- `GENERATED`: none currently untracked
- `LOCAL ONLY`: none currently untracked
- `FUTURE ARCHIVE CANDIDATE`: only `templates/blocks/product-card.php` appears in this role today
- accidental local files: none identified in the current untracked set

## Recommended Tracking Policy

This section separates future tracking policy from immediate action.

### Should eventually track

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

### Requires manual validation first

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/product-card.php`
- `templates/blocks/products-portfolio.php`

### Looks safe to keep untracked temporarily until classification is closed

- `templates/blocks/product-card.php` because it is preserved legacy and not the canonical active card owner

### Ignore permanently

No current untracked file qualifies for a permanent ignore recommendation in this slice.

### Appears accidental or purely local

No current untracked file appears accidental, editor-local, cache-local, or machine-local.

## Safe Future Tracking Plan

This plan defines safe grouping without applying tracking changes now.

### Commit now group

- `WORKTREE_NORMALIZATION_SUMMARY.md`

### Validate first group

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

### Validate carefully before any decision

- `templates/blocks/product-card.php`

### Ignore permanently group

- none from the current untracked set

### Archive later group

- `templates/blocks/product-card.php` as a future archive candidate once its compatibility role is explicitly retired

### Mixed authored vs generated surface warning

- The current untracked set itself is authored source-heavy.
- The broader worktree still mixes generated artifacts with authored theme surfaces, especially under `debug/`, `import_logs/`, and `repo_portfolio/`, but those are not currently part of the untracked set shown by Git.

### Safe tracking policy summary

- do not mass-add all untracked files
- treat the recovered template and template-part files as likely track-worthy source after proof-based validation
- do not classify legacy wrappers as safe-to-track automatically just because they are visible again
- keep generated/log/export artifacts out of the future tracking plan unless a repository policy explicitly promotes them

## Tracking Commit Matrix

This section converts the untracked classification into explicit commit buckets.

### File → commit bucket

| File | Commit bucket | Ownership actual | Runtime participation | Canonical owner status | Migration risk | Recommended action | Tracking recommendation | Commit phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `WORKTREE_NORMALIZATION_SUMMARY.md` | COMMIT_NOW | repository-level normalization documentation | none | canonical documentation surface for this audit stream | LOW | keep as standalone documentation commit candidate | track independently from runtime source | Phase 1 |
| `template-parts/cards/product-card.php` | VALIDATE_FIRST | active theme runtime partial | direct active participation through product-card render chain | canonical active card leaf partial | HIGH | validate render ownership and template usage, then track | should be tracked after proof pass | Phase 2 |
| `template-parts/content/archive_hero.php` | VALIDATE_FIRST | active runtime bridge to Kadence parent behavior | direct active participation for Woo archive hero suppression | canonical active suppression bridge, preserved parent fallback | HIGH | validate archive suppression behavior, then track | should be tracked after proof pass | Phase 2 |
| `template-parts/header/header-widget.php` | VALIDATE_FIRST | active theme runtime partial | direct active participation where header widget path is used | active reusable header partial, not a fallback-only artifact | HIGH | validate inclusion sites and runtime ownership, then track | should be tracked after proof pass | Phase 2 |
| `templates/blocks/discover.php` | VALIDATE_FIRST | active homepage/runtime fallback block | direct active participation from `front-page.php` fallback chain | canonical active fallback block today | HIGH | validate fallback routing and media dependency, then track | should be tracked after proof pass | Phase 2 |
| `templates/blocks/hero.php` | VALIDATE_FIRST | active homepage/runtime fallback block with theme media | direct active participation from `front-page.php` fallback chain | canonical active fallback block today | HIGH | validate fallback routing and media ownership, then track | should be tracked after proof pass | Phase 2 |
| `templates/blocks/products-portfolio.php` | VALIDATE_FIRST | active storefront/homepage fallback block | direct active participation from `front-page.php` fallback chain | canonical active fallback block today | HIGH | validate loop/render ownership, then track | should be tracked after proof pass | Phase 2 |
| `templates/blocks/product-card.php` | FUTURE_ARCHIVE_CANDIDATE | preserved compatibility wrapper | not the canonical active card owner | preserved legacy wrapper, not canonical owner | MEDIUM | keep visible, do not auto-track with runtime batch | leave untracked temporarily until explicit legacy decision | Phase 4 |

## Safe Commit Sequencing

This section proposes a safe incremental commit order without applying any git
operation in this slice.

### Proposed commit phases

#### Phase 1: docs only

Include only:

- `WORKTREE_NORMALIZATION_SUMMARY.md`

Rationale:

- isolates normalization/audit intent from runtime source recovery
- keeps blame/history clear for documentation work
- avoids mixing policy documentation with recovered render surfaces

#### Phase 2: recovered runtime surfaces

Candidate set after manual validation:

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

Rationale:

- these surfaces participate in active runtime or active fallback routing
- they represent recovered authored source rather than tooling or generated noise
- they should be grouped as visibility-recovered runtime source, not mixed with legacy cleanup

#### Phase 3: tooling normalization

Not part of the current untracked set, but this should remain a separate future
commit category for any path/tooling work.

#### Phase 4: archive cleanup or preserved legacy decision

Candidate set:

- `templates/blocks/product-card.php`

Rationale:

- preserved wrapper status introduces ownership ambiguity
- should not share a commit with active recovered runtime surfaces

### Files that should not enter the same commit

- `WORKTREE_NORMALIZATION_SUMMARY.md` should not be bundled with recovered runtime surfaces if the goal is a clean docs-only first commit.
- `templates/blocks/product-card.php` should not be bundled with `template-parts/cards/product-card.php` because that mixes canonical active ownership with preserved legacy wrapper status.
- `template-parts/content/archive_hero.php` should not be bundled with any future parent-theme cleanup or archive-behavior refactor because it currently acts as an active bridge.
- recovered runtime surfaces should not be bundled with future generated-artifact ignore policy changes, to avoid mixing authored source recovery with hygiene policy.

### Merge-noise and blame-clarity notes

| File | Merge noise risk | Ownership confusion risk | History clarity risk |
| --- | --- | --- | --- |
| `WORKTREE_NORMALIZATION_SUMMARY.md` | LOW | LOW | LOW |
| `template-parts/cards/product-card.php` | MEDIUM | HIGH because `templates/blocks/product-card.php` still exists as a wrapper | HIGH if committed together with wrapper decisions |
| `template-parts/content/archive_hero.php` | MEDIUM | HIGH because it looks legacy but is active | HIGH if mixed with archive cleanup work |
| `template-parts/header/header-widget.php` | MEDIUM | MEDIUM due to multiple inclusion sites | MEDIUM |
| `templates/blocks/discover.php` | MEDIUM | MEDIUM because it is active through fallback routing | MEDIUM |
| `templates/blocks/hero.php` | MEDIUM | MEDIUM because it is active through fallback routing and media-heavy | MEDIUM |
| `templates/blocks/products-portfolio.php` | MEDIUM | MEDIUM due to fallback routing and Woo loop delegation | MEDIUM |
| `templates/blocks/product-card.php` | HIGH | HIGH because it overlaps semantically with canonical product-card ownership | HIGH |

## Runtime Surface Tracking Policy

This section states the tracking rule for recovered runtime/theme source.

### Policy

- active recovered runtime surfaces should not remain untracked indefinitely
- active recovered runtime surfaces should be tracked only after a proof-based validation pass confirms their current ownership role
- fallback runtime blocks used by `front-page.php` should be treated as track-worthy runtime source, not as optional content snippets
- bridge templates that look legacy but still control runtime behavior should be tracked separately from archive/cleanup work

### Runtime-critical recovered files in scope

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

### Files to keep out of the first runtime tracking batch

- `templates/blocks/product-card.php`

Reason:

- it behaves as a preserved wrapper and not as the canonical active card owner
- tracking it together with canonical recovered card surfaces would increase ownership confusion

## Legacy Wrapper Tracking Notes

This section isolates preserved wrappers and bridge surfaces from canonical
active owners.

### Preserved legacy wrapper in the current untracked set

| File | Wrapper type | Why not `COMMIT_NOW` | Recommended interim state |
| --- | --- | --- | --- |
| `templates/blocks/product-card.php` | preserved compatibility wrapper | not the canonical active owner; overlaps with tracked product-card ownership decisions; future archive candidate | KEEP_UNTRACKED_TEMPORARILY |

### Active bridge surfaces that are not wrappers to defer automatically

| File | Bridge type | Why it still belongs to runtime tracking policy |
| --- | --- | --- |
| `template-parts/content/archive_hero.php` | runtime bridge to parent theme archive behavior | actively suppresses Woo archive hero output and therefore participates in runtime |

### Commit bucket summary by required bucket

#### COMMIT_NOW

- `WORKTREE_NORMALIZATION_SUMMARY.md`

#### VALIDATE_FIRST

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

#### PRESERVED_LEGACY

- `templates/blocks/product-card.php`

#### KEEP_UNTRACKED_TEMPORARILY

- `templates/blocks/product-card.php`

#### FUTURE_ARCHIVE_CANDIDATE

- `templates/blocks/product-card.php`

## Staging Checklist

This section translates the tracking policy into a reproducible staging
checklist without executing any git action in this slice.

### Phase 1: docs-only commit

#### Files to stage

- `WORKTREE_NORMALIZATION_SUMMARY.md`

#### Files explicitly NOT to stage

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/product-card.php`
- `templates/blocks/products-portfolio.php`
- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/*.json`
- `wp-content/themes/beslock-custom/repo_portfolio/*.restored`

#### Validation required before staging

- documentation diff review only
- ensure the summary reflects the intended policy and does not claim actions not taken

#### Runtime verification required

- none beyond confirming this is docs-only

#### Git status expectation before commit

- staged: only `WORKTREE_NORMALIZATION_SUMMARY.md`
- unstaged/untracked: all runtime surfaces and generated noise remain outside the commit

#### Rollback consideration

- docs-only staging should be discardable without affecting runtime or tooling state

### Phase 2: recovered runtime surfaces

#### Files to stage

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

#### Files explicitly NOT to stage

- `WORKTREE_NORMALIZATION_SUMMARY.md` if Phase 1 already shipped separately
- `templates/blocks/product-card.php`
- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/assets/css/base/variables.css`
- `wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
- `wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/inc/debug/debug.php`
- all logs, sqlite artifacts, exports, and backups

#### Validation required before staging

- manual diff review of each recovered runtime file
- ownership review against the canonical/bridge classification already documented
- check that no preserved wrapper is accidentally staged with active owners

#### Runtime verification required

- homepage verification for `hero.php`, `discover.php`, and `products-portfolio.php`
- header verification for `header-widget.php` where applicable
- Woo archive verification for `archive_hero.php`
- product-card verification for `template-parts/cards/product-card.php`

#### Git status expectation before commit

- staged: only the six recovered runtime surfaces
- unstaged/untracked: legacy wrapper remains outside staging
- generated and debug noise remains unstaged

#### Rollback consideration

- if validation fails, unstage the entire batch and split by surface rather than patching the commit scope ad hoc

### Phase 3: tooling normalization

#### Files to stage

- none from the current untracked set yet
- future tooling files only after a separate tooling slice exists

#### Files explicitly NOT to stage

- recovered runtime surfaces from Phase 2
- `templates/blocks/product-card.php`
- generated outputs, exporter artifacts, backups, sqlite, logs, cache-like files

#### Validation required before staging

- importer/exporter verification
- path-resolution verification
- CLI/bootstrap verification when tooling code changes exist later

#### Runtime verification required

- importer behavior unchanged
- exporter behavior unchanged
- no dependency-graph changes leaking into runtime theme behavior

#### Git status expectation before commit

- tooling-only diff, no runtime templates mixed in

#### Rollback consideration

- revert staging scope to the tooling slice only; never compensate by bundling runtime files into the same commit

### Phase 4: legacy/archive decisions

#### Files to stage

- `templates/blocks/product-card.php` only after an explicit preserved-legacy decision

#### Files explicitly NOT to stage

- active recovered runtime surfaces if they were not already committed separately
- docs-only files
- generated artifacts, backups, exports, logs, sqlite, cache-like files

#### Validation required before staging

- manual diff review
- ownership confirmation that the wrapper is still preserved legacy rather than active canonical owner
- archive/retention decision documented first

#### Runtime verification required

- verify no active render path still depends on the wrapper as a canonical surface

#### Git status expectation before commit

- staged: only the preserved legacy file or an explicitly scoped legacy batch

#### Rollback consideration

- if ownership remains ambiguous, keep it untracked temporarily rather than forcing it into a legacy commit

## Commit Execution Plan

This section proposes the exact safe command sequence to execute later. These
commands are recommendations only and are not executed in this slice.

### Phase 1 safe command sequence

```bash
git status --short --untracked-files=all
git add -- WORKTREE_NORMALIZATION_SUMMARY.md
git diff --cached -- WORKTREE_NORMALIZATION_SUMMARY.md
git status --short
git commit -m "docs: add worktree normalization audit summary"
```

### Phase 2 safe command sequence

```bash
git status --short --untracked-files=all
git add -- \
	wp-content/themes/beslock-custom/template-parts/cards/product-card.php \
	wp-content/themes/beslock-custom/template-parts/content/archive_hero.php \
	wp-content/themes/beslock-custom/template-parts/header/header-widget.php \
	wp-content/themes/beslock-custom/templates/blocks/discover.php \
	wp-content/themes/beslock-custom/templates/blocks/hero.php \
	wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php
git diff --cached -- \
	wp-content/themes/beslock-custom/template-parts/cards/product-card.php \
	wp-content/themes/beslock-custom/template-parts/content/archive_hero.php \
	wp-content/themes/beslock-custom/template-parts/header/header-widget.php \
	wp-content/themes/beslock-custom/templates/blocks/discover.php \
	wp-content/themes/beslock-custom/templates/blocks/hero.php \
	wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php
git status --short
git commit -m "theme: track recovered runtime surfaces"
```

### Phase 3 safe command sequence

```bash
git status --short --untracked-files=all
# stage only tooling files from the future tooling slice
git diff --cached
git status --short
git commit -m "tooling: normalize path and ownership surfaces"
```

### Phase 4 safe command sequence

```bash
git status --short --untracked-files=all
git add -- wp-content/themes/beslock-custom/templates/blocks/product-card.php
git diff --cached -- wp-content/themes/beslock-custom/templates/blocks/product-card.php
git status --short
git commit -m "theme: classify preserved legacy product-card wrapper"
```

### Explicitly excluded from any staging sequence

- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/*.json`
- `wp-content/themes/beslock-custom/repo_portfolio/*.restored`
- cache-like outputs and local backups

## Validation Gates

This section defines the verification gates before each staging action.

### Manual diff review required

- `WORKTREE_NORMALIZATION_SUMMARY.md`
- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/product-card.php`
- `templates/blocks/products-portfolio.php`

### Runtime screenshot or visual verification recommended

- `templates/blocks/hero.php`
- `templates/blocks/discover.php`
- `templates/blocks/products-portfolio.php`
- `template-parts/header/header-widget.php`
- `template-parts/cards/product-card.php`

### WooCommerce verification recommended

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `templates/blocks/products-portfolio.php`

### Importer/exporter verification required

- none for Phase 1 and Phase 2 docs/runtime tracking-only commits
- mandatory later for any Phase 3 tooling commit

### Recommended manual verification order

1. docs diff review
2. product-card runtime surface verification
3. archive hero suppression verification
4. header widget verification
5. homepage hero and discover verification
6. homepage/storefront products-portfolio verification
7. only later, tooling/importer/exporter verification for tooling commits

## Rollback Strategy

This section defines how to back out safely if a staging boundary is crossed.

### Staging rollback principles

- if a docs-only phase accidentally includes runtime files, unstage everything and restage the docs file only
- if a runtime phase accidentally includes `templates/blocks/product-card.php`, unstage it and keep it for the legacy phase
- if any generated artifact appears in staged diff, unstage the entire batch and rebuild the staging set explicitly
- never correct a contaminated staging set by expanding the commit scope; shrink it back to the intended phase

### Safe rollback commands to use later

```bash
git restore --staged WORKTREE_NORMALIZATION_SUMMARY.md
git restore --staged wp-content/themes/beslock-custom/template-parts/cards/product-card.php
git restore --staged wp-content/themes/beslock-custom/template-parts/content/archive_hero.php
git restore --staged wp-content/themes/beslock-custom/template-parts/header/header-widget.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/discover.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/hero.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/product-card.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php
```

These commands are recommended as unstage operations only. They do not discard
working tree content.

## Never-Stage-Together Matrix

This matrix defines combinations that should remain separated to preserve
ownership clarity.

| Group A | Group B | Why they should never stage together |
| --- | --- | --- |
| `WORKTREE_NORMALIZATION_SUMMARY.md` | recovered runtime surfaces | docs-only commit should remain isolated from runtime source recovery |
| `template-parts/cards/product-card.php` | `templates/blocks/product-card.php` | canonical active card owner should not be mixed with preserved legacy wrapper |
| `template-parts/content/archive_hero.php` | future archive/cleanup changes | active runtime bridge should not be conflated with archive cleanup intent |
| recovered runtime surfaces | tooling normalization files | runtime ownership recovery and tooling/path normalization are separate concerns |
| authored source | logs/sqlite/exports/backups | generated outputs would pollute blame, review scope, and tracking policy |
| runtime surfaces | tracked-modified debug/debt files such as `enqueued-styles.log`, `variables.css`, `single-product.css`, `product-gallery-init.js`, `header.php`, `inc/debug/debug.php` | those are different slices with different ownership and validation needs |

## Runtime Surface Review

This section is the file-by-file pre-stage review for the recovered runtime
surfaces targeted by the future runtime tracking phase.

### Individual runtime surface review

| File under review | Ownership actual | Canonical owner status | Runtime participation real | Bridge / delegator role | Preserved legacy role | Dependency relationships | Enqueue / runtime coupling | Migration risk | Tracking risk | Archive risk | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `template-parts/cards/product-card.php` | active theme runtime leaf partial | canonical active card leaf owner | direct, active via `woocommerce/content-product.php` -> `template-parts/product-card.php` -> this file | no; it is the leaf render target, not the delegator | no | depends on Woo product object, permalink/add-to-cart flow, install badge asset, and the delegating `template-parts/product-card.php` surface | runtime-coupled through Woo loop rendering, not enqueue-coupled | HIGH | HIGH due to overlapping product-card naming surfaces | LOW | `VALIDATE_MORE` |
| `template-parts/content/archive_hero.php` | active runtime bridge | canonical active suppression bridge for Woo archive hero behavior | direct, active on Woo shop/product archive contexts | yes; defers to Kadence parent for non-Woo contexts | yes; preserved compatibility toward parent archive behavior | depends on Woo conditional functions, parent template availability, and child/parent archive behavior contract | runtime-coupled through template loading, not enqueue-coupled | HIGH | HIGH because it looks legacy while remaining active | LOW | `VALIDATE_MORE` |
| `template-parts/header/header-widget.php` | active theme runtime partial | active reusable header partial, canonical for the widgetized/header include path | direct where included from `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` | no thin delegation inside the file itself | no | depends on logo asset, cart URL/cart count, Woo availability, and multiple include sites | runtime-coupled through include paths, not enqueue-coupled | MEDIUM | MEDIUM because of multiple inclusion sites | LOW | `VALIDATE_MORE` |
| `templates/blocks/discover.php` | active homepage fallback block | canonical active fallback block today | direct, active from `front-page.php` fallback routing | yes only in the sense that `front-page.php` delegates to it when `template-parts/discover.php` is absent | no | depends on `front-page.php` fallback chain and `assets/images/discover.png` | coupled to homepage runtime and discover styling; no special Woo coupling | MEDIUM | LOW | LOW | `TRACK_NOW` |
| `templates/blocks/hero.php` | active homepage fallback block | canonical active fallback block today | direct, active from `front-page.php` fallback routing | yes only in the sense that `front-page.php` delegates to it when `template-parts/hero.php` is absent | no | depends on `front-page.php` fallback chain, hero media tree, icon assets, and hero CSS/JS runtime | tightly coupled to homepage runtime and theme media paths | MEDIUM | MEDIUM because of media-heavy footprint | LOW | `TRACK_NOW` |
| `templates/blocks/products-portfolio.php` | active storefront/homepage fallback block | canonical active fallback block today | direct, active from `front-page.php` fallback routing | yes only in the sense that `front-page.php` delegates to it when `template-parts/products.php` is absent | no | depends on Woo query loop, `wc_get_template_part( 'content', 'product' )`, and product-card runtime ownership | coupled to Woo loop rendering but not to importer/exporter flows | MEDIUM | MEDIUM because it bridges homepage routing into Woo loop rendering | LOW | `TRACK_NOW` |

### Review notes

- `template-parts/cards/product-card.php` is not a legacy wrapper. The overlapping ownership risk comes from nearby delegators and preserved compatibility templates with similar names.
- `template-parts/content/archive_hero.php` is not accidental duplication. It is an active bridge that suppresses Woo archive hero output and only defers to the parent theme for non-Woo contexts.
- `template-parts/header/header-widget.php` is active runtime source, but it has enough inclusion surfaces to justify one more manual validation pass before tracking.
- `templates/blocks/discover.php`, `templates/blocks/hero.php`, and `templates/blocks/products-portfolio.php` behave as active fallback blocks, not legacy wrappers.

## Runtime Tracking Readiness

This section turns the review into an explicit readiness gate.

### Runtime surfaces ready for tracking

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

Reasoning:

- each file has clear active runtime participation through the `front-page.php` fallback chain
- none of the three behaves as a preserved legacy wrapper
- their ownership is locally coherent enough to track as recovered runtime source once the runtime batch is opened

### Runtime surfaces needing deeper validation

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`

Reasoning:

- `template-parts/cards/product-card.php` overlaps semantically with nearby product-card delegators and preserved compatibility templates
- `template-parts/content/archive_hero.php` is an active bridge surface and should not be tracked casually as if it were a plain content template
- `template-parts/header/header-widget.php` has multiple include sites and should be validated once more for ownership clarity

### Likely legacy wrappers

- none among the six files under this runtime pre-stage review

### Preserved bridge surfaces

- `template-parts/content/archive_hero.php`

### Fallback-only active surfaces

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

These are still active runtime surfaces even though their activation depends on
`front-page.php` fallback routing rather than on a primary `template-parts/*`
owner.

## Wrapper/Fallback Audit

This section isolates overlapping responsibilities and delegator relationships.

### Duplicated or overlapping runtime responsibilities

- product-card responsibility is split across:
	`woocommerce/content-product.php`
	`template-parts/product-card.php`
	`template-parts/cards/product-card.php`
	preserved compatibility wrapper `templates/blocks/product-card.php`
- homepage composition responsibility is split across `front-page.php` and the
	fallback block files for hero, products, and discover
- archive hero behavior is split between child override suppression logic and
	Kadence parent fallback rendering

### Bridge templates

- `template-parts/content/archive_hero.php`

### Fallback blocks

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

### Legacy wrappers in nearby ownership graph, but not in this review set

- `templates/blocks/product-card.php`

### Files that should not be mixed casually in a future runtime commit

- `template-parts/cards/product-card.php` with `templates/blocks/product-card.php`
- `template-parts/content/archive_hero.php` with any archive-cleanup or parent-theme normalization slice
- `template-parts/header/header-widget.php` with unrelated header cleanup or header-state retirement work

## Runtime Surface Risk Notes

This section defines validation and grouping implications.

### Files that could enter together in a future runtime commit

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

This is the safest future runtime commit group because these three files share
the same fallback-routing ownership model from `front-page.php`.

### Files that should not be mixed into that first runtime group

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`

### Screenshot validation recommended

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`
- `template-parts/header/header-widget.php`
- `template-parts/cards/product-card.php`

### WooCommerce validation recommended

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `templates/blocks/products-portfolio.php`
- `template-parts/header/header-widget.php` for cart/count behavior where rendered

### Importer / exporter validation required

- none for the six reviewed runtime surfaces as a precondition to tracking

### Highest-risk runtime tracking mistake

- treating `template-parts/content/archive_hero.php` as disposable legacy and bundling it with cleanup work instead of tracking it as an active bridge surface

### Safest future runtime commit group

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`

## Ownership Ambiguity Review

This section resolves the remaining ownership ambiguity for the three runtime
surfaces that were still classified as `VALIDATE_MORE`.

### Deep review by file

| File | Include graph | Render ownership | Bridge / delegation behavior | Wrapper behavior | Fallback behavior | Parent theme coupling | WooCommerce coupling | Ownership overlap detected | Final determination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `template-parts/cards/product-card.php` | `woocommerce/content-product.php` -> `template-parts/product-card.php` -> `template-parts/cards/product-card.php`; nearby compatibility wrapper `templates/blocks/product-card.php` delegates back into `template-parts/product-card.php` | canonical active leaf render owner for card markup | receives delegated control from `template-parts/product-card.php`, but does not delegate further | no | no | none | direct and active via Woo product object, add-to-cart behavior, and product loop rendering | yes, but overlap is around neighboring delegators/wrappers, not inside this file | canonical owner |
| `template-parts/content/archive_hero.php` | child theme override loaded on archive hero path; returns early for Woo contexts; otherwise includes parent archive hero template | canonical active suppression bridge for Woo archive hero behavior | yes, explicit bridge to parent behavior for non-Woo archives | no | yes, parent fallback for non-Woo contexts | high | indirect but active because it gates Woo archive hero output | yes, between child override suppression and parent fallback rendering | active bridge |
| `template-parts/header/header-widget.php` | loaded through duplicated helper functions in `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` | canonical template partial for the header widget markup | yes, but the delegation ambiguity lives in loader helpers, not the template file | no | no | none | moderate via cart URL/cart count behavior | yes, because three helper-definition surfaces point to the same template | canonical partial with duplicated loader responsibility around it |

### File-specific conclusions

#### `template-parts/cards/product-card.php`

- active runtime participant: yes
- canonical owner: yes, for final card markup
- wrapper: no
- fallback surface: no
- compatibility layer: no
- duplicated responsibility surface: only indirectly, because `template-parts/product-card.php` delegates into it and `templates/blocks/product-card.php` remains a preserved compatibility wrapper nearby

Final recommendation: `TRACK_NOW`

#### `template-parts/content/archive_hero.php`

- active runtime participant: yes
- canonical owner: yes, but specifically as a bridge/suppression surface, not as a full content owner
- wrapper: no
- fallback surface: yes, for non-Woo archive behavior through parent include
- compatibility layer: yes
- duplicated responsibility surface: yes, between child override logic and parent archive rendering contract

Final recommendation: `PRESERVE_AS_BRIDGE`

#### `template-parts/header/header-widget.php`

- active runtime participant: yes
- canonical owner: yes, for the widget template markup itself
- wrapper: no
- fallback surface: no
- compatibility layer: limited, but helper definitions around it are duplicated across multiple loader surfaces
- duplicated responsibility surface: yes, not in markup, but in helper/loader registration ownership

Final recommendation: `TRACK_LATER`

## Bridge Surface Analysis

This section isolates true bridge behavior from normal template ownership.

### True bridge surface

- `template-parts/content/archive_hero.php`

Reason:

- it conditionally suppresses Woo archive hero output in the child theme
- it preserves parent Kadence archive behavior for non-Woo contexts
- its runtime purpose is bridge/suppression, not plain template rendering

### Bridge-risk surface

- `template-parts/content/archive_hero.php`

Tracking implication:

- it should not be staged with cleanup, parent-theme normalization, or archive refactors
- if tracked, it should be described as a preserved active bridge rather than as a normal recovered template

## Delegation/Wrapper Analysis

This section clarifies where the remaining ambiguity lives.

### Product-card delegation chain

- `woocommerce/content-product.php` is the Woo loop delegator
- `template-parts/product-card.php` is the runtime delegator into the leaf partial
- `template-parts/cards/product-card.php` is the canonical leaf owner
- `templates/blocks/product-card.php` is the preserved compatibility wrapper outside the canonical owner chain

Conclusion:

- ambiguity exists around the chain, but `template-parts/cards/product-card.php` itself is no longer ambiguous enough to block tracking

### Header-widget delegation chain

- `functions.php` defines a helper that loads `template-parts/header/header-widget.php`
- `inc/header-widget.php` defines the same helper contract again behind `function_exists` guards
- `inc/features/header.php` defines the same helper contract again behind `function_exists` guards
- all three loaders converge on the same template partial

Conclusion:

- the template file is stable, but loader ownership is duplicated
- future ownership normalization should target the helper-definition surfaces, not the template markup first

### Wrapper-risk surfaces

- none among the three files under this deep review
- wrapper risk remains adjacent at `templates/blocks/product-card.php`, which stays outside the first runtime tracking batch

## Runtime Ownership Final Recommendation

This section closes the last ownership gate for the ambiguous runtime set.

### Final recommendation by file

| File | Final recommendation | Why |
| --- | --- | --- |
| `template-parts/cards/product-card.php` | `TRACK_NOW` | canonical active leaf owner; overlap exists around delegators, not in the file itself |
| `template-parts/content/archive_hero.php` | `PRESERVE_AS_BRIDGE` | active bridge with parent-theme coupling; track only as a bridge-preservation surface |
| `template-parts/header/header-widget.php` | `TRACK_LATER` | template is active, but helper-definition ownership around it is still duplicated |

### Files that can coexist in one runtime commit

- `template-parts/cards/product-card.php` can coexist with the previously ready fallback blocks:
	`templates/blocks/discover.php`
	`templates/blocks/hero.php`
	`templates/blocks/products-portfolio.php`

### Files that should not be mixed into that same runtime commit

- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`
- `templates/blocks/product-card.php`

### Screenshot verification required

- `template-parts/cards/product-card.php`
- `template-parts/header/header-widget.php`

### WooCommerce verification required

- `template-parts/cards/product-card.php`
- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`

### Parent-theme verification required

- `template-parts/content/archive_hero.php`

### Ownership-safe runtime surfaces from this ambiguity set

- `template-parts/cards/product-card.php`

### Bridge-risk surfaces

- `template-parts/content/archive_hero.php`

### Wrapper-risk surfaces

- none in this ambiguity set

### Files that should remain temporarily outside tracking

- `template-parts/content/archive_hero.php`
- `template-parts/header/header-widget.php`

### Safest runtime tracking batch after this review

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`
- `template-parts/cards/product-card.php`

## Phase 2 Runtime Batch Proposal

This section defines the first small runtime tracking batch that is now safe to
prepare, but not yet execute.

### Proposed batch contents

Included files:

- `wp-content/themes/beslock-custom/templates/blocks/discover.php`
- `wp-content/themes/beslock-custom/templates/blocks/hero.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`

Explicitly excluded files:

- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/*.json`
- `wp-content/themes/beslock-custom/repo_portfolio/*.restored`
- any logs, exports, backups, caches, or unrelated tracked-modified debt files

### Batch rationale

- `discover.php`, `hero.php`, and `products-portfolio.php` share the same `front-page.php` fallback-routing ownership model.
- `template-parts/cards/product-card.php` is now resolved as the canonical active card leaf owner.
- None of the four files is a preserved wrapper.
- None of the four files carries parent-theme bridge ambiguity strong enough to block a first runtime batch.

### Final coexistence check for the four files

| File | Runtime participation | Canonical owner status | Include graph stability | WooCommerce coupling | Parent-theme coupling | Batch fit |
| --- | --- | --- | --- | --- | --- | --- |
| `templates/blocks/discover.php` | active via `front-page.php` fallback | active fallback owner today | stable | low | none | yes |
| `templates/blocks/hero.php` | active via `front-page.php` fallback | active fallback owner today | stable | low | none | yes |
| `templates/blocks/products-portfolio.php` | active via `front-page.php` fallback | active fallback owner today | stable | medium through Woo loop rendering | none | yes |
| `template-parts/cards/product-card.php` | active via Woo loop render chain | canonical active leaf owner | stable owner chain after ambiguity review | high | none | yes |

### Hidden dependency review

- no hidden parent-theme bleedthrough was found for the four included files
- no shared bridge file is required from `archive_hero.php`
- no shared duplicated loader contract like the one around `header-widget.php` blocks this batch
- the only nearby ownership overlap is the preserved wrapper `templates/blocks/product-card.php`, which remains excluded

## Runtime Batch Boundaries

This section defines what belongs inside and outside the first runtime batch.

### Included boundary

- active homepage fallback surfaces:
	`templates/blocks/discover.php`
	`templates/blocks/hero.php`
	`templates/blocks/products-portfolio.php`
- canonical Woo card leaf partial:
	`template-parts/cards/product-card.php`

### Excluded boundary

- active bridge surfaces:
	`template-parts/content/archive_hero.php`
- duplicated loader ownership surfaces:
	`template-parts/header/header-widget.php`
- preserved legacy wrapper surfaces:
	`templates/blocks/product-card.php`
- generated and local-only outputs:
	logs, exports, backups, sqlite artifacts, cache-like files
- unrelated tracked-modified debt:
	`variables.css`, `single-product.css`, `product-gallery-init.js`, `header.php`, `inc/debug/debug.php`, `enqueued-styles.log`

### Files that must not be added by accident during this batch

- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`

## Runtime Batch Validation Plan

This section defines the validation order and commit blockers for the future
batch execution.

### Pre-stage checks

1. confirm current untracked set still contains exactly the intended four runtime files plus excluded surfaces
2. confirm excluded tracked-modified files remain unstaged
3. review each target file diff individually before any collective staging

### Validation targets

#### Screenshot or visual validation

- `templates/blocks/discover.php`
- `templates/blocks/hero.php`
- `templates/blocks/products-portfolio.php`
- `template-parts/cards/product-card.php`

#### WooCommerce verification

- `templates/blocks/products-portfolio.php`
- `template-parts/cards/product-card.php`

#### Parent-theme verification

- none required for the four-file batch

#### Importer / exporter verification

- none required for this runtime-only tracking batch

### Runtime validation order

1. homepage render with fallback hero/discover/products sections
2. visual pass on hero media and discover section
3. storefront/homepage products loop rendering
4. product-card render verification inside Woo loop contexts

### Commit blockers

- any excluded file appears in the staged diff
- `templates/blocks/product-card.php` is accidentally staged
- `template-parts/content/archive_hero.php` or `template-parts/header/header-widget.php` is accidentally staged
- `debug/enqueued-styles.log` or any generated artifact appears in staged diff
- visual/runtime verification shows ownership mismatch or missing render output

### Validation failures that should stop the batch

- hero/discover/products fallback routing does not behave as expected on the homepage
- product cards render differently than the currently accepted runtime behavior
- staged diff shows bridge, wrapper, log, export, or backup surfaces outside the intended four-file scope

## Runtime Batch Rollback Plan

This section defines the safe rollback path if the future batch is staged and
then rejected.

### Exact future staging sequence

```bash
git status --short --untracked-files=all
git add -- \
	wp-content/themes/beslock-custom/templates/blocks/discover.php \
	wp-content/themes/beslock-custom/templates/blocks/hero.php \
	wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php \
	wp-content/themes/beslock-custom/template-parts/cards/product-card.php
git diff --cached -- \
	wp-content/themes/beslock-custom/templates/blocks/discover.php \
	wp-content/themes/beslock-custom/templates/blocks/hero.php \
	wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php \
	wp-content/themes/beslock-custom/template-parts/cards/product-card.php
git status --short
```

### Exact future rollback sequence

```bash
git restore --staged wp-content/themes/beslock-custom/templates/blocks/discover.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/hero.php
git restore --staged wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php
git restore --staged wp-content/themes/beslock-custom/template-parts/cards/product-card.php
git status --short
```

### Rollback triggers

- any excluded surface appears in staged diff
- any runtime validation blocker is hit
- any ownership ambiguity reappears during manual review

### Highest-risk runtime commit mistake for this batch

- accidentally expanding the batch to include `archive_hero.php`, `header-widget.php`, or the preserved wrapper `templates/blocks/product-card.php`, which would reintroduce bridge/wrapper ambiguity into the first runtime tracking commit

## Pre-Execution Runtime Review

This section is the last documentation-only gate before any real runtime batch
execution.

### Scope under pre-execution review

- `wp-content/themes/beslock-custom/templates/blocks/discover.php`
- `wp-content/themes/beslock-custom/templates/blocks/hero.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`

### Explicitly out of scope

- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- logs, exports, generated artifacts, backups, sqlite artifacts, cache-like files

### Pre-execution conclusion

- the four-file batch remains the smallest runtime grouping that is both meaningful and ownership-coherent
- no new hidden dependency was found that forces `archive_hero.php` or `header-widget.php` back into scope
- the current worktree still contains contamination sources, but they are separable from the target batch if staging is path-explicit

## Expected Staging State

This section models the future git state conceptually without executing any
staging command.

### Expected `git status --short --untracked-files=all` before staging

- tracked-modified but excluded:
	`wp-content/themes/beslock-custom/assets/css/base/variables.css`
	`wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
	`wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
	`wp-content/themes/beslock-custom/debug/enqueued-styles.log`
	`wp-content/themes/beslock-custom/header.php`
	`wp-content/themes/beslock-custom/inc/debug/debug.php`
- untracked and intentionally included later:
	`wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
	`wp-content/themes/beslock-custom/templates/blocks/discover.php`
	`wp-content/themes/beslock-custom/templates/blocks/hero.php`
	`wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- untracked but explicitly excluded:
	`wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
	`wp-content/themes/beslock-custom/templates/blocks/product-card.php`
	`WORKTREE_NORMALIZATION_SUMMARY.md`

### Expected staged state after future path-explicit `git add`

- staged:
	`wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
	`wp-content/themes/beslock-custom/templates/blocks/discover.php`
	`wp-content/themes/beslock-custom/templates/blocks/hero.php`
	`wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- unstaged and still excluded:
	all tracked-modified CSS/JS/debug files listed above
- untracked and still excluded:
	`WORKTREE_NORMALIZATION_SUMMARY.md`
	`template-parts/content/archive_hero.php`
	`template-parts/header/header-widget.php`
	`templates/blocks/product-card.php`

### Expected staged diff shape

- exactly four `new file mode` entries
- no staged hunks for already tracked files
- no staged logs, debug outputs, exports, backups, or wrapper/bridge surfaces
- no staged documentation file

## Runtime Batch Integrity Check

This section confirms that the batch remains internally coherent.

### Ownership integrity

- `templates/blocks/discover.php`, `templates/blocks/hero.php`, and `templates/blocks/products-portfolio.php` remain active fallback owners through `front-page.php`
- `template-parts/cards/product-card.php` remains the canonical card leaf owner through `woocommerce/content-product.php` -> `template-parts/product-card.php`
- no file inside the batch is a preserved wrapper
- no file inside the batch is a parent-theme bridge

### Responsibility integrity

- no duplicate runtime responsibility exists inside the four-file set itself
- homepage block responsibility and Woo card responsibility remain adjacent but not overlapping
- `products-portfolio.php` depends on Woo loop rendering, but does not pull `archive_hero.php` or `header-widget.php` into the ownership boundary

### Fallback integrity

- homepage fallback routing is stable because `front-page.php` already selects these block files when `template-parts/*` equivalents are absent
- no fallback collision exists between the three block files because each owns a separate homepage section
- no parent-theme fallback path participates in the four-file batch

### Conditions that completely block execution

- any future staged diff includes `archive_hero.php`, `header-widget.php`, or `templates/blocks/product-card.php`
- any future staged diff includes tracked-modified CSS/JS/debug files outside the four-file target
- any future review shows that one of the four files is no longer the active owner on its current runtime path
- homepage fallback validation or Woo card validation no longer matches the current accepted render behavior

### Signals that mean `safe to execute`

- `git status` still shows the same four target files as untracked and stageable
- excluded bridge, wrapper, log, export, backup, and debug surfaces remain outside the path-explicit add set
- staged diff contains only the four expected new files
- visual homepage validation and Woo card validation align with current accepted behavior

## Staging Contamination Risks

This section identifies the most likely sources of accidental scope expansion.

### Possible staging contamination

- tracked-modified files already present in the worktree:
	`variables.css`, `single-product.css`, `product-gallery-init.js`, `header.php`, `inc/debug/debug.php`, `enqueued-styles.log`
- nearby untracked but excluded runtime surfaces:
	`template-parts/content/archive_hero.php`, `template-parts/header/header-widget.php`, `templates/blocks/product-card.php`
- the documentation file itself:
	`WORKTREE_NORMALIZATION_SUMMARY.md`

### Likely accidental inclusions

- `templates/blocks/product-card.php` because its name overlaps with the canonical card path
- `template-parts/content/archive_hero.php` because it sits beside actively reviewed runtime templates and looks easy to batch
- `template-parts/header/header-widget.php` because it is an active partial but not part of the first ownership-safe commit
- `WORKTREE_NORMALIZATION_SUMMARY.md` if the docs slice and runtime slice are staged together by habit

### Diff review hotspots

- verify that `products-portfolio.php` stages without pulling any other Woo template surface
- verify that `template-parts/cards/product-card.php` is staged without the preserved wrapper `templates/blocks/product-card.php`
- verify that the staged set contains no tracked-modified debt files, especially `enqueued-styles.log`

### Commit-message ambiguity risks

- wording the future commit as a general runtime cleanup would be misleading because this batch is not cleanup, not archive normalization, and not header normalization
- wording the future commit as a product-card normalization would be misleading because three homepage fallback blocks are also included
- the future commit message should describe recovered runtime tracking scope, not behavior change

### Rollback complexity risks

- rollback complexity remains low if the batch stays limited to four untracked files because unstaging is path-explicit and does not require content restoration
- rollback complexity becomes medium immediately if docs, tracked-modified files, or excluded runtime surfaces leak into the staged set

## Commit Message Rubric

This section defines how the first runtime tracking commit should be named and
described once the batch is actually staged.

### Runtime commit naming convention

- use a scope that describes tracking of recovered runtime source, not behavior change
- keep the title specific to the four-file batch and avoid broader architectural claims
- prefer `theme` or `runtime` wording over `cleanup`, `refactor`, or `migration`

### Recommended first runtime commit message

Title:

```text
theme: track recovered runtime fallback blocks and product card partial
```

Recommended body structure:

```text
- track recovered runtime-owned homepage fallback blocks
- track the canonical product-card leaf partial used in the Woo loop
- keep bridge, wrapper, docs, logs, exports, backups, and unrelated tracked-modified files outside this commit
- no intended runtime behavior change; commit scope is tracking and history normalization only
```

### Ownership wording to prefer

- `track recovered runtime-owned surfaces`
- `track active fallback blocks`
- `track the canonical product-card leaf partial`
- `keep bridge and wrapper surfaces outside this commit`

### Scope wording to prefer

- `first runtime tracking batch`
- `four-file runtime tracking scope`
- `recovered runtime source`
- `tracking-only commit`

### Migration wording to prefer

- `history normalization`
- `tracking normalization`
- `ownership-preserving tracking step`

### Tracking wording to prefer

- `track`
- `preserve ownership clarity`
- `exclude bridge and wrapper surfaces`

## Runtime Commit Semantics

This section defines what the commit is and what it is not allowed to claim.

### What the commit means

- it records four already-active runtime files that belong in version control
- it preserves the current ownership map without widening scope
- it improves repository history clarity for active runtime surfaces

### What the commit does not mean

- not a cleanup commit
- not a refactor commit
- not a migration commit
- not a runtime behavior change
- not a WooCommerce template behavior adjustment
- not a header or archive normalization step

### Language to avoid in the future commit message

Avoid ambiguous ownership language:

- `consolidate product-card ownership`
- `normalize template ownership`
- `unify runtime surfaces`

Avoid cleanup wording:

- `cleanup old templates`
- `remove legacy runtime clutter`

Avoid refactor wording:

- `refactor homepage runtime`
- `refactor Woo product-card rendering`

Avoid migration claims:

- `migrate runtime templates`
- `complete runtime migration`

Avoid runtime behavior claims:

- `fix homepage rendering`
- `improve Woo product cards`
- `change storefront output`

### Highest-risk semantic mistake

- describing the commit as cleanup, refactor, or migration instead of a narrow tracking-only step, which would make the historical record imply behavior or ownership work that did not actually happen in the commit

## Staged Diff Review Checklist

This section defines the exact rubric that the staged diff must satisfy before
the first runtime commit can be considered acceptable.

### Exact staged diff checks

- exact file count: 4
- exact paths:
	`wp-content/themes/beslock-custom/templates/blocks/discover.php`
	`wp-content/themes/beslock-custom/templates/blocks/hero.php`
	`wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
	`wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
- exact diff shape: four `new file mode` entries only
- no staged hunks for already tracked files
- no staged documentation file
- no staged logs, exports, backups, sqlite artifacts, or generated outputs

### Ownership clarity checks

- the three block files still read as active homepage fallback owners only
- `template-parts/cards/product-card.php` still reads as the canonical leaf partial, not as wrapper or bridge
- no staged file creates or implies ownership transfer for `archive_hero.php`, `header-widget.php`, or `templates/blocks/product-card.php`

### Scope discipline checks

- no tracked-modified contamination from CSS, JS, debug, or header files
- no wrapper or bridge bleedthrough
- no mixed docs-plus-runtime staging scope
- no accidental inclusion of unrelated theme runtime debt

### Acceptable staged diff characteristics

- the diff is narrow, path-explicit, and limited to recovered runtime source
- the diff preserves already-established ownership boundaries
- the diff is readable as a pure tracking commit with no behavioral claims
- the diff does not require explanation of parent-theme behavior, header loader duplication, or legacy wrapper retention because those files remain outside scope

### Commit blockers

- staged file count differs from 4
- staged path set differs from the approved four-file list
- any tracked-modified file is staged
- `archive_hero.php`, `header-widget.php`, `templates/blocks/product-card.php`, or `WORKTREE_NORMALIZATION_SUMMARY.md` appears in staged diff
- the staged diff wording or scope would require a cleanup/refactor/migration message to explain it
- manual diff review reveals ownership ambiguity, wrapper bleedthrough, bridge bleedthrough, or mixed runtime scope

## Safe-to-Commit Signals

This section defines the final semantic and technical signals required before
the first runtime tracking commit should be created.

### Final safe-to-commit checklist

- the staged diff contains exactly the approved four files and nothing else
- the commit title uses tracking language rather than cleanup, refactor, or migration language
- the commit body states that the change is tracking-only and ownership-preserving
- excluded bridge, wrapper, docs, logs, exports, and backups remain out of scope
- the staged diff still matches the runtime batch integrity assumptions already documented
- homepage visual validation and Woo product-card validation remain aligned with current accepted output

### Safest commit wording

- describe the commit as tracking recovered runtime-owned files
- describe the scope as homepage fallback blocks plus the canonical Woo card leaf partial
- describe the purpose as preserving ownership clarity in version control

### Pre-commit readiness assessment

- readiness is high if and only if the staged diff remains four-file, path-exact, tracking-only, and semantically narrow
- readiness drops immediately if the commit message starts needing cleanup/refactor/migration language to justify the staged set

## archive_hero Bridge Slice

This section defines the dedicated tracking slice for
`template-parts/content/archive_hero.php` after the first runtime-owner batch
has already been committed separately.

### Current bridge audit

| Surface | Include graph | Delegation behavior | Parent-theme coupling | Woo archive behavior | Fallback behavior | Render ownership boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `template-parts/content/archive_hero.php` | loaded on the child archive-hero path; for non-Woo contexts includes parent `template-parts/content/archive_hero.php`; related hook-level buffering also exists on `kadence_entry_archive_hero` in `functions.php` and `inc/cleanup-kadence.php` | explicit active bridge, not a leaf owner | high | suppresses hero output for shop and product taxonomy archives by returning early | defers to the parent template for non-Woo archive contexts | controls suppression/delegation only; canonical markup ownership remains in Kadence parent |

### Bridge classification confirmation

- active bridge: yes
- legacy disposable: no
- canonical owner: no
- wrapper-only surface: no
- preserved for parent-theme compatibility: yes

### Bridge chain and dependency notes

- bridge chain:
	child `template-parts/content/archive_hero.php` -> parent `template-parts/content/archive_hero.php` for non-Woo contexts
- companion runtime dependency:
	`kadence_entry_archive_hero` buffering in `functions.php` and `inc/cleanup-kadence.php` reinforces Woo hero suppression but does not change the file's bridge classification
- routing assumption:
	the child override must remain on the Kadence archive-hero template path to intercept archive rendering before parent fallback
- Woo coupling:
	depends on `is_shop()`, `is_product_category()`, and `is_product_tag()` semantics remaining stable

### Tracking-scope recommendation

- safest staging scope: `template-parts/content/archive_hero.php` only
- required companion file: none for tracking scope itself
- required companion validation: yes, because the bridge depends on parent-template availability and Kadence archive routing assumptions
- screenshot verification required: yes
- parent-theme verification required: yes

## Bridge Preservation Semantics

This section defines how the bridge slice should be described historically.

### What this slice means

- it tracks an already-active bridge surface that suppresses Woo archive hero output
- it preserves the child-to-parent delegation path for non-Woo archive contexts
- it records a compatibility surface that remains behaviorally important even though it is not the canonical markup owner

### What this slice must not claim

- not archive cleanup
- not archive refactor
- not legacy removal
- not archive behavior normalization
- not a Woo behavior change

### Recommended commit semantics

Recommended title:

```text
theme: track preserved archive hero bridge override
```

Recommended body structure:

```text
- track the preserved child override that suppresses Kadence archive hero output on Woo archive contexts
- preserve parent-theme fallback behavior for non-Woo archives
- keep runtime owners, header surfaces, wrappers, docs, logs, exports, and tracked-modified debt outside this commit
- no intended runtime behavior change; commit scope is bridge preservation and tracking normalization only
```

### Language to avoid

- `cleanup archive hero`
- `refactor archive rendering`
- `remove legacy archive template`
- `simplify archives`
- `normalize archive behavior`
- `fix Woo archive hero`

## Parent Theme Coupling Notes

This section captures why the file cannot be treated as a normal runtime-owner
template.

### Coupling facts

- non-Woo archive behavior still delegates into the Kadence parent template file
- the child file owns the suppression/delegation decision, not the final archive hero markup
- the bridge remains sensitive to parent path stability: `get_template_directory() . '/template-parts/content/archive_hero.php'`
- the bridge also overlaps behaviorally with hook-based hero buffering already present in `functions.php` and `inc/cleanup-kadence.php`

### Risk assessment

- parent-theme dependency risk: HIGH
- tracking-in-isolation risk: MEDIUM
- cleanup-misclassification risk: HIGH
- wrapper-confusion risk: LOW

### Implication for future tracking

- the file can be tracked alone
- the file should not be bundled with any Kadence cleanup, archive refactor, or parent-theme normalization work
- the file should not be described as a canonical owner because the canonical markup remains upstream in Kadence

## Bridge Tracking Validation Plan

This section defines the validation gates and rollback boundaries for the
future bridge-only tracking slice.

### Proposed staging scope

- include:
	`wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- explicitly exclude:
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
	`wp-content/themes/beslock-custom/templates/blocks/product-card.php`
	`WORKTREE_NORMALIZATION_SUMMARY.md`
	tracked-modified CSS/JS/debug debt
	logs, exports, backups, sqlite artifacts, generated outputs

### Validation gates

- confirm the staged diff contains exactly one file: `template-parts/content/archive_hero.php`
- confirm no tracked-modified debt is staged alongside the bridge
- confirm Woo shop and product taxonomy archives render without the Kadence hero
- confirm a non-Woo archive context still falls back to the Kadence parent template behavior
- confirm the staged diff does not imply archive cleanup or runtime-owner semantics

### Bridge-specific validation order

1. verify staged path scope is bridge-only
2. verify Woo shop archive hero remains suppressed
3. verify Woo product category or tag archive hero remains suppressed
4. verify a non-Woo archive still renders through the parent Kadence archive hero path
5. review commit wording for bridge-preservation semantics

### Rollback boundaries

- rollback scope should be only `template-parts/content/archive_hero.php`
- if any parent-theme cleanup or tracked-modified debt enters the staged set, the whole bridge slice is blocked
- if validation suggests the file is being used to justify archive behavior cleanup, stop and split semantics before tracking

### Commit blockers

- staged diff contains more than the single bridge file
- staged diff includes `header-widget.php`, `templates/blocks/product-card.php`, docs, logs, exports, backups, or tracked-modified debt
- review language describes cleanup, refactor, normalization, or legacy removal
- parent-theme verification cannot confirm preserved non-Woo fallback behavior
- Woo archive verification cannot confirm continued hero suppression

## Pre-Execution Bridge Review

This section closes the last non-functional gate before any real staging of the
preserved bridge surface.

### Scope under review

- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`

### Explicitly out of scope

- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `WORKTREE_NORMALIZATION_SUMMARY.md`
- tracked-modified CSS/JS/debug debt
- logs, exports, backups, sqlite artifacts, generated outputs

### Conceptual post-stage model

- expected `git status` before staging:
	tracked-modified debt remains unstaged, `archive_hero.php` remains the only bridge target, and excluded untracked files remain visible but outside scope
- expected staged state after future bridge-only add:
	exactly one staged file: `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- expected bridge boundary after staging:
	the staged set records only the child suppression/delegation surface; it does not widen into header, wrapper, docs, or tracked-modified debt

### Pre-execution bridge conclusion

- `archive_hero.php` can be staged alone without ownership bleedthrough
- parent-theme coupling remains high, but it is explicit rather than ambiguous
- Woo suppression remains explicit in the bridge file and reinforced by hook buffering, not confused by wrapper or runtime-owner semantics

## Bridge Staging Integrity Check

This section confirms that the bridge slice remains coherent when modeled as a
single-file stage.

### Real chain review

- Woo archive suppression:
	`archive_hero.php` returns early on `is_shop()`, `is_product_category()`, and `is_product_tag()`
- parent Kadence fallback:
	non-Woo archive contexts include `get_template_directory() . '/template-parts/content/archive_hero.php'`
- buffer interaction:
	`functions.php` and `inc/cleanup-kadence.php` also buffer `kadence_entry_archive_hero`, which means suppression logic is duplicated at the hook level but does not create a staging companion requirement
- include/delegation flow:
	child template override decides suppression/delegation; parent template remains the final markup owner outside Woo archives

### Hidden dependency findings

- hidden bridge dependency: none that forces a second file into the tracking slice
- accidental companion requirement: none for staging scope
- duplicated suppression logic: yes, at the `kadence_entry_archive_hero` hook layer in `functions.php` and `inc/cleanup-kadence.php`
- parent-theme fallback risk: yes, because the bridge assumes the Kadence parent template path remains stable

### Expected clean staged state

- staged file count: 1
- staged path:
	`wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- staged diff shape:
	one `new file mode` entry only
- unstaged and excluded:
	`header-widget.php`, `templates/blocks/product-card.php`, `WORKTREE_NORMALIZATION_SUMMARY.md`, tracked-modified debt, logs, exports, backups, generated outputs

### Bridge-only integrity conditions

- no ownership bleedthrough into runtime owners
- no wrapper contamination
- no cleanup semantics contamination
- no parent-theme ambiguity beyond the already-documented explicit fallback dependency
- no requirement to batch hook-buffer files into the same tracking commit

## Bridge-Specific Commit Blockers

This section defines what would completely block the future bridge-only stage.

### Structural blockers

- any future staged diff contains more than `archive_hero.php`
- any future staged diff includes `header-widget.php`, `templates/blocks/product-card.php`, or `WORKTREE_NORMALIZATION_SUMMARY.md`
- any tracked-modified CSS/JS/debug file appears staged
- any log, export, backup, sqlite artifact, or generated output appears staged

### Semantic blockers

- the staged diff or commit wording implies cleanup, refactor, normalization, or legacy removal
- the file is described as a canonical owner instead of a preserved bridge
- the staged set is used to justify broader archive behavior changes

### Validation blockers

- Woo shop archive cannot be confirmed as hero-suppressed
- Woo product category/tag archive cannot be confirmed as hero-suppressed
- non-Woo archive fallback to the Kadence parent template cannot be confirmed
- review reveals the parent-template path assumption is no longer valid

## Bridge Safe-to-Stage Signals

This section defines the exact signals that mean the bridge slice is ready for
real staging.

### Bridge staged diff review rubric

- exact file count: 1
- exact path:
	`wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- exact diff shape:
	one `new file mode` entry only
- no staged docs
- no staged wrapper or header surfaces
- no staged tracked-modified debt
- no staged generated artifacts

### Safe-to-stage signals

- `git status` still shows `archive_hero.php` as the only intended bridge target
- excluded untracked surfaces remain outside the path-explicit stage plan
- tracked-modified debt remains unstaged
- the bridge is still accurately described as preserved suppression/delegation, not cleanup or runtime ownership
- parent-theme fallback behavior remains conceptually intact and verifiable
- Woo archive suppression remains conceptually intact and verifiable

### Final bridge readiness assessment criteria

- readiness is high only if the staged set remains single-file, bridge-only, and semantically preservation-focused
- readiness drops to blocked immediately if staging scope widens or if the commit language starts needing archive cleanup/refactor framing

## Bridge Commit Message Rubric

This section defines how the future bridge-preservation commit should be named
and described.

### Bridge commit wording convention

- use wording that describes preserved bridge tracking, not archive behavior change
- describe Kadence as the parent markup owner outside Woo archive suppression contexts
- describe Woo suppression as already-active behavior being tracked, not newly introduced behavior
- keep the wording narrow enough that the commit still reads as single-file bridge preservation

### Recommended bridge commit message

Title:

```text
theme: track preserved archive hero bridge override
```

Recommended body structure:

```text
- track the preserved child override that suppresses Kadence archive hero output on Woo archive contexts
- preserve parent-theme fallback behavior for non-Woo archives
- keep wrappers, header surfaces, docs, logs, exports, backups, generated artifacts, and tracked-modified debt outside this commit
- no intended runtime behavior change; commit scope is bridge preservation and tracking normalization only
```

### Bridge wording to prefer

- `track preserved archive hero bridge override`
- `preserve child-to-parent archive hero delegation`
- `record the Woo archive suppression bridge`

### Parent-theme wording to prefer

- `preserve parent-theme fallback behavior`
- `Kadence parent remains the markup owner for non-Woo archive contexts`
- `child override controls suppression/delegation only`

### Woo suppression wording to prefer

- `suppress Kadence archive hero output on Woo archive contexts`
- `preserve existing Woo archive hero suppression`
- `record the active suppression bridge`

### Preservation wording to prefer

- `preserved bridge`
- `bridge preservation`
- `tracking normalization`
- `compatibility-preserving tracking step`

## Bridge Commit Semantics

This section defines what the bridge commit means and what it must not imply.

### What the commit means

- it records one already-active bridge surface in version control
- it preserves the current child-to-parent delegation contract for archive hero behavior
- it improves history clarity for a runtime-relevant compatibility surface

### What the commit does not mean

- not archive cleanup
- not archive refactor
- not archive behavior simplification
- not archive normalization
- not legacy removal
- not a Woo rendering fix
- not a parent-theme ownership transfer

### Language to avoid

- `cleanup archive hero`
- `refactor archive rendering`
- `remove legacy archive template`
- `simplify archive behavior`
- `normalize archives`
- `fix archive rendering`
- `migrate archive hero`

### Highest-risk semantic mistake

- describing the commit as archive cleanup, refactor, normalization, or a rendering fix, which would incorrectly imply that the commit changed archive behavior instead of simply tracking an already-active preserved bridge

## Bridge Diff Review Checklist

This section defines the exact staged diff rubric for the future bridge-only
commit.

### Exact staged diff checks

- exact file count: 1
- exact path:
	`wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`
- exact diff shape:
	one `new file mode` entry only
- no staged docs
- no staged wrapper contamination
- no staged header-surface contamination
- no staged tracked-modified debt
- no staged logs, exports, backups, sqlite artifacts, or generated outputs

### Ownership clarity checks

- the diff still reads as a preserved bridge, not as a canonical owner
- the diff still reads as a suppression/delegation surface, not as final markup ownership
- the diff does not imply that Kadence parent fallback has been removed or superseded

### Semantics checks

- the diff can be described without using cleanup, refactor, normalization, migration, or rendering-fix language
- the diff does not require claiming that Woo archive behavior changed in this commit
- the diff does not blur bridge semantics with runtime-owner semantics

### Acceptable staged diff characteristics

- single-file, bridge-only, path-exact scope
- no companion files required to explain the staging intent
- readable as preserved compatibility behavior with explicit parent-theme coupling
- narrow enough that bridge-preservation wording fully explains the change

### Bridge-specific commit blockers

- staged file count differs from 1
- staged path differs from `template-parts/content/archive_hero.php`
- any tracked-modified debt is staged
- `header-widget.php`, `templates/blocks/product-card.php`, `WORKTREE_NORMALIZATION_SUMMARY.md`, or any generated artifact appears in staged diff
- the staged diff would need cleanup/refactor/normalization/migration wording to explain it
- the staged diff introduces ownership ambiguity around Kadence parent markup ownership

## Bridge Safe-to-Commit Signals

This section defines the final technical and semantic signals that must be true
before the future bridge commit is created.

### Safe-to-commit signals

- the staged diff contains exactly one file and it is `template-parts/content/archive_hero.php`
- the commit title uses preserved-bridge tracking language
- the commit body explicitly preserves parent fallback and Woo suppression semantics
- excluded wrapper, header, docs, logs, exports, backups, generated artifacts, and tracked-modified debt remain outside the commit
- parent-theme ownership remains clearly described as upstream for non-Woo archive markup
- Woo archive suppression remains clearly described as preserved active behavior, not a new fix

### Safest bridge wording

- describe the file as a `preserved archive hero bridge override`
- describe Kadence as the `parent markup owner` outside Woo archive contexts
- describe the child file as `suppression/delegation only`

### Final bridge pre-commit readiness assessment

- readiness is high only if the future staged diff remains single-file, bridge-only, parent-aware, and preservation-focused
- readiness becomes blocked immediately if the wording starts implying cleanup, refactor, ownership transfer, or archive behavior change

## header-widget Ownership Slice

This section defines the dedicated tracking slice for
`template-parts/header/header-widget.php`, which remains pending because the
template is stable while the loader ownership around it is duplicated.

### Current ownership audit

| Surface | Include graph | Loader chain | Helper contract | Header coupling | Ownership role | Final classification |
| --- | --- | --- | --- | --- | --- | --- |
| `template-parts/header/header-widget.php` | loaded through `beslock_get_header_widget_html()` -> `beslock_render_header_widget()` or shortcode path | identical loader helpers exist in `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` | `beslock_get_header_widget_html()`, `beslock_render_header_widget()`, `beslock_header_widget_shortcode()` | stable dependency on logo asset, home URL, Woo cart URL/count behavior | canonical template partial, but surrounded by duplicated loader responsibility | stable partial with duplicated-loader ambiguity around it |

### Classification confirmation

- canonical owner: yes, for the partial markup itself
- stable partial: yes
- loader endpoint: yes, as the template target of the helper chain
- compatibility layer: no, not in the template file itself
- delegator: no, the template does not delegate further
- duplicated-responsibility surface: yes, but the duplication lives in the loader helpers, not in the template markup

### Tracking-scope recommendation

- safest staging scope: `template-parts/header/header-widget.php` only
- companion file required for tracking scope: none
- extra validation required: yes
- screenshot verification required: yes
- header rendering verification required: yes

## Duplicated Loader Analysis

This section captures where ownership becomes ambiguous.

### Duplicated loader paths

- `functions.php`
- `inc/header-widget.php`
- `inc/features/header.php`

Each file defines the same three helper surfaces behind `function_exists()`:

- `beslock_get_header_widget_html()`
- `beslock_header_widget_shortcode()`
- `beslock_render_header_widget()`

### Overlapping ownership findings

- the template partial is singular and stable
- the loader contract is triplicated
- the shortcode registration path is triplicated
- the runtime ambiguity is about who owns the loader contract, not who owns the header-widget markup

### Hidden dependencies and assumptions

- template dependency on `assets/images/logo-green.png`
- template dependency on `home_url()`
- conditional Woo dependency on `wc_get_cart_url()` and `WC()->cart->get_cart_contents_count()`
- implicit assumption that at least one loader file is included before shortcode or render helper use
- no confirmed dependency on `header.php` itself for rendering the widget template; `header.php` currently routes through `template-parts/header/site-header.php` instead

### Header responsibility boundary

- `header-widget.php` owns widget markup only
- `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` overlap on loader/helper registration
- `header.php` owns the main header bridge to `template-parts/header/site-header.php`, not the widget partial contract

## Header Ownership Boundaries

This section turns the audit into an explicit ownership model.

### What `header-widget.php` is

- canonical template partial for header widget markup
- stable render target for helper/shortcode paths
- runtime-active partial with logo/cart coupling

### What `header-widget.php` is not

- not the canonical owner of the loader contract
- not a bridge to parent-theme behavior
- not a preserved wrapper
- not a cleanup target by itself

### Implication for future tracking

- the template can be tracked alone
- the template should be described as a stable partial with duplicated-loader ambiguity around it
- loader cleanup or consolidation should remain a later, separate slice

## Header Tracking Validation Plan

This section defines the validation gates, staging proposal, rollback boundaries,
and commit semantics for the future tracking slice.

### Proposed staging scope

- include:
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- explicitly exclude:
	`wp-content/themes/beslock-custom/functions.php`
	`wp-content/themes/beslock-custom/inc/header-widget.php`
	`wp-content/themes/beslock-custom/inc/features/header.php`
	`wp-content/themes/beslock-custom/header.php`
	`wp-content/themes/beslock-custom/templates/blocks/product-card.php`
	`WORKTREE_NORMALIZATION_SUMMARY.md`
	tracked-modified CSS/JS/debug debt
	logs, exports, backups, sqlite artifacts, generated outputs

### Validation gates

- confirm the staged diff contains exactly one file: `template-parts/header/header-widget.php`
- confirm no loader helper file is staged with it
- confirm no tracked-modified debt is staged
- confirm the widget still renders correctly wherever the helper/shortcode contract is used
- confirm Woo cart URL/count behavior remains visually intact when Woo is active
- confirm the staged diff does not imply header cleanup or loader consolidation

### Header-specific validation order

1. verify staged path scope is template-only
2. verify the header widget renders with logo and cart entry intact
3. verify Woo cart count/cart URL behavior where the widget is rendered
4. verify commit wording describes stable partial tracking, not loader cleanup
5. verify no loader contract file leaked into the staged set

### Rollback boundaries

- rollback scope should be only `template-parts/header/header-widget.php`
- if any loader helper file enters the staged set, the slice is blocked rather than widened
- if review starts needing cleanup/refactor language to explain the staged diff, stop and split semantics before tracking

### Recommended commit semantics

Recommended title:

```text
theme: track stable header widget partial
```

Recommended body structure:

```text
- track the stable header widget partial used by the duplicated helper/shortcode contract
- preserve existing header rendering and Woo cart behavior
- keep loader helpers, header bridges, wrappers, docs, logs, exports, backups, generated artifacts, and tracked-modified debt outside this commit
- no intended runtime behavior change; commit scope is stable partial tracking only
```

### Language to avoid

- `cleanup header`
- `simplify header`
- `refactor header rendering`
- `remove duplicate logic`
- `normalize header behavior`

### Risk assessment

- duplicated-loader risk: HIGH
- single-file tracking risk: MEDIUM
- cleanup-misclassification risk: HIGH
- template-ownership ambiguity risk: LOW

## Pre-Execution Header Review

This section closes the last non-functional gate before any real staging of the
stable header widget partial.

### Scope under review

- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`

### Explicitly out of scope

- `wp-content/themes/beslock-custom/functions.php`
- `wp-content/themes/beslock-custom/inc/header-widget.php`
- `wp-content/themes/beslock-custom/inc/features/header.php`
- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- `WORKTREE_NORMALIZATION_SUMMARY.md`
- tracked-modified CSS/JS/debug debt
- logs, exports, backups, sqlite artifacts, generated outputs

### Conceptual post-stage model

- expected `git status` before staging:
	tracked-modified debt remains unstaged, `header-widget.php` remains the only partial target, and excluded untracked files remain visible but outside scope
- expected staged state after future partial-only add:
	exactly one staged file: `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- expected ownership boundary after staging:
	the staged set records only the stable markup partial; it does not widen into helper registration, header bridges, wrappers, docs, or tracked-modified debt

### Pre-execution conclusion

- `header-widget.php` can be staged alone without loader bleedthrough
- duplicated-loader ownership risk remains real, but it stays outside the staged file boundary if the add is path-explicit
- `header.php` does not currently create a competing ownership path for this widget partial because its active bridge points to `template-parts/header/site-header.php`

## Header Staging Integrity Check

This section confirms that the header slice remains coherent when modeled as a
single-file stage.

### Real chain review

- helper contracts:
	`beslock_get_header_widget_html()`, `beslock_header_widget_shortcode()`, and `beslock_render_header_widget()` all point to the same template partial
- shortcode/render paths:
	content shortcode and PHP render helper both terminate in `template-parts/header/header-widget.php`
- Woo cart rendering:
	the template conditionally uses `wc_get_cart_url()` and `WC()->cart->get_cart_contents_count()` but does not own Woo bootstrapping
- loader/delegation flow:
	duplicated loaders in `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` all include the same template
- template ownership boundary:
	the template owns widget markup only; helper registration and loader ownership remain outside the file

### Hidden dependency findings

- hidden helper dependency: none that forces a companion file into the tracking slice
- accidental companion requirement: none for staging scope
- duplicated loader paths: yes, across `functions.php`, `inc/header-widget.php`, and `inc/features/header.php`
- implicit rendering assumptions:
	at least one helper-definition file must load before shortcode or render-helper use, and Woo cart APIs may or may not be available at render time

### Expected clean staged state

- staged file count: 1
- staged path:
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- staged diff shape:
	one `new file mode` entry only
- unstaged and excluded:
	loader helper files, `header.php`, `templates/blocks/product-card.php`, `WORKTREE_NORMALIZATION_SUMMARY.md`, tracked-modified debt, logs, exports, backups, generated outputs

### Partial-only integrity conditions

- no loader bleedthrough into the staged set
- no helper contamination
- no wrapper contamination
- no cleanup semantics contamination
- no ownership ambiguity inside the staged file itself

## Header-Specific Commit Blockers

This section defines what would completely block the future partial-only stage.

### Structural blockers

- any future staged diff contains more than `header-widget.php`
- any future staged diff includes `functions.php`, `inc/header-widget.php`, `inc/features/header.php`, `header.php`, `templates/blocks/product-card.php`, or `WORKTREE_NORMALIZATION_SUMMARY.md`
- any tracked-modified CSS/JS/debug file appears staged
- any log, export, backup, sqlite artifact, or generated output appears staged

### Semantic blockers

- the staged diff or commit wording implies header cleanup, simplification, refactor, duplicate removal, or header normalization
- the file is described as owning the loader contract rather than the markup partial
- the staged set is used to justify loader consolidation or header behavior changes

### Validation blockers

- header widget cannot be confirmed to render with logo and cart entry intact
- Woo cart URL/count behavior cannot be confirmed where the widget renders
- review reveals a hidden loader dependency that actually requires companion staging

## Header Safe-to-Stage Signals

This section defines the exact signals that mean the header slice is ready for
real staging.

### Header staged diff review rubric

- exact file count: 1
- exact path:
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- exact diff shape:
	one `new file mode` entry only
- no staged helper files
- no staged `header.php`
- no staged docs
- no staged wrapper contamination
- no staged tracked-modified debt
- no staged generated artifacts

### Safe-to-stage signals

- `git status` still shows `header-widget.php` as the only intended partial target
- excluded helper files remain outside the path-explicit stage plan
- tracked-modified debt remains unstaged
- the partial is still accurately described as stable markup ownership with duplicated-loader ambiguity around it
- header rendering remains conceptually intact and verifiable
- Woo cart rendering remains conceptually intact and verifiable

### Final header readiness assessment criteria

- readiness is high only if the staged set remains single-file, partial-only, and semantically focused on stable markup tracking
- readiness becomes blocked immediately if staging scope widens into loader helpers or if the wording starts implying cleanup, duplicate removal, or header behavior refactor

## Header Commit Message Rubric

This section defines how the future stable-partial tracking commit for
`header-widget.php` should be named and described.

### Stable-partial commit wording convention

- use wording that describes tracking of a stable markup partial, not helper cleanup
- describe duplicated loaders as surrounding ownership risk, not as part of the staged change
- describe Woo cart behavior as preserved runtime behavior, not as a newly introduced capability
- keep the wording narrow enough that the commit still reads as a single-file partial-tracking step

### Recommended header commit message

Title:

```text
theme: track stable header widget partial
```

Recommended body structure:

```text
- track the stable header widget partial used by the duplicated helper/shortcode contract
- preserve existing header rendering and Woo cart behavior
- keep loader helpers, header bridges, wrappers, docs, logs, exports, backups, generated artifacts, and tracked-modified debt outside this commit
- no intended runtime behavior change; commit scope is stable partial tracking only
```

### Partial wording to prefer

- `track stable header widget partial`
- `track canonical widget markup partial`
- `record the stable widget render target`

### Helper-contract wording to prefer

- `used by the duplicated helper/shortcode contract`
- `surrounded by duplicated loader ownership`
- `helper registration remains out of scope`

### Woo cart wording to prefer

- `preserve existing Woo cart behavior`
- `preserve cart URL/count rendering`
- `record the widget partial without changing Woo cart behavior`

### Preservation wording to prefer

- `stable partial tracking`
- `tracking normalization`
- `ownership-preserving tracking step`
- `preserve existing header rendering`

## Header Commit Semantics

This section defines what the future header commit means and what it must not
imply.

### What the commit means

- it records one already-active stable partial in version control
- it preserves the current widget markup ownership boundary
- it improves history clarity for a runtime-relevant header partial

### What the commit does not mean

- not header cleanup
- not header simplification
- not header refactor
- not duplicate-loader removal
- not header normalization
- not a Woo cart rendering fix
- not helper-contract consolidation

### Language to avoid

- `cleanup header`
- `simplify header`
- `refactor header rendering`
- `remove duplicate logic`
- `normalize header behavior`
- `fix header rendering`
- `migrate header widget`

### Highest-risk semantic mistake

- describing the commit as helper cleanup, header refactor, duplicate removal, or a rendering fix, which would incorrectly imply that the commit changed the loader contract or header behavior instead of simply tracking the stable markup partial

## Header Diff Review Checklist

This section defines the exact staged diff rubric for the future stable-partial
commit.

### Exact staged diff checks

- exact file count: 1
- exact path:
	`wp-content/themes/beslock-custom/template-parts/header/header-widget.php`
- exact diff shape:
	one `new file mode` entry only
- no staged helper files
- no staged `header.php`
- no staged docs
- no staged wrapper contamination
- no staged tracked-modified debt
- no staged logs, exports, backups, sqlite artifacts, or generated outputs

### Ownership clarity checks

- the diff still reads as stable markup ownership only
- the diff does not imply ownership of the helper contract
- the diff does not imply that duplicated loaders were removed, consolidated, or normalized
- the diff does not imply that `header.php` or site-header ownership changed

### Semantics checks

- the diff can be described without using cleanup, simplify, refactor, duplicate-removal, normalization, migration, or rendering-fix language
- the diff does not require claiming that Woo cart behavior changed in this commit
- the diff does not blur stable-partial semantics with loader-consolidation semantics

### Acceptable staged diff characteristics

- single-file, partial-only, path-exact scope
- no companion files required to explain the staging intent
- readable as stable widget markup tracking with duplicated-loader ambiguity remaining outside scope
- narrow enough that stable-partial wording fully explains the change

### Header-specific commit blockers

- staged file count differs from 1
- staged path differs from `template-parts/header/header-widget.php`
- any tracked-modified debt is staged
- `functions.php`, `inc/header-widget.php`, `inc/features/header.php`, `header.php`, `templates/blocks/product-card.php`, `WORKTREE_NORMALIZATION_SUMMARY.md`, or any generated artifact appears in staged diff
- the staged diff would need cleanup/refactor/duplicate-removal/normalization language to explain it
- the staged diff introduces ownership ambiguity around loader contract ownership or header rendering boundaries

## Header Safe-to-Commit Signals

This section defines the final technical and semantic signals that must be true
before the future header commit is created.

### Safe-to-commit signals

- the staged diff contains exactly one file and it is `template-parts/header/header-widget.php`
- the commit title uses stable-partial tracking language
- the commit body explicitly preserves existing header rendering and Woo cart behavior
- excluded helper files, header bridges, wrappers, docs, logs, exports, backups, generated artifacts, and tracked-modified debt remain outside the commit
- stable markup ownership remains clearly separated from duplicated helper ownership
- Woo cart URL/count rendering remains clearly described as preserved active behavior, not a new fix

### Safest stable-partial wording

- describe the file as a `stable header widget partial`
- describe the helper layer as a `duplicated helper/shortcode contract` that remains out of scope
- describe the commit as `stable partial tracking only`

### Final header pre-commit readiness assessment

- readiness is high only if the future staged diff remains single-file, partial-only, helper-aware, and semantically focused on stable markup tracking
- readiness becomes blocked immediately if the wording starts implying cleanup, duplicate removal, helper consolidation, or header behavior change

## Header Helper-Layer Consolidation Planning

This section is analysis-only. It does not consolidate the helper layer yet; it
defines the safest future path for doing so.

### Duplication assessment

Duplicated helper contracts exist in three places:

- `wp-content/themes/beslock-custom/functions.php`
- `wp-content/themes/beslock-custom/inc/header-widget.php`
- `wp-content/themes/beslock-custom/inc/features/header.php`

Each location defines the same contract behind `function_exists()` guards:

- `beslock_get_header_widget_html()`
- `beslock_header_widget_shortcode()`
- `beslock_render_header_widget()`

### Include graph and execution graph

- `functions.php` is part of the active theme bootstrap and is always loaded by WordPress for the child theme
- the audited active bootstrap shows explicit includes from `functions.php` into `inc/core/enqueue.php` and Woo modules, but no confirmed active include edge into `inc/header-widget.php` or `inc/features/header.php`
- because the duplicate helper definitions are wrapped in `function_exists()`, whichever file defines the helpers first wins ownership silently
- `inc/features/header.php` also has an `error_log()` side effect, which makes accidental activation more observable but also more fragile

### Render flow and shortcode flow

- shortcode flow:
	`[beslock_header_widget]` -> `beslock_header_widget_shortcode()` -> `beslock_get_header_widget_html()` -> `template-parts/header/header-widget.php`
- PHP render flow:
	`beslock_render_header_widget()` -> `beslock_get_header_widget_html()` -> `template-parts/header/header-widget.php`
- template flow:
	helper contract -> stable partial `template-parts/header/header-widget.php`
- Woo flow:
	the template itself conditionally reads `wc_get_cart_url()` and `WC()->cart->get_cart_contents_count()` during render; Woo coupling is in the template, not in helper registration

### Canonical ownership recommendation

- canonical helper owner: `functions.php`
- canonical shortcode owner: `functions.php`
- canonical render owner: `functions.php`

Why:

- it is the only audited file guaranteed to be part of the active child-theme bootstrap
- it already contains the active contract used by the currently tracked stable partial
- choosing `functions.php` avoids transferring ownership into an include path that is not clearly guaranteed by the audited bootstrap

### Runtime instrumentation findings

A runtime instrumentation pass was executed through WordPress via WP-CLI to
confirm the real declaring file and execution flow.

Observed runtime results:

- `beslock_get_header_widget_html()` was declared from `functions.php`
- `beslock_header_widget_shortcode()` was declared from `functions.php`
- `beslock_render_header_widget()` was declared from `functions.php`
- `shortcode_exists( 'beslock_header_widget' )` returned `yes`
- helper, shortcode, and render invocation all executed successfully and returned/rendered the same output length

Observed runtime implication:

- in the audited runtime path, `functions.php` wins the helper contract
- no runtime evidence was produced in this pass that `inc/header-widget.php` or `inc/features/header.php` were actively loaded before `functions.php`
- the duplicate files remain architectural risk because their include path is still unresolved, not because they won in the observed runtime

### Duplicated implementations and shadowing behavior

- `functions.php` contains a full implementation of the contract
- `inc/header-widget.php` contains the same implementation
- `inc/features/header.php` contains the same implementation plus a debug side effect
- the `function_exists()` guards create silent first-definition-wins shadowing, which masks load-order problems instead of resolving them

### Fragility assessment

- bootstrap-order fragility: HIGH
- conditional loading fragility: HIGH
- plugin/theme coupling: LOW
- shortcode timing risk: MEDIUM
- Woo timing risk: LOW to MEDIUM

Notes:

- shortcode timing risk exists because duplicate files may register the shortcode at different moments if they become included later through non-audited paths
- Woo timing risk is lower because the helper layer only includes the template; the Woo-specific logic lives in the template and already degrades when Woo helpers are unavailable

### Safest future consolidation strategy

1. freeze ownership in `functions.php` as the canonical helper layer
2. confirm no active bootstrap path still requires `inc/header-widget.php` or `inc/features/header.php` for header widget availability
3. convert duplicate helper files into compatibility wrappers or no-op includes before any deletion
4. remove debug side effects like the `error_log()` in `inc/features/header.php` only in a later functional slice with focused validation
5. only after execution-graph confirmation, retire duplicate implementations one by one

### Safest fallback strategy

- preserve the public helper names unchanged
- preserve the shortcode name unchanged
- preserve the stable partial path unchanged
- if duplicate files must remain temporarily, they should defer to the canonical owner rather than redefining the helpers

### Rollback strategy

- rollback should restore helper ownership in `functions.php` first
- if a future consolidation breaks rendering, revert the consolidation slice without touching the tracked stable partial
- never combine helper consolidation with header markup changes, Woo changes, or shortcode renaming

### Compatibility preservation strategy

- keep `beslock_get_header_widget_html()`, `beslock_render_header_widget()`, and `beslock_header_widget_shortcode()` stable
- keep `template-parts/header/header-widget.php` as the render target
- keep helper consolidation separate from any header/site-header bridge work

### What must not be done

- direct deletion of duplicate helper files without confirming active include paths
- mass refactor of header rendering and helper ownership in one slice
- loader merge without an execution-graph audit
- runtime ownership transfer away from `functions.php` without evidence
- shortcode renaming

### Consolidation risk assessment

- overall consolidation risk: HIGH

Reason:

- the duplicate code itself is simple, but the hidden risk is bootstrap-order ambiguity and silent shadowing created by `function_exists()` guards

### Highest-risk cleanup mistake

- deleting or rewriting duplicate helper files based only on textual duplication, without first proving which file actually wins in the active bootstrap and whether any non-audited include path still depends on the others

### Safest first functional step

- instrument and confirm the real active include order for `functions.php`, `inc/header-widget.php`, and `inc/features/header.php` in runtime before changing any helper definition

## Header Helper Consolidation Result

This slice performed the minimal functional consolidation of the duplicated
header helper layer.

### Canonical Ownership Confirmation

- `functions.php` remains the only active owner of:
	- `beslock_get_header_widget_html()`
	- `beslock_header_widget_shortcode()`
	- `beslock_render_header_widget()`
- the duplicate active definitions were removed from:
	- `wp-content/themes/beslock-custom/inc/header-widget.php`
	- `wp-content/themes/beslock-custom/inc/features/header.php`
- the shortcode name remains unchanged: `beslock_header_widget`
- the render target remains unchanged: `template-parts/header/header-widget.php`

### Compat Shim Preservation Notes

- `inc/header-widget.php` now acts as a legacy compat shim only
- `inc/features/header.php` now acts as a legacy compat shim only
- both files remain present to preserve existing include paths
- both files no longer redefine the helper contract, so silent `function_exists()` shadowing from those files is removed
- both files retain lightweight audit logging only to confirm whether legacy include paths still execute after consolidation

### Consolidation Safety Result

- ownership preserved: yes
- bootstrap-safe by design: yes, because the canonical owner remains in `functions.php`
- public API preserved: yes
- shortcode preserved: yes
- Woo behavior touched: no
- template ownership changed: no
- rendering structure changed: no
- dependency graph changed functionally: no

## GLOB_BRACE Compatibility Fix

This slice remediated a preexisting runtime portability failure in
`templates/models-mobile.php`.

### Compatibility issue root cause

- the file used `glob( ... , GLOB_BRACE )` to scan product images across multiple extensions
- the active validation environment does not expose the `GLOB_BRACE` constant
- this creates a fatal error before the mobile models template can finish rendering
- the issue is environment-specific and is consistent with PHP builds where brace glob support is unavailable

### Environment Compatibility Notes

- the previous implementation assumed `GLOB_BRACE` existed unconditionally
- that assumption is not portable across all libc / PHP build combinations
- the failure is independent from header helper ownership and independent from Woo behavior

### Fallback strategy

- preserve the same image extension set: `webp`, `png`, `jpg`, `jpeg`
- use `GLOB_BRACE` only when the constant exists
- otherwise, run one `glob()` per extension and merge the results
- keep the rest of the grouping, underscore filtering, title generation, and rendering flow unchanged
- guard the local title helper so repeated loads of `templates/models-mobile.php` in the same runtime do not trigger a redeclare fatal during validation or reuse

### Runtime Validation Recovery

- syntax remains valid after the compatibility fix
- the fatal caused by `Undefined constant GLOB_BRACE` is removed from the `models-mobile.php` scan path
- broader runtime validation now completes through `get_header()` and repeated `get_template_part( 'templates/models-mobile' )` execution in WP-CLI
- helper-layer validation remained stable after the fix: shortcode registration still succeeds and helper / shortcode / render output stayed equivalent

## product-card Legacy Wrapper Slice

This section defines the dedicated slice for
`templates/blocks/product-card.php`, which remains outside tracking because it
behaves as a preserved legacy wrapper rather than as a runtime owner.

### Current wrapper audit

| Surface | Include graph | Wrapper chain | Compatibility behavior | WooCommerce coupling | Ownership role | Final classification |
| --- | --- | --- | --- | --- | --- | --- |
| `templates/blocks/product-card.php` | receives an array-based `$product` payload and, when normalization succeeds, delegates to `template-parts/product-card.php` | `templates/blocks/product-card.php` -> `template-parts/product-card.php` -> `template-parts/cards/product-card.php` | adapts array-shaped portfolio/block data into a `WC_Product` for the canonical render path | medium, because it calls `wc_get_product()` and depends on Woo attachments/IDs for normalization | compatibility shim and delegator, not final markup owner | preserved legacy wrapper and future archive candidate |

### Wrapper classification confirmation

- wrapper-only: yes, in its active role
- compatibility shim: yes
- preserved fallback: yes, for older portfolio-array flow
- delegator: yes
- legacy compatibility surface: yes
- archive candidate: yes
- active runtime dependency: not on the canonical Woo loop path, but still a compatibility dependency if older array-based callers survive

### Relationship to the canonical owner chain

- canonical Woo runtime owner chain:
	`woocommerce/content-product.php` -> `template-parts/product-card.php` -> `template-parts/cards/product-card.php`
- legacy wrapper chain:
	`templates/blocks/product-card.php` -> `template-parts/product-card.php` -> `template-parts/cards/product-card.php`
- ownership consequence:
	the wrapper shares the downstream render path but does not own the canonical entrypoint for Woo product rendering

## Wrapper Preservation Semantics

This section defines how the wrapper slice should be described historically.

### What this slice means

- it tracks or preserves a compatibility wrapper that still delegates into the canonical product-card render path
- it records a non-canonical surface whose value is historical/runtime compatibility rather than markup ownership
- it keeps legacy array-to-`WC_Product` adaptation explicit in repository history

### What this slice must not claim

- not Woo product-card cleanup
- not product rendering refactor
- not product-card normalization
- not compatibility removal
- not ownership transfer to the wrapper

### Recommended commit semantics

Recommended title:

```text
theme: track preserved legacy product-card wrapper
```

Recommended body structure:

```text
- track the preserved legacy wrapper that adapts array-based product data into the canonical product-card render path
- preserve compatibility with older portfolio-style callers while keeping the canonical Woo owner path unchanged
- keep runtime owners, docs, logs, exports, backups, generated artifacts, and tracked-modified debt outside this commit
- no intended runtime behavior change; commit scope is wrapper preservation and tracking normalization only
```

### Language to avoid

- `remove legacy`
- `cleanup wrapper`
- `simplify Woo cards`
- `refactor product rendering`
- `normalize product cards`
- `remove compatibility layer`

## Wrapper Ownership Boundaries

This section turns the audit into an explicit ownership model.

### What `templates/blocks/product-card.php` is

- preserved legacy wrapper
- compatibility shim from array-shaped product input to `WC_Product`
- delegator into the canonical product-card partial chain
- future archive candidate once compatibility need is explicitly retired

### What `templates/blocks/product-card.php` is not

- not the canonical Woo product-card owner
- not the final markup owner
- not a parent-theme bridge
- not a cleanup target by default

### Hidden dependencies and assumptions

- assumes some caller still provides array-based `$product` or query-var product payloads
- assumes `wc_get_product()` can normalize a `product_id` into a `WC_Product`
- assumes downstream `template-parts/product-card.php` and `template-parts/cards/product-card.php` remain present
- contains historical image-normalization code above the active delegating wrapper block, which increases legacy surface area but does not change the canonical owner chain

### Compatibility risk assessment

- compatibility risk: HIGH
- single-file tracking risk: MEDIUM
- cleanup-misclassification risk: HIGH
- runtime-owner ambiguity risk: MEDIUM

## Wrapper Tracking Validation Plan

This section defines the staging proposal, validation gates, rollback
boundaries, and commit semantics for the future wrapper slice.

### Proposed staging scope

- include:
	`wp-content/themes/beslock-custom/templates/blocks/product-card.php`
- explicitly exclude:
	`wp-content/themes/beslock-custom/woocommerce/content-product.php`
	`wp-content/themes/beslock-custom/template-parts/product-card.php`
	`wp-content/themes/beslock-custom/template-parts/cards/product-card.php`
	`WORKTREE_NORMALIZATION_SUMMARY.md`
	tracked-modified CSS/JS/debug debt
	logs, exports, backups, sqlite artifacts, generated outputs

### Validation gates

- confirm the staged diff contains exactly one file: `templates/blocks/product-card.php`
- confirm no canonical owner file is staged with it
- confirm no tracked-modified debt is staged
- confirm the wrapper still reads as compatibility preservation, not canonical ownership
- confirm Woo/product-card verification remains focused on compatibility callers rather than the standard Woo loop owner path
- confirm the staged diff does not imply wrapper cleanup or compatibility removal

### Wrapper-specific validation order

1. verify staged path scope is wrapper-only
2. verify the canonical owner chain remains outside the staged set
3. verify any compatibility caller expectations still map into `template-parts/product-card.php`
4. verify Woo/product-card behavior is described as preserved downstream behavior, not new rendering ownership
5. verify commit wording describes preserved legacy wrapper semantics

### Rollback boundaries

- rollback scope should be only `templates/blocks/product-card.php`
- if any canonical owner file enters the staged set, the slice is blocked rather than widened
- if review starts needing cleanup/refactor/removal language to explain the staged diff, stop and split semantics before tracking

### Track-now recommendation

- no immediate tracking recommendation yet
- safest current posture remains: keep untracked temporarily until an explicit preserved-legacy decision is made
- if tracked later, it must be described as preserved legacy wrapper only

## Legacy Wrapper Disposition Analysis

This section closes the current architectural disposition question for
`templates/blocks/product-card.php`.

### Caller review result

- no direct caller to `templates/blocks/product-card.php` was found in the audited PHP codebase
- no active include from the canonical Woo owner chain points to this wrapper
- no `set_query_var( 'product', ... )` caller was found outside the wrapper itself in the audited theme code
- no direct `get_template_part( 'templates/blocks/product-card' )` caller was found in the audited theme code

### Plausible remaining value

- runtime value: LOW
- compatibility value: MEDIUM
- migration value: LOW
- debugging value: MEDIUM
- rollback value: MEDIUM

Reasoning:

- the wrapper still documents how an older array-based product payload was adapted into the canonical `WC_Product` render path
- the file still preserves a fallback shim if an older portfolio-style caller exists outside the currently audited call graph
- however, the active runtime owner chain no longer depends on it

### What would be lost if the file disappeared today

- the explicit adapter from array-shaped product payloads to `WC_Product`
- a debugging reference for legacy `product_id` / `show_desc` payload expectations
- an immediate fallback surface for any un-audited or external legacy caller still invoking the wrapper path

### What would not be lost based on current evidence

- the canonical Woo product-card runtime owner chain
- homepage/storefront product rendering through `woocommerce/content-product.php`
- the active leaf card markup in `template-parts/cards/product-card.php`

### Final disposition category

- `SAFE_TO_ARCHIVE_LATER`

Why this category fits best:

- current evidence does not show active callers in the audited codebase
- the file still has enough compatibility/debugging value that immediate removal would be a stronger claim than the current evidence supports
- keeping it untracked temporarily remains safer than forcing a preservation commit without clear active value

### Final recommendation

- preserve semantically for now, but do not track immediately
- keep the file untracked temporarily until an explicit archive or retirement decision is made
- treat it as a future archive candidate with residual compatibility value, not as an active runtime dependency

### Safest future action

- leave `templates/blocks/product-card.php` untracked temporarily
- if a future archive slice is opened, verify once more that no external caller or content-level include depends on the wrapper path
- if future evidence of active callers appears, reclassify to preserved legacy wrapper and revisit tracking

## Final Ownership Classification

This section consolidates the current normalization state using the terminology
that remains accurate after the tracking commits already created in this worktree.

### `TRACKED_RUNTIME_OWNERS`

- `wp-content/themes/beslock-custom/templates/blocks/discover.php`
- `wp-content/themes/beslock-custom/templates/blocks/hero.php`
- `wp-content/themes/beslock-custom/templates/blocks/products-portfolio.php`
- `wp-content/themes/beslock-custom/template-parts/cards/product-card.php`

Definition:

- active runtime-owned entrypoints or leaf owners already committed as tracking-only runtime surfaces

### `TRACKED_BRIDGES`

- `wp-content/themes/beslock-custom/template-parts/content/archive_hero.php`

Definition:

- active bridge surfaces already committed with preservation semantics rather than owner semantics

### `TRACKED_STABLE_PARTIALS`

- `wp-content/themes/beslock-custom/template-parts/header/header-widget.php`

Definition:

- stable markup partials already committed without pulling surrounding helper ambiguity into the same change

### `PRESERVED_LEGACY_WRAPPERS`

- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`

Definition:

- legacy compatibility wrappers that delegate into canonical owner paths and must not be described as runtime owners

### `FUTURE_ARCHIVE_CANDIDATES`

- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`

Definition:

- preserved legacy surfaces that may be retired or archived only after compatibility need is explicitly disproven

### `TRACK_LATER_SURFACES`

- tracked-modified debt currently outside normalization commits:
	`wp-content/themes/beslock-custom/assets/css/base/variables.css`
	`wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
	`wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
	`wp-content/themes/beslock-custom/header.php`
	`wp-content/themes/beslock-custom/inc/debug/debug.php`

Definition:

- surfaces still deferred because they require separate cleanup, consolidation, or debt-specific review rather than tracking-only treatment

### `GENERATED_OR_LOCAL_ONLY`

- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/import_logs/*.log`
- `wp-content/themes/beslock-custom/repo_portfolio/*.sqlite`
- `wp-content/themes/beslock-custom/repo_portfolio/*.restored`
- `wp-content/themes/beslock-custom/repo_portfolio/products_backup_latest.json`
- `wp-content/uploads/`
- database exports under `database/.gitignore`

Definition:

- generated, environment-specific, or local-only outputs that should remain outside authored runtime tracking

## Current Tracking State

This section aligns the summary with the tracking decisions already executed.

### Tracking commits already created

- `c7bdf5cc` — `theme: track recovered runtime fallback blocks and product card partial`
- `d404265a` — `theme: track preserved archive hero bridge override`
- `43aafaf1` — `theme: track stable header widget partial`
- `2c7efbad` — `theme: consolidate header helper ownership and preserve compat shims`
- `e3ecc23a` — `theme: add portable models-mobile glob fallback`

### Current untracked authored source

- `wp-content/themes/beslock-custom/templates/blocks/product-card.php`

### Current tracked-modified debt outside normalization commits

- `wp-content/themes/beslock-custom/assets/css/base/variables.css`
- `wp-content/themes/beslock-custom/assets/css/pages/single-product.css`
- `wp-content/themes/beslock-custom/assets/js/product-gallery-init.js`
- `wp-content/themes/beslock-custom/debug/enqueued-styles.log`
- `wp-content/themes/beslock-custom/header.php`
- `wp-content/themes/beslock-custom/inc/debug/debug.php`

### Alignment check

- the current summary remains aligned with the five normalization commits already created
- the only remaining authored untracked runtime-related file is the preserved legacy wrapper `templates/blocks/product-card.php`
- documentation remains intentionally isolated into its own commit boundary so runtime and narrative history stay separate

## Deferred Cleanup Surfaces

This section isolates work that remains intentionally outside the tracking-only
normalization slices.

### Deferred because they are cleanup/consolidation work, not tracking work

- tracked-modified CSS/JS/header/debug debt:
	`variables.css`, `single-product.css`, `product-gallery-init.js`, `header.php`, `inc/debug/debug.php`
- generated debug output:
	`debug/enqueued-styles.log`

### Deferred because they are preserved compatibility surfaces

- `templates/blocks/product-card.php`

### Deferred because they should remain local-only or generated

- logs, exports, backups, sqlite artifacts, uploads, database exports

## Remaining Normalization Work

This section consolidates the remaining pending areas after the tracking commits
already created.

### What remains untracked

- `templates/blocks/product-card.php` as preserved legacy wrapper pending an explicit preserve-vs-archive decision
- `WORKTREE_NORMALIZATION_SUMMARY.md` as the documentation artifact for this normalization effort

### What remains preserved

- the legacy wrapper semantics around `templates/blocks/product-card.php`
- the explicit distinction between bridge surfaces, stable partials, runtime owners, and generated/local-only outputs

### What remains deferred

- tracked-modified debt in CSS/JS/header/debug files
- any cleanup or archive retirement work for the legacy wrapper

### What remains future-cleanup-only

- any decision to archive or retire `templates/blocks/product-card.php`
- any tooling/path-resolution implementation work beyond the current design/spec documentation

### Documentation commit semantics recommendation

Recommended title:

```text
docs: consolidate worktree normalization summary
```

Recommended body structure:

```text
- consolidate current ownership classifications and tracking state after the runtime, bridge, and stable-partial tracking commits
- record deferred cleanup surfaces and remaining normalization work without changing runtime behavior
- keep authored runtime tracking, wrapper/archive decisions, and cleanup work outside this documentation-only commit
```

### Language to avoid in the future documentation commit

- `final cleanup`
- `normalization complete`
- `archive finished`
- `migration completed`
- `ownership fully resolved`

## Result

The repository is more legible than it was at the start of this effort:

- active runtime owners, the preserved bridge, and the stable header partial are now tracked in separate ownership-safe commits
- the remaining authored untracked runtime-related surface is the preserved legacy wrapper `templates/blocks/product-card.php`
- the current worktree is not clean, but the remaining noise is now clearly separated into documentation, preserved wrapper, tracked-modified debt, and generated/local-only outputs
- the remaining normalization work is now primarily consolidation and cleanup planning, not blind runtime recovery