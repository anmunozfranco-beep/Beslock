# Doctrine 10 — Publication philosophy

_Schema: `visual-constitution/1.0` · canonical doctrine · generated 2026-05-13T16:25:41Z._

## Status

This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.

- Runtime authority: `visual-system/_governance/publication-constraints/policy.md`
- This file is constitutional. The runtime file is enforceable.

## Philosophy

Each visual exists for a specific delivery surface (web, PDF, support, onboarding, chatbot, RAG, API). Per-channel constraints (resolution, aspect ratio, colour space, format, alt-text schema, load-time caps) are first-class governance, not packaging metadata. Today the per-channel specification is a known gap; format dimensions are hardcoded in the orchestrator.

## Why this matters

A visual that satisfies generation governance but not channel governance still ships broken: oversized for a chatbot, wrong colour space for print, missing alt-text for accessibility. Treating publication as an afterthought reproduces all of these failures across thousands of assets.

## Principles

1. Channel targets are declared per visual-intent in `publication-intent-map.json`.
2. Hero, catalogue, specification and onboarding-identification surfaces fall back to the canonical PNG by default.
3. App UI surfaces prefer real captures over generated UI; generated phone renders are acceptable only as context.
4. Multilingual publication is anticipated; canonical Colombian-Spanish terminology is the baseline.
5. Per-channel delivery specifications must be authored before mass orchestration begins.

## Boundary with the runtime layer

- This doctrine **MUST NOT** be the place where new operational rules are added.
- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.
- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.
