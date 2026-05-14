# Context Dimensions

## Dimensions

- **user-role** — {"values": ["beginner", "intermediate", "advanced", "installer", "administrator", "operator", "maintenance"]}
- **operational-mode** — {"values": ["normal", "onboarding", "troubleshooting", "recovery", "maintenance", "degraded", "emergency"]}
- **lifecycle-stage** — {"values": ["pre-install", "installing", "configuring", "operating", "decommissioning"]}
- **confidence-level** — {"values": ["verified-truth", "inferred", "ocr-derived", "ambiguous", "unverified"]}
- **severity-level** — {"values": ["nominal", "warning", "blocked", "unsafe", "irrecoverable"]}
- **recovery-status** — {"values": ["none", "in-progress", "succeeded", "failed", "escalated"]}
- **onboarding-stage** — {"values": ["unboxed", "physically-installed", "powered", "paired", "enrolled", "verified"]}
- **environmental** — {"values": ["normal-power", "low-battery", "offline", "noisy", "physical-restricted-access"]}
- **evidence-completeness** — {"values": ["complete", "partial", "missing", "conflicting"]}
- **intent-clarity** — {"values": ["explicit", "inferred", "ambiguous", "missing"]}

## Rules

- context dimensions are observed, never assumed
- missing dimensions resolve to the safest value
- dimension values must be declared (no free-form context)
- multiple dimensions compose; no dimension overrides another silently
- context vector must be reproducible from declared inputs
