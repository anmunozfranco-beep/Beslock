#!/usr/bin/env python3
"""Phase 7 — Promote consolidated visual governance into KNOWLEDGE_BUILDING.

NON-DESTRUCTIVE. Establishes the constitutional / architectural layer at
`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`. Does NOT duplicate the runtime
governance at `visual-system/_governance/` — it references it.

Hard rules:
  * The runtime governance tree is left untouched.
  * No prompt, manifest, run record or Comfy workflow is altered.
  * No image is generated.
  * The constitution is doctrine; runtime files remain authoritative for
    operational rules.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
VG = KB / "VISUAL_GOVERNANCE"
RUNTIME_GOV = USER_MANUALS / "visual-system/_governance"
GOV_REPO = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "visual-constitution/1.0"

DOMAINS = [
    "visual-style-policy",
    "human-interaction-policy",
    "mechanical-consistency",
    "truth-source",
    "rendering-constraints",
    "comfy-contracts",
    "negative-prompts",
    "visual-risk",
    "visual-validation",
    "visual-lineage",
    "publication-constraints",
]

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]


# ---------------------------------------------------------------------------
# Doctrine documents (architectural — not operational rules).
# ---------------------------------------------------------------------------
def doctrine(slug: str, title: str, philosophy: str, principles: list[str],
             runtime_pointer: str, why: str = "") -> str:
    out = [
        f"# {title}",
        "",
        f"_Schema: `{SCHEMA}` · canonical doctrine · generated {NOW}._",
        "",
        "## Status",
        "",
        "This document is **architectural doctrine**. It explains *why* the policy exists and what it means for the platform. Operational, modular, runtime-oriented rules live in the runtime governance tree and are NOT restated here.",
        "",
        f"- Runtime authority: `{runtime_pointer}`",
        "- This file is constitutional. The runtime file is enforceable.",
        "",
        "## Philosophy",
        "",
        philosophy.strip(),
        "",
    ]
    if why:
        out += ["## Why this matters", "", why.strip(), ""]
    out += ["## Principles", ""] + [f"{i+1}. {p}" for i, p in enumerate(principles)] + [""]
    out += [
        "## Boundary with the runtime layer",
        "",
        "- This doctrine **MUST NOT** be the place where new operational rules are added.",
        "- New operational rules belong in the runtime governance tree under `visual-system/_governance/`.",
        "- When runtime rules change in a way that contradicts this doctrine, the contradiction is resolved by amending this doctrine first, then updating the runtime — not the other way round.",
        "",
    ]
    return "\n".join(out)


DOCS: dict[str, dict] = {
    "00-CONSTITUTION.md": {
        "title": "Beslock Visual Constitution",
        "body": [
            f"_Schema: `{SCHEMA}` · master constitutional document · generated {NOW}._",
            "",
            "## Mission",
            "",
            "The Beslock visual system exists to produce **deterministic, instructional, mechanically consistent visualisations of real Beslock products** so that customers, installers, support agents, and automated assistants can answer concrete operational questions without ambiguity. The visual system is part of the product knowledge layer, not a marketing surface.",
            "",
            "## Absolute principle",
            "",
            "> **Maximum operational clarity.** Not marketing aesthetics. Not cinematic storytelling. Not decorative AI art.",
            "",
            "Every doctrine in this constitution descends from this principle.",
            "",
            "## Architectural pillars",
            "",
            "1. **Truth-source primacy.** A single canonical PNG per product is the absolute visual ground truth. All other visuals extend, infer, contextualise or operationalise that PNG; they never redesign it.",
            "2. **Mechanical consistency.** Each product preserves the same hardware identity across every visual that depicts it: silhouette, sensor positions, keypad grid, handle geometry, latch/deadbolt structure, mounting layout, materials.",
            "3. **Hands-only human policy.** No faces, no bodies, no lifestyle. Hands appear only as instructional silhouettes when a procedure literally requires touch context.",
            "4. **Schematic / hybrid only.** Cinematic, marketing, photoreal-human and decorative styles are forbidden. Schematic and hybrid technical illustration are the only sanctioned modes for new work.",
            "5. **Comfy-native rendering.** ComfyUI is the sole approved rendering runtime. Every approved visual is produced through a registered, hashed, reviewer-approved workflow conditioned on the canonical PNG.",
            "6. **Semantic orchestration.** Generation is driven by the semantic layer (visual-intent, component-visibility, procedural-semantics, visual-risk, publication-intent) — not by free prompting.",
            "7. **Provenance-bound lineage.** Every approved visual has an immutable run record linking it to a canonical PNG, a workflow version, conditioning inputs, and an approver. No run record means not approved.",
            "8. **Validation-first promotion.** A visual is not in a product nucleus until it passes the manual review checklist, the per-product validation passes, and (when implemented) the automated tolerance gates.",
            "9. **Risk-tiered rigour.** Visuals that affect installation, operation, troubleshooting, pairing, safety or locking behaviour carry the strictest constraints, the lowest inference tolerance, and the highest validation bar.",
            "10. **Single canonical governance.** This document is the platform's visual constitution. The runtime authority is `visual-system/_governance/`. There are no parallel standards.",
            "",
            "## Governance hierarchy",
            "",
            "| Level | Layer | Location | Role |",
            "|---:|---|---|---|",
            "| 1 | Canonical doctrine | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` (this folder) | Constitutional / architectural / conceptual. Explains *why*. |",
            "| 2 | Runtime governance | `visual-system/_governance/` | Operational, modular policies. Enforces *what* and *how*. |",
            "| 3 | Per-product implementation | `ext-images/<slug>/visual-system/` and `ext-images/<slug>/knowledge-core/` | Local implementation: prompts, generation matrices, visual profiles, semantic intent / risk / publication maps. |",
            "| 4 | Execution / orchestration | `tools/visual_generation.py`, `tools/comfy/`, `ext-images/<slug>/automation/` | The Comfy runtime, the orchestration manifests and the immutable run records. |",
            "",
            "## Navigation",
            "",
            "Doctrine documents (this folder):",
            "",
            "- [`doctrine/01-purpose-and-philosophy.md`](doctrine/01-purpose-and-philosophy.md)",
            "- [`doctrine/02-truth-source-doctrine.md`](doctrine/02-truth-source-doctrine.md)",
            "- [`doctrine/03-mechanical-consistency-doctrine.md`](doctrine/03-mechanical-consistency-doctrine.md)",
            "- [`doctrine/04-human-interaction-doctrine.md`](doctrine/04-human-interaction-doctrine.md)",
            "- [`doctrine/05-rendering-style-doctrine.md`](doctrine/05-rendering-style-doctrine.md)",
            "- [`doctrine/06-comfy-constitution.md`](doctrine/06-comfy-constitution.md)",
            "- [`doctrine/07-semantic-orchestration-doctrine.md`](doctrine/07-semantic-orchestration-doctrine.md)",
            "- [`doctrine/08-validation-philosophy.md`](doctrine/08-validation-philosophy.md)",
            "- [`doctrine/09-visual-risk-philosophy.md`](doctrine/09-visual-risk-philosophy.md)",
            "- [`doctrine/10-publication-philosophy.md`](doctrine/10-publication-philosophy.md)",
            "- [`doctrine/11-lineage-and-provenance-doctrine.md`](doctrine/11-lineage-and-provenance-doctrine.md)",
            "",
            "Hierarchy and runtime linkage:",
            "",
            "- [`hierarchy/governance-hierarchy.md`](hierarchy/governance-hierarchy.md)",
            "- [`hierarchy/runtime-linkage-map.json`](hierarchy/runtime-linkage-map.json)",
            "",
            "Future extensibility:",
            "",
            "- [`extensibility/future-extensibility.md`](extensibility/future-extensibility.md)",
            "",
            "## Hard guarantees of this promotion",
            "",
            "- The runtime governance tree at `visual-system/_governance/` was not modified.",
            "- Per-product prompts, generation matrices, visual profiles and semantic JSON were not modified.",
            "- ComfyUI workflows under `tools/comfy/` were not modified.",
            "- No image was generated by this phase.",
            "",
            "## Amendment policy",
            "",
            "Changing a doctrine requires updating this folder first, then propagating the change into `visual-system/_governance/<domain>/policy.md`. Direct edits to runtime governance that contradict the constitution are out of policy and must be reverted, then re-introduced through this folder.",
        ],
    },
    "doctrine/01-purpose-and-philosophy.md": {
        "body": doctrine(
            "purpose",
            "Doctrine 01 — Purpose and philosophy",
            "Visuals exist to **answer concrete operational questions** about a real product. A visual is successful when a user can identify the product, locate the components a procedure references, follow the procedure without cross-checking another source, and trust that what they see matches what they own.",
            [
                "Visuals are knowledge artefacts, not marketing assets.",
                "A visual that delights but misleads is a regression.",
                "If clarity and aesthetics conflict, clarity wins.",
                "Editorial composition (callouts, arrows, labels) is added on top of generated images, not baked into them.",
                "The system optimises for support-burden reduction, not for visual virality.",
            ],
            "visual-system/_governance/visual-style-policy/policy.md",
            "Marketing-grade visuals encourage redesign, embellishment and stylistic drift. Each drift increment increases the chance that a user follows an instruction whose depicted hardware does not match the product they own. Misidentification is the most expensive failure mode the support function carries.",
        ),
    },
    "doctrine/02-truth-source-doctrine.md": {
        "body": doctrine(
            "truth-source",
            "Doctrine 02 — Truth-source primacy",
            "For each Beslock product there is exactly one canonical PNG at `ext-images/<slug>/source-of-truth/product-images/<Product>.png`. That PNG is the absolute visual ground truth. Every other visual the system produces extends, infers, contextualises or operationalises that PNG. None of them redesigns it.",
            [
                "The canonical PNG is editorial and authoritative; replacing it requires explicit governance, not opportunistic regeneration.",
                "Compatibility PNGs at the `ext-images/` root are legacy and decommission-pending.",
                "If visual QA cannot certify a generated or composited output, the canonical PNG is used directly. There is no degraded-quality fallback chain.",
                "Hero, catalogue, specification, onboarding-identification and certification-adjacent surfaces fall back to the canonical PNG by default.",
                "All conditioning inputs (cutouts, masks, depth, normal, line-art, IPAdapter references) derive from the canonical PNG of the SAME product.",
            ],
            "visual-system/_governance/truth-source/policy.md",
            "Once a derived visual is allowed to redesign hardware, every downstream surface that consumes that visual silently drifts away from the physical product. The canonical PNG anchors the entire visual lineage; if it stops being primary, the lineage stops being trustworthy.",
        ),
    },
    "doctrine/03-mechanical-consistency-doctrine.md": {
        "body": doctrine(
            "mechanical",
            "Doctrine 03 — Mechanical consistency",
            "Each product carries a fixed mechanical identity across every visual that depicts it: silhouette, component count and positions, sensor placement and count, keypad grid, screen position and size, indicator LEDs, handle geometry, mounting hardware, materials, and brand marks. Drift in any of these attributes is a regression.",
            [
                "Immutable attributes are listed verbatim in the runtime policy and in `component-visibility-map.json` per product.",
                "Position drift is bounded to ≤4 px on a 1024-px reference; rotation ≤1°; scale ≤1%; material region drift = 0 px.",
                "Edge / latch / deadbolt / mortise structure must match the OEM-confirmed mechanism for that product family.",
                "Exterior, interior and door-edge views are separate frames. They may not be combined in a single image.",
                "Inferred or partially-visible components inherit the same mechanical contract as fully-visible components.",
            ],
            "visual-system/_governance/mechanical-consistency/policy.md",
            "Customers and installers reason about the product as a physical object. A visual that shifts a sensor by 30 px or replaces a knob with a lever is not a stylistic variation — it is a different product. Mechanical drift turns the visual library into a contradiction set rather than a knowledge base.",
        ),
    },
    "doctrine/04-human-interaction-doctrine.md": {
        "body": doctrine(
            "human",
            "Doctrine 04 — Human interaction (hands-only)",
            "Humans do not exist in the Beslock visual ecosystem. Hands may exist, and only as instructional silhouettes when a procedure literally requires a touch context (installation, button-press, fingerprint enrolment, pairing, unlocking, operation guidance). No faces. No bodies. No portraits. No crowds. No lifestyle scenes. No emotional gestures.",
            [
                "When a hand is required, it appears as a silhouette or low-detail finger pointer, never as a realistic photograph.",
                "Hand presence is justified by the procedure being illustrated, not by composition.",
                "Hand interactions never alter the depicted hardware geometry.",
                "Multi-hand or two-person scenes are categorically forbidden.",
                "If a procedure can be illustrated by an arrow, an arrow is preferred over a hand.",
            ],
            "visual-system/_governance/human-interaction-policy/policy.md",
            "Faces and bodies introduce three kinds of risk simultaneously: (a) demographic and emotional implications that have no place in operational documentation, (b) generative artefacts (deformed hands, wrong fingers, uncanny faces) that destroy trust, and (c) attention competition with the product. Removing humans removes all three risks at once.",
        ),
    },
    "doctrine/05-rendering-style-doctrine.md": {
        "body": doctrine(
            "rendering-style",
            "Doctrine 05 — Rendering style",
            "Approved styles are schematic and hybrid technical illustration. Realistic and semi-realistic outputs are legacy-only and may not be produced for new work. Cinematic drama, marketing glamour, lifestyle staging, decorative rendering, dramatic / neon lighting, plastic-render aesthetics and brochure styling are forbidden. The single hardware side per image rule (exterior / interior / edge) applies across all styles.",
            [
                "New work uses schematic or hybrid only. Realistic and semi-realistic are reserved for legacy assets in transition.",
                "Schematic style is preferred for installation, wiring, anatomy, mounting, reset sequences, battery replacement and troubleshooting.",
                "Hybrid style is preferred for exterior identity, installed context, app context and product-shell-with-cues compositions.",
                "Generated text and numbers are not trustworthy and may not be used as instructional proof.",
                "Backgrounds are quiet, diagram-like or lightly contextual. Atmosphere is not a goal.",
            ],
            "visual-system/_governance/rendering-constraints/policy.md",
            "Photoreal, cinematic and lifestyle outputs encourage the model to invent geometry that 'looks right'. The cost of that invention is borne by every downstream consumer. Schematic and hybrid styles constrain the search space toward hardware fidelity by construction, not by hope.",
        ),
    },
    "doctrine/06-comfy-constitution.md": {
        "body": doctrine(
            "comfy",
            "Doctrine 06 — ComfyUI constitution",
            "ComfyUI is the only approved rendering runtime for the Beslock visual system. Every visual that ends up in a product nucleus is produced through a registered, semver-tagged, content-hashed, reviewer-approved ComfyUI workflow. No web UIs, no ad-hoc API calls, no one-off scripts, no parallel pipelines.",
            [
                "All approved workflows live under `tools/comfy/` and are listed in the workflow registry with id, semver, content hash, reviewer and approval timestamp.",
                "A workflow change is a NEW VERSION, not an in-place mutation.",
                "Every approved generation has an immutable run record under `ext-images/<slug>/automation/runs/` recording: canonical PNG path + hash, workflow id + version + content hash, prompt contract, seed, sampler / steps / CFG / scheduler / model name + hash, ControlNet / IPAdapter inputs, output paths, approval state, reviewer, timestamp.",
                "Identity-affecting generation must be conditioned on the canonical PNG of the SAME product or its derivatives.",
                "Cross-product IPAdapter references and cross-product prompt copy-paste are forbidden.",
            ],
            "visual-system/_governance/comfy-contracts/policy.md",
            "A single rendering runtime gives the system one place to enforce conditioning, one place to enforce reproducibility, and one place to add automated QA. Any parallel pipeline (a designer's web UI session, an exploratory API call) silently bypasses all three and ends up in the nucleus as an asset that cannot be regenerated, audited, or trusted.",
        ),
    },
    "doctrine/07-semantic-orchestration-doctrine.md": {
        "body": doctrine(
            "semantic-orchestration",
            "Doctrine 07 — Semantic orchestration",
            "Generation is driven by the semantic knowledge layer, not by freeform prompting. For each product the orchestrator consumes `visual-intent/`, `component-visibility/`, `procedural-semantics/`, `visual-risk/` and `publication-intent/` JSON to assemble prompts, conditioning, target dimensions and validation gates. Prompts are knowledge artefacts and are versioned alongside the semantic layer.",
            [
                "Prompts may not silently embed product identity from another product.",
                "Shared prompt fragments are referenced by component ID; they are not copy-pasted across products.",
                "Negative prompts resolve to a registry of components, not to ad-hoc strings.",
                "Per-slot generation declares its image class (schematic / hybrid), its mandatory visible components, its forbidden visual deviations, its target publication channels and (when implemented) whether it is a generation or a compositing slot.",
                "Procedural-semantics linkage is mandatory for any visual whose purpose is to illustrate a procedure.",
            ],
            "visual-system/_governance/comfy-contracts/policy.md",
            "Freeform prompting decouples the visual from the knowledge it is supposed to convey. When the prompt drifts from the procedure, the image drifts too. Anchoring prompts in the semantic layer keeps generation honest with the documentation it serves.",
        ),
    },
    "doctrine/08-validation-philosophy.md": {
        "body": doctrine(
            "validation",
            "Doctrine 08 — Validation philosophy",
            "A visual is not in a product nucleus until it passes the shared review checklist, the per-product validation passes, and — once implemented — the automated tolerance gates. Validation is mandatory; it is not a courtesy step. Failure modes are explicit (rework / reject / blocked-pending-OEM-validation), not implicit.",
            [
                "Manual pass conditions: product unmistakably identified; protected geometry matches; one hardware side per frame; schematic or hybrid; no full human figure; no generated text used as proof.",
                "Automated checks today are narrow (aspect, dimensions, edge energy, contrast, brightness, SHA-256 duplication).",
                "Automated checks required next: silhouette tolerance, component-anchor tolerance, sensor count, keypad grid, handle orientation, cross-product contamination, text presence, human presence, publication-format compliance, run-record compliance.",
                "QA gate states form a closed enum: pending, approved, rework, reject, blocked-pending-oem-validation.",
                "Validation evidence is part of the run record. A visual cannot be approved without it.",
            ],
            "visual-system/_governance/visual-validation/policy.md",
            "Manual review at scale degrades silently: tired reviewers approve drift they would have caught fresh. Automated tolerance gates and explicit gate states keep the validation bar constant regardless of throughput pressure.",
        ),
    },
    "doctrine/09-visual-risk-philosophy.md": {
        "body": doctrine(
            "visual-risk",
            "Doctrine 09 — Visual risk philosophy",
            "Visual inaccuracies are operational risks, not aesthetic flaws. A misplaced sensor, a wrong keypad layout or a hallucinated emergency port can break installation, mislead troubleshooting, or compromise lock-state interpretation. The visual-risk layer classifies every potential failure by severity (critical / high / medium / low), trigger components, failure mode, mitigation, and downstream consumers.",
            [
                "Critical risks include hallucinated sensors, wrong keypad layout, geometry that misleads at unboxing.",
                "High risks include missing mechanical key, misplaced fingerprint zone, incorrect handle direction.",
                "Medium risks include wrong camera position, fake emergency port, wrong indicator placement.",
                "Mitigation is uniform: the workflow MUST anchor the listed trigger components against OEM evidence and refuse to render the asset if anchors are missing.",
                "User risk levels (low / medium / high / critical) and visual-assistance priorities (P1 critical-path, P2 support, P3 editorial) are independent dimensions used for routing and prioritisation.",
            ],
            "visual-system/_governance/visual-risk/policy.md",
            "Treating visual errors as aesthetic concerns underestimates their downstream cost. A single misleading hero on a category page produces returns. A single misleading installation diagram produces support tickets, refunds and warranty claims. The risk model is what makes those costs visible at generation time.",
        ),
    },
    "doctrine/10-publication-philosophy.md": {
        "body": doctrine(
            "publication",
            "Doctrine 10 — Publication philosophy",
            "Each visual exists for a specific delivery surface (web, PDF, support, onboarding, chatbot, RAG, API). Per-channel constraints (resolution, aspect ratio, colour space, format, alt-text schema, load-time caps) are first-class governance, not packaging metadata. Today the per-channel specification is a known gap; format dimensions are hardcoded in the orchestrator.",
            [
                "Channel targets are declared per visual-intent in `publication-intent-map.json`.",
                "Hero, catalogue, specification and onboarding-identification surfaces fall back to the canonical PNG by default.",
                "App UI surfaces prefer real captures over generated UI; generated phone renders are acceptable only as context.",
                "Multilingual publication is anticipated; canonical Colombian-Spanish terminology is the baseline.",
                "Per-channel delivery specifications must be authored before mass orchestration begins.",
            ],
            "visual-system/_governance/publication-constraints/policy.md",
            "A visual that satisfies generation governance but not channel governance still ships broken: oversized for a chatbot, wrong colour space for print, missing alt-text for accessibility. Treating publication as an afterthought reproduces all of these failures across thousands of assets.",
        ),
    },
    "doctrine/11-lineage-and-provenance-doctrine.md": {
        "body": doctrine(
            "lineage",
            "Doctrine 11 — Lineage and provenance",
            "Visual lineage roots at the canonical PNG and flows through conditioning asset → ComfyUI workflow run → approved support visual → delivery placement. Run records are immutable. Delivery placements update writeback trackers (`image-production-status.md`, `generated/selected-assets-register.md`). Every approved visual must be traceable from the surface back to the canonical PNG.",
            [
                "The canonical PNG is the lineage root; everything else is downstream.",
                "Run records are append-only; new findings produce new run records, not edits to old ones.",
                "Missing run record == not approved == cannot be promoted.",
                "Delivery placements reference the run-record id explicitly.",
                "Lineage is queryable: given any approved visual, the chain back to its canonical PNG must be reconstructible.",
            ],
            "visual-system/_governance/visual-lineage/policy.md",
            "Without an immutable lineage chain, the visual library becomes a set of files whose origins cannot be explained or reproduced. With one, every visual carries its own audit trail and the platform can trust its own outputs.",
        ),
    },
    "hierarchy/governance-hierarchy.md": {
        "body": "\n".join([
            "# Governance hierarchy",
            "",
            f"_Schema: `{SCHEMA}` · generated {NOW}._",
            "",
            "Visual governance flows top-down. Higher levels constrain lower levels; lower levels implement higher levels. Conflicts are resolved at the highest level the conflict touches.",
            "",
            "| Level | Layer | Location | Authority over | Authority from |",
            "|---:|---|---|---|---|",
            "| 1 | Canonical doctrine | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` | Why visuals exist; architectural principles; future direction. | Platform leadership; this constitution. |",
            "| 2 | Runtime governance | `visual-system/_governance/<domain>/` | What the operational rules are; how they are enforced; what the registry IDs are. | Doctrine + implementation experience. |",
            "| 3 | Per-product implementation | `ext-images/<slug>/visual-system/`, `ext-images/<slug>/knowledge-core/` | Which slots a product has; what its prompts say; which components are visible; which procedures are illustrated. | Runtime governance + product nucleus rules. |",
            "| 4 | Execution / orchestration | `tools/visual_generation.py`, `tools/comfy/`, `ext-images/<slug>/automation/` | How a specific run is executed and recorded. | Per-product implementation + Comfy contracts. |",
            "",
            "## Resolution rules",
            "",
            "1. A doctrine change requires editing Level 1, then Level 2, then Level 3, then Level 4.",
            "2. A runtime rule that contradicts doctrine is out of policy and must be reverted.",
            "3. A per-product implementation that contradicts the runtime rule is out of policy and must be reverted.",
            "4. An execution-layer behaviour that contradicts the per-product implementation is a bug.",
            "",
            "## Cross-cutting boundaries",
            "",
            "- The constitution does NOT contain operational thresholds or registry IDs.",
            "- The runtime governance does NOT contain philosophy.",
            "- Per-product implementations do NOT redefine doctrine for themselves.",
            "- The execution layer does NOT carry policy state outside run records.",
        ]) + "\n",
    },
    "extensibility/future-extensibility.md": {
        "body": "\n".join([
            "# Future extensibility",
            "",
            f"_Schema: `{SCHEMA}` · generated {NOW}._",
            "",
            "The visual constitution is sized for current needs (still images of door locks, schematic + hybrid styles, web / PDF / support / onboarding / chatbot / RAG / API channels). Future extensions inherit the same doctrine without exemption.",
            "",
            "## Extension surfaces",
            "",
            "1. **Video and motion.** Mechanical consistency must hold across frames; the canonical PNG remains the truth source for every key frame; one hardware side per shot.",
            "2. **Onboarding flows.** Visuals tied to first-use must carry the strictest tolerance (product identification is the highest-cost failure).",
            "3. **Chatbot and RAG visuals.** Trustworthiness scoring becomes mandatory: canonical PNG = 1.0, approved support visual with full run record = 0.95, generated visual without run record = ineligible.",
            "4. **Troubleshooting visuals.** Must surface state changes (LED colour, latch position) without inventing UI text or labels.",
            "5. **AR guidance.** Anchor maps from `component-visibility/` become the authoritative target geometry; AR overlays must respect the same tolerances as static visuals.",
            "6. **Dynamic / on-demand rendering.** Same Comfy constitution applies; no exception path that bypasses workflow registration.",
            "7. **Multilingual publication.** Canonical Colombian-Spanish terminology glossary becomes prerequisite; translation rules live alongside the publication policy.",
            "8. **Automated visual QA.** The required-next checks listed in the validation doctrine (silhouette tolerance, component anchors, cross-product contamination, etc.) become mandatory before any extension surface ships.",
            "",
            "## Non-negotiable across extensions",
            "",
            "- Truth-source primacy applies to every extension.",
            "- Mechanical consistency applies to every extension.",
            "- Hands-only human policy applies to every extension.",
            "- Comfy-native rendering applies to every extension.",
            "- Provenance-bound lineage applies to every extension.",
            "",
            "## What this constitution does not yet cover",
            "",
            "- Audio guidance synchronised with visuals.",
            "- Live-feed integration with hardware telemetry.",
            "- Customer-uploaded photographs of installed locks (a different trust model).",
            "",
            "These are explicitly out of scope today. Adding them requires new doctrine, not stretched interpretation of the current text.",
        ]) + "\n",
    },
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else content + "\n")


def main() -> int:
    VG.mkdir(parents=True, exist_ok=True)

    written: list[str] = []

    # Master constitution
    body = "\n".join(["# Beslock Visual Constitution", ""] + DOCS["00-CONSTITUTION.md"]["body"])
    write(VG / "00-CONSTITUTION.md", body)
    written.append((VG / "00-CONSTITUTION.md").relative_to(REPO).as_posix())

    # Doctrine docs
    for rel, payload in DOCS.items():
        if rel == "00-CONSTITUTION.md":
            continue
        write(VG / rel, payload["body"])
        written.append((VG / rel).relative_to(REPO).as_posix())

    # Runtime linkage map
    runtime_map = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "policy": "Constitutional doctrine maps to runtime governance one-to-one. Each entry names the canonical doctrine file (Level 1) and the runtime authority it descends to (Level 2).",
        "links": [
            {"doctrine": "doctrine/01-purpose-and-philosophy.md",          "runtime": "visual-system/_governance/visual-style-policy/policy.md"},
            {"doctrine": "doctrine/02-truth-source-doctrine.md",           "runtime": "visual-system/_governance/truth-source/policy.md"},
            {"doctrine": "doctrine/03-mechanical-consistency-doctrine.md", "runtime": "visual-system/_governance/mechanical-consistency/policy.md"},
            {"doctrine": "doctrine/04-human-interaction-doctrine.md",      "runtime": "visual-system/_governance/human-interaction-policy/policy.md"},
            {"doctrine": "doctrine/05-rendering-style-doctrine.md",        "runtime": "visual-system/_governance/rendering-constraints/policy.md"},
            {"doctrine": "doctrine/06-comfy-constitution.md",              "runtime": "visual-system/_governance/comfy-contracts/policy.md"},
            {"doctrine": "doctrine/07-semantic-orchestration-doctrine.md", "runtime": "visual-system/_governance/comfy-contracts/policy.md"},
            {"doctrine": "doctrine/08-validation-philosophy.md",           "runtime": "visual-system/_governance/visual-validation/policy.md"},
            {"doctrine": "doctrine/09-visual-risk-philosophy.md",          "runtime": "visual-system/_governance/visual-risk/policy.md"},
            {"doctrine": "doctrine/10-publication-philosophy.md",          "runtime": "visual-system/_governance/publication-constraints/policy.md"},
            {"doctrine": "doctrine/11-lineage-and-provenance-doctrine.md", "runtime": "visual-system/_governance/visual-lineage/policy.md"},
        ],
        "negative_prompts_runtime": "visual-system/_governance/negative-prompts/policy.md (no separate doctrine file; covered under doctrine 07 — semantic orchestration)",
        "per_product_implementation_pattern": {
            "prompts":             "ext-images/<slug>/visual-system/prompts/ai-image-prompts.md",
            "generation_matrix":   "ext-images/<slug>/visual-system/generation-matrices/image-generation-matrix.md",
            "visual_profile":      "ext-images/<slug>/visual-system/references/<slug>-visual-profile.md",
            "validation":          "ext-images/<slug>/visual-system/validations/visual-validation.md",
            "visual_intent":       "ext-images/<slug>/knowledge-core/visual-intent/intent-*.json",
            "visual_risk":         "ext-images/<slug>/knowledge-core/visual-risk/risk-*.json",
            "component_visibility":"ext-images/<slug>/knowledge-core/component-visibility/component-visibility-map.json",
            "publication_intent":  "ext-images/<slug>/knowledge-core/publication-intent/publication-intent-map.json",
            "procedural_semantics":"ext-images/<slug>/knowledge-core/procedural-semantics/semantic-*.json",
        },
        "execution_layer": {
            "runner":               "tools/visual_generation.py",
            "workflow_baseline":    "tools/comfy/workflow_api.json.json",
            "orchestration_manifest":"ext-images/<slug>/automation/orchestrators/orchestration-manifest.json",
            "run_records":          "ext-images/<slug>/automation/runs/",
        },
        "products_in_scope": PRODUCTS,
    }
    write(VG / "hierarchy/runtime-linkage-map.json", json.dumps(runtime_map, ensure_ascii=False, indent=2))
    written.append((VG / "hierarchy/runtime-linkage-map.json").relative_to(REPO).as_posix())

    # ----- Reports -----
    rep_dir = GOV_REPO / "reports" / "visual-constitution"
    rep_dir.mkdir(parents=True, exist_ok=True)

    def report(name: str, payload: dict) -> None:
        (rep_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    # 1 — new KNOWLEDGE_BUILDING governance structure
    structure = {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/",
        "files": written,
        "principle": "Constitutional layer. References runtime governance; never duplicates it.",
        "preserved_unchanged": [
            "wp-content/themes/beslock-custom/User manuals/visual-system/_governance/",
            "wp-content/themes/beslock-custom/User manuals/ext-images/<all products>/visual-system/",
            "wp-content/themes/beslock-custom/User manuals/ext-images/<all products>/knowledge-core/",
            "tools/visual_generation.py",
            "tools/comfy/",
        ],
        "modified_existing_files": [],
        "moved_existing_files": [],
        "deleted_existing_files": [],
    }
    report("01-knowledge-building-governance-structure.json", structure)

    # 2 — master policy document summary
    report("02-master-policy-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "master_document": "KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/00-CONSTITUTION.md",
        "ten_pillars": [
            "Truth-source primacy",
            "Mechanical consistency",
            "Hands-only human policy",
            "Schematic / hybrid only",
            "Comfy-native rendering",
            "Semantic orchestration",
            "Provenance-bound lineage",
            "Validation-first promotion",
            "Risk-tiered rigour",
            "Single canonical governance",
        ],
        "absolute_principle": "Maximum operational clarity — not marketing aesthetics, not cinematic storytelling, not decorative AI art.",
        "doctrine_documents": [
            "doctrine/01-purpose-and-philosophy.md",
            "doctrine/02-truth-source-doctrine.md",
            "doctrine/03-mechanical-consistency-doctrine.md",
            "doctrine/04-human-interaction-doctrine.md",
            "doctrine/05-rendering-style-doctrine.md",
            "doctrine/06-comfy-constitution.md",
            "doctrine/07-semantic-orchestration-doctrine.md",
            "doctrine/08-validation-philosophy.md",
            "doctrine/09-visual-risk-philosophy.md",
            "doctrine/10-publication-philosophy.md",
            "doctrine/11-lineage-and-provenance-doctrine.md",
        ],
    })

    # 3 — governance hierarchy map
    report("03-governance-hierarchy-map.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "levels": [
            {"level": 1, "name": "Canonical doctrine",          "root": "KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/", "role": "constitutional / architectural / conceptual"},
            {"level": 2, "name": "Runtime governance",          "root": "visual-system/_governance/",            "role": "operational, modular, runtime-oriented"},
            {"level": 3, "name": "Per-product implementation", "root": "ext-images/<slug>/{visual-system,knowledge-core}/", "role": "local prompts, profiles, semantic JSON"},
            {"level": 4, "name": "Execution / orchestration",  "root": "tools/visual_generation.py + tools/comfy/ + ext-images/<slug>/automation/", "role": "ComfyUI runtime + run records"},
        ],
        "resolution_rules": [
            "Doctrine changes propagate downward (Level 1 → 2 → 3 → 4).",
            "Runtime rules contradicting doctrine are out of policy and must be reverted.",
            "Per-product implementations contradicting runtime rules are out of policy.",
            "Execution-layer behaviour contradicting per-product implementation is a bug.",
        ],
    })

    # 4 — doctrine promotion summary
    report("04-doctrine-promotion-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "promoted_domains": DOMAINS,
        "doctrine_to_runtime_links": runtime_map["links"],
        "promotion_rule": "Doctrine documents reference the runtime authority they descend to. They do not restate operational rules.",
        "products_in_scope": PRODUCTS,
    })

    # 5 — runtime linkage summary
    report("05-runtime-linkage-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "constitutional_root":     "KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/",
        "runtime_root":            "visual-system/_governance/",
        "per_product_root_pattern":"ext-images/<slug>/{visual-system,knowledge-core}/",
        "execution_root":          "tools/visual_generation.py + tools/comfy/",
        "linkage_map_file":        "KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/hierarchy/runtime-linkage-map.json",
        "guarantee":               "No runtime file was modified by this promotion.",
    })

    # 6 — unresolved governance conflicts (carry-over from Phase 6)
    report("06-unresolved-governance-conflicts.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "policy": "Conflicts inherited from Phase 6 visual-governance consolidation. NOT resolved by this promotion. Resolution is a separate, dedicated phase.",
        "carry_over_source": "_repository-governance/reports/visual-governance/03-duplications-and-conflicts.json",
        "items": [
            {"id": "conflict.negative-prompts.cross-product-duplication",     "status": "open"},
            {"id": "conflict.image-class.assignment-implicit",                 "status": "open"},
            {"id": "conflict.blocked-slots.no-status-enum",                    "status": "open"},
            {"id": "conflict.composite-vs-generate.unspecified-per-slot",      "status": "open"},
            {"id": "conflict.workflow-filename.double-extension",              "status": "open"},
            {"id": "conflict.legacy-png.no-decommission-timeline",             "status": "open"},
        ],
    })

    # 7 — future governance extensibility
    report("07-future-extensibility-report.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "extension_surfaces": [
            "video and motion",
            "onboarding flows",
            "chatbot and RAG visuals",
            "troubleshooting visuals",
            "AR guidance",
            "dynamic / on-demand rendering",
            "multilingual publication",
            "automated visual QA",
        ],
        "non_negotiable_across_extensions": [
            "truth-source primacy",
            "mechanical consistency",
            "hands-only human policy",
            "comfy-native rendering",
            "provenance-bound lineage",
        ],
        "out_of_scope_today": [
            "audio guidance synchronised with visuals",
            "live-feed integration with hardware telemetry",
            "customer-uploaded photographs of installed locks",
        ],
        "extensibility_doc": "KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/extensibility/future-extensibility.md",
    })

    # 8 — visual constitution readiness
    report("08-visual-constitution-readiness.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "constitutional_layer_ready": True,
        "runtime_governance_ready":   True,
        "per_product_layer_ready_count": 5,
        "per_product_layer_blocked":  ["e-nova (0 procedural semantics from Phase 3)"],
        "execution_layer_blockers": [
            "tools/comfy/workflow_api.json.json filename normalisation + workflow registry",
            "negative-prompt component registry wiring into per-product prompts",
            "model + sampler approval registry",
            "automated tolerance + cross-product-contamination QA",
            "per-channel publication spec (publication-constraints policy is currently a draft)",
        ],
        "ready_for": [
            "constitutional reference and review",
            "downstream platform documentation linking",
            "future video / AR / chatbot extension authoring",
            "next-phase implementation work that resolves the open conflicts",
        ],
        "not_ready_for": [
            "mass Comfy orchestration (workflow registry + QA gates required first)",
            "production image generation against unresolved conflicts",
        ],
    })

    print("Visual constitution promotion complete.")
    print(f"  Constitutional root: {VG.relative_to(REPO).as_posix()}")
    print(f"  Files written:       {len(written)}")
    print(f"  Reports:             {rep_dir.relative_to(REPO).as_posix()}/01..08")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
