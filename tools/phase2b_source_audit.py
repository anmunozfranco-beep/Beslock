#!/usr/bin/env python3
"""Phase 2B audit report generator (read-only).

Builds the JSON / Markdown reports under
`wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/phase2b-source-coverage/`
without modifying any extraction artifact, manifest, or OEM source.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUCLEI = REPO / "wp-content/themes/beslock-custom/User manuals/ext-images"
OUT = REPO / "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/phase2b-source-coverage"
GEN_OCR = REPO / "generated_manuals"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_pages(path: Path) -> int | None:
    try:
        out = subprocess.check_output(
            ["mdls", "-name", "kMDItemNumberOfPages", str(path)], text=True
        ).strip()
        # "kMDItemNumberOfPages = 8"
        val = out.split("=", 1)[-1].strip()
        return None if val == "(null)" else int(val)
    except Exception:
        return None


def load_manifest(product: str) -> list[dict]:
    fp = NUCLEI / product / "knowledge" / "entities" / "manifest.json"
    if not fp.exists():
        return []
    data = json.loads(fp.read_text())
    return data if isinstance(data, list) else data.get("entities", [])


KNOWLEDGE_BUCKETS = (
    "capabilities",
    "operation",
    "installation",
    "configuration",
    "troubleshooting",
    "warning",
    "workflows",
    "terminology",
    "faq",
    "extracted-text",
)


def load_full_entities(product: str) -> list[dict]:
    """Load every per-entity JSON payload from the bucket folders.

    The `entities/manifest.json` index only carries a summary stub; the full
    payload (steps, resolutions, storage_bucket, content fields) lives in the
    per-bucket files. We need the full payload for quality scoring.
    """
    base = NUCLEI / product / "knowledge"
    out: list[dict] = []
    for bucket in KNOWLEDGE_BUCKETS:
        d = base / bucket
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.json")):
            try:
                payload = json.loads(fp.read_text())
            except Exception:
                continue
            payload.setdefault("storage_bucket", bucket)
            out.append(payload)
    return out


def load_extraction_report(product: str) -> dict:
    fp = NUCLEI / product / "knowledge" / "extraction-report.json"
    return json.loads(fp.read_text()) if fp.exists() else {}


def load_ocr_manual(product: str) -> dict:
    fp = GEN_OCR / product / "manual.json"
    return json.loads(fp.read_text()) if fp.exists() else {}


# ---- Inventory walk ---------------------------------------------------------
def walk_sources(product: str) -> list[dict]:
    base = NUCLEI / product / "source-of-truth"
    rows: list[dict] = []
    for sub in (
        "manuals",
        "specifications",
        "visual-evidence",
        "installation",
        "dimensions",
        "hardware",
        "certifications",
        "ui",
        "screenshots",
    ):
        d = base / sub
        if not d.is_dir():
            continue
        for root, _, files in os.walk(d):
            for fname in sorted(files):
                if fname.startswith("."):
                    continue
                full = Path(root) / fname
                rel = full.relative_to(REPO).as_posix()
                ext = full.suffix.lower()
                kind = {
                    ".md": "normalized-markdown",
                    ".pdf": "oem-pdf",
                    ".xls": "oem-spreadsheet",
                    ".xlsx": "oem-spreadsheet",
                    ".png": "page-render-or-image",
                    ".jpg": "page-render-or-image",
                    ".jpeg": "page-render-or-image",
                    ".webp": "page-render-or-image",
                }.get(ext, "other")
                row = {
                    "product": product,
                    "path": rel,
                    "filename": fname,
                    "category": sub,
                    "kind": kind,
                    "size_bytes": full.stat().st_size,
                }
                if ext == ".pdf":
                    row["pdf_pages"] = pdf_pages(full)
                    row["md5"] = md5_of(full)
                rows.append(row)
    return rows


# ---- Status scoring ---------------------------------------------------------
def classify_source(row: dict, ext_report: dict, ocr: dict, dup_groups: dict) -> dict:
    """Return ingestion / OCR / semantic-extraction status for one source."""
    path = row["path"]
    fname = row["filename"]
    ext = Path(fname).suffix.lower()
    kind = row["kind"]
    sources_used = set(ext_report.get("sources_used", []))

    # Ingestion: did the semantic extractor read this file?
    ingestion = "ignored-by-design" if kind != "normalized-markdown" else "missing"
    if path in sources_used:
        ingestion = "ingested"

    # OCR: only the user-manual.pdf flows through generated_manuals/
    if ext == ".pdf":
        is_user_manual = fname.lower().endswith("user manual.pdf")
        if is_user_manual:
            ocr_status = (
                "ocr-completed" if ocr.get("pages") else "ocr-missing"
            )
        else:
            ocr_status = "ocr-not-attempted"
    elif kind == "page-render-or-image":
        ocr_status = "render-only"
    elif ext in (".xls", ".xlsx"):
        ocr_status = "not-applicable-binary-spreadsheet"
    else:
        ocr_status = "not-applicable"

    # Semantic extraction: did entities provably derive from this file?
    semantic = "no-entities-emitted"
    if kind == "normalized-markdown" and path in sources_used:
        semantic = "entities-emitted"
    elif (
        ext == ".pdf"
        and fname.lower().endswith("user manual.pdf")
        and ocr.get("pages")
    ):
        # OCR fallback contributes extracted-text entities only
        semantic = "extracted-text-only"

    # Duplicate flag
    dup_of = None
    if "md5" in row and dup_groups.get(row["md5"], 1) > 1:
        dup_of = row["md5"]

    out = {
        "ingestion_status": ingestion,
        "ocr_status": ocr_status,
        "semantic_extraction_status": semantic,
    }
    if dup_of:
        out["duplicate_md5"] = dup_of
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # Pass 1: gather raw inventory + extraction reports
    all_sources: list[dict] = []
    ext_reports: dict[str, dict] = {}
    ocr_reports: dict[str, dict] = {}
    manifests: dict[str, list[dict]] = {}
    full_entities: dict[str, list[dict]] = {}
    for p in PRODUCTS:
        ext_reports[p] = load_extraction_report(p)
        ocr_reports[p] = load_ocr_manual(p)
        manifests[p] = load_manifest(p)
        full_entities[p] = load_full_entities(p)
        all_sources.extend(walk_sources(p))

    # Duplicate-detection across all PDFs
    md5_counts: dict[str, int] = {}
    for r in all_sources:
        if "md5" in r:
            md5_counts[r["md5"]] = md5_counts.get(r["md5"], 0) + 1

    # Pass 2: classify every source
    for r in all_sources:
        r.update(
            classify_source(r, ext_reports[r["product"]], ocr_reports[r["product"]], md5_counts)
        )

    # ---- 01 source-coverage-matrix.json -----------------------------------
    coverage_matrix = {
        "generated_at": NOW,
        "schema_version": "phase2b.1",
        "products": PRODUCTS,
        "sources": all_sources,
    }
    (OUT / "01-source-coverage-matrix.json").write_text(
        json.dumps(coverage_matrix, indent=2, ensure_ascii=False)
    )

    # ---- 04 semantic extraction completeness ------------------------------
    # Knowledge dimensions evaluated per product
    DIMENSIONS = [
        ("entities", lambda m: len(m)),
        ("procedures", lambda m: sum(1 for e in m if e.get("type") == "procedure")),
        ("workflows", lambda m: sum(1 for e in m if e.get("type") == "workflow")),
        ("warnings", lambda m: sum(1 for e in m if e.get("type") == "warning")),
        ("terminology", lambda m: sum(1 for e in m if e.get("type") == "glossary-term")),
        ("troubleshooting", lambda m: sum(1 for e in m if e.get("type") == "troubleshooting")),
        ("capabilities", lambda m: sum(1 for e in m if e.get("type") == "capability")),
        ("installation_flows", lambda m: sum(1 for e in m if e.get("type") == "installation-flow")),
        ("configuration", lambda m: sum(1 for e in m if e.get("type") == "configuration")),
        ("faq", lambda m: sum(1 for e in m if e.get("type") == "faq")),
        ("extracted_text", lambda m: sum(1 for e in m if e.get("type") == "extracted-text")),
    ]

    completeness = {"generated_at": NOW, "products": {}}
    for p in PRODUCTS:
        ents = full_entities[p]
        per = {name: fn(ents) for name, fn in DIMENSIONS}
        per["sources_ingested"] = len(ext_reports[p].get("sources_used", []))
        per["sources_missing_declared_by_extractor"] = ext_reports[p].get("sources_missing", [])
        per["sections_seen"] = ext_reports[p].get("sections_seen", 0)
        # Bucket folder counts (filesystem ground truth)
        per["bucket_file_counts"] = {
            b: len(list((NUCLEI / p / "knowledge" / b).glob("*.json")))
            for b in KNOWLEDGE_BUCKETS
            if (NUCLEI / p / "knowledge" / b).is_dir()
        }
        completeness["products"][p] = per
    (OUT / "04-semantic-extraction-completeness.json").write_text(
        json.dumps(completeness, indent=2, ensure_ascii=False)
    )

    # ---- 03 OCR-only diagnostics -----------------------------------------
    ocr_diag = {"generated_at": NOW, "products": {}}
    OCR_CAUSES = {
        "e-nova": {
            "diagnosis": "OCR-only product. No normalized markdown manuals exist under source-of-truth/manuals/. The extractor therefore emitted only 14 'extracted-text' fragments echoed from generated_manuals/e-nova/manual.json (pytesseract, avg confidence 84.3 over 10 pages). No procedures, workflows, warnings, terminology, or installation flows were emitted.",
            "root_causes": [
                "Missing normalized e-Nova installation manual.md",
                "Missing normalized e-Nova app manual.md",
                "Missing normalized e-Nova user manual.md",
                "No supplemental OEM PDF (no e-Nova_1.pdf) to seed authoring",
            ],
            "fix_path": "Author the three normalized .md files from generated_manuals/e-nova/manual_raw.txt + OEM PDF page renders, then re-run tools/knowledge_extraction.py for e-nova only.",
        },
    }
    for p in PRODUCTS:
        ocr = ocr_reports[p]
        diag = {
            "ocr_method": ocr.get("ocr_method"),
            "ocr_pages": ocr.get("pages"),
            "ocr_avg_confidence": ocr.get("avg_confidence"),
            "ocr_sections_detected": len(ocr.get("sections", [])),
            "extracted_text_entities_emitted": sum(
                1 for e in manifests[p] if e.get("type") == "extracted-text"
            ),
            "normalized_markdown_present": bool(
                ext_reports[p].get("sources_used")
            ),
        }
        if p in OCR_CAUSES:
            diag.update(OCR_CAUSES[p])
        ocr_diag["products"][p] = diag
    (OUT / "03-ocr-only-diagnostics.json").write_text(
        json.dumps(ocr_diag, indent=2, ensure_ascii=False)
    )

    # ---- 05 unresolved sources (zero entities) ---------------------------
    unresolved = []
    for r in all_sources:
        if r["semantic_extraction_status"] == "no-entities-emitted" and r["kind"] in (
            "oem-pdf",
            "oem-spreadsheet",
            "normalized-markdown",
        ):
            unresolved.append(
                {
                    "product": r["product"],
                    "path": r["path"],
                    "filename": r["filename"],
                    "kind": r["kind"],
                    "ingestion_status": r["ingestion_status"],
                    "ocr_status": r["ocr_status"],
                    "reason": (
                        "Spreadsheet not supported by extractor (manuals/*.md only)."
                        if r["kind"] == "oem-spreadsheet"
                        else "Supplemental PDF without normalized .md counterpart and not flagged for OCR."
                        if r["kind"] == "oem-pdf" and not r["filename"].lower().endswith("user manual.pdf")
                        else "User manual PDF — content reaches knowledge only via OCR fallback (extracted-text bucket)."
                        if r["kind"] == "oem-pdf"
                        else "Markdown present but extractor did not record it in sources_used."
                    ),
                }
            )
    (OUT / "05-unresolved-source-report.json").write_text(
        json.dumps({"generated_at": NOW, "items": unresolved}, indent=2, ensure_ascii=False)
    )

    # ---- 06 ignored documents (by-design) --------------------------------
    ignored = []
    for r in all_sources:
        if r["ingestion_status"] == "ignored-by-design":
            ignored.append(
                {
                    "product": r["product"],
                    "path": r["path"],
                    "filename": r["filename"],
                    "kind": r["kind"],
                    "size_bytes": r["size_bytes"],
                    "duplicate_md5": r.get("duplicate_md5"),
                }
            )
    (OUT / "06-ignored-document-report.json").write_text(
        json.dumps({"generated_at": NOW, "items": ignored}, indent=2, ensure_ascii=False)
    )

    # ---- 07 low-confidence + ambiguity -----------------------------------
    low_conf = {"generated_at": NOW, "products": {}}
    for p in PRODUCTS:
        ocr = ocr_reports[p]
        ext = ext_reports[p]
        ents = full_entities[p]
        flags = []
        avg = ocr.get("avg_confidence")
        if avg is not None and avg < 90:
            flags.append(
                {
                    "kind": "low-ocr-confidence",
                    "avg_confidence": avg,
                    "method": ocr.get("ocr_method"),
                }
            )
        if ext.get("ambiguities"):
            for a in ext["ambiguities"]:
                flags.append({"kind": "extractor-ambiguity", "detail": a})
        # Suspicious entities — duplicate ids in manifest index
        ids: dict[str, int] = {}
        for e in manifests[p]:
            ids[e.get("id")] = ids.get(e.get("id"), 0) + 1
        dups = [{"id": k, "occurrences": v} for k, v in ids.items() if v > 1]
        if dups:
            flags.append({"kind": "duplicate-entity-ids-in-manifest", "items": dups})
        # Procedures whose payload has no `steps` array
        empty_proc = [
            e["id"]
            for e in ents
            if e.get("type") == "procedure" and not e.get("steps")
        ]
        if empty_proc:
            flags.append({"kind": "procedure-with-no-steps", "ids": empty_proc})
        # Troubleshooting entries that look like sitemap/route lists
        sitemap_ts = []
        for e in ents:
            if e.get("type") != "troubleshooting":
                continue
            blob = json.dumps(e.get("resolutions", []) + e.get("symptoms", []), ensure_ascii=False)
            if "/productos/" in blob or blob.count("`/") >= 3:
                sitemap_ts.append(e["id"])
        if sitemap_ts:
            flags.append({"kind": "troubleshooting-misclassified-as-sitemap", "ids": sitemap_ts})
        low_conf["products"][p] = flags
    (OUT / "07-low-confidence-extraction.json").write_text(
        json.dumps(low_conf, indent=2, ensure_ascii=False)
    )

    # ---- 08 operational knowledge coverage --------------------------------
    OP_DIMS = [
        "installation_flows",
        "operation_procedures",
        "configuration",
        "troubleshooting",
        "workflows",
        "terminology",
        "warnings",
        "capabilities",
        "faq",
    ]
    op_cov = {"generated_at": NOW, "products": {}}
    for p in PRODUCTS:
        ents = full_entities[p]
        per = {
            "installation_flows": sum(1 for e in ents if e.get("type") == "installation-flow"),
            "operation_procedures": sum(
                1
                for e in ents
                if e.get("type") == "procedure" and e.get("storage_bucket") == "operation"
            ),
            "configuration": sum(1 for e in ents if e.get("type") == "configuration")
            + sum(1 for e in ents if e.get("storage_bucket") == "configuration"),
            "troubleshooting": sum(1 for e in ents if e.get("type") == "troubleshooting"),
            "workflows": sum(1 for e in ents if e.get("type") == "workflow"),
            "terminology": sum(1 for e in ents if e.get("type") == "glossary-term"),
            "warnings": sum(1 for e in ents if e.get("type") == "warning"),
            "capabilities": sum(1 for e in ents if e.get("type") == "capability"),
            "faq": sum(1 for e in ents if e.get("type") == "faq")
            + sum(1 for e in ents if e.get("storage_bucket") == "faq"),
        }
        # de-dup configuration / faq counts (avoid double-counting a single entity that has both type and bucket)
        per["configuration"] = sum(
            1 for e in ents if e.get("storage_bucket") == "configuration"
        )
        per["faq"] = sum(1 for e in ents if e.get("storage_bucket") == "faq")
        present = sum(1 for v in per.values() if v > 0)
        per["dimensions_with_coverage"] = present
        per["dimensions_total"] = len(OP_DIMS)
        per["coverage_ratio"] = round(present / len(OP_DIMS), 2)
        op_cov["products"][p] = per
    (OUT / "08-operational-knowledge-coverage.json").write_text(
        json.dumps(op_cov, indent=2, ensure_ascii=False)
    )

    # ---- 09 quality scorecard --------------------------------------------
    score = {"generated_at": NOW, "products": {}, "scoring_notes": [
        "provenance_complete: 1 - (entities_missing_source_refs / total_entities)",
        "non_duplicated: 1 - (duplicate_id_entities / total_entities)",
        "classification_meaningful: 1 - (sitemap-like-troubleshooting / troubleshooting_total)",
        "lineage_to_oem: 1 if normalized .md sources cite OEM PDF or OCR fallback; 0.5 if only OCR; 0 if none",
        "procedure_step_completeness: 1 - (procedures_with_no_steps / procedures_total)",
        "knowledge_breadth: ratio of operational dimensions with at least one entity (see report 08)",
        "rag_ready: 0.25*provenance + 0.10*non_duplicated + 0.15*classification + 0.15*lineage + 0.15*procedure_step_completeness + 0.20*knowledge_breadth",
    ]}
    SITEMAP_PATTERN_HINT = "/productos/"
    for p in PRODUCTS:
        m = manifests[p]
        ents = full_entities[p]
        total = len(m) or 1
        miss_prov = sum(1 for e in m if not e.get("source_refs"))
        ids: dict[str, int] = {}
        for e in m:
            ids[e.get("id")] = ids.get(e.get("id"), 0) + 1
        dup_entities = sum(v for v in ids.values() if v > 1) - sum(1 for v in ids.values() if v > 1)
        # Misclassification heuristic: troubleshooting entries that look like sitemaps
        misc = 0
        ts_total = 0
        for e in ents:
            if e.get("type") != "troubleshooting":
                continue
            ts_total += 1
            blob = json.dumps(e.get("resolutions", []) + e.get("symptoms", []), ensure_ascii=False)
            if SITEMAP_PATTERN_HINT in blob:
                misc += 1
        # Procedures with no steps in their full payload
        proc_total = sum(1 for e in ents if e.get("type") == "procedure")
        proc_no_steps = sum(
            1 for e in ents if e.get("type") == "procedure" and not e.get("steps")
        )
        provenance_complete = round(1 - miss_prov / total, 3)
        non_duplicated = round(1 - dup_entities / total, 3)
        classification_meaningful = (
            round(1 - misc / ts_total, 3) if ts_total else 1.0
        )
        if ext_reports[p].get("sources_used"):
            lineage = 1.0
        elif ocr_reports[p].get("pages"):
            lineage = 0.5
        else:
            lineage = 0.0
        proc_step_completeness = (
            round(1 - proc_no_steps / proc_total, 3) if proc_total else 1.0
        )
        knowledge_breadth = op_cov["products"][p]["coverage_ratio"]
        rag_ready = round(
            0.25 * provenance_complete
            + 0.10 * non_duplicated
            + 0.15 * classification_meaningful
            + 0.15 * lineage
            + 0.15 * proc_step_completeness
            + 0.20 * knowledge_breadth,
            3,
        )
        score["products"][p] = {
            "provenance_complete": provenance_complete,
            "non_duplicated": non_duplicated,
            "classification_meaningful": classification_meaningful,
            "lineage_to_oem": lineage,
            "procedure_step_completeness": proc_step_completeness,
            "knowledge_breadth": knowledge_breadth,
            "procedures_total": proc_total,
            "procedures_with_no_steps": proc_no_steps,
            "rag_ready": rag_ready,
            "duplicate_id_count": sum(1 for v in ids.values() if v > 1),
            "entities_missing_source_refs": miss_prov,
            "misclassified_troubleshooting": misc,
        }
    (OUT / "09-extraction-quality-scorecard.json").write_text(
        json.dumps(score, indent=2, ensure_ascii=False)
    )

    # ---- 02 per-product narrative report ---------------------------------
    lines = ["# Phase 2B — Per-product ingestion report", "",
             f"_Generated {NOW}_", ""]
    for p in PRODUCTS:
        sources = [r for r in all_sources if r["product"] == p]
        ext = ext_reports[p]
        ocr = ocr_reports[p]
        m = manifests[p]
        lines.append(f"## {p}")
        lines.append("")
        lines.append("**Sources on disk**")
        lines.append("")
        lines.append("| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in sources:
            if r["kind"] == "page-render-or-image":
                continue  # collapse renders for readability
            ps = (
                f"{r.get('pdf_pages','?')} pages"
                if r["kind"] == "oem-pdf"
                else f"{r['size_bytes']} B"
            )
            dup = " *(dup)*" if r.get("duplicate_md5") else ""
            lines.append(
                f"| `{r['filename']}`{dup} | {r['category']} | {r['kind']} | {ps} | {r['ingestion_status']} | {r['ocr_status']} | {r['semantic_extraction_status']} |"
            )
        # render summary count
        renders = [r for r in sources if r["kind"] == "page-render-or-image"]
        if renders:
            by_dir: dict[str, int] = {}
            for r in renders:
                d = Path(r["path"]).parent.name
                by_dir[d] = by_dir.get(d, 0) + 1
            rdesc = ", ".join(f"{k}: {v}" for k, v in sorted(by_dir.items()))
            lines.append("")
            lines.append(f"_PDF renders on disk_: {rdesc}")
        lines.append("")
        lines.append("**Extractor view**")
        lines.append("")
        lines.append(f"- Sources used: {len(ext.get('sources_used', []))}")
        lines.append(f"- Sources reported missing: {ext.get('sources_missing', [])}")
        lines.append(f"- Sections seen: {ext.get('sections_seen', 0)}")
        lines.append(f"- Entities emitted: {ext.get('entities_emitted', 0)}")
        lines.append(f"- Bucket counts: {ext.get('bucket_counts', {})}")
        lines.append(f"- Gaps: {ext.get('gaps', [])}")
        lines.append(f"- Ambiguities: {ext.get('ambiguity_total', 0)}")
        lines.append("")
        lines.append("**OCR fallback view**")
        lines.append("")
        lines.append(f"- Method: `{ocr.get('ocr_method')}`")
        lines.append(f"- Pages: {ocr.get('pages')}")
        lines.append(f"- Avg confidence: {ocr.get('avg_confidence')}")
        lines.append(f"- Sections detected: {len(ocr.get('sections', []))}")
        lines.append(f"- Steps detected: {len(ocr.get('steps', []))}")
        lines.append(f"- App instructions detected: {len(ocr.get('app_instructions', []))}")
        lines.append(f"- Warnings detected: {len(ocr.get('warnings', []))}")
        lines.append("")
        lines.append("**Knowledge nucleus view**")
        lines.append("")
        per = completeness["products"][p]
        for k in (
            "entities",
            "procedures",
            "workflows",
            "warnings",
            "terminology",
            "troubleshooting",
            "capabilities",
            "installation_flows",
            "configuration",
            "faq",
            "extracted_text",
        ):
            lines.append(f"- {k}: {per[k]}")
        lines.append("")
        lines.append("**Quality scorecard**")
        lines.append("")
        for k, v in score["products"][p].items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    (OUT / "02-per-product-ingestion-report.md").write_text("\n".join(lines))

    print(f"Wrote 9 reports to {OUT}")


if __name__ == "__main__":
    main()
