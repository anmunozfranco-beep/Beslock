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
