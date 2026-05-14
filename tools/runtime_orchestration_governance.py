"""
Phase 43 — GOVERNED REFRESH, REBUILD & PROPAGATION ORCHESTRATION.

Constitutional layer 36. Modeling-only. Subordinate to knowledge-core and to
all thirty-five prior governance layers (in particular layer 35 identity-
resolution, layer 34 semantic-domain, layer 33 intake & navigation, layer 32
multimodal evidence).

Writes (idempotent, non-destructive, stdlib-only) under
wp-content/themes/beslock-custom/User manuals/runtime-orchestration/:

  dependency-graph/        (semantic, publication, identity, runtime, propagation)
  refresh-pipelines/       (8 declarative pipelines)
  orchestration/           (5 declarative orchestrator contracts -- NOT executable)
  manifests/               (refresh, propagation, rebuild-history, stale reports)
  lifecycle/               (change-detection, rebuild, propagation, publication)
  governance/              (rebuild, propagation-rules, dependency, refresh-safety)

Plus:
  KNOWLEDGE_BUILDING/RUNTIME_ORCHESTRATION_GOVERNANCE/  (00-INDEX + 8 doctrines + manifest)
  _repository-governance/reports/runtime-orchestration/ (10 reports .json + .md)

Hard rules:
  - Mutates no knowledge-core, no source-of-truth, no runtime, no publication.
  - No CI/CD, no autonomous orchestration, no production automation.
  - No frontend, no ML, no embeddings, no agents.
  - Auto-propagation across canonical/cross-product boundaries is FORBIDDEN
    without reviewer attestation.
  - Reviewer governance is NEVER bypassed.
  - Source-truth is never auto-mutated.
  - 19/19 runtime tests must remain green.

The orchestrator/engine/detector/resolver "scripts" are declared as JSON
contract files (.contract.json) -- NOT executable Python. Production CLI is
DEFERRED.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

RO_ROOT = THEME_ROOT / "runtime-orchestration"
DEP_ROOT = RO_ROOT / "dependency-graph"
PIPE_ROOT = RO_ROOT / "refresh-pipelines"
ORCH_ROOT = RO_ROOT / "orchestration"
MAN_ROOT = RO_ROOT / "manifests"
LIFE_ROOT = RO_ROOT / "lifecycle"
GOV_ROOT = RO_ROOT / "governance"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "RUNTIME_ORCHESTRATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "runtime-orchestration"

SCHEMA = "runtime-orchestration-governance/1.0"
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
    "semantic-domain-governance", "identity-resolution-governance",
]

PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]

# --- Dependency graph nodes & edges (declarative, deterministic) ---
NODE_KINDS = [
    "evidence-source",            # layer-32 multimodal evidence
    "intake-routing",             # layer-33 intake pipeline output
    "candidate-entity",           # extracted candidate
    "knowledge-core",             # validated knowledge
    "identity-record",            # layer-35 canonical / alias
    "semantic-domain",            # layer-34 domain-scoped knowledge
    "specifications-fragment",    # specifications skeleton
    "linguistic-rendering",       # layer-31 publication-time linguistic
    "publication-html",           # layer-30 rendered HTML
    "runtime-index",              # runtime retrieval surface
    "lineage-manifest",           # provenance / lineage record
]

# Dependency edges define DOWNSTREAM relationship: when SOURCE refreshes,
# TARGET must be re-evaluated for staleness.
SEMANTIC_DEP_EDGES = [
    ("evidence-source",      "intake-routing"),
    ("intake-routing",       "candidate-entity"),
    ("candidate-entity",     "knowledge-core"),
    ("knowledge-core",       "specifications-fragment"),
    ("knowledge-core",       "semantic-domain"),
    ("semantic-domain",      "specifications-fragment"),
]

PUBLICATION_DEP_EDGES = [
    ("knowledge-core",       "linguistic-rendering"),
    ("specifications-fragment", "linguistic-rendering"),
    ("identity-record",      "linguistic-rendering"),
    ("linguistic-rendering", "publication-html"),
]

IDENTITY_DEP_EDGES = [
    ("evidence-source",      "identity-record"),
    ("identity-record",      "knowledge-core"),
    ("identity-record",      "lineage-manifest"),
    ("identity-record",      "publication-html"),
]

RUNTIME_DEP_EDGES = [
    ("publication-html",     "runtime-index"),
    ("knowledge-core",       "runtime-index"),
    ("identity-record",      "runtime-index"),
]

PROPAGATION_DEP_EDGES = [
    ("semantic-domain",      "knowledge-core"),
    ("identity-record",      "semantic-domain"),
    ("knowledge-core",       "publication-html"),
    ("publication-html",     "runtime-index"),
]

# --- Refresh pipelines (declarative; each is a JSON contract) ---
REFRESH_PIPELINES = [
    {
        "id": "ingestion-refresh",
        "scope": "evidence-source -> intake-routing",
        "trigger": "new-or-modified-evidence-detected",
        "steps": [
            "detect-evidence-mutation",
            "consult-intake-pipeline-layer-33",
            "classify-evidence-class-layer-32",
            "emit-intake-routing-record",
        ],
        "downstream_invalidates": ["candidate-entity", "identity-record"],
        "auto_promotion": False,
    },
    {
        "id": "extraction-refresh",
        "scope": "intake-routing -> candidate-entity",
        "trigger": "intake-routing-record-changed",
        "steps": [
            "select-extraction-contract-layer-34",
            "deterministic-extract",
            "emit-candidate-entity",
            "defer-to-reviewer-for-validation",
        ],
        "downstream_invalidates": ["knowledge-core"],
        "auto_promotion": False,
    },
    {
        "id": "propagation-refresh",
        "scope": "knowledge-core / semantic-domain / identity-record",
        "trigger": "validated-mutation-detected",
        "steps": [
            "load-propagation-modes-layer-34",
            "load-identity-propagation-rules-layer-35",
            "compute-affected-fragments",
            "emit-propagation-manifest",
        ],
        "downstream_invalidates": ["specifications-fragment", "linguistic-rendering"],
        "auto_promotion": False,
    },
    {
        "id": "publication-refresh",
        "scope": "linguistic-rendering -> publication-html",
        "trigger": "knowledge-core-or-identity-or-spec-changed",
        "steps": [
            "resolve-canonical-ids-layer-35",
            "apply-linguistic-renderers-layer-31",
            "render-html-layer-30",
            "stamp-publication-lineage",
        ],
        "downstream_invalidates": ["runtime-index"],
        "auto_promotion": False,
    },
    {
        "id": "linguistic-refresh",
        "scope": "linguistic-rendering only",
        "trigger": "terminology-or-warning-language-rule-updated",
        "steps": [
            "reload-terminology-rules",
            "reload-warning-language-rules",
            "re-render-linguistic-layer",
            "trigger-publication-refresh",
        ],
        "downstream_invalidates": ["publication-html", "runtime-index"],
        "auto_promotion": False,
    },
    {
        "id": "html-regeneration",
        "scope": "publication-html only",
        "trigger": "renderer-template-or-style-rule-changed",
        "steps": [
            "diff-template-version",
            "regenerate-affected-pages",
            "stamp-publication-lineage",
        ],
        "downstream_invalidates": ["runtime-index"],
        "auto_promotion": False,
    },
    {
        "id": "runtime-refresh",
        "scope": "runtime-index only",
        "trigger": "publication-html-changed-or-knowledge-core-validated",
        "steps": [
            "diff-publication-set",
            "rebuild-runtime-index",
            "emit-runtime-rebuild-event",
        ],
        "downstream_invalidates": [],
        "auto_promotion": False,
    },
    {
        "id": "lineage-refresh",
        "scope": "lineage-manifest",
        "trigger": "identity-or-supersession-event",
        "steps": [
            "append-lineage-event",
            "validate-no-overwrite",
            "publish-manifest-version-bump",
        ],
        "downstream_invalidates": ["publication-html", "runtime-index"],
        "auto_promotion": False,
    },
]

# --- Orchestration contracts (NOT executable) ---
ORCH_CONTRACTS = [
    {
        "id": "refresh-orchestrator",
        "role": "Coordinate which pipelines run, in which order, for a given change-set",
        "inputs": ["change-detection-report", "dependency-graph", "scope-request"],
        "outputs": ["refresh-manifest"],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": True,
    },
    {
        "id": "propagation-engine",
        "role": "Apply propagation modes deterministically from a validated mutation",
        "inputs": ["validated-mutation", "propagation-rules-layer-34", "identity-rules-layer-35"],
        "outputs": ["propagation-manifest"],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": True,
    },
    {
        "id": "stale-detector",
        "role": "Identify outputs whose dependencies have advanced past their lineage stamp",
        "inputs": ["dependency-graph", "publication-lineage", "runtime-index-lineage"],
        "outputs": ["stale-output-report"],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": False,
    },
    {
        "id": "dependency-resolver",
        "role": "Compute the minimal downstream set affected by a given upstream change",
        "inputs": ["change-set", "dependency-graph"],
        "outputs": ["affected-node-set"],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": False,
    },
    {
        "id": "rebuild-manifest-generator",
        "role": "Produce a deterministic, reviewer-approvable rebuild plan",
        "inputs": ["affected-node-set", "scope-request"],
        "outputs": ["rebuild-manifest"],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": True,
    },
]

# --- Change detection ---
CHANGE_KINDS = [
    "new-evidence",
    "modified-evidence",
    "updated-mapping",
    "terminology-rule-change",
    "specification-update",
    "propagation-update",
    "stale-publication",
    "stale-runtime-output",
]

# --- Stale output classes ---
STALE_CLASSES = [
    "stale-html",
    "outdated-publication",
    "unresolved-rebuild",
    "dependency-mismatch",
    "propagation-gap",
    "terminology-drift",
    "outdated-lineage-manifest",
]

# --- Incremental rebuild scopes ---
REBUILD_SCOPES = [
    {"id": "product-scope",   "selector": "single canonical product (e.g. e-nova)"},
    {"id": "domain-scope",    "selector": "single semantic domain (e.g. specifications)"},
    {"id": "publication-scope", "selector": "publication-html for a slice"},
    {"id": "runtime-scope",   "selector": "runtime-index for a slice"},
    {"id": "portfolio-scope", "selector": "portfolio-level domains only"},
]

# --- Future CLI commands (declarative; NOT implemented) ---
FUTURE_CLI = [
    {
        "command": "refresh publication-system --linguistic",
        "resolves_to_pipelines": ["linguistic-refresh", "publication-refresh"],
        "scope": "publication-scope",
        "reviewer_authorization_required": True,
    },
    {
        "command": "refresh identity-resolution --propagate",
        "resolves_to_pipelines": ["propagation-refresh", "publication-refresh", "runtime-refresh"],
        "scope": "domain-scope (identity-resolution)",
        "reviewer_authorization_required": True,
    },
    {
        "command": "refresh e-nova --domain specifications",
        "resolves_to_pipelines": ["extraction-refresh", "propagation-refresh", "publication-refresh"],
        "scope": "product-scope=e-nova / domain-scope=specifications",
        "reviewer_authorization_required": True,
    },
    {
        "command": "refresh portfolio-level --structured-evidence",
        "resolves_to_pipelines": ["ingestion-refresh", "extraction-refresh", "propagation-refresh"],
        "scope": "portfolio-scope",
        "reviewer_authorization_required": True,
    },
]

# --- Refresh safety rules ---
SAFETY_RULES = [
    {"id": "no-uncontrolled-propagation",
     "rule": "Propagation only fires after a reviewer-validated mutation; layer-34 propagation modes apply."},
    {"id": "no-stale-semantic-reuse",
     "rule": "Identity-resolution memory must be re-consulted on every refresh; stale alias mappings are not reused."},
    {"id": "no-rebuild-loops",
     "rule": "Each refresh manifest must declare a strictly downstream node set; cycles are rejected by dependency-resolver."},
    {"id": "no-cross-product-contamination",
     "rule": "Product-scope rebuilds may not write to fragments owned by other canonical products."},
    {"id": "no-invalid-lineage-refresh",
     "rule": "lineage-manifest is append-only; lineage-refresh may never overwrite or delete lineage events."},
    {"id": "no-publication-runtime-divergence",
     "rule": "runtime-refresh may not run while publication-refresh of the same slice is unresolved."},
    {"id": "no-source-truth-mutation",
     "rule": "No pipeline may write to source-of-truth; source-of-truth is human-curated only."},
    {"id": "reviewer-authorization-required",
     "rule": "Any refresh that crosses canonical boundaries or touches identity-resolution requires reviewer authorization."},
]

# --- Doctrine docs ---
DOCTRINE = [
    ("01-deterministic-refresh-doctrine.md",
     "Deterministic refresh doctrine",
     "Every refresh is the deterministic image of a declared change-set against the dependency-graph. "
     "No refresh runs without a recorded upstream change. Outputs are reproducible: same change-set + "
     "same governance state -> same refresh-manifest."),
    ("02-dependency-graph-doctrine.md",
     "Dependency-graph doctrine",
     "Dependencies are declared, not inferred. The graph is the single source of truth for what is "
     "downstream of what. Any node not declared in the graph is treated as having NO dependents and "
     "MUST be reviewer-attested before being added."),
    ("03-incremental-rebuild-doctrine.md",
     "Incremental-rebuild doctrine",
     "The default rebuild scope is the smallest scope that satisfies the change-set. Whole-ecosystem "
     "rebuilds are exceptional and require reviewer authorization."),
    ("04-propagation-discipline-doctrine.md",
     "Propagation-discipline doctrine",
     "Propagation runs only after a reviewer-validated mutation, applies layer-34 propagation modes, "
     "honours layer-35 identity rules, and never crosses ecosystem boundaries silently."),
    ("05-stale-output-doctrine.md",
     "Stale-output doctrine",
     "Outputs are stale when their lineage stamp is older than any of their declared upstream nodes. "
     "Stale detection is a query, never an automatic rebuild."),
    ("06-non-execution-doctrine.md",
     "Non-execution doctrine",
     "Phase 43 produces governance and contracts. Orchestrator, engine, detector, resolver, and "
     "manifest-generator are declared as JSON contracts, NOT runnable code. Production CLI is deferred."),
    ("07-non-mutation-doctrine.md",
     "Non-mutation doctrine",
     "Refresh orchestration never mutates knowledge-core, source-of-truth, runtime, or publication "
     "without an explicit reviewer-authorized refresh-manifest."),
    ("08-safety-doctrine.md",
     "Safety doctrine",
     "Refresh safety rules (no uncontrolled propagation, no rebuild loops, no cross-product "
     "contamination, no lineage rewrite, no publication/runtime divergence, no source-truth mutation, "
     "reviewer authorization for cross-canonical refresh) are unconditional."),
]


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def envelope(extra: dict = None) -> dict:
    base = {
        "schema": SCHEMA,
        "constitutional_layer_index": 36,
        "subordinate_to": list(SUBORDINATE_TO),
        "updated_at": NOW,
        "modeling_only": True,
        "executable": False,
        "introduces_autonomous_agents": False,
        "introduces_ci_cd": False,
        "auto_mutates_source_truth": False,
        "auto_propagates_across_canonicals": False,
        "bypasses_reviewer_governance": False,
    }
    if extra:
        base.update(extra)
    return base


# ----------------------------------------------------------------------------
# TASK 1 — DEPENDENCY GRAPH GOVERNANCE
# ----------------------------------------------------------------------------
def _edges(edges):
    return [{"from": s, "to": t} for s, t in edges]


def task_dependency_graph() -> None:
    write_json(DEP_ROOT / "semantic-dependencies.json", {
        **envelope(),
        "node_kinds": NODE_KINDS,
        "edges": _edges(SEMANTIC_DEP_EDGES),
        "notes": "Semantic dependencies trace evidence -> candidate -> knowledge-core -> domain/specs.",
    })
    write_json(DEP_ROOT / "publication-dependencies.json", {
        **envelope(),
        "edges": _edges(PUBLICATION_DEP_EDGES),
        "notes": "Publication depends on knowledge-core, specifications, and identity records.",
    })
    write_json(DEP_ROOT / "identity-dependencies.json", {
        **envelope(),
        "edges": _edges(IDENTITY_DEP_EDGES),
        "notes": "Identity changes ripple into knowledge-core, lineage, and publication.",
    })
    write_json(DEP_ROOT / "runtime-dependencies.json", {
        **envelope(),
        "edges": _edges(RUNTIME_DEP_EDGES),
        "notes": "Runtime index depends on publication, knowledge-core, and identity.",
    })
    write_json(DEP_ROOT / "propagation-dependencies.json", {
        **envelope(),
        "edges": _edges(PROPAGATION_DEP_EDGES),
        "notes": "Propagation paths used by propagation-engine to compute downstream invalidations.",
    })
    write_text(DEP_ROOT / "README.md",
        "# Dependency graph\n\n"
        "Declarative dependency graph for the ecosystem. Edges are DOWNSTREAM "
        "relationships: when SOURCE changes, TARGET must be re-evaluated.\n\n"
        "Files:\n"
        "- semantic-dependencies.json\n"
        "- publication-dependencies.json\n"
        "- identity-dependencies.json\n"
        "- runtime-dependencies.json\n"
        "- propagation-dependencies.json\n")


# ----------------------------------------------------------------------------
# TASK 2 — DETERMINISTIC REFRESH ORCHESTRATION
# ----------------------------------------------------------------------------
def task_refresh_pipelines() -> None:
    for pipe in REFRESH_PIPELINES:
        sub = PIPE_ROOT / pipe["id"]
        write_json(sub / "pipeline.json", {**envelope(), **pipe})
        write_text(sub / "README.md",
            f"# {pipe['id']}\n\n"
            f"Scope: {pipe['scope']}\n\n"
            f"Trigger: {pipe['trigger']}\n\n"
            f"Auto-promotion: {pipe['auto_promotion']}\n")
    write_json(PIPE_ROOT / "_index.json", {
        **envelope(),
        "pipelines": [p["id"] for p in REFRESH_PIPELINES],
        "count": len(REFRESH_PIPELINES),
    })


# ----------------------------------------------------------------------------
# TASK 3 — CHANGE DETECTION GOVERNANCE
# ----------------------------------------------------------------------------
def task_change_detection() -> None:
    cd_root = LIFE_ROOT / "change-detection"
    write_json(cd_root / "change-kinds.json", {
        **envelope(),
        "change_kinds": CHANGE_KINDS,
    })
    write_json(cd_root / "detection-rules.json", {
        **envelope(),
        "rules": [
            {"id": "evidence-hash-changed",
             "applies_to": "evidence-source",
             "signal": "deterministic content-hash differs from last lineage stamp"},
            {"id": "mapping-record-appended",
             "applies_to": "identity-record",
             "signal": "new alias / OEM mapping appended to layer-35 stores"},
            {"id": "terminology-rule-version-bumped",
             "applies_to": "linguistic-rendering",
             "signal": "linguistic-governance terminology rule version changed"},
            {"id": "specification-fragment-validated",
             "applies_to": "specifications-fragment",
             "signal": "reviewer-attested validation event recorded"},
            {"id": "propagation-rule-updated",
             "applies_to": "semantic-domain",
             "signal": "layer-34 propagation rule version bumped"},
            {"id": "publication-lineage-older-than-upstream",
             "applies_to": "publication-html",
             "signal": "publication lineage stamp predates upstream lineage stamp"},
            {"id": "runtime-lineage-older-than-publication",
             "applies_to": "runtime-index",
             "signal": "runtime-index lineage predates publication lineage"},
        ],
        "auto_action": "none",
        "emits": "change-detection-report (consumed by refresh-orchestrator)",
    })
    write_text(cd_root / "README.md",
        "# Change detection\n\nDeclarative signals only. Detection NEVER triggers "
        "a refresh automatically -- it emits a change-detection-report consumed by "
        "the refresh-orchestrator under reviewer authorization.\n")


# ----------------------------------------------------------------------------
# TASK 4 — PROPAGATION ORCHESTRATION
# ----------------------------------------------------------------------------
def task_propagation() -> None:
    write_json(ORCH_ROOT / "propagation-engine.contract.json", {
        **envelope({"contract_kind": "propagation-engine"}),
        "role": "Apply propagation modes deterministically to a validated mutation.",
        "inputs": [
            "validated-mutation (with reviewer attestation)",
            "layer-34 propagation-modes + propagation-rules",
            "layer-35 identity-rules + propagation-rules",
            "dependency-graph/propagation-dependencies.json",
        ],
        "outputs": [
            "propagation-manifest (one per mutation, append-only)",
            "downstream-invalidation-set",
        ],
        "propagation_targets": [
            "shared-semantics", "specifications", "warnings", "workflows",
            "identity-mappings", "publication-systems", "runtime-retrieval",
        ],
        "executable": False,
        "production_ready": False,
        "reviewer_authorization_required": True,
        "auto_propagates_across_canonicals": False,
    })
    pm_root = MAN_ROOT / "propagation-manifests"
    write_json(pm_root / "propagation-manifest-schema.json", {
        **envelope(),
        "shape": {
            "manifest_id": "string (uuid-like, deterministic from inputs)",
            "mutation_id": "string (id of the validated mutation)",
            "reviewer_attestation_id": "string",
            "source_node": "string (one of NODE_KINDS)",
            "downstream_invalidations": "array<{node, scope, reason}>",
            "propagation_modes_applied": "array<{mode, rule_id}>",
            "emitted_at": "ISO-8601 UTC",
            "executed": "boolean (always false in modeling-only state)",
        },
        "append_only": True,
    })
    write_json(pm_root / "manifest-store.json", {
        **envelope(),
        "manifests": [],
        "policy": "Append-only. Manifests are NEVER deleted or rewritten.",
    })


# ----------------------------------------------------------------------------
# TASK 5 — STALE OUTPUT DETECTION
# ----------------------------------------------------------------------------
def task_stale_detection() -> None:
    write_json(ORCH_ROOT / "stale-detector.contract.json", {
        **envelope({"contract_kind": "stale-detector"}),
        "role": "Identify outputs whose lineage stamp is older than any upstream node lineage.",
        "stale_classes": STALE_CLASSES,
        "inputs": [
            "dependency-graph/*.json",
            "publication-lineage stamps",
            "runtime-index lineage",
            "lineage-manifests",
        ],
        "outputs": ["stale-output-report (one per scan, append-only)"],
        "auto_rebuild": False,
        "executable": False,
        "production_ready": False,
    })
    sr_root = MAN_ROOT / "stale-output-reports"
    write_json(sr_root / "report-schema.json", {
        **envelope(),
        "shape": {
            "report_id": "string",
            "scanned_at": "ISO-8601 UTC",
            "stale_entries": "array<{node, kind, upstream_node, lineage_gap}>",
            "auto_action": "none",
            "reviewer_review_required": True,
        },
    })
    write_json(sr_root / "report-store.json", {
        **envelope(),
        "reports": [],
        "policy": "Append-only. Stale reports are evidence, not triggers.",
    })


# ----------------------------------------------------------------------------
# TASK 6 — INCREMENTAL REBUILD GOVERNANCE
# ----------------------------------------------------------------------------
def task_incremental_rebuild() -> None:
    ir_root = GOV_ROOT / "incremental-rebuild-governance"
    write_json(ir_root / "rebuild-scopes.json", {
        **envelope(),
        "scopes": REBUILD_SCOPES,
    })
    write_json(ir_root / "rebuild-rules.json", {
        **envelope(),
        "rules": [
            {"id": "smallest-sufficient-scope",
             "rule": "The dependency-resolver must select the smallest scope that satisfies the change-set."},
            {"id": "scope-isolation",
             "rule": "A product-scope rebuild may not write to fragments owned by another canonical product."},
            {"id": "domain-scope-respects-propagation-modes",
             "rule": "Domain-scope rebuilds must honour layer-34 propagation modes (inherit/override/reject/extend)."},
            {"id": "publication-scope-requires-canonical-resolution",
             "rule": "Publication-scope rebuilds must resolve canonical_id via layer-35 before rendering."},
            {"id": "runtime-scope-follows-publication",
             "rule": "Runtime-scope rebuilds may only run on the slice already covered by a fresh publication."},
            {"id": "portfolio-scope-requires-reviewer",
             "rule": "Portfolio-scope rebuilds always require reviewer authorization."},
        ],
    })
    write_json(ir_root / "rebuild-manifest-schema.json", {
        **envelope(),
        "shape": {
            "manifest_id": "string",
            "scope": "one of REBUILD_SCOPES.id",
            "selector": "string (e.g. canonical_id, domain_id)",
            "pipelines": "array<refresh-pipeline-id>",
            "downstream_invalidations": "array<node>",
            "reviewer_authorization_id": "string (required for portfolio-scope and cross-canonical)",
            "emitted_at": "ISO-8601 UTC",
            "executed": "boolean (always false in modeling-only state)",
        },
    })
    rh_root = MAN_ROOT / "rebuild-history"
    write_json(rh_root / "history-store.json", {
        **envelope(),
        "history": [],
        "policy": "Append-only. Each rebuild emits one history entry; history is never rewritten.",
    })
    rm_root = MAN_ROOT / "refresh-manifests"
    write_json(rm_root / "refresh-manifest-store.json", {
        **envelope(),
        "manifests": [],
        "policy": "Append-only.",
    })


# ----------------------------------------------------------------------------
# TASK 7 — FUTURE CLI & OPERATOR READINESS
# ----------------------------------------------------------------------------
def task_future_cli() -> None:
    cli_root = RO_ROOT / "future-cli-readiness"
    write_json(cli_root / "future-commands.json", {
        **envelope({"production_ready": False}),
        "commands": FUTURE_CLI,
        "notes": "Declarative only. No CLI is implemented in phase 43.",
    })
    write_json(cli_root / "operator-protocol.json", {
        **envelope(),
        "protocol_steps": [
            "operator-prepares-change-set",
            "change-detection emits change-detection-report",
            "dependency-resolver computes affected-node-set",
            "rebuild-manifest-generator drafts a rebuild-manifest",
            "reviewer authorizes the manifest",
            "refresh-orchestrator (future) executes the manifest deterministically",
            "stale-detector confirms no remaining staleness in scope",
        ],
        "reviewer_authorization_required": True,
    })
    write_text(cli_root / "README.md",
        "# Future CLI readiness\n\n"
        "Declarative contracts for future operator commands. NO CLI is implemented; "
        "no automation runs. Reviewer authorization is required for every scoped refresh.\n")


# ----------------------------------------------------------------------------
# TASK 8 — REFRESH SAFETY & GOVERNANCE
# ----------------------------------------------------------------------------
def task_refresh_safety() -> None:
    rs_root = GOV_ROOT / "refresh-safety"
    write_json(rs_root / "safety-rules.json", {
        **envelope(),
        "rules": SAFETY_RULES,
        "enforcement": "All rules are unconditional. Violations block manifest emission.",
    })
    write_json(GOV_ROOT / "rebuild-governance" / "rebuild-rules.json", {
        **envelope(),
        "rules": [
            {"id": "no-implicit-rebuild",
             "rule": "Rebuilds occur only via an authorized rebuild-manifest."},
            {"id": "deterministic-output",
             "rule": "Same change-set + same governance state must yield the same rebuild-manifest."},
            {"id": "non-mutation-of-source-truth",
             "rule": "Rebuilds never write to source-of-truth."},
        ],
    })
    write_json(GOV_ROOT / "propagation-rules" / "propagation-orchestration-rules.json", {
        **envelope(),
        "rules": [
            {"id": "propagation-after-validation-only",
             "rule": "Propagation runs only after a reviewer-validated mutation."},
            {"id": "propagation-honours-layer-34-modes",
             "rule": "Propagation applies layer-34 propagation modes (inherit/override/reject/extend)."},
            {"id": "propagation-honours-layer-35-identity",
             "rule": "Propagation honours layer-35 identity-resolution rules; cross-ecosystem reuse forbidden without reviewer."},
        ],
    })
    write_json(GOV_ROOT / "dependency-governance" / "dependency-rules.json", {
        **envelope(),
        "rules": [
            {"id": "declared-only",
             "rule": "Only edges declared in dependency-graph/*.json are considered. Undeclared edges do not exist."},
            {"id": "acyclic",
             "rule": "Dependency graph must remain acyclic; cycles are rejected by dependency-resolver."},
            {"id": "additive",
             "rule": "Edges are added by reviewer-attested governance change only; never auto-discovered."},
        ],
    })


# ----------------------------------------------------------------------------
# Lifecycle skeletons (rebuild / propagation / publication)
# ----------------------------------------------------------------------------
def task_lifecycle_skeletons() -> None:
    write_json(LIFE_ROOT / "rebuild-lifecycle" / "rebuild-states.json", {
        **envelope(),
        "states": ["requested", "manifest-drafted", "reviewer-authorized",
                   "executed", "verified", "rejected"],
        "transitions": [
            {"from": "requested",          "to": "manifest-drafted",     "trigger": "rebuild-manifest-generator"},
            {"from": "manifest-drafted",   "to": "reviewer-authorized",  "trigger": "reviewer-attestation"},
            {"from": "manifest-drafted",   "to": "rejected",             "trigger": "reviewer-rejection or safety-violation"},
            {"from": "reviewer-authorized","to": "executed",             "trigger": "future-cli (deferred)"},
            {"from": "executed",           "to": "verified",             "trigger": "stale-detector confirms no residual staleness"},
        ],
    })
    write_json(LIFE_ROOT / "propagation-lifecycle" / "propagation-states.json", {
        **envelope(),
        "states": ["pending-validation", "validated", "manifest-emitted",
                   "downstream-invalidated", "completed"],
        "transitions": [
            {"from": "pending-validation",   "to": "validated",             "trigger": "reviewer-attestation"},
            {"from": "validated",            "to": "manifest-emitted",      "trigger": "propagation-engine"},
            {"from": "manifest-emitted",     "to": "downstream-invalidated","trigger": "dependency-resolver"},
            {"from": "downstream-invalidated","to": "completed",            "trigger": "all downstream pipelines refreshed"},
        ],
    })
    write_json(LIFE_ROOT / "publication-lifecycle" / "publication-states.json", {
        **envelope(),
        "states": ["upstream-stable", "publication-stale", "republishing",
                   "published", "verified"],
        "transitions": [
            {"from": "upstream-stable",   "to": "publication-stale", "trigger": "stale-detector"},
            {"from": "publication-stale", "to": "republishing",      "trigger": "publication-refresh pipeline"},
            {"from": "republishing",      "to": "published",         "trigger": "html-regeneration completed"},
            {"from": "published",         "to": "verified",          "trigger": "runtime-refresh confirmed"},
        ],
    })


# ----------------------------------------------------------------------------
# Orchestration contracts (refresh-orchestrator, dependency-resolver, rebuild-manifest-generator)
# ----------------------------------------------------------------------------
def task_orchestration_contracts() -> None:
    for c in ORCH_CONTRACTS:
        write_json(ORCH_ROOT / f"{c['id']}.contract.json", {
            **envelope({"contract_kind": c["id"]}),
            **c,
        })
    write_text(ORCH_ROOT / "README.md",
        "# Orchestration contracts\n\n"
        "These files declare the contracts of future orchestration components. "
        "They are NOT executable. Production CLI / runtime execution is deferred.\n\n"
        "Contracts: refresh-orchestrator, propagation-engine, stale-detector, "
        "dependency-resolver, rebuild-manifest-generator.\n")


# ----------------------------------------------------------------------------
# Doctrine + reports
# ----------------------------------------------------------------------------
def write_doctrine() -> None:
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(CONST_ROOT / "00-INDEX.md",
        "# Runtime orchestration governance — doctrine\n\n"
        + "\n".join(f"- {fname}" for fname, _, _ in DOCTRINE) + "\n")
    for fname, title, body in DOCTRINE:
        write_text(CONST_ROOT / fname, f"# {title}\n\n{body}\n")
    write_json(CONST_ROOT / "manifest.json", {
        **envelope(),
        "doctrine_files": [fname for fname, _, _ in DOCTRINE],
        "count": len(DOCTRINE),
    })


def write_reports() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    reports = [
        ("01-dependency-graph-summary",
         {"node_kinds_count": len(NODE_KINDS),
          "semantic_edges": len(SEMANTIC_DEP_EDGES),
          "publication_edges": len(PUBLICATION_DEP_EDGES),
          "identity_edges": len(IDENTITY_DEP_EDGES),
          "runtime_edges": len(RUNTIME_DEP_EDGES),
          "propagation_edges": len(PROPAGATION_DEP_EDGES)},
         "Declarative dependency graph spanning 11 node kinds across 5 dependency files."),
        ("02-deterministic-refresh-summary",
         {"pipelines": [p["id"] for p in REFRESH_PIPELINES],
          "count": len(REFRESH_PIPELINES)},
         "8 declarative refresh pipelines (ingestion, extraction, propagation, publication, "
         "linguistic, html-regeneration, runtime, lineage). All non-executing."),
        ("03-change-detection-summary",
         {"change_kinds": CHANGE_KINDS,
          "detection_rules": 7,
          "auto_action": "none"},
         "Change detection emits reports only; never triggers refresh automatically."),
        ("04-propagation-orchestration-summary",
         {"engine": "propagation-engine.contract.json",
          "manifests_store": "propagation-manifests/manifest-store.json",
          "append_only": True,
          "auto_propagates_across_canonicals": False},
         "Propagation engine declared as contract; manifest store append-only; reviewer required."),
        ("05-stale-output-detection-summary",
         {"stale_classes": STALE_CLASSES,
          "detector": "stale-detector.contract.json",
          "auto_rebuild": False},
         "Stale-detector identifies 7 stale classes; outputs reports, never rebuilds automatically."),
        ("06-incremental-rebuild-summary",
         {"scopes": [s["id"] for s in REBUILD_SCOPES],
          "rules": 6,
          "history_store_append_only": True},
         "Five rebuild scopes (product/domain/publication/runtime/portfolio) with isolation rules."),
        ("07-future-cli-readiness-summary",
         {"commands": [c["command"] for c in FUTURE_CLI],
          "production_ready": False,
          "reviewer_authorization_required": True},
         "Four future operator commands declared. No CLI implemented; reviewer required."),
        ("08-refresh-safety-summary",
         {"rules": [r["id"] for r in SAFETY_RULES],
          "count": len(SAFETY_RULES),
          "enforcement": "unconditional"},
         "Eight unconditional safety rules; violations block manifest emission."),
        ("09-unresolved-orchestration-risks",
         {"risks": [
            "No orchestrator/engine/detector/resolver is yet executable; manifests cannot be enacted.",
            "Change-detection signals require an emitter; none is wired yet.",
            "Lineage stamps must be present on all upstream nodes before stale-detector is meaningful.",
            "Reviewer authorization workflow is declared but not wired to a UI/CLI.",
            "Cross-canonical refresh paths exist in the graph but are intentionally gated; no fast-path.",
            "Propagation manifest store starts empty; first manifest awaits the first validated mutation.",
            "Runtime-index lineage discipline is not yet uniformly stamped across runtime artifacts.",
         ]},
         "Seven unresolved risks documented; all reviewer-gated, none auto-actionable."),
        ("10-ecosystem-lifecycle-maturity-reassessment",
         {"layer": 36,
          "subordinate_chain_length": len(SUBORDINATE_TO),
          "pipelines": len(REFRESH_PIPELINES),
          "scopes": len(REBUILD_SCOPES),
          "safety_rules": len(SAFETY_RULES),
          "doctrines": len(DOCTRINE),
          "knowledge_core_untouched": True,
          "source_of_truth_untouched": True,
          "runtime_untouched": True,
          "publication_untouched": True,
          "ml_introduced": False,
          "agents_introduced": False,
          "ci_cd_introduced": False},
         "Ecosystem now has a deterministic refresh, propagation, and rebuild governance layer. "
         "Modeling-only. Ready to receive a future reviewer-authorized CLI."),
    ]
    for slug, payload, summary in reports:
        write_json(REPORTS_ROOT / f"{slug}.json", {**envelope(), **payload, "summary": summary})
        write_text(REPORTS_ROOT / f"{slug}.md", f"# {slug}\n\n{summary}\n")


def write_root_readme() -> None:
    write_text(RO_ROOT / "README.md",
        "# runtime-orchestration\n\n"
        "Phase 43 — governed refresh, rebuild & propagation orchestration. "
        "Modeling-only. No executable orchestrator. No CI/CD. No autonomous agents. "
        "No source-truth mutation. Reviewer authorization required for every scoped refresh.\n\n"
        "Subroots:\n"
        "- dependency-graph/\n"
        "- refresh-pipelines/\n"
        "- orchestration/ (contracts, NOT executable)\n"
        "- manifests/ (refresh, propagation, rebuild-history, stale reports; append-only)\n"
        "- lifecycle/ (change-detection, rebuild, propagation, publication)\n"
        "- governance/ (rebuild, propagation-rules, dependency, refresh-safety)\n"
        "- future-cli-readiness/\n")


def main() -> None:
    task_dependency_graph()
    task_refresh_pipelines()
    task_change_detection()
    task_propagation()
    task_stale_detection()
    task_incremental_rebuild()
    task_future_cli()
    task_refresh_safety()
    task_lifecycle_skeletons()
    task_orchestration_contracts()
    write_doctrine()
    write_reports()
    write_root_readme()
    print("Phase 43 — runtime-orchestration governance written.")
    print(f"Subordinate chain length: {len(SUBORDINATE_TO)}")
    print(
        f"Node kinds: {len(NODE_KINDS)} | "
        f"Pipelines: {len(REFRESH_PIPELINES)} | "
        f"Scopes: {len(REBUILD_SCOPES)} | "
        f"Safety rules: {len(SAFETY_RULES)} | "
        f"Future CLI: {len(FUTURE_CLI)} | "
        f"Doctrines: {len(DOCTRINE)}"
    )


if __name__ == "__main__":
    main()
