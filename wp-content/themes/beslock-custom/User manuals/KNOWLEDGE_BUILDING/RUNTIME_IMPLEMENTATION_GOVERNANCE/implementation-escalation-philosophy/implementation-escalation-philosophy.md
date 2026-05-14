# Implementation Escalation Philosophy

Escalation is monotonic, append-only, and locks the slice into read-only handoff.

## Principles

- Escalation is monotonic; tier never decreases.
- Escalation produces append-only records bound to run-id + slice-id.
- Escalation locks the slice into a read-only handoff state.
- Escalation is a safety mechanism, not a fallback for low quality.
