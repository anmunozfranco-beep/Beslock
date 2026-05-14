# Cross-product semantic map

_Schema: `knowledge-center/1.0` · cross-product intelligence · generated 2026-05-13T16:54:29Z._

## Purpose

Identify shared hardware concepts, shared workflows, shared warnings, shared
terminology, shared operational semantics and shared troubleshooting concepts
across the six Beslock products. The goal is platform-level intelligence
without flattening per-product nuclei.

## Coverage by semantic domain

| Domain | Coverage | Products with at least one artifact |
|---|---:|---|
| entities | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| procedures | 0 / 6 | — |
| workflows | 5 / 6 | e-flex, e-orbit, e-prime, e-shield, e-touch |
| warnings | 5 / 6 | e-flex, e-orbit, e-prime, e-shield, e-touch |
| terminology | 5 / 6 | e-flex, e-orbit, e-prime, e-shield, e-touch |
| capabilities | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| specifications | 1 / 6 | e-orbit |
| troubleshooting | 1 / 6 | e-shield |
| procedural-semantics | 5 / 6 | e-flex, e-orbit, e-prime, e-shield, e-touch |
| visual-intent | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| visual-risk | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| publication-intent | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| component-visibility | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |
| provenance | 6 / 6 | e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch |

## Shared-concept membership pattern

For every shared concept defined in the ontology, the cross-product map
declares which products instantiate it and where the per-product artifact
lives:

```json
{
  "concept_id": "procedure.factory-reset",
  "members": [
    {"product": "e-orbit", "artifact": "ext-images/e-orbit/knowledge-core/procedural-semantics/semantic-factory-reset.json"},
    {"product": "e-flex",  "artifact": "ext-images/e-flex/knowledge-core/procedural-semantics/semantic-factory-reset.json"}
  ]
}
```

The membership map itself lives at
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`
once the per-product artifacts are tagged with their concept IDs (Phase 8 does
not retroactively tag artifacts; it specifies the contract).

## Shared workflow patterns

The following workflows recur across multiple products and SHOULD be modelled
as shared concepts in the knowledge graph:

- Initial pairing with the companion app.
- First-user enrolment (PIN, fingerprint).
- Battery replacement.
- Emergency power application.
- Factory reset.
- Firmware update.

## Shared warning patterns

- Low-battery behaviour.
- Lockout after consecutive failed attempts.
- Tamper alert.
- Data loss on factory reset.

## Shared terminology

- The canonical locale is Colombian Spanish (`es-CO`).
- Term collisions across products are resolved by promoting the term to the
  shared terminology vocabulary; per-product synonyms are preserved with a
  pointer to the canonical term.

## Cross-product queries

The cross-product map enables queries such as:

- "Which products support fingerprint enrolment?"
- "What is the factory-reset procedure across the line?"
- "Which products share the same low-battery warning behaviour?"
- "Which procedures touch the deadbolt across the line?"
