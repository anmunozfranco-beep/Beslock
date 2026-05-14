#!/usr/bin/env python3
"""Phase 2 — Semantic Knowledge Extraction Runtime.

Transforms normalized OEM manuals (and OCR fallbacks) inside each product
nucleus into atomic, provenance-bearing semantic knowledge entities.

This script is **non-destructive**:
  * It only writes under `<nucleus>/knowledge/`.
  * It never edits or replaces existing `structured-knowledge/`,
    `source-of-truth/`, `visual-system/`, or OEM source files.
  * Every emitted entity carries `source_refs` pointing back to the OEM-derived
    file and section it was derived from.

Outputs per product nucleus (`wp-content/themes/beslock-custom/User manuals/ext-images/<slug>/knowledge/`):

  entities/         — envelope index of every atomic entity emitted
  procedures/       — procedural knowledge (one JSON per procedure)
  installation/     — installation flows
  configuration/    — configuration / settings procedures
  operation/        — day-to-day operation procedures
  troubleshooting/  — symptom -> resolution units
  faq/              — question/answer pairs derived from OEM Q&A blocks
  capabilities/     — feature capabilities inferred from headings + access methods
  terminology/      — glossary candidates (OEM tokens, model codes, app names)
  workflows/        — multi-actor workflows (e.g. app pairing)
  semantic-index/   — index.json + per-entity-type indices used by RAG/search
  extracted-text/   — verbatim per-section snapshots (raw evidence)
  normalized/       — consolidated normalized-knowledge.json
  relationships/    — cross-references graph (adjacency-inferred edges)

A repository-wide report is written to
`wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/phase2-reports/`.

Run:
    python3 tools/knowledge_extraction.py
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
NUCLEI_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals" / "ext-images"
GENERATED_MANUALS_ROOT = REPO_ROOT / "generated_manuals"
REPORTS_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals" / "KNOWLEDGE_BUILDING" / "phase2-reports"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

KNOWLEDGE_SUBDIRS = [
    "entities",
    "procedures",
    "installation",
    "configuration",
    "operation",
    "troubleshooting",
    "faq",
    "capabilities",
    "terminology",
    "workflows",
    "semantic-index",
    "extracted-text",
    "normalized",
    "relationships",
]

SCHEMA_VERSION = "2.0"
LANGUAGE = "es-CO"
CHANNEL_TARGETS = ["web", "pdf", "support", "onboarding", "chatbot", "rag", "api"]


# ----------------------------------------------------------------------------
# Section parsing
# ----------------------------------------------------------------------------


@dataclass
class Section:
    n: int  # 1-based section index in the manual (top-level)
    sub_n: int  # 0 if top-level, otherwise subsection ordinal
    title: str
    body: str
    subsections: list["Section"] = field(default_factory=list)
    source_file: str = ""
    anchor: str = ""

    @property
    def lower_title(self) -> str:
        return self.title.lower()


HEADING_RE = re.compile(r"^(#{2,4})\s+(.*?)\s*$")
NUM_PREFIX_RE = re.compile(r"^\s*(\d+)[\.)]\s*(.*)$")


def parse_markdown(path: Path) -> list[Section]:
    """Parse a normalized OEM-derived markdown manual into top-level sections.

    The parser is intentionally conservative: it only recognises `##` (top
    section) and `###` (sub section). The very first `#` title is consumed as
    the document title and ignored.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    sections: list[Section] = []
    current_top: Section | None = None
    current_sub: Section | None = None
    buffer: list[str] = []

    def flush_buffer_into_current():
        nonlocal buffer
        if not buffer:
            return
        chunk = "\n".join(buffer).strip()
        target = current_sub if current_sub is not None else current_top
        if target is not None and chunk:
            target.body = (target.body + "\n" + chunk).strip() if target.body else chunk
        buffer = []

    top_index = 0
    sub_index = 0
    rel = path.relative_to(REPO_ROOT).as_posix()

    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            hashes, title = m.group(1), m.group(2).strip()
            depth = len(hashes)
            flush_buffer_into_current()

            if depth == 2:
                # New top section; close any previous sub
                current_sub = None
                top_index += 1
                sub_index = 0
                # Strip leading "N. " from the title
                m2 = NUM_PREFIX_RE.match(title)
                clean_title = m2.group(2).strip() if m2 else title
                current_top = Section(
                    n=top_index,
                    sub_n=0,
                    title=clean_title,
                    body="",
                    source_file=rel,
                    anchor=f"#{top_index}",
                )
                sections.append(current_top)
            elif depth >= 3 and current_top is not None:
                sub_index += 1
                clean_title = title
                current_sub = Section(
                    n=top_index,
                    sub_n=sub_index,
                    title=clean_title,
                    body="",
                    source_file=rel,
                    anchor=f"#{top_index}.{sub_index}",
                )
                current_top.subsections.append(current_sub)
            # depth == 1 is the document title; ignore.
            continue

        buffer.append(line)

    flush_buffer_into_current()

    return [s for s in sections if s.title]


