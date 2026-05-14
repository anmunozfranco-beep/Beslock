# Maturity Validation Rules

## Rules

- Every artifact MUST declare validation_status from the governed set.
- Promoted/verified artifacts with confidence=low or ocr_dependency=full are unsafe-promotions.
- Promoted/verified artifacts MUST have non-empty source_refs (no unresolved-evidence-leak).
