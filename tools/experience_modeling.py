#!/usr/bin/env python3
"""Phase 10 — Knowledge Experience & Guidance Modeling.

NON-DESTRUCTIVE.

Builds the constitutional + modeling layer for knowledge experience under
`KNOWLEDGE_BUILDING/EXPERIENCE_GOVERNANCE/`. No per-product knowledge-core
file is modified. No image generated. No PDF / chatbot runtime / frontend
built. This phase only MODELS knowledge experience.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
EG = KB / "EXPERIENCE_GOVERNANCE"
GOV_REPO = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "experience-governance/1.0"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# User journeys (canonical archetypes; per-product specialisation pending).
# ---------------------------------------------------------------------------
JOURNEYS = [
    {
        "id": "journey.first-installation",
        "label": "First installation",
        "actors": ["installer", "admin-owner"],
        "phases": [
            "unbox", "verify-contents", "identify-door-type", "mechanical-mount",
            "wire-internal", "insert-batteries", "power-on-test", "register-administrator",
        ],
        "trigger": "User receives a new lock.",
        "success_state": "Lock physically mounted, powered, with at least one administrator registered.",
        "failure_modes": ["wrong-door-type", "incorrect-handle-orientation", "missed-mounting-screw", "low-battery-on-first-power-on"],
        "guidance_intensity": "high",
        "criticality": "critical",
    },
    {
        "id": "journey.first-unlock",
        "label": "First unlock",
        "actors": ["admin-owner"],
        "phases": ["wake-keypad", "enter-default-or-set-pin", "observe-feedback", "open-door"],
        "trigger": "Lock is mounted and powered.",
        "success_state": "Door physically opens via lock.",
        "failure_modes": ["forgot-default-credentials", "fingerprint-not-yet-enrolled", "low-battery"],
        "guidance_intensity": "medium",
        "criticality": "high",
    },
    {
        "id": "journey.first-app-pairing",
        "label": "First app pairing",
        "actors": ["admin-owner"],
        "phases": ["install-app", "create-account", "scan-qr-or-ez-mode", "confirm-on-lock", "verify-online-status"],
        "trigger": "Admin wants remote / multi-user features.",
        "success_state": "Lock visible in companion app, admin authenticated.",
        "failure_modes": ["weak-wifi", "wrong-network-band", "app-version-mismatch", "qr-unreadable"],
        "guidance_intensity": "high",
        "criticality": "high",
    },
    {
        "id": "journey.administrator-setup",
        "label": "Administrator setup",
        "actors": ["admin-owner"],
        "phases": ["enter-management-menu", "register-administrator-pin", "register-administrator-fingerprint", "set-language", "set-time-zone"],
        "trigger": "First admin needs full control.",
        "success_state": "At least one administrator with PIN + fingerprint enrolled.",
        "failure_modes": ["confused-with-user-role", "fingerprint-rejection", "menu-timeout"],
        "guidance_intensity": "medium",
        "criticality": "high",
    },
    {
        "id": "journey.user-enrolment",
        "label": "User enrolment",
        "actors": ["admin-owner", "regular-user"],
        "phases": ["admin-authenticates", "open-add-user", "register-pin", "register-fingerprint", "test-unlock"],
        "trigger": "A new household / office member needs access.",
        "success_state": "User can unlock independently with at least one credential.",
        "failure_modes": ["over-permission-grant", "duplicate-fingerprint-conflict", "weak-pin-choice"],
        "guidance_intensity": "medium",
        "criticality": "medium",
    },
    {
        "id": "journey.battery-replacement",
        "label": "Battery replacement",
        "actors": ["admin-owner"],
        "phases": ["receive-low-battery-warning", "open-battery-bay", "remove-old-batteries", "insert-new-batteries", "verify-power"],
        "trigger": "Low-battery warning OR scheduled maintenance.",
        "success_state": "Lock fully powered with fresh batteries; clock and configuration preserved.",
        "failure_modes": ["wrong-battery-orientation", "mixed-battery-ages", "battery-bay-cover-not-reseated"],
        "guidance_intensity": "low",
        "criticality": "medium",
    },
    {
        "id": "journey.emergency-recovery",
        "label": "Emergency recovery",
        "actors": ["admin-owner", "occupant"],
        "phases": ["detect-no-power", "locate-emergency-port", "apply-9V-source", "wake-keypad", "unlock", "replace-batteries"],
        "trigger": "Lock unresponsive, batteries depleted, occupant locked out.",
        "success_state": "Door opens; batteries are replaced before next sleep cycle.",
        "failure_modes": ["wrong-port-orientation", "incorrect-voltage-source", "credentials-forgotten", "no-mechanical-key"],
        "guidance_intensity": "very-high",
        "criticality": "critical",
    },
    {
        "id": "journey.factory-reset-recovery",
        "label": "Factory reset recovery",
        "actors": ["admin-owner"],
        "phases": ["confirm-data-loss-acceptance", "open-reset-pinhole-or-menu", "execute-reset-sequence", "observe-confirmation", "re-register-administrator"],
        "trigger": "Lost admin credentials OR re-deployment.",
        "success_state": "Lock returned to factory state; new administrator registered.",
        "failure_modes": ["accidental-reset", "incomplete-sequence", "data-loss-not-anticipated"],
        "guidance_intensity": "very-high",
        "criticality": "critical",
    },
    {
        "id": "journey.troubleshooting-escalation",
        "label": "Troubleshooting escalation",
        "actors": ["admin-owner", "support"],
        "phases": ["observe-symptom", "self-diagnosis", "guided-recovery", "escalate-to-support", "rma-or-field-service"],
        "trigger": "Lock behaves unexpectedly.",
        "success_state": "Issue resolved at lowest possible support tier.",
        "failure_modes": ["misdiagnosis", "premature-escalation", "skipped-recovery-steps"],
        "guidance_intensity": "high",
        "criticality": "high",
    },
]

# ---------------------------------------------------------------------------
# Knowledge consumption: prerequisite chains.
# ---------------------------------------------------------------------------
PREREQS = [
    {"concept": "procedure.unlock-pin",          "requires": ["procedure.register-pin"]},
    {"concept": "procedure.unlock-fingerprint",  "requires": ["procedure.register-fingerprint"]},
    {"concept": "procedure.register-fingerprint","requires": ["procedure.add-administrator", "concept.management-menu-access"]},
    {"concept": "procedure.register-pin",        "requires": ["procedure.add-administrator", "concept.management-menu-access"]},
    {"concept": "procedure.add-user",            "requires": ["procedure.add-administrator"]},
    {"concept": "procedure.add-administrator",   "requires": ["procedure.first-power-on"]},
    {"concept": "procedure.first-power-on",      "requires": ["procedure.battery-installation"]},
    {"concept": "procedure.pair-with-app",       "requires": ["procedure.add-administrator", "concept.companion-app-installed"]},
    {"concept": "procedure.qr-pairing",          "requires": ["procedure.pair-with-app"]},
    {"concept": "procedure.ez-mode-pairing",     "requires": ["procedure.pair-with-app"]},
    {"concept": "procedure.factory-reset",       "requires": ["concept.data-loss-acknowledgement"]},
    {"concept": "procedure.firmware-update",     "requires": ["procedure.pair-with-app", "concept.stable-power-source"]},
    {"concept": "procedure.battery-replacement", "requires": ["concept.battery-bay-access"]},
    {"concept": "procedure.emergency-power",     "requires": ["concept.9v-source-available"]},
    {"concept": "procedure.member-management",   "requires": ["procedure.pair-with-app"]},
]

LEARNING_PATHS = [
    {
        "id": "path.beginner",
        "label": "Beginner — first 24 hours",
        "ordered_concepts": [
            "procedure.battery-installation",
            "procedure.first-power-on",
            "procedure.add-administrator",
            "procedure.register-pin",
            "procedure.unlock-pin",
        ],
    },
    {
        "id": "path.intermediate",
        "label": "Intermediate — first week",
        "ordered_concepts": [
            "procedure.register-fingerprint",
            "procedure.unlock-fingerprint",
            "procedure.add-user",
            "procedure.pair-with-app",
            "procedure.qr-pairing",
        ],
    },
    {
        "id": "path.advanced",
        "label": "Advanced — full ownership",
        "ordered_concepts": [
            "procedure.member-management",
            "procedure.firmware-update",
            "procedure.factory-reset",
            "procedure.emergency-power",
        ],
    },
]

# ---------------------------------------------------------------------------
# Contextual guidance triggers.
# ---------------------------------------------------------------------------
GUIDANCE_TRIGGERS = [
    {"id": "trigger.first-time-procedure",       "rule": "Surface step-by-step guidance the first time a user attempts a procedure.", "intensity": "high"},
    {"id": "trigger.high-risk-procedure",        "rule": "Surface confirmation + explicit risk note before factory-reset, firmware-update, emergency-power.", "intensity": "very-high", "interrupts_flow": True},
    {"id": "trigger.failure-prone-step",         "rule": "Inline visual reinforcement on steps with documented failure modes.", "intensity": "medium"},
    {"id": "trigger.warning-blocking",           "rule": "Hard interrupt (modal-equivalent) for safety + data-loss + lockout warnings.", "intensity": "very-high", "interrupts_flow": True},
    {"id": "trigger.warning-non-blocking",       "rule": "Inline banner for low-battery, weak-wifi, suboptimal-but-allowed states.", "intensity": "low"},
    {"id": "trigger.troubleshooting-escalation", "rule": "Offer escalation path after N failed self-diagnosis attempts.", "intensity": "high"},
    {"id": "trigger.onboarding-branch",          "rule": "Branch onboarding when role choice is detected (admin vs user, app-paired vs local-only).", "intensity": "medium"},
    {"id": "trigger.contextual-visual",          "rule": "Surface a visual when component-visibility map indicates the step references a non-obvious component.", "intensity": "medium"},
    {"id": "trigger.cross-product-divergence",   "rule": "Surface a divergence note when the procedure differs from the platform default for this product.", "intensity": "low"},
]

# ---------------------------------------------------------------------------
# Cognitive load model.
# ---------------------------------------------------------------------------
COGNITIVE_DIMENSIONS = [
    {"id": "dim.procedural-density",   "definition": "Steps per minute of expected user time."},
    {"id": "dim.memory-burden",        "definition": "Number of items the user must hold in working memory simultaneously."},
    {"id": "dim.role-switching",       "definition": "Number of role transitions (admin↔user, app↔lock) the procedure forces."},
    {"id": "dim.modality-switching",   "definition": "Transitions between physical, app and audio modalities."},
    {"id": "dim.failure-cost",         "definition": "Cost of a single mis-step (e.g. lockout, data-loss, broken hardware)."},
    {"id": "dim.recoverability",       "definition": "How easily an error is undone within the same flow."},
    {"id": "dim.terminology-ambiguity","definition": "Density of synonyms or unfamiliar terms in the procedure surface."},
]

COGNITIVE_LOAD_MAP = [
    {"procedure": "procedure.factory-reset",       "load": "very-high", "dominant": ["dim.failure-cost", "dim.recoverability"]},
    {"procedure": "procedure.emergency-power",     "load": "very-high", "dominant": ["dim.failure-cost", "dim.modality-switching"]},
    {"procedure": "procedure.firmware-update",     "load": "high",      "dominant": ["dim.failure-cost", "dim.role-switching"]},
    {"procedure": "procedure.pair-with-app",       "load": "high",      "dominant": ["dim.modality-switching", "dim.role-switching"]},
    {"procedure": "procedure.register-fingerprint","load": "medium",    "dominant": ["dim.procedural-density"]},
    {"procedure": "procedure.add-administrator",   "load": "medium",    "dominant": ["dim.role-switching"]},
    {"procedure": "procedure.add-user",            "load": "medium",    "dominant": ["dim.role-switching"]},
    {"procedure": "procedure.register-pin",        "load": "low",       "dominant": ["dim.memory-burden"]},
    {"procedure": "procedure.unlock-pin",          "load": "low",       "dominant": []},
    {"procedure": "procedure.unlock-fingerprint",  "load": "low",       "dominant": []},
    {"procedure": "procedure.battery-replacement", "load": "low",       "dominant": []},
]

# ---------------------------------------------------------------------------
# Troubleshooting escalation tiers.
# ---------------------------------------------------------------------------
TROUBLESHOOTING_TIERS = [
    {"tier": 0, "label": "Self-observation",       "scope": "User notices and classifies a symptom."},
    {"tier": 1, "label": "Guided self-recovery",   "scope": "Documented recovery procedures (battery-replacement, emergency-power, re-pairing)."},
    {"tier": 2, "label": "Soft reset / reconfig",  "scope": "Unpair + re-pair, re-enroll credentials, network change."},
    {"tier": 3, "label": "Factory reset",          "scope": "Last-resort local recovery; data-loss accepted."},
    {"tier": 4, "label": "Support contact",        "scope": "Asynchronous support channel; logs collected."},
    {"tier": 5, "label": "Field service / RMA",    "scope": "Hardware fault confirmed; physical exchange or technician dispatch."},
]

SYMPTOM_CATEGORIES = [
    {"id": "symptom.power", "tiers_in_play": [1, 2, 4, 5]},
    {"id": "symptom.connectivity", "tiers_in_play": [1, 2, 3, 4]},
    {"id": "symptom.credential-failure", "tiers_in_play": [1, 2, 3]},
    {"id": "symptom.mechanical", "tiers_in_play": [4, 5]},
    {"id": "symptom.firmware", "tiers_in_play": [2, 3, 4]},
    {"id": "symptom.lockout", "tiers_in_play": [1, 2, 3, 4, 5]},
]

# ---------------------------------------------------------------------------
# Onboarding flows.
# ---------------------------------------------------------------------------
ONBOARDING_FLOWS = [
    {
        "id": "onboarding.first-time-user",
        "label": "First-time end user",
        "branch_when": "no-admin-yet OR no-companion-app",
        "steps": ["safety-overview", "battery-installation", "first-power-on", "set-administrator-pin", "first-unlock", "save-credentials-reminder"],
        "exit_state": "User can unlock independently and knows recovery basics.",
    },
    {
        "id": "onboarding.installation",
        "label": "Installation onboarding",
        "branch_when": "physical-mount-required",
        "steps": ["identify-door-type", "tools-checklist", "mechanical-mount", "wire-routing", "verify-handle-orientation", "test-without-power", "first-power-on"],
        "exit_state": "Hardware mounted and verified; ready for credential setup.",
    },
    {
        "id": "onboarding.app",
        "label": "App onboarding",
        "branch_when": "user-opts-into-companion-app",
        "steps": ["install-app", "create-account", "pair-with-app", "verify-online-status", "explore-member-management"],
        "exit_state": "Lock visible in companion app; admin can manage remotely.",
    },
    {
        "id": "onboarding.admin",
        "label": "Administrator onboarding",
        "branch_when": "first-admin-or-admin-handover",
        "steps": ["set-administrator-pin", "set-administrator-fingerprint", "set-language", "set-time-zone", "review-member-policy", "review-recovery-procedures"],
        "exit_state": "Administrator fully provisioned and informed about recovery.",
    },
    {
        "id": "onboarding.safe-first-use",
        "label": "Safe first use",
        "branch_when": "always-after-installation",
        "steps": ["mechanical-key-test", "first-unlock-test", "lockout-behavior-explanation", "low-battery-explanation", "emergency-power-walkthrough"],
        "exit_state": "User has been exposed to the four most common recovery scenarios before they are needed.",
    },
]

# ---------------------------------------------------------------------------
# Knowledge prioritization dimensions.
# ---------------------------------------------------------------------------
PRIORITY_DIMENSIONS = [
    {"id": "prio.operational-criticality", "definition": "How essential the knowledge is to using the lock at all."},
    {"id": "prio.user-frequency",          "definition": "How often a typical user needs the knowledge."},
    {"id": "prio.support-burden",          "definition": "How much support time is spent on the underlying topic."},
    {"id": "prio.failure-impact",          "definition": "Consequence of getting the knowledge wrong (lockout, data-loss, hardware damage)."},
    {"id": "prio.onboarding-importance",   "definition": "Whether the knowledge is required for a successful first use."},
    {"id": "prio.safety-importance",       "definition": "Whether the knowledge protects users or property."},
]

PRIORITY_TIERS = [
    {"tier": "P0", "label": "Critical-path",      "rule": "Required to operate the lock or to recover from a critical failure."},
    {"tier": "P1", "label": "High-frequency",     "rule": "Daily-to-weekly user need."},
    {"tier": "P2", "label": "Onboarding-key",     "rule": "Required for safe first use even if not high-frequency afterwards."},
    {"tier": "P3", "label": "Support-driver",     "rule": "Drives a measurable fraction of support tickets."},
    {"tier": "P4", "label": "Reference",          "rule": "Read on demand; not required for daily use."},
    {"tier": "P5", "label": "Edge / advanced",    "rule": "Power-user or rare scenarios."},
]

PRIORITY_ASSIGNMENTS = [
    {"concept": "procedure.unlock-pin",            "tier": "P0"},
    {"concept": "procedure.unlock-fingerprint",    "tier": "P0"},
    {"concept": "procedure.battery-replacement",   "tier": "P0"},
    {"concept": "procedure.emergency-power",       "tier": "P0"},
    {"concept": "procedure.add-administrator",     "tier": "P2"},
    {"concept": "procedure.register-pin",          "tier": "P2"},
    {"concept": "procedure.register-fingerprint",  "tier": "P2"},
    {"concept": "procedure.pair-with-app",         "tier": "P2"},
    {"concept": "procedure.add-user",              "tier": "P3"},
    {"concept": "procedure.member-management",     "tier": "P3"},
    {"concept": "procedure.firmware-update",       "tier": "P4"},
    {"concept": "procedure.qr-pairing",            "tier": "P3"},
    {"concept": "procedure.ez-mode-pairing",       "tier": "P3"},
    {"concept": "procedure.factory-reset",         "tier": "P5"},
    {"concept": "procedure.change-language",       "tier": "P4"},
]


# ---------------------------------------------------------------------------
# Documents.
# ---------------------------------------------------------------------------
def doc_charter() -> str:
    return f"""# Experience Governance Charter

