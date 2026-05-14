# Operational Validation Methodology

Smallest read-only slice; declared evidence; operator observation; deterministic replay.

## Methodology

- Define the smallest read-only slice that exercises retrieval + assembly + guidance.
- Declare evidence per step; evidence is binding and append-only.
- Run under operator observation with append-only NDJSON traces.
- Promote only on documented evidence; demote on any anomaly.
- Replay deterministically from the captured channels alone.
