# Operational History Tracking

## Record Types

- **operational-history** — {"captures": "completed steps + outcomes"}
- **troubleshooting-history** — {"captures": "symptoms, branches, hypotheses, outcomes"}
- **attempted-recoveries** — {"captures": "recovery attempts + results + checkpoint used"}
- **failed-paths** — {"captures": "abandoned/refuted paths + reason"}
- **escalation-history** — {"captures": "tier transitions + triggers + provenance"}
- **warning-history** — {"captures": "warnings surfaced + acknowledgement + outcome"}
- **confidence-evolution** — {"captures": "confidence tier of key claims over time"}

## Rules

- history is append-only; no silent edits
- every record carries timestamp + provenance + confidence at time of recording
- destructive operations always emit a history record
- failed paths cannot be silently re-attempted in the same incident (retry caps apply)
- history is queryable; queries do not mutate state
- history of OEM-required events is preserved verbatim
- history may not be used to silently elevate confidence; it can only reference the original tier

## Query Patterns

- by-session-id
- by-incident-id
- by-procedure-id
- by-failure-class
- by-escalation-tier
- by-time-range
