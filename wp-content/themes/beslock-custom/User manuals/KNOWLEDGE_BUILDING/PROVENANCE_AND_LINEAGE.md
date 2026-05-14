# PROVENANCE AND LINEAGE

Status: Active governance.
Scope: How all knowledge and visual assets in the BESLOCK Product Knowledge Core preserve source traceability.
Authoritative storage: `ext-images/<slug>/metadata/lineage/source-lineage.json` per nucleus.
Reference implementation: `ext-images/e-orbit/metadata/lineage/source-lineage.json`.

This document defines the rules. The schema and examples below are normative.

---

## 1. Why provenance is mandatory

Every claim in the knowledge core must be answerable to four questions:

1. Where did this knowledge come from?
2. What OEM source created this?
3. What workflow generated this?
4. What transformations occurred between source and current state?

A claim that cannot answer all four questions is not knowledge. It is unverified output and must carry an explicit non-`verified` validation status (see `KNOWLEDGE_SCHEMA.md` §3).

Provenance is enforced at write time, not asserted at read time.

---

## 2. Provenance vs lineage

- **Provenance** — the immediate origin of an artifact (which OEM file, which canonical PNG, which workflow run). Answers "where did this come from?".
- **Lineage** — the full chain of transformations from origin to current state. Answers "what happened to it along the way?".

Every artifact in a nucleus carries both:
- Provenance is recorded inline on the artifact (e.g. `source_refs[]` on a knowledge entity, sidecar metadata on a generated visual).
- Lineage is aggregated in `metadata/lineage/source-lineage.json` per nucleus.

---

## 3. Lineage levels

Lineage is recorded at three independent levels. All three are mandatory.

### 3.1 File lineage

```
OEM source file → normalized derivative → structured derivative → delivery file
```

Tracks the physical file chain.

### 3.2 Semantic lineage

```
OEM source section → semantic entity (capability, procedure, ...) → delivery slice (chunk, page section)
```

Tracks the meaning chain. A single OEM section may produce multiple semantic entities; a single semantic entity may serve multiple delivery slices.

### 3.3 Visual lineage

```
canonical PNG  →  conditioning asset  →  ComfyUI workflow run  →  approved support visual  →  delivery placement
                  (or: OEM diagram)
```

Tracks the visual chain. The canonical PNG is the root; OEM diagrams may serve as secondary roots for support visuals that illustrate procedures rather than depict the product.

---

## 4. Source attribution rules

- Every artifact declares its source explicitly. No implicit inheritance from folder location.
- Source references use repository-relative paths anchored at the nucleus root.
- Source references include a sub-anchor when the source is sectioned (`<file>#<anchor>`), a page when the source is a PDF (`<file>#page=<n>`), or a region when the source is an image (`<file>#region=<x>,<y>,<w>,<h>`).
- Multiple sources are allowed; all are recorded.
- A source must exist when it is referenced; dangling references are rejected at validation time.

---

## 5. Asset ancestry

Every artifact has a typed ancestry:

| Artifact                       | Allowed parent types                                                |
|--------------------------------|---------------------------------------------------------------------|
| Normalized manual              | OEM PDF, OEM markdown, OEM spreadsheet                              |
| Structured-knowledge entity    | Normalized manual, normalized specification, canonical PNG          |
| Glossary term                  | Normalized manual, OEM source, editorial decision (with reviewer)   |
| Visual constraint              | Canonical PNG (always), optional OEM visual evidence                |
| Conditioning asset             | Canonical PNG, OEM visual evidence                                  |
| Run record                     | Workflow registry entry + canonical PNG + conditioning assets       |
| Approved support visual        | Run record (always)                                                 |
| Delivery surface chunk         | Structured-knowledge entity (preferred), normalized manual section  |

Ancestry rule: an artifact may not have a parent of an unallowed type. A "generated visual derived from another generated visual" is not an allowed chain unless the intermediate visual is explicitly an approved support visual with a complete run record.

---

## 6. Transformation tracking

Every transformation is recorded with:
- transformation type (`extract`, `normalize`, `structure`, `translate`, `condition`, `generate`, `approve`, `publish`)
- inputs (artifact IDs or paths)
- outputs (artifact IDs or paths)
- tool and version (e.g. `extract_manual.py@<git-sha>`, `comfyui@<workflow-version>`)
- parameters (deterministic-affecting only; e.g. seed, sampler, threshold)
- operator (user or CI run)
- timestamp (ISO-8601)
- result status (`success`, `partial`, `failed`)

Transformations are append-only. A correction is a new transformation, not an edit.

---

## 7. Workflow traceability

For ComfyUI runs (defined in `COMFY_GENERATION_GOVERNANCE.md` §3 and §7):