def extract_steps(body: str) -> list[str]:
    """Pull numbered steps out of a section body.

    Recognises `1. ...`, `1) ...`, and `- [ ] 1. ...` prefixes. Lines that do
    not start with a numeric token are treated as continuations of the prior
    step.
    """
    steps: list[str] = []
    current: list[str] = []
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            if current:
                steps.append(" ".join(current).strip())
                current = []
            continue
        # Strip checkbox prefix
        line = re.sub(r"^\s*-\s*\[\s*[xX ]?\s*\]\s*", "", line)
        m = NUM_PREFIX_RE.match(line)
        if m:
            if current:
                steps.append(" ".join(current).strip())
            current = [m.group(2).strip()]
        else:
            if current:
                current.append(line.strip("- ").strip())
    if current:
        steps.append(" ".join(current).strip())
    # Filter empty / pure punctuation
    return [s for s in steps if s and len(s) > 1]


def extract_bullets(body: str) -> list[str]:
    bullets: list[str] = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            bullets.append(s[2:].strip())
    return bullets


# ----------------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------------


PROC_VERBS = (
    "agregar", "registrar", "cambiar", "configurar", "conectar", "vincular",
    "eliminar", "borrar", "restablecer", "reset", "inicializar", "actualizar",
    "abrir", "desbloquear", "bloquear", "habilitar", "deshabilitar", "activar",
    "desactivar", "ajustar", "renombrar", "compartir", "asignar",
)
INSTALL_KEYWORDS = (
    "instal", "montar", "montaje", "perforar", "preparar la puerta",
    "preparar puerta", "prepara la puerta", "compatibilidad fisica",
    "energia e inicializacion",
)
WARN_KEYWORDS = (
    "precauci", "advertenc", "warning", "atenci", "no retire", "no cuelgue",
    "limites de evidencia",
)
TERM_KEYWORDS = ("glosari", "terminolog", "definici")
FAQ_KEYWORDS = ("faq", "preguntas frecuentes", "preguntas y respuestas")
WORKFLOW_KEYWORDS = (
    "secuencia local", "alta desde", "vinculacion", "emparejamiento",
    "pairing", "qr y mini", "flujo de", "modo ez",
)
TROUBLESHOOT_KEYWORDS = (
    "no funciona", "si no", "si falla", "no responde", "solucion", "error",
    "no abre",
)
CAPABILITY_KEYWORDS = (
    "alcance", "que vas a", "metodos de acceso", "conectividad", "compatibilidad",
    "objetivo",
)
OVERVIEW_KEYWORDS = ("introducc", "primeros pasos", "objetivo", "alcance real")
VALIDATION_KEYWORDS = ("validacion despues", "que validar", "validar despues")


def classify_section(sec: Section) -> str:
    title = sec.lower_title
    body = sec.body.lower()

    if any(k in title for k in TERM_KEYWORDS):
        return "terminology"
    if any(k in title for k in FAQ_KEYWORDS):
        return "faq"
    if any(k in title for k in WARN_KEYWORDS):
        return "warning"
    if any(k in title for k in INSTALL_KEYWORDS):
        return "installation"
    if any(k in title for k in WORKFLOW_KEYWORDS):
        return "workflow"
    if any(k in title for k in TROUBLESHOOT_KEYWORDS) or any(k in body for k in TROUBLESHOOT_KEYWORDS):
        if any(k in title for k in PROC_VERBS):
            return "procedure"
        return "troubleshooting"
    if any(title.startswith(v) or f" {v}" in title for v in PROC_VERBS):
        return "procedure"
    if any(k in title for k in CAPABILITY_KEYWORDS):
        return "capability"
    if any(k in title for k in OVERVIEW_KEYWORDS):
        return "overview"
    if any(k in title for k in VALIDATION_KEYWORDS):
        return "procedure"
    return "other"


# Surface inference (where the action happens)
def infer_surface(sec: Section, manual_kind: str) -> str:
    title = sec.lower_title
    body = sec.body.lower()
    if manual_kind == "app":
        if "secuencia local" in title or "en la cerradura" in title:
            return "local-device"
        return "mobile-app"
    if manual_kind == "installation":
        return "physical-installation"
    if "app" in title or "tuya" in body or "smart life" in body:
        return "mobile-app"
    return "local-device"


def manual_kind(path: Path) -> str:
    name = path.name.lower()
    if "installation" in name or "instalacion" in name:
        return "installation"
    if "app manual" in name or "app-manual" in name:
        return "app"
    if "user manual" in name:
        return "user"
    if "starter pack" in name:
        return "implementation"
    if "supplemental" in name:
        return "supplemental"
    return "other"


# ----------------------------------------------------------------------------
# Entity emission
# ----------------------------------------------------------------------------


SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str, max_len: int = 64) -> str:
    s = value.lower().strip()
    # Strip accents (best-effort for es-CO)
    s = (
        s.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
         .replace("ú", "u").replace("ñ", "n").replace("ü", "u")
    )
    s = SLUG_RE.sub("-", s).strip("-")
    return s[:max_len] or "item"


def now_iso() -> str:
    return _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(
    *,
    entity_id: str,
    entity_type: str,
    product: str,
    summary: str,
    source_refs: list[str],
    validation_status: str = "extraction-pending-review",
) -> dict:
    return {
        "id": entity_id,
        "type": entity_type,
        "product": product,
        "summary": summary,
        "language": LANGUAGE,
        "validation_status": validation_status,
        "channel_targets": list(CHANNEL_TARGETS),
        "source_refs": source_refs,
        "related": {},
        "updated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
    }


