"""Phase 15 — Operational Execution & State Semantics.

Idempotent, non-destructive, modeling-only. Builds the ninth constitutional
layer `EXECUTION_GOVERNANCE` and 10 numbered reports.

Hard rules honored:
  * NEVER modifies per-product knowledge-core/* files
  * NEVER modifies prior governance layers
  * NEVER builds chatbots, PDFs, images, rendering runtimes, frontends, automation runtimes
  * Modeling-only. Defines HOW operational procedures unfold through state.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content" / "themes" / "beslock-custom" / "User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
EG = KB / "EXECUTION_GOVERNANCE"
REPORTS = USER_MANUALS / "_repository-governance" / "reports" / "execution"

SCHEMA = "execution-governance/1.0"
TODAY = date.today().isoformat()

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. State models

STATE_MODELS = [
    {"id": "lock-state",     "states": ["locked", "unlocking", "unlocked", "lockout"], "initial": "locked", "terminal": [], "safe_states": ["locked", "unlocked"], "unsafe_states": ["lockout"]},
    {"id": "pairing-state",  "states": ["unpaired", "pairing", "paired", "pairing-failed"], "initial": "unpaired", "terminal": ["paired"], "safe_states": ["unpaired", "paired"], "unsafe_states": ["pairing-failed"]},
    {"id": "enrollment-state","states": ["unenrolled", "enrolling", "enrolled", "enrollment-failed"], "initial": "unenrolled", "terminal": ["enrolled"], "safe_states": ["unenrolled", "enrolled"], "unsafe_states": ["enrollment-failed"]},
    {"id": "battery-state",  "states": ["nominal", "low-battery", "replacement-in-progress", "restored", "depleted"], "initial": "nominal", "terminal": [], "safe_states": ["nominal", "restored"], "unsafe_states": ["depleted"]},
    {"id": "operational-state","states": ["normal", "warning", "troubleshooting", "recovery", "blocked"], "initial": "normal", "terminal": [], "safe_states": ["normal"], "unsafe_states": ["blocked"]},
    {"id": "install-state",  "states": ["uninstalled", "mounting", "wired", "configured", "verified-install"], "initial": "uninstalled", "terminal": ["verified-install"], "safe_states": ["uninstalled", "verified-install"], "unsafe_states": []},
    {"id": "admin-state",    "states": ["no-admin", "admin-pending", "admin-set", "admin-locked-out"], "initial": "no-admin", "terminal": ["admin-set"], "safe_states": ["no-admin", "admin-set"], "unsafe_states": ["admin-locked-out"]},
]

STATE_TRANSITIONS = [
    # lock-state
    ("lock-state", "locked", "unlocking", "valid-credential-presented"),
    ("lock-state", "unlocking", "unlocked", "credential-accepted"),
    ("lock-state", "unlocking", "locked", "credential-rejected"),
    ("lock-state", "unlocked", "locked", "auto-relock OR manual-lock"),
    ("lock-state", "unlocking", "lockout", "max-failed-attempts"),
    ("lock-state", "lockout", "locked", "lockout-timer-elapsed OR admin-override"),
    # pairing-state
    ("pairing-state", "unpaired", "pairing", "pairing-mode-activated"),
    ("pairing-state", "pairing", "paired", "pairing-confirmed"),
    ("pairing-state", "pairing", "pairing-failed", "timeout OR network-error"),
    ("pairing-state", "pairing-failed", "unpaired", "user-acknowledged-failure"),
    # enrollment-state
    ("enrollment-state", "unenrolled", "enrolling", "enrollment-started"),
    ("enrollment-state", "enrolling", "enrolled", "credential-captured-and-confirmed"),
    ("enrollment-state", "enrolling", "enrollment-failed", "capture-rejected OR timeout"),
    ("enrollment-state", "enrollment-failed", "unenrolled", "retry-acknowledged"),
    # battery-state
    ("battery-state", "nominal", "low-battery", "voltage-below-threshold"),
    ("battery-state", "low-battery", "replacement-in-progress", "replacement-procedure-started"),
    ("battery-state", "replacement-in-progress", "restored", "battery-installed-and-verified"),
    ("battery-state", "low-battery", "depleted", "voltage-critical"),
    ("battery-state", "depleted", "replacement-in-progress", "emergency-power-applied OR replacement-started"),
    # operational-state
    ("operational-state", "normal", "warning", "warning-trigger-fired"),
    ("operational-state", "warning", "normal", "warning-acknowledged-and-cleared"),
    ("operational-state", "warning", "troubleshooting", "symptom-observed"),
    ("operational-state", "troubleshooting", "recovery", "recovery-procedure-started"),
    ("operational-state", "recovery", "normal", "recovery-completed-and-verified"),
    ("operational-state", "troubleshooting", "blocked", "tier-4-or-5-required"),
    # install-state
    ("install-state", "uninstalled", "mounting", "install-procedure-started"),
    ("install-state", "mounting", "wired", "mechanical-mount-complete"),
    ("install-state", "wired", "configured", "wiring-and-power-confirmed"),
    ("install-state", "configured", "verified-install", "install-validation-passed"),
    # admin-state
    ("admin-state", "no-admin", "admin-pending", "admin-setup-started"),
    ("admin-state", "admin-pending", "admin-set", "admin-credential-confirmed"),
    ("admin-state", "admin-set", "admin-locked-out", "admin-credential-lost OR factory-reset-required"),
    ("admin-state", "admin-locked-out", "no-admin", "factory-reset-completed"),
]

# ---------------------------------------------------------------------------
# 2. Execution flow semantics

FLOW_SEMANTICS = [
    {"id": "step-progression",       "rule": "Steps execute in declared order; out-of-order execution is a safety violation."},
    {"id": "step-dependency",        "rule": "A step is enterable only when all declared preconditions are satisfied."},
    {"id": "checkpoint",             "rule": "Procedures declare ≥1 checkpoint; checkpoints are safe restart anchors."},
    {"id": "safe-transition",        "rule": "Transitions to unsafe states require explicit user confirmation + warning surface."},
    {"id": "confirmation-required",  "rule": "Steps marked `confirmation_required=true` cannot be auto-completed by an assistant."},
    {"id": "completion-condition",   "rule": "A procedure is complete only when its terminal state is reached AND its validation predicate passes."},
    {"id": "no-implicit-completion", "rule": "Absence of error is not completion; completion is positively asserted by validation predicate."},
    {"id": "deterministic-execution","rule": "Given the same starting state + inputs, execution traces are reproducible."},
]

EXECUTION_OUTCOMES = ["completed", "interrupted", "failed", "blocked", "escalated", "abandoned"]

# ---------------------------------------------------------------------------
# 3. Interruption & recovery

INTERRUPTION_TYPES = [
    {"id": "user-pause",             "user_initiated": True,  "safe": True,  "resume_strategy": "resume-from-last-step"},
    {"id": "user-cancel",            "user_initiated": True,  "safe": True,  "resume_strategy": "rollback-to-checkpoint"},
    {"id": "session-timeout",        "user_initiated": False, "safe": True,  "resume_strategy": "resume-from-last-checkpoint"},
    {"id": "device-disconnect",      "user_initiated": False, "safe": False, "resume_strategy": "rollback-to-checkpoint OR escalate"},
    {"id": "power-loss-mid-step",    "user_initiated": False, "safe": False, "resume_strategy": "safe-restart-from-initial OR emergency-recovery"},
    {"id": "validation-failure",     "user_initiated": False, "safe": False, "resume_strategy": "retry-step OR escalate"},
    {"id": "external-error",         "user_initiated": False, "safe": False, "resume_strategy": "retry-or-escalate-with-cause"},
]

RECOVERY_RULES = [
    "Every procedure declares ≥1 checkpoint as a safe re-entry anchor.",
    "Rollback never partially applies a destructive step; either the destructive step completes fully or it never began.",
    "Restart from initial state requires explicit user re-confirmation if any destructive step had previously begun.",
    "Recovery from `pairing-failed`, `enrollment-failed`, `lockout` returns to the prior safe state, never directly to a terminal state.",
    "Power-loss during destructive procedures (factory-reset, firmware-upgrade) requires emergency-recovery; never auto-resume.",
    "Recovery traces preserve provenance: original procedure id, interruption cause, recovery path taken.",
]

# ---------------------------------------------------------------------------
# 4. Failure-state semantics

FAILURE_STATES = [
    {"id": "blocked-state",          "recoverable": True,  "requires": "tier-3 or tier-4 escalation",                   "examples": ["operational-state.blocked", "admin-state.admin-locked-out"]},
    {"id": "unsafe-state",           "recoverable": True,  "requires": "warning acknowledgement + prerequisite restore", "examples": ["lock-state.lockout"]},
    {"id": "unresolved-state",       "recoverable": False, "requires": "human/OEM intervention",                          "examples": ["pairing-failed (after N retries)", "enrollment-failed (after N retries)"]},
    {"id": "irrecoverable-state",    "recoverable": False, "requires": "vendor RMA",                                      "examples": ["depleted + battery-physically-damaged", "firmware-bricked"]},
    {"id": "escalation-required",    "recoverable": True,  "requires": "tier-3..5 troubleshooting",                       "examples": ["repeated validation-failure across procedures"]},
]

UNSAFE_SEQUENCES = [
    {"sequence": ["unlocking", "factory-reset"],            "reason": "factory-reset during unlocking corrupts credential state"},
    {"sequence": ["pairing", "factory-reset"],              "reason": "factory-reset during pairing leaves device in inconsistent network state"},
    {"sequence": ["enrolling", "battery-replacement"],      "reason": "battery removal during enrollment loses captured credential"},
    {"sequence": ["replacement-in-progress", "factory-reset"], "reason": "factory-reset during battery swap can brick configuration"},
    {"sequence": ["mounting", "configured"],                "reason": "skipping wired/power confirmation step before configuration"},
]

FAILURE_RULES = [
    "Failure states classify recoverable vs unrecoverable; classification is non-negotiable.",
    "Unsafe sequences are blocked at composition time; assemblies cannot include them as adjacent steps.",
    "Escalation-required failures transition operational-state to `troubleshooting` and cannot return to `normal` without verified recovery.",
    "Irrecoverable failures emit a vendor-RMA escalation and never present a 'retry' affordance.",
]

# ---------------------------------------------------------------------------
# 5. User intent progression

INTENTS = [
    "install", "configure", "unlock", "pair-app", "enrol-user",
    "recover", "troubleshoot", "maintain", "administer", "factory-reset",
]

INTENT_TRANSITIONS = [
    ("install", "configure", "post-install configuration kicks in"),
    ("configure", "pair-app", "post-config app pairing"),
    ("pair-app", "enrol-user", "post-pairing user enrolment"),
    ("enrol-user", "unlock", "credential available -> first unlock"),
    ("unlock", "maintain", "routine operation -> maintenance window"),
    ("maintain", "troubleshoot", "anomaly observed during maintenance"),
    ("troubleshoot", "recover", "recovery path identified"),
    ("recover", "unlock", "post-recovery resume operation"),
    ("recover", "factory-reset", "recovery requires reset"),
    ("factory-reset", "install", "post-reset re-installation/re-configuration"),
    ("administer", "enrol-user", "admin enrols new credential"),
    ("administer", "factory-reset", "admin initiates reset"),
]

INTENT_RULES = [
    "User intent is declarative; the execution layer never infers intent silently from behaviour.",
    "Intent transitions are tracked; abrupt intent changes (e.g. troubleshoot -> install) require checkpoint recovery.",
    "Intent and operational-state must remain consistent; mismatched pairs are a composition error.",
    "Intent `factory-reset` automatically attaches hard-interrupting guidance triggers and irreversibility warnings.",
]

# ---------------------------------------------------------------------------
# 6. Confirmation & validation semantics

CONFIRMATION_TYPES = [
    {"id": "user-acknowledgement",   "required_for": "warning surfacing"},
    {"id": "explicit-action",        "required_for": "destructive steps (factory-reset, delete-credential)"},
    {"id": "device-feedback",        "required_for": "step that depends on physical device response"},
    {"id": "validation-predicate",   "required_for": "procedure completion"},
    {"id": "oem-confirmation",       "required_for": "P0 safety-critical promotions only"},
]

VALIDATION_PREDICATES = [
    {"procedure_class": "pairing",        "predicate": "device reports `paired` and round-trip ping succeeds"},
    {"procedure_class": "enrollment",     "predicate": "device reports `enrolled` and credential-id is recorded"},
    {"procedure_class": "factory-reset",  "predicate": "device reports `factory-default` and admin-state=no-admin"},
    {"procedure_class": "battery-replacement", "predicate": "battery-state=restored and device boots nominally"},
    {"procedure_class": "installation",   "predicate": "install-state=verified-install and operational-state=normal"},
]

CONFIRMATION_RULES = [
    "Procedure completion requires both: terminal state reached AND validation-predicate satisfied.",
    "Destructive steps require explicit-action confirmation; user-acknowledgement is insufficient.",
    "Device-feedback failures within timeout default to `validation-failure` interruption.",
    "OEM-confirmation is mandatory for promoting any procedure to verified-truth at P0.",
    "Confirmation traces are recorded and feed knowledge-health monitoring.",
]

# ---------------------------------------------------------------------------
# 7. Safe execution governance

SAFEGUARDS = [
    {"id": "irreversibility-warning",   "applies_to": ["factory-reset", "delete-all-users", "firmware-rollback"]},
    {"id": "double-confirmation",       "applies_to": ["factory-reset", "delete-all-users"]},
    {"id": "battery-precondition",      "applies_to": ["firmware-upgrade", "factory-reset"], "reason": "low-battery may brick mid-operation"},
    {"id": "network-precondition",      "applies_to": ["app-pairing", "remote-unlock"], "reason": "2.4G band requirement"},
    {"id": "physical-presence",         "applies_to": ["factory-reset", "battery-replacement"], "reason": "remote initiation forbidden"},
    {"id": "mandatory-warning-surface", "applies_to": ["all destructive procedures"], "reason": "warning must reach user before step starts"},
]

ESCALATION_THRESHOLDS = [
    {"trigger": "3 consecutive validation-failures",        "escalate_to": "tier-2"},
    {"trigger": "pairing-failed after 3 retries",           "escalate_to": "tier-3"},
    {"trigger": "lockout (max-failed-attempts) ≥ 2 cycles","escalate_to": "tier-3"},
    {"trigger": "depleted + replacement fails",             "escalate_to": "tier-4 (vendor)"},
    {"trigger": "firmware-bricked",                          "escalate_to": "tier-5 (RMA)"},
]

IRREVERSIBLE_OPERATIONS = ["factory-reset", "delete-all-users", "firmware-rollback"]

# ---------------------------------------------------------------------------
# 8. Charter

CHARTER_PRINCIPLES = [
    "Execution is observed and modelled; the layer does not perform operations.",
    "State transitions are explicit, validated, and provenance-attached.",
    "Completion is positively asserted; absence of error is not completion.",
    "Interruption is a first-class concept; recovery paths are declared, not improvised.",
    "Failure classification is non-negotiable: recoverable vs unrecoverable.",
    "Destructive operations require explicit-action confirmation and irreversibility warnings.",
    "Unsafe sequences are blocked at composition time; the execution layer enforces the prohibition.",
    "Execution governance is subordinate to knowledge-core, lifecycle, validation, access, composition.",
    "Future execution consumers inherit execution contracts; contracts never bend to satisfy a consumer.",
]

AUTHORITY_AREAS = [
    "state-models", "flow-semantics", "interruption-recovery", "failure-states",
    "intent-progression", "confirmation-semantics", "safe-execution",
    "execution-governance", "execution-risks", "future-execution-readiness",
]

# ---------------------------------------------------------------------------
# 9. Unresolved execution risks

EXECUTION_RISKS = [
    {"id": "thin-troubleshooting-corpus",       "severity": "high",   "description": "5/6 products have no troubleshooting symptoms; recovery-path resolution is blocked.", "ref": "validation/02-workflow-executability.json"},
    {"id": "warning-corpus-gap",                "severity": "high",   "description": "2 products lack warnings; mandatory-warning-surface safeguard cannot fire.",          "ref": "validation/05-experience-validation.json"},
    {"id": "no-checkpoints-declared",           "severity": "high",   "description": "Per-procedure checkpoint declarations are not yet authored in the knowledge-core; recovery anchors are heuristic."},
    {"id": "no-validation-predicates-declared", "severity": "high",   "description": "Procedures do not yet declare validation-predicates; completion currently inferred from terminal state alone."},
    {"id": "no-confirmation-flags-on-steps",    "severity": "medium", "description": "Steps do not yet carry `confirmation_required` flags; assistants would need conservative defaults."},
    {"id": "intent-mismatch-detection",         "severity": "medium", "description": "Intent vs operational-state coherence checking is contractual; no live detector yet."},
    {"id": "snapshot-hash-not-emitted",         "severity": "medium", "description": "Execution traces require knowledge-core snapshot hash for determinism; awaiting lifecycle integration."},
    {"id": "shared-concepts-undeclared",        "severity": "medium", "description": "Cross-product entity/terminology collisions block uniform state-model application across products."},
]

# ---------------------------------------------------------------------------
# 10. Future execution-system readiness

FUTURE_CONSUMERS = [
    {"system": "guided-onboarding",       "consumes": ["state-models", "intent-progression", "confirmation-semantics"], "readiness_gate": "checkpoints + validation-predicates authored per procedure"},
    {"system": "troubleshooting-assistant","consumes": ["failure-states", "recovery-rules", "escalation-thresholds"],   "readiness_gate": "symptom corpus ≥ 10 per product"},
    {"system": "adaptive-operational-guidance","consumes": ["state-models", "flow-semantics", "intent-progression"],   "readiness_gate": "intent-mismatch detector live"},
    {"system": "contextual-recovery-system","consumes": ["interruption-recovery", "failure-states"],                     "readiness_gate": "checkpoint registry per procedure"},
    {"system": "multimodal-operational-assistance","consumes": ["state-models", "visual-intent (composition layer)"],    "readiness_gate": "visual-intent attached to physical-installation procedures"},
    {"system": "future-visual-assistance","consumes": ["state-models", "visual-risk", "component-visibility"],           "readiness_gate": "visual-risk reclassification freeze in place"},
    {"system": "state-aware-chatbot",     "consumes": ["state-models", "intent-progression", "safeguards"],              "readiness_gate": "snapshot-hash on traces + access-trace logging"},
]

# ---------------------------------------------------------------------------
# Writers

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    payload = {"schema": SCHEMA, "generated": TODAY, **payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _table(rows: list[dict], cols: list[str]) -> str:
    out = "| " + " | ".join(cols) + " |\n"
    out += "|" + "|".join("---" for _ in cols) + "|\n"
    for r in rows:
        out += "| " + " | ".join(_cell(r.get(c, "")) for c in cols) + " |\n"
    return out


def _cell(v) -> str:
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}={v2}" for k, v2 in v.items())
    return str(v) if v is not None else ""


def doc_readme() -> str:
    return f"""# EXECUTION_GOVERNANCE

