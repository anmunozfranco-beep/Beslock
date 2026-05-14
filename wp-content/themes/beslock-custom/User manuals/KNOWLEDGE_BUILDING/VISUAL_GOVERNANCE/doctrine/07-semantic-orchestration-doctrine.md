# Doctrine 07 — Semantic orchestration

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/comfy-contracts/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Generation is driven by the semantic knowledge layer, not by freeform prompting. For each product the orchestrator consumes `visual-intent/`, `component-visibility/`, `procedural-semantics/`, `visual-risk/` and `publication-intent/` JSON to assemble prompts, conditioning, target dimensions and validation gates. Prompts are knowledge artefacts and are versioned alongside the semantic layer.

## Why this matters

Freeform prompting decouples the visual from the knowledge it is supposed to convey. When the prompt drifts from the procedure, the image drifts too. Anchoring prompts in the semantic layer keeps generation honest with the documentation it serves.

## Principles

1. Prompts may not silently embed product identity from another product.
2. Shared prompt fragments are referenced by component ID; they are not copy-pasted across products.
3. Negative prompts resolve to a registry of components, not to ad-hoc strings.
4. Per-slot generation declares its image class (schematic / hybrid), its mandatory visible components, its forbidden visual deviations, its target publication channels and (when implemented) whether it is a generation or a compositing slot.
5. Procedural-semantics linkage is mandatory for any visual whose purpose is to illustrate a procedure.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
