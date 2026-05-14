#!/usr/bin/env python3
"""Phase 3 — Semantic enrichment + visual orchestration preparation.

Reads the existing `knowledge-core/` for each product and emits FIVE new
sibling subdomains:

  visual-intent/          — what each future visual must communicate
  procedural-semantics/   — normalized machine-readable action tokens
  component-visibility/   — components that must remain visually accurate
  visual-risk/            — where visual inaccuracy creates real-world harm
  publication-intent/     — channel routing per asset

Architectural rules honoured:
  * Does NOT generate manuals, PDFs, marketing, websites, or images.
  * Does NOT restructure the repository or rewrite canonical artifacts.
  * Does NOT invent hardware geometry, sensors, or components.
  * Vocabulary-anchored: enrichment fires only when an existing entity in
    knowledge-core surfaces the matching token.
  * Provenance preserved on every emitted artifact (`source_refs`,
    `extraction_lineage`).
  * Gap-aware: emits an explicit `semantic-gaps.json` per product instead of
    blocking when a domain is empty.
  * ComfyUI is the only authorised downstream visual generator.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[1]
NUCLEI = REPO / "wp-content/themes/beslock-custom/User manuals/ext-images"
REPORTS = REPO / "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/phase3-execution-reports"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "knowledge-core/1.1-semantic-enrichment"

NEW_SUBDOMAINS = (
    "visual-intent",
    "procedural-semantics",
    "component-visibility",
    "visual-risk",
    "publication-intent",
)


# ---------------------------------------------------------------------------
# Vocabulary anchors (curated from observed OEM corpus)
# ---------------------------------------------------------------------------
# Procedural action verbs → normalized semantic action tokens.
ACTION_LEXICON: list[tuple[str, list[str]]] = [
    ("press",        ["press", "tap", "presione", "pulsar", "toque"]),
    ("hold",         ["hold", "long press", "mantenga", "mantener pulsado"]),
    ("scan",         ["scan", "show the qr", "escanee", "muestre el qr"]),
    ("place-finger", ["place the finger", "place finger", "coloque el dedo", "huella"]),
    ("enroll",       ["enroll", "register", "registrar", "agregar usuario", "add user"]),
    ("pair",         ["pair", "pairing", "vincular", "vinculación", "emparejar"]),
    ("unlock",       ["unlock", "desbloquear", "abrir la cerradura"]),
    ("lock",         ["lock", "bloquear", "cerrar"]),
    ("reset",        ["reset", "restore factory", "restablecer", "restablecimiento"]),
    ("confirm",      ["confirm", "confirmar", "validar", "wait for confirmation"]),
    ("enter-menu",   ["enter the menu", "entre al menú", "ingrese al menú", "menu"]),
    ("select",       ["select", "choose", "seleccione", "elija"]),
    ("connect-wifi", ["wi-fi", "wifi", "select the target wi-fi", "conectar al wifi"]),
    ("install",      ["install", "instalar", "mount", "montar", "perforar"]),
    ("replace-battery", ["battery", "batería", "reemplazar batería"]),
    ("open-app",     ["open smart life", "open the app", "abra la aplicación", "tuya app"]),
    ("show-qr",      ["show the generated phone qr", "muestre el qr"]),
    ("test",         ["test", "probar", "verificar"]),
]

# Visible product components that MUST stay accurate in any future Comfy render.
COMPONENT_LEXICON: list[tuple[str, str, list[str]]] = [
    # (component_id, kind, surface phrases)
    ("fingerprint-zone",      "sensor",   ["fingerprint", "huella"]),
    ("keypad",                "input",    ["keypad", "teclado", "panel táctil"]),
    ("face-recognition-cam",  "sensor",   ["face recognition", "facial", "rostro"]),
    ("palm-vein-sensor",      "sensor",   ["palm vein", "vena palmar"]),
    ("ic-card-zone",          "sensor",   ["ic card", "tarjeta", "rfid"]),
    ("camera-cluster",        "sensor",   ["camera", "qr to the lock camera", "cámara"]),
    ("exterior-handle",       "mechanic", ["handle", "manija", "exterior handle"]),
    ("interior-thumbturn",    "mechanic", ["thumbturn", "knob", "perilla interior"]),
    ("deadbolt",              "mechanic", ["deadbolt", "pasador", "cerrojo"]),
    ("latch",                 "mechanic", ["latch", "pestillo"]),
    ("lock-body",             "mechanic", ["lock body", "cuerpo de la cerradura", "6068"]),
    ("emergency-usb-port",    "power",    ["usb-c", "type-c", "emergency power"]),
    ("mechanical-key-slot",   "fallback", ["mechanical key", "llave mecánica", "llave"]),
    ("led-indicator",         "feedback", ["led", "indicator", "indicador"]),
    ("buzzer",                "feedback", ["buzzer", "speaker", "altavoz", "voice prompt"]),
    ("battery-compartment",   "power",    ["battery", "batería"]),
]

# Visual-intent semantic objectives (anchor by entity type + token).
INTENT_TEMPLATES: list[dict] = [
    {
        "intent_id": "intent-installation-assistance",
        "objective": "Help an installer mount the lock correctly the first time.",
        "anchor_subdomain": "install",
        "user_risk_level": "high",
        "visual_assistance_priority": "P0",
    },
    {
        "intent_id": "intent-fingerprint-enrollment",
        "objective": "Show the user where and how to place their finger during enrollment.",
        "anchor_tokens": ["place-finger", "enroll"],
        "user_risk_level": "low",
        "visual_assistance_priority": "P1",
    },
    {
        "intent_id": "intent-app-pairing",
        "objective": "Show the user the app pairing flow without ambiguity.",
        "anchor_tokens": ["pair", "open-app", "connect-wifi", "show-qr"],
        "user_risk_level": "medium",
        "visual_assistance_priority": "P1",
    },
    {
        "intent_id": "intent-reset-procedure",
        "objective": "Visualise the factory-reset procedure, including the irreversible nature.",
        "anchor_tokens": ["reset"],
        "user_risk_level": "high",
        "visual_assistance_priority": "P0",
    },
    {
        "intent_id": "intent-battery-replacement",
        "objective": "Show how to access and replace the battery without damaging the lock.",
        "anchor_tokens": ["replace-battery"],
        "user_risk_level": "medium",
        "visual_assistance_priority": "P1",
    },
    {
        "intent_id": "intent-emergency-unlock",
        "objective": "Show the emergency unlock paths (USB-C power, mechanical key) when batteries are dead.",
        "anchor_components": ["emergency-usb-port", "mechanical-key-slot"],
        "user_risk_level": "high",
        "visual_assistance_priority": "P0",
    },
    {
        "intent_id": "intent-warning-visualisation",
        "objective": "Visualise OEM warnings so they are unmissable.",
        "anchor_subdomain": "warnings",
        "user_risk_level": "high",
        "visual_assistance_priority": "P0",
    },
    {
        "intent_id": "intent-onboarding-overview",
        "objective": "Provide a single overview image that introduces the lock anatomy to new owners.",
        "anchor_subdomain": "entities",
        "user_risk_level": "low",
        "visual_assistance_priority": "P2",
    },
]

# Visual-risk catalogue (token → real-world failure mode).
RISK_CATALOG: list[dict] = [
    {
        "risk_id": "risk-misplaced-fingerprint-zone",
        "trigger_components": ["fingerprint-zone"],
        "failure_mode": "User taps the wrong area during enrollment, enrollment fails, support ticket opens.",
        "severity": "high",
    },
    {
        "risk_id": "risk-incorrect-handle-direction",
        "trigger_components": ["exterior-handle", "interior-thumbturn"],
        "failure_mode": "Customer installs the lock with the wrong handing and cannot close the door.",
        "severity": "critical",
    },
    {
        "risk_id": "risk-wrong-camera-position",
        "trigger_components": ["camera-cluster"],
        "failure_mode": "QR pairing image shows the camera in the wrong location; user cannot complete pairing.",
        "severity": "high",
    },
    {
        "risk_id": "risk-fake-emergency-port",
        "trigger_components": ["emergency-usb-port"],
        "failure_mode": "Customer searches for a USB-C port that does not exist on this model and is locked out.",
        "severity": "critical",
    },
    {
        "risk_id": "risk-wrong-keypad-layout",
        "trigger_components": ["keypad"],
        "failure_mode": "User cannot follow PIN-entry instructions because the rendered keypad does not match physical reality.",
        "severity": "medium",
    },
    {
        "risk_id": "risk-hallucinated-sensor",
        "trigger_components": ["face-recognition-cam", "palm-vein-sensor", "ic-card-zone"],
        "failure_mode": "Marketing-style render shows a sensor the unit does not include, eroding trust at unboxing.",
        "severity": "critical",
    },
    {
        "risk_id": "risk-missing-mechanical-key",
        "trigger_components": ["mechanical-key-slot"],
        "failure_mode": "Owner does not realise they have a mechanical fallback during an emergency.",
        "severity": "high",
    },
]

# Publication-channel routing per entity type.
CHANNEL_ROUTING: dict[str, list[str]] = {
    "procedure":        ["pdf", "web", "chatbot", "support", "onboarding", "rag"],
    "workflow":         ["pdf", "web", "chatbot", "support", "onboarding", "rag", "future-video"],
    "installation":     ["pdf", "web", "support", "onboarding"],
    "installation-flow": ["pdf", "web", "support", "onboarding", "future-video"],
    "installation-step": ["pdf", "web", "support", "onboarding"],
    "glossary":         ["web", "chatbot", "rag"],
    "visual-semantic-map": ["comfyui"],
    "capability":       ["web", "chatbot", "rag"],
    "warning":          ["pdf", "web", "chatbot", "support"],
    "glossary-term":    ["web", "chatbot", "rag"],
    "faq":              ["web", "chatbot", "rag", "support"],
    "capability-map":   ["web", "chatbot", "rag", "comfyui"],
    "entity-catalog":   ["chatbot", "rag", "comfyui"],
    "hardware-specification": ["pdf", "web", "chatbot", "rag"],
    "knowledge-graph":  ["rag", "chatbot", "comfyui"],
    "extracted-text":   ["rag"],
    "ocr-draft-index":  ["rag"],
}

# Subdomains in the existing knowledge-core that the enricher reads.
KC_SUBDOMAINS = (
    "install",
    "operation",
    "workflows",
    "troubleshooting",
    "warnings",
    "terminology",
    "entities",
    "capabilities",
    "specifications",
    "semantic",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def load_json(path: Path):
    return json.loads(path.read_text())


def kc_root(product: str) -> Path:
    return NUCLEI / product / "knowledge-core"


def iter_kc_entities(product: str) -> Iterable[tuple[Path, dict]]:
    root = kc_root(product)
    for sub in KC_SUBDOMAINS:
        d = root / sub
        if not d.is_dir():
            continue
        for fp in sorted(d.rglob("*.json")):
            try:
                payload = load_json(fp)
            except Exception:
                continue
            if not isinstance(payload, dict):
                # Legacy aggregates (lists or index files) are skipped here.
                continue
            yield fp, payload


def text_blob(entity: dict) -> str:
    """Concatenate the textual fields of an entity for token matching."""
    parts: list[str] = []
    for k in ("summary", "menu_path", "title", "term", "definition", "question", "answer", "text"):
        v = entity.get(k)
        if isinstance(v, str):
            parts.append(v)
    for k in ("steps", "validation_checks", "outcomes", "preconditions"):
        v = entity.get(k)
        if isinstance(v, list):
            for x in v:
                if isinstance(x, str):
                    parts.append(x)
                elif isinstance(x, dict):
                    t = x.get("text") or x.get("instruction") or x.get("check")
                    if isinstance(t, str):
                        parts.append(t)
    return "\n".join(parts).lower()


def envelope(eid: str, etype: str, product: str, summary: str,
             source_refs: list[str], lineage: list[str],
             validation_status: str = "extraction-pending-review",
             confidence: str = "medium",
             extra: dict | None = None) -> dict:
    out = {
        "id": eid,
        "type": etype,
        "product": product,
        "summary": summary,
        "language": "es-CO",
        "validation_status": validation_status,
        "confidence": confidence,
        "ocr_dependency": "none",
        "channel_targets": ["chatbot", "rag", "comfyui"],
        "source_refs": source_refs,
        "extraction_lineage": lineage,
        "schema_version": SCHEMA,
        "updated_at": NOW,
    }
    if extra:
        for k, v in extra.items():
            if k not in out:
                out[k] = v
    return out


def relpath(p: Path) -> str:
    return p.relative_to(REPO).as_posix()


# ---------------------------------------------------------------------------
# 1. procedural-semantics/
# ---------------------------------------------------------------------------
def build_procedural_semantics(product: str) -> tuple[int, dict[str, int]]:
    """Tokenise the steps of every procedural entity into action tokens."""
    out_dir = kc_root(product) / "procedural-semantics"
    n = 0
    token_counts: dict[str, int] = {a: 0 for a, _ in ACTION_LEXICON}
    for fp, ent in iter_kc_entities(product):
        if ent.get("type") not in ("procedure", "workflow", "installation", "installation-flow"):
            continue
        steps = ent.get("steps")
        if not isinstance(steps, list) or not steps:
            continue
        norm_steps: list[dict] = []
        for i, raw in enumerate(steps):
            if isinstance(raw, dict):
                text = raw.get("text") or raw.get("instruction") or ""
            elif isinstance(raw, str):
                text = raw
            else:
                continue
            if not text:
                continue
            lower = text.lower()
            actions: list[str] = []
            for action, phrases in ACTION_LEXICON:
                if any(p in lower for p in phrases):
                    actions.append(action)
                    token_counts[action] += 1
            norm_steps.append(
                {
                    "step_index": i + 1,
                    "raw_text": text,
                    "semantic_actions": actions,
                    "matched_lexicon": [a for a in actions],
                }
            )
        if not norm_steps:
            continue
        eid = f"semantic-{ent['id']}"
        env = envelope(
            eid=eid,
            etype="procedural-semantics",
            product=product,
            summary=f"Normalized semantic actions for {ent['id']}",
            source_refs=[relpath(fp)] + ent.get("source_refs", []),
            lineage=[relpath(fp), "tools/knowledge_core_semantic_enrich.py::ACTION_LEXICON"],
            validation_status=ent.get("validation_status", "extraction-pending-review"),
            confidence=ent.get("confidence", "medium"),
            extra={
                "source_entity_id": ent["id"],
                "source_entity_type": ent.get("type"),
                "surface": ent.get("surface"),
                "menu_path": ent.get("menu_path"),
                "normalized_steps": norm_steps,
                "lexicon_version": "ACTION_LEXICON@1",
                "policy": "Vocabulary-anchored; no actions invented beyond ACTION_LEXICON matches against the original step text.",
            },
        )
        write_json(out_dir / f"{eid}.json", env)
        n += 1
    return n, {k: v for k, v in token_counts.items() if v}


# ---------------------------------------------------------------------------
# 2. component-visibility/
# ---------------------------------------------------------------------------
def build_component_visibility(product: str) -> tuple[int, list[str]]:
    """Identify which components must remain visually accurate based on KC corpus."""
    corpus_chunks: list[str] = []
    evidence_refs: list[str] = []
    for fp, ent in iter_kc_entities(product):
        blob = text_blob(ent)
        if blob:
            corpus_chunks.append(blob)
            evidence_refs.append(relpath(fp))
    corpus = "\n".join(corpus_chunks)
    components: list[dict] = []
    matched: list[str] = []
    for cid, kind, phrases in COMPONENT_LEXICON:
        hits = [p for p in phrases if p in corpus]
        if not hits:
            continue
        # Find up to 5 entity files where this component is referenced.
        evidence: list[str] = []
        for fp, ent in iter_kc_entities(product):
            if any(p in text_blob(ent) for p in hits):
                evidence.append(relpath(fp))
                if len(evidence) >= 5:
                    break
        components.append(
            {
                "component_id": cid,
                "kind": kind,
                "matched_surface_terms": hits,
                "evidence_entity_refs": evidence,
                "must_remain_geometrically_accurate": True,
                "trusted_visual_reference": f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/source-of-truth/product-images/",
            }
        )
        matched.append(cid)
    if not components:
        return 0, []
    payload = envelope(
        eid="component-visibility-map",
        etype="component-visibility-map",
        product=product,
        summary=f"Components that must stay geometrically accurate in future Comfy renders for {product}",
        source_refs=sorted(set(evidence_refs)),
        lineage=["tools/knowledge_core_semantic_enrich.py::COMPONENT_LEXICON"],
        extra={
            "components": components,
            "authorized_visual_renderer": "ComfyUI",
            "policy": "Future ComfyUI workflows MUST consume the trusted_visual_reference PNGs as anchor inputs for any of these components. No generative inference of component position, count, sensor type, keypad layout, or handle direction is allowed.",
        },
    )
    write_json(kc_root(product) / "component-visibility" / "component-visibility-map.json", payload)
    return len(components), matched


# ---------------------------------------------------------------------------
# 3. visual-risk/
# ---------------------------------------------------------------------------
def build_visual_risk(product: str, present_components: list[str]) -> int:
    out_dir = kc_root(product) / "visual-risk"
    n = 0
    for risk in RISK_CATALOG:
        triggers = [c for c in risk["trigger_components"] if c in present_components]
        if not triggers:
            continue
        eid = risk["risk_id"]
        payload = envelope(
            eid=eid,
            etype="visual-risk",
            product=product,
            summary=risk["failure_mode"],
            source_refs=[
                f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/knowledge-core/component-visibility/component-visibility-map.json",
            ],
            lineage=["tools/knowledge_core_semantic_enrich.py::RISK_CATALOG"],
            validation_status="extraction-pending-review",
            confidence="medium",
            extra={
                "severity": risk["severity"],
                "trigger_components": triggers,
                "failure_mode": risk["failure_mode"],
                "mitigation": "Future ComfyUI workflow MUST anchor the listed trigger_components against the OEM PNG references and refuse to render this asset if anchors are missing.",
                "downstream_consumers": ["comfyui", "visual-qa"],
            },
        )
        write_json(out_dir / f"{eid}.json", payload)
        n += 1
    return n


# ---------------------------------------------------------------------------
# 4. visual-intent/
# ---------------------------------------------------------------------------
def build_visual_intent(product: str, action_index: dict[str, int],
                        present_components: list[str]) -> int:
    out_dir = kc_root(product) / "visual-intent"
    n = 0
    # Per-product subdomain counts (to know whether 'install' / 'warnings' have anything)
    sub_counts: dict[str, int] = {}
    for sub in KC_SUBDOMAINS:
        d = kc_root(product) / sub
        sub_counts[sub] = sum(1 for _ in d.rglob("*.json")) if d.is_dir() else 0

    for tpl in INTENT_TEMPLATES:
        # Anchor check
        anchor_sub = tpl.get("anchor_subdomain")
        anchor_tokens = tpl.get("anchor_tokens", [])
        anchor_components = tpl.get("anchor_components", [])
        anchored = False
        anchor_evidence: list[str] = []
        if anchor_sub and sub_counts.get(anchor_sub, 0) > 0:
            anchored = True
            anchor_evidence.append(
                f"knowledge-core/{anchor_sub}/ has {sub_counts[anchor_sub]} entities"
            )
        if anchor_tokens and any(t in action_index for t in anchor_tokens):
            anchored = True
            anchor_evidence.append(
                f"procedural-semantics tokens present: {[t for t in anchor_tokens if t in action_index]}"
            )
        if anchor_components and any(c in present_components for c in anchor_components):
            anchored = True
            anchor_evidence.append(
                f"components present: {[c for c in anchor_components if c in present_components]}"
            )
        if not anchored:
            continue

        # Collect critical components.
        critical_components: list[str] = []
        if anchor_components:
            critical_components.extend(c for c in anchor_components if c in present_components)
        # Hard pairing components for some intents.
        if tpl["intent_id"] == "intent-fingerprint-enrollment" and "fingerprint-zone" in present_components:
            critical_components.append("fingerprint-zone")
        if tpl["intent_id"] == "intent-app-pairing":
            for c in ("camera-cluster", "keypad"):
                if c in present_components:
                    critical_components.append(c)
        if tpl["intent_id"] == "intent-installation-assistance":
            for c in ("exterior-handle", "interior-thumbturn", "lock-body", "deadbolt", "latch"):
                if c in present_components:
                    critical_components.append(c)
        critical_components = sorted(set(critical_components))

        payload = envelope(
            eid=tpl["intent_id"],
            etype="visual-intent",
            product=product,
            summary=tpl["objective"],
            source_refs=[
                f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/knowledge-core/component-visibility/component-visibility-map.json",
                f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/knowledge-core/procedural-semantics/",
            ],
            lineage=["tools/knowledge_core_semantic_enrich.py::INTENT_TEMPLATES"],
            extra={
                "semantic_objective": tpl["objective"],
                "procedure_linkage_subdomain": tpl.get("anchor_subdomain"),
                "procedure_linkage_tokens": anchor_tokens,
                "critical_components": critical_components,
                "mandatory_visible_elements": critical_components,
                "forbidden_visual_deviations": [
                    "fabricated sensors not in component-visibility-map",
                    "wrong handle direction",
                    "incorrect keypad layout",
                    "fictional product variants",
                    "stylised humans (per visual-system reset 2026-05-13)",
                ],
                "user_risk_level": tpl["user_risk_level"],
                "visual_assistance_priority": tpl["visual_assistance_priority"],
                "target_publication_channels": ["pdf", "web", "support", "onboarding", "chatbot"],
                "anchor_evidence": anchor_evidence,
                "authorized_visual_renderer": "ComfyUI",
                "policy": "This intent only describes WHAT must be communicated. Visual generation is deferred to a future ComfyUI workflow that MUST honour critical_components and forbidden_visual_deviations.",
            },
        )
        write_json(out_dir / f"{tpl['intent_id']}.json", payload)
        n += 1
    return n


# ---------------------------------------------------------------------------
# 5. publication-intent/
# ---------------------------------------------------------------------------
def build_publication_intent(product: str) -> tuple[int, dict[str, int]]:
    out_dir = kc_root(product) / "publication-intent"
    routing: list[dict] = []
    channel_counts: dict[str, int] = {}
    for fp, ent in iter_kc_entities(product):
        etype = ent.get("type", "unknown")
        channels = CHANNEL_ROUTING.get(etype)
        if not channels:
            continue
        # Demote low-confidence OCR evidence: never publish to web/pdf/onboarding.
        vstatus = ent.get("validation_status", "")
        if vstatus.startswith("low-confidence-evidence"):
            channels = [c for c in channels if c in ("rag",)]
            if not channels:
                continue
        if vstatus == "inferred-but-unverified":
            channels = [c for c in channels if c in ("rag", "chatbot", "support")]
            if not channels:
                continue
        routing.append(
            {
                "entity_ref": relpath(fp),
                "entity_id": ent.get("id"),
                "entity_type": etype,
                "validation_status": vstatus,
                "channels": channels,
            }
        )
        for c in channels:
            channel_counts[c] = channel_counts.get(c, 0) + 1
    if not routing:
        return 0, channel_counts
    payload = envelope(
        eid="publication-intent-map",
        etype="publication-intent-map",
        product=product,
        summary=f"Channel routing for every publishable knowledge-core asset of {product}",
        source_refs=[f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/knowledge-core/"],
        lineage=["tools/knowledge_core_semantic_enrich.py::CHANNEL_ROUTING"],
        extra={
            "routing": routing,
            "channel_totals": channel_counts,
            "demotion_rules": {
                "low-confidence-evidence-only": "rag-only",
                "low-confidence-evidence": "rag-only",
                "inferred-but-unverified": "rag + chatbot + support only",
                "extraction-pending-review": "default channels (per CHANNEL_ROUTING)",
                "verified": "default channels (per CHANNEL_ROUTING)",
            },
            "policy": "Channel routing is advisory metadata. Actual PDF/web/chatbot pipelines must read this map; nothing is published from this layer directly.",
        },
    )
    write_json(out_dir / "publication-intent-map.json", payload)
    return len(routing), channel_counts


# ---------------------------------------------------------------------------
# Per-product semantic gaps
# ---------------------------------------------------------------------------
def build_gaps(product: str, action_index: dict[str, int],
               present_components: list[str], intent_count: int,
               risk_count: int, routing_count: int) -> dict:
    sub_counts: dict[str, int] = {}
    for sub in KC_SUBDOMAINS:
        d = kc_root(product) / sub
        sub_counts[sub] = sum(1 for _ in d.rglob("*.json")) if d.is_dir() else 0

    missing_actions = [a for a, _ in ACTION_LEXICON if a not in action_index]
    missing_components = [c for c, _, _ in COMPONENT_LEXICON if c not in present_components]
    missing_intents = [
        t["intent_id"] for t in INTENT_TEMPLATES
        if not (kc_root(product) / "visual-intent" / f"{t['intent_id']}.json").exists()
    ]

    payload = {
        "id": "semantic-gaps",
        "type": "semantic-gaps",
        "product": product,
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "kc_subdomain_counts": sub_counts,
        "missing_action_tokens": missing_actions,
        "missing_components": missing_components,
        "missing_visual_intents": missing_intents,
        "intent_count": intent_count,
        "risk_count": risk_count,
        "publication_routing_count": routing_count,
        "policy": "Gaps are explicit. They do NOT block downstream systems; they instruct future enrichment passes to look for missing tokens in OEM corpus refreshes (new manuals, supplemental OCR, structured-knowledge promotions).",
    }
    write_json(kc_root(product) / "semantic-gaps.json", payload)
    return payload


# ---------------------------------------------------------------------------
# Reset before rebuild
# ---------------------------------------------------------------------------
def reset_enrichment(product: str) -> None:
    import shutil
    root = kc_root(product)
    for sub in NEW_SUBDOMAINS:
        d = root / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    gaps_fp = root / "semantic-gaps.json"
    if gaps_fp.exists():
        gaps_fp.unlink()


# ---------------------------------------------------------------------------
# Cross-product reports
# ---------------------------------------------------------------------------
def build_reports(results: dict[str, dict]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    write_json(REPORTS / "01-semantic-enrichment-coverage.json",
               {"generated_at": NOW, "products": results})

    # Visual orchestration readiness — combines components + intents + risks.
    visrep = {"generated_at": NOW, "products": {}}
    for p, r in results.items():
        score = round(
            0.4 * (1.0 if r["procedural_semantics"] > 0 else 0.0)
            + 0.3 * (min(r["components"], 10) / 10.0)
            + 0.2 * (min(r["intents"], len(INTENT_TEMPLATES)) / len(INTENT_TEMPLATES))
            + 0.1 * (min(r["risks"], len(RISK_CATALOG)) / len(RISK_CATALOG)),
            3,
        )
        blockers: list[str] = []
        if r["procedural_semantics"] == 0:
            blockers.append("no procedural semantics (no procedure/workflow/installation entities had textual steps)")
        if r["components"] == 0:
            blockers.append("no recognised components in KC corpus")
        if r["intents"] == 0:
            blockers.append("no anchored visual intents")
        visrep["products"][p] = {
            "procedural_semantics": r["procedural_semantics"],
            "components_anchored": r["components"],
            "visual_intents": r["intents"],
            "visual_risks": r["risks"],
            "publication_routing_entries": r["publication_routing"],
            "visual_orchestration_score": score,
            "ready_for_comfy_intent_consumption": (
                r["procedural_semantics"] > 0 and r["components"] > 0 and r["intents"] > 0
            ),
            "blockers": blockers,
        }
    write_json(REPORTS / "02-visual-orchestration-readiness.json", visrep)

    # Comfy automation opportunities — list each visual-intent that has all anchors.
    opportunities: list[dict] = []
    for p, r in results.items():
        intent_dir = kc_root(p) / "visual-intent"
        if not intent_dir.is_dir():
            continue
        for fp in sorted(intent_dir.glob("*.json")):
            d = load_json(fp)
            opportunities.append(
                {
                    "product": p,
                    "intent_id": d["id"],
                    "summary": d["summary"],
                    "critical_components": d.get("critical_components", []),
                    "user_risk_level": d.get("user_risk_level"),
                    "visual_assistance_priority": d.get("visual_assistance_priority"),
                    "knowledge_core_anchor_path": relpath(fp),
                }
            )
    write_json(REPORTS / "03-comfy-automation-opportunities.json", {"generated_at": NOW, "opportunities": opportunities})

    # Aggregated semantic gaps.
    gaps = {"generated_at": NOW, "products": {}}
    for p in PRODUCTS:
        fp = kc_root(p) / "semantic-gaps.json"
        if fp.exists():
            gaps["products"][p] = load_json(fp)
    write_json(REPORTS / "04-aggregate-semantic-gaps.json", gaps)

    # Summary markdown.
    lines = [
        "# Phase 3 — Semantic enrichment + visual orchestration prep",
        "",
        f"_Generated {NOW} by `tools/knowledge_core_semantic_enrich.py`._",
        "",
        "## Per-product enrichment inventory",
        "",
        "| Product | proc-semantics | components | visual-intents | visual-risks | publication routing | comfy-ready |",
        "|---|---:|---:|---:|---:|---:|:---:|",
    ]
    for p, v in visrep["products"].items():
        ready = "✅" if v["ready_for_comfy_intent_consumption"] else "❌"
        lines.append(
            f"| {p} | {v['procedural_semantics']} | {v['components_anchored']} | {v['visual_intents']} | {v['visual_risks']} | {v['publication_routing_entries']} | {ready} |"
        )
    lines += [
        "",
        "## Visual orchestration score",
        "",
        "| Product | score |",
        "|---|---:|",
    ]
    for p, v in visrep["products"].items():
        lines.append(f"| {p} | {v['visual_orchestration_score']} |")
    lines += [
        "",
        "## Reports in this folder",
        "",
        "- 01-semantic-enrichment-coverage.json",
        "- 02-visual-orchestration-readiness.json",
        "- 03-comfy-automation-opportunities.json",
        "- 04-aggregate-semantic-gaps.json",
        "",
        "## Critical rules honoured",
        "",
        "- No manuals, PDFs, websites, marketing, or images generated.",
        "- No invented hardware, sensors, components, or procedures.",
        "- All enrichment vocabulary-anchored against existing knowledge-core entities.",
        "- ComfyUI is the only authorised downstream visual generator (recorded in every visual-intent).",
        "- Every emitted artifact carries source_refs + extraction_lineage.",
        "- Gaps recorded explicitly per product in `semantic-gaps.json`.",
    ]
    (REPORTS / "00-summary.md").write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    results: dict[str, dict] = {}
    for p in PRODUCTS:
        reset_enrichment(p)

        n_proc, action_index = build_procedural_semantics(p)
        n_comp, present_components = build_component_visibility(p)
        n_risk = build_visual_risk(p, present_components)
        n_intent = build_visual_intent(p, action_index, present_components)
        n_route, channel_counts = build_publication_intent(p)
        gaps = build_gaps(p, action_index, present_components, n_intent, n_risk, n_route)

        results[p] = {
            "procedural_semantics": n_proc,
            "action_token_index": action_index,
            "components": n_comp,
            "components_anchored": present_components,
            "risks": n_risk,
            "intents": n_intent,
            "publication_routing": n_route,
            "publication_channel_counts": channel_counts,
            "missing_action_tokens": gaps["missing_action_tokens"],
            "missing_components": gaps["missing_components"],
            "missing_visual_intents": gaps["missing_visual_intents"],
        }

    build_reports(results)

    print("Semantic enrichment complete.")
    for p, r in results.items():
        print(f"  {p}: proc={r['procedural_semantics']} comp={r['components']} intent={r['intents']} risk={r['risks']} route={r['publication_routing']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
