# Risks

| id | severity | description | ref |
|---|---|---|---|
| channel-targets-coverage-gap | high | Many artifacts lack channel_targets; retrieval-bundle synthesis is constrained. | validation/06-retrieval-validation.json |
| shared-concepts-undeclared | high | Cross-product entity/terminology collisions detected without shared-concept registry; access fan-out cannot deduplicate. | validation/03-entity-consistency.json |
| troubleshooting-corpus-thin | high | 5/6 products have no troubleshooting artifacts; troubleshooting-bundle synthesis blocked per product. | validation/02-workflow-executability.json |
| warning-corpus-gap | high | 2 products have empty warning corpus; procedural-context warning-injection cannot fire. | validation/05-experience-validation.json |
| maturity-floor-population | medium | Most artifacts are extraction-pending-review; canonical/verified pool is small (~7%); RAG gating excludes the majority. |  |
| snapshot-hash-not-emitted | medium | Bundles do not yet carry knowledge-core snapshot hash; deterministic re-issue requires future lifecycle integration. |  |
| audience-scope-not-declared | medium | Per-artifact audience-scope assignments are not yet authored; hierarchy filtering relies on heuristics. |  |
| disambiguation-set-untested | low | Disambiguation contract is declared but not exercised against a real query corpus. |  |
