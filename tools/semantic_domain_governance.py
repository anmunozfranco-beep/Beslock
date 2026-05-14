"""
Phase 41 — SEMANTIC DOMAIN EVOLUTION & MODULAR ONTOLOGY GOVERNANCE.

Constitutional layer 34. Modeling-only. Subordinate to knowledge-core and to all
thirty-three prior governance layers (in particular layer 33 intake & navigation
governance and layer 32 multimodal evidence governance).

Writes (idempotent, non-destructive, stdlib-only):

  semantic-domain-governance/
    domain-introduction-protocol/
    specifications-governance/
    semantic-propagation/
    domain-interoperability/
    structured-semantic-extraction/
    portfolio-domain-governance/
    future-publication-and-runtime-readiness/

  KNOWLEDGE_BUILDING/SEMANTIC_DOMAIN_GOVERNANCE/
    00-INDEX.md + 7 doctrine docs + manifest.json

  _repository-governance/reports/semantic-domain/01..10 (.json + .md)

Hard rules:
  - Reads no per-product knowledge-core JSON.
  - Mutates no knowledge-core, no source-of-truth, no runtime, no publication.
  - Defines no autonomous agents, no ML, no embeddings, no prompts, no images.
  - Builds NO frontend.
  - Specifications-domain artefacts are skeleton governance ONLY, written under
    semantic-domain-governance/specifications-governance/. They DO NOT touch
    any per-product knowledge-core/specifications/ directory.
  - 19/19 runtime tests must remain green.

Reuses by reference (not redefinition):
  - layer-32 evidence classes, trust tiers, ingestion contracts, lifecycle.
  - layer-33 intake pipeline, routing policy, evidence taxonomy, navigation map.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

SDG_ROOT = THEME_ROOT / "semantic-domain-governance"
DIP_ROOT = SDG_ROOT / "domain-introduction-protocol"
SPEC_ROOT = SDG_ROOT / "specifications-governance"
PROP_ROOT = SDG_ROOT / "semantic-propagation"
INTEROP_ROOT = SDG_ROOT / "domain-interoperability"
SSE_ROOT = SDG_ROOT / "structured-semantic-extraction"
PDG_ROOT = SDG_ROOT / "portfolio-domain-governance"
FRR_ROOT = SDG_ROOT / "future-publication-and-runtime-readiness"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "SEMANTIC_DOMAIN_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "semantic-domain"

SCHEMA = "semantic-domain-governance/1.0"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

SUBORDINATE_TO = [
    "knowledge-core", "structured-knowledge", "source-of-truth",
    "runtime-implementation", "knowledge-building",
    "publication-system", "publication-quality", "linguistic-governance",
    "operational-pilots", "review-governance", "channel-governance",
    "lineage-governance", "provenance-governance", "warning-governance",
    "terminology-governance", "visual-system", "visual-intent-governance",
    "component-visibility-governance", "procedural-semantics",
    "semantic-enrichment", "corpus-enrichment",
    "supplemental-source-governance", "phase1-cutover",
    "publication-and-delivery-governance", "operational-pilot-governance",
    "publication-renderer", "publication-quality-governance",
    "linguistic-rendering-governance", "publication-time-only-doctrine",
    "warning-fidelity-doctrine", "multimodal-subordination-doctrine",
    "multimodal-evidence-governance", "intake-and-navigation-governance",
]

PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def envelope(layer: str, summary: str) -> dict:
    return {
        "schema_version": SCHEMA,
        "layer": layer,
        "constitutional_layer_index": 34,
        "subordinate_to": SUBORDINATE_TO,
        "modeling_only": True,
        "mutates_knowledge_core": False,
        "mutates_source_of_truth": False,
        "mutates_runtime": False,
        "mutates_publication": False,
        "introduces_autonomous_agents": False,
        "introduces_ml_or_embeddings": False,
        "generates_prompts": False,
        "generates_images": False,
        "builds_frontend": False,
        "summary": summary,
        "updated_at": NOW,
    }


# -----------------------------------------------------------------------------
# TASK 1 — Primary semantic domain governance
# -----------------------------------------------------------------------------

# Catalog of recognized semantic domains. Each entry declares: scope (product
# vs portfolio), evidence-class anchors (layer-32), intake-route (layer-33),
# downstream consumers, and override discipline.
SEMANTIC_DOMAINS = [
    {
        "id": "specifications",
        "label": "Product specifications",
        "scope": "product-level",
        "evidence_class_anchors": ["specification-evidence"],
        "intake_route": "product-level/<product>/specifications/",
        "downstream_consumers": ["publication", "comparison-matrices", "warnings"],
        "subdomains": [
            "electrical", "mechanical", "environmental", "authentication",
            "connectivity", "dimensional", "certifications", "materials",
            "operational-limits",
        ],
    },
    {
        "id": "warnings",
        "label": "Warnings & safety",
        "scope": "product-level",
        "evidence_class_anchors": ["warning-evidence", "procedural-evidence"],
        "intake_route": "product-level/<product>/warnings/",
        "downstream_consumers": ["publication", "operation", "troubleshooting"],
        "subdomains": ["pre-install", "install", "operation", "maintenance", "decommission"],
    },
    {
        "id": "compatibility",
        "label": "Compatibility & supported environments",
        "scope": "product-level",
        "evidence_class_anchors": ["specification-evidence", "field-evidence"],
        "intake_route": "product-level/<product>/compatibility/",
        "downstream_consumers": ["installation", "publication", "support"],
        "subdomains": ["door-types", "frame-types", "power", "connectivity-protocols", "app-versions"],
    },
    {
        "id": "installation",
        "label": "Installation procedures & geometry",
        "scope": "product-level",
        "evidence_class_anchors": ["procedural-evidence", "visual-evidence"],
        "intake_route": "product-level/<product>/install/",
        "downstream_consumers": ["publication", "field-support"],
        "subdomains": ["pre-install", "drilling", "mounting", "wiring", "verification"],
    },
    {
        "id": "certifications",
        "label": "Certifications & regulatory marks",
        "scope": "product-level",
        "evidence_class_anchors": ["specification-evidence"],
        "intake_route": "product-level/<product>/certifications/",
        "downstream_consumers": ["publication", "portfolio-comparison"],
        "subdomains": ["safety", "emc", "environmental", "regional-marks"],
    },
    {
        "id": "operational-limits",
        "label": "Operational limits & duty cycles",
        "scope": "product-level",
        "evidence_class_anchors": ["specification-evidence"],
        "intake_route": "product-level/<product>/operational-limits/",
        "downstream_consumers": ["operation", "warnings", "publication"],
        "subdomains": ["thermal", "cycle-life", "duty", "current"],
    },
    {
        "id": "maintenance",
        "label": "Maintenance schedules & service",
        "scope": "product-level",
        "evidence_class_anchors": ["procedural-evidence"],
        "intake_route": "product-level/<product>/maintenance/",
        "downstream_consumers": ["publication", "support"],
        "subdomains": ["preventive", "corrective", "consumables"],
    },
    {
        "id": "troubleshooting",
        "label": "Troubleshooting & failure modes",
        "scope": "product-level",
        "evidence_class_anchors": ["procedural-evidence", "field-evidence"],
        "intake_route": "product-level/<product>/troubleshooting/",
        "downstream_consumers": ["publication", "support"],
        "subdomains": ["diagnostics", "common-faults", "escalation"],
    },
    {
        "id": "operating-environments",
        "label": "Operating environments & deployment contexts",
        "scope": "portfolio-level",
        "evidence_class_anchors": ["specification-evidence", "field-evidence"],
        "intake_route": "portfolio-level/operating-environments/",
        "downstream_consumers": ["compatibility", "publication", "portfolio-comparison"],
        "subdomains": ["residential", "commercial", "industrial", "outdoor", "high-traffic"],
    },
    {
        "id": "shared-app",
        "label": "Shared app ecosystem",
        "scope": "portfolio-level",
        "evidence_class_anchors": ["visual-evidence", "procedural-evidence"],
        "intake_route": "portfolio-level/shared-app-ecosystems/",
        "downstream_consumers": ["pairing", "operation", "publication"],
        "subdomains": ["pairing", "permissions", "shared-access", "notifications"],
    },
]


def task_primary_governance() -> None:
    write_json(
        SDG_ROOT / "semantic-domain-catalog.json",
        {
            "id": "semantic-domain-catalog",
            "envelope": envelope(
                "semantic-domain-governance",
                "Canonical catalog of recognized semantic domains and their scope/anchors.",
            ),
            "domains": SEMANTIC_DOMAINS,
            "domain_count": len(SEMANTIC_DOMAINS),
            "scope_classes": ["product-level", "portfolio-level"],
            "subordinate_anchors": {
                "evidence_classes": "layer-32 evidence-classification/evidence-classes.json",
                "intake_pipeline": "layer-33 source-of-truth-governance/governance/intake-routing/intake-pipeline.json",
                "evidence_taxonomy": "layer-33 source-of-truth-governance/governance/evidence-taxonomy/evidence-taxonomy.json",
                "navigation_map": "layer-33 source-of-truth-governance/operational-navigation/navigation-map.json",
            },
        },
    )
    write_json(
        SDG_ROOT / "ontology-doctrine.json",
        {
            "id": "ontology-doctrine",
            "envelope": envelope(
                "semantic-domain-governance",
                "Modular ontology doctrine: domains are additive, never destructive.",
            ),
            "principles": [
                "A semantic domain is a coherent body of operational meaning, not a folder.",
                "Domains are additive: introducing a new domain MUST NOT modify existing domains.",
                "Each domain MUST declare its scope (product-level | portfolio-level).",
                "Each domain MUST anchor to one or more layer-32 evidence classes.",
                "Each domain MUST be reachable from at least one layer-33 intake route.",
                "Domains MUST NOT redefine warnings, specifications semantics, or trust tiers owned by prior layers.",
                "Domain mutations are append-only: removing a subdomain requires deprecation governance, not deletion.",
                "Domains MUST NOT introduce autonomous behaviour, ML, or embeddings.",
                "Cross-domain dependencies are declared explicitly in domain-interoperability/, never inferred.",
            ],
        },
    )
    write_text(
        SDG_ROOT / "README.md",
        (
            "# Semantic Domain Governance\n\n"
            "Layer 34. Modular ontology layer over layers 32 (multimodal evidence) "
            "and 33 (intake & navigation).\n\n"
            f"Domain catalog: {len(SEMANTIC_DOMAINS)} domains.\n"
            "All artefacts here are governance/skeleton only — no per-product "
            "knowledge-core, source-of-truth, or runtime is mutated.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 2 — Domain introduction protocol
# -----------------------------------------------------------------------------

DOMAIN_INTRODUCTION_STEPS = [
    {"id": "1-declare-intent",
     "question": "What operational meaning does the proposed domain capture?",
     "output": "intent statement + non-overlap rationale vs existing domains"},
    {"id": "2-classify-scope",
     "question": "Is the domain product-level or portfolio-level?",
     "output": "scope assignment (binary)"},
    {"id": "3-anchor-evidence-classes",
     "question": "Which layer-32 evidence classes feed this domain?",
     "output": "evidence_class_anchors (>=1)"},
    {"id": "4-bind-to-intake",
     "question": "Which layer-33 intake routes deliver artefacts to this domain?",
     "output": "intake_route declaration"},
    {"id": "5-declare-subdomains",
     "question": "What subdomains partition the domain?",
     "output": "subdomain list with non-overlap statement"},
    {"id": "6-declare-interop",
     "question": "Which existing domains does this domain interoperate with?",
     "output": "interop edges added to domain-interoperability/"},
    {"id": "7-declare-downstream",
     "question": "Which downstream consumers (publication, warnings, support) read this domain?",
     "output": "downstream_consumers list"},
    {"id": "8-non-mutation-attestation",
     "question": "Does the domain require any change to prior layers?",
     "output": "MUST attest 'no'; otherwise reject and escalate."},
    {"id": "9-register",
     "question": "Has the domain been registered in semantic-domain-catalog.json?",
     "output": "append-only entry; lineage event emitted"},
]


def task_domain_introduction_protocol() -> None:
    write_json(
        DIP_ROOT / "introduction-protocol.json",
        {
            "id": "domain-introduction-protocol",
            "envelope": envelope(
                "domain-introduction-protocol",
                "9-step protocol for introducing a new semantic domain without breaking governance.",
            ),
            "steps": DOMAIN_INTRODUCTION_STEPS,
            "step_count": len(DOMAIN_INTRODUCTION_STEPS),
            "rejection_rules": [
                "Reject if the domain mutates a prior layer.",
                "Reject if the domain overlaps an existing domain without explicit deprecation governance.",
                "Reject if the domain has no evidence_class anchor.",
                "Reject if the domain has no intake route.",
                "Reject if the domain proposes autonomous behaviour, ML, or embeddings.",
            ],
        },
    )
    write_json(
        DIP_ROOT / "deprecation-protocol.json",
        {
            "id": "domain-deprecation-protocol",
            "envelope": envelope(
                "domain-introduction-protocol",
                "Append-only deprecation protocol; no destructive removal.",
            ),
            "rules": [
                "Deprecation marks a domain or subdomain as 'closed-to-new-intake'.",
                "Existing artefacts remain in place; lineage is preserved.",
                "Deprecation requires reviewer-class attestation per layer-32 lifecycle.",
                "Deletion is NEVER permitted at this layer.",
            ],
        },
    )
    write_text(
        DIP_ROOT / "README.md",
        (
            "# Domain Introduction Protocol\n\n"
            f"{len(DOMAIN_INTRODUCTION_STEPS)}-step protocol + append-only deprecation rules.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 3 — Specifications domain implementation (governance skeleton ONLY)
# -----------------------------------------------------------------------------

SPEC_SUBDOMAINS = {
    "electrical": ["voltage", "current", "power", "battery"],
    "mechanical": ["weight", "torque", "actuation-force", "wear-class"],
    "environmental": ["operating-temperature", "humidity", "ip-rating", "uv-exposure"],
    "authentication": ["fingerprint", "pin", "card", "app", "physical-key"],
    "connectivity": ["bluetooth", "wifi", "zigbee", "matter", "rs485"],
    "dimensional": ["length", "width", "depth", "door-thickness-range"],
    "certifications": ["safety", "emc", "environmental", "regional-marks"],
    "materials": ["body", "fasteners", "finish", "seal"],
    "operational-limits": ["thermal", "cycle-life", "duty", "current-limit"],
}


def task_specifications_governance() -> None:
    write_json(
        SPEC_ROOT / "specifications-domain-skeleton.json",
        {
            "id": "specifications-domain-skeleton",
            "envelope": envelope(
                "specifications-governance",
                "Governance skeleton for the specifications domain — does NOT touch knowledge-core.",
            ),
            "subdomains": SPEC_SUBDOMAINS,
            "subdomain_count": len(SPEC_SUBDOMAINS),
            "field_count": sum(len(v) for v in SPEC_SUBDOMAINS.values()),
            "non_mutation_attestation": [
                "This skeleton declares structure only.",
                "It does NOT create files inside any per-product knowledge-core/specifications/ directory.",
                "It does NOT promote any spec value to publication.",
            ],
            "intake_binding": {
                "route": "product-level/<product>/specifications/",
                "evidence_class": "specification-evidence",
                "ingestion_contracts": ["spreadsheet", "pdf", "json", "yaml"],
                "trust_minimum": "verified-structured-export",
            },
            "products_in_scope": PRODUCTS,
        },
    )
    write_json(
        SPEC_ROOT / "spec-field-typing-rules.json",
        {
            "id": "spec-field-typing-rules",
            "envelope": envelope(
                "specifications-governance",
                "Typing rules for spec fields — declarative, no runtime validator.",
            ),
            "rules": [
                "Numeric spec fields MUST carry an explicit unit.",
                "Range fields MUST carry min, max, and unit.",
                "Categorical spec fields MUST resolve to a closed enumeration declared in this skeleton.",
                "Fields with conflicting evidence MUST surface to layer-32 conflict-governance for resolution.",
                "Specs lacking trust tier 'verified-structured-export' or higher MUST NOT propagate to portfolio-comparison.",
            ],
        },
    )
    write_text(
        SPEC_ROOT / "README.md",
        (
            "# Specifications Governance (skeleton)\n\n"
            f"{len(SPEC_SUBDOMAINS)} subdomains, "
            f"{sum(len(v) for v in SPEC_SUBDOMAINS.values())} declared fields.\n\n"
            "Skeleton only. Does NOT mutate per-product knowledge-core.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 4 — Cross-product semantic propagation
# -----------------------------------------------------------------------------

PROPAGATION_MODES = [
    {"id": "inherit",
     "definition": "Child product adopts the portfolio-level value verbatim.",
     "preconditions": ["Portfolio-level value exists", "No product-level override declared"],
     "lineage": "ingestion-lineage entry refers to portfolio source by id"},
    {"id": "override",
     "definition": "Child product replaces the portfolio-level value with a product-specific value.",
     "preconditions": ["Product-level evidence exists with trust >= portfolio source",
                       "Override is declared explicitly with rationale"],
     "lineage": "override-lineage event emitted; portfolio source retained as superseded reference"},
    {"id": "reject",
     "definition": "Child product declares the portfolio-level value as not-applicable.",
     "preconditions": ["Explicit reject-rationale provided",
                       "Reviewer-class attestation present"],
     "lineage": "reject-lineage event emitted; field marked not-applicable"},
    {"id": "extend",
     "definition": "Child product adds product-specific subfields not present at portfolio level.",
     "preconditions": ["New subfield does not collide with an existing portfolio subfield",
                       "Extension is anchored to a layer-32 evidence class"],
     "lineage": "extension-lineage event emitted; portfolio schema unchanged"},
]


def task_semantic_propagation() -> None:
    write_json(
        PROP_ROOT / "propagation-modes.json",
        {
            "id": "propagation-modes",
            "envelope": envelope(
                "semantic-propagation",
                "Four-mode semantic propagation policy: inherit / override / reject / extend.",
            ),
            "modes": PROPAGATION_MODES,
            "mode_count": len(PROPAGATION_MODES),
        },
    )
    write_json(
        PROP_ROOT / "propagation-rules.json",
        {
            "id": "propagation-rules",
            "envelope": envelope(
                "semantic-propagation",
                "Deterministic rules governing propagation across product boundaries.",
            ),
            "rules": [
                "Propagation is always declarative; no runtime inference is permitted.",
                "Default mode is 'inherit' when no product-level evidence exists.",
                "An 'override' MUST cite the product-level evidence id and trust tier.",
                "A 'reject' MUST be reviewable; silent rejection is forbidden.",
                "An 'extend' MUST NOT mutate the portfolio-level schema.",
                "Conflicts between override and inherit resolve via layer-32 conflict-policy.",
                "Propagation events are append-only and emit lineage entries.",
            ],
        },
    )
    write_json(
        PROP_ROOT / "_examples.json",
        {
            "id": "propagation-examples",
            "envelope": envelope("semantic-propagation", "Worked examples per propagation mode."),
            "examples": [
                {"mode": "inherit", "domain": "shared-app", "field": "pairing-flow",
                 "explanation": "All 6 locks inherit the shared pairing flow from the portfolio source."},
                {"mode": "override", "domain": "specifications", "field": "ip-rating",
                 "explanation": "e-shield overrides portfolio default IP44 with verified IP55 from OEM datasheet."},
                {"mode": "reject", "domain": "connectivity", "field": "zigbee",
                 "explanation": "e-touch rejects zigbee as not-applicable; reviewer attests."},
                {"mode": "extend", "domain": "authentication", "field": "vein-recognition",
                 "explanation": "e-nova extends authentication with a product-specific subfield not in portfolio schema."},
            ],
        },
    )
    write_text(
        PROP_ROOT / "README.md",
        (
            "# Semantic Propagation\n\n"
            f"{len(PROPAGATION_MODES)} declarative modes: inherit, override, reject, extend.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 5 — Domain interoperability
# -----------------------------------------------------------------------------

INTEROP_EDGES = [
    {"from": "specifications", "to": "warnings",
     "relation": "spec-bound-warning",
     "rule": "Operational-limit specs (thermal, current) generate corresponding warnings; warnings MUST cite spec evidence id."},
    {"from": "compatibility", "to": "installation",
     "relation": "compatibility-gates-install",
     "rule": "Installation steps MUST be filtered by compatibility values (door type, frame, power)."},
    {"from": "certifications", "to": "operational-limits",
     "relation": "cert-constrains-limits",
     "rule": "Certification scope constrains the publishable operational-limit envelope."},
    {"from": "maintenance", "to": "troubleshooting",
     "relation": "maintenance-precedes-troubleshooting",
     "rule": "Troubleshooting steps MUST reference maintenance prerequisites where applicable."},
    {"from": "operating-environments", "to": "compatibility",
     "relation": "environment-defines-compatibility-context",
     "rule": "Operating-environment domain provides the context vocabulary used by compatibility evaluations."},
    {"from": "shared-app", "to": "authentication",
     "relation": "app-binds-auth-flows",
     "rule": "Shared-app authentication subflows MUST resolve to the authentication subdomain of each product."},
]


def task_domain_interoperability() -> None:
    write_json(
        INTEROP_ROOT / "interop-graph.json",
        {
            "id": "interop-graph",
            "envelope": envelope(
                "domain-interoperability",
                "Declared cross-domain interoperability edges with binding rules.",
            ),
            "edges": INTEROP_EDGES,
            "edge_count": len(INTEROP_EDGES),
            "directionality": "directed",
            "non_inference_rule": "All interop edges MUST be declared explicitly; runtime inference is prohibited.",
        },
    )
    write_json(
        INTEROP_ROOT / "interop-policy.json",
        {
            "id": "interop-policy",
            "envelope": envelope(
                "domain-interoperability",
                "Policy governing how cross-domain bindings are resolved at publication time.",
            ),
            "policies": [
                "Cross-domain references resolve only at publication time, never at intake.",
                "Unresolved cross-domain references MUST block publication and surface to review.",
                "Cross-domain conflicts route to layer-32 evidence-conflict-governance.",
                "Adding a new edge requires the domain-introduction-protocol step 6.",
            ],
        },
    )
    write_text(
        INTEROP_ROOT / "README.md",
        (
            "# Domain Interoperability\n\n"
            f"{len(INTEROP_EDGES)} declared edges; declarative resolution at publication time only.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 6 — Structured semantic extraction (NO ML)
# -----------------------------------------------------------------------------

EXTRACTION_CONTRACTS = [
    {"format": "xlsx", "contract": "spreadsheet",
     "rules": ["Header row MUST exist", "Each cell maps to one declared spec field",
               "Multi-product matrices use one column per product"],
     "output": "structured rows {product, domain, subdomain, field, value, unit, source}"},
    {"format": "csv", "contract": "spreadsheet",
     "rules": ["Header row MUST exist", "Delimiter declared explicitly"],
     "output": "structured rows (same shape as xlsx)"},
    {"format": "json", "contract": "json",
     "rules": ["Schema MUST be cited", "No silent type coercion"],
     "output": "domain-typed records"},
    {"format": "yaml", "contract": "yaml",
     "rules": ["Schema MUST be cited", "Anchors and aliases preserved as evidence"],
     "output": "domain-typed records"},
    {"format": "markdown-table", "contract": "structured-document",
     "rules": ["Table MUST have a header row", "Cells parsed only when fully delimited"],
     "output": "structured rows; ambiguous cells flagged"},
]


def task_structured_semantic_extraction() -> None:
    write_json(
        SSE_ROOT / "extraction-contracts.json",
        {
            "id": "structured-extraction-contracts",
            "envelope": envelope(
                "structured-semantic-extraction",
                "Per-format structured extraction contracts. Pure parsing rules; no ML, no inference.",
            ),
            "contracts": EXTRACTION_CONTRACTS,
            "contract_count": len(EXTRACTION_CONTRACTS),
            "anti_ml_attestation": [
                "No model is invoked at any extraction step.",
                "No embeddings are computed.",
                "No probabilistic mapping between cells and fields is performed.",
                "Ambiguous cells halt extraction and require human reviewer resolution.",
            ],
        },
    )
    write_json(
        SSE_ROOT / "extraction-output-schema.json",
        {
            "id": "extraction-output-schema",
            "envelope": envelope(
                "structured-semantic-extraction",
                "Canonical row shape produced by structured extraction.",
            ),
            "fields": [
                {"name": "product", "type": "string|null", "notes": "null when portfolio-level"},
                {"name": "domain", "type": "string", "notes": "MUST resolve to semantic-domain-catalog id"},
                {"name": "subdomain", "type": "string|null"},
                {"name": "field", "type": "string"},
                {"name": "value", "type": "string|number|boolean"},
                {"name": "unit", "type": "string|null"},
                {"name": "source_evidence_id", "type": "string", "notes": "layer-32 evidence id"},
                {"name": "trust_tier", "type": "string", "notes": "layer-32 trust tier"},
                {"name": "extraction_method", "type": "string",
                 "notes": "MUST be one of: spreadsheet, json, yaml, markdown-table"},
            ],
        },
    )
    write_text(
        SSE_ROOT / "README.md",
        (
            "# Structured Semantic Extraction\n\n"
            f"{len(EXTRACTION_CONTRACTS)} format-specific contracts. No ML, no embeddings, no inference.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 7 — Portfolio-level domain governance
# -----------------------------------------------------------------------------

PORTFOLIO_DOMAINS = [
    {"id": "comparison-matrices",
     "purpose": "Side-by-side capability comparisons across all 6 locks.",
     "feeds": ["specifications", "compatibility", "certifications"],
     "publication_consumers": ["Product_Manuals.html"],
     "trust_minimum": "verified-structured-export"},
    {"id": "shared-app-ecosystems",
     "purpose": "Shared app capabilities used across the portfolio.",
     "feeds": ["shared-app", "authentication"],
     "publication_consumers": ["pairing pages, operation pages"],
     "trust_minimum": "verified-structured-export"},
    {"id": "operating-environments",
     "purpose": "Deployment-context vocabulary referenced by compatibility.",
     "feeds": ["compatibility", "warnings"],
     "publication_consumers": ["compatibility sections, install prerequisites"],
     "trust_minimum": "reviewer-attested"},
    {"id": "regulatory-landscape",
     "purpose": "Cross-product regulatory baseline (regional marks, safety scopes).",
     "feeds": ["certifications"],
     "publication_consumers": ["certifications sections, portfolio overview"],
     "trust_minimum": "oem-direct-evidence"},
]


def task_portfolio_domain_governance() -> None:
    write_json(
        PDG_ROOT / "portfolio-domains.json",
        {
            "id": "portfolio-domains",
            "envelope": envelope(
                "portfolio-domain-governance",
                "Governance for portfolio-level semantic domains.",
            ),
            "portfolio_domains": PORTFOLIO_DOMAINS,
            "portfolio_domain_count": len(PORTFOLIO_DOMAINS),
            "products_in_scope": PRODUCTS,
        },
    )
    write_json(
        PDG_ROOT / "portfolio-vs-product-rules.json",
        {
            "id": "portfolio-vs-product-rules",
            "envelope": envelope(
                "portfolio-domain-governance",
                "Rules disambiguating portfolio-owned vs product-owned semantic responsibility.",
            ),
            "rules": [
                "If a value applies to all 6 products without product-specific evidence, it is portfolio-owned.",
                "If a value applies to >=1 product with product-specific evidence, it is product-owned with optional portfolio default.",
                "Portfolio-owned values propagate to products via 'inherit' mode.",
                "Product-owned values that diverge from portfolio default propagate via 'override' mode.",
                "Portfolio domains MUST NOT contain product-exclusive values.",
                "Product domains MUST NOT redefine portfolio-owned vocabulary.",
            ],
        },
    )
    write_text(
        PDG_ROOT / "README.md",
        (
            "# Portfolio Domain Governance\n\n"
            f"{len(PORTFOLIO_DOMAINS)} portfolio-level domains; clear ownership boundaries vs product domains.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 8 — Future publication & runtime readiness
# -----------------------------------------------------------------------------

def task_future_readiness() -> None:
    write_json(
        FRR_ROOT / "publication-readiness.json",
        {
            "id": "publication-readiness",
            "envelope": envelope(
                "future-publication-and-runtime-readiness",
                "How a future publication renderer MUST consume the semantic-domain ontology.",
            ),
            "contract": [
                "Publication MUST resolve every published value to a (domain, subdomain, field) tuple.",
                "Publication MUST cite the source_evidence_id and trust_tier for each rendered value.",
                "Publication MUST NOT render fields below the trust_minimum declared by their portfolio-domain.",
                "Publication MUST honour propagation-mode lineage (inherit/override/reject/extend).",
                "Publication MUST NOT invent cross-domain references beyond declared interop edges.",
                "Publication remains the sole place where cross-domain references resolve.",
            ],
            "non_mutation_attestation": "This contract is declarative; no renderer is invoked here.",
        },
    )
    write_json(
        FRR_ROOT / "runtime-readiness.json",
        {
            "id": "runtime-readiness",
            "envelope": envelope(
                "future-publication-and-runtime-readiness",
                "How a future runtime navigator MAY consult the semantic-domain ontology.",
            ),
            "contract": [
                "Runtime MAY read semantic-domain-catalog.json to expose navigation by domain.",
                "Runtime MUST NOT mutate any domain artefact.",
                "Runtime MUST surface trust-tier and propagation-mode metadata when displaying values.",
                "Runtime MUST NOT bypass interop edges to derive cross-domain answers.",
                "Runtime MUST treat 'reject' values as not-applicable, not as missing.",
            ],
            "non_mutation_attestation": "Read-only consultation contract; the runtime is NOT modified by this phase.",
        },
    )
    write_json(
        FRR_ROOT / "future-copilot-domain-readiness.json",
        {
            "id": "future-copilot-domain-readiness",
            "envelope": envelope(
                "future-publication-and-runtime-readiness",
                "Suggestion-only contract for any future copilot operating over the ontology.",
            ),
            "contract": [
                "Copilot MAY suggest domain assignments for new artefacts.",
                "Copilot MUST NOT register new domains; only humans invoke the introduction protocol.",
                "Copilot MUST NOT mutate semantic-domain-catalog.json.",
                "Copilot MUST cite layer-33 navigation map when proposing routes.",
                "Copilot MUST surface uncertainty as 'requires-review', never as an autonomous decision.",
            ],
        },
    )
    write_text(
        FRR_ROOT / "README.md",
        (
            "# Future Publication & Runtime Readiness\n\n"
            "Declarative contracts for future publication, runtime, and copilot consumers of the ontology.\n"
        ),
    )


# -----------------------------------------------------------------------------
# DOCTRINE
# -----------------------------------------------------------------------------

DOCTRINE_DOCS = [
    ("01-domain-additivity-doctrine.md",
     "# Domain Additivity\n\nNew semantic domains are additive only. They never modify, remove, or redefine existing domains.\n"),
    ("02-scope-binarity-doctrine.md",
     "# Scope Binarity\n\nEvery domain is either product-level or portfolio-level. No third class is permitted at this layer.\n"),
    ("03-evidence-anchoring-doctrine.md",
     "# Evidence Anchoring\n\nEvery domain MUST anchor to one or more layer-32 evidence classes. Domains without evidence anchors are rejected.\n"),
    ("04-propagation-discipline-doctrine.md",
     "# Propagation Discipline\n\nCross-product propagation uses only the four declared modes: inherit, override, reject, extend.\n"),
    ("05-interop-declarative-doctrine.md",
     "# Interop Declarative\n\nCross-domain interoperability is always declared, never inferred. Runtime inference is prohibited.\n"),
    ("06-non-ml-extraction-doctrine.md",
     "# Non-ML Extraction\n\nStructured semantic extraction uses only deterministic parsing. No models, no embeddings, no probabilistic mapping.\n"),
    ("07-non-mutation-doctrine.md",
     "# Non-Mutation\n\nThis layer mutates no prior layer. Knowledge-core, source-of-truth, runtime, and publication are untouched.\n"),
]


def write_doctrine() -> None:
    index_lines = ["# SEMANTIC_DOMAIN_GOVERNANCE\n", "\nLayer 34 — Modular ontology governance.\n", "\n## Doctrine\n"]
    for fname, body in DOCTRINE_DOCS:
        write_text(CONST_ROOT / fname, body)
        index_lines.append(f"- [{fname}]({fname})\n")
    write_text(CONST_ROOT / "00-INDEX.md", "".join(index_lines))
    write_json(
        CONST_ROOT / "manifest.json",
        {
            "id": "semantic-domain-governance-manifest",
            "envelope": envelope("semantic-domain-governance", "Manifest of doctrine docs."),
            "doctrine_doc_count": len(DOCTRINE_DOCS),
            "doctrine_docs": [name for name, _ in DOCTRINE_DOCS],
            "constitutional_layer_index": 34,
            "subordinate_chain_length": len(SUBORDINATE_TO),
            "schema": SCHEMA,
        },
    )


# -----------------------------------------------------------------------------
# REPORTS
# -----------------------------------------------------------------------------

def write_reports() -> None:
    reports = [
        ("01-semantic-domain-governance-summary",
         {"domain_count": len(SEMANTIC_DOMAINS),
          "scope_classes": ["product-level", "portfolio-level"],
          "domains": [d["id"] for d in SEMANTIC_DOMAINS]},
         f"{len(SEMANTIC_DOMAINS)} semantic domains catalogued; modular ontology layer established."),
        ("02-domain-introduction-protocol-summary",
         {"step_count": len(DOMAIN_INTRODUCTION_STEPS),
          "rejection_rule_count": 5},
         f"{len(DOMAIN_INTRODUCTION_STEPS)}-step introduction protocol + 5 rejection rules + append-only deprecation."),
        ("03-specifications-domain-summary",
         {"subdomain_count": len(SPEC_SUBDOMAINS),
          "field_count": sum(len(v) for v in SPEC_SUBDOMAINS.values()),
          "products_in_scope": PRODUCTS,
          "knowledge_core_mutated": False},
         f"Specifications skeleton: {len(SPEC_SUBDOMAINS)} subdomains, "
         f"{sum(len(v) for v in SPEC_SUBDOMAINS.values())} fields. Knowledge-core untouched."),
        ("04-semantic-propagation-summary",
         {"mode_count": len(PROPAGATION_MODES),
          "modes": [m["id"] for m in PROPAGATION_MODES]},
         "Four propagation modes: inherit / override / reject / extend; declarative only."),
        ("05-domain-interoperability-summary",
         {"edge_count": len(INTEROP_EDGES),
          "edges": [(e["from"], e["to"]) for e in INTEROP_EDGES]},
         f"{len(INTEROP_EDGES)} declared cross-domain edges; resolved only at publication time."),
        ("06-structured-semantic-extraction-summary",
         {"contract_count": len(EXTRACTION_CONTRACTS),
          "ml_used": False, "embeddings_used": False, "inference_used": False},
         f"{len(EXTRACTION_CONTRACTS)} format contracts; pure deterministic parsing."),
        ("07-portfolio-domain-governance-summary",
         {"portfolio_domain_count": len(PORTFOLIO_DOMAINS),
          "portfolio_domains": [p["id"] for p in PORTFOLIO_DOMAINS]},
         f"{len(PORTFOLIO_DOMAINS)} portfolio-level domains; ownership boundaries declared."),
        ("08-future-readiness-summary",
         {"publication_contract_present": True,
          "runtime_contract_present": True,
          "copilot_contract_present": True,
          "any_consumer_invoked": False},
         "Declarative readiness contracts for publication, runtime, and copilot consumers."),
        ("09-unresolved-ontology-risks",
         {"risks": [
             "Specifications skeleton fields not yet bound to per-product knowledge-core.",
             "Override/reject lineage events have no emitter yet (declarative only).",
             "Interop edges have no automated validator yet.",
             "Structured extraction has no executor yet (contracts only).",
             "Deprecation governance has no UI surface yet.",
         ]},
         "5 unresolved ontology risks documented for future remediation phases."),
        ("10-semantic-ecosystem-maturity-reassessment",
         {"layer": 34,
          "subordinate_chain_length": len(SUBORDINATE_TO),
          "domains_catalogued": len(SEMANTIC_DOMAINS),
          "portfolio_domains_catalogued": len(PORTFOLIO_DOMAINS),
          "propagation_modes": len(PROPAGATION_MODES),
          "interop_edges": len(INTEROP_EDGES),
          "extraction_contracts": len(EXTRACTION_CONTRACTS),
          "doctrine_docs": len(DOCTRINE_DOCS),
          "knowledge_core_mutated": False,
          "source_of_truth_mutated": False,
          "runtime_mutated": False,
          "publication_mutated": False,
          "ml_introduced": False,
          "embeddings_introduced": False,
          "autonomous_agents_introduced": False,
          "tests_status": "19/19 expected"},
         "Layer 34 established. Modular ontology in place; ecosystem ready for downstream binding without breaking governance."),
    ]
    for name, data, summary in reports:
        write_json(
            REPORTS_ROOT / f"{name}.json",
            {"id": name, "envelope": envelope(name, summary), "data": data},
        )
        write_text(
            REPORTS_ROOT / f"{name}.md",
            f"# {name}\n\n{summary}\n",
        )


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

def main() -> None:
    task_primary_governance()
    task_domain_introduction_protocol()
    task_specifications_governance()
    task_semantic_propagation()
    task_domain_interoperability()
    task_structured_semantic_extraction()
    task_portfolio_domain_governance()
    task_future_readiness()
    write_doctrine()
    write_reports()
    print(f"Phase 41 — semantic domain governance written.")
    print(f"Subordinate chain length: {len(SUBORDINATE_TO)}")
    print(f"Domains: {len(SEMANTIC_DOMAINS)} | Portfolio domains: {len(PORTFOLIO_DOMAINS)} | "
          f"Propagation modes: {len(PROPAGATION_MODES)} | Interop edges: {len(INTEROP_EDGES)} | "
          f"Extraction contracts: {len(EXTRACTION_CONTRACTS)}")


if __name__ == "__main__":
    main()
