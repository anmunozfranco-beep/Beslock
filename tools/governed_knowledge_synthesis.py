"""
Phase 48 — Governed Knowledge Synthesis & Canonical Publication Generation.

Layer 41 over layer 40 (governed-transactional-execution-and-recovery).

Idempotent, additive, stdlib-only. Builds the deterministic synthesis surface,
the publication generation rule tables, the publication state machine, the
Colombian operational rendering ruleset, and the reviewer-governed
publication lifecycle. NEVER writes manuals or filesystem mutations on its
own — those land only via the layer-41 executor with --confirm and via the
layer-39 mutation executor it delegates to.

Posture: deterministic, reviewer-authoritative, append-only, local-first,
fail-closed. NO LLM. NO probabilistic inference. NO embeddings. NO cloud.
NO SaaS. NO autonomous synthesis. NO silent evidence merging. NO auto
publication.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
SYNTHESIS_DRAFTS_ROOT = OC_ROOT / "synthesis-drafts"
PUBLICATION_BUILDS_ROOT = OC_ROOT / "publication-builds"
ASSETS_ROOT = OC_ROOT / "assets" / "exec"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "GOVERNED_KNOWLEDGE_SYNTHESIS_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "governed-knowledge-synthesis"

SCHEMA = "governed-knowledge-synthesis/1.0"
LAYER = 41

SUBORDINATE_TO = [
    "domain-evidence-extraction",
    "ontology-mapping",
    "semantic-bindings",
    "knowledge-core",
    "evidence-trust-tiers",
    "domain-routing",
    "lineage-graph",
    "operational-classification",
    "operator-experience-shell",
    "review-state-machine",
    "draft-and-publication-staging",
    "intake-and-routing-doctrines",
    "console-rendering-policies",
    "operator-history-substrate",
    "envelope-versioning",
    "publication-source-of-truth",
    "publication-trust-projection",
    "publication-pre-publication-gates",
    "publication-rollback-doctrine",
    "publication-rendering-doctrine",
    "publication-lifecycle-doctrine",
    "publication-deletion-doctrine",
    "publication-archival-doctrine",
    "publication-promotion-doctrine",
    "publication-naming-doctrine",
    "publication-supersedence-doctrine",
    "publication-traceability-doctrine",
    "publication-conflict-doctrine",
    "publication-rendering-language-doctrine",
    "publication-publishing-locality-doctrine",
    "publication-publishing-stamping-doctrine",
    "publication-publishing-evidence-doctrine",
    "publication-publishing-explanation-doctrine",
    "publication-publishing-coherence-doctrine",
    "publication-publishing-stability-doctrine",
    "publication-publishing-determinism-doctrine",
    "operator-cli-execution-doctrine",
    "executable-operational-bindings-governance",
    "governed-filesystem-orchestration-governance",
    "governed-transactional-execution-and-recovery-governance",
]

POSTURE_FLAGS = {
    "is_saas": False,
    "is_cloud": False,
    "daemon": False,
    "watcher": False,
    "scheduled_trigger": False,
    "autonomous_synthesis": False,
    "uses_llm": False,
    "uses_embeddings": False,
    "uses_ml": False,
    "probabilistic_inference": False,
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_publication_lineage": True,
    "publication_rollback_via_supersedence": True,
    "preserves_evidence_lineage": True,
    "preserves_trust_tiers": True,
    "preserves_source_attribution": True,
    "no_silent_evidence_merge": True,
    "no_auto_publication": True,
    "fail_closed_on_unresolved_conflict": True,
    "writes_to_live_publication_tree": False,
    "publishes_only_into_publication_builds": True,
}

MANUAL_SECTIONS = [
    "overview", "prerequisites", "installation", "operation",
    "troubleshooting", "maintenance", "specifications", "warnings",
    "support",
]

PUBLICATION_STATES = [
    "draft", "synthesized", "review-required", "reviewer-approved",
    "publication-ready", "superseded", "deprecated",
]
PUBLICATION_TERMINAL_STATES = {"superseded", "deprecated"}

PUBLICATION_TRANSITIONS = [
    ("draft", "synthesized"),
    ("synthesized", "review-required"),
    ("review-required", "reviewer-approved"),
    ("review-required", "draft"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
]

CONFLICT_CLASSES = [
    "trust-tier-mismatch",
    "specification-divergence",
    "warning-divergence",
    "procedure-divergence",
    "terminology-divergence",
    "identity-divergence",
    "evidence-recency-divergence",
    "scope-overlap-divergence",
]

OUTPUT_FORMATS = ["html", "json"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def envelope(extra: dict) -> dict:
    base = {
        "schema": SCHEMA,
        "constitutional_layer_index": LAYER,
        "subordinate_to": SUBORDINATE_TO,
        "generated_at_iso": now_iso(),
    }
    base.update(POSTURE_FLAGS)
    base.update(extra)
    return base


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists() and not any(path.iterdir()):
        keep.write_text("", encoding="utf-8")


# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

SYNTHESIS_RULES = envelope({
    "kind": "synthesis-rules",
    "summary": "Deterministic rules for assembling evidence into synthesis manifests.",
    "rules": [
        {"id": "SYN-1", "rule": "Synthesis MUST cite every contributing evidence_id."},
        {"id": "SYN-2", "rule": "Synthesis MUST preserve trust tier of each evidence fragment."},
        {"id": "SYN-3", "rule": "Synthesis MUST emit a reasoning_chain explaining inclusion of each fragment."},
        {"id": "SYN-4", "rule": "No fragment without explicit lineage may enter synthesis."},
        {"id": "SYN-5", "rule": "No probabilistic, ML or LLM-derived inference is permitted in synthesis."},
        {"id": "SYN-6", "rule": "Unresolved conflicts BLOCK synthesis advancement."},
        {"id": "SYN-7", "rule": "Synthesis manifests are append-only; revision yields a new manifest version."},
        {"id": "SYN-8", "rule": "Synthesis MUST declare the contributing manifests and reviewer attribution."},
    ],
})

PUBLICATION_GENERATION_RULES = envelope({
    "kind": "publication-generation-rules",
    "summary": "Deterministic rules for publication output generation.",
    "supported_outputs": OUTPUT_FORMATS,
    "rules": [
        {"id": "PUB-1", "rule": "Publication outputs are written ONLY under publication-builds/<build_id>/."},
        {"id": "PUB-2", "rule": "Publication generation NEVER overwrites the live publication tree."},
        {"id": "PUB-3", "rule": "HTML and JSON outputs MUST be byte-deterministic for identical inputs."},
        {"id": "PUB-4", "rule": "Every publication build MUST carry a publication_manifest.json with synthesis lineage."},
        {"id": "PUB-5", "rule": "Publication generation refuses to run if upstream synthesis state is not 'reviewer-approved'."},
        {"id": "PUB-6", "rule": "No external network call, no remote asset fetch, no cloud rendering."},
        {"id": "PUB-7", "rule": "Publication generation emits an append-only publication-build-event."},
    ],
})

MANUAL_ASSEMBLY_RULES = envelope({
    "kind": "manual-assembly-rules",
    "summary": "Section policy for canonical product manuals.",
    "sections": MANUAL_SECTIONS,
    "rules": [
        {"id": "MA-1", "rule": "Each section MUST declare its evidence_ids and contributing manifests."},
        {"id": "MA-2", "rule": "Empty sections MUST be marked 'evidence-not-available' rather than silently omitted."},
        {"id": "MA-3", "rule": "Specifications and warnings MUST flag 'unresolved-fields' explicitly."},
        {"id": "MA-4", "rule": "Sections MAY declare 'review-required' if any contributing evidence is below reviewer-approved trust."},
        {"id": "MA-5", "rule": "Manual assembly MUST preserve canonical_product_id and product version."},
        {"id": "MA-6", "rule": "No section may contain text without an evidence pointer or governance pointer."},
        {"id": "MA-7", "rule": "Reviewer attribution MUST be carried per-section and at the manual root."},
    ],
})

EVIDENCE_RESOLUTION_RULES = envelope({
    "kind": "evidence-resolution-rules",
    "summary": "Multi-source evidence reconciliation rules.",
    "conflict_classes": CONFLICT_CLASSES,
    "resolution_strategies": [
        "highest-trust-tier-wins (only if delta >= 1 tier)",
        "newest-evidence-wins (only within same trust tier)",
        "scope-narrowest-wins (for scope-overlap)",
        "reviewer-arbitration (for ties or contradictions)",
    ],
    "rules": [
        {"id": "ER-1", "rule": "Conflicts MUST be enumerated explicitly; no silent merge."},
        {"id": "ER-2", "rule": "Trust-tier ties REQUIRE reviewer arbitration."},
        {"id": "ER-3", "rule": "Contradiction (incompatible scalar values) BLOCKS publication until reviewer resolves."},
        {"id": "ER-4", "rule": "Each resolution emits a conflict-event with chosen strategy and reasoning_chain."},
        {"id": "ER-5", "rule": "No resolution strategy may discard evidence; superseded evidence remains in lineage."},
        {"id": "ER-6", "rule": "Unresolved ambiguity is flagged 'review-required'; downstream synthesis halts for affected fields."},
    ],
})

COLOMBIAN_RENDERING_RULES = envelope({
    "kind": "colombian-rendering-rules",
    "summary": "Deterministic Colombian Spanish operational rendering rules.",
    "rules": [
        {"id": "CR-1", "rule": "Apply canonical terminology mapping table; no synonym substitution outside the table."},
        {"id": "CR-2", "rule": "Procedural verbs MUST use the imperative second-person formal ('usted') by default."},
        {"id": "CR-3", "rule": "OEM-language artifacts (raw English fragments, untranslated unit phrases) MUST be flagged for reviewer."},
        {"id": "CR-4", "rule": "Numerical units MUST be normalized (mm, A, V, Hz, etc.); no conversion is performed silently."},
        {"id": "CR-5", "rule": "Brand and model identifiers are NEVER translated."},
        {"id": "CR-6", "rule": "Rendering preserves canonical evidence pointers; no text without provenance."},
        {"id": "CR-7", "rule": "Readability normalization is rule-based only (sentence length cap, voice pattern); no rewriting."},
        {"id": "CR-8", "rule": "Rendering emits a rendering-event recording all transformations applied."},
    ],
    "terminology_table": [
        {"oem": "lock", "canonical_es_co": "cerradura"},
        {"oem": "deadbolt", "canonical_es_co": "cerrojo"},
        {"oem": "strike", "canonical_es_co": "contraplaca"},
        {"oem": "fingerprint", "canonical_es_co": "huella dactilar"},
        {"oem": "rfid card", "canonical_es_co": "tarjeta RFID"},
        {"oem": "battery", "canonical_es_co": "batería"},
        {"oem": "low battery", "canonical_es_co": "batería baja"},
        {"oem": "factory reset", "canonical_es_co": "restablecimiento de fábrica"},
        {"oem": "user code", "canonical_es_co": "código de usuario"},
        {"oem": "master code", "canonical_es_co": "código maestro"},
        {"oem": "lockout", "canonical_es_co": "bloqueo temporal"},
    ],
})

TROUBLESHOOTING_SYNTHESIS_RULES = envelope({
    "kind": "troubleshooting-synthesis-rules",
    "summary": "Rules for assembling deterministic troubleshooting flows.",
    "rules": [
        {"id": "TS-1", "rule": "Each symptom MUST cite its evidence_ids."},
        {"id": "TS-2", "rule": "Root-cause grouping is permitted only when explicit lineage links symptoms."},
        {"id": "TS-3", "rule": "Escalation steps MUST cite the support/escalation manifest."},
        {"id": "TS-4", "rule": "Warnings MUST be integrated, not duplicated; cross-references are explicit."},
        {"id": "TS-5", "rule": "Continuity-aware reasoning preserves canonical_product_id across the flow."},
        {"id": "TS-6", "rule": "Flows MUST declare confidence_state per step (reviewer-approved | review-required | unresolved)."},
        {"id": "TS-7", "rule": "Unresolved ambiguity MUST be carried forward, not flattened."},
    ],
})

SPECIFICATION_SYNTHESIS_RULES = envelope({
    "kind": "specification-synthesis-rules",
    "summary": "Rules for assembling specification sheets and matrices.",
    "ontology_axes": [
        "dimensional", "connectivity", "authentication",
        "certification", "operational-limits", "power",
    ],
    "rules": [
        {"id": "SP-1", "rule": "Every spec field MUST cite evidence_id and trust_tier."},
        {"id": "SP-2", "rule": "Speculative or interpolated values are FORBIDDEN."},
        {"id": "SP-3", "rule": "Unresolved fields MUST be marked 'unresolved' (not omitted, not estimated)."},
        {"id": "SP-4", "rule": "Connectivity and authentication matrices MUST cite per-cell evidence."},
        {"id": "SP-5", "rule": "Certification rows MUST carry document reference and issuer attribution."},
        {"id": "SP-6", "rule": "Conflicts in dimensional fields BLOCK the spec sheet until reviewer arbitration."},
    ],
})

PUBLICATION_LIFECYCLE_RULES = envelope({
    "kind": "publication-lifecycle-rules",
    "summary": "Reviewer-governed publication state machine.",
    "states": PUBLICATION_STATES,
    "terminal_states": sorted(PUBLICATION_TERMINAL_STATES),
    "transitions": [{"from": a, "to": b} for a, b in PUBLICATION_TRANSITIONS],
    "rules": [
        {"id": "PL-1", "rule": "Reviewer attribution is required on every transition."},
        {"id": "PL-2", "rule": "publication-ready REQUIRES a prior reviewer-approved transition with reasoning_chain."},
        {"id": "PL-3", "rule": "No silent regeneration; every regeneration is a new build_id with explicit supersedence."},
        {"id": "PL-4", "rule": "Rollback is achieved via 'superseded' (publication-ready -> superseded), never via overwrite."},
        {"id": "PL-5", "rule": "Append-only publication-lifecycle-events store every transition."},
        {"id": "PL-6", "rule": "Terminal states (superseded, deprecated) are immutable."},
        {"id": "PL-7", "rule": "Conflict-blocked synthesis CANNOT advance past 'review-required'."},
    ],
})

RULE_TABLES = {
    "synthesis-rules.json": SYNTHESIS_RULES,
    "publication-generation-rules.json": PUBLICATION_GENERATION_RULES,
    "manual-assembly-rules.json": MANUAL_ASSEMBLY_RULES,
    "evidence-resolution-rules.json": EVIDENCE_RESOLUTION_RULES,
    "colombian-rendering-rules.json": COLOMBIAN_RENDERING_RULES,
    "troubleshooting-synthesis-rules.json": TROUBLESHOOTING_SYNTHESIS_RULES,
    "specification-synthesis-rules.json": SPECIFICATION_SYNTHESIS_RULES,
    "publication-lifecycle-rules.json": PUBLICATION_LIFECYCLE_RULES,
}


# ---------------------------------------------------------------------------
# Event stores (append-only)
# ---------------------------------------------------------------------------

NEW_EVENT_STORES = [
    "synthesis-events",
    "publication-build-events",
    "evidence-resolution-events",
    "conflict-events",
    "rendering-events",
    "publication-lifecycle-events",
]


def build_runtime_event_stores() -> int:
    created = 0
    for kind in NEW_EVENT_STORES:
        store_path = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        if store_path.exists():
            continue
        write_json(store_path, {
            "schema": "governed-fs-event-store/1.0",
            "constitutional_layer_index": LAYER,
            "kind": kind,
            "append_only": True,
            "deterministic": True,
            "reviewer_authoritative": True,
            "created_at": now_iso(),
            "events": [],
        })
        created += 1
    return created


def build_storage_roots() -> int:
    SYNTHESIS_DRAFTS_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLICATION_BUILDS_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(SYNTHESIS_DRAFTS_ROOT / "README.md",
               "# synthesis-drafts/\n\nAppend-only synthesis manifests written by "
               "`tools/governed_knowledge_synthesis_executor.py --kind synthesis --confirm`.\n"
               "Never overwritten. Each manifest carries evidence_ids, trust composition, "
               "reviewer attribution, and a reasoning chain.\n")
    write_text(PUBLICATION_BUILDS_ROOT / "README.md",
               "# publication-builds/\n\nDeterministic publication outputs (HTML + JSON) "
               "written by `tools/governed_knowledge_synthesis_executor.py --kind publication-build --confirm`.\n"
               "Never overlap with the live publication tree. Each build sits under a unique build_id.\n")
    for sub in ("draft", "review-required", "reviewer-approved", "publication-ready",
                "superseded", "deprecated"):
        ensure_dir(PUBLICATION_BUILDS_ROOT / sub)
    return 1


# ---------------------------------------------------------------------------
# JS engines (browser only — never write FS)
# ---------------------------------------------------------------------------

JS_HEADER = """// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.
"""

SYNTHESIS_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.SynthesisEngine = (function () {
  function buildSynthesisRequest({ canonical_product_id, evidence_ids, contributing_manifests,
                                   trust_composition, reasoning_chain, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!Array.isArray(evidence_ids) || evidence_ids.length === 0)
      throw new Error("SYN-1: at least one evidence_id required");
    if (!reviewer) throw new Error("synthesis requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "synthesis",
      reviewer: reviewer,
      payload: {
        synthesis_id: "syn-" + canonical_product_id + "-" + Date.now(),
        canonical_product_id: canonical_product_id,
        evidence_ids: evidence_ids.slice(),
        contributing_manifests: (contributing_manifests || []).slice(),
        trust_composition: trust_composition || {},
        reasoning_chain: reasoning_chain || [],
        deterministic: true,
        no_llm: true,
      },
    });
  }
  return { buildSynthesisRequest: buildSynthesisRequest };
})();
"""

