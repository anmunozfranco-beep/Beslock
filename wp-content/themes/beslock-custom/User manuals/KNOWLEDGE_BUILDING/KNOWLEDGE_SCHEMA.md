# KNOWLEDGE SCHEMA

Status: Active governance.
Scope: Official semantic model of the BESLOCK Product Knowledge Core.
Authority: Defines the canonical schema all `structured-knowledge/` files must conform to.
Reference implementation: `ext-images/e-orbit/structured-knowledge/`.

---

## 1. What constitutes "knowledge"

In this system, "knowledge" is any structured, addressable, and provenance-bearing assertion about a BESLOCK product. A statement that is not addressable (no stable ID), not structured (free prose only), or not provenance-bearing (no source reference) is **not** knowledge. It is editorial output.

Three required properties for every knowledge unit:
1. **Identity** — a stable ID, scoped by product slug and entity type.
2. **Structure** — typed fields conforming to one of the entity schemas in §3.
3. **Provenance** — `source_refs[]` pointing to `source-of-truth/` files, or an explicit `validation_status` of `inferred-but-unverified` or `blocked-pending-validation`.

A knowledge unit may carry editorial renderings, but its truth is defined by the structured fields, not by the rendering.

---

## 2. Document-level vs atomic knowledge

The system distinguishes two layers:

- **Document-level knowledge** — a normalized representation of an OEM document or an editorial manual. Stored in `structured-knowledge/manual.json`. Used for archival recovery, section-targeted delivery, and RAG fallback evidence.
- **Atomic knowledge** — typed semantic objects (capabilities, procedures, components, warnings, glossary terms, workflows, operational states, installation flows, UI elements, troubleshooting items). Stored in dedicated files under `structured-knowledge/`. Used for support actions, chatbot answers, comparison matrices, and structured publishing.

Atomic knowledge is the primary read surface. Document-level knowledge is the secondary read surface.

Rule: a delivery channel that reads only document-level knowledge is operating in degraded mode.

---

## 3. Knowledge entities

All entities share a common envelope:

```jsonc
{
  "id": "string",                    // stable, slug-scoped, kebab-case
  "type": "string",                  // entity type (see below)
  "product": "string",               // product slug (e.g. "e-orbit")
  "summary": "string",               // one-sentence Colombian-Spanish canonical
  "language": "es-CO",               // canonical language tag
  "validation_status": "verified | normalized | inferred-but-unverified | blocked-pending-validation | deprecated-historical",
  "channel_targets": ["web", "pdf", "support", "onboarding", "chatbot", "rag", "api"],
  "source_refs": ["source-of-truth/manuals/<file>#<anchor>"],
  "related": { "<relation>": ["<entity-id>", "..."] },
  "updated_at": "ISO-8601",
  "schema_version": "1.0"
}
```

Entity types (`type` values): `capability`, `procedure`, `component`, `ui-element`, `warning`, `operational-state`, `installation-flow`, `troubleshooting`, `glossary-term`, `workflow`, `visual-constraint`.

### 3.1 Capability (feature)

```jsonc
{
  "id": "credential-pin",
  "type": "capability",
  "product": "e-orbit",
  "summary": "Soporta acceso por código PIN.",
  "category": "access-method",
  "depends_on": ["component-keypad"],
  "operational_states": ["state-armed", "state-unlocked"],
  "ui_elements": ["ui-keypad-panel"],
  "procedures": ["register-pin", "delete-pin"],
  "constraints": { "min_pin_length": 4, "max_pin_length": 10 },
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#5"],
  "validation_status": "verified"
}
```

### 3.2 Procedure (procedural knowledge)

Procedures are the most reused unit. They drive support, chatbot, and onboarding renderings.

