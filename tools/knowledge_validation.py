"""Phase 12 — Knowledge Validation & Operational Integrity.

Idempotent, non-destructive, modeling-only. Builds the sixth constitutional
layer `VALIDATION_GOVERNANCE` and runs validators against the existing
per-product `knowledge-core/` data. Produces 10 numbered reports.

Hard rules honored:
  * NEVER modifies per-product knowledge-core/* files (read-only)
  * NEVER modifies prior governance layers
  * NEVER touches Comfy / orchestration / runtime / frontend
  * NEVER generates PDFs, images, chatbots, publication systems
  * Modeling + read-only validation only.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content" / "themes" / "beslock-custom" / "User manuals"
EXT = USER_MANUALS / "ext-images"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
VG = KB / "VALIDATION_GOVERNANCE"
REPORTS = USER_MANUALS / "_repository-governance" / "reports" / "validation"

SCHEMA = "validation-governance/1.0"
TODAY = date.today().isoformat()

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]
DOMAINS = [
    "entities", "workflows", "warnings", "terminology", "capabilities",
    "specifications", "troubleshooting", "visual-intent", "visual-risk",
    "publication-intent", "component-visibility", "provenance",
    "procedural-semantics", "install", "operation",
]

ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
PROCEDURAL_DOMAINS = {"workflows", "install", "operation", "procedural-semantics"}

# ---------------------------------------------------------------------------
# Loader

def load_corpus() -> dict:
    corpus = {}
    for product in PRODUCTS:
        corpus[product] = {}
        base = EXT / product / "knowledge-core"
        for domain in DOMAINS:
            ddir = base / domain
            items = []
            if ddir.is_dir():
                for f in sorted(ddir.glob("*.json")):
                    try:
                        data = json.loads(f.read_text(encoding="utf-8"))
                    except Exception as e:
                        items.append({"_load_error": str(e), "_file": str(f.relative_to(USER_MANUALS))})
                        continue
                    if isinstance(data, list):
                        for d in data:
                            if isinstance(d, dict):
                                d["_file"] = str(f.relative_to(USER_MANUALS))
                                items.append(d)
                    elif isinstance(data, dict):
                        data["_file"] = str(f.relative_to(USER_MANUALS))
                        items.append(data)
            corpus[product][domain] = items
    return corpus


# ---------------------------------------------------------------------------
# Helpers

def all_ids(corpus: dict) -> dict:
    """product -> set of declared ids."""
    out = {}
    for p, domains in corpus.items():
        ids = set()
        for items in domains.values():
            for it in items:
                if isinstance(it, dict) and "id" in it:
                    ids.add(it["id"])
        out[p] = ids
    return out


# ---------------------------------------------------------------------------
# 1. Procedural integrity

def validate_procedural_integrity(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    per_product = defaultdict(lambda: Counter())
    for product, domains in corpus.items():
        # Workflow steps
        for it in domains.get("workflows", []):
            wid = it.get("id", "<unknown>")
            steps = it.get("steps") or []
            if not steps:
                findings.append({"class": "empty-step-chain", "product": product, "id": wid, "domain": "workflows"})
                by_class["empty-step-chain"] += 1
                per_product[product]["empty-step-chain"] += 1
                continue
            ns = [s.get("n") for s in steps if isinstance(s, dict)]
            if any(n is None for n in ns):
                findings.append({"class": "missing-step-index", "product": product, "id": wid, "domain": "workflows"})
                by_class["missing-step-index"] += 1
                per_product[product]["missing-step-index"] += 1
            else:
                if sorted(ns) != list(range(1, len(ns) + 1)):
                    findings.append({"class": "non-sequential-steps", "product": product, "id": wid, "domain": "workflows", "ns": ns})
                    by_class["non-sequential-steps"] += 1
                    per_product[product]["non-sequential-steps"] += 1
                if len(set(ns)) != len(ns):
                    findings.append({"class": "duplicate-step-index", "product": product, "id": wid, "domain": "workflows"})
                    by_class["duplicate-step-index"] += 1
                    per_product[product]["duplicate-step-index"] += 1
            for s in steps:
                if isinstance(s, dict) and not (s.get("text") or "").strip():
                    findings.append({"class": "empty-step-text", "product": product, "id": wid, "domain": "workflows", "n": s.get("n")})
                    by_class["empty-step-text"] += 1
                    per_product[product]["empty-step-text"] += 1
        # procedural-semantics — look for empty normalized_steps or empty raw_text
        for it in domains.get("procedural-semantics", []):
            pid = it.get("id", "<unknown>")
            ns = it.get("normalized_steps") or []
            if not ns:
                findings.append({"class": "empty-procedural-semantics", "product": product, "id": pid, "domain": "procedural-semantics"})
                by_class["empty-procedural-semantics"] += 1
                per_product[product]["empty-procedural-semantics"] += 1
            else:
                idx = [s.get("step_index") for s in ns if isinstance(s, dict)]
                if any(i is None for i in idx):
                    findings.append({"class": "missing-step-index", "product": product, "id": pid, "domain": "procedural-semantics"})
                    by_class["missing-step-index"] += 1
                    per_product[product]["missing-step-index"] += 1
                elif sorted(idx) != list(range(1, len(idx) + 1)):
                    findings.append({"class": "non-sequential-steps", "product": product, "id": pid, "domain": "procedural-semantics", "ns": idx})
                    by_class["non-sequential-steps"] += 1
                    per_product[product]["non-sequential-steps"] += 1
                # All-empty semantic_actions across every step → unresolved-action-references
                if all(not (s.get("semantic_actions") or []) for s in ns if isinstance(s, dict)):
                    findings.append({"class": "unresolved-action-references", "product": product, "id": pid, "domain": "procedural-semantics"})
                    by_class["unresolved-action-references"] += 1
                    per_product[product]["unresolved-action-references"] += 1
        # install / operation — look for empty steps
        for domain in ("install", "operation"):
            for it in domains.get(domain, []):
                pid = it.get("id", "<unknown>")
                steps = it.get("steps") or it.get("normalized_steps") or []
                if not steps:
                    findings.append({"class": "empty-step-chain", "product": product, "id": pid, "domain": domain})
                    by_class["empty-step-chain"] += 1
                    per_product[product]["empty-step-chain"] += 1
    return {
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "per_product": {p: dict(c) for p, c in per_product.items()},
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# 2. Workflow executability

def validate_workflow_executability(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    summary = {p: {"workflows": 0, "with_actors": 0, "with_preconditions": 0, "with_channel_targets": 0} for p in PRODUCTS}
    for product, domains in corpus.items():
        for it in domains.get("workflows", []):
            wid = it.get("id", "<unknown>")
            summary[product]["workflows"] += 1
            actors = it.get("actors") or []
            preconds = it.get("preconditions") or []
            channels = it.get("channel_targets") or []
            steps = it.get("steps") or []
            if actors: summary[product]["with_actors"] += 1
            if preconds: summary[product]["with_preconditions"] += 1
            if channels: summary[product]["with_channel_targets"] += 1
            if not actors:
                findings.append({"class": "missing-actors", "product": product, "id": wid})
                by_class["missing-actors"] += 1
            if not steps:
                findings.append({"class": "non-terminating-workflow", "product": product, "id": wid})
                by_class["non-terminating-workflow"] += 1
            if not channels:
                findings.append({"class": "no-channel-targets", "product": product, "id": wid})
                by_class["no-channel-targets"] += 1
        # Onboarding completeness proxy: products with zero workflows cannot onboard
        if summary[product]["workflows"] == 0:
            findings.append({"class": "no-workflows-for-product", "product": product})
            by_class["no-workflows-for-product"] += 1
        # Troubleshooting recovery proxy
        if not domains.get("troubleshooting"):
            findings.append({"class": "no-troubleshooting-corpus", "product": product})
            by_class["no-troubleshooting-corpus"] += 1
    return {
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "per_product": summary,
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# 3. Entity consistency

def validate_entity_consistency(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    per_product = {}
    cross_product_collisions = []
    seen_entity_ids = defaultdict(set)  # entity_id -> {products}

    for product, domains in corpus.items():
        catalog = None
        for it in domains.get("entities", []):
            if it.get("type") == "entity-catalog":
                catalog = it
                break
        declared = set()
        if catalog:
            for e in catalog.get("entities") or []:
                eid = e.get("id")
                if not eid:
                    findings.append({"class": "entity-without-id", "product": product})
                    by_class["entity-without-id"] += 1
                    continue
                declared.add(eid)
                seen_entity_ids[eid].add(product)
                if not ID_RE.match(eid):
                    findings.append({"class": "non-conforming-entity-id", "product": product, "id": eid})
                    by_class["non-conforming-entity-id"] += 1
                if not (e.get("matched_surface_terms") or []):
                    findings.append({"class": "entity-without-surface-terms", "product": product, "id": eid})
                    by_class["entity-without-surface-terms"] += 1
        per_product[product] = {"declared_entities": len(declared)}

    for eid, prods in seen_entity_ids.items():
        if len(prods) > 1:
            cross_product_collisions.append({"entity_id": eid, "products": sorted(prods)})
            by_class["cross-product-entity-collision"] += 1

    # Orphan entities: declared but not referenced anywhere in product
    for product, domains in corpus.items():
        declared = set()
        catalog = next((it for it in domains.get("entities", []) if it.get("type") == "entity-catalog"), None)
        if catalog:
            declared = {e.get("id") for e in (catalog.get("entities") or []) if e.get("id")}
        # collect all text-form references in product
        text_blob_parts = []
        for d in DOMAINS:
            for it in domains.get(d, []):
                text_blob_parts.append(json.dumps(it, ensure_ascii=False))
        blob = "\n".join(text_blob_parts)
        for eid in declared:
            # entity-id usually like "entity-keypad" — search loose form too
            short = eid.replace("entity-", "")
            if blob.count(eid) <= 1 and short not in blob:
                findings.append({"class": "orphan-entity", "product": product, "id": eid})
                by_class["orphan-entity"] += 1

    return {
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "per_product": per_product,
        "cross_product_collisions": cross_product_collisions,
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# 4. Knowledge graph validation

def validate_knowledge_graph(corpus: dict) -> dict:
    nodes = {}  # (product, id) -> {type, refs:set}
    findings = []
    by_class = Counter()

    for product, domains in corpus.items():
        for d, items in domains.items():
            for it in items:
                if not isinstance(it, dict):
                    continue
                nid = it.get("id")
                if not nid:
                    continue
                key = (product, nid)
                refs = set()
                related = it.get("related") or {}
                if isinstance(related, dict):
                    for v in related.values():
                        if isinstance(v, list):
                            refs.update(x for x in v if isinstance(x, str))
                        elif isinstance(v, str):
                            refs.add(v)
                # source_entity_id (procedural-semantics → install/operation/workflow)
                if it.get("source_entity_id"):
                    refs.add(it["source_entity_id"])
                nodes[key] = {"type": it.get("type") or d, "domain": d, "refs": refs}

    # Build per-product id index
    per_product_ids = defaultdict(set)
    for (p, i) in nodes:
        per_product_ids[p].add(i)

    # Unresolved references and orphans
    referenced = defaultdict(set)
    for (p, i), n in nodes.items():
        for r in n["refs"]:
            if r not in per_product_ids[p]:
                findings.append({"class": "unresolved-reference", "product": p, "from": i, "to": r})
                by_class["unresolved-reference"] += 1
            else:
                referenced[p].add(r)

    # Orphan nodes: never referenced AND not a top-level catalog/charter
    TOP_TYPES = {"entity-catalog", "workflow", "capability", "publication-intent", "component-visibility", "provenance"}
    for (p, i), n in nodes.items():
        if i in referenced[p]:
            continue
        if n["type"] in TOP_TYPES:
            continue
        findings.append({"class": "orphan-node", "product": p, "id": i, "type": n["type"]})
        by_class["orphan-node"] += 1

    # Cycle detection (per product) over `related` refs
    for product in PRODUCTS:
        graph = {i: [r for r in nodes[(product, i)]["refs"] if r in per_product_ids[product]] for i in per_product_ids[product]}
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {i: WHITE for i in graph}
        cycles = []
        def dfs(u, stack):
            color[u] = GRAY
            for v in graph.get(u, []):
                if color[v] == GRAY:
                    cycles.append(stack + [u, v])
                elif color[v] == WHITE:
                    dfs(v, stack + [u])
            color[u] = BLACK
        for n_ in list(graph):
            if color[n_] == WHITE:
                dfs(n_, [])
        for c in cycles:
            findings.append({"class": "circular-reference", "product": product, "cycle": c})
            by_class["circular-reference"] += 1

    return {
        "total_nodes": len(nodes),
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "findings": findings[:200],  # cap dump
        "findings_truncated_to": min(200, len(findings)),
    }


# ---------------------------------------------------------------------------
# 5. Experience validation (cross-reference EXPERIENCE_GOVERNANCE)

def validate_experience(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    exp_priority = KB / "EXPERIENCE_GOVERNANCE" / "knowledge-priority" / "knowledge-priority.json"
    referenced_procedure_ids = []
    if exp_priority.is_file():
        try:
            data = json.loads(exp_priority.read_text(encoding="utf-8"))
            for a in data.get("priority_assignments", []) or data.get("assignments", []) or []:
                pid = a.get("procedure_id") or a.get("id") or a.get("procedure")
                if pid:
                    referenced_procedure_ids.append(pid)
        except Exception as e:
            findings.append({"class": "experience-doctrine-load-error", "error": str(e)})
            by_class["experience-doctrine-load-error"] += 1

    all_ids_per_product = all_ids(corpus)
    union_ids = set()
    for s in all_ids_per_product.values():
        union_ids.update(s)

    for pid in referenced_procedure_ids:
        if pid not in union_ids:
            # try fuzzy: priority assignments are often abstract names like "unlock-pin" — accept if any id contains it
            if not any(pid in i for i in union_ids):
                findings.append({"class": "experience-references-missing-procedure", "procedure_id": pid})
                by_class["experience-references-missing-procedure"] += 1

    # Onboarding gaps: products with no procedural-semantics → onboarding cannot guide
    for p in PRODUCTS:
        if not corpus[p].get("procedural-semantics"):
            findings.append({"class": "onboarding-no-procedural-semantics", "product": p})
            by_class["onboarding-no-procedural-semantics"] += 1
        if not corpus[p].get("warnings"):
            findings.append({"class": "warning-corpus-empty", "product": p})
            by_class["warning-corpus-empty"] += 1

    return {
        "experience_priority_assignments_checked": len(referenced_procedure_ids),
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# 6. Retrieval validation

REQUIRED_RAG_CHANNELS = {"chatbot", "rag"}

def validate_retrieval(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    per_product = {p: {"items": 0, "rag_ready": 0, "missing_summary": 0, "missing_channel_targets": 0} for p in PRODUCTS}

    for product, domains in corpus.items():
        for d, items in domains.items():
            for it in items:
                if not isinstance(it, dict):
                    continue
                per_product[product]["items"] += 1
                summary = it.get("summary") or it.get("definition")
                if not summary:
                    findings.append({"class": "missing-summary", "product": product, "id": it.get("id"), "domain": d})
                    by_class["missing-summary"] += 1
                    per_product[product]["missing_summary"] += 1
                channels = set(it.get("channel_targets") or [])
                if not channels:
                    findings.append({"class": "missing-channel-targets", "product": product, "id": it.get("id"), "domain": d})
                    by_class["missing-channel-targets"] += 1
                    per_product[product]["missing_channel_targets"] += 1
                elif REQUIRED_RAG_CHANNELS.issubset(channels):
                    per_product[product]["rag_ready"] += 1
                if not (it.get("source_refs") or []):
                    findings.append({"class": "missing-provenance-refs", "product": product, "id": it.get("id"), "domain": d})
                    by_class["missing-provenance-refs"] += 1

    # Terminology retrieval coherence: bilingual canonical-term collisions
    canon_seen = defaultdict(list)
    for product, domains in corpus.items():
        for it in domains.get("terminology", []):
            c = it.get("canonical")
            if c:
                canon_seen[c.lower()].append((product, it.get("id")))
    for c, occ in canon_seen.items():
        if len({p for p, _ in occ}) > 1:
            findings.append({"class": "cross-product-terminology-canonical", "canonical": c, "occurrences": occ})
            by_class["cross-product-terminology-canonical"] += 1

    return {
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "per_product": per_product,
        "findings_sample": findings[:200],
        "findings_truncated_to": min(200, len(findings)),
    }


# ---------------------------------------------------------------------------
# 7. Maturity validation

VALID_STATUSES = {
    "extraction-pending-review", "normalized", "canonicalized",
    "verified", "promoted", "deprecated", "superseded", "archived", "unresolved",
    "inferred", "inferred-but-unverified", "ocr-derived", "discovered", "extracted",
}

PROMOTED_STATUSES = {"promoted", "verified"}

def validate_maturity(corpus: dict) -> dict:
    findings = []
    by_class = Counter()
    distribution = Counter()
    per_product = {p: Counter() for p in PRODUCTS}

    for product, domains in corpus.items():
        for d, items in domains.items():
            for it in items:
                if not isinstance(it, dict):
                    continue
                status = it.get("validation_status")
                conf = it.get("confidence")
                ocr = it.get("ocr_dependency")
                if status:
                    distribution[status] += 1
                    per_product[product][status] += 1
                else:
                    findings.append({"class": "missing-validation-status", "product": product, "id": it.get("id"), "domain": d})
                    by_class["missing-validation-status"] += 1
                if status not in VALID_STATUSES and status is not None:
                    findings.append({"class": "unknown-validation-status", "product": product, "id": it.get("id"), "domain": d, "status": status})
                    by_class["unknown-validation-status"] += 1
                # Promoted/verified with low confidence or heavy OCR is a contradiction
                if status in PROMOTED_STATUSES and conf == "low":
                    findings.append({"class": "unsafe-promotion-low-confidence", "product": product, "id": it.get("id"), "domain": d})
                    by_class["unsafe-promotion-low-confidence"] += 1
                if status in PROMOTED_STATUSES and ocr == "full":
                    findings.append({"class": "unsafe-promotion-full-ocr", "product": product, "id": it.get("id"), "domain": d})
                    by_class["unsafe-promotion-full-ocr"] += 1
                # Unresolved evidence leak: status=normalized/canonical but no source_refs
                if status in {"normalized", "canonicalized", "verified", "promoted"} and not (it.get("source_refs") or []):
                    findings.append({"class": "unresolved-evidence-leak", "product": product, "id": it.get("id"), "domain": d})
                    by_class["unresolved-evidence-leak"] += 1

    return {
        "distribution": dict(distribution),
        "per_product_distribution": {p: dict(c) for p, c in per_product.items()},
        "total_findings": len(findings),
        "by_class": dict(by_class),
        "findings_sample": findings[:200],
        "findings_truncated_to": min(200, len(findings)),
    }


# ---------------------------------------------------------------------------
# 8. Health scorecards

def health_scorecards(corpus: dict, results: dict) -> dict:
    cards = {}
    for product in PRODUCTS:
        domains = corpus[product]
        item_count = sum(len(items) for items in domains.values())
        domain_coverage = sum(1 for d in DOMAINS if domains.get(d)) / len(DOMAINS)
        # Completeness: ratio of domains with ≥1 item
        completeness = round(domain_coverage, 3)
        # Consistency: 1 - (validation_findings_for_product / item_count)
        proc = results["procedural"]["per_product"].get(product, {})
        proc_findings = sum(proc.values()) if proc else 0
        ret = results["retrieval"]["per_product"].get(product, {})
        ret_findings = (ret.get("missing_summary", 0) + ret.get("missing_channel_targets", 0))
        mat = results["maturity"]["per_product_distribution"].get(product, {})
        mat_findings = mat.get("extraction-pending-review", 0)
        all_findings = proc_findings + ret_findings
        consistency = round(max(0.0, 1 - (all_findings / max(1, item_count))), 3)
        # Validation confidence: ratio normalized/canonicalized/verified/promoted vs total
        confident = sum(mat.get(s, 0) for s in ("normalized", "canonicalized", "verified", "promoted"))
        validation_confidence = round(confident / max(1, item_count), 3)
        # Operational usability: workflows present and at least one has actors+steps
        wf_count = len(domains.get("workflows", []))
        usable_wf = sum(1 for w in domains.get("workflows", []) if (w.get("steps") and w.get("actors")))
        operational_usability = round(usable_wf / max(1, wf_count), 3) if wf_count else 0.0
        # Semantic coherence: 1 - cross-product collisions involving this product / declared_entities
        ent = results["entity"]["per_product"].get(product, {}).get("declared_entities", 0) or 1
        coll = sum(1 for c in results["entity"]["cross_product_collisions"] if product in c["products"])
        semantic_coherence = round(max(0.0, 1 - coll / ent), 3)
        cards[product] = {
            "items": item_count,
            "domains_covered": int(domain_coverage * len(DOMAINS)),
            "completeness": completeness,
            "consistency": consistency,
            "validation_confidence": validation_confidence,
            "operational_usability": operational_usability,
            "semantic_coherence": semantic_coherence,
        }
    return cards


# ---------------------------------------------------------------------------
# 9. Validation governance doctrine

CHARTER_PRINCIPLES = [
    "Validation does not author knowledge; it observes and reports.",
    "Operational integrity is a precondition for promotion to verified-truth.",
    "Every validator is read-only; findings produce reports, not mutations.",
    "Findings are typed (class), located (product+id+domain), and explainable.",
    "Critical findings (unresolved-reference, lineage-break, promotion-without-evidence) have zero tolerance.",
    "Validation is continuous; thresholds are governed, not negotiated.",
    "Validation is subordinate to the knowledge-core and to LIFECYCLE_GOVERNANCE.",
    "Future systems (RAG, chatbot, onboarding, troubleshooting) inherit validation results, never override them.",
]

AUTHORITY_AREAS = [
    "procedural-integrity", "workflow-executability", "entity-consistency",
    "graph-validation", "experience-validation", "retrieval-validation",
    "maturity-validation", "health-scoring", "validation-philosophy",
    "future-system-safety",
]

VALIDATION_RULES = [
    "Workflows MUST have non-empty steps with sequential 1..N indices.",
    "Procedural-semantics MUST have non-empty normalized_steps; absent semantic_actions on every step => unresolved-action-references.",
    "Entities MUST have id matching `^[a-z0-9][a-z0-9-]*$` and at least one matched_surface_term.",
    "Cross-product entity-id collisions are only permitted when the entity represents a shared concept (must be declared).",
    "Every artifact MUST declare validation_status from the governed set.",
    "Promoted/verified artifacts with confidence=low or ocr_dependency=full are unsafe-promotions.",
    "Promoted/verified artifacts MUST have non-empty source_refs (no unresolved-evidence-leak).",
    "Every artifact MUST declare channel_targets; chatbot+rag readiness is required for retrieval-promotion.",
    "Cross-product canonical-term collisions in terminology require an explicit shared-terminology declaration.",
    "All findings MUST be reproducible by re-running the validator against unchanged inputs (idempotency).",
]

def doc_readme() -> str:
    return f"""# VALIDATION_GOVERNANCE

