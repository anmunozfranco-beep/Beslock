# Runtime Packaging Strategy

## Package Types

- **retrieval-package** — {"consumers": ["onboarding-systems", "troubleshooting-systems", "contextual-assistants", "operational-copilots"], "surface": "read-only"}
- **assembly-package** — {"consumers": ["contextual-assistants", "operational-copilots", "future-visual-assistance"], "surface": "read-only"}
- **guidance-package** — {"consumers": ["onboarding-copilots", "troubleshooting-assistants", "operational-copilots"], "surface": "read-only + supervised-confirmation"}
- **escalation-package** — {"consumers": ["support-handoff", "OEM-handoff"], "surface": "read-only snapshot"}
- **continuity-package** — {"consumers": ["session-aware-operational-copilots", "operational-memory-systems"], "surface": "read-only + supervised-resume"}
- **multimodal-package (gated)** — {"consumers": ["multimodal-runtime-systems", "future-visual-assistance"], "surface": "read-only", "gated_by": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable"]}

## Rules

- packages declare: surface (read-only / supervised), consumers, contracts honoured, schema version, gates
- packages are immutable once emitted; updates produce a new package version
- packages carry provenance manifests (which knowledge-core nodes contributed)
- packages cannot include un-promoted content beyond declared tier
- no package mixes read-only and executive surfaces in a single artefact
