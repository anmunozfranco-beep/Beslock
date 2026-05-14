#!/usr/bin/env python3
"""Phase 8 — Knowledge Center consolidation.

Promotes the existing per-product semantic nuclei into a coherent, queryable
knowledge-center architecture under `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/`.

NON-DESTRUCTIVE:
  * No semantic artifact under `ext-images/<slug>/knowledge-core/` is modified.
  * No governance file under `visual-system/_governance/` is modified.
  * No Comfy / orchestration / visual-generation file is touched.
  * No image is generated.

This phase produces:
  * the knowledge-center constitutional documents
  * the global ontology, relationship-graph, maturity-model, retrieval-strategy,
    cross-product map, domain-boundaries, semantic-lineage, architecture, and
    future-extensibility documents
  * 10 JSON reports
  * an inventory grounded in real per-product file counts
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
KC = KB / "KNOWLEDGE_CENTER"
EXT = USER_MANUALS / "ext-images"
GOV_REPO = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "knowledge-center/1.0"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

SEMANTIC_DOMAINS = [
    "entities",
    "procedures",
    "workflows",
    "warnings",
    "terminology",
    "capabilities",
    "specifications",
    "troubleshooting",
    "procedural-semantics",
    "visual-intent",
    "visual-risk",
    "publication-intent",
    "component-visibility",
    "provenance",
]

# ---------------------------------------------------------------------------
# Inventory: count real files under each product / domain.
# ---------------------------------------------------------------------------
def inventory() -> dict:
    out: dict = {"products": {}, "totals": {d: 0 for d in SEMANTIC_DOMAINS}}
    for p in PRODUCTS:
        d_counts: dict = {}
        for d in SEMANTIC_DOMAINS:
            base = EXT / p / "knowledge-core" / d
            n = sum(1 for f in base.rglob("*") if f.is_file()) if base.exists() else 0
            d_counts[d] = n
            out["totals"][d] += n
        out["products"][p] = d_counts
    return out


def list_files(rel: str) -> list[str]:
    base = USER_MANUALS / rel
    if not base.exists():
        return []
    return sorted(
        f.relative_to(USER_MANUALS).as_posix()
        for f in base.rglob("*")
        if f.is_file() and not f.name.startswith(".")
    )


# ---------------------------------------------------------------------------
# Ontology: shared semantic primitives across products.
# ---------------------------------------------------------------------------
SHARED_ENTITY_CONCEPTS = [
    {"id": "entity.lock-body",         "label": "lock body",            "scope": "shared", "definition": "Outer hardware shell mounted on the door."},
    {"id": "entity.keypad",            "label": "keypad",               "scope": "shared", "definition": "Touch or capacitive input surface accepting numeric codes."},
    {"id": "entity.fingerprint-sensor","label": "fingerprint sensor",   "scope": "shared", "definition": "Capacitive biometric sensor for enrolment and verification."},
    {"id": "entity.handle",            "label": "handle",               "scope": "shared", "definition": "Lever or knob actuating the latch."},
    {"id": "entity.deadbolt",          "label": "deadbolt",             "scope": "shared", "definition": "Sliding bolt mechanism actuated independently of the latch."},
    {"id": "entity.latch",             "label": "latch",                "scope": "shared", "definition": "Spring-loaded retracting tongue for door retention."},
    {"id": "entity.battery-bay",       "label": "battery bay",          "scope": "shared", "definition": "Compartment housing the AA cells (interior side)."},
    {"id": "entity.emergency-port",    "label": "emergency power port", "scope": "shared", "definition": "External contact point for emergency battery jump."},
    {"id": "entity.indicator-led",     "label": "indicator LED",        "scope": "shared", "definition": "Status indicator (colour and pattern carry meaning)."},
    {"id": "entity.mortise",           "label": "mortise mechanism",    "scope": "shared", "definition": "Through-door mechanism connecting interior and exterior."},
    {"id": "entity.app",               "label": "companion app",        "scope": "shared", "definition": "Mobile companion application for pairing and management."},
]

SHARED_PROCEDURE_CONCEPTS = [
    {"id": "procedure.pairing-app",        "label": "Pair lock with app"},
    {"id": "procedure.enrol-fingerprint",  "label": "Enrol fingerprint"},
    {"id": "procedure.add-pin-code",       "label": "Add PIN code"},
    {"id": "procedure.remove-user",        "label": "Remove user"},
    {"id": "procedure.factory-reset",      "label": "Factory reset"},
    {"id": "procedure.battery-replacement","label": "Replace batteries"},
    {"id": "procedure.emergency-power",    "label": "Apply emergency power"},
    {"id": "procedure.unlock-mechanical",  "label": "Unlock with mechanical key"},
    {"id": "procedure.unlock-pin",         "label": "Unlock with PIN"},
    {"id": "procedure.unlock-fingerprint", "label": "Unlock with fingerprint"},
    {"id": "procedure.firmware-update",    "label": "Firmware update"},
]

SHARED_WARNING_CONCEPTS = [
    {"id": "warning.low-battery",            "label": "Low-battery warning"},
    {"id": "warning.lockout-after-attempts", "label": "Temporary lockout after failed attempts"},
    {"id": "warning.tamper-alert",           "label": "Tamper alert"},
    {"id": "warning.factory-reset-data-loss","label": "Factory reset clears all users"},
]

SHARED_CAPABILITY_CONCEPTS = [
    {"id": "capability.pin-unlock",         "label": "PIN unlock"},
    {"id": "capability.fingerprint-unlock", "label": "Fingerprint unlock"},
    {"id": "capability.app-unlock",         "label": "App unlock"},
    {"id": "capability.mechanical-key",     "label": "Mechanical key fallback"},
    {"id": "capability.emergency-power",    "label": "Emergency external power"},
    {"id": "capability.audit-log",          "label": "Access audit log"},
    {"id": "capability.firmware-update",    "label": "Firmware update"},
]

SHARED_VISUAL_INTENTS = [
    {"id": "visual-intent.hero",                "label": "Hero identification image"},
    {"id": "visual-intent.installation",        "label": "Installation diagram"},
    {"id": "visual-intent.exploded-anatomy",    "label": "Exploded anatomy"},
    {"id": "visual-intent.battery-replacement", "label": "Battery replacement step"},
    {"id": "visual-intent.fingerprint-enrol",   "label": "Fingerprint enrolment step"},
    {"id": "visual-intent.app-pairing",         "label": "App pairing context"},
    {"id": "visual-intent.factory-reset",       "label": "Factory reset sequence"},
    {"id": "visual-intent.emergency-power",     "label": "Emergency power application"},
]

PUBLICATION_CHANNELS = [
    "web", "pdf", "support", "onboarding", "chatbot", "rag", "api",
]

MATURITY_TIERS = [
    {"tier": "verified",        "definition": "Cross-checked against OEM documentation and accepted by reviewer."},
    {"tier": "canonical",       "definition": "Promoted into the canonical knowledge core; authoritative for downstream consumers."},
    {"tier": "ocr-derived",     "definition": "Extracted from OCR of OEM manuals; awaits semantic reconciliation."},
    {"tier": "inferred",        "definition": "Derived by semantic interpretation; supported by multiple evidences but not OEM-confirmed."},
    {"tier": "low-confidence",  "definition": "Single-source or weakly evidenced; flagged for review."},
    {"tier": "deprecated",      "definition": "Superseded by a newer artifact; retained for lineage only."},
    {"tier": "unresolved",      "definition": "Known gap; tracked in the gaps register pending evidence."},
    {"tier": "transitional",    "definition": "Migration in progress between two schema versions or two storage layouts."},
]

DOMAIN_BOUNDARIES = [
    {"domain": "source-of-truth",         "owner": "ext-images/<slug>/source-of-truth/",                       "scope": "OEM PDFs, OEM manuals, OEM product PNGs.", "boundary": "Editorial content. Read-only outside ingest."},
    {"domain": "evidence",                "owner": "ext-images/<slug>/source-of-truth/manuals/, generated_manuals/<slug>/", "scope": "OCR text, page renders, raw extracted text.", "boundary": "Append-only. Never edited in place."},
    {"domain": "semantic-interpretation", "owner": "ext-images/<slug>/knowledge-core/{entities,procedures,workflows,warnings,terminology,capabilities,specifications,troubleshooting}/", "scope": "Structured semantic interpretation of evidence.", "boundary": "Carries provenance pointers back to evidence."},
    {"domain": "canonical-knowledge",     "owner": "ext-images/<slug>/knowledge-core/", "scope": "Promoted, reviewed, indexed semantic artifacts.", "boundary": "Only canonical artifacts may be served downstream."},
    {"domain": "visual-semantics",        "owner": "ext-images/<slug>/knowledge-core/{visual-intent,visual-risk,component-visibility,publication-intent,procedural-semantics}/", "scope": "Semantic descriptors that condition future visual generation.", "boundary": "Authored from canonical knowledge; never invented at the visual layer."},
    {"domain": "publication-semantics",   "owner": "ext-images/<slug>/knowledge-core/publication-intent/", "scope": "Channel targets, formats, alt-text contracts.", "boundary": "Publication-specific concerns live here, not in entities."},
    {"domain": "governance",              "owner": "visual-system/_governance/ + KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/", "scope": "Policy and doctrine.", "boundary": "Governance never stores product knowledge."},
    {"domain": "orchestration",           "owner": "tools/visual_generation.py + tools/comfy/ + ext-images/<slug>/automation/", "scope": "Execution: workflows, runs, manifests.", "boundary": "Reads canonical and visual semantics; writes only run records."},
]


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------
def doc_architecture() -> str:
    return f"""# Beslock Knowledge Center — architecture

