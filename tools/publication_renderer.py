"""
Phase 36 — FIRST GOVERNED PUBLICATION RENDERING.

Constitutional position: subordinate to knowledge-core + 29 prior governance
layers. EXECUTABLE, NOT a new doctrine layer.

Reads (read-only) the per-product knowledge-core under
  `wp-content/themes/beslock-custom/User manuals/ext-images/<product>/knowledge-core/`
and renders human-consumable HTML publication previews under
  `wp-content/themes/beslock-custom/User manuals/publication-system/generated-publications/<product>/`
plus a navigation index at
  `wp-content/themes/beslock-custom/User manuals/publication-system/generated-publications/Product_Manuals.html`
plus 8 reports under
  `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/publication-rendering/`.

Hard rules upheld:
  - text-first only; no images generated; no prompts generated; ComfyUI not invoked
  - knowledge-core is the ONLY source of truth (renderer adds form, never content)
  - publications are RENDERED VIEWS, never an independent knowledge authority
  - lineage + confidence + provenance disclosed on every rendered surface
  - idempotent, deterministic; non-destructive (overwrites only its own outputs)
  - touches no runtime code; runtime test suite must remain green (19/19)
  - audience filter not applied here (single rendering profile = reviewer-preview)
"""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
EXT_IMAGES_ROOT = THEME_ROOT / "ext-images"
PUB_SYS_ROOT = THEME_ROOT / "publication-system"
GENERATED_ROOT = PUB_SYS_ROOT / "generated-publications"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "publication-rendering"

SCHEMA = "publication-rendering/1.0"
RENDERER_ID = "publication-renderer-textfirst"
RENDERER_VERSION = "1.0.0"
TARGET_PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]
PRIMARY_PRODUCTS = ["e-orbit", "e-prime"]  # full rendering required by phase brief
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")

