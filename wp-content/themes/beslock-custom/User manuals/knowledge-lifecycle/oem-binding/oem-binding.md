# OEM Evidence Binding

Content-addressed, append-only bindings to OEM source artifacts.

## Binding kinds

- `pdf` — fields: sha256, path_or_url, page, region_bbox, extract_lineage
- `ocr-fragment` — fields: sha256, source_pdf_sha256, page, region_bbox, ocr_tool, ocr_confidence
- `screenshot` — fields: sha256, captured_from, captured_at, annotator, region_bbox
- `extracted-procedure` — fields: sha256, source_pdf_sha256, page_range, extract_lineage
- `troubleshooting-evidence` — fields: sha256, source_kind, source_ref, observed_failure_mode
- `warning-evidence` — fields: sha256, source_kind, source_ref, irreversibility_flag

## Binding rules

- every binding record is content-addressed (sha256 of the source artifact)
- every binding record is append-only; updates create a new binding with prior_binding_id
- no binding may reference a non-existent or non-pinned source
- OEM-verified state requires at least one binding of kind pdf | ocr-fragment | extracted-procedure
- warning-evidence + troubleshooting-evidence bindings are required for those domains' OEM promotion
- runtime exposes binding ids via the provenance manifest; the runtime never edits bindings

## Traceable trust pipeline

- node -> oem_binding[] -> source artifact (sha256-pinned) -> declared origin
- any break in the chain demotes the node to candidate and emits escalation
- traceability is queryable; queries are read-only and bounded by knowledge-core scope