Constitutional layer governing **operational validation and semantic QA** of the
Beslock knowledge center.

- Schema: `{SCHEMA}`
- Generated: {TODAY}
- Subordinate to: `knowledge-core`, `LIFECYCLE_GOVERNANCE`
- Coexists with: `VISUAL_GOVERNANCE`, `KNOWLEDGE_CENTER`, `SEMANTIC_GOVERNANCE`,
  `EXPERIENCE_GOVERNANCE`, `LIFECYCLE_GOVERNANCE`

This layer is **read-only**. It does not modify per-product `knowledge-core/`
files. It runs validators, produces typed findings, and publishes scorecards.

## Authority areas
{chr(10).join(f"- {a}" for a in AUTHORITY_AREAS)}

## Doctrine layout
- `00-charter.md` — principles + authority areas
- `procedural-integrity/` — step-chain & sequence rules
- `workflow-executability/` — operational completeness rules
- `entity-validation/` — entity id, surface, collision rules
- `graph-validation/` — connectivity, orphan, cycle rules
- `experience-validation/` — cross-reference to EXPERIENCE_GOVERNANCE
- `retrieval-validation/` — channel + summary + provenance rules
- `maturity-validation/` — status / confidence / ocr coherence rules
- `health-scorecards/` — per-product scoring methodology
- `validation-philosophy/` — read-only, idempotent, zero-tolerance principles
- `future-system-safety/` — downstream-consumer inheritance gates

