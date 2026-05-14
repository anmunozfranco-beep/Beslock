# Change Impact Modeling

## Impact targets

- ontology
- schemas
- terminology
- entities
- procedures
- workflows
- warnings
- capabilities
- specifications
- troubleshooting
- procedural-semantics
- visual-intent
- visual-risk
- publication-intent
- component-visibility
- provenance
- retrieval-index
- onboarding-flows
- guidance-triggers
- cognitive-load-map
- priority-assignments
- experience-charter

## Propagation rules

- **terminology rename without alias** → entities, procedures, workflows, warnings, retrieval-index, guidance-triggers
- **ontology field removed** → schemas, all knowledge-core domains, retrieval-index
- **procedure step reordered** → workflows, cognitive-load-map, onboarding-flows, guidance-triggers
- **warning removed** → procedures, workflows, publication-intent, experience-charter
- **entity superseded** → procedures, workflows, visual-intent, component-visibility, retrieval-index
- **priority tier change (P-level)** → onboarding-flows, guidance-triggers, review-checkpoints
- **visual-risk reclassification** → visual-intent, publication-intent, guidance-triggers
- **schema breaking change** → all knowledge-core domains, retrieval-index, review-checkpoints

## Procedure

1. Detect change class (additive / corrective / breaking).
2. Resolve propagation set via IMPACT_RULES.
3. Generate change-impact-report listing every dependent artifact id.
4. Block promotion if any dependent artifact would enter unresolved/lineage-break state.
5. Attach the impact-report id to the version-bump record.
