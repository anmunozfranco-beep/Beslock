# Image-to-Image Guide

## Purpose
Use the canonical reference image as the geometry anchor when a generation tool supports image conditioning or image-to-image workflows.

## Recommended sequence
1. Start from the product visual profile.
2. Use the canonical product reference image from `../../ext-images/*.webp` as the first visual input.
3. Add one interaction-type module and only the scene context needed for the manual step.
4. Keep denoising or transformation strength low enough to preserve geometry.
5. Reject any variant that swaps the lock family or moves protected features.

## Good candidates
- hero or installed-context images
- fingerprint or keypad interactions where the hardware shape must stay strict
- product-in-context scenes with limited pose changes

## Poor candidates
- wiring diagrams
- battery internals without real references
- complex app UI explanations