PUBLICATION_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.PublicationEngine = (function () {
  function buildPublicationBuildRequest({ synthesis_id, output_formats, manual_id, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!synthesis_id) throw new Error("PUB-5: synthesis_id required");
    if (!reviewer) throw new Error("publication build requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "publication-build",
      reviewer: reviewer,
      payload: {
        build_id: "pubb-" + manual_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        manual_id: manual_id,
        output_formats: (output_formats || ["html", "json"]).slice(),
        writes_live_tree: false,
        deterministic: true,
      },
    });
  }
  return { buildPublicationBuildRequest: buildPublicationBuildRequest };
})();
"""

MANUAL_ASSEMBLY_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.ManualAssemblyEngine = (function () {
  var SECTIONS = ["overview","prerequisites","installation","operation",
                  "troubleshooting","maintenance","specifications","warnings","support"];
  function buildAssemblyRequest({ manual_id, canonical_product_id, sections, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("manual assembly requires reviewer attribution");
    var normalized = {};
    SECTIONS.forEach(function (s) {
      var src = (sections && sections[s]) || {};
      normalized[s] = {
        evidence_ids: (src.evidence_ids || []).slice(),
        contributing_manifests: (src.contributing_manifests || []).slice(),
        trust_composition: src.trust_composition || {},
        text_pointer: src.text_pointer || null,
        review_state: src.review_state || (src.evidence_ids && src.evidence_ids.length
                                           ? "draft" : "evidence-not-available"),
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "manual-assembly",
      reviewer: reviewer,
      payload: {
        manual_id: manual_id,
        canonical_product_id: canonical_product_id,
        sections: normalized,
        section_count: SECTIONS.length,
      },
    });
  }
  return { buildAssemblyRequest: buildAssemblyRequest, SECTIONS: SECTIONS };
})();
"""

