# Runtime Observation Philosophy

Observation is non-mutating. The runtime under observation behaves identically whether telemetry is or is not collected (modulo sink I/O).

## Tenets

- telemetry MUST NOT change runtime decisions
- instrumentation MUST be removable without runtime regression
- observation surface is bounded; new observation requires governance entry
