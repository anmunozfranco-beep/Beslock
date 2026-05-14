# Semantic identifier system

_Schema: `semantic-governance/1.0` · identifier governance · generated 2026-05-13T17:11:48Z._

## Purpose

Define the persistent, stable, lineage-safe identifier system used by every
semantic artifact in the knowledge core.

## Grammar

- **Lowercase** ASCII.
- **Kebab-case** (segments separated by single `-`).
- No leading or trailing `-`. No double `-`.
- Regex: `^[a-z0-9]+(?:-[a-z0-9]+)*$`.

## Compound identifier shape

```
<domain-prefix>-<concept>[-<qualifier>][.<schema-version>]
```

| Domain | Prefix |
|---|---|
| terminology          | `term-`              |
| entities             | `entity-`            |
| warnings             | `warning-`           |
| capabilities         | `capability-` (or legacy `cap-`) |
| specifications       | `spec-`              |
| workflows            | `workflow-` (legacy `semantic-wf-` accepted) |
| procedures           | `procedure-` (legacy `semantic-proc-` accepted) |
| procedural-semantics | `semantic-proc-` / `semantic-wf-` |
| visual-intent        | `intent-` / `visual-intent-` |
| visual-risk          | `risk-` / `visual-risk-` |
| publication-intent   | `publication-` / `publication-intent-` |
| component-visibility | `component-`          |
| provenance           | `prov-` / `provenance-` |

## Cross-product linking

- A per-product artifact references a shared concept via the ontology ID
  (e.g. `procedure.factory-reset`).
- The per-product artifact is keyed by `<product>/<domain>/<filename-stem>`.
- The mapping `concept_id ↔ per-product artifact` lives in
  `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`.

## Stability and lineage rules

1. A published ID is **never renamed in place**.
2. A deprecated ID becomes a synonym pointing to its replacement.
3. A renamed file MUST emit a `<old>.lineage.json` receipt with `old_path`,
   `new_path`, `reason`, `timestamp`, `tool`.
4. Cross-product linking uses canonical IDs only. Per-product local IDs are
   never embedded across products.

## Companion files

- [`identifier-grammar.json`](identifier-grammar.json) — machine-readable grammar + prefix table.
