# Semantic lineage

_Schema: `knowledge-center/1.0` · lineage specification · generated 2026-05-13T16:54:29Z._

## Lineage chain

```
OEM source (PDF / OEM image / OEM brief)
        │
        ▼
OCR / extraction evidence
   (generated_manuals/<slug>/, ext-images/<slug>/source-of-truth/)
        │
        ▼
Semantic entities / procedures / warnings / terminology / capabilities
   (ext-images/<slug>/knowledge-core/{entities,procedures,workflows,
                                       warnings,terminology,capabilities,
                                       specifications,troubleshooting}/)
        │
        ▼
Canonical knowledge (maturity ∈ {verified, canonical})
        │
        ├─► Procedural semantics
        │     (knowledge-core/procedural-semantics/)
        │
        ├─► Visual semantics
        │     (knowledge-core/{visual-intent,visual-risk,
        │                       component-visibility,publication-intent}/)
        │
        └─► Cross-product map
              (KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/cross-product-semantic-map/)
        │
        ▼
Governance + orchestration contracts
   (KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/, visual-system/_governance/,
    tools/visual_generation.py + tools/comfy/)
        │
        ▼
Future visual / chatbot / RAG / AR / video assistance
```

## Required provenance fields

Every semantic artifact carries:

- `provenance.source_kind`: one of `oem-pdf`, `oem-image`, `oem-brief`,
  `support-record`, `field-observation`.
- `provenance.source_id`: stable identifier of the source.
- `provenance.span`: page + region or timestamp range as applicable.
- `provenance.extracted_by`: the tool or reviewer that produced the artifact.
- `provenance.extracted_at`: ISO-8601 timestamp.
- `provenance.evidence_hash`: SHA-256 of the original evidence (when binary).

## Lineage strength rules

- A `verified` artifact MUST have at least one OEM evidence span.
- A `canonical` artifact MUST have at least one evidence pointer (OEM or
  multi-evidence support).
- An `inferred` artifact MUST list the upstream artifacts it was inferred
  from.
- A visual-semantics artifact MUST point to the canonical knowledge it
  conditions.
- A run record (orchestration layer) MUST point to the visual-semantics
  artifact + the canonical PNG it was conditioned on.

## Forbidden lineage shapes

- An artifact whose only upstream is itself.
- A canonical artifact whose only upstream is an inferred artifact (must be
  promoted to verified or downgraded).
- A visual artifact whose only justification is "designer preference".
- A run record without a workflow id and content hash.
