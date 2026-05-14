# Semantic conflicts register

_Schema: `semantic-governance/1.0` · conflict register · generated 2026-05-13T17:11:48Z._

## Purpose

Detect duplicated entities, conflicting procedures, overlapping capabilities,
contradictory terminology, semantic collisions, ambiguous relationships and
maturity conflicts. **Conflicts are never auto-resolved.**

## Detection categories

| Category | Count |
|---|---:|
| `duplicate-entity-within-product` | 15 |
| `synonym-duplication` | 41 |
| `bilingual-duplication` | 15 |
| `non-conforming-id` | 61 |
| `missing-prefix` | 42 |
| `verb-out-of-registry` | 26 |
| `cross-product-collision` | 19 |
| `ambiguous-procedure-naming` | 0 |

## Detection categories — definitions

- **duplicate-entity-within-product** — two artifacts in the same product +
  domain that resolve to the same canonical ID. Severity: high.
- **synonym-duplication** — an artifact whose local ID is a known synonym of
  a canonical ID. Severity: medium.
- **bilingual-duplication** — both an English and a Spanish file for the same
  concept exist in one product. Severity: medium.
- **non-conforming-id** — filename or local ID violates the grammar.
  Severity: low.
- **missing-prefix** — filename lacks the expected domain prefix.
  Severity: low.
- **verb-out-of-registry** — leading procedure token is not a canonical
  action verb. Severity: low.
- **cross-product-collision** — same canonical ID appears in multiple
  products. Severity: info (candidate for shared-concept membership; verify
  intent first).
- **ambiguous-procedure-naming** — same target addressed with multiple verbs
  (e.g. `add-`, `register-`, `enroll-`). Severity: medium.

## Resolution policy

1. Detect → classify → surface in this register.
2. Editorial decides: merge, deprecate, rename, leave-as-is-with-rationale.
3. Update canonical-terminology / procedural-normalization registries.
4. Re-run the audit; the conflict count for each category MUST drop or stay
   constant — it MUST NOT silently grow.

## Companion files

- [`semantic-conflicts.json`](semantic-conflicts.json) — full machine-readable conflict catalogue.
