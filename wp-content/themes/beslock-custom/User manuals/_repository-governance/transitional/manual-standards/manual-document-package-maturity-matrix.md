# Beslock Manual Document Package Maturity Matrix

## Purpose
Track which document types are already normalized per product and which ones are still pending because a reliable source has not been integrated yet.

## Status legend
- `ready` -> normalized and present in `User manuals/`
- `guide-only` -> technical companion exists, but it is not a full-scale drilling template
- `template` -> dedicated installation template companion exists and is backed by a source suitable for print/use
- `pending` -> no normalized document yet

## Product maturity

| Product | User manual | Installation manual | App manual | Installation companion | Notes |
|---|---|---|---|---|---|
| e-Flex | ready | ready | ready | guide-only | `e-Flex_1.pdf` adds strong installation and app context, but no 1:1 drilling template |
| e-Nova | ready | pending | pending | pending | current package still centers on user-manual coverage |
| e-Orbit | ready | pending | ready | pending | `e-Orbit_1.xls` and `e-Orbit_2.pdf` add strong app and technical-spec knowledge, but no mounting guide or drilling template |
| e-Prime | ready | ready | ready | guide-only | `e-Prime_1.pdf` is a mounting guide, not a print-scale drilling template |
| e-Shield | ready | ready | ready | template | `e-Shied_2.pdf` works as a dedicated installation-template companion |
| e-Touch | ready | ready | ready | guide-only | `e-Touch_1.pdf` adds installation and Bluetooth app guidance, but no 1:1 drilling template |

## Current reference files

| Product | Key files |
|---|---|
| e-Flex | `e-Flex user manual - image-ready.md`, `e-Flex installation manual.md`, `e-Flex app manual.md`, `e-Flex - installation template standard.md` |
| e-Nova | `e-Nova user manual - image-ready.md` |
| e-Orbit | `e-Orbit user manual - image-ready.md`, `e-Orbit app manual.md`, `e-Orbit - supplemental source review.md` |
| e-Prime | `e-Prime user manual - image-ready.md`, `e-Prime installation manual.md`, `e-Prime app manual.md`, `e-Prime - installation template standard.md` |
| e-Shield | `e-Shield user manual - image-ready.md`, `e-Shield installation manual.md`, `e-Shield app manual.md`, `e-Shield - installation template standard.md` |
| e-Touch | `e-Touch user manual - image-ready.md`, `e-Touch installation manual.md`, `e-Touch app manual.md`, `e-Touch - installation template standard.md` |

## Operational note
This matrix follows the progressive package rule from `manual-document-package-standard.md`: missing installation or app docs stay `pending` until a trustworthy source is integrated, instead of being invented to fill the grid.