# Phase 2B — Source Coverage & Semantic Extraction Validation

_Generated 2026-05-13 (audit run, no extraction pipeline re-execution)._

This audit validates that **all OEM source materials present in the repository
were actually ingested and operationalised** by the Phase 2 semantic extractor
(`tools/knowledge_extraction.py`). It measures knowledge coverage, **not** file
counts.

The audit is **read-only**. It does not modify any entity, manifest, or
provenance file under `ext-images/<slug>/knowledge/`, `structured-knowledge/`,
or `source-of-truth/`. It does not re-run OCR.

---

## TL;DR — One-line verdict per product

| Product  | OEM artifacts (unique) | Normalized `.md` feeds | Semantic entities | Coverage verdict |
|----------|------------------------|-------------------------|-------------------|------------------|
| e-flex   | 1 PDF (8p)             | install + app           | 63                | **Partial — user manual not normalized; supplemental PDF is byte-identical to user manual (duplicate provenance).** |
| e-nova   | 1 PDF (10p)            | **none**                | 14 (OCR-only)     | **Critical gap — fully OCR-only. Zero normalized feeds. No supplemental, app, or installation source.** |
| e-orbit  | 1 PDF (2p) + 1 PDF (17p) + 1 XLS | user + app + impl-pack + supplemental | 109 | **Best-covered, but `e-Orbit_1.xls` spec sheet is completely unprocessed and one entity is misclassified.** |
| e-prime  | 3 PDFs (8p+6p+7p)      | install + app           | 65                | **Partial — user manual not normalized; supplemental PDFs (`_1`, `_2`) never reached the extractor.** |
| e-shield | 3 PDFs (20p+2p+1p)     | install + app           | 62                | **Partial — user manual not normalized; supplemental PDFs (`_1`, `_2`) never reached the extractor.** |
| e-touch  | 1 PDF (2p)             | install + app           | 98                | **Partial — user manual not normalized; supplemental PDF is byte-identical to user manual (duplicate provenance).** |

Repository-wide structural findings:

1. **Knowledge extraction reads only `.md` files.** Every `*.pdf` and `.xls`
   artifact under `source-of-truth/manuals/` and `source-of-truth/specifications/`
   is invisible to `tools/knowledge_extraction.py`. PDFs only contribute through
   either (a) the OCR fallback in `generated_manuals/<slug>/manual.json` or
   (b) human-authored normalized markdown.
2. **OCR is gated to `<Display> user manual.pdf`.** Every supplemental
   `*_N.pdf` (and `e-Orbit_1.xls`) is **never** OCR'd, never page-coverage-tracked,
   and never reflected in `extracted-text/` evidence.
3. **Two supplementals are byte-identical duplicates** of the corresponding user
   manual: `e-Flex_1.pdf` and `e-Touch_1.pdf`. They inflate the apparent OEM
   inventory without contributing knowledge.
4. **`configuration/` and `faq/` buckets are empty for every product.** No
   semantic entity has ever been emitted into either nucleus. This is a
   structural gap, not a product-level gap.
5. **`troubleshooting/` is virtually empty** — only e-orbit has a single entity,
   and it is **misclassified** (the entry "Páginas prioritarias para Fase 1"
   is a routing/sitemap list, not a symptom/resolution pair).
6. **Silent duplication in e-orbit manifest**: entity id `cap-objetivo` appears
   **3 times** in `e-orbit/knowledge/entities/manifest.json`.
7. **`extraction-report.json` `bucket_counts` does not name a `procedures`
   bucket.** Procedure entities are folded into `operation/`,
   `installation/`, or `troubleshooting/` based on classification. Anyone
   reading the per-product report will under-count procedures unless they
   inspect the `semantic-index/by-type-procedure.json` index.

The detailed evidence behind every verdict above is in the JSON reports
listed below.

---

## Reports in this folder

| File | Purpose |
|------|---------|
| `01-source-coverage-matrix.json`            | Authoritative per-source inventory: path, size, MD5, page count, ingestion / OCR / semantic-extraction status. |
| `02-per-product-ingestion-report.md`        | Narrative ingestion report per product nucleus. |
| `03-ocr-only-diagnostics.json`              | Root-cause analysis for every OCR-only or partially processed source. |
| `04-semantic-extraction-completeness.json`  | Per-product matrix of which knowledge dimensions (procedures / workflows / warnings / terminology / troubleshooting / capabilities / configuration / faq) actually emitted entities. |
| `05-unresolved-source-report.json`          | OEM artifacts present in `source-of-truth/` that produced **zero** semantic entities. |
| `06-ignored-document-report.json`           | OEM artifacts the extractor ignores by design (PDFs, XLS, duplicates). |
| `07-low-confidence-extraction.json`         | OCR runs with `avg_confidence < 90`, ambiguities flagged in `extraction-report.json`, and structurally suspect entities. |
| `08-operational-knowledge-coverage.json`    | Per-product completeness scoring across installation / operation / configuration / troubleshooting / workflows / terminology. |
| `09-extraction-quality-scorecard.json`      | Composite quality score per product (provenance, classification, duplication, lineage). |

---

## Critical rules honoured

- ❌ Did not re-run the extraction pipeline.
- ❌ Did not fabricate or back-fill semantic entities.
- ❌ Did not overwrite any provenance, manifest, or `extraction-report.json`.
- ❌ Did not delete or rename any OEM source.
- ✅ Did read PDF page counts (via macOS `mdls`) and MD5 hashes for
  duplication detection — both non-destructive.
- ✅ Did surface every silent failure / misclassification observed.
- ✅ Did refuse to score "knowledge completeness" by file count; scoring is
  driven by entity presence per knowledge dimension and per OEM page.

---

## Recommended Phase 2C follow-ups (not executed here)

These are **proposals**, surfaced for the next session. Do not act on them
without explicit approval.

1. **e-Nova normalisation**: author `e-Nova installation manual.md`,
   `e-Nova app manual.md`, and `e-Nova user manual.md` from
   `generated_manuals/e-nova/manual_raw.txt` + the OEM PDF, then re-run
   `tools/knowledge_extraction.py` for the e-nova nucleus only.
2. **e-Orbit XLS ingestion**: convert `e-Orbit_1.xls` into a normalized
   spec markdown (`e-Orbit hardware specifications.md`) under
   `source-of-truth/specifications/` and teach the extractor to read
   `specifications/*.md` (currently it only walks `manuals/*.md`).
3. **Duplicate provenance**: replace `e-Flex_1.pdf` and `e-Touch_1.pdf` with
   a `metadata/audit/duplicate-oem-sources.json` ledger entry pointing at the
   canonical user manual PDFs.
4. **Supplemental PDF ingestion path**: define an explicit extractor branch
   for `_N.pdf` supplementals that have no normalized markdown counterpart
   (currently e-Shield_1, e-Shied_2, e-Prime_1, e-Prime_2, e-Orbit_2). The
   short-form layout/installation guides in those PDFs are not represented
   anywhere in `knowledge/`.
5. **Misclassified troubleshooting**: re-bucket
   `e-orbit/knowledge/troubleshooting/ts-paginas-prioritarias-para-fase-1.json`
   into `relationships/` or `metadata/` — it is a sitemap, not a symptom.
6. **e-orbit manifest dedupe**: collapse the three `cap-objetivo` rows in
   `e-orbit/knowledge/entities/manifest.json` to a single entry.
7. **Extraction-report schema fix**: add an explicit `procedures` count to
   `extraction-report.json` so per-product summaries stop folding procedures
   under bucket folders.
