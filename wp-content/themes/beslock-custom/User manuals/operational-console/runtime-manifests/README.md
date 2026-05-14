# Runtime manifest event stores (phase 46, layer 39)

Eight append-only event stores populated exclusively by the CLI executor (`tools/governed_fs_executor.py`). The browser surface reads these via `fetch`; it never writes them.

- `intake-events/_event-store.json`
- `routing-events/_event-store.json`
- `mutation-events/_event-store.json`
- `refresh-events/_event-store.json`
- `lineage-events/_event-store.json`
- `rollback-events/_event-store.json`
- `publication-events/_event-store.json`
- `audit-events/_event-store.json`
