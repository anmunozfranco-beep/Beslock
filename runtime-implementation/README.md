# Runtime Implementation — Track #1

First **real executable** supervised operational runtime for the Beslock cognition ecosystem.

This is implementation, not modeling. It reads real `knowledge-core/` JSON files,
performs scored retrieval, supervised contextual assembly, continuous safety
validation, and append-only observability — all subordinate to knowledge-core
and bound by the constitutional governance layers.

## Scope

- First slice: **contextual onboarding + troubleshooting retrieval**.
- Read-only over knowledge-core. No mutations to any per-product data.
- Supervised by default. Operator approval required at declared checkpoints.
- Append-only NDJSON observability under `observability/logs/`.
- Hard exclusions enforced: no autonomous agents, no production deployment,
  no images, no PDFs, no large frontend, no perf optimization.

## Layout

```
runtime-implementation/
  runtime/                  # Python package (snake_case)
    config.py               # paths, products, slice declaration
    provenance.py           # manifest builder + content hashing
    retrieval.py            # knowledge-core loader + scored retrieval
    assembly.py             # procedure + warnings + prerequisites merge
    supervision.py          # review checkpoints + override channel
    safety.py               # continuous safety predicates
    observability.py        # append-only NDJSON channels
    flows.py                # six supervised flows
  cli.py                    # supervised CLI entrypoint
  retrieval/                # docs
  context-assembly/         # docs
  supervision/              # docs
  observability/            # logs + docs
  safety/                   # docs
  testing/                  # real test suite
```

## Run

```bash
.venv/bin/python runtime-implementation/cli.py --help
.venv/bin/python runtime-implementation/cli.py retrieve --product e-prime --query "vincular cerradura" --kind onboarding
.venv/bin/python runtime-implementation/cli.py flow onboarding --product e-prime --query "primer uso"
.venv/bin/python runtime-implementation/cli.py test
```

## Supervision posture

Every flow halts at the **pre-emission** checkpoint and waits for operator
approval (`--approve` or interactive `y/n`) before emitting a guidance package.
Demotion is the safe response to any anomaly; the runtime never elevates
confidence to compensate for missing inputs.

## Governance

This implementation is bound by the twentieth constitutional layer
`KNOWLEDGE_BUILDING/RUNTIME_IMPLEMENTATION_GOVERNANCE/` and remains subordinate
to knowledge-core and to all nineteen prior governance layers.
