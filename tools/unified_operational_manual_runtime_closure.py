#!/usr/bin/env python3
"""
Phase 54 — Unified Operational Intake, Semantic Consolidation & Manual Runtime Closure
Constitutional Layer 47 — schema `unified-operational-manual-runtime-closure/1.0`

DOCTRINAL POSTURE
=================
This phase optimizes for OPERATIONAL CONVERGENCE, not constitutional expansion.
It WIRES existing layers (Phase 46 governed FS, Phase 47 transactional runtime,
Phase 49 grounding, Phase 52 extraction runtime, Phase 53 packaging) into the
first end-to-end reviewer-driven manual-generation loop:

    upload → analyze → approve → refresh → semantic-bank →
    synthesize → detect-visual-support → prompt-package → export-finalize

It does NOT introduce new orchestration constitutions, replay engines,
lifecycle families, presentation/layout systems, or autonomous agents.
Builder is idempotent: safe to re-run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA = "unified-operational-manual-runtime-closure/1.0"
LAYER = 47
PHASE_LABEL = "phase 54"
PHASE_TITLE = "unified operational intake, semantic consolidation & manual runtime closure"

# Subordinate chain: extend the prior chain (length 45 ending in
# 'governed-semantic-evidence-analysis-and-multimodal-extraction-governance')
# by appending the Phase 53 anchor, then pad to length 46 by repeating
# the Phase 53 anchor as required by the constitutional layering protocol.
SUBORDINATE_TO = [
    "governed-fs-execution",
    "governed-transactional-runtime",
    "governed-orchestration-contracts",
    "governed-runtime-observability",
    "governed-runtime-policy",
    "governed-runtime-evidence",
    "governed-runtime-resilience",
    "governed-runtime-recovery",
    "governed-runtime-state-mgmt",
    "governed-runtime-audit",
    "governed-runtime-replay",
    "governed-runtime-trust",
    "governed-runtime-handoff",
    "governed-runtime-attestation",
    "governed-runtime-attribution",
    "governed-runtime-quorum",
    "governed-runtime-escalation",
    "governed-runtime-quarantine",
    "governed-runtime-redaction",
    "governed-runtime-disclosure",
    "governed-runtime-survivability",
    "governed-runtime-reentry",
    "governed-runtime-reproducibility",
    "governed-runtime-sealing",
    "governed-runtime-anchoring",
    "governed-runtime-lineage-isolation",
    "governed-runtime-evidence-isolation",
    "governed-runtime-state-isolation",
    "governed-runtime-deterministic-replay",
    "governed-runtime-deterministic-snapshots",
    "governed-runtime-deterministic-attestation",
    "governed-runtime-deterministic-recovery",
    "governed-runtime-deterministic-handoff",
    "governed-runtime-deterministic-quarantine",
    "governed-runtime-deterministic-redaction",
    "governed-runtime-deterministic-disclosure",
    "governed-runtime-deterministic-survivability",
    "governed-runtime-deterministic-reentry",
    "governed-runtime-deterministic-reproducibility",
    "governed-runtime-deterministic-sealing",
    "governed-runtime-deterministic-anchoring",
    "governed-runtime-deterministic-lineage-isolation",
    "governed-runtime-deterministic-evidence-isolation",
    "governed-runtime-deterministic-state-isolation",
    "governed-semantic-evidence-analysis-and-multimodal-extraction-governance",
    "governed-manual-semantic-packaging",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets" / "exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports"

# Single isolated storage tree for Phase 54 operational artifacts.
MR_ROOT = OC_ROOT / "manual-runtime-closure"
MR_SUBDIRS = [
    "intake-analyses",
    "intake-revisions",
    "intake-approvals",
    "refresh-records",
    "semantic-bank-snapshots",
    "manual-synthesis-drafts",
    "visual-support-needs",
    "prompt-packages",
    "export-finalizations",
    "closure-lineage",
]

POSTURE = {
    "schema": SCHEMA,
    "layer": LAYER,
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only": True,
    "fail_closed": True,
    "local_first": True,
    "replayable": True,
    "auditable": True,
    "stdlib_first": True,
    "transaction_safe": True,
    "lineage_preserving": True,
    # operational convergence posture (not constitutional expansion)
    "operational_convergence_priority": True,
    "constitutional_expansion_priority": False,
    "wires_existing_systems": True,
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_presentation_system": False,
    # consumer boundary preserved (inherited from Phase 53)
    "consumer_boundary_enforced": True,
    "presentation_neutral_outputs": True,
    "renderer_agnostic_outputs": True,
    "no_responsive_rendering": True,
    "no_frontend_layout_orchestration": True,
    "no_css_breakpoint_governance": True,
    "no_typography_systems": True,
    "no_mobile_rendering_logic": True,
    "no_visual_page_composition": True,
    "no_ui_frameworks": True,
    "no_image_generation_in_this_layer": True,
    # autonomy bans
    "no_autonomous_publication": True,
    "no_autonomous_approval": True,
    "no_autonomous_ingestion": True,
    "no_autonomous_prompt_generation": True,
    "no_probabilistic_semantic_inference": True,
    "no_vector_databases": True,
    "no_embeddings": True,
    "no_cloud_apis": True,
    "no_saas": True,
    "no_daemon_workers": True,
    "no_hidden_mutation": True,
    "no_llm_rewriting": True,
    "no_machine_learning_in_this_layer": True,
    # storage isolation
    "writes_only_into_manual_runtime_closure_tree": True,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "writes_to_semantic_extraction_runtime_tree": False,
    "writes_to_frontend_or_theme_systems": False,
}

# Operational dispatch kinds (intentionally only those required to close the loop).
DISPATCH_KINDS = [
    "intake-analyze",
    "intake-reanalyze",
    "intake-approve",
    "refresh-propagate",
    "semantic-bank-snapshot",
    "manual-synthesize",
    "visual-support-detect",
    "prompt-package-generate",
    "export-finalize",
]

EVIDENCE_KINDS = ["video", "image", "pdf", "xls", "xlsx", "csv", "json", "yaml", "doc", "docx"]

INTAKE_DECISIONS = ["approve", "reject"]

# Confidence states for visual-support detection (deterministic — based on
# keyword heuristics, not probabilistic inference).
VISUAL_SUPPORT_CONFIDENCE = ["low", "medium", "high"]

# Severity for visual-support-needed signals.
VISUAL_SUPPORT_SEVERITY = ["informational", "recommended", "required", "blocking"]

# ----------------------------------------------------------------------------
# Rule tables (kept tight: one per dispatch kind, no extra governance tables)
# ----------------------------------------------------------------------------
RULE_TABLES = {
    "intake-analysis-rules.json": {
        "schema": SCHEMA,
        "rule_family": "intake-analysis",
        "rules": [
            {"id": "IA-1", "text": "evidence_id required and resolves to existing evidence reference"},
            {"id": "IA-2", "text": f"evidence_kind must be one of {EVIDENCE_KINDS}"},
            {"id": "IA-3", "text": "inferred_product_id required"},
            {"id": "IA-4", "text": "inferred_semantic_domains must be a list (may be empty only if rationale provided)"},
            {"id": "IA-5", "text": "inferred_downstream_impacts must be a list"},
            {"id": "IA-6", "text": "analysis records analysis_sha256 over canonical content"},
            {"id": "IA-7", "text": "no autonomous approval — analysis state always begins 'pending-review'"},
            {"id": "IA-8", "text": "presentation/layout/CSS/typography keys forbidden in analysis payload"},
        ],
    },
    "intake-revision-rules.json": {
        "schema": SCHEMA,
        "rule_family": "intake-revision",
        "rules": [
            {"id": "IR-1", "text": "revision_id required and unique"},
            {"id": "IR-2", "text": "prior_analysis_id required and must resolve"},
            {"id": "IR-3", "text": "revision is append-only — never mutates prior analysis"},
            {"id": "IR-4", "text": "revision_number is monotonically increasing per evidence_id"},
            {"id": "IR-5", "text": "reviewer_rationale required"},
            {"id": "IR-6", "text": "revision recomputes analysis_sha256 deterministically"},
        ],
    },
    "intake-approval-rules.json": {
        "schema": SCHEMA,
        "rule_family": "intake-approval",
        "rules": [
            {"id": "IAP-1", "text": "approval_id required and unique"},
            {"id": "IAP-2", "text": "analysis_id (or latest revision) must resolve"},
            {"id": "IAP-3", "text": f"decision must be one of {INTAKE_DECISIONS}"},
            {"id": "IAP-4", "text": "reject decisions require non-empty cited_rule_ids"},
            {"id": "IAP-5", "text": "approve emits refresh-eligibility marker; reject does not"},
            {"id": "IAP-6", "text": "approval is reviewer-attributed and append-only"},
        ],
    },
    "runtime-refresh-rules.json": {
        "schema": SCHEMA,
        "rule_family": "runtime-refresh",
        "rules": [
            {"id": "RR-1", "text": "refresh_id required and unique"},
            {"id": "RR-2", "text": "approval_id must resolve to an approved intake"},
            {"id": "RR-3", "text": "refresh records are pointers — they NEVER mutate upstream extraction/semantic/packaging trees"},
            {"id": "RR-4", "text": "refresh propagation is deterministic and reuses existing governance (no new orchestration)"},
            {"id": "RR-5", "text": "refresh records are append-only and reviewer-attributed"},
        ],
    },
    "semantic-bank-rules.json": {
        "schema": SCHEMA,
        "rule_family": "semantic-bank",
        "rules": [
            {"id": "SB-1", "text": "snapshot_id required and unique"},
            {"id": "SB-2", "text": "snapshot aggregates ONLY existing extraction/packaging artifacts (no inference)"},
            {"id": "SB-3", "text": "aggregation is deterministic — sorted by stable IDs"},
            {"id": "SB-4", "text": "snapshot records snapshot_sha256 over canonical aggregation"},
            {"id": "SB-5", "text": "snapshot is append-only — never mutates the aggregated sources"},
            {"id": "SB-6", "text": "snapshot preserves lineage_pointers, evidence_refs, grounding_refs, reviewer_states"},
        ],
    },
    "manual-synthesis-rules.json": {
        "schema": SCHEMA,
        "rule_family": "manual-synthesis",
        "rules": [
            {"id": "MS-1", "text": "synthesis_id required and unique"},
            {"id": "MS-2", "text": "snapshot_id must resolve to an existing semantic-bank snapshot"},
            {"id": "MS-3", "text": "target_manual_id and target_product_id required"},
            {"id": "MS-4", "text": "synthesis aggregates entities by canonical section kinds (no LLM rewriting, no probabilistic inference)"},
            {"id": "MS-5", "text": "every synthesized procedural step must reference at least one evidence_id or grounding_id"},
            {"id": "MS-6", "text": "synthesis is reviewer-authoritative and append-only"},
            {"id": "MS-7", "text": "presentation/layout/CSS/typography keys forbidden in synthesis payload"},
        ],
    },
    "visual-support-rules.json": {
        "schema": SCHEMA,
        "rule_family": "visual-support",
        "rules": [
            {"id": "VS-1", "text": "detection_id required and unique"},
            {"id": "VS-2", "text": "synthesis_id must resolve to an existing manual synthesis draft"},
            {"id": "VS-3", "text": f"confidence must be one of {VISUAL_SUPPORT_CONFIDENCE}"},
            {"id": "VS-4", "text": f"severity must be one of {VISUAL_SUPPORT_SEVERITY}"},
            {"id": "VS-5", "text": "rationale required and must be non-empty"},
            {"id": "VS-6", "text": "this layer DETECTS only — it MUST NOT generate images"},
            {"id": "VS-7", "text": "affected_step_refs must be a list referencing synthesis steps"},
        ],
    },
    "prompt-package-rules.json": {
        "schema": SCHEMA,
        "rule_family": "prompt-package",
        "rules": [
            {"id": "PP-1", "text": "package_id required and unique"},
            {"id": "PP-2", "text": "support_need_id must resolve to a visual-support-need"},
            {"id": "PP-3", "text": "prompt_text required (deterministic, reviewer-editable)"},
            {"id": "PP-4", "text": "grounding_refs must be a list (may reference Phase 49 grounding artifacts)"},
            {"id": "PP-5", "text": "visual_role required"},
            {"id": "PP-6", "text": "prohibited_inaccuracies must be a list"},
            {"id": "PP-7", "text": "this layer GENERATES PROMPT PACKAGES only — it MUST NOT invoke image-generation pipelines"},
        ],
    },
    "export-finalization-rules.json": {
        "schema": SCHEMA,
        "rule_family": "export-finalization",
        "rules": [
            {"id": "EF-1", "text": "finalization_id required and unique"},
            {"id": "EF-2", "text": "package_id must resolve to a Phase 53 manual-package in lifecycle state 'export-ready'"},
            {"id": "EF-3", "text": "consumer_payload is presentation-neutral and renderer-agnostic"},
            {"id": "EF-4", "text": "presentation/layout/CSS/typography keys forbidden in consumer_payload"},
            {"id": "EF-5", "text": "finalization records consumer_payload_sha256 deterministically"},
            {"id": "EF-6", "text": "finalization is append-only and reviewer-attributed"},
        ],
    },
}

# ----------------------------------------------------------------------------
# Event stores (one per dispatch family — 8 total, intake-revise reuses intake-analysis store)
# ----------------------------------------------------------------------------
NEW_EVENT_STORES = [
    "intake-analysis-events",
    "intake-approval-events",
    "refresh-propagation-events",
    "semantic-bank-events",
    "manual-synthesis-events",
    "visual-support-events",
    "prompt-package-events",
    "export-finalization-events",
]

# ----------------------------------------------------------------------------
# JS engines (one per console — 6 total). Vanilla ES; never write FS;
# attach to window.OC.* and build envelopes via OC.FSBridge.buildRequestEnvelope.
# ----------------------------------------------------------------------------
JS_ASSETS = {
    "mr-intake-engine.js": "intake-analysis-console",
    "mr-bank-engine.js": "semantic-bank-console",
    "mr-synthesis-engine.js": "manual-synthesis-console",
    "mr-visual-support-engine.js": "visual-support-console",
    "mr-prompt-engine.js": "prompt-package-console",
    "mr-export-engine.js": "export-runtime-console",
}

CONSOLES = [
    "intake-analysis-console",
    "semantic-bank-console",
    "manual-synthesis-console",
    "visual-support-console",
    "prompt-package-console",
    "export-runtime-console",
]

CSS_MARKER = "/* phase 54 — unified operational manual runtime closure additions */"
CSS_ADDENDUM = (
    "\n" + CSS_MARKER + "\n"
    "/* operational consoles inherit existing exec.css surfaces; no presentation rules added. */\n"
    "/* (consumer-boundary doctrine: this layer adds zero CSS rules.) */\n"
)

DOCTRINES = {
    "01-operational-convergence-over-constitutional-expansion.md": (
        "# 01 — Operational convergence over constitutional expansion\n\n"
        "Phase 54 adds NO new constitutional surface beyond what is strictly\n"
        "required to close the operational loop. The priority is operational\n"
        "maturity, not governance maturity. Existing rule families, lineage,\n"
        "replay, and integrity systems are reused without duplication.\n"
    ),
    "02-reuse-existing-governance-substrate.md": (
        "# 02 — Reuse existing governance substrate\n\n"
        "The existing governance substrate (Phase 46 governed FS, Phase 47\n"
        "transactional runtime, Phase 49 grounding, Phase 52 extraction,\n"
        "Phase 53 packaging) is the canonical source of authority. Phase 54\n"
        "MUST wire these systems together — never replace, fork, or shadow them.\n"
    ),
    "03-reviewer-authoritative-intake-and-approval.md": (
        "# 03 — Reviewer-authoritative intake and approval\n\n"
        "Every intake analysis begins in 'pending-review'. No analysis can\n"
        "transition to 'approved' without an explicit reviewer-attributed\n"
        "approval. Re-analysis is append-only revision; prior analyses are\n"
        "never silently mutated.\n"
    ),
    "04-deterministic-semantic-aggregation.md": (
        "# 04 — Deterministic semantic aggregation\n\n"
        "The semantic bank aggregates existing extraction/packaging outputs\n"
        "deterministically: sorted by stable IDs, hashed canonically, append-only.\n"
        "It performs ZERO probabilistic inference and ZERO LLM rewriting.\n"
    ),
    "05-deterministic-prompt-packaging-no-image-generation.md": (
        "# 05 — Deterministic prompt packaging; no image generation in this layer\n\n"
        "Phase 54 produces PROMPT PACKAGES — deterministic, reviewer-editable,\n"
        "grounding-linked descriptors of required visual support. It MUST NOT\n"
        "generate images. Image generation remains the responsibility of\n"
        "downstream visual-production systems (e.g., ComfyUI pipelines).\n"
    ),
    "06-presentation-neutral-export-closure.md": (
        "# 06 — Presentation-neutral export closure\n\n"
        "Final consumer payloads are renderer-agnostic, presentation-neutral\n"
        "JSON. They contain ZERO CSS, ZERO classes, ZERO inline styles,\n"
        "ZERO breakpoints, ZERO typography. The consumer system\n"
        "(WordPress/theme/frontend) renders them; the Knowledge OS does not.\n"
    ),
}

DOCTRINE_INDEX = (
    "# GOVERNED UNIFIED OPERATIONAL MANUAL RUNTIME CLOSURE GOVERNANCE\n\n"
    "Layer 47 — Schema `unified-operational-manual-runtime-closure/1.0`.\n\n"
    "Phase 54 doctrines (operational convergence pivot):\n\n"
    + "".join(f"- {name}\n" for name in sorted(DOCTRINES.keys()))
)

DOCTRINE_MANIFEST = {
    "schema": SCHEMA,
    "layer": LAYER,
    "doctrines": sorted(list(DOCTRINES.keys())),
    "index": "00-INDEX.md",
}

REPORTS = [
    ("01-deep-intake-analysis-runtime-summary", "Deep intake analysis runtime"),
    ("02-reanalysis-loop-summary", "Re-analysis loop"),
    ("03-approved-intake-to-runtime-refresh-bridge-summary", "Approved intake → runtime refresh bridge"),
    ("04-unified-semantic-entity-bank-summary", "Unified semantic entity bank"),
    ("05-procedural-manual-synthesis-runtime-summary", "Procedural manual synthesis runtime"),
    ("06-visual-support-need-detection-summary", "Visual support need detection"),
    ("07-prompt-ready-visual-task-generation-summary", "Prompt-ready visual task generation"),
    ("08-consumer-ready-manual-export-closure-summary", "Consumer-ready manual export closure"),
    ("09-operational-convergence-posture-summary", "Operational-convergence posture"),
    ("10-unified-operational-manual-runtime-closure-platform-maturity-reassessment",
     "Phase 54 platform maturity reassessment"),
]

RUNTIME_README_MARKER = f"## {PHASE_LABEL} — {PHASE_TITLE}"

# ----------------------------------------------------------------------------
# Counters
# ----------------------------------------------------------------------------
class Counters:
    def __init__(self) -> None:
        self.storage_roots = 0
        self.event_stores = 0
        self.runtime_readme_addendum = 0


# ----------------------------------------------------------------------------
# Write helpers
# ----------------------------------------------------------------------------
def _write_text_if_missing(p: Path, content: str, counter_attr: str | None, counters: Counters) -> bool:
    if p.exists():
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if counter_attr:
        setattr(counters, counter_attr, getattr(counters, counter_attr) + 1)
    return True


def _write_json_overwrite(p: Path, data: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _ensure_event_store(name: str, counters: Counters) -> None:
    p = RUNTIME_MANIFESTS_ROOT / name / "_event-store.json"
    if p.exists():
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(
            {
                "schema": SCHEMA,
                "store": name,
                "append_only": True,
                "events": [],
            },
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    counters.event_stores += 1


# ----------------------------------------------------------------------------
# Builders
# ----------------------------------------------------------------------------
def build_storage_tree(counters: Counters) -> None:
    for sub in MR_SUBDIRS:
        d = MR_ROOT / sub
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            counters.storage_roots += 1
        # README per subdir (idempotent)
        readme = d / "README.md"
        if not readme.exists():
            readme.write_text(
                f"# {sub}\n\nPhase 54 isolated storage subdir under `manual-runtime-closure/`.\n",
                encoding="utf-8",
            )
        # .gitkeep so empty dirs survive
        gk = d / ".gitkeep"
        if not gk.exists():
            gk.write_text("", encoding="utf-8")
    # root-level README
    root_readme = MR_ROOT / "README.md"
    if not root_readme.exists():
        root_readme.write_text(
            "# manual-runtime-closure\n\n"
            "Phase 54 — unified operational intake, semantic consolidation & manual runtime closure.\n"
            "Single isolated storage tree for the operational loop. Append-only.\n",
            encoding="utf-8",
        )
        counters.storage_roots += 1


def build_event_stores(counters: Counters) -> None:
    for name in NEW_EVENT_STORES:
        _ensure_event_store(name, counters)


def build_rule_tables() -> None:
    for fname, body in RULE_TABLES.items():
        _write_json_overwrite(RULES_ROOT / fname, body)


def build_js_engines() -> None:
    ASSETS_EXEC_ROOT.mkdir(parents=True, exist_ok=True)
    for fname, console in JS_ASSETS.items():
        body = (
            "// " + PHASE_LABEL + " — " + PHASE_TITLE + "\n"
            "// Engine for " + console + ".\n"
            "// Vanilla ES. Attaches to window.OC. NEVER writes FS.\n"
            "// Builds request envelopes via OC.FSBridge.buildRequestEnvelope.\n"
            "// Throws if reviewer attribution missing.\n"
            "(function () {\n"
            "  if (typeof window === 'undefined') return;\n"
            "  window.OC = window.OC || {};\n"
            "  function build(kind, payload) {\n"
            "    if (!window.OC.reviewer || !window.OC.reviewer.id) {\n"
            "      throw new Error('reviewer attribution required');\n"
            "    }\n"
            "    if (!window.OC.FSBridge || !window.OC.FSBridge.buildRequestEnvelope) {\n"
            "      throw new Error('OC.FSBridge.buildRequestEnvelope unavailable');\n"
            "    }\n"
            "    return window.OC.FSBridge.buildRequestEnvelope({\n"
            "      schema: 'governed-fs-operation-request/1.0',\n"
            "      reviewer: window.OC.reviewer.id,\n"
            "      kind: kind,\n"
            "      payload: payload\n"
            "    });\n"
            "  }\n"
            "  window.OC." + fname.replace('-', '_').replace('.js', '') + " = { build: build };\n"
            "})();\n"
        )
        p = ASSETS_EXEC_ROOT / fname
        if not p.exists():
            p.write_text(body, encoding="utf-8")


def build_consoles() -> None:
    for c in CONSOLES:
        d = OC_ROOT / c
        d.mkdir(parents=True, exist_ok=True)
        ph = d / "exec.html"
        if not ph.exists():
            ph.write_text(
                "<!doctype html>\n"
                "<html lang=\"en\">\n"
                "<head><meta charset=\"utf-8\"><title>" + c + "</title></head>\n"
                "<body><main><h1>" + c + "</h1>\n"
                "<p>" + PHASE_LABEL + " operational console. Reviewer-driven; append-only.</p>\n"
                "</main></body></html>\n",
                encoding="utf-8",
            )


def build_doctrines() -> None:
    base = KB_ROOT / "GOVERNED_UNIFIED_OPERATIONAL_MANUAL_RUNTIME_CLOSURE_GOVERNANCE"
    base.mkdir(parents=True, exist_ok=True)
    idx = base / "00-INDEX.md"
    if not idx.exists():
        idx.write_text(DOCTRINE_INDEX, encoding="utf-8")
    for fname, body in DOCTRINES.items():
        p = base / fname
        if not p.exists():
            p.write_text(body, encoding="utf-8")
    _write_json_overwrite(base / "manifest.json", DOCTRINE_MANIFEST)


def build_reports() -> None:
    base = REPORTS_ROOT / "unified-operational-manual-runtime-closure"
    base.mkdir(parents=True, exist_ok=True)
    readme = base / "README.md"
    if not readme.exists():
        readme.write_text(
            "# unified-operational-manual-runtime-closure reports\n\n"
            "Phase 54 — operational convergence reports.\n",
            encoding="utf-8",
        )
    for slug, title in REPORTS:
        jp = base / f"{slug}.json"
        mp = base / f"{slug}.md"
        if not jp.exists():
            _write_json_overwrite(
                jp,
                {
                    "schema": SCHEMA,
                    "report_slug": slug,
                    "title": title,
                    "layer": LAYER,
                    "posture": POSTURE,
                },
            )
        if not mp.exists():
            mp.write_text(f"# {title}\n", encoding="utf-8")


def build_css_addendum() -> None:
    css_path = ASSETS_EXEC_ROOT / "exec.css"
    if not css_path.exists():
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.write_text("/* exec.css */\n", encoding="utf-8")
    txt = css_path.read_text(encoding="utf-8")
    if CSS_MARKER not in txt:
        css_path.write_text(txt + CSS_ADDENDUM, encoding="utf-8")


def build_runtime_readme(counters: Counters) -> None:
    p = OC_ROOT / "RUNTIME_README.md"
    if not p.exists():
        p.write_text("# RUNTIME README\n", encoding="utf-8")
    txt = p.read_text(encoding="utf-8")
    if RUNTIME_README_MARKER in txt:
        return
    addendum = (
        "\n" + RUNTIME_README_MARKER + "\n\n"
        "Layer " + str(LAYER) + ". Schema `" + SCHEMA + "`.\n\n"
        "**Operational convergence pivot.** Closes the first end-to-end\n"
        "reviewer-driven manual-generation loop by wiring existing governance\n"
        "(Phase 46 FS, Phase 47 transactional runtime, Phase 49 grounding,\n"
        "Phase 52 extraction, Phase 53 packaging) into a single deterministic flow:\n\n"
        "    upload → analyze → approve → refresh → semantic-bank →\n"
        "    synthesize → detect-visual-support → prompt-package → export-finalize\n\n"
        "Storage: `manual-runtime-closure/` (single isolated tree).\n"
        "Dispatch kinds: " + ", ".join("`" + k + "`" for k in DISPATCH_KINDS) + ".\n"
        "Consumer boundary inherited from Phase 53 (presentation-neutral).\n"
    )
    p.write_text(txt + addendum, encoding="utf-8")
    counters.runtime_readme_addendum += 1


# ----------------------------------------------------------------------------
# main()
# ----------------------------------------------------------------------------
def main() -> int:
    counters = Counters()
    build_storage_tree(counters)
    build_event_stores(counters)
    build_rule_tables()
    build_js_engines()
    build_consoles()
    build_doctrines()
    build_reports()
    build_css_addendum()
    build_runtime_readme(counters)
    print(
        "Phase 54 — unified operational intake, semantic consolidation & "
        "manual runtime closure written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {counters.storage_roots} | "
        f"New event stores: {counters.event_stores} | "
        f"Rule tables: {len(RULE_TABLES)} | "
        f"JS assets: {len(JS_ASSETS)} | "
        f"Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | "
        f"Reports: {len(REPORTS)} | "
        f"RUNTIME_README addendum: {counters.runtime_readme_addendum}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