# ----------------------------------------------------------------------------
# Terminology mining
# ----------------------------------------------------------------------------


# Common OEM tokens worth tracking when present in source text. Each pattern is
# tried verbatim in the source; matches that never occur are silently dropped.
TERM_CANDIDATES = [
    ("TUYA", "TUYA", ["TUYA APP", "Tuya"], "Plataforma OEM de aplicación móvil."),
    ("Smart Life", "Smart Life", [], "Aplicación móvil OEM compatible."),
    ("WeChat", "WeChat", [], "Plataforma china de mini-programas usada como canal OEM."),
    ("2.4G", "2.4G", ["2.4 GHz", "2.4Ghz"], "Banda de red Wi-Fi requerida."),
    ("EZ Mode", "EZ Mode", ["EZ"], "Modo de provisión rápida en TUYA."),
    ("AP Mode", "AP Mode", ["modo AP"], "Modo de provisión por punto de acceso."),
    ("QR", "QR", ["código QR", "codigo QR"], "Código gráfico de provisión."),
    ("PIN", "PIN", ["contraseña", "contrasena", "Contrasena"], "Código numérico de acceso."),
    ("huella", "huella", ["fingerprint"], "Credencial biométrica dactilar."),
    ("administrador", "administrador", ["administrator", "admin"], "Usuario con permisos de gestión."),
    ("Reset", "Reset", ["RESET", "reinicio"], "Acción o botón de inicialización."),
    ("Bluetooth", "Bluetooth", ["BLE"], "Canal inalámbrico de corto alcance."),
    ("Wi-Fi", "Wi-Fi", ["WiFi", "WIFI"], "Canal inalámbrico de red local."),
    ("IP66", "IP66", [], "Clasificación de protección ambiental."),
    ("IP68", "IP68", [], "Clasificación de protección ambiental."),
]


def mine_terminology(text: str, product: str, source_refs: list[str]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for canonical, primary, variants, definition in TERM_CANDIDATES:
        haystack = text
        if primary not in haystack and not any(v in haystack for v in variants):
            continue
        slug = slugify(canonical)
        if slug in seen:
            continue
        seen.add(slug)
        out.append({
            **envelope(
                entity_id=f"term-{slug}",
                entity_type="glossary-term",
                product=product,
                summary=definition,
                source_refs=source_refs,
                validation_status="normalized",
            ),
            "canonical": canonical,
            "oem_variants": [primary, *variants],
            "definition": definition,
        })
    return out


# ----------------------------------------------------------------------------
# Per-product extraction pipeline
# ----------------------------------------------------------------------------


@dataclass
class ProductExtraction:
    product: str
    nucleus: Path
    sections_seen: int = 0
    entities: list[dict] = field(default_factory=list)
    raw_text_files: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    sources_used: list[str] = field(default_factory=list)
    sources_missing: list[str] = field(default_factory=list)


def ensure_knowledge_dirs(nucleus: Path) -> Path:
    knowledge_root = nucleus / "knowledge"
    for sub in KNOWLEDGE_SUBDIRS:
        (knowledge_root / sub).mkdir(parents=True, exist_ok=True)
    # README so the directory purpose is self-documenting in the repo.
    readme = knowledge_root / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Phase 2 — Semantic Knowledge Runtime\n\n"
            "This folder is auto-managed by `tools/knowledge_extraction.py`.\n"
            "It contains atomic, provenance-bearing semantic entities derived\n"
            "from this product's OEM-aligned `source-of-truth/` materials.\n\n"
            "Do **not** hand-author files here without also updating the\n"
            "extractor or recording the override in `relationships/manual-overrides.json`.\n",
            encoding="utf-8",
        )
    return knowledge_root


STANDARD_SUB_TITLES = {
    "paso a paso", "ruta de menu", "ruta de menú",
    "que necesitas antes", "qué necesitas antes",
    "que validar despues", "qué validar después",
    "recomendacion", "recomendación",
}


def _aggregated_steps(sec: Section) -> list[str]:
    """Collect steps from a section: own body first, then any 'paso a paso' subs."""
    own = extract_steps(sec.body)
    if own:
        return own
    for sub in sec.subsections:
        if "paso a paso" in sub.lower_title or "pasos" in sub.lower_title:
            steps = extract_steps(sub.body)
            if steps:
                return steps
    # Fallback: any subsection whose body parses to >=2 numbered steps
    for sub in sec.subsections:
        steps = extract_steps(sub.body)
        if len(steps) >= 2:
            return steps
    return []


def _full_section_text(sec: Section, sub: Section | None) -> str:
    if sub is not None:
        return sub.body
    parts = [sec.body] + [f"### {s.title}\n{s.body}" for s in sec.subsections]
    return "\n\n".join(p for p in parts if p)


