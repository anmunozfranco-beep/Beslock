#!/usr/bin/env python3
"""Phase 2 — Build the canonical Beslock product knowledge core.

Read-only over OEM sources and the existing `knowledge/` and
`structured-knowledge/` layers. Writes a brand-new
`ext-images/<slug>/knowledge-core/` per product plus cross-product reports
under `KNOWLEDGE_BUILDING/phase2-execution-reports/`.

Idempotent: re-running rewrites the `knowledge-core/` and reports.
Never touches `knowledge/`, `structured-knowledge/`, `source-of-truth/`, or
`generated_manuals*/`.

Decisions encoded (set by user during Phase 2 kickoff):
  * Additive — `knowledge-core/` lives alongside `knowledge/`.
  * OCR-derived drafts allowed for OCR-only domains, marked
    `inferred-but-unverified` with explicit confidence.
  * Supplemental PDFs OCR'd into `generated_manuals_supplemental/<slug-N>/`
    are promoted as `extracted-text` evidence with `non-canonical` flag.
  * `e-Orbit_1.xls` (NF14) ingested deterministically.
  * For e-orbit, when `structured-knowledge/` overlaps the Phase 2
    `knowledge/` layer, structured-knowledge wins and is promoted as
    `validation_status: verified`.

NEVER fabricates entities, procedures, capabilities, or visual semantics.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
NUCLEI = REPO / "wp-content/themes/beslock-custom/User manuals/ext-images"
REPORTS = REPO / "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/phase2-execution-reports"
GEN_OCR = REPO / "generated_manuals"
GEN_OCR_SUP = REPO / "generated_manuals_supplemental"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "knowledge-core/1.0"

SUBDOMAINS = (
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
    "provenance",
    "visual",
    "orchestration",
)

# Map from existing knowledge/ bucket folder → knowledge-core/ subdomain.
LEGACY_BUCKET_MAP = {
    "installation": "install",
    "operation": "operation",
    "procedures": "operation",  # generic procedure folder if used
    "workflows": "workflows",
    "troubleshooting": "troubleshooting",
    "warning": "warnings",
    "warnings": "warnings",
    "terminology": "terminology",
    "capabilities": "capabilities",
    "configuration": "operation",
    "faq": "operation",
    "extracted-text": "semantic",  # semantic/extracted-text/
}

# Misclassified entities to relocate (auditor-confirmed).
RELOCATIONS = {
    # e-orbit ts-paginas-prioritarias-para-fase-1 is a sitemap / routing list,
    # not a symptom/resolution pair.
    ("e-orbit", "troubleshooting", "ts-paginas-prioritarias-para-fase-1"): (
        "orchestration",
        "publishing-priority-pages",
    ),
}

# Manifest duplicates to collapse (auditor-confirmed).
DUP_COLLAPSES = {
    ("e-orbit", "cap-objetivo"): 1,  # keep 1 of the 3 occurrences
}


def slug_to_display(slug: str) -> str:
    return "e-" + slug.split("-", 1)[1].capitalize()


def now() -> str:
    return NOW


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# Helpers — load existing artifacts
# ---------------------------------------------------------------------------
def load_legacy_knowledge(product: str) -> list[tuple[str, dict]]:
    """Return list of (legacy_bucket, entity_payload) from `knowledge/`."""
    base = NUCLEI / product / "knowledge"
    out: list[tuple[str, dict]] = []
    if not base.is_dir():
        return out
    for bucket in (
        "installation",
        "operation",
        "procedures",
        "workflows",
        "troubleshooting",
        "warning",
        "warnings",
        "terminology",
        "capabilities",
        "configuration",
        "faq",
        "extracted-text",
    ):
        d = base / bucket
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.json")):
            try:
                payload = load_json(fp)
            except Exception:
                continue
            payload.setdefault("storage_bucket", bucket)
            out.append((bucket, payload))
    return out


def load_structured_knowledge_orbit() -> dict[str, Any]:
    """Load the Phase 1 verified e-orbit `structured-knowledge/` payloads."""
    base = NUCLEI / "e-orbit" / "structured-knowledge"
    if not base.is_dir():
        return {}
    out: dict[str, Any] = {}
    for rel in (
        "glossary.json",
        "faq.json",
        "workflows.json",
        "features/capabilities.json",
        "procedures/procedure-catalog.json",
        "semantic-relations/knowledge-graph.json",
    ):
        fp = base / rel
        if fp.exists():
            out[rel] = load_json(fp)
    return out


def load_ocr(product: str) -> dict:
    fp = GEN_OCR / product / "manual.json"
    return load_json(fp) if fp.exists() else {}


def load_supplemental_ocr(slug_with_n: str) -> dict:
    fp = GEN_OCR_SUP / slug_with_n / "manual.json"
    return load_json(fp) if fp.exists() else {}


# ---------------------------------------------------------------------------
# Provenance envelope
# ---------------------------------------------------------------------------
LANG_DEFAULT = "es-CO"


def envelope(
    *,
    eid: str,
    etype: str,
    product: str,
    summary: str,
    source_refs: list[str],
    validation_status: str,
    confidence: float | str,
    ocr_dependency: str = "none",
    lineage: list[str] | None = None,
    extra: dict | None = None,
    language: str = LANG_DEFAULT,
) -> dict:
    out = {
        "id": eid,
        "type": etype,
        "product": product,
        "summary": summary,
        "language": language,
        "validation_status": validation_status,
        "confidence": confidence,
        "ocr_dependency": ocr_dependency,
        "channel_targets": [
            "web",
            "pdf",
            "support",
            "onboarding",
            "chatbot",
            "rag",
            "api",
        ],
        "source_refs": source_refs,
        "extraction_lineage": lineage or [],
        "schema_version": SCHEMA,
        "updated_at": NOW,
    }
    if extra:
        # Don't overwrite envelope fields by accident.
        for k, v in extra.items():
            if k not in out:
                out[k] = v
    return out


def safe_filename(eid: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", eid.lower()).strip("-") + ".json"


# ---------------------------------------------------------------------------
# Promotion: legacy knowledge/ → knowledge-core/
# ---------------------------------------------------------------------------
def promote_legacy(product: str, core: Path) -> tuple[int, list[str]]:
    """Promote legacy entities, applying relocation + dedup rules."""
    seen_ids: set[tuple[str, str]] = set()  # (subdomain, id)
    legacy_id_promotions = 0
    notes: list[str] = []

    for bucket, ent in load_legacy_knowledge(product):
        eid = ent.get("id")
        if not eid:
            continue

        # Default subdomain mapping.
        subdomain = LEGACY_BUCKET_MAP.get(bucket, "operation")

        # Relocation overrides.
        relkey = (product, bucket, eid)
        if relkey in RELOCATIONS:
            subdomain, new_eid = RELOCATIONS[relkey]
            ent = {**ent, "id": new_eid, "type": ent.get("type")}
            ent["relocation_note"] = (
                f"Relocated from knowledge/{bucket}/ to knowledge-core/{subdomain}/ "
                "after Phase 2B audit (entity is a publishing/sitemap list, not a symptom/resolution pair)."
            )
            ent["original_storage_bucket"] = bucket
            eid = new_eid

        # Manifest dedup.
        dupkey = (product, eid)
        if dupkey in DUP_COLLAPSES:
            keep = DUP_COLLAPSES[dupkey]
            count = sum(1 for s, i in seen_ids if i == eid)
            if count >= keep:
                continue

        # Special handling: extracted-text bucket lives under semantic/extracted-text/
        if bucket == "extracted-text":
            target_dir = core / "semantic" / "extracted-text"
        else:
            target_dir = core / subdomain

        unique_key = (subdomain, eid)
        if unique_key in seen_ids:
            continue
        seen_ids.add(unique_key)

        # Build the canonical envelope, preserving payload fields verbatim
        # but stamping the new schema_version + lineage.
        legacy_status = ent.get("validation_status", "extraction-pending-review")
        # Confidence for promoted Phase 2 entities:
        if legacy_status == "inferred-but-unverified":
            confidence = "ocr-fallback-low"
            ocr_dep = "full"
        elif legacy_status == "normalized":
            confidence = "high"
            ocr_dep = "none"
        else:
            confidence = "medium"
            ocr_dep = "none"

        env = envelope(
            eid=eid,
            etype=ent.get("type", "entity"),
            product=product,
            summary=ent.get("summary", ""),
            source_refs=ent.get("source_refs", []),
            validation_status=legacy_status,
            confidence=confidence,
            ocr_dependency=ocr_dep,
            lineage=[
                f"knowledge/{bucket}/{safe_filename(eid)}",
            ],
            extra={
                k: v
                for k, v in ent.items()
                if k
                not in (
                    "id",
                    "type",
                    "product",
                    "summary",
                    "language",
                    "validation_status",
                    "channel_targets",
                    "source_refs",
                    "schema_version",
                    "updated_at",
                    "storage_bucket",
                )
            },
        )
        env["legacy_storage_bucket"] = bucket
        write_json(target_dir / safe_filename(eid), env)
        legacy_id_promotions += 1

    return legacy_id_promotions, notes


# ---------------------------------------------------------------------------
# Promotion: structured-knowledge/ (e-orbit only, verified layer)
# ---------------------------------------------------------------------------
ORBIT_VERIFIED_PROVENANCE = "wp-content/themes/beslock-custom/User manuals/ext-images/e-orbit/structured-knowledge"


def promote_structured_orbit(core: Path) -> int:
    sk = load_structured_knowledge_orbit()
    if not sk:
        return 0
    n = 0

    # Glossary → terminology/ (verified)
    for entry in sk.get("glossary.json", {}).get("entries", []):
        eid = "term-" + re.sub(r"[^a-z0-9]+", "-", entry["term"].lower()).strip("-")
        env = envelope(
            eid=eid,
            etype="glossary-term",
            product="e-orbit",
            summary=entry["term"],
            source_refs=entry.get("source_refs", [])
            + [f"{ORBIT_VERIFIED_PROVENANCE}/glossary.json"],
            validation_status="verified",
            confidence="high",
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/glossary.json"],
            language="en",
            extra={
                "term": entry["term"],
                "definition": entry["definition"],
                "domain": entry.get("domain"),
                "verified_layer": "structured-knowledge",
            },
        )
        write_json(core / "terminology" / safe_filename(eid), env)
        n += 1

    # FAQ → operation/faq/
    for f in sk.get("faq.json", {}).get("faq", []):
        eid = "faq-" + f["id"]
        env = envelope(
            eid=eid,
            etype="faq",
            product="e-orbit",
            summary=f["question"],
            source_refs=f.get("source_refs", [])
            + [f"{ORBIT_VERIFIED_PROVENANCE}/faq.json"],
            validation_status="verified",
            confidence=f.get("confidence", "high"),
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/faq.json"],
            language="en",
            extra={"question": f["question"], "answer": f["answer"]},
        )
        write_json(core / "operation" / "faq" / safe_filename(eid), env)
        n += 1

    # Workflows → workflows/ (verified, EN)
    for w in sk.get("workflows.json", {}).get("workflows", []):
        eid = "wf-" + w["id"]
        env = envelope(
            eid=eid,
            etype="workflow",
            product="e-orbit",
            summary=w["title"],
            source_refs=[f"{ORBIT_VERIFIED_PROVENANCE}/workflows.json#{w['id']}"],
            validation_status="verified",
            confidence="high",
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/workflows.json"],
            language="en",
            extra={
                "surface": w.get("surface"),
                "outcomes": w.get("outcomes", []),
                "preconditions": w.get("preconditions", []),
                "steps": w.get("steps", []),
                "validation_checks": w.get("validation_checks", []),
                "authorized_visual_renderer": "ComfyUI",
            },
        )
        write_json(core / "workflows" / safe_filename(eid), env)
        n += 1

    # Procedures → operation/ (verified, EN)
    for p in sk.get("procedures/procedure-catalog.json", {}).get("procedures", []):
        eid = "proc-" + p["id"]
        env = envelope(
            eid=eid,
            etype="procedure",
            product="e-orbit",
            summary=p.get("menu_path") or p.get("id"),
            source_refs=[
                f"{ORBIT_VERIFIED_PROVENANCE}/procedures/procedure-catalog.json#{p['id']}"
            ],
            validation_status="verified",
            confidence="high",
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/procedures/procedure-catalog.json"],
            language="en",
            extra={
                "surface": p.get("surface"),
                "menu_path": p.get("menu_path"),
                "steps": p.get("steps", []),
                "validation_checks": p.get("validation_checks", []),
            },
        )
        write_json(core / "operation" / safe_filename(eid), env)
        n += 1

    # Capabilities → capabilities/ (verified, structured map)
    feats = sk.get("features/capabilities.json", {}).get("capabilities", {})
    if feats:
        env = envelope(
            eid="cap-map-verified",
            etype="capability-map",
            product="e-orbit",
            summary="Verified capability + identity map for e-Orbit (NF14)",
            source_refs=[f"{ORBIT_VERIFIED_PROVENANCE}/features/capabilities.json"],
            validation_status="verified",
            confidence="high",
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/features/capabilities.json"],
            language="en",
            extra={"capabilities": feats},
        )
        write_json(core / "capabilities" / "cap-map-verified.json", env)
        n += 1

    # Knowledge graph → semantic/relationships/
    kg = sk.get("semantic-relations/knowledge-graph.json", {})
    if kg:
        env = envelope(
            eid="rel-knowledge-graph-verified",
            etype="knowledge-graph",
            product="e-orbit",
            summary="Verified e-Orbit semantic graph (Phase 1 structured-knowledge)",
            source_refs=[f"{ORBIT_VERIFIED_PROVENANCE}/semantic-relations/knowledge-graph.json"],
            validation_status="verified",
            confidence="high",
            ocr_dependency="none",
            lineage=[f"{ORBIT_VERIFIED_PROVENANCE}/semantic-relations/knowledge-graph.json"],
            language="en",
            extra={"nodes": kg.get("nodes", []), "edges": kg.get("edges", [])},
        )
        write_json(core / "semantic" / "relationships" / "knowledge-graph-verified.json", env)
        n += 1

    return n


# ---------------------------------------------------------------------------
# XLS ingestion: e-Orbit_1.xls
# ---------------------------------------------------------------------------
ORBIT_XLS = NUCLEI / "e-orbit/source-of-truth/specifications/e-Orbit_1.xls"


def ingest_orbit_xls(core: Path) -> bool:
    if not ORBIT_XLS.exists():
        return False
    import xlrd

    book = xlrd.open_workbook(str(ORBIT_XLS))
    sheet = book.sheet_by_index(0)

    # Column layout (verified manually before authoring this script):
    # col 0 = item key, col 1 = value continuation, col 5 = language code map.
    spec_rows: list[dict[str, str]] = []
    current_key: str | None = None
    current_values: list[str] = []
    for r in range(sheet.nrows):
        key = (sheet.cell_value(r, 0) or "").strip()
        val = (sheet.cell_value(r, 1) or "").strip()
        if key and key != "Remark:":
            # close prior
            if current_key is not None:
                spec_rows.append(
                    {"key": current_key, "value": "\n".join(current_values).strip()}
                )
            current_key = key
            current_values = [val] if val else []
        elif key == "Remark:":
            if current_key is not None:
                spec_rows.append(
                    {"key": current_key, "value": "\n".join(current_values).strip()}
                )
            current_key = "Remark"
            current_values = [val] if val else []
        else:
            if val:
                current_values.append(val)
    if current_key is not None:
        spec_rows.append({"key": current_key, "value": "\n".join(current_values).strip()})

    languages: list[dict[str, str]] = []
    for r in range(sheet.nrows):
        cell = (sheet.cell_value(r, 5) or "").strip() if sheet.ncols > 5 else ""
        if not cell:
            continue
        # Format: "3009 Spanish" or "Tuya- Enter 888#..."
        m = re.match(r"^(\d{3,4})\s*[\u2003\s]+(.+)$", cell)
        if m:
            languages.append({"code": m.group(1), "name": m.group(2).strip()})

    page_ref = f"{ORBIT_XLS.relative_to(REPO).as_posix()}#sheet=Sheet1"
    env = envelope(
        eid="hardware-nf14",
        etype="hardware-specification",
        product="e-orbit",
        summary="OEM hardware specification sheet for e-Orbit (model NF14)",
        source_refs=[ORBIT_XLS.relative_to(REPO).as_posix()],
        validation_status="verified",
        confidence="high",
        ocr_dependency="none",
        lineage=[ORBIT_XLS.relative_to(REPO).as_posix()],
        language="en",
        extra={
            "model": "NF14",
            "spec_rows": spec_rows,
            "supported_language_codes": languages,
            "ingestion_method": "xlrd-deterministic",
            "ingestion_caveats": [
                "User-capacity counts in the OEM XLS reflect Tuya/Tongtong firmware tiers and have historically conflicted with the NX5 menu text — do not promote them as canonical without commercial confirmation.",
                "IP rating row carries an OEM-side caveat: actual grade IP68 is custom-order; suggested customer-facing grade is IP66; rear panel is not waterproof.",
            ],
        },
    )
    write_json(core / "specifications" / "hardware-nf14.json", env)
    return True


# ---------------------------------------------------------------------------
# Supplemental OCR promotion (5 PDFs)
# ---------------------------------------------------------------------------
SUPPLEMENTALS = [
    # (slug-folder under generated_manuals_supplemental, source_pdf path, owner product)
    ("e-shield-1", NUCLEI / "e-shield/source-of-truth/manuals/e-Shield_1.pdf", "e-shield"),
    ("e-shied-2", NUCLEI / "e-shield/source-of-truth/manuals/e-Shied_2.pdf", "e-shield"),
    ("e-prime-1", NUCLEI / "e-prime/source-of-truth/manuals/e-Prime_1.pdf", "e-prime"),
    ("e-prime-2", NUCLEI / "e-prime/source-of-truth/manuals/e-Prime_2.pdf", "e-prime"),
    ("e-orbit-2", NUCLEI / "e-orbit/source-of-truth/manuals/e-Orbit_2.pdf", "e-orbit"),
]


def confidence_tier(avg_conf: float) -> tuple[str, str]:
    """Map OCR avg confidence (0-100) to (tier, validation_status)."""
    if avg_conf >= 85:
        return "ocr-good", "inferred-but-unverified"
    if avg_conf >= 70:
        return "ocr-medium", "inferred-but-unverified"
    if avg_conf >= 50:
        return "ocr-low", "low-confidence-evidence"
    return "ocr-very-low", "low-confidence-evidence-only"


def promote_supplementals(per_product_cores: dict[str, Path]) -> dict:
    summary: dict[str, list[dict]] = {p: [] for p in PRODUCTS}
    for slug_n, pdf_path, owner in SUPPLEMENTALS:
        ocr = load_supplemental_ocr(slug_n)
        if not ocr:
            continue
        avg = float(ocr.get("avg_confidence", 0))
        tier, vstatus = confidence_tier(avg)
        ocr_path = (GEN_OCR_SUP / slug_n / "manual.json").relative_to(REPO).as_posix()
        sections = ocr.get("sections", [])
        steps = ocr.get("steps", [])
        warnings = ocr.get("warnings", [])
        app_instr = ocr.get("app_instructions", [])
        specs = ocr.get("specifications", [])

        # Promote each section as one extracted-text evidence entity.
        n_emitted = 0
        for i, sec in enumerate(sections):
            text = sec.get("content") if isinstance(sec, dict) else str(sec)
            title = sec.get("title", f"section-{i+1}") if isinstance(sec, dict) else f"section-{i+1}"
            page = sec.get("page", "?") if isinstance(sec, dict) else "?"
            eid = f"sup-{slug_n}-section-{i+1:03d}"
            env = envelope(
                eid=eid,
                etype="extracted-text",
                product=owner,
                summary=title[:200],
                source_refs=[
                    f"{pdf_path.relative_to(REPO).as_posix()}#page={page}",
                    f"{ocr_path}#sections[{i}]",
                ],
                validation_status=vstatus,
                confidence=tier,
                ocr_dependency="full",
                lineage=[ocr_path],
                language="es-CO",
                extra={
                    "title": title,
                    "page": page,
                    "text": text,
                    "ocr_avg_confidence": avg,
                    "non_canonical": True,
                    "candidate_for_semantic_extraction": True,
                    "supplemental_source": slug_n,
                },
            )
            write_json(per_product_cores[owner] / "semantic" / "extracted-text-supplemental" / safe_filename(eid), env)
            n_emitted += 1

        # Warnings → warnings/ as candidate
        for j, w in enumerate(warnings):
            text = w.get("text") if isinstance(w, dict) else str(w)
            page = w.get("page", "?") if isinstance(w, dict) else "?"
            eid = f"sup-{slug_n}-warning-{j+1:03d}"
            env = envelope(
                eid=eid,
                etype="warning",
                product=owner,
                summary=text[:200],
                source_refs=[
                    f"{pdf_path.relative_to(REPO).as_posix()}#page={page}",
                    f"{ocr_path}#warnings[{j}]",
                ],
                validation_status=vstatus,
                confidence=tier,
                ocr_dependency="full",
                lineage=[ocr_path],
                language="es-CO",
                extra={
                    "text": text,
                    "page": page,
                    "non_canonical": True,
                    "candidate_for_semantic_extraction": True,
                    "supplemental_source": slug_n,
                },
            )
            write_json(per_product_cores[owner] / "warnings" / "supplemental-candidates" / safe_filename(eid), env)
            n_emitted += 1

        # App instructions → operation/ as candidate
        for j, ai in enumerate(app_instr):
            text = ai.get("text") if isinstance(ai, dict) else str(ai)
            page = ai.get("page", "?") if isinstance(ai, dict) else "?"
            eid = f"sup-{slug_n}-app-{j+1:03d}"
            env = envelope(
                eid=eid,
                etype="extracted-text",
                product=owner,
                summary=("[app] " + text)[:200],
                source_refs=[
                    f"{pdf_path.relative_to(REPO).as_posix()}#page={page}",
                    f"{ocr_path}#app_instructions[{j}]",
                ],
                validation_status=vstatus,
                confidence=tier,
                ocr_dependency="full",
                lineage=[ocr_path],
                language="es-CO",
                extra={
                    "channel": "app",
                    "text": text,
                    "page": page,
                    "non_canonical": True,
                    "candidate_for_semantic_extraction": True,
                    "supplemental_source": slug_n,
                },
            )
            write_json(per_product_cores[owner] / "semantic" / "extracted-text-supplemental" / safe_filename(eid), env)
            n_emitted += 1

        # Steps → operation/ as candidate (do NOT package them as procedures yet)
        for j, st in enumerate(steps):
            text = st.get("text") if isinstance(st, dict) else str(st)
            page = st.get("page", "?") if isinstance(st, dict) else "?"
            eid = f"sup-{slug_n}-step-{j+1:03d}"
            env = envelope(
                eid=eid,
                etype="extracted-text",
                product=owner,
                summary=("[step] " + text)[:200],
                source_refs=[
                    f"{pdf_path.relative_to(REPO).as_posix()}#page={page}",
                    f"{ocr_path}#steps[{j}]",
                ],
                validation_status=vstatus,
                confidence=tier,
                ocr_dependency="full",
                lineage=[ocr_path],
                language="es-CO",
                extra={
                    "channel": "step-candidate",
                    "text": text,
                    "page": page,
                    "non_canonical": True,
                    "candidate_for_semantic_extraction": True,
                    "supplemental_source": slug_n,
                },
            )
            write_json(per_product_cores[owner] / "semantic" / "extracted-text-supplemental" / safe_filename(eid), env)
            n_emitted += 1

        summary[owner].append(
            {
                "supplemental_source": slug_n,
                "pdf_path": pdf_path.relative_to(REPO).as_posix(),
                "pdf_md5": md5_of(pdf_path),
                "pdf_pages": ocr.get("pages"),
                "ocr_method": ocr.get("ocr_method"),
                "ocr_avg_confidence": avg,
                "confidence_tier": tier,
                "validation_status_assigned": vstatus,
                "entities_emitted": n_emitted,
                "non_canonical": True,
            }
        )
    return summary


# ---------------------------------------------------------------------------
# OCR-derived drafts for products without normalized markdown (e-nova)
# ---------------------------------------------------------------------------
def emit_ocr_drafts(product: str, core: Path) -> int:
    """Emit conservative OCR-derived candidate entities, never marked verified."""
    ocr = load_ocr(product)
    if not ocr:
        return 0
    avg = float(ocr.get("avg_confidence", 0))
    tier, vstatus = confidence_tier(avg)
    ocr_path = (GEN_OCR / product / "manual.json").relative_to(REPO).as_posix()
    pdf_path = ocr.get("source_pdf")
    n = 0
    # Already in legacy `knowledge/extracted-text/` so we only emit the
    # consolidated step/warning/app candidate index here, to make the OCR
    # draft surface explicit in the new core.
    consolidated = {
        "id": "ocr-draft-index",
        "type": "ocr-draft-index",
        "product": product,
        "summary": f"OCR-derived candidate index for {product} (no normalized markdown source)",
        "language": LANG_DEFAULT,
        "validation_status": vstatus,
        "confidence": tier,
        "ocr_dependency": "full",
        "channel_targets": ["chatbot", "rag", "support"],
        "source_refs": [ocr_path] + ([pdf_path] if pdf_path else []),
        "extraction_lineage": [ocr_path],
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "ocr_method": ocr.get("ocr_method"),
        "ocr_pages": ocr.get("pages"),
        "ocr_avg_confidence": avg,
        "section_count": len(ocr.get("sections", [])),
        "step_candidate_count": len(ocr.get("steps", [])),
        "warning_candidate_count": len(ocr.get("warnings", [])),
        "app_instruction_candidate_count": len(ocr.get("app_instructions", [])),
        "specification_candidate_count": len(ocr.get("specifications", [])),
        "feature_candidate_count": len(ocr.get("features", [])),
        "non_canonical": True,
        "policy": "OCR-DERIVED DRAFTS: candidates may be promoted to verified entities only after a human reviews them against the OEM PDF.",
    }
    write_json(core / "semantic" / "ocr-draft-index.json", consolidated)
    n += 1
    return n


# ---------------------------------------------------------------------------
# Entity catalog: derive product entity inventory from existing artifacts
# ---------------------------------------------------------------------------
# Curated whitelist of entity vocabulary observed across normalized manuals.
# Entries are intentionally conservative; if a token does not match any source
# text, no entity is emitted for that product.
ENTITY_VOCAB: list[tuple[str, str, list[str]]] = [
    # (canonical_id, kind, surface phrases observed in OEM/normalized manuals)
    ("entity-fingerprint-sensor", "hardware", ["fingerprint", "huella"]),
    ("entity-keypad", "hardware", ["keypad", "teclado", "panel táctil", "panel"]),
    ("entity-handle-exterior", "hardware", ["handle", "manija", "exterior handle"]),
    ("entity-handle-interior", "hardware", ["thumbturn", "knob", "perilla interior"]),
    ("entity-lock-body", "hardware", ["lock body", "cuerpo de la cerradura", "6068", "lock body"]),
    ("entity-emergency-power", "hardware", ["emergency power", "usb-c", "type-c", "alimentación de emergencia"]),
    ("entity-mechanical-key", "hardware", ["mechanical key", "llave mecánica", "llave"]),
    ("entity-buzzer", "hardware", ["buzzer", "speaker", "altavoz", "voice prompt"]),
    ("entity-led-indicator", "hardware", ["led", "indicator", "indicador"]),
    ("entity-deadbolt", "hardware", ["deadbolt", "pasador", "cerrojo"]),
    ("entity-latch", "hardware", ["latch", "pestillo"]),
    ("entity-ic-card-reader", "hardware", ["ic card", "tarjeta", "rfid"]),
    ("entity-face-recognition", "hardware", ["face recognition", "facial", "rostro"]),
    ("entity-palm-vein", "hardware", ["palm vein", "vena palmar"]),
    ("entity-tuya-app", "software", ["tuya", "tuya smart", "smart life"]),
    ("entity-tongtong-app", "software", ["tongtong"]),
    ("entity-administrator-user", "role", ["administrator", "administrador"]),
    ("entity-regular-user", "role", ["regular user", "usuario", "user"]),
    ("entity-temporary-password", "feature", ["temporary password", "contraseña temporal"]),
    ("entity-anti-lock-mode", "feature", ["anti-lock", "anti-lockout"]),
    ("entity-auto-lock", "feature", ["auto-lock", "auto lock", "bloqueo automático"]),
]


def collect_product_text_corpus(product: str) -> str:
    """Concatenate normalized manuals + supplemental OCR text for entity matching."""
    chunks: list[str] = []
    base = NUCLEI / product / "source-of-truth/manuals"
    if base.is_dir():
        for fp in base.glob("*.md"):
            chunks.append(fp.read_text(errors="ignore"))
    spec_review = NUCLEI / product / "source-of-truth/specifications"
    if spec_review.is_dir():
        for fp in spec_review.glob("*.md"):
            chunks.append(fp.read_text(errors="ignore"))
    # OCR primary
    ocr = load_ocr(product)
    for sec in ocr.get("sections", []):
        if isinstance(sec, dict):
            c = sec.get("content", "")
            if isinstance(c, list):
                c = "\n".join(str(x) for x in c)
            chunks.append(c if isinstance(c, str) else str(c))
    # OCR supplementals owned by this product
    for slug_n, _, owner in SUPPLEMENTALS:
        if owner != product:
            continue
        sup = load_supplemental_ocr(slug_n)
        for sec in sup.get("sections", []):
            if isinstance(sec, dict):
                c = sec.get("content", "")
                if isinstance(c, list):
                    c = "\n".join(str(x) for x in c)
                chunks.append(c if isinstance(c, str) else str(c))
    return "\n".join(chunks).lower()


def build_entity_catalog(product: str, core: Path) -> int:
    corpus = collect_product_text_corpus(product)
    if not corpus.strip():
        return 0
    entities: list[dict] = []
    for eid, kind, phrases in ENTITY_VOCAB:
        hits = [p for p in phrases if p.lower() in corpus]
        if not hits:
            continue
        entities.append(
            {
                "id": eid,
                "kind": kind,
                "matched_surface_terms": hits,
                "evidence_corpus": "normalized-manuals + spec-review + ocr-fallback + supplemental-ocr",
            }
        )
    if not entities:
        return 0
    catalog = {
        "id": "entity-catalog",
        "type": "entity-catalog",
        "product": product,
        "summary": f"Entities observed in {product} OEM corpus",
        "language": LANG_DEFAULT,
        "validation_status": "extraction-pending-review",
        "confidence": "medium",
        "ocr_dependency": "partial",
        "channel_targets": ["chatbot", "rag", "support", "onboarding"],
        "source_refs": [
            f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/source-of-truth/"
        ],
        "extraction_lineage": [
            "tools/knowledge_core_build.py::build_entity_catalog::ENTITY_VOCAB"
        ],
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "policy": "Vocabulary-anchored. An entity is only emitted when at least one OEM-source text fragment matches a curated surface phrase. No inference beyond surface presence.",
        "entities": entities,
    }
    write_json(core / "entities" / "entity-catalog.json", catalog)
    return len(entities)


# ---------------------------------------------------------------------------
# Capability map (verified-where-possible, derived elsewhere)
# ---------------------------------------------------------------------------
CAPABILITY_VOCAB = [
    ("cap-fingerprint-unlock", ["fingerprint", "huella"]),
    ("cap-pin-unlock", ["pin", "contraseña", "password"]),
    ("cap-ic-card-unlock", ["ic card", "tarjeta", "rfid"]),
    ("cap-face-unlock", ["face recognition", "facial"]),
    ("cap-palm-vein-unlock", ["palm vein", "vena palmar"]),
    ("cap-bluetooth-pairing", ["bluetooth"]),
    ("cap-wifi-tuya-integration", ["tuya wifi", "tuya"]),
    ("cap-emergency-unlock-mechanical-key", ["mechanical key", "llave mecánica", "llave"]),
    ("cap-emergency-unlock-usb", ["usb-c", "emergency power", "type-c"]),
    ("cap-auto-lock", ["auto-lock", "auto lock", "bloqueo automático"]),
    ("cap-anti-lock", ["anti-lock", "anti-lockout"]),
    ("cap-low-battery-alert", ["low battery", "batería baja"]),
    ("cap-temporary-password", ["temporary password", "contraseña temporal"]),
    ("cap-remote-unlock", ["remote unlock", "desbloqueo remoto"]),
    ("cap-multi-language", ["language", "idioma"]),
]


def build_capability_map(product: str, core: Path) -> int:
    corpus = collect_product_text_corpus(product)
    caps = []
    for cid, phrases in CAPABILITY_VOCAB:
        hits = [p for p in phrases if p.lower() in corpus]
        if not hits:
            continue
        caps.append({"id": cid, "matched_surface_terms": hits})
    if not caps:
        return 0
    payload = {
        "id": "capability-map",
        "type": "capability-map",
        "product": product,
        "summary": f"Capabilities surfaced from {product} OEM corpus (vocabulary-anchored)",
        "language": LANG_DEFAULT,
        "validation_status": "extraction-pending-review",
        "confidence": "medium",
        "ocr_dependency": "partial",
        "channel_targets": ["chatbot", "rag", "web", "onboarding"],
        "source_refs": [
            f"wp-content/themes/beslock-custom/User manuals/ext-images/{product}/source-of-truth/"
        ],
        "extraction_lineage": [
            "tools/knowledge_core_build.py::build_capability_map::CAPABILITY_VOCAB"
        ],
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "policy": "Vocabulary-anchored. Capabilities are surfaced ONLY when the OEM corpus contains the matched phrase. No inference, no claims.",
        "capabilities": caps,
    }
    write_json(core / "capabilities" / "capability-map.json", payload)
    return len(caps)


# ---------------------------------------------------------------------------
# Visual semantic map
# ---------------------------------------------------------------------------
def build_visual_semantic_map(product: str, core: Path) -> int:
    base = NUCLEI / product
    images_dir = base / "source-of-truth/product-images"
    visual_system = base / "visual-system"
    pngs: list[str] = []
    if images_dir.is_dir():
        pngs = [
            p.relative_to(REPO).as_posix()
            for p in sorted(images_dir.rglob("*.png"))
        ]
    prompt_files: list[str] = []
    if (visual_system / "prompts").is_dir():
        prompt_files = [
            p.relative_to(REPO).as_posix()
            for p in sorted((visual_system / "prompts").glob("*.md"))
        ]
    matrices: list[str] = []
    if (visual_system / "generation-matrices").is_dir():
        matrices = [
            p.relative_to(REPO).as_posix()
            for p in sorted((visual_system / "generation-matrices").glob("*.md"))
        ]
    payload = {
        "id": "visual-semantic-map",
        "type": "visual-semantic-map",
        "product": product,
        "summary": f"OEM visual reference index for {product}",
        "language": "en",
        "validation_status": "extraction-pending-review",
        "confidence": "medium",
        "ocr_dependency": "none",
        "channel_targets": ["comfyui", "support", "rag"],
        "source_refs": [base.relative_to(REPO).as_posix()],
        "extraction_lineage": ["tools/knowledge_core_build.py::build_visual_semantic_map"],
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "trusted_visual_references": pngs,
        "prompt_packs": prompt_files,
        "generation_matrices": matrices,
        "authorized_visual_renderer": "ComfyUI",
        "prohibited": [
            "midjourney",
            "dall-e production pipelines",
            "external visual systems",
            "hallucinated geometry",
            "fake product variants",
            "hand-drawn human figures (per visual system reset 2026-05-13)",
        ],
        "policy": "All future production imagery for this product MUST originate from a ComfyUI workflow that consumes the trusted_visual_references PNGs as anchor inputs. Component geometry, sensor location, keypad layout, and handle position must NOT be inferred outside the OEM PNGs and the verified `structured-knowledge/` (where present).",
    }
    write_json(core / "visual" / "visual-semantic-map.json", payload)
    return 1 if pngs else 0


# ---------------------------------------------------------------------------
# Orchestration metadata
# ---------------------------------------------------------------------------
def build_orchestration(product: str, core: Path) -> None:
    payload = {
        "id": "comfyui-readiness",
        "type": "orchestration-readiness",
        "product": product,
        "language": "en",
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "authorized_visual_renderer": "ComfyUI",
        "policy": [
            "All visual generation is ComfyUI-only.",
            "No Midjourney, no DALL-E production pipelines, no external visual systems.",
            "No hallucinated geometry. No fake product variants.",
            "Comfy prompts MUST cite a `visual/visual-semantic-map.json` trusted reference.",
        ],
        "downstream_consumers": [
            "comfy-prompts",
            "comfy-workflows",
            "visual-qa",
            "chatbot-answers",
            "future-pdfs",
            "future-websites",
            "onboarding-systems",
            "installation-diagrams",
            "troubleshooting-visuals",
            "video-generation",
        ],
        "knowledge_core_consumes": [
            f"ext-images/{product}/knowledge-core/visual/visual-semantic-map.json",
            f"ext-images/{product}/knowledge-core/capabilities/capability-map.json",
            f"ext-images/{product}/knowledge-core/entities/entity-catalog.json",
            f"ext-images/{product}/knowledge-core/specifications/",
        ],
    }
    write_json(core / "orchestration" / "comfyui-readiness.json", payload)


# ---------------------------------------------------------------------------
# Provenance manifest (per product)
# ---------------------------------------------------------------------------
def build_provenance(product: str, core: Path) -> dict:
    base = NUCLEI / product
    sources: list[dict] = []
    sot_root = base / "source-of-truth"
    if sot_root.is_dir():
        for root, _, files in __import__("os").walk(sot_root):
            for f in sorted(files):
                if f.startswith("."):
                    continue
                fp = Path(root) / f
                rel = fp.relative_to(REPO).as_posix()
                ext = fp.suffix.lower()
                row = {
                    "path": rel,
                    "ext": ext,
                    "size_bytes": fp.stat().st_size,
                }
                if ext == ".pdf":
                    row["md5"] = md5_of(fp)
                    is_user_manual = f.lower().endswith("user manual.pdf")
                    row["semantic_pipeline_status"] = (
                        "ocr-fallback (extracted-text only)"
                        if is_user_manual
                        else "ocr-supplemental (extracted-text-supplemental)"
                        if any(p[1].name == f for p in SUPPLEMENTALS)
                        else "not-ingested"
                    )
                elif ext in (".xls", ".xlsx") and product == "e-orbit" and f == "e-Orbit_1.xls":
                    row["semantic_pipeline_status"] = "verified-deterministic-ingest"
                elif ext == ".md":
                    row["semantic_pipeline_status"] = "normalized-markdown-canonical"
                else:
                    row["semantic_pipeline_status"] = "reference-or-render"
                sources.append(row)
    # Hash duplicates
    md5_groups: dict[str, list[str]] = {}
    for s in sources:
        if "md5" in s:
            md5_groups.setdefault(s["md5"], []).append(s["path"])
    for s in sources:
        if "md5" in s and len(md5_groups[s["md5"]]) > 1:
            s["duplicate_of"] = md5_groups[s["md5"]]

    manifest = {
        "id": f"oem-source-index-{product}",
        "type": "oem-source-index",
        "product": product,
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "policy": "Every OEM source artifact in source-of-truth/ is listed here with its semantic pipeline status. PDFs flagged 'not-ingested' have NO representation in knowledge-core except via supplemental OCR (where present).",
        "sources": sources,
    }
    write_json(core / "provenance" / "oem-source-index.json", manifest)
    return manifest


# ---------------------------------------------------------------------------
# Per-product manifest (final summary)
# ---------------------------------------------------------------------------
def write_product_manifest(product: str, core: Path) -> dict:
    counts: dict[str, int] = {}
    for sub in SUBDOMAINS:
        d = core / sub
        if not d.is_dir():
            counts[sub] = 0
            continue
        n = sum(1 for _ in d.rglob("*.json"))
        counts[sub] = n
    manifest = {
        "id": f"manifest-{product}",
        "type": "knowledge-core-manifest",
        "product": product,
        "schema_version": SCHEMA,
        "updated_at": NOW,
        "subdomain_counts": counts,
        "subdomains": list(SUBDOMAINS),
    }
    write_json(core / "MANIFEST.json", manifest)
    return manifest


def write_readme(product: str, core: Path) -> None:
    text = f"""# {product} — Knowledge Core

