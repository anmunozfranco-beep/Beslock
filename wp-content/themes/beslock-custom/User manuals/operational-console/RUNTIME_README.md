# Governed filesystem execution — RUNTIME README (phase 46, layer 39)

## What this layer adds

This is the FIRST repo-native layer that performs REAL filesystem mutation. All prior governance is preserved.

Three pieces work together:

1. **Browser surfaces** under `mutation-console/`, `lineage-console/`, `rollback-console/`, `safety-console/` — propose / inspect only.
2. **Rule tables** under `execution-engine/` — deterministic, reviewer-authoritative, consumed by both browser and CLI.
3. **CLI executor** at `tools/governed_fs_executor.py` — the ONLY filesystem-writing component. Reviewer must invoke it explicitly with `--confirm`.

## Reviewer workflow

```
# 1. Drop a file into the staging root
cp ~/Downloads/manual.pdf wp-content/themes/beslock-custom/"User manuals"/operational-console/staging/incoming/

# 2. Open the mutation console (or any exec console) in the browser:
python3 -m http.server 8000
# then visit http://localhost:8000/wp-content/themes/beslock-custom/User%20manuals/operational-console/mutation-console/exec.html

# 3. Fill in the form, click "Resolve destination" and "Build & download request".
#    A mutation-request-<uuid>.json is downloaded.

# 4. Run the executor (the console prints the exact command):
python3 tools/governed_fs_executor.py --kind mutation --request ~/Downloads/mutation-request-<uuid>.json --confirm
```

## Hard guarantees

- No daemon, no watcher, no autonomous agent.
- Destructive overwrite is forbidden — the executor fails closed.
- Knowledge-core, governance, runtime-implementation and the runtime-manifest event stores are immutable from intake.
- Every successful operation appends to (a) operation event store, (b) lineage event store, (c) audit event store.
- Every failed operation routes the source to `staging/quarantined/` and emits an audit event.


---

## Phase 47 addendum — governed transactional execution & recovery (layer 40)

Layer 39 introduced REAL filesystem mutation. Layer 40 wraps every mutation in a governed transaction with deterministic snapshot capture, reviewer-authorized rollback execution, interrupted-operation recovery detection, deterministic replay, and multi-channel integrity verification.

### New CLI

```
python3 tools/governed_transactional_executor.py \
    --kind {transaction|rollback-exec|recovery-detect|replay|integrity|consistency} \
    --request /path/to/request.json \
    --confirm
```

Without `--confirm`: dry-run (validates request, prints plan, exits non-zero on any failure). With `--confirm`: appends transaction-events / snapshot-events / mutation-events / lineage-events / audit-events as appropriate.

### New surfaces

- `transaction-console/exec.html` — transaction inspector + builder
- `snapshot-console/exec.html` — snapshot explorer (read-only)
- `recovery-console/exec.html` — recovery manifest detector (read-only)
- `replay-console/exec.html` — deterministic replay reconstructor
- `integrity-console/exec.html` — multi-channel integrity dashboard
- `failure-console/exec.html` — failed-operation explorer

### Hard guarantees added by layer 40

- No mutation outside a governed transaction boundary (TX-1).
- Snapshot capture must precede mutation (SN-1); snapshot failure blocks the transaction (SN-8).
- Snapshots are append-only and never pruned by the executor (SN-5).
- Rollback restores into `rollback-target/`, never overwrites the live tree (RBE-6).
- No autonomous recovery, rollback, or replay (REC-5 / RBE-1 / RPL-5).
- Integrity engine is strictly read-only and never auto-repairs (INT-R-1 / INT-R-4).
- No silent failure recovery (FG-5); every failure emits an append-only failure-event.


## phase 48 — governed knowledge synthesis & canonical publication generation

Layer 41. Subordinate to layer 40.

Reviewer flow:
1. Open the synthesis console; pick evidence_ids; export an envelope.
2. Run `python3 tools/governed_knowledge_synthesis_executor.py --kind synthesis --request <file> --confirm`.
3. Inspect the synthesis manifest in `operational-console/synthesis-drafts/`.
4. Resolve any conflicts via the evidence-resolution console + `--kind evidence-resolve --confirm`.
5. Approve the synthesis (publication-lifecycle: draft → synthesized → review-required → reviewer-approved).
6. Build the publication: `--kind publication-build --confirm`. Outputs land under `operational-console/publication-builds/<build_id>/` (HTML + JSON).
7. Transition the build to `publication-ready`; rollback is achieved by superseding, never by overwrite.