Reports: `_repository-governance/reports/validation/01..10`.
"""


def doc_charter() -> str:
    body = "# 00 — Validation Governance Charter\n\n## Principles\n"
    for i, p in enumerate(CHARTER_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## Authority areas\n"
    for a in AUTHORITY_AREAS:
        body += f"- {a}\n"
    body += "\n## Hard guarantees\n"
    body += "- Read-only. Modifies no per-product knowledge.\n"
    body += "- Idempotent. Same inputs => same findings.\n"
    body += "- Subordinate. Cannot override knowledge-core or lifecycle decisions.\n"
    body += "- Non-destructive. Findings never delete artifacts.\n"
    return body


def doc_section(title: str, rules: list[str]) -> str:
    body = f"# {title}\n\n## Rules\n\n"
    for r in rules:
        body += f"- {r}\n"
    return body


# ---------------------------------------------------------------------------
# Future system safety

FUTURE_SAFETY_GATES = [
    {"system": "chatbot",                 "requires": ["maturity.unsafe-promotions=0", "graph.unresolved-reference=0", "retrieval.missing-channel-targets=0"]},
    {"system": "onboarding-assistant",    "requires": ["procedural.empty-step-chain=0", "experience.warning-corpus-empty per product=0"]},
    {"system": "troubleshooting-assistant","requires": ["troubleshooting corpus per product ≥ 1", "graph.unresolved-reference=0"]},
    {"system": "dynamic-publication",     "requires": ["maturity.unresolved-evidence-leak=0", "publication-intent present per product"]},
    {"system": "multimodal-guidance",     "requires": ["visual-intent present", "visual-risk classified", "component-visibility declared"]},
    {"system": "future-visual-assistance","requires": ["visual-risk reclassification freeze", "graph orphan-node ratio reviewed"]},
]


# ---------------------------------------------------------------------------
# Main

def main() -> None:
    corpus = load_corpus()

    res_proc   = validate_procedural_integrity(corpus)
    res_wf     = validate_workflow_executability(corpus)
    res_entity = validate_entity_consistency(corpus)
    res_graph  = validate_knowledge_graph(corpus)
    res_exp    = validate_experience(corpus)
    res_ret    = validate_retrieval(corpus)
    res_mat    = validate_maturity(corpus)

    aggregated = {
        "procedural": res_proc,
        "workflow": res_wf,
        "entity": res_entity,
        "graph": res_graph,
        "experience": res_exp,
        "retrieval": res_ret,
        "maturity": res_mat,
    }

    cards = health_scorecards(corpus, aggregated)

    # Doctrine
    VG.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (VG / "README.md").write_text(doc_readme(), encoding="utf-8")
    (VG / "00-charter.md").write_text(doc_charter(), encoding="utf-8")
    (VG / "00-charter.json").write_text(json.dumps({
        "schema": SCHEMA, "generated": TODAY,
        "principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS,
    }, indent=2) + "\n", encoding="utf-8")

    sections = [
        ("procedural-integrity", "Procedural Integrity Rules", VALIDATION_RULES[:2]),
        ("workflow-executability", "Workflow Executability Rules",
         ["Workflows MUST declare actors and at least one step.",
          "Workflows MUST declare channel_targets.",
          "Products MUST have ≥1 workflow to support onboarding.",
          "Products MUST have ≥1 troubleshooting artifact to support escalation."]),
        ("entity-validation", "Entity Consistency Rules", VALIDATION_RULES[2:4]),
        ("graph-validation", "Graph Validation Rules",
         ["No unresolved references (target id MUST exist within product scope).",
          "No circular reference chains.",
          "Orphan nodes outside the top-type allowlist are findings."]),
        ("experience-validation", "Experience Validation Rules",
         ["Procedure ids referenced by EXPERIENCE_GOVERNANCE MUST resolve to a knowledge-core artifact.",
          "Every product MUST have a non-empty warning corpus.",
          "Every product MUST have ≥1 procedural-semantics artifact."]),
        ("retrieval-validation", "Retrieval Validation Rules", VALIDATION_RULES[7:9]),
        ("maturity-validation", "Maturity Validation Rules", VALIDATION_RULES[4:7]),
        ("health-scorecards", "Health Scoring Methodology",
         ["completeness = covered_domains / total_domains",
          "consistency = 1 − (procedural+retrieval findings / items)",
          "validation_confidence = (normalized+canonicalized+verified+promoted) / items",
          "operational_usability = workflows_with_steps_and_actors / total_workflows",
          "semantic_coherence = 1 − (cross-product collisions involving product / declared entities)"]),
        ("validation-philosophy", "Validation Philosophy",
         ["Read-only.", "Idempotent.", "Typed findings.", "Zero-tolerance for critical classes.",
          "Subordinate to knowledge-core and LIFECYCLE_GOVERNANCE."]),
        ("future-system-safety", "Future System Safety Gates",
         [f"`{g['system']}` requires: {', '.join(g['requires'])}" for g in FUTURE_SAFETY_GATES]),
    ]

    for slug, title, rules in sections:
        folder = VG / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{slug}.md").write_text(doc_section(title, rules), encoding="utf-8")
        (folder / f"{slug}.json").write_text(json.dumps({
            "schema": SCHEMA, "generated": TODAY, "title": title, "rules": rules,
        }, indent=2) + "\n", encoding="utf-8")

    # Reports
    def _wr(name: str, payload: dict) -> None:
        (REPORTS / name).write_text(json.dumps(
            {"schema": SCHEMA, "generated": TODAY, **payload}, indent=2, ensure_ascii=False
        ) + "\n", encoding="utf-8")

    _wr("01-procedural-integrity.json", res_proc)
    _wr("02-workflow-executability.json", res_wf)
    _wr("03-entity-consistency.json", res_entity)
    _wr("04-graph-validation.json", res_graph)
    _wr("05-experience-validation.json", res_exp)
    _wr("06-retrieval-validation.json", res_ret)
    _wr("07-maturity-validation.json", res_mat)
    _wr("08-knowledge-health-scorecards.json", {"scorecards": cards})
    _wr("09-validation-governance-summary.json", {
        "principles": CHARTER_PRINCIPLES,
        "authority_areas": AUTHORITY_AREAS,
        "rules": VALIDATION_RULES,
    })

    # 10 — unresolved operational risks (synthesis)
    risks = []
    if res_graph["by_class"].get("unresolved-reference"):
        risks.append({"risk": "unresolved-reference", "count": res_graph["by_class"]["unresolved-reference"], "blocks": ["RAG", "chatbot", "onboarding"]})
    if res_mat["by_class"].get("unresolved-evidence-leak"):
        risks.append({"risk": "unresolved-evidence-leak", "count": res_mat["by_class"]["unresolved-evidence-leak"], "blocks": ["verified-truth promotion"]})
    if res_proc["by_class"].get("unresolved-action-references"):
        risks.append({"risk": "unresolved-action-references", "count": res_proc["by_class"]["unresolved-action-references"], "blocks": ["procedural execution by assistants"]})
    if res_wf["by_class"].get("no-troubleshooting-corpus"):
        risks.append({"risk": "no-troubleshooting-corpus", "count": res_wf["by_class"]["no-troubleshooting-corpus"], "blocks": ["troubleshooting-assistant per product"]})
    if res_exp["by_class"].get("warning-corpus-empty"):
        risks.append({"risk": "warning-corpus-empty", "count": res_exp["by_class"]["warning-corpus-empty"], "blocks": ["safe-first-use onboarding"]})
    if res_ret["by_class"].get("missing-channel-targets"):
        risks.append({"risk": "missing-channel-targets", "count": res_ret["by_class"]["missing-channel-targets"], "blocks": ["retrieval-promotion"]})
    if res_entity["by_class"].get("orphan-entity"):
        risks.append({"risk": "orphan-entity", "count": res_entity["by_class"]["orphan-entity"], "blocks": ["entity-graph integrity"]})
    if res_entity["by_class"].get("cross-product-entity-collision"):
        risks.append({"risk": "cross-product-entity-collision", "count": res_entity["by_class"]["cross-product-entity-collision"], "blocks": ["cross-product canonicalization"]})

    _wr("10-unresolved-operational-risks.json", {"risks": risks, "future_safety_gates": FUTURE_SAFETY_GATES})

    # Console summary
    print("Validation modeling complete.")
    print(f"  Constitutional root: {VG.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  Procedural findings:  {res_proc['total_findings']}")
    print(f"  Workflow findings:    {res_wf['total_findings']}")
    print(f"  Entity findings:      {res_entity['total_findings']}")
    print(f"  Graph findings:       {res_graph['total_findings']} (nodes={res_graph['total_nodes']})")
    print(f"  Experience findings:  {res_exp['total_findings']}")
    print(f"  Retrieval findings:   {res_ret['total_findings']}")
    print(f"  Maturity findings:    {res_mat['total_findings']}")


if __name__ == "__main__":
    main()
