#!/usr/bin/env python3
"""Phase 9 — Knowledge Normalization & Semantic Governance.

NON-DESTRUCTIVE.

Builds the constitutional layer for semantic governance under
`KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/` and emits machine-readable
normalization indices plus 10 reports under
`_repository-governance/reports/semantic-governance/`.

Existing per-product knowledge-core files are NOT modified, NOT moved, NOT
deleted. Conflicts are detected and reported — never auto-resolved.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
SG = KB / "SEMANTIC_GOVERNANCE"
EXT = USER_MANUALS / "ext-images"
GOV_REPO = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "semantic-governance/1.0"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

DOMAINS = [
    "entities", "procedures", "workflows", "warnings", "terminology",
    "capabilities", "specifications", "troubleshooting",
    "procedural-semantics", "visual-intent", "visual-risk",
    "publication-intent", "component-visibility", "provenance",
]

# ---------------------------------------------------------------------------
# Synonym table (bilingual + brand). Detection-only; declarative.
# ---------------------------------------------------------------------------
SYNONYM_GROUPS: list[dict] = [
    {"canonical": "administrator",        "synonyms": ["administrador", "admin"],          "domain": "terminology"},
    {"canonical": "user",                 "synonyms": ["usuario"],                          "domain": "terminology"},
    {"canonical": "fingerprint",          "synonyms": ["huella", "huella-dactilar"],       "domain": "terminology"},
    {"canonical": "pin",                  "synonyms": ["contrasena", "contraseña", "password", "codigo", "código"], "domain": "terminology"},
    {"canonical": "temporary-password",   "synonyms": ["virtual-password", "contrasena-temporal", "contraseña-temporal", "clave-temporal"], "domain": "terminology"},
    {"canonical": "factory-reset",        "synonyms": ["reset", "restablecer", "restablecer-de-fabrica", "restauracion-de-fabrica"], "domain": "terminology"},
    {"canonical": "qr-pairing",           "synonyms": ["qr", "vincular-por-qr", "alta-del-dispositivo-por-qr", "pair-by-qr"], "domain": "terminology"},
    {"canonical": "ez-mode-pairing",      "synonyms": ["ez-mode", "pair-by-ez-mode", "alta-del-dispositivo-por-wi-fi-ez-mode", "app-pairing-ez-mode"], "domain": "terminology"},
    {"canonical": "tuya-smart-app",       "synonyms": ["tuya", "tuya-smart", "tongtong-app", "smart-life"],         "domain": "terminology"},
    {"canonical": "wi-fi",                "synonyms": ["wifi"],                                                      "domain": "terminology"},
    {"canonical": "register-fingerprint", "synonyms": ["registrar-una-huella", "enrol-fingerprint", "enroll-fingerprint"], "domain": "procedure"},
    {"canonical": "register-pin",         "synonyms": ["registrar-una-contrasena-o-pin", "registrar-una-contrasena", "registrar-una-contraseña", "add-pin", "set-pin"], "domain": "procedure"},
    {"canonical": "add-administrator",    "synonyms": ["agregar-un-administrador"],                                  "domain": "procedure"},
    {"canonical": "add-user",             "synonyms": ["agregar-un-usuario"],                                         "domain": "procedure"},
    {"canonical": "change-language",      "synonyms": ["cambiar-el-idioma"],                                          "domain": "procedure"},
    {"canonical": "pair-with-app",        "synonyms": ["conectar-la-cerradura-a-la-aplicacion", "conectar-la-cerradura-a-la-aplicación", "primeros-pasos", "local-onboarding"], "domain": "procedure"},
    {"canonical": "member-management",    "synonyms": ["gestion-de-miembros", "gestión-de-miembros"],                "domain": "procedure"},
]

# ---------------------------------------------------------------------------
# Standardised action verbs for procedural normalization.
# ---------------------------------------------------------------------------
CANONICAL_VERBS = [
    "press", "hold", "tap", "swipe", "scan",
    "unlock", "lock",
    "enroll", "register", "remove",
    "pair", "unpair", "confirm", "cancel",
    "reset", "restart", "power-cycle",
    "install", "uninstall", "mount", "dismount",
    "configure", "select", "open", "close",
    "insert", "extract", "replace",
    "wait", "verify", "observe",
]
VERB_SYNONYMS = {
    "presionar": "press", "mantener": "hold", "mantener-presionado": "hold",
    "tocar": "tap", "deslizar": "swipe", "escanear": "scan",
    "desbloquear": "unlock", "bloquear": "lock",
    "registrar": "register", "inscribir": "enroll", "eliminar": "remove",
    "vincular": "pair", "desvincular": "unpair", "confirmar": "confirm",
    "cancelar": "cancel", "restablecer": "reset", "reiniciar": "restart",
    "instalar": "install", "desinstalar": "uninstall",
    "montar": "mount", "desmontar": "dismount",
    "configurar": "configure", "seleccionar": "select",
    "abrir": "open", "cerrar": "close",
    "insertar": "insert", "extraer": "extract", "reemplazar": "replace",
    "esperar": "wait", "verificar": "verify", "observar": "observe",
    "agregar": "add",  # add is not in verb registry; flagged below
    "set": "configure",
}

# ---------------------------------------------------------------------------
# ID grammar.
# ---------------------------------------------------------------------------
ID_GRAMMAR = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ARTIFACT_RE = re.compile(r"^(?:semantic|term|entity|warning|capability|spec|workflow|procedure|risk|intent|publication|component|prov)(?:-[a-z0-9-]+)?(?:\.[a-z0-9-]+)*$", re.IGNORECASE)


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def derive_local_id(domain: str, filename: str) -> str:
    stem = Path(filename).stem
    # Strip well-known prefixes.
    for prefix in (
        "semantic-proc-", "semantic-wf-", "semantic-",
        "term-", "entity-", "warning-", "capability-", "cap-",
        "spec-", "workflow-", "procedure-", "risk-", "intent-",
        "publication-", "component-", "prov-",
    ):
        if stem.startswith(prefix):
            return stem[len(prefix):]
    return stem


# ---------------------------------------------------------------------------
# Scan filesystem.
# ---------------------------------------------------------------------------
def scan() -> dict:
    by_domain: dict[str, list[dict]] = {d: [] for d in DOMAINS}
    for p in PRODUCTS:
        for d in DOMAINS:
            base = EXT / p / "knowledge-core" / d
            if not base.exists():
                continue
            for f in sorted(base.rglob("*")):
                if not f.is_file() or f.name.startswith("."):
                    continue
                rel = f.relative_to(USER_MANUALS).as_posix()
                local = derive_local_id(d, f.name)
                by_domain[d].append({
                    "product": p,
                    "filename": f.name,
                    "local_id": local,
                    "slug": slugify(local),
                    "path": rel,
                    "ext": f.suffix.lower(),
                })
    return by_domain


# ---------------------------------------------------------------------------
# Build canonical term → synonym lookup.
# ---------------------------------------------------------------------------
def build_synonym_lookup() -> tuple[dict[str, str], dict[str, list[str]]]:
    """Return (variant→canonical, canonical→list of variants)."""
    variant_to_canonical: dict[str, str] = {}
    canonical_to_variants: dict[str, list[str]] = {}
    for g in SYNONYM_GROUPS:
        c = g["canonical"]
        canonical_to_variants[c] = []
        variant_to_canonical[c] = c
        for v in g["synonyms"]:
            v_slug = slugify(v)
            variant_to_canonical[v_slug] = c
            canonical_to_variants[c].append(v_slug)
    return variant_to_canonical, canonical_to_variants


# ---------------------------------------------------------------------------
# Conflict detection.
# ---------------------------------------------------------------------------
def detect_conflicts(by_domain: dict, variant_to_canonical: dict[str, str]) -> dict:
    conflicts: dict[str, list[dict]] = {
        "duplicate-entity-within-product": [],
        "synonym-duplication": [],
        "bilingual-duplication": [],
        "non-conforming-id": [],
        "missing-prefix": [],
        "verb-out-of-registry": [],
        "cross-product-collision": [],
        "ambiguous-procedure-naming": [],
    }

    # 1) duplicate within product (same domain + same canonical id).
    for domain, items in by_domain.items():
        seen: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for it in items:
            canonical = variant_to_canonical.get(it["slug"], it["slug"])
            seen[(it["product"], canonical)].append(it)
        for (prod, canon), entries in seen.items():
            if len(entries) > 1:
                conflicts["duplicate-entity-within-product"].append({
                    "domain": domain,
                    "product": prod,
                    "canonical_id": canon,
                    "files": [e["path"] for e in entries],
                    "severity": "high",
                })

    # 2) synonym duplication regardless of language.
    for domain, items in by_domain.items():
        groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for it in items:
            canonical = variant_to_canonical.get(it["slug"])
            if canonical is None:
                continue
            if canonical == it["slug"]:
                continue  # this file IS the canonical
            groups[(it["product"], canonical)].append(it)
        for (prod, canon), entries in groups.items():
            for e in entries:
                conflicts["synonym-duplication"].append({
                    "domain": domain,
                    "product": prod,
                    "file": e["path"],
                    "found_slug": e["slug"],
                    "canonical_slug": canon,
                    "severity": "medium",
                })

    # 3) bilingual duplication: same product+domain has files for both
    #    canonical and synonym (English + Spanish present).
    for domain, items in by_domain.items():
        per_prod: dict[str, set[str]] = defaultdict(set)
        for it in items:
            canonical = variant_to_canonical.get(it["slug"], it["slug"])
            per_prod[it["product"]].add((canonical, it["slug"]))
        for prod, pairs in per_prod.items():
            by_canon: dict[str, set[str]] = defaultdict(set)
            for canon, slug in pairs:
                by_canon[canon].add(slug)
            for canon, slugs in by_canon.items():
                if len(slugs) > 1:
                    conflicts["bilingual-duplication"].append({
                        "domain": domain,
                        "product": prod,
                        "canonical_slug": canon,
                        "variants_present": sorted(slugs),
                        "severity": "medium",
                        "note": "Both canonical and synonym artifacts present in the same product nucleus.",
                    })

    # 4) non-conforming ID.
    for domain, items in by_domain.items():
        for it in items:
            stem = Path(it["filename"]).stem
            if not ARTIFACT_RE.match(stem):
                conflicts["non-conforming-id"].append({
                    "domain": domain, "product": it["product"], "file": it["path"],
                    "severity": "low",
                    "note": "Filename does not match the artifact prefix grammar.",
                })
            elif not ID_GRAMMAR.match(it["slug"]):
                conflicts["non-conforming-id"].append({
                    "domain": domain, "product": it["product"], "file": it["path"],
                    "severity": "low",
                    "note": "Local id does not match kebab-case grammar.",
                })

    # 5) missing prefix on procedural-semantics / workflows.
    expected_prefix = {
        "procedural-semantics": ("semantic-proc-", "semantic-wf-"),
        "workflows": ("workflow-", "wf-", "semantic-wf-"),
        "terminology": ("term-",),
        "warnings": ("warning-",),
        "capabilities": ("capability-", "cap-"),
        "entities": ("entity-",),
        "specifications": ("spec-", "specification-"),
        "visual-intent": ("intent-", "visual-intent-"),
        "visual-risk": ("risk-", "visual-risk-"),
        "publication-intent": ("publication-", "publication-intent-"),
        "component-visibility": ("component-", "component-visibility-"),
        "provenance": ("prov-", "provenance-"),
    }
    for domain, expected in expected_prefix.items():
        for it in by_domain.get(domain, []):
            stem = Path(it["filename"]).stem
            if it["filename"] in {"entity-catalog.json", "legacy-manifest.json", "component-visibility-map.json", "publication-intent-map.json"}:
                continue
            if not any(stem.startswith(pref) for pref in expected):
                conflicts["missing-prefix"].append({
                    "domain": domain, "product": it["product"], "file": it["path"],
                    "expected_prefixes": list(expected), "severity": "low",
                })

    # 6) verb out-of-registry on procedural-semantics file ids.
    for it in by_domain.get("procedural-semantics", []):
        local = it["local_id"]
        first_token = local.split("-")[0] if local else ""
        if not first_token:
            continue
        en = VERB_SYNONYMS.get(first_token, first_token)
        if en not in CANONICAL_VERBS and en not in {"add", "set", "wf", "proc"}:
            conflicts["verb-out-of-registry"].append({
                "product": it["product"], "file": it["path"],
                "first_token": first_token, "english_token": en,
                "severity": "low",
                "note": "Leading procedure token is neither a canonical verb nor a known synonym.",
            })

    # 7) cross-product collision on canonical id where the underlying intent
    #    might differ (we only flag for human review; never resolve).
    for domain in ("procedural-semantics", "workflows", "warnings", "capabilities", "terminology"):
        canon_to_prods: dict[str, list[dict]] = defaultdict(list)
        for it in by_domain.get(domain, []):
            canon = variant_to_canonical.get(it["slug"], it["slug"])
            canon_to_prods[canon].append(it)
        for canon, entries in canon_to_prods.items():
            prods = sorted({e["product"] for e in entries})
            if len(prods) >= 2:
                conflicts["cross-product-collision"].append({
                    "domain": domain, "canonical_id": canon,
                    "products": prods,
                    "files": [e["path"] for e in entries],
                    "severity": "info",
                    "note": "Same canonical id appears in multiple products — candidate for shared-concept membership; verify intent matches before linking.",
                })

    # 8) ambiguous procedure naming (mix of `add-`, `register-`, `enroll-`).
    family_prefixes = ("add-", "register-", "registrar-", "enroll-", "enrol-", "agregar-")
    by_target: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for it in by_domain.get("procedural-semantics", []):
        local = it["local_id"]
        for pref in family_prefixes:
            if local.startswith(pref):
                target = local[len(pref):]
                # canonicalize the target via synonyms
                target_canon = variant_to_canonical.get(slugify(target), slugify(target))
                by_target[(it["product"], target_canon)].append((pref.rstrip("-"), it))
                break
    for (prod, target), entries in by_target.items():
        verbs = sorted({v for v, _ in entries})
        if len(verbs) > 1:
            conflicts["ambiguous-procedure-naming"].append({
                "product": prod, "target": target, "verbs_used": verbs,
                "files": [it["path"] for _, it in entries],
                "severity": "medium",
                "note": "Same target object addressed with multiple action verbs — pick one canonical verb.",
            })

    return conflicts


# ---------------------------------------------------------------------------
# Documents.
# ---------------------------------------------------------------------------
def doc_charter() -> str:
    return f"""# Knowledge Governance Charter