def section_to_entity(
    sec: Section,
    sub: Section | None,
    product: str,
    manual_kind_value: str,
) -> tuple[dict, str] | None:
    """Convert a (section, optional subsection) tuple into a typed entity.

    Returns `(entity, bucket)` or `None` if the section does not carry
    extractable knowledge (empty body, overview-only, etc.).
    """
    target = sub if sub is not None else sec
    full_text = _full_section_text(sec, sub)
    if not full_text.strip():
        return None

    section_class = classify_section(sec)
    if sub is None:
        steps = _aggregated_steps(sec)
    else:
        steps = extract_steps(sub.body)
    body = full_text
    bullets = extract_bullets(body)
    has_steps = len(steps) >= 2

    title_for_id = f"{sec.title}" if sub is None else f"{sec.title} {sub.title}"
    base_slug = slugify(title_for_id)
    surface = infer_surface(sec, manual_kind_value)
    src = f"{target.source_file}{target.anchor}"

    if section_class == "warning" or _is_warning_subsection(target):
        ent = envelope(
            entity_id=f"warning-{base_slug}",
            entity_type="warning",
            product=product,
            summary=_first_sentence(body) or sec.title,
            source_refs=[src],
        )
        ent["severity"] = "caution"
        ent["details"] = bullets or [body.strip()]
        return ent, "warning"

    if section_class == "terminology":
        # Terminology is harvested separately; skip section-level emission.
        return None

    if section_class == "faq":
        ent = envelope(
            entity_id=f"faq-{base_slug}",
            entity_type="faq",
            product=product,
            summary=sec.title,
            source_refs=[src],
        )
        ent["body"] = body.strip()
        return ent, "faq"

    if section_class == "installation" or manual_kind_value == "installation":
        if has_steps:
            ent = envelope(
                entity_id=f"install-{base_slug}",
                entity_type="installation-flow",
                product=product,
                summary=_first_sentence(body) or sec.title,
                source_refs=[src],
            )
            ent["surface"] = "physical-installation"
            ent["preconditions"] = _section_preconditions(sec)
            ent["steps"] = [{"n": i + 1, "text": s} for i, s in enumerate(steps)]
            ent["validation_checks"] = _section_validation(sec)
            return ent, "installation"
        # Installation overview / requirements
        ent = envelope(
            entity_id=f"install-context-{base_slug}",
            entity_type="installation-flow",
            product=product,
            summary=_first_sentence(body) or sec.title,
            source_refs=[src],
        )
        ent["surface"] = "physical-installation"
        ent["notes"] = bullets or [body.strip()]
        return ent, "installation"

    if section_class == "workflow" or (manual_kind_value == "app" and has_steps):
        ent = envelope(
            entity_id=f"wf-{base_slug}",
            entity_type="workflow",
            product=product,
            summary=_first_sentence(body) or sec.title,
            source_refs=[src],
        )
        ent["surface"] = surface
        ent["actors"] = _infer_actors(body)
        ent["steps"] = [{"n": i + 1, "text": s} for i, s in enumerate(steps)]
        ent["preconditions"] = _section_preconditions(sec)
        return ent, "workflows"

    if section_class == "procedure" or (has_steps and manual_kind_value == "user"):
        bucket = _procedure_bucket(sec, sub)
        title_summary = (sub.title if sub is not None else sec.title).strip()
        first_sent = _first_sentence(body)
        summary = title_summary if (not first_sent or len(first_sent) < 8) else first_sent
        ent = envelope(
            entity_id=f"proc-{base_slug}",
            entity_type="procedure",
            product=product,
            summary=summary,
            source_refs=[src],
        )
        ent["surface"] = surface
        ent["menu_path"] = _extract_menu_path(sec)
        ent["preconditions"] = _section_preconditions(sec)
        ent["steps"] = [{"n": i + 1, "text": s} for i, s in enumerate(steps)] if steps else []
        ent["validation_checks"] = _section_validation(sec)
        return ent, bucket

    if section_class == "troubleshooting":
        ent = envelope(
            entity_id=f"ts-{base_slug}",
            entity_type="troubleshooting",
            product=product,
            summary=sec.title,
            source_refs=[src],
        )
        ent["symptoms"] = [_first_sentence(body) or sec.title]
        ent["resolutions"] = steps or bullets or [body.strip()]
        return ent, "troubleshooting"

    if section_class == "capability":
        ent = envelope(
            entity_id=f"cap-{base_slug}",
            entity_type="capability",
            product=product,
            summary=_first_sentence(body) or sec.title,
            source_refs=[src],
        )
        ent["details"] = bullets or [body.strip()]
        return ent, "capabilities"

    return None


def _is_warning_subsection(sec: Section) -> bool:
    t = sec.lower_title
    return any(k in t for k in ("precauci", "advertenc", "atenci", "warning"))


def _first_sentence(body: str) -> str:
    body = body.strip()
    if not body:
        return ""
    # Skip headings, list markers (- only) and blockquotes; allow `*` so that
    # `**bold**` inline emphasis is not discarded.
    line = next(
        (
            l.strip()
            for l in body.splitlines()
            if l.strip() and not l.strip().startswith(("-", "#", ">"))
        ),
        body.split("\n", 1)[0],
    )
    line = line.strip("*_`> ")
    line = re.sub(r"\s+", " ", line)
    # Strip leading numbered-step prefix so "1. activa el panel" -> "activa el panel".
    line = re.sub(r"^\d+[\.\)]\s*", "", line)
    line = line.split(".")[0].strip()
    return line[:280]


