# e-flex — Knowledge Core

Schema: `knowledge-core/1.0`. Generated 2026-05-13T15:18:31Z by `tools/knowledge_core_build.py`.

This layer is **additive** alongside the legacy `knowledge/` and (for e-orbit)
`structured-knowledge/` layers. Every artifact carries provenance back to an
OEM source under `source-of-truth/` or to the OCR fallback under
`generated_manuals*/`.

## Subdomains

| Subdomain | Purpose |
|---|---|
| install/ | Installation procedures and installation flows. |
| operation/ | Day-to-day operation procedures, configuration, FAQ. |
| workflows/ | End-to-end multi-step workflows (onboarding, pairing, reset, etc). |
| troubleshooting/ | Symptom → resolution entries. |
| warnings/ | OEM warnings and safety notices. |
| terminology/ | Glossary terms. |
| entities/ | Hardware / software / role entity catalog (vocabulary-anchored). |
| capabilities/ | Capability maps (vocabulary-anchored). |
| specifications/ | Hardware specification sheets (e.g. NF14 XLS). |
| semantic/ | Extracted-text evidence, relationships, OCR drafts. |
| provenance/ | OEM source index + extraction lineage. |
| visual/ | Trusted visual references + ComfyUI input contract. |
| orchestration/ | Downstream system contracts (ComfyUI-only). |

## Validation status legend

| Status | Meaning |
|---|---|
| `verified` | Promoted from `structured-knowledge/` (Phase 1) or deterministic spec ingest. Safe for production. |
| `extraction-pending-review` | Authored from normalized markdown by Phase 2 extractor. Needs human review. |
| `inferred-but-unverified` | OCR-derived candidate. Not safe for canonical use. |
| `low-confidence-evidence` | OCR with avg confidence 50–70 %. Evidence-only. |
| `low-confidence-evidence-only` | OCR with avg confidence < 50 %. Evidence-only, do not surface. |

## Critical rules

1. Do not generate final manuals, PDFs, marketing assets, or website pages from
   this layer until each consuming flow has explicit approval.
2. Visual generation downstream of this layer is **ComfyUI-only**.
3. Never edit a `verified` artifact without updating the source under
   `structured-knowledge/` or `source-of-truth/specifications/` first.
4. Never promote a `low-confidence-evidence-only` entity to a higher status
   without independent OEM PDF confirmation.
