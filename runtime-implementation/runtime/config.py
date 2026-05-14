"""Runtime configuration — paths, declared products, slice declaration.

All paths anchor relative to the repository root. Read-only by construction.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
KNOWLEDGE_CORE_ROOT = THEME_ROOT / "ext-images"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# Declared knowledge-core domains the runtime is permitted to read.
ALLOWED_DOMAINS = (
    "operation",
    "install",
    "workflows",
    "procedural-semantics",
    "warnings",
    "warnings/supplemental-candidates",
    "warnings-expanded",
    "troubleshooting",
    "troubleshooting-expanded",
    "continuity-checkpoints",
    "causal-graphs",
    "confidence-tiers",
    "specifications",
    "capabilities",
    "terminology",
    "entities",
)

# Confidence tier weights used for retrieval ranking. Mirrors the per-product
# `confidence-tiers/confidence-tier-manifest-<product>.json` defaults but is
# applied as a runtime fallback when the per-product manifest is absent.
CONFIDENCE_WEIGHTS = {
    "verified-oem":         1.0,
    "verified-internal":    0.95,
    "high":                 0.90,
    "ocr-derived":          0.85,
    "medium":               0.75,
    "inferred-operational": 0.65,
    "low":                  0.50,
    "candidate":            0.40,
    "unresolved":           0.10,
    "unknown":              0.50,
}

# First slice declared by Phases 24 + 25.
FIRST_SLICE = "contextual-onboarding+troubleshooting-retrieval"

# Hard exclusions enforced at runtime boundary.
HARD_EXCLUSIONS = (
    "no-autonomous-agents",
    "no-production-deployment",
    "no-image-generation",
    "no-pdf-generation",
    "no-large-frontend",
    "no-perf-optimization",
)

# Observability log directory (append-only).
LOG_DIR = REPO_ROOT / "runtime-implementation" / "observability" / "logs"


def product_knowledge_root(product: str) -> Path:
    if product not in PRODUCTS:
        raise ValueError(f"unknown product: {product}")
    return KNOWLEDGE_CORE_ROOT / product / "knowledge-core"


def assert_in_scope(path: Path) -> None:
    """Refuse any path that is not under a declared knowledge-core domain."""
    resolved = path.resolve()
    if KNOWLEDGE_CORE_ROOT not in resolved.parents and resolved != KNOWLEDGE_CORE_ROOT:
        raise PermissionError(f"out-of-scope read attempt: {path}")
