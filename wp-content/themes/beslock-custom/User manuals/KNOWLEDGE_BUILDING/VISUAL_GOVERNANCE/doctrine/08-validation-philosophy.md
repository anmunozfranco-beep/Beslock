# Doctrine 08 — Validation philosophy

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/visual-validation/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

A visual is not in a product nucleus until it passes the shared review checklist, the per-product validation passes, and — once implemented — the automated tolerance gates. Validation is mandatory; it is not a courtesy step. Failure modes are explicit (rework / reject / blocked-pending-OEM-validation), not implicit.

## Why this matters

Manual review at scale degrades silently: tired reviewers approve drift they would have caught fresh. Automated tolerance gates and explicit gate states keep the validation bar constant regardless of throughput pressure.

## Principles

1. Manual pass conditions: product unmistakably identified; protected geometry matches; one hardware side per frame; schematic or hybrid; no full human figure; no generated text used as proof.
2. Automated checks today are narrow (aspect, dimensions, edge energy, contrast, brightness, SHA-256 duplication).
3. Automated checks required next: silhouette tolerance, component-anchor tolerance, sensor count, keypad grid, handle orientation, cross-product contamination, text presence, human presence, publication-format compliance, run-record compliance.
4. QA gate states form a closed enum: pending, approved, rework, reject, blocked-pending-oem-validation.
5. Validation evidence is part of the run record. A visual cannot be approved without it.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