EVIDENCE_RESOLUTION_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.EvidenceResolutionEngine = (function () {
  var CLASSES = ["trust-tier-mismatch","specification-divergence","warning-divergence",
                 "procedure-divergence","terminology-divergence","identity-divergence",
                 "evidence-recency-divergence","scope-overlap-divergence"];
  function detectConflict(fragmentA, fragmentB) {
    if (!fragmentA || !fragmentB) return null;
    if (fragmentA.canonical_product_id && fragmentB.canonical_product_id &&
        fragmentA.canonical_product_id !== fragmentB.canonical_product_id)
      return { conflict_class: "identity-divergence", a: fragmentA.id, b: fragmentB.id };
    if (fragmentA.field === fragmentB.field && fragmentA.value !== fragmentB.value) {
      if ((fragmentA.trust_tier || "") === (fragmentB.trust_tier || ""))
        return { conflict_class: "specification-divergence", a: fragmentA.id, b: fragmentB.id,
                 reason: "same trust tier, divergent value" };
      return { conflict_class: "trust-tier-mismatch", a: fragmentA.id, b: fragmentB.id };
    }
    return null;
  }
  function buildResolutionRequest({ synthesis_id, conflicts, strategy, reviewer, reasoning_chain }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("resolution requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "evidence-resolve",
      reviewer: reviewer,
      payload: {
        resolution_id: "res-" + synthesis_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        conflicts: (conflicts || []).slice(),
        strategy: strategy || "reviewer-arbitration",
        reasoning_chain: reasoning_chain || [],
      },
    });
  }
  return { detectConflict: detectConflict, buildResolutionRequest: buildResolutionRequest, CLASSES: CLASSES };
})();
"""

COLOMBIAN_RENDERING_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.ColombianRenderingEngine = (function () {
  var TERM_TABLE = [
    ["lock","cerradura"],["deadbolt","cerrojo"],["strike","contraplaca"],
    ["fingerprint","huella dactilar"],["rfid card","tarjeta RFID"],
    ["battery","batería"],["low battery","batería baja"],
    ["factory reset","restablecimiento de fábrica"],
    ["user code","código de usuario"],["master code","código maestro"],
    ["lockout","bloqueo temporal"],
  ];
  function applyTerminology(text) {
    if (typeof text !== "string") return { text: text, transformations: [] };
    var transformations = [];
    var out = text;
    TERM_TABLE.forEach(function (pair) {
      var rx = new RegExp("\\\\b" + pair[0] + "\\\\b", "gi");
      if (rx.test(out)) {
        out = out.replace(rx, pair[1]);
        transformations.push({ rule: "CR-1", from: pair[0], to: pair[1] });
      }
    });
    return { text: out, transformations: transformations };
  }
  function buildRenderingRequest({ synthesis_id, segments, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("rendering requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "rendering",
      reviewer: reviewer,
      payload: {
        rendering_id: "ren-" + synthesis_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        target_locale: "es-CO",
        segments: (segments || []).slice(),
      },
    });
  }
  return { applyTerminology: applyTerminology, buildRenderingRequest: buildRenderingRequest };
})();
"""