_Schema: `{SCHEMA}` · semantic-governance constitution · generated {NOW}._

## Purpose

This charter is the constitutional layer of **knowledge governance**. It
defines who owns semantic content, how the ontology stays stable, how
terminology is canonicalised, how conflicts are resolved, how maturity is
governed, how lineage is preserved, and how retrieval stays consistent.

Knowledge governance is distinct from visual governance
(`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) and from runtime governance
(`visual-system/_governance/`). The three layers cooperate; none subsumes the
others.

## Principles

1. **Semantic ownership lives with the knowledge core.** No surface owns
   semantics. A surface that needs new semantics requests them from the
   knowledge layer.
2. **Ontology is platform-wide and stable.** Shared concept IDs are
   immutable once published. Refinement happens via sub-ids, never by
   renaming.
3. **One canonical name per concept.** Synonyms are tracked and mapped, not
   tolerated as parallel canonicals.
4. **Conflicts are surfaced, never silenced.** Auto-resolution would erase
   editorial judgement; the system reports and waits.
5. **Maturity is a first-class field.** Every artifact carries a maturity
   tier; downstream systems filter by tier.
6. **Lineage is mandatory.** Every artifact carries a provenance pointer;
   no provenance == not eligible for promotion.
7. **Retrieval stability is a contract.** Identifier shapes, index sources,
   and served fields are governed; arbitrary changes break consumers.
8. **Cross-product reuse over duplication.** Reusable concepts are promoted
   to the shared ontology rather than copy-edited per product.
9. **Subordination of all surfaces.** Every consumer (web, PDF, chatbot,
   RAG, AR, video, future Comfy orchestration) is subordinate to the
   knowledge core.

## Authorities

| Concern | Authority | Location |
|---|---|---|
| Ontology + shared concepts        | Knowledge Center | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/` |
| Canonical terminology             | Semantic Governance (this folder) | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/canonical-terminology/` |
| Procedural normalization          | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/procedural-normalization/` |
| Identifier grammar                | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-identifiers/` |
| Maturity classification           | Knowledge Center  | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/` |
| Maturity governance / consistency | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/maturity-governance/` |
| Retrieval indexing strategy       | Knowledge Center  | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/retrieval-readiness/` |
| Retrieval governance              | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/retrieval-governance/` |
| Cross-product coherence           | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/cross-product-governance/` |
| Conflict detection + register     | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-conflicts/` |
| Visual policy                     | Visual Governance | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` |
| Runtime enforcement               | Runtime governance | `visual-system/_governance/` |

## Conflict-resolution philosophy

1. Detect.
2. Classify (severity, domain, product scope).
3. Surface (write to the conflict register).
4. Wait for editorial resolution.
5. Promote the resolution into canonical terminology / shared ontology.
6. Re-scan to confirm no regression.

The system never deletes artifacts to silence a conflict. Mergers and
deprecations happen in editorial, then reflect in the registry.

## Amendment policy

Changing this charter requires updating this folder first, then propagating
into the relevant runtime artifacts. Direct edits to per-product nuclei that
contradict the charter are out of policy and must be reverted.
"""


def doc_terminology(syn_groups: list[dict]) -> str:
    rows = []
    for g in syn_groups:
        rows.append(f"| `{g['canonical']}` | {g['domain']} | " + ", ".join(f"`{slugify(s)}`" for s in g["synonyms"]) + " |")
    body = "\n".join(rows)
    return f"""# Canonical terminology registry

_Schema: `{SCHEMA}` · canonical terminology layer · generated {NOW}._

## Purpose

A platform-wide canonical terminology registry. Each entry declares one
canonical name and the synonyms (across English, Spanish, brand names and
abbreviations) that resolve to it. Detection-only: this registry is consulted
during conflict scans and during retrieval expansion. It does not rename
existing files.

## Registry

| Canonical | Domain | Synonyms |
|---|---|---|
{body}

## Authoring rules

1. Canonical names are kebab-case, lowercase, ASCII-only.
2. Synonyms include language variants (es-CO baseline + en), brand variants,
   abbreviations and common typos.
3. Adding a new canonical requires (a) an entry here, (b) a check that no
   existing canonical already covers the concept, (c) a re-scan via
   `tools/knowledge_normalize_audit.py` to surface any new conflicts.
4. Changing a canonical requires a deprecation entry — the previous canonical
   becomes a synonym and is never silently dropped.

## Companion files

- [`canonical-terminology.json`](canonical-terminology.json) — machine-readable form of the table above.
"""


def doc_procedural() -> str:
    rows = "\n".join(f"| `{v}` |" for v in CANONICAL_VERBS)
    syn_rows = "\n".join(f"| `{src}` | `{dst}` |" for src, dst in sorted(VERB_SYNONYMS.items()))
    return f"""# Procedural semantic normalization

_Schema: `{SCHEMA}` · procedural normalization spec · generated {NOW}._

## Purpose

Normalize action verbs, action granularity, procedural sequencing and
operational state transitions across all per-product procedural-semantics
artifacts.

## Canonical action verbs

| Verb |
|---|
{rows}

## Verb synonyms (auto-mapped during conflict detection)

| Found token | Maps to canonical |
|---|---|
{syn_rows}

## Action granularity

- A procedure step represents **one user-observable action** (one button
  press, one swipe, one selection) or **one observable system state change**
  (one LED change, one tone, one screen transition).
- Multi-action steps must be decomposed before promotion.
- Implicit waits become explicit `wait` steps with a duration field.

## Sequencing contract

- Steps are 1-indexed and totally ordered.
- Branches (success / failure / retry) are modelled as sub-procedures with
  explicit links, not as inline conditionals.
- Cross-procedure links use canonical procedure IDs from the ontology.

## State-transition vocabulary

- `unlocked`, `locked`, `paired`, `unpaired`, `enrolled`, `removed`,
  `factory-default`, `low-battery`, `lockout`, `firmware-updating`.

## Companion files

- [`procedural-normalization.json`](procedural-normalization.json) — machine-readable verb registry + synonym map.
"""


def doc_identifiers() -> str:
    return f"""# Semantic identifier system

_Schema: `{SCHEMA}` · identifier governance · generated {NOW}._

## Purpose

Define the persistent, stable, lineage-safe identifier system used by every
semantic artifact in the knowledge core.

## Grammar

- **Lowercase** ASCII.
- **Kebab-case** (segments separated by single `-`).
- No leading or trailing `-`. No double `-`.
- Regex: `^[a-z0-9]+(?:-[a-z0-9]+)*$`.

## Compound identifier shape

```
<domain-prefix>-<concept>[-<qualifier>][.<schema-version>]
```

| Domain | Prefix |
|---|---|
| terminology          | `term-`              |
| entities             | `entity-`            |
| warnings             | `warning-`           |
| capabilities         | `capability-` (or legacy `cap-`) |
| specifications       | `spec-`              |
| workflows            | `workflow-` (legacy `semantic-wf-` accepted) |
| procedures           | `procedure-` (legacy `semantic-proc-` accepted) |
| procedural-semantics | `semantic-proc-` / `semantic-wf-` |
| visual-intent        | `intent-` / `visual-intent-` |
| visual-risk          | `risk-` / `visual-risk-` |
| publication-intent   | `publication-` / `publication-intent-` |
| component-visibility | `component-`          |
| provenance           | `prov-` / `provenance-` |

## Cross-product linking

- A per-product artifact references a shared concept via the ontology ID
  (e.g. `procedure.factory-reset`).
- The per-product artifact is keyed by `<product>/<domain>/<filename-stem>`.
- The mapping `concept_id ↔ per-product artifact` lives in
  `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`.

## Stability and lineage rules

1. A published ID is **never renamed in place**.
2. A deprecated ID becomes a synonym pointing to its replacement.
3. A renamed file MUST emit a `<old>.lineage.json` receipt with `old_path`,
   `new_path`, `reason`, `timestamp`, `tool`.
4. Cross-product linking uses canonical IDs only. Per-product local IDs are
   never embedded across products.

## Companion files

- [`identifier-grammar.json`](identifier-grammar.json) — machine-readable grammar + prefix table.
"""


def doc_conflicts(conflicts: dict) -> str:
    counts = {k: len(v) for k, v in conflicts.items()}
    counts_table = "\n".join(f"| `{k}` | {v} |" for k, v in counts.items())
    return f"""# Semantic conflicts register

_Schema: `{SCHEMA}` · conflict register · generated {NOW}._

## Purpose

Detect duplicated entities, conflicting procedures, overlapping capabilities,
contradictory terminology, semantic collisions, ambiguous relationships and
maturity conflicts. **Conflicts are never auto-resolved.**

## Detection categories

| Category | Count |
|---|---:|
{counts_table}

## Detection categories — definitions

- **duplicate-entity-within-product** — two artifacts in the same product +
  domain that resolve to the same canonical ID. Severity: high.
- **synonym-duplication** — an artifact whose local ID is a known synonym of
  a canonical ID. Severity: medium.
- **bilingual-duplication** — both an English and a Spanish file for the same
  concept exist in one product. Severity: medium.
- **non-conforming-id** — filename or local ID violates the grammar.
  Severity: low.
- **missing-prefix** — filename lacks the expected domain prefix.
  Severity: low.
- **verb-out-of-registry** — leading procedure token is not a canonical
  action verb. Severity: low.
- **cross-product-collision** — same canonical ID appears in multiple
  products. Severity: info (candidate for shared-concept membership; verify
  intent first).
- **ambiguous-procedure-naming** — same target addressed with multiple verbs
  (e.g. `add-`, `register-`, `enroll-`). Severity: medium.

## Resolution policy

1. Detect → classify → surface in this register.
2. Editorial decides: merge, deprecate, rename, leave-as-is-with-rationale.
3. Update canonical-terminology / procedural-normalization registries.
4. Re-run the audit; the conflict count for each category MUST drop or stay
   constant — it MUST NOT silently grow.

## Companion files

- [`semantic-conflicts.json`](semantic-conflicts.json) — full machine-readable conflict catalogue.
"""


def doc_maturity_governance() -> str:
    return f"""# Maturity governance

_Schema: `{SCHEMA}` · maturity governance · generated {NOW}._

## Purpose

Normalize the maturity classification across the whole repository. The
authoritative tier list lives in
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/maturity-tiers.json`;
this document governs **how** maturity is assigned and changed.

## Required field

`maturity` is required on every semantic artifact under
`ext-images/<slug>/knowledge-core/`. Artifacts without a `maturity` field are
treated as `unresolved` until backfilled.

## Promotion rules

| From | To | Required evidence |
|---|---|---|
| absent       | unresolved   | none — auto |
| ocr-derived  | inferred     | reviewer note + at least one cross-evidence link |
| inferred     | canonical    | OEM evidence pointer + reviewer approval |
| canonical    | verified     | second OEM source OR field-confirmation record |
| any          | deprecated   | replacement artifact ID |
| any          | low-confidence | reviewer note explaining the downgrade |
| any          | transitional | migration target + ETA |

## Demotion rules

A demotion (e.g. `verified → low-confidence`) is allowed only with an
explicit reviewer note. Silent demotion is forbidden.

## Consistency invariants

1. A `verified` artifact MUST have ≥1 OEM evidence span.
2. A `canonical` artifact MUST have ≥1 evidence pointer.
3. A `deprecated` artifact MUST point to a replacement.
4. A `transitional` artifact MUST point to its migration target.
5. A `low-confidence` artifact MUST carry a `confidence_note`.

## Audit contract

A scan emits `_repository-governance/reports/semantic-governance/maturity-distribution.json`
on demand. The current phase declares the contract; the per-artifact backfill
is a separate phase.

## Companion files

- [`maturity-policies.json`](maturity-policies.json) — promotion/demotion table in machine-readable form.
"""


def doc_retrieval_governance() -> str:
    return f"""# Retrieval governance

_Schema: `{SCHEMA}` · retrieval governance · generated {NOW}._

## Purpose

Strengthen long-term retrieval consistency. The retrieval **strategy** lives
in `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/retrieval-readiness/`; this document
governs **how** retrieval contracts are kept stable.

## Stability contracts

1. Index source patterns are governed; changing a pattern requires a new
   index ID, not an in-place change.
2. Served fields (`id`, `maturity`, `provenance`, `last_updated`,
   `channel_targets`) are the minimum surface; consumers may rely on them.
3. Identifier grammar is governed; renames require lineage receipts.
4. Synonym expansion at retrieval time uses the canonical-terminology
   registry; consumers SHOULD NOT maintain private synonym lists.
5. Maturity gates are applied at the consumer; consumers MUST read the
   maturity field and MUST surface it in their UX.

## Discoverability rules

- Every entity, procedure, workflow, warning, capability, terminology entry,
  specification and visual semantic MUST be reachable by:
  - direct ID lookup,
  - shared-concept lookup (when applicable),
  - product-level enumeration.
- An artifact that exists on disk but is unreachable by any of the above is
  flagged in the conflict register as `discoverability-orphan` (added in a
  future audit).

## Provenance presentation

- Every served artifact MUST carry its provenance.
- Consumers MUST surface provenance to end users when delivering safety,
  installation, or troubleshooting content.

## Companion files

- [`retrieval-governance.json`](retrieval-governance.json) — machine-readable contract.
"""


def doc_cross_product() -> str:
    return f"""# Cross-product semantic governance

_Schema: `{SCHEMA}` · cross-product governance · generated {NOW}._

## Purpose

Identify reusable semantic primitives, shared operational concepts, reusable
warning models, reusable installation logic and reusable workflow archetypes.
Prevent cross-product semantic contamination.

## Promotion rules (concept → shared)

A concept becomes shared when it is observed in **two or more products** AND
the editorial review confirms semantic equivalence. The concept is then
promoted to the shared ontology in
`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/ontology.json` and
its members are recorded in `shared-concept-membership.json`.

## Anti-contamination rules

1. A per-product artifact MUST NOT silently inherit text or fields from
   another product.
2. A per-product artifact MUST NOT reference another product's local ID;
   cross-product links go through shared concept IDs only.
3. A per-product artifact MUST NOT borrow a warning, terminology entry or
   procedural step from another product without (a) explicit reviewer
   note and (b) provenance pointing back to OEM evidence for the borrowing
   product.

## Reusable archetypes

- **Pairing archetype**: pair-with-app + variant (qr-pairing, ez-mode-pairing).
- **Enrolment archetype**: register-fingerprint + register-pin + add-administrator + add-user.
- **Recovery archetype**: factory-reset + emergency-power + battery-replacement.
- **Operational archetype**: unlock-* (pin / fingerprint / app / mechanical).
- **Maintenance archetype**: firmware-update + battery-replacement.

## Companion files

- [`cross-product-coherence.json`](cross-product-coherence.json) — archetype list + promotion rules.
"""


def doc_future() -> str:
    return f"""# Future readiness (semantic governance)

_Schema: `{SCHEMA}` · future readiness · generated {NOW}._

## Subordination

Every future surface — multilingual support, chatbot retrieval,
troubleshooting assistants, onboarding systems, semantic publication, visual
assistance, contextual rendering, RAG — is **subordinate to the knowledge
core** and bound by this charter.

## Multilingual support

- Baseline locale: `es-CO`.
- Localized variants append a BCP-47 tag to artifact IDs (e.g.
  `term-fingerprint.en-US`).
- Canonical terminology is locale-independent; localized labels live as
  variants of the canonical term.

## Chatbot / RAG

- Serve `verified` and `canonical` only by default.
- Surface provenance (OEM evidence id + span).
- Use synonym expansion via the canonical-terminology registry.
- Apply consumer-side maturity gates.

## Troubleshooting assistant

- Traverse procedure / warning / troubleshooting graph.
- Respect maturity gates; allow `inferred` with explicit confidence label.

## Onboarding

- Traverse workflow graph (pairing, enrolment, first-use).
- Serve only `canonical` / `verified`.

## Visual assistance / contextual rendering

- Bound by the visual constitution
  (`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) and the runtime governance
  (`visual-system/_governance/`).
