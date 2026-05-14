# LIFECYCLE_GOVERNANCE

Constitutional layer governing the **long-term evolution** of the Beslock knowledge center.

- Schema: `lifecycle-governance/1.0`
- Generated: 2026-05-13
- Subordinate to: `knowledge-core`
- Coexists with: `VISUAL_GOVERNANCE`, `KNOWLEDGE_CENTER`, `SEMANTIC_GOVERNANCE`, `EXPERIENCE_GOVERNANCE`

This layer governs **how knowledge changes over time**. It does not originate
knowledge, does not author content, and does not modify per-product
`knowledge-core/` files. It defines the lifecycle, promotion gates, deprecation
rules, versioning axes, health monitoring, review checkpoints, change-impact
propagation, knowledge debt classes, long-term architecture rules, and future
system readiness gates.

## Authority areas
- lifecycle-stages
- promotion-governance
- deprecation-governance
- versioning-governance
- knowledge-health
- review-governance
- change-impact
- knowledge-debt
- long-term-architecture
- future-readiness

## Doctrine layout
- `00-charter.md` — principles + authority areas
- `knowledge-lifecycle/` — stages and transitions
- `promotion-governance/` — evidence → verified-truth gates
- `deprecation-governance/` — retirement, supersession, archival rules
- `version-governance/` — semver / calver / revision axes
- `knowledge-health/` — indicators and thresholds
- `review-governance/` — human and OEM checkpoints
- `change-impact/` — propagation rules and procedure
- `knowledge-debt/` — debt classes and resolution rules
- `long-term-architecture/` — principles, integration, subordination
- `future-readiness/` — downstream-consumer readiness gates
