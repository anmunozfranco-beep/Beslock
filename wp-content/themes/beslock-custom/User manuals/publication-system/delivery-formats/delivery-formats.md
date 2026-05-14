# Delivery Format Governance

Six formats (markdown, web, structured-runtime, pdf-ready, support-article, visual-prompt). Structured-runtime is the source-of-truth format; all others derive from it.

## Formats

- `markdown` — purpose: primary canonical publication output; lossless: True; constraints: no executable scripts; no inline HTML beyond declared subset
- `web` — purpose: browser-consumable publication; lossless: False; constraints: no client-side mutation of canonical content; must preserve provenance citations
- `structured-runtime` — purpose: runtime-consumable JSON for assembled responses; lossless: True; constraints: schema = publication-output/1.0 (declared in this layer); MUST embed provenance + confidence band
- `pdf-ready` — purpose: print-fidelity export; lossless: False; constraints: no interactive elements; explicit page-break markers; warnings retained verbatim
- `support-article` — purpose: support-agent knowledge article; lossless: True; constraints: scenario/diagnosis/resolution structure required; internal notes section required
- `visual-prompt` — purpose: MODELING ONLY — declarative input to a future visual pipeline; lossless: True; constraints: text declaration only — generates no image; subordinate to VISUAL governance + dual-review env (layer 25)

## Format rules

- no format may add semantic content beyond what assembly produced
- lossy formats MUST disclose what is lost (e.g. interactivity, color fidelity)
- structured-runtime is the source-of-truth format; all other formats are derived from it
- visual-prompt format is declarative; this layer does NOT execute visual generation
- every format embeds provenance + confidence at minimum