_Schema: `{SCHEMA}` · canonical architecture document · generated {NOW}._

## What this repository is

Beslock is **a multimodal product knowledge center**.

It is not a manual generator. It is not an image-generation pipeline. It is not
a prompt repository. It is not a marketing site. It is a structured, queryable,
provenance-bound description of a real family of products, expressed as
machine-readable semantic artifacts that any future surface (web, PDF, support,
onboarding, chatbot, RAG, API, AR, voice, video) can consume.

Visual generation is a future emergent capability of this knowledge center, not
its purpose. The visual constitution at `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`
governs how that emergent capability is allowed to draw on the knowledge core.

## Knowledge-first principles

1. **Knowledge before delivery.** Every surface (web page, PDF, chatbot
   answer, generated image) descends from canonical knowledge. No surface
   originates knowledge.
2. **Provenance everywhere.** Every semantic artifact carries pointers back
   to the OEM evidence that justifies it.
3. **Schema before content.** New knowledge enters via a typed schema, not a
   freeform document.
4. **Federation over duplication.** Per-product knowledge stays in the
   product nucleus; cross-product intelligence references it, never copies it.
5. **Maturity is explicit.** Every artifact is classified (verified,
   canonical, ocr-derived, inferred, low-confidence, deprecated, unresolved,
   transitional). Downstream consumers may filter by tier.
6. **Boundaries are enforced.** Source-of-truth, evidence, semantic
   interpretation, canonical knowledge, visual semantics, publication
   semantics, governance and orchestration are separate domains with
   separate owners.
7. **Retrieval is a first-class output.** The knowledge core is designed to
   be queried — by humans, by chatbots, by RAG, by future agents.

## Semantic layering

