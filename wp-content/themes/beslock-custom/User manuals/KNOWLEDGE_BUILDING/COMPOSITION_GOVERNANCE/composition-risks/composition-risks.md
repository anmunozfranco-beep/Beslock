# Unresolved Composition Risks

| id | severity | description | ref |
|---|---|---|---|
| thin-troubleshooting-corpus | high | 5/6 products lack troubleshooting symptoms; troubleshooting-package only assembles for e-shield. | validation/02-workflow-executability.json |
| warning-corpus-gap | high | 2 products have empty warning corpora; warnings-follow-procedures rule cannot fire. | validation/05-experience-validation.json |
| channel-targets-coverage | high | 417 artifacts missing channel_targets; package channel-binding under-determined. | validation/06-retrieval-validation.json |
| capability-not-declared-per-product | medium | Capability assemblies (e.g. fingerprint-management) cannot resolve where capability is undeclared per product. |  |
| audience-scope-not-authored | medium | Per-artifact audience_scope assignments not yet authored; contextual composition relies on heuristics. |  |
| snapshot-hash-not-emitted | medium | Determinism contract requires knowledge-core snapshot hash on every assembly; not yet integrated. |  |
| circular-prerequisite-detection | low | Cycle detection at composition time depends on graph-validation passing; currently 0 cycles, but contract must remain enforced. |  |
| shared-concepts-undeclared | high | 15 cross-product entity-collisions + 10 terminology-collisions block cross-product capability composition. |  |