Constitutional layer governing **operational execution intelligence** and
**state semantics** for the Beslock knowledge center.

- Schema: `{SCHEMA}`
- Generated: {TODAY}
- Subordinate to: `knowledge-core`, `LIFECYCLE_GOVERNANCE`, `VALIDATION_GOVERNANCE`,
  `ACCESS_AND_CONSUMPTION_GOVERNANCE`, `COMPOSITION_GOVERNANCE`

This layer **does not perform** operations. It models how procedures unfold
through state transitions, interruption, recovery, and completion.

## Authority areas
{chr(10).join(f"- {a}" for a in AUTHORITY_AREAS)}

Reports: `_repository-governance/reports/execution/01..10`.
"""


def doc_charter() -> str:
    body = "# 00 — Execution Governance Charter\n\n## Principles\n"
    for i, p in enumerate(CHARTER_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## Authority areas\n" + "\n".join(f"- {a}" for a in AUTHORITY_AREAS)
    body += "\n\n## Hard guarantees\n"
    body += "- Modeling-only. Builds no chatbots, PDFs, images, renderers, frontends, automation runtimes.\n"
    body += "- Read-only. Mutates no per-product knowledge.\n"
    body += "- Subordinate. Cannot override knowledge-core, lifecycle, validation, access, composition governance.\n"
    body += "- Deterministic. Same starting state + inputs => reproducible execution traces.\n"
    return body


# ---------------------------------------------------------------------------
# Main

def main() -> None:
    EG.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    _write(EG / "README.md", doc_readme())
    _write(EG / "00-charter.md", doc_charter())
    _write_json(EG / "00-charter.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS})

    transitions_table = "| model | from | to | guard |\n|---|---|---|---|\n" + "".join(
        f"| {m} | {a} | {b} | {g} |\n" for (m, a, b, g) in STATE_TRANSITIONS
    )

    intent_transitions_table = "| from | to | rationale |\n|---|---|---|\n" + "".join(
        f"| {a} | {b} | {r} |\n" for (a, b, r) in INTENT_TRANSITIONS
    )

    sections = [
        ("state-models",
         "# State Models\n\n" + _table(STATE_MODELS, ["id", "states", "initial", "terminal", "safe_states", "unsafe_states"])
         + "\n## Allowed transitions\n\n" + transitions_table,
         {"models": STATE_MODELS, "transitions": [{"model": m, "from": a, "to": b, "guard": g} for (m, a, b, g) in STATE_TRANSITIONS]}),
        ("flow-semantics",
         "# Execution Flow Semantics\n\n" + _table(FLOW_SEMANTICS, ["id", "rule"])
         + "\n## Outcomes\n\n" + "\n".join(f"- {o}" for o in EXECUTION_OUTCOMES) + "\n",
         {"rules": FLOW_SEMANTICS, "outcomes": EXECUTION_OUTCOMES}),
        ("interruption-recovery",
         "# Interruption & Recovery\n\n" + _table(INTERRUPTION_TYPES, ["id", "user_initiated", "safe", "resume_strategy"])
         + "\n## Recovery rules\n\n" + "\n".join(f"- {r}" for r in RECOVERY_RULES) + "\n",
         {"interruption_types": INTERRUPTION_TYPES, "recovery_rules": RECOVERY_RULES}),
        ("failure-states",
         "# Failure States\n\n" + _table(FAILURE_STATES, ["id", "recoverable", "requires", "examples"])
         + "\n## Unsafe sequences\n\n" + _table(UNSAFE_SEQUENCES, ["sequence", "reason"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in FAILURE_RULES) + "\n",
         {"failure_states": FAILURE_STATES, "unsafe_sequences": UNSAFE_SEQUENCES, "rules": FAILURE_RULES}),
        ("intent-progression",
         "# User Intent Progression\n\n## Intents\n\n" + "\n".join(f"- {i}" for i in INTENTS)
         + "\n\n## Transitions\n\n" + intent_transitions_table
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in INTENT_RULES) + "\n",
         {"intents": INTENTS, "transitions": [{"from": a, "to": b, "rationale": r} for (a, b, r) in INTENT_TRANSITIONS], "rules": INTENT_RULES}),
        ("confirmation-semantics",
         "# Confirmation & Validation Semantics\n\n## Confirmation types\n\n"
         + _table(CONFIRMATION_TYPES, ["id", "required_for"])
         + "\n## Validation predicates\n\n"
         + _table(VALIDATION_PREDICATES, ["procedure_class", "predicate"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in CONFIRMATION_RULES) + "\n",
         {"confirmation_types": CONFIRMATION_TYPES, "validation_predicates": VALIDATION_PREDICATES, "rules": CONFIRMATION_RULES}),
        ("safe-execution",
         "# Safe Execution Governance\n\n## Safeguards\n\n" + _table(SAFEGUARDS, ["id", "applies_to", "reason"])
         + "\n## Escalation thresholds\n\n" + _table(ESCALATION_THRESHOLDS, ["trigger", "escalate_to"])
         + "\n## Irreversible operations\n\n" + "\n".join(f"- {o}" for o in IRREVERSIBLE_OPERATIONS) + "\n",
         {"safeguards": SAFEGUARDS, "escalation_thresholds": ESCALATION_THRESHOLDS, "irreversible_operations": IRREVERSIBLE_OPERATIONS}),
        ("execution-governance",
         doc_charter(),
         {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("execution-risks",
         "# Unresolved Execution Risks\n\n" + _table(EXECUTION_RISKS, ["id", "severity", "description", "ref"]),
         {"risks": EXECUTION_RISKS}),
        ("future-execution-readiness",
         "# Future Execution-System Readiness\n\n" + _table(FUTURE_CONSUMERS, ["system", "consumes", "readiness_gate"]),
         {"consumers": FUTURE_CONSUMERS, "products_in_scope": PRODUCTS}),
    ]

    for slug, md_text, payload in sections:
        folder = EG / slug
        folder.mkdir(parents=True, exist_ok=True)
        _write(folder / f"{slug}.md", md_text)
        _write_json(folder / f"{slug}.json", payload)

    reports = [
        ("01-state-model-summary.json",          {"models": STATE_MODELS, "transition_count": len(STATE_TRANSITIONS)}),
        ("02-execution-flow-summary.json",       {"rules": FLOW_SEMANTICS, "outcomes": EXECUTION_OUTCOMES}),
        ("03-interruption-recovery-summary.json",{"interruption_types": INTERRUPTION_TYPES, "recovery_rules": RECOVERY_RULES}),
        ("04-failure-state-summary.json",        {"failure_states": FAILURE_STATES, "unsafe_sequences": UNSAFE_SEQUENCES, "rules": FAILURE_RULES}),
        ("05-intent-progression-summary.json",   {"intents": INTENTS, "transitions": [{"from": a, "to": b, "rationale": r} for (a, b, r) in INTENT_TRANSITIONS], "rules": INTENT_RULES}),
        ("06-confirmation-semantics-summary.json",{"confirmation_types": CONFIRMATION_TYPES, "validation_predicates": VALIDATION_PREDICATES, "rules": CONFIRMATION_RULES}),
        ("07-safe-execution-summary.json",       {"safeguards": SAFEGUARDS, "escalation_thresholds": ESCALATION_THRESHOLDS, "irreversible_operations": IRREVERSIBLE_OPERATIONS}),
        ("08-execution-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-execution-risks.json",   {"risks": EXECUTION_RISKS}),
        ("10-future-execution-readiness.json",   {"consumers": FUTURE_CONSUMERS, "products_in_scope": PRODUCTS}),
    ]
    for name, payload in reports:
        _write_json(REPORTS / name, payload)

    print("Execution modeling complete.")
    print(f"  Constitutional root: {EG.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  State models: {len(STATE_MODELS)} | transitions: {len(STATE_TRANSITIONS)}")


if __name__ == "__main__":
    main()
