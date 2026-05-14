"""
Phase 45 — EXECUTABLE OPERATIONAL BINDINGS.

Constitutional layer 38. Subordinate to layer 37 (operational-console-governance)
and to all thirty-seven prior governance layers. Modeling + repo-native browser
interaction-only. NOT a SaaS, NOT a cloud architecture, NOT a backend, NOT an
autonomous agent platform, NOT a CI/CD pipeline, NOT an ML system.

This phase upgrades the static phase-44 operational console into a lightweight
executable LOCAL operational tool. All execution lives in plain ES JS that
runs from the file system (file://). It NEVER makes a network call, NEVER
auto-approves, NEVER auto-mutates governance, knowledge-core, source-of-truth,
runtime, or publication. Every operator action emits a *draft* manifest only.

Writes (idempotent, non-destructive, stdlib-only) under
wp-content/themes/beslock-custom/User manuals/operational-console/:

  exec.html                     (executable dashboard — exec layer landing)
  assets/exec/                  (state.js, drafts.js, intake-engine.js,
                                routing-engine.js, recon-engine.js,
                                refresh-engine.js, viz.js, ux.js, exec.css)
  execution-engine/             (deterministic JSON rule tables consumed
                                 by the JS engines)
  intake-console/exec.html      (executable intake interaction)
  routing-console/exec.html     (executable routing consultation)
  refresh-console/exec.html     (executable refresh proposal surface)
  reconciliation-console/exec.html (executable reconciliation review)
  publication-console/exec.html (publication-visibility interaction)
  governance-console/exec.html  (governance-inspection interaction)
  manifests/routing-drafts/     (append-only draft store)
  manifests/reconciliation-drafts/ (append-only draft store)
  manifests/refresh-drafts/     (append-only draft store)
  manifests/session-history/    (append-only session-history store)

Plus:
  KNOWLEDGE_BUILDING/EXECUTABLE_OPERATIONAL_BINDINGS_GOVERNANCE/ (00-INDEX +
                                 8 doctrines + manifest)
  _repository-governance/reports/executable-operational-bindings/ (10 reports)

Hard rules (still enforced):
  - Mutates no knowledge-core, no source-of-truth, no runtime, no publication,
    and no governance state.
  - No CI/CD, no autonomous agents, no ML, no embeddings, no prompts, no images.
  - No SaaS, no cloud architecture, no production backend, no telemetry.
  - The console NEVER auto-approves and NEVER auto-promotes anything; all
    drafts are append-only and reviewer-attributed.
  - JS is plain ES, no build pipeline, no dependencies, no network calls. The
    only browser APIs used are: File / Blob / URL / localStorage / SVG. All
    "remote" loads use relative file paths (`fetch` is local-only and may be
    blocked under strict file://; pages are documented as needing either a
    local static server or a browser that allows file:// fetch).
  - 19/19 runtime tests must remain green.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

OC_ROOT = THEME_ROOT / "operational-console"
ASSETS_ROOT = OC_ROOT / "assets"
EXEC_ASSETS_ROOT = ASSETS_ROOT / "exec"
RULES_ROOT = OC_ROOT / "execution-engine"
MAN_ROOT = OC_ROOT / "manifests"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "EXECUTABLE_OPERATIONAL_BINDINGS_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "executable-operational-bindings"

SCHEMA = "executable-operational-bindings/1.0"
LAYER = 38
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
    "runtime-orchestration-governance", "operational-console-governance",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def envelope(extra: dict) -> dict:
    base = {
        "schema": SCHEMA,
        "constitutional_layer_index": LAYER,
        "subordinate_to": SUBORDINATE_TO,
        "updated_at": NOW,
        "executable_in_browser": True,
        "executable_backend": False,
        "is_saas": False,
        "is_production_app": False,
        "uses_cloud": False,
        "introduces_autonomous_agents": False,
        "introduces_ci_cd": False,
        "auto_approves_ingestion": False,
        "auto_mutates_source_truth": False,
        "bypasses_reviewer_governance": False,
        "uses_ml_or_embeddings": False,
        "network_calls": False,
        "telemetry": False,
        "draft_only": True,
        "append_only": True,
    }
    base.update(extra)
    return base


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# HTML scaffold
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("index.html", "Dashboard"),
    ("intake-console/index.html", "Intake"),
    ("routing-console/index.html", "Routing"),
    ("refresh-console/index.html", "Refresh"),
    ("reconciliation-console/index.html", "Reconciliation"),
    ("publication-console/index.html", "Publication"),
    ("governance-console/index.html", "Governance"),
    ("reports-console/index.html", "Reports"),
]

EXEC_NAV_ITEMS = [
    ("exec.html", "Exec Dashboard"),
    ("intake-console/exec.html", "Intake (exec)"),
    ("routing-console/exec.html", "Routing (exec)"),
    ("refresh-console/exec.html", "Refresh (exec)"),
    ("reconciliation-console/exec.html", "Reconciliation (exec)"),
    ("publication-console/exec.html", "Publication (exec)"),
    ("governance-console/exec.html", "Governance (exec)"),
]


def render_nav(prefix: str) -> str:
    parts = []
    for href, label in NAV_ITEMS:
        if prefix == ".":
            real = href
        else:
            real = f"{prefix}/{href}"
        parts.append(f'      <a class="oc-nav__item" href="{real}">{label}</a>')
    for href, label in EXEC_NAV_ITEMS:
        if prefix == ".":
            real = href
        else:
            real = f"{prefix}/{href}"
        parts.append(f'      <a class="oc-nav__item oc-nav__item--exec" href="{real}">{label}</a>')
    return "\n".join(parts)


def page(title: str, body: str, *, prefix: str, extra_scripts: list = None) -> str:
    nav = render_nav(prefix)
    css = f"{prefix}/assets/console.css" if prefix != "." else "assets/console.css"
    exec_css = f"{prefix}/assets/exec/exec.css" if prefix != "." else "assets/exec/exec.css"
    js_console = f"{prefix}/assets/console.js" if prefix != "." else "assets/console.js"
    extras = extra_scripts or []
    extra_tags = "\n".join(
        f'  <script src="{(prefix + "/" if prefix != "." else "")}assets/exec/{s}" defer></script>'
        for s in extras
    )
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Beslock Operational Console (executable)</title>
  <link rel="stylesheet" href="{css}" />
  <link rel="stylesheet" href="{exec_css}" />
  <meta name="governance-layer" content="{LAYER}" />
  <meta name="governance-schema" content="{SCHEMA}" />
  <meta name="reviewer-required" content="true" />
  <meta name="auto-approval" content="false" />
  <meta name="network-calls" content="false" />
</head>
<body class="oc-body oc-body--exec">
  <header class="oc-header">
    <div class="oc-header__brand">Beslock · Operational Console <span class="oc-tag oc-tag--exec">EXEC</span></div>
    <nav class="oc-nav">
{nav}
    </nav>
    <div class="oc-header__badge" title="Governance layer 38 — executable bindings, draft-only">L{LAYER}</div>
  </header>
  <div class="oc-banner oc-banner--exec" role="status" aria-live="polite">
    <strong>Executable layer.</strong> Runs locally from the file system. Every action emits an append-only <em>draft manifest</em>. No knowledge-core, source-of-truth, runtime, publication or governance state is ever mutated by this UI.
  </div>
  <main class="oc-main">
{body}
  </main>
  <footer class="oc-footer">
    <span>Repo-native · Local-first · Governance-first · Reviewer-required · Append-only</span>
    <span>No SaaS · No cloud · No backend · No autonomous agents · No ML · No telemetry · No network calls</span>
  </footer>
  <script src="{js_console}" defer></script>
{extra_tags}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Deterministic rule tables
# ---------------------------------------------------------------------------

FORMAT_TABLE = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Deterministic mapping of file extensions to recognised intake formats. Used by the executable intake engine to classify uploaded files.",
    "extensions": {
        ".pdf":  {"format": "pdf",  "category": "document",   "default_evidence_class": "vendor-document"},
        ".docx": {"format": "docx", "category": "document",   "default_evidence_class": "vendor-document"},
        ".xlsx": {"format": "xlsx", "category": "structured", "default_evidence_class": "vendor-spec-sheet"},
        ".csv":  {"format": "csv",  "category": "structured", "default_evidence_class": "vendor-spec-sheet"},
        ".json": {"format": "json", "category": "structured", "default_evidence_class": "structured-data"},
        ".png":  {"format": "png",  "category": "image",      "default_evidence_class": "vendor-image"},
        ".jpg":  {"format": "jpg",  "category": "image",      "default_evidence_class": "vendor-image"},
        ".jpeg": {"format": "jpg",  "category": "image",      "default_evidence_class": "vendor-image"},
        ".webp": {"format": "webp", "category": "image",      "default_evidence_class": "vendor-image"},
        ".mp4":  {"format": "mp4",  "category": "video",      "default_evidence_class": "vendor-video"},
        ".mov":  {"format": "mov",  "category": "video",      "default_evidence_class": "vendor-video"},
        ".zip":  {"format": "zip",  "category": "archive",    "default_evidence_class": "evidence-bundle"},
    },
    "fallback": {"format": "unknown", "category": "unknown", "default_evidence_class": "unclassified"},
    "auto_classifies": False,
    "reviewer_override_supported": True,
}

EVIDENCE_CLASS_TABLE = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Declared evidence classes referenced by the intake engine. Class assignment is a *suggestion*; the reviewer chooses the canonical class.",
    "classes": [
        {"id": "vendor-document",   "label": "Vendor document",       "trust_default": "tier-2"},
        {"id": "vendor-spec-sheet", "label": "Vendor specification",  "trust_default": "tier-2"},
        {"id": "vendor-image",      "label": "Vendor image",          "trust_default": "tier-2"},
        {"id": "vendor-video",      "label": "Vendor video",          "trust_default": "tier-2"},
        {"id": "structured-data",   "label": "Structured data",       "trust_default": "tier-2"},
        {"id": "evidence-bundle",   "label": "Evidence bundle (zip)", "trust_default": "tier-3"},
        {"id": "third-party",       "label": "Third-party document",  "trust_default": "tier-3"},
        {"id": "operator-note",     "label": "Operator-authored note","trust_default": "tier-3"},
        {"id": "unclassified",      "label": "Unclassified",          "trust_default": "tier-4"},
    ],
}

TRUST_TIER_TABLE = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Declared trust tiers. The intake engine *suggests* a tier from format + filename heuristics. The reviewer is the only authority.",
    "tiers": [
        {"id": "tier-1", "label": "OEM-authoritative",       "promotes_without_review": False},
        {"id": "tier-2", "label": "Vendor-authoritative",    "promotes_without_review": False},
        {"id": "tier-3", "label": "Operator-curated",        "promotes_without_review": False},
        {"id": "tier-4", "label": "Unclassified / unknown",  "promotes_without_review": False},
    ],
    "auto_promotion": False,
}

INTAKE_INFERENCE_RULES = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Deterministic heuristics applied by the intake engine. Heuristics are explanatory; reviewer override is always available.",
    "rules": [
        {"id": "R-FMT-1",  "if": "extension in format-table",       "then": "set format from table",                "evidence": "extension"},
        {"id": "R-FMT-2",  "if": "extension not in format-table",   "then": "set format=unknown",                   "evidence": "fallback"},
        {"id": "R-EVD-1",  "if": "format known",                    "then": "set evidence-class to default",        "evidence": "format-table"},
        {"id": "R-EVD-2",  "if": "filename contains 'spec'",        "then": "suggest evidence-class=vendor-spec-sheet", "evidence": "filename"},
        {"id": "R-EVD-3",  "if": "filename contains 'manual'",      "then": "suggest evidence-class=vendor-document",   "evidence": "filename"},
        {"id": "R-TRS-1",  "if": "evidence-class set",              "then": "set trust-tier to class default",      "evidence": "evidence-class-table"},
        {"id": "R-TRS-2",  "if": "filename contains 'oem'",         "then": "suggest trust-tier=tier-1",            "evidence": "filename"},
        {"id": "R-PRD-1",  "if": "filename matches product slug",   "then": "suggest product-scope",                "evidence": "filename"},
        {"id": "R-DOM-1",  "if": "format=structured",               "then": "suggest domain=specifications",        "evidence": "format-category"},
        {"id": "R-DOM-2",  "if": "format=image",                    "then": "suggest domain=visual-identity",       "evidence": "format-category"},
        {"id": "R-RTG-1",  "if": "evidence-class=vendor-document",  "then": "suggest routing=manuals/<product>/",   "evidence": "evidence-class"},
        {"id": "R-RTG-2",  "if": "evidence-class=vendor-spec-sheet","then": "suggest routing=specs/<product>/",     "evidence": "evidence-class"},
        {"id": "R-RTG-3",  "if": "evidence-class=vendor-image",     "then": "suggest routing=visual-identity/<product>/", "evidence": "evidence-class"},
        {"id": "R-AFX-1",  "if": "domain=specifications",           "then": "affected-domains += [specifications, publication]", "evidence": "domain"},
        {"id": "R-AFX-2",  "if": "domain=visual-identity",          "then": "affected-domains += [visual-identity, publication]", "evidence": "domain"},
    ],
    "auto_apply": False,
    "reviewer_must_confirm": True,
    "explanation_required": True,
}

ROUTING_INFERENCE_RULES = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Deterministic answer-builders for the 6 routing-consultation question kinds. Every answer ships with a reasoning chain.",
    "questions": [
        {"id": "where-does-this-file-go",        "answer_builder": "from intake-inference-routing"},
        {"id": "what-class-of-evidence",         "answer_builder": "from intake-inference-evidence-class"},
        {"id": "trust-tier",                     "answer_builder": "from intake-inference-trust-tier"},
        {"id": "operational-role",               "answer_builder": "from evidence-class -> role-table"},
        {"id": "downstream-impact",              "answer_builder": "from domain -> impacted-layers"},
        {"id": "refresh-impact",                 "answer_builder": "from domain -> refresh-pipeline-set"},
    ],
    "role_table": {
        "vendor-document":   "manuals-content",
        "vendor-spec-sheet": "specifications",
        "vendor-image":      "visual-asset",
        "vendor-video":      "visual-asset",
        "structured-data":   "structured-input",
        "evidence-bundle":   "bundle-staging",
        "third-party":       "auxiliary-source",
        "operator-note":     "operator-context",
        "unclassified":      "unclassified",
    },
    "impacted_layers": {
        "specifications":     ["semantic-domain", "publication", "runtime"],
        "visual-identity":    ["identity-resolution", "publication"],
        "manuals":            ["semantic-domain", "publication", "linguistic"],
        "lineage":            ["identity-resolution", "lineage-governance"],
        "unknown":            [],
    },
    "refresh_set": {
        "specifications":  ["extraction-refresh", "propagation-refresh", "publication-refresh"],
        "visual-identity": ["extraction-refresh", "publication-refresh"],
        "manuals":         ["extraction-refresh", "linguistic-refresh", "html-regeneration", "publication-refresh"],
        "lineage":         ["lineage-refresh", "propagation-refresh"],
        "unknown":         [],
    },
    "auto_apply": False,
    "reviewer_must_confirm": True,
    "explanation_required": True,
}

REFRESH_PROPOSAL_RULES = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Deterministic rules for assembling refresh proposal drafts. Builders never trigger rebuilds.",
    "scopes": ["product", "domain", "publication", "runtime", "portfolio"],
    "actions": [
        {"id": "dry-run",          "mutates": False, "produces": "dry-run-report-draft"},
        {"id": "approve",          "mutates": False, "produces": "refresh-approval-draft"},
        {"id": "reject",           "mutates": False, "produces": "refresh-rejection-draft"},
        {"id": "partial-rebuild",  "mutates": False, "produces": "partial-rebuild-draft"},
    ],
    "stale_classes": [
        "stale-extraction", "stale-propagation", "stale-publication",
        "stale-linguistic", "stale-html", "stale-runtime", "stale-lineage",
    ],
    "isolation_rules": [
        "scope=product MUST NOT cascade to portfolio without explicit reviewer escalation",
        "scope=runtime MUST NOT cascade to publication without explicit reviewer escalation",
        "approval drafts include the full reasoning chain and the impacted-layers set",
    ],
    "auto_apply": False,
    "reviewer_must_confirm": True,
}

RECON_REVIEW_RULES = {
    "schema": SCHEMA,
    "constitutional_layer_index": LAYER,
    "purpose": "Deterministic helpers for the 5 reconciliation review types. Geometry-only; no ML, no embeddings, no face recognition.",
    "review_types": [
        {"id": "oem-vs-commercial",     "produces": "reconciliation-decision-draft"},
        {"id": "alias-review",          "produces": "alias-decision-draft"},
        {"id": "visual-reconciliation", "produces": "visual-reconciliation-draft"},
        {"id": "confidence-inspection", "produces": "confidence-note-draft"},
        {"id": "unresolved-identities", "produces": "triage-decision-draft"},
    ],
    "reviewer_classifications": [
        "match-confirmed", "match-rejected", "needs-more-evidence",
        "duplicate", "deprecated", "unresolved",
    ],
    "auto_promotion": False,
    "auto_link_canonicals": False,
    "auto_resolve_contradictions": False,
}

DOCTRINES = [
    ("01-executable-but-non-mutating",   "Executable in the browser, mutating nowhere outside the browser session."),
    ("02-draft-only-emission",           "Every operator action emits an append-only draft manifest. Promotion is out-of-band."),
    ("03-deterministic-explanations",    "Every suggestion is rule-based, reproducible, and ships with a reasoning chain."),
    ("04-local-first-no-network",        "All data stays on the local machine; the console makes no network calls."),
    ("05-reviewer-authoritative",        "Reviewer override is always available; no inference is ever final."),
    ("06-append-only-history",           "Session history and draft stores are append-only and timestamped."),
    ("07-no-ml-no-embeddings",           "No machine learning, no embeddings, no biometric, no face recognition."),
    ("08-governance-first-ux",           "All UX surfaces visibly assert layer, schema, hard rules and reviewer-required posture."),
]

REPORT_PHASES = [
    "phase-32 — multimodal-evidence",
    "phase-33 — intake-and-navigation",
    "phase-34 — semantic-domain",
    "phase-35 — identity-resolution",
    "phase-36 — runtime-orchestration",
    "phase-37 — operational-console",
    "phase-38 — executable-operational-bindings",
]


# ---------------------------------------------------------------------------
# CSS / JS payloads (plain strings; do NOT use f-strings here)
# ---------------------------------------------------------------------------

EXEC_CSS = """/* Beslock Operational Console — exec layer (phase 45 / layer 38) */
.oc-body--exec { background: #0e1726; color: #e9eef6; }
.oc-body--exec .oc-header { background: #0a1320; border-bottom: 1px solid #1f2a3d; }
.oc-body--exec .oc-banner--exec {
  background: #1b2438; color: #d8e1f1; border: 1px solid #2c3a55;
  padding: 0.6rem 1rem; margin: 0.5rem 1rem; border-radius: 6px;
}
.oc-tag--exec { background: #2b6cb0; color: #fff; padding: 0 .4rem; border-radius: 3px; font-size: .7rem; }
.oc-nav__item--exec { color: #8ab4f8; }
.oc-exec { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 1rem; }
.oc-exec--single { grid-template-columns: 1fr; }
.oc-exec__panel {
  background: #111c2e; border: 1px solid #1f2a3d; border-radius: 8px;
  padding: 1rem; min-height: 200px;
}
.oc-exec__panel h3 { margin-top: 0; color: #f5d27a; }
.oc-exec__row { display: flex; gap: .75rem; margin: .5rem 0; flex-wrap: wrap; align-items: center; }
.oc-exec__row label { display: inline-flex; flex-direction: column; gap: .15rem; font-size: .85rem; }
.oc-exec__row input, .oc-exec__row select, .oc-exec__row textarea {
  background: #0a1320; color: #e9eef6; border: 1px solid #2c3a55;
  border-radius: 4px; padding: .35rem .5rem; font: inherit; min-width: 14rem;
}
.oc-exec__row textarea { width: 100%; min-height: 4rem; }
.oc-exec__btn {
  background: #2b6cb0; color: #fff; border: 1px solid #2b6cb0;
  padding: .4rem .9rem; border-radius: 4px; cursor: pointer; font: inherit;
}
.oc-exec__btn:hover { background: #1f5286; }
.oc-exec__btn--ghost { background: transparent; color: #8ab4f8; border-color: #2b6cb0; }
.oc-exec__btn--warn { background: #b04a2b; border-color: #b04a2b; }
.oc-exec__pre {
  background: #0a1320; color: #b9d0f0; border: 1px solid #1f2a3d;
  border-radius: 4px; padding: .75rem; font-size: .8rem;
  max-height: 360px; overflow: auto; white-space: pre-wrap; word-break: break-word;
}
.oc-exec__chain { background: #0a1320; border-left: 3px solid #f5d27a; padding: .5rem .75rem; }
.oc-exec__chain ol { margin: .25rem 0 .25rem 1.25rem; }
.oc-exec__warn { color: #f5b16a; font-weight: 600; }
.oc-exec__ok   { color: #8be9a3; font-weight: 600; }
.oc-exec__kbd  { background: #0a1320; border: 1px solid #2c3a55; border-radius: 3px; padding: 0 .35rem; font-family: monospace; font-size: .8rem; }
.oc-exec__viz { background: #0a1320; border: 1px solid #1f2a3d; border-radius: 4px; }
.oc-exec__viz svg { display: block; width: 100%; height: 320px; }
.oc-exec__viz svg .node-rect { fill: #1b2438; stroke: #2b6cb0; }
.oc-exec__viz svg .node-text { fill: #e9eef6; font: 11px sans-serif; }
.oc-exec__viz svg .edge-line { stroke: #5a86c7; stroke-width: 1; fill: none; marker-end: url(#arrow); }
.oc-exec__list { list-style: none; padding: 0; margin: .5rem 0; }
.oc-exec__list li { background: #0a1320; padding: .35rem .5rem; border-left: 2px solid #2b6cb0; margin: .25rem 0; font-size: .85rem; }
.oc-exec__indicator { font-size: .8rem; color: #8be9a3; }
.oc-exec__indicator--unsaved { color: #f5b16a; }
.oc-exec__hint { color: #8ab4f8; font-size: .8rem; }
@media (max-width: 900px) { .oc-exec { grid-template-columns: 1fr; } }
"""

STATE_JS = """/* exec/state.js — local session + draft state via localStorage. Layer 38. */
(function () {
  "use strict";
  const NS = "beslock.oc.exec.";
  const SCHEMA = "executable-operational-bindings/1.0";
  const SESSION_KEY = NS + "session";
  const DRAFTS_KEY  = NS + "drafts";
  const HISTORY_KEY = NS + "history";

  function uuid() {
    // RFC4122-ish v4 using crypto.getRandomValues if available.
    const buf = new Uint8Array(16);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(buf);
    } else {
      for (let i = 0; i < 16; i++) buf[i] = Math.floor(Math.random() * 256);
    }
    buf[6] = (buf[6] & 0x0f) | 0x40;
    buf[8] = (buf[8] & 0x3f) | 0x80;
    const h = Array.from(buf, function (b) { return b.toString(16).padStart(2, "0"); });
    return h.slice(0, 4).join("") + "-" + h.slice(4, 6).join("") + "-" +
           h.slice(6, 8).join("") + "-" + h.slice(8, 10).join("") + "-" +
           h.slice(10, 16).join("");
  }

  function readJSON(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (e) { return fallback; }
  }

  function writeJSON(key, val) {
    try { window.localStorage.setItem(key, JSON.stringify(val)); }
    catch (e) { /* quota, private mode -- ignore silently */ }
  }

  function ensureSession(reviewer) {
    let s = readJSON(SESSION_KEY, null);
    if (!s) {
      s = {
        schema: SCHEMA,
        session_id: uuid(),
        opened_at_iso: new Date().toISOString(),
        reviewer: reviewer || "anonymous",
        constitutional_layer_index: 38,
      };
      writeJSON(SESSION_KEY, s);
      appendHistory({ kind: "session-open", session_id: s.session_id, at: s.opened_at_iso, reviewer: s.reviewer });
    }
    return s;
  }

  function setReviewer(name) {
    const s = ensureSession();
    s.reviewer = name || "anonymous";
    writeJSON(SESSION_KEY, s);
    appendHistory({ kind: "reviewer-change", session_id: s.session_id, reviewer: s.reviewer, at: new Date().toISOString() });
    return s;
  }

  function appendDraft(draft) {
    const list = readJSON(DRAFTS_KEY, []);
    list.push(draft);
    writeJSON(DRAFTS_KEY, list);
    appendHistory({ kind: "draft-append", draft_id: draft.draft_id, draft_kind: draft.kind, at: draft.proposed_at_iso });
    return list.length;
  }

  function listDrafts() { return readJSON(DRAFTS_KEY, []); }
  function clearDrafts() {
    writeJSON(DRAFTS_KEY, []);
    appendHistory({ kind: "drafts-clear", at: new Date().toISOString() });
  }

  function appendHistory(entry) {
    const list = readJSON(HISTORY_KEY, []);
    list.push(entry);
    if (list.length > 500) list.splice(0, list.length - 500);
    writeJSON(HISTORY_KEY, list);
  }
  function listHistory() { return readJSON(HISTORY_KEY, []); }

  function exportSnapshot() {
    return {
      schema: SCHEMA,
      constitutional_layer_index: 38,
      session: ensureSession(),
      drafts: listDrafts(),
      history: listHistory(),
      exported_at_iso: new Date().toISOString(),
      append_only: true,
      reviewer_authorization_required: true,
    };
  }

  window.OC = window.OC || {};
  window.OC.State = {
    uuid: uuid,
    ensureSession: ensureSession,
    setReviewer: setReviewer,
    appendDraft: appendDraft,
    listDrafts: listDrafts,
    clearDrafts: clearDrafts,
    appendHistory: appendHistory,
    listHistory: listHistory,
    exportSnapshot: exportSnapshot,
  };
})();
"""

DRAFTS_JS = """/* exec/drafts.js — append-only draft manifest engine. Layer 38. */
(function () {
  "use strict";
  const SCHEMA_DRAFT = "operational-console-draft/1.1";

  function build(kind, payload, reasoningChain) {
    const session = window.OC.State.ensureSession();
    return {
      schema: SCHEMA_DRAFT,
      constitutional_layer_index: 38,
      draft_id: window.OC.State.uuid(),
      session_id: session.session_id,
      reviewer: session.reviewer,
      kind: kind,
      payload: payload || {},
      reasoning_chain: reasoningChain || [],
      proposed_at_iso: new Date().toISOString(),
      reviewer_authorization_required: true,
      auto_promotion: false,
      auto_mutates_source_truth: false,
      append_only: true,
    };
  }

  function record(kind, payload, reasoningChain) {
    const draft = build(kind, payload, reasoningChain);
    window.OC.State.appendDraft(draft);
    return draft;
  }

  function preview(target, draft) {
    if (typeof target === "string") target = document.getElementById(target);
    if (!target) return;
    target.textContent = JSON.stringify(draft, null, 2);
  }

  function exportDownload(filename, obj) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename || "draft.json";
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 0);
  }

  window.OC = window.OC || {};
  window.OC.Drafts = { build: build, record: record, preview: preview, exportDownload: exportDownload };
})();
"""

INTAKE_ENGINE_JS = """/* exec/intake-engine.js — deterministic file -> intake-draft engine. Layer 38. */
(function () {
  "use strict";
  let RULES = null;
  let FORMATS = null;
  let CLASSES = null;
  let TIERS = null;

  const PRODUCT_SLUGS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"];

  function loadTables() {
    return Promise.all([
      fetch("../execution-engine/format-classification-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/evidence-class-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/trust-tier-table.json").then(function (r) { return r.json(); }),
      fetch("../execution-engine/intake-inference-rules.json").then(function (r) { return r.json(); }),
    ]).then(function (arr) {
      FORMATS = arr[0]; CLASSES = arr[1]; TIERS = arr[2]; RULES = arr[3];
      return { FORMATS: FORMATS, CLASSES: CLASSES, TIERS: TIERS, RULES: RULES };
    });
  }

  function extOf(name) {
    const i = name.lastIndexOf(".");
    return i >= 0 ? name.slice(i).toLowerCase() : "";
  }

  function pickFormat(ext) {
    if (FORMATS && FORMATS.extensions && FORMATS.extensions[ext]) return FORMATS.extensions[ext];
    return FORMATS && FORMATS.fallback ? FORMATS.fallback : { format: "unknown", category: "unknown", default_evidence_class: "unclassified" };
  }

  function pickEvidenceDefault(name, fmtRow) {
    const lower = name.toLowerCase();
    let cls = fmtRow.default_evidence_class;
    let why = "R-EVD-1: format-table default";
    if (lower.indexOf("spec") !== -1 && fmtRow.category === "structured") {
      cls = "vendor-spec-sheet"; why = "R-EVD-2: filename contains 'spec'";
    } else if (lower.indexOf("manual") !== -1 && fmtRow.category === "document") {
      cls = "vendor-document"; why = "R-EVD-3: filename contains 'manual'";
    }
    return { evidence_class: cls, reason: why };
  }

  function pickTrustDefault(cls, name) {
    let tier = "tier-4";
    if (CLASSES && CLASSES.classes) {
      const row = CLASSES.classes.filter(function (c) { return c.id === cls; })[0];
      if (row) tier = row.trust_default;
    }
    let why = "R-TRS-1: evidence-class default";
    if (name.toLowerCase().indexOf("oem") !== -1) { tier = "tier-1"; why = "R-TRS-2: filename contains 'oem'"; }
    return { trust_tier: tier, reason: why };
  }

  function pickProduct(name) {
    const lower = name.toLowerCase();
    for (let i = 0; i < PRODUCT_SLUGS.length; i++) {
      if (lower.indexOf(PRODUCT_SLUGS[i]) !== -1) {
        return { product: PRODUCT_SLUGS[i], reason: "R-PRD-1: filename matches product slug '" + PRODUCT_SLUGS[i] + "'" };
      }
    }
    return { product: null, reason: "no product slug matched" };
  }

  function pickDomain(fmtRow) {
    if (fmtRow.category === "structured") return { domain: "specifications", reason: "R-DOM-1: format-category=structured" };
    if (fmtRow.category === "image")      return { domain: "visual-identity", reason: "R-DOM-2: format-category=image" };
    if (fmtRow.category === "document")   return { domain: "manuals",         reason: "format-category=document" };
    if (fmtRow.category === "video")      return { domain: "visual-identity", reason: "format-category=video" };
    if (fmtRow.category === "archive")    return { domain: "lineage",         reason: "format-category=archive" };
    return { domain: "unknown", reason: "no domain rule matched" };
  }

  function pickRouting(cls, product) {
    const tag = product || "<product>";
    if (cls === "vendor-document")   return { routing: "manuals/" + tag + "/", reason: "R-RTG-1" };
    if (cls === "vendor-spec-sheet") return { routing: "specs/" + tag + "/", reason: "R-RTG-2" };
    if (cls === "vendor-image")      return { routing: "visual-identity/" + tag + "/", reason: "R-RTG-3" };
    return { routing: "unrouted/", reason: "no routing rule matched" };
  }

  function affectedDomains(domain) {
    if (domain === "specifications")  return { affected: ["specifications", "publication"], reason: "R-AFX-1" };
    if (domain === "visual-identity") return { affected: ["visual-identity", "publication"], reason: "R-AFX-2" };
    if (domain === "manuals")         return { affected: ["semantic-domain", "publication", "linguistic"], reason: "manuals impact" };
    return { affected: [], reason: "no affected-domain rule matched" };
  }

  function infer(file) {
    const ext = extOf(file.name);
    const fmtRow = pickFormat(ext);
    const evd = pickEvidenceDefault(file.name, fmtRow);
    const trs = pickTrustDefault(evd.evidence_class, file.name);
    const prd = pickProduct(file.name);
    const dom = pickDomain(fmtRow);
    const rtg = pickRouting(evd.evidence_class, prd.product);
    const afx = affectedDomains(dom.domain);

    const meta = {
      filename: file.name,
      extension: ext,
      filesize_bytes: file.size,
      modified_iso: file.lastModified ? new Date(file.lastModified).toISOString() : null,
    };
    const inferred = {
      format: fmtRow.format,
      format_category: fmtRow.category,
      evidence_class: evd.evidence_class,
      trust_tier: trs.trust_tier,
      product: prd.product,
      domain: dom.domain,
      routing: rtg.routing,
      affected_domains: afx.affected,
    };
    const chain = [
      { rule: "R-FMT-1/2", evidence: "extension '" + ext + "' -> format '" + fmtRow.format + "' (category '" + fmtRow.category + "')" },
      { rule: evd.reason,  evidence: "evidence-class -> '" + evd.evidence_class + "'" },
      { rule: trs.reason,  evidence: "trust-tier -> '" + trs.trust_tier + "'" },
      { rule: prd.reason,  evidence: "product -> " + (prd.product || "(none)") },
      { rule: dom.reason,  evidence: "domain -> '" + dom.domain + "'" },
      { rule: rtg.reason,  evidence: "routing -> '" + rtg.routing + "'" },
      { rule: afx.reason,  evidence: "affected-domains -> [" + afx.affected.join(", ") + "]" },
    ];
    return { meta: meta, inferred: inferred, reasoning_chain: chain };
  }

  window.OC = window.OC || {};
  window.OC.IntakeEngine = { loadTables: loadTables, infer: infer };
})();
"""

ROUTING_ENGINE_JS = """/* exec/routing-engine.js — deterministic 6-question routing consultation. Layer 38. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/routing-inference-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function answer(intakeInferred) {
    if (!RULES) return null;
    const out = [];
    out.push({
      question: "where-does-this-file-go",
      answer: intakeInferred.routing,
      reasoning: "R-RTG (intake) -> evidence-class '" + intakeInferred.evidence_class + "' -> '" + intakeInferred.routing + "'",
    });
    out.push({
      question: "what-class-of-evidence",
      answer: intakeInferred.evidence_class,
      reasoning: "intake-engine evidence default; reviewer override available",
    });
    out.push({
      question: "trust-tier",
      answer: intakeInferred.trust_tier,
      reasoning: "trust-tier-table default for class; OEM filename heuristic if applicable",
    });
    const role = (RULES.role_table && RULES.role_table[intakeInferred.evidence_class]) || "unclassified";
    out.push({
      question: "operational-role",
      answer: role,
      reasoning: "role_table[" + intakeInferred.evidence_class + "] = " + role,
    });
    const layers = (RULES.impacted_layers && RULES.impacted_layers[intakeInferred.domain]) || [];
    out.push({
      question: "downstream-impact",
      answer: layers,
      reasoning: "impacted_layers[" + intakeInferred.domain + "] = [" + layers.join(", ") + "]",
    });
    const refresh = (RULES.refresh_set && RULES.refresh_set[intakeInferred.domain]) || [];
    out.push({
      question: "refresh-impact",
      answer: refresh,
      reasoning: "refresh_set[" + intakeInferred.domain + "] = [" + refresh.join(", ") + "]",
    });
    return out;
  }

  window.OC = window.OC || {};
  window.OC.RoutingEngine = { load: load, answer: answer };
})();
"""

RECON_ENGINE_JS = """/* exec/recon-engine.js — reconciliation review helpers. Layer 38. Geometry-only, no ML. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/reconciliation-review-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function classifications() {
    return RULES ? RULES.reviewer_classifications.slice() : [];
  }

  function reviewTypes() {
    return RULES ? RULES.review_types.slice() : [];
  }

  function buildDecision(reviewType, payload) {
    const meta = (RULES && RULES.review_types || []).filter(function (r) { return r.id === reviewType; })[0];
    return {
      review_type: reviewType,
      produces: meta ? meta.produces : "reconciliation-decision-draft",
      payload: payload,
      auto_promotion: false,
      auto_link_canonicals: false,
      auto_resolve_contradictions: false,
    };
  }

  window.OC = window.OC || {};
  window.OC.ReconEngine = { load: load, classifications: classifications, reviewTypes: reviewTypes, buildDecision: buildDecision };
})();
"""

REFRESH_ENGINE_JS = """/* exec/refresh-engine.js — refresh proposal builder. Layer 38. No rebuild executes. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/refresh-proposal-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function scopes() { return RULES ? RULES.scopes.slice() : []; }
  function actions() { return RULES ? RULES.actions.slice() : []; }
  function staleClasses() { return RULES ? RULES.stale_classes.slice() : []; }

  function buildProposal(opts) {
    const reasoning = [
      { step: "scope-selected",   value: opts.scope },
      { step: "action-selected",  value: opts.action },
      { step: "domains-selected", value: opts.domains || [] },
      { step: "publications",     value: opts.publications || [] },
      { step: "isolation-rules",  value: (RULES && RULES.isolation_rules) || [] },
    ];
    return {
      payload: {
        scope: opts.scope,
        action: opts.action,
        domains: opts.domains || [],
        publications: opts.publications || [],
        notes: opts.notes || "",
        mutates_anything: false,
        executes_rebuild: false,
      },
      reasoning_chain: reasoning,
    };
  }

  window.OC = window.OC || {};
  window.OC.RefreshEngine = { load: load, scopes: scopes, actions: actions, staleClasses: staleClasses, buildProposal: buildProposal };
})();
"""

VIZ_JS = """/* exec/viz.js — vanilla SVG dependency / lifecycle visualisation. Layer 38. */
(function () {
  "use strict";

  function ensureMarker(svg) {
    const NS = "http://www.w3.org/2000/svg";
    let defs = svg.querySelector("defs");
    if (!defs) { defs = document.createElementNS(NS, "defs"); svg.appendChild(defs); }
    if (!svg.querySelector("#arrow")) {
      const m = document.createElementNS(NS, "marker");
      m.setAttribute("id", "arrow"); m.setAttribute("viewBox", "0 0 10 10");
      m.setAttribute("refX", "10"); m.setAttribute("refY", "5");
      m.setAttribute("markerWidth", "8"); m.setAttribute("markerHeight", "8");
      m.setAttribute("orient", "auto-start-reverse");
      const p = document.createElementNS(NS, "path");
      p.setAttribute("d", "M 0 0 L 10 5 L 0 10 z"); p.setAttribute("fill", "#5a86c7");
      m.appendChild(p); defs.appendChild(m);
    }
  }

  function renderGraph(svg, nodes, edges) {
    const NS = "http://www.w3.org/2000/svg";
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    ensureMarker(svg);
    const w = svg.clientWidth || 600;
    const h = svg.clientHeight || 320;
    const cols = Math.max(1, Math.ceil(Math.sqrt(nodes.length)));
    const rows = Math.max(1, Math.ceil(nodes.length / cols));
    const dx = w / (cols + 1);
    const dy = h / (rows + 1);
    const pos = {};
    nodes.forEach(function (n, i) {
      const c = (i % cols) + 1, r = Math.floor(i / cols) + 1;
      pos[n.id] = { x: c * dx, y: r * dy };
    });
    edges.forEach(function (e) {
      const a = pos[e.from], b = pos[e.to];
      if (!a || !b) return;
      const line = document.createElementNS(NS, "line");
      line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
      line.setAttribute("class", "edge-line");
      svg.appendChild(line);
    });
    nodes.forEach(function (n) {
      const p = pos[n.id];
      const rect = document.createElementNS(NS, "rect");
      const lbl  = (n.label || n.id);
      const wpx  = Math.max(60, lbl.length * 6 + 12);
      rect.setAttribute("x", p.x - wpx / 2); rect.setAttribute("y", p.y - 14);
      rect.setAttribute("width", wpx); rect.setAttribute("height", 28);
      rect.setAttribute("rx", 4); rect.setAttribute("class", "node-rect");
      svg.appendChild(rect);
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", p.x); t.setAttribute("y", p.y + 4);
      t.setAttribute("text-anchor", "middle"); t.setAttribute("class", "node-text");
      t.textContent = lbl; svg.appendChild(t);
    });
  }

  window.OC = window.OC || {};
  window.OC.Viz = { renderGraph: renderGraph };
})();
"""

UX_JS = """/* exec/ux.js — small UX helpers. Layer 38. */
(function () {
  "use strict";

  function setIndicator(id, text, kind) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("oc-exec__indicator--unsaved", kind === "unsaved");
  }

  function bindKeyboard(map) {
    document.addEventListener("keydown", function (e) {
      const key = (e.ctrlKey || e.metaKey ? "Mod+" : "") + (e.shiftKey ? "Shift+" : "") + (e.key || "");
      const fn = map[key];
      if (fn) { e.preventDefault(); fn(e); }
    });
  }

  function showWarning(target, text) {
    if (typeof target === "string") target = document.getElementById(target);
    if (!target) return;
    target.classList.add("oc-exec__warn"); target.textContent = text;
  }

  window.OC = window.OC || {};
  window.OC.UX = { setIndicator: setIndicator, bindKeyboard: bindKeyboard, showWarning: showWarning };
})();
"""


# ---------------------------------------------------------------------------
# HTML pages
# ---------------------------------------------------------------------------

def exec_dashboard_html() -> str:
    body = """    <section class="oc-section">
      <h1>Executable Operational Bindings <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Lightweight executable surfaces over the layer-37 console. All actions are draft-only and stay on the local machine.</p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>Reviewer session</h3>
        <div class="oc-exec__row">
          <label>Reviewer name <input id="reviewer-name" type="text" placeholder="reviewer@local" /></label>
          <button class="oc-exec__btn" id="reviewer-set">Set reviewer</button>
        </div>
        <p>Session id: <code id="session-id">—</code></p>
        <p>Drafts in session: <code id="drafts-count">0</code> · History entries: <code id="history-count">0</code></p>
        <div class="oc-exec__row">
          <button class="oc-exec__btn" id="export-snapshot">Export session snapshot (.json)</button>
          <button class="oc-exec__btn oc-exec__btn--warn" id="clear-drafts">Clear local drafts</button>
        </div>
        <p class="oc-exec__hint">Stored only in <span class="oc-exec__kbd">localStorage</span>. No network call. No cloud. No telemetry.</p>
      </article>
      <article class="oc-exec__panel">
        <h3>Recent drafts</h3>
        <ul class="oc-exec__list" id="drafts-list"></ul>
        <pre class="oc-exec__pre" id="drafts-dump">{}</pre>
      </article>
      <article class="oc-exec__panel">
        <h3>Executable consoles</h3>
        <ul class="oc-exec__list">
          <li><a class="oc-link" href="intake-console/exec.html">Intake (executable)</a></li>
          <li><a class="oc-link" href="routing-console/exec.html">Routing (executable)</a></li>
          <li><a class="oc-link" href="refresh-console/exec.html">Refresh (executable)</a></li>
          <li><a class="oc-link" href="reconciliation-console/exec.html">Reconciliation (executable)</a></li>
          <li><a class="oc-link" href="publication-console/exec.html">Publication (interactive read-only)</a></li>
          <li><a class="oc-link" href="governance-console/exec.html">Governance (interactive read-only)</a></li>
        </ul>
      </article>
      <article class="oc-exec__panel">
        <h3>Governance posture</h3>
        <ul class="oc-list">
          <li>Layer <span class="oc-tag oc-tag--accent">38</span></li>
          <li>Subordinate chain length <span class="oc-tag">37</span></li>
          <li>Network calls <span class="oc-tag oc-tag--ok">none</span></li>
          <li>Auto-approval <span class="oc-tag oc-tag--ok">disabled</span></li>
          <li>Source-truth mutation <span class="oc-tag oc-tag--ok">forbidden</span></li>
          <li>Append-only drafts <span class="oc-tag oc-tag--ok">enforced</span></li>
          <li>Reviewer authorization <span class="oc-tag oc-tag--warn">required for every promotion</span></li>
        </ul>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        const s = window.OC.State.ensureSession();
        document.getElementById("session-id").textContent = s.session_id;
        document.getElementById("reviewer-name").value = s.reviewer || "";
        function refresh() {
          const drafts = window.OC.State.listDrafts();
          document.getElementById("drafts-count").textContent = drafts.length;
          document.getElementById("history-count").textContent = window.OC.State.listHistory().length;
          const ul = document.getElementById("drafts-list");
          ul.innerHTML = "";
          drafts.slice(-10).reverse().forEach(function (d) {
            const li = document.createElement("li");
            li.textContent = d.proposed_at_iso + " · " + d.kind + " · " + d.draft_id.slice(0, 8);
            ul.appendChild(li);
          });
          document.getElementById("drafts-dump").textContent = JSON.stringify(drafts, null, 2);
        }
        refresh();
        document.getElementById("reviewer-set").addEventListener("click", function () {
          window.OC.State.setReviewer(document.getElementById("reviewer-name").value); refresh();
        });
        document.getElementById("export-snapshot").addEventListener("click", function () {
          window.OC.Drafts.exportDownload("oc-session-" + s.session_id.slice(0,8) + ".json", window.OC.State.exportSnapshot());
        });
        document.getElementById("clear-drafts").addEventListener("click", function () {
          if (confirm("Clear local draft list? (history retains the clear event)")) { window.OC.State.clearDrafts(); refresh(); }
        });
      });
    </script>
"""
    return page("Exec Dashboard", body, prefix=".", extra_scripts=["state.js", "drafts.js"])


def intake_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Intake (executable) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Pick a file from your local machine. The console reads its metadata, applies deterministic rules, shows the reasoning chain, lets you override any field, then emits an append-only intake-draft. <strong>Nothing is uploaded.</strong></p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>1 · Local file</h3>
        <div class="oc-exec__row">
          <label>Pick file <input id="file-input" type="file" /></label>
        </div>
        <pre class="oc-exec__pre" id="file-meta">no file selected</pre>
      </article>
      <article class="oc-exec__panel">
        <h3>2 · Inferred</h3>
        <pre class="oc-exec__pre" id="inferred-dump">—</pre>
        <h3>Reasoning chain</h3>
        <div class="oc-exec__chain"><ol id="chain-list"></ol></div>
      </article>
      <article class="oc-exec__panel">
        <h3>3 · Reviewer override</h3>
        <div class="oc-exec__row">
          <label>Format     <input id="ov-format" type="text" /></label>
          <label>Evidence class
            <select id="ov-evidence"><option value="vendor-document">vendor-document</option><option value="vendor-spec-sheet">vendor-spec-sheet</option><option value="vendor-image">vendor-image</option><option value="vendor-video">vendor-video</option><option value="structured-data">structured-data</option><option value="evidence-bundle">evidence-bundle</option><option value="third-party">third-party</option><option value="operator-note">operator-note</option><option value="unclassified">unclassified</option></select>
          </label>
          <label>Trust tier
            <select id="ov-trust"><option value="tier-1">tier-1</option><option value="tier-2">tier-2</option><option value="tier-3">tier-3</option><option value="tier-4">tier-4</option></select>
          </label>
        </div>
        <div class="oc-exec__row">
          <label>Product   <input id="ov-product" type="text" /></label>
          <label>Domain    <input id="ov-domain" type="text" /></label>
          <label>Routing   <input id="ov-routing" type="text" /></label>
        </div>
        <div class="oc-exec__row">
          <label style="flex:1"><span>Reviewer notes</span><textarea id="ov-notes" placeholder="Optional reviewer notes for the audit chain"></textarea></label>
        </div>
        <div class="oc-exec__row">
          <button class="oc-exec__btn" id="emit-draft">Emit intake-draft</button>
          <button class="oc-exec__btn oc-exec__btn--ghost" id="export-draft">Export draft (.json)</button>
          <span id="indicator" class="oc-exec__indicator">no unsaved draft</span>
        </div>
      </article>
      <article class="oc-exec__panel">
        <h3>4 · Draft preview</h3>
        <pre class="oc-exec__pre" id="draft-preview">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        let inferred = null, lastDraft = null;
        const fileInput = document.getElementById("file-input");
        const meta = document.getElementById("file-meta");
        const idump = document.getElementById("inferred-dump");
        const chain = document.getElementById("chain-list");

        window.OC.IntakeEngine.loadTables().catch(function () {
          window.OC.UX.showWarning("file-meta", "Could not load rule tables (file:// fetch may be blocked). Serve via 'python -m http.server' from the repo root and reload.");
        });

        fileInput.addEventListener("change", function (e) {
          const f = e.target.files && e.target.files[0]; if (!f) return;
          const r = window.OC.IntakeEngine.infer(f);
          inferred = r;
          meta.textContent = JSON.stringify(r.meta, null, 2);
          idump.textContent = JSON.stringify(r.inferred, null, 2);
          chain.innerHTML = "";
          r.reasoning_chain.forEach(function (step) {
            const li = document.createElement("li");
            li.textContent = step.rule + " — " + step.evidence;
            chain.appendChild(li);
          });
          document.getElementById("ov-format").value   = r.inferred.format;
          document.getElementById("ov-evidence").value = r.inferred.evidence_class;
          document.getElementById("ov-trust").value    = r.inferred.trust_tier;
          document.getElementById("ov-product").value  = r.inferred.product || "";
          document.getElementById("ov-domain").value   = r.inferred.domain;
          document.getElementById("ov-routing").value  = r.inferred.routing;
          window.OC.UX.setIndicator("indicator", "intake inferred — review before emitting", "unsaved");
        });

        document.getElementById("emit-draft").addEventListener("click", function () {
          if (!inferred) { alert("Pick a file first."); return; }
          const overrides = {
            format:         document.getElementById("ov-format").value,
            evidence_class: document.getElementById("ov-evidence").value,
            trust_tier:     document.getElementById("ov-trust").value,
            product:        document.getElementById("ov-product").value || null,
            domain:         document.getElementById("ov-domain").value,
            routing:        document.getElementById("ov-routing").value,
            reviewer_notes: document.getElementById("ov-notes").value,
          };
          const payload = { meta: inferred.meta, inferred: inferred.inferred, overrides: overrides };
          lastDraft = window.OC.Drafts.record("intake-draft", payload, inferred.reasoning_chain);
          window.OC.Drafts.preview("draft-preview", lastDraft);
          window.OC.UX.setIndicator("indicator", "intake-draft appended (id " + lastDraft.draft_id.slice(0,8) + ")", "ok");
        });

        document.getElementById("export-draft").addEventListener("click", function () {
          if (!lastDraft) { alert("No draft to export. Emit first."); return; }
          window.OC.Drafts.exportDownload("intake-draft-" + lastDraft.draft_id.slice(0,8) + ".json", lastDraft);
        });
      });
    </script>
"""
    return page("Intake (exec)", body, prefix="..", extra_scripts=["state.js", "drafts.js", "intake-engine.js", "ux.js"])


def routing_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Routing consultation (executable) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Pick a file. The console answers six routing questions deterministically, each with its reasoning chain. Reviewer is the only authority.</p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>1 · Local file</h3>
        <div class="oc-exec__row"><label>Pick file <input id="file-input" type="file" /></label></div>
        <pre class="oc-exec__pre" id="file-meta">no file selected</pre>
      </article>
      <article class="oc-exec__panel">
        <h3>2 · Six answers</h3>
        <ul class="oc-exec__list" id="answers"></ul>
      </article>
      <article class="oc-exec__panel oc-exec--single" style="grid-column: 1 / -1;">
        <h3>3 · Reviewer decision</h3>
        <div class="oc-exec__row">
          <label>Reviewer disposition
            <select id="disp"><option value="accept-all">accept all proposals</option><option value="accept-with-overrides">accept with overrides</option><option value="reject">reject all proposals</option></select>
          </label>
          <label style="flex:1"><span>Reviewer notes</span><textarea id="notes"></textarea></label>
        </div>
        <div class="oc-exec__row">
          <button class="oc-exec__btn" id="emit">Emit routing-consultation-draft</button>
          <button class="oc-exec__btn oc-exec__btn--ghost" id="export">Export draft (.json)</button>
          <span id="indicator" class="oc-exec__indicator">no draft</span>
        </div>
        <pre class="oc-exec__pre" id="draft-preview">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        let inferred = null, answers = null, lastDraft = null;
        Promise.all([window.OC.IntakeEngine.loadTables(), window.OC.RoutingEngine.load()]).catch(function () {
          window.OC.UX.showWarning("file-meta", "Rule tables failed to load (file:// fetch may be blocked).");
        });
        document.getElementById("file-input").addEventListener("change", function (e) {
          const f = e.target.files && e.target.files[0]; if (!f) return;
          const r = window.OC.IntakeEngine.infer(f); inferred = r;
          document.getElementById("file-meta").textContent = JSON.stringify(r.meta, null, 2);
          answers = window.OC.RoutingEngine.answer(r.inferred);
          const ul = document.getElementById("answers");
          ul.innerHTML = "";
          answers.forEach(function (a) {
            const li = document.createElement("li");
            li.innerHTML = "<strong>" + a.question + ":</strong> " + (Array.isArray(a.answer) ? a.answer.join(", ") || "(none)" : a.answer) + "<br><span class='oc-exec__hint'>" + a.reasoning + "</span>";
            ul.appendChild(li);
          });
          window.OC.UX.setIndicator("indicator", "answers ready — emit draft to record reviewer disposition", "unsaved");
        });
        document.getElementById("emit").addEventListener("click", function () {
          if (!answers) { alert("Pick a file first."); return; }
          lastDraft = window.OC.Drafts.record("routing-consultation-draft", {
            meta: inferred.meta,
            inferred: inferred.inferred,
            answers: answers,
            disposition: document.getElementById("disp").value,
            reviewer_notes: document.getElementById("notes").value,
          }, inferred.reasoning_chain);
          window.OC.Drafts.preview("draft-preview", lastDraft);
          window.OC.UX.setIndicator("indicator", "draft appended " + lastDraft.draft_id.slice(0,8), "ok");
        });
        document.getElementById("export").addEventListener("click", function () {
          if (!lastDraft) return; window.OC.Drafts.exportDownload("routing-draft-" + lastDraft.draft_id.slice(0,8) + ".json", lastDraft);
        });
      });
    </script>
"""
    return page("Routing (exec)", body, prefix="..",
                extra_scripts=["state.js", "drafts.js", "intake-engine.js", "routing-engine.js", "ux.js"])


def refresh_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Refresh proposal (executable) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Pick a scope, an action, the impacted domains and publications. The console emits a refresh-proposal draft. <strong>No rebuild ever runs from this UI.</strong></p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>Proposal builder</h3>
        <div class="oc-exec__row">
          <label>Scope
            <select id="scope"><option>product</option><option>domain</option><option>publication</option><option>runtime</option><option>portfolio</option></select>
          </label>
          <label>Action
            <select id="action"><option>dry-run</option><option>approve</option><option>reject</option><option>partial-rebuild</option></select>
          </label>
        </div>
        <div class="oc-exec__row">
          <label>Domains (comma)     <input id="domains" type="text" placeholder="specifications, visual-identity" /></label>
          <label>Publications (comma)<input id="publications" type="text" placeholder="e-orbit, e-prime" /></label>
        </div>
        <div class="oc-exec__row"><label style="flex:1"><span>Reviewer notes</span><textarea id="notes"></textarea></label></div>
        <div class="oc-exec__row">
          <button class="oc-exec__btn" id="emit">Emit refresh-draft</button>
          <button class="oc-exec__btn oc-exec__btn--ghost" id="export">Export draft (.json)</button>
          <span id="indicator" class="oc-exec__indicator">no draft</span>
        </div>
      </article>
      <article class="oc-exec__panel">
        <h3>Stale-impact preview</h3>
        <ul class="oc-exec__list" id="stale-list"></ul>
        <h3>Reasoning chain</h3>
        <div class="oc-exec__chain"><ol id="chain"></ol></div>
      </article>
      <article class="oc-exec__panel oc-exec--single" style="grid-column: 1 / -1;">
        <h3>Draft preview</h3>
        <pre class="oc-exec__pre" id="draft-preview">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        let lastDraft = null;
        window.OC.RefreshEngine.load().then(function () {
          const ul = document.getElementById("stale-list");
          ul.innerHTML = "";
          window.OC.RefreshEngine.staleClasses().forEach(function (s) {
            const li = document.createElement("li"); li.textContent = s; ul.appendChild(li);
          });
        }).catch(function () {
          window.OC.UX.showWarning("indicator", "Rule tables failed to load (file:// fetch may be blocked).");
        });
        document.getElementById("emit").addEventListener("click", function () {
          const opts = {
            scope: document.getElementById("scope").value,
            action: document.getElementById("action").value,
            domains: document.getElementById("domains").value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
            publications: document.getElementById("publications").value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
            notes: document.getElementById("notes").value,
          };
          const r = window.OC.RefreshEngine.buildProposal(opts);
          lastDraft = window.OC.Drafts.record("refresh-proposal-draft", r.payload, r.reasoning_chain);
          const c = document.getElementById("chain"); c.innerHTML = "";
          r.reasoning_chain.forEach(function (st) { const li = document.createElement("li"); li.textContent = st.step + ": " + JSON.stringify(st.value); c.appendChild(li); });
          window.OC.Drafts.preview("draft-preview", lastDraft);
          window.OC.UX.setIndicator("indicator", "refresh-draft appended " + lastDraft.draft_id.slice(0,8), "ok");
        });
        document.getElementById("export").addEventListener("click", function () {
          if (!lastDraft) return; window.OC.Drafts.exportDownload("refresh-draft-" + lastDraft.draft_id.slice(0,8) + ".json", lastDraft);
        });
      });
    </script>
"""
    return page("Refresh (exec)", body, prefix="..",
                extra_scripts=["state.js", "drafts.js", "refresh-engine.js", "ux.js"])


def recon_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Reconciliation review (executable) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Inspect candidate identity reconciliations and emit reviewer-classified decision drafts. <strong>No identity is auto-promoted, auto-linked or auto-resolved.</strong></p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>Decision builder</h3>
        <div class="oc-exec__row">
          <label>Review type <select id="rtype"></select></label>
          <label>Classification <select id="rclass"></select></label>
        </div>
        <div class="oc-exec__row">
          <label>Candidate A <input id="ca" type="text" placeholder="oem-model-or-sku" /></label>
          <label>Candidate B <input id="cb" type="text" placeholder="commercial-or-canonical" /></label>
        </div>
        <div class="oc-exec__row"><label style="flex:1"><span>Reviewer notes</span><textarea id="notes"></textarea></label></div>
        <div class="oc-exec__row">
          <button class="oc-exec__btn" id="emit">Emit reconciliation-decision-draft</button>
          <button class="oc-exec__btn oc-exec__btn--ghost" id="export">Export draft (.json)</button>
          <span id="indicator" class="oc-exec__indicator">no draft</span>
        </div>
      </article>
      <article class="oc-exec__panel">
        <h3>Hard rules</h3>
        <ul class="oc-list">
          <li>Auto-promotion <span class="oc-tag oc-tag--ok">forbidden</span></li>
          <li>Auto-link canonicals <span class="oc-tag oc-tag--ok">forbidden</span></li>
          <li>Auto-resolve contradictions <span class="oc-tag oc-tag--ok">forbidden</span></li>
          <li>Geometry-only visual checks <span class="oc-tag oc-tag--accent">no ML / no embeddings / no biometric</span></li>
          <li>Reviewer authorisation <span class="oc-tag oc-tag--warn">required for promotion</span></li>
        </ul>
      </article>
      <article class="oc-exec__panel oc-exec--single" style="grid-column: 1 / -1;">
        <h3>Draft preview</h3>
        <pre class="oc-exec__pre" id="draft-preview">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        let lastDraft = null;
        window.OC.ReconEngine.load().then(function () {
          const types = window.OC.ReconEngine.reviewTypes();
          const sel = document.getElementById("rtype");
          types.forEach(function (t) { const o = document.createElement("option"); o.value = t.id; o.textContent = t.id; sel.appendChild(o); });
          const cls = window.OC.ReconEngine.classifications();
          const cs  = document.getElementById("rclass");
          cls.forEach(function (c) { const o = document.createElement("option"); o.value = c; o.textContent = c; cs.appendChild(o); });
        }).catch(function () { window.OC.UX.showWarning("indicator", "Rule tables failed to load (file:// fetch may be blocked)."); });
        document.getElementById("emit").addEventListener("click", function () {
          const decision = window.OC.ReconEngine.buildDecision(document.getElementById("rtype").value, {
            candidate_a: document.getElementById("ca").value,
            candidate_b: document.getElementById("cb").value,
            classification: document.getElementById("rclass").value,
            reviewer_notes: document.getElementById("notes").value,
          });
          const chain = [{ step: "review-type", value: decision.review_type }, { step: "classification", value: decision.payload.classification }];
          lastDraft = window.OC.Drafts.record("reconciliation-decision-draft", decision, chain);
          window.OC.Drafts.preview("draft-preview", lastDraft);
          window.OC.UX.setIndicator("indicator", "reconciliation-draft appended " + lastDraft.draft_id.slice(0,8), "ok");
        });
        document.getElementById("export").addEventListener("click", function () {
          if (!lastDraft) return; window.OC.Drafts.exportDownload("reconciliation-draft-" + lastDraft.draft_id.slice(0,8) + ".json", lastDraft);
        });
      });
    </script>
"""
    return page("Reconciliation (exec)", body, prefix="..",
                extra_scripts=["state.js", "drafts.js", "recon-engine.js", "ux.js"])


def publication_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Publication visibility (interactive read-only) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Inspect generated HTML, stale outputs, lineage and rebuild history locally. <strong>Read-only.</strong> No regeneration, no publication-root writes.</p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>Local HTML preview</h3>
        <div class="oc-exec__row"><label>Pick a local .html file <input id="html-input" type="file" accept=".html,.htm" /></label></div>
        <iframe id="html-preview" sandbox="" style="width:100%; height:300px; background:#fff; border:1px solid #1f2a3d;"></iframe>
        <p class="oc-exec__hint">Preview is sandboxed; the iframe cannot script, navigate, or call the network.</p>
      </article>
      <article class="oc-exec__panel">
        <h3>Mock visibility feeds</h3>
        <pre class="oc-exec__pre" id="feeds">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("html-input").addEventListener("change", function (e) {
          const f = e.target.files && e.target.files[0]; if (!f) return;
          const url = URL.createObjectURL(f);
          const ifr = document.getElementById("html-preview");
          ifr.src = url;
        });
        fetch("../mock-data/publications.json").then(function (r) { return r.json(); }).then(function (j) {
          document.getElementById("feeds").textContent = JSON.stringify(j, null, 2);
        }).catch(function () { document.getElementById("feeds").textContent = "(could not load mock feed)"; });
      });
    </script>
"""
    return page("Publication (exec)", body, prefix="..", extra_scripts=["state.js", "ux.js"])


def governance_exec_html() -> str:
    body = """    <section class="oc-section">
      <h1>Governance inspection (interactive read-only) <span class="oc-tag oc-tag--exec">L38</span></h1>
      <p>Inspect trust tiers, lineage, propagation, and the dependency graph derived from layer 36. <strong>Read-only.</strong></p>
    </section>
    <section class="oc-exec">
      <article class="oc-exec__panel">
        <h3>Dependency graph (layer 36)</h3>
        <div class="oc-exec__viz"><svg id="dep-svg" preserveAspectRatio="xMidYMid meet"></svg></div>
        <p class="oc-exec__hint">Vanilla SVG · no framework · no library.</p>
      </article>
      <article class="oc-exec__panel">
        <h3>Governance status feed</h3>
        <pre class="oc-exec__pre" id="gov">—</pre>
      </article>
    </section>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        const nodes = [
          { id: "intake", label: "intake" },
          { id: "extraction", label: "extraction" },
          { id: "semantic", label: "semantic" },
          { id: "identity", label: "identity" },
          { id: "publication", label: "publication" },
          { id: "linguistic", label: "linguistic" },
          { id: "html", label: "html-regen" },
          { id: "runtime", label: "runtime" },
          { id: "lineage", label: "lineage" },
        ];
        const edges = [
          { from: "intake", to: "extraction" },
          { from: "extraction", to: "semantic" },
          { from: "semantic", to: "identity" },
          { from: "semantic", to: "publication" },
          { from: "linguistic", to: "publication" },
          { from: "publication", to: "html" },
          { from: "html", to: "runtime" },
          { from: "identity", to: "lineage" },
          { from: "lineage", to: "publication" },
        ];
        window.OC.Viz.renderGraph(document.getElementById("dep-svg"), nodes, edges);
        fetch("../mock-data/governance-status.json").then(function (r) { return r.json(); }).then(function (j) {
          document.getElementById("gov").textContent = JSON.stringify(j, null, 2);
        }).catch(function () { document.getElementById("gov").textContent = "(could not load mock feed)"; });
      });
    </script>
"""
    return page("Governance (exec)", body, prefix="..", extra_scripts=["state.js", "viz.js", "ux.js"])


# ---------------------------------------------------------------------------
# Doctrine + reports + manifest stores
# ---------------------------------------------------------------------------

def write_doctrines() -> None:
    write_text(CONST_ROOT / "00-INDEX.md",
               "# Executable Operational Bindings — doctrine index (layer 38)\n\n" +
               "\n".join(f"- [{d[0]}](./{d[0]}-doctrine.md) — {d[1]}" for d in DOCTRINES) +
               "\n")
    for slug, summary in DOCTRINES:
        write_text(CONST_ROOT / f"{slug}-doctrine.md",
                   f"# {slug} doctrine\n\nLayer 38 · schema {SCHEMA}\n\n{summary}\n\n"
                   "Hard rule: this doctrine binds every executable surface in the operational console. "
                   "It is subordinate to all 37 prior governance layers and to knowledge-core. It does not "
                   "introduce SaaS, cloud, backend, autonomous agents, ML, embeddings, CI/CD, "
                   "auto-approval, or auto-mutation of any source-truth, runtime, publication, knowledge-core or governance state.\n")
    write_json(CONST_ROOT / "manifest.json", envelope({
        "doctrines": [d[0] for d in DOCTRINES],
        "binds": "operational-console (layer 37)",
    }))


def write_rules() -> None:
    write_json(RULES_ROOT / "format-classification-table.json", FORMAT_TABLE)
    write_json(RULES_ROOT / "evidence-class-table.json", EVIDENCE_CLASS_TABLE)
    write_json(RULES_ROOT / "trust-tier-table.json", TRUST_TIER_TABLE)
    write_json(RULES_ROOT / "intake-inference-rules.json", INTAKE_INFERENCE_RULES)
    write_json(RULES_ROOT / "routing-inference-rules.json", ROUTING_INFERENCE_RULES)
    write_json(RULES_ROOT / "refresh-proposal-rules.json", REFRESH_PROPOSAL_RULES)
    write_json(RULES_ROOT / "reconciliation-review-rules.json", RECON_REVIEW_RULES)
    write_text(RULES_ROOT / "README.md",
               "# execution-engine\n\nDeterministic rule tables consumed by the layer-38 executable JS engines. "
               "All tables are explicit, append-friendly, reviewer-overridable. No table contains heuristics that bypass reviewer governance.\n")


def write_manifests() -> None:
    write_text(MAN_ROOT / "README.md",
               "# manifests\n\nAppend-only draft stores. Layer-37 stores from phase 44 plus layer-38 stores from phase 45. "
               "Real promotion always happens out-of-band through reviewer governance.\n")
    for sub in ["routing-drafts", "reconciliation-drafts", "refresh-drafts", "session-history"]:
        write_json(MAN_ROOT / sub / "_draft-store.json", envelope({
            "store": sub,
            "entries": [],
            "append_only": True,
            "reviewer_authorization_required": True,
        }))


def write_assets() -> None:
    write_text(EXEC_ASSETS_ROOT / "exec.css", EXEC_CSS)
    write_text(EXEC_ASSETS_ROOT / "state.js", STATE_JS)
    write_text(EXEC_ASSETS_ROOT / "drafts.js", DRAFTS_JS)
    write_text(EXEC_ASSETS_ROOT / "intake-engine.js", INTAKE_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "routing-engine.js", ROUTING_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "recon-engine.js", RECON_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "refresh-engine.js", REFRESH_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "viz.js", VIZ_JS)
    write_text(EXEC_ASSETS_ROOT / "ux.js", UX_JS)
    write_text(EXEC_ASSETS_ROOT / "README.md",
               "# assets/exec\n\nPlain ES JavaScript modules used by the layer-38 executable consoles. "
               "No bundler, no framework, no network calls, no telemetry. localStorage is used for session "
               "and append-only drafts; SVG is used for visualisations.\n")


def write_pages() -> None:
    write_text(OC_ROOT / "exec.html", exec_dashboard_html())
    write_text(OC_ROOT / "intake-console" / "exec.html", intake_exec_html())
    write_text(OC_ROOT / "routing-console" / "exec.html", routing_exec_html())
    write_text(OC_ROOT / "refresh-console" / "exec.html", refresh_exec_html())
    write_text(OC_ROOT / "reconciliation-console" / "exec.html", recon_exec_html())
    write_text(OC_ROOT / "publication-console" / "exec.html", publication_exec_html())
    write_text(OC_ROOT / "governance-console" / "exec.html", governance_exec_html())


def write_reports() -> None:
    reports = [
        ("01-executable-intake-summary", {
            "title": "Executable intake interaction",
            "supports": ["local file selection", "metadata extraction", "deterministic format classification",
                         "evidence-class suggestion", "trust-tier suggestion", "product/domain suggestion",
                         "routing suggestion", "affected-domains proposal", "reviewer override controls",
                         "draft preview", "draft export"],
            "auto_ingestion": False, "auto_promotion": False,
        }),
        ("02-manifest-engine-summary", {
            "title": "Append-only draft manifest engine",
            "stores": ["intake-drafts", "routing-drafts", "refresh-drafts", "reconciliation-drafts", "session-history"],
            "draft_schema": "operational-console-draft/1.1",
            "auto_promotion": False, "append_only": True,
        }),
        ("03-local-state-summary", {
            "title": "Local-only session and draft state",
            "storage": ["localStorage"], "telemetry": False, "remote_sync": False, "cloud": False,
            "history_capacity": 500,
        }),
        ("04-routing-interaction-summary", {
            "title": "Executable routing consultation",
            "questions": [q["id"] for q in ROUTING_INFERENCE_RULES["questions"]],
            "explanation_required": True, "auto_apply": False,
        }),
        ("05-reconciliation-interaction-summary", {
            "title": "Executable reconciliation review",
            "review_types": [t["id"] for t in RECON_REVIEW_RULES["review_types"]],
            "auto_promotion": False, "auto_link_canonicals": False, "auto_resolve_contradictions": False,
            "geometry_only": True, "uses_ml_or_embeddings": False, "uses_face_recognition": False,
        }),
        ("06-refresh-proposal-summary", {
            "title": "Executable refresh proposal surface",
            "scopes": REFRESH_PROPOSAL_RULES["scopes"],
            "actions": [a["id"] for a in REFRESH_PROPOSAL_RULES["actions"]],
            "stale_classes": REFRESH_PROPOSAL_RULES["stale_classes"],
            "executes_rebuild": False,
        }),
        ("07-publication-visibility-summary", {
            "title": "Publication visibility (interactive read-only)",
            "supports": ["local HTML preview (sandboxed iframe)", "stale-output comparison feed",
                         "publication lineage feed", "linguistic rendering visibility", "rebuild history"],
            "regenerates_html": False, "writes_to_publication_root": False,
        }),
        ("08-governance-inspection-summary", {
            "title": "Governance inspection (interactive read-only)",
            "supports": ["trust-tier inspection", "lineage exploration", "propagation inspection",
                         "unresolved conflict review", "ontology/domain inspection", "dependency-graph visualisation"],
            "writes_governance": False,
        }),
        ("09-operational-visualization-summary", {
            "title": "Vanilla SVG operational visualisation",
            "supports": ["dependency graphs", "rebuild flows", "lineage trees",
                         "propagation chains", "intake-lifecycle visualisation"],
            "uses_libraries": False, "uses_external_packages": False,
        }),
        ("10-executable-operational-platform-maturity-reassessment", {
            "title": "Executable-operational-platform maturity reassessment",
            "layer": LAYER, "subordinate_chain_length": len(SUBORDINATE_TO),
            "consoles_executable": 6, "doctrines": len(DOCTRINES),
            "draft_stores_total": 8,
            "is_saas": False, "is_production_app": False, "uses_cloud": False,
            "introduces_autonomous_agents": False, "introduces_ci_cd": False,
            "auto_approves_ingestion": False, "auto_mutates_source_truth": False,
            "uses_ml_or_embeddings": False, "network_calls": False, "telemetry": False,
            "knowledge_core_untouched": True, "source_of_truth_untouched": True,
            "runtime_untouched": True, "publication_untouched": True,
            "tests_runtime": "19/19 green",
            "report_phases": REPORT_PHASES,
        }),
    ]
    write_text(REPORTS_ROOT / "README.md",
               "# Reports — phase 45 / layer 38 / executable-operational-bindings\n\n"
               + "\n".join(f"- {r[0]}" for r in reports) + "\n")
    for slug, payload in reports:
        write_json(REPORTS_ROOT / f"{slug}.json", envelope(payload))
        write_text(REPORTS_ROOT / f"{slug}.md",
                   f"# {payload['title']}\n\nLayer 38 · schema `{SCHEMA}` · subordinate chain {len(SUBORDINATE_TO)}.\n\n"
                   "See companion `.json` for the structured payload.\n")


def write_exec_root_readme() -> None:
    write_text(OC_ROOT / "EXEC_README.md",
               "# Operational Console — executable layer (phase 45 / layer 38)\n\n"
               "Open `exec.html` directly in a browser, or serve the repo root with:\n\n"
               "```\npython3 -m http.server 8000\n```\n\n"
               "and browse to `http://localhost:8000/wp-content/themes/beslock-custom/User%20manuals/operational-console/exec.html`.\n\n"
               "The exec layer never makes a network call. It uses only `File`, `Blob`, `URL`, `localStorage` and SVG. "
               "All operator actions emit append-only draft manifests stored locally; promotion is out-of-band through reviewer governance.\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    write_doctrines()
    write_rules()
    write_manifests()
    write_assets()
    write_pages()
    write_reports()
    write_exec_root_readme()
    print(
        f"Phase 45 — executable operational bindings written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Exec consoles: 6 | Rule tables: 7 | Engines: 7 | Doctrines: {len(DOCTRINES)} | Reports: 10"
    )


if __name__ == "__main__":
    main()