def _section_preconditions(sec: Section) -> list[str]:
    for sub in sec.subsections:
        t = sub.lower_title
        if "necesitas antes" in t or "requisitos" in t or "antes de" in t:
            return [b for b in extract_bullets(sub.body) if b]
    # Top-level body fallback
    return []


def _section_validation(sec: Section) -> list[str]:
    for sub in sec.subsections:
        t = sub.lower_title
        if "validar despues" in t or "validacion" in t or "que validar" in t:
            return [b for b in extract_bullets(sub.body) if b]
    return []


def _extract_menu_path(sec: Section) -> str:
    for sub in sec.subsections:
        if "ruta de menu" in sub.lower_title or "ruta de menú" in sub.lower_title:
            text = sub.body.strip().splitlines()
            for line in text:
                clean = line.strip("* _`-").strip()
                if clean:
                    return clean
    return ""


def _infer_actors(body: str) -> list[str]:
    actors: list[str] = []
    low = body.lower()
    if "app" in low or "tuya" in low or "smart life" in low:
        actors.append("mobile-app")
    if "cerradura" in low or "panel" in low or "dispositivo" in low:
        actors.append("device")
    if "usuario" in low or "administrador" in low or "instala" in low:
        actors.append("user")
    return actors or ["user", "device"]


def _procedure_bucket(sec: Section, sub: Section | None) -> str:
    title = (sub.title if sub else sec.title).lower()
    if any(k in title for k in ("instal", "montar", "perforar")):
        return "installation"
    if any(k in title for k in ("ajustar", "configurar", "idioma", "volumen", "seleccionar", "modo")):
        return "configuration"
    return "operation"


# ----------------------------------------------------------------------------
# OCR fallback (generated_manuals/<product>/manual.json)
# ----------------------------------------------------------------------------


def ingest_ocr_fallback(product: str) -> list[dict]:
    """Emit lightweight evidence stubs from the OCR archive.

    These are marked `inferred-but-unverified` so downstream readers know the
    text is verbatim OCR output, not normalized OEM truth.
    """
    path = GENERATED_MANUALS_ROOT / product / "manual.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    src = path.relative_to(REPO_ROOT).as_posix()
    out: list[dict] = []
    for idx, sec in enumerate(data.get("sections", []), start=1):
        title = (sec.get("title") or "").strip()
        if not title:
            continue
        content_lines = sec.get("content") or []
        body = "\n".join(content_lines).strip()
        if not body:
            continue
        slug = slugify(f"ocr-{title}-{idx}")
        ent = envelope(
            entity_id=f"ocr-{slug}",
            entity_type="extracted-text",
            product=product,
            summary=title[:200],
            source_refs=[f"{src}#section-{idx}"],
            validation_status="inferred-but-unverified",
        )
        ent["semantic_category"] = sec.get("semantic_category", "Unknown")
        ent["raw_text"] = body
        out.append(ent)
    return out


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_product(product: str) -> ProductExtraction:
    nucleus = NUCLEI_ROOT / product
    knowledge_root = ensure_knowledge_dirs(nucleus)
    result = ProductExtraction(product=product, nucleus=nucleus)

    manuals_dir = nucleus / "source-of-truth" / "manuals"
    md_files = sorted(p for p in manuals_dir.glob("*.md") if p.is_file()) if manuals_dir.exists() else []

    if not md_files:
        result.sources_missing.append(str(manuals_dir.relative_to(REPO_ROOT)))
        result.gaps.append(
            f"No normalized markdown manuals available under {manuals_dir.relative_to(REPO_ROOT)}; "
            "only OCR fallback will be emitted."
        )

    all_text_chunks: list[str] = []
    bucket_counts: dict[str, int] = {}

    for md in md_files:
        result.sources_used.append(md.relative_to(REPO_ROOT).as_posix())
        kind = manual_kind(md)
        sections = parse_markdown(md)
        result.sections_seen += sum(1 + len(s.subsections) for s in sections)

        for sec in sections:
            # Verbatim snapshot for evidence layer
            snapshot_path = knowledge_root / "extracted-text" / f"{slugify(md.stem)}__{sec.n:02d}-{slugify(sec.title)}.txt"
            snapshot = f"# {sec.title}\n\nSource: {sec.source_file}{sec.anchor}\n\n{sec.body}\n"
            for sub in sec.subsections:
                snapshot += f"\n\n## {sub.title}\n\nSource: {sub.source_file}{sub.anchor}\n\n{sub.body}\n"
            snapshot_path.write_text(snapshot, encoding="utf-8")
            result.raw_text_files.append(snapshot_path.relative_to(knowledge_root).as_posix())
            all_text_chunks.append(snapshot)

            # Top-level entity
            outcome = section_to_entity(sec, None, product, kind)
            if outcome is not None:
                ent, bucket = outcome
                _persist_entity(knowledge_root, bucket, ent)
                result.entities.append(ent)
                bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
            else:
                # Empty / overview-only section is fine; just skip.
                pass

            # Subsection entities — only when they carry independent meaning
            # beyond what the parent section already rolled up.
            parent_class = classify_section(sec)
            parent_emitted = outcome is not None
            for sub in sec.subsections:
                if sub.lower_title.strip() in STANDARD_SUB_TITLES:
                    continue
                if not sub.body.strip():
                    continue
                # Warnings are always worth emitting independently.
                if _is_warning_subsection(sub):
                    sub_outcome = section_to_entity(sec, sub, product, kind)
                    if sub_outcome is not None:
                        ent, bucket = sub_outcome
                        _persist_entity(knowledge_root, bucket, ent)
                        result.entities.append(ent)
                        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
                    continue
                # Otherwise emit only when the subsection has its own step block
                # AND the parent did not already emit a procedure (otherwise we
                # would duplicate rolled-up content).
                sub_steps = extract_steps(sub.body)
                if len(sub_steps) < 2:
                    continue
                if parent_emitted and parent_class in ("procedure", "installation", "workflow"):
                    continue
                sub_outcome = section_to_entity(sec, sub, product, kind)
                if sub_outcome is None:
                    continue
                ent, bucket = sub_outcome
                _persist_entity(knowledge_root, bucket, ent)
                result.entities.append(ent)
                bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1

    # Terminology (mined across all manuals)
    if md_files:
        joined = "\n".join(p.read_text(encoding="utf-8") for p in md_files)
        glossary = mine_terminology(joined, product, [p.relative_to(REPO_ROOT).as_posix() for p in md_files])
        for term in glossary:
            _persist_entity(knowledge_root, "terminology", term)
            result.entities.append(term)
        bucket_counts["terminology"] = bucket_counts.get("terminology", 0) + len(glossary)

    # OCR fallback evidence
    ocr_entities = ingest_ocr_fallback(product)
    for ent in ocr_entities:
        _persist_entity(knowledge_root, "extracted-text", ent, file_kind="json")
    if ocr_entities:
        bucket_counts["ocr-evidence"] = len(ocr_entities)
        result.entities.extend(ocr_entities)

    # Gap detection — installation / app / user manual presence
    have_kinds = {manual_kind(p) for p in md_files}
    for required in ("user", "installation", "app"):
        if required not in have_kinds:
            result.gaps.append(f"Missing normalized {required} manual under source-of-truth/manuals/.")

    # Ambiguity detection — sections without steps but classified as procedure
    for ent in result.entities:
        if ent["type"] == "procedure" and not ent.get("steps"):
            result.ambiguities.append(
                f"Procedure {ent['id']} has no extractable numbered steps (source: {ent['source_refs'][0]})."
            )

    # Indices and aggregates
    _emit_indices(knowledge_root, product, result.entities, bucket_counts)
    _emit_relationships(knowledge_root, product, result.entities)
    _emit_normalized(knowledge_root, product, result.entities)

    # Per-product extraction report
    write_json(knowledge_root / "extraction-report.json", {
        "product": product,
        "generated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
        "sources_used": result.sources_used,
        "sources_missing": result.sources_missing,
        "sections_seen": result.sections_seen,
        "entities_emitted": len(result.entities),
        "bucket_counts": bucket_counts,
        "gaps": result.gaps,
        "ambiguities": result.ambiguities[:50],
        "ambiguity_total": len(result.ambiguities),
    })

    return result


