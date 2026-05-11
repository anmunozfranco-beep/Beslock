# Beslock Product Interactions — TODO

## Stage 2 — Frontend

### Core integration
- [ ] Update `inc/woocommerce/product-features.php`
- [ ] Filter reviews to only include:
  - [ ] explicit `interaction_type = review`
  - [ ] legacy reviews with rating and no interaction_type
- [ ] Exclude:
  - [ ] `question`
  - [ ] `reply`
- [ ] Add `beslock_get_product_questions_list()`

### Form template
- [ ] Create `template-parts/product/product-interactions-form.php`
- [ ] Add heading
- [ ] Add moderation notice
- [ ] Add selector:
  - [ ] review
  - [ ] question
- [ ] Add rating field for review mode only
- [ ] Add textarea
- [ ] Add name field
- [ ] Add email field
- [ ] Add success and error containers
- [ ] Add nonce
- [ ] Add hidden `product_id`

### Theme wiring
- [ ] Require `inc/woocommerce/product-interactions.php` in `functions.php`
- [ ] Render block in `woocommerce/single-product.php`
- [ ] Place it below `.product-tabs`
- [ ] Keep it outside `.product-tabs`

### Styling
- [ ] Add styles for `.product-interactions`
- [ ] Add styles for selector
- [ ] Add styles for success/error/notice
- [ ] Add responsive behavior
- [ ] Verify mobile usability

### JS enhancement
- [ ] Toggle rating field by interaction type
- [ ] Keep textarea label aligned with selected mode
- [ ] Keep JS optional and progressive

### Validation
- [ ] Review requires rating
- [ ] Question does not use rating
- [ ] Name or email required
- [ ] Invalid email rejected
- [ ] Product ID validated
- [ ] Review saved as pending
- [ ] Question saved as pending

---

## Stage 1 — Backup / Restore

### Documentation
- [x] Keep README aligned with implementation
- [x] Prepare dedicated brief for exporter/importer if implementation begins

### Schema
- [x] Preserve schema v1
- [x] Keep `interaction_type` aligned with frontend metadata
- [x] Ensure future exporter/importer use:
  - [x] `review`
  - [x] `question`
  - [x] `reply`