_Schema: `{SCHEMA}` · experience-governance constitution · generated {NOW}._

## Purpose

This charter defines the constitutional layer of **knowledge experience**.
It governs how the knowledge core is presented to users, how guidance is
triggered, how onboarding branches, how troubleshooting escalates and how
operational complexity is bounded.

Experience governance is distinct from:

- knowledge governance (`KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/`) — owns terminology, identifiers, conflicts, retrieval contracts.
- knowledge-center architecture (`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/`) — owns ontology, maturity tiers, retrieval strategy.
- visual governance (`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) — owns visual policy.
- runtime governance (`visual-system/_governance/`) — operational rules.

## Principles

1. **Experience descends from knowledge.** Every user-facing interaction is a
   projection of canonical knowledge; experience MAY refine presentation, MAY
   NOT redefine semantics.
2. **Progressive disclosure by default.** Show what is needed for the
   current step; hide complexity until the user is ready for it.
3. **Interruption is a budget.** Hard interrupts are reserved for safety,
   data-loss and lockout risks. Everything else is inline.
4. **Onboarding is safety-first.** The first 24 hours optimise for safe
   recovery awareness, not for feature exposure.
5. **Troubleshooting respects tiers.** Self-recovery before reconfiguration,
   reconfiguration before factory-reset, factory-reset before support
   contact, support before RMA.
6. **Cognitive load is a design budget.** Procedures with high failure
   cost and low recoverability MUST receive the strongest guidance.
7. **Subordination of all surfaces.** Chatbot, onboarding assistant,
   troubleshooting assistant, contextual UI, adaptive docs, dynamic
   rendering and multimodal assistance are subordinate to the knowledge
   core. None of them originates knowledge.

## Authorities

| Concern | Authority | Location |
|---|---|---|
| User journeys                  | Experience Governance | `experience-semantics/user-journeys/` |
| Knowledge consumption flow     | Experience Governance | `knowledge-consumption/` |
| Contextual guidance triggers   | Experience Governance | `guidance-semantics/` |
| Cognitive load model           | Experience Governance | `cognitive-modeling/` |
| Troubleshooting escalation     | Experience Governance | `troubleshooting-experience/` |
| Onboarding flows               | Experience Governance | `onboarding-semantics/` |
| Knowledge prioritization       | Experience Governance | `knowledge-priority/` |
| Procedural verbs / IDs         | Semantic Governance   | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/` |
| Maturity tiers                 | Knowledge Center      | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/` |
| Visual policy                  | Visual Governance     | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` |

## Amendment policy

A change in experience governance MUST NOT change canonical semantics. If a
change requires renaming a concept or changing a procedure's identity, the
amendment first goes through Semantic Governance.
"""


def doc_index() -> str:
    return f"""# Beslock Experience Governance

_Schema: `{SCHEMA}` · index · generated {NOW}._

This folder is the **constitutional + modeling layer for knowledge
experience**. It models how users consume the knowledge core; it does not
implement chatbots, onboarding apps, troubleshooting assistants or
documentation surfaces.

## Documents

- [`00-charter.md`](00-charter.md)
- [`experience-semantics/user-journeys/user-journeys.md`](experience-semantics/user-journeys/user-journeys.md)
- [`experience-semantics/user-journeys/user-journeys.json`](experience-semantics/user-journeys/user-journeys.json)
- [`knowledge-consumption/consumption-flow.md`](knowledge-consumption/consumption-flow.md)
- [`knowledge-consumption/prerequisites.json`](knowledge-consumption/prerequisites.json)
- [`knowledge-consumption/learning-paths.json`](knowledge-consumption/learning-paths.json)
- [`guidance-semantics/contextual-guidance.md`](guidance-semantics/contextual-guidance.md)
- [`guidance-semantics/guidance-triggers.json`](guidance-semantics/guidance-triggers.json)
- [`cognitive-modeling/cognitive-load.md`](cognitive-modeling/cognitive-load.md)
- [`cognitive-modeling/cognitive-load.json`](cognitive-modeling/cognitive-load.json)
- [`troubleshooting-experience/escalation-model.md`](troubleshooting-experience/escalation-model.md)
- [`troubleshooting-experience/escalation-model.json`](troubleshooting-experience/escalation-model.json)
- [`onboarding-semantics/onboarding-flows.md`](onboarding-semantics/onboarding-flows.md)
- [`onboarding-semantics/onboarding-flows.json`](onboarding-semantics/onboarding-flows.json)
- [`knowledge-priority/priority-model.md`](knowledge-priority/priority-model.md)
- [`knowledge-priority/priority-assignments.json`](knowledge-priority/priority-assignments.json)
- [`future-experience-readiness/future-experience.md`](future-experience-readiness/future-experience.md)

## Sibling constitutional layers

- Visual governance: [`../VISUAL_GOVERNANCE/00-CONSTITUTION.md`](../VISUAL_GOVERNANCE/00-CONSTITUTION.md)
- Knowledge center: [`../KNOWLEDGE_CENTER/00-architecture.md`](../KNOWLEDGE_CENTER/00-architecture.md)
- Semantic governance: [`../SEMANTIC_GOVERNANCE/00-charter.md`](../SEMANTIC_GOVERNANCE/00-charter.md)

## Hard guarantees

- No artifact under `ext-images/<slug>/knowledge-core/` was modified.
- No governance file under `visual-system/_governance/` was modified.
- No Comfy / orchestration / visual-generation file was modified.
- No PDF, image, chatbot runtime or frontend was generated or built.
- All experience modeling is descriptive of the knowledge core; it adds no
  new product knowledge.
"""


def doc_journeys() -> str:
    rows = "\n".join(
        f"| `{j['id']}` | {j['label']} | {j['criticality']} | {j['guidance_intensity']} | {len(j['phases'])} |"
        for j in JOURNEYS
    )
    return f"""# User journey semantics

_Schema: `{SCHEMA}` · user-journey model · generated {NOW}._

## Purpose

Model the operational journeys a real user undertakes with a Beslock product.
Per-product specialisation extends these archetypes; it does not invent
parallel journeys.

## Journey archetypes

| ID | Label | Criticality | Guidance intensity | Phases |
|---|---|---|---|---:|
{rows}

## Schema

```json
{{
  "id": "journey.<slug>",
  "label": "<human label>",
  "actors": ["installer", "admin-owner", "regular-user", "support"],
  "phases": ["..."],
  "trigger": "<plain-language event>",
  "success_state": "<observable end state>",
  "failure_modes": ["..."],
  "guidance_intensity": "low | medium | high | very-high",
  "criticality": "low | medium | high | critical"
}}
```

## Cross-journey rules

- A journey MUST reference canonical procedure IDs from the ontology.
- A journey MAY reference per-product specialisations via the shared concept
  membership map (Knowledge Center).
- A journey MUST declare its success state and at least its three most
  common failure modes.
- A journey's `guidance_intensity` determines the default contextual
  guidance trigger profile (see `guidance-semantics/`).

## Companion file

- [`user-journeys.json`](user-journeys.json) — machine-readable archetype set.
"""


def doc_consumption() -> str:
    rows = "\n".join(f"| `{e['concept']}` | {', '.join(f'`{r}`' for r in e['requires'])} |" for e in PREREQS)
    paths = "\n".join(
        f"### {p['label']} (`{p['id']}`)\n\n"
        + "\n".join(f"{i+1}. `{c}`" for i, c in enumerate(p["ordered_concepts"]))
        + "\n"
        for p in LEARNING_PATHS
    )
    return f"""# Knowledge consumption flow

_Schema: `{SCHEMA}` · consumption model · generated {NOW}._

## Prerequisite chains

| Concept | Requires |
|---|---|
{rows}

## Learning paths

{paths}

## Rules

1. A surface MUST NOT present a procedure before its prerequisites have been
   surfaced or marked as already-known.
2. A surface SHOULD detect prior completion by reading run records / user
   state and skip already-mastered prerequisites.
3. A surface MAY collapse adjacent low-load procedures into a single
   walkthrough; high-load procedures MUST stand alone.
4. Beginner → intermediate → advanced is the default ordering; surfaces MAY
   override only with editorial justification.

## Companion files

- [`prerequisites.json`](prerequisites.json)
- [`learning-paths.json`](learning-paths.json)
"""


def doc_guidance() -> str:
    rows = "\n".join(
        f"| `{t['id']}` | {t['intensity']} | {'yes' if t.get('interrupts_flow') else 'no'} | {t['rule']} |"
        for t in GUIDANCE_TRIGGERS
    )
    return f"""# Contextual guidance semantics

_Schema: `{SCHEMA}` · guidance triggers · generated {NOW}._

## Trigger registry

| Trigger | Intensity | Interrupts flow | Rule |
|---|---|---|---|
{rows}

## Interruption budget

- Hard interrupts: reserved for `trigger.high-risk-procedure` and
  `trigger.warning-blocking`.
- Inline reinforcement: default for all other triggers.
- A surface MUST NOT exceed two hard interrupts in a single onboarding
  session.

## Composition rules

1. Triggers are evaluated per step, not per page.
2. Triggers stack additively; a single step may fire multiple triggers.
3. The highest-intensity trigger wins the presentation contract.
4. Visual reinforcement (`trigger.contextual-visual`) is bound by the visual
   constitution; conditioning comes from `component-visibility`.

## Companion file

- [`guidance-triggers.json`](guidance-triggers.json)
"""


def doc_cognitive() -> str:
    dim_rows = "\n".join(f"| `{d['id']}` | {d['definition']} |" for d in COGNITIVE_DIMENSIONS)
    proc_rows = "\n".join(
        f"| `{p['procedure']}` | {p['load']} | {', '.join(f'`{x}`' for x in p['dominant']) or '—'} |"
        for p in COGNITIVE_LOAD_MAP
    )
    return f"""# Cognitive load modeling

_Schema: `{SCHEMA}` · cognitive load model · generated {NOW}._

## Dimensions

| Dimension | Definition |
|---|---|
{dim_rows}

## Per-procedure load assessment

| Procedure | Load | Dominant dimensions |
|---|---|---|
{proc_rows}

## Design rules

1. `very-high` load procedures MUST receive the highest guidance intensity
   and MUST be flanked by recovery context.
2. `high` load procedures SHOULD provide an explicit success-state
   confirmation and a documented rollback.
3. `low` load procedures SHOULD NOT trigger hard interrupts.
4. A procedure whose load is `very-high` and whose recoverability is poor
   MUST appear in onboarding even if it is rare.

## Companion file

- [`cognitive-load.json`](cognitive-load.json)
"""


def doc_troubleshooting() -> str:
    tier_rows = "\n".join(f"| {t['tier']} | {t['label']} | {t['scope']} |" for t in TROUBLESHOOTING_TIERS)
    sym_rows = "\n".join(f"| `{s['id']}` | {', '.join(str(x) for x in s['tiers_in_play'])} |" for s in SYMPTOM_CATEGORIES)
    return f"""# Troubleshooting escalation model

_Schema: `{SCHEMA}` · escalation model · generated {NOW}._

## Tiers

| Tier | Label | Scope |
|---|---|---|
{tier_rows}

## Symptom → tier coverage

| Symptom | Tiers in play |
|---|---|
{sym_rows}

## Escalation rules

1. Symptom triage starts at the lowest tier the symptom maps to.
2. A user MUST be allowed to skip up to two tiers if they explicitly opt in
   (e.g. "I have already replaced batteries").
3. Skipping into Tier 3 (factory-reset) requires acknowledgement of data
   loss.
4. Skipping into Tier 4–5 requires symptom evidence (logs / observed
   behaviour).
5. A failed Tier-N procedure SHOULD propose Tier-N+1 with rationale.

## Recovery prioritization

- Power and lockout symptoms outrank everything else; the surface MUST
  surface battery and emergency-power guidance immediately when those
  symptoms are present.
- Connectivity symptoms allow longer self-diagnosis loops before escalation.
- Mechanical symptoms escalate fast (Tier 4 within two failed Tier-1
  attempts).

## Companion file

- [`escalation-model.json`](escalation-model.json)
"""


def doc_onboarding() -> str:
    rows = "\n".join(
        f"| `{o['id']}` | {o['label']} | `{o['branch_when']}` | {len(o['steps'])} | {o['exit_state']} |"
        for o in ONBOARDING_FLOWS
    )
    return f"""# Onboarding semantics

_Schema: `{SCHEMA}` · onboarding flows · generated {NOW}._

## Flows

| ID | Label | Branch trigger | Steps | Exit state |
|---|---|---|---:|---|
{rows}

## Branch policy

- Onboarding is composed of independent flows. The user enters the union of
  flows whose branch conditions hold.
- `onboarding.safe-first-use` ALWAYS runs after `onboarding.installation`
  and before any optional flow; it is non-skippable.
- `onboarding.app` is opt-in; users without app intent skip it without
  penalty.

## Safe-first-use rule

The four scenarios surfaced in `onboarding.safe-first-use` (mechanical-key
test, first-unlock test, lockout behaviour, low-battery + emergency-power)
account for the majority of avoidable support tickets. They MUST be
exposed to the user before the user is left to operate the lock alone.

## Companion file

- [`onboarding-flows.json`](onboarding-flows.json)
"""


def doc_priority() -> str:
    dim_rows = "\n".join(f"| `{d['id']}` | {d['definition']} |" for d in PRIORITY_DIMENSIONS)
    tier_rows = "\n".join(f"| `{t['tier']}` | {t['label']} | {t['rule']} |" for t in PRIORITY_TIERS)
    assign_rows = "\n".join(f"| `{a['concept']}` | `{a['tier']}` |" for a in PRIORITY_ASSIGNMENTS)
    return f"""# Knowledge prioritization

_Schema: `{SCHEMA}` · knowledge priority model · generated {NOW}._

## Prioritization dimensions

| Dimension | Definition |
|---|---|
{dim_rows}

## Tiers

| Tier | Label | Rule |
|---|---|---|
{tier_rows}

## Assignments (canonical procedures)

| Concept | Tier |
|---|---|
{assign_rows}

## Consumer rules

- Surfaces presenting limited real-estate (chatbot card list, AR overlay,
  short SMS) MUST sort by tier ascending then by user frequency descending.
- A `P0` concept MUST always be reachable in ≤2 interactions from any
  consumer surface.
- `P5` concepts MUST be reachable, but MAY be hidden behind an "advanced"
  affordance.

## Companion file

- [`priority-assignments.json`](priority-assignments.json)
"""


def doc_future() -> str:
    return f"""# Future experience readiness

_Schema: `{SCHEMA}` · future experience surfaces · generated {NOW}._

## Subordination

Every future experience surface — chatbot guidance, onboarding assistants,
troubleshooting assistants, contextual UI guidance, adaptive documentation,
progressive manuals, dynamic knowledge rendering, multimodal assistance — is
**subordinate to the knowledge core** and bound by this charter.

## Surface contracts

| Surface | Required inputs | Constraints |
|---|---|---|
| Chatbot guidance        | priority assignments + maturity gate ≥ canonical + journey context | Must surface provenance, must respect interruption budget. |
| Onboarding assistant    | onboarding-flows.json + cognitive-load.json + safe-first-use rule | Must always run safe-first-use before optional flows. |
| Troubleshooting assistant | escalation-model.json + symptom-category map + run records | Must respect tier escalation rules; never auto-jumps two tiers. |
| Contextual UI guidance  | guidance-triggers.json + component-visibility | Must apply highest-intensity trigger; visual reinforcement bound by visual constitution. |
| Adaptive documentation  | learning-paths + prerequisites + maturity gate | Surfaces only what the user is ready for; collapses already-mastered prerequisites. |
| Progressive manuals     | priority assignments + cognitive load | Reorders sections by tier; never drops P0/P2 content. |
| Dynamic knowledge rendering | knowledge-graph + publication-intent | Per-channel formatting via Knowledge Center retrieval strategy. |
| Multimodal assistance   | terminology synonyms + procedural-semantics + visual semantics | Voice + visual + text must converge on the same canonical procedure id. |

## Out of scope

- Implementing any of the above surfaces (rendering, runtime, frontend).
- Generating images, PDFs, or final manuals.
- Building chatbot or assistant runtimes.
- Optimising rendering systems.

These remain explicitly out of scope until separate, dedicated phases.
"""


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)


def main() -> int:
    EG.mkdir(parents=True, exist_ok=True)

    write(EG / "README.md", doc_index())
    write(EG / "00-charter.md", doc_charter())
    write(EG / "experience-semantics/user-journeys/user-journeys.md", doc_journeys())
    write(EG / "experience-semantics/user-journeys/user-journeys.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW, "journeys": JOURNEYS}, ensure_ascii=False, indent=2))

    write(EG / "knowledge-consumption/consumption-flow.md", doc_consumption())
    write(EG / "knowledge-consumption/prerequisites.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW, "prerequisites": PREREQS}, ensure_ascii=False, indent=2))
    write(EG / "knowledge-consumption/learning-paths.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW, "learning_paths": LEARNING_PATHS}, ensure_ascii=False, indent=2))

    write(EG / "guidance-semantics/contextual-guidance.md", doc_guidance())
    write(EG / "guidance-semantics/guidance-triggers.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW, "triggers": GUIDANCE_TRIGGERS}, ensure_ascii=False, indent=2))

    write(EG / "cognitive-modeling/cognitive-load.md", doc_cognitive())
    write(EG / "cognitive-modeling/cognitive-load.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW,
                      "dimensions": COGNITIVE_DIMENSIONS, "per_procedure_load": COGNITIVE_LOAD_MAP},
                     ensure_ascii=False, indent=2))

    write(EG / "troubleshooting-experience/escalation-model.md", doc_troubleshooting())
    write(EG / "troubleshooting-experience/escalation-model.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW,
                      "tiers": TROUBLESHOOTING_TIERS, "symptom_categories": SYMPTOM_CATEGORIES},
                     ensure_ascii=False, indent=2))

    write(EG / "onboarding-semantics/onboarding-flows.md", doc_onboarding())
    write(EG / "onboarding-semantics/onboarding-flows.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW, "flows": ONBOARDING_FLOWS}, ensure_ascii=False, indent=2))

    write(EG / "knowledge-priority/priority-model.md", doc_priority())
    write(EG / "knowledge-priority/priority-assignments.json",
          json.dumps({"schema_version": SCHEMA, "generated_at": NOW,
                      "dimensions": PRIORITY_DIMENSIONS, "tiers": PRIORITY_TIERS,
                      "assignments": PRIORITY_ASSIGNMENTS}, ensure_ascii=False, indent=2))

    write(EG / "future-experience-readiness/future-experience.md", doc_future())

    # ----- Reports -----
    rep_dir = GOV_REPO / "reports" / "experience-governance"
    rep_dir.mkdir(parents=True, exist_ok=True)

    def report(name: str, payload: dict) -> None:
        (rep_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    report("01-user-journey-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "journey_count": len(JOURNEYS),
        "criticality_distribution": {
            t: sum(1 for j in JOURNEYS if j["criticality"] == t)
            for t in ("critical", "high", "medium", "low")
        },
        "journeys": [{"id": j["id"], "label": j["label"], "criticality": j["criticality"], "guidance_intensity": j["guidance_intensity"]} for j in JOURNEYS],
    })

    report("02-knowledge-consumption-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "prerequisite_links": len(PREREQS),
        "learning_path_count": len(LEARNING_PATHS),
        "rule_count": 4,
    })

    report("03-contextual-guidance-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "trigger_count": len(GUIDANCE_TRIGGERS),
        "interrupting_triggers": [t["id"] for t in GUIDANCE_TRIGGERS if t.get("interrupts_flow")],
        "interruption_budget": "≤2 hard interrupts per onboarding session",
    })

    report("04-cognitive-load-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "dimension_count": len(COGNITIVE_DIMENSIONS),
        "load_distribution": {
            l: sum(1 for x in COGNITIVE_LOAD_MAP if x["load"] == l)
            for l in ("very-high", "high", "medium", "low")
        },
        "very_high_procedures": [x["procedure"] for x in COGNITIVE_LOAD_MAP if x["load"] == "very-high"],
    })

    report("05-troubleshooting-escalation-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "tier_count": len(TROUBLESHOOTING_TIERS),
        "symptom_category_count": len(SYMPTOM_CATEGORIES),
        "skip_rule": "≤2 tiers skippable with explicit user opt-in; data-loss tier requires acknowledgement.",
    })

    report("06-onboarding-semantics-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "flow_count": len(ONBOARDING_FLOWS),
        "always_on_flow": "onboarding.safe-first-use",
        "opt_in_flows": ["onboarding.app"],
    })

    report("07-knowledge-priority-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "dimension_count": len(PRIORITY_DIMENSIONS),
        "tier_count": len(PRIORITY_TIERS),
        "assignment_count": len(PRIORITY_ASSIGNMENTS),
        "p0_concepts": [a["concept"] for a in PRIORITY_ASSIGNMENTS if a["tier"] == "P0"],
    })

    report("08-experience-governance-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "principle_count": 7,
        "authority_areas_count": 9,
        "charter_doc": "KNOWLEDGE_BUILDING/EXPERIENCE_GOVERNANCE/00-charter.md",
    })

    report("09-unresolved-usability-gaps.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "gaps": [
            {"id": "gap.per-product-journey-specialisation", "severity": "medium",
             "note": "Journey archetypes are platform-wide; per-product overrides not yet authored."},
            {"id": "gap.troubleshooting-symptom-corpus", "severity": "high",
             "note": "Per-product symptom catalogue is mostly empty (only e-shield has any troubleshooting/ artifact)."},
            {"id": "gap.onboarding-flow-instantiation-per-product", "severity": "medium",
             "note": "Onboarding flows are archetypes; per-product step content uses canonical procedure ids that themselves carry coverage gaps (e-nova)."},
            {"id": "gap.priority-assignment-coverage", "severity": "low",
             "note": "Priority tiers cover canonical procedures only; per-product specialisations not yet tiered."},
            {"id": "gap.cognitive-load-evidence", "severity": "medium",
             "note": "Cognitive load assignments are editorial estimates; no field evidence corpus yet."},
            {"id": "gap.guidance-trigger-instrumentation", "severity": "low",
             "note": "Triggers declared, not yet wired to any consumer surface."},
            {"id": "gap.maturity-field-backfill", "severity": "high",
             "note": "Carry-over from Phase 9 — required maturity field not yet on per-product artifacts."},
            {"id": "gap.shared-concept-membership", "severity": "medium",
             "note": "Carry-over — shared-concept membership map is empty; experience layer cannot yet resolve concept→per-product artifact."},
        ],
    })

    report("10-future-experience-system-readiness.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "ready_for": [
            "editorial review of journeys, onboarding flows and priority tiers",
            "per-product specialisation authoring",
            "downstream-consumer interface specification (chatbot, onboarding assistant, troubleshooting assistant)",
            "instrumentation contracts for guidance triggers",
        ],
        "not_ready_for": [
            "implementation of any consumer surface",
            "rendering of progressive manuals",
            "production of multimodal assistance runtimes",
            "automated A/B of onboarding flows (no instrumentation yet)",
        ],
        "subordination_rule": "All future experience surfaces remain subordinate to the knowledge core; none originates knowledge.",
    })

    print("Experience governance modeling complete.")
    print(f"  Constitutional root: {EG.relative_to(REPO).as_posix()}")
    print(f"  Reports:             {rep_dir.relative_to(REPO).as_posix()}/01..10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
