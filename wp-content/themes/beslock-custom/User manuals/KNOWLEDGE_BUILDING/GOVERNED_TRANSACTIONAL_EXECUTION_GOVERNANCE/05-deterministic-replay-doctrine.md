# Deterministic Replay

*Layer 40. Subordinate to all 39 prior layers.*

Replay is reconstructed from snapshots + transaction journal + manifest events; same inputs always yield the same replay. Default mode is verify-only; writing mode requires --confirm and lands in rollback-target/, never the live tree.