Hard rules:
- No LLM, no ML, no embeddings.
- No silent evidence merge; every conflict is explicit.
- Live publication tree is never overwritten by this layer.
- All transitions are append-only and reviewer-attributed.


## phase 49 — governed multimodal knowledge grounding & visual publication orchestration

Layer 42. Subordinate to layer 41 (governed-knowledge-synthesis-and-canonical-publication-governance).

Mutation is performed exclusively by `tools/governed_multimodal_grounding_executor.py --confirm`.
Subcommands (`--kind`):

- `grounding` — bind images to procedural / troubleshooting / specification / warning / installation / operational targets.
- `supportive-image-mapping` — declare image role and applicability.
- `prompt` — append a reviewer-authored prompt (append-only; revisions carry prior_prompt_id).
- `visual-publication-build` — write a deterministic visual manual (HTML + JSON) under `operational-console/visual-publication-builds/draft/<build_id>/`.
- `visual-troubleshooting` — bind visuals to a troubleshooting flow.
- `procedural-continuity` — record continuity check (gaps, orphans, broken lineage, reviewer-accepted gaps).
- `visual-asset-lifecycle-transition` — advance an image through candidate → grounded → review-required → reviewer-approved → publication-ready → {superseded | deprecated}.

Every command:
- requires reviewer attribution,
- is fail-closed on missing evidence / broken lineage / illegal transitions,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `grounding-drafts/`, `prompt-drafts/`, `visual-publication-builds/`, or `visual-asset-ledger/`.


## phase 50 — governed visual generation & deterministic asset production

Layer 43. Subordinate to layer 42 (governed-multimodal-grounding-and-visual-publication-governance).

Mutation is performed exclusively by `tools/governed_visual_generation_executor.py --confirm`.
Subcommands (`--kind`):

- `generation-request` — record a reviewer-authored generation request (the runtime never generates).
- `generated-asset-register` — record a reviewer-supplied generated asset with sha256 + prompt + grounding lineage.
- `review-comparison` — record a reviewer-authored multi-variant comparison (no ML scoring).
- `publication-visual-selection` — record a reviewer-attributed publication selection (asset MUST be reviewer-approved).
- `visual-supersedence` — append-only supersedence between asset records.
- `generation-session` — open / freeze / close / reject a reviewer-led generation session.
- `asset-lifecycle-transition` — advance an asset through candidate → review-required → reviewer-approved → publication-selected → {superseded | deprecated}; or → rejected.
- `visual-integrity` — record a reviewer-led integrity check (sha256 + lineage + grounding-preservation).

Every command:
- requires reviewer attribution,
- is fail-closed on missing grounding / missing prompt lineage / missing sha256 / illegal transitions / OEM overwrite attempts,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/visual-generation-runtime/` subtrees.

The visual-generation-runtime tree is isolated from:
- the live publication tree,
- the layer-42 visual-publication-builds tree,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads.


## phase 51 — governed multimodal publication composition & page orchestration

Layer 44. Subordinate to layer 43 (governed-visual-generation-and-deterministic-asset-production-governance).

Mutation is performed exclusively by `tools/governed_publication_composition_executor.py --confirm`.
Subcommands (`--kind`):

- `composition-draft` — record a reviewer-authored composition draft (synthesis_id + section_order + manual_kind).
- `page-layout` — record a reviewer-authored page layout (deterministic block list, role-typed).
- `multimodal-sequence` — record a procedural / troubleshooting / comparison sequence with reviewer-declared ordering.
- `responsive-layout` — record per-block parity across mobile/tablet/desktop/print (warnings cannot be omitted).
- `page-continuity` — record a continuity scan: page-index contiguity, orphan sections, orphan visuals.
- `publication-assembly` — record a deterministic page-layout assembly with sha256 of the manifest.
- `layout-review` — record a reviewer's page-level decision (approve / request-changes / reject + cited_rule_ids).
- `composition-lifecycle-transition` — advance composition through draft → composed → review-required → reviewer-approved → publication-ready → {superseded → deprecated}.
- `composition-integrity` — record a reviewer-led integrity scan (orphan visuals, warning placement, responsive parity, hidden-section detection).

Every command:
- requires reviewer attribution,
- is fail-closed on missing section lineage / orphan visuals / warning-placement violations / broken responsive parity / illegal lifecycle transitions / hidden section insertion,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/publication-composition-runtime/` subtrees.

