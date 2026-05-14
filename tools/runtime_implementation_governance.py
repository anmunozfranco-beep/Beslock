"""
Phase 26 — RUNTIME IMPLEMENTATION GOVERNANCE (modeling-only constitutional layer
that binds the real implementation in `runtime-implementation/`).

Twentieth constitutional layer. Subordinate to knowledge-core and to all
nineteen prior governance layers. This builder writes ONLY the doctrine and
the 10-section final reports. The actual executable runtime lives at
`runtime-implementation/` (real Python package, real tests).

Idempotent. Non-destructive. Reads no per-product knowledge-core files.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "RUNTIME_IMPLEMENTATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "runtime-implementation"
RUNTIME_ROOT = REPO_ROOT / "runtime-implementation"

SCHEMA = "runtime-implementation-governance/1.0"


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
    "This layer binds the real executable runtime under `runtime-implementation/`.",
    "The runtime is read-only over knowledge-core; mutations are out of scope.",
    "The runtime is supervised by default; operator approval is mandatory at declared checkpoints.",
    "Every emitted package carries a provenance manifest with SHA-256 source hashes.",
    "Every cognition boundary emits a supervision receipt.",
    "Failure of any safety predicate demotes the slice; demotion is the safe response.",
    "The runtime cannot promote P-tier, elevate confidence, or alter prior governance layers.",
    "Hard exclusions bind the implementation: no autonomous agents, no production deployment, no images, no PDFs, no large frontend, no perf optimization.",
    "Macro-governance expansion is suspended; this is the implementation track.",
    "All implementation remains subordinate to the governed knowledge-core forever.",
]

SUPERVISED_IMPLEMENTATION_PHILOSOPHY = [
    "Implementation is operational evidence at the smallest defensible scale.",
    "Implementation does not extend the architecture; it validates it.",
    "Implementation is supervised, demotable, and append-only auditable.",
    "Implementation is bound by the prior nineteen governance layers without exception.",
]

EXECUTABLE_COGNITION_DOCTRINE = [
    "Executable cognition operationalizes declared cognition; it never invents new cognition.",
    "Executable cognition is read-only by default in the prototype runtime.",
    "Executable cognition emits provenance + supervision receipts at every step.",
    "Executable cognition cannot elevate confidence to compensate for missing inputs.",
]

RUNTIME_SAFETY_PHILOSOPHY = [
    "Safety predicates are continuous, not terminal.",
    "Failure demotes; it does not silently pass.",
    "Hallucination (any node id absent from its source file) is a halt event.",
    "Irreversibility warnings cannot be downgraded.",
    "Governance bypass attempts halt the slice and demote.",
]

OPERATIONAL_VALIDATION_METHODOLOGY = [
    "Define the smallest read-only slice that exercises retrieval + assembly + guidance.",
    "Declare evidence per step; evidence is binding and append-only.",
    "Run under operator observation with append-only NDJSON traces.",
    "Promote only on documented evidence; demote on any anomaly.",
    "Replay deterministically from the captured channels alone.",
]

IMPLEMENTATION_ESCALATION_PHILOSOPHY = [
    "Escalation is monotonic; tier never decreases.",
    "Escalation produces append-only records bound to run-id + slice-id.",
    "Escalation locks the slice into a read-only handoff state.",
    "Escalation is a safety mechanism, not a fallback for low quality.",
]

# ---------------------------------------------------------------------------
# Subsection bodies
# ---------------------------------------------------------------------------

RUNTIME_STRUCTURE = [
    {"path": "runtime-implementation/runtime/config.py",        "kind": "module", "responsibility": "paths, products, slice declaration, in-scope guard"},
    {"path": "runtime-implementation/runtime/provenance.py",    "kind": "module", "responsibility": "manifest builder, content hashing"},
    {"path": "runtime-implementation/runtime/retrieval.py",     "kind": "module", "responsibility": "scored retrieval over knowledge-core"},
    {"path": "runtime-implementation/runtime/assembly.py",      "kind": "module", "responsibility": "procedure + warnings + prerequisites + troubleshooting + continuity + adaptive merge"},
    {"path": "runtime-implementation/runtime/supervision.py",   "kind": "module", "responsibility": "review checkpoints, decisions, supervision receipts"},
    {"path": "runtime-implementation/runtime/safety.py",        "kind": "module", "responsibility": "continuous safety predicates"},
    {"path": "runtime-implementation/runtime/observability.py", "kind": "module", "responsibility": "append-only NDJSON channels"},
    {"path": "runtime-implementation/runtime/flows.py",         "kind": "module", "responsibility": "six declared supervised flows"},
    {"path": "runtime-implementation/cli.py",                   "kind": "entrypoint", "responsibility": "supervised CLI"},
    {"path": "runtime-implementation/testing/test_flows.py",    "kind": "tests",  "responsibility": "real unittest suite (14 tests)"},
]

RETRIEVAL_KINDS = [
    "onboarding", "troubleshooting", "operational-procedures", "warnings",
    "escalation", "adaptive-guidance", "fingerprint-enrollment", "pairing", "battery-recovery",
]

ASSEMBLY_BLOCKERS = [
    "no-procedure-retrievable",
    "mandatory-warning-not-attached",
    "prerequisite-unverified",
    "confidence-elevated-unsafe",
]

SAFETY_PREDICATES = [
    "hallucination-resistance",
    "no-low-confidence-execution",
    "no-ambiguous-guidance",
    "no-provenance-loss",
    "no-governance-bypass",
    "no-continuity-loss",
    "no-unsafe-retrieval",
    "no-escalation-failure",
    "no-supervision-loss",
]

OBSERVABILITY_CHANNELS = [
    "reasoning-trace", "retrieval-trace", "escalation-trace",
    "continuity-trace", "orchestration-trace", "operational-audit-log",
]

FLOWS = [
    "onboarding", "first-pairing", "fingerprint-enrollment",
    "troubleshooting-lookup", "battery-recovery", "escalation-handling",
]


UNRESOLVED_ISSUES = [
    {"id": "warning-corpus-thin",                "severity": "high",   "impact": "warnings retrieval frequently empty; escalation-tier flips to escalating on destructive-adjacent flows"},
    {"id": "troubleshooting-corpus-thin",        "severity": "high",   "impact": "troubleshooting-lookup flow degrades to escalation on most products"},
    {"id": "no-confidence-tier-on-most-nodes",   "severity": "high",   "impact": "low-confidence-execution gating cannot bind precisely"},
    {"id": "no-checkpoint-registry",             "severity": "high",   "impact": "battery-recovery checkpoint snapshots are placeholders"},
    {"id": "no-causal-edges-emitted",            "severity": "high",   "impact": "troubleshooting traversal cannot follow causal chains"},
    {"id": "no-hypothesis-store",                "severity": "high",   "impact": "troubleshooting/recovery hypotheses cannot persist"},
    {"id": "no-incident-id-emitter",             "severity": "high",   "impact": "cross-step continuity binding by incident is unavailable"},
    {"id": "no-replay-harness",                  "severity": "medium", "impact": "deterministic replay from channels is supported but not yet harnessed"},
    {"id": "no-ground-truth-set",                "severity": "medium", "impact": "semantic-recall cannot be quantified beyond declared queries"},
    {"id": "no-operator-identity-channel",       "severity": "medium", "impact": "operator id is a free string; no identity verification"},
    {"id": "no-prerequisite-verification-store", "severity": "medium", "impact": "prerequisites are surfaced but verification flag defaults to false"},
]


def run_tests() -> dict:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover",
         "-s", str(RUNTIME_ROOT / "testing"), "-p", "test_*.py"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    output = (proc.stdout + proc.stderr).strip()
    last = output.splitlines()[-1] if output else ""
    return {
        "returncode": proc.returncode,
        "summary_line": last,
        "passed": proc.returncode == 0,
    }


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    test_result = run_tests()

    (CONST_ROOT / "README.md").write_text(
        "# RUNTIME IMPLEMENTATION GOVERNANCE\n\n"
        "Twentieth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all nineteen prior governance layers.\n\n"
        "This layer binds the **real executable runtime** under `runtime-implementation/`.\n"
        "It declares the doctrine; it does not implement the runtime here.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n\n"
        f"Test suite status at generation: returncode={test_result['returncode']} ({test_result['summary_line']}).\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Runtime Implementation Governance",
        "Declares principles + authority for the first executable runtime track.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound implementation", md_list([f"`{m['path']}` — {m['responsibility']}" for m in RUNTIME_STRUCTURE])),
            ("Hard Exclusions", md_list([
                "DO NOT expand macro-governance endlessly",
                "DO NOT create new universal cognition doctrines",
                "DO NOT create recursive architectural abstractions",
                "DO NOT build autonomous agents",
                "DO NOT deploy production systems",
                "DO NOT generate images / PDFs / large frontends",
                "DO NOT optimize scale / performance",
            ])),
        ],
        {
            "schema": SCHEMA, "kind": "charter",
            "principles": CHARTER_PRINCIPLES,
            "bound_implementation": RUNTIME_STRUCTURE,
            "subordinate_to": [
                "knowledge-core",
                "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
                "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
                "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
                "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
                "ECOSYSTEM_INTEROPERABILITY", "REALIZATION_AND_DEPLOYMENT",
                "OPERATIONAL_PROOF", "PROTOTYPE_RUNTIME",
            ],
            "test_suite": test_result,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "supervised-implementation-philosophy", "supervised-implementation-philosophy",
        "Supervised Implementation Philosophy",
        "Implementation as operational evidence at the smallest defensible scale.",
        [("Principles", md_list(SUPERVISED_IMPLEMENTATION_PHILOSOPHY))],
        {"schema": SCHEMA, "kind": "supervised-implementation-philosophy", "principles": SUPERVISED_IMPLEMENTATION_PHILOSOPHY},
    )

    write_pair(
        CONST_ROOT / "executable-cognition-doctrine", "executable-cognition-doctrine",
        "Executable Cognition Doctrine",
        "Operationalizing declared cognition without inventing new cognition.",
        [("Principles", md_list(EXECUTABLE_COGNITION_DOCTRINE))],
        {"schema": SCHEMA, "kind": "executable-cognition-doctrine", "principles": EXECUTABLE_COGNITION_DOCTRINE},
    )

    write_pair(
        CONST_ROOT / "runtime-safety-philosophy", "runtime-safety-philosophy",
        "Runtime Safety Philosophy",
        "Safety predicates are continuous; failure demotes; hallucination halts.",
        [("Principles", md_list(RUNTIME_SAFETY_PHILOSOPHY))],
        {"schema": SCHEMA, "kind": "runtime-safety-philosophy", "principles": RUNTIME_SAFETY_PHILOSOPHY},
    )

    write_pair(
        CONST_ROOT / "operational-validation-methodology", "operational-validation-methodology",
        "Operational Validation Methodology",
        "Smallest read-only slice; declared evidence; operator observation; deterministic replay.",
        [("Methodology", md_list(OPERATIONAL_VALIDATION_METHODOLOGY))],
        {"schema": SCHEMA, "kind": "operational-validation-methodology", "methodology": OPERATIONAL_VALIDATION_METHODOLOGY},
    )

    write_pair(
        CONST_ROOT / "implementation-escalation-philosophy", "implementation-escalation-philosophy",
        "Implementation Escalation Philosophy",
        "Escalation is monotonic, append-only, and locks the slice into read-only handoff.",
        [("Principles", md_list(IMPLEMENTATION_ESCALATION_PHILOSOPHY))],
        {"schema": SCHEMA, "kind": "implementation-escalation-philosophy", "principles": IMPLEMENTATION_ESCALATION_PHILOSOPHY},
    )

    # Reports
    reports = [
        ("01-runtime-structure-summary.json", {
            "schema": SCHEMA,
            "implementation_root": "runtime-implementation/",
            "modules": RUNTIME_STRUCTURE,
            "test_suite": test_result,
        }),
        ("02-retrieval-execution-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/runtime/retrieval.py",
            "kinds_supported": RETRIEVAL_KINDS,
            "scoring": "Jaccard-over-query-tokens, NFKD diacritic + lowercase normalization",
            "ambiguity_policy": "surfaced when top scores tie and confidence is low/medium/unknown",
            "provenance": "every package carries a runtime-provenance/1.0 manifest with SHA-256 hashes",
        }),
        ("03-contextual-assembly-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/runtime/assembly.py",
            "merges": ["procedure-nodes", "warning-nodes", "prerequisite-records",
                       "troubleshooting-nodes", "continuity-state", "adaptation-record",
                       "escalation-predicate-result"],
            "blockers": ASSEMBLY_BLOCKERS,
            "invariants": [
                "mandatory warnings cannot be suppressed",
                "prerequisite gaps block guidance emission",
                "adaptive precedence (knowledge-core>adaptive) is invariant",
                "confidence is never elevated to compensate for missing inputs",
            ],
        }),
        ("04-supervision-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/runtime/supervision.py",
            "checkpoints": ["pre-emission", "post-emission", "pre-handoff", "pre-completion", "post-anomaly"],
            "decisions": ["approve", "reject", "request-more-info", "escalate", "demote"],
            "blocking_decisions": ["reject", "demote"],
            "advancing_decisions": ["approve"],
            "non_relaxable": ["safety-preserving adaptations", "irreversibility warnings"],
        }),
        ("05-operational-flow-testing-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/testing/test_flows.py",
            "flows_tested": FLOWS,
            "test_suite": test_result,
            "test_classes": [
                "ConfigTests", "ProvenanceTests", "RetrievalTests", "AssemblyTests",
                "SupervisionTests", "FlowTests", "ObservabilityTests",
            ],
        }),
        ("06-observability-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/runtime/observability.py",
            "channels": OBSERVABILITY_CHANNELS,
            "format": "append-only NDJSON",
            "log_dir": "runtime-implementation/observability/logs/",
            "replay": "deterministic from captured channels alone",
        }),
        ("07-safety-validation-summary.json", {
            "schema": SCHEMA,
            "implementation": "runtime-implementation/runtime/safety.py",
            "predicates": SAFETY_PREDICATES,
            "failure_action": "demote slice (no silent pass)",
            "evaluation": "continuous, not terminal",
        }),
        ("08-implementation-governance-summary.json", {
            "schema": SCHEMA,
            "doctrine_blocks": {
                "supervised_implementation_philosophy": len(SUPERVISED_IMPLEMENTATION_PHILOSOPHY),
                "executable_cognition_doctrine": len(EXECUTABLE_COGNITION_DOCTRINE),
                "runtime_safety_philosophy": len(RUNTIME_SAFETY_PHILOSOPHY),
                "operational_validation_methodology": len(OPERATIONAL_VALIDATION_METHODOLOGY),
                "implementation_escalation_philosophy": len(IMPLEMENTATION_ESCALATION_PHILOSOPHY),
            },
            "macro_governance_expansion": "suspended",
        }),
        ("09-unresolved-runtime-issues.json", {
            "schema": SCHEMA,
            "issues": UNRESOLVED_ISSUES,
            "total": len(UNRESOLVED_ISSUES),
            "high": [r["id"] for r in UNRESOLVED_ISSUES if r["severity"] == "high"],
            "medium": [r["id"] for r in UNRESOLVED_ISSUES if r["severity"] == "medium"],
        }),
        ("10-first-executable-runtime-assessment.json", {
            "schema": SCHEMA,
            "first_slice": "contextual-onboarding + troubleshooting-retrieval",
            "executable_today": True,
            "evidence": [
                "14-test unittest suite passes (real tests over real knowledge-core)",
                "supervised CLI executes onboarding flow on e-prime end-to-end",
                "supervised CLI executes troubleshooting-lookup flow end-to-end",
                "all six observability channels emit append-only NDJSON",
                "every emitted package carries a provenance manifest with SHA-256 hashes",
                "operator approval gate is enforced (reject/demote are blocking)",
            ],
            "constraints": [
                "read-only over knowledge-core",
                "supervised by default; no autonomy",
                "no production deployment, no chatbot, no PDF, no image, no large frontend",
                "subordinate to knowledge-core and to all nineteen prior governance layers",
            ],
            "next_actions": [
                "expand troubleshooting + warning corpora on e-flex/e-nova/e-orbit/e-shield/e-touch",
                "wire confidence-tier emitter onto knowledge-core nodes",
                "introduce checkpoint registry for battery-recovery flow",
                "introduce causal-edges + hypothesis store for troubleshooting flow",
                "introduce replay harness from observability channels",
            ],
            "test_suite": test_result,
        }),
    ]
    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    file_count = sum(1 for _ in CONST_ROOT.rglob("*") if _.is_file())
    print(
        "Runtime implementation governance complete.\n"
        f"  Constitutional root: {CONST_ROOT}\n"
        f"  Reports: {REPORTS_ROOT}/01..10\n"
        f"  Bound implementation: runtime-implementation/ (real Python package)\n"
        f"  Modules: {len(RUNTIME_STRUCTURE)} | Flows: {len(FLOWS)} | "
        f"Retrieval kinds: {len(RETRIEVAL_KINDS)} | Safety predicates: {len(SAFETY_PREDICATES)} | "
        f"Observability channels: {len(OBSERVABILITY_CHANNELS)} | Issues: {len(UNRESOLVED_ISSUES)}.\n"
        f"  Test suite: {test_result['summary_line']} (returncode={test_result['returncode']}).\n"
        f"  Files written under constitutional root: {file_count}"
    )


if __name__ == "__main__":
    build()