SUBORDINATE_TO = [
    "knowledge-core/1.0",
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
# IO helpers (idempotent, deterministic)
# ---------------------------------------------------------------------------

def read_json(p: Path) -> Optional[Dict[str, Any]]:
    try:
        with p.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_text(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def write_json(p: Path, payload: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def esc(s: Any) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def list_json_files(d: Path) -> List[Path]:
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.json") if p.is_file())


# ---------------------------------------------------------------------------
# Knowledge-core loader (read-only)
# ---------------------------------------------------------------------------

def load_knowledge_core(product: str) -> Dict[str, Any]:
    kc = EXT_IMAGES_ROOT / product / "knowledge-core"
    bundle: Dict[str, Any] = {
        "product": product,
        "knowledge_core_path": rel(kc),
        "exists": kc.is_dir(),
        "manifest": None,
        "operation": [],
        "workflows": [],
        "install": [],
        "warnings_supplemental": [],
        "warnings_expanded": [],
        "troubleshooting": [],
        "troubleshooting_expanded": [],
        "visual_intent": [],
        "publication_intent": None,
        "provenance": None,
    }
    if not kc.is_dir():
        return bundle
    bundle["manifest"] = read_json(kc / "MANIFEST.json")
    bundle["operation"] = [read_json(p) for p in list_json_files(kc / "operation") if p.name != "faq"]
    bundle["operation"] = [x for x in bundle["operation"] if x]
    bundle["workflows"] = [x for x in (read_json(p) for p in list_json_files(kc / "workflows")) if x]
    bundle["install"] = [x for x in (read_json(p) for p in list_json_files(kc / "install")) if x]
    bundle["warnings_supplemental"] = [
        x for x in (read_json(p) for p in list_json_files(kc / "warnings" / "supplemental-candidates")) if x
    ]
    bundle["warnings_expanded"] = [
        x for x in (read_json(p) for p in list_json_files(kc / "warnings-expanded")) if x
    ]
    bundle["troubleshooting"] = [x for x in (read_json(p) for p in list_json_files(kc / "troubleshooting")) if x]
    bundle["troubleshooting_expanded"] = [
        x for x in (read_json(p) for p in list_json_files(kc / "troubleshooting-expanded")) if x
    ]
    bundle["visual_intent"] = [x for x in (read_json(p) for p in list_json_files(kc / "visual-intent")) if x]
    bundle["publication_intent"] = read_json(kc / "publication-intent" / "publication-intent-map.json")
    bundle["provenance"] = read_json(kc / "provenance" / "oem-source-index.json")
    return bundle


# ---------------------------------------------------------------------------
# HTML rendering primitives
# ---------------------------------------------------------------------------

CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 960px; margin: 0 auto; padding: 24px 32px 64px; color: #1a1a1a; line-height: 1.55; }
header.gov { background: #f5f3ef; border-left: 4px solid #8a7d5a; padding: 12px 16px; margin-bottom: 24px; font-size: 12px; color: #4a4435; }
header.gov .label { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: #6b5f3f; }
nav.topnav { margin: 0 0 24px; padding: 8px 0; border-bottom: 1px solid #e0d9c8; font-size: 13px; }
nav.topnav a { margin-right: 14px; color: #5a4d2a; text-decoration: none; }
nav.topnav a:hover { text-decoration: underline; }
h1 { color: #2b2b2b; border-bottom: 2px solid #8a7d5a; padding-bottom: 8px; }
h2 { color: #3d3a30; margin-top: 32px; }
h3 { color: #4a4435; }
section.entity { background: #fafafa; border: 1px solid #e8e2d2; border-radius: 4px; padding: 14px 18px; margin: 14px 0; }
section.entity .meta { font-size: 11px; color: #6f6750; margin-bottom: 6px; }
section.entity .meta .pill { display: inline-block; padding: 1px 7px; border-radius: 9px; background: #ece6d3; color: #5a4d2a; margin-right: 6px; font-weight: 600; letter-spacing: 0.04em; }
section.entity .meta .pill.confidence-high { background: #d8e8d4; color: #2f5728; }
section.entity .meta .pill.confidence-medium { background: #f3e9c8; color: #6b5418; }
section.entity .meta .pill.confidence-low, section.entity .meta .pill.confidence-candidate, section.entity .meta .pill.confidence-ocr-medium { background: #f1d6c9; color: #7a3a18; }
section.entity .meta .pill.severity-high { background: #f5c5b9; color: #7a2010; }
section.entity .meta .pill.severity-medium { background: #f3e0c2; color: #6b4818; }
section.entity ol, section.entity ul { padding-left: 22px; }
.visual-need { font-size: 11px; color: #6b5418; background: #fcf7e6; border: 1px dashed #d6c486; padding: 4px 8px; border-radius: 3px; margin-top: 8px; display: inline-block; }
.lineage { font-size: 11px; color: #6b6760; margin-top: 10px; }
.lineage code { background: #f0eee8; padding: 1px 4px; border-radius: 2px; }
footer.disclosure { margin-top: 48px; padding: 16px; background: #f5f3ef; border-top: 2px solid #8a7d5a; font-size: 11px; color: #5a4d2a; }
footer.disclosure ul { padding-left: 18px; margin: 4px 0; }
.gap { color: #7a3a18; font-style: italic; }
table.index { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
table.index th, table.index td { text-align: left; padding: 8px 12px; border-bottom: 1px solid #e8e2d2; }
table.index th { background: #f5f3ef; color: #4a4435; }
"""


def page_header(title: str, product: Optional[str], section: str) -> str:
    nav_links = ""
    if product:
        nav_links = (
            f'<a href="index.html">Index</a>'
            f'<a href="onboarding.html">Onboarding</a>'
            f'<a href="installation.html">Installation</a>'
            f'<a href="warnings.html">Warnings</a>'
            f'<a href="troubleshooting.html">Troubleshooting</a>'
            f'<a href="full-manual.html">Full manual</a>'
            f'<a href="../Product_Manuals.html">All products</a>'
        )
    else:
        nav_links = '<a href="../publication-system/">Publication system</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="gov">
  <div class="label">Governed publication preview — text-first</div>
  <div>This is a <strong>rendered view</strong> of the governed knowledge-core. It is <strong>not</strong> an independent source of truth. Knowledge-core remains canonical; this surface adds form only. Visuals are <strong>not generated</strong> in this phase — visual needs are flagged inline.</div>
  <div>Renderer: <code>{esc(RENDERER_ID)}@{esc(RENDERER_VERSION)}</code> · Section: <code>{esc(section)}</code> · Generated: <code>{esc(NOW)}</code></div>
</header>
<nav class="topnav">{nav_links}</nav>
<h1>{esc(title)}</h1>
"""


def page_footer(product: Optional[str], lineage_refs: Iterable[str], gaps: Iterable[str]) -> str:
    refs = "\n".join(f"<li><code>{esc(r)}</code></li>" for r in lineage_refs)
    gaplis = "\n".join(f"<li class='gap'>{esc(g)}</li>" for g in gaps)
    return f"""
<footer class="disclosure">
  <strong>Provenance &amp; lineage (mandatory disclosure):</strong>
  <ul>{refs or '<li>(no source refs collected)</li>'}</ul>
  <strong>Unresolved gaps in this rendered surface:</strong>
  <ul>{gaplis or '<li>(none detected at render time)</li>'}</ul>
  <div>Subordinate to knowledge-core + {len(SUBORDINATE_TO) - 1} governance layers. Confidence is disclosed per entity. Audience filter: <code>reviewer-preview</code> (single profile).</div>
</footer>
</body>
</html>
"""


def confidence_pill(conf: Optional[str]) -> str:
    if not conf:
        return ""
    cls = f"pill confidence-{esc(conf)}"
    return f'<span class="{cls}">conf:{esc(conf)}</span>'


def severity_pill(sev: Optional[str]) -> str:
    if not sev:
        return ""
    return f'<span class="pill severity-{esc(sev)}">severity:{esc(sev)}</span>'


def status_pill(status: Optional[str]) -> str:
    if not status:
        return ""
    return f'<span class="pill">{esc(status)}</span>'


def render_steps(items: Iterable[str], ordered: bool = True) -> str:
    tag = "ol" if ordered else "ul"
    body = "\n".join(f"<li>{esc(i)}</li>" for i in items if i)
    if not body:
        return ""
    return f"<{tag}>{body}</{tag}>"


def visual_need_badge(category: str, why: str, priority: str) -> str:
    return (
        f'<div class="visual-need">Visual need: <strong>{esc(category)}</strong> · '
        f'priority {esc(priority)} · {esc(why)} '
        f'(declarative only — no image generated this phase)</div>'
    )


def lineage_block(refs: Iterable[str]) -> str:
    refs = [r for r in refs if r]
    if not refs:
        return ""
    items = "".join(f"<code>{esc(r)}</code> " for r in refs)
    return f'<div class="lineage">Source refs: {items}</div>'


# ---------------------------------------------------------------------------
# Visual-need detection (NON-GENERATIVE)
# ---------------------------------------------------------------------------

def detect_visual_need(entity: Dict[str, Any], section: str) -> Optional[Dict[str, Any]]:
    etype = entity.get("type", "")
    severity = entity.get("severity")
    if section == "installation":
        return {
            "category": "installation-orientation",
            "why": "physical mounting requires visual orientation reference",
            "priority": "P0",
            "user_risk_level": "high",
            "criticality": "blocking-without-visual",
        }
    if etype == "warning" or "warning" in etype:
        if entity.get("is_irreversible") or severity == "high":
            return {
                "category": "warning-illustration",
                "why": "irreversible or high-severity warning benefits from icon/illustration",
                "priority": "P1",
                "user_risk_level": "high",
                "criticality": "high",
            }
        return {
            "category": "warning-illustration",
            "why": "operational warning improves comprehension with icon",
            "priority": "P2",
            "user_risk_level": "medium",
            "criticality": "medium",
        }
    if etype == "procedure" and entity.get("steps"):
        return {
            "category": "procedural-sequence",
            "why": "multi-step procedure improves with sequence illustration",
            "priority": "P2",
            "user_risk_level": "medium",
            "criticality": "medium",
        }
    if etype == "workflow":
        return {
            "category": "hybrid-ui",
            "why": "app + device workflow benefits from UI screenshot composite",
            "priority": "P2",
            "user_risk_level": "medium",
            "criticality": "medium",
        }
    if "troubleshooting" in etype:
        return {
            "category": "troubleshooting-support",
            "why": "diagnostic decision tree benefits from a flow diagram",
            "priority": "P2",
            "user_risk_level": "medium",
            "criticality": "medium",
        }
    return None


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def render_entity(entity: Dict[str, Any], section: str, visual_needs_collector: List[Dict[str, Any]]) -> str:
    eid = entity.get("id", "?")
    summary = entity.get("summary", "")
    conf = entity.get("confidence")
    status = entity.get("validation_status")
    pills = (
        confidence_pill(conf)
        + status_pill(status)
        + severity_pill(entity.get("severity"))
        + (status_pill(f"surface:{entity.get('surface')}") if entity.get("surface") else "")
    )
    parts: List[str] = [f'<section class="entity" id="{esc(eid)}">']
    parts.append(f'<div class="meta">{pills}<code>{esc(eid)}</code></div>')
    parts.append(f"<h3>{esc(summary or eid)}</h3>")
    if entity.get("menu_path"):
        parts.append(f"<p><strong>Menu path:</strong> <code>{esc(entity['menu_path'])}</code></p>")
    if entity.get("preconditions"):
        parts.append("<p><strong>Preconditions:</strong></p>")
        parts.append(render_steps(entity["preconditions"], ordered=False))
    if entity.get("symptoms"):
        parts.append("<p><strong>Symptoms:</strong></p>")
        parts.append(render_steps(entity["symptoms"], ordered=False))
    if entity.get("diagnostic_questions"):
        parts.append("<p><strong>Diagnostic questions:</strong></p>")
        parts.append(render_steps(entity["diagnostic_questions"], ordered=False))
    if entity.get("steps"):
        parts.append("<p><strong>Steps:</strong></p>")
        parts.append(render_steps(entity["steps"], ordered=True))
    if entity.get("notes"):
        parts.append("<p><strong>Notes:</strong></p>")
        parts.append(render_steps(entity["notes"], ordered=False))
    if entity.get("text") and not entity.get("steps"):
        parts.append(f"<p>{esc(entity['text'])}</p>")
    if entity.get("validation_checks"):
        parts.append("<p><strong>Validation checks:</strong></p>")
        parts.append(render_steps(entity["validation_checks"], ordered=False))
    if entity.get("next_actions"):
        parts.append("<p><strong>Next actions:</strong></p>")
        parts.append(render_steps(entity["next_actions"], ordered=False))
    if entity.get("outcomes"):
        parts.append("<p><strong>Outcomes:</strong></p>")
        parts.append(render_steps(entity["outcomes"], ordered=False))
    if entity.get("must_be_attached_to_kinds"):
        parts.append(
            "<p><strong>Attach to kinds:</strong> "
            + ", ".join(f"<code>{esc(k)}</code>" for k in entity["must_be_attached_to_kinds"])
            + "</p>"
        )
    if entity.get("escalation_required"):
        parts.append("<p><strong>Escalation required:</strong> yes</p>")

    need = detect_visual_need(entity, section)
    if need:
        visual_needs_collector.append({
            "entity_id": eid,
            "entity_type": entity.get("type"),
            "section": section,
            **need,
            "source_refs": entity.get("source_refs", []),
        })
        parts.append(visual_need_badge(need["category"], need["why"], need["priority"]))

    parts.append(lineage_block(entity.get("source_refs", []) + entity.get("extraction_lineage", [])))
    parts.append("</section>")
    return "\n".join(parts)


def render_section_page(
    title: str,
    product: str,
    section: str,
    entities: List[Dict[str, Any]],
    visual_needs_collector: List[Dict[str, Any]],
    intro: str = "",
) -> Tuple[str, List[str], List[str]]:
    body_parts: List[str] = [page_header(title, product, section)]
    if intro:
        body_parts.append(f"<p>{esc(intro)}</p>")
    if not entities:
        body_parts.append('<p class="gap">No entities of this kind currently exist in the knowledge-core for this product.</p>')
    refs: List[str] = []
    gaps: List[str] = []
    for ent in entities:
        body_parts.append(render_entity(ent, section, visual_needs_collector))
        for r in ent.get("source_refs", []) or []:
            refs.append(r)
        status = (ent.get("validation_status") or "").lower()
        if "candidate" in status or "pending" in status or "inferred" in status:
            gaps.append(f"{ent.get('id')}: validation_status={status}")
        if (ent.get("confidence") or "").lower() in {"candidate", "low", "ocr-medium", "medium"}:
            gaps.append(f"{ent.get('id')}: confidence={ent.get('confidence')}")
    body_parts.append(page_footer(product, sorted(set(refs)), sorted(set(gaps))))
    return "\n".join(body_parts), sorted(set(refs)), sorted(set(gaps))


def select_onboarding(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    pairing = [w for w in bundle["workflows"] if "pairing" in (w.get("id") or "") or "onboarding" in (w.get("id") or "")]
    procs = [
        p for p in bundle["operation"]
        if any(k in (p.get("id") or "") for k in ("add-administrator", "add-user", "agregar-un-administrador", "conectar-la-cerradura"))
    ]
    return pairing + procs


def select_installation(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(bundle["install"])


def select_warnings(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(bundle["warnings_supplemental"]) + list(bundle["warnings_expanded"])


def select_troubleshooting(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(bundle["troubleshooting"]) + list(bundle["troubleshooting_expanded"])


def select_operation(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    onboarding_ids = {e.get("id") for e in select_onboarding(bundle)}
    return [p for p in bundle["operation"] if p.get("id") not in onboarding_ids]


# ---------------------------------------------------------------------------
# Per-product render
# ---------------------------------------------------------------------------

def render_product(product: str) -> Dict[str, Any]:
    bundle = load_knowledge_core(product)
    out_root = GENERATED_ROOT / product
    html_dir = out_root / "html"
    manifests_dir = out_root / "manifests"
    previews_dir = out_root / "previews"
    metadata_dir = out_root / "publication-metadata"
    visual_needs_dir = out_root / "visual-needs"

    visual_needs_collector: List[Dict[str, Any]] = []
    page_summaries: List[Dict[str, Any]] = []
    all_refs: List[str] = []
    all_gaps: List[str] = []

    if not bundle["exists"]:
        # still produce a stub so navigation reflects reality
        write_text(html_dir / "index.html", page_header(f"{product} — knowledge-core absent", product, "index")
                   + f'<p class="gap">No knowledge-core directory found at <code>{esc(bundle["knowledge_core_path"])}</code>. '
                     "This product is declared in the topology but has no governed source data.</p>"
                   + page_footer(product, [], [f"knowledge-core directory missing for {product}"]))
        write_json(visual_needs_dir / "visual-needs.json", {
            "schema": SCHEMA, "product": product, "generated_at": NOW,
            "knowledge_core_present": False, "needs": [],
        })
        write_json(manifests_dir / "publication-manifest.json", {
            "schema": SCHEMA, "product": product, "generated_at": NOW,
            "renderer": {"id": RENDERER_ID, "version": RENDERER_VERSION},
            "knowledge_core_present": False, "pages": [], "source_refs": [], "gaps": ["knowledge-core absent"],
            "subordinate_to": SUBORDINATE_TO,
        })
        return {
            "product": product, "knowledge_core_present": False,
            "pages_rendered": 1, "entities_rendered": 0,
            "visual_needs": 0, "gaps": 1, "source_refs": 0,
        }

    sections: List[Tuple[str, str, str, List[Dict[str, Any]], str]] = [
        ("onboarding.html", "Onboarding", "onboarding", select_onboarding(bundle),
         "Pairing workflows and core enrollment procedures, rendered from the governed knowledge-core."),
        ("installation.html", "Installation", "installation", select_installation(bundle),
         "Physical installation guidance. Visual support is operationally mandatory and is flagged below for downstream visual pipelines (none generated this phase)."),
        ("warnings.html", "Warnings", "warnings", select_warnings(bundle),
         "Supplemental and expanded warning candidates. Severity and irreversibility are disclosed per entity."),
        ("troubleshooting.html", "Troubleshooting", "troubleshooting", select_troubleshooting(bundle),
         "Diagnostic candidates. Most entries are reviewer-pending; render preserves this status visibly."),
        ("operational-guidance.html", "Operational guidance", "operation", select_operation(bundle),
         "Day-to-day operating procedures beyond initial onboarding."),
    ]

    for filename, title, section_key, entities, intro in sections:
        page_html, refs, gaps = render_section_page(
            f"{product} — {title}", product, section_key, entities, visual_needs_collector, intro=intro
        )
        write_text(html_dir / filename, page_html)
        page_summaries.append({
            "filename": filename,
            "title": title,
            "section": section_key,
            "entity_count": len(entities),
            "source_ref_count": len(refs),
            "gap_count": len(gaps),
        })
        all_refs.extend(refs)
        all_gaps.extend(gaps)

    # full-manual: concatenated
    full_parts = [page_header(f"{product} — Full manual (rendered preview)", product, "full-manual")]
    full_parts.append(
        "<p><em>This is a single-page concatenation of every rendered section. It exists only as a reviewer convenience. "
        "Knowledge-core remains the canonical source.</em></p>"
    )
    for filename, title, section_key, entities, intro in sections:
        full_parts.append(f"<h2>{esc(title)}</h2>")
        if intro:
            full_parts.append(f"<p>{esc(intro)}</p>")
        if not entities:
            full_parts.append('<p class="gap">No entities of this kind currently exist in the knowledge-core for this product.</p>')
        for ent in entities:
            full_parts.append(render_entity(ent, section_key, []))  # no double-count of visual needs
    full_parts.append(page_footer(product, sorted(set(all_refs)), sorted(set(all_gaps))))
    write_text(html_dir / "full-manual.html", "\n".join(full_parts))

    # index.html (per product)
    rows = "\n".join(
        f'<tr><td><a href="{esc(s["filename"])}">{esc(s["title"])}</a></td>'
        f'<td>{s["entity_count"]}</td><td>{s["source_ref_count"]}</td><td>{s["gap_count"]}</td></tr>'
        for s in page_summaries
    )
    rows += (
        f'<tr><td><a href="full-manual.html">Full manual (concatenated)</a></td>'
        f'<td>{sum(s["entity_count"] for s in page_summaries)}</td>'
        f'<td>{len(set(all_refs))}</td><td>{len(set(all_gaps))}</td></tr>'
    )
    index_html = page_header(f"{product} — Publication index", product, "index") + (
        f"<p>Knowledge-core path: <code>{esc(bundle['knowledge_core_path'])}</code></p>"
        f"<table class='index'><thead><tr><th>Section</th><th>Entities</th><th>Source refs</th><th>Gaps</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<p>Visual needs detected: <strong>{len(visual_needs_collector)}</strong> "
        f"(see <a href='../visual-needs/visual-needs.json'>visual-needs.json</a> — declarative only).</p>"
    ) + page_footer(product, sorted(set(all_refs)), sorted(set(all_gaps)))
    write_text(html_dir / "index.html", index_html)

    # preview navigation (lighter, focused on review)
    preview_parts = [page_header(f"{product} — Reviewer preview", product, "preview")]
    preview_parts.append(
        "<p>Reviewer-focused preview. Use this to inspect rendered manuals, unresolved procedural gaps, "
        "visual-need markers and provenance lineage. No downstream side-effects.</p>"
    )
    preview_parts.append("<h2>Pages</h2><ul>")
    for s in page_summaries:
        preview_parts.append(
            f'<li><a href="../html/{esc(s["filename"])}">{esc(s["title"])}</a> '
            f'— {s["entity_count"]} entities, {s["gap_count"]} gaps</li>'
        )
    preview_parts.append('<li><a href="../html/full-manual.html">Full manual</a></li>')
    preview_parts.append("</ul>")
    preview_parts.append(f"<h2>Visual needs ({len(visual_needs_collector)})</h2><ul>")
    for n in visual_needs_collector[:30]:
        preview_parts.append(
            f"<li><code>{esc(n['entity_id'])}</code> — {esc(n['category'])} "
            f"(priority {esc(n['priority'])}): {esc(n['why'])}</li>"
        )
    if len(visual_needs_collector) > 30:
        preview_parts.append(f"<li>… and {len(visual_needs_collector) - 30} more in visual-needs.json</li>")
    preview_parts.append("</ul>")
    preview_parts.append(f"<h2>Gaps ({len(set(all_gaps))})</h2><ul>")
    for g in sorted(set(all_gaps))[:50]:
        preview_parts.append(f"<li class='gap'>{esc(g)}</li>")
    if len(set(all_gaps)) > 50:
        preview_parts.append(f"<li>… and {len(set(all_gaps)) - 50} more</li>")
    preview_parts.append("</ul>")
    preview_parts.append(page_footer(product, sorted(set(all_refs)), sorted(set(all_gaps))))
    write_text(previews_dir / "review-preview.html", "\n".join(preview_parts))

    # publication metadata
    write_json(metadata_dir / "metadata.json", {
        "schema": SCHEMA,
        "product": product,
        "generated_at": NOW,
        "renderer": {"id": RENDERER_ID, "version": RENDERER_VERSION},
        "audience_profile": "reviewer-preview",
        "format": "html-text-first",
        "lossy_format": True,
        "lossy_disclosure": "HTML is a lossy projection of structured-runtime; structured-runtime remains source of truth.",
        "knowledge_core_path": bundle["knowledge_core_path"],
        "manifest_summary": (bundle["manifest"] or {}).get("subdomain_counts"),
        "subordinate_to": SUBORDINATE_TO,
    })

    # visual-needs.json
    write_json(visual_needs_dir / "visual-needs.json", {
        "schema": SCHEMA,
        "product": product,
        "generated_at": NOW,
        "policy": "non-generative; identifies visual-assistance necessity only; no prompts produced; no images produced.",
        "categories_used": sorted({n["category"] for n in visual_needs_collector}),
        "needs_count": len(visual_needs_collector),
        "needs": visual_needs_collector,
    })

    # publication-manifest.json
    write_json(manifests_dir / "publication-manifest.json", {
        "schema": SCHEMA,
        "product": product,
        "generated_at": NOW,
        "renderer": {"id": RENDERER_ID, "version": RENDERER_VERSION},
        "knowledge_core_present": True,
        "knowledge_core_path": bundle["knowledge_core_path"],
        "subordinate_to": SUBORDINATE_TO,
        "pages": page_summaries + [{
            "filename": "full-manual.html", "title": "Full manual",
            "section": "full-manual",
            "entity_count": sum(s["entity_count"] for s in page_summaries),
            "source_ref_count": len(set(all_refs)),
            "gap_count": len(set(all_gaps)),
        }],
        "rendered_procedure_ids": [e.get("id") for e in (select_onboarding(bundle) + select_operation(bundle)) if e.get("id")],
        "rendered_warning_ids": [e.get("id") for e in select_warnings(bundle) if e.get("id")],
        "rendered_troubleshooting_ids": [e.get("id") for e in select_troubleshooting(bundle) if e.get("id")],
        "source_refs": sorted(set(all_refs)),
        "gaps": sorted(set(all_gaps)),
        "visual_needs_ref": rel(visual_needs_dir / "visual-needs.json"),
        "preview_ref": rel(previews_dir / "review-preview.html"),
        "metadata_ref": rel(metadata_dir / "metadata.json"),
        "publication_intent_ref": rel(EXT_IMAGES_ROOT / product / "knowledge-core" / "publication-intent" / "publication-intent-map.json"),
        "provenance_ref": rel(EXT_IMAGES_ROOT / product / "knowledge-core" / "provenance" / "oem-source-index.json"),
    })

    return {
        "product": product,
        "knowledge_core_present": True,
        "pages_rendered": len(page_summaries) + 2,  # + index + full-manual
        "entities_rendered": sum(s["entity_count"] for s in page_summaries),
        "visual_needs": len(visual_needs_collector),
        "gaps": len(set(all_gaps)),
        "source_refs": len(set(all_refs)),
    }


# ---------------------------------------------------------------------------
# Product_Manuals.html (top-level navigation)
# ---------------------------------------------------------------------------

def render_index(product_results: List[Dict[str, Any]]) -> None:
    rows = []
    for r in product_results:
        if r["knowledge_core_present"]:
            link = f'<a href="{esc(r["product"])}/html/index.html">{esc(r["product"])}</a>'
            preview_link = f'<a href="{esc(r["product"])}/previews/review-preview.html">reviewer preview</a>'
        else:
            link = f'{esc(r["product"])} <span class="gap">(no knowledge-core)</span>'
            preview_link = '<span class="gap">n/a</span>'
        rows.append(
            f'<tr><td>{link}</td><td>{r["entities_rendered"]}</td>'
            f'<td>{r["source_refs"]}</td><td>{r["visual_needs"]}</td>'
            f'<td>{r["gaps"]}</td><td>{preview_link}</td></tr>'
        )
    page = page_header("Product manuals — rendered preview index", None, "Product_Manuals") + (
        "<p>This index lists every product for which the publication renderer attempted to assemble "
        "an HTML manual from the governed knowledge-core. <strong>Each rendered manual is a view, not a source.</strong> "
        "Knowledge-core remains canonical. Visuals are flagged but not generated.</p>"
        "<table class='index'><thead><tr>"
        "<th>Product</th><th>Entities</th><th>Source refs</th>"
        "<th>Visual needs</th><th>Gaps</th><th>Reviewer preview</th>"
        "</tr></thead><tbody>"
        + "\n".join(rows)
        + "</tbody></table>"
    ) + page_footer(None, [], [])
    write_text(GENERATED_ROOT / "Product_Manuals.html", page)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def md(title: str, body: str) -> str:
    return f"# {title}\n\nGenerated: `{NOW}`\n\nSchema: `{SCHEMA}`\n\n{body}\n"


def write_report(name: str, payload: Dict[str, Any], md_body: str) -> None:
    write_json(REPORTS_ROOT / f"{name}.json", payload)
    write_text(REPORTS_ROOT / f"{name}.md", md(payload.get("title", name), md_body))


def emit_reports(product_results: List[Dict[str, Any]]) -> None:
    primary = [r for r in product_results if r["product"] in PRIMARY_PRODUCTS]
    secondary = [r for r in product_results if r["product"] not in PRIMARY_PRODUCTS]
    total_entities = sum(r["entities_rendered"] for r in product_results)
    total_needs = sum(r["visual_needs"] for r in product_results)
    total_gaps = sum(r["gaps"] for r in product_results)

    write_report(
        "01-generated-publications-summary",
        {
            "title": "01 — Generated publications summary",
            "schema": SCHEMA, "generated_at": NOW,
            "products_attempted": [r["product"] for r in product_results],
            "products_rendered": [r["product"] for r in product_results if r["knowledge_core_present"]],
            "products_missing_kc": [r["product"] for r in product_results if not r["knowledge_core_present"]],
            "total_pages_rendered": sum(r["pages_rendered"] for r in product_results),
            "total_entities_rendered": total_entities,
            "primary_products": [r["product"] for r in primary],
        },
        f"- Products attempted: {len(product_results)}\n"
        f"- Rendered: {sum(1 for r in product_results if r['knowledge_core_present'])}\n"
        f"- Missing knowledge-core: {sum(1 for r in product_results if not r['knowledge_core_present'])}\n"
        f"- Total entities rendered: {total_entities}\n",
    )
    write_report(
        "02-html-rendering-summary",
        {
            "title": "02 — HTML rendering summary",
            "schema": SCHEMA, "generated_at": NOW,
            "renderer": {"id": RENDERER_ID, "version": RENDERER_VERSION},
            "format": "html-text-first",
            "image_generation_invoked": False,
            "prompt_generation_invoked": False,
            "comfy_invoked": False,
            "per_product": product_results,
        },
        "Renderer is text-first. Visuals are detected but not generated.\n\n"
        + "\n".join(f"- {r['product']}: pages={r['pages_rendered']}, entities={r['entities_rendered']}, gaps={r['gaps']}"
                    for r in product_results),
    )
    write_report(
        "03-product-manuals-summary",
        {
            "title": "03 — Product_Manuals.html summary",
            "schema": SCHEMA, "generated_at": NOW,
            "index_path": rel(GENERATED_ROOT / "Product_Manuals.html"),
            "linked_products": [r["product"] for r in product_results],
            "purpose": "publication navigation only — not a source of truth",
        },
        f"Top-level index at `{rel(GENERATED_ROOT / 'Product_Manuals.html')}` "
        f"links {len(product_results)} products.\n",
    )
    write_report(
        "04-visual-need-detection-summary",
        {
            "title": "04 — Visual-need detection summary",
            "schema": SCHEMA, "generated_at": NOW,
            "policy": "non-generative; identifies necessity only",
            "total_needs_detected": total_needs,
            "categories_supported": [
                "schematic", "hybrid-ui", "procedural-sequence",
                "warning-illustration", "installation-orientation", "troubleshooting-support",
            ],
            "per_product": [{"product": r["product"], "needs": r["visual_needs"]} for r in product_results],
        },
        f"Detected {total_needs} visual-assistance markers across all products. "
        "No prompts or images produced.\n",
    )
    write_report(
        "05-publication-manifest-summary",
        {
            "title": "05 — Publication manifests summary",
            "schema": SCHEMA, "generated_at": NOW,
            "manifest_locations": [
                rel(GENERATED_ROOT / r["product"] / "manifests" / "publication-manifest.json")
                for r in product_results
            ],
            "manifest_fields": [
                "renderer", "knowledge_core_path", "subordinate_to", "pages",
                "rendered_procedure_ids", "rendered_warning_ids", "rendered_troubleshooting_ids",
                "source_refs", "gaps", "visual_needs_ref", "preview_ref",
                "metadata_ref", "publication_intent_ref", "provenance_ref",
            ],
        },
        f"One manifest per product ({len(product_results)} total).\n",
    )
    write_report(
        "06-review-preview-summary",
        {
            "title": "06 — Review preview summary",
            "schema": SCHEMA, "generated_at": NOW,
            "preview_locations": [
                rel(GENERATED_ROOT / r["product"] / "previews" / "review-preview.html")
                for r in product_results if r["knowledge_core_present"]
            ],
            "audience": "reviewer-preview",
            "navigation_features": [
                "per-page links", "visual-needs preview list", "gap preview list", "provenance lineage in footer",
            ],
        },
        "One reviewer preview per product with knowledge-core.\n",
    )
    write_report(
        "07-unresolved-publication-gaps",
        {
            "title": "07 — Unresolved publication gaps",
            "schema": SCHEMA, "generated_at": NOW,
            "total_gaps_across_products": total_gaps,
            "per_product": [{"product": r["product"], "gaps": r["gaps"]} for r in product_results],
            "structural_gaps": [
                "no publication version registry yet",
                "no assembly-receipt emitter (carry-over from layer 29)",
                "no audience filter applied (single profile = reviewer-preview)",
                "no revocation propagation index",
                "no freshness-detection between knowledge-core updates and rendered HTML",
                "no section-order validator beyond hard-coded section list",
                "no lossy-format machine-checkable diff between html and structured-runtime",
                "no reviewer-validation surface (carry-over from layer 24 console gap)",
            ],
            "policy_gaps": [
                "visual-prompt pipeline intentionally absent in this phase",
                "image generation intentionally absent in this phase",
            ],
        },
        f"Total per-entity gaps surfaced: {total_gaps}. Structural gaps tracked separately.\n",
    )
    write_report(
        "08-publication-rendering-readiness-reassessment",
        {
            "title": "08 — Publication rendering readiness reassessment",
            "schema": SCHEMA, "generated_at": NOW,
            "platform_status": "FIRST GOVERNED PUBLICATION RENDERING — OPERATIONAL",
            "publication_readiness": "EXECUTABLE (text-first, single audience profile, lossy by disclosure)",
            "primary_bottleneck_resolved": "renderer absence (resolved by this phase)",
            "remaining_bottlenecks": [
                "publication version registry",
                "assembly-receipt emitter",
                "audience-aware filtering",
                "revocation propagation",
                "freshness detection",
                "reviewer-validation console",
            ],
            "next_track": "version registry + receipts + audience filtering + freshness checks",
            "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
            "runtime_impact": "none (renderer is read-only over knowledge-core)",
        },
        "First executable rendering layer is now operational. The knowledge-core remains the only "
        "source of truth; this layer produces views, not authority.\n",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build() -> None:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    product_results: List[Dict[str, Any]] = []
    for product in TARGET_PRODUCTS:
        product_results.append(render_product(product))

    render_index(product_results)
    emit_reports(product_results)

    print("First Governed Publication Rendering written to:")
    print(f"  {rel(GENERATED_ROOT)}")
    print(f"  {rel(REPORTS_ROOT)}")
    for r in product_results:
        flag = "" if r["knowledge_core_present"] else "  [no knowledge-core]"
        print(
            f"  {r['product']:8s} pages={r['pages_rendered']:2d} "
            f"entities={r['entities_rendered']:3d} "
            f"visual_needs={r['visual_needs']:3d} "
            f"gaps={r['gaps']:3d}{flag}"
        )


if __name__ == "__main__":
    build()
