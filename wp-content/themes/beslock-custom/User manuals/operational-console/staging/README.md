# Governed staging roots (phase 46, layer 39)

Six append-only buckets governing the lifecycle of intake evidence. The browser surface never writes here directly; the reviewer either drops files manually into `incoming/` or the CLI executor moves files between buckets under explicit reviewer authorization.

- **incoming/** — Drop new evidence here. Reviewer triages in the intake / mutation consoles.
- **review-pending/** — Holds evidence awaiting trust-tier promotion or destination decision.
- **accepted/** — Originals retained after successful copy to canonical destination.
- **rejected/** — Reviewer-rejected evidence (kept for audit; never deleted).
- **quarantined/** — Sources whose mutation failed closed (e.g., destination collision).
- **failed/** — Operations that failed mid-execution (preserved for rollback / inspection).