Schema: `{SCHEMA}`. Generated {NOW} by `tools/knowledge_core_build.py`.

This layer is **additive** alongside the legacy `knowledge/` and (for e-orbit)
`structured-knowledge/` layers. Every artifact carries provenance back to an
OEM source under `source-of-truth/` or to the OCR fallback under
`generated_manuals*/`.

## Subdomains

| Subdomain | Purpose |
|---|---|
| install/ | Installation procedures and installation flows. |
| operation/ | Day-to-day operation procedures, configuration, FAQ. |
| workflows/ | End-to-end multi-step workflows (onboarding, pairing, reset, etc). |
| troubleshooting/ | Symptom → resolution entries. |
| warnings/ | OEM warnings and safety notices. |
| terminology/ | Glossary terms. |
| entities/ | Hardware / software / role entity catalog (vocabulary-anchored). |
| capabilities/ | Capability maps (vocabulary-anchored). |
| specifications/ | Hardware specification sheets (e.g. NF14 XLS). |
| semantic/ | Extracted-text evidence, relationships, OCR drafts. |
| provenance/ | OEM source index + extraction lineage. |
| visual/ | Trusted visual references + ComfyUI input contract. |
| orchestration/ | Downstream system contracts (ComfyUI-only). |

## Validation status legend

| Status | Meaning |
|---|---|
| `verified` | Promoted from `structured-knowledge/` (Phase 1) or deterministic spec ingest. Safe for production. |
| `extraction-pending-review` | Authored from normalized markdown by Phase 2 extractor. Needs human review. |
| `inferred-but-unverified` | OCR-derived candidate. Not safe for canonical use. |
| `low-confidence-evidence` | OCR with avg confidence 50–70 %. Evidence-only. |
| `low-confidence-evidence-only` | OCR with avg confidence < 50 %. Evidence-only, do not surface. |

