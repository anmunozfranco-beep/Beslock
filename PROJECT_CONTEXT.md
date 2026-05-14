# PROJECT_CONTEXT.md

Operational continuity & reviewer-handoff reference. Optimized for fast session
resumption — not a historical or architectural dump.

---

## 1. Project identity

- **Project**: Beslock — reviewer-driven manual generation platform.
- **Branch strategy**:
  - `main` — protected, pinned. Current pin: `2bd456cda88315d4d9bd1b41162f19cbf535c174`.
  - `info_gen_struct` — active integration branch. All shipped work merges here.
  - Topic branches per phase / per task; deleted local + remote after merge.
- **Operational objective**:
  Reviewer-driven manual generation from multimodal evidence
  (text, images, structured assets) — produced under a fully governed,
  reproducible, locally-executable substrate.

---

## 2. Current maturity state

- **Maturity estimate**: ~99.5%.
- **Architecture**: considered complete. Constitutional substrate (Phases 1–59)
  is closed. Runtime, governance, lineage, replay, stabilization, hardening
  and corpus validation are in place.
- **Current focus**: operational UX compression and reviewer usability.
  The platform now exposes a single coherent reviewer-facing product
  on top of the existing substrate.

> The project is **NO LONGER focused on constitutional expansion**.
> Further work must reuse and integrate, not extend.

---

## 3. Core doctrinal posture

Critical invariants. Treat as non-negotiable:

- Reviewer-authoritative — no autonomous approval, ever.
- Append-only — every artifact, log, lineage entry.
- Deterministic — identical inputs produce identical outputs.
- Fail-closed — missing reviewer / missing inputs → refuse, do not infer.
- Local-first — repo-native, no SaaS, no backend.
- Replayable — every operation reconstructable from event store.
- Auditable — full lineage, full attribution, full envelopes.
- No ML / no LLM.
- No embeddings.
- No probabilistic inference.
- No telemetry, no dashboards, no analytics.
- No autonomous behavior.
- No presentation logic in runtime layers (presentation is consumer-owned).

---

## 4. Operational workflow target

Reviewer-visible workflow (the only flow the reviewer should perceive):

```
Select file → Analyze → Review → Accept → Export
```

Internally this single flow orchestrates dispatches across
Phases 52–59 (extraction, convergence, synthesis, visual support,
prompt packaging, lifecycle, export, stabilization, readiness audit,
production handoff, final attestation).

The reviewer must never be required to know phase boundaries.

---

## 5. Existing operational substrate

Brief operational summary only — deep reports live in their own SUMMARY files
and `/memories/repo/` notes.

| Phase | Role |
|-------|------|
| 52 | Extraction runtime — candidate evidence + lifecycle transitions. |
| 53 | Semantic packaging — structured packaging of extracted units. |
| 54 | Operational closure — synthesis, visual-support, prompt packages, export. |
| 55 | Semantic convergence — cross-evidence fusion, canonical consolidation, stabilization. |
| 56 | Robustness + readiness — readiness audit, real-world hardening. |
| 57 | Deployment activation — operational deployment readiness, controlled activation. |
| 58 | Reviewer ergonomics — guided runtime workflows, usability closure. |
| 59 | Hardening + validation — production hardening, corpus validation, final attestation. |

All eight phases are draft-only at the runtime layer; reviewer authority is
enforced at every dispatch.

---

## 6. Current implementation focus

**Active layer**: Phase 60 — *Unified Reviewer Operational Workbench &
Parallel Runtime Orchestration*.

This layer is **operational, not constitutional**. Implementation goals:

- Single **Analyze** button → orchestrates Phase 52/54/55 envelopes.
- Single **Accept** button → orchestrates Phase 52/54/55/56/58/59 envelopes.
- Lineage-aware **Re-analyze** flow → preserves prior, supersedes via
  `prior_workflow_id`.
- Unified semantic review surface — knowledge inventory authored by reviewer.
- Unified operational reviewer workflow — 3-pane shell, single product.
- Runtime abstraction — reviewer never sees per-phase consoles in the
  primary flow (advanced consoles available via disclosure only).
- Operational UX compression — the substrate is invisible.

Shipped façade lives at:
- [reviewer-workflow.js](wp-content/themes/beslock-custom/User%20manuals/operational-console/assets/exec/reviewer-workflow.js)
- [exec.html](wp-content/themes/beslock-custom/User%20manuals/operational-console/exec.html)
- [exec.css](wp-content/themes/beslock-custom/User%20manuals/operational-console/assets/exec/exec.css)

---

## 7. Critical restrictions

When working on Phase 60 (or any successor UX/integration layer):

**DO NOT**:

- Create new runtimes.
- Create new governance families.
- Create new replay systems.
- Create new lifecycle systems.
- Create new event stores.
- Create new constitutional layers.
- Expand the constitutional substrate unnecessarily.
- Add new dispatch handlers that duplicate existing ones.

**Priority order**:

1. Operational usability.
2. Reviewer cognition (less is more).
3. Workflow simplicity.
4. Production operability.

If a request feels like it requires a new runtime, the answer is almost
certainly: *reuse and compose what already exists*.

---

## 8. Runtime isolation posture

All integration work must remain:

- **Additive only** — never modify prior runtime semantics.
- **Overwrite-protected** — destructive overwrite is forbidden;
  enforced at the FS bridge and the executor.
- **Prior-runtime isolated** — prior phases never depend on later phases.
- **Lineage-preserving** — `prior_workflow_id` chains, never mutation.
- **Stabilization-preserving** — convergence + stabilization records
  remain the source of truth for export readiness.

Re-analyze, supersede, replay — yes.
Edit-in-place, overwrite, delete — no.

---

## 9. Reviewer UX doctrine

The reviewer must feel they are operating:

> **a single coherent operational system.**

NOT:

> 50 independent governance runtimes.

Practical implications:

- One primary surface, three reviewer actions, one knowledge-inventory card.
- Per-runtime consoles are *available* but not *primary*.
- Phase numbers do not appear in the reviewer-facing copy.
- All envelopes bundle into one downloadable artifact, executed once via
  `tools/governed_fs_executor.py`.
- Reviewer authors counts and conclusions; the platform never infers them.

---

## 10. Session restart guidance

When resuming work in a new chat session:

1. **Prioritize operational integration** over new substrate.
2. **Prioritize UX compression** over surface fragmentation.
3. **Avoid governance expansion** — no new layers, no new schemas
   unless explicitly requested and justified.
4. **Avoid unnecessary new runtimes** — reuse existing dispatch kinds.
5. **Preserve doctrinal posture** (Section 3) without exception.
6. **Preserve deterministic lineage and fail-closed behavior** —
   missing reviewer / missing inputs / already-accepted workflows
   must throw, never silently coerce.
7. **Read first**:
   - This document.
   - `/memories/repo/beslock-reviewer-ux-compression.md`
   - `/memories/repo/beslock-phase59-production-hardening-corpus-validation.md`
   - The current `info_gen_struct` HEAD log.
8. **Verify before shipping**:
   - `cd runtime-implementation && python3 -m unittest discover -s testing`
     must remain GREEN (currently 19/19).
   - `git rev-parse main` must remain pinned at
     `2bd456cda88315d4d9bd1b41162f19cbf535c174`.
9. **Ship via**: topic branch → commit → push → merge `--no-ff` into
   `info_gen_struct` → push → delete topic local + remote.

When in doubt: **compress, don't expand.**
