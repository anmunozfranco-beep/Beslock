# Failure Governance Summary

*Phase 47 · layer 40.*

Nine failure classes (mutation-failure, snapshot-failure, replay-failure, rollback-failure, publication-divergence, stale-runtime, partial-refresh, lineage-break, collision-conflict). Each emits an append-only failure-event preserving transaction state, snapshots, and audit history. Blocking classes block new transactions until the reviewer clears them (FG-6).