TROUBLESHOOTING_SYNTHESIS_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.TroubleshootingSynthesisEngine = (function () {
  function buildFlowRequest({ synthesis_id, canonical_product_id, symptoms, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("troubleshooting synthesis requires reviewer attribution");
    var steps = (symptoms || []).map(function (s, i) {
      return {
        step_id: "ts-" + i,
        symptom: s.symptom,
        evidence_ids: (s.evidence_ids || []).slice(),
        candidate_root_causes: (s.candidate_root_causes || []).slice(),
        confidence_state: s.confidence_state || "review-required",
        unresolved: !!s.unresolved,
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "troubleshooting-synthesis",
      reviewer: reviewer,
      payload: {
        flow_id: "ts-" + canonical_product_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        canonical_product_id: canonical_product_id,
        steps: steps,
      },
    });
  }
  return { buildFlowRequest: buildFlowRequest };
})();
"""

SPECIFICATION_SYNTHESIS_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.SpecificationSynthesisEngine = (function () {
  var AXES = ["dimensional","connectivity","authentication","certification","operational-limits","power"];
  function buildSpecRequest({ synthesis_id, canonical_product_id, fields, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("specification synthesis requires reviewer attribution");
    var normalized = (fields || []).map(function (f) {
      return {
        axis: f.axis,
        key: f.key,
        value: f.value,
        evidence_id: f.evidence_id || null,
        trust_tier: f.trust_tier || null,
        unresolved: f.value === undefined || f.value === null || f.value === "",
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "specification-synthesis",
      reviewer: reviewer,
      payload: {
        spec_id: "spec-" + canonical_product_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        canonical_product_id: canonical_product_id,
        fields: normalized,
      },
    });
  }
  return { AXES: AXES, buildSpecRequest: buildSpecRequest };
})();
"""

PUBLICATION_LIFECYCLE_ENGINE_JS = JS_HEADER + """
window.OC = window.OC || {};
window.OC.PublicationLifecycleEngine = (function () {
  var STATES = ["draft","synthesized","review-required","reviewer-approved",
                "publication-ready","superseded","deprecated"];
  var EDGES = [["draft","synthesized"],["synthesized","review-required"],
               ["review-required","reviewer-approved"],["review-required","draft"],
               ["reviewer-approved","publication-ready"],["reviewer-approved","review-required"],
               ["publication-ready","superseded"],["publication-ready","deprecated"],
               ["superseded","deprecated"]];
  function isLegal(from, to) {
    return EDGES.some(function (e) { return e[0] === from && e[1] === to; });
  }
  function buildTransitionRequest({ build_id, from_state, to_state, reviewer, reasoning_chain }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("transition requires reviewer attribution");
    if (!isLegal(from_state, to_state))
      throw new Error("PL: illegal transition " + from_state + " -> " + to_state);
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "publication-lifecycle-transition",
      reviewer: reviewer,
      payload: {
        transition_id: "plt-" + build_id + "-" + Date.now(),
        build_id: build_id,
        from_state: from_state,
        to_state: to_state,
        reasoning_chain: reasoning_chain || [],
      },
    });
  }
  return { STATES: STATES, isLegal: isLegal, buildTransitionRequest: buildTransitionRequest };
})();
"""

JS_ENGINES = {
    "synthesis-engine.js": SYNTHESIS_ENGINE_JS,
    "publication-engine.js": PUBLICATION_ENGINE_JS,
    "manual-assembly-engine.js": MANUAL_ASSEMBLY_ENGINE_JS,
    "evidence-resolution-engine.js": EVIDENCE_RESOLUTION_ENGINE_JS,
    "colombian-rendering-engine.js": COLOMBIAN_RENDERING_ENGINE_JS,
    "troubleshooting-synthesis-engine.js": TROUBLESHOOTING_SYNTHESIS_ENGINE_JS,
    "specification-synthesis-engine.js": SPECIFICATION_SYNTHESIS_ENGINE_JS,
    "publication-lifecycle-engine.js": PUBLICATION_LIFECYCLE_ENGINE_JS,
}

CSS_ADDENDUM = """
/* phase 48 — governed knowledge synthesis & canonical publication additions */
.oc-synth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.oc-synth-card { border: 1px solid var(--oc-border, #d0d7de); border-radius: 8px; padding: 10px; background: #fff; }
.oc-pub-state { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600;
  background: #f6f8fa; color: #1f2328; border: 1px solid #d0d7de; }
.oc-pub-state[data-state="reviewer-approved"] { background: #dafbe1; color: #14532d; border-color: #86efac; }
.oc-pub-state[data-state="publication-ready"] { background: #dbeafe; color: #1e3a8a; border-color: #93c5fd; }
.oc-pub-state[data-state="superseded"], .oc-pub-state[data-state="deprecated"] { background: #fee2e2; color: #7f1d1d; border-color: #fca5a5; }
.oc-conflict { background: #fff7ed; border-left: 4px solid #ea580c; padding: 8px 10px; margin: 6px 0; }
.oc-evidence-pin { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: #475569; }
"""


def build_assets() -> int:
    ASSETS_ROOT.mkdir(parents=True, exist_ok=True)
    written = 0
    for name, body in JS_ENGINES.items():
        write_text(ASSETS_ROOT / name, body)
        written += 1

    css_path = ASSETS_ROOT / "exec.css"
    marker = "/* phase 48 — governed knowledge synthesis & canonical publication additions */"
    existing = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    if marker not in existing:
        write_text(css_path, existing + CSS_ADDENDUM)
        written += 1
    return written


# ---------------------------------------------------------------------------
# HTML consoles
# ---------------------------------------------------------------------------

def _html_head(title: str) -> str:
    return f"""<!doctype html><html lang=\"es-CO\"><head>
<meta charset=\"utf-8\"><title>{title}</title>
<link rel=\"stylesheet\" href=\"../assets/exec/exec.css\">
</head><body>
<header><h1>{title}</h1>
<p class=\"oc-meta\">Layer 41 — governed knowledge synthesis &amp; canonical publication generation. Browser builds envelopes only; the CLI executor is the only writer.</p>
</header>
<main>
"""

HTML_TAIL = """
</main>
<script src="../assets/exec/fs-bridge.js"></script>
<script src="../assets/exec/dest-resolver.js"></script>
<script src="../assets/exec/transaction-engine.js"></script>
<script src="../assets/exec/snapshot-engine.js"></script>
<script src="../assets/exec/synthesis-engine.js"></script>
<script src="../assets/exec/publication-engine.js"></script>
<script src="../assets/exec/manual-assembly-engine.js"></script>
<script src="../assets/exec/evidence-resolution-engine.js"></script>
<script src="../assets/exec/colombian-rendering-engine.js"></script>
<script src="../assets/exec/troubleshooting-synthesis-engine.js"></script>
<script src="../assets/exec/specification-synthesis-engine.js"></script>
<script src="../assets/exec/publication-lifecycle-engine.js"></script>
</body></html>
"""

CONSOLES = {
    "synthesis-console": ("Synthesis console",
        "<section><h2>Build a synthesis envelope</h2>"
        "<p>Select evidence ids, declare contributing manifests, attribute the reviewer, "
        "and export a <code>governed-fs-operation-request/1.0</code> envelope. The browser does NOT write.</p>"
        "<ul><li>SYN-1: every evidence_id is cited.</li><li>SYN-5: no LLM, no ML, no embeddings.</li>"
        "<li>SYN-6: unresolved conflicts block synthesis.</li></ul></section>"),
    "publication-console": ("Publication build console",
        "<section><h2>Request a deterministic publication build</h2>"
        "<p>Builds land under <code>operational-console/publication-builds/&lt;build_id&gt;/</code>. "
        "Live publication tree is never overwritten. HTML + JSON only; no PDF.</p></section>"),
    "manual-assembly-console": ("Manual assembly console",
        "<section><h2>Compose a 9-section canonical manual</h2>"
        "<p>Sections: overview, prerequisites, installation, operation, troubleshooting, maintenance, "
        "specifications, warnings, support. Empty sections are explicitly marked "
        "<em>evidence-not-available</em>.</p></section>"),
    "evidence-resolution-console": ("Evidence resolution console",
        "<section><h2>Resolve multi-source conflicts</h2>"
        "<p>Conflicts are enumerated explicitly. No silent merge. "
        "Trust-tier ties and contradictions require reviewer arbitration.</p></section>"),
    "rendering-console": ("Colombian rendering console",
        "<section><h2>Deterministic Spanish (Colombia) rendering</h2>"
        "<p>Rule-based terminology table. No machine translation. No silent rewriting. "
        "OEM-language artifacts are flagged for reviewer.</p></section>"),
    "publication-lifecycle-console": ("Publication lifecycle console",
        "<section><h2>Reviewer-governed publication state machine</h2>"
        "<p>States: draft &rarr; synthesized &rarr; review-required &rarr; reviewer-approved "
        "&rarr; publication-ready &rarr; (superseded | deprecated). "
        "Rollback = supersedence; never overwrite.</p></section>"),
}


def build_consoles() -> int:
    written = 0
    for slug, (title, body) in CONSOLES.items():
        path = OC_ROOT / slug / "exec.html"
        write_text(path, _html_head(title) + body + HTML_TAIL)
        written += 1
    return written


# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = [
    ("01-deterministic-synthesis-only-doctrine.md",
     "Synthesis is deterministic and rule-based. No LLM, no ML, no embeddings, no probabilistic inference."),
    ("02-evidence-lineage-preservation-doctrine.md",
     "Every synthesized output preserves evidence_ids, contributing manifests, trust composition, and reviewer attribution."),
    ("03-no-silent-evidence-merge-doctrine.md",
     "Conflicts are enumerated explicitly. No fragment is silently dropped or fused."),
    ("04-canonical-terminology-preservation-doctrine.md",
     "Colombian rendering uses a deterministic terminology table. Brand and model identifiers are never translated."),
    ("05-fail-closed-on-unresolved-conflict-doctrine.md",
     "Unresolved conflicts BLOCK publication advancement until reviewer arbitration."),
    ("06-no-auto-publication-doctrine.md",
     "Publication advancement requires explicit reviewer transitions. No silent regeneration."),
    ("07-publication-rollback-via-supersedence-doctrine.md",
     "Rollback is achieved by transitioning publication-ready -> superseded with append-only lineage. Live tree is never overwritten."),
    ("08-publication-builds-isolated-from-live-tree-doctrine.md",
     "All generated outputs live under operational-console/publication-builds/<build_id>/. The live publication tree is untouched."),
    ("09-append-only-publication-lineage-doctrine.md",
     "Every synthesis, build, resolution, rendering, and lifecycle transition appends an event. Nothing is mutated in place."),
    ("10-cli-only-no-daemon-doctrine.md",
     "Browser surfaces only build envelopes. The CLI executor with --confirm is the only writer. No daemon, no watcher, no scheduler."),
]


def build_doctrines() -> int:
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(KB_ROOT / "00-INDEX.md",
               "# GOVERNED_KNOWLEDGE_SYNTHESIS_GOVERNANCE\n\n"
               "Layer 41. Subordinate to layer 40 (governed transactional execution & recovery).\n\n"
               + "\n".join(f"- [{name}]({name})" for name, _ in DOCTRINES) + "\n")
    for name, body in DOCTRINES:
        write_text(KB_ROOT / name,
                   f"# {name.replace('.md','').replace('-',' ')}\n\n{body}\n\n"
                   f"Layer index: {LAYER}.\n")
    write_json(KB_ROOT / "manifest.json", envelope({
        "doctrine_set": "GOVERNED_KNOWLEDGE_SYNTHESIS_GOVERNANCE",
        "doctrine_count": len(DOCTRINES),
        "doctrines": [name for name, _ in DOCTRINES],
    }))
    return len(DOCTRINES)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORT_PHASES = [
    ("39", "Governed knowledge synthesis & canonical publication generation",
     "phase 48 → layer 41 (this phase)"),
]

REPORTS = [
    ("01-synthesis-engine-summary",
     "Deterministic synthesis engine over evidence fragments; preserves lineage, trust tiers, reviewer attribution."),
    ("02-canonical-publication-summary",
     "Deterministic HTML + JSON publication generation under publication-builds/<build_id>/."),
    ("03-manual-assembly-summary",
     "Nine-section canonical manual assembly with per-section evidence provenance and trust composition."),
    ("04-multi-source-resolution-summary",
     "Explicit conflict enumeration across 8 conflict classes; reviewer-arbitrated resolution; no silent merge."),
    ("05-colombian-rendering-summary",
     "Rule-based Spanish (Colombia) terminology + procedural tone + readability normalization. No machine translation."),
    ("06-troubleshooting-synthesis-summary",
     "Symptom aggregation, root-cause grouping, escalation integration, continuity-aware confidence per step."),
    ("07-specification-synthesis-summary",
     "Specifications across 6 ontology axes; per-field evidence + trust + unresolved-flag; no speculation."),
    ("08-publication-lifecycle-summary",
     "Reviewer-governed state machine (7 states); reviewer attribution + reasoning chain on every transition."),
    ("09-synthesis-visibility-summary",
     "Six exec consoles for synthesis, publication, manual assembly, conflict resolution, rendering, and lifecycle."),
    ("10-governed-publication-platform-maturity-reassessment",
     "Maturity reassessment after Phase 48: ecosystem now produces canonical, reviewer-governed publications deterministically."),
]


def build_reports() -> int:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(REPORTS_ROOT / "README.md",
               "# governed-knowledge-synthesis reports\n\n"
               "Phase 48 / layer 41 reports. Each .md is a short brief; each .json is the structured envelope.\n")
    for slug, summary in REPORTS:
        write_text(REPORTS_ROOT / f"{slug}.md",
                   f"# {slug}\n\n{summary}\n\nLayer: {LAYER}. Subordinate chain length: {len(SUBORDINATE_TO)}.\n")
        write_json(REPORTS_ROOT / f"{slug}.json", envelope({
            "report_id": slug,
            "summary": summary,
            "layer_history": REPORT_PHASES,
            "rule_tables": list(RULE_TABLES.keys()),
            "doctrines": [name for name, _ in DOCTRINES],
            "event_stores": NEW_EVENT_STORES,
            "manual_sections": MANUAL_SECTIONS,
            "publication_states": PUBLICATION_STATES,
            "conflict_classes": CONFLICT_CLASSES,
            "supported_outputs": OUTPUT_FORMATS,
        }))
    return len(REPORTS)


# ---------------------------------------------------------------------------
# Rule-table emitter
# ---------------------------------------------------------------------------

def build_rule_tables() -> int:
    RULES_ROOT.mkdir(parents=True, exist_ok=True)
    for name, payload in RULE_TABLES.items():
        write_json(RULES_ROOT / name, payload)
    return len(RULE_TABLES)


# ---------------------------------------------------------------------------
# Runtime README addendum (idempotent via marker)
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 48 — governed knowledge synthesis & canonical publication generation"

RUNTIME_README_ADDENDUM = f"""

{RUNTIME_README_MARKER}

Layer 41. Subordinate to layer 40.

Reviewer flow:
1. Open the synthesis console; pick evidence_ids; export an envelope.
2. Run `python3 tools/governed_knowledge_synthesis_executor.py --kind synthesis --request <file> --confirm`.
3. Inspect the synthesis manifest in `operational-console/synthesis-drafts/`.
4. Resolve any conflicts via the evidence-resolution console + `--kind evidence-resolve --confirm`.
5. Approve the synthesis (publication-lifecycle: draft → synthesized → review-required → reviewer-approved).
6. Build the publication: `--kind publication-build --confirm`. Outputs land under `operational-console/publication-builds/<build_id>/` (HTML + JSON).
7. Transition the build to `publication-ready`; rollback is achieved by superseding, never by overwrite.

Hard rules:
- No LLM, no ML, no embeddings.
- No silent evidence merge; every conflict is explicit.
- Live publication tree is never overwritten by this layer.
- All transitions are append-only and reviewer-attributed.
"""


def build_runtime_readme_addendum() -> int:
    path = OC_ROOT / "RUNTIME_README.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if RUNTIME_README_MARKER in existing:
        return 0
    write_text(path, existing + RUNTIME_README_ADDENDUM)
    return 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    storage = build_storage_roots()
    stores_created = build_runtime_event_stores()
    rules = build_rule_tables()
    assets = build_assets()
    consoles = build_consoles()
    doctrines = build_doctrines()
    reports = build_reports()
    readme = build_runtime_readme_addendum()
    print(
        f"Phase 48 — governed knowledge synthesis & canonical publication generation written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores_created} | "
        f"Rule tables: {rules} | JS assets: {assets} | Exec consoles: {consoles} | "
        f"Doctrines: {doctrines} | Reports: {reports} | RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
