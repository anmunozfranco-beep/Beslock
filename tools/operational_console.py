"""
Phase 44 — HUMAN GOVERNED KNOWLEDGE OPERATIONS CONSOLE.

Constitutional layer 37. Modeling-only / interface-only. Subordinate to
knowledge-core and to all thirty-six prior governance layers (in particular
layer 36 runtime-orchestration, layer 35 identity-resolution, layer 34
semantic-domain, layer 33 intake-and-navigation, layer 32 multimodal evidence).

This phase introduces the FIRST human-operable interface layer: a lightweight,
repo-native, governance-first operational console rendered as static HTML/CSS/JS
files. It is NOT a SaaS, NOT a production web app, NOT a cloud architecture
and NOT a backend.

Writes (idempotent, non-destructive, stdlib-only) under
wp-content/themes/beslock-custom/User manuals/operational-console/:

  index.html                    (dashboard linking every console)
  architecture/                 (canonical structure + design principles)
  assets/                       (console.css, console.js)
  shared/                       (header partial + nav-config + footer)
  intake-console/               (12-step evidence intake workflow page)
  routing-console/              (routing consultation workflow page)
  refresh-console/              (refresh-approval workflow page)
  reconciliation-console/       (identity reconciliation review page)
  publication-console/          (publication & output visibility page)
  governance-console/           (governance & safety visibility page)
  reports-console/              (governance reports browsing page)
  manifests/                    (draft manifest stores -- empty append-only)
  mock-data/                    (declarative JSON consumed by the static JS)
  future-expansion-readiness.json

Plus:
  KNOWLEDGE_BUILDING/OPERATIONAL_CONSOLE_GOVERNANCE/ (00-INDEX + 8 doctrines + manifest)
  _repository-governance/reports/operational-console/ (10 reports .json + .md)

Hard rules (still enforced):
  - Mutates no knowledge-core, no source-of-truth, no runtime, no publication.
  - No CI/CD, no autonomous agents, no ML, no embeddings, no prompts, no images.
  - No SaaS, no cloud architecture, no production backend.
  - The console NEVER auto-approves, NEVER auto-mutates, NEVER bypasses reviewer.
  - Every operator action is modelled as a *draft* manifest only; nothing is
    ever executed automatically. Real promotion still requires reviewer
    authorization through an out-of-band protocol.
  - JS is plain ES, no build pipeline, no dependencies, no network calls.
  - 19/19 runtime tests must remain green.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

OC_ROOT = THEME_ROOT / "operational-console"
ARCH_ROOT = OC_ROOT / "architecture"
ASSETS_ROOT = OC_ROOT / "assets"
SHARED_ROOT = OC_ROOT / "shared"
INTAKE_ROOT = OC_ROOT / "intake-console"
ROUTING_ROOT = OC_ROOT / "routing-console"
REFRESH_ROOT = OC_ROOT / "refresh-console"
RECON_ROOT = OC_ROOT / "reconciliation-console"
PUB_ROOT = OC_ROOT / "publication-console"
GOV_ROOT = OC_ROOT / "governance-console"
REPORTS_ROOT_UI = OC_ROOT / "reports-console"
MAN_ROOT = OC_ROOT / "manifests"
MOCK_ROOT = OC_ROOT / "mock-data"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "OPERATIONAL_CONSOLE_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "operational-console"

SCHEMA = "operational-console-governance/1.0"
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
    "runtime-orchestration-governance",
]

PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def envelope(extra: dict) -> dict:
    base = {
        "schema": SCHEMA,
        "constitutional_layer_index": 37,
        "subordinate_to": SUBORDINATE_TO,
        "updated_at": NOW,
        "executable": False,
        "is_saas": False,
        "is_production_app": False,
        "uses_cloud": False,
        "introduces_autonomous_agents": False,
        "introduces_ci_cd": False,
        "auto_approves_ingestion": False,
        "auto_mutates_source_truth": False,
        "bypasses_reviewer_governance": False,
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
# HTML scaffold helpers
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("../index.html", "Dashboard"),
    ("../intake-console/index.html", "Intake"),
    ("../routing-console/index.html", "Routing"),
    ("../refresh-console/index.html", "Refresh"),
    ("../reconciliation-console/index.html", "Reconciliation"),
    ("../publication-console/index.html", "Publication"),
    ("../governance-console/index.html", "Governance"),
    ("../reports-console/index.html", "Reports"),
]


def render_nav(prefix: str) -> str:
    parts = []
    for href, label in NAV_ITEMS:
        if prefix == ".":
            href = href.replace("../", "")
            if label == "Dashboard":
                href = "index.html"
        parts.append(f'      <a class="oc-nav__item" href="{href}">{label}</a>')
    return "\n".join(parts)


def page(title: str, body: str, *, css_prefix: str = "../assets",
         js_prefix: str = "../assets", nav_prefix: str = "..") -> str:
    nav = render_nav(nav_prefix)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Beslock Operational Console</title>
  <link rel="stylesheet" href="{css_prefix}/console.css" />
  <meta name="governance-layer" content="37" />
  <meta name="governance-schema" content="{SCHEMA}" />
  <meta name="reviewer-required" content="true" />
  <meta name="auto-approval" content="false" />
</head>
<body class="oc-body">
  <header class="oc-header">
    <div class="oc-header__brand">Beslock · Operational Console</div>
    <nav class="oc-nav">
{nav}
    </nav>
    <div class="oc-header__badge" title="Governance layer 37 — modeling-only">L37</div>
  </header>
  <main class="oc-main">
{body}
  </main>
  <footer class="oc-footer">
    <span>Repo-native · Local-first · Governance-first · Reviewer-required</span>
    <span>No SaaS · No cloud · No autonomous agents · No auto-approval</span>
  </footer>
  <script src="{js_prefix}/console.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Architecture
# ---------------------------------------------------------------------------

def task_architecture() -> None:
    write_text(ARCH_ROOT / "README.md", (
        "# Operational console architecture\n\n"
        "Canonical structure for the repo-native human-governed knowledge\n"
        "operations console. Lightweight HTML/CSS/JS only. Local-first.\n"
        "Governance-first. Deterministic. Audit-friendly. No cloud, no\n"
        "production backend, no SaaS.\n"
    ))
    write_json(ARCH_ROOT / "architecture.json", envelope({
        "id": "operational-console-architecture",
        "topology": [
            "operational-console/index.html",
            "operational-console/assets/",
            "operational-console/shared/",
            "operational-console/intake-console/",
            "operational-console/routing-console/",
            "operational-console/refresh-console/",
            "operational-console/reconciliation-console/",
            "operational-console/publication-console/",
            "operational-console/governance-console/",
            "operational-console/reports-console/",
            "operational-console/manifests/",
            "operational-console/mock-data/",
        ],
        "delivery_model": "static-files-opened-locally",
        "transport": "file:// or any static HTTP server",
        "build_pipeline": None,
        "dependencies": [],
        "network_calls": False,
        "service_workers": False,
        "cookies": False,
        "telemetry": False,
        "consoles": [
            "intake", "routing", "refresh", "reconciliation",
            "publication", "governance", "reports",
        ],
    }))
    write_json(ARCH_ROOT / "design-principles.json", envelope({
        "id": "operational-console-design-principles",
        "principles": [
            {"id": "lightweight", "rule": "HTML/CSS/JS only; no framework, no bundler."},
            {"id": "local-first", "rule": "Opens from disk; no server required."},
            {"id": "governance-first", "rule": "Every action is modelled as a draft manifest; reviewer authorization is always required for promotion."},
            {"id": "deterministic", "rule": "Same input → same rendered view; no randomness, no clock-dependent layout."},
            {"id": "audit-friendly", "rule": "Every operator action surfaces the exact JSON payload that would be sent to governance."},
            {"id": "no-cloud", "rule": "No fetch() to remote hosts; no third-party CDN; no analytics."},
            {"id": "no-backend", "rule": "No persistent server-side state; manifest stores are append-only JSON files in the repo."},
            {"id": "no-auto-approval", "rule": "The UI cannot promote, mutate, or publish; it only proposes."},
            {"id": "non-mutation", "rule": "The console never writes into knowledge-core, source-of-truth, runtime, or publication."},
            {"id": "transparency", "rule": "Every screen exposes the governance layer, schema, and the exact subordinate chain."},
        ],
    }))
    write_json(ARCH_ROOT / "interaction-model.json", envelope({
        "id": "operational-console-interaction-model",
        "operator_actions": [
            "view", "classify", "re-evaluate", "override-with-justification",
            "propose-routing", "propose-refresh", "propose-reconciliation",
            "request-reviewer-authorization",
        ],
        "actions_that_mutate_governance": [],
        "actions_that_emit_drafts": [
            "propose-routing", "propose-refresh", "propose-reconciliation",
            "request-reviewer-authorization",
        ],
        "draft_destination": "operational-console/manifests/",
        "promotion_path": "out-of-band reviewer protocol",
    }))


# ---------------------------------------------------------------------------
# Assets (CSS + JS)
# ---------------------------------------------------------------------------

CSS = """/* Beslock Operational Console — layer 37 — modeling-only */
:root {
  --oc-bg: #0f1115;
  --oc-panel: #161a22;
  --oc-panel-2: #1d2330;
  --oc-border: #2a3142;
  --oc-text: #e6e9ef;
  --oc-text-dim: #9aa3b2;
  --oc-accent: #4f8cff;
  --oc-warn: #ffb454;
  --oc-danger: #ff6b6b;
  --oc-ok: #4fd1a5;
  --oc-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
.oc-body {
  background: var(--oc-bg);
  color: var(--oc-text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  min-height: 100vh;
  display: flex; flex-direction: column;
}
.oc-header {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.75rem 1.25rem;
  background: var(--oc-panel);
  border-bottom: 1px solid var(--oc-border);
}
.oc-header__brand { font-weight: 600; letter-spacing: 0.02em; }
.oc-nav { display: flex; flex-wrap: wrap; gap: 0.25rem; flex: 1; }
.oc-nav__item {
  color: var(--oc-text-dim); text-decoration: none;
  padding: 0.35rem 0.7rem; border-radius: 6px; font-size: 0.9rem;
}
.oc-nav__item:hover { background: var(--oc-panel-2); color: var(--oc-text); }
.oc-header__badge {
  background: var(--oc-panel-2); color: var(--oc-accent);
  padding: 0.25rem 0.55rem; border-radius: 999px;
  font-family: var(--oc-mono); font-size: 0.75rem;
  border: 1px solid var(--oc-border);
}
.oc-main { flex: 1; padding: 1.5rem; max-width: 1280px; width: 100%; margin: 0 auto; }
.oc-footer {
  display: flex; justify-content: space-between; gap: 1rem;
  padding: 0.75rem 1.25rem; font-size: 0.75rem; color: var(--oc-text-dim);
  background: var(--oc-panel); border-top: 1px solid var(--oc-border);
}
h1, h2, h3 { color: var(--oc-text); margin: 0 0 0.5rem; }
h1 { font-size: 1.5rem; } h2 { font-size: 1.15rem; } h3 { font-size: 1rem; }
p { color: var(--oc-text-dim); line-height: 1.5; }
.oc-grid { display: grid; gap: 1rem; }
.oc-grid--3 { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.oc-grid--2 { grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); }
.oc-card {
  background: var(--oc-panel); border: 1px solid var(--oc-border);
  border-radius: 8px; padding: 1rem;
}
.oc-card__title { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.oc-tag {
  display: inline-block; padding: 0.1rem 0.45rem; border-radius: 999px;
  font-family: var(--oc-mono); font-size: 0.7rem;
  background: var(--oc-panel-2); color: var(--oc-text-dim);
  border: 1px solid var(--oc-border);
}
.oc-tag--ok { color: var(--oc-ok); }
.oc-tag--warn { color: var(--oc-warn); }
.oc-tag--danger { color: var(--oc-danger); }
.oc-tag--accent { color: var(--oc-accent); }
.oc-list { list-style: none; padding: 0; margin: 0; }
.oc-list > li {
  padding: 0.5rem 0; border-bottom: 1px solid var(--oc-border);
  display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;
}
.oc-list > li:last-child { border-bottom: 0; }
.oc-step {
  display: grid; grid-template-columns: 2rem 1fr; gap: 0.5rem 0.75rem;
  padding: 0.6rem 0; border-bottom: 1px solid var(--oc-border);
}
.oc-step:last-child { border-bottom: 0; }
.oc-step__index {
  width: 2rem; height: 2rem; border-radius: 999px;
  background: var(--oc-panel-2); color: var(--oc-accent);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--oc-mono); font-size: 0.85rem; border: 1px solid var(--oc-border);
}
.oc-step__title { font-weight: 600; }
.oc-step__hint { color: var(--oc-text-dim); font-size: 0.85rem; }
.oc-pre {
  background: #0a0c11; border: 1px solid var(--oc-border);
  color: var(--oc-text); padding: 0.75rem; border-radius: 6px;
  font-family: var(--oc-mono); font-size: 0.78rem;
  white-space: pre-wrap; overflow-x: auto;
}
.oc-banner {
  background: var(--oc-panel-2); border-left: 3px solid var(--oc-warn);
  padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1.25rem;
  color: var(--oc-text);
}
.oc-banner--ok { border-left-color: var(--oc-ok); }
.oc-banner--danger { border-left-color: var(--oc-danger); }
.oc-section { margin-bottom: 2rem; }
.oc-meta { color: var(--oc-text-dim); font-size: 0.78rem; font-family: var(--oc-mono); }
.oc-link { color: var(--oc-accent); text-decoration: none; }
.oc-link:hover { text-decoration: underline; }
table.oc-table { width: 100%; border-collapse: collapse; }
.oc-table th, .oc-table td {
  text-align: left; padding: 0.5rem; border-bottom: 1px solid var(--oc-border);
  font-size: 0.85rem;
}
.oc-table th { color: var(--oc-text-dim); font-weight: 500; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.04em; }
"""

JS = """/* Beslock Operational Console — layer 37 — local-first, no network calls */
(function () {
  "use strict";

  // Hard rules surfaced at runtime (read by the optional banner element).
  const GOVERNANCE = {
    layer: 37,
    schema: "operational-console-governance/1.0",
    auto_approval: false,
    mutates_governance: false,
    network_calls: false,
    is_saas: false,
  };

  function loadJSON(path) {
    return fetch(path, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("Failed to load " + path);
        return r.json();
      })
      .catch(function () { return null; });
  }

  function renderList(targetId, items, formatter) {
    const el = document.getElementById(targetId);
    if (!el || !Array.isArray(items)) return;
    el.innerHTML = "";
    items.forEach(function (item) {
      const li = document.createElement("li");
      li.innerHTML = formatter(item);
      el.appendChild(li);
    });
  }

  function buildDraft(kind, payload) {
    return {
      schema: "operational-console-draft/1.0",
      constitutional_layer_index: 37,
      kind: kind,
      reviewer_authorization_required: true,
      auto_promotion: false,
      auto_mutates_source_truth: false,
      payload: payload,
      proposed_at_iso: new Date().toISOString(),
    };
  }

  function showDraft(kind, payload, targetId) {
    const draft = buildDraft(kind, payload);
    const el = document.getElementById(targetId);
    if (!el) return;
    el.textContent = JSON.stringify(draft, null, 2);
  }

  // Wire up data-driven sections per page.
  document.addEventListener("DOMContentLoaded", function () {
    const dataAttr = document.body.getAttribute("data-mock");
    if (dataAttr) {
      loadJSON(dataAttr).then(function (data) {
        if (!data) return;
        const slot = document.getElementById("oc-mock-dump");
        if (slot) slot.textContent = JSON.stringify(data, null, 2);
      });
    }

    document.querySelectorAll("[data-propose]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const kind = btn.getAttribute("data-propose");
        const target = btn.getAttribute("data-target");
        const sourceId = btn.getAttribute("data-source");
        let payload = {};
        if (sourceId) {
          const src = document.getElementById(sourceId);
          if (src) {
            try { payload = JSON.parse(src.textContent || "{}"); }
            catch (e) { payload = { raw: src.textContent }; }
          }
        }
        showDraft(kind, payload, target);
      });
    });
  });

  window.OC = { GOVERNANCE: GOVERNANCE, loadJSON: loadJSON, buildDraft: buildDraft };
})();
"""


def task_assets() -> None:
    write_text(ASSETS_ROOT / "console.css", CSS)
    write_text(ASSETS_ROOT / "console.js", JS)


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

def task_shared() -> None:
    write_json(SHARED_ROOT / "nav-config.json", envelope({
        "id": "operational-console-nav",
        "items": [{"href": h, "label": l} for h, l in NAV_ITEMS],
    }))
    write_text(SHARED_ROOT / "header.partial.html", (
        "<!-- Reference partial. Each page inlines the equivalent header. -->\n"
        "<!-- Kept for documentation; not loaded at runtime (no build pipeline). -->\n"
    ))
    write_text(SHARED_ROOT / "README.md", (
        "# Shared scaffolding\n\nNav configuration consumed by every console.\n"
        "No runtime templating engine; pages inline the header for portability.\n"
    ))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def task_dashboard() -> None:
    cards = [
        ("intake-console/index.html", "Intake", "Upload, classify, route and propose refresh for new evidence."),
        ("routing-console/index.html", "Routing", "“Where should this file go?” — consultation only, never auto-routed."),
        ("refresh-console/index.html", "Refresh", "Inspect detected changes and propose dry-run / approve / partial / reject."),
        ("reconciliation-console/index.html", "Reconciliation", "Review OEM ↔ commercial mappings, aliases and visual identity matches."),
        ("publication-console/index.html", "Publication", "Visibility into generated HTML, stale outputs and publication lineage."),
        ("governance-console/index.html", "Governance", "Trust levels, propagation warnings, lineage integrity, governance conflicts."),
        ("reports-console/index.html", "Reports", "Browse all governance reports across thirty-seven layers."),
    ]
    body = (
        '    <section class="oc-section">\n'
        '      <h1>Human Governed Knowledge Operations Console</h1>\n'
        '      <p>Repo-native, local-first, reviewer-authoritative. The console proposes; reviewers decide.</p>\n'
        '    </section>\n'
        '    <div class="oc-banner">'
        'This console is <strong>modeling-only</strong>. Every action emits a <em>draft manifest</em>; '
        'no governance state, source-of-truth, runtime or publication is ever mutated from the UI.'
        '</div>\n'
        '    <section class="oc-grid oc-grid--3">\n'
    )
    for href, title, desc in cards:
        body += (
            f'      <article class="oc-card">\n'
            f'        <div class="oc-card__title"><h2>{title}</h2><span class="oc-tag oc-tag--accent">L37</span></div>\n'
            f'        <p>{desc}</p>\n'
            f'        <p><a class="oc-link" href="{href}">Open {title} →</a></p>\n'
            f'      </article>\n'
        )
    body += '    </section>\n'
    body += (
        '    <section class="oc-section">\n'
        '      <h2>Governance posture</h2>\n'
        '      <ul class="oc-list">\n'
        '        <li>Layer <span class="oc-tag oc-tag--accent">37</span></li>\n'
        '        <li>Subordinate chain length <span class="oc-tag">36</span></li>\n'
        '        <li>Auto-approval <span class="oc-tag oc-tag--ok">disabled</span></li>\n'
        '        <li>Source-truth mutation <span class="oc-tag oc-tag--ok">forbidden</span></li>\n'
        '        <li>Network calls <span class="oc-tag oc-tag--ok">none</span></li>\n'
        '        <li>Reviewer authorization <span class="oc-tag oc-tag--warn">required for every promotion</span></li>\n'
        '      </ul>\n'
        '    </section>\n'
    )
    write_text(OC_ROOT / "index.html", page(
        "Dashboard", body,
        css_prefix="assets", js_prefix="assets", nav_prefix=".",
    ))
    write_text(OC_ROOT / "README.md", (
        "# Operational Console (layer 37)\n\n"
        "Open `index.html` in any browser (file:// works) to launch the console.\n"
        "All consoles are static HTML/CSS/JS. No build, no server, no network.\n"
    ))


# ---------------------------------------------------------------------------
# Intake console
# ---------------------------------------------------------------------------

INTAKE_FORMATS = [
    {"id": "pdf", "label": "PDF", "evidence_class_default": "official-document"},
    {"id": "xlsx", "label": "XLSX", "evidence_class_default": "structured-spreadsheet"},
    {"id": "csv", "label": "CSV", "evidence_class_default": "structured-spreadsheet"},
    {"id": "json", "label": "JSON", "evidence_class_default": "structured-data"},
    {"id": "png", "label": "PNG", "evidence_class_default": "raster-image"},
    {"id": "jpg", "label": "JPG", "evidence_class_default": "raster-image"},
    {"id": "webp", "label": "WebP", "evidence_class_default": "raster-image"},
    {"id": "mp4", "label": "MP4", "evidence_class_default": "video-evidence"},
    {"id": "mov", "label": "MOV", "evidence_class_default": "video-evidence"},
    {"id": "zip", "label": "ZIP", "evidence_class_default": "bundle-archive"},
    {"id": "docx", "label": "DOCX", "evidence_class_default": "narrative-document"},
]

INTAKE_STEPS = [
    ("upload-document", "Upload document", "Operator selects a local file. The console reads filename + size only."),
    ("detect-format", "Detect format", "MIME / extension inferred deterministically; no content parsing."),
    ("infer-evidence-class", "Infer evidence class", "Default class proposed from layer-32 evidence taxonomy; operator can override."),
    ("infer-product-scope", "Infer product scope", "Suggested e-orbit/e-prime/e-flex/e-touch/e-shield/e-nova/portfolio-level."),
    ("infer-trust-level", "Infer trust level", "Default trust tier from layer-33 trust rules; never auto-promoted."),
    ("suggest-routing", "Suggest routing destination", "Layer-33 routing-policy lookup; operator confirms."),
    ("suggest-affected-domains", "Suggest affected domains/products", "Layer-34 domain map + layer-35 identity links."),
    ("operator-re-evaluation", "Operator re-evaluation", "Operator may revise any inferred field with a reason field."),
    ("operator-override", "Operator override", "Override is recorded as part of the draft manifest, not silently applied."),
    ("confirm-ingestion", "Confirm ingestion", "Emits an intake-draft manifest; nothing ingested yet."),
    ("propose-refresh-plan", "Propose refresh plan", "Layer-36 pipelines proposed for downstream invalidation."),
    ("approve-or-skip-refresh", "Approve or skip refresh", "Reviewer authorization required for promotion; the console only proposes."),
]


def task_intake_console() -> None:
    workflow = envelope({
        "id": "intake-workflow",
        "supported_formats": INTAKE_FORMATS,
        "steps": [
            {"index": i + 1, "id": s[0], "title": s[1], "hint": s[2]}
            for i, s in enumerate(INTAKE_STEPS)
        ],
        "emits_draft_manifests_to": "operational-console/manifests/intake-drafts/",
        "promotion_path": "out-of-band reviewer protocol",
    })
    write_json(INTAKE_ROOT / "workflow.json", workflow)

    body = '    <section class="oc-section">\n'
    body += '      <h1>Evidence Intake</h1>\n'
    body += '      <p>Twelve-step governed intake workflow. Every step is a proposal; nothing is committed automatically.</p>\n'
    body += '    </section>\n'
    body += '    <div class="oc-banner">'
    body += 'Reviewer authorization is required for promotion. The console only emits an <em>intake-draft</em> manifest.</div>\n'
    body += '    <section class="oc-section oc-card">\n      <h2>Workflow</h2>\n'
    for i, (sid, title, hint) in enumerate(INTAKE_STEPS, start=1):
        body += (
            f'      <div class="oc-step">\n'
            f'        <div class="oc-step__index">{i:02d}</div>\n'
            f'        <div>\n'
            f'          <div class="oc-step__title">{title} <span class="oc-tag">{sid}</span></div>\n'
            f'          <div class="oc-step__hint">{hint}</div>\n'
            f'        </div>\n'
            f'      </div>\n'
        )
    body += '    </section>\n'
    body += '    <section class="oc-grid oc-grid--2">\n'
    body += '      <article class="oc-card">\n        <h2>Supported formats</h2>\n        <ul class="oc-list">\n'
    for fmt in INTAKE_FORMATS:
        body += (
            f'          <li><span>{fmt["label"]}</span>'
            f'<span class="oc-tag oc-tag--accent">{fmt["evidence_class_default"]}</span></li>\n'
        )
    body += '        </ul>\n      </article>\n'
    body += '      <article class="oc-card">\n        <h2>Pending intake (mock)</h2>\n        <pre id="oc-mock-dump" class="oc-pre">loading…</pre>\n      </article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card">\n'
    body += '      <h2>Proposed intake-draft</h2>\n'
    body += '      <p>Click below to render the JSON payload that would be filed under <code>manifests/intake-drafts/</code>. Promotion still requires a reviewer.</p>\n'
    body += '      <button data-propose="intake-draft" data-target="oc-intake-draft" data-source="oc-mock-dump">Propose intake-draft</button>\n'
    body += '      <pre id="oc-intake-draft" class="oc-pre">// nothing proposed yet</pre>\n'
    body += '    </section>\n'

    html = page("Intake", body)
    html = html.replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/pending-intake.json">')
    write_text(INTAKE_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Routing console
# ---------------------------------------------------------------------------

ROUTING_QUESTIONS = [
    {"id": "where-does-this-file-go", "operator_question": "Where should this file go?",
     "console_response_kind": "suggested-destination"},
    {"id": "what-class-of-evidence", "operator_question": "What class of evidence is this?",
     "console_response_kind": "evidence-classification"},
    {"id": "trust-tier", "operator_question": "What trust tier should this carry?",
     "console_response_kind": "trust-tier"},
    {"id": "operational-role", "operator_question": "What is the operational role of this evidence?",
     "console_response_kind": "operational-role"},
    {"id": "downstream-impact", "operator_question": "What downstream domains/products are affected?",
     "console_response_kind": "downstream-impact"},
    {"id": "refresh-impact", "operator_question": "Will this trigger a refresh?",
     "console_response_kind": "refresh-impact"},
]


def task_routing_console() -> None:
    write_json(ROUTING_ROOT / "routing-questions.json", envelope({
        "id": "routing-consultation-questions",
        "questions": ROUTING_QUESTIONS,
        "all_responses_are_proposals": True,
        "operator_can_reject_every_suggestion": True,
    }))
    body = '    <section class="oc-section"><h1>Routing Consultation</h1>\n'
    body += '      <p>“I have this file — where should it go?” The console proposes; the operator decides; reviewer authorizes any cross-canonical move.</p></section>\n'
    body += '    <div class="oc-banner">Routing suggestions are <strong>advisory</strong>. The console never moves files automatically.</div>\n'
    body += '    <section class="oc-grid oc-grid--2">\n'
    body += '      <article class="oc-card"><h2>Operator questions</h2><ul class="oc-list">\n'
    for q in ROUTING_QUESTIONS:
        body += f'        <li><span>{q["operator_question"]}</span><span class="oc-tag oc-tag--accent">{q["console_response_kind"]}</span></li>\n'
    body += '      </ul></article>\n'
    body += '      <article class="oc-card"><h2>Routing suggestions (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card">\n      <h2>Propose routing consultation</h2>\n'
    body += '      <button data-propose="routing-consultation" data-target="oc-routing-draft" data-source="oc-mock-dump">Propose routing-consultation</button>\n'
    body += '      <pre id="oc-routing-draft" class="oc-pre">// nothing proposed yet</pre>\n    </section>\n'
    html = page("Routing", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/routing-suggestions.json">')
    write_text(ROUTING_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Refresh console
# ---------------------------------------------------------------------------

REFRESH_VIEWS = [
    "detected-changes", "impacted-layers", "rebuild-plans",
    "propagation-plans", "stale-outputs", "affected-publications",
    "affected-runtime-domains",
]
REFRESH_ACTIONS = [
    {"id": "dry-run", "effect": "Preview rebuild manifest only", "mutates": False},
    {"id": "approve", "effect": "Emit refresh-approval draft for reviewer", "mutates": False},
    {"id": "reject", "effect": "Emit refresh-rejection draft", "mutates": False},
    {"id": "partial-rebuild", "effect": "Emit scoped rebuild draft (single product/domain/publication)", "mutates": False},
]


def task_refresh_console() -> None:
    write_json(REFRESH_ROOT / "approval-workflow.json", envelope({
        "id": "refresh-approval-workflow",
        "views": REFRESH_VIEWS,
        "actions": REFRESH_ACTIONS,
        "scopes": ["product", "domain", "publication", "runtime", "portfolio"],
        "auto_promotion": False,
        "every_action_requires_reviewer": True,
        "draft_destination": "operational-console/manifests/refresh-approvals/",
    }))
    body = '    <section class="oc-section"><h1>Refresh Approval</h1>\n'
    body += '      <p>Visualize detected changes, impacted layers and rebuild/propagation plans. Approve, reject or scope partial rebuilds — every action is a draft.</p></section>\n'
    body += '    <div class="oc-banner oc-banner--danger">No action on this screen executes a rebuild. All four buttons emit reviewer-bound drafts only.</div>\n'
    body += '    <section class="oc-grid oc-grid--3">\n'
    for v in REFRESH_VIEWS:
        body += f'      <article class="oc-card"><h2>{v.replace("-", " ").title()}</h2><p class="oc-meta">layer-36 dependency-graph view</p></article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card"><h2>Pending refresh (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></section>\n'
    body += '    <section class="oc-section oc-card"><h2>Operator actions</h2>\n'
    for a in REFRESH_ACTIONS:
        body += f'      <div class="oc-step"><div class="oc-step__index">·</div><div><div class="oc-step__title">{a["id"]} <span class="oc-tag oc-tag--warn">draft only</span></div><div class="oc-step__hint">{a["effect"]}</div></div></div>\n'
    body += '      <button data-propose="refresh-approval" data-target="oc-refresh-draft" data-source="oc-mock-dump">Propose refresh-approval</button>\n'
    body += '      <pre id="oc-refresh-draft" class="oc-pre">// nothing proposed yet</pre>\n    </section>\n'
    html = page("Refresh", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/pending-refresh.json">')
    write_text(REFRESH_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Reconciliation console
# ---------------------------------------------------------------------------

RECON_REVIEW_TYPES = [
    {"id": "oem-vs-commercial", "title": "OEM ↔ commercial review", "source": "layer-35 oem-mappings"},
    {"id": "alias-review", "title": "Alias review", "source": "layer-35 alias-registry"},
    {"id": "visual-reconciliation", "title": "Visual reconciliation review", "source": "layer-35 visual-identity (geometry-only, no AI)"},
    {"id": "confidence-inspection", "title": "Confidence inspection", "source": "layer-35 confidence-history"},
    {"id": "unresolved-identities", "title": "Unresolved identity handling", "source": "layer-35 unresolved-identities"},
]


def task_reconciliation_console() -> None:
    write_json(RECON_ROOT / "review-types.json", envelope({
        "id": "reconciliation-review-types",
        "types": RECON_REVIEW_TYPES,
        "auto_promotion_of_match": False,
        "no_face_recognition": True,
        "no_embeddings": True,
        "no_ml_models": True,
        "draft_destination": "operational-console/manifests/reconciliation-decisions/",
    }))
    body = '    <section class="oc-section"><h1>Identity Reconciliation</h1>\n'
    body += '      <p>Review OEM ↔ commercial pairings, aliases and visual identity matches. Reviewer attests every promotion.</p></section>\n'
    body += '    <div class="oc-banner">Visual reconciliation uses <strong>geometry features only</strong> — no AI, no embeddings, no face recognition.</div>\n'
    body += '    <section class="oc-grid oc-grid--3">\n'
    for t in RECON_REVIEW_TYPES:
        body += f'      <article class="oc-card"><h2>{t["title"]}</h2><p class="oc-meta">{t["source"]}</p></article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card"><h2>Unresolved identities (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></section>\n'
    body += '    <section class="oc-section oc-card"><h2>Propose reconciliation decision</h2>\n'
    body += '      <button data-propose="reconciliation-decision" data-target="oc-recon-draft" data-source="oc-mock-dump">Propose reconciliation-decision</button>\n'
    body += '      <pre id="oc-recon-draft" class="oc-pre">// nothing proposed yet</pre>\n    </section>\n'
    html = page("Reconciliation", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/unresolved-identities.json">')
    write_text(RECON_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Publication console
# ---------------------------------------------------------------------------

PUB_FEEDS = [
    "generated-html", "stale-outputs", "publication-lineage",
    "linguistic-rendering-status", "rebuild-history",
]


def task_publication_console() -> None:
    write_json(PUB_ROOT / "visibility-feeds.json", envelope({
        "id": "publication-visibility-feeds",
        "feeds": PUB_FEEDS,
        "writes_to_publication_root": False,
        "regenerates_html": False,
    }))
    body = '    <section class="oc-section"><h1>Publication & Output Visibility</h1>\n'
    body += '      <p>Read-only view across generated HTML, stale outputs, linguistic rendering status and rebuild history.</p></section>\n'
    body += '    <div class="oc-banner oc-banner--ok">Read-only. The console never regenerates HTML and never publishes.</div>\n'
    body += '    <section class="oc-grid oc-grid--3">\n'
    for f in PUB_FEEDS:
        body += f'      <article class="oc-card"><h2>{f.replace("-", " ").title()}</h2><p class="oc-meta">layer-36 / layer-38 read-only</p></article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card"><h2>Publications (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></section>\n'
    body += '    <section class="oc-section oc-card"><h2>Stale outputs (mock)</h2><pre id="oc-stale-dump" class="oc-pre">// loaded by JS</pre></section>\n'
    html = page("Publication", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/publications.json">')
    write_text(PUB_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Governance console
# ---------------------------------------------------------------------------

GOV_FEEDS = [
    "trust-levels", "unresolved-risks", "propagation-warnings",
    "lineage-integrity", "review-status", "candidate-status",
    "governance-conflicts",
]


def task_governance_console() -> None:
    write_json(GOV_ROOT / "safety-feeds.json", envelope({
        "id": "governance-safety-feeds",
        "feeds": GOV_FEEDS,
        "exposes_safety_rules": True,
        "writes_governance": False,
    }))
    body = '    <section class="oc-section"><h1>Governance & Safety Visibility</h1>\n'
    body += '      <p>Trust levels, unresolved risks, propagation warnings, lineage integrity, review status and governance conflicts.</p></section>\n'
    body += '    <div class="oc-banner">All counters are read from append-only governance reports. Nothing on this screen mutates governance.</div>\n'
    body += '    <section class="oc-grid oc-grid--3">\n'
    for f in GOV_FEEDS:
        body += f'      <article class="oc-card"><h2>{f.replace("-", " ").title()}</h2><p class="oc-meta">read-only</p></article>\n'
    body += '    </section>\n'
    body += '    <section class="oc-section oc-card"><h2>Governance status (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></section>\n'
    html = page("Governance", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/governance-status.json">')
    write_text(GOV_ROOT / "index.html", html)


# ---------------------------------------------------------------------------
# Reports console
# ---------------------------------------------------------------------------

REPORT_PHASES = [
    ("phase-32", "Multimodal evidence governance"),
    ("phase-33", "Intake and navigation governance"),
    ("phase-34", "Semantic domain governance"),
    ("phase-35", "Identity resolution governance"),
    ("phase-36", "Runtime orchestration governance"),
    ("phase-37", "Operational console governance"),
]


def task_reports_console() -> None:
    write_json(REPORTS_ROOT_UI / "reports-feed.json", envelope({
        "id": "reports-feed",
        "report_roots": [
            "_repository-governance/reports/multimodal-evidence/",
            "_repository-governance/reports/intake-and-navigation/",
            "_repository-governance/reports/semantic-domain/",
            "_repository-governance/reports/identity-resolution/",
            "_repository-governance/reports/runtime-orchestration/",
            "_repository-governance/reports/operational-console/",
        ],
        "writes_reports": False,
    }))
    body = '    <section class="oc-section"><h1>Governance Reports</h1>\n'
    body += '      <p>Browse all governance reports across the constitutional layers.</p></section>\n'
    body += '    <section class="oc-card"><table class="oc-table"><thead><tr><th>Phase</th><th>Title</th><th>Status</th></tr></thead><tbody>\n'
    for pid, title in REPORT_PHASES:
        body += f'      <tr><td>{pid}</td><td>{title}</td><td><span class="oc-tag oc-tag--ok">complete</span></td></tr>\n'
    body += '    </tbody></table></section>\n'
    body += '    <section class="oc-section oc-card"><h2>Reports index (mock)</h2><pre id="oc-mock-dump" class="oc-pre">loading…</pre></section>\n'
    html = page("Reports", body).replace('<body class="oc-body">', '<body class="oc-body" data-mock="../mock-data/reports-index.json">')
    write_text(REPORTS_ROOT_UI / "index.html", html)


# ---------------------------------------------------------------------------
# Manifests (draft stores -- empty append-only)
# ---------------------------------------------------------------------------

DRAFT_STORES = [
    "intake-drafts",
    "routing-consultations",
    "refresh-approvals",
    "reconciliation-decisions",
]


def task_manifests() -> None:
    write_text(MAN_ROOT / "README.md", (
        "# Operational console — draft manifests\n\n"
        "Append-only stores for proposals emitted by the console. Reviewer\n"
        "authorization (out-of-band) is required to promote any draft into\n"
        "governance. The console never auto-promotes.\n"
    ))
    for kind in DRAFT_STORES:
        write_json(MAN_ROOT / kind / "_draft-store.json", envelope({
            "id": f"{kind}-store",
            "kind": kind,
            "items": [],
            "append_only": True,
            "auto_promotion": False,
        }))


# ---------------------------------------------------------------------------
# Mock data (declarative JSON only)
# ---------------------------------------------------------------------------

def task_mock_data() -> None:
    write_json(MOCK_ROOT / "pending-intake.json", envelope({
        "id": "mock-pending-intake",
        "is_mock": True,
        "items": [
            {"filename": "e-orbit-installation.pdf", "format": "pdf", "size_bytes": 1234567,
             "suggested_evidence_class": "official-document", "suggested_scope": "e-orbit",
             "suggested_trust": "tier-2-oem", "suggested_destination": "knowledge-building/e-orbit/raw/"},
            {"filename": "portfolio-comparison.xlsx", "format": "xlsx", "size_bytes": 45678,
             "suggested_evidence_class": "structured-spreadsheet", "suggested_scope": "portfolio-level",
             "suggested_trust": "tier-3-internal", "suggested_destination": "knowledge-building/portfolio/raw/"},
        ],
    }))
    write_json(MOCK_ROOT / "routing-suggestions.json", envelope({
        "id": "mock-routing-suggestions",
        "is_mock": True,
        "examples": [
            {"file": "installer-photo.jpg", "suggested_destination": "knowledge-building/e-flex/visual-evidence/",
             "evidence_class": "raster-image", "trust_tier": "tier-4-field",
             "downstream_impact": ["e-flex/visual-identity", "publication-system/e-flex"],
             "refresh_impact": ["html-regeneration", "runtime-refresh"]},
        ],
    }))
    write_json(MOCK_ROOT / "pending-refresh.json", envelope({
        "id": "mock-pending-refresh",
        "is_mock": True,
        "detected_changes": [
            {"change_kind": "modified-evidence", "source": "e-orbit-installation.pdf",
             "downstream_invalidates": ["specifications", "warnings", "publication-html"]},
        ],
        "impacted_layers": ["32", "33", "34", "36", "publication"],
        "rebuild_plan_scope": "product",
        "propagation_plan": "in-product only (no cross-canonical)",
    }))
    write_json(MOCK_ROOT / "unresolved-identities.json", envelope({
        "id": "mock-unresolved-identities",
        "is_mock": True,
        "items": [
            {"alias": "OrbitPro 2024", "candidates": ["e-orbit"], "confidence": 0.62,
             "requires_reviewer": True, "method": "geometry-features-only"},
        ],
    }))
    write_json(MOCK_ROOT / "stale-outputs.json", envelope({
        "id": "mock-stale-outputs",
        "is_mock": True,
        "items": [
            {"path": "publication-system/e-orbit/index.html", "stale_class": "stale-html",
             "reason": "modified-evidence detected", "requires_rebuild": True},
        ],
    }))
    write_json(MOCK_ROOT / "publications.json", envelope({
        "id": "mock-publications",
        "is_mock": True,
        "products": [
            {"product": p, "pages_published": 6, "stale_pages": 0,
             "linguistic_rendering": "pending", "last_rebuild_iso": NOW}
            for p in PRODUCTS
        ],
    }))
    write_json(MOCK_ROOT / "governance-status.json", envelope({
        "id": "mock-governance-status",
        "is_mock": True,
        "trust_distribution": {"tier-1": 0, "tier-2-oem": 0, "tier-3-internal": 0, "tier-4-field": 0},
        "unresolved_risks": 7,
        "propagation_warnings": 0,
        "lineage_integrity": "ok",
        "review_status": {"pending_reviews": 0, "blocked": 0},
        "candidate_status": {"candidate-entities": 0, "promoted": 0},
        "governance_conflicts": 0,
    }))
    write_json(MOCK_ROOT / "reports-index.json", envelope({
        "id": "mock-reports-index",
        "is_mock": True,
        "phases": [{"id": pid, "title": title, "report_count": 10} for pid, title in REPORT_PHASES],
    }))


# ---------------------------------------------------------------------------
# Future-expansion-readiness
# ---------------------------------------------------------------------------

def task_future_readiness() -> None:
    write_json(OC_ROOT / "future-expansion-readiness.json", envelope({
        "id": "operational-console-future-readiness",
        "future_capabilities_declared_only": [
            "publication-generation-trigger",
            "runtime-inspection-panel",
            "semantic-propagation-review",
            "multilingual-rendering",
            "multimodal-grounding-review",
            "visual-generation-governance-panel",
            "operator-teams-and-roles",
        ],
        "implementation_status": "not-implemented",
        "requires_reviewer_authorization": True,
        "no_production_infrastructure_introduced": True,
        "no_cloud_dependencies": True,
        "no_autonomous_agents": True,
    }))


# ---------------------------------------------------------------------------
# Doctrine
# ---------------------------------------------------------------------------

DOCTRINE = [
    ("01-human-operability-doctrine.md",
     "Human operability doctrine",
     "The console exists so humans can operate governed knowledge with clarity."),
    ("02-governance-first-doctrine.md",
     "Governance-first doctrine",
     "Every UI affordance defers to governance; no action ever bypasses reviewers."),
    ("03-non-mutation-doctrine.md",
     "Non-mutation doctrine",
     "The console never writes into knowledge-core, source-of-truth, runtime or publication."),
    ("04-non-execution-doctrine.md",
     "Non-execution doctrine",
     "The console emits drafts only; rebuilds, refreshes and propagations are out-of-band."),
    ("05-local-first-doctrine.md",
     "Local-first doctrine",
     "Static HTML/CSS/JS opens from disk; no network calls, no telemetry, no CDN."),
    ("06-determinism-doctrine.md",
     "Determinism doctrine",
     "Same mock data → same rendered view. No randomness. No clock-dependent layout."),
    ("07-audit-friendly-doctrine.md",
     "Audit-friendly doctrine",
     "Every operator action surfaces the JSON payload that would be filed under manifests/."),
    ("08-no-saas-doctrine.md",
     "No SaaS doctrine",
     "No cloud architecture. No multi-tenant backend. No production web app."),
]


def task_doctrine() -> None:
    write_text(CONST_ROOT / "00-INDEX.md", "# Operational Console Governance — index\n\n" + "\n".join(
        f"- [{title}]({fname})" for fname, title, _ in DOCTRINE
    ) + "\n")
    for fname, title, body in DOCTRINE:
        write_text(CONST_ROOT / fname, f"# {title}\n\n{body}\n")
    write_json(CONST_ROOT / "manifest.json", envelope({
        "id": "operational-console-governance-manifest",
        "doctrines": [{"file": f, "title": t} for f, t, _ in DOCTRINE],
    }))


# ---------------------------------------------------------------------------
# Reports (10 .json + .md)
# ---------------------------------------------------------------------------

def task_reports() -> None:
    reports = [
        ("01-operational-console-summary", {
            "consoles": ["intake", "routing", "refresh", "reconciliation",
                         "publication", "governance", "reports"],
            "delivery": "static HTML/CSS/JS, local-first",
            "build_pipeline": None, "network_calls": False,
            "auto_approval": False, "is_saas": False,
        }),
        ("02-intake-console-summary", {
            "steps": [s[0] for s in INTAKE_STEPS],
            "supported_formats": [f["id"] for f in INTAKE_FORMATS],
            "draft_destination": "operational-console/manifests/intake-drafts/",
            "auto_ingestion": False,
        }),
        ("03-routing-consultation-summary", {
            "questions": [q["id"] for q in ROUTING_QUESTIONS],
            "all_responses_are_proposals": True,
            "auto_routing": False,
        }),
        ("04-reconciliation-console-summary", {
            "review_types": [t["id"] for t in RECON_REVIEW_TYPES],
            "no_face_recognition": True, "no_embeddings": True,
            "auto_promotion_of_match": False,
        }),
        ("05-refresh-console-summary", {
            "views": REFRESH_VIEWS,
            "actions": [a["id"] for a in REFRESH_ACTIONS],
            "scopes": ["product", "domain", "publication", "runtime", "portfolio"],
            "auto_promotion": False,
        }),
        ("06-publication-visibility-summary", {
            "feeds": PUB_FEEDS,
            "writes_to_publication_root": False, "regenerates_html": False,
        }),
        ("07-governance-visibility-summary", {
            "feeds": GOV_FEEDS,
            "writes_governance": False,
        }),
        ("08-future-expansion-readiness-summary", {
            "future_capabilities_declared_only": [
                "publication-generation-trigger", "runtime-inspection-panel",
                "semantic-propagation-review", "multilingual-rendering",
                "multimodal-grounding-review", "visual-generation-governance-panel",
                "operator-teams-and-roles",
            ],
            "implementation_status": "not-implemented",
        }),
        ("09-unresolved-operational-interface-risks", {
            "risks": [
                "draft-store promotion is out-of-band — protocol not yet wired into UI",
                "operator team / role boundaries are declared but not enforced in the UI",
                "there is no built-in diff between proposed-draft and current governance state",
                "stale-output and refresh signals are visualised from mock-data; live wiring requires layer-36 emitter",
                "browser CSP is not enforced server-side (file:// has no CSP)",
                "accessibility audit (WCAG) is pending",
                "internationalisation of console copy is pending (currently mixed es/en)",
            ],
            "blocks_release": False,
        }),
        ("10-operational-platform-maturity-reassessment", {
            "layer_index": 37,
            "subordinate_chain_length": 36,
            "consoles_delivered": 7,
            "draft_stores_initialised": len(DRAFT_STORES),
            "mock_data_files": 8,
            "doctrines": len(DOCTRINE),
            "is_saas": False, "is_production_app": False, "uses_cloud": False,
            "introduces_autonomous_agents": False, "introduces_ci_cd": False,
            "auto_approves_ingestion": False, "auto_mutates_source_truth": False,
            "knowledge_core_untouched": True, "source_of_truth_untouched": True,
            "runtime_untouched": True, "publication_untouched": True,
            "tests_status": "19/19 expected green",
        }),
    ]
    for stem, payload in reports:
        write_json(REPORTS_ROOT / f"{stem}.json", envelope({"id": stem, **payload}))
        write_text(REPORTS_ROOT / f"{stem}.md",
                   f"# {stem.replace('-', ' ').title()}\n\nSee `{stem}.json`.\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    task_architecture()
    task_assets()
    task_shared()
    task_dashboard()
    task_intake_console()
    task_routing_console()
    task_refresh_console()
    task_reconciliation_console()
    task_publication_console()
    task_governance_console()
    task_reports_console()
    task_manifests()
    task_mock_data()
    task_future_readiness()
    task_doctrine()
    task_reports()
    print(
        "Phase 44 — operational console written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO) - 1}. "
        f"Consoles: 7 | Intake steps: {len(INTAKE_STEPS)} | Formats: {len(INTAKE_FORMATS)} | "
        f"Routing questions: {len(ROUTING_QUESTIONS)} | Refresh actions: {len(REFRESH_ACTIONS)} | "
        f"Recon types: {len(RECON_REVIEW_TYPES)} | Doctrines: {len(DOCTRINE)}"
    )


if __name__ == "__main__":
    main()
