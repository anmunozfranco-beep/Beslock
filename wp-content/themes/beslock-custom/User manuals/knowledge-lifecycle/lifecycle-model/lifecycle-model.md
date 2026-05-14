# Knowledge Lifecycle Model

States, transitions, promotion gates, demotion paths, archival rules.

## States

- `candidate` — declared but unverified; lowest trust
- `ocr-derived` — extracted from OEM source via OCR; not yet reviewer-confirmed
- `inferred` — derived from declared neighbours by governed inference
- `reviewer-confirmed` — human reviewer signed off after evidence attachment
- `oem-verified` — bound to a verified OEM source artifact (PDF/screenshot/firmware doc)
- `operationally-proven` — deployed in supervised runtime flows for N successful supervised runs without incident
- `disputed` — two or more declared sources contradict; runtime must escalate
- `deprecated` — superseded by a newer record but preserved for lineage
- `archived` — removed from active retrieval; lineage preserved read-only

## Transitions

- `candidate` → `ocr-derived` via *ocr-evidence-attached* (actor: ocr-pipeline+reviewer, reversible: True)
- `candidate` → `inferred` via *inference-evidence-attached* (actor: reasoning-layer+reviewer, reversible: True)
- `ocr-derived` → `reviewer-confirmed` via *single-reviewer-approval* (actor: reviewer, reversible: True)
- `inferred` → `reviewer-confirmed` via *single-reviewer-approval* (actor: reviewer, reversible: True)
- `reviewer-confirmed` → `oem-verified` via *oem-binding-attached + dual-review* (actor: reviewer x2, reversible: True)
- `oem-verified` → `operationally-proven` via *N supervised runs without incident + signoff* (actor: operator+reviewer, reversible: True)
- `*` → `disputed` via *contradiction-detected* (actor: runtime+reviewer, reversible: True)
- `*` → `deprecated` via *supersession-record-attached* (actor: reviewer, reversible: True)
- `deprecated` → `archived` via *retention-period-elapsed* (actor: governance, reversible: False)
- `*` → `candidate` via *evidence-invalidated (demotion)* (actor: reviewer, reversible: True)

## Promotion gates

- **ocr-evidence-attached** — requires: source_refs[*].kind in {pdf, ocr-fragment, screenshot}, sha256 binding, page/region
- **inference-evidence-attached** — requires: inference_lineage with source node ids, inference rule id, confidence floor
- **single-reviewer-approval** — requires: reviewer identity, supervision receipt, evidence checksum match
- **dual-review** — requires: two distinct reviewers, no shared review session, no escalation override
- **oem-binding-attached** — requires: oem_binding record present, oem source artifact pinned by sha256
- **N supervised runs without incident** — requires: replay-deterministic, no safety-demote, no escalation
- **contradiction-detected** — requires: two oem-verified or reviewer-confirmed records disagree on a binding field
- **supersession-record-attached** — requires: successor node id, rationale, reviewer
- **retention-period-elapsed** — requires: age >= retention_days, no active lineage references
- **evidence-invalidated** — requires: invalidation rationale, reviewer, demotion target tier

## Archival rules

- archival never deletes the node — it moves it out of active retrieval domains
- archived nodes remain readable for lineage queries only
- archival is reversible only by governance review (re-promotion to candidate)
- archival of an OEM-verified record requires a supersession record
