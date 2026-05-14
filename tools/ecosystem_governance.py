"""
Phase 22 — ECOSYSTEM INTEROPERABILITY & FEDERATION (modeling-only).

Sixteenth constitutional layer. Subordinate to knowledge-core and to all
fifteen prior governance layers. Models how multiple operational cognition
runtimes coexist, coordinate, exchange context, preserve continuity, and
interoperate safely across a federated operational ecosystem.

Hard exclusions (verbatim):
- DO NOT implement runtime federation
- DO NOT build chatbot systems
- DO NOT generate images
- DO NOT create PDFs
- DO NOT implement autonomous ecosystems
- DO NOT build frontend systems

Idempotent. Non-destructive. Reads no per-product knowledge-core files.

Writes:
- KNOWLEDGE_BUILDING/ECOSYSTEM_INTEROPERABILITY_GOVERNANCE/
    README.md
    00-charter.(md|json)
    interoperability-models/         (md+json)
    runtime-contracts/               (md+json)
    shared-context/                  (md+json)
    escalation/                      (md+json)
    orchestration/                   (md+json)
    observability/                   (md+json)
    safety-governance/               (md+json)
    ecosystem-governance/            (md+json)
    future-ecosystem-readiness/      (md+json)
- _repository-governance/reports/ecosystem/01..10
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "ECOSYSTEM_INTEROPERABILITY_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "ecosystem"

SCHEMA = "ecosystem-interoperability-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items):
    return "\n".join(f"- {x}" for x in items)


def write_pair(folder: Path, slug: str, title: str, intro: str, sections, payload: dict):
    folder.mkdir(parents=True, exist_ok=True)
    md_lines = [f"# {title}", "", intro, ""]
    for h, body in sections:
        md_lines.append(f"## {h}")
        md_lines.append("")
        md_lines.append(body)
        md_lines.append("")
    (folder / f"{slug}.md").write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")
    (folder / f"{slug}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Charter
# ---------------------------------------------------------------------------

CHARTER_PRINCIPLES = [
    "This ecosystem layer is itself modeling-only; it federates nothing.",
    "Federation is supervised by default; no autonomous cross-runtime behavior is modelled here.",
    "Runtimes interoperate only via declared inter-runtime contracts.",
    "Every runtime in the federation remains subordinate to the same governed knowledge-core.",
    "Cross-runtime exchange is read-only into knowledge-core, append-only into shared continuity.",
    "Provenance crosses runtime boundaries; an unattributable cross-runtime message is invalid.",
    "Confidence tier, P-tier, role, and irreversibility flags are immutable across runtime boundaries.",
    "Degraded federation is a first-class state; safest defaults always apply.",
    "Escalation across runtimes is monotonic; downgrades across runtime boundaries are unsafe.",
    "Ecosystem coordination cannot create cognitive capabilities — only coordinate declared ones.",
]

CHARTER_AUTHORITY = [
    "Declares the catalog of interoperability models between future runtime kinds.",
    "Declares inter-runtime contracts (context / escalation / reasoning / orchestration / shared-cognition).",
    "Declares shared operational context kinds and inheritance rules across runtimes.",
    "Declares ecosystem-wide escalation flows, propagation rules, and OEM federation handoff.",
    "Declares federated orchestration roles, coordination, delegation, and coexistence rules.",
    "Declares ecosystem observability requirements and trace-federation rules.",
    "Declares prohibited cross-runtime behaviors and unsafe federation states.",
    "Declares the future-ecosystem consumer gate set.",
    "Declares that ecosystem interoperability remains subordinate to knowledge-core forever.",
]

# ---------------------------------------------------------------------------
# TASK 1 — Interoperability models
# ---------------------------------------------------------------------------

RUNTIME_KINDS = [
    "onboarding-runtime",
    "troubleshooting-runtime",
    "retrieval-runtime",
    "operational-copilot",
    "visual-assistance-runtime",
    "publication-runtime",
    "continuity-system",
]

INTEROPERABILITY_MODELS = [
    {
        "id": "retrieval↔copilot",
        "from": "retrieval-runtime",
        "to": "operational-copilot",
        "kind": "read-only context supply",
        "destructive_surface": False,
    },
    {
        "id": "copilot↔troubleshooting",
        "from": "operational-copilot",
        "to": "troubleshooting-runtime",
        "kind": "supervised handoff with continuity snapshot",
        "destructive_surface": False,
    },
    {
        "id": "copilot↔onboarding",
        "from": "operational-copilot",
        "to": "onboarding-runtime",
        "kind": "supervised handoff with intent declaration",
        "destructive_surface": False,
    },
    {
        "id": "troubleshooting↔visual",
        "from": "troubleshooting-runtime",
        "to": "visual-assistance-runtime",
        "kind": "read-only visual surface request (gated by visual-risk freeze)",
        "destructive_surface": False,
    },
    {
        "id": "onboarding↔continuity",
        "from": "onboarding-runtime",
        "to": "continuity-system",
        "kind": "checkpoint emission (append-only)",
        "destructive_surface": False,
    },
    {
        "id": "troubleshooting↔continuity",
        "from": "troubleshooting-runtime",
        "to": "continuity-system",
        "kind": "checkpoint + hypothesis snapshot (append-only)",
        "destructive_surface": False,
    },
    {
        "id": "any↔publication",
        "from": "any-runtime",
        "to": "publication-runtime",
        "kind": "read-only publication contract; never bypasses lifecycle P-tier gates",
        "destructive_surface": False,
    },
    {
        "id": "continuity↔any",
        "from": "continuity-system",
        "to": "any-runtime",
        "kind": "context inheritance (read-only, with non-inheritable signals filtered)",
        "destructive_surface": False,
    },
    {
        "id": "copilot↔visual",
        "from": "operational-copilot",
        "to": "visual-assistance-runtime",
        "kind": "read-only visual reference; no image generation",
        "destructive_surface": False,
    },
    {
        "id": "any↔retrieval",
        "from": "any-runtime",
        "to": "retrieval-runtime",
        "kind": "read-only retrieval request bound by declared access pattern",
        "destructive_surface": False,
    },
]

INTEROPERABILITY_RULES = [
    "Interoperability is bilateral and declared; no undeclared edges may be opened at runtime.",
    "Interoperability never creates a destructive cross-runtime path (destructive surface remains intra-runtime + supervised).",
    "Interoperability messages carry provenance (origin runtime, schema version, incident-id when available).",
    "Interoperability cannot bridge two runtimes via a third, undeclared intermediary.",
    "Interoperability with publication-runtime cannot bypass lifecycle P-tier gates.",
    "Interoperability with visual-assistance-runtime cannot trigger image generation, PDF rendering, or any rendered artefact.",
    "Interoperability respects knowledge-core directionality (read-only); cross-runtime mutation of knowledge-core is forbidden.",
]


# ---------------------------------------------------------------------------
# TASK 2 — Federated runtime contracts
# ---------------------------------------------------------------------------

FEDERATED_CONTRACTS = [
    {
        "id": "inter-runtime-base",
        "kind": "inter-runtime",
        "guarantee": "every cross-runtime message is signed with origin runtime id, schema version, and provenance manifest",
        "violation": "unsigned or unattributable cross-runtime message",
    },
    {
        "id": "context-exchange",
        "kind": "context-exchange",
        "guarantee": "context vectors exchanged read-only; receiver never mutates supplied context",
        "violation": "receiver mutates exchanged context",
    },
    {
        "id": "escalation-exchange",
        "kind": "escalation-exchange",
        "guarantee": "escalation tier is monotonic across runtime boundaries; receiver may raise but never lower",
        "violation": "receiver lowers escalation tier",
    },
    {
        "id": "reasoning-interoperability",
        "kind": "reasoning",
        "guarantee": "chain-records cross runtime boundaries verbatim; receiver may extend, never edit",
        "violation": "receiver edits chain-record",
    },
    {
        "id": "orchestration-federation",
        "kind": "orchestration",
        "guarantee": "delegated orchestration step preserves the source runtime's supervision state; supervised stays supervised",
        "violation": "delegation downgrades supervision",
    },
    {
        "id": "shared-cognition-boundary",
        "kind": "shared-cognition",
        "guarantee": "only declared cognition surfaces are shared; private cognition state stays inside its runtime",
        "violation": "private cognition state leaks across runtime boundary",
    },
    {
        "id": "continuity-exchange",
        "kind": "continuity",
        "guarantee": "continuity records cross runtime boundaries append-only; non-inheritable signals are filtered out",
        "violation": "non-inheritable signal (e.g. destructive-confirmation) crosses a runtime boundary",
    },
    {
        "id": "visual-federation",
        "kind": "visual",
        "guarantee": "visual references cross runtime boundaries read-only; visual-risk freeze contract is honored",
        "violation": "visual-assistance request triggers any rendering",
    },
    {
        "id": "publication-federation",
        "kind": "publication",
        "guarantee": "publication requests honor lifecycle P-tier gates; un-promoted content is rejected",
        "violation": "publication-runtime accepts content above its P-tier",
    },
    {
        "id": "schema-pin-federation",
        "kind": "schema",
        "guarantee": "all federated runtimes pin a compatible schema version; mismatch is a federation error",
        "violation": "federation proceeds under mismatched schema",
    },
]

FEDERATED_CONTRACT_RULES = [
    "Contracts are declared; runtimes cannot invent new contracts at runtime.",
    "Contract violations are federation errors, not warnings.",
    "Contracts preserve directionality (read-only / append-only / gated).",
    "Contracts are versioned; receivers verify schema compatibility before acceptance.",
    "Contracts cannot elevate confidence, promote P-tier, or reassign role across boundaries.",
]


# ---------------------------------------------------------------------------
# TASK 3 — Shared operational context
# ---------------------------------------------------------------------------

SHARED_CONTEXT_KINDS = [
    {"id": "shared-operational-memory", "scope": "ecosystem-session", "mutability": "append-only"},
    {"id": "shared-troubleshooting-context", "scope": "ecosystem-session + incident-id", "mutability": "append-only"},
    {"id": "cross-runtime-continuity", "scope": "incident-id", "mutability": "append-only"},
    {"id": "shared-escalation-state", "scope": "incident-id", "mutability": "monotonic (tier only rises)"},
    {"id": "context-inheritance-record", "scope": "ecosystem-session", "mutability": "append-only; non-inheritable signals filtered"},
    {"id": "federated-operational-session", "scope": "ecosystem-session", "mutability": "open/close lifecycle; no in-place edit"},
    {"id": "shared-skill-model", "scope": "ecosystem-session", "mutability": "read-only inside a session"},
    {"id": "shared-confidence-tier", "scope": "per-node", "mutability": "immutable across boundary"},
]

INHERITABLE_SIGNALS = [
    "context-vector",
    "skill-model",
    "open-warnings (acknowledged or not)",
    "incident-id",
    "session-id",
    "active-package references (read-only)",
]

NON_INHERITABLE_SIGNALS = [
    "destructive-confirmation",
    "irreversibility-acknowledgement",
    "explicit-action-receipt",
    "operator-identity (re-asserted per runtime)",
    "supervised-resume token",
]

SHARED_CONTEXT_RULES = [
    "Shared context kinds are declared; ad-hoc shared state is forbidden.",
    "Shared context is append-only or monotonic; in-place edits are unsafe.",
    "Non-inheritable signals are filtered at the runtime boundary; receiver must re-acquire.",
    "Confidence tier is immutable across boundaries; receivers may not elevate.",
    "Shared context binds via incident-id (when emitter exists) or session-id (best-effort).",
    "Shared context cannot mutate knowledge-core under any circumstances.",
]


# ---------------------------------------------------------------------------
# TASK 4 — Ecosystem-wide escalation
# ---------------------------------------------------------------------------

ECOSYSTEM_ESCALATION_FLOWS = [
    {
        "id": "intra→inter",
        "trigger": "tier-3 threshold crossed inside a runtime",
        "next": "propagate to ecosystem escalation registry; receiver runtime acquires read-only handoff",
    },
    {
        "id": "runtime→runtime",
        "trigger": "source runtime declares the receiver runtime as the next handler",
        "next": "supervised handoff with continuity snapshot + 12-field escalation package",
    },
    {
        "id": "ecosystem→OEM",
        "trigger": "tier-4/5 reached and OEM channel contract exists",
        "next": "federated OEM handoff; orchestration locks to read-only at all involved runtimes",
    },
    {
        "id": "ecosystem→human",
        "trigger": "tier-3+ with no declared receiver runtime",
        "next": "supervised human handoff; orchestration locks to read-only at source",
    },
    {
        "id": "continuity-preserving",
        "trigger": "any escalation",
        "next": "continuity snapshot must precede handoff; restoration plan attached",
    },
    {
        "id": "ecosystem-broadcast",
        "trigger": "tier-5 with cross-runtime impact",
        "next": "all federated runtimes lock to read-only until receiver acknowledges",
    },
]

ECOSYSTEM_ESCALATION_RULES = [
    "Escalation tier is monotonic across runtimes; receivers may raise but never lower.",
    "Escalation crossings carry the 12-field escalation package + continuity snapshot ref.",
    "Tier-4/5 escalations require a declared receiver (OEM channel or human); otherwise queue + lock.",
    "Escalation events are append-only across the ecosystem.",
    "An ecosystem-broadcast at tier-5 locks every involved runtime to read-only.",
    "OEM federation requires the OEM channel contract; absent, escalations queue and orchestration locks.",
]


# ---------------------------------------------------------------------------
# TASK 5 — Federated orchestration
# ---------------------------------------------------------------------------

FEDERATED_ORCH_ROLES = [
    {"id": "primary-runtime", "duty": "owns the active orchestration loop and is the source of truth for the current step"},
    {"id": "delegated-runtime", "duty": "executes a delegated step under the primary's supervision posture"},
    {"id": "observer-runtime", "duty": "consumes traces read-only; cannot mutate state"},
    {"id": "receiver-runtime", "duty": "receives handoff (escalation or delegation) and acquires read-only state until acknowledged"},
    {"id": "publication-runtime", "duty": "consumes packaging requests bound by lifecycle P-tier gates"},
    {"id": "continuity-runtime", "duty": "owns append-only continuity state and serves all runtimes read-only"},
]

FEDERATED_ORCH_PATTERNS = [
    "delegation (primary → delegated under preserved supervision)",
    "handoff (primary → receiver with read-only lock at source)",
    "broadcast (primary → all observers read-only)",
    "co-execution (two runtimes execute disjoint loops on a shared incident-id)",
    "escalation-handoff (primary → receiver under monotonic escalation contract)",
    "degraded-federation (one runtime is L3+; primary downgrades the federation to read-only-only)",
    "coexistence (multiple runtimes operate on disjoint scopes within one ecosystem-session)",
]

FEDERATED_ORCH_RULES = [
    "Roles are declared per orchestration loop; runtime cannot self-promote a role.",
    "Delegation preserves supervision posture (supervised stays supervised).",
    "Co-execution requires disjoint scopes; overlapping scopes require declared arbitration.",
    "Degraded federation forces the federation level to the most degraded participant.",
    "Coexistence cannot share private cognition state; only declared shared-context kinds cross boundaries.",
    "Federated orchestration cannot create a destructive cross-runtime path.",
    "Federated completion requires all participating runtimes to satisfy their declared completion conditions.",
]


# ---------------------------------------------------------------------------
# TASK 6 — Ecosystem observability
# ---------------------------------------------------------------------------

ECOSYSTEM_TRACES = [
    "ecosystem-session-trace (one record per session open/close)",
    "federation-message-trace (one record per cross-runtime message)",
    "delegation-trace (one record per delegated step)",
    "handoff-trace (one record per escalation/handoff)",
    "shared-context-trace (one record per shared-context append or monotonic update)",
    "schema-pin-trace (one record per schema-pin verification)",
    "broadcast-trace (one record per ecosystem-broadcast)",
]

ECOSYSTEM_TRACE_FIELDS = [
    "ecosystem-session-id",
    "incident-id (when emitter exists)",
    "origin-runtime-id",
    "destination-runtime-id (when applicable)",
    "contract-id",
    "schema-version",
    "supervision-receipt-ref (when applicable)",
    "provenance-manifest-ref",
    "tier (for escalation-related traces)",
    "timestamp (UTC)",
]

ECOSYSTEM_AUDITABILITY = [
    "Every cross-runtime message is auditable from declared inputs.",
    "Every delegated step carries a delegation-trace + supervision receipt.",
    "Every handoff carries a handoff-trace + 12-field escalation package ref + continuity snapshot ref.",
    "Every shared-context update carries an append-only shared-context-trace.",
    "Every schema-pin verification (success or failure) is logged.",
    "Audit records are append-only at the ecosystem level.",
]

SHARED_REASONING_TRACES = [
    "Chain-records cross runtime boundaries verbatim with origin-runtime-id stamp.",
    "Receiving runtime may append to the chain (declared edges only) but never edit prior steps.",
    "Hypothesis lifecycle stages are visible across the federation.",
    "Termination outcomes (concluded/inconclusive/escalated) are mandatory and immutable.",
]

CONTINUITY_OBSERVABILITY = [
    "Continuity records are visible read-only to all runtimes under the same incident-id.",
    "Restoration records reference source checkpoint and originating runtime.",
    "Non-inheritable signals are explicitly marked as filtered at boundary.",
]

ESCALATION_TRACE_FEDERATION = [
    "Escalation traces are aggregated per incident-id across all involved runtimes.",
    "Tier monotonicity is observable end-to-end.",
    "Receiver acknowledgement (when receiver provides one) is mandatory.",
]


# ---------------------------------------------------------------------------
# TASK 7 — Interoperability safety governance
# ---------------------------------------------------------------------------

INTEROP_SAFE_COGNITION = [
    "Cross-runtime cognition is bounded by declared contracts; outside the contracts is undefined.",
    "Cross-runtime cognition is read-only into knowledge-core, append-only into shared continuity.",
    "Cross-runtime cognition cannot elevate confidence or promote P-tier.",
    "Cross-runtime cognition preserves supervision posture.",
    "Cross-runtime cognition emits provenance at every boundary crossing.",
]

PROHIBITED_CROSS_RUNTIME_BEHAVIORS = [
    "Mutating knowledge-core from a non-owning runtime.",
    "Mutating shared continuity in place (only append-only allowed).",
    "Lowering escalation tier across a runtime boundary.",
    "Stripping provenance from a cross-runtime message.",
    "Bridging two runtimes via an undeclared intermediary.",
    "Auto-resuming destructive activity at a receiver runtime.",
    "Sharing private cognition state across boundaries.",
    "Triggering image generation, PDF rendering, or any rendered artefact via federation.",
    "Federating across runtimes with mismatched schemas.",
    "Promoting P-tier or elevating confidence at a federation boundary.",
    "Inheriting non-inheritable signals (e.g. destructive-confirmation).",
]

UNSAFE_FEDERATION_STATES = [
    "schema-mismatch + any non-escalation cross-runtime message",
    "tier-4/5 escalation + no declared receiver",
    "delegated-step + supervision posture downgraded",
    "co-execution + overlapping scopes without declared arbitration",
    "degraded participant at L3+ + non-degraded federation level (mismatch)",
    "cross-runtime destructive path proposed",
    "shared-context update under uncertain-confidence (must escalate)",
]

ESCALATION_REQUIRED_INTEROP = [
    "ambiguity at a federation boundary",
    "contradiction between two runtimes' chain-records on the same incident-id",
    "schema-mismatch detected mid-session",
    "delegated runtime fails its declared completion conditions",
    "receiver runtime rejects a handoff (handoff-failed)",
    "OEM channel contract absent at tier-4/5",
]

SUPERVISION_REQUIRED_FEDERATION_STATES = [
    "any handoff",
    "any delegation that touches a destructive surface inside the receiver runtime",
    "any ecosystem-broadcast at tier-3+",
    "any restoration that crosses a runtime boundary",
    "any degraded-federation transition into L3+",
]

FEDERATED_RUNTIME_SAFETY_BOUNDARIES = [
    "Knowledge-core remains the single source of truth across the federation.",
    "Lifecycle P-tier gates are enforced at the federation boundary.",
    "Visual-risk freeze contract applies at every federation boundary involving visual-assistance.",
    "Irreversibility safeguards (two-token gate) are not bypassable via federation.",
    "Provenance is mandatory at every cross-runtime crossing; unattributable messages are dropped.",
]


# ---------------------------------------------------------------------------
# TASK 8 — Ecosystem governance philosophy
# ---------------------------------------------------------------------------

ECOSYSTEM_PHILOSOPHY = [
    "An ecosystem is a federation of supervised runtimes around one governed knowledge-core.",
    "Federation is coordination by declared contracts; it is never autonomy.",
    "Interoperability earns the right to exchange; it does not assume it.",
    "Provenance is the connective tissue of the federation.",
    "Degraded federation is honest federation.",
    "The ecosystem exists to serve the knowledge-core, never to extend it.",
]

RUNTIME_FEDERATION_DOCTRINE = [
    "Every runtime is independently governed under the same constitutional layers.",
    "No runtime gains authority by joining the federation.",
    "Federation preserves supervision, observability, and reversibility properties of each runtime.",
    "Federation can only narrow authority, never widen it.",
]

INTEROP_PHILOSOPHY = [
    "Interoperability is bilateral, declared, and observable.",
    "Interoperability never invents cognition; it only coordinates declared cognition.",
    "Interoperability respects every directionality (read-only into knowledge-core; append-only into continuity).",
    "Interoperability with rendering capabilities is forbidden by hard exclusion.",
]

SHARED_OP_CONTEXT_DOCTRINE = [
    "Shared operational context is append-only or monotonic.",
    "Shared operational context filters non-inheritable signals at every boundary.",
    "Shared operational context binds via incident-id (when available) or session-id (best-effort).",
    "Shared operational context cannot replace per-runtime context acquisition.",
]

ECOSYSTEM_ESC_PHILOSOPHY = [
    "Escalation across the ecosystem is monotonic.",
    "Escalation across the ecosystem preserves continuity.",
    "Escalation across the ecosystem requires a declared receiver at tier 4-5.",
    "Escalation is the ecosystem's safe degradation pathway.",
]

FEDERATED_COGNITION_GOVERNANCE = [
    "Federated cognition is the coordination of declared cognition systems across runtimes.",
    "Federated cognition cannot create cognitive capabilities; only orchestrate declared ones.",
    "Federated cognition preserves confidence, P-tier, role, and irreversibility flags across boundaries.",
    "Federated cognition is supervised by default.",
]

ECOSYSTEM_OBS_PRINCIPLES = [
    "What cannot be observed across the federation cannot be trusted.",
    "What cannot be replayed across the federation cannot be governed.",
    "What cannot be audited across the federation cannot be approved.",
    "Provenance crossing runtime boundaries is mandatory.",
]


# ---------------------------------------------------------------------------
# TASK 9 — Future ecosystem readiness
# ---------------------------------------------------------------------------

FUTURE_ECOSYSTEM_CONSUMERS = [
    {
        "id": "federated-operational-copilots",
        "gates": ["incident-id emitter", "schema-pin federation", "supervision receipt emitter"],
    },
    {
        "id": "interoperable-onboarding-systems",
        "gates": ["checkpoint registry", "intent declaration channel", "shared-context kind: federated-operational-session"],
    },
    {
        "id": "troubleshooting-ecosystems",
        "gates": ["symptom corpus ≥ 10/product", "causal edges emitted", "hypothesis store"],
    },
    {
        "id": "multimodal-runtime-ecosystems",
        "gates": ["visual-risk freeze contract", "visual-unavailable fallback", "no-image-generation hard exclusion preserved"],
    },
    {
        "id": "future-visual-assistance-ecosystems",
        "gates": ["visual provenance contract", "no-rendering-runtime hard exclusion preserved"],
    },
    {
        "id": "adaptive-operational-runtime-federation",
        "gates": ["ADAPTIVE precedence engine declared", "skill-model emitter", "warning-corpus complete on all products"],
    },
]

FUTURE_ECOSYSTEM_DOCTRINE = [
    "All future ecosystem consumers remain subordinate to knowledge-core.",
    "All future ecosystem consumers operate under declared inter-runtime contracts only.",
    "All future ecosystem consumers are gated by declared blocking risks until resolved.",
    "All future ecosystem consumers are supervised by default.",
    "All future ecosystem consumers preserve directionality, provenance, and monotonicity.",
]


# ---------------------------------------------------------------------------
# Risks
# ---------------------------------------------------------------------------

RISKS = [
    {"id": "no-incident-id-emitter", "severity": "high", "impact": "ecosystem cannot bind shared context across runtimes"},
    {"id": "no-ecosystem-session-id", "severity": "high", "impact": "ecosystem-session traces and shared-context kinds cannot bind"},
    {"id": "no-schema-pin-enforcement", "severity": "high", "impact": "federation may proceed under mismatched schemas"},
    {"id": "no-cross-runtime-provenance-bus", "severity": "high", "impact": "cross-runtime messages may lose provenance at boundary"},
    {"id": "no-supervision-receipt-emitter", "severity": "high", "impact": "delegation and handoff supervision unauditable"},
    {"id": "no-shared-context-store", "severity": "high", "impact": "shared-context kinds cannot persist append-only"},
    {"id": "no-escalation-aggregator", "severity": "high", "impact": "tier monotonicity not observable end-to-end"},
    {"id": "oem-channel-contract-missing", "severity": "high", "impact": "tier-4/5 ecosystem→OEM federation cannot complete"},
    {"id": "no-confidence-tier-on-nodes", "severity": "high", "impact": "confidence cannot be preserved across boundary"},
    {"id": "no-checkpoint-registry", "severity": "high", "impact": "continuity-preserving escalation degrades"},
    {"id": "no-arbitration-rule-set", "severity": "medium", "impact": "co-execution cannot resolve overlapping scopes"},
    {"id": "no-receiver-acknowledgement-channel", "severity": "medium", "impact": "handoff-failed cannot be detected promptly"},
    {"id": "no-broadcast-lock-mechanism", "severity": "medium", "impact": "tier-5 ecosystem-broadcast cannot enforce read-only lock"},
    {"id": "thin-troubleshooting-corpus", "severity": "high", "impact": "troubleshooting ecosystem cannot release on most products"},
    {"id": "warning-corpus-gap", "severity": "high", "impact": "guidance federation with mandatory-warning surface gated"},
]


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    (CONST_ROOT / "README.md").write_text(
        "# ECOSYSTEM INTEROPERABILITY GOVERNANCE\n\n"
        "Sixteenth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all fifteen prior governance layers.\n\n"
        "Models how multiple operational cognition runtimes coexist, coordinate, exchange "
        "context, preserve continuity, and interoperate safely across a federated operational "
        "ecosystem. It does not implement runtime federation, agents, chatbots, frontends, "
        "image generators, PDF renderers, or autonomous ecosystems.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Ecosystem Interoperability Governance",
        "Declares the principles and authority of this layer. Subordinate to knowledge-core and to all fifteen prior governance layers.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Authority", md_list(CHARTER_AUTHORITY)),
            ("Hard Exclusions", md_list([
                "DO NOT implement runtime federation",
                "DO NOT build chatbot systems",
                "DO NOT generate images",
                "DO NOT create PDFs",
                "DO NOT implement autonomous ecosystems",
                "DO NOT build frontend systems",
            ])),
        ],
        {
            "schema": SCHEMA, "kind": "charter",
            "principles": CHARTER_PRINCIPLES, "authority": CHARTER_AUTHORITY,
            "subordinate_to": [
                "knowledge-core",
                "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
                "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
                "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
                "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
            ],
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "interoperability-models", "interoperability-models",
        "Cross-Runtime Interoperability Models",
        "Declared interoperability edges between future runtime kinds. None create destructive cross-runtime paths.",
        [
            ("Runtime kinds", md_list([f"`{r}`" for r in RUNTIME_KINDS])),
            ("Models", md_list([f"`{m['id']}` — {m['from']} → {m['to']} ({m['kind']})" for m in INTEROPERABILITY_MODELS])),
            ("Rules", md_list(INTEROPERABILITY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "interoperability-models", "runtime_kinds": RUNTIME_KINDS, "models": INTEROPERABILITY_MODELS, "rules": INTEROPERABILITY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "runtime-contracts", "runtime-contracts",
        "Federated Runtime Contracts",
        "Declared inter-runtime contracts. Violations are federation errors, not warnings.",
        [
            ("Contracts", md_list([f"`{c['id']}` — kind: {c['kind']}" for c in FEDERATED_CONTRACTS])),
            ("Rules", md_list(FEDERATED_CONTRACT_RULES)),
        ],
        {"schema": SCHEMA, "kind": "runtime-contracts", "contracts": FEDERATED_CONTRACTS, "rules": FEDERATED_CONTRACT_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "shared-context", "shared-context",
        "Shared Operational Context",
        "Declared shared-context kinds and inheritance rules across runtimes.",
        [
            ("Shared context kinds", md_list([f"`{k['id']}` — scope: {k['scope']} — mutability: {k['mutability']}" for k in SHARED_CONTEXT_KINDS])),
            ("Inheritable signals", md_list(INHERITABLE_SIGNALS)),
            ("Non-inheritable signals", md_list(NON_INHERITABLE_SIGNALS)),
            ("Rules", md_list(SHARED_CONTEXT_RULES)),
        ],
        {
            "schema": SCHEMA, "kind": "shared-context",
            "shared_context_kinds": SHARED_CONTEXT_KINDS,
            "inheritable_signals": INHERITABLE_SIGNALS,
            "non_inheritable_signals": NON_INHERITABLE_SIGNALS,
            "rules": SHARED_CONTEXT_RULES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "escalation", "escalation",
        "Ecosystem-Wide Escalation",
        "Declared ecosystem escalation flows. Tier is monotonic across runtimes; receivers may raise but never lower.",
        [
            ("Flows", md_list([f"`{f['id']}` — trigger: {f['trigger']}" for f in ECOSYSTEM_ESCALATION_FLOWS])),
            ("Rules", md_list(ECOSYSTEM_ESCALATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "escalation", "flows": ECOSYSTEM_ESCALATION_FLOWS, "rules": ECOSYSTEM_ESCALATION_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "orchestration", "orchestration",
        "Federated Orchestration",
        "Declared orchestration roles, coordination patterns, and rules across runtimes.",
        [
            ("Roles", md_list([f"`{r['id']}` — {r['duty']}" for r in FEDERATED_ORCH_ROLES])),
            ("Patterns", md_list(FEDERATED_ORCH_PATTERNS)),
            ("Rules", md_list(FEDERATED_ORCH_RULES)),
        ],
        {
            "schema": SCHEMA, "kind": "orchestration",
            "roles": FEDERATED_ORCH_ROLES,
            "patterns": FEDERATED_ORCH_PATTERNS,
            "rules": FEDERATED_ORCH_RULES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "observability", "observability",
        "Ecosystem Observability",
        "Declared trace kinds, fields, and audit + reasoning + continuity + escalation traceability rules across the federation.",
        [
            ("Trace kinds", md_list(ECOSYSTEM_TRACES)),
            ("Trace fields", md_list(ECOSYSTEM_TRACE_FIELDS)),
            ("Auditability", md_list(ECOSYSTEM_AUDITABILITY)),
            ("Shared reasoning traces", md_list(SHARED_REASONING_TRACES)),
            ("Continuity observability", md_list(CONTINUITY_OBSERVABILITY)),
            ("Escalation trace federation", md_list(ESCALATION_TRACE_FEDERATION)),
        ],
        {
            "schema": SCHEMA, "kind": "observability",
            "trace_kinds": ECOSYSTEM_TRACES,
            "trace_fields": ECOSYSTEM_TRACE_FIELDS,
            "auditability": ECOSYSTEM_AUDITABILITY,
            "shared_reasoning_traces": SHARED_REASONING_TRACES,
            "continuity_observability": CONTINUITY_OBSERVABILITY,
            "escalation_trace_federation": ESCALATION_TRACE_FEDERATION,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "safety-governance", "safety-governance",
        "Interoperability Safety Governance",
        "Hard boundaries on cross-runtime behavior. Unsafe federation states. Escalation- and supervision-required interoperability.",
        [
            ("Interoperability-safe cognition", md_list(INTEROP_SAFE_COGNITION)),
            ("Prohibited cross-runtime behaviors", md_list(PROHIBITED_CROSS_RUNTIME_BEHAVIORS)),
            ("Unsafe federation states", md_list(UNSAFE_FEDERATION_STATES)),
            ("Escalation-required interoperability", md_list(ESCALATION_REQUIRED_INTEROP)),
            ("Supervision-required federation states", md_list(SUPERVISION_REQUIRED_FEDERATION_STATES)),
            ("Federated-runtime safety boundaries", md_list(FEDERATED_RUNTIME_SAFETY_BOUNDARIES)),
        ],
        {
            "schema": SCHEMA, "kind": "safety-governance",
            "safe_cognition": INTEROP_SAFE_COGNITION,
            "prohibited": PROHIBITED_CROSS_RUNTIME_BEHAVIORS,
            "unsafe_states": UNSAFE_FEDERATION_STATES,
            "escalation_required": ESCALATION_REQUIRED_INTEROP,
            "supervision_required": SUPERVISION_REQUIRED_FEDERATION_STATES,
            "boundaries": FEDERATED_RUNTIME_SAFETY_BOUNDARIES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "ecosystem-governance", "ecosystem-governance",
        "Ecosystem Governance Doctrine",
        "Philosophy + doctrine for ecosystem, federation, interoperability, shared context, escalation, federated cognition, and observability.",
        [
            ("Ecosystem philosophy", md_list(ECOSYSTEM_PHILOSOPHY)),
            ("Runtime federation doctrine", md_list(RUNTIME_FEDERATION_DOCTRINE)),
            ("Interoperability philosophy", md_list(INTEROP_PHILOSOPHY)),
            ("Shared operational context doctrine", md_list(SHARED_OP_CONTEXT_DOCTRINE)),
            ("Ecosystem escalation philosophy", md_list(ECOSYSTEM_ESC_PHILOSOPHY)),
            ("Federated cognition governance", md_list(FEDERATED_COGNITION_GOVERNANCE)),
            ("Ecosystem observability principles", md_list(ECOSYSTEM_OBS_PRINCIPLES)),
        ],
        {
            "schema": SCHEMA, "kind": "ecosystem-governance",
            "philosophy": ECOSYSTEM_PHILOSOPHY,
            "federation_doctrine": RUNTIME_FEDERATION_DOCTRINE,
            "interop_philosophy": INTEROP_PHILOSOPHY,
            "shared_context_doctrine": SHARED_OP_CONTEXT_DOCTRINE,
            "escalation_philosophy": ECOSYSTEM_ESC_PHILOSOPHY,
            "federated_cognition_governance": FEDERATED_COGNITION_GOVERNANCE,
            "observability_principles": ECOSYSTEM_OBS_PRINCIPLES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "future-ecosystem-readiness", "future-ecosystem-readiness",
        "Future Ecosystem Readiness",
        "Declared future ecosystem consumers and the gates each must clear. All future ecosystem intelligence remains subordinate to the governed knowledge-core.",
        [
            ("Future consumers", md_list([f"`{c['id']}` — gates: {len(c['gates'])}" for c in FUTURE_ECOSYSTEM_CONSUMERS])),
            ("Doctrine", md_list(FUTURE_ECOSYSTEM_DOCTRINE)),
        ],
        {"schema": SCHEMA, "kind": "future-ecosystem-readiness", "consumers": FUTURE_ECOSYSTEM_CONSUMERS, "doctrine": FUTURE_ECOSYSTEM_DOCTRINE, "generated": now_iso()},
    )

    reports = [
        ("01-interoperability-model-summary.json", {
            "schema": SCHEMA,
            "runtime_kinds": RUNTIME_KINDS,
            "models": len(INTEROPERABILITY_MODELS),
            "destructive_models": [m["id"] for m in INTEROPERABILITY_MODELS if m["destructive_surface"]],
            "rules": len(INTEROPERABILITY_RULES),
        }),
        ("02-federated-contract-summary.json", {
            "schema": SCHEMA,
            "contracts": [c["id"] for c in FEDERATED_CONTRACTS],
            "by_kind": sorted({c["kind"] for c in FEDERATED_CONTRACTS}),
            "rules": len(FEDERATED_CONTRACT_RULES),
        }),
        ("03-shared-context-summary.json", {
            "schema": SCHEMA,
            "shared_context_kinds": [k["id"] for k in SHARED_CONTEXT_KINDS],
            "inheritable": INHERITABLE_SIGNALS,
            "non_inheritable": NON_INHERITABLE_SIGNALS,
            "rules": len(SHARED_CONTEXT_RULES),
        }),
        ("04-ecosystem-escalation-summary.json", {
            "schema": SCHEMA,
            "flows": [f["id"] for f in ECOSYSTEM_ESCALATION_FLOWS],
            "rules": len(ECOSYSTEM_ESCALATION_RULES),
        }),
        ("05-federated-orchestration-summary.json", {
            "schema": SCHEMA,
            "roles": [r["id"] for r in FEDERATED_ORCH_ROLES],
            "patterns": FEDERATED_ORCH_PATTERNS,
            "rules": len(FEDERATED_ORCH_RULES),
        }),
        ("06-ecosystem-observability-summary.json", {
            "schema": SCHEMA,
            "trace_kinds": ECOSYSTEM_TRACES,
            "trace_fields": ECOSYSTEM_TRACE_FIELDS,
            "auditability_count": len(ECOSYSTEM_AUDITABILITY),
        }),
        ("07-interoperability-safety-summary.json", {
            "schema": SCHEMA,
            "prohibited_count": len(PROHIBITED_CROSS_RUNTIME_BEHAVIORS),
            "unsafe_states_count": len(UNSAFE_FEDERATION_STATES),
            "escalation_required_count": len(ESCALATION_REQUIRED_INTEROP),
            "supervision_required_count": len(SUPERVISION_REQUIRED_FEDERATION_STATES),
            "safety_boundaries": FEDERATED_RUNTIME_SAFETY_BOUNDARIES,
        }),
        ("08-ecosystem-governance-summary.json", {
            "schema": SCHEMA,
            "philosophy_principles": len(ECOSYSTEM_PHILOSOPHY),
            "federation_doctrine": len(RUNTIME_FEDERATION_DOCTRINE),
            "interop_philosophy": len(INTEROP_PHILOSOPHY),
            "shared_context_doctrine": len(SHARED_OP_CONTEXT_DOCTRINE),
            "escalation_philosophy": len(ECOSYSTEM_ESC_PHILOSOPHY),
            "federated_cognition": len(FEDERATED_COGNITION_GOVERNANCE),
            "observability_principles": len(ECOSYSTEM_OBS_PRINCIPLES),
        }),
        ("09-unresolved-federation-risks.json", {
            "schema": SCHEMA,
            "risks": RISKS,
            "total": len(RISKS),
            "high": [r["id"] for r in RISKS if r["severity"] == "high"],
            "medium": [r["id"] for r in RISKS if r["severity"] == "medium"],
        }),
        ("10-future-ecosystem-readiness.json", {
            "schema": SCHEMA,
            "consumers": FUTURE_ECOSYSTEM_CONSUMERS,
            "doctrine": FUTURE_ECOSYSTEM_DOCTRINE,
            "subordinate_to": "knowledge-core (forever)",
        }),
    ]

    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    file_count = sum(1 for _ in CONST_ROOT.rglob("*") if _.is_file())
    high_risks = [r["id"] for r in RISKS if r["severity"] == "high"]

    print(
        "Ecosystem interoperability & federation modeling complete.\n"
        f"  Constitutional root: {CONST_ROOT}\n"
        f"  Reports: {REPORTS_ROOT}/01..10\n"
        f"  Runtime kinds: {len(RUNTIME_KINDS)} | Interop models: {len(INTEROPERABILITY_MODELS)} | "
        f"Contracts: {len(FEDERATED_CONTRACTS)} | Shared-context kinds: {len(SHARED_CONTEXT_KINDS)} | "
        f"Escalation flows: {len(ECOSYSTEM_ESCALATION_FLOWS)} | Roles: {len(FEDERATED_ORCH_ROLES)} | "
        f"Risks: {len(RISKS)} (high: {len(high_risks)}).\n"
        f"  Files written under constitutional root: {file_count}"
    )


if __name__ == "__main__":
    build()
