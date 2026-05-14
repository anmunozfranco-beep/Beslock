# Doctrine 03 — Mechanical consistency

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/mechanical-consistency/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Each product carries a fixed mechanical identity across every visual that depicts it: silhouette, component count and positions, sensor placement and count, keypad grid, screen position and size, indicator LEDs, handle geometry, mounting hardware, materials, and brand marks. Drift in any of these attributes is a regression.

## Why this matters

Customers and installers reason about the product as a physical object. A visual that shifts a sensor by 30 px or replaces a knob with a lever is not a stylistic variation — it is a different product. Mechanical drift turns the visual library into a contradiction set rather than a knowledge base.

## Principles

1. Immutable attributes are listed verbatim in the runtime policy and in `component-visibility-map.json` per product.
2. Position drift is bounded to ≤4 px on a 1024-px reference; rotation ≤1°; scale ≤1%; material region drift = 0 px.
3. Edge / latch / deadbolt / mortise structure must match the OEM-confirmed mechanism for that product family.
4. Exterior, interior and door-edge views are separate frames. They may not be combined in a single image.
5. Inferred or partially-visible components inherit the same mechanical contract as fully-visible components.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
