# Doctrine 06 — ComfyUI constitution

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/comfy-contracts/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

ComfyUI is the only approved rendering runtime for the Beslock visual system. Every visual that ends up in a product nucleus is produced through a registered, semver-tagged, content-hashed, reviewer-approved ComfyUI workflow. No web UIs, no ad-hoc API calls, no one-off scripts, no parallel pipelines.

## Why this matters

A single rendering runtime gives the system one place to enforce conditioning, one place to enforce reproducibility, and one place to add automated QA. Any parallel pipeline (a designer's web UI session, an exploratory API call) silently bypasses all three and ends up in the nucleus as an asset that cannot be regenerated, audited, or trusted.

## Principles

1. All approved workflows live under `tools/comfy/` and are listed in the workflow registry with id, semver, content hash, reviewer and approval timestamp.
2. A workflow change is a NEW VERSION, not an in-place mutation.
3. Every approved generation has an immutable run record under `ext-images/<slug>/automation/runs/` recording: canonical PNG path + hash, workflow id + version + content hash, prompt contract, seed, sampler / steps / CFG / scheduler / model name + hash, ControlNet / IPAdapter inputs, output paths, approval state, reviewer, timestamp.
4. Identity-affecting generation must be conditioned on the canonical PNG of the SAME product or its derivatives.
5. Cross-product IPAdapter references and cross-product prompt copy-paste are forbidden.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