| Layer | Location pattern | Role |
|---|---|---|
| L0 — OEM evidence | `ext-images/<slug>/source-of-truth/`, `generated_manuals/<slug>/` | Editorial / append-only OEM artifacts. |
| L1 — Semantic interpretation | `ext-images/<slug>/knowledge-core/{{entities,procedures,workflows,warnings,terminology,capabilities,specifications,troubleshooting}}/` | Typed extraction of L0. |
| L2 — Canonical knowledge | promoted artifacts within L1 with `maturity ∈ {{verified, canonical}}` | Single source consumed by downstream surfaces. |
| L3 — Visual / publication semantics | `ext-images/<slug>/knowledge-core/{{visual-intent,visual-risk,component-visibility,publication-intent,procedural-semantics}}/` | Conditioning for delivery surfaces. |
| L4 — Cross-product intelligence | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/cross-product-semantic-map/` | Shared concepts and platform-wide references. |
| L5 — Constitutional layer | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/` (this folder) and `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` | Doctrine, ontology, boundaries, lineage rules. |

## Subordination rule

All present and future systems — websites, PDFs, chatbots, troubleshooting
assistants, onboarding flows, semantic search, contextual publication, visual
assistance, future Comfy orchestration — are **subordinate to the knowledge
core**. They consume it; they may not redefine it.

A surface that wants knowledge it cannot find may request it. It may not
invent it.
"""


def doc_ontology(inv: dict) -> str:
    lines = [
        f"# Global knowledge ontology",
        "",
        f"_Schema: `{SCHEMA}` · canonical ontology layer · generated {NOW}._",
        "",
        "## Purpose",
        "",
        "Define the shared semantic primitives that span the Beslock product line. Per-product knowledge nuclei use these shared concepts as their vocabulary; product-specific concepts extend them, they do not replace them.",
        "",
        "## Shared entity concepts",
        "",
        "| ID | Label | Definition |",
        "|---|---|---|",
    ]
    for e in SHARED_ENTITY_CONCEPTS:
        lines.append(f"| `{e['id']}` | {e['label']} | {e['definition']} |")
    lines += ["", "## Shared procedure concepts", "", "| ID | Label |", "|---|---|"]
    for p in SHARED_PROCEDURE_CONCEPTS:
        lines.append(f"| `{p['id']}` | {p['label']} |")
    lines += ["", "## Shared warning concepts", "", "| ID | Label |", "|---|---|"]
    for w in SHARED_WARNING_CONCEPTS:
        lines.append(f"| `{w['id']}` | {w['label']} |")
    lines += ["", "## Shared capability concepts", "", "| ID | Label |", "|---|---|"]
    for c in SHARED_CAPABILITY_CONCEPTS:
        lines.append(f"| `{c['id']}` | {c['label']} |")
    lines += ["", "## Shared visual-intent concepts", "", "| ID | Label |", "|---|---|"]
    for v in SHARED_VISUAL_INTENTS:
        lines.append(f"| `{v['id']}` | {v['label']} |")
    lines += [
        "",
        "## Inheritance rule",
        "",
        "1. Per-product nuclei reference shared concept IDs verbatim.",
        "2. A product-specific extension adds a sub-id, e.g. `entity.keypad.e-touch.capacitive-grid-3x4`.",
        "3. Shared concepts are immutable; their IDs are stable across products and versions.",
        "4. Adding a shared concept requires a new entry in this ontology and a new entry in the relevant per-product schema.",
        "",
        "## Reusable semantic primitives",
        "",
        "- **Identifier**: stable, lowercase, dot-separated, no spaces.",
        "- **Provenance pointer**: `{source: <oem-evidence-id>, span: <page-and-region>, extracted_at: <iso-timestamp>}`.",
        "- **Maturity tier**: one of the eight values defined in the maturity model.",
        "- **Locale tag**: defaults to `es-CO`; localized variants append the BCP-47 tag.",
        "- **Channel target**: zero or more values from the publication-channel registry.",
        "",
        "## Inventory snapshot",
        "",
        "Per-product file counts in each semantic domain (real, observed at generation time):",
        "",
        "| Product | " + " | ".join(SEMANTIC_DOMAINS) + " |",
        "|---|" + "|".join(["---:"] * len(SEMANTIC_DOMAINS)) + "|",
    ]
    for p in PRODUCTS:
        row = [p] + [str(inv["products"][p][d]) for d in SEMANTIC_DOMAINS]
        lines.append("| " + " | ".join(row) + " |")
    totals = ["**totals**"] + [f"**{inv['totals'][d]}**" for d in SEMANTIC_DOMAINS]
    lines.append("| " + " | ".join(totals) + " |")
    return "\n".join(lines) + "\n"


def doc_graph() -> str:
    return f"""# Knowledge relationship graph

_Schema: `{SCHEMA}` · canonical relationship-graph specification · generated {NOW}._

## Purpose

Express explicit, machine-readable relationships between products, entities,
procedures, components, operational flows, warnings, visual-support
requirements and troubleshooting dependencies. The intent is a product
intelligence graph that downstream systems (chatbot, RAG, troubleshooting
assistant, onboarding) can traverse.

## Node types

- `product` — a single Beslock product (e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch).
- `entity` — a hardware component or named conceptual object.
- `procedure` — a user-facing task expressed as ordered steps.
- `workflow` — a longer multi-procedure flow (installation, onboarding, recovery).
- `warning` — a hazard, caution or operational caveat.
- `capability` — an externally visible feature.
- `specification` — a measurable property.
- `terminology-entry` — a canonical term.
- `visual-intent` — a delivery-surface visual descriptor.
- `procedural-semantics` — semantic annotation of one procedure step.
- `publication-target` — `{{channel, format}}` pair.
- `oem-evidence` — a span of an OEM document.

## Edge types

