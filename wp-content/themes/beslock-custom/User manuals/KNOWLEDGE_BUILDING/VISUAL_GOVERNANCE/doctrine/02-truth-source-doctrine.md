# Doctrine 02 — Truth-source primacy

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/truth-source/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

For each Beslock product there is exactly one canonical PNG at `ext-images/<slug>/source-of-truth/product-images/<Product>.png`. That PNG is the absolute visual ground truth. Every other visual the system produces extends, infers, contextualises or operationalises that PNG. None of them redesigns it.

## Why this matters

Once a derived visual is allowed to redesign hardware, every downstream surface that consumes that visual silently drifts away from the physical product. The canonical PNG anchors the entire visual lineage; if it stops being primary, the lineage stops being trustworthy.

## Principles

1. The canonical PNG is editorial and authoritative; replacing it requires explicit governance, not opportunistic regeneration.
2. Compatibility PNGs at the `ext-images/` root are legacy and decommission-pending.
3. If visual QA cannot certify a generated or composited output, the canonical PNG is used directly. There is no degraded-quality fallback chain.
4. Hero, catalogue, specification, onboarding-identification and certification-adjacent surfaces fall back to the canonical PNG by default.
5. All conditioning inputs (cutouts, masks, depth, normal, line-art, IPAdapter references) derive from the canonical PNG of the SAME product.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