def _persist_entity(knowledge_root: Path, bucket: str, entity: dict, *, file_kind: str = "json") -> None:
    target_dir = knowledge_root / bucket
    target_dir.mkdir(parents=True, exist_ok=True)
    entity["storage_bucket"] = bucket
    fname = f"{entity['id']}.{file_kind}"
    write_json(target_dir / fname, entity)


def _emit_indices(knowledge_root: Path, product: str, entities: list[dict], bucket_counts: dict[str, int]) -> None:
    by_type: dict[str, list[dict]] = {}
    for ent in entities:
        by_type.setdefault(ent["type"], []).append({
            "id": ent["id"],
            "summary": ent["summary"],
            "source_refs": ent["source_refs"],
            "validation_status": ent["validation_status"],
        })

    write_json(knowledge_root / "semantic-index" / "index.json", {
        "product": product,
        "generated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
        "language": LANGUAGE,
        "channel_targets": CHANNEL_TARGETS,
        "totals": {"entities": len(entities), **bucket_counts},
        "by_type": {k: [e["id"] for e in v] for k, v in by_type.items()},
    })

    for type_name, lst in by_type.items():
        write_json(knowledge_root / "semantic-index" / f"by-type-{type_name}.json", lst)

    # Entities envelope manifest (lightweight cross-list)
    write_json(knowledge_root / "entities" / "manifest.json", [
        {
            "id": e["id"],
            "type": e["type"],
            "summary": e["summary"],
            "validation_status": e["validation_status"],
            "source_refs": e["source_refs"],
        }
        for e in entities
    ])