- `product.has-entity` (product → entity)
- `product.has-capability` (product → capability)
- `product.has-procedure` (product → procedure)
- `procedure.composes` (workflow → procedure)
- `procedure.touches-entity` (procedure → entity)
- `procedure.requires-capability` (procedure → capability)
- `procedure.warns` (procedure → warning)
- `procedure.illustrated-by` (procedure → visual-intent)
- `procedure.troubleshoots` (procedure → procedure)
- `entity.contains-entity` (entity → entity)
- `visual-intent.depicts-entity` (visual-intent → entity)
- `visual-intent.targets` (visual-intent → publication-target)
- `artifact.derived-from` (any node → oem-evidence)

## Storage layout

Relationship records live next to the artifacts they describe:

- per-product edges: `ext-images/<slug>/knowledge-core/semantic/relationships/`
- cross-product edges: `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/cross-product-edges.json`
- shared-concept membership: `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`

## Traversal contracts

1. **Identification query**: given a product, return its capabilities,
   procedures, warnings and the visual intents that depict it.
2. **Procedure query**: given a procedure, return the workflow it composes,
   the entities it touches, the warnings it triggers, the visual intents that
   illustrate it and the OEM evidence that justifies it.
3. **Troubleshooting query**: given a symptom, return the candidate
   procedures, the entities they touch, and the publication targets that
   explain them.
4. **Cross-product query**: given a shared concept, return every product that
   instantiates it and every per-product specialisation.

## Acceptance criteria

- Every edge carries a maturity tier.
- Every edge carries a provenance pointer back to OEM evidence (or to the
  semantic interpretation that derived it).
- No edge crosses domain boundaries silently — visual semantics may reference
  canonical knowledge, but canonical knowledge may not depend on visual
  semantics.
"""


def doc_maturity() -> str:
    rows = "\n".join(f"| `{t['tier']}` | {t['definition']} |" for t in MATURITY_TIERS)
    return f"""# Knowledge maturity model

_Schema: `{SCHEMA}` · canonical maturity classification · generated {NOW}._

## Tiers

| Tier | Definition |
|---|---|
{rows}

## Required field

Every semantic artifact under `ext-images/<slug>/knowledge-core/` MUST carry a
`maturity` field with one of the eight values above. Artifacts without a
`maturity` field are treated as `unresolved` until backfilled.

## Promotion path

```
ocr-derived  ──► inferred  ──► canonical  ──► verified
                  │                              │
                  └─► low-confidence ◄───────────┘
                         │
                         └─► deprecated
```

- `transitional` is orthogonal: it indicates an artifact in motion between two
  schema versions or two storage layouts.
- `unresolved` is the entry-point for a known gap that has no artifact yet.

## Downstream filtering

- Chatbot / RAG: serve `verified` and `canonical` only.
- Troubleshooting assistants: may include `inferred` with a confidence label.
- Onboarding surfaces: serve `verified` and `canonical` only.
- Web / PDF: serve `canonical` and above.
- API consumers: receive the maturity tier and decide locally.

## Audit

A weekly scan emits the maturity distribution per product into
`_repository-governance/reports/knowledge-center/maturity-snapshot.json` (the
report file is not generated by this phase; the contract is declared here).
"""


def doc_retrieval() -> str:
    return f"""# Retrieval and query readiness

_Schema: `{SCHEMA}` · retrieval strategy · generated {NOW}._

## Purpose

Prepare the knowledge core for chatbot retrieval, RAG, semantic querying,
troubleshooting lookup, onboarding retrieval and contextual publication.
This document defines the indexing strategy and the semantic identifiers
downstream systems will use; it does not implement the index.

## Identifier policy

- Per-product artifacts use the path-derived ID:
  `<slug>/<domain>/<artifact-name-without-extension>`.
  Example: `e-orbit/procedural-semantics/semantic-pin-unlock`.
- Cross-product shared concepts use the ontology IDs (e.g.
  `procedure.factory-reset`).
- Workflow runs use the run-record ID emitted by the orchestrator.

## Indexing strategy

| Index | Source | Consumers |
|---|---|---|
| `entities.idx`              | `ext-images/<slug>/knowledge-core/entities/`             | identification queries, AR overlays |
| `procedures.idx`            | `ext-images/<slug>/knowledge-core/procedural-semantics/` | chatbot, troubleshooting, onboarding |
| `warnings.idx`              | `ext-images/<slug>/knowledge-core/warnings/`             | chatbot safety filter, support |
| `terminology.idx`           | `ext-images/<slug>/knowledge-core/terminology/`          | search expansion, multilingual lookup |
| `capabilities.idx`          | `ext-images/<slug>/knowledge-core/capabilities/`         | catalogue, comparison |
| `troubleshooting.idx`       | `ext-images/<slug>/knowledge-core/troubleshooting/`      | troubleshooting assistant |
| `visual-intent.idx`         | `ext-images/<slug>/knowledge-core/visual-intent/`        | visual assistance, RAG image cards |
| `publication-intent.idx`    | `ext-images/<slug>/knowledge-core/publication-intent/`   | per-channel routing |
| `cross-concept.idx`         | shared ontology + per-product membership                 | cross-product queries |

## Retrieval paths

1. **Direct**: ID → artifact.
2. **Concept**: shared concept ID → membership map → per-product artifacts.
3. **Procedure**: procedure ID → composing workflow + touched entities + warnings + visual intents.
4. **Symptom**: free-text symptom → troubleshooting matches → procedures.
5. **Visual**: visual-intent ID → procedural-semantics + component-visibility + visual-risk.

## Provenance-aware retrieval

Every served artifact MUST carry:

- `id`
- `maturity`
- `provenance` (OEM evidence id + span)
- `last_updated`
- `channel_targets` (when applicable)

Consumers MAY refuse to render artifacts whose `maturity` is below their
threshold. They MUST surface the provenance.

## Future contracts

