# Retrieval and query readiness

_Schema: `knowledge-center/1.0` · retrieval strategy · generated 2026-05-13T16:54:29Z._

## Purpose

Prepare the knowledge core for chatbot retrieval, RAG, semantic querying,
troubleshooting lookup, onboarding retrieval and contextual publication.
This document defines the indexing strategy and the semantic identifiers
downstream systems will use; it does not implement the index.

## Identifier policy

- Per-product artifacts use the path-derived ID:
  `<slug>/<domain>/<artifact-name-without-extension>`.
  Example: `e-orbit/procedural-semantics/semantic-pin-unlock`.
- Cross-product shared concepts use the ontology IDs (e.g.
  `procedure.factory-reset`).
- Workflow runs use the run-record ID emitted by the orchestrator.

## Indexing strategy

| Index | Source | Consumers |
|---|---|---|
| `entities.idx`              | `ext-images/<slug>/knowledge-core/entities/`             | identification queries, AR overlays |
| `procedures.idx`            | `ext-images/<slug>/knowledge-core/procedural-semantics/` | chatbot, troubleshooting, onboarding |
| `warnings.idx`              | `ext-images/<slug>/knowledge-core/warnings/`             | chatbot safety filter, support |
| `terminology.idx`           | `ext-images/<slug>/knowledge-core/terminology/`          | search expansion, multilingual lookup |
| `capabilities.idx`          | `ext-images/<slug>/knowledge-core/capabilities/`         | catalogue, comparison |
| `troubleshooting.idx`       | `ext-images/<slug>/knowledge-core/troubleshooting/`      | troubleshooting assistant |
| `visual-intent.idx`         | `ext-images/<slug>/knowledge-core/visual-intent/`        | visual assistance, RAG image cards |
| `publication-intent.idx`    | `ext-images/<slug>/knowledge-core/publication-intent/`   | per-channel routing |
| `cross-concept.idx`         | shared ontology + per-product membership                 | cross-product queries |

## Retrieval paths

1. **Direct**: ID → artifact.
2. **Concept**: shared concept ID → membership map → per-product artifacts.
3. **Procedure**: procedure ID → composing workflow + touched entities + warnings + visual intents.
4. **Symptom**: free-text symptom → troubleshooting matches → procedures.
5. **Visual**: visual-intent ID → procedural-semantics + component-visibility + visual-risk.

## Provenance-aware retrieval

Every served artifact MUST carry:

- `id`
- `maturity`
- `provenance` (OEM evidence id + span)
- `last_updated`
- `channel_targets` (when applicable)

Consumers MAY refuse to render artifacts whose `maturity` is below their
threshold. They MUST surface the provenance.

## Future contracts

- Embeddings storage location and embedding-model identity will be declared
  in a future `embeddings/` sub-document; not in scope here.
- Multilingual variants will be addressed by appending a BCP-47 tag to
  artifact IDs; the core ID remains stable.