def _emit_relationships(knowledge_root: Path, product: str, entities: list[dict]) -> None:
    """Emit adjacency-inferred edges between entities sharing a source manual.

    Edges are kept conservative: a procedure that lives in the same manual as
    a warning gets a `co-located-with` edge, marked `inferred-by-adjacency`.
    """
    edges: list[dict] = []

    by_source: dict[str, list[dict]] = {}
    for ent in entities:
        for src in ent["source_refs"]:
            base = src.split("#", 1)[0]
            by_source.setdefault(base, []).append(ent)

    for src, group in by_source.items():
        warnings = [e for e in group if e["type"] == "warning"]
        procedures = [e for e in group if e["type"] in ("procedure", "installation-flow", "workflow")]
        for proc in procedures:
            for w in warnings:
                edges.append({
                    "from": f"{proc['type']}:{proc['id']}",
                    "to": f"warning:{w['id']}",
                    "rel": "co-located-with",
                    "evidence": src,
                    "validation_status": "inferred-by-adjacency",
                })
        # Procedure -> terminology references
        for proc in procedures:
            text = " ".join(s.get("text", "") if isinstance(s, dict) else str(s) for s in proc.get("steps", []))
            for term in (e for e in entities if e["type"] == "glossary-term"):
                if term.get("canonical") and term["canonical"].lower() in text.lower():
                    edges.append({
                        "from": f"{proc['type']}:{proc['id']}",
                        "to": f"glossary-term:{term['id']}",
                        "rel": "references",
                        "evidence": "step-text-match",
                        "validation_status": "inferred-by-text-match",
                    })

    write_json(knowledge_root / "relationships" / "cross-references.json", {
        "product": product,
        "generated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
        "edges": edges,
        "edge_total": len(edges),
        "policy": (
            "Only adjacency- and text-match-inferred edges are emitted. "
            "Verified semantic edges must be authored in manual-overrides.json."
        ),
    })

    overrides = knowledge_root / "relationships" / "manual-overrides.json"
    if not overrides.exists():
        write_json(overrides, {
            "product": product,
            "edges": [],
            "policy": "Author verified semantic edges here. Each edge must include `source_refs`.",
        })


def _emit_normalized(knowledge_root: Path, product: str, entities: list[dict]) -> None:
    write_json(knowledge_root / "normalized" / "normalized-knowledge.json", {
        "product": product,
        "generated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
        "language": LANGUAGE,
        "entities": entities,
    })


# ----------------------------------------------------------------------------
# Repo-level reports
# ----------------------------------------------------------------------------


def emit_repo_reports(extractions: list[ProductExtraction]) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    inventory = {
        "generated_at": now_iso(),
        "schema_version": SCHEMA_VERSION,
        "products": {
            x.product: {
                "sources_used": x.sources_used,
                "sources_missing": x.sources_missing,
                "sections_seen": x.sections_seen,
                "entities_emitted": len(x.entities),
                "by_type": _count_by_type(x.entities),
            }
            for x in extractions
        },
    }
    write_json(REPORTS_ROOT / "01-extracted-knowledge-inventory.json", inventory)

    gaps = {
        "generated_at": now_iso(),
        "products": {x.product: x.gaps for x in extractions},
    }
    write_json(REPORTS_ROOT / "02-unresolved-extraction-gaps.json", gaps)

    terminology = {
        "generated_at": now_iso(),
        "products": {
            x.product: sorted({e["id"] for e in x.entities if e["type"] == "glossary-term"})
            for x in extractions
        },
        "policy": (
            "Glossary terms are mined from a fixed candidate vocabulary. Terms that surface in only "
            "one product are candidates for verification. Add new candidates in TERM_CANDIDATES."
        ),
    }
    write_json(REPORTS_ROOT / "03-unresolved-terminology.json", terminology)

    ambiguities = {
        "generated_at": now_iso(),
        "products": {x.product: x.ambiguities for x in extractions},
        "policy": (
            "Procedures listed here had no extractable numbered steps. They likely require manual "
            "review of the OEM source before being marked verified."
        ),
    }
    write_json(REPORTS_ROOT / "04-ambiguous-oem-language.json", ambiguities)

    visual_unsupported = {
        "generated_at": now_iso(),
        "policy": (
            "Phase 2 does not consume visual content. Visual interpretation entities are not produced by "
            "this extractor; they remain owned by visual-system/ and the canonical PNG truth source. "
            "Any OEM diagram interpretation must be authored manually with a `visual-constraint` envelope."
        ),
        "products": {
            x.product: {
                "visual_constraint_entities": sum(1 for e in x.entities if e["type"] == "visual-constraint"),
                "note": "Visual-constraint emission deferred to visual-system pipeline.",
            }
            for x in extractions
        },
    }
    write_json(REPORTS_ROOT / "05-unsupported-visual-interpretation.json", visual_unsupported)

    semantic_coverage = {
        "generated_at": now_iso(),
        "matrix": {
            x.product: {
                bucket: sum(1 for e in x.entities if _bucket_for(e) == bucket)
                for bucket in [
                    "installation", "configuration", "operation", "workflows",
                    "warning", "troubleshooting", "capabilities",
                    "terminology", "faq",
                ]
            }
            for x in extractions
        },
        "policy": "Per-bucket counts of emitted entities. 0 = bucket empty (gap).",
    }
    write_json(REPORTS_ROOT / "06-semantic-coverage.json", semantic_coverage)

    rag_readiness = {
        "generated_at": now_iso(),
        "products": {
            x.product: {
                "entities": len(x.entities),
                "extracted_text_files": len(x.raw_text_files),
                "has_index": (x.nucleus / "knowledge" / "semantic-index" / "index.json").exists(),
                "has_normalized": (x.nucleus / "knowledge" / "normalized" / "normalized-knowledge.json").exists(),
                "has_relationships": (x.nucleus / "knowledge" / "relationships" / "cross-references.json").exists(),
                "blockers": [
                    *(["No normalized OEM markdown sources"] if not x.sources_used else []),
                    *(["Embeddings layer not yet generated (out of Phase 2 scope)"]),
                ],
            }
            for x in extractions
        },
        "next_steps": [
            "Generate vector embeddings per entity (Phase 3).",
            "Author manual-overrides.json edges for verified semantic relationships.",
            "Promote `extraction-pending-review` entities to `verified` after human review.",
        ],
    }
    write_json(REPORTS_ROOT / "07-rag-readiness.json", rag_readiness)

    # Top-level human-readable summary
    summary_md = ["# Phase 2 — Semantic Knowledge Extraction Summary", "",
                  f"_Generated {now_iso()}_", "",
                  "| Product | Sources | Sections | Entities | Procedures | Installation | Warnings | Workflows | Terminology |",
                  "|---|---|---|---|---|---|---|---|---|"]
    for x in extractions:
        counts = _count_by_type(x.entities)
        summary_md.append(
            "| {p} | {srcs} | {secs} | {ent} | {pro} | {ins} | {warn} | {wf} | {term} |".format(
                p=x.product,
                srcs=len(x.sources_used),
                secs=x.sections_seen,
                ent=len(x.entities),
                pro=counts.get("procedure", 0),
                ins=counts.get("installation-flow", 0),
                warn=counts.get("warning", 0),
                wf=counts.get("workflow", 0),
                term=counts.get("glossary-term", 0),
            )
        )
    summary_md.append("")
    summary_md.append("Reports: `01-extracted-knowledge-inventory.json` ... `07-rag-readiness.json` in this folder.")
    (REPORTS_ROOT / "00-summary.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")


