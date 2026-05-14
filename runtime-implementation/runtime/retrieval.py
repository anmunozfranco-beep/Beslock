"""Knowledge-core retrieval — read-only, scored, provenance-attached.

Supports the six declared retrieval kinds:
  operational-procedures, troubleshooting, warnings, onboarding, escalation, adaptive-guidance.

Scoring is intentionally simple (token overlap with diacritic + lowercase
normalization). No ML, no network, no caching layer. Determinism > recall.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from . import config, provenance

# Map retrieval kinds to allowed knowledge-core domains.
KIND_DOMAINS: dict[str, tuple[str, ...]] = {
    "onboarding":               ("operation", "workflows", "procedural-semantics", "install"),
    "troubleshooting":          ("troubleshooting", "troubleshooting-expanded",
                                 "warnings", "warnings-expanded",
                                 "warnings/supplemental-candidates", "causal-graphs"),
    "operational-procedures":   ("operation", "workflows", "procedural-semantics", "install"),
    "warnings":                 ("warnings", "warnings-expanded",
                                 "warnings/supplemental-candidates"),
    "escalation":               ("workflows", "warnings", "warnings-expanded",
                                 "warnings/supplemental-candidates"),
    "adaptive-guidance":        ("operation", "procedural-semantics"),
    "fingerprint-enrollment":   ("operation", "workflows", "procedural-semantics"),
    "pairing":                  ("operation", "workflows", "procedural-semantics"),
    "battery-recovery":         ("operation", "workflows", "warnings", "warnings-expanded",
                                 "troubleshooting", "troubleshooting-expanded",
                                 "continuity-checkpoints"),
    "continuity":               ("continuity-checkpoints",),
    "causal":                   ("causal-graphs",),
}


@dataclass
class RetrievedNode:
    id: str
    type: str
    product: str
    summary: str
    confidence: str
    validation_status: str
    score: float
    path: Path
    raw: dict = field(repr=False)


@dataclass
class RetrievalPackage:
    package_id: str
    run_id: str
    slice_id: str
    query: str
    kind: str
    product: str
    nodes: list[RetrievedNode]
    manifest: dict
    ambiguous: bool
    no_results: bool


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _normalize(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _tokens(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(_normalize(text)))


def _score_node(query_tokens: set[str], node_tokens: set[str]) -> float:
    if not query_tokens or not node_tokens:
        return 0.0
    overlap = query_tokens & node_tokens
    if not overlap:
        return 0.0
    # Jaccard over query tokens (recall-leaning).
    return round(len(overlap) / len(query_tokens), 4)


def _iter_domain_files(product: str, domains: Iterable[str]) -> Iterable[Path]:
    root = config.product_knowledge_root(product)
    if not root.exists():
        return
    for domain in domains:
        domain_root = root / domain
        if not domain_root.exists() or not domain_root.is_dir():
            continue
        for path in sorted(domain_root.glob("*.json")):
            config.assert_in_scope(path)
            yield path


def _load_node(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _node_text(node: dict, path: Path) -> str:
    parts = [
        node.get("id", ""),
        node.get("summary", ""),
        node.get("type", ""),
        path.stem.replace("-", " "),
    ]
    for step in node.get("steps", []) or []:
        if isinstance(step, dict):
            parts.append(step.get("text", "") or step.get("summary", ""))
        elif isinstance(step, str):
            parts.append(step)
    for pre in node.get("preconditions", []) or []:
        if isinstance(pre, dict):
            parts.append(pre.get("text", ""))
        elif isinstance(pre, str):
            parts.append(pre)
    return " ".join(p for p in parts if p)


def retrieve(
    *,
    run_id: str,
    slice_id: str,
    product: str,
    query: str,
    kind: str,
    top_k: int = 5,
) -> RetrievalPackage:
    """Execute a read-only retrieval over knowledge-core.

    Returns a RetrievalPackage carrying nodes + a provenance manifest.
    Ambiguity is surfaced (not silently resolved) when top results tie.
    """
    if kind not in KIND_DOMAINS:
        raise ValueError(f"unknown retrieval kind: {kind}")
    if product not in config.PRODUCTS:
        raise ValueError(f"unknown product: {product}")

    qtokens = _tokens(query)
    candidates: list[RetrievedNode] = []
    for path in _iter_domain_files(product, KIND_DOMAINS[kind]):
        node = _load_node(path)
        if not node:
            continue
        ntokens = _tokens(_node_text(node, path))
        token_score = _score_node(qtokens, ntokens)
        if token_score <= 0:
            continue
        confidence = node.get("confidence", "unknown")
        weight = config.CONFIDENCE_WEIGHTS.get(confidence, 0.5)
        score = round(token_score * weight, 4)
        if score <= 0:
            continue
        candidates.append(
            RetrievedNode(
                id=node.get("id", path.stem),
                type=node.get("type", "unknown"),
                product=node.get("product", product),
                summary=(node.get("summary") or "").strip(),
                confidence=confidence,
                validation_status=node.get("validation_status", "unknown"),
                score=score,
                path=path,
                raw=node,
            )
        )

    candidates.sort(key=lambda n: (-n.score, n.id))
    top = candidates[:top_k]

    # Ambiguity: tied top scores AND none of the tied candidates are verified.
    if len(top) >= 2 and top[0].score == top[1].score:
        verified_at_top = any(n.confidence in {"verified-oem", "verified-internal", "high"}
                              for n in top if n.score == top[0].score)
        ambiguous = not verified_at_top
    else:
        ambiguous = False

    # Candidate-only retrieval is itself a soft escalation signal.
    candidate_only = bool(top) and all(n.confidence in {"candidate", "unresolved"} for n in top)

    manifest = provenance.build_manifest(
        run_id=run_id,
        slice_id=slice_id,
        package_kind="retrieval-package",
        source_files=[n.path for n in top],
        source_node_ids=[n.id for n in top],
        extra={"query": query, "kind": kind, "product": product, "top_k": top_k,
               "ambiguous": ambiguous, "candidate_only": candidate_only,
               "candidate_count": len(candidates)},
    )

    return RetrievalPackage(
        package_id=provenance.new_id("retr"),
        run_id=run_id,
        slice_id=slice_id,
        query=query,
        kind=kind,
        product=product,
        nodes=top,
        manifest=manifest,
        ambiguous=ambiguous,
        no_results=not top,
    )


def package_to_dict(pkg: RetrievalPackage) -> dict:
    return {
        "package_id": pkg.package_id,
        "run_id": pkg.run_id,
        "slice_id": pkg.slice_id,
        "query": pkg.query,
        "kind": pkg.kind,
        "product": pkg.product,
        "ambiguous": pkg.ambiguous,
        "no_results": pkg.no_results,
        "nodes": [
            {
                "id": n.id, "type": n.type, "product": n.product,
                "summary": n.summary, "confidence": n.confidence,
                "validation_status": n.validation_status, "score": n.score,
                "path": str(n.path),
            }
            for n in pkg.nodes
        ],
        "manifest": pkg.manifest,
    }
