"""
Phase 31 — OPERATIONAL ENVIRONMENT & INTEGRATION GOVERNANCE.

Constitutional layer 25. Modeling-only. Subordinate to knowledge-core and
to all twenty-four prior governance layers.

Writes:
  - the seven environment-governance artifact folders under
    `wp-content/themes/beslock-custom/User manuals/environment-governance/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ENVIRONMENT_AND_INTEGRATION_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/environment-integration/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
No production deployment, no infrastructure automation, no frontends,
no autonomous integrations.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
ENV_ROOT = THEME_ROOT / "environment-governance"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "ENVIRONMENT_AND_INTEGRATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "environment-integration"

SCHEMA = "environment-integration-governance/1.0"


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
    "HUMAN_OPERATIONS",
]


# =============================================================================
# TASK 1 — OPERATIONAL ENVIRONMENT MODEL
# =============================================================================

ENVIRONMENTS = [
    {"id": "local-supervised-runtime",  "trust_level": "high (operator-bounded)",  "supervision_level": "full HITL on every checkpoint", "constraints": ["single operator", "append-only logs to local disk", "no outbound writes"], "isolation": "process-local; no network egress required"},
    {"id": "staging-environment",       "trust_level": "medium",                    "supervision_level": "full HITL + dual-review on promotions",   "constraints": ["synthetic OEM bindings", "no live OEM writes", "no production knowledge-core writes"], "isolation": "dedicated staging trust-zone; no cross-env reads"},
    {"id": "controlled-pilot",          "trust_level": "medium (scoped)",           "supervision_level": "full HITL + escalation-supervisor on slice-halt", "constraints": ["bounded operator pool", "slice-level kill-switch", "fixed product subset"], "isolation": "pilot trust-zone; no governance-console exposure"},
    {"id": "future-production",         "trust_level": "governed (declared, not active)", "supervision_level": "full HITL + dual-review + auditor co-signature for emergency actions", "constraints": ["MUST satisfy all promotion gates from layer 22", "MUST satisfy all health indicators from layer 23", "MUST satisfy all operator-readiness items from layer 24"], "isolation": "production trust-zone; one-way ingress for OEM evidence"},
    {"id": "oem-ingestion-environment", "trust_level": "semi-trusted",              "supervision_level": "OEM-reviewer dual-review",                "constraints": ["read-only OEM source mirrors", "checksum-verified ingest", "no runtime emission from this env"], "isolation": "ingestion trust-zone; outputs only to staging"},
    {"id": "reviewer-operation-environment","trust_level": "high (reviewer-bounded)","supervision_level": "reviewer claim + queue ceiling",         "constraints": ["per-reviewer concurrent claim ceiling", "no production demotion writes", "all actions emit supervision-receipt"], "isolation": "reviewer trust-zone; read-only against runtime channels"},
]

ENVIRONMENT_INVARIANTS = [
    "every environment declares a trust level, a supervision level, and an isolation guarantee",
    "no environment ever inherits trust from another environment",
    "no environment ever shares write paths with a higher-trust environment",
    "no environment ever bypasses the supervision level declared by the layer above it",
    "no environment runs without an append-only log destination",
]


# =============================================================================
# TASK 2 — DEPLOYMENT BOUNDARIES
# =============================================================================

DEPLOYMENT_BOUNDARIES = [
    {"id": "runtime-boundary",      "rule": "the runtime emits packages; it never writes canonical knowledge-core JSON"},
    {"id": "deployment-isolation",  "rule": "each environment is a separate deployment unit; no shared mutable state across envs"},
    {"id": "cognition-isolation",   "rule": "cognition (retrieval/assembly/escalation) runs only inside the runtime boundary; never inside ingestion or reviewer envs"},
    {"id": "reviewer-isolation",    "rule": "reviewer surfaces never co-locate with the runtime emission path; reviewer writes target staging, not production"},
    {"id": "escalation-isolation",  "rule": "escalation channels are append-only and live in their own boundary; demotions are events, not direct mutations"},
    {"id": "provenance-isolation",  "rule": "provenance records (manifests, source SHAs, lineage) are write-once; any environment may read, only governance pipelines may append"},
    {"id": "operational-segmentation","rule": "operational segments (runtime / reviewer / governance / ingestion / audit) are declared; cross-segment calls are forbidden unless declared by an integration contract"},
]

BOUNDARY_INVARIANTS = [
    "no boundary is ever crossed implicitly; every crossing is a declared contract",
    "no boundary permits silent escalation of trust",
    "no boundary permits a higher-trust environment to read from a lower-trust environment without verification",
    "no boundary permits write paths from a lower-trust environment into a higher-trust environment",
    "every boundary crossing emits an observability event",
]


# =============================================================================
# TASK 3 — EXTERNAL INTEGRATION CONTRACTS
# =============================================================================

INTEGRATION_CONTRACTS = [
    {"id": "wordpress",            "trust_contract": "render-only consumer of knowledge-core JSON; no write path back", "interaction_contract": "read-only via theme/template; no runtime invocation from PHP", "supervision_contract": "all rendered packages carry a supervision-receipt id", "provenance_guarantee": "every rendered fragment cites manifest_id + source_files[].sha256", "escalation_obligation": "render path MUST surface candidate-only / unresolved markers verbatim"},
    {"id": "retrieval-apis",       "trust_contract": "read-only against runtime channels", "interaction_contract": "request/response over declared schema; no streaming side effects", "supervision_contract": "every response carries supervision-receipt + manifest_id", "provenance_guarantee": "responses include provenance block before content block", "escalation_obligation": "responses MUST refuse to omit candidate_only when present"},
    {"id": "oem-ingestion-systems","trust_contract": "semi-trusted; mirrors OEM sources via checksum-verified ingest", "interaction_contract": "one-way: OEM source → ingestion env → staging; never directly to production", "supervision_contract": "OEM-reviewer dual-review on every binding", "provenance_guarantee": "every ingested artifact records source url, sha256, fetched_at, fetched_by", "escalation_obligation": "checksum mismatch halts ingestion and emits an escalation-trace event"},
    {"id": "observability-systems","trust_contract": "read-only consumer of NDJSON channels", "interaction_contract": "tail-based subscription; no back-channel mutation", "supervision_contract": "consumer identity is declared; no anonymous consumers", "provenance_guarantee": "events are immutable; consumers receive verbatim records", "escalation_obligation": "consumers MUST forward unsafe-runtime events to escalation-console subscribers"},
    {"id": "operational-consoles", "trust_contract": "operator-surfaces (layer 24); design-only here", "interaction_contract": "all actions go through declared decision sets per checkpoint", "supervision_contract": "every console action carries operator id + supervision-receipt", "provenance_guarantee": "consoles render provenance before recommendation", "escalation_obligation": "consoles MUST surface escalation-trace events without delay"},
    {"id": "future-copilots",      "trust_contract": "supervised assistive surface; never autonomous", "interaction_contract": "operator-led activation; per-checkpoint approval", "supervision_contract": "every copilot suggestion is logged + reversible", "provenance_guarantee": "copilots cite manifest_id + confidence tier alongside every suggestion", "escalation_obligation": "copilots MUST refuse to suggest at candidate-only + irreversible-adjacent context"},
    {"id": "future-multimodal-runtimes","trust_contract": "subordinate to runtime governance; new modalities are channels, not new architecture", "interaction_contract": "modalities subscribe to existing NDJSON channels; do not introduce parallel channels", "supervision_contract": "every modality declares its operator profile mapping", "provenance_guarantee": "every modality renders provenance and confidence in its native form", "escalation_obligation": "modalities MUST honor halt and demote events from the runtime"},
]

CONTRACT_INVARIANTS = [
    "every integration is governed by a declared trust contract; undeclared integrations are forbidden",
    "no integration may write to canonical knowledge-core JSON",
    "no integration may bypass supervision-receipt emission",
    "no integration may suppress provenance or candidate-only markers for UX reasons",
    "every integration is reversible; revocation is a first-class governance action",
]


# =============================================================================
# TASK 4 — RUNTIME SANDBOXING & ISOLATION
# =============================================================================

SANDBOX_PATTERNS = [
    {"id": "runtime-sandbox",          "purpose": "execute retrieval + assembly + escalation under bounded scope; no outbound writes"},
    {"id": "unsafe-runtime-containment","purpose": "any runtime that fails a safety predicate is demoted to a quarantine sandbox; emission is suspended"},
    {"id": "escalation-quarantine",    "purpose": "slices on escalation hold are isolated from new emissions until escalation-supervisor decision"},
    {"id": "reviewer-safe-execution",  "purpose": "reviewer actions execute in a sandbox that cannot reach production write paths"},
    {"id": "provenance-safe-isolation","purpose": "provenance records are mounted read-only into every sandbox; mutation paths require governance pipeline auth"},
    {"id": "replay-safe-environment",  "purpose": "replay sandbox executes against frozen orchestration-trace input; outputs go to a side channel, never to production"},
]

SANDBOX_INVARIANTS = [
    "every sandbox declares its inputs, outputs, and isolation guarantees",
    "no sandbox writes to a higher-trust environment",
    "no sandbox shares mutable state with another sandbox",
    "every sandbox emits an append-only execution log",
    "every sandbox is reproducible: same inputs → same outputs",
]


# =============================================================================
# TASK 5 — INFRASTRUCTURE TRUST ZONES
# =============================================================================

TRUST_ZONES = [
    {"id": "trusted-operational-zone",  "examples": ["runtime-emission path", "production knowledge-core read path"], "rule": "highest trust; reads are unrestricted; writes require governance pipeline auth"},
    {"id": "semi-trusted-ingestion-zone","examples": ["OEM ingestion env", "candidate enrichment workspace"],         "rule": "may read trusted-zone provenance; may write only to staging"},
    {"id": "reviewer-controlled-zone",  "examples": ["reviewer-workbench surfaces", "review queue store"],            "rule": "reviewer-bounded; may stage decisions; may not directly mutate production"},
    {"id": "escalation-zone",           "examples": ["escalation-trace channel", "escalation console surfaces"],      "rule": "append-only; isolated from new emissions until decision"},
    {"id": "quarantined-runtime-zone",  "examples": ["unsafe-runtime sandbox", "rolled-back slice"],                  "rule": "no emission; read-only access to provenance; awaits operator decision"},
    {"id": "prohibited-operational-zone","examples": ["public internet writes", "unbounded autonomous agents", "untracked LLM calls"], "rule": "categorically forbidden; integration with these zones is a governance violation"},
]

TRUST_ZONE_INVARIANTS = [
    "every artifact, sandbox, and integration is mapped to exactly one trust zone",
    "no zone may inherit privileges from another; trust is declared per-zone",
    "no prohibited zone is ever introduced as a 'temporary' integration",
    "zone changes are governance actions; they are dual-audited",
    "every zone has a declared revocation path",
]


# =============================================================================
# TASK 6 — ENVIRONMENT LIFECYCLE
# =============================================================================

ENVIRONMENT_LIFECYCLE_STATES = [
    {"id": "proposed",      "description": "declared but not provisioned"},
    {"id": "provisioned",   "description": "infrastructure declared; not yet receiving traffic"},
    {"id": "active",        "description": "receiving traffic under declared supervision level"},
    {"id": "under-review",  "description": "active with elevated audit; promotion or demotion pending"},
    {"id": "deprecated",    "description": "frozen at last state; reads only; no new writes"},
    {"id": "quarantined",   "description": "isolated due to safety event; no traffic; replay-only access"},
    {"id": "retired",       "description": "tombstoned; provenance retained; no infra; no surfaces"},
]

LIFECYCLE_TRANSITIONS = [
    {"from": "proposed",     "to": "provisioned", "actor": "governance-maintainer", "requires": "charter approval + trust-zone assignment"},
    {"from": "provisioned",  "to": "active",      "actor": "governance-maintainer", "requires": "promotion gates from layer 22 satisfied"},
    {"from": "active",       "to": "under-review","actor": "operational-auditor",   "requires": "raised finding or health indicator threshold"},
    {"from": "under-review", "to": "active",      "actor": "governance-maintainer + auditor co-sign", "requires": "finding closed; no open critical health indicators"},
    {"from": "under-review", "to": "quarantined", "actor": "escalation-supervisor", "requires": "safety event or replay drift > floor"},
    {"from": "active",       "to": "deprecated",  "actor": "governance-maintainer", "requires": "successor environment in active state"},
    {"from": "deprecated",   "to": "retired",     "actor": "governance-maintainer + auditor co-sign", "requires": "no open references; provenance archived"},
    {"from": "quarantined",  "to": "active",      "actor": "governance-maintainer + auditor co-sign", "requires": "incident closed; replay deterministic; rollback verified"},
    {"from": "quarantined",  "to": "retired",     "actor": "governance-maintainer + auditor co-sign", "requires": "incident review complete; environment unrecoverable"},
]

LIFECYCLE_INVARIANTS = [
    "every transition is a governance action with a declared actor and rationale",
    "no environment may be silently retired; deprecation precedes retirement",
    "no quarantined environment may resume active state without auditor co-signature",
    "every transition emits an environment-lifecycle-trace event",
    "tombstones are immutable; retired environments are never re-activated under the same id",
]


# =============================================================================
# TASK 7 — INCIDENT CONTAINMENT
# =============================================================================

INCIDENT_CONTAINMENT_PATTERNS = [
    {"id": "runtime-incident-isolation","trigger": "safety predicate failure or replay drift > floor", "containment": "halt slice → quarantine sandbox → emit incident-trace event"},
    {"id": "escalation-containment",    "trigger": "escalation-trace event with no responder",          "containment": "auto-route to escalation-supervisor; raise SLA tier; suspend dependent slices"},
    {"id": "rollback-containment",      "trigger": "operator-initiated rollback exceeding declared scope", "containment": "halt rollback; require governance + auditor co-sign before fan-out"},
    {"id": "provenance-breach-handling","trigger": "provenance hash mismatch or missing source binding","containment": "demote affected node tier to candidate; halt emissions citing the node; escalation-supervisor notified"},
    {"id": "unsafe-runtime-shutdown",   "trigger": "unrecoverable safety failure",                      "containment": "shut down emission path in env; preserve append-only logs; quarantine env"},
    {"id": "replay-assisted-incident-review","trigger": "any incident closed",                          "containment": "replay frozen orchestration-trace; compare to live; emit replay-trace; auditor finding"},
]

CONTAINMENT_INVARIANTS = [
    "no incident is ever silently absorbed; every incident emits an event",
    "no incident response writes to canonical knowledge-core JSON",
    "no incident response bypasses the supervision-receipt",
    "every containment action is reversible by an equal-or-higher governance decision",
    "every incident closure is accompanied by a replay-validated finding",
]


# =============================================================================
# TASK 8 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs the environments and integrations through which the runtime may exist.",
    "All environments are declared, trust-tiered, and supervision-bound.",
    "All integrations are governed by declared trust contracts; undeclared integrations are forbidden.",
    "All boundary crossings are events; none are silent.",
    "All deployment remains subordinate to governance, provenance, supervision, and trust-boundary enforcement.",
    "No production deployment is performed by this layer; this layer governs the conditions under which deployment may later occur.",
    "Subordinate to knowledge-core and to all twenty-four prior governance layers.",
]

ENVIRONMENT_PHILOSOPHY = [
    "Environments are declared facts, not emergent states.",
    "Environments inherit nothing implicitly; trust is per-environment.",
    "Environments are reversible: deprecation, quarantine, and retirement are first-class.",
    "Environments exist to serve governance, not to bypass it.",
]

OPERATIONAL_ISOLATION_DOCTRINE = [
    "Isolation is the default; integration is the declared exception.",
    "Isolation protects provenance, supervision, and reversibility above performance.",
    "Isolation is measured by observable boundary crossings, not by hopeful policy.",
    "Isolation failures are incidents, not anomalies.",
]

INTEGRATION_GOVERNANCE_PHILOSOPHY = [
    "Every integration is a contract; every contract is auditable.",
    "Integrations may not silently widen scope; widening is a governance action.",
    "Integrations may not silently degrade provenance or supervision guarantees.",
    "Integrations are revocable; revocation is a first-class event.",
]

TRUST_BOUNDARY_DOCTRINE = [
    "Trust is declared per-zone; it is never inherited.",
    "Trust is asymmetric: higher-trust never imports from lower-trust without verification.",
    "Trust is observable: every crossing emits an event.",
    "Trust is revocable: any zone may be demoted by governance action.",
]

SANDBOXING_PHILOSOPHY = [
    "Sandboxes exist to contain effects, not to permit them.",
    "Sandboxes are reproducible; non-determinism is a defect.",
    "Sandboxes may not write to higher-trust zones, ever.",
    "Sandboxes are first-class operational artifacts; they are governed, not improvised.",
]

DEPLOYMENT_BOUNDARY_PRINCIPLES = [
    "Deployment is subordinate to governance; governance never trails deployment.",
    "Deployment never expands scope without a governance action.",
    "Deployment never bypasses promotion gates, health indicators, or operator-readiness items.",
    "Deployment is reversible; rollback is a first-class operational action, not an exception.",
]


# =============================================================================
# TASK 9 — FUTURE DEPLOYMENT READINESS
# =============================================================================

FUTURE_COMMITMENTS = [
    "supervised production pilots are gated by promotion gates (layer 22), health indicators (layer 23), and operator-readiness items (layer 24)",
    "operational deployment slices are bounded by product × domain × environment; no global deployment exists",
    "reviewer ecosystems are provisioned through the reviewer registry; revocation remains first-class",
    "OEM integration pipelines are gated by checksum-verified ingest + dual-review binding",
    "future operator consoles inherit all invariants from layer 24; new consoles are not new architecture",
    "multimodal runtime environments subscribe to existing NDJSON channels; they do not introduce parallel channels",
]

FUTURE_INVARIANTS = [
    "no deployment is ever performed without a declared environment, trust zone, and supervision level",
    "no integration is ever introduced without a declared trust contract",
    "no boundary is ever crossed silently",
    "no environment is ever resumed from quarantine without auditor co-signature",
    "no macro-governance mega-layer is spawned by environment-and-integration work",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    ENV_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "environment-model", "environment-model",
        "Operational Environment Model",
        "Six declared operational environments with trust levels, supervision levels, constraints, and isolation guarantees.",
        [
            ("Environments", md_list([f"`{e['id']}` — trust: {e['trust_level']}; supervision: {e['supervision_level']}; isolation: {e['isolation']}" for e in ENVIRONMENTS])),
            ("Invariants", md_list(ENVIRONMENT_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "environment-model",
         "environments": ENVIRONMENTS,
         "environment_invariants": ENVIRONMENT_INVARIANTS},
    )

    # --- Task 2 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "deployment-boundaries", "deployment-boundaries",
        "Deployment Boundary Governance",
        "Seven declared deployment boundaries; every crossing is a contract and an observable event.",
        [
            ("Boundaries", md_list([f"`{b['id']}` — {b['rule']}" for b in DEPLOYMENT_BOUNDARIES])),
            ("Invariants", md_list(BOUNDARY_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "deployment-boundaries",
         "deployment_boundaries": DEPLOYMENT_BOUNDARIES,
         "boundary_invariants": BOUNDARY_INVARIANTS},
    )

    # --- Task 3 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "integration-contracts", "integration-contracts",
        "External Integration Contracts",
        "Seven declared integration contracts; undeclared integrations are forbidden.",
        [
            ("Contracts", md_list([f"`{c['id']}` — trust: {c['trust_contract']}" for c in INTEGRATION_CONTRACTS])),
            ("Invariants", md_list(CONTRACT_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "integration-contracts",
         "integration_contracts": INTEGRATION_CONTRACTS,
         "contract_invariants": CONTRACT_INVARIANTS},
    )

    # --- Task 4 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "sandboxing", "sandboxing",
        "Runtime Sandboxing & Isolation",
        "Six sandbox patterns; reproducible, append-only, no writes to higher-trust zones.",
        [
            ("Patterns", md_list([f"`{s['id']}` — {s['purpose']}" for s in SANDBOX_PATTERNS])),
            ("Invariants", md_list(SANDBOX_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "sandboxing",
         "sandbox_patterns": SANDBOX_PATTERNS,
         "sandbox_invariants": SANDBOX_INVARIANTS},
    )

    # --- Task 5 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "trust-zones", "trust-zones",
        "Infrastructure Trust Zones",
        "Six declared trust zones, including a categorically prohibited zone.",
        [
            ("Zones", md_list([f"`{z['id']}` — {z['rule']}" for z in TRUST_ZONES])),
            ("Invariants", md_list(TRUST_ZONE_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "trust-zones",
         "trust_zones": TRUST_ZONES,
         "trust_zone_invariants": TRUST_ZONE_INVARIANTS},
    )

    # --- Task 6 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "environment-lifecycle", "environment-lifecycle",
        "Environment Lifecycle Governance",
        "Seven lifecycle states + nine declared transitions; every transition is a governance action.",
        [
            ("States", md_list([f"`{s['id']}` — {s['description']}" for s in ENVIRONMENT_LIFECYCLE_STATES])),
            ("Transitions", md_list([f"`{t['from']}` → `{t['to']}` — actor: {t['actor']}; requires: {t['requires']}" for t in LIFECYCLE_TRANSITIONS])),
            ("Invariants", md_list(LIFECYCLE_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "environment-lifecycle",
         "lifecycle_states": ENVIRONMENT_LIFECYCLE_STATES,
         "lifecycle_transitions": LIFECYCLE_TRANSITIONS,
         "lifecycle_invariants": LIFECYCLE_INVARIANTS},
    )

    # --- Task 7 ----------------------------------------------------------
    write_pair(
        ENV_ROOT / "incident-containment", "incident-containment",
        "Operational Incident Containment",
        "Six containment patterns; every incident emits an event and is closed by a replay-validated finding.",
        [
            ("Patterns", md_list([f"`{p['id']}` — trigger: {p['trigger']}; containment: {p['containment']}" for p in INCIDENT_CONTAINMENT_PATTERNS])),
            ("Invariants", md_list(CONTAINMENT_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "incident-containment",
         "incident_containment_patterns": INCIDENT_CONTAINMENT_PATTERNS,
         "containment_invariants": CONTAINMENT_INVARIANTS},
    )

    # --- Task 8 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# ENVIRONMENT AND INTEGRATION GOVERNANCE\n\n"
        "Twenty-fifth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-four prior governance layers.\n\n"
        "Governs the environments, deployment boundaries, integration contracts, sandboxes, "
        "trust zones, environment lifecycle, and incident containment under which the runtime "
        "may safely exist and interact with external systems.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Environment and Integration Governance",
        "Declares principles + authority for environment, deployment, and integration governance.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/environment-model/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/deployment-boundaries/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/integration-contracts/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/sandboxing/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/trust-zones/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/environment-lifecycle/`",
                "`wp-content/themes/beslock-custom/User manuals/environment-governance/incident-containment/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT deploy production systems",
                "DO NOT implement infrastructure automation",
                "DO NOT build frontend applications",
                "DO NOT create autonomous integrations",
                "DO NOT expand cognition recursively",
            ])),
        ],
        {"schema": SCHEMA, "kind": "charter",
         "principles": CHARTER_PRINCIPLES,
         "subordinate_to": SUBORDINATE_TO,
         "generated": now_iso()},
    )

    for slug, title, intro, principles in [
        ("environment-philosophy", "Environment Philosophy",
         "Environments are declared facts, not emergent states.",
         ENVIRONMENT_PHILOSOPHY),
        ("operational-isolation-doctrine", "Operational Isolation Doctrine",
         "Isolation is the default; integration is the declared exception.",
         OPERATIONAL_ISOLATION_DOCTRINE),
        ("integration-governance-philosophy", "Integration Governance Philosophy",
         "Every integration is a contract; every contract is auditable.",
         INTEGRATION_GOVERNANCE_PHILOSOPHY),
        ("trust-boundary-doctrine", "Trust Boundary Doctrine",
         "Trust is declared per-zone, asymmetric, observable, and revocable.",
         TRUST_BOUNDARY_DOCTRINE),
        ("sandboxing-philosophy", "Sandboxing Philosophy",
         "Sandboxes exist to contain effects, not to permit them.",
         SANDBOXING_PHILOSOPHY),
        ("deployment-boundary-principles", "Deployment Boundary Principles",
         "Deployment is subordinate to governance; rollback is first-class.",
         DEPLOYMENT_BOUNDARY_PRINCIPLES),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # --- Final 10 reports ------------------------------------------------
    reports = [
        ("01-environment-model-summary.json", {
            "schema": SCHEMA, "kind": "environment-model-summary",
            "environments": [e["id"] for e in ENVIRONMENTS],
            "invariants_count": len(ENVIRONMENT_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/environment-model/",
        }),
        ("02-deployment-boundary-summary.json", {
            "schema": SCHEMA, "kind": "deployment-boundary-summary",
            "boundaries": [b["id"] for b in DEPLOYMENT_BOUNDARIES],
            "invariants_count": len(BOUNDARY_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/deployment-boundaries/",
        }),
        ("03-integration-contract-summary.json", {
            "schema": SCHEMA, "kind": "integration-contract-summary",
            "contracts": [c["id"] for c in INTEGRATION_CONTRACTS],
            "invariants_count": len(CONTRACT_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/integration-contracts/",
        }),
        ("04-sandboxing-summary.json", {
            "schema": SCHEMA, "kind": "sandboxing-summary",
            "patterns": [s["id"] for s in SANDBOX_PATTERNS],
            "invariants_count": len(SANDBOX_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/sandboxing/",
        }),
        ("05-trust-zone-summary.json", {
            "schema": SCHEMA, "kind": "trust-zone-summary",
            "zones": [z["id"] for z in TRUST_ZONES],
            "invariants_count": len(TRUST_ZONE_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/trust-zones/",
        }),
        ("06-environment-lifecycle-summary.json", {
            "schema": SCHEMA, "kind": "environment-lifecycle-summary",
            "states": [s["id"] for s in ENVIRONMENT_LIFECYCLE_STATES],
            "transitions_count": len(LIFECYCLE_TRANSITIONS),
            "invariants_count": len(LIFECYCLE_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/environment-lifecycle/",
        }),
        ("07-incident-containment-summary.json", {
            "schema": SCHEMA, "kind": "incident-containment-summary",
            "patterns": [p["id"] for p in INCIDENT_CONTAINMENT_PATTERNS],
            "invariants_count": len(CONTAINMENT_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/environment-governance/incident-containment/",
        }),
        ("08-environment-governance-summary.json", {
            "schema": SCHEMA, "kind": "environment-governance-summary",
            "layer_index": 25,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/ENVIRONMENT_AND_INTEGRATION_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/environment-integration/",
            "doctrine_sections": [
                "environment-philosophy",
                "operational-isolation-doctrine",
                "integration-governance-philosophy",
                "trust-boundary-doctrine",
                "sandboxing-philosophy",
                "deployment-boundary-principles",
            ],
        }),
        ("09-unresolved-deployment-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-deployment-risks",
            "items": [
                {"id": "no-provisioned-environments",       "severity": "high",   "impact": "all six environments are declared; only local-supervised-runtime exists in fact"},
                {"id": "no-trust-zone-mapping-enforcement", "severity": "high",   "impact": "trust zones declared; no automated enforcement maps artifacts to zones"},
                {"id": "no-integration-contract-registry",  "severity": "high",   "impact": "contracts declared; no registry validates that production integrations match a declared contract"},
                {"id": "no-sandbox-runtime",                "severity": "high",   "impact": "sandbox patterns declared; no executable sandbox harness yet"},
                {"id": "no-environment-lifecycle-store",    "severity": "medium", "impact": "lifecycle states + transitions declared; no store records env state per id"},
                {"id": "no-incident-trace-channel",         "severity": "medium", "impact": "incident-trace events declared; channel not yet provisioned in observability"},
                {"id": "no-checksum-verified-ingest",       "severity": "high",   "impact": "OEM ingestion contract requires checksum-verified ingest; ingest tooling not yet implemented"},
                {"id": "no-quarantine-resume-co-sign-flow", "severity": "medium", "impact": "quarantine→active transition requires auditor co-sign; no flow enforces it"},
                {"id": "carry-overs-from-phases-28-30",     "severity": "high",   "impact": "no executable consoles, identity store, claim mediator, explanation renderer, reviewer registry, queue store, event log, OEM binding store; 132 candidates still await elevation"},
            ],
        }),
        ("10-deployment-readiness-reassessment.json", {
            "schema": SCHEMA, "kind": "deployment-readiness-reassessment",
            "platform_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "environment_governance_status": "MODELED (executable provisioning pending)",
            "primary_bottleneck": "SAFE ENVIRONMENTAL INTEGRATION + DEPLOYMENT BOUNDARY GOVERNANCE (now governed by declared model)",
            "next_bottleneck": "executable enforcement of environment provisioning, trust-zone mapping, integration registry, sandbox harness, lifecycle store, and incident-trace channel",
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

    print(f"Environment & Integration Governance (layer 25) written to:\n  {ENV_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")


if __name__ == "__main__":
    build()
