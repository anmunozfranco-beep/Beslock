# Decision Confidence

## Levels

- **high** — {"evidence_basis": "verified-truth", "may_drive_destructive": true, "presentation": "assert"}
- **medium** — {"evidence_basis": "inferred from verified inputs", "may_drive_destructive": false, "presentation": "suggest"}
- **low** — {"evidence_basis": "ocr-derived or partial", "may_drive_destructive": false, "presentation": "downgrade-to-likely"}
- **ambiguous** — {"evidence_basis": "conflicting / unresolved", "may_drive_destructive": false, "presentation": "ask-disambiguation-or-withhold"}
- **missing** — {"evidence_basis": "absent", "may_drive_destructive": false, "presentation": "block"}
- **oem-required** — {"evidence_basis": "verified-truth not yet OEM-confirmed for P0 promotion", "may_drive_destructive": false, "presentation": "withhold-and-escalate"}

## Rules

- decision confidence = lowest tier across required evidence nodes
- high-confidence is the only level that may drive destructive decisions without administrator override
- low/ambiguous/missing decisions cannot be silently elevated
- OEM-required decisions cannot be assumed; they escalate
- confidence must be recorded with the decision (audit trail)
- aggregation never elevates inferred to verified-truth
