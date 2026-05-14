# Doctrine 11 — Lineage and provenance

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/visual-lineage/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Visual lineage roots at the canonical PNG and flows through conditioning asset → ComfyUI workflow run → approved support visual → delivery placement. Run records are immutable. Delivery placements update writeback trackers (`image-production-status.md`, `generated/selected-assets-register.md`). Every approved visual must be traceable from the surface back to the canonical PNG.

## Why this matters

Without an immutable lineage chain, the visual library becomes a set of files whose origins cannot be explained or reproduced. With one, every visual carries its own audit trail and the platform can trust its own outputs.

## Principles

1. The canonical PNG is the lineage root; everything else is downstream.
2. Run records are append-only; new findings produce new run records, not edits to old ones.
3. Missing run record == not approved == cannot be promoted.
4. Delivery placements reference the run-record id explicitly.
5. Lineage is queryable: given any approved visual, the chain back to its canonical PNG must be reconstructible.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
