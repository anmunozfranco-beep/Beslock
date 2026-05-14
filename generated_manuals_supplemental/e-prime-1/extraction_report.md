# Extraction Report

**Source file:** `e-Prime_1.pdf`  
**Generated:** 2026-05-13 15:09 UTC

## Summary

| Field | Value |
|---|---|
| PDF type | Scanned / image-based |
| Pages processed | 6 |
| Final OCR method | pytesseract |
| Average OCR confidence | 86.4% |
| Extraction quality | **Good** |
| Total text characters | 6,424 |
| Sections detected | 3 |
| Specifications detected | 3 |
| Setup steps detected | 2 |
| Warning notes detected | 2 |

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

1. **Manual De Cerradura Inteligente** (General) — 61 lines
2. **Instale Las Baterias E Intente Desbloquear Usando El Huella Dactilar O Ingresando La** (General) — 40 lines
3. **Después De Instalar Una Nueva Cerradura, Realice La Inicializacién Para Borrar Cualquier** (General) — 16 lines

## Quality Notes

- Extraction quality is good. The content should be usable for manual generation.
- Troubleshooting candidates detected: 1.
- Missing expected sections: App Instructions.

## Downstream Readiness

Generated artifacts are organized for use in:

- **WooCommerce product pages** — use `manual.json` `.specifications` and `.sections`
- **Technical manuals** — use `manual.md` as a structured draft base
- **FAQs** — extract from `manual.json` `.sections` with category `Troubleshooting`
- **Installation guides** — extract from `manual.json` `.sections` with category `Installation`
