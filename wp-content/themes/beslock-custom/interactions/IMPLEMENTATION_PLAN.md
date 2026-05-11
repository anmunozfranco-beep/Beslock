# Beslock Product Interactions — Implementation Plan

## Branch
`Beslock_Product_Reseñas`

## Objective
Implement a unified product interactions system for Beslock covering:

- `review`
- `question`
- `reply`

The work is split into two independent stages:

### Stage 1 — Backup / Restore
Artifacts under:
`wp-content/themes/beslock-custom/interactions/`

Includes:
- `interactions.json`
- `exporter_interactions.zip`
- `importer_interactions.zip`

### Stage 2 — Frontend Product Interactions
A permanent interactions block in `single-product` to let users:
- leave a review
- ask a question

---

## Current state
Already documented:
- project master README
- schema v1 for `interactions.json`

Already created:
- `inc/woocommerce/product-interactions.php`

Current relevant files:
- `woocommerce/single-product.php`
- `functions.php`
- `inc/woocommerce/product-features.php`
- `inc/woocommerce/product-interactions.php`

---

## Critical technical decisions

### 1. Use comment meta to distinguish interaction type
Do **not** rely on a custom `comment_type` for business semantics.

Use:
- `interaction_type = review`
- `interaction_type = question`
- `interaction_type = reply`

### 2. Daily operation does not use Stage 1 artifacts
Do not use:
- `interactions.json`
- exporter/importer

for normal frontend submission or rendering.

### 3. All new frontend interactions must be moderated
Every new review or question must be created as:
- pending / not auto-approved

### 4. Reviews and questions must not be mixed in public rendering
The current review helper must be updated so questions do not appear in the reviews tab.

### 5. Legacy review compatibility
Legacy approved reviews with rating and no `interaction_type` should still be treated as reviews.

---

## Recommended implementation order

### Step 1
Update `inc/woocommerce/product-features.php`

Goals:
- make `beslock_get_product_reviews_list()` exclude:
  - `question`
  - `reply`
- add `beslock_get_product_questions_list()`

### Step 2
Create:
`template-parts/product/product-interactions-form.php`

Goals:
- render the interactions block
- render selector `review` / `question`
- render rating only in review mode
- render notice / success / error messages

### Step 3
Update:
`functions.php`

Goals:
- load `inc/woocommerce/product-interactions.php`

### Step 4
Update:
`woocommerce/single-product.php`

Goals:
- render the new interactions block below `.product-tabs`
- keep it outside the tab container
- keep it always visible

### Step 5
Add styles

Goals:
- integrate visually with product page
- keep the block separate from the tabset
- support mobile and desktop

### Step 6
Optional JS enhancement

Goals:
- toggle rating visibility when switching between review/question
- improve UX only
- do not move business logic to JS

---

## Immediate pending tasks
1. Adjust product reviews helper
2. Add product questions helper
3. Add template partial for interactions form
4. Require interactions module from `functions.php`
5. Render interactions block in `single-product.php`
6. Add styles
7. Add optional JS
8. Validate moderation flow

---

## Validation checklist
- review submission works
- question submission works
- both remain pending
- reviews tab shows only reviews
- questions are not mixed into reviews
- block remains visible regardless of active tab
- no dependency on `interactions.json`
