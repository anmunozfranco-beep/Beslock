"""
Phase 42 — PRODUCT IDENTITY, ALIAS & SEMANTIC CONTINUITY GOVERNANCE.

Constitutional layer 35. Modeling-only. Subordinate to knowledge-core and to
all thirty-four prior governance layers (in particular layer 34 semantic-domain
governance and layer 33 intake & navigation governance).

Writes (idempotent, non-destructive, stdlib-only) under
wp-content/themes/beslock-custom/User manuals/identity-resolution/:

  canonical-products/                        (1 .json per canonical product)
  oem-mappings/                              (manufacturer-models, sku-recon,
                                              alias-registry, unresolved,
                                              deprecated)
  visual-identity/                           (geometry-signatures,
                                              component-anchor-maps,
                                              visual-match-candidates,
                                              reconciliation-evidence)
  lineage/                                   (platform-lineages,
                                              variant-relationships,
                                              generation-evolution,
                                              ecosystem-affiliations)
  continuity/                                (persistent-memory,
                                              confidence-history,
                                              reviewer-validations,
                                              semantic-continuity)
  governance/                                (product-identity,
                                              identity-trust-models,
                                              reconciliation-rules,
                                              propagation-rules,
                                              continuity-governance)

Plus:
  KNOWLEDGE_BUILDING/IDENTITY_RESOLUTION_GOVERNANCE/  (00-INDEX + 8 doctrines + manifest)
  _repository-governance/reports/identity-resolution/ (10 reports .json + .md)

Hard rules:
  - Mutates no knowledge-core, no source-of-truth, no runtime, no publication.
  - Defines no autonomous agents, no ML/embeddings/prompts/images/face-recognition.
  - Builds NO frontend.
  - Auto-promotion of unresolved identities is FORBIDDEN.
  - Reviewer governance is NEVER bypassed.
  - 19/19 runtime tests must remain green.

Reuses by reference (not redefinition):
  - layer-32 evidence classes, trust tiers, lifecycle, conflict policy.
  - layer-33 intake pipeline + evidence taxonomy + navigation map.
  - layer-34 semantic-domain catalog + propagation modes + interop edges.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

IR_ROOT = THEME_ROOT / "identity-resolution"

CANON_ROOT = IR_ROOT / "canonical-products"
OEM_ROOT = IR_ROOT / "oem-mappings"
VIS_ROOT = IR_ROOT / "visual-identity"
LIN_ROOT = IR_ROOT / "lineage"
CONT_ROOT = IR_ROOT / "continuity"
GOV_ROOT = IR_ROOT / "governance"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "IDENTITY_RESOLUTION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "identity-resolution"

SCHEMA = "identity-resolution-governance/1.0"
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
    "semantic-domain-governance",
]

# Canonical product roster known to the ecosystem.
PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]

# Per-product canonical record seed (declarative skeleton; OEM mapping noted as
# 'unresolved' until reviewer-attested in oem-mappings/manufacturer-models.json).
CANONICAL_SEED = {
    "e-orbit":  {"commercial_label": "e-Orbit",  "ecosystem_affiliations": ["tuya"],   "form_factor_hint": "smart-deadbolt"},
    "e-prime":  {"commercial_label": "e-Prime",  "ecosystem_affiliations": ["tuya"],   "form_factor_hint": "smart-deadbolt"},
    "e-flex":   {"commercial_label": "e-Flex",   "ecosystem_affiliations": ["tuya"],   "form_factor_hint": "smart-lever"},
    "e-touch":  {"commercial_label": "e-Touch",  "ecosystem_affiliations": ["ttlock"], "form_factor_hint": "keypad-deadbolt"},
    "e-shield": {"commercial_label": "e-Shield", "ecosystem_affiliations": ["ttlock"], "form_factor_hint": "smart-mortise"},
    "e-nova":   {"commercial_label": "e-Nova",   "ecosystem_affiliations": ["tuya"],   "form_factor_hint": "smart-padlock"},
}


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
        "constitutional_layer_index": 35,
        "subordinate_to": SUBORDINATE_TO,
        "modeling_only": True,
        "mutates_knowledge_core": False,
        "mutates_source_of_truth": False,
        "mutates_runtime": False,
        "mutates_publication": False,
        "introduces_autonomous_agents": False,
        "introduces_ml_or_embeddings": False,
        "introduces_face_or_image_recognition": False,
        "auto_promotes_unresolved_identities": False,
        "bypasses_reviewer_governance": False,
        "summary": summary,
        "updated_at": NOW,
    }


# -----------------------------------------------------------------------------
# TASK 1 — PRODUCT IDENTITY GOVERNANCE
# -----------------------------------------------------------------------------

IDENTITY_KINDS = [
    {"id": "canonical-identity",
     "definition": "Ecosystem-stable identity for the product (e.g., e-nova).",
     "uniqueness": "exactly-one-per-product",
     "mutability": "append-only; rename requires deprecation governance"},
    {"id": "oem-identity",
     "definition": "Manufacturer/factory identity (e.g., model code SB-1).",
     "uniqueness": "may map to multiple commercial identities",
     "mutability": "append-only; alias additions allowed"},
    {"id": "commercial-identity",
     "definition": "Public-facing label sold to end users.",
     "uniqueness": "one canonical label per region; aliases allowed",
     "mutability": "append-only"},
    {"id": "reseller-identity",
     "definition": "Identity used by a third-party reseller (white-label, distributor).",
     "uniqueness": "many-per-canonical; provenance bound to reseller",
     "mutability": "append-only"},
    {"id": "variant-identity",
     "definition": "Distinguishes hardware/firmware variants of the same canonical product.",
     "uniqueness": "many-per-canonical",
     "mutability": "append-only; supersession permitted"},
    {"id": "platform-identity",
     "definition": "Shared OEM platform (e.g., Tuya BLE platform v3) underpinning multiple products.",
     "uniqueness": "many-canonicals-per-platform",
     "mutability": "append-only"},
    {"id": "regional-identity",
     "definition": "Region-specific identity (regulatory, language, SKU).",
     "uniqueness": "many-per-canonical",
     "mutability": "append-only"},
]


def task_product_identity_governance() -> None:
    write_json(
        GOV_ROOT / "product-identity" / "identity-kinds.json",
        {
            "id": "identity-kinds",
            "envelope": envelope("product-identity",
                                 "Seven canonical identity kinds and their uniqueness/mutability rules."),
            "kinds": IDENTITY_KINDS,
            "kind_count": len(IDENTITY_KINDS),
        },
    )
    write_json(
        GOV_ROOT / "product-identity" / "identity-rules.json",
        {
            "id": "identity-rules",
            "envelope": envelope("product-identity",
                                 "Rules governing how identities are declared, related, and persisted."),
            "rules": [
                "Every product MUST have exactly one canonical-identity record.",
                "OEM, commercial, reseller, variant, platform, and regional identities MUST be linked to a canonical-identity.",
                "An identity record MUST cite at least one source_evidence_id (layer-32 evidence id) before reaching 'validated'.",
                "Identity links are append-only; supersession emits a lineage event but does not delete prior links.",
                "Renaming a canonical-identity is FORBIDDEN; deprecation governance is the only path.",
                "An identity MUST NOT cross into a different canonical-identity without explicit reviewer attestation.",
                "Auto-promotion from candidate to validated is FORBIDDEN.",
            ],
        },
    )
    # Per-product canonical seeds.
    for pid in PRODUCTS:
        seed = CANONICAL_SEED[pid]
        write_json(
            CANON_ROOT / f"{pid}.json",
            {
                "id": pid,
                "envelope": envelope("canonical-products", f"Canonical identity record for {pid}."),
                "canonical_id": pid,
                "commercial_label": seed["commercial_label"],
                "ecosystem_affiliations": seed["ecosystem_affiliations"],
                "form_factor_hint": seed["form_factor_hint"],
                "oem_identity": {"status": "unresolved",
                                 "candidates": [],
                                 "review_required": True},
                "aliases": [],
                "variants": [],
                "regional_identities": [],
                "platform_identity": {"status": "unresolved", "candidates": []},
                "lifecycle_state": "canonical",
                "trust_tier": "reviewer-attested",
                "lineage_refs": [],
                "non_mutation_attestation": "Created from declarative seed; mutation requires reviewer governance.",
            },
        )
    write_text(
        GOV_ROOT / "product-identity" / "README.md",
        (
            "# Product Identity Governance\n\n"
            f"{len(IDENTITY_KINDS)} identity kinds. {len(PRODUCTS)} canonical products seeded.\n"
            "All OEM/platform mappings begin in 'unresolved' state and require reviewer attestation.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 2 — OEM ↔ COMMERCIAL RECONCILIATION
# -----------------------------------------------------------------------------

def task_oem_reconciliation() -> None:
    write_json(
        OEM_ROOT / "manufacturer-models.json",
        {
            "id": "manufacturer-models",
            "envelope": envelope("oem-mappings",
                                 "OEM model registry. All entries start as candidates pending reviewer attestation."),
            "entries": [
                {"oem_model": p.get("oem_model_hint", ""),
                 "manufacturer_hint": p.get("mfr_hint", ""),
                 "candidate_canonicals": p.get("candidates", []),
                 "status": "candidate",
                 "review_required": True,
                 "evidence_refs": []}
                for p in []  # intentionally empty until reviewer-fed
            ],
            "entry_count": 0,
            "policy": "Entries are added only via reviewer-attested intake; no auto-population.",
        },
    )
    write_json(
        OEM_ROOT / "sku-reconciliation.json",
        {
            "id": "sku-reconciliation",
            "envelope": envelope("oem-mappings", "SKU normalization and reconciliation rules."),
            "rules": [
                "SKUs are normalized via case-folding, whitespace collapse, and dash unification BEFORE matching.",
                "Normalization is non-destructive: original SKU is preserved as 'sku_raw'.",
                "Two SKUs match only when normalized forms are identical AND reviewer has not flagged divergence.",
                "An SKU MUST NOT be linked to more than one canonical-identity without explicit reviewer attestation.",
                "Cross-catalog SKU collisions raise an 'unresolved-identity' record.",
            ],
            "normalization_steps": [
                "trim whitespace",
                "collapse repeated separators",
                "unify dash/underscore to dash",
                "lowercase",
                "strip non-essential suffixes (region codes recorded separately)",
            ],
        },
    )
    write_json(
        OEM_ROOT / "alias-registry.json",
        {
            "id": "alias-registry",
            "envelope": envelope("oem-mappings",
                                 "Persistent registry of validated aliases. Append-only."),
            "aliases": [],
            "alias_count": 0,
            "schema": {
                "alias": "string (raw form as encountered)",
                "alias_normalized": "string (post-normalization)",
                "canonical_id": "string (must exist in canonical-products/)",
                "kind": "oem | commercial | reseller | variant | regional",
                "first_seen_evidence_id": "string (layer-32 evidence id)",
                "validated_at": "ISO-8601 timestamp",
                "validated_by": "reviewer class id",
                "lifecycle_state": "candidate | probable | validated | canonical | deprecated | superseded",
            },
            "policy": "Aliases reach 'validated' only via reviewer attestation; auto-promotion is FORBIDDEN.",
        },
    )
    write_json(
        OEM_ROOT / "unresolved-identities.json",
        {
            "id": "unresolved-identities",
            "envelope": envelope("oem-mappings",
                                 "Identities awaiting reviewer reconciliation. Append-only."),
            "entries": [],
            "entry_count": 0,
            "schema": {
                "raw_label": "string",
                "observed_in_evidence_id": "string (layer-32 id)",
                "candidate_canonicals": "list[string]",
                "blocking_reason": "string (e.g., 'multiple-candidates', 'no-canonical-match', 'sku-collision')",
                "raised_at": "ISO-8601 timestamp",
                "reviewer_assigned": "string|null",
            },
            "resolution_policy": "Resolution requires explicit reviewer attestation; resolved entries move to alias-registry.",
        },
    )
    write_json(
        OEM_ROOT / "deprecated-identities.json",
        {
            "id": "deprecated-identities",
            "envelope": envelope("oem-mappings",
                                 "Append-only record of deprecated/superseded identities."),
            "entries": [],
            "entry_count": 0,
            "policy": "Deprecation is non-destructive; original identity records remain in canonical-products/.",
        },
    )
    write_json(
        OEM_ROOT / "reconciliation-rules.json",
        {
            "id": "reconciliation-rules",
            "envelope": envelope("reconciliation-rules",
                                 "Deterministic rules governing OEM↔commercial reconciliation."),
            "rules": [
                "Reconciliation MUST cite at least two independent evidence sources before reaching 'validated'.",
                "Reconciliation MUST NOT cross ecosystem affiliations (tuya↔ttlock) without reviewer attestation.",
                "Reconciliation MUST honour the four propagation modes from layer 34 (inherit/override/reject/extend).",
                "Reconciliation conflicts route to layer-32 conflict-governance.",
                "Reconciliation events are append-only and emit lineage entries to continuity/.",
            ],
        },
    )
    write_text(
        OEM_ROOT / "README.md",
        (
            "# OEM Mappings & Reconciliation\n\n"
            "All registries begin empty and grow only via reviewer-attested intake.\n"
            "Auto-population, auto-promotion, and silent merging are FORBIDDEN.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 3 — PERSISTENT RECONCILIATION MEMORY
# -----------------------------------------------------------------------------

def task_persistent_memory() -> None:
    write_json(
        CONT_ROOT / "persistent-memory" / "memory-schema.json",
        {
            "id": "persistent-memory-schema",
            "envelope": envelope("persistent-memory",
                                 "Schema for the persistent reconciliation-memory store."),
            "record_shape": {
                "alias_normalized": "string",
                "canonical_id": "string",
                "first_validated_at": "ISO-8601",
                "first_validated_by": "reviewer class id",
                "validating_evidence_ids": "list[string] (>=2 required for 'validated')",
                "confidence_state": "candidate | probable | validated | canonical",
                "supersession_chain": "list[{old_canonical_id, new_canonical_id, reviewer, at}]",
                "contradiction_events": "list[{evidence_id, raised_at, status}]",
            },
            "behaviour": [
                "Once an alias is 'validated', subsequent evidence mentioning the same normalized alias resolves to the same canonical_id.",
                "If subsequent evidence contradicts the validated mapping, a contradiction-event is raised; the mapping is NOT auto-revoked.",
                "Contradiction resolution requires reviewer attestation; outcome is appended (validated/superseded/deprecated).",
                "Persistent memory is append-only; entries are never silently overwritten.",
            ],
        },
    )
    write_json(
        CONT_ROOT / "persistent-memory" / "memory-store.json",
        {
            "id": "persistent-memory-store",
            "envelope": envelope("persistent-memory",
                                 "Persistent memory store seeded empty; populated only by reviewer attestation."),
            "records": [],
            "record_count": 0,
            "non_mutation_attestation": "No memory record exists yet; the store is initialised empty.",
        },
    )
    write_json(
        CONT_ROOT / "confidence-history" / "confidence-history-schema.json",
        {
            "id": "confidence-history-schema",
            "envelope": envelope("confidence-history",
                                 "Append-only history of confidence-state transitions per memory record."),
            "transition_shape": {
                "alias_normalized": "string",
                "from_state": "candidate | probable | validated | canonical | deprecated | superseded",
                "to_state": "candidate | probable | validated | canonical | deprecated | superseded",
                "trigger_evidence_ids": "list[string]",
                "reviewer": "reviewer class id",
                "at": "ISO-8601",
                "rationale": "string",
            },
            "rule": "Every state transition MUST be recorded; missing transitions are a governance violation.",
        },
    )
    write_json(
        CONT_ROOT / "reviewer-validations" / "validation-protocol.json",
        {
            "id": "reviewer-validation-protocol",
            "envelope": envelope("reviewer-validations",
                                 "Protocol governing reviewer validation events for identity reconciliations."),
            "steps": [
                {"id": "1-collect-evidence", "rule": "At least two independent evidence sources MUST be collected."},
                {"id": "2-classify-confidence",
                 "rule": "Reviewer assigns confidence_state per identity-trust-models."},
                {"id": "3-emit-lineage",
                 "rule": "Validation event MUST emit a lineage entry citing all evidence ids."},
                {"id": "4-update-memory",
                 "rule": "Persistent memory store gets an append-only record."},
                {"id": "5-attest-non-mutation",
                 "rule": "Reviewer attests that source-of-truth and knowledge-core were not mutated."},
            ],
        },
    )
    write_text(
        CONT_ROOT / "persistent-memory" / "README.md",
        (
            "# Persistent Reconciliation Memory\n\n"
            "Append-only store. Validated alias↔canonical mappings persist across future intake.\n"
            "Contradictions are surfaced, never silently overwritten.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 4 — VISUAL IDENTITY RECONCILIATION (NO AI / NO ML)
# -----------------------------------------------------------------------------

GEOMETRY_FEATURES = [
    {"id": "fingerprint-placement",
     "kind": "categorical",
     "values": ["top", "centre", "bottom", "side", "absent"],
     "extraction_method": "human-annotated or trusted-PNG metadata"},
    {"id": "keypad-topology",
     "kind": "categorical",
     "values": ["3x4-numeric", "3x4-numeric-plus-fn", "circular-touch", "absent"],
     "extraction_method": "human-annotated"},
    {"id": "handle-geometry",
     "kind": "categorical",
     "values": ["lever", "knob", "thumb-turn", "smart-bolt", "padlock-shackle"],
     "extraction_method": "human-annotated"},
    {"id": "dimensional-overlap",
     "kind": "ranged",
     "values_format": "{length_mm, width_mm, depth_mm} with tolerance",
     "extraction_method": "from declared specifications"},
    {"id": "indicator-layout",
     "kind": "categorical",
     "values": ["led-ring", "single-led", "rgb-strip", "absent"],
     "extraction_method": "human-annotated"},
]


def task_visual_identity() -> None:
    write_json(
        VIS_ROOT / "geometry-signatures" / "geometry-feature-schema.json",
        {
            "id": "geometry-feature-schema",
            "envelope": envelope("visual-identity",
                                 "Declarative geometry features used for non-ML visual identity matching."),
            "features": GEOMETRY_FEATURES,
            "feature_count": len(GEOMETRY_FEATURES),
            "anti_ml_attestation": [
                "No image recognition model is invoked.",
                "No embeddings are computed.",
                "No face or biometric processing is performed.",
                "All feature values originate from human annotation or trusted-PNG metadata.",
            ],
        },
    )
    write_json(
        VIS_ROOT / "geometry-signatures" / "signatures-store.json",
        {
            "id": "geometry-signatures-store",
            "envelope": envelope("visual-identity",
                                 "Per-canonical geometry signatures. Initialised empty."),
            "signatures": [],
            "signature_count": 0,
            "policy": "Signatures are added via reviewer attestation citing trusted PNG ids.",
        },
    )
    write_json(
        VIS_ROOT / "component-anchor-maps" / "anchor-map-schema.json",
        {
            "id": "component-anchor-map-schema",
            "envelope": envelope("visual-identity",
                                 "Schema for component anchor maps (relative coordinates within a trusted PNG)."),
            "shape": {
                "trusted_png_id": "string",
                "canonical_id": "string",
                "anchors": "list[{component, x_rel, y_rel, w_rel, h_rel, source_method}]",
            },
            "rule": "Coordinates are normalized to [0,1]; absolute pixel mapping is not stored here.",
        },
    )
    write_json(
        VIS_ROOT / "visual-match-candidates" / "matching-policy.json",
        {
            "id": "visual-matching-policy",
            "envelope": envelope("visual-identity",
                                 "Deterministic matching policy over geometry signatures."),
            "policy": [
                "Two products match visually only when ALL declared categorical features are identical AND dimensional overlap is within tolerance.",
                "Partial matches surface as 'candidates' for reviewer attention; they are NEVER auto-promoted.",
                "Clone detection: identical signature across non-equivalent canonical_ids raises an unresolved-identity event.",
                "OEM equivalence detection: identical signature with shared platform_identity raises a 'platform-equivalence' candidate.",
                "All matches MUST cite source_evidence_id for each feature.",
            ],
        },
    )
    write_json(
        VIS_ROOT / "reconciliation-evidence" / "evidence-binding.json",
        {
            "id": "visual-reconciliation-evidence-binding",
            "envelope": envelope("visual-identity",
                                 "Binding rules connecting visual matches to layer-32 evidence ids."),
            "rules": [
                "Every visual signature MUST cite a layer-32 evidence_id.",
                "Trust tier of the signature inherits the lowest tier among its citing evidence.",
                "Visual evidence MUST be marked with intake-route 'product-level/<product>/visual-evidence/' or 'portfolio-level/shared-app-ecosystems/'.",
                "Visual reconciliation events emit lineage entries to continuity/.",
            ],
        },
    )
    write_text(
        VIS_ROOT / "README.md",
        (
            "# Visual Identity Reconciliation\n\n"
            f"{len(GEOMETRY_FEATURES)} declarative geometry features. Pure deterministic matching.\n"
            "No AI image recognition, no embeddings, no face/biometric processing.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 5 — CONFIDENCE & REVIEW GOVERNANCE
# -----------------------------------------------------------------------------

LIFECYCLE_STATES = [
    {"id": "candidate",
     "definition": "Identity link proposed by intake; awaiting reviewer triage.",
     "exit_to": ["probable", "deprecated"]},
    {"id": "probable",
     "definition": "Reviewer has triaged; ≥1 evidence source supports the link, but <2 independent sources or pending verification.",
     "exit_to": ["validated", "deprecated"]},
    {"id": "validated",
     "definition": "≥2 independent evidence sources + reviewer attestation; safe for downstream consumption.",
     "exit_to": ["canonical", "superseded", "deprecated"]},
    {"id": "canonical",
     "definition": "Validated and elevated to ecosystem-stable identity; persisted in canonical-products/.",
     "exit_to": ["superseded", "deprecated"]},
    {"id": "deprecated",
     "definition": "Closed-to-new-intake; record retained for lineage.",
     "exit_to": []},
    {"id": "superseded",
     "definition": "Replaced by a newer identity; supersession chain emitted.",
     "exit_to": []},
]

LIFECYCLE_TRANSITIONS = [
    ("candidate", "probable", "reviewer-triage"),
    ("candidate", "deprecated", "reviewer-rejection"),
    ("probable", "validated", "reviewer-attestation + 2nd-evidence"),
    ("probable", "deprecated", "reviewer-rejection"),
    ("validated", "canonical", "reviewer-elevation"),
    ("validated", "superseded", "newer-identity-validated"),
    ("validated", "deprecated", "reviewer-deprecation"),
    ("canonical", "superseded", "platform-or-variant-replacement"),
    ("canonical", "deprecated", "reviewer-deprecation"),
]


def task_confidence_governance() -> None:
    write_json(
        GOV_ROOT / "identity-trust-models" / "lifecycle-states.json",
        {
            "id": "identity-lifecycle-states",
            "envelope": envelope("identity-trust-models",
                                 "Six-state identity lifecycle with declared transitions."),
            "states": LIFECYCLE_STATES,
            "state_count": len(LIFECYCLE_STATES),
            "transitions": [
                {"from": a, "to": b, "trigger": t} for (a, b, t) in LIFECYCLE_TRANSITIONS
            ],
            "transition_count": len(LIFECYCLE_TRANSITIONS),
            "auto_promotion_policy": "AUTO-PROMOTION IS FORBIDDEN. Every transition requires a declared trigger and reviewer attestation.",
        },
    )
    write_json(
        GOV_ROOT / "identity-trust-models" / "trust-rules.json",
        {
            "id": "identity-trust-rules",
            "envelope": envelope("identity-trust-models",
                                 "Trust rules anchoring identity confidence to layer-32 trust tiers."),
            "rules": [
                "Identity 'candidate' MAY rely on a single intake event; trust tier inherits the source.",
                "Identity 'probable' MUST cite ≥1 evidence with trust tier ≥ 'reviewer-attested'.",
                "Identity 'validated' MUST cite ≥2 independent evidence sources.",
                "Identity 'canonical' MUST cite ≥1 evidence with trust tier 'oem-direct-evidence' OR equivalent reviewer attestation.",
                "Cross-ecosystem identity links (tuya↔ttlock) MUST require trust tier 'oem-direct-evidence' on at least one source.",
            ],
        },
    )
    write_text(
        GOV_ROOT / "identity-trust-models" / "README.md",
        (
            "# Identity Trust Models\n\n"
            f"{len(LIFECYCLE_STATES)} states, {len(LIFECYCLE_TRANSITIONS)} declared transitions.\n"
            "Auto-promotion is forbidden; every transition requires reviewer governance.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 6 — LINEAGE & PLATFORM GOVERNANCE
# -----------------------------------------------------------------------------

PLATFORM_LINEAGES = [
    {"id": "tuya-ble-platform",
     "ecosystem": "tuya",
     "covers_canonicals": ["e-orbit", "e-prime", "e-flex", "e-nova"],
     "kind": "shared-OEM-platform",
     "evidence_status": "candidate"},
    {"id": "ttlock-platform",
     "ecosystem": "ttlock",
     "covers_canonicals": ["e-touch", "e-shield"],
     "kind": "shared-OEM-platform",
     "evidence_status": "candidate"},
]

LINEAGE_RELATION_KINDS = [
    "variant-of", "generation-of", "white-label-of", "regional-of",
    "platform-sibling-of", "supersedes", "co-developed-with",
]


def task_lineage_governance() -> None:
    write_json(
        LIN_ROOT / "platform-lineages" / "platform-lineages.json",
        {
            "id": "platform-lineages",
            "envelope": envelope("lineage",
                                 "Declared platform lineages. All entries are candidate until reviewer-attested."),
            "lineages": PLATFORM_LINEAGES,
            "lineage_count": len(PLATFORM_LINEAGES),
            "non_promotion_attestation": "All lineages start as 'candidate'; reviewer governance required for promotion.",
        },
    )
    write_json(
        LIN_ROOT / "variant-relationships" / "relation-kinds.json",
        {
            "id": "lineage-relation-kinds",
            "envelope": envelope("lineage",
                                 "Declared kinds of lineage relationships."),
            "kinds": LINEAGE_RELATION_KINDS,
            "kind_count": len(LINEAGE_RELATION_KINDS),
            "rule": "All relationships are directed and append-only.",
        },
    )
    write_json(
        LIN_ROOT / "variant-relationships" / "relationships-store.json",
        {
            "id": "variant-relationships-store",
            "envelope": envelope("lineage",
                                 "Empty store; populated via reviewer-attested intake."),
            "relationships": [],
            "relationship_count": 0,
            "schema": {
                "from_canonical_id": "string",
                "to_canonical_id": "string",
                "relation_kind": "one of relation-kinds",
                "evidence_ids": "list[string]",
                "reviewer": "string",
                "lifecycle_state": "candidate | probable | validated | canonical | deprecated | superseded",
            },
        },
    )
    write_json(
        LIN_ROOT / "generation-evolution" / "generation-schema.json",
        {
            "id": "generation-evolution-schema",
            "envelope": envelope("lineage",
                                 "Schema for hardware/firmware generation evolution chains."),
            "shape": {
                "canonical_id": "string",
                "generation_chain": "list[{generation_label, hardware_rev, firmware_rev, evidence_ids, reviewer}]",
                "supersession_links": "list[{superseded_by_canonical_id, reviewer, at}]",
            },
            "rule": "Generations are append-only; older generations are never deleted.",
        },
    )
    write_json(
        LIN_ROOT / "ecosystem-affiliations" / "ecosystem-affiliations.json",
        {
            "id": "ecosystem-affiliations",
            "envelope": envelope("lineage",
                                 "Per-canonical ecosystem affiliations."),
            "affiliations": [
                {"canonical_id": pid,
                 "ecosystems": CANONICAL_SEED[pid]["ecosystem_affiliations"],
                 "evidence_status": "candidate",
                 "review_required": True}
                for pid in PRODUCTS
            ],
            "ecosystem_classes": ["tuya", "ttlock", "other-shared-platform", "standalone"],
        },
    )
    write_text(
        LIN_ROOT / "README.md",
        (
            "# Lineage Governance\n\n"
            f"{len(PLATFORM_LINEAGES)} declared platform lineages, "
            f"{len(LINEAGE_RELATION_KINDS)} relation kinds.\n"
            "All lineages remain candidate until reviewer-attested.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 7 — CROSS-EVIDENCE SEMANTIC CONTINUITY
# -----------------------------------------------------------------------------

CONTINUITY_SOURCE_FORMATS = [
    "pdf", "xlsx", "csv", "json", "yaml", "md", "html",
    "raster-image", "vector-image", "video", "firmware-bundle",
    "support-ticket", "spreadsheet-export",
]


def task_semantic_continuity() -> None:
    write_json(
        CONT_ROOT / "semantic-continuity" / "continuity-policy.json",
        {
            "id": "semantic-continuity-policy",
            "envelope": envelope("semantic-continuity",
                                 "Policy ensuring future evidence reuses past identity reconciliations."),
            "policy": [
                "Every new evidence intake MUST consult persistent-memory before assigning identity.",
                "If a normalized alias matches a 'validated' or 'canonical' record, the new evidence inherits the canonical_id automatically.",
                "Inheritance is logged in confidence-history and lineage; it is never silent.",
                "If new evidence contradicts an existing validated mapping, it raises a contradiction-event; no auto-revocation.",
                "If no match exists, an 'unresolved-identity' record is raised for reviewer attention.",
                "Continuity inheritance respects layer-34 propagation modes (inherit/override/reject/extend).",
            ],
            "supported_source_formats": CONTINUITY_SOURCE_FORMATS,
            "format_count": len(CONTINUITY_SOURCE_FORMATS),
        },
    )
    write_json(
        CONT_ROOT / "semantic-continuity" / "reuse-rules.json",
        {
            "id": "semantic-continuity-reuse-rules",
            "envelope": envelope("semantic-continuity",
                                 "Rules governing reuse of past reconciliations across evidence sources."),
            "rules": [
                "Reuse is keyed on alias_normalized, not raw alias.",
                "Reuse is keyed on canonical_id, never on commercial_label string match.",
                "Reuse MUST emit a lineage entry citing the persistent-memory record id.",
                "Cross-format reuse (e.g., PDF→video) is permitted; format does not affect identity continuity.",
                "Cross-ecosystem reuse (tuya→ttlock) is FORBIDDEN without explicit reviewer attestation.",
            ],
        },
    )
    write_json(
        GOV_ROOT / "continuity-governance" / "continuity-rules.json",
        {
            "id": "continuity-governance-rules",
            "envelope": envelope("continuity-governance",
                                 "Governance rules surrounding semantic continuity invariants."),
            "rules": [
                "Continuity is append-only; no historical reconciliation is ever deleted.",
                "Contradiction events are first-class lineage entries.",
                "Continuity governance MUST NOT mutate source-of-truth or knowledge-core.",
                "Continuity governance MUST NOT introduce autonomous behaviour, ML, or embeddings.",
                "Continuity governance MUST defer all unresolved cases to reviewer attention.",
            ],
        },
    )
    write_json(
        GOV_ROOT / "propagation-rules" / "propagation-rules.json",
        {
            "id": "identity-propagation-rules",
            "envelope": envelope("propagation-rules",
                                 "How validated identity decisions propagate across the ecosystem."),
            "rules": [
                "Validated identity propagates from persistent-memory into all downstream domain consumers.",
                "Propagation honours the four layer-34 modes: inherit (default), override, reject, extend.",
                "Propagation is read-only with respect to source-of-truth.",
                "Propagation events emit lineage entries.",
                "Propagation MUST NOT cross ecosystem boundaries without reviewer attestation.",
            ],
        },
    )
    write_text(
        CONT_ROOT / "semantic-continuity" / "README.md",
        (
            "# Semantic Continuity\n\n"
            "Persistent reconciliations are reused across PDFs, XLSX, catalogs, firmware, support, video, images.\n"
            "Reuse is always logged; cross-ecosystem reuse requires reviewer attestation.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 8 — FUTURE RUNTIME & PUBLICATION READINESS
# -----------------------------------------------------------------------------

def task_future_readiness() -> None:
    write_json(
        IR_ROOT / "future-runtime-readiness.json",
        {
            "id": "identity-future-runtime-readiness",
            "envelope": envelope("future-runtime-readiness",
                                 "Read-only consumption contract for future runtime, publication, and copilot consumers."),
            "publication_contract": [
                "Publication MUST resolve every product reference to a canonical_id via identity-resolution.",
                "Publication MUST cite the persistent-memory record id when emitting an aliased mention.",
                "Publication MUST NOT render values associated with 'candidate' or 'probable' identities.",
                "Publication MUST honour deprecation/supersession state and surface successor identity when present.",
            ],
            "runtime_contract": [
                "Runtime MAY read canonical-products/ and persistent-memory store (read-only).",
                "Runtime MUST NOT mutate any identity artefact.",
                "Runtime MUST surface confidence_state when displaying alias resolutions.",
                "Runtime MUST defer to reviewer-validations for any contested alias.",
            ],
            "copilot_contract": [
                "Copilot MAY suggest reconciliations; it MUST NOT register identities.",
                "Copilot MUST surface uncertainty as 'requires-review', never as autonomous decision.",
                "Copilot MUST NOT cross ecosystem boundaries when proposing matches.",
                "Copilot MUST cite persistent-memory entries when proposing an alias resolution.",
            ],
            "specification_fusion_contract": [
                "Specification fusion MUST operate on canonical_id, not on aliases.",
                "Specification fusion MUST honour layer-34 propagation modes.",
                "Specification fusion MUST refuse to fuse data across distinct canonical_ids without reviewer attestation.",
            ],
            "non_mutation_attestation": "All contracts are declarative; no consumer is invoked here.",
        },
    )
    write_text(
        IR_ROOT / "README.md",
        (
            "# Identity Resolution\n\n"
            "Layer 35 — product identity, alias governance, persistent reconciliation memory, "
            "lineage governance, and semantic continuity.\n\n"
            f"Canonical products seeded: {len(PRODUCTS)}.\n"
            "All registries begin empty (or unresolved) and grow only via reviewer attestation.\n"
        ),
    )


# -----------------------------------------------------------------------------
# DOCTRINE
# -----------------------------------------------------------------------------

DOCTRINE_DOCS = [
    ("01-identity-singularity-doctrine.md",
     "# Identity Singularity\n\nEvery product has exactly one canonical identity. All other identities (OEM, commercial, reseller, variant, platform, regional) link to it.\n"),
    ("02-no-auto-promotion-doctrine.md",
     "# No Auto-Promotion\n\nIdentity links never auto-promote between lifecycle states. Every transition requires reviewer attestation.\n"),
    ("03-append-only-doctrine.md",
     "# Append-Only\n\nIdentity records, alias registries, lineage edges, persistent memory, and confidence history are append-only. Deletion is forbidden; deprecation is the only closure path.\n"),
    ("04-evidence-anchored-doctrine.md",
     "# Evidence-Anchored\n\nEvery identity link MUST cite layer-32 evidence ids. 'Validated' requires ≥2 independent sources.\n"),
    ("05-non-ml-visual-doctrine.md",
     "# Non-ML Visual Reconciliation\n\nVisual identity matching uses declarative geometry features only. No image recognition, no embeddings, no biometric processing.\n"),
    ("06-cross-ecosystem-firewall-doctrine.md",
     "# Cross-Ecosystem Firewall\n\nIdentity links across ecosystems (tuya↔ttlock) require explicit reviewer attestation and ≥1 OEM-direct evidence source.\n"),
    ("07-continuity-without-overwrite-doctrine.md",
     "# Continuity Without Overwrite\n\nPersistent memory reuses past validated mappings on new intake. Contradictions are surfaced as events; they NEVER silently overwrite the prior mapping.\n"),
    ("08-non-mutation-doctrine.md",
     "# Non-Mutation\n\nThis layer mutates no prior layer. Knowledge-core, source-of-truth, runtime, and publication remain untouched.\n"),
]


def write_doctrine() -> None:
    index_lines = ["# IDENTITY_RESOLUTION_GOVERNANCE\n",
                   "\nLayer 35 — Product identity, alias governance, persistent reconciliation, lineage, continuity.\n",
                   "\n## Doctrine\n"]
    for fname, body in DOCTRINE_DOCS:
        write_text(CONST_ROOT / fname, body)
        index_lines.append(f"- [{fname}]({fname})\n")
    write_text(CONST_ROOT / "00-INDEX.md", "".join(index_lines))
    write_json(
        CONST_ROOT / "manifest.json",
        {
            "id": "identity-resolution-governance-manifest",
            "envelope": envelope("identity-resolution-governance",
                                 "Manifest of identity-resolution doctrine docs."),
            "doctrine_doc_count": len(DOCTRINE_DOCS),
            "doctrine_docs": [name for name, _ in DOCTRINE_DOCS],
            "constitutional_layer_index": 35,
            "subordinate_chain_length": len(SUBORDINATE_TO),
            "schema": SCHEMA,
        },
    )


# -----------------------------------------------------------------------------
# REPORTS
# -----------------------------------------------------------------------------

def write_reports() -> None:
    reports = [
        ("01-product-identity-governance-summary",
         {"identity_kinds": len(IDENTITY_KINDS),
          "canonical_products_seeded": len(PRODUCTS),
          "all_oem_links_unresolved_until_attestation": True},
         f"{len(IDENTITY_KINDS)} identity kinds defined; {len(PRODUCTS)} canonical seeds; OEM links start unresolved."),
        ("02-oem-reconciliation-summary",
         {"registries_initialised": ["manufacturer-models", "sku-reconciliation", "alias-registry",
                                     "unresolved-identities", "deprecated-identities"],
          "auto_population": False,
          "auto_promotion": False},
         "Five OEM/reconciliation registries initialised empty; populated only via reviewer attestation."),
        ("03-persistent-memory-summary",
         {"memory_schema_present": True,
          "memory_store_seeded_empty": True,
          "confidence_history_schema_present": True,
          "validation_protocol_steps": 5},
         "Persistent memory store + schema + confidence-history + 5-step reviewer validation protocol established."),
        ("04-visual-identity-summary",
         {"geometry_features": len(GEOMETRY_FEATURES),
          "image_recognition_used": False,
          "embeddings_used": False,
          "face_or_biometric_used": False},
         f"{len(GEOMETRY_FEATURES)} declarative geometry features; deterministic matching only."),
        ("05-confidence-governance-summary",
         {"lifecycle_states": len(LIFECYCLE_STATES),
          "transitions": len(LIFECYCLE_TRANSITIONS),
          "auto_promotion_forbidden": True},
         f"{len(LIFECYCLE_STATES)} lifecycle states + {len(LIFECYCLE_TRANSITIONS)} declared transitions; auto-promotion forbidden."),
        ("06-lineage-governance-summary",
         {"platform_lineages": len(PLATFORM_LINEAGES),
          "relation_kinds": len(LINEAGE_RELATION_KINDS),
          "all_lineages_candidate_until_attested": True},
         f"{len(PLATFORM_LINEAGES)} platform lineages; {len(LINEAGE_RELATION_KINDS)} relation kinds; all candidate."),
        ("07-semantic-continuity-summary",
         {"supported_source_formats": len(CONTINUITY_SOURCE_FORMATS),
          "cross_format_reuse_allowed": True,
          "cross_ecosystem_reuse_requires_reviewer": True,
          "auto_revocation_on_contradiction": False},
         f"Continuity policy across {len(CONTINUITY_SOURCE_FORMATS)} source formats; contradictions surface as events, never silent revocation."),
        ("08-future-runtime-readiness-summary",
         {"publication_contract_present": True,
          "runtime_contract_present": True,
          "copilot_contract_present": True,
          "specification_fusion_contract_present": True,
          "any_consumer_invoked": False},
         "Four declarative readiness contracts (publication, runtime, copilot, spec-fusion); no consumer invoked."),
        ("09-unresolved-identity-risks",
         {"risks": [
             "All OEM↔canonical mappings are unresolved until reviewer-attested intake begins.",
             "Persistent memory store is empty; no validated alias mappings exist yet.",
             "Platform lineages (tuya, ttlock) remain candidate until OEM evidence is supplied.",
             "Visual signature store is empty; geometry signatures must be human-annotated.",
             "Confidence-history has no entries yet; first entries arrive with the first reviewer triage.",
             "No emitter exists yet for contradiction-events (declarative only).",
         ]},
         "6 unresolved identity risks documented for future remediation phases."),
        ("10-semantic-memory-maturity-reassessment",
         {"layer": 35,
          "subordinate_chain_length": len(SUBORDINATE_TO),
          "identity_kinds": len(IDENTITY_KINDS),
          "canonical_products_seeded": len(PRODUCTS),
          "lifecycle_states": len(LIFECYCLE_STATES),
          "lifecycle_transitions": len(LIFECYCLE_TRANSITIONS),
          "geometry_features": len(GEOMETRY_FEATURES),
          "platform_lineages": len(PLATFORM_LINEAGES),
          "lineage_relation_kinds": len(LINEAGE_RELATION_KINDS),
          "continuity_source_formats": len(CONTINUITY_SOURCE_FORMATS),
          "doctrine_docs": len(DOCTRINE_DOCS),
          "knowledge_core_mutated": False,
          "source_of_truth_mutated": False,
          "runtime_mutated": False,
          "publication_mutated": False,
          "ml_introduced": False,
          "embeddings_introduced": False,
          "face_recognition_introduced": False,
          "autonomous_agents_introduced": False,
          "auto_promotion_introduced": False,
          "tests_status": "19/19 expected"},
         "Layer 35 established. Identity, alias, persistent reconciliation, lineage, and continuity governance in place. Ecosystem ready for long-term identity persistence without bypassing reviewer governance."),
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
    task_product_identity_governance()
    task_oem_reconciliation()
    task_persistent_memory()
    task_visual_identity()
    task_confidence_governance()
    task_lineage_governance()
    task_semantic_continuity()
    task_future_readiness()
    write_doctrine()
    write_reports()
    print("Phase 42 — identity-resolution governance written.")
    print(f"Subordinate chain length: {len(SUBORDINATE_TO)}")
    print(f"Identity kinds: {len(IDENTITY_KINDS)} | Canonicals: {len(PRODUCTS)} | "
          f"Lifecycle states: {len(LIFECYCLE_STATES)} | Transitions: {len(LIFECYCLE_TRANSITIONS)} | "
          f"Geometry features: {len(GEOMETRY_FEATURES)} | Platform lineages: {len(PLATFORM_LINEAGES)} | "
          f"Relation kinds: {len(LINEAGE_RELATION_KINDS)} | Continuity formats: {len(CONTINUITY_SOURCE_FORMATS)}")


if __name__ == "__main__":
    main()
