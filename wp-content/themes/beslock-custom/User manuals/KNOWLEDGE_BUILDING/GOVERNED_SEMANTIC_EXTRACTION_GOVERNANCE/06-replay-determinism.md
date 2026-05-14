# 06-replay-determinism

Replay reconstructs lineage chains, verifies manifest sha256, and is deterministic across invocations. Non-determinism and hash mismatch are fail-closed. Replay NEVER mutates live publication trees, prior-layer runtime trees, or source evidence.