Each run record contains:
- product slug
- canonical PNG path + content hash
- workflow registry ID + version + content hash
- prompt contract (positive, negative, conditioning, resolved snippet IDs)
- seed, sampler, steps, CFG, scheduler, model name + hash
- ControlNet/IPAdapter inputs (paths + hashes)
- output paths
- approval state, reviewer, approval timestamp
- run timestamp

Run records live in `ext-images/<slug>/automation/runs/` and are indexed in `metadata/lineage/source-lineage.json`.

A run record is immutable once written. Re-running produces a new record.

---

## 8. Source confidence

Confidence is a first-class lineage attribute, not a post-hoc decoration.

- Each source reference may carry a `confidence` field (0.0–1.0).
- Confidence is composed from OCR confidence, normalization confidence, and source agreement (see `OEM_EXTRACTION_PIPELINE.md` §13).
- Aggregation rule for a derived artifact: confidence is the **minimum** of all parent confidences, unless an editorial reviewer explicitly overrides with a recorded justification.
- Confidence below the configured threshold forces `validation_status` to `inferred-but-unverified` or `blocked-pending-validation`.

Confidence is never silently averaged upward.

---

## 9. Derived-content governance

Derived content (anything produced from a source) obeys:

1. The source must exist and be referenced.
2. The transformation that produced the derived content must be recorded.
3. The derived content must declare its own validation status.
4. Generated visuals never become product truth (they are derivatives only).
5. Editorial outputs (manuals, web pages) never become primary truth (they read from structured knowledge).
6. A derived artifact may be regenerated at any time from its declared inputs and parameters.

A derived artifact that cannot be regenerated from the recorded lineage is broken and must be repaired or removed.

---

## 10. Lineage manifest schema

Per nucleus: `ext-images/<slug>/metadata/lineage/source-lineage.json`.

```jsonc
{
  "product": "e-orbit",
  "schema_version": "1.0",
  "updated_at": "2026-05-13T00:00:00Z",
  "sources": [
    {
      "id": "src:user-manual-original",
      "kind": "oem-pdf",
      "path": "source-of-truth/manuals/originals/e-Orbit user manual.pdf",
      "sha256": "…",
      "language_hint": ["es", "en"],
      "ingested_at": "…"
    },
    {
      "id": "src:canonical-png",
      "kind": "canonical-png",
      "path": "source-of-truth/product-images/e-Orbit.png",
      "sha256": "…"
    }
  ],
  "transformations": [
    {
      "id": "tx:extract-user-manual",
      "type": "extract",
      "tool": "tools/manual_ocr/extract_manual.py",
      "tool_version": "git:<sha>",
      "inputs": ["src:user-manual-original"],
      "outputs": ["art:user-manual-normalized"],
      "parameters": { "ocr_engine": "ocrmypdf+pytesseract", "languages": ["spa", "eng"] },
      "operator": "ci-run-1234",
      "timestamp": "…",
      "result": "success"
    },
    {
      "id": "tx:structure-procedures",
      "type": "structure",
      "tool": "phase2/structure-procedures",
      "tool_version": "…",
      "inputs": ["art:user-manual-normalized"],
      "outputs": ["entity:procedure:register-pin", "entity:procedure:add-administrator"],
      "operator": "andres",
      "timestamp": "…",
      "result": "success"
    }
  ],
  "artifacts": [
    {
      "id": "art:user-manual-normalized",
      "kind": "normalized-manual",
      "path": "source-of-truth/manuals/e-Orbit user manual.md",
      "parents": ["src:user-manual-original"],
      "produced_by": "tx:extract-user-manual",
      "validation_status": "normalized",
      "confidence": 0.92
    },
    {
      "id": "entity:procedure:register-pin",
      "kind": "knowledge-entity",
      "path": "structured-knowledge/procedures/procedure-catalog.json#register-pin",
      "parents": ["art:user-manual-normalized"],
      "produced_by": "tx:structure-procedures",
      "validation_status": "verified",
      "confidence": 0.95
    }
  ],
  "edges": [
    { "from": "src:user-manual-original", "to": "art:user-manual-normalized", "rel": "produces" },
    { "from": "art:user-manual-normalized", "to": "entity:procedure:register-pin", "rel": "produces" }
  ]
}
```

Rules:
- IDs are unique within the manifest. Cross-manifest references are forbidden (provenance does not cross product boundaries).
- `transformations[]` and `artifacts[]` are append-only.
- `edges[]` is derivable from `parents[]` and `produced_by`; it is denormalized for fast graph queries.

---

## 11. Lineage examples

### 11.1 Text extraction

```
src:user-manual-original (OEM PDF)
   └─ tx:extract-user-manual  (extract_manual.py)
      └─ art:user-manual-normalized  (source-of-truth/manuals/e-Orbit user manual.md)
         └─ tx:structure-procedures  (Phase 2)
            └─ entity:procedure:register-pin  (structured-knowledge/procedures/...)
               └─ tx:render-web  (publishing)
                  └─ deliverable:web/procedures/register-pin.html
```

