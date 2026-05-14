# Runtime snapshots (phase 47, layer 40)

Append-only deterministic snapshot roots. The CLI executor (`tools/governed_transactional_executor.py`) writes here exclusively; nothing else does. Snapshots are NEVER pruned by the executor (SN-5).

- **repository/** — Snapshots of pre-mutation destination state (one tree per transaction).
- **manifests/** — Snapshots of touched event-store manifests at transaction start.
- **lineage/** — Snapshots of lineage event store at transaction start.
- **publications/** — Snapshots of publication-events store before regeneration.
- **refresh-state/** — Snapshots of refresh-events store before refresh execution.
- **transaction-state/** — Snapshots of the transaction journal at executing → committed boundary.
- **recovery-checkpoints/** — Snapshots taken when a transaction enters recovery-required state.