- Conditioned on the canonical PNG; never originates knowledge.

## Out of scope

- Generated images, Comfy execution, prompt generation, manual rendering,
  publication system construction. These belong to later phases and are
  bound by the visual + knowledge constitutions.
"""


def doc_index() -> str:
    return f"""# Beslock Semantic Governance

_Schema: `{SCHEMA}` · index · generated {NOW}._

This folder is the **constitutional layer of semantic governance**. The
authoritative semantic content remains per-product under
`ext-images/<slug>/knowledge-core/`; this folder governs *how* that content
is named, normalized, classified, conflict-managed and retrieved.

## Documents

- [`00-charter.md`](00-charter.md)
- [`canonical-terminology/canonical-terminology.md`](canonical-terminology/canonical-terminology.md)
- [`canonical-terminology/canonical-terminology.json`](canonical-terminology/canonical-terminology.json)
- [`procedural-normalization/procedural-normalization.md`](procedural-normalization/procedural-normalization.md)
- [`procedural-normalization/procedural-normalization.json`](procedural-normalization/procedural-normalization.json)
- [`semantic-identifiers/identifier-grammar.md`](semantic-identifiers/identifier-grammar.md)
- [`semantic-identifiers/identifier-grammar.json`](semantic-identifiers/identifier-grammar.json)
- [`semantic-conflicts/semantic-conflicts.md`](semantic-conflicts/semantic-conflicts.md)
- [`semantic-conflicts/semantic-conflicts.json`](semantic-conflicts/semantic-conflicts.json)
- [`maturity-governance/maturity-governance.md`](maturity-governance/maturity-governance.md)
- [`maturity-governance/maturity-policies.json`](maturity-governance/maturity-policies.json)
- [`retrieval-governance/retrieval-governance.md`](retrieval-governance/retrieval-governance.md)
- [`retrieval-governance/retrieval-governance.json`](retrieval-governance/retrieval-governance.json)
- [`cross-product-governance/cross-product-coherence.md`](cross-product-governance/cross-product-coherence.md)
- [`cross-product-governance/cross-product-coherence.json`](cross-product-governance/cross-product-coherence.json)
- [`future-readiness/future-readiness.md`](future-readiness/future-readiness.md)

