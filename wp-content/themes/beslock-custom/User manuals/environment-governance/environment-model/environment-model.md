# Operational Environment Model

Six declared operational environments with trust levels, supervision levels, constraints, and isolation guarantees.

## Environments

- `local-supervised-runtime` — trust: high (operator-bounded); supervision: full HITL on every checkpoint; isolation: process-local; no network egress required
- `staging-environment` — trust: medium; supervision: full HITL + dual-review on promotions; isolation: dedicated staging trust-zone; no cross-env reads
- `controlled-pilot` — trust: medium (scoped); supervision: full HITL + escalation-supervisor on slice-halt; isolation: pilot trust-zone; no governance-console exposure
- `future-production` — trust: governed (declared, not active); supervision: full HITL + dual-review + auditor co-signature for emergency actions; isolation: production trust-zone; one-way ingress for OEM evidence
- `oem-ingestion-environment` — trust: semi-trusted; supervision: OEM-reviewer dual-review; isolation: ingestion trust-zone; outputs only to staging
- `reviewer-operation-environment` — trust: high (reviewer-bounded); supervision: reviewer claim + queue ceiling; isolation: reviewer trust-zone; read-only against runtime channels

## Invariants

- every environment declares a trust level, a supervision level, and an isolation guarantee
- no environment ever inherits trust from another environment
- no environment ever shares write paths with a higher-trust environment
- no environment ever bypasses the supervision level declared by the layer above it
- no environment runs without an append-only log destination
