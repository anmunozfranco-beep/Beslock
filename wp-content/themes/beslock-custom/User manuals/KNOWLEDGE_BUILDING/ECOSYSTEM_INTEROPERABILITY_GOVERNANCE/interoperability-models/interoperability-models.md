# Cross-Runtime Interoperability Models

Declared interoperability edges between future runtime kinds. None create destructive cross-runtime paths.

## Runtime kinds

- `onboarding-runtime`
- `troubleshooting-runtime`
- `retrieval-runtime`
- `operational-copilot`
- `visual-assistance-runtime`
- `publication-runtime`
- `continuity-system`

## Models

- `retrieval↔copilot` — retrieval-runtime → operational-copilot (read-only context supply)
- `copilot↔troubleshooting` — operational-copilot → troubleshooting-runtime (supervised handoff with continuity snapshot)
- `copilot↔onboarding` — operational-copilot → onboarding-runtime (supervised handoff with intent declaration)
- `troubleshooting↔visual` — troubleshooting-runtime → visual-assistance-runtime (read-only visual surface request (gated by visual-risk freeze))
- `onboarding↔continuity` — onboarding-runtime → continuity-system (checkpoint emission (append-only))
- `troubleshooting↔continuity` — troubleshooting-runtime → continuity-system (checkpoint + hypothesis snapshot (append-only))
- `any↔publication` — any-runtime → publication-runtime (read-only publication contract; never bypasses lifecycle P-tier gates)
- `continuity↔any` — continuity-system → any-runtime (context inheritance (read-only, with non-inheritable signals filtered))
- `copilot↔visual` — operational-copilot → visual-assistance-runtime (read-only visual reference; no image generation)
- `any↔retrieval` — any-runtime → retrieval-runtime (read-only retrieval request bound by declared access pattern)

## Rules

- Interoperability is bilateral and declared; no undeclared edges may be opened at runtime.
- Interoperability never creates a destructive cross-runtime path (destructive surface remains intra-runtime + supervised).
- Interoperability messages carry provenance (origin runtime, schema version, incident-id when available).
- Interoperability cannot bridge two runtimes via a third, undeclared intermediary.
- Interoperability with publication-runtime cannot bypass lifecycle P-tier gates.
- Interoperability with visual-assistance-runtime cannot trigger image generation, PDF rendering, or any rendered artefact.
- Interoperability respects knowledge-core directionality (read-only); cross-runtime mutation of knowledge-core is forbidden.
