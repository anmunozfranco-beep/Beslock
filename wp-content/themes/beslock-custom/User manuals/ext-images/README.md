# ext-images

## Purpose
This directory is the visual truth layer for the Beslock manual-reconstruction system.

Each product currently has one canonical reference image that anchors geometry, interaction zones, proportions, and product-specific constraints for AI-assisted image generation.

## Current compatibility model
The flat files at this directory root remain the current canonical references:
- `e-flex.webp`
- `e-nova.webp`
- `e-orbit.webp`
- `e-prime.webp`
- `e-shield.webp`
- `e-touch.webp`

New product subfolders now hold the operational metadata for those same products:
- visual profiles
- review notes
- future colocated reference variants when needed

This keeps backward compatibility while allowing the visual system to grow around the references already present.

## Update rule
When a better reference image becomes available:
1. replace or version the product reference deliberately
2. update the product visual profile if geometry or finish assumptions change
3. record the reason in the product `notes.md`
4. re-review any generated assets derived from the previous reference

## Non-goals
Do not use this directory for marketing moodboards, decorative inspiration, or unrelated screenshots.