- Embeddings storage location and embedding-model identity will be declared
  in a future `embeddings/` sub-document; not in scope here.
- Multilingual variants will be addressed by appending a BCP-47 tag to
  artifact IDs; the core ID remains stable.
"""


def doc_cross_product(inv: dict) -> str:
    # Compute coverage: products that have any artifact in each domain.
    coverage = {}
    for d in SEMANTIC_DOMAINS:
        coverage[d] = [p for p in PRODUCTS if inv["products"][p][d] > 0]
    rows = "\n".join(
        f"| {d} | {len(coverage[d])} / {len(PRODUCTS)} | {', '.join(coverage[d]) or '—'} |"
        for d in SEMANTIC_DOMAINS
    )
    return f"""# Cross-product semantic map

_Schema: `{SCHEMA}` · cross-product intelligence · generated {NOW}._

## Purpose

Identify shared hardware concepts, shared workflows, shared warnings, shared
terminology, shared operational semantics and shared troubleshooting concepts
across the six Beslock products. The goal is platform-level intelligence
without flattening per-product nuclei.

## Coverage by semantic domain

| Domain | Coverage | Products with at least one artifact |
|---|---:|---|
{rows}

## Shared-concept membership pattern

For every shared concept defined in the ontology, the cross-product map
declares which products instantiate it and where the per-product artifact
lives:

```json
{{
  "concept_id": "procedure.factory-reset",
  "members": [
    {{"product": "e-orbit", "artifact": "ext-images/e-orbit/knowledge-core/procedural-semantics/semantic-factory-reset.json"}},
    {{"product": "e-flex",  "artifact": "ext-images/e-flex/knowledge-core/procedural-semantics/semantic-factory-reset.json"}}
  ]
}}
```

The membership map itself lives at
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`
once the per-product artifacts are tagged with their concept IDs (Phase 8 does
not retroactively tag artifacts; it specifies the contract).

## Shared workflow patterns

The following workflows recur across multiple products and SHOULD be modelled
as shared concepts in the knowledge graph:

- Initial pairing with the companion app.
- First-user enrolment (PIN, fingerprint).
- Battery replacement.
- Emergency power application.
- Factory reset.
- Firmware update.

## Shared warning patterns

- Low-battery behaviour.
- Lockout after consecutive failed attempts.
- Tamper alert.
- Data loss on factory reset.

## Shared terminology

- The canonical locale is Colombian Spanish (`es-CO`).
- Term collisions across products are resolved by promoting the term to the
  shared terminology vocabulary; per-product synonyms are preserved with a
  pointer to the canonical term.

## Cross-product queries

The cross-product map enables queries such as:

- "Which products support fingerprint enrolment?"
- "What is the factory-reset procedure across the line?"
- "Which products share the same low-battery warning behaviour?"
- "Which procedures touch the deadbolt across the line?"
"""


def doc_boundaries() -> str:
    rows = "\n".join(
        f"| `{b['domain']}` | {b['owner']} | {b['scope']} | {b['boundary']} |"
        for b in DOMAIN_BOUNDARIES
    )
    return f"""# Knowledge domain boundaries

_Schema: `{SCHEMA}` · domain-boundary specification · generated {NOW}._

## Purpose

Formalise the distinction between source-of-truth, evidence, semantic
interpretation, canonical knowledge, governance, orchestration, visual
semantics and publication semantics. The boundaries below are the platform
contract; they prevent knowledge drift and semantic overlap.

## Boundaries

| Domain | Owner | Scope | Boundary |
|---|---|---|---|
{rows}

## Cross-boundary rules

1. A semantic interpretation MAY reference its evidence; it MUST NOT modify it.
2. Canonical knowledge MAY reference semantic interpretations; new fields enter
   only by promotion, not by editing in place.
3. Visual semantics MAY consume canonical knowledge; they MUST NOT invent new
   product attributes.
4. Publication semantics MAY constrain how canonical knowledge is delivered;
   they MUST NOT redefine it.
5. Governance MUST NOT contain product knowledge.
6. Orchestration MUST NOT alter governance, semantics, or canonical knowledge;
   it writes only run records.

## Anti-patterns (out of policy)

- A new entity that exists only inside a visual-intent file.
- A warning whose only source is a prompt.
- A procedure whose only evidence is a generated image.
- A canonical entry edited directly without a maturity-tier promotion.
- A governance document containing per-product specifications.
"""


def doc_lineage() -> str:
    return f"""# Semantic lineage

_Schema: `{SCHEMA}` · lineage specification · generated {NOW}._

## Lineage chain

```
OEM source (PDF / OEM image / OEM brief)
        │
        ▼
OCR / extraction evidence
   (generated_manuals/<slug>/, ext-images/<slug>/source-of-truth/)
        │
        ▼
Semantic entities / procedures / warnings / terminology / capabilities
   (ext-images/<slug>/knowledge-core/{{entities,procedures,workflows,
                                       warnings,terminology,capabilities,
                                       specifications,troubleshooting}}/)
        │
        ▼
Canonical knowledge (maturity ∈ {{verified, canonical}})
        │
        ├─► Procedural semantics
        │     (knowledge-core/procedural-semantics/)
        │
        ├─► Visual semantics
        │     (knowledge-core/{{visual-intent,visual-risk,
        │                       component-visibility,publication-intent}}/)
        │
        └─► Cross-product map
              (KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/cross-product-semantic-map/)
        │
        ▼
Governance + orchestration contracts
   (KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/, visual-system/_governance/,
    tools/visual_generation.py + tools/comfy/)
        │
        ▼
