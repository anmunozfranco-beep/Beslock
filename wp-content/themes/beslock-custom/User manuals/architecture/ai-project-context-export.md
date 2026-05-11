# AI Project Context Export

## Working definition
Beslock is operating an AI-assisted technical documentation platform for smart-lock manuals.

The visual subsystem is not tasked with inventing brand imagery. It is tasked with reconstructing missing, documentation-grade visuals from minimal source material while preserving product truth.

## Stable assumptions
- Markdown is the primary coordination surface.
- OCR outputs and editorial standardization remain file-based.
- Each product has a canonical visual reference in `../ext-images/`.
- App UI should prefer real captures over generated UI.
- Generated images are support assets that may later be replaced by real photography or captures.

## Production priorities
1. preserve geometry
2. preserve interaction clarity
3. prefer maintainable prompt composition over monolithic prompts
4. classify realism intentionally
5. track status per asset so planning becomes operational

## Review standard
An image is acceptable only if:
- the product remains visually identifiable
- the interaction zone is clear
- the scene helps a documentation task
- AI artifacts do not create false instructions
- the asset can be mapped deterministically to a manual or CMS slot
