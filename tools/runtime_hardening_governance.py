"""
Phase 27 — RUNTIME HARDENING GOVERNANCE (constitutional layer 21).

Twenty-first constitutional layer. Subordinate to knowledge-core and to
all twenty prior governance layers. Binds:
- the additive corpus enrichment under each product's
  `knowledge-core/{troubleshooting-expanded,warnings-expanded,
  continuity-checkpoints,causal-graphs,confidence-tiers}/`,
- the runtime hardening modules under
  `runtime-implementation/runtime-hardening/`,
- the new replay harness `runtime-implementation/runtime/replay.py`.

Modeling-only here; the executable changes live in `runtime-implementation/`
and the additive candidate records live per-product. Idempotent.
Non-destructive. Reads no per-product knowledge-core JSON.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "RUNTIME_HARDENING_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "runtime-hardening"
RUNTIME_ROOT = REPO_ROOT / "runtime-implementation"
EXT_ROOT = THEME_ROOT / "ext-images"
PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

SCHEMA = "runtime-hardening-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items):
    return "\n".join(f"- {x}" for x in items)


def write_pair(folder: Path, slug: str, title: str, intro: str, sections, payload: dict):
    folder.mkdir(parents=True, exist_ok=True)
    md = [f"# {title}", "", intro, ""]
    for h, body in sections:
        md += [f"## {h}", "", body, ""]
    (folder / f"{slug}.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    (folder / f"{slug}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Doctrine
# ---------------------------------------------------------------------------

CHARTER_PRINCIPLES = [
    "This layer hardens the runtime; it does not extend the architecture.",
    "Hardening is additive and non-destructive over per-product knowledge-core.",
    "Operational density is increased through declared candidate records, never fabricated truth.",
    "Every candidate record carries `validation_status: candidate-pending-review` and `confidence: candidate`.",
    "Confidence weighting is declarative; candidate nodes cannot outrank verified nodes on equal token overlap.",
    "Replay is deterministic by node-id-set parity, not by timing or score arithmetic.",
    "Macro-governance expansion remains suspended; this is the second and final implementation-track layer of Phase 27.",
    "All hardening is subordinate to knowledge-core and to all twenty prior layers.",
]

CORPUS_HARDENING_PHILOSOPHY = [
    "Operational depth is a corpus property, not a runtime trick.",
    "Density is added through additive supplemental folders; canonical records are never edited.",
    "Every supplemental record is reviewable, demotable, and replaceable.",
    "Candidate confidence is honest: it ranks low and is surfaced as a soft escalation signal.",
]

TROUBLESHOOTING_ENRICHMENT_DOCTRINE = [
    "Troubleshooting candidates declare a symptom category, an evidence requirement, and an escalation policy.",
    "Troubleshooting candidates do not invent device behavior; they declare lookup slots.",
    "Troubleshooting retrieval routes through both canonical and `troubleshooting-expanded` folders.",
    "Candidate-only troubleshooting hits raise the `troubleshooting-candidate-only` escalation trigger.",
]

CONFIDENCE_DISCLOSURE_DOCTRINE = [
    "Confidence is a tier, not a number-from-thin-air.",
    "Tiers are declared per product in `confidence-tiers/confidence-tier-manifest-<product>.json`.",
    "Runtime ranking weights confidence as a declarative multiplier over Jaccard.",
    "Candidate-only retrieval is honestly disclosed in the package manifest (`extra.candidate_only=True`).",
]

DETERMINISTIC_REPLAY_PHILOSOPHY = [
    "Replay is deterministic by node-id-set parity over captured retrieval-trace events.",
    "Synthetic empty packages are excluded from replay; they are not real retrieval calls.",
    "Replay is reporting-only: drift is surfaced, never auto-corrected.",
    "The captured NDJSON channels remain append-only ground truth.",
]

OPERATIONAL_DENSITY_PRINCIPLES = [
    "Density grows through declared categories, not free-form expansion.",
    "Each product receives the same category set; coverage gaps are visible by symmetry.",
    "Density never compromises the read-only posture over canonical knowledge-core.",
    "Density is bounded by the candidate-confidence ceiling until human review elevates a record.",
]

RUNTIME_MATURATION_METHODOLOGY = [
    "Identify the bottleneck (operational density, not architecture).",
    "Add additive supplemental corpus surfaces.",
    "Extend retrieval routing without weakening safety.",
    "Add a deterministic validator (replay) before claiming maturity.",
    "Govern the change as a single layer; do not spawn macro-governance.",
]

# ---------------------------------------------------------------------------
# Module + corpus references
# ---------------------------------------------------------------------------

HARDENING_MODULES = [
    {"path": "runtime-implementation/runtime/config.py",       "change": "ALLOWED_DOMAINS extended; CONFIDENCE_WEIGHTS table added"},
    {"path": "runtime-implementation/runtime/retrieval.py",    "change": "KIND_DOMAINS extended; confidence-weighted scoring; candidate_only manifest field"},
    {"path": "runtime-implementation/runtime/assembly.py",     "change": "candidate-only escalation triggers wired in"},
    {"path": "runtime-implementation/runtime/replay.py",       "change": "new module — deterministic replay harness"},
    {"path": "runtime-implementation/cli.py",                  "change": "new `replay` subcommand"},
    {"path": "runtime-implementation/testing/test_hardening.py", "change": "new tests for domains, weights, candidate disclosure, replay determinism"},
    {"path": "runtime-implementation/runtime-hardening/retrieval-quality/README.md", "change": "doctrine note for retrieval hardening"},
    {"path": "runtime-implementation/runtime-hardening/replay-validation/README.md", "change": "doctrine note for replay validation"},
    {"path": "tools/corpus_enrichment.py",                     "change": "additive supplemental corpus builder (idempotent)"},
]

CANDIDATE_DOMAINS = [
    "troubleshooting-expanded",
    "warnings-expanded",
    "continuity-checkpoints",
    "causal-graphs",
    "confidence-tiers",
]

UNRESOLVED_AFTER_HARDENING = [
    {"id": "candidate-records-not-yet-reviewed",     "severity": "high",   "impact": "all 132 records remain at `candidate-pending-review`; need human elevation"},
    {"id": "no-oem-source-binding-on-candidates",    "severity": "high",   "impact": "candidate records carry no OEM source_refs yet"},
    {"id": "no-incident-id-emitter",                 "severity": "high",   "impact": "cross-step continuity binding by incident is still unavailable"},
    {"id": "no-prerequisite-verification-store",     "severity": "high",   "impact": "prerequisite verification flag still defaults to false"},
    {"id": "no-causal-traversal-engine",             "severity": "medium", "impact": "causal-graphs are retrievable but not yet traversed during reasoning"},
    {"id": "no-checkpoint-snapshot-store",           "severity": "medium", "impact": "continuity-checkpoints are declared but not yet snapshotted at runtime"},
    {"id": "no-confidence-elevation-workflow",       "severity": "medium", "impact": "no governed path to promote a candidate to ocr-derived/verified"},
    {"id": "no-ground-truth-test-set",               "severity": "medium", "impact": "semantic-recall numerics still unmeasured"},
]


# ---------------------------------------------------------------------------
# Runtime helpers
# ---------------------------------------------------------------------------

def run_tests() -> dict:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover",
         "-s", str(RUNTIME_ROOT / "testing"), "-p", "test_*.py"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    output = (proc.stdout + proc.stderr).strip()
    last = output.splitlines()[-1] if output else ""
    return {"returncode": proc.returncode, "summary_line": last,
            "passed": proc.returncode == 0}


def count_candidate_records() -> dict:
    counts: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {d: 0 for d in CANDIDATE_DOMAINS}
    for product in PRODUCTS:
        kc = EXT_ROOT / product / "knowledge-core"
        per: dict[str, int] = {}
        for d in CANDIDATE_DOMAINS:
            n = len(list((kc / d).glob("*.json"))) if (kc / d).exists() else 0
            per[d] = n
            totals[d] += n
        counts[product] = per
    counts["_totals"] = totals
    counts["_grand_total"] = sum(totals.values())
    return counts


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    test_result = run_tests()
    candidate_counts = count_candidate_records()

    (CONST_ROOT / "README.md").write_text(
        "# RUNTIME HARDENING GOVERNANCE\n\n"
        "Twenty-first constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty prior governance layers.\n\n"
        "Binds the Phase 27 corpus enrichment + runtime hardening modules. "
        "Does not extend the architecture; it hardens the existing runtime.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n\n"
        f"Test suite at generation: returncode={test_result['returncode']} ({test_result['summary_line']}).\n\n"
        f"Candidate corpus records (grand total): {candidate_counts['_grand_total']}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Runtime Hardening Governance",
        "Declares principles + authority for the corpus + runtime hardening track.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound modules", md_list([f"`{m['path']}` — {m['change']}" for m in HARDENING_MODULES])),
            ("Bound corpus surfaces", md_list([f"`ext-images/<product>/knowledge-core/{d}/`" for d in CANDIDATE_DOMAINS])),
            ("Hard Exclusions", md_list([
                "DO NOT mutate any canonical per-product knowledge-core JSON",
                "DO NOT auto-promote candidate records",
                "DO NOT spawn macro-governance mega-layers",
                "DO NOT introduce stochastic ranking, ML, or embeddings",
                "DO NOT build autonomous agents",
                "DO NOT deploy production systems",
            ])),
        ],
        {
            "schema": SCHEMA, "kind": "charter",
            "principles": CHARTER_PRINCIPLES,
            "bound_modules": HARDENING_MODULES,
            "bound_corpus_surfaces": CANDIDATE_DOMAINS,
            "subordinate_to": [
                "knowledge-core",
                "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
                "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
                "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
                "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
                "ECOSYSTEM_INTEROPERABILITY", "REALIZATION_AND_DEPLOYMENT",
                "OPERATIONAL_PROOF", "PROTOTYPE_RUNTIME", "RUNTIME_IMPLEMENTATION",
            ],
            "test_suite": test_result,
            "candidate_record_counts": candidate_counts,
            "generated": now_iso(),
        },
    )

    for slug, title, intro, body_list in [
        ("corpus-hardening-philosophy", "Corpus Hardening Philosophy",
         "Operational depth is a corpus property, not a runtime trick.", CORPUS_HARDENING_PHILOSOPHY),
        ("troubleshooting-enrichment-doctrine", "Troubleshooting Enrichment Doctrine",
         "Symptom categories, evidence requirements, escalation policy — declared, not invented.",
         TROUBLESHOOTING_ENRICHMENT_DOCTRINE),
        ("confidence-disclosure-doctrine", "Confidence Disclosure Doctrine",
         "Confidence is a declared tier; candidate-only retrieval is honestly surfaced.",
         CONFIDENCE_DISCLOSURE_DOCTRINE),
        ("deterministic-replay-philosophy", "Deterministic Replay Philosophy",
         "Replay is node-id-set parity over append-only NDJSON channels.",
         DETERMINISTIC_REPLAY_PHILOSOPHY),
        ("operational-density-principles", "Operational Density Principles",
         "Density grows by declared categories, not free-form expansion.",
         OPERATIONAL_DENSITY_PRINCIPLES),
        ("runtime-maturation-methodology", "Runtime Maturation Methodology",
         "Identify the bottleneck, add additive surfaces, extend safely, validate deterministically, govern as one layer.",
         RUNTIME_MATURATION_METHODOLOGY),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(body_list))],
            {"schema": SCHEMA, "kind": slug, "principles": body_list},
        )

    # ----- 10 reports (verbatim ordering required by Phase 27) ---------------
    reports = [
        ("01-troubleshooting-expansion-summary.json", {
            "schema": SCHEMA, "kind": "troubleshooting-expansion-summary",
            "domain": "troubleshooting-expanded",
            "categories_per_product": [
                "pairing-failures", "enrollment-failures", "battery-issues",
                "connectivity-failures", "lock-state-inconsistencies",
                "administrator-access-recovery", "app-synchronization-issues",
            ],
            "records_per_product": {p: candidate_counts[p]["troubleshooting-expanded"] for p in PRODUCTS},
            "total_records": candidate_counts["_totals"]["troubleshooting-expanded"],
            "validation_status": "candidate-pending-review",
        }),
        ("02-warning-enrichment-summary.json", {
            "schema": SCHEMA, "kind": "warning-enrichment-summary",
            "domain": "warnings-expanded",
            "categories_per_product": [
                "operational", "irreversible-operation", "unsafe-state",
                "installation", "low-battery", "recovery", "escalation-required",
            ],
            "records_per_product": {p: candidate_counts[p]["warnings-expanded"] for p in PRODUCTS},
            "total_records": candidate_counts["_totals"]["warnings-expanded"],
            "validation_status": "candidate-pending-review",
        }),
        ("03-continuity-checkpoint-summary.json", {
            "schema": SCHEMA, "kind": "continuity-checkpoint-summary",
            "domain": "continuity-checkpoints",
            "checkpoint_kinds": [
                "onboarding", "pairing", "enrollment",
                "troubleshooting", "battery-replacement", "recovery",
            ],
            "records_per_product": {p: candidate_counts[p]["continuity-checkpoints"] for p in PRODUCTS},
            "total_records": candidate_counts["_totals"]["continuity-checkpoints"],
        }),
        ("04-causal-graph-summary.json", {
            "schema": SCHEMA, "kind": "causal-graph-summary",
            "domain": "causal-graphs",
            "structure": "symptom -> hypothesised-cause edges + hypothesis chains",
            "records_per_product": {p: candidate_counts[p]["causal-graphs"] for p in PRODUCTS},
            "total_records": candidate_counts["_totals"]["causal-graphs"],
            "consumed_by": "retrieval kind `causal` and `troubleshooting`",
        }),
        ("05-confidence-tier-summary.json", {
            "schema": SCHEMA, "kind": "confidence-tier-summary",
            "domain": "confidence-tiers",
            "tiers": [
                "verified-oem (1.00)", "verified-internal (0.95)",
                "ocr-derived (0.85)", "inferred-operational (0.65)",
                "candidate (0.40)", "unresolved (0.10)",
            ],
            "records_per_product": {p: candidate_counts[p]["confidence-tiers"] for p in PRODUCTS},
            "consumed_by": "retrieval scoring (Jaccard * confidence-weight)",
        }),
        ("06-retrieval-hardening-summary.json", {
            "schema": SCHEMA, "kind": "retrieval-hardening-summary",
            "module": "runtime-implementation/runtime/retrieval.py",
            "config": "runtime-implementation/runtime/config.py",
            "changes": [
                "ALLOWED_DOMAINS extended with the 5 supplemental domains",
                "CONFIDENCE_WEIGHTS table introduced (verified-oem=1.0 .. unresolved=0.10)",
                "KIND_DOMAINS routes troubleshooting/warnings/escalation/battery-recovery through supplemental folders",
                "scoring = Jaccard(query, node) * CONFIDENCE_WEIGHTS[node.confidence]",
                "manifest carries extra.candidate_only when top-K is candidate/unresolved only",
                "assembly raises procedure-candidate-only and troubleshooting-candidate-only triggers",
            ],
            "doctrine": "runtime-implementation/runtime-hardening/retrieval-quality/README.md",
        }),
        ("07-replay-validation-summary.json", {
            "schema": SCHEMA, "kind": "replay-validation-summary",
            "module": "runtime-implementation/runtime/replay.py",
            "cli": "runtime-implementation/cli.py replay",
            "contract": "node-id-set parity between captured and replayed retrieval-trace events",
            "synthetic_skip": "packages with manifest.extra.empty=True are skipped",
            "tests": [
                "testing/test_hardening.py::ReplayDeterminismTests::test_replay_run_is_deterministic",
                "testing/test_hardening.py::ReplayDeterminismTests::test_replay_summary_shape",
            ],
            "doctrine": "runtime-implementation/runtime-hardening/replay-validation/README.md",
        }),
        ("08-runtime-hardening-governance-summary.json", {
            "schema": SCHEMA, "kind": "runtime-hardening-governance-summary",
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/RUNTIME_HARDENING_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/runtime-hardening/",
            "layer_index": 21,
            "subordinate_to_count": 21,
            "test_suite": test_result,
        }),
        ("09-unresolved-corpus-weaknesses.json", {
            "schema": SCHEMA, "kind": "unresolved-corpus-weaknesses",
            "items": UNRESOLVED_AFTER_HARDENING,
        }),
        ("10-runtime-maturity-reassessment.json", {
            "schema": SCHEMA, "kind": "runtime-maturity-reassessment",
            "architecture_status": "SUFFICIENTLY MATURE (unchanged)",
            "operational_density_status": "MATERIALLY INCREASED (132 candidate records added)",
            "retrieval_status": "HARDENED (confidence-weighted, supplemental-aware)",
            "validation_status": "DETERMINISTIC REPLAY AVAILABLE",
            "remaining_bottleneck": "human review and elevation of candidate records to ocr-derived / verified tiers",
            "next_natural_track": "candidate-record review workflow + OEM source-binding ingestion",
            "test_suite": test_result,
            "candidate_record_counts": candidate_counts,
        }),
    ]

    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(f"Runtime Hardening Governance (layer 21) written to:\n  {CONST_ROOT}\n  {REPORTS_ROOT}")
    print(f"  candidate_records_grand_total = {candidate_counts['_grand_total']}")
    print(f"  test_suite                    = {test_result}")


if __name__ == "__main__":
    build()