```jsonc
{
  "id": "register-pin",
  "type": "procedure",
  "product": "e-orbit",
  "summary": "Registra un PIN para un usuario o administrador.",
  "surface": "local-device",                  // local-device | mobile-app | web
  "menu_path": "Agregar usuario -> Agregar administrador",
  "preconditions": ["state-admin-authenticated"],
  "steps": [
    { "n": 1, "text": "Despierte el panel de la cerradura.", "ui_ref": "ui-wake-panel" },
    { "n": 2, "text": "Ingrese al menú.", "ui_ref": "ui-main-menu" },
    { "n": 3, "text": "Seleccione Agregar usuario." },
    { "n": 4, "text": "Seleccione el tipo de usuario." },
    { "n": 5, "text": "Seleccione Contraseña." },
    { "n": 6, "text": "Ingrese el PIN." },
    { "n": 7, "text": "Confirme el PIN." },
    { "n": 8, "text": "Guarde el registro." }
  ],
  "validation_checks": [
    "El acceso funciona.",
    "El usuario comprende cómo usar la credencial."
  ],
  "warnings": ["warning-shared-pin"],
  "troubleshooting": ["ts-pin-not-saved"],
  "visual_constraints": ["vc-keypad-layout"],
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#3"],
  "validation_status": "verified"
}
```

### 3.3 Component (hardware)

```jsonc
{
  "id": "component-keypad",
  "type": "component",
  "product": "e-orbit",
  "summary": "Teclado capacitivo frontal para entrada de PIN.",
  "location": "exterior-front",
  "anchor_ref": "visual-system/anchors/keypad.json",
  "interacts_with": ["ui-keypad-panel"],
  "materials": ["glass-touch"],
  "source_refs": ["source-of-truth/product-images/e-Orbit.png", "source-of-truth/manuals/e-Orbit user manual.md#1"],
  "validation_status": "verified"
}
```

### 3.4 UI element

```jsonc
{
  "id": "ui-keypad-panel",
  "type": "ui-element",
  "product": "e-orbit",
  "summary": "Panel numérico iluminado para ingreso de PIN.",
  "surface": "local-device",
  "renders_on": ["component-keypad"],
  "states": ["idle", "active", "error"],
  "labels": { "es-CO": "Teclado" },
  "source_refs": ["source-of-truth/product-images/e-Orbit.png"],
  "validation_status": "verified"
}
```

### 3.5 Warning

```jsonc
{
  "id": "warning-shared-pin",
  "type": "warning",
  "product": "e-orbit",
  "severity": "caution",            // info | caution | critical
  "summary": "No comparta el PIN administrador con usuarios estándar.",
  "scope": ["procedure:register-pin"],
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#7"],
  "validation_status": "verified"
}
```

### 3.6 Operational state

```jsonc
{
  "id": "state-armed",
  "type": "operational-state",
  "product": "e-orbit",
  "summary": "Cerradura asegurada y a la espera de credencial.",
  "indicators": ["led-blue-steady"],
  "transitions_to": ["state-unlocked", "state-error"],
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#9"],
  "validation_status": "verified"
}
```

### 3.7 Installation flow

```jsonc
{
  "id": "install-standard",
  "type": "installation-flow",
  "product": "e-orbit",
  "summary": "Instalación estándar para puerta con preparación europea.",
  "preconditions": ["door-prep-65mm"],
  "phases": [
    { "phase": "preparation", "steps": ["..."] },
    { "phase": "mounting", "steps": ["..."] },
    { "phase": "wiring", "steps": ["..."] },
    { "phase": "first-boot", "steps": ["..."] },
    { "phase": "verification", "steps": ["..."] }
  ],
  "tools_required": ["phillips-screwdriver", "drill-template"],
  "warnings": ["warning-power-polarity"],
  "source_refs": ["source-of-truth/manuals/e-Orbit installation manual.md#2"],
  "validation_status": "verified"
}
```

### 3.8 Troubleshooting

```jsonc
{
  "id": "ts-pin-not-saved",
  "type": "troubleshooting",
  "product": "e-orbit",
  "symptom": "El PIN no se guarda al finalizar el registro.",
  "likely_causes": ["timeout-during-confirmation", "duplicate-pin"],
  "diagnostic_steps": ["Reintente el registro.", "Verifique que el PIN no esté en uso."],
  "resolutions": ["Use un PIN distinto.", "Reinicie el menú y reintente."],
  "related_procedures": ["register-pin"],
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#11"],
  "validation_status": "verified"
}
```

