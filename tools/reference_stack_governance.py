"""
Phase 32 — REFERENCE STACK & OPERATIONAL CONVERGENCE.

Constitutional layer 26. Modeling-only. Subordinate to knowledge-core and
to all twenty-five prior governance layers.

Writes:
  - the six reference-stack artifact folders under
    `wp-content/themes/beslock-custom/User manuals/reference-stack/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/REFERENCE_STACK_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/reference-stack/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
No production deployment, no infrastructure automation, no frontends,
no autonomous systems.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
STACK_ROOT = THEME_ROOT / "reference-stack"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "REFERENCE_STACK_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "reference-stack"

SCHEMA = "reference-stack-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items): return "\n".join(f"- {x}" for x in items)


def write_pair(folder: Path, slug: str, title: str, intro: str, sections, payload: dict):
    folder.mkdir(parents=True, exist_ok=True)
    md = [f"# {title}", "", intro, ""]
    for h, body in sections:
        md += [f"## {h}", "", body, ""]
    (folder / f"{slug}.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    (folder / f"{slug}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


SUBORDINATE_TO = [
    "knowledge-core",
    "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
    "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
    "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
    "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
    "ECOSYSTEM_INTEROPERABILITY", "REALIZATION_AND_DEPLOYMENT",
    "OPERATIONAL_PROOF", "PROTOTYPE_RUNTIME", "RUNTIME_IMPLEMENTATION",
    "RUNTIME_HARDENING", "KNOWLEDGE_LIFECYCLE", "KNOWLEDGE_OPERATIONS",
    "HUMAN_OPERATIONS", "ENVIRONMENT_AND_INTEGRATION",
]


# =============================================================================
# TASK 1 — CANONICAL REFERENCE STACK
# =============================================================================

CANONICAL_STACK = [
    {"id": "retrieval-runtime",     "module": "runtime-implementation/runtime/retrieval.py", "responsibility": "kind→domain routing, Jaccard scoring, confidence weighting, candidate-only marker"},
    {"id": "orchestration-runtime", "module": "runtime-implementation/runtime/flows.py + runtime/assembly.py", "responsibility": "supervised flow composition, package assembly, escalation evaluation"},
    {"id": "escalation-runtime",    "module": "runtime-implementation/runtime/assembly.py (_evaluate_escalation) + escalation-trace channel", "responsibility": "trigger evaluation, halt semantics, candidate-only routing"},
    {"id": "provenance-system",     "module": "ext-images/<product>/knowledge-core/**/*.json + manifest_id + source_files[].sha256", "responsibility": "write-once provenance records; read-only into all sandboxes"},
    {"id": "replay-system",         "module": "runtime-implementation/runtime/replay.py + cli.py replay subcommand", "responsibility": "deterministic re-execution against frozen orchestration-trace"},
    {"id": "reviewer-operations",   "module": "knowledge-operations/reviewer-workbench/ + review-queues/ (design-only, layer 23)", "responsibility": "queue, claim, evidence, decision, audit"},
    {"id": "governance-operations", "module": "knowledge-operations/governance-workflows/ + KNOWLEDGE_BUILDING/* (design-only)", "responsibility": "scope assignment, revocation, dual-audit, emergency intervention"},
    {"id": "oem-ingestion-system",  "module": "knowledge-operations/oem-operations/ + ingestion env (design-only)", "responsibility": "checksum-verified ingest, dual-review binding, supersession"},
    {"id": "observability-system",  "module": "runtime-implementation/runtime/channels.py (NDJSON channels)", "responsibility": "append-only event streams: orchestration, retrieval, escalation, continuity, replay, incident"},
]

STACK_INVARIANTS = [
    "every module declares its responsibility, its inputs, and its outputs",
    "no module owns provenance writes except the governance pipeline",
    "no module emits effects outside its declared responsibility",
    "every module is traceable end-to-end via the observability system",
    "every module is replaceable by a substitute that satisfies the same contract",
]


# =============================================================================
# TASK 2 — MODULE TOPOLOGY
# =============================================================================

MODULE_RELATIONSHIPS = [
    {"from": "orchestration-runtime", "to": "retrieval-runtime",     "kind": "synchronous-call",       "contract": "retrieve(product, query, kind) → package"},
    {"from": "orchestration-runtime", "to": "escalation-runtime",    "kind": "evaluation-call",        "contract": "_evaluate_escalation(packages) → triggers[]"},
    {"from": "orchestration-runtime", "to": "observability-system",  "kind": "append-only-emit",       "contract": "orchestration-trace, retrieval-trace, escalation-trace events"},
    {"from": "retrieval-runtime",     "to": "provenance-system",     "kind": "read-only-load",         "contract": "load knowledge-core JSON; never write"},
    {"from": "replay-system",         "to": "observability-system",  "kind": "read-only-tail",         "contract": "consume orchestration-trace; emit replay-trace"},
    {"from": "replay-system",         "to": "retrieval-runtime",     "kind": "deterministic-re-call",  "contract": "re-execute retrieve() with captured (product, query, kind)"},
    {"from": "reviewer-operations",   "to": "observability-system",  "kind": "read-only-tail + emit",  "contract": "consume runtime events; emit review-decision events"},
    {"from": "reviewer-operations",   "to": "provenance-system",     "kind": "read-only-load",         "contract": "render provenance for evidence-pull; no writes"},
    {"from": "governance-operations", "to": "reviewer-operations",   "kind": "scope-assignment",       "contract": "assign / revoke reviewer scope; dual-audited"},
    {"from": "governance-operations", "to": "provenance-system",     "kind": "pipeline-write",         "contract": "only governance pipeline appends to provenance"},
    {"from": "oem-ingestion-system",  "to": "provenance-system",     "kind": "staged-write",           "contract": "checksum-verified ingest into staging; never directly to production"},
    {"from": "oem-ingestion-system",  "to": "reviewer-operations",   "kind": "dual-review-handoff",    "contract": "binding handoff for OEM-reviewer dual-review"},
    {"from": "escalation-runtime",    "to": "observability-system",  "kind": "append-only-emit",       "contract": "escalation-trace events; never silent"},
]

ISOLATION_BOUNDARIES = [
    "retrieval ↔ provenance: retrieval reads provenance; never writes",
    "orchestration ↔ canonical knowledge-core: orchestration emits packages; never writes canonical JSON",
    "reviewer ↔ production write paths: reviewer surfaces stage decisions; never directly mutate production",
    "ingestion ↔ production: OEM ingestion writes only to staging; supersession requires governance pipeline",
    "replay ↔ live runtime: replay outputs go to a side channel; never to production emission paths",
    "observability ↔ all modules: observability is read-only consumer; no back-channel mutation",
]

TOPOLOGY_INVARIANTS = [
    "every module relationship is declared; undeclared calls are forbidden",
    "every cross-module call satisfies a declared contract",
    "every cross-module call emits an observability event",
    "no cross-module call escalates trust silently",
    "no cross-module call bypasses an isolation boundary",
]


# =============================================================================
# TASK 3 — DEPLOYMENT COMPOSITION
# =============================================================================

DEPLOYMENT_COMPOSITIONS = [
    {"id": "local-supervised-stack", "environment": "local-supervised-runtime", "modules": ["retrieval-runtime", "orchestration-runtime", "escalation-runtime", "provenance-system (read-only mount)", "observability-system"], "supervision": "full HITL on every checkpoint", "exclusions": ["reviewer-operations", "governance-operations", "oem-ingestion-system"]},
    {"id": "reviewer-stack",         "environment": "reviewer-operation-environment", "modules": ["reviewer-operations", "observability-system (read-only tail)", "provenance-system (read-only mount)"], "supervision": "reviewer claim + queue ceiling", "exclusions": ["retrieval-runtime", "orchestration-runtime", "escalation-runtime", "production write paths"]},
    {"id": "ingestion-stack",        "environment": "oem-ingestion-environment",      "modules": ["oem-ingestion-system", "observability-system", "provenance-system (staged-write only)"], "supervision": "OEM-reviewer dual-review",   "exclusions": ["retrieval-runtime", "orchestration-runtime", "production knowledge-core writes"]},
    {"id": "replay-stack",           "environment": "local-supervised-runtime or staging", "modules": ["replay-system", "retrieval-runtime (re-call only)", "observability-system (read-only tail)"], "supervision": "operator-initiated; no auto-replay", "exclusions": ["orchestration emission to production", "reviewer-operations write paths"]},
    {"id": "observability-stack",    "environment": "any (read-only consumer)",       "modules": ["observability-system"], "supervision": "consumer identity declared",   "exclusions": ["all back-channel mutation"]},
    {"id": "controlled-pilot-stack", "environment": "controlled-pilot",               "modules": ["retrieval-runtime", "orchestration-runtime", "escalation-runtime", "provenance-system (read-only)", "observability-system", "reviewer-operations (scoped)"], "supervision": "full HITL + escalation-supervisor on slice-halt", "exclusions": ["governance-console exposure", "oem-ingestion-system"]},
]

COMPOSITION_INVARIANTS = [
    "every deployment composition declares its environment, modules, supervision, and exclusions",
    "no composition includes a module not authorized for its environment's trust zone",
    "no composition silently widens its module set",
    "no composition shares mutable state with another composition",
    "every composition emits a composition-manifest at startup",
]


# =============================================================================
# TASK 4 — INTEROPERABILITY CONTRACTS
# =============================================================================

INTEROPERABILITY_CONTRACTS = [
    {"id": "runtime-contract",      "scope": "retrieval ↔ orchestration",    "shape": "retrieve(product, query, kind) → {nodes[], manifest{extra.candidate_only?}}"},
    {"id": "escalation-contract",   "scope": "orchestration ↔ escalation",   "shape": "_evaluate_escalation(packages) → triggers[{id, source, rule}]"},
    {"id": "provenance-contract",   "scope": "any-module ↔ provenance",      "shape": "read: load(path) → JSON; write: governance-pipeline-only with manifest_id + source_files[].sha256"},
    {"id": "replay-contract",       "scope": "replay ↔ runtime + observability", "shape": "replay_run(run_id) → {deterministic: bool, drift?: details}"},
    {"id": "retrieval-contract",    "scope": "retrieval ↔ provenance",       "shape": "read-only load of canonical knowledge-core JSON; scoring = Jaccard × CONFIDENCE_WEIGHTS[node.confidence]"},
    {"id": "governance-contract",   "scope": "governance ↔ all modules",     "shape": "scope assignment / revocation / emergency intervention; dual-audited; append-only"},
    {"id": "continuity-contract",   "scope": "orchestration ↔ continuity",   "shape": "checkpoint snapshot id + resume points; append-only continuity-trace events"},
]

CONTRACT_DISCIPLINE = [
    "every contract declares scope, shape, and an append-only event surface",
    "every contract is versioned; breaking changes require a governance action",
    "every contract refuses to suppress provenance, candidate-only, or supervision-receipt fields",
    "every contract is reversible: any party may withdraw; revocation is first-class",
    "every contract is testable: a substitute satisfying the contract is interchangeable",
]


# =============================================================================
# TASK 5 — PACKAGING & ASSEMBLY
# =============================================================================

PACKAGING_STANDARDS = [
    {"id": "runtime-package-manifest",   "fields": ["package_id", "manifest_id", "source_files[]", "extra{candidate_only?, empty?}", "supervision_receipt"]},
    {"id": "module-assembly-manifest",   "fields": ["composition_id", "module_ids[]", "environment_id", "trust_zone_id", "supervision_level"]},
    {"id": "deployment-manifest",        "fields": ["deployment_id", "composition_id", "environment_id", "started_at", "started_by", "scope"]},
    {"id": "environment-manifest",       "fields": ["environment_id", "trust_level", "supervision_level", "isolation", "lifecycle_state"]},
    {"id": "governance-manifest",        "fields": ["governance_event_id", "actor", "decision", "rationale", "dual_audit?", "audit_co_signature?"]},
    {"id": "operational-composition-manifest", "fields": ["composition_id", "module_topology_hash", "interop_contract_versions{}", "trust_zone_map{}"]},
]

PACKAGING_INVARIANTS = [
    "every manifest is append-only; manifests are never edited in place",
    "every manifest carries an id and a generated_at timestamp",
    "every manifest references the parent manifest it composes (if any)",
    "no manifest may omit provenance, candidate-only, or supervision fields when applicable",
    "manifests are the basis for replay; reproducibility depends on manifest fidelity",
]


# =============================================================================
# TASK 6 — DEPLOYMENT SLICES
# =============================================================================

DEPLOYMENT_SLICES = [
    {"id": "onboarding-only-runtime",  "composition": "local-supervised-stack", "kinds": ["pairing", "onboarding-prereqs"],          "halt_conditions": ["safety-demote"]},
    {"id": "troubleshooting-runtime",  "composition": "local-supervised-stack", "kinds": ["troubleshooting", "warnings"],            "halt_conditions": ["candidate-only + irreversible-adjacent"]},
    {"id": "reviewer-runtime",         "composition": "reviewer-stack",         "kinds": ["queue-claim", "evidence-pull", "decision"], "halt_conditions": ["missing-binding"]},
    {"id": "governance-runtime",       "composition": "controlled-pilot-stack (governance-scoped subset)", "kinds": ["scope-assign", "revoke", "emergency-intervention"], "halt_conditions": ["dual-audit-disagreement"]},
    {"id": "ingestion-runtime",        "composition": "ingestion-stack",        "kinds": ["fetch", "checksum-verify", "stage", "dual-review"], "halt_conditions": ["checksum-mismatch"]},
    {"id": "replay-runtime",           "composition": "replay-stack",           "kinds": ["replay-run", "drift-compare", "finding-emit"], "halt_conditions": ["replay-drift > floor"]},
]

SLICE_INVARIANTS = [
    "every slice is bounded by composition + kinds + halt conditions",
    "every slice emits a slice-manifest at startup and at every halt",
    "no slice silently widens its kinds",
    "no slice resumes from a halt without an operator decision",
    "every slice is product-scoped; cross-product slices are forbidden",
]


# =============================================================================
# TASK 7 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs how all prior modules converge into a coherent operational stack.",
    "All modules are declared, contract-bound, and observability-traceable.",
    "All compositions are declared; undeclared compositions are forbidden.",
    "All deployment manifests are append-only and reproducible.",
    "All convergence remains subordinate to provenance, supervision, trust-boundary, and isolation governance.",
    "No production deployment is performed by this layer; this layer governs the conditions under which deployment may later be assembled.",
    "Subordinate to knowledge-core and to all twenty-five prior governance layers.",
]

CONVERGENCE_PHILOSOPHY = [
    "Convergence is declared, not emergent.",
    "Convergence preserves every prior invariant; it never relaxes any of them.",
    "Convergence is observable end-to-end via append-only channels.",
    "Convergence is reversible: any module, contract, or composition may be withdrawn by governance action.",
]

CANONICAL_ASSEMBLY_DOCTRINE = [
    "Assembly composes declared modules; it never invents new responsibilities.",
    "Assembly preserves isolation boundaries; it never collapses them for performance.",
    "Assembly is reproducible: same manifests → same composition.",
    "Assembly is auditable: every assembly event is an append-only record.",
]

OPERATIONAL_STACK_PHILOSOPHY = [
    "The stack is a declared topology of contracts, not a tower of code.",
    "The stack is governed by interoperability contracts, not by implementation detail.",
    "The stack admits substitutes that satisfy contracts; it does not require monoculture.",
    "The stack honors provenance and supervision above every other property.",
]

INTEROPERABILITY_DOCTRINE = [
    "Contracts declare scope, shape, and event surface.",
    "Contracts refuse to suppress supervision, provenance, or uncertainty fields.",
    "Contracts are versioned; breaking changes are governance actions.",
    "Contracts are testable; a substitute satisfying the contract is interchangeable.",
]

DEPLOYMENT_COMPOSITION_PHILOSOPHY = [
    "Compositions are declared per environment and per trust zone.",
    "Compositions never silently include modules outside their authorization.",
    "Compositions emit manifests; manifests are the basis for replay.",
    "Compositions are revocable; rollback is a first-class composition action.",
]

ECOSYSTEM_CONVERGENCE_PRINCIPLES = [
    "Convergence is the assembly of governed parts, never the creation of new architecture.",
    "Convergence respects all twenty-five prior layers without exception.",
    "Convergence is bounded by declared compositions; it never produces undeclared topologies.",
    "Convergence honors the platform's foundational completeness; it does not seek expansion.",
]


# =============================================================================
# TASK 8 — FUTURE DEPLOYMENT EVOLUTION
# =============================================================================

FUTURE_COMMITMENTS = [
    "supervised production pilots are assembled from declared deployment slices and composition manifests",
    "operational deployment slices are bounded by product × domain × environment; no global slice exists",
    "future operator consoles inherit all invariants from layer 24 and bind to declared compositions only",
    "future copilots are supervised assistive surfaces bound by the runtime-contract and the supervision-receipt invariant",
    "multimodal operational runtimes subscribe to existing observability channels; no parallel channels are introduced",
    "federated reviewer ecosystems are partitioned by scope; revocation remains first-class across federations",
]

FUTURE_INVARIANTS = [
    "no deployment is ever assembled without a declared composition manifest",
    "no module is ever introduced without a declared interoperability contract",
    "no contract is ever loosened to suppress provenance, supervision, or uncertainty",
    "no convergence step ever weakens a prior layer's invariant",
    "no macro-governance mega-layer is spawned by reference-stack work",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    STACK_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "canonical-stack", "canonical-stack",
        "Canonical Reference Stack",
        "Nine declared modules composing the canonical operational stack.",
        [
            ("Modules", md_list([f"`{m['id']}` — {m['responsibility']} (module: {m['module']})" for m in CANONICAL_STACK])),
            ("Invariants", md_list(STACK_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "canonical-stack",
         "canonical_stack": CANONICAL_STACK,
         "stack_invariants": STACK_INVARIANTS},
    )

    # --- Task 2 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "module-topology", "module-topology",
        "Operational Module Topology",
        "Declared module relationships, isolation boundaries, and topology invariants.",
        [
            ("Relationships", md_list([f"`{r['from']}` → `{r['to']}` ({r['kind']}) — {r['contract']}" for r in MODULE_RELATIONSHIPS])),
            ("Isolation boundaries", md_list(ISOLATION_BOUNDARIES)),
            ("Invariants", md_list(TOPOLOGY_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "module-topology",
         "module_relationships": MODULE_RELATIONSHIPS,
         "isolation_boundaries": ISOLATION_BOUNDARIES,
         "topology_invariants": TOPOLOGY_INVARIANTS},
    )

    # --- Task 3 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "deployment-composition", "deployment-composition",
        "Canonical Deployment Composition",
        "Six declared compositions, each with environment, modules, supervision, and exclusions.",
        [
            ("Compositions", md_list([f"`{c['id']}` — env: {c['environment']}; modules: " + ", ".join(c['modules']) for c in DEPLOYMENT_COMPOSITIONS])),
            ("Invariants", md_list(COMPOSITION_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "deployment-composition",
         "deployment_compositions": DEPLOYMENT_COMPOSITIONS,
         "composition_invariants": COMPOSITION_INVARIANTS},
    )

    # --- Task 4 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "interoperability", "interoperability",
        "Runtime Interoperability Contracts",
        "Seven declared interoperability contracts; versioned, testable, reversible.",
        [
            ("Contracts", md_list([f"`{c['id']}` — scope: {c['scope']}; shape: `{c['shape']}`" for c in INTEROPERABILITY_CONTRACTS])),
            ("Discipline", md_list(CONTRACT_DISCIPLINE)),
        ],
        {"schema": SCHEMA, "kind": "interoperability",
         "interoperability_contracts": INTEROPERABILITY_CONTRACTS,
         "contract_discipline": CONTRACT_DISCIPLINE},
    )

    # --- Task 5 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "packaging", "packaging",
        "Operational Packaging & Assembly",
        "Six declared manifest standards; manifests are append-only and reproducible.",
        [
            ("Standards", md_list([f"`{s['id']}` — fields: " + ", ".join(s['fields']) for s in PACKAGING_STANDARDS])),
            ("Invariants", md_list(PACKAGING_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "packaging",
         "packaging_standards": PACKAGING_STANDARDS,
         "packaging_invariants": PACKAGING_INVARIANTS},
    )

    # --- Task 6 ----------------------------------------------------------
    write_pair(
        STACK_ROOT / "deployment-slices", "deployment-slices",
        "Executable Deployment Slices",
        "Six declared slices, each bounded by composition + kinds + halt conditions.",
        [
            ("Slices", md_list([f"`{s['id']}` — composition: {s['composition']}; kinds: " + ", ".join(s['kinds']) + f"; halts on: " + ", ".join(s['halt_conditions']) for s in DEPLOYMENT_SLICES])),
            ("Invariants", md_list(SLICE_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "deployment-slices",
         "deployment_slices": DEPLOYMENT_SLICES,
         "slice_invariants": SLICE_INVARIANTS},
    )

    # --- Task 7 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# REFERENCE STACK GOVERNANCE\n\n"
        "Twenty-sixth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-five prior governance layers.\n\n"
        "Governs the canonical operational reference stack: module convergence, topology, "
        "deployment composition, interoperability contracts, packaging standards, and "
        "executable deployment slices.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Reference Stack Governance",
        "Declares principles + authority for canonical operational stack convergence.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/canonical-stack/`",
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/module-topology/`",
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/deployment-composition/`",
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/interoperability/`",
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/packaging/`",
                "`wp-content/themes/beslock-custom/User manuals/reference-stack/deployment-slices/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT deploy production systems",
                "DO NOT implement infrastructure automation",
                "DO NOT create frontend applications",
                "DO NOT introduce autonomous cognition",
                "DO NOT recursively expand governance abstractions",
            ])),
        ],
        {"schema": SCHEMA, "kind": "charter",
         "principles": CHARTER_PRINCIPLES,
         "subordinate_to": SUBORDINATE_TO,
         "generated": now_iso()},
    )

    for slug, title, intro, principles in [
        ("convergence-philosophy", "Convergence Philosophy",
         "Convergence is declared, not emergent.",
         CONVERGENCE_PHILOSOPHY),
        ("canonical-assembly-doctrine", "Canonical Assembly Doctrine",
         "Assembly composes declared modules; it never invents new responsibilities.",
         CANONICAL_ASSEMBLY_DOCTRINE),
        ("operational-stack-philosophy", "Operational Stack Philosophy",
         "The stack is a declared topology of contracts, not a tower of code.",
         OPERATIONAL_STACK_PHILOSOPHY),
        ("interoperability-doctrine", "Interoperability Doctrine",
         "Contracts declare scope, shape, event surface; they are versioned and testable.",
         INTEROPERABILITY_DOCTRINE),
        ("deployment-composition-philosophy", "Deployment Composition Philosophy",
         "Compositions are declared per environment and per trust zone.",
         DEPLOYMENT_COMPOSITION_PHILOSOPHY),
        ("ecosystem-convergence-principles", "Ecosystem Convergence Principles",
         "Convergence is the assembly of governed parts, never the creation of new architecture.",
         ECOSYSTEM_CONVERGENCE_PRINCIPLES),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # --- Final 10 reports ------------------------------------------------
    reports = [
        ("01-canonical-stack-summary.json", {
            "schema": SCHEMA, "kind": "canonical-stack-summary",
            "modules": [m["id"] for m in CANONICAL_STACK],
            "invariants_count": len(STACK_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/canonical-stack/",
        }),
        ("02-module-topology-summary.json", {
            "schema": SCHEMA, "kind": "module-topology-summary",
            "relationships_count": len(MODULE_RELATIONSHIPS),
            "isolation_boundaries_count": len(ISOLATION_BOUNDARIES),
            "invariants_count": len(TOPOLOGY_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/module-topology/",
        }),
        ("03-deployment-composition-summary.json", {
            "schema": SCHEMA, "kind": "deployment-composition-summary",
            "compositions": [c["id"] for c in DEPLOYMENT_COMPOSITIONS],
            "invariants_count": len(COMPOSITION_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/deployment-composition/",
        }),
        ("04-interoperability-contract-summary.json", {
            "schema": SCHEMA, "kind": "interoperability-contract-summary",
            "contracts": [c["id"] for c in INTEROPERABILITY_CONTRACTS],
            "discipline_rules_count": len(CONTRACT_DISCIPLINE),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/interoperability/",
        }),
        ("05-packaging-summary.json", {
            "schema": SCHEMA, "kind": "packaging-summary",
            "standards": [s["id"] for s in PACKAGING_STANDARDS],
            "invariants_count": len(PACKAGING_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/packaging/",
        }),
        ("06-deployment-slice-summary.json", {
            "schema": SCHEMA, "kind": "deployment-slice-summary",
            "slices": [s["id"] for s in DEPLOYMENT_SLICES],
            "invariants_count": len(SLICE_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/reference-stack/deployment-slices/",
        }),
        ("07-convergence-governance-summary.json", {
            "schema": SCHEMA, "kind": "convergence-governance-summary",
            "layer_index": 26,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/REFERENCE_STACK_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/reference-stack/",
            "doctrine_sections": [
                "convergence-philosophy",
                "canonical-assembly-doctrine",
                "operational-stack-philosophy",
                "interoperability-doctrine",
                "deployment-composition-philosophy",
                "ecosystem-convergence-principles",
            ],
        }),
        ("08-future-deployment-evolution-summary.json", {
            "schema": SCHEMA, "kind": "future-deployment-evolution-summary",
            "future_commitments": FUTURE_COMMITMENTS,
            "future_invariants": FUTURE_INVARIANTS,
        }),
        ("09-unresolved-convergence-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-convergence-risks",
            "items": [
                {"id": "no-composition-manifest-emitter",   "severity": "high",   "impact": "compositions declared; runtime does not yet emit composition-manifests at startup"},
                {"id": "no-interop-contract-registry",      "severity": "high",   "impact": "contracts declared; no registry validates that running modules satisfy a declared contract version"},
                {"id": "no-slice-manifest-emitter",         "severity": "high",   "impact": "deployment slices declared; runtime does not yet emit slice-manifests at startup or at halts"},
                {"id": "no-substitute-contract-tests",      "severity": "medium", "impact": "contracts asserted as testable; substitute conformance tests not yet written"},
                {"id": "no-topology-hash",                  "severity": "medium", "impact": "operational-composition-manifest declares module_topology_hash; not yet computed at runtime"},
                {"id": "no-environment-lifecycle-store",    "severity": "medium", "impact": "environment-manifest declares lifecycle_state; no store records state per env id (carry-over from layer 25)"},
                {"id": "carry-overs-from-phases-28-31",     "severity": "high",   "impact": "no executable consoles, identity store, claim mediator, explanation renderer, reviewer registry, queue store, event log, OEM binding store, integration registry, sandbox harness, incident-trace channel; 132 candidates still await elevation"},
            ],
        }),
        ("10-operational-ecosystem-convergence-assessment.json", {
            "schema": SCHEMA, "kind": "operational-ecosystem-convergence-assessment",
            "platform_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "convergence_status": "MODELED (executable composition emission pending)",
            "primary_bottleneck": "REFERENCE OPERATIONAL CONVERGENCE (now governed by declared canonical stack)",
            "next_bottleneck": "executable enforcement of composition + slice manifests, interop contract registry, substitute-conformance tests, topology hash computation",
            "future_commitments": FUTURE_COMMITMENTS,
            "future_invariants": FUTURE_INVARIANTS,
            "generated": now_iso(),
        }),
    ]
    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(f"Reference Stack Governance (layer 26) written to:\n  {STACK_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")


if __name__ == "__main__":
    build()
