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
