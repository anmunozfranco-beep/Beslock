"""
Phase 37 — OPERATIONAL READABILITY & PUBLICATION QUALITY GOVERNANCE.

Constitutional layer 30. Modeling-only. Subordinate to knowledge-core and
to all twenty-nine prior governance layers + the executable publication
renderer (layer 36 — execution, not doctrine).

Writes:
  - the seven publication-quality artifact folders under
    `wp-content/themes/beslock-custom/User manuals/publication-quality/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PUBLICATION_QUALITY_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/publication-quality/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
Adds NO macro-governance mega-layer. Defines readability/sequencing/cognitive-load/
flow-coherence/audience-readability/drift-control/future-visual-readiness models
that the renderer + reviewer ecosystem can later instrument against. Touches no
runtime code. Generates NO prompts and NO images. ComfyUI is NOT invoked.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
PQ_ROOT = THEME_ROOT / "publication-quality"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "PUBLICATION_QUALITY_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "publication-quality"

SCHEMA = "publication-quality-governance/1.0"
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")

SUBORDINATE_TO = [
    "knowledge-core/1.0",
    "publication-rendering/1.0",
    "publication-and-delivery-governance/1.0",
    "operational-pilot-governance/1.0",
    "ecosystem-normalization-governance/1.0",
    "reference-stack-governance/1.0",
    "environment-integration-governance/1.0",
    "human-operations-governance/1.0",
    "knowledge-operations-governance/1.0",
    "knowledge-lifecycle-governance/1.0",
    "runtime-hardening-governance/1.0",
    "runtime-implementation-governance/1.0",
    "runtime-orchestration-governance/1.0",
    "runtime-governance/1.0",
    "operational-proof-governance/1.0",
    "prototype-runtime-governance/1.0",
    "realization-and-deployment-governance/1.0",
    "execution-governance/1.0",
    "decision-intelligence-governance/1.0",
    "reasoning-governance/1.0",
    "lifecycle-governance/1.0",
    "composition-governance/1.0",
    "continuity-governance/1.0",
    "ecosystem-interoperability-governance/1.0",
    "adaptive-operational-governance/1.0",
    "repo-governance/1.0",
    "visual-governance/1.0",
    "visual-constitution/1.0",
]

# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def write_json(p: Path, payload: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def write_md(p: Path, title: str, body: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f"# {title}\n\nGenerated: `{NOW}`\n\nSchema: `{SCHEMA}`\n\n{body}\n",
        encoding="utf-8",
    )


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def base_envelope(layer: str, summary: str) -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "layer": layer,
        "summary": summary,
        "generated_at": NOW,
        "modeling_only": True,
        "non_destructive": True,
        "idempotent": True,
        "touches_runtime": False,
        "generates_prompts": False,
        "generates_images": False,
        "invokes_comfyui": False,
        "subordinate_to": SUBORDINATE_TO,
        "audience_filter_applied": False,
        "out_of_scope": [
            "visual generation",
            "prompt generation",
            "frontend styling",
            "production deployment",
            "autonomous writing",
            "new cognition architecture",
        ],
    }


# ---------------------------------------------------------------------------
# TASK 1 — Publication readability model
# ---------------------------------------------------------------------------

def task_readability() -> None:
    base = PQ_ROOT / "readability"

    write_json(base / "readability-model.json", {
        **base_envelope("readability", "Per-section readability standards for governed manuals."),
        "dimensions": {
            "sentence_density": {
                "definition": "average words per sentence within a procedural step",
                "target_band_words": [6, 18],
                "hard_cap_words": 24,
                "rationale": "longer sentences inflate cognitive load and hide branching conditions",
            },
            "instruction_granularity": {
                "definition": "atomicity of each instruction step",
                "rule": "one verb, one observable outcome, one decision boundary per step",
                "anti_pattern": "compound steps joined by 'and then' or commas hiding multiple actions",
            },
            "procedural_clarity": {
                "definition": "operator can predict the next state before performing the step",
                "required_elements_per_step": ["action_verb", "target_object", "expected_observation"],
            },
            "operator_comprehension": {
                "definition": "operator with stated audience profile can execute without external clarification",
                "evidence_artifact": "audience-readability profile applied at render time",
            },
            "navigation_simplicity": {
                "definition": "operator can locate any procedure in <= 2 hops from product index",
                "structural_rule": "index -> section page -> entity",
            },
        },
        "per_section_standards": {
            "onboarding": {
                "max_steps_per_procedure": 12,
                "preconditions_required": True,
                "outcomes_required": True,
                "warning_density_max_per_step": 1,
                "tone": "instructional, second-person, present tense",
            },
            "installation": {
                "max_steps_per_procedure": 15,
                "preconditions_required": True,
                "tooling_disclosure_required": True,
                "irreversibility_warning_required": True,
                "tone": "imperative, second-person, present tense, no idioms",
            },
            "troubleshooting": {
                "structure": "symptom -> diagnostic_questions -> next_actions -> escalation",
                "max_diagnostic_questions": 5,
                "next_action_must_be_actionable": True,
                "tone": "diagnostic, neutral, no blame",
            },
            "warnings": {
                "must_state": ["consequence", "trigger_condition", "operator_action"],
                "tone": "direct, factual, no euphemism",
                "irreversibility_must_be_explicit": True,
            },
            "operational_guidance": {
                "max_steps_per_procedure": 10,
                "tone": "instructional, second-person, present tense",
            },
            "quick_start": {
                "max_total_steps": 7,
                "must_link_to_full_procedure": True,
                "must_disclose_skipped_safety_content": True,
                "tone": "concise, second-person, present tense",
            },
        },
        "scoring_signals": [
            "step_count_vs_section_max",
            "avg_words_per_step_vs_band",
            "missing_preconditions_when_required",
            "missing_outcomes_when_required",
            "warning_density_per_step",
            "compound_verb_count_per_step",
            "ambiguous_pronoun_count_per_step",
        ],
        "scoring_policy": "advisory at render time; not a publishing gate (gate lives in publication-and-delivery-governance)",
    })

    write_md(base / "README.md", "Publication readability model",
        "Defines section-level readability standards (sentence density, granularity, "
        "clarity, comprehension, navigation simplicity). Renderer consumes these as "
        "advisory signals; the publishing gate remains in publication-and-delivery-governance.\n\n"
        "**Out of scope:** visual generation, prompt generation, autonomous writing.\n"
    )


# ---------------------------------------------------------------------------
# TASK 2 — Procedural sequencing governance
# ---------------------------------------------------------------------------

def task_procedural_sequencing() -> None:
    base = PQ_ROOT / "procedural-sequencing"
    write_json(base / "sequencing-model.json", {
        **base_envelope("procedural-sequencing",
                        "Governed sequencing rules for procedure assembly inside a rendered page."),
        "ordering_rules": [
            {
                "id": "preconditions-before-steps",
                "rule": "all preconditions must be presented before the first numbered step",
            },
            {
                "id": "warnings-before-irreversible-steps",
                "rule": "any warning whose target step is irreversible MUST appear immediately before that step, not at end of document",
            },
            {
                "id": "warnings-with-dependent-procedures",
                "rule": "warnings with `must_be_attached_to_kinds` MUST be inlined into every matching kind's procedure block",
            },
            {
                "id": "escalation-at-failure-edge",
                "rule": "escalation guidance MUST appear at the failure-edge of a step (after expected observation), never aggregated at end",
            },
            {
                "id": "troubleshooting-progression",
                "rule": "symptoms -> diagnostic_questions -> next_actions -> escalation; reverse ordering is forbidden",
            },
            {
                "id": "procedural-dependencies",
                "rule": "if procedure A is a precondition of procedure B, A MUST be linked from B's preconditions block (not silently assumed)",
            },
            {
                "id": "recovery-after-irreversible",
                "rule": "every irreversible step MUST have an associated recovery_path or explicit `no_recovery_possible: true` flag",
            },
            {
                "id": "no-orphan-warnings",
                "rule": "warnings without a target procedure MUST NOT appear in the main flow; they belong in the warnings index page",
            },
            {
                "id": "no-late-prerequisites",
                "rule": "a prerequisite revealed mid-procedure is a sequencing defect; it must be promoted to preconditions",
            },
        ],
        "warning_placement_policy": {
            "P0-irreversible-or-safety-blocking": "inline immediately before triggering step; visually distinct",
            "P1-high-severity": "inline immediately before triggering step",
            "P2-operational": "inline before triggering step; may collapse if repeated within same procedure",
            "P3-informational": "appendix or inline footnote",
        },
        "escalation_insertion_policy": {
            "trigger_signals": ["escalation_required: true", "candidate-pending-review", "no recovery available"],
            "format_rule": "single-line escalation cue with channel reference; no embedded narrative",
        },
        "recovery_instruction_policy": {
            "rule": "recovery instructions appear with the failure they recover from, not in a separate recovery section",
            "exception": "system-wide reset paths may have a dedicated section AND inline reference",
        },
    })
    write_md(base / "README.md", "Procedural sequencing governance",
        "Defines ordering rules for preconditions, warnings, escalation, and recovery "
        "within rendered procedural blocks. Renderer applies these as structural rules; "
        "violations surface as readability defects (not silent reorderings).\n")


# ---------------------------------------------------------------------------
# TASK 3 — Cognitive load reduction
# ---------------------------------------------------------------------------

def task_cognitive_load() -> None:
    base = PQ_ROOT / "cognitive-load"
    write_json(base / "cognitive-load-model.json", {
        **base_envelope("cognitive-load",
                        "Models progressive disclosure, chunk sizing, repetition elimination, ambiguity minimisation."),
        "progressive_disclosure": {
            "rule": "show only what is needed at the current decision boundary; defer details to expandable sub-sections or linked pages",
            "rendering_signals": ["short_summary", "expand_link", "deferred_block"],
            "anti_pattern": "front-loading every safety, edge case and exception before the first step",
        },
        "chunk_sizing": {
            "step_chunk_max_steps": 7,
            "rationale": "Miller-bound chunking keeps a single sequence within working memory",
            "overflow_policy": "split into named sub-procedures; do not silently grow the list",
        },
        "repetition_elimination": {
            "rule": "an identical instruction MUST appear once per procedure; repeated occurrences indicate a missing shared block",
            "exception": "safety-critical instructions may repeat at each irreversibility boundary",
        },
        "ambiguity_minimisation": {
            "forbidden_constructs": [
                "ambiguous pronouns ('it', 'this') without clear antecedent in same sentence",
                "vague quantifiers ('a few', 'some', 'usually') in steps",
                "conditional steps without explicit branch ('if needed')",
                "passive voice in instructions ('the lock should be paired')",
            ],
            "required_constructs": [
                "explicit subject + verb + object",
                "explicit branch outcomes ('if X, do A; otherwise do B')",
                "explicit observable confirmation",
            ],
        },
        "operational_clarity": {
            "rule": "every step must answer: what to do, on what, expected result, what counts as failure",
        },
        "step_isolation": {
            "rule": "a step's success or failure must be observable BEFORE the next step begins",
            "anti_pattern": "compound steps that only become observable after the entire block",
        },
        "interruption_reduction": {
            "rule": "do not interleave unrelated content (marketing, version notes, glossary) inside a procedural block",
            "exception": "warnings tied to the next step (per sequencing model) are not interruptions",
        },
        "cognitive_signals_for_renderer": [
            "chunk_overflow_step_count",
            "repeated_instruction_count",
            "ambiguous_pronoun_count",
            "passive_voice_count",
            "interleaved_unrelated_block_count",
            "missing_branch_resolution_count",
        ],
    })
    write_md(base / "README.md", "Human cognitive load reduction",
        "Models progressive disclosure, chunk sizing, repetition elimination, and "
        "ambiguity minimisation for rendered manuals. Cognitive signals are surfaced "
        "as readability defects, not silently fixed by the renderer.\n")


# ---------------------------------------------------------------------------
# TASK 4 — Operational flow coherence
# ---------------------------------------------------------------------------

def task_flow_coherence() -> None:
    base = PQ_ROOT / "flow-coherence"
    write_json(base / "flow-coherence-model.json", {
        **base_envelope("flow-coherence",
                        "Defines coherent end-to-end flows across rendered manual pages."),
        "flows": {
            "onboarding": {
                "stages": ["unbox", "physical-prep", "app-install", "pairing", "primary-credential-enrolment", "verification"],
                "exit_criterion": "operator can perform a successful unlock with the enrolled credential",
                "must_link_to": ["installation", "warnings (low-battery, irreversible enrolment)", "troubleshooting (pairing, enrolment)"],
            },
            "installation": {
                "stages": ["site-survey", "tooling-prep", "mounting", "wiring-or-mechanical-engagement", "power-on", "post-install-verification"],
                "exit_criterion": "lock powers on and responds to first credential challenge",
                "must_link_to": ["onboarding", "warnings (irreversible install)", "troubleshooting (install failures)"],
            },
            "troubleshooting": {
                "stages": ["symptom-capture", "diagnostic-questions", "candidate-causes", "next-actions", "escalation-or-resolution"],
                "exit_criterion": "operator either resolves the issue or escalates with a captured diagnostic packet",
                "must_link_to": ["operational-guidance", "warnings (recurrence)", "recovery (if irreversible)"],
            },
        },
        "continuity_awareness": {
            "rule": "every flow must declare its entry preconditions and exit guarantees",
            "renderer_signal": "missing_entry_or_exit_declaration",
        },
        "escalation_aware_navigation": {
            "rule": "any escalation cue must link to the corresponding human-operations channel",
            "fallback_rule": "if no channel reference exists, surface as readability gap",
        },
        "operational_recovery_continuity": {
            "rule": "after any failure path, the operator must be returned to a known-good resumption point or a final 'do not proceed' state",
            "anti_pattern": "open-ended failure with no resumption guidance",
        },
        "coherence_signals_for_renderer": [
            "missing_flow_entry_declaration",
            "missing_flow_exit_declaration",
            "broken_inter_flow_link",
            "unbacked_escalation_cue",
            "open_ended_failure_path",
        ],
    })
    write_md(base / "README.md", "Operational flow coherence",
        "Defines stage models for onboarding, installation, troubleshooting flows and "
        "the continuity, escalation, and recovery guarantees each must satisfy.\n")


# ---------------------------------------------------------------------------
# TASK 5 — Audience readability governance
# ---------------------------------------------------------------------------

def task_audience_readability() -> None:
    base = PQ_ROOT / "audience-readability"
    write_json(base / "audience-profiles.json", {
        **base_envelope("audience-readability",
                        "Per-audience readability rendering profiles. Selection is declarative; renderer applies one profile at a time."),
        "profiles": {
            "end-user": {
                "tone": "friendly, second-person, no jargon",
                "max_steps_per_procedure": 10,
                "include": ["preconditions", "outcomes", "P0/P1 warnings", "next-actions on failure"],
                "exclude": ["internal IDs", "OEM source citations", "candidate-status disclosures", "menu-path code blocks unless essential"],
                "default_section_visibility": ["onboarding", "operational-guidance", "warnings (P0/P1 only)", "quick-start"],
            },
            "installer": {
                "tone": "imperative, technical, terse",
                "max_steps_per_procedure": 15,
                "include": ["tooling list", "preconditions", "irreversibility warnings", "post-install verification"],
                "exclude": ["marketing copy", "end-user friendly framings"],
                "default_section_visibility": ["installation", "warnings (irreversible)", "troubleshooting (install failures)"],
            },
            "operator": {
                "tone": "operational, neutral, present tense",
                "max_steps_per_procedure": 12,
                "include": ["preconditions", "outcomes", "all warnings", "escalation paths"],
                "exclude": [],
                "default_section_visibility": ["onboarding", "operational-guidance", "warnings", "troubleshooting"],
            },
            "reviewer": {
                "tone": "auditable, exhaustive, neutral",
                "max_steps_per_procedure": "unbounded",
                "include": ["everything", "internal IDs", "confidence pills", "validation_status pills", "source_refs", "extraction_lineage", "candidate flags"],
                "exclude": [],
                "default_section_visibility": ["all sections including candidates and pending-review"],
                "default_profile_for_phase_36_renderer": True,
            },
            "support-agent": {
                "tone": "diagnostic, neutral, fast-scan",
                "max_steps_per_procedure": 10,
                "include": ["symptoms", "diagnostic_questions", "next_actions", "escalation cues", "warnings (P0/P1)"],
                "exclude": ["marketing copy", "long-form onboarding narrative"],
                "default_section_visibility": ["troubleshooting", "warnings", "operational-guidance"],
            },
        },
        "selection_rule": "exactly one profile applied per render pass; profile name recorded in publication-metadata",
        "non_visibility_is_not_deletion": "audience filtering hides; knowledge-core never loses content",
        "current_renderer_profile": "reviewer (per phase 36 default)",
        "audience_signals_for_renderer": [
            "profile_id",
            "filtered_entity_count",
            "filtered_section_count",
            "untranslatable_jargon_count",
            "tone_violation_count",
        ],
    })
    write_md(base / "README.md", "Audience readability governance",
        "Defines five rendering profiles (end-user, installer, operator, reviewer, "
        "support-agent). Selection is declarative; the renderer applies exactly one "
        "per pass. Filtering is visibility-only — knowledge-core never loses content.\n")


# ---------------------------------------------------------------------------
# TASK 6 — Drift control
# ---------------------------------------------------------------------------

def task_drift_control() -> None:
    base = PQ_ROOT / "drift-control"
    write_json(base / "drift-control-model.json", {
        **base_envelope("drift-control",
                        "Detects redundancy, duplication, divergence, conflict, and publication drift across renderable knowledge."),
        "detectors": {
            "repeated_procedural_blocks": {
                "signal": "two procedures share >= 80% of normalized step text",
                "action": "promote shared block to a named sub-procedure; replace with reference",
            },
            "duplicated_warnings": {
                "signal": "two warnings share >= 90% of normalized text after lowercasing and whitespace normalisation",
                "action": "merge in knowledge-core (NOT in renderer); record provenance lineage of merged sources",
            },
            "semantic_redundancy": {
                "signal": "two entities have distinct ids but produce indistinguishable rendered output for same audience profile",
                "action": "flag as redundancy candidate; reviewer must resolve",
            },
            "procedural_divergence": {
                "signal": "two procedures targeting the same `summary` produce different step sequences",
                "action": "raise divergence defect; do not auto-pick a winner",
            },
            "conflicting_instructions": {
                "signal": "step A asserts X; step B asserts ¬X; both reachable in same flow",
                "action": "P0 defect; block publication for the affected flow until resolved in knowledge-core",
            },
            "publication_drift": {
                "signal": "rendered HTML byte-checksum differs from manifest's recorded source-ref checksums beyond renderer-version delta",
                "action": "re-render required; rendered HTML is stale",
            },
        },
        "drift_classes": [
            "stale-render", "stale-source", "stale-renderer-version",
            "audience-profile-drift", "subordinate-chain-drift",
        ],
        "non_deletion_rule": "drift control NEVER deletes from knowledge-core; it only flags for reviewer action",
        "no_renderer_authored_merging": "renderer must not silently merge or de-duplicate; only knowledge-core edits resolve drift",
        "drift_signals_for_renderer": [
            "repeated_block_count",
            "duplicated_warning_count",
            "semantic_redundancy_count",
            "procedural_divergence_count",
            "conflicting_instruction_count",
            "publication_drift_flag",
        ],
    })
    write_md(base / "README.md", "Redundancy & publication drift control",
        "Defines six detectors for repetition, duplication, divergence, conflict and "
        "drift. All resolutions occur in knowledge-core; the renderer is forbidden "
        "from silent merging or de-duplication.\n")


# ---------------------------------------------------------------------------
# TASK 7 — Publication quality governance (constitutional doctrine)
# ---------------------------------------------------------------------------

def task_constitution() -> None:
    docs = {
        "00-INDEX.md": (
            "# Publication Quality Governance — index\n\n"
            "Layer 30 doctrine. Modeling-only. Subordinate to knowledge-core, the 29 "
            "prior governance layers, and the executable publication renderer.\n\n"
            "Documents:\n"
            "1. operational-readability-philosophy.md\n"
            "2. human-usability-doctrine.md\n"
            "3. publication-sequencing-principles.md\n"
            "4. cognitive-load-doctrine.md\n"
            "5. procedural-clarity-philosophy.md\n"
            "6. readability-governed-rendering-principles.md\n"
        ),
        "01-operational-readability-philosophy.md": (
            "# Operational readability philosophy\n\n"
            "A governed manual is not measured by what it contains, but by what an "
            "operator can do with it under operational pressure. Readability is a "
            "property of the rendered surface, not of the knowledge-core.\n\n"
            "Principles:\n\n"
            "- The knowledge-core is the source of truth; readability is its rendered projection.\n"
            "- Readability is audience-conditioned; one profile renders at a time.\n"
            "- Readability defects are surfaced, never silently fixed by the renderer.\n"
            "- Readability never licenses content omission outside an explicit audience profile.\n"
        ),
        "02-human-usability-doctrine.md": (
            "# Human usability doctrine\n\n"
            "Usability is judged at the failure edge, not the happy path.\n\n"
            "- Every step must be observable before the next begins.\n"
            "- Every failure must offer a recovery path or an explicit terminal state.\n"
            "- Every escalation must reach a real channel (no orphan cues).\n"
            "- Every irreversible action must be flagged immediately before it occurs.\n"
            "- Operator comprehension is a render-time signal, not a post-hoc audit.\n"
        ),
        "03-publication-sequencing-principles.md": (
            "# Publication sequencing principles\n\n"
            "- Preconditions precede steps.\n"
            "- Warnings precede the steps they govern.\n"
            "- Escalation appears at failure edges, not aggregated at the end.\n"
            "- Recovery instructions accompany the failure they recover from.\n"
            "- Procedural dependencies are explicit; nothing is assumed.\n"
        ),
        "04-cognitive-load-doctrine.md": (
            "# Cognitive-load doctrine\n\n"
            "- Progressive disclosure: present what the current decision needs, defer the rest.\n"
            "- Chunk size: ≤ 7 steps per atomic procedure block.\n"
            "- One verb, one observable outcome, one decision boundary per step.\n"
            "- Repetition is a signal of a missing shared block, not a feature.\n"
            "- Ambiguity (vague pronouns, vague quantifiers, passive voice) is a defect.\n"
        ),
        "05-procedural-clarity-philosophy.md": (
            "# Procedural clarity philosophy\n\n"
            "Clarity is the operator's ability to predict the next state before "
            "performing a step. A procedure that requires the operator to perform "
            "the step before understanding it has failed clarity governance.\n\n"
            "- Action verb + target object + expected observation, every step.\n"
            "- Branches are explicit, never implicit.\n"
            "- Failure observability is mandatory.\n"
        ),
        "06-readability-governed-rendering-principles.md": (
            "# Readability-governed rendering principles\n\n"
            "- The renderer applies readability rules as advisory signals at render time.\n"
            "- The renderer is forbidden from silently editing knowledge-core text.\n"
            "- The renderer is forbidden from silently merging or de-duplicating entities.\n"
            "- The renderer is forbidden from generating prompts or images.\n"
            "- The renderer surfaces every defect; resolution lives in knowledge-core.\n"
            "- The renderer records the active audience profile in publication-metadata.\n"
        ),
    }
    for name, body in docs.items():
        (CONST_ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (CONST_ROOT / name).write_text(body, encoding="utf-8")

    write_json(CONST_ROOT / "manifest.json", {
        **base_envelope("publication-quality-constitution",
                        "Doctrine root for layer 30 — publication quality governance."),
        "documents": list(docs.keys()),
        "constitutional_position": "layer 30 of 30 (knowledge-core counted as layer 0)",
        "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
    })


# ---------------------------------------------------------------------------
# TASK 8 — Future visual integration readiness
# ---------------------------------------------------------------------------

def task_future_visual_readiness() -> None:
    base = PQ_ROOT / "future-visual-readiness"
    write_json(base / "future-visual-readiness.json", {
        **base_envelope("future-visual-readiness",
                        "Prepares publication system for future visual support WITHOUT generating any visuals now."),
        "policy_now": {
            "visuals_generated": False,
            "prompts_generated": False,
            "comfyui_invoked": False,
            "visual_support_status": "declarative-only (consumed from publication-rendering visual-needs.json)",
        },
        "subordination_invariant": "visual support is and remains subordinate to operational readability and procedural clarity",
        "future_integration_points": {
            "supportive_visual_insertion": {
                "where": "renderer attaches a visual asset reference to an entity at render time",
                "constraint": "visual must not replace the procedural text; it augments only",
                "fallback": "if visual asset missing, render proceeds with text; visual-need flag persists",
            },
            "procedural_visual_orchestration": {
                "where": "multi-step procedures may receive a sequence-illustration asset",
                "constraint": "step text remains canonical; visual asset is annotated with step ids",
            },
            "hybrid_schematic_rendering": {
                "where": "installation flows may receive a schematic alongside textual orientation",
                "constraint": "schematic must not contradict component-visibility-map",
            },
            "visual_assisted_onboarding": {
                "where": "onboarding flows may receive UI screenshots for app-pairing steps",
                "constraint": "screenshots subject to visual-system app-ui-policy",
            },
            "troubleshooting_visual_support": {
                "where": "diagnostic decision trees may receive a flow diagram",
                "constraint": "decision text remains canonical; diagram is supplementary",
            },
        },
        "consumed_inputs_when_visuals_arrive": [
            "publication-rendering/visual-needs/visual-needs.json (per product)",
            "ext-images/<product>/knowledge-core/visual-intent/*.json",
            "ext-images/<product>/knowledge-core/component-visibility/*.json",
            "visual-system/_governance/* (existing visual-system policies)",
        ],
        "ordering_rule_for_future_phase": [
            "do not generate visuals before audience-aware readability filtering is operational",
            "do not generate visuals before drift-control detectors are wired",
            "do not generate visuals before reviewer-validation console exists",
        ],
        "explicit_non_goals_this_phase": [
            "no prompt strings produced",
            "no image bytes produced",
            "no comfy workflow definitions produced",
            "no visual placement decisions made",
        ],
    })
    write_md(base / "README.md", "Future visual integration readiness",
        "Declarative readiness for visual support in a future phase. No visuals, no "
        "prompts, no ComfyUI invocation now. Visual support remains subordinate to "
        "operational readability and procedural clarity.\n")


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def write_report(name: str, payload: Dict[str, Any], md_body: str) -> None:
    write_json(REPORTS_ROOT / f"{name}.json", payload)
    write_md(REPORTS_ROOT / f"{name}.md", payload.get("title", name), md_body)


def emit_reports() -> None:
    write_report("01-readability-model-summary", {
        "title": "01 — Readability model summary",
        **base_envelope("readability", "Per-section readability standards for rendered manuals."),
        "section_standards_count": 6,
        "scoring_signals_count": 7,
        "artifact": rel(PQ_ROOT / "readability" / "readability-model.json"),
    }, "Six section standards (onboarding, installation, troubleshooting, warnings, "
       "operational-guidance, quick-start). Seven scoring signals exposed to renderer "
       "as advisory only.\n")

    write_report("02-procedural-sequencing-summary", {
        "title": "02 — Procedural sequencing summary",
        **base_envelope("procedural-sequencing", "Sequencing rules for warnings, escalation, and recovery."),
        "ordering_rules_count": 9,
        "warning_priority_classes": ["P0", "P1", "P2", "P3"],
        "artifact": rel(PQ_ROOT / "procedural-sequencing" / "sequencing-model.json"),
    }, "Nine ordering rules including warnings-before-irreversible, escalation-at-failure-edge, "
       "no-orphan-warnings, no-late-prerequisites.\n")

    write_report("03-cognitive-load-summary", {
        "title": "03 — Cognitive load summary",
        **base_envelope("cognitive-load", "Progressive disclosure, chunking, ambiguity controls."),
        "chunk_size_max_steps": 7,
        "cognitive_signals_count": 6,
        "artifact": rel(PQ_ROOT / "cognitive-load" / "cognitive-load-model.json"),
    }, "Chunk size capped at 7 steps. Six cognitive defect signals exposed to renderer.\n")

    write_report("04-flow-coherence-summary", {
        "title": "04 — Flow coherence summary",
        **base_envelope("flow-coherence", "End-to-end coherence across onboarding/installation/troubleshooting."),
        "flows_modeled": ["onboarding", "installation", "troubleshooting"],
        "coherence_signals_count": 5,
        "artifact": rel(PQ_ROOT / "flow-coherence" / "flow-coherence-model.json"),
    }, "Three flow stage models with explicit entry preconditions and exit guarantees.\n")

    write_report("05-audience-readability-summary", {
        "title": "05 — Audience readability summary",
        **base_envelope("audience-readability", "Five audience profiles for rendering."),
        "profiles": ["end-user", "installer", "operator", "reviewer", "support-agent"],
        "current_renderer_profile": "reviewer",
        "non_visibility_is_not_deletion": True,
        "artifact": rel(PQ_ROOT / "audience-readability" / "audience-profiles.json"),
    }, "Five profiles. Renderer applies exactly one per pass. Filtering is visibility-only; "
       "knowledge-core never loses content.\n")

    write_report("06-drift-control-summary", {
        "title": "06 — Drift control summary",
        **base_envelope("drift-control", "Detection of redundancy, duplication, divergence, conflict, drift."),
        "detectors_count": 6,
        "renderer_authored_merging_allowed": False,
        "artifact": rel(PQ_ROOT / "drift-control" / "drift-control-model.json"),
    }, "Six detectors. Renderer is forbidden from silent merging or de-duplication; all "
       "resolutions occur in knowledge-core.\n")

    write_report("07-publication-quality-governance-summary", {
        "title": "07 — Publication quality governance constitution summary",
        **base_envelope("publication-quality-constitution", "Layer 30 doctrine summary."),
        "documents_count": 7,
        "constitutional_position": "layer 30",
        "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
        "artifact": rel(CONST_ROOT / "manifest.json"),
    }, "Seven doctrine documents covering readability philosophy, human usability, "
       "sequencing, cognitive load, procedural clarity, and rendering principles.\n")

    write_report("08-future-visual-readiness-summary", {
        "title": "08 — Future visual readiness summary",
        **base_envelope("future-visual-readiness", "Declarative readiness for visuals; nothing generated."),
        "visuals_generated": False,
        "prompts_generated": False,
        "comfyui_invoked": False,
        "subordination_invariant": "visual support remains subordinate to operational readability and procedural clarity",
        "future_integration_points_count": 5,
        "artifact": rel(PQ_ROOT / "future-visual-readiness" / "future-visual-readiness.json"),
    }, "Five integration points declared. No visuals, prompts, or ComfyUI invocations.\n")

    write_report("09-unresolved-readability-risks", {
        "title": "09 — Unresolved readability risks",
        **base_envelope("readability-risks", "Risks not resolved by this phase."),
        "structural_risks": [
            "no readability scorer wired into renderer yet (signals defined, not computed)",
            "no audience-profile selector in renderer yet (single 'reviewer' profile applied)",
            "no drift detectors implemented yet (model defined, detectors not run)",
            "no shared-procedure-block extraction yet (repetition surfaces but does not auto-promote)",
            "no escalation channel registry referenced (escalation cues currently free-text)",
            "no recovery-path attachment validator yet",
            "no publication freshness check between knowledge-core and rendered HTML",
            "no quick-start renderer pass yet (model defined; section not yet emitted)",
            "no per-step linguistic linter yet (passive voice, ambiguous pronouns undetected)",
        ],
        "policy_risks": [
            "audience-profile filtering may silently hide safety content if applied incorrectly — must remain visibility-only",
            "renderer-authored merging is currently impossible by policy but enforcement is policy-only, not mechanical",
        ],
        "out_of_scope_for_this_phase": [
            "implementing the scorer",
            "implementing audience selection",
            "implementing drift detectors",
            "implementing the linter",
            "rendering a quick-start section",
        ],
    }, "Risks are documented; remediation lives in subsequent execution phases. No silent "
       "enforcement is added here.\n")

    write_report("10-publication-usability-reassessment", {
        "title": "10 — Publication usability reassessment",
        **base_envelope("publication-usability-reassessment", "Reassesses platform usability after layer 30 doctrine."),
        "platform_status": "publication-capable + runtime-governed + publication-rendering ready + readability-governed",
        "readability_governance_status": "MODELED (executable enforcement scheduled for next track)",
        "primary_bottleneck_resolved": "absence of doctrine for readability, sequencing, cognitive-load, audience filtering, drift control, and future-visual-readiness",
        "remaining_bottlenecks": [
            "readability scorer (executable)",
            "audience-profile selector in renderer",
            "drift detectors (executable)",
            "linguistic linter",
            "publication freshness check",
            "escalation channel registry",
            "quick-start render path",
            "reviewer-validation console (carry-over)",
        ],
        "next_track": "scorer + audience selector + drift detectors + linter (executable companions to this layer)",
        "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
        "runtime_impact": "none (modeling-only)",
        "renderer_impact": "additive advisory signals only; no behaviour change required to keep current outputs valid",
    }, "Doctrine for human readability and publication quality is now in place. "
       "Knowledge-core remains canonical; renderer remains the only assembler; "
       "executable enforcement is the next track.\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build() -> None:
    PQ_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    task_readability()
    task_procedural_sequencing()
    task_cognitive_load()
    task_flow_coherence()
    task_audience_readability()
    task_drift_control()
    task_constitution()
    task_future_visual_readiness()
    emit_reports()

    print("Publication Quality Governance written to:")
    print(f"  {rel(PQ_ROOT)}")
    print(f"  {rel(CONST_ROOT)}")
    print(f"  {rel(REPORTS_ROOT)}")
    print(f"  Subordinate chain length: {len(SUBORDINATE_TO) + 1}")


if __name__ == "__main__":
    build()