The publication-composition-runtime tree is isolated from:
- the live publication tree,
- the layer-42 visual-publication-builds tree,
- the layer-43 visual-generation-runtime tree,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads.


## phase 52 — governed semantic evidence analysis & multimodal extraction runtime

Layer 45. Subordinate to layer 44 (governed-multimodal-publication-composition-and-page-orchestration-governance).

Mutation is performed exclusively by `tools/governed_semantic_extraction_executor.py --confirm`.
Subcommands (`--kind`):

- `evidence-decomposition` — record a reviewer-authored decomposition of video / image / pdf / xls / xlsx / csv evidence (keyframes / pages / worksheets / regions).
- `ocr-fragment` — record a reviewer-attributed OCR fragment with verbatim text and lineage to a decomposition region/page/frame.
- `ocr-correction` — record a reviewer override of a prior OCR fragment (cites prior_fragment_id; append-only).
- `extraction-candidate` — record a typed extraction candidate (one of CANDIDATE_KINDS) with full lineage pointers, reasoning_chain, and confidence_state.
- `temporal-continuity` — record a temporal continuity scan for a video decomposition (gaps fail-closed for procedural sequences).
- `extraction-lineage` — record a deterministic lineage replay with sha256 verification of every linked artifact.
- `extraction-replay` — record a full extraction replay event verifying lineage and manifest hashes.
- `extraction-lifecycle-transition` — advance a candidate through unresolved → review-required → reviewer-approved → {superseded → deprecated}.
- `extraction-integrity` — record a reviewer-led integrity scan (orphan candidates, broken lineage, invalid OCR references, missing evidence, continuity gaps, hidden mutation).
- `reviewer-override` — record a reviewer-attributed override of any extraction artifact (rejection requires cited_rule_ids).

Every command:
- requires reviewer attribution,
- is fail-closed on missing source evidence / orphan candidates / broken lineage / invalid OCR references / temporal continuity gaps / illegal candidate states / duplicate IDs / forbidden overwrite paths / hidden extraction mutation,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/semantic-extraction-runtime/` subtrees.

The semantic-extraction-runtime tree is isolated from:
- the live publication tree,
- the layer-44 publication-composition-runtime tree,
- the layer-43 visual-generation-runtime tree,
- the layer-42 visual-publication-builds tree,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads, uploads.

Nothing in this surface uses embeddings, vector databases, probabilistic semantic matching, autonomous LLM reasoning, cloud APIs, SaaS, telemetry, watchers, daemons, or background workers.


## phase 53 — governed manual semantic packaging & consumer-ready export contracts

Layer 46. Subordinate to layer 45 (governed-semantic-evidence-analysis-and-multimodal-extraction-governance).

The Knowledge OS packages SEMANTIC manual knowledge ONLY. Presentation, CSS,
breakpoints, layouts, typography, responsive behavior, mobile rendering, UI
frameworks, and visual page composition are OUT OF SCOPE and FORBIDDEN at this
layer. Consumer systems (WordPress, WooCommerce, React frontends, PDF generators,
documentation renderers) render UI; the runtime emits only presentation-neutral,
renderer-agnostic, lineage-preserving, trust-aware semantic payloads.

Mutation is performed exclusively by `tools/governed_manual_semantic_packaging_executor.py --confirm`.
Subcommands (`--kind`):

- `manual-package` — record a reviewer-authored manual package manifest (semantic_structure, lineage refs, continuity_status, package_sha256).
- `semantic-section` — record a typed semantic section (one of SECTION_KINDS) with extraction/grounding/evidence lineage and trust composition.
- `export-contract` — register a presentation-neutral export contract (raw-html-export, structured-json-export, semantic-markdown-export) bound to a package.
- `export-render` — produce the deterministic export payload defined by a contract; payload sha256 is recorded for replay.
- `packaging-continuity` — record a continuity scan over a package (procedural, warning, grounding, troubleshooting, duplicate-id, orphan-section).
- `packaging-lineage` — record a deterministic lineage replay with sha256 verification of every linked artifact.
- `packaging-replay` — record a full package replay event verifying semantic structure, package_sha256, continuity, and lineage.
- `packaging-lifecycle-transition` — advance a package through draft → review-required → reviewer-approved → export-ready → {superseded → deprecated}.
- `packaging-integrity` — record a reviewer-led integrity scan (missing lineage, unresolved grounding, orphan procedures, duplicate section ids, broken continuity, unresolved evidence, invalid contracts, hidden mutation).
- `reviewer-packaging-override` — record a reviewer-attributed override of any packaging artifact (rejection requires cited_rule_ids).

Every command:
- requires reviewer attribution,
- is fail-closed on missing lineage / unresolved grounding / orphan sections / duplicate section ids / broken continuity chains / unresolved evidence refs / invalid export contracts / forbidden overwrite paths / hidden semantic mutation,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/manual-semantic-packaging-runtime/` subtrees.

