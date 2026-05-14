# Cross-product semantic governance

_Schema: `semantic-governance/1.0` · cross-product governance · generated 2026-05-13T17:11:48Z._

## Purpose

Identify reusable semantic primitives, shared operational concepts, reusable
warning models, reusable installation logic and reusable workflow archetypes.
Prevent cross-product semantic contamination.

## Promotion rules (concept → shared)

A concept becomes shared when it is observed in **two or more products** AND
the editorial review confirms semantic equivalence. The concept is then
promoted to the shared ontology in
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/ontology.json` and
its members are recorded in `shared-concept-membership.json`.

## Anti-contamination rules

1. A per-product artifact MUST NOT silently inherit text or fields from
   another product.
2. A per-product artifact MUST NOT reference another product's local ID;
   cross-product links go through shared concept IDs only.
3. A per-product artifact MUST NOT borrow a warning, terminology entry or
   procedural step from another product without (a) explicit reviewer
   note and (b) provenance pointing back to OEM evidence for the borrowing
   product.

## Reusable archetypes

- **Pairing archetype**: pair-with-app + variant (qr-pairing, ez-mode-pairing).
- **Enrolment archetype**: register-fingerprint + register-pin + add-administrator + add-user.
- **Recovery archetype**: factory-reset + emergency-power + battery-replacement.
- **Operational archetype**: unlock-* (pin / fingerprint / app / mechanical).
- **Maintenance archetype**: firmware-update + battery-replacement.

## Companion files

- [`cross-product-coherence.json`](cross-product-coherence.json) — archetype list + promotion rules.
