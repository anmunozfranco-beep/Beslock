# Human Review Workflows

Reviewer assignment, evidence attachment, single/dual review, consensus, irreversible-operation review.

## Reviewer assignment

- reviewers are declared in a reviewer registry (identity + signoff scope)
- assignment is by domain (operation, warnings, troubleshooting, install, ...) and product
- no reviewer may approve their own authored record
- OEM-binding reviews require an OEM-scope reviewer

## Workflow steps

- **intake** — validate candidate schema + scope (actor: automation)
- **triage** — assign reviewer(s) by domain+product (actor: governance)
- **evidence-pull** — attach OEM source artifacts + checksums (actor: reviewer)
- **single-review** — first-pass approve/reject + rationale (actor: reviewer-1)
- **dual-review** — second-pass (required for OEM promotion) (actor: reviewer-2)
- **consensus** — resolve disagreement via documented merge (actor: governance)
- **signoff** — emit supervision receipt + state transition (actor: governance)
- **post-audit** — append append-only review record (actor: automation)

## Consensus rules

- approve/approve → promote
- approve/reject  → escalate to consensus reviewer
- reject/reject   → demote to candidate + rationale
- any reviewer flags irreversible-operation → force escalation review
- no silent overrides; every override is a logged decision

## Irreversible-operation review

- records touching irreversible operations (factory reset, admin wipe, firmware) require:
-   - dual-review
-   - operator co-signature
-   - explicit reversibility statement (or declared irreversibility)
-   - mandatory escalation policy on the record
