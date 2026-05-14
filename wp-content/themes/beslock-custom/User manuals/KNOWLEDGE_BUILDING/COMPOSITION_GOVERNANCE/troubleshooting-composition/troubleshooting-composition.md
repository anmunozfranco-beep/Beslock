# Troubleshooting Composition

## Inputs

- symptom-category
- observed-state
- product-state
- user-role
- audience-scope

## Outputs

- matched-symptom (or unresolved-symptom)
- tier-assignment (0..5)
- recovery-procedure-set
- warnings-injected
- safety-constraints-attached
- escalation-path
- provenance-bundle

## Rules

- If symptom does not match the corpus, return unresolved-symptom + escalation to tier-4 (vendor) — never fabricate a recovery.
- Recovery procedures attached MUST be at maturity ≥ verified for safety-critical tiers.
- Tier escalation is monotonic: a single trace cannot oscillate down a tier.
- Safety constraints (P0 warnings) are always attached; consumers cannot suppress them.