The manual-semantic-packaging-runtime tree is isolated from:
- the live publication tree,
- the layer-45 semantic-extraction-runtime tree,
- the layer-44 publication-composition-runtime tree,
- the layer-43 visual-generation-runtime tree,
- the layer-42 visual-publication-builds tree,
- frontend/theme systems and WordPress runtime,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads, uploads.

Nothing in this surface uses CSS, layouts, breakpoints, typography, responsive
logic, UI frameworks, embeddings, vector databases, autonomous LLM reasoning,
cloud APIs, SaaS, telemetry, watchers, daemons, or background workers.

## phase 54 — unified operational intake, semantic consolidation & manual runtime closure

Layer 47. Schema `unified-operational-manual-runtime-closure/1.0`.

**Operational convergence pivot.** Closes the first end-to-end
reviewer-driven manual-generation loop by wiring existing governance
(Phase 46 FS, Phase 47 transactional runtime, Phase 49 grounding,
Phase 52 extraction, Phase 53 packaging) into a single deterministic flow:

    upload → analyze → approve → refresh → semantic-bank →
    synthesize → detect-visual-support → prompt-package → export-finalize

Storage: `manual-runtime-closure/` (single isolated tree).
Dispatch kinds: `intake-analyze`, `intake-reanalyze`, `intake-approve`, `refresh-propagate`, `semantic-bank-snapshot`, `manual-synthesize`, `visual-support-detect`, `prompt-package-generate`, `export-finalize`.
Consumer boundary inherited from Phase 53 (presentation-neutral).

## phase 55 — semantic convergence, cross-evidence fusion & operational runtime cohesion

- schema: `semantic-convergence-cross-evidence-fusion/1.0`
- constitutional layer: 48
- storage tree: `operational-console/semantic-convergence-runtime/`
- 10 storage subdirs: evidence-fingerprints, fusion-clusters, canonical-entities, canonical-procedures,
  conflict-surfacings, arbitration-decisions, refresh-cohesion-records, workspace-flows,
  robustness-records, export-stabilizations.
- 9 dispatch kinds: evidence-fingerprint, fusion-cluster-form, canonical-entity-promote,
  canonical-procedure-converge, conflict-surface, arbitration-decide, refresh-cohesion-propagate,
  workspace-flow-record, export-stabilize.
- posture: deterministic fingerprints only; NO embeddings; NO vector DBs; NO probabilistic inference;
  reviewer-authoritative arbitration; lineage-preserving; transaction-safe refresh cohesion;
  consumer-boundary-enforced; presentation-neutral; writes ONLY into the layer's own runtime tree.
- this is the FIRST POST-CONSTITUTIONAL convergence layer: it wires existing systems into operational
  semantic intelligence WITHOUT expanding governance complexity.

## phase 56 — final operational closure, real-world robustness & production-ready manual delivery

