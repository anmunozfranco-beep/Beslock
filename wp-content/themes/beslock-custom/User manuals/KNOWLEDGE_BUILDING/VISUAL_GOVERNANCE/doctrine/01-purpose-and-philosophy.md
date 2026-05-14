# Doctrine 01 — Purpose and philosophy

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/visual-style-policy/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Visuals exist to **answer concrete operational questions** about a real product. A visual is successful when a user can identify the product, locate the components a procedure references, follow the procedure without cross-checking another source, and trust that what they see matches what they own.

## Why this matters

Marketing-grade visuals encourage redesign, embellishment and stylistic drift. Each drift increment increases the chance that a user follows an instruction whose depicted hardware does not match the product they own. Misidentification is the most expensive failure mode the support function carries.

## Principles

1. Visuals are knowledge artefacts, not marketing assets.
2. A visual that delights but misleads is a regression.
3. If clarity and aesthetics conflict, clarity wins.
4. Editorial composition (callouts, arrows, labels) is added on top of generated images, not baked into them.
5. The system optimises for support-burden reduction, not for visual virality.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
