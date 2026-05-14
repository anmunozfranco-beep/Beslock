# Doctrine 09 — Visual risk philosophy

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/visual-risk/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Visual inaccuracies are operational risks, not aesthetic flaws. A misplaced sensor, a wrong keypad layout or a hallucinated emergency port can break installation, mislead troubleshooting, or compromise lock-state interpretation. The visual-risk layer classifies every potential failure by severity (critical / high / medium / low), trigger components, failure mode, mitigation, and downstream consumers.

## Why this matters

Treating visual errors as aesthetic concerns underestimates their downstream cost. A single misleading hero on a category page produces returns. A single misleading installation diagram produces support tickets, refunds and warranty claims. The risk model is what makes those costs visible at generation time.

## Principles

1. Critical risks include hallucinated sensors, wrong keypad layout, geometry that misleads at unboxing.
2. High risks include missing mechanical key, misplaced fingerprint zone, incorrect handle direction.
3. Medium risks include wrong camera position, fake emergency port, wrong indicator placement.
4. Mitigation is uniform: the workflow MUST anchor the listed trigger components against OEM evidence and refuse to render the asset if anchors are missing.
5. User risk levels (low / medium / high / critical) and visual-assistance priorities (P1 critical-path, P2 support, P3 editorial) are independent dimensions used for routing and prioritisation.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
