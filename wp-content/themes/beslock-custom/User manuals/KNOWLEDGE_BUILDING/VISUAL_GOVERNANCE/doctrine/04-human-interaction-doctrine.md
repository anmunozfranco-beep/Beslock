# Doctrine 04 — Human interaction (hands-only)

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/human-interaction-policy/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Humans do not exist in the Beslock visual ecosystem. Hands may exist, and only as instructional silhouettes when a procedure literally requires a touch context (installation, button-press, fingerprint enrolment, pairing, unlocking, operation guidance). No faces. No bodies. No portraits. No crowds. No lifestyle scenes. No emotional gestures.

## Why this matters

Faces and bodies introduce three kinds of risk simultaneously: (a) demographic and emotional implications that have no place in operational documentation, (b) generative artefacts (deformed hands, wrong fingers, uncanny faces) that destroy trust, and (c) attention competition with the product. Removing humans removes all three risks at once.

## Principles

1. When a hand is required, it appears as a silhouette or low-detail finger pointer, never as a realistic photograph.
2. Hand presence is justified by the procedure being illustrated, not by composition.
3. Hand interactions never alter the depicted hardware geometry.
4. Multi-hand or two-person scenes are categorically forbidden.
5. If a procedure can be illustrated by an arrow, an arrow is preferred over a hand.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