- schema: `final-operational-closure-production-readiness/1.0`
- constitutional layer: 49
- storage tree: `operational-console/production-closure-runtime/`
- 9 storage subdirs: evidence-robustness-records, multilingual-normalization-tables,
  multilingual-normalization-records, export-stability-guarantees, canonical-drift-records,
  reviewer-summaries, incremental-refresh-records, readiness-audit-records, closure-path-records.
- 9 dispatch kinds: evidence-robustness-record, multilingual-normalization-table-create,
  multilingual-normalization-apply, export-stability-guarantee, canonical-drift-detect,
  reviewer-summary-publish, incremental-refresh-propagate, readiness-audit-run, closure-path-record.
- posture: production robustness over architectural growth; deterministic only;
  NO embeddings; NO vector DBs; NO probabilistic inference; NO machine translation;
  NO autonomous arbitration / convergence / publication; reviewer-authoritative;
  lineage-preserving; transaction-safe incremental refresh; no silent canonical mutation;
  presentation-neutral; writes ONLY into the layer's own runtime tree.
- this is the FINAL closure layer before true production-ready operational maturity:
  it hardens the existing constitutional substrate WITHOUT introducing new architecture.

## phase 57 — operational deployment readiness, reviewer enablement & controlled production activation

- schema: `operational-deployment-readiness-controlled-production-activation/1.0`
- constitutional layer: 50
- storage tree: `operational-console/operational-deployment-runtime/`
- 10 storage subdirs: reviewer-playbooks, recovery-playbooks, production-activations,
  activation-lifecycle-records, deployment-verifications, portfolio-summaries,
  observability-summaries, deployment-packages, dependency-manifests, consumer-payload-bundles.
- 9 dispatch kinds: reviewer-playbook-publish, recovery-playbook-publish,
  production-activation-transition, deployment-verification-run, portfolio-summary-publish,
  observability-summary-publish, deployment-package-build, dependency-manifest-publish,
  consumer-payload-bundle-publish.
- activation lifecycle: production-candidate → production-approved → production-active → superseded;
  rollback-candidate observable from any pre-superseded state. APPEND-ONLY; no overwrite semantics.
- posture: deployability + reviewer operability over architectural growth; deterministic only;
  NO embeddings; NO vector DBs; NO probabilistic inference; NO ML / LLMs / MT;
  NO autonomous activation / publication / repair; NO silent production replacement;
  NO dashboards / telemetry / deployment automation daemons; reviewer-authoritative;
  lineage-preserving; transaction-safe activation; rollback-governed; presentation-neutral;
  writes ONLY into the layer's own runtime tree.
- this is the operational activation layer that transforms the Phase 47–56 substrate
  into a deployable reviewer-operated production system.

## phase 58 — reviewer operational ergonomics, guided runtime workflows & production usability closure

- schema: `reviewer-operational-ergonomics-convergence/1.0`
- constitutional layer: 51 (CONVERGENCE — not constitutional expansion)
- storage tree: `operational-console/reviewer-operational-runtime/`
- 10 storage subdirs: guided-workflows, onboarding-sequences, deployment-checklists,
  operational-diagnostics, runtime-navigation-indexes, corpus-review-queues,
  operational-confidence-summaries, reproducibility-proofs, reviewer-session-records,
  production-handoff-records.
- 10 dispatch kinds: reviewer-guided-workflow, onboarding-sequence-publish,
  deployment-checklist-publish, operational-diagnostics-summary, runtime-navigation-index,
  corpus-review-queue, operational-confidence-summary, reproducibility-proof,
  reviewer-session-record, production-handoff-record.
- posture: reviewer operability + operational ergonomics + deployment repeatability +
  deterministic reproducibility + onboarding clarity over architectural growth;
  pointer-only operational views; deterministic only; NO embeddings; NO vector DBs;
  NO probabilistic inference; NO ML / LLMs / MT; NO autonomous agents;
  NO autonomous prioritization; NO behavior tracking; NO analytics;
  NO telemetry; NO dashboards; NO operational automation;
  NO hidden runtime mutation; reviewer-authoritative; lineage-preserving;
  presentation-neutral; writes ONLY into the layer's own runtime tree.
- this is the reviewer operational ergonomics convergence layer that makes the
  Phase 47–57 production-ready substrate easier, safer, faster, and clearer for
  human operators WITHOUT new architectural complexity.