### 11.2 Visual generation (ComfyUI)

```
src:canonical-png  (source-of-truth/product-images/e-Orbit.png)
   ├─ tx:derive-conditioning-keypad  (segmentation + depth)
   │  └─ art:conditioning:keypad-depth  (visual-system/conditioning/keypad-depth.png)
   └─ tx:run-support-visual  (ComfyUI; workflow wf-keypad-closeup@1.2)
      └─ run:2026-05-13T10:15:00Z-abc123
         └─ art:support-visual:keypad-closeup-v1  (visual-system/qa/selected-assets/keypad-closeup.png)
            └─ tx:publish-web
               └─ deliverable:web/components/keypad.html
```

### 11.3 Semantic normalization

```
art:user-manual-normalized
   └─ tx:normalize-terminology  (Colombian-Spanish)
      ├─ art:user-manual-es-CO  (normalized.md)
      └─ entity:glossary-term:term-administrator  (structured-knowledge/glossary.json#term-administrator)
         (oem_variants: ["administrator", "admin", "master user"])
```

### 11.4 Comfy outputs (provenance sidecar)

Every approved support visual carries a sidecar JSON next to the image:

```jsonc
// visual-system/qa/selected-assets/keypad-closeup.png.provenance.json
{
  "artifact_id": "art:support-visual:keypad-closeup-v1",
  "product": "e-orbit",
  "run_record": "automation/runs/2026-05-13T10-15-00Z-abc123.json",
  "workflow": { "id": "wf-keypad-closeup", "version": "1.2", "sha256": "…" },
  "canonical_png": { "path": "source-of-truth/product-images/e-Orbit.png", "sha256": "…" },
  "conditioning": [
    { "path": "visual-system/conditioning/keypad-depth.png", "sha256": "…" }
  ],
  "prompt_contract": {
    "positive": "…",
    "negative": "…",
    "snippets": ["studio-lighting/v3", "no-text-guard/v1"]
  },
  "seed": 1234567890,
  "sampler": "dpmpp_2m_sde",
  "steps": 28,
  "cfg": 5.5,
  "scheduler": "karras",
  "model": { "name": "…", "sha256": "…" },
  "approval": { "state": "approved", "reviewer": "andres", "timestamp": "…" },
  "delivery_targets": ["web", "support"]
}
```

The sidecar is the visual analog of `source_refs[]` on a knowledge entity.

---

## 12. Cross-channel lineage queries

The system must support these queries from the lineage manifest alone:

- "Where did this delivery chunk come from?" → traverse `parents[]` from the deliverable to the OEM source.
- "What entities depend on this OEM source?" → forward-traverse `edges[]` from the source.
- "Which support visuals reference this conditioning asset?" → forward-traverse from the conditioning artifact.
- "If this OEM source is replaced, what must be re-derived?" → forward-traversal yields the impact set.
- "Which entities are below confidence threshold?" → filter `artifacts[]` by `confidence`.

Tooling that cannot answer these queries from the manifest alone is incomplete.

---

## 13. Replacement and invalidation

When an OEM source is replaced (new revision):
1. Append a new `sources[]` entry with a new ID and the new SHA-256.
2. Mark the old source as `superseded_by: <new-id>` (the old entry is retained, not deleted).
3. Forward-traverse to identify all derived artifacts.
4. Mark each derived artifact as `validation_status: blocked-pending-validation` until re-derivation completes.
5. Record the re-derivation transformations as new entries.

When the canonical PNG is replaced, the same procedure applies, plus:
- Every visual constraint is re-validated against the new PNG.
- Every conditioning asset is regenerated.
- Every approved support visual is marked `blocked-pending-validation` until re-approved through new ComfyUI runs.

Silent replacement of the canonical PNG is forbidden.

---

## 14. Conformance

A nucleus is provenance-conforming when:
1. `metadata/lineage/source-lineage.json` exists and validates against the schema in §10.
2. Every artifact in the nucleus appears either as a source or as an artifact in the manifest.
3. Every transformation that produced an artifact in the manifest is recorded.
4. No artifact has a dangling parent reference.
5. Every approved support visual has a sidecar provenance JSON matching §11.4.
6. Every knowledge entity's `source_refs[]` resolves to a manifest entry.

A non-conforming nucleus may not be cited by delivery channels or by RAG export, regardless of how mature its content appears.

---

## 15. Authority

This document defines the lineage contract. `KNOWLEDGE_SCHEMA.md` defines what entities look like. `OEM_EXTRACTION_PIPELINE.md` defines how raw sources become artifacts. `COMFY_GENERATION_GOVERNANCE.md` defines how visuals are produced. This document defines how all of those connect.
