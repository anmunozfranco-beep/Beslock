# Extraction Report

**Source file:** `e-Shied_2.pdf`  
**Generated:** 2026-05-13 15:09 UTC

## Summary

| Field | Value |
|---|---|
| PDF type | Scanned / image-based |
| Pages processed | 1 |
| Final OCR method | pytesseract |
| Average OCR confidence | 55.6% |
| Extraction quality | **Poor** |
| Total text characters | 814 |
| Sections detected | 1 |
| Specifications detected | 1 |
| Setup steps detected | 0 |
| Warning notes detected | 0 |

## OCR Methods Attempted

- **ocrmypdf**: ❌ Failed — OCR engine does not have language data for the following requested languages: 
spa
Please install the appropriate language data for your OCR engine.

See the online documentation for instructions:
    https://ocrmypdf.readthedocs.io/en/latest/languages.html

Note: most languages are identified by a 3-letter ISO 639-2 Code.
For example, English is 'eng', German is 'deu', and Spanish is 'spa'.
Simplified Chinese is 'chi_sim' and Traditional Chinese is 'chi_tra'.
- **pytesseract**: ✅ Success

## Detected Semantic Sections

- (no specific categories detected)

## Section Index

1. **Plantilla De Instalacion** (General) — 5 lines

## Quality Notes

- Extraction quality is poor. Manual correction of the raw text is recommended before use.
- Low OCR confidence detected. Consider rescanning or improving image quality.
- No numbered setup steps were automatically detected.
- Missing expected sections: Setup Steps, App Instructions.

## Downstream Readiness

Generated artifacts are organized for use in:

- **WooCommerce product pages** — use `manual.json` `.specifications` and `.sections`
- **Technical manuals** — use `manual.md` as a structured draft base
- **FAQs** — extract from `manual.json` `.sections` with category `Troubleshooting`
- **Installation guides** — extract from `manual.json` `.sections` with category `Installation`
