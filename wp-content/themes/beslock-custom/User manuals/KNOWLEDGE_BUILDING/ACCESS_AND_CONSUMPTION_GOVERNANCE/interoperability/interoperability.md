# Interop Targets

| system | consumes | guarantees_required |
|---|---|---|
| chatbot | retrieval-bundle, context-assembly.troubleshooting, context-assembly.procedural | provenance per chunk, disambiguation-set support |
| onboarding | onboarding-bundle, context-hierarchies.beginner|installer|administrator | cognitive-load-aware, interruption budget |
| troubleshooting | troubleshooting-bundle | tier-aware escalation, warning injection |
| publication | publication-bundle | maturity ≥ verified, deprecation badges |
| visual-assistance | visual-bundle | visual-risk classified, component-visibility declared |
| multilingual | terminology by-domain, context-assembly with language scope | bilingual variants resolved, shared-terminology declared |


## Invariants

- provenance preserved across all interop boundaries
- governance preserved (no consumer overrides access-governance defaults silently)
- validation integrity preserved (consumers receive validation-passed artifacts only by default)
- ontology coherence preserved (cross-product collisions resolved before exposure)