## Sibling constitutional layers

- Visual governance: [`../VISUAL_GOVERNANCE/00-CONSTITUTION.md`](../VISUAL_GOVERNANCE/00-CONSTITUTION.md)
- Knowledge center: [`../KNOWLEDGE_CENTER/00-architecture.md`](../KNOWLEDGE_CENTER/00-architecture.md)

## Hard guarantees

- No artifact under `ext-images/<slug>/knowledge-core/` was modified.
- No governance file under `visual-system/_governance/` was modified.
- No Comfy / orchestration / visual-generation file was modified.
- No image was generated.
- All conflicts detected by this phase are reported, never auto-resolved.
"""


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)


def main() -> int:
    SG.mkdir(parents=True, exist_ok=True)
    by_domain = scan()
    variant_to_canonical, canonical_to_variants = build_synonym_lookup()
    conflicts = detect_conflicts(by_domain, variant_to_canonical)

    # Charter + doctrines.
    write(SG / "README.md", doc_index())
    write(SG / "00-charter.md", doc_charter())
    write(SG / "canonical-terminology/canonical-terminology.md", doc_terminology(SYNONYM_GROUPS))
    write(SG / "procedural-normalization/procedural-normalization.md", doc_procedural())
    write(SG / "semantic-identifiers/identifier-grammar.md", doc_identifiers())
    write(SG / "semantic-conflicts/semantic-conflicts.md", doc_conflicts(conflicts))
    write(SG / "maturity-governance/maturity-governance.md", doc_maturity_governance())
    write(SG / "retrieval-governance/retrieval-governance.md", doc_retrieval_governance())
    write(SG / "cross-product-governance/cross-product-coherence.md", doc_cross_product())
    write(SG / "future-readiness/future-readiness.md", doc_future())

    # Machine-readable companions.
    write(
        SG / "canonical-terminology/canonical-terminology.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "groups": [
                {"canonical": g["canonical"], "domain": g["domain"],
                 "synonyms": [slugify(s) for s in g["synonyms"]]}
                for g in SYNONYM_GROUPS
            ],
            "variant_to_canonical": variant_to_canonical,
            "canonical_to_variants": canonical_to_variants,
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "procedural-normalization/procedural-normalization.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "canonical_verbs": CANONICAL_VERBS,
            "verb_synonyms": VERB_SYNONYMS,
            "state_vocabulary": [
                "unlocked", "locked", "paired", "unpaired", "enrolled",
                "removed", "factory-default", "low-battery", "lockout",
                "firmware-updating",
            ],
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "semantic-identifiers/identifier-grammar.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "grammar_regex": ID_GRAMMAR.pattern,
            "domain_prefixes": {
                "terminology":          ["term-"],
                "entities":             ["entity-"],
                "warnings":             ["warning-"],
                "capabilities":         ["capability-", "cap-"],
                "specifications":       ["spec-", "specification-"],
                "workflows":            ["workflow-", "wf-", "semantic-wf-"],
                "procedures":           ["procedure-", "semantic-proc-"],
                "procedural-semantics": ["semantic-proc-", "semantic-wf-"],
                "visual-intent":        ["intent-", "visual-intent-"],
                "visual-risk":          ["risk-", "visual-risk-"],
                "publication-intent":   ["publication-", "publication-intent-"],
                "component-visibility": ["component-"],
                "provenance":           ["prov-", "provenance-"],
            },
            "stability_rules": [
                "Published IDs are immutable.",
                "Deprecated IDs become synonyms; never silently dropped.",
                "Renames require <old>.lineage.json receipts.",
                "Cross-product links use canonical concept IDs only.",
            ],
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "semantic-conflicts/semantic-conflicts.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "categories": {k: len(v) for k, v in conflicts.items()},
            "items": conflicts,
            "policy": "Conflicts are reported, not resolved. Editorial owns resolution.",
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "maturity-governance/maturity-policies.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "required_field": "maturity",
            "default_when_absent": "unresolved",
            "promotion_table": [
                {"from": "absent",      "to": "unresolved",     "evidence": "auto"},
                {"from": "ocr-derived", "to": "inferred",       "evidence": "reviewer note + cross-evidence link"},
                {"from": "inferred",    "to": "canonical",      "evidence": "OEM evidence + reviewer approval"},
                {"from": "canonical",   "to": "verified",       "evidence": "second OEM source OR field confirmation"},
                {"from": "any",         "to": "deprecated",     "evidence": "replacement artifact id"},
                {"from": "any",         "to": "low-confidence", "evidence": "reviewer downgrade note"},
                {"from": "any",         "to": "transitional",   "evidence": "migration target + ETA"},
            ],
            "invariants": [
                "verified ⇒ ≥1 OEM evidence span",
                "canonical ⇒ ≥1 evidence pointer",
                "deprecated ⇒ replacement reference",
                "transitional ⇒ migration target",
                "low-confidence ⇒ confidence_note",
            ],
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "retrieval-governance/retrieval-governance.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "stability_contracts": [
                "index source patterns are governed",
                "served fields are minimum surface",
                "identifier grammar is governed",
                "synonym expansion via canonical-terminology",
                "maturity gates applied at consumer",
            ],
            "minimum_served_fields": ["id", "maturity", "provenance", "last_updated", "channel_targets"],
            "discoverability_paths": ["direct id", "shared-concept lookup", "product-level enumeration"],
        }, ensure_ascii=False, indent=2),
    )

    write(
        SG / "cross-product-governance/cross-product-coherence.json",
        json.dumps({
            "schema_version": SCHEMA, "generated_at": NOW,
            "archetypes": [
                {"id": "archetype.pairing",     "members": ["pair-with-app", "qr-pairing", "ez-mode-pairing"]},
                {"id": "archetype.enrolment",   "members": ["register-fingerprint", "register-pin", "add-administrator", "add-user"]},
                {"id": "archetype.recovery",    "members": ["factory-reset", "emergency-power", "battery-replacement"]},
                {"id": "archetype.operational", "members": ["unlock-pin", "unlock-fingerprint", "unlock-app", "unlock-mechanical"]},
                {"id": "archetype.maintenance", "members": ["firmware-update", "battery-replacement"]},
            ],
            "promotion_rule": "Promote a concept to shared once observed in ≥2 products with reviewer-confirmed semantic equivalence.",
            "anti_contamination_rules": [
                "No silent inheritance of fields between products",
                "No per-product cross-references except via shared concept IDs",
                "Borrowed text requires reviewer note + product-specific provenance",
            ],
        }, ensure_ascii=False, indent=2),
    )

    # ----- Reports -----
    rep_dir = GOV_REPO / "reports" / "semantic-governance"
    rep_dir.mkdir(parents=True, exist_ok=True)

    def report(name: str, payload: dict) -> None:
        (rep_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    # 1
    report("01-terminology-normalization-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "groups_count": len(SYNONYM_GROUPS),
        "variants_count": sum(len(g["synonyms"]) for g in SYNONYM_GROUPS),
        "canonical_terms": [g["canonical"] for g in SYNONYM_GROUPS],
        "registry_doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/canonical-terminology/canonical-terminology.md",
        "registry_json": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/canonical-terminology/canonical-terminology.json",
    })

    # 2
    report("02-procedural-normalization-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "canonical_verb_count": len(CANONICAL_VERBS),
        "verb_synonym_count": len(VERB_SYNONYMS),
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/procedural-normalization/procedural-normalization.md",
    })

    # 3
    report("03-semantic-id-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "grammar_regex": ID_GRAMMAR.pattern,
        "prefix_domains_count": 13,
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-identifiers/identifier-grammar.md",
    })

    # 4
    report("04-conflict-detection-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "category_counts": {k: len(v) for k, v in conflicts.items()},
        "total_conflicts_recorded": sum(len(v) for v in conflicts.values()),
        "policy": "Conflicts surfaced; never auto-resolved.",
        "register_doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-conflicts/semantic-conflicts.md",
        "register_json": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-conflicts/semantic-conflicts.json",
    })

    # 5
    report("05-maturity-governance-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "required_field": "maturity",
        "default_when_absent": "unresolved",
        "promotion_paths_count": 7,
        "invariants_count": 5,
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/maturity-governance/maturity-governance.md",
    })

    # 6
    report("06-retrieval-governance-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "stability_contracts_count": 5,
        "minimum_served_fields": ["id", "maturity", "provenance", "last_updated", "channel_targets"],
        "discoverability_paths_count": 3,
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/retrieval-governance/retrieval-governance.md",
    })

    # 7
    report("07-cross-product-coherence-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "archetype_count": 5,
        "anti_contamination_rules_count": 3,
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/cross-product-governance/cross-product-coherence.md",
    })

    # 8
    report("08-governance-charter-summary.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "principle_count": 9,
        "authority_areas_count": 11,
        "doc": "KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/00-charter.md",
    })

    # 9 — unresolved semantic risks (synthesised from conflicts + carry-over).
    risks = []
    if conflicts["bilingual-duplication"]:
        risks.append({"id": "risk.bilingual-duplication", "severity": "medium",
                      "count": len(conflicts["bilingual-duplication"]),
                      "note": "Concepts present in both English and Spanish artifact slugs in the same product nucleus."})
    if conflicts["ambiguous-procedure-naming"]:
        risks.append({"id": "risk.ambiguous-procedure-naming", "severity": "medium",
                      "count": len(conflicts["ambiguous-procedure-naming"]),
                      "note": "Same target addressed with multiple action verbs."})
    if conflicts["synonym-duplication"]:
        risks.append({"id": "risk.synonym-duplication", "severity": "medium",
                      "count": len(conflicts["synonym-duplication"]),
                      "note": "Artifact local IDs are synonyms of canonical terms."})
    if conflicts["duplicate-entity-within-product"]:
        risks.append({"id": "risk.duplicate-within-product", "severity": "high",
                      "count": len(conflicts["duplicate-entity-within-product"]),
                      "note": "Two artifacts collapse to the same canonical id inside one product."})
    risks += [
        {"id": "risk.maturity-field-absent",          "severity": "high",   "note": "maturity field is required by doctrine but most existing artifacts have not been backfilled."},
        {"id": "risk.shared-concept-membership-empty","severity": "medium", "note": "shared-concept-membership.json is specified but unpopulated; cross-product retrieval cannot run."},
        {"id": "risk.discoverability-orphans-unaudited","severity": "low", "note": "Orphan-detection audit not implemented yet; currently only declared as a contract."},
        {"id": "risk.embeddings-strategy-missing",    "severity": "low",    "note": "Embedding model + store identity not declared; future RAG cannot freeze its surface."},
        {"id": "risk.publication-channel-spec-draft", "severity": "high",   "note": "Per-channel publication specs remain draft (carry-over from Phase 6)."},
    ]
    report("09-unresolved-semantic-risks.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "risks_count": len(risks),
        "risks": risks,
    })

    # 10
    report("10-future-knowledge-system-readiness.json", {
        "schema_version": SCHEMA, "generated_at": NOW,
        "ready_for": [
            "editorial conflict-resolution sweeps",
            "maturity-field backfill phase",
            "shared-concept tagging phase",
            "synonym-expansion at retrieval time",
            "downstream consumer integration with stable identifier grammar",
        ],
        "not_ready_for": [
            "production multilingual publication (BCP-47 variants not yet authored)",
            "RAG / embeddings (embedding strategy undeclared)",
            "automated knowledge QA in CI (audit jobs not wired)",
            "mass image generation (carry-over: visual constitution + workflow registry blockers)",
        ],
        "subordination_rule": "All future surfaces remain subordinate to the knowledge core; none originates knowledge.",
    })

    print("Semantic governance promotion complete.")
    print(f"  Constitutional root: {SG.relative_to(REPO).as_posix()}")
    print(f"  Reports:             {rep_dir.relative_to(REPO).as_posix()}/01..10")
    print(f"  Conflict counts:     {{ {', '.join(f'{k}: {len(v)}' for k, v in conflicts.items())} }}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