### 3.9 Glossary term

```jsonc
{
  "id": "term-administrator",
  "type": "glossary-term",
  "product": "e-orbit",
  "canonical": "administrador",
  "language": "es-CO",
  "oem_variants": ["administrator", "admin", "master user"],
  "definition": "Usuario con permisos para gestionar credenciales y configuración.",
  "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#2"],
  "validation_status": "normalized"
}
```

### 3.10 Workflow (app/operational sequence)

```jsonc
{
  "id": "wf-mobile-pairing",
  "type": "workflow",
  "product": "e-orbit",
  "summary": "Emparejamiento del producto con la app móvil.",
  "actors": ["user", "mobile-app", "device"],
  "steps": [
    { "n": 1, "actor": "user", "text": "Abra la app." },
    { "n": 2, "actor": "mobile-app", "text": "Solicite descubrimiento Bluetooth." },
    { "n": 3, "actor": "device", "text": "Anuncie disponibilidad de emparejamiento." }
  ],
  "preconditions": ["state-pairing-mode"],
  "outcomes": ["device-bound-to-account"],
  "source_refs": ["source-of-truth/manuals/e-Orbit app manual.md#1"],
  "validation_status": "verified"
}
```

### 3.11 Visual constraint

Visual constraints bind procedural and component knowledge to the canonical PNG. They are consumed by ComfyUI orchestration.

```jsonc
{
  "id": "vc-keypad-layout",
  "type": "visual-constraint",
  "product": "e-orbit",
  "summary": "El teclado conserva su grilla 3x4 visible en la cara frontal.",
  "anchor_ref": "visual-system/anchors/keypad.json",
  "canonical_png": "source-of-truth/product-images/e-Orbit.png",
  "preserves": ["silhouette", "key-grid", "key-spacing", "label-positions"],
  "tolerances": { "position_px": 4, "rotation_deg": 1 },
  "source_refs": ["source-of-truth/product-images/e-Orbit.png"],
  "validation_status": "verified"
}
```

---

## 4. Semantic relationships

Relationships are first-class. They are stored both inline (`related[]` in the envelope) and aggregated in `structured-knowledge/semantic-relations/knowledge-graph.json`.

Allowed relations:
- `depends_on` — A requires B to function.
- `implements` — A is a concrete realization of B.
- `triggers` — A causes B.
- `transitions_to` — operational state A → state B.
- `documented_in` — A is described by document section B.
- `rendered_by` — A is visually represented by B.
- `mitigates` — A addresses warning/troubleshooting B.
- `replaces` — A supersedes B (deprecated-historical).
- `related_to` — generic, weakest relation; avoid when a stronger relation fits.

Knowledge graph entry shape:

```jsonc
{
  "edges": [
    { "from": "capability:credential-pin", "to": "procedure:register-pin", "rel": "implements" },
    { "from": "procedure:register-pin", "to": "warning:warning-shared-pin", "rel": "mitigates" },
    { "from": "procedure:register-pin", "to": "visual-constraint:vc-keypad-layout", "rel": "rendered_by" }
  ]
}
```

Rules:
- Edges are typed and directional.
- Edges may not cross product slugs.
- Edges must reference existing entity IDs; dangling edges are rejected.

---

## 5. Reusable knowledge units and granularity

The smallest reusable unit per family:

| Family            | Smallest reusable unit | Why                                                |
|-------------------|------------------------|----------------------------------------------------|
| Capability        | The whole capability   | Capabilities are atomic by definition.             |
| Procedure         | A single step          | Steps are independently citable in support flows.  |
| Installation      | A phase                | Phases compose into different installation paths.  |
| Troubleshooting   | The whole item         | Symptom-to-resolution is the atomic support unit.  |
| Warning           | The whole warning      | Warnings attach to multiple procedures.            |
| Glossary          | The whole term         | Terms are reused across all surfaces.              |
| Workflow          | A single actor-step    | Workflows recompose for different surfaces.        |
| Visual constraint | The whole constraint   | Constraints bind to specific anchor regions.       |

