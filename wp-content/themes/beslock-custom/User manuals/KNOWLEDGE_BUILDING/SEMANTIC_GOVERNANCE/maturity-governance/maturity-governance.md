# Maturity governance

_Schema: `semantic-governance/1.0` · maturity governance · generated 2026-05-13T17:11:48Z._

## Purpose

Normalize the maturity classification across the whole repository. The
authoritative tier list lives in
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/maturity-tiers.json`;
this document governs **how** maturity is assigned and changed.

## Required field

`maturity` is required on every semantic artifact under
`ext-images/<slug>/knowledge-core/`. Artifacts without a `maturity` field are
treated as `unresolved` until backfilled.

## Promotion rules

| From | To | Required evidence |
|---|---|---|
| absent       | unresolved   | none — auto |
| ocr-derived  | inferred     | reviewer note + at least one cross-evidence link |
| inferred     | canonical    | OEM evidence pointer + reviewer approval |
| canonical    | verified     | second OEM source OR field-confirmation record |
| any          | deprecated   | replacement artifact ID |
| any          | low-confidence | reviewer note explaining the downgrade |
| any          | transitional | migration target + ETA |

## Demotion rules

A demotion (e.g. `verified → low-confidence`) is allowed only with an
explicit reviewer note. Silent demotion is forbidden.

## Consistency invariants

1. A `verified` artifact MUST have ≥1 OEM evidence span.
2. A `canonical` artifact MUST have ≥1 evidence pointer.
3. A `deprecated` artifact MUST point to a replacement.
4. A `transitional` artifact MUST point to its migration target.
5. A `low-confidence` artifact MUST carry a `confidence_note`.

## Audit contract

A scan emits `_repository-governance/reports/semantic-governance/maturity-distribution.json`
on demand. The current phase declares the contract; the per-artifact backfill
is a separate phase.

## Companion files

- [`maturity-policies.json`](maturity-policies.json) — promotion/demotion table in machine-readable form.
