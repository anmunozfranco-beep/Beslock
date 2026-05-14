# Semantic Query Intents

| id | examples | primary_targets |
|---|---|---|
| how-to | how to reset e-orbit, how to enroll fingerprint | procedures, workflows, procedural-semantics |
| what-is | what is 2.4G, what is admin mode | terminology, entities, capabilities |
| where-is | where is the reset button | entities, component-visibility, visual-intent |
| why-failure | pairing failures, why won't it unlock | troubleshooting, warnings |
| prerequisite | installation prerequisites, what do I need before | workflows.preconditions, procedural-semantics |
| comparison | e-orbit vs e-shield | capabilities, specifications, shared-concepts |
| safety | is it safe to factory reset | warnings, visual-risk, publication-intent |
| lookup-id | wf-alta-desde-tuya-app | by-id |
| ambiguous | app, lock | disambiguation-set |


## Resolution procedure

1. Detect intent class.
2. Resolve product scope (explicit token, current session product, or fan-out across all products).
3. Map intent to primary targets via QUERY_INTENTS.
4. Apply access-governance filters (maturity, deprecation, unresolved).
5. Assemble context bundle (see context-assembly).
6. If zero results, escalate to fallback strategy.
7. If multiple equal-confidence results, return disambiguation-set, never silently choose.

## Fallbacks

- synonym expansion via terminology.oem_variants
- bilingual expansion via terminology.canonical/oem_variants
- domain-broaden (procedures -> workflows -> procedural-semantics)
- product-broaden (single -> shared-concepts -> all)
- explicit unresolved-knowledge response (never fabricate)

## Ambiguity rules

- An ambiguous query MUST return a disambiguation-set, not a guess.
- Disambiguation-set entries carry: id, product, summary, maturity, confidence.
- Resolution chosen by the consumer is recorded in the access trace.