Future visual / chatbot / RAG / AR / video assistance
```

## Required provenance fields

Every semantic artifact carries:

- `provenance.source_kind`: one of `oem-pdf`, `oem-image`, `oem-brief`,
  `support-record`, `field-observation`.
- `provenance.source_id`: stable identifier of the source.
- `provenance.span`: page + region or timestamp range as applicable.
- `provenance.extracted_by`: the tool or reviewer that produced the artifact.
- `provenance.extracted_at`: ISO-8601 timestamp.
- `provenance.evidence_hash`: SHA-256 of the original evidence (when binary).

## Lineage strength rules

- A `verified` artifact MUST have at least one OEM evidence span.
- A `canonical` artifact MUST have at least one evidence pointer (OEM or
  multi-evidence support).
- An `inferred` artifact MUST list the upstream artifacts it was inferred
  from.
- A visual-semantics artifact MUST point to the canonical knowledge it
  conditions.
- A run record (orchestration layer) MUST point to the visual-semantics
  artifact + the canonical PNG it was conditioned on.

## Forbidden lineage shapes

- An artifact whose only upstream is itself.
- A canonical artifact whose only upstream is an inferred artifact (must be
  promoted to verified or downgraded).
- A visual artifact whose only justification is "designer preference".
- A run record without a workflow id and content hash.
"""


def doc_extensibility() -> str:
    return f"""# Future extensibility (knowledge center)

_Schema: `{SCHEMA}` · future extensibility · generated {NOW}._

## Subordination rule

Every future system listed below is **subordinate to the knowledge core**.
None of them originates knowledge.

## Anticipated surfaces

- **PDFs**: rendered from canonical knowledge + publication-intent for the
  `pdf` channel.
- **Websites**: rendered from canonical knowledge + publication-intent for
  the `web` channel.
- **Chatbot systems**: query the indexes; serve canonical/verified content;
  surface provenance and maturity.
- **Troubleshooting assistants**: traverse the procedure / warning /
  troubleshooting graph; respect maturity gates.
- **Onboarding systems**: traverse the workflow graph; serve only canonical
  content.
- **Semantic search**: implements retrieval over the indexes defined in
  retrieval-readiness.
- **Contextual publication**: per-channel rendering using publication-intent
  contracts.
- **Visual assistance**: governed by `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`;
  consumes visual semantics; conditioned on canonical PNG.
- **Future Comfy orchestration**: consumes the visual semantics; emits run
  records only; never edits knowledge.
- **AR overlays**: consume `component-visibility` anchors; respect mechanical
  consistency.
- **Voice assistance**: consumes terminology + procedural-semantics; renders
  canonical Colombian-Spanish phrasing.
- **Video guidance**: consumes workflow + procedural-semantics; bound by the
  visual constitution.

## Out of scope today

- Customer-uploaded photographs as evidence (different trust model).
- Live telemetry from installed locks (different schema, different lifecycle).
- Crowd-sourced procedure variants (no provenance authority).

## Extension protocol

Adding a future surface requires:

1. Declaring its publication channel in the channel registry.
2. Declaring its maturity threshold.
3. Declaring its retrieval contract (which indexes it consumes).
4. Declaring its provenance presentation (how it surfaces evidence).

A surface that cannot satisfy these four declarations does not ship.
"""


def doc_index() -> str:
    return f"""# Beslock Knowledge Center

_Schema: `{SCHEMA}` · index · generated {NOW}._

This folder is the **constitutional layer of the Beslock knowledge center**.
The runtime semantic content lives per product under
`ext-images/<slug>/knowledge-core/` and is not duplicated here.

## Documents

- [`00-architecture.md`](00-architecture.md)
- [`knowledge-ontology/global-ontology.md`](knowledge-ontology/global-ontology.md)
- [`knowledge-ontology/ontology.json`](knowledge-ontology/ontology.json)
- [`knowledge-graph/relationship-graph.md`](knowledge-graph/relationship-graph.md)
- [`knowledge-graph/graph-schema.json`](knowledge-graph/graph-schema.json)
- [`knowledge-maturity/maturity-model.md`](knowledge-maturity/maturity-model.md)
- [`knowledge-maturity/maturity-tiers.json`](knowledge-maturity/maturity-tiers.json)
- [`retrieval-readiness/retrieval-strategy.md`](retrieval-readiness/retrieval-strategy.md)
- [`retrieval-readiness/index-registry.json`](retrieval-readiness/index-registry.json)
- [`cross-product-semantic-map/cross-product-map.md`](cross-product-semantic-map/cross-product-map.md)
- [`cross-product-semantic-map/coverage.json`](cross-product-semantic-map/coverage.json)
- [`knowledge-domain-boundaries/domain-boundaries.md`](knowledge-domain-boundaries/domain-boundaries.md)
- [`semantic-lineage/lineage-specification.md`](semantic-lineage/lineage-specification.md)
- [`future-extensibility/future-extensibility.md`](future-extensibility/future-extensibility.md)

## Sibling constitutional layer

Visual governance constitution: [`../VISUAL_GOVERNANCE/00-CONSTITUTION.md`](../VISUAL_GOVERNANCE/00-CONSTITUTION.md).

## Hard guarantees

- No semantic artifact under `ext-images/<slug>/knowledge-core/` was modified.
- No governance file under `visual-system/_governance/` was modified.
- No Comfy / orchestration / visual-generation file was modified.
- No image was generated.
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)


def main() -> int:
    inv = inventory()
    written: list[str] = []

    files = {
        "README.md":                                                 doc_index(),
        "00-architecture.md":                                        doc_architecture(),
        "knowledge-ontology/global-ontology.md":                     doc_ontology(inv),
        "knowledge-graph/relationship-graph.md":                     doc_graph(),
        "knowledge-maturity/maturity-model.md":                      doc_maturity(),
        "retrieval-readiness/retrieval-strategy.md":                 doc_retrieval(),
        "cross-product-semantic-map/cross-product-map.md":           doc_cross_product(inv),
        "knowledge-domain-boundaries/domain-boundaries.md":          doc_boundaries(),
        "semantic-lineage/lineage-specification.md":                 doc_lineage(),
        "future-extensibility/future-extensibility.md":              doc_extensibility(),
    }
    for rel, body in files.items():
        write(KC / rel, body)
        written.append((KC / rel).relative_to(REPO).as_posix())

    # Machine-readable companions.
    ontology = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "shared_entities": SHARED_ENTITY_CONCEPTS,
        "shared_procedures": SHARED_PROCEDURE_CONCEPTS,
        "shared_warnings": SHARED_WARNING_CONCEPTS,
        "shared_capabilities": SHARED_CAPABILITY_CONCEPTS,
        "shared_visual_intents": SHARED_VISUAL_INTENTS,
        "publication_channels": PUBLICATION_CHANNELS,
        "inheritance_rule": "Per-product nuclei reference shared IDs verbatim; product-specific extensions add a sub-id.",
    }
    write(KC / "knowledge-ontology/ontology.json", json.dumps(ontology, ensure_ascii=False, indent=2))
    written.append((KC / "knowledge-ontology/ontology.json").relative_to(REPO).as_posix())

    graph_schema = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "node_types": [
            "product", "entity", "procedure", "workflow", "warning", "capability",
            "specification", "terminology-entry", "visual-intent",
            "procedural-semantics", "publication-target", "oem-evidence",
        ],
        "edge_types": [
            "product.has-entity", "product.has-capability", "product.has-procedure",
            "procedure.composes", "procedure.touches-entity",
            "procedure.requires-capability", "procedure.warns",
            "procedure.illustrated-by", "procedure.troubleshoots",
            "entity.contains-entity", "visual-intent.depicts-entity",
            "visual-intent.targets", "artifact.derived-from",
        ],
        "edge_required_fields": ["from", "to", "type", "maturity", "provenance"],
        "storage": {
            "per_product_edges": "ext-images/<slug>/knowledge-core/semantic/relationships/",
            "cross_product_edges": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/cross-product-edges.json",
            "shared_concept_membership": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json",
        },
    }
    write(KC / "knowledge-graph/graph-schema.json", json.dumps(graph_schema, ensure_ascii=False, indent=2))
    written.append((KC / "knowledge-graph/graph-schema.json").relative_to(REPO).as_posix())

    maturity_json = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "tiers": MATURITY_TIERS,
        "required_field": "maturity",
        "default_when_absent": "unresolved",
    }
    write(KC / "knowledge-maturity/maturity-tiers.json", json.dumps(maturity_json, ensure_ascii=False, indent=2))
    written.append((KC / "knowledge-maturity/maturity-tiers.json").relative_to(REPO).as_posix())

    index_registry = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "indexes": [
            {"id": "entities.idx",           "source_pattern": "ext-images/<slug>/knowledge-core/entities/**"},
            {"id": "procedures.idx",         "source_pattern": "ext-images/<slug>/knowledge-core/procedural-semantics/**"},
            {"id": "warnings.idx",           "source_pattern": "ext-images/<slug>/knowledge-core/warnings/**"},
            {"id": "terminology.idx",        "source_pattern": "ext-images/<slug>/knowledge-core/terminology/**"},
            {"id": "capabilities.idx",       "source_pattern": "ext-images/<slug>/knowledge-core/capabilities/**"},
            {"id": "troubleshooting.idx",    "source_pattern": "ext-images/<slug>/knowledge-core/troubleshooting/**"},
            {"id": "visual-intent.idx",      "source_pattern": "ext-images/<slug>/knowledge-core/visual-intent/**"},
            {"id": "publication-intent.idx", "source_pattern": "ext-images/<slug>/knowledge-core/publication-intent/**"},
            {"id": "cross-concept.idx",      "source_pattern": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json"},
        ],
        "served_fields": ["id", "maturity", "provenance", "last_updated", "channel_targets"],
    }
    write(KC / "retrieval-readiness/index-registry.json", json.dumps(index_registry, ensure_ascii=False, indent=2))
    written.append((KC / "retrieval-readiness/index-registry.json").relative_to(REPO).as_posix())

    coverage = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "products": PRODUCTS,
        "domains": SEMANTIC_DOMAINS,
        "per_product_counts": inv["products"],
        "totals": inv["totals"],
        "coverage_by_domain": {
            d: [p for p in PRODUCTS if inv["products"][p][d] > 0]
            for d in SEMANTIC_DOMAINS
        },
    }
    write(KC / "cross-product-semantic-map/coverage.json", json.dumps(coverage, ensure_ascii=False, indent=2))
    written.append((KC / "cross-product-semantic-map/coverage.json").relative_to(REPO).as_posix())

    # ----- Reports -----
    rep_dir = GOV_REPO / "reports" / "knowledge-center"
    rep_dir.mkdir(parents=True, exist_ok=True)

    def report(name: str, payload: dict) -> None:
        (rep_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    report("01-ontology-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "shared_entity_count":      len(SHARED_ENTITY_CONCEPTS),
        "shared_procedure_count":   len(SHARED_PROCEDURE_CONCEPTS),
        "shared_warning_count":     len(SHARED_WARNING_CONCEPTS),
        "shared_capability_count":  len(SHARED_CAPABILITY_CONCEPTS),
        "shared_visual_intent_count": len(SHARED_VISUAL_INTENTS),
        "publication_channels":     PUBLICATION_CHANNELS,
        "ontology_doc":             "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/global-ontology.md",
        "ontology_json":            "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/ontology.json",
    })

    report("02-relationship-graph-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "node_types_count":  len(graph_schema["node_types"]),
        "edge_types_count":  len(graph_schema["edge_types"]),
        "graph_doc":         "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/relationship-graph.md",
        "graph_schema":      "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/graph-schema.json",
        "edges_pending_population": True,
    })

    report("03-maturity-model-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "tier_count": len(MATURITY_TIERS),
        "tiers": [t["tier"] for t in MATURITY_TIERS],
        "default_when_absent": "unresolved",
        "required_field": "maturity",
        "promotion_path": "ocr-derived → inferred → canonical → verified",
    })

    report("04-retrieval-readiness-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "index_count": len(index_registry["indexes"]),
        "indexes": [i["id"] for i in index_registry["indexes"]],
        "served_fields": index_registry["served_fields"],
        "embeddings_status": "deferred (out of scope this phase)",
    })

    report("05-cross-product-intelligence-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "products": PRODUCTS,
        "domains": SEMANTIC_DOMAINS,
        "per_product_counts": inv["products"],
        "totals": inv["totals"],
        "coverage_by_domain": coverage["coverage_by_domain"],
        "coverage_doc": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/cross-product-semantic-map/cross-product-map.md",
    })

    report("06-semantic-boundary-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "boundaries": DOMAIN_BOUNDARIES,
        "boundary_doc": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-domain-boundaries/domain-boundaries.md",
    })

    report("07-lineage-strength-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "required_provenance_fields": [
            "provenance.source_kind", "provenance.source_id", "provenance.span",
            "provenance.extracted_by", "provenance.extracted_at",
            "provenance.evidence_hash",
        ],
        "lineage_doc": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/semantic-lineage/lineage-specification.md",
        "audit_status": "contract declared; per-artifact backfill is a separate phase",
    })

    report("08-knowledge-center-architecture-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "system_purpose": "multimodal product knowledge center",
        "is_not": [
            "manual generator", "image-generation pipeline",
            "prompt repository", "marketing site",
        ],
        "principles_count": 7,
        "layers": ["L0 evidence", "L1 semantic interpretation", "L2 canonical knowledge",
                   "L3 visual / publication semantics", "L4 cross-product intelligence",
                   "L5 constitutional layer"],
        "architecture_doc": "KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/00-architecture.md",
    })

    # 09 — unresolved semantic gaps (synthesised from inventory and prior phases).
    gaps: list[dict] = []
    # Domains with zero artifacts anywhere in the line.
    for d in SEMANTIC_DOMAINS:
        if inv["totals"][d] == 0:
            gaps.append({
                "id": f"gap.no-artifacts.{d}",
                "domain": d,
                "products_affected": PRODUCTS,
                "severity": "high",
                "note": f"No semantic artifacts of type '{d}' exist for any product.",
            })
    # Per-product missing critical domains.
    critical = ["procedural-semantics", "warnings", "terminology", "workflows"]
    for p in PRODUCTS:
        for d in critical:
            if inv["products"][p][d] == 0 and inv["totals"][d] > 0:
                gaps.append({
                    "id": f"gap.product-empty.{p}.{d}",
                    "domain": d,
                    "products_affected": [p],
                    "severity": "high" if d in ("procedural-semantics", "warnings") else "medium",
                    "note": f"{p} has zero artifacts in '{d}' while other products do.",
                })
    # Carry-over architectural gaps.
    gaps += [
        {"id": "gap.maturity-field.backfill",         "severity": "high",   "note": "`maturity` field is now required by doctrine but is not yet present on most existing artifacts; backfill required."},
        {"id": "gap.shared-concept-membership.empty", "severity": "medium", "note": "shared-concept-membership.json is specified but not populated; per-product concept tagging is required."},
        {"id": "gap.cross-product-edges.empty",       "severity": "medium", "note": "cross-product-edges.json is specified but not populated."},
        {"id": "gap.embeddings-strategy.deferred",    "severity": "low",    "note": "Embeddings store + embedding-model identity not yet declared."},
        {"id": "gap.publication-channel-spec",        "severity": "high",   "note": "Per-channel publication specifications (resolution, alt-text, format caps) are still inherited as a draft from Phase 6."},
        {"id": "gap.troubleshooting-coverage",        "severity": "high",   "note": "Only e-shield has any `troubleshooting/` artifact (1 file); the rest of the line is empty."},
        {"id": "gap.specifications-coverage",         "severity": "medium", "note": "Only e-orbit has any `specifications/` artifact; specifications layer is otherwise empty."},
    ]
    report("09-unresolved-semantic-gaps.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "gaps_count": len(gaps),
        "gaps": gaps,
    })

    report("10-future-knowledge-opportunities.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "opportunities": [
            {"id": "opp.maturity-backfill",        "value": "Promotes the maturity model from doctrine to enforced policy."},
            {"id": "opp.shared-concept-tagging",   "value": "Unlocks all cross-product queries and platform intelligence."},
            {"id": "opp.troubleshooting-build-out","value": "Highest user-facing impact; reduces support burden directly."},
            {"id": "opp.embeddings-layer",         "value": "Enables semantic search and RAG without re-architecting the knowledge core."},
            {"id": "opp.multilingual-publication", "value": "es-CO baseline + BCP-47 variants; large addressable surface."},
            {"id": "opp.voice-and-ar-surfaces",    "value": "Reuse procedural-semantics + component-visibility without new schemas."},
            {"id": "opp.automated-qa-for-knowledge", "value": "Maturity + lineage rules are machine-checkable; CI hooks are a small step."},
            {"id": "opp.field-evidence-channel",   "value": "A controlled inbound channel for support-record evidence with explicit trust rules."},
        ],
        "subordination_rule": "Every opportunity remains subordinate to the knowledge core. None of them originates knowledge.",
    })

    print("Knowledge Center consolidation complete.")
    print(f"  Constitutional root: {KC.relative_to(REPO).as_posix()}")
    print(f"  Files written:       {len(written)}")
    print(f"  Reports:             {rep_dir.relative_to(REPO).as_posix()}/01..10")
    print(f"  Inventory totals:    {inv['totals']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
