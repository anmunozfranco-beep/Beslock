# Review Governance

## Checkpoints

| id | trigger | actor |
|---|---|---|
| `ontology-conformance-review` | promotion to normalized-artifact | automated + ontology-steward |
| `canonicalization-review` | promotion to canonical-knowledge | canonicalization-resolver + human-reviewer |
| `human-verification-review` | promotion to verified-truth | human-reviewer |
| `oem-verification-checkpoint` | safety-critical or P0 priority | OEM-confirmation |
| `deprecation-review` | any deprecation request | human-reviewer |
| `ambiguity-escalation-review` | unresolved-stage entry | human-reviewer + OEM-when-applicable |
| `governance-revision-review` | doctrine principle change | governance-steward (multi-party) |

## Rules

- Every promotion to verified-truth requires a human reviewer signature recorded in lineage.
- Safety-critical (P0) artifacts require OEM confirmation in addition to human review.
- Unresolved-stage artifacts are surfaced to a review queue, never silently dropped.
- Ambiguity escalation must record: the ambiguity, the candidates considered, the decision rationale.
- Governance principle changes require multi-party review and a revision-number bump.