## Critical rules

1. Do not generate final manuals, PDFs, marketing assets, or website pages from
   this layer until each consuming flow has explicit approval.
2. Visual generation downstream of this layer is **ComfyUI-only**.
3. Never edit a `verified` artifact without updating the source under
   `structured-knowledge/` or `source-of-truth/specifications/` first.
4. Never promote a `low-confidence-evidence-only` entity to a higher status
   without independent OEM PDF confirmation.
"""
    (core / "README.md").write_text(text)


# ---------------------------------------------------------------------------
# Cross-product reports
# ---------------------------------------------------------------------------
def build_reports(product_results: dict[str, dict]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    # 1 — semantic-extraction-coverage.json
    cov = {
        "generated_at": NOW,
        "products": {p: r["manifest"]["subdomain_counts"] for p, r in product_results.items()},
    }
    write_json(REPORTS / "01-semantic-extraction-coverage.json", cov)

    # 2 — unresolved-ocr-risks.json
    risks: list[dict] = []
    for p, r in product_results.items():
        for sup in r.get("supplementals", []):
            if sup["confidence_tier"] in ("ocr-low", "ocr-very-low"):
                risks.append(
                    {
                        "product": p,
                        "supplemental_source": sup["supplemental_source"],
                        "pdf_path": sup["pdf_path"],
                        "ocr_avg_confidence": sup["ocr_avg_confidence"],
                        "confidence_tier": sup["confidence_tier"],
                        "risk": "Promoted as evidence-only. Do not surface to chatbot/RAG without human review against the OEM PDF.",
                    }
                )
        # OCR-only product
        if not (NUCLEI / p / "source-of-truth/manuals").glob("*.md"):
            pass  # generator: keeps below
    # Always check normalized-markdown presence
    for p in PRODUCTS:
        normalized = list((NUCLEI / p / "source-of-truth/manuals").glob("*.md"))
        if not normalized:
            risks.append(
                {
                    "product": p,
                    "risk": "OCR-only product. Knowledge core relies entirely on OCR fallback with no normalized markdown counterpart. All operational entities are inferred-but-unverified.",
                    "ocr_avg_confidence": load_ocr(p).get("avg_confidence"),
                }
            )
    write_json(REPORTS / "02-unresolved-ocr-risks.json", risks)

    # 3 — missing-oem-knowledge.json
    missing: list[dict] = []
    expected_doc_types = {
        "user_manual": "<Display> user manual.md (or .pdf)",
        "installation_manual": "<Display> installation manual.md",
        "app_manual": "<Display> app manual.md",
        "spec_sheet": "<Display>_*.xls or supplemental source review",
    }
    for p in PRODUCTS:
        manuals = list((NUCLEI / p / "source-of-truth/manuals").glob("*"))
        names = " ".join(m.name.lower() for m in manuals)
        m_missing = []
        if "user manual.md" not in names:
            m_missing.append("normalized user-manual markdown")
        if "installation manual.md" not in names:
            m_missing.append("normalized installation-manual markdown")
        if "app manual.md" not in names:
            m_missing.append("normalized app-manual markdown")
        spec = list((NUCLEI / p / "source-of-truth/specifications").glob("*"))
        if not spec:
            m_missing.append("any spec sheet or supplemental source review")
        if m_missing:
            missing.append({"product": p, "missing": m_missing})
    write_json(REPORTS / "03-missing-oem-knowledge.json", {"generated_at": NOW, "items": missing})

    # 4 — semantic-completeness-scorecard.json
    scorecard = {"generated_at": NOW, "products": {}}
    for p, r in product_results.items():
        counts = r["manifest"]["subdomain_counts"]
        operational_dims = [
            "install",
            "operation",
            "workflows",
            "troubleshooting",
            "warnings",
            "terminology",
            "entities",
            "capabilities",
            "specifications",
        ]
        present = sum(1 for d in operational_dims if counts.get(d, 0) > 0)
        breadth = round(present / len(operational_dims), 3)
        normalized_present = bool(
            list((NUCLEI / p / "source-of-truth/manuals").glob("*.md"))
        )
        sk = NUCLEI / p / "structured-knowledge"
        verified_present = sk.is_dir() and any(
            f.is_file() and not f.name.startswith(".") and f.suffix in (".json",)
            for f in sk.rglob("*")
        )
        # composite score
        score = round(
            0.40 * breadth
            + 0.30 * (1.0 if normalized_present else 0.0)
            + 0.20 * (1.0 if verified_present else 0.0)
            + 0.10 * (1.0 if counts.get("provenance", 0) > 0 else 0.0),
            3,
        )
        scorecard["products"][p] = {
            "subdomain_breadth": breadth,
            "has_normalized_markdown": normalized_present,
            "has_verified_layer": verified_present,
            "subdomain_counts": counts,
            "completeness_score": score,
        }
    write_json(REPORTS / "04-semantic-completeness-scorecard.json", scorecard)

    # 5 — visual-orchestration-readiness.json
    visrep = {"generated_at": NOW, "products": {}}
    for p in PRODUCTS:
        pngs = list((NUCLEI / p / "source-of-truth/product-images").rglob("*.png"))
        prompts = list((NUCLEI / p / "visual-system/prompts").glob("*.md"))
        matrices = list((NUCLEI / p / "visual-system/generation-matrices").glob("*.md"))
        visrep["products"][p] = {
            "trusted_png_count": len(pngs),
            "prompt_pack_count": len(prompts),
            "matrix_count": len(matrices),
            "ready_for_comfy": bool(pngs and prompts),
        }
    write_json(REPORTS / "05-visual-orchestration-readiness.json", visrep)

    # 6 — comfyui-integration-readiness.json
    write_json(
        REPORTS / "06-comfyui-integration-readiness.json",
        {
            "generated_at": NOW,
            "policy": "ComfyUI-only for all future product imagery, manuals, troubleshooting visuals, installation diagrams, and video generation.",
            "prohibited_renderers": ["midjourney", "dall-e production pipelines", "any external visual system"],
            "required_inputs_per_product": {
                p: f"ext-images/{p}/knowledge-core/visual/visual-semantic-map.json"
                for p in PRODUCTS
            },
            "verified_workflow_reference": "tools/comfy/workflow_api.json.json (OpenAIGPTImage1 + LoadImage + SaveImage)",
        },
    )

    # 7 — repository-inconsistencies.json
    inconsistencies = []
    # Duplicate PDFs
    inconsistencies.append(
        {
            "kind": "duplicate-oem-pdf",
            "items": [
                "wp-content/themes/beslock-custom/User manuals/ext-images/e-flex/source-of-truth/manuals/e-Flex_1.pdf is byte-identical to e-Flex user manual.pdf",
                "wp-content/themes/beslock-custom/User manuals/ext-images/e-touch/source-of-truth/manuals/e-Touch_1.pdf is byte-identical to e-Touch user manual.pdf",
            ],
            "remediation": "Replace with metadata/audit/duplicate-oem-sources.json ledger pointing at the canonical user-manual PDF.",
        }
    )
    inconsistencies.append(
        {
            "kind": "structural-empty-buckets-in-legacy-knowledge",
            "items": ["configuration/", "faq/"],
            "scope": "every product",
            "remediation": "knowledge-core/ resolves this by folding configuration into operation/ and surfacing FAQ via operation/faq/ (e-orbit only, from verified structured-knowledge/).",
        }
    )
    inconsistencies.append(
        {
            "kind": "duplicate-entity-id-in-legacy-manifest",
            "items": ["e-orbit knowledge/entities/manifest.json contains cap-objetivo three times"],
            "remediation": "knowledge-core/ collapses to a single entity at promotion time (DUP_COLLAPSES rule).",
        }
    )
    inconsistencies.append(
        {
            "kind": "misclassified-troubleshooting",
            "items": ["e-orbit knowledge/troubleshooting/ts-paginas-prioritarias-para-fase-1.json is a sitemap routing list, not a symptom/resolution pair"],
            "remediation": "knowledge-core/ relocates to orchestration/publishing-priority-pages.json (RELOCATIONS rule).",
        }
    )
    inconsistencies.append(
        {
            "kind": "extractor-blind-to-non-md",
            "items": [
                "tools/knowledge_extraction.py only reads source-of-truth/manuals/*.md; XLS, supplemental PDFs, and specifications/*.md are invisible",
            ],
            "remediation": "knowledge-core build ingests XLS and supplemental OCR explicitly; future Phase 2 cutover should move this logic into the canonical extractor.",
        }
    )
    write_json(REPORTS / "07-repository-inconsistencies.json", inconsistencies)

    # 8 — manual-generation-readiness.json
    mgr = {"generated_at": NOW, "products": {}}
    for p, r in product_results.items():
        counts = r["manifest"]["subdomain_counts"]
        ready_blockers = []
        if counts.get("install", 0) == 0:
            ready_blockers.append("no install entities")
        if counts.get("operation", 0) == 0:
            ready_blockers.append("no operation entities")
        if counts.get("warnings", 0) == 0:
            ready_blockers.append("no warning entities")
        if counts.get("specifications", 0) == 0:
            ready_blockers.append("no specifications")
        if counts.get("workflows", 0) == 0:
            ready_blockers.append("no workflows")
        if not (NUCLEI / p / "source-of-truth/manuals").glob("*.md"):
            ready_blockers.append("no normalized markdown source")
        mgr["products"][p] = {
            "ready_for_manual_generation": not ready_blockers,
            "blockers": ready_blockers,
        }
    write_json(REPORTS / "08-manual-generation-readiness.json", mgr)

    # 0 — summary.md
    lines = [
        "# Phase 2 — Semantic operationalization summary",
        "",
        f"_Generated {NOW} by `tools/knowledge_core_build.py`._",
        "",
        "## Per-product knowledge-core inventory",
        "",
        "| Product | install | operation | workflows | trbl | warn | term | entities | cap | spec | semantic | prov | visual | orch |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p, r in product_results.items():
        c = r["manifest"]["subdomain_counts"]
        lines.append(
            f"| {p} | {c['install']} | {c['operation']} | {c['workflows']} | {c['troubleshooting']} | {c['warnings']} | {c['terminology']} | {c['entities']} | {c['capabilities']} | {c['specifications']} | {c['semantic']} | {c['provenance']} | {c['visual']} | {c['orchestration']} |"
        )
    lines += [
        "",
        "## Completeness score (see report 04)",
        "",
        "| Product | breadth | normalized? | verified-layer? | composite |",
        "|---|---|---|---|---|",
    ]
    sc = json.loads((REPORTS / "04-semantic-completeness-scorecard.json").read_text())
    for p, v in sc["products"].items():
        lines.append(
            f"| {p} | {v['subdomain_breadth']} | {v['has_normalized_markdown']} | {v['has_verified_layer']} | {v['completeness_score']} |"
        )
    lines += [
        "",
        "## Reports in this folder",
        "",
        "- 01-semantic-extraction-coverage.json",
        "- 02-unresolved-ocr-risks.json",
        "- 03-missing-oem-knowledge.json",
        "- 04-semantic-completeness-scorecard.json",
        "- 05-visual-orchestration-readiness.json",
        "- 06-comfyui-integration-readiness.json",
        "- 07-repository-inconsistencies.json",
        "- 08-manual-generation-readiness.json",
        "",
        "## Critical rules honoured",
        "",
        "- Did not generate final manuals.",
        "- Did not generate PDFs.",
        "- Did not generate marketing assets.",
        "- Did not generate website pages.",
        "- Did not invent hardware, sensors, app functionality, lock states, or capabilities.",
        "- All visual orchestration metadata enforces ComfyUI-only downstream.",
        "- Every emitted entity carries source_refs + extraction_lineage.",
    ]
    (REPORTS / "00-summary.md").write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def reset_core(core: Path) -> None:
    """Idempotent: wipe and recreate the knowledge-core/ tree for one product."""
    if core.exists():
        shutil.rmtree(core)
    for sub in SUBDOMAINS:
        (core / sub).mkdir(parents=True, exist_ok=True)


def main() -> int:
    cores: dict[str, Path] = {}
    results: dict[str, dict] = {}

    for p in PRODUCTS:
        core = NUCLEI / p / "knowledge-core"
        cores[p] = core
        reset_core(core)

    # Phase A — promote legacy knowledge/ for every product.
    for p in PRODUCTS:
        n, _ = promote_legacy(p, cores[p])
        results.setdefault(p, {})["legacy_promotions"] = n
        # Also copy across cross-cutting helpers (entities/manifest, relationships,
        # semantic-index, normalized) verbatim — they are derived aggregates and
        # we preserve them for continuity, not as canonical entities.
        legacy_root = NUCLEI / p / "knowledge"
        helper_targets = [
            (legacy_root / "entities" / "manifest.json", cores[p] / "entities" / "legacy-manifest.json"),
            (legacy_root / "normalized" / "normalized-knowledge.json", cores[p] / "semantic" / "legacy-normalized.json"),
        ]
        for src, dst in helper_targets:
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(src.read_text())
        rel_dir = legacy_root / "relationships"
        if rel_dir.is_dir():
            for fp in rel_dir.glob("*.json"):
                tgt = cores[p] / "semantic" / "relationships" / f"legacy-{fp.name}"
                tgt.parent.mkdir(parents=True, exist_ok=True)
                tgt.write_text(fp.read_text())
        idx_dir = legacy_root / "semantic-index"
        if idx_dir.is_dir():
            for fp in idx_dir.glob("*.json"):
                tgt = cores[p] / "semantic" / "legacy-indexes" / fp.name
                tgt.parent.mkdir(parents=True, exist_ok=True)
                tgt.write_text(fp.read_text())

    # Phase B — promote e-orbit verified structured-knowledge/.
    n_verified = promote_structured_orbit(cores["e-orbit"])
    results["e-orbit"]["verified_promotions"] = n_verified

    # Phase C — XLS ingest for e-orbit.
    results["e-orbit"]["xls_ingested"] = ingest_orbit_xls(cores["e-orbit"])

    # Phase D — supplemental OCR promotion.
    sup_summary = promote_supplementals(cores)
    for p in PRODUCTS:
        results.setdefault(p, {})["supplementals"] = sup_summary.get(p, [])

    # Phase E — OCR-derived drafts (every product gets an index pointer; e-nova
    # is the only one fully dependent on OCR but the index is informative for all).
    for p in PRODUCTS:
        results[p]["ocr_draft_index"] = emit_ocr_drafts(p, cores[p])

    # Phase F — entity catalog + capability map.
    for p in PRODUCTS:
        results[p]["entities"] = build_entity_catalog(p, cores[p])
        results[p]["capabilities"] = build_capability_map(p, cores[p])

    # Phase G — visual + orchestration.
    for p in PRODUCTS:
        results[p]["visual"] = build_visual_semantic_map(p, cores[p])
        build_orchestration(p, cores[p])

    # Phase H — provenance manifests + per-product manifest + readme.
    for p in PRODUCTS:
        prov = build_provenance(p, cores[p])
        results[p]["provenance_sources"] = len(prov["sources"])
        manifest = write_product_manifest(p, cores[p])
        results[p]["manifest"] = manifest
        write_readme(p, cores[p])

    # Cross-product reports.
    build_reports(results)

    print("knowledge-core build complete.")
    for p in PRODUCTS:
        print(f"  {p}: {results[p]['manifest']['subdomain_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