Granularity rule: if a unit is cited from two different surfaces with different scopes, it must be split.

---

## 6. Canonical identifiers

ID rules:
- Lowercase, kebab-case.
- Scoped within the product nucleus; product slug is implicit (carried in the envelope).
- Entity-type prefix is allowed when the same noun appears in multiple types (e.g. `state-armed` vs `ui-armed`).
- IDs are stable across reorganizations. A rename is a deliberate, lineage-recorded operation.
- IDs are unique within the product across all entity types.

Cross-references:
- Inline `related[]` keys use the relation name; values are bare IDs.
- Knowledge-graph edges use `<type>:<id>` (e.g. `procedure:register-pin`) to disambiguate.

---

## 7. Semantic normalization

Normalization is enforced at write time, not at read time.

Required normalizations:
1. Language: canonical Colombian-Spanish for `summary`, `text`, `definition`, `symptom`, `resolutions`.
2. Terminology: all terms in normalized text must resolve to either the shared terminology registry or the product-local glossary.
3. Validation status: every entity carries a status from the controlled vocabulary in §3.
4. OEM wording: preserved verbatim only in `source-of-truth/manuals/` and in glossary `oem_variants[]`.

Forbidden normalizations:
- Silently rewording an OEM claim without recording the change in the validation ledger.
- Promoting a guess to `verified`.
- Removing OEM-original wording from `source-of-truth/`.

---

## 8. Cross-channel reproducibility

A delivery channel renders from structured knowledge. Two renderings of the same entity for the same channel and the same `schema_version` must produce equivalent output (subject to channel templating).

Required for reproducibility:
- Stable IDs (§6).
- Pinned `schema_version`.
- Channel-target whitelist (`channel_targets[]`).
- Deterministic templating (channel templates do not invent fields).

A channel that needs a field not present in the schema must propose a schema change, not invent the field locally.

---

## 9. RAG and chatbot readiness

Each entity is RAG-ready when it carries:
- `id`, `type`, `product`, `summary`, `language`, `validation_status`, `channel_targets`, `source_refs`, `updated_at`, `schema_version`.

Required RAG export shape (produced by tooling, not authored by hand):

```jsonc
{
  "id": "e-orbit:procedure:register-pin",
  "product": "e-orbit",
  "type": "procedure",
  "title": "Registrar un PIN",
  "text": "<rendered procedure body in es-CO>",
  "metadata": {
    "validation_status": "verified",
    "channel_targets": ["chatbot", "rag", "support"],
    "source_refs": ["source-of-truth/manuals/e-Orbit user manual.md#3"],
    "related": { "warnings": ["warning-shared-pin"] }
  }
}
```

Chunking strategy:
- One chunk per atomic entity by default.
- Procedures may be split per step when step-level retrieval is required, with parent ID retained in metadata.
- Document-level chunks are produced from `manual.json` only as fallback evidence.

---

## 10. Schema versioning

- The schema is versioned (`schema_version`, currently `1.0`).
- Backwards-incompatible changes require a major version bump and a migration entry per nucleus in `metadata/lineage/source-lineage.json`.
- Tooling must accept entities at the declared `schema_version` and reject unknown versions.

---

## 11. Conformance

A `structured-knowledge/` file is conforming when:
1. Every entity carries the required envelope fields.
2. Every `source_refs[]` resolves to a real path under `source-of-truth/` or carries an explicit non-`verified` validation status.
3. Every `related[]` reference resolves to an existing entity in the same nucleus.
4. Every `channel_targets[]` value is from the controlled vocabulary.
5. Every `validation_status` is from the controlled vocabulary.
6. The file declares `schema_version`.

A non-conforming file may not be cited by delivery channels or RAG export.
