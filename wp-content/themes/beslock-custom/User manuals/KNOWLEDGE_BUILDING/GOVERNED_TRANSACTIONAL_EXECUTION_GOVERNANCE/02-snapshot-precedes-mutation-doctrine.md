# Snapshot Precedes Mutation

*Layer 40. Subordinate to all 39 prior layers.*

Every mutation must be preceded by deterministic snapshot capture into runtime-snapshots/<kind>/<tx_id>/<iso>/. Snapshot failure blocks the transaction (SN-8). Snapshots are append-only and never pruned by the executor (SN-5).
