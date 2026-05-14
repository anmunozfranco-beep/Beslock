# No Autonomous Recovery

*Layer 40. Subordinate to all 39 prior layers.*

The recovery engine is read-only. It detects incomplete operations and emits a recovery manifest with recommendations; the reviewer chooses replay or rollback and runs the executor explicitly.