def _count_by_type(entities: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in entities:
        out[e["type"]] = out.get(e["type"], 0) + 1
    return out


def _bucket_for(entity: dict) -> str:
    if entity.get("storage_bucket"):
        return entity["storage_bucket"]
    t = entity["type"]
    if t == "installation-flow":
        return "installation"
    if t == "workflow":
        return "workflow"
    if t == "warning":
        return "warning"
    if t == "troubleshooting":
        return "troubleshooting"
    if t == "capability":
        return "capability"
    if t == "glossary-term":
        return "terminology"
    if t == "faq":
        return "faq"
    if t == "procedure":
        # configuration vs operation buckets recorded only via folder, not type
        return "procedure"
    return t


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    if not NUCLEI_ROOT.exists():
        print(f"ERROR: nucleus root not found: {NUCLEI_ROOT}", file=sys.stderr)
        return 2

    extractions: list[ProductExtraction] = []
    for product in PRODUCTS:
        nucleus = NUCLEI_ROOT / product
        if not nucleus.exists():
            print(f"WARN: nucleus missing for {product}: {nucleus}")
            continue
        print(f"==> extracting {product}")
        ext = extract_product(product)
        extractions.append(ext)
        print(f"    sections={ext.sections_seen} entities={len(ext.entities)} gaps={len(ext.gaps)}")

    emit_repo_reports(extractions)
    _write_eorbit_reconciliation()
    print(f"\nReports written to {REPORTS_ROOT.relative_to(REPO_ROOT)}")
    return 0


def _write_eorbit_reconciliation() -> None:
    target = (
        NUCLEI_ROOT
        / "e-orbit"
        / "knowledge"
        / "relationships"
        / "legacy-structured-knowledge-reconciliation.json"
    )
    if not (NUCLEI_ROOT / "e-orbit" / "knowledge").exists():
        return
    payload = {
        "product": "e-orbit",
        "policy": (
            "Phase 2 does not overwrite the pre-existing verified `structured-knowledge/` "
            "reference implementation. This pointer file declares the canonical relationship "
            "between the two layers."
        ),
        "legacy_layer": {
            "root": "wp-content/themes/beslock-custom/User manuals/ext-images/e-orbit/structured-knowledge",
            "validation_status": "verified",
            "owners": ["Phase 1 reference implementation"],
            "files_of_record": [
                "structured-knowledge/manual.json",
                "structured-knowledge/glossary.json",
                "structured-knowledge/faq.json",
                "structured-knowledge/workflows.json",
                "structured-knowledge/features/capabilities.json",
                "structured-knowledge/procedures/procedure-catalog.json",
                "structured-knowledge/semantic-relations/knowledge-graph.json",
            ],
        },
        "phase2_layer": {
            "root": "wp-content/themes/beslock-custom/User manuals/ext-images/e-orbit/knowledge",
            "default_validation_status": "extraction-pending-review",
            "purpose": (
                "Atomized, per-entity files derived directly from `source-of-truth/manuals/*.md` "
                "for RAG, support, and chatbot retrieval."
            ),
            "reconciliation_rules": [
                "When a Phase 2 entity overlaps a verified Phase 1 entity, the Phase 1 file is the source of truth.",
                "Promote Phase 2 entities to `verified` only after they are reviewed against the Phase 1 reference and the OEM source.",
                "Do not edit `structured-knowledge/` from this folder; record any reconciliation in `relationships/manual-overrides.json`.",
            ],
        },
    }
    write_json(target, payload)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
