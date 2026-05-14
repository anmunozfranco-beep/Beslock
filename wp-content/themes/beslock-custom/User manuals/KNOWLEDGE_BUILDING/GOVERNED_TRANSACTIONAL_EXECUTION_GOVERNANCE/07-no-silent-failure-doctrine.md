# No Silent Failure

*Layer 40. Subordinate to all 39 prior layers.*

Every failure class emits an append-only failure event preserving transaction state, snapshots, and audit history. Blocking failure classes (snapshot-failure, rollback-failure, replay-failure, lineage-break) block new transactions until the reviewer clears them.
