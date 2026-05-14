# Deployment Dependencies

Declared deployment dependencies across runtime / cognition / orchestration / interop / governance layers.

## Dependencies

- `context-vector-emitter` (kind: cognition) → required by: operational-copilot, procedural-assembly-runtime
- `confidence-tier-on-nodes` (kind: cognition) → required by: operational-copilot, troubleshooting-runtime, administrator-assistant
- `provenance-emitter` (kind: observability) → required by: operational-copilot, onboarding-runtime, troubleshooting-runtime, administrator-assistant
- `incident-id-emitter` (kind: continuity) → required by: onboarding-runtime, troubleshooting-runtime, operational-copilot
- `checkpoint-registry` (kind: continuity) → required by: onboarding-runtime, troubleshooting-runtime, administrator-assistant
- `fallback-registry` (kind: decision) → required by: operational-copilot, troubleshooting-runtime
- `intent-declaration-channel` (kind: interop) → required by: onboarding-runtime, operational-copilot
- `supervision-receipt-emitter` (kind: supervision) → required by: operational-copilot, onboarding-runtime, administrator-assistant
- `schema-pin-enforcement` (kind: governance) → required by: all
- `oem-channel-contract` (kind: interop) → required by: administrator-assistant
- `role-declaration-channel` (kind: supervision) → required by: administrator-assistant
- `hypothesis-store` (kind: reasoning) → required by: troubleshooting-runtime
- `causal-edges-emitted` (kind: reasoning) → required by: troubleshooting-runtime, operational-copilot
- `warning-corpus-complete` (kind: experience) → required by: onboarding-runtime, troubleshooting-runtime, operational-copilot, administrator-assistant
- `symptom-corpus-≥10-per-product` (kind: knowledge-core) → required by: troubleshooting-runtime

## Rules

- Dependencies are declared; ad-hoc dependencies are unsafe.
- A runtime cannot be promoted past supervised-runtime phase while any declared dependency is unmet.
- Cross-runtime dependencies follow the federation contracts; never invented at deployment time.
- Governance dependencies (schema-pin-enforcement) bind every candidate.
- Dependency satisfaction requires evidence (a passing report or a declared emitter).
