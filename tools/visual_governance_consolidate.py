#!/usr/bin/env python3
"""Phase 6 — Canonical visual-governance consolidation (NON-DESTRUCTIVE).

Builds a SINGLE consolidated visual governance home at:
  wp-content/themes/beslock-custom/User manuals/visual-system/_governance/

Each canonical policy is a thin pointer + normalisation document. Source
fragments are NOT moved, copied, rewritten, or summarised in a way that
loses fidelity. Each canonical policy carries a `sources.json` that lists
the upstream documents it consolidates.

Also emits the 12 final reports under:
  _repository-governance/reports/visual-governance/

Hard rules:
  * No file is moved.
  * No existing governance fragment is modified.
  * No prompt, manifest, or run record is rewritten.
  * No image is generated.
  * No Comfy workflow is altered.
  * Conflicts are reported, not resolved.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
VS = USER_MANUALS / "visual-system"
GOV_VS = VS / "_governance"
GOV_REPO = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "visual-governance/1.0"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]


# ---------------------------------------------------------------------------
# Discovered governance fragments (from the deep-discovery pass).
# ---------------------------------------------------------------------------
DOMAIN_FRAGMENTS = {
    "visual-style-policy": {
        "title": "Global visual style policy",
        "intent": (
            "Restrict ALL future visual generation to operational-clarity styles. "
            "Schematic, hybrid technical, instructional rendering, semi-realistic "
            "operational visualisation, technical close-ups, annotated procedural "
            "visuals and simplified operational diagrams are the only allowed modes. "
            "Cinematic, lifestyle, marketing, decorative, photoreal-human and "
            "dramatic-lighting styles are forbidden."
        ),
        "sources": [
            "visual-system/shared/visual-rules/manual-image-reset-policy.md",
            "visual-system/shared/visual-rules/realism-vs-schematic.md",
            "visual-system/shared/visual-rules/ai-limitations.md",
            "visual-system/README.md",
            "KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md",
        ],
        "allowed_classes": ["schematic", "hybrid"],
        "legacy_only_classes": ["realistic", "semi-realistic"],
        "forbidden": [
            "cinematic drama",
            "marketing glamor",
            "photorealistic lifestyle staging",
            "decorative AI rendering",
            "stock-photo aesthetics",
            "dramatic / neon lighting",
            "brochure imagery",
            "emotional composition",
        ],
    },
    "human-interaction-policy": {
        "title": "Human representation policy (hands-only)",
        "intent": (
            "No faces. No bodies. No human identity. Hands MAY appear, and only as "
            "instructional silhouettes when a procedure (installation, button "
            "pressing, fingerprint enrolment, pairing, unlocking) requires a touch "
            "context. Cross-product / lifestyle hand photos are forbidden."
        ),
        "sources": [
            "visual-system/shared/visual-rules/manual-image-reset-policy.md",
            "visual-system/shared/generation-guides/review-checklist.md",
            "visual-system/shared/visual-rules/ai-limitations.md",
            "KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md",
        ],
        "allowed_subjects": [
            "hand silhouette",
            "single finger pointing at interaction zone",
            "schematic touch indicator",
        ],
        "forbidden_subjects": [
            "human face",
            "human body",
            "portrait",
            "crowd",
            "lifestyle scene",
            "emotional gesture",
            "realistic hand photograph",
        ],
        "trigger_procedures_allowed": [
            "installation",
            "button-press",
            "fingerprint-enrolment",
            "pairing",
            "unlocking",
            "operation-guidance",
        ],
    },
    "mechanical-consistency": {
        "title": "Mechanical consistency policy",
        "intent": (
            "Every generated visual of a given product MUST preserve the same "
            "mechanical identity: bolt spacing, latch position, deadbolt geometry, "
            "mortise structure, sensor placement, keypad grid, handle proportions, "
            "camera-cluster layout and visible locking architecture. Tolerances are "
            "inherited from `PRODUCT_VISUAL_TRUTH.md`."
        ),
        "sources": [
            "KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md",
            "KNOWLEDGE_BUILDING/PRODUCT_NUCLEUS_RULES.md",
            "ext-images/<product>/visual-system/references/<product>-visual-profile.md",
            "ext-images/<product>/knowledge-core/component-visibility/component-visibility-map.json",
            "visual-system/shared/visual-rules/product-truth-policy.md",
        ],
        "immutable_attributes": [
            "silhouette",
            "component-count and component-positions",
            "sensor positions and count",
            "keypad grid (rows, columns, spacing)",
            "screen position / size / aspect",
            "indicator-LED positions",
            "handle geometry and mounting orientation",
            "visible mounting hardware (screws, bezels, gaskets)",
            "material identity per visible region",
            "brand marks, logos, certifications visible in canonical PNG",
        ],
        "tolerances": {
            "position_drift_px_at_1024_ref": 4,
            "rotation_drift_deg": 1,
            "scale_drift_pct": 1,
            "material_region_drift_px": 0,
        },
    },
    "truth-source": {
        "title": "Truth-source PNG policy",
        "intent": (
            "The single canonical PNG at `ext-images/<slug>/source-of-truth/"
            "product-images/<Product>.png` is the absolute visual source of truth. "
            "Every generated visual must extend / infer / contextualise / "
            "operationalise this PNG. Generation must NEVER redesign hardware, "
            "change geometry, invent components, relocate sensors, modify "
            "proportions or hallucinate mechanical systems."
        ),
        "sources": [
            "KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md",
            "KNOWLEDGE_BUILDING/PHASE_1_IMPLEMENTATION.md",
            "KNOWLEDGE_BUILDING/KNOWLEDGE_CORE_PRINCIPLES.md",
            "visual-system/shared/visual-rules/product-truth-policy.md",
        ],
        "fallback_surfaces_use_canonical_png": [
            "hero / primary product imagery (web, PDF, support)",
            "catalog imagery used for purchase decisions",
            "specification-sheet imagery",
            "imagery cited as 'product image' in delivery contracts",
            "imagery rendered next to legal text, certifications, warranty",
            "imagery accompanying technical specifications",
            "onboarding imagery used for product identification",
        ],
        "fallback_rule": (
            "If visual QA cannot certify a generated/composited output meets "
            "tolerance checks, the canonical PNG is used directly. There is no "
            "degraded-quality fallback chain."
        ),
    },
    "rendering-constraints": {
        "title": "Rendering constraints",
        "intent": (
            "One hardware side per image (exterior, interior or edge). No mixed-side "
            "frames. App UI must use real captures or low-detail generated screens "
            "only — never invented labels or menu hierarchies. Generated text/numbers "
            "are not trustworthy and must not be cited as instructional proof."
        ),
        "sources": [
            "visual-system/shared/visual-rules/manual-image-reset-policy.md",
            "visual-system/shared/visual-rules/app-ui-policy.md",
            "visual-system/shared/visual-rules/ai-limitations.md",
            "visual-system/shared/generation-guides/review-checklist.md",
        ],
        "constraints": [
            "one-side-per-image (exterior | interior | edge)",
            "no mixed interior+exterior frame",
            "no generated readable text used as instruction",
            "no invented app-UI labels or menu hierarchies",
            "low-detail phone renders only when phone is contextual, not source-of-truth",
            "schematic fallback for wiring / installation / anatomy / reset",
            "background quiet, diagram-like or lightly contextual",
            "callouts/labels added in editorial composition, not baked into render",
        ],
    },
    "comfy-contracts": {
        "title": "ComfyUI contracts (only authorised renderer)",
        "intent": (
            "ComfyUI is the SOLE authorised visual orchestration engine. Every "
            "approved visual must be produced through a registered, hashed, "
            "approved ComfyUI workflow conditioned on the canonical PNG. No other "
            "generation engine, web UI, ad-hoc API call or one-off script may "
            "produce visuals promoted into a product nucleus."
        ),
        "sources": [
            "KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md",
            "_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md",
            "tools/comfy/workflow_api.json.json",
            "tools/visual_generation.py",
            "ext-images/<product>/automation/orchestrators/orchestration-manifest.json",
        ],
        "registry_requirements": [
            "stable workflow id + semver",
            "content-hash of the JSON",
            "explicit reviewer + approval timestamp",
            "purpose / inputs / outputs / required-conditioning / known-limitations",
            "anonymous or unregistered workflows MUST NOT run against canonical PNGs",
            "a workflow change is a NEW VERSION, not an in-place mutation",
        ],
        "run_record_required_fields": [
            "product slug",
            "canonical PNG path + hash",
            "workflow id + version + content hash",
            "prompt contract id",
            "seed",
            "sampler / steps / CFG / scheduler / model name + hash",
            "ControlNet / IPAdapter inputs (paths + hashes)",
            "output paths",
            "approval state / reviewer / timestamp",
        ],
        "conditioning_rules": [
            "all identity-affecting generation must be conditioned on the canonical PNG or its derivatives",
            "ControlNet preprocessors apply only to the canonical PNG or its component cutouts",
            "IPAdapter references limited to canonical PNG, OEM evidence in source-of-truth/visual-evidence/, or approved support visuals from the SAME product",
            "cross-product IPAdapter references are FORBIDDEN",
            "cross-product prompt copy-paste is FORBIDDEN",
        ],
        "authoritative_tooling": {
            "runner": "tools/visual_generation.py",
            "baseline_workflow": "tools/comfy/workflow_api.json.json (filename normalisation pending)",
            "per_product_orchestration_manifest": "ext-images/<slug>/automation/orchestrators/orchestration-manifest.json",
        },
    },
    "negative-prompts": {
        "title": "Consolidated negative-prompt registry",
        "intent": (
            "All future negative prompts MUST resolve to component IDs in this "
            "registry. Inline, ad-hoc negative strings duplicated across product "
            "ai-image-prompts.md files are deprecated and will be migrated."
        ),
        "sources": [
            "ext-images/<product>/visual-system/prompts/ai-image-prompts.md (all 6 products)",
            "KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md (§4 prompt lineage)",
        ],
        "components": {
            "neg.shared.anti-marketing": [
                "marketing glamor",
                "cinematic drama",
                "photorealistic lifestyle staging",
                "neon lighting",
                "plastic render look",
                "low resolution",
            ],
            "neg.shared.anti-human": [
                "full human figure",
                "human face",
                "body-led scene",
                "photorealistic people",
                "realistic hand photo",
                "extra fingers",
            ],
            "neg.shared.anti-text": [
                "invented UI text",
                "fake labels",
                "fake readable app UI",
            ],
            "neg.shared.anti-geometry": [
                "wrong geometry",
                "mixed interior and exterior hardware in one frame",
                "wrong lock-edge mechanism",
                "floating objects",
                "cluttered background",
            ],
            "neg.shared.anti-generic-lock": [
                "standard keypad lever lock silhouette",
                "knob lock silhouette",
                "fingerprint sensor on the front panel",
                "missing upper sensor cluster",
                "merged display and handle",
                "missing interior screen",
                "rim-lock box geometry",
            ],
        },
        "per_product_negatives_pointer": (
            "Product-specific additions remain in "
            "ext-images/<product>/visual-system/prompts/ai-image-prompts.md and "
            "must declare the shared component IDs they extend."
        ),
        "anti_contamination_rule": (
            "neg.shared.anti-generic-lock currently appears verbatim in 6/6 "
            "products despite different geometries. Future migration: each product "
            "must declare which sub-bullets apply and add product-specific "
            "negatives under neg.<product>.* component IDs."
        ),
    },
    "visual-risk": {
        "title": "Visual risk model",
        "intent": (
            "Every visual artefact is classified by the consequence of getting it "
            "wrong: visuals that affect installation, operation, troubleshooting, "
            "pairing, safety or locking behaviour are HIGH visual risk. Risk drives "
            "stricter constraints, lower inference tolerance, stronger provenance "
            "grounding, and higher semantic validation."
        ),
        "sources": [
            "ext-images/<product>/knowledge-core/visual-risk/risk-*.json (all 6 products)",
            "ext-images/<product>/knowledge-core/visual-intent/intent-*.json",
            "KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md",
        ],
        "severity_levels": {
            "critical": "hallucinated sensor; wrong keypad layout; geometry that misleads at unboxing or first install",
            "high":     "missing mechanical key; misplaced fingerprint zone; incorrect handle direction",
            "medium":   "wrong camera position; fake emergency port; wrong indicator placement",
            "low":      "non-critical visibility issues that do not affect identification or operation",
        },
        "user_risk_levels": ["low", "medium", "high", "critical"],
        "visual_assistance_priorities": ["P1 critical-path", "P2 support", "P3 editorial"],
        "mitigation_template": (
            "ComfyUI workflow MUST anchor the listed trigger_components against "
            "the OEM PNG references and refuse to render the asset if anchors are "
            "missing."
        ),
    },
    "visual-validation": {
        "title": "Visual validation contracts",
        "intent": (
            "Every approved visual must pass (a) the shared review checklist, (b) "
            "per-product visual-validation.md passes, and (c) automated tolerance "
            "checks against the component-visibility-map of its product. Validation "
            "is mandatory before promotion to any product nucleus."
        ),
        "sources": [
            "visual-system/shared/generation-guides/review-checklist.md",
            "ext-images/<product>/visual-system/validations/visual-validation.md",
            "ext-images/<product>/knowledge-core/component-visibility/component-visibility-map.json",
            "tools/visual_generation.py (score subcommand)",
        ],
        "manual_pass_conditions": [
            "product unmistakably identified",
            "protected geometry matches visual-profile.md",
            "exactly one hardware side shown",
            "schematic or hybrid class",
            "no full human figure / face",
            "no generated technical text used as proof",
        ],
        "automated_checks_today": [
            "aspect-ratio mismatch",
            "undersized output",
            "low edge energy",
            "low contrast",
            "too dark / too bright",
            "SHA-256 duplication detection",
        ],
        "automated_checks_required_next": [
            "silhouette tolerance vs canonical PNG (≤2 px on 1024-ref)",
            "component-position tolerance per component-visibility-map",
            "sensor-count validation",
            "keypad-grid validation",
            "handle-orientation check",
            "cross-product contamination scan",
        ],
        "qa_gate_states": ["pending", "approved", "rework", "reject", "blocked-pending-oem-validation"],
    },
    "visual-lineage": {
        "title": "Visual lineage / provenance",
        "intent": (
            "Visual lineage roots at the canonical PNG and flows through "
            "conditioning asset → ComfyUI workflow run → approved support visual → "
            "delivery placement. Run records are immutable and stored under "
            "`ext-images/<slug>/automation/runs/`. Delivery placements update the "
            "writeback trackers in `image-production-status.md` and "
            "`generated/selected-assets-register.md`."
        ),
        "sources": [
            "KNOWLEDGE_BUILDING/PROVENANCE_AND_LINEAGE.md",
            "KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md (§3 reproducibility, §7 storage)",
            "_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md",
            "ext-images/<product>/automation/runs/",
        ],
        "lineage_chain": [
            "canonical PNG",
            "conditioning asset (cutout / mask / depth / normal / line-art / IPAdapter ref)",
            "approved ComfyUI workflow (registry id + semver + content hash)",
            "run record (immutable, ext-images/<slug>/automation/runs/)",
            "approved support visual (with reviewer + timestamp)",
            "delivery placement (writeback to image-production-status / selected-assets-register)",
        ],
        "immutability_rules": [
            "no edits after approval; new findings require a new run record",
            "missing run record == not approved; cannot be promoted",
            "delivery placement must reference the run-record id",
        ],
    },
    "publication-constraints": {
        "title": "Publication-channel constraints (DRAFT — gap)",
        "intent": (
            "Per-channel publication constraints (resolution, aspect, color space, "
            "format, file-size, alt-text schema) are NOT yet defined. Today the "
            "channel targets are declared in publication-intent-map.json per "
            "product but the per-channel delivery spec is absent. This policy file "
            "is a placeholder marking the gap; it must be populated before mass "
            "Comfy orchestration begins."
        ),
        "sources": [
            "ext-images/<product>/knowledge-core/publication-intent/publication-intent-map.json",
            "tools/visual_generation.py (FORMAT_DIMENSIONS hardcoded)",
            "visual-system/shared/visual-rules/app-ui-policy.md",
        ],
        "channels": ["web", "pdf", "support", "onboarding", "chatbot", "rag", "api"],
        "format_dimensions_today": {
            "16:9": [1536, 864],
            "4:3":  [1408, 1056],
            "4:5":  [1024, 1280],
            "1:1":  [1024, 1024],
        },
        "open_questions": [
            "color space and bit depth per channel",
            "file format + compression per channel",
            "required alt-text schema per channel",
            "load-time / bandwidth caps per channel",
            "dimension validation hook in visual_generation.py",
        ],
    },
}

# Fragments grouped per the discovery report (Section A summary).
DISCOVERED_FRAGMENT_INDEX = [
    {"path": "wp-content/themes/beslock-custom/User manuals/_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md", "domains": ["comfy-contracts", "rendering-constraints", "publication-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md", "domains": ["comfy-contracts", "negative-prompts", "visual-risk", "visual-validation", "visual-lineage", "mechanical-consistency", "truth-source"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md", "domains": ["truth-source", "mechanical-consistency", "human-interaction-policy", "rendering-constraints", "visual-validation"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PRODUCT_NUCLEUS_RULES.md", "domains": ["mechanical-consistency", "truth-source", "visual-lineage"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PROVENANCE_AND_LINEAGE.md", "domains": ["visual-lineage", "publication-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_CORE_PRINCIPLES.md", "domains": ["truth-source", "visual-lineage", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_SCHEMA.md", "domains": ["visual-validation"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PHASE_1_IMPLEMENTATION.md", "domains": ["truth-source", "mechanical-consistency", "visual-lineage"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/README.md", "domains": ["visual-style-policy", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/generation-guides/review-checklist.md", "domains": ["visual-validation", "human-interaction-policy", "mechanical-consistency"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/visual-rules/manual-image-reset-policy.md", "domains": ["visual-style-policy", "human-interaction-policy", "mechanical-consistency", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/visual-rules/product-truth-policy.md", "domains": ["truth-source", "mechanical-consistency"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/visual-rules/realism-vs-schematic.md", "domains": ["visual-style-policy", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/visual-rules/ai-limitations.md", "domains": ["visual-risk", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "wp-content/themes/beslock-custom/User manuals/visual-system/shared/visual-rules/app-ui-policy.md", "domains": ["rendering-constraints", "publication-constraints"], "scope": "repo-wide"},
    {"path": "tools/visual_generation.py", "domains": ["comfy-contracts", "rendering-constraints"], "scope": "repo-wide"},
    {"path": "tools/comfy/workflow_api.json.json", "domains": ["comfy-contracts"], "scope": "repo-wide"},
]
for prod in PRODUCTS:
    base = f"wp-content/themes/beslock-custom/User manuals/ext-images/{prod}"
    DISCOVERED_FRAGMENT_INDEX += [
        {"path": f"{base}/visual-system/prompts/ai-image-prompts.md", "domains": ["negative-prompts", "mechanical-consistency", "human-interaction-policy"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/visual-system/generation-matrices/image-generation-matrix.md", "domains": ["visual-validation", "mechanical-consistency"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/visual-system/references/{prod}-visual-profile.md", "domains": ["mechanical-consistency", "truth-source"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/visual-system/validations/visual-validation.md", "domains": ["visual-validation", "mechanical-consistency"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/knowledge-core/visual-intent/", "domains": ["visual-validation", "publication-constraints"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/knowledge-core/visual-risk/", "domains": ["visual-risk"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/knowledge-core/component-visibility/component-visibility-map.json", "domains": ["mechanical-consistency", "visual-validation"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/knowledge-core/publication-intent/publication-intent-map.json", "domains": ["publication-constraints"], "scope": f"per-product:{prod}"},
        {"path": f"{base}/knowledge-core/procedural-semantics/", "domains": ["visual-validation"], "scope": f"per-product:{prod}"},
    ]


CONFLICTS = [
    {
        "id": "conflict.negative-prompts.cross-product-duplication",
        "summary": "neg.shared.anti-generic-lock is duplicated VERBATIM in all 6 product ai-image-prompts.md files despite different product geometries.",
        "affected_paths": [f"wp-content/themes/beslock-custom/User manuals/ext-images/{p}/visual-system/prompts/ai-image-prompts.md" for p in PRODUCTS],
        "policy_pointer": "_governance/negative-prompts/registry.json#components.neg.shared.anti-generic-lock",
        "resolution_recommended": "Each product must declare which sub-bullets apply and add product-specific negatives under neg.<product>.* component IDs. NOT performed in this phase.",
    },
    {
        "id": "conflict.image-class.assignment-implicit",
        "summary": "schematic vs hybrid assignment per slot is documented in per-product matrices but not exposed in the orchestration manifest export contract; downstream readers cannot tell why a class was chosen.",
        "affected_paths": [
            "tools/visual_generation.py",
            "_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md",
        ],
        "policy_pointer": "_governance/visual-style-policy/policy.md#class-assignment",
        "resolution_recommended": "Add `image_class` and `class_rationale` fields to the per-slot manifest export. NOT performed in this phase.",
    },
    {
        "id": "conflict.blocked-slots.no-status-enum",
        "summary": "IMG-012 is 'blocked-pending-OEM-validation' across e-orbit and e-shield matrices but no explicit status enum exists in the run-record / manifest schema.",
        "affected_paths": [
            "wp-content/themes/beslock-custom/User manuals/ext-images/e-orbit/visual-system/generation-matrices/image-generation-matrix.md",
            "wp-content/themes/beslock-custom/User manuals/ext-images/e-shield/visual-system/generation-matrices/image-generation-matrix.md",
        ],
        "policy_pointer": "_governance/visual-validation/policy.md#qa_gate_states",
        "resolution_recommended": "Add `blocked-pending-oem-validation` to the QA gate states enum (already present in this policy). Manifest exporter NOT updated in this phase.",
    },
    {
        "id": "conflict.composite-vs-generate.unspecified-per-slot",
        "summary": "PRODUCT_VISUAL_TRUTH.md §13 prefers compositing over generation for hero/multi-view scenarios; per-slot generation matrices do not declare `transformation_type`.",
        "affected_paths": [f"wp-content/themes/beslock-custom/User manuals/ext-images/{p}/visual-system/generation-matrices/image-generation-matrix.md" for p in PRODUCTS],
        "policy_pointer": "_governance/comfy-contracts/policy.md#run_record_required_fields",
        "resolution_recommended": "Add `transformation_type: generate|composite` to per-slot manifest. NOT performed in this phase.",
    },
    {
        "id": "conflict.workflow-filename.double-extension",
        "summary": "tools/comfy/workflow_api.json.json has a known double-extension filename; documented as historical artifact in COMFY_GENERATION_GOVERNANCE.md §2.",
        "affected_paths": ["tools/comfy/workflow_api.json.json"],
        "policy_pointer": "_governance/comfy-contracts/policy.md#authoritative_tooling",
        "resolution_recommended": "Normalise in the workflow registry on first registry creation. NOT performed in this phase.",
    },
    {
        "id": "conflict.legacy-png.no-decommission-timeline",
        "summary": "Compatibility PNGs at ext-images/ root (e-Flex.png, e-Nova.png, …) are 'scheduled for retirement' per multiple docs but no decommission timeline or check exists.",
        "affected_paths": ["wp-content/themes/beslock-custom/User manuals/ext-images/*.png"],
        "policy_pointer": "_governance/truth-source/policy.md#fallback_surfaces_use_canonical_png",
        "resolution_recommended": "Add automated check in repository_governance_audit.py classifying root-level legacy PNGs as decommission-pending. NOT performed in this phase.",
    },
]


GAPS = [
    {"id": "gap.negatives.component-registry-implementation", "domain": "negative-prompts", "summary": "Negative-prompt component registry is declared in this policy but NOT yet wired into product prompts or the manifest exporter."},
    {"id": "gap.comfy.model-and-sampler-approval", "domain": "comfy-contracts", "summary": "No registry of approved AI models, samplers, schedulers, CFG ranges, step counts."},
    {"id": "gap.qa.automated-tolerance-checks", "domain": "visual-validation", "summary": "Silhouette / component-position / sensor-count / keypad-grid / handle-orientation checks not implemented; only narrow heuristics in visual_generation.py score."},
    {"id": "gap.publication.per-channel-spec", "domain": "publication-constraints", "summary": "Per-channel resolution / colour-space / format / alt-text schema undefined; FORMAT_DIMENSIONS hardcoded in visual_generation.py."},
    {"id": "gap.mechanical.anchor-map-tooling", "domain": "mechanical-consistency", "summary": "component-visibility-map.json exists but no formal schema for derivation, refresh, or comparison tooling."},
    {"id": "gap.rendering.edge-case-geometries", "domain": "rendering-constraints", "summary": "Variant-PNG handling (handed variants, procedure-specific exposed mechanics, transparent-panel reveals) is not documented."},
    {"id": "gap.prompts.canonical-terminology-glossary", "domain": "negative-prompts", "summary": "Colombian-Spanish lock-component glossary is implied but not centralised; cross-language prompt rules undefined."},
    {"id": "gap.lineage.run-record-schema", "domain": "visual-lineage", "summary": "Run-record JSON schema is described prosaically; no formal schema file or compliance checker."},
    {"id": "gap.rag.visual-grounding-rules", "domain": "visual-validation", "summary": "RAG/chatbot trustworthiness scoring of visual artefacts undefined."},
    {"id": "gap.qa.cross-product-contamination-scanner", "domain": "visual-validation", "summary": "Cross-product geometry leakage detection is a documented risk but has no automated scanner."},
]


# ---------------------------------------------------------------------------
# Build canonical policy files
# ---------------------------------------------------------------------------
def write_policy(domain: str, payload: dict) -> tuple[Path, Path]:
    folder = GOV_VS / domain
    folder.mkdir(parents=True, exist_ok=True)
    policy_md = folder / "policy.md"
    sources_json = folder / "sources.json"
    lines = [
        f"# {payload['title']}",
        "",
        f"_Schema: `{SCHEMA}` · canonical policy · generated {NOW}._",
        "",
        "## Intent",
        "",
        payload["intent"],
        "",
        "## Authoritative source documents",
        "",
        "This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.",
        "",
    ]
    for s in payload.get("sources", []):
        lines.append(f"- `{s}`")
    # Domain-specific bullets
    for key, val in payload.items():
        if key in ("title", "intent", "sources"):
            continue
        lines += ["", f"## {key.replace('_', ' ').title()}", ""]
        if isinstance(val, list):
            for item in val:
                lines.append(f"- {item}")
        elif isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, list):
                    lines.append(f"- **{k}**:")
                    for item in v:
                        lines.append(f"  - {item}")
                else:
                    lines.append(f"- **{k}**: {v}")
        else:
            lines.append(str(val))
    policy_md.write_text("\n".join(lines) + "\n")
    sources_json.write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "domain": domain,
                "title": payload["title"],
                "generated_at": NOW,
                "sources": payload.get("sources", []),
                "consolidates": "All listed source documents are preserved. This file lists ownership, not content.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return policy_md, sources_json


def main() -> int:
    GOV_VS.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for domain, payload in DOMAIN_FRAGMENTS.items():
        md, sj = write_policy(domain, payload)
        written.append(md.relative_to(REPO).as_posix())
        written.append(sj.relative_to(REPO).as_posix())

    # Index README
    index_lines = [
        "# Canonical visual governance",
        "",
        f"_Schema: `{SCHEMA}` · generated {NOW} by `tools/visual_governance_consolidate.py`._",
        "",
        "This folder is the SINGLE CANONICAL ROOT for visual-generation governance. Each subfolder owns one policy domain. Every policy file is a CONSOLIDATION POINTER: the underlying rules live in the source documents listed in each `sources.json`.",
        "",
        "## Domains",
        "",
    ]
    for domain, payload in DOMAIN_FRAGMENTS.items():
        index_lines.append(f"- [`{domain}/policy.md`]({domain}/policy.md) — {payload['title']}")
    index_lines += [
        "",
        "## Hard guarantees of this consolidation",
        "",
        "- No source document was moved, copied, or rewritten.",
        "- No prompt, manifest, or run record was modified.",
        "- No image was generated.",
        "- No ComfyUI workflow was altered.",
        "- Conflicts are reported in `_repository-governance/reports/visual-governance/`, never silently resolved.",
        "",
        "## Reports",
        "",
        "- `_repository-governance/reports/visual-governance/01-discovered-artifacts.json`",
        "- `_repository-governance/reports/visual-governance/02-consolidated-governance-map.json`",
        "- `_repository-governance/reports/visual-governance/03-duplications-and-conflicts.json`",
        "- `_repository-governance/reports/visual-governance/04-canonical-governance-structure.json`",
        "- `_repository-governance/reports/visual-governance/05-new-governance-structure.json`",
        "- `_repository-governance/reports/visual-governance/06-visual-policy-summary.json`",
        "- `_repository-governance/reports/visual-governance/07-mechanical-consistency-summary.json`",
        "- `_repository-governance/reports/visual-governance/08-human-representation-summary.json`",
        "- `_repository-governance/reports/visual-governance/09-visual-risk-model-summary.json`",
        "- `_repository-governance/reports/visual-governance/10-comfy-orchestration-readiness.json`",
        "- `_repository-governance/reports/visual-governance/11-future-validation-opportunities.json`",
        "- `_repository-governance/reports/visual-governance/12-unresolved-governance-gaps.json`",
    ]
    (GOV_VS / "README.md").write_text("\n".join(index_lines) + "\n")
    written.append((GOV_VS / "README.md").relative_to(REPO).as_posix())

    # ----- Reports -----
    rep_dir = GOV_REPO / "reports" / "visual-governance"
    rep_dir.mkdir(parents=True, exist_ok=True)

    def write(path_name: str, payload: dict):
        (rep_dir / path_name).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    # 1
    write("01-discovered-artifacts.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "fragment_count": len(DISCOVERED_FRAGMENT_INDEX),
        "fragments": DISCOVERED_FRAGMENT_INDEX,
    })

    # 2 — consolidated map (domain → fragments)
    domain_to_frags: dict[str, list[str]] = {}
    for frag in DISCOVERED_FRAGMENT_INDEX:
        for d in frag["domains"]:
            domain_to_frags.setdefault(d, []).append(frag["path"])
    write("02-consolidated-governance-map.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "policy": "Each domain owns ONE canonical pointer at visual-system/_governance/<domain>/policy.md. Source fragments listed below remain authoritative for their content.",
        "domain_to_sources": {k: sorted(set(v)) for k, v in domain_to_frags.items()},
    })

    # 3 — duplications and conflicts
    write("03-duplications-and-conflicts.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "policy": "Conflicts reported, never silently resolved. Each entry carries a recommended resolution that is NOT executed in this phase.",
        "count": len(CONFLICTS),
        "conflicts": CONFLICTS,
    })

    # 4 — canonical governance structure
    write("04-canonical-governance-structure.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "root": "wp-content/themes/beslock-custom/User manuals/visual-system/_governance/",
        "domains": list(DOMAIN_FRAGMENTS.keys()),
        "files_written": written,
        "principle": "SINGLE canonical visual governance root. No parallel standards.",
    })

    # 5 — new governance structure (what this phase introduces vs pre-existing)
    write("05-new-governance-structure.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "newly_introduced": {
            "directories": [f"visual-system/_governance/{d}/" for d in DOMAIN_FRAGMENTS],
            "files": written,
            "report_dir": "_repository-governance/reports/visual-governance/",
        },
        "preserved_unchanged": [f["path"] for f in DISCOVERED_FRAGMENT_INDEX],
        "modified_existing_files": [],
        "moved_existing_files": [],
        "deleted_existing_files": [],
    })

    # 6 — visual policy summary
    write("06-visual-policy-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "absolute_principle": "MAXIMUM OPERATIONAL CLARITY — NOT marketing aesthetics, NOT cinematic storytelling, NOT decorative AI art.",
        "allowed_classes": DOMAIN_FRAGMENTS["visual-style-policy"]["allowed_classes"],
        "legacy_only_classes": DOMAIN_FRAGMENTS["visual-style-policy"]["legacy_only_classes"],
        "forbidden": DOMAIN_FRAGMENTS["visual-style-policy"]["forbidden"],
        "rendering_constraints": DOMAIN_FRAGMENTS["rendering-constraints"]["constraints"],
        "canonical_policy": "visual-system/_governance/visual-style-policy/policy.md",
    })

    # 7 — mechanical consistency summary
    write("07-mechanical-consistency-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "immutable_attributes": DOMAIN_FRAGMENTS["mechanical-consistency"]["immutable_attributes"],
        "tolerances": DOMAIN_FRAGMENTS["mechanical-consistency"]["tolerances"],
        "per_product_anchor_maps_present": {p: True for p in PRODUCTS},
        "canonical_policy": "visual-system/_governance/mechanical-consistency/policy.md",
        "blockers": [
            "anchor-map derivation tooling missing (gap.mechanical.anchor-map-tooling)",
            "automated tolerance checker missing (gap.qa.automated-tolerance-checks)",
        ],
    })

    # 8 — human representation summary
    write("08-human-representation-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "rule": "No faces. No bodies. Hands ONLY when a procedure requires touch context.",
        "allowed_subjects": DOMAIN_FRAGMENTS["human-interaction-policy"]["allowed_subjects"],
        "forbidden_subjects": DOMAIN_FRAGMENTS["human-interaction-policy"]["forbidden_subjects"],
        "trigger_procedures_allowed": DOMAIN_FRAGMENTS["human-interaction-policy"]["trigger_procedures_allowed"],
        "canonical_policy": "visual-system/_governance/human-interaction-policy/policy.md",
    })

    # 9 — visual risk model summary
    write("09-visual-risk-model-summary.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "severity_levels": DOMAIN_FRAGMENTS["visual-risk"]["severity_levels"],
        "user_risk_levels": DOMAIN_FRAGMENTS["visual-risk"]["user_risk_levels"],
        "visual_assistance_priorities": DOMAIN_FRAGMENTS["visual-risk"]["visual_assistance_priorities"],
        "mitigation_template": DOMAIN_FRAGMENTS["visual-risk"]["mitigation_template"],
        "canonical_policy": "visual-system/_governance/visual-risk/policy.md",
    })

    # 10 — Comfy orchestration readiness
    write("10-comfy-orchestration-readiness.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "ready_today": [
            "ComfyUI declared the only authorised renderer (COMFY_GENERATION_GOVERNANCE.md §1)",
            "Per-product orchestration manifest contract (visual_generation.py + VISUAL_GENERATION_AUTOMATION.md)",
            "Run-record fields enumerated (canonical PNG hash, workflow id+version+hash, prompt, seed, model, ControlNet/IPAdapter inputs)",
            "Conditioning policy: canonical-PNG-only or its derivatives",
            "Per-product visual-intent + visual-risk + component-visibility + publication-intent JSONs in place (5/6 products Comfy-ready from Phase 3; e-nova still blocked by zero procedural-semantics)",
        ],
        "blockers_before_mass_orchestration": [
            "tools/comfy/workflow_api.json.json filename normalisation + workflow registry creation",
            "negative-prompt component registry must be wired into per-product prompts",
            "model + sampler approval registry missing (gap.comfy.model-and-sampler-approval)",
            "automated tolerance + cross-product-contamination QA missing (gap.qa.*)",
            "per-channel publication spec missing (gap.publication.per-channel-spec)",
            "e-nova procedural-semantics gap from Phase 3",
        ],
        "canonical_policy": "visual-system/_governance/comfy-contracts/policy.md",
    })

    # 11 — future validation opportunities
    write("11-future-validation-opportunities.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "opportunities": [
            {"id": "val.silhouette-tolerance", "summary": "Silhouette comparison vs canonical PNG with ≤2 px tolerance on 1024-ref."},
            {"id": "val.component-anchor-tolerance", "summary": "Per-component position tolerance check using component-visibility-map.json (≤4 px)."},
            {"id": "val.sensor-count", "summary": "Detected sensor count must equal anchor map sensor count."},
            {"id": "val.keypad-grid", "summary": "Keypad row/column inference must match anchor map."},
            {"id": "val.handle-orientation", "summary": "Handle orientation classifier (left/right/none) vs anchor map."},
            {"id": "val.cross-product-contamination", "summary": "Reject if foreign-product geometry (e.g., e-shield rim-lock box in an e-orbit run) is detected."},
            {"id": "val.text-presence", "summary": "Reject any candidate containing legible text other than approved logos/marks."},
            {"id": "val.human-presence", "summary": "Reject any candidate containing a face or full human figure."},
            {"id": "val.publication-format", "summary": "Per-channel resolution/aspect/format/alt-text validation hook."},
            {"id": "val.run-record-compliance", "summary": "Promotion-time check that every approved visual has a complete run record."},
        ],
    })

    # 12 — unresolved governance gaps
    write("12-unresolved-governance-gaps.json", {
        "schema_version": SCHEMA,
        "generated_at": NOW,
        "policy": "These gaps are NOT resolved by this phase. Each is recorded so the next governance pass (or a dedicated implementation phase) can pick them up explicitly.",
        "count": len(GAPS),
        "gaps": GAPS,
    })

    print(f"Visual governance consolidation complete.")
    print(f"  Canonical root: {GOV_VS.relative_to(REPO).as_posix()}")
    print(f"  Domains: {len(DOMAIN_FRAGMENTS)}")
    print(f"  Discovered fragments: {len(DISCOVERED_FRAGMENT_INDEX)}")
    print(f"  Conflicts reported: {len(CONFLICTS)}")
    print(f"  Gaps reported: {len(GAPS)}")
    print(f"  Reports: {rep_dir.relative_to(REPO).as_posix()}/01..12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
