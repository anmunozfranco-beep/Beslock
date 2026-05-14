# Retrieval governance

_Schema: `semantic-governance/1.0` · retrieval governance · generated 2026-05-13T17:11:48Z._

## Purpose

Strengthen long-term retrieval consistency. The retrieval **strategy** lives
in `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/retrieval-readiness/`; this document
governs **how** retrieval contracts are kept stable.

## Stability contracts

1. Index source patterns are governed; changing a pattern requires a new
   index ID, not an in-place change.
2. Served fields (`id`, `maturity`, `provenance`, `last_updated`,
   `channel_targets`) are the minimum surface; consumers may rely on them.
3. Identifier grammar is governed; renames require lineage receipts.
4. Synonym expansion at retrieval time uses the canonical-terminology
   registry; consumers SHOULD NOT maintain private synonym lists.
5. Maturity gates are applied at the consumer; consumers MUST read the
   maturity field and MUST surface it in their UX.

## Discoverability rules

- Every entity, procedure, workflow, warning, capability, terminology entry,
  specification and visual semantic MUST be reachable by:
  - direct ID lookup,
  - shared-concept lookup (when applicable),
  - product-level enumeration.
- An artifact that exists on disk but is unreachable by any of the above is
  flagged in the conflict register as `discoverability-orphan` (added in a
  future audit).

## Provenance presentation

- Every served artifact MUST carry its provenance.
- Consumers MUST surface provenance to end users when delivering safety,
  installation, or troubleshooting content.

## Companion files

- [`retrieval-governance.json`](retrieval-governance.json) — machine-readable contract.
