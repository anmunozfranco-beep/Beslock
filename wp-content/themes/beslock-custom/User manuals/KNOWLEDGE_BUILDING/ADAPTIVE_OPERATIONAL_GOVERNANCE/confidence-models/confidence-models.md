# Confidence-Aware Guidance

## Tiers

- **verified-truth** — {"claim_strength": "asserts", "may_drive_destructive_step": true, "disclosure_required": false}
- **inferred** — {"claim_strength": "suggests", "may_drive_destructive_step": false, "disclosure_required": true}
- **ocr-derived** — {"claim_strength": "transcribes", "may_drive_destructive_step": false, "disclosure_required": true}
- **ambiguous** — {"claim_strength": "questions", "may_drive_destructive_step": false, "disclosure_required": true}
- **unverified** — {"claim_strength": "withholds", "may_drive_destructive_step": false, "disclosure_required": true}
- **missing** — {"claim_strength": "blocks", "may_drive_destructive_step": false, "disclosure_required": true}

## Rules

- destructive operations require verified-truth or explicit administrator override
- non-verified content must be linguistically downgraded ('likely', 'reported', 'per OCR')
- missing evidence blocks the dependent step; never silently inferred
- OEM-confirmed content cannot be downgraded by adaptation
- confidence tier of a step = lowest tier among its required evidence nodes
- guidance must not aggregate inferred claims into a verified-truth presentation

## Failsafes

- ambiguity present => surface disambiguation, not a guess
- conflicting evidence => block + escalate to knowledge-health
- OCR disagreement with verified-truth => verified-truth wins; OCR flagged
- thresholded numeric specs missing => substitute 'manufacturer-specified' placeholder, do not invent
