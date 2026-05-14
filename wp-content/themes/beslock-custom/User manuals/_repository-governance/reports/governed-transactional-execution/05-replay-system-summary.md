# Replay System Summary

*Phase 47 · layer 40.*

Deterministic replay reconstructed from snapshots + transaction journal + mutation/lineage/snapshot events. Two modes (verify-only, reconstruct-into-rollback-target). Default mode is read-only (RPL-2); writing mode requires --confirm and never overwrites the live tree (RPL-6).
