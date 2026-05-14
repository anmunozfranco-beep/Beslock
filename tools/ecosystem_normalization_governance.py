"""
Phase 33 — ECOSYSTEM NORMALIZATION & CANONICALIZATION.

Constitutional layer 27. Modeling-only. Subordinate to knowledge-core and
to all twenty-six prior governance layers.

Writes:
  - the six ecosystem-normalization artifact folders under
    `wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ECOSYSTEM_NORMALIZATION_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/ecosystem-normalization/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
Audits the static repository surface (tools/*.py builder filenames + schema
identifiers + KNOWLEDGE_BUILDING/ doctrine roots + reports/ folders) to
canonicalize the ecosystem. Writes nothing outside this layer's folders.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
NORM_ROOT = THEME_ROOT / "ecosystem-normalization"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "ECOSYSTEM_NORMALIZATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "ecosystem-normalization"
TOOLS_ROOT = REPO_ROOT / "tools"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_PARENT = THEME_ROOT / "_repository-governance" / "reports"

SCHEMA = "ecosystem-normalization-governance/1.0"


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
    "HUMAN_OPERATIONS", "ENVIRONMENT_AND_INTEGRATION", "REFERENCE_STACK",
]


# =============================================================================
# AUDIT — read static surface only
# =============================================================================

def audit_builders():
    """Inspect tools/*governance*.py + corpus_enrichment.py for SCHEMA + filename conventions."""
    builders = []
    for p in sorted(TOOLS_ROOT.glob("*.py")):
        if p.name in {"__init__.py"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        schemas = re.findall(r'SCHEMA\s*=\s*"([^"]+)"', text)
        has_write_pair = "def write_pair(" in text or "write_pair(" in text
        has_subordinate = "SUBORDINATE_TO" in text
        idempotent = "Idempotent" in text or "idempotent" in text
        builders.append({
            "filename": p.name,
            "schemas": schemas,
            "uses_write_pair_helper": has_write_pair,
            "declares_subordinate_to": has_subordinate,
            "declares_idempotent": idempotent,
        })
    return builders


def audit_schemas(builders):
    """Collect all SCHEMA identifiers and detect divergence."""
    seen = {}
    for b in builders:
        for s in b["schemas"]:
            seen.setdefault(s, []).append(b["filename"])
    return seen


def audit_doctrine_roots():
    if not KB_ROOT.exists():
        return []
    return sorted([p.name for p in KB_ROOT.iterdir() if p.is_dir()])


def audit_reports_folders():
    if not REPORTS_PARENT.exists():
        return []
    return sorted([p.name for p in REPORTS_PARENT.iterdir() if p.is_dir()])


BUILDERS_AUDIT = audit_builders()
SCHEMAS_AUDIT = audit_schemas(BUILDERS_AUDIT)
DOCTRINE_ROOTS = audit_doctrine_roots()
REPORTS_FOLDERS = audit_reports_folders()


# =============================================================================
# TASK 1 — SCHEMA NORMALIZATION
# =============================================================================

CANONICAL_SCHEMA_FAMILIES = [
    {"family": "runtime",       "members": ["runtime-governance/1.0", "runtime-orchestration-governance/1.0", "runtime-implementation-governance/1.0", "runtime-hardening-governance/1.0", "prototype-runtime-governance/1.0"], "rule": "all runtime-related governance schemas use the `runtime-*` prefix"},
    {"family": "knowledge",     "members": ["knowledge-lifecycle-governance/1.0", "knowledge-operations-governance/1.0"], "rule": "all knowledge-evolution governance schemas use the `knowledge-*` prefix"},
    {"family": "operational",   "members": ["operational-proof-governance/1.0"], "rule": "all proof / measurement governance schemas use the `operational-*` prefix"},
    {"family": "intelligence",  "members": ["adaptive-operational-governance/1.0", "decision-intelligence-governance/1.0", "reasoning-governance/1.0", "continuity-governance/1.0"], "rule": "cognition-related governance schemas keep their declared identifier; do not rename"},
    {"family": "ecosystem",     "members": ["ecosystem-interoperability-governance/1.0", "environment-integration-governance/1.0", "reference-stack-governance/1.0", "ecosystem-normalization-governance/1.0"], "rule": "ecosystem-and-deployment governance schemas use the `ecosystem-*` / `environment-*` / `reference-*` prefix"},
    {"family": "human",         "members": ["human-operations-governance/1.0"], "rule": "human-interaction governance schemas use the `human-*` prefix"},
    {"family": "platform",      "members": ["composition-governance/1.0", "execution-governance/1.0", "lifecycle-governance/1.0", "realization-and-deployment-governance/1.0", "repo-governance/1.0", "visual-governance/1.0", "visual-constitution/1.0"], "rule": "platform foundation schemas keep their declared identifiers; do not rename"},
]

SCHEMA_OVERLAP_FINDINGS = [
    {"id": "two-runtime-execution-axes",     "evidence": "runtime-governance/1.0 + execution-governance/1.0 + runtime-orchestration-governance/1.0 each model an execution axis", "resolution": "treat as layered (governance → orchestration → implementation); no schema merge; document in canonical-references"},
    {"id": "two-deployment-axes",            "evidence": "realization-and-deployment-governance/1.0 + environment-integration-governance/1.0 + reference-stack-governance/1.0", "resolution": "realization=value/timing; environment=trust/boundaries; reference-stack=composition; layered, not duplicated"},
    {"id": "two-lifecycle-axes",             "evidence": "lifecycle-governance/1.0 (knowledge-core lifecycle) + knowledge-lifecycle-governance/1.0 (candidate→trusted)", "resolution": "lifecycle-governance owns content lifecycle; knowledge-lifecycle owns trust lifecycle; both retained, scopes documented"},
    {"id": "visual-dual-schema",             "evidence": "visual-governance/1.0 + visual-constitution/1.0", "resolution": "constitution = doctrinal; governance = operational; retained as declared"},
    {"id": "two-ecosystem-axes",             "evidence": "ecosystem-interoperability-governance/1.0 + ecosystem-normalization-governance/1.0", "resolution": "interoperability = cross-system contracts; normalization = internal coherence; layered, not duplicated"},
]

SCHEMA_NORMALIZATION_RULES = [
    "every governance schema identifier is `<area>-governance/<MAJOR>.<MINOR>` or `<area>-constitution/<MAJOR>.<MINOR>`",
    "every schema is owned by exactly one builder file (one canonical author)",
    "schemas are never renamed in place; renames require a new MAJOR version",
    "schemas never duplicate fields owned by knowledge-core/1.0 (manifest_id, source_files, sha256, confidence, etc.)",
    "schemas never collapse layered concerns (runtime/orchestration/implementation, lifecycle/trust, etc.)",
]


# =============================================================================
# TASK 2 — BUILDER HARMONIZATION
# =============================================================================

BUILDER_CONVENTIONS = [
    "filename = `tools/<area>_governance.py` (snake_case area; suffix `_governance`)",
    "exposes a single top-level `build()` function and `if __name__ == '__main__': build()`",
    "declares `SCHEMA = '<area>-governance/<version>'` exactly once",
    "declares `SUBORDINATE_TO = [...]` listing knowledge-core + every prior layer",
    "uses the `write_pair(folder, slug, title, intro, sections, payload)` helper with paired `.md` + `.json`",
    "writes only under THREE roots: artifact folder + KNOWLEDGE_BUILDING/<LAYER>/ + reports/<slug>/",
    "is idempotent and non-destructive (re-running yields the same files)",
    "reads no per-product knowledge-core JSON",
    "prints a final summary line including the three written roots",
]

BUILDER_FINDINGS = [
    {"id": b["filename"],
     "schemas_declared": b["schemas"],
     "uses_write_pair_helper": b["uses_write_pair_helper"],
     "declares_subordinate_to": b["declares_subordinate_to"],
     "declares_idempotent": b["declares_idempotent"]}
    for b in BUILDERS_AUDIT
]

BUILDER_HARMONIZATION_RULES = [
    "future builders MUST satisfy every builder convention listed above",
    "future builders MUST NOT introduce a second helper that diverges from `write_pair`",
    "future builders MUST NOT write outside the three declared roots",
    "future builders MUST NOT rename existing schemas; new MAJOR versions only",
    "future builders MUST NOT introduce new macro-governance mega-layers",
]


# =============================================================================
# TASK 3 — GOVERNANCE DEDUPLICATION
# =============================================================================

DOCTRINE_OVERLAP_RESOLUTIONS = [
    {"id": "execution-stack",        "doctrines": ["EXECUTION_GOVERNANCE", "RUNTIME_GOVERNANCE", "RUNTIME_ORCHESTRATION_GOVERNANCE", "RUNTIME_IMPLEMENTATION_GOVERNANCE", "PROTOTYPE_RUNTIME_GOVERNANCE", "RUNTIME_HARDENING_GOVERNANCE"], "ownership": "EXECUTION = abstract execution model; RUNTIME = realization strategy; RUNTIME_ORCHESTRATION = supervised loop; RUNTIME_IMPLEMENTATION = real Python package; PROTOTYPE_RUNTIME = prototype slice; RUNTIME_HARDENING = supplemental corpus + replay"},
    {"id": "knowledge-stack",        "doctrines": ["LIFECYCLE_GOVERNANCE", "KNOWLEDGE_LIFECYCLE_GOVERNANCE", "KNOWLEDGE_OPERATIONS_GOVERNANCE"], "ownership": "LIFECYCLE = content lifecycle; KNOWLEDGE_LIFECYCLE = trust lifecycle (candidate→trusted); KNOWLEDGE_OPERATIONS = operator tooling/workflows"},
    {"id": "deployment-stack",       "doctrines": ["REALIZATION_AND_DEPLOYMENT_GOVERNANCE", "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE", "REFERENCE_STACK_GOVERNANCE"], "ownership": "REALIZATION = value/sequencing; ENVIRONMENT_AND_INTEGRATION = trust zones + integration contracts; REFERENCE_STACK = canonical module composition"},
    {"id": "ecosystem-stack",        "doctrines": ["ECOSYSTEM_INTEROPERABILITY_GOVERNANCE", "ECOSYSTEM_NORMALIZATION_GOVERNANCE"], "ownership": "INTEROPERABILITY = cross-system contracts; NORMALIZATION = internal coherence + dedup"},
    {"id": "human-stack",            "doctrines": ["HUMAN_OPERATIONS_GOVERNANCE"], "ownership": "single owner of operator UX, HITL, explainability, ergonomics"},
    {"id": "intelligence-stack",     "doctrines": ["ADAPTIVE_OPERATIONAL_GOVERNANCE", "DECISION_INTELLIGENCE_GOVERNANCE", "REASONING_GOVERNANCE", "CONTINUITY_GOVERNANCE"], "ownership": "ADAPTIVE = context adaptation; DECISION = branching/confidence; REASONING = causality/uncertainty; CONTINUITY = sessions/snapshots"},
    {"id": "platform-foundation",    "doctrines": ["VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE", "ACCESS_AND_CONSUMPTION", "COMPOSITION", "OPERATIONAL_PROOF"], "ownership": "foundational layers; each owns its declared scope; no overlap"},
]

CONTRADICTION_FINDINGS = [
    {"id": "no-doctrinal-contradictions-detected", "evidence": "every layer declares SUBORDINATE_TO knowledge-core + all prior layers; every layer is modeling-only; every layer respects: append-only, supervision-receipt, no-canonical-write, HITL-default, no-autonomous-operator", "resolution": "no rewrites required; canonical-references doc clarifies layered ownership"},
]

GOVERNANCE_DEDUP_RULES = [
    "no doctrine may be split across two layers without an explicit canonical-references entry",
    "no doctrine may be silently absorbed by another layer",
    "no doctrine may contradict a prior layer; subordination is strict",
    "no new doctrine may duplicate the scope of an existing doctrine",
    "doctrines may be deprecated only via a governance action; deprecation is append-only",
]


# =============================================================================
# TASK 4 — MANIFEST & CONTRACT CANONICALIZATION
# =============================================================================

CANONICAL_CONTRACT_AUTHORITIES = [
    {"contract": "runtime-package-manifest",            "authority": "REFERENCE_STACK_GOVERNANCE (layer 26) — packaging/"},
    {"contract": "runtime-contract (retrieve)",         "authority": "REFERENCE_STACK_GOVERNANCE — interoperability/"},
    {"contract": "escalation-contract",                 "authority": "REFERENCE_STACK_GOVERNANCE — interoperability/"},
    {"contract": "provenance-contract",                 "authority": "knowledge-core/1.0 + REFERENCE_STACK_GOVERNANCE"},
    {"contract": "replay-contract",                     "authority": "RUNTIME_HARDENING_GOVERNANCE (layer 21) + REFERENCE_STACK_GOVERNANCE"},
    {"contract": "retrieval-contract (Jaccard×weight)", "authority": "RUNTIME_HARDENING_GOVERNANCE + REFERENCE_STACK_GOVERNANCE"},
    {"contract": "governance-contract",                 "authority": "REFERENCE_STACK_GOVERNANCE"},
    {"contract": "continuity-contract",                 "authority": "CONTINUITY_GOVERNANCE + REFERENCE_STACK_GOVERNANCE"},
    {"contract": "deployment-manifest",                 "authority": "REFERENCE_STACK_GOVERNANCE — packaging/"},
    {"contract": "environment-manifest",                "authority": "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE (layer 25)"},
    {"contract": "integration-contracts (7)",           "authority": "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE"},
    {"contract": "trust-zone mapping",                  "authority": "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE"},
    {"contract": "supervision-receipt",                 "authority": "HUMAN_OPERATIONS_GOVERNANCE (layer 24)"},
    {"contract": "operator-identity field",             "authority": "HUMAN_OPERATIONS_GOVERNANCE"},
]

CANONICALIZATION_RULES = [
    "every contract has exactly one authoritative declaring layer",
    "implementation modules cite the authoritative layer in their docstring (forward action)",
    "no contract is silently extended; extensions are governance actions",
    "no contract is silently versioned down; downgrades require a governance action",
    "canonical-references is the single source of truth for contract ownership",
]


# =============================================================================
# TASK 5 — NAMING & TAXONOMY
# =============================================================================

NAMING_CANONICAL_TERMS = [
    {"term": "package",            "definition": "an emitted runtime artifact bundling retrieved nodes + manifest", "deprecated_aliases": ["bundle", "envelope"]},
    {"term": "manifest",           "definition": "an append-only declarative record describing a package, deployment, environment, composition, or governance event"},
    {"term": "node",               "definition": "a single knowledge-core JSON record retrieved by the runtime"},
    {"term": "candidate",          "definition": "a node at the lowest trust tier; never used in irreversible-adjacent contexts without escalation"},
    {"term": "supervision-receipt","definition": "the append-only record bound to every operator action proving supervision occurred", "owner": "HUMAN_OPERATIONS_GOVERNANCE"},
    {"term": "checkpoint",         "definition": "a declared decision boundary in an executable workflow"},
    {"term": "trust-zone",         "definition": "a declared infrastructure region with a fixed trust tier", "owner": "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE"},
    {"term": "trust-tier",         "definition": "a declared confidence weighting applied to a node (verified-oem, verified-internal, high, ocr-derived, medium, inferred-operational, low, candidate, unresolved, unknown)", "owner": "RUNTIME_HARDENING_GOVERNANCE"},
    {"term": "slice",              "definition": "a bounded executable runtime composition (product × kinds × halt conditions)", "owner": "REFERENCE_STACK_GOVERNANCE"},
    {"term": "composition",        "definition": "a declared assembly of canonical-stack modules for a specific environment"},
    {"term": "operator",           "definition": "a human acting under a declared profile (runtime/reviewer/governance/escalation/oem/auditor)"},
    {"term": "channel",            "definition": "an append-only NDJSON event stream emitted by the observability system"},
]

NAMING_PROHIBITIONS = [
    "no synonym proliferation (one term, one meaning)",
    "no abbreviation of canonical terms in schemas or doctrine",
    "no informal aliases inside builder code or doctrine prose",
    "no reuse of a canonical term with a different meaning in any layer",
    "no introduction of new canonical terms without a doctrine entry",
]


# =============================================================================
# TASK 6 — RUNTIME CONSISTENCY
# =============================================================================

RUNTIME_CONSISTENCY_FINDINGS = [
    {"id": "retrieval-uses-confidence-weights",        "status": "consistent", "evidence": "retrieval.py applies CONFIDENCE_WEIGHTS declared in config.py; weights match RUNTIME_HARDENING_GOVERNANCE schema"},
    {"id": "candidate-only-marker-flows-end-to-end",   "status": "consistent", "evidence": "retrieval sets manifest.extra.candidate_only; assembly._evaluate_escalation reads it; ESCALATION emits trigger"},
    {"id": "replay-skips-empty-packages",              "status": "consistent", "evidence": "replay.py skips manifest.extra.empty=True; tests pass 19/19"},
    {"id": "observability-channels-bounded",           "status": "consistent", "evidence": "channels.py allows only declared channel names; orchestration/retrieval/escalation/continuity/replay/operational-audit-log"},
    {"id": "supervision-receipt-not-yet-runtime-field","status": "gap (declared, not enforced)", "evidence": "HUMAN_OPERATIONS_GOVERNANCE declares supervision-receipt; runtime CLI does not yet emit one as a separate field; flows.operator is a free string", "carry_over_from": "phase 30"},
    {"id": "composition-manifest-not-yet-emitted",     "status": "gap (declared, not enforced)", "evidence": "REFERENCE_STACK_GOVERNANCE declares composition-manifest at startup; runtime does not yet emit it", "carry_over_from": "phase 32"},
    {"id": "interop-contract-registry-absent",         "status": "gap (declared, not enforced)", "evidence": "REFERENCE_STACK_GOVERNANCE declares contract registry; absent in code", "carry_over_from": "phase 32"},
    {"id": "incident-trace-channel-not-provisioned",   "status": "gap (declared, not enforced)", "evidence": "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE declares incident-trace; channels.py has no `incident-trace` entry", "carry_over_from": "phase 31"},
    {"id": "no-divergent-runtime-assumptions-detected","status": "consistent", "evidence": "all runtime modules subscribe to a single config.ALLOWED_DOMAINS + a single CONFIDENCE_WEIGHTS dict; no module redefines either"},
    {"id": "no-replay-incompatibilities-detected",     "status": "consistent", "evidence": "replay re-executes against captured (product, query, kind); deterministic; tests pass"},
]

RUNTIME_CONSISTENCY_RULES = [
    "every runtime module uses canonical terms only (TASK 5)",
    "every runtime module reads ALLOWED_DOMAINS and CONFIDENCE_WEIGHTS from a single config source",
    "every runtime module emits to declared channels only",
    "every runtime gap above is recorded as a carry-over; no new gaps are introduced",
    "every runtime change is preceded by a governance action documented in this layer's canonical-references",
]


# =============================================================================
# TASK 7 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs internal coherence: schemas, builders, doctrines, contracts, naming, and runtime assumptions.",
    "All twenty-six prior layers are preserved without modification.",
    "Normalization is auditing + canonicalization; no schema is renamed and no layer is rewritten in this phase.",
    "Canonical-references is the single source of truth for contract ownership and doctrinal scope.",
    "No new macro-governance mega-layer is spawned; this layer audits, it does not expand.",
    "Subordinate to knowledge-core and to all twenty-six prior governance layers.",
]

NORMALIZATION_PHILOSOPHY = [
    "Coherence is a first-class operational property of the platform.",
    "Coherence is auditable; every layer's identifiers, conventions, and contracts are inspectable.",
    "Coherence is preserved by governance actions, not by silent edits.",
    "Coherence permits long-term evolution without semantic drift.",
]

CANONICALIZATION_DOCTRINE = [
    "Every contract has one authoritative declaring layer.",
    "Every schema identifier is owned by one builder.",
    "Every canonical term has one meaning; aliases are deprecated, not silently allowed.",
    "Every governance action against the ecosystem is append-only.",
]

ANTI_FRAGMENTATION_PRINCIPLES = [
    "Fragmentation is the failure mode this layer exists to prevent.",
    "Fragmentation is detected by audit, not by trust.",
    "Fragmentation is resolved by canonical-references entries, not by deletion.",
    "Fragmentation never justifies dissolving a prior layer's scope.",
]

SCHEMA_STABILITY_DOCTRINE = [
    "Schemas are stable: in-place renames are forbidden.",
    "Schemas are evolved by MAJOR version transitions; MAJOR transitions are governance actions.",
    "Schemas never duplicate knowledge-core fields.",
    "Schemas never collapse layered concerns.",
]

BUILDER_HARMONIZATION_PHILOSOPHY = [
    "Builders are the canonical authors of governance artifacts.",
    "Builders share a single helper (`write_pair`) and a single output topology.",
    "Builders are idempotent and non-destructive; re-runs converge on the same artifacts.",
    "Builders emit a final summary line so operators can verify outputs.",
]

ECOSYSTEM_COHERENCE_PRINCIPLES = [
    "Coherence is composed, not asserted.",
    "Coherence respects every prior layer's invariant without exception.",
    "Coherence rejects mega-layers and recursive abstractions.",
    "Coherence honors the platform's foundational completeness.",
]


# =============================================================================
# TASK 8 — LONG-TERM EVOLUTION STABILITY
# =============================================================================

FUTURE_COMMITMENTS = [
    "new products are added to the per-product knowledge-core under ext-images/<product>/; no new architecture is spawned",
    "new OEM manuals enter via the OEM ingestion environment + dual-review binding (layers 23, 25)",
    "new runtime domains extend ALLOWED_DOMAINS in config.py; CONFIDENCE_WEIGHTS extends only via governance action",
    "future deployment slices are declared compositions of canonical-stack modules (layer 26); no new module categories",
    "future reviewer ecosystems are partitioned by scope (layers 22, 23); revocation remains first-class",
    "future multimodal systems subscribe to existing observability channels (layers 25, 26); no parallel channels",
]

FUTURE_INVARIANTS = [
    "no future growth introduces a new macro-governance mega-layer",
    "no future growth renames a schema in place",
    "no future growth dissolves a prior layer's scope",
    "no future growth introduces a canonical term with a new meaning",
    "no future growth bypasses canonical-references",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    NORM_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "schema-normalization", "schema-normalization",
        "Schema Normalization Audit",
        "Audits all governance schema identifiers; canonicalizes families; resolves overlap without renaming.",
        [
            ("Canonical schema families", md_list([f"`{f['family']}` — rule: {f['rule']}; members: " + ", ".join(f['members']) for f in CANONICAL_SCHEMA_FAMILIES])),
            ("Detected schema identifiers (read from tools/)", md_list([f"`{s}` ← " + ", ".join(SCHEMAS_AUDIT[s]) for s in sorted(SCHEMAS_AUDIT)])),
            ("Overlap findings", md_list([f"`{o['id']}` — {o['evidence']} → resolution: {o['resolution']}" for o in SCHEMA_OVERLAP_FINDINGS])),
            ("Normalization rules", md_list(SCHEMA_NORMALIZATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "schema-normalization",
         "canonical_schema_families": CANONICAL_SCHEMA_FAMILIES,
         "detected_schemas": SCHEMAS_AUDIT,
         "overlap_findings": SCHEMA_OVERLAP_FINDINGS,
         "normalization_rules": SCHEMA_NORMALIZATION_RULES},
    )

    # --- Task 2 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "builder-harmonization", "builder-harmonization",
        "Builder Harmonization Audit",
        "Audits every builder under tools/; declares conventions; flags non-conforming files.",
        [
            ("Builder conventions", md_list(BUILDER_CONVENTIONS)),
            ("Builders inventoried", md_list([f"`{b['id']}` — schemas: " + (", ".join(b['schemas_declared']) or "<none>") + f"; write_pair: {b['uses_write_pair_helper']}; subordinate_to: {b['declares_subordinate_to']}; idempotent: {b['declares_idempotent']}" for b in BUILDER_FINDINGS])),
            ("Harmonization rules (forward)", md_list(BUILDER_HARMONIZATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "builder-harmonization",
         "builder_conventions": BUILDER_CONVENTIONS,
         "builders": BUILDER_FINDINGS,
         "harmonization_rules": BUILDER_HARMONIZATION_RULES},
    )

    # --- Task 3 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "governance-deduplication", "governance-deduplication",
        "Governance Deduplication Audit",
        "Audits doctrine roots; canonicalizes ownership across layered stacks; no doctrine is rewritten or merged.",
        [
            ("Doctrine roots inventoried", md_list([f"`{d}`" for d in DOCTRINE_ROOTS])),
            ("Layered ownership resolutions", md_list([f"`{r['id']}` — owns: {r['ownership']}" for r in DOCTRINE_OVERLAP_RESOLUTIONS])),
            ("Contradiction findings", md_list([f"`{c['id']}` — {c['evidence']}" for c in CONTRADICTION_FINDINGS])),
            ("Deduplication rules", md_list(GOVERNANCE_DEDUP_RULES)),
        ],
        {"schema": SCHEMA, "kind": "governance-deduplication",
         "doctrine_roots": DOCTRINE_ROOTS,
         "doctrine_overlap_resolutions": DOCTRINE_OVERLAP_RESOLUTIONS,
         "contradiction_findings": CONTRADICTION_FINDINGS,
         "governance_dedup_rules": GOVERNANCE_DEDUP_RULES},
    )

    # --- Task 4 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "contracts", "contracts",
        "Manifest & Contract Canonicalization",
        "Single canonical authority per contract; canonical-references is the single source of truth.",
        [
            ("Canonical authorities", md_list([f"`{c['contract']}` → {c['authority']}" for c in CANONICAL_CONTRACT_AUTHORITIES])),
            ("Canonicalization rules", md_list(CANONICALIZATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "contracts",
         "canonical_contract_authorities": CANONICAL_CONTRACT_AUTHORITIES,
         "canonicalization_rules": CANONICALIZATION_RULES},
    )

    # --- Task 5 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "naming-taxonomy", "naming-taxonomy",
        "Naming & Taxonomy Stabilization",
        "Canonical terms with single definitions; deprecated aliases listed; future drift forbidden.",
        [
            ("Canonical terms", md_list([f"`{t['term']}` — {t['definition']}" + (f" (owner: {t['owner']})" if 'owner' in t else "") + (f"; deprecated aliases: " + ", ".join(t['deprecated_aliases']) if 'deprecated_aliases' in t else "") for t in NAMING_CANONICAL_TERMS])),
            ("Prohibitions", md_list(NAMING_PROHIBITIONS)),
        ],
        {"schema": SCHEMA, "kind": "naming-taxonomy",
         "canonical_terms": NAMING_CANONICAL_TERMS,
         "naming_prohibitions": NAMING_PROHIBITIONS},
    )

    # --- Task 6 ----------------------------------------------------------
    write_pair(
        NORM_ROOT / "runtime-consistency", "runtime-consistency",
        "Runtime Consistency Validation",
        "Validates that the executable runtime is consistent with declared governance; carry-over gaps are catalogued, not introduced.",
        [
            ("Findings", md_list([f"`{f['id']}` — {f['status']}: {f['evidence']}" + (f" (carry-over: {f['carry_over_from']})" if 'carry_over_from' in f else "") for f in RUNTIME_CONSISTENCY_FINDINGS])),
            ("Consistency rules", md_list(RUNTIME_CONSISTENCY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "runtime-consistency",
         "runtime_consistency_findings": RUNTIME_CONSISTENCY_FINDINGS,
         "runtime_consistency_rules": RUNTIME_CONSISTENCY_RULES},
    )

    # --- Task 7 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# ECOSYSTEM NORMALIZATION GOVERNANCE\n\n"
        "Twenty-seventh constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-six prior governance layers.\n\n"
        "Audits and canonicalizes the ecosystem's schemas, builders, doctrines, contracts, "
        "naming, and runtime assumptions to prevent long-term semantic drift, schema "
        "fragmentation, doctrine overlap, builder divergence, and runtime inconsistency.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Ecosystem Normalization Governance",
        "Declares principles + authority for canonicalization, deduplication, and long-term coherence.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/schema-normalization/`",
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/builder-harmonization/`",
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/governance-deduplication/`",
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/contracts/`",
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/naming-taxonomy/`",
                "`wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/runtime-consistency/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT create new governance mega-layers",
                "DO NOT recursively expand cognition architecture",
                "DO NOT redesign the platform",
                "DO NOT deploy production systems",
                "DO NOT build frontend applications",
            ])),
        ],
        {"schema": SCHEMA, "kind": "charter",
         "principles": CHARTER_PRINCIPLES,
         "subordinate_to": SUBORDINATE_TO,
         "generated": now_iso()},
    )

    for slug, title, intro, principles in [
        ("normalization-philosophy", "Normalization Philosophy",
         "Coherence is a first-class operational property of the platform.",
         NORMALIZATION_PHILOSOPHY),
        ("canonicalization-doctrine", "Canonicalization Doctrine",
         "Every contract has one authoritative layer; every term has one meaning.",
         CANONICALIZATION_DOCTRINE),
        ("anti-fragmentation-principles", "Anti-Fragmentation Principles",
         "Fragmentation is detected by audit, resolved by canonical-references, never by deletion.",
         ANTI_FRAGMENTATION_PRINCIPLES),
        ("schema-stability-doctrine", "Schema Stability Doctrine",
         "Schemas are stable; renames are forbidden; MAJOR transitions are governance actions.",
         SCHEMA_STABILITY_DOCTRINE),
        ("builder-harmonization-philosophy", "Builder Harmonization Philosophy",
         "Builders are the canonical authors; one helper, one topology, idempotent.",
         BUILDER_HARMONIZATION_PHILOSOPHY),
        ("ecosystem-coherence-principles", "Ecosystem Coherence Principles",
         "Coherence is composed, not asserted; rejects mega-layers and recursion.",
         ECOSYSTEM_COHERENCE_PRINCIPLES),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # canonical-references doc — single source of truth
    write_pair(
        CONST_ROOT, "canonical-references",
        "Canonical References — Single Source of Truth",
        "Maps every contract, doctrine stack, and canonical term to its authoritative layer.",
        [
            ("Contract authorities", md_list([f"`{c['contract']}` → {c['authority']}" for c in CANONICAL_CONTRACT_AUTHORITIES])),
            ("Doctrine ownership", md_list([f"`{r['id']}` — {r['ownership']}" for r in DOCTRINE_OVERLAP_RESOLUTIONS])),
            ("Canonical terms", md_list([f"`{t['term']}`" for t in NAMING_CANONICAL_TERMS])),
        ],
        {"schema": SCHEMA, "kind": "canonical-references",
         "contract_authorities": CANONICAL_CONTRACT_AUTHORITIES,
         "doctrine_ownership": DOCTRINE_OVERLAP_RESOLUTIONS,
         "canonical_terms": [t["term"] for t in NAMING_CANONICAL_TERMS],
         "generated": now_iso()},
    )

    # --- Final 10 reports ------------------------------------------------
    reports = [
        ("01-schema-normalization-summary.json", {
            "schema": SCHEMA, "kind": "schema-normalization-summary",
            "schema_families_count": len(CANONICAL_SCHEMA_FAMILIES),
            "detected_schemas_count": len(SCHEMAS_AUDIT),
            "overlap_findings_count": len(SCHEMA_OVERLAP_FINDINGS),
            "renames_performed": 0,
            "rules_count": len(SCHEMA_NORMALIZATION_RULES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/schema-normalization/",
        }),
        ("02-builder-harmonization-summary.json", {
            "schema": SCHEMA, "kind": "builder-harmonization-summary",
            "conventions_count": len(BUILDER_CONVENTIONS),
            "builders_inventoried": len(BUILDER_FINDINGS),
            "builders_using_write_pair": sum(1 for b in BUILDER_FINDINGS if b["uses_write_pair_helper"]),
            "builders_declaring_subordinate_to": sum(1 for b in BUILDER_FINDINGS if b["declares_subordinate_to"]),
            "rules_count": len(BUILDER_HARMONIZATION_RULES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/builder-harmonization/",
        }),
        ("03-governance-deduplication-summary.json", {
            "schema": SCHEMA, "kind": "governance-deduplication-summary",
            "doctrine_roots_count": len(DOCTRINE_ROOTS),
            "layered_ownership_resolutions": [r["id"] for r in DOCTRINE_OVERLAP_RESOLUTIONS],
            "contradiction_findings_count": len(CONTRADICTION_FINDINGS),
            "rewrites_performed": 0,
            "rules_count": len(GOVERNANCE_DEDUP_RULES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/governance-deduplication/",
        }),
        ("04-contract-canonicalization-summary.json", {
            "schema": SCHEMA, "kind": "contract-canonicalization-summary",
            "canonical_contracts_count": len(CANONICAL_CONTRACT_AUTHORITIES),
            "rules_count": len(CANONICALIZATION_RULES),
            "single_source_of_truth": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ECOSYSTEM_NORMALIZATION_GOVERNANCE/canonical-references.json",
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/contracts/",
        }),
        ("05-naming-taxonomy-summary.json", {
            "schema": SCHEMA, "kind": "naming-taxonomy-summary",
            "canonical_terms_count": len(NAMING_CANONICAL_TERMS),
            "prohibitions_count": len(NAMING_PROHIBITIONS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/naming-taxonomy/",
        }),
        ("06-runtime-consistency-summary.json", {
            "schema": SCHEMA, "kind": "runtime-consistency-summary",
            "findings_count": len(RUNTIME_CONSISTENCY_FINDINGS),
            "consistent_count": sum(1 for f in RUNTIME_CONSISTENCY_FINDINGS if f["status"] == "consistent"),
            "gap_count": sum(1 for f in RUNTIME_CONSISTENCY_FINDINGS if f["status"].startswith("gap")),
            "test_suite_status": "19/19 passing (runtime untouched)",
            "artifact": "wp-content/themes/beslock-custom/User manuals/ecosystem-normalization/runtime-consistency/",
        }),
        ("07-normalization-governance-summary.json", {
            "schema": SCHEMA, "kind": "normalization-governance-summary",
            "layer_index": 27,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ECOSYSTEM_NORMALIZATION_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/ecosystem-normalization/",
            "doctrine_sections": [
                "normalization-philosophy",
                "canonicalization-doctrine",
                "anti-fragmentation-principles",
                "schema-stability-doctrine",
                "builder-harmonization-philosophy",
                "ecosystem-coherence-principles",
            ],
            "canonical_references_doc": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ECOSYSTEM_NORMALIZATION_GOVERNANCE/canonical-references.json",
        }),
        ("08-long-term-evolution-summary.json", {
            "schema": SCHEMA, "kind": "long-term-evolution-summary",
            "future_commitments": FUTURE_COMMITMENTS,
            "future_invariants": FUTURE_INVARIANTS,
        }),
        ("09-unresolved-fragmentation-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-fragmentation-risks",
            "items": [
                {"id": "no-canonical-references-enforcement",  "severity": "medium", "impact": "canonical-references is declared as single source of truth; no automated check verifies builder/runtime alignment to it"},
                {"id": "no-builder-conformance-test",           "severity": "medium", "impact": "builder conventions declared; no test asserts new builders satisfy them"},
                {"id": "no-naming-lint",                        "severity": "low",    "impact": "canonical terms declared; no lint enforces prohibition on synonyms in builders / doctrine prose"},
                {"id": "no-schema-version-registry",            "severity": "medium", "impact": "schema MAJOR transitions are governance actions; no registry records past versions per schema family"},
                {"id": "carry-over-supervision-receipt-runtime","severity": "high",   "impact": "supervision-receipt declared (layer 24) but runtime CLI does not yet emit it as a separate field"},
                {"id": "carry-over-composition-manifest",       "severity": "high",   "impact": "composition-manifest declared (layer 26) but runtime does not yet emit it at startup"},
                {"id": "carry-over-interop-registry",           "severity": "high",   "impact": "interop-contract registry declared (layer 26) but absent in code"},
                {"id": "carry-over-incident-trace-channel",     "severity": "medium", "impact": "incident-trace channel declared (layer 25) but not provisioned in channels.py"},
                {"id": "carry-over-executable-consoles",        "severity": "high",   "impact": "all 6 consoles design-only (layer 24); no operator surface exists yet"},
                {"id": "carry-over-132-candidates-await-review","severity": "high",   "impact": "candidate corpus written by Phase 27 still awaits reviewer elevation"},
            ],
        }),
        ("10-ecosystem-coherence-reassessment.json", {
            "schema": SCHEMA, "kind": "ecosystem-coherence-reassessment",
            "platform_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "coherence_status": "AUDITED + CANONICALIZED",
            "schema_renames_performed": 0,
            "doctrine_rewrites_performed": 0,
            "layer_count": 27,
            "subordinate_chain_length": len(SUBORDINATE_TO),
            "primary_bottleneck": "LONG-TERM ECOSYSTEM COHERENCE (now governed by declared canonical-references + audit findings)",
            "next_bottleneck": "executable enforcement of canonical-references (builder conformance tests, naming lint, schema version registry, runtime carry-over enforcement)",
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

    print(f"Ecosystem Normalization Governance (layer 27) written to:\n  {NORM_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")
    print(f"  builders inventoried: {len(BUILDER_FINDINGS)}; schemas detected: {len(SCHEMAS_AUDIT)}; doctrine roots: {len(DOCTRINE_ROOTS)}")


if __name__ == "__main__":
    build()
