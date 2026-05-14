# Unresolved Execution Risks

| id | severity | description | ref |
|---|---|---|---|
| thin-troubleshooting-corpus | high | 5/6 products have no troubleshooting symptoms; recovery-path resolution is blocked. | validation/02-workflow-executability.json |
| warning-corpus-gap | high | 2 products lack warnings; mandatory-warning-surface safeguard cannot fire. | validation/05-experience-validation.json |
| no-checkpoints-declared | high | Per-procedure checkpoint declarations are not yet authored in the knowledge-core; recovery anchors are heuristic. |  |
| no-validation-predicates-declared | high | Procedures do not yet declare validation-predicates; completion currently inferred from terminal state alone. |  |
| no-confirmation-flags-on-steps | medium | Steps do not yet carry `confirmation_required` flags; assistants would need conservative defaults. |  |
| intent-mismatch-detection | medium | Intent vs operational-state coherence checking is contractual; no live detector yet. |  |
| snapshot-hash-not-emitted | medium | Execution traces require knowledge-core snapshot hash for determinism; awaiting lifecycle integration. |  |
| shared-concepts-undeclared | medium | Cross-product entity/terminology collisions block uniform state-model application across products. |  |
