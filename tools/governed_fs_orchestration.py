"""
Phase 46 — GOVERNED FILESYSTEM INGESTION & REPOSITORY ORCHESTRATION.

Constitutional layer 39. Subordinate to layer 38
(executable-operational-bindings-governance) and to all thirty-eight prior
governance layers. This is the FIRST repo-native layer that enables REAL local
filesystem mutation — but only via a deterministic, reviewer-authorized,
append-only CLI executor (`tools/governed_fs_executor.py`). Browser surfaces
remain non-mutating: they propose, validate, and export operation-request
manifests; only the executor (run by the reviewer with --confirm) performs
actual copy / move / mkdir operations, and only under the safety rules
declared here.

NOT a SaaS, NOT a cloud architecture, NOT a backend, NOT an autonomous agent
platform, NOT a CI/CD pipeline, NOT an ML system, NOT a daemon. Stdlib-only,
local-first, deterministic, governance-first, repo-native.

This builder writes (idempotent, non-destructive, additive) under
`wp-content/themes/beslock-custom/User manuals/operational-console/`:

  staging/                              (governed staging roots — empty dirs)
    incoming/ review-pending/ accepted/
    rejected/ quarantined/ failed/
  runtime-manifests/                    (append-only event stores)
    intake-events/   routing-events/   mutation-events/   refresh-events/
    lineage-events/  rollback-events/  publication-events/ audit-events/
  execution-engine/                     (4 NEW deterministic rule tables)
    destination-resolution-rules.json
    mutation-safety-rules.json
    rollback-rules.json
    repository-safety-rules.json
  assets/exec/                          (5 NEW vanilla-ES engines)
    fs-bridge.js  dest-resolver.js  mutation-engine.js
    rollback-engine.js  safety-engine.js
  mutation-console/exec.html            (proposes mutation-request manifests)
  lineage-console/exec.html             (reads lineage event store)
  rollback-console/exec.html            (proposes rollback-request manifests)
  safety-console/exec.html              (reads safety violations)

Plus:
  KNOWLEDGE_BUILDING/GOVERNED_FILESYSTEM_ORCHESTRATION_GOVERNANCE/
    00-INDEX + 8 doctrines + manifest
  _repository-governance/reports/governed-filesystem-orchestration/
    10 reports

Hard rules (still enforced — extends layer 38):
  - The BROWSER surface NEVER touches the filesystem; it only emits operation
    requests as JSON downloads.
  - The CLI executor NEVER runs as a daemon; the reviewer invokes it
    explicitly with `--confirm`. There is no auto-execution, no watcher,
    no background process, no scheduled trigger, no autonomous agent.
  - Destructive overwrite is forbidden. If a destination exists, the op
    fails closed and the source is routed to staging/quarantined/.
  - Originals in staging/incoming/ are COPIED to canonical destinations
    (never moved by deletion); the original is then moved into
    staging/accepted/<timestamp>/ for audit retention.
  - All mutations emit (a) operation manifest, (b) lineage manifest,
    (c) audit entry — append-only, hashed, reviewer-attributed.
  - Knowledge-core, source-of-truth, runtime, publication, and governance
    state are NOT mutated by this builder. The executor may copy reviewer-
    classified evidence into ext-images/ext-videos/source documents trees
    only when a reviewer-authorized request explicitly targets them.
  - 19/19 runtime tests must remain green.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

OC_ROOT = THEME_ROOT / "operational-console"
ASSETS_ROOT = OC_ROOT / "assets"
EXEC_ASSETS_ROOT = ASSETS_ROOT / "exec"
RULES_ROOT = OC_ROOT / "execution-engine"
STAGING_ROOT = OC_ROOT / "staging"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "GOVERNED_FILESYSTEM_ORCHESTRATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "governed-filesystem-orchestration"

SCHEMA = "governed-filesystem-orchestration/1.0"
LAYER = 39
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

SUBORDINATE_TO = [
    "knowledge-core", "structured-knowledge", "source-of-truth",
    "runtime-implementation", "knowledge-building",
    "publication-system", "publication-quality", "linguistic-governance",
    "operational-pilots", "review-governance", "channel-governance",
    "lineage-governance", "provenance-governance", "warning-governance",
    "terminology-governance", "visual-system", "visual-intent-governance",
    "component-visibility-governance", "procedural-semantics",
    "semantic-enrichment", "corpus-enrichment",
    "supplemental-source-governance", "phase1-cutover",
    "publication-and-delivery-governance", "operational-pilot-governance",
    "publication-renderer", "publication-quality-governance",
    "linguistic-rendering-governance", "publication-time-only-doctrine",
    "warning-fidelity-doctrine", "multimodal-subordination-doctrine",
    "multimodal-evidence-governance", "intake-and-navigation-governance",
    "semantic-domain-governance", "identity-resolution-governance",
    "runtime-orchestration-governance", "operational-console-governance",
    "executable-operational-bindings-governance",
]

STAGING_BUCKETS = [
    "incoming", "review-pending", "accepted",
    "rejected", "quarantined", "failed",
]

EVENT_STORES = [
    "intake-events", "routing-events", "mutation-events", "refresh-events",
    "lineage-events", "rollback-events", "publication-events", "audit-events",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def envelope(extra: dict) -> dict:
    base = {
        "schema": SCHEMA,
        "constitutional_layer_index": LAYER,
        "subordinate_to": SUBORDINATE_TO,
        "updated_at": NOW,
        # Layer-39 specific posture flags
        "executes_filesystem_mutation": True,
        "browser_executes_filesystem_mutation": False,
        "executor_kind": "cli-only-explicit-confirm",
        "daemon": False,
        "background_process": False,
        "watcher_process": False,
        "auto_ingestion": False,
        "auto_publication": False,
        "auto_promotion": False,
        "destructive_overwrite_forbidden": True,
        "requires_reviewer_confirmation": True,
        # Inherited posture flags from prior layers
        "is_saas": False,
        "is_production_app": False,
        "uses_cloud": False,
        "introduces_autonomous_agents": False,
        "introduces_ci_cd": False,
        "auto_approves_ingestion": False,
        "auto_mutates_source_truth": False,
        "bypasses_reviewer_governance": False,
        "uses_ml_or_embeddings": False,
        "network_calls": False,
        "telemetry": False,
        "append_only": True,
        "deterministic": True,
    }
    base.update(extra)
    return base


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def ensure_dir(path: Path, gitkeep_note: str = "") -> None:
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text(gitkeep_note + ("\n" if gitkeep_note else ""), encoding="utf-8")


# ---------------------------------------------------------------------------
# Rule tables (deterministic, JSON, consumed by the JS engines and the
# Python CLI executor)
# ---------------------------------------------------------------------------

DESTINATION_RESOLUTION_RULES = envelope({
    "title": "Destination Resolution Rules",
    "purpose": (
        "Deterministically map (evidence_class, format_category, product, "
        "domain, trust_tier) -> proposed repository destination. The "
        "reviewer may override; the engine never auto-commits."
    ),
    "product_slugs": ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"],
    "rules": [
        {
            "id": "R-DEST-1",
            "match": {"evidence_class": "manual", "format_category": "document"},
            "destination_template": "ext-documents/{product}/source-of-truth/manuals/",
            "trust_tier_required": "tier-2-reviewer-validated",
            "reasoning": "Manuals are canonical product source-of-truth documents.",
        },
        {
            "id": "R-DEST-2",
            "match": {"evidence_class": "datasheet", "format_category": "document"},
            "destination_template": "ext-documents/{product}/source-of-truth/datasheets/",
            "trust_tier_required": "tier-2-reviewer-validated",
            "reasoning": "Datasheets are canonical specifications evidence.",
        },
        {
            "id": "R-DEST-3",
            "match": {"evidence_class": "image", "format_category": "image"},
            "destination_template": "ext-images/{product}/intake/",
            "trust_tier_required": "tier-1-intake",
            "reasoning": "Raw images enter through intake before reviewer promotion.",
        },
        {
            "id": "R-DEST-4",
            "match": {"evidence_class": "video", "format_category": "video"},
            "destination_template": "ext-videos/{product}/intake/",
            "trust_tier_required": "tier-1-intake",
            "reasoning": "Raw videos enter through intake before reviewer promotion.",
        },
        {
            "id": "R-DEST-5",
            "match": {"evidence_class": "specification", "format_category": "structured"},
            "destination_template": "ext-documents/{product}/source-of-truth/specifications/",
            "trust_tier_required": "tier-2-reviewer-validated",
            "reasoning": "Structured specifications attach to canonical specs domain.",
        },
        {
            "id": "R-DEST-6",
            "match": {"evidence_class": "service-bulletin", "format_category": "document"},
            "destination_template": "ext-documents/{product}/source-of-truth/service-bulletins/",
            "trust_tier_required": "tier-2-reviewer-validated",
            "reasoning": "Service bulletins are reviewer-validated operational evidence.",
        },
        {
            "id": "R-DEST-7",
            "match": {"evidence_class": "reference-archive", "format_category": "archive"},
            "destination_template": "ext-documents/{product}/intake/archives/",
            "trust_tier_required": "tier-0-unvalidated",
            "reasoning": "Archives must be reviewer-unpacked before promotion.",
        },
        {
            "id": "R-DEST-8",
            "match": {"evidence_class": "portfolio-asset"},
            "destination_template": "ext-documents/_portfolio/{domain}/",
            "trust_tier_required": "tier-2-reviewer-validated",
            "reasoning": "Portfolio assets attach to portfolio domain, not product.",
        },
        {
            "id": "R-DEST-9",
            "match": {"trust_tier": "tier-0-unvalidated"},
            "destination_template": "operational-console/staging/review-pending/{product}/",
            "trust_tier_required": "tier-0-unvalidated",
            "reasoning": "Unvalidated evidence is held in staging until reviewer raises trust tier.",
        },
        {
            "id": "R-DEST-10",
            "match": {"product": "*", "evidence_class": "*"},
            "destination_template": "operational-console/staging/review-pending/_uncategorised/",
            "trust_tier_required": "tier-0-unvalidated",
            "reasoning": "Fallback when no specific rule matched; reviewer triage required.",
        },
    ],
    "forbidden_destinations": [
        "wp-includes/", "wp-admin/", "wp-content/plugins/",
        "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/",
        "wp-content/themes/beslock-custom/User manuals/_repository-governance/",
        "wp-content/themes/beslock-custom/User manuals/operational-console/runtime-manifests/",
        "runtime-implementation/",
    ],
    "forbidden_destination_reason": (
        "Knowledge-core, governance, runtime-implementation and the runtime "
        "manifest event stores are immutable from intake. Mutation requests "
        "targeting them MUST fail closed in the executor."
    ),
})


MUTATION_SAFETY_RULES = envelope({
    "title": "Mutation Safety Rules",
    "purpose": (
        "Hard preconditions every mutation operation must satisfy before "
        "the CLI executor performs any filesystem write."
    ),
    "preconditions": [
        {"id": "M-PRE-1", "rule": "source_path_must_exist",
         "fail_closed": True,
         "reasoning": "Cannot operate on a non-existent source."},
        {"id": "M-PRE-2", "rule": "destination_path_must_not_exist",
         "fail_closed": True,
         "on_violation": "route_to_quarantined",
         "reasoning": "Destructive overwrite is forbidden."},
        {"id": "M-PRE-3", "rule": "destination_must_be_under_repo_root",
         "fail_closed": True,
         "reasoning": "Prevents path-traversal escape."},
        {"id": "M-PRE-4", "rule": "destination_must_not_match_forbidden_destinations",
         "fail_closed": True,
         "reasoning": "Knowledge-core / governance / runtime-manifests are immutable from intake."},
        {"id": "M-PRE-5", "rule": "request_must_carry_reviewer_attribution",
         "fail_closed": True,
         "reasoning": "Every mutation must be reviewer-attributed."},
        {"id": "M-PRE-6", "rule": "request_must_carry_reasoning_chain",
         "fail_closed": True,
         "reasoning": "Determinism + auditability require explicit reasoning."},
        {"id": "M-PRE-7", "rule": "request_schema_must_match_mutation_request_v1",
         "fail_closed": True,
         "reasoning": "Schema-locked requests are replayable."},
        {"id": "M-PRE-8", "rule": "executor_must_be_invoked_with_explicit_confirm_flag",
         "fail_closed": True,
         "reasoning": "Reviewer authorization gate at the OS level."},
        {"id": "M-PRE-9", "rule": "source_hash_must_match_request_hash",
         "fail_closed": True,
         "reasoning": "Detects source mutation between request build and execution."},
        {"id": "M-PRE-10", "rule": "duplicate_hash_in_accepted_must_be_flagged",
         "fail_closed": False,
         "on_violation": "emit_audit_warning_and_route_to_review_pending",
         "reasoning": "Duplicate evidence is allowed only with reviewer attestation."},
    ],
    "operation_kinds": [
        {"kind": "copy", "description": "Copies source to destination; original retained."},
        {"kind": "stage-accept", "description": "Moves staging/incoming/<file> to staging/accepted/<ts>/<file> after a successful copy."},
        {"kind": "mkdir", "description": "Creates a destination directory tree (no file content)."},
        {"kind": "manifest-write", "description": "Writes a manifest JSON next to a destination file (sibling .manifest.json)."},
    ],
    "forbidden_operation_kinds": [
        "delete", "destructive-move", "in-place-overwrite",
        "rename-across-trust-boundary", "chmod-source-truth", "symlink",
    ],
    "hash_algorithm": "sha256",
    "collision_handling": "fail_closed_then_route_source_to_quarantined",
})


ROLLBACK_RULES = envelope({
    "title": "Rollback Rules",
    "purpose": (
        "Deterministic rollback governance. Rollback NEVER deletes evidence; "
        "it copies the previous state forward and marks the failed state "
        "as preserved."
    ),
    "rollback_kinds": [
        {"kind": "revert-failed-placement",
         "action": "copy_destination_back_to_staging_review_pending",
         "preserves_failed_state": True},
        {"kind": "revert-failed-mutation",
         "action": "restore_previous_manifest_and_mark_destination_as_quarantined",
         "preserves_failed_state": True},
        {"kind": "revert-failed-refresh",
         "action": "mark_refresh_event_as_rolled_back_and_restore_prior_publication_pointer",
         "preserves_failed_state": True},
        {"kind": "restore-previous-manifest",
         "action": "append_previous_manifest_back_to_event_store",
         "preserves_failed_state": True},
        {"kind": "preserve-failed-state-evidence",
         "action": "no_op_evidence_already_preserved_in_failed_directory",
         "preserves_failed_state": True},
    ],
    "rules": [
        {"id": "R-RB-1", "rule": "rollback_requires_reviewer_authorization",
         "fail_closed": True},
        {"id": "R-RB-2", "rule": "rollback_must_be_append_only",
         "fail_closed": True},
        {"id": "R-RB-3", "rule": "rollback_must_not_delete_evidence",
         "fail_closed": True},
        {"id": "R-RB-4", "rule": "rollback_must_emit_lineage_event",
         "fail_closed": True},
        {"id": "R-RB-5", "rule": "rollback_must_reference_original_operation_id",
         "fail_closed": True},
        {"id": "R-RB-6", "rule": "rollback_must_preserve_audit_history",
         "fail_closed": True},
    ],
})


REPOSITORY_SAFETY_RULES = envelope({
    "title": "Repository Safety Rules",
    "purpose": (
        "Pre-execution and post-execution safety scans. Violations BLOCK "
        "execution and emit audit manifests; they NEVER auto-resolve."
    ),
    "checks": [
        {"id": "S-CHK-1", "kind": "duplicate-evidence",
         "detects": "two distinct sources with identical sha256 in accepted/",
         "blocks_execution": False,
         "emits_audit": True},
        {"id": "S-CHK-2", "kind": "overwrite-collision",
         "detects": "destination path already exists",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-3", "kind": "cross-product-contamination",
         "detects": "evidence claims product X but destination contains product slug Y",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-4", "kind": "invalid-routing",
         "detects": "destination matches forbidden_destinations or escapes repo root",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-5", "kind": "trust-violation",
         "detects": "destination_template trust_tier_required exceeds request trust_tier",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-6", "kind": "unresolved-canonical-conflict",
         "detects": "request product slug not present in identity-resolution canonical-products",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-7", "kind": "unsafe-propagation",
         "detects": "refresh request claims to mutate publication outputs without reviewer-authorized refresh-event",
         "blocks_execution": True,
         "emits_audit": True},
        {"id": "S-CHK-8", "kind": "stale-rebuild-chain",
         "detects": "publication regeneration requested from inputs whose accepted-event timestamp is older than last-known stale marker",
         "blocks_execution": False,
         "emits_audit": True},
    ],
    "fail_closed_default": True,
    "audit_event_store": "runtime-manifests/audit-events/_event-store.json",
})


# ---------------------------------------------------------------------------
# JS payloads (vanilla ES, no dependencies, no network calls)
# ---------------------------------------------------------------------------

FS_BRIDGE_JS = """// fs-bridge.js — file:// safe bridge between the browser surfaces and the
// CLI executor. The browser CANNOT mutate the filesystem; this module only
// (a) reads append-only event stores via relative fetch, (b) builds operation
// request manifests, (c) exports them as Blob downloads, and (d) shows the
// reviewer the exact CLI command to run.
(function () {
  if (!window.OC) window.OC = {};
  const RUNTIME_MANIFESTS_BASE = '../runtime-manifests/';
  const RULES_BASE = '../execution-engine/';

  async function loadEventStore(kind) {
    const url = RUNTIME_MANIFESTS_BASE + kind + '/_event-store.json';
    try {
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) {
      if (window.OC && window.OC.UX && window.OC.UX.showWarning) {
        window.OC.UX.showWarning('Could not load ' + url + ' — ' + e.message);
      }
      return null;
    }
  }

  async function loadRules(name) {
    const url = RULES_BASE + name + '.json';
    try {
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) {
      if (window.OC && window.OC.UX && window.OC.UX.showWarning) {
        window.OC.UX.showWarning('Could not load ' + url + ' — ' + e.message);
      }
      return null;
    }
  }

  function buildRequestEnvelope(kind, payload) {
    const session = window.OC.State ? window.OC.State.ensureSession() : null;
    const reviewer = (session && session.reviewer) || 'UNATTRIBUTED';
    return {
      schema: 'governed-fs-operation-request/1.0',
      constitutional_layer_index: 39,
      kind: kind,
      request_id: window.OC.State ? window.OC.State.uuid() : String(Date.now()),
      session_id: session ? session.session_id : null,
      reviewer: reviewer,
      proposed_at_iso: new Date().toISOString(),
      requires_reviewer_confirmation: true,
      destructive_overwrite_forbidden: true,
      executor_invocation_required: true,
      payload: payload,
    };
  }

  function exportRequest(req, suggestedName) {
    const json = JSON.stringify(req, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = suggestedName || (req.kind + '-' + req.request_id + '.json');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function executorCommand(requestKind, savedFilename) {
    return 'python3 tools/governed_fs_executor.py ' +
           '--kind ' + requestKind + ' ' +
           '--request "' + (savedFilename || '<path/to/request.json>') + '" ' +
           '--confirm';
  }

  window.OC.FSBridge = {
    loadEventStore: loadEventStore,
    loadRules: loadRules,
    buildRequestEnvelope: buildRequestEnvelope,
    exportRequest: exportRequest,
    executorCommand: executorCommand,
  };
})();
"""

DEST_RESOLVER_JS = """// dest-resolver.js — deterministic destination proposal. Consumes the
// destination-resolution-rules.json table; never auto-commits.
(function () {
  if (!window.OC) window.OC = {};

  let _rules = null;

  async function ensureRules() {
    if (_rules) return _rules;
    _rules = await window.OC.FSBridge.loadRules('destination-resolution-rules');
    return _rules;
  }

  function _matches(rule, ctx) {
    const m = rule.match || {};
    for (const k of Object.keys(m)) {
      if (m[k] === '*') continue;
      if (ctx[k] !== m[k]) return false;
    }
    return true;
  }

  function _render(template, ctx) {
    return template
      .replace('{product}', ctx.product || '_unknown')
      .replace('{domain}', ctx.domain || '_unknown');
  }

  async function resolve(ctx) {
    const rules = await ensureRules();
    if (!rules || !rules.rules) {
      return { destination: null, rule_id: null, reasoning_chain: ['no rules loaded'] };
    }
    const reasoning = [];
    for (const rule of rules.rules) {
      if (_matches(rule, ctx)) {
        reasoning.push('matched ' + rule.id + ': ' + rule.reasoning);
        const dest = _render(rule.destination_template, ctx);
        const trustOk = !rule.trust_tier_required ||
                         (ctx.trust_tier === rule.trust_tier_required) ||
                         (ctx.trust_tier === 'tier-3-reviewer-attested');
        if (!trustOk) {
          reasoning.push('trust-tier mismatch: required ' + rule.trust_tier_required +
                         ', request carries ' + ctx.trust_tier + '. Falling back to staging.');
          continue;
        }
        return {
          destination: dest,
          rule_id: rule.id,
          trust_tier_required: rule.trust_tier_required,
          reasoning_chain: reasoning,
        };
      }
    }
    reasoning.push('no rule matched — fallback to staging/review-pending/_uncategorised/');
    return {
      destination: 'operational-console/staging/review-pending/_uncategorised/',
      rule_id: 'R-DEST-FALLBACK',
      trust_tier_required: 'tier-0-unvalidated',
      reasoning_chain: reasoning,
    };
  }

  function isForbidden(dest, rules) {
    if (!rules || !rules.forbidden_destinations) return false;
    for (const f of rules.forbidden_destinations) {
      if (dest && dest.indexOf(f) === 0) return true;
    }
    return false;
  }

  window.OC.DestResolver = { ensureRules: ensureRules, resolve: resolve, isForbidden: isForbidden };
})();
"""

MUTATION_ENGINE_JS = """// mutation-engine.js — proposes a mutation request. The browser NEVER
// performs the mutation; the reviewer downloads the request JSON and feeds
// it into tools/governed_fs_executor.py.
(function () {
  if (!window.OC) window.OC = {};

  function buildMutationRequest(form) {
    // form: { kind, source_path, destination, evidence_class, format_category,
    //        product, domain, trust_tier, source_hash_sha256, reviewer_notes }
    const reasoning = [];
    if (!form.source_path) reasoning.push('WARN: missing source_path');
    if (!form.destination) reasoning.push('WARN: missing destination');
    if (!form.source_hash_sha256) reasoning.push('NOTE: source_hash_sha256 will be computed by the executor and re-verified at execute time');
    reasoning.push('mutation kind: ' + (form.kind || 'copy'));
    reasoning.push('reviewer attribution required: true');
    reasoning.push('destructive overwrite forbidden');
    reasoning.push('destination collision routes source to staging/quarantined/');

    const req = window.OC.FSBridge.buildRequestEnvelope('mutation', {
      operation_kind: form.kind || 'copy',
      source_path: form.source_path,
      destination: form.destination,
      evidence_class: form.evidence_class || null,
      format_category: form.format_category || null,
      product: form.product || null,
      domain: form.domain || null,
      trust_tier: form.trust_tier || 'tier-0-unvalidated',
      source_hash_sha256: form.source_hash_sha256 || null,
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      preconditions_required: [
        'M-PRE-1', 'M-PRE-2', 'M-PRE-3', 'M-PRE-4',
        'M-PRE-5', 'M-PRE-6', 'M-PRE-7', 'M-PRE-8',
      ],
    });
    return req;
  }

  function previewExecutorCommand(req, suggestedName) {
    return window.OC.FSBridge.executorCommand('mutation', suggestedName);
  }

  window.OC.MutationEngine = {
    buildMutationRequest: buildMutationRequest,
    previewExecutorCommand: previewExecutorCommand,
  };
})();
"""

ROLLBACK_ENGINE_JS = """// rollback-engine.js — proposes a rollback request. Reviewer-only;
// browser does not execute. Append-only. Preserves failed-state evidence.
(function () {
  if (!window.OC) window.OC = {};

  function buildRollbackRequest(form) {
    // form: { rollback_kind, original_operation_id, reason, reviewer_notes }
    const reasoning = [
      'rollback_kind: ' + form.rollback_kind,
      'targets original operation: ' + form.original_operation_id,
      'preserves failed-state evidence (no deletion)',
      'append-only: emits a new lineage + rollback event, never mutates prior events',
      'requires reviewer authorization at the executor invocation gate',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('rollback', {
      rollback_kind: form.rollback_kind,
      original_operation_id: form.original_operation_id,
      reason: form.reason || '',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      rules_required: ['R-RB-1', 'R-RB-2', 'R-RB-3', 'R-RB-4', 'R-RB-5', 'R-RB-6'],
    });
  }

  window.OC.RollbackEngine = { buildRollbackRequest: buildRollbackRequest };
})();
"""

SAFETY_ENGINE_JS = """// safety-engine.js — reads the safety-violation audit feed and surfaces it
// for reviewer triage. Read-only; never mutates.
(function () {
  if (!window.OC) window.OC = {};

  async function loadAuditEvents() {
    return await window.OC.FSBridge.loadEventStore('audit-events');
  }

  function summarise(events) {
    if (!events || !events.events) return { total: 0, by_kind: {} };
    const by_kind = {};
    for (const e of events.events) {
      const k = (e.payload && e.payload.kind) || (e.kind) || 'unknown';
      by_kind[k] = (by_kind[k] || 0) + 1;
    }
    return { total: events.events.length, by_kind: by_kind };
  }

  window.OC.SafetyEngine = { loadAuditEvents: loadAuditEvents, summarise: summarise };
})();
"""


# ---------------------------------------------------------------------------
# CSS addendum — tiny extension on top of phase-45 exec.css
# ---------------------------------------------------------------------------

EXEC_CSS_ADDENDUM = """
/* phase 46 — governed filesystem orchestration additions */
.oc-exec__danger { border-left: 3px solid #d96d6d; padding-left: .75rem; }
.oc-exec__pre--cmd { background: #1b1b1b; color: #cfe6ff; padding: .75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px;
    white-space: pre-wrap; word-break: break-all; border-radius: 4px; }
.oc-exec__table { width: 100%; border-collapse: collapse; font-size: 13px; }
.oc-exec__table th, .oc-exec__table td {
    border-bottom: 1px solid #2a2a2a; padding: .35rem .5rem; text-align: left; }
.oc-exec__pill { display: inline-block; padding: 1px 6px; border-radius: 8px;
    font-size: 11px; background: #243a52; color: #cfe6ff; }
"""


# ---------------------------------------------------------------------------
# HTML pages (4 NEW exec consoles)
# ---------------------------------------------------------------------------

def _html_head(title: str, prefix: str = "..") -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<title>{title} — Beslock Operational Console</title>
<link rel=\"stylesheet\" href=\"{prefix}/assets/console.css\" />
<link rel=\"stylesheet\" href=\"{prefix}/assets/exec/exec.css\" />
</head>
<body class=\"oc-body oc-body--exec\">
<header class=\"oc-header\">
  <a class=\"oc-header__brand\" href=\"{prefix}/index.html\">Beslock Operational Console</a>
  <nav class=\"oc-header__nav\">
    <a href=\"{prefix}/exec.html\">Exec dashboard</a>
    <a href=\"{prefix}/intake-console/exec.html\">Intake</a>
    <a href=\"{prefix}/routing-console/exec.html\">Routing</a>
    <a href=\"{prefix}/refresh-console/exec.html\">Refresh</a>
    <a href=\"{prefix}/reconciliation-console/exec.html\">Recon</a>
    <a href=\"{prefix}/mutation-console/exec.html\">Mutation</a>
    <a href=\"{prefix}/lineage-console/exec.html\">Lineage</a>
    <a href=\"{prefix}/rollback-console/exec.html\">Rollback</a>
    <a href=\"{prefix}/safety-console/exec.html\">Safety</a>
  </nav>
</header>
<main class=\"oc-main oc-exec\">
"""


HTML_TAIL = """</main>
<script src="../assets/exec/state.js"></script>
<script src="../assets/exec/ux.js"></script>
<script src="../assets/exec/drafts.js"></script>
<script src="../assets/exec/fs-bridge.js"></script>
<script src="../assets/exec/dest-resolver.js"></script>
<script src="../assets/exec/mutation-engine.js"></script>
<script src="../assets/exec/rollback-engine.js"></script>
<script src="../assets/exec/safety-engine.js"></script>
</body></html>
"""


MUTATION_CONSOLE_HTML = _html_head("Mutation console") + """
<section class="oc-exec__panel">
  <h1>Governed mutation request</h1>
  <p class="oc-exec__danger">
    This surface NEVER mutates the filesystem. It builds a deterministic
    operation-request manifest, downloads it as JSON, and prints the exact
    CLI command. Only the reviewer (running
    <code>python3 tools/governed_fs_executor.py … --confirm</code>) performs
    the actual copy. Destructive overwrite is forbidden.
  </p>

  <form id="mut-form" class="oc-exec__form" autocomplete="off">
    <label>Source path (relative to repo root)
      <input name="source_path" placeholder="wp-content/themes/beslock-custom/User manuals/operational-console/staging/incoming/manual.pdf" />
    </label>
    <label>Operation kind
      <select name="kind">
        <option value="copy">copy</option>
        <option value="stage-accept">stage-accept</option>
        <option value="mkdir">mkdir</option>
        <option value="manifest-write">manifest-write</option>
      </select>
    </label>
    <label>Evidence class
      <select name="evidence_class">
        <option value="manual">manual</option>
        <option value="datasheet">datasheet</option>
        <option value="image">image</option>
        <option value="video">video</option>
        <option value="specification">specification</option>
        <option value="service-bulletin">service-bulletin</option>
        <option value="reference-archive">reference-archive</option>
        <option value="portfolio-asset">portfolio-asset</option>
      </select>
    </label>
    <label>Format category
      <select name="format_category">
        <option value="document">document</option>
        <option value="image">image</option>
        <option value="video">video</option>
        <option value="structured">structured</option>
        <option value="archive">archive</option>
      </select>
    </label>
    <label>Product slug
      <select name="product">
        <option value="">(none)</option>
        <option value="e-orbit">e-orbit</option>
        <option value="e-prime">e-prime</option>
        <option value="e-flex">e-flex</option>
        <option value="e-touch">e-touch</option>
        <option value="e-shield">e-shield</option>
        <option value="e-nova">e-nova</option>
      </select>
    </label>
    <label>Trust tier
      <select name="trust_tier">
        <option value="tier-0-unvalidated">tier-0-unvalidated</option>
        <option value="tier-1-intake">tier-1-intake</option>
        <option value="tier-2-reviewer-validated">tier-2-reviewer-validated</option>
        <option value="tier-3-reviewer-attested">tier-3-reviewer-attested</option>
      </select>
    </label>
    <label>Reviewer notes
      <textarea name="reviewer_notes" rows="3"></textarea>
    </label>
    <div class="oc-exec__row">
      <button type="button" id="mut-resolve" class="oc-exec__btn">Resolve destination</button>
      <button type="button" id="mut-build" class="oc-exec__btn">Build &amp; download request</button>
    </div>
  </form>

  <h2>Resolved destination</h2>
  <pre id="mut-dest" class="oc-exec__pre">(none yet)</pre>

  <h2>Request preview</h2>
  <pre id="mut-preview" class="oc-exec__pre">(none yet)</pre>

  <h2>Reviewer execution command</h2>
  <pre id="mut-cmd" class="oc-exec__pre oc-exec__pre--cmd">(none yet)</pre>
</section>

<script>
(function () {
  const form = document.getElementById('mut-form');
  function readForm() {
    const fd = new FormData(form);
    const o = {};
    fd.forEach(function (v, k) { o[k] = v; });
    return o;
  }
  document.getElementById('mut-resolve').addEventListener('click', async function () {
    const ctx = readForm();
    const r = await window.OC.DestResolver.resolve(ctx);
    document.getElementById('mut-dest').textContent = JSON.stringify(r, null, 2);
  });
  document.getElementById('mut-build').addEventListener('click', async function () {
    const ctx = readForm();
    const dest = await window.OC.DestResolver.resolve(ctx);
    ctx.destination = ctx.destination || dest.destination;
    const req = window.OC.MutationEngine.buildMutationRequest(ctx);
    document.getElementById('mut-preview').textContent = JSON.stringify(req, null, 2);
    const fname = 'mutation-request-' + req.request_id + '.json';
    document.getElementById('mut-cmd').textContent =
      window.OC.MutationEngine.previewExecutorCommand(req, fname);
    if (window.OC.Drafts) window.OC.Drafts.record('mutation-request-draft', req);
    window.OC.FSBridge.exportRequest(req, fname);
  });
})();
</script>
""" + HTML_TAIL


LINEAGE_CONSOLE_HTML = _html_head("Lineage console") + """
<section class="oc-exec__panel">
  <h1>Operational lineage</h1>
  <p>Read-only inspection of the append-only lineage event store
    (<code>runtime-manifests/lineage-events/_event-store.json</code>).
    The store is populated by the CLI executor on every successful mutation,
    refresh, publication-regeneration and rollback.</p>
  <div class="oc-exec__row">
    <button type="button" id="lin-load" class="oc-exec__btn">Load lineage events</button>
    <span id="lin-count" class="oc-exec__pill">0 events</span>
  </div>
  <h2>Events</h2>
  <pre id="lin-events" class="oc-exec__pre">(not loaded)</pre>
</section>
<script>
(function () {
  document.getElementById('lin-load').addEventListener('click', async function () {
    const data = await window.OC.FSBridge.loadEventStore('lineage-events');
    if (!data) { document.getElementById('lin-events').textContent = '(load failed — see warnings)'; return; }
    const n = (data.events || []).length;
    document.getElementById('lin-count').textContent = n + ' events';
    document.getElementById('lin-events').textContent = JSON.stringify(data, null, 2);
  });
})();
</script>
""" + HTML_TAIL


ROLLBACK_CONSOLE_HTML = _html_head("Rollback console") + """
<section class="oc-exec__panel">
  <h1>Rollback request</h1>
  <p class="oc-exec__danger">
    Rollback NEVER deletes evidence. It copies the previous state forward
    and marks the failed state as preserved. Reviewer authorization is
    required at the executor invocation gate.
  </p>
  <form id="rb-form" class="oc-exec__form" autocomplete="off">
    <label>Rollback kind
      <select name="rollback_kind">
        <option value="revert-failed-placement">revert-failed-placement</option>
        <option value="revert-failed-mutation">revert-failed-mutation</option>
        <option value="revert-failed-refresh">revert-failed-refresh</option>
        <option value="restore-previous-manifest">restore-previous-manifest</option>
        <option value="preserve-failed-state-evidence">preserve-failed-state-evidence</option>
      </select>
    </label>
    <label>Original operation id (UUID from the prior mutation/refresh request)
      <input name="original_operation_id" />
    </label>
    <label>Reason
      <textarea name="reason" rows="2"></textarea>
    </label>
    <label>Reviewer notes
      <textarea name="reviewer_notes" rows="2"></textarea>
    </label>
    <div class="oc-exec__row">
      <button type="button" id="rb-build" class="oc-exec__btn">Build &amp; download rollback request</button>
    </div>
  </form>

  <h2>Request preview</h2>
  <pre id="rb-preview" class="oc-exec__pre">(none yet)</pre>

  <h2>Reviewer execution command</h2>
  <pre id="rb-cmd" class="oc-exec__pre oc-exec__pre--cmd">(none yet)</pre>
</section>
<script>
(function () {
  document.getElementById('rb-build').addEventListener('click', function () {
    const fd = new FormData(document.getElementById('rb-form'));
    const o = {}; fd.forEach(function (v, k) { o[k] = v; });
    const req = window.OC.RollbackEngine.buildRollbackRequest(o);
    document.getElementById('rb-preview').textContent = JSON.stringify(req, null, 2);
    const fname = 'rollback-request-' + req.request_id + '.json';
    document.getElementById('rb-cmd').textContent =
      window.OC.FSBridge.executorCommand('rollback', fname);
    if (window.OC.Drafts) window.OC.Drafts.record('rollback-request-draft', req);
    window.OC.FSBridge.exportRequest(req, fname);
  });
})();
</script>
""" + HTML_TAIL


SAFETY_CONSOLE_HTML = _html_head("Safety console") + """
<section class="oc-exec__panel">
  <h1>Repository safety inspection</h1>
  <p>Read-only inspection of the append-only audit event store
    (<code>runtime-manifests/audit-events/_event-store.json</code>).
    Safety violations BLOCK execution and require reviewer intervention.</p>
  <div class="oc-exec__row">
    <button type="button" id="sf-load" class="oc-exec__btn">Load audit events</button>
    <span id="sf-count" class="oc-exec__pill">0 events</span>
  </div>
  <h2>By violation kind</h2>
  <pre id="sf-summary" class="oc-exec__pre">(not loaded)</pre>
  <h2>Raw events</h2>
  <pre id="sf-events" class="oc-exec__pre">(not loaded)</pre>
</section>
<script>
(function () {
  document.getElementById('sf-load').addEventListener('click', async function () {
    const data = await window.OC.SafetyEngine.loadAuditEvents();
    if (!data) { document.getElementById('sf-events').textContent = '(load failed — see warnings)'; return; }
    const summary = window.OC.SafetyEngine.summarise(data);
    document.getElementById('sf-count').textContent = summary.total + ' events';
    document.getElementById('sf-summary').textContent = JSON.stringify(summary, null, 2);
    document.getElementById('sf-events').textContent = JSON.stringify(data, null, 2);
  });
})();
</script>
""" + HTML_TAIL


# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = [
    ("01-real-mutation-but-reviewer-authorized",
     "Real Mutation, Reviewer Authorized",
     "The filesystem MAY be mutated by this layer, but ONLY by an explicit "
     "CLI executor invocation carrying --confirm. The browser surface "
     "never mutates."),
    ("02-cli-only-no-daemon",
     "CLI Only, No Daemon",
     "There is no watcher, no scheduled trigger, no background process, no "
     "queue worker. Every mutation is a foreground reviewer-invoked command."),
    ("03-no-destructive-overwrite",
     "No Destructive Overwrite",
     "If a destination exists, the operation fails closed and the source is "
     "routed to staging/quarantined/. Originals are retained in "
     "staging/accepted/<ts>/."),
    ("04-append-only-event-stores",
     "Append-Only Event Stores",
     "All eight runtime-manifest event stores are append-only. Prior events "
     "are never modified. Rollback emits new events; it never deletes."),
    ("05-deterministic-destination-resolution",
     "Deterministic Destination Resolution",
     "Destinations are derived from declarative rules tables (R-DEST-1 … "
     "R-DEST-10). Reviewer override is permitted; randomised routing is not."),
    ("06-fail-closed-safety",
     "Fail-Closed Safety",
     "Eight safety checks (S-CHK-1 … S-CHK-8) run before every mutation. "
     "Violations BLOCK execution and emit audit manifests. Auto-resolution "
     "is forbidden."),
    ("07-rollback-preserves-evidence",
     "Rollback Preserves Evidence",
     "Rollback copies the prior state forward and marks the failed state as "
     "preserved. It never deletes evidence."),
    ("08-knowledge-core-and-governance-immutable-from-intake",
     "Knowledge-Core and Governance Immutable From Intake",
     "Forbidden destinations include knowledge-core, governance, "
     "runtime-implementation, and the runtime-manifest event stores. "
     "Mutation requests targeting them fail closed at S-CHK-4."),
]


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORT_PHASES = [
    ("32", "Semantic domain governance", "phase 41 → layer 34"),
    ("33", "Identity resolution governance", "phase 42 → layer 35"),
    ("34", "Runtime orchestration governance", "phase 43 → layer 36"),
    ("35", "Operational console governance", "phase 44 → layer 37"),
    ("36", "Executable operational bindings", "phase 45 → layer 38"),
    ("37", "Governed filesystem orchestration", "phase 46 → layer 39 (this phase)"),
]


REPORTS = [
    ("01-real-intake-summary", "Real Intake Summary",
     "Establishes governed staging roots (incoming/review-pending/accepted/"
     "rejected/quarantined/failed), append-only intake-events store, drag-"
     "drop / multi-file staging surfaces, and the executor-mediated path "
     "from staging to canonical destinations. Browser never mutates; "
     "reviewer always confirms."),
    ("02-destination-resolution-summary", "Destination Resolution Summary",
     "Layers 10 deterministic R-DEST rules over (evidence_class, "
     "format_category, product, domain, trust_tier) → repository "
     "destination. Forbidden destinations enforced. Trust-tier mismatch "
     "falls back to staging/review-pending/."),
    ("03-filesystem-mutation-summary", "Filesystem Mutation Summary",
     "Introduces tools/governed_fs_executor.py — the only component in the "
     "ecosystem with filesystem write capability. Enforces 10 M-PRE "
     "preconditions, four operation kinds (copy, stage-accept, mkdir, "
     "manifest-write), seven forbidden operation kinds, fail-closed "
     "collision handling."),
    ("04-executable-manifest-summary", "Executable Manifest Summary",
     "Establishes eight append-only runtime-manifest event stores under "
     "operational-console/runtime-manifests/. Every executor invocation "
     "writes (a) operation manifest, (b) lineage manifest, (c) audit entry "
     "— hashed, reviewer-attributed, replayable, deterministic."),
    ("05-refresh-execution-summary", "Refresh Execution Summary",
     "Upgrades refresh-console from proposal-only to reviewer-authorized "
     "execution by routing approved refresh-event drafts through the same "
     "CLI executor (kind=refresh). Every refresh remains deterministic, "
     "scoped, append-only, rollback-capable. No autonomous refresh."),
    ("06-publication-regeneration-summary", "Publication Regeneration Summary",
     "Establishes publication-events store and reviewer-authorized "
     "publication regeneration request kind. Regeneration runs only via "
     "the executor; no autonomous publishing; rollback-capable; deterministic."),
    ("07-lineage-execution-summary", "Lineage Execution Summary",
     "Every operational action emits a lineage event chained to its "
     "originating operation_id, reviewer, timestamp, and reasoning chain. "
     "Lineage events are append-only, replayable, and support deterministic "
     "reconstruction."),
    ("08-rollback-governance-summary", "Rollback Governance Summary",
     "Five rollback kinds + six R-RB rules. Rollback is reviewer-authorized, "
     "append-only, never destructive, always preserves failed-state "
     "evidence, always references original_operation_id."),
    ("09-repository-safety-summary", "Repository Safety Summary",
     "Eight S-CHK checks (duplicate-evidence, overwrite-collision, "
     "cross-product-contamination, invalid-routing, trust-violation, "
     "unresolved-canonical-conflict, unsafe-propagation, stale-rebuild-chain). "
     "Fail-closed default; audit-events emitted on every violation."),
    ("10-executable-knowledge-platform-maturity-reassessment",
     "Executable Knowledge Platform Maturity Reassessment",
     "The platform is now an executable knowledge operations system: "
     "governed intake, governed placement, governed propagation, governed "
     "refresh, governed publication regeneration, governed lineage, "
     "governed rollback, governed repository mutation. All under reviewer "
     "authority, append-only discipline, local-first execution, repo-native "
     "operations. No SaaS, no cloud, no daemon, no autonomous agent, no ML."),
]


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_staging_tree() -> int:
    notes = {
        "incoming": "Drop new evidence here. Reviewer triages in the intake / mutation consoles.",
        "review-pending": "Holds evidence awaiting trust-tier promotion or destination decision.",
        "accepted": "Originals retained after successful copy to canonical destination.",
        "rejected": "Reviewer-rejected evidence (kept for audit; never deleted).",
        "quarantined": "Sources whose mutation failed closed (e.g., destination collision).",
        "failed": "Operations that failed mid-execution (preserved for rollback / inspection).",
    }
    n = 0
    for bucket in STAGING_BUCKETS:
        ensure_dir(STAGING_ROOT / bucket, notes[bucket])
        n += 1
    write_text(STAGING_ROOT / "README.md",
               "# Governed staging roots (phase 46, layer 39)\n\n"
               "Six append-only buckets governing the lifecycle of intake "
               "evidence. The browser surface never writes here directly; "
               "the reviewer either drops files manually into `incoming/` or "
               "the CLI executor moves files between buckets under explicit "
               "reviewer authorization.\n\n"
               + "\n".join(f"- **{b}/** — {notes[b]}" for b in STAGING_BUCKETS) + "\n")
    return n


def build_runtime_manifest_stores() -> int:
    n = 0
    for kind in EVENT_STORES:
        path = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        if path.exists():
            # never overwrite existing append-only stores
            n += 1
            continue
        write_json(path, {
            "schema": "governed-fs-event-store/1.0",
            "constitutional_layer_index": LAYER,
            "kind": kind,
            "append_only": True,
            "deterministic": True,
            "reviewer_authoritative": True,
            "created_at": NOW,
            "events": [],
        })
        n += 1
    write_text(RUNTIME_MANIFESTS_ROOT / "README.md",
               "# Runtime manifest event stores (phase 46, layer 39)\n\n"
               "Eight append-only event stores populated exclusively by the "
               "CLI executor (`tools/governed_fs_executor.py`). The browser "
               "surface reads these via `fetch`; it never writes them.\n\n"
               + "\n".join(f"- `{k}/_event-store.json`" for k in EVENT_STORES) + "\n")
    return n


def build_rule_tables() -> int:
    write_json(RULES_ROOT / "destination-resolution-rules.json", DESTINATION_RESOLUTION_RULES)
    write_json(RULES_ROOT / "mutation-safety-rules.json", MUTATION_SAFETY_RULES)
    write_json(RULES_ROOT / "rollback-rules.json", ROLLBACK_RULES)
    write_json(RULES_ROOT / "repository-safety-rules.json", REPOSITORY_SAFETY_RULES)
    return 4


def build_assets() -> int:
    write_text(EXEC_ASSETS_ROOT / "fs-bridge.js", FS_BRIDGE_JS)
    write_text(EXEC_ASSETS_ROOT / "dest-resolver.js", DEST_RESOLVER_JS)
    write_text(EXEC_ASSETS_ROOT / "mutation-engine.js", MUTATION_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "rollback-engine.js", ROLLBACK_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "safety-engine.js", SAFETY_ENGINE_JS)
    # CSS addendum: append idempotently
    css_path = EXEC_ASSETS_ROOT / "exec.css"
    existing = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    marker = "/* phase 46 — governed filesystem orchestration additions */"
    if marker not in existing:
        write_text(css_path, existing + EXEC_CSS_ADDENDUM)
    return 6


def build_consoles() -> int:
    write_text(OC_ROOT / "mutation-console" / "exec.html", MUTATION_CONSOLE_HTML)
    write_text(OC_ROOT / "lineage-console" / "exec.html", LINEAGE_CONSOLE_HTML)
    write_text(OC_ROOT / "rollback-console" / "exec.html", ROLLBACK_CONSOLE_HTML)
    write_text(OC_ROOT / "safety-console" / "exec.html", SAFETY_CONSOLE_HTML)
    return 4


def build_doctrines() -> int:
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    index_lines = ["# Governed Filesystem Orchestration Governance (phase 46, layer 39)\n"]
    for slug, title, summary in DOCTRINES:
        body = f"# {title}\n\n*Layer {LAYER}. Subordinate to all 38 prior layers.*\n\n{summary}\n"
        write_text(CONST_ROOT / f"{slug}-doctrine.md", body)
        index_lines.append(f"- [{title}](./{slug}-doctrine.md)")
    write_text(CONST_ROOT / "00-INDEX.md", "\n".join(index_lines) + "\n")
    write_json(CONST_ROOT / "manifest.json", envelope({
        "title": "Governed Filesystem Orchestration Governance",
        "doctrines": [slug for slug, _, _ in DOCTRINES],
    }))
    return len(DOCTRINES)


def build_reports() -> int:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(REPORTS_ROOT / "README.md",
               "# Governed Filesystem Orchestration — phase 46 reports\n\n"
               "Ten reports describing the layer-39 surface delivered by "
               "`tools/governed_fs_orchestration.py`.\n")
    n = 0
    for slug, title, body in REPORTS:
        write_json(REPORTS_ROOT / f"{slug}.json", envelope({
            "title": title,
            "report_slug": slug,
            "phase": "46",
            "layer": LAYER,
            "summary": body,
            "phase_ladder": [
                {"phase": p, "title": t, "anchor": a} for (p, t, a) in REPORT_PHASES
            ],
        }))
        write_text(REPORTS_ROOT / f"{slug}.md",
                   f"# {title}\n\n*Phase 46 · layer {LAYER}.*\n\n{body}\n")
        n += 1
    return n


def build_runtime_readme() -> None:
    body = (
        "# Governed filesystem execution — RUNTIME README (phase 46, layer 39)\n\n"
        "## What this layer adds\n\n"
        "This is the FIRST repo-native layer that performs REAL filesystem "
        "mutation. All prior governance is preserved.\n\n"
        "Three pieces work together:\n\n"
        "1. **Browser surfaces** under `mutation-console/`, `lineage-console/`, "
        "`rollback-console/`, `safety-console/` — propose / inspect only.\n"
        "2. **Rule tables** under `execution-engine/` — deterministic, "
        "reviewer-authoritative, consumed by both browser and CLI.\n"
        "3. **CLI executor** at `tools/governed_fs_executor.py` — the ONLY "
        "filesystem-writing component. Reviewer must invoke it explicitly "
        "with `--confirm`.\n\n"
        "## Reviewer workflow\n\n"
        "```\n"
        "# 1. Drop a file into the staging root\n"
        "cp ~/Downloads/manual.pdf wp-content/themes/beslock-custom/\"User manuals\"/operational-console/staging/incoming/\n"
        "\n"
        "# 2. Open the mutation console (or any exec console) in the browser:\n"
        "python3 -m http.server 8000\n"
        "# then visit http://localhost:8000/wp-content/themes/beslock-custom/User%20manuals/operational-console/mutation-console/exec.html\n"
        "\n"
        "# 3. Fill in the form, click \"Resolve destination\" and \"Build & download request\".\n"
        "#    A mutation-request-<uuid>.json is downloaded.\n"
        "\n"
        "# 4. Run the executor (the console prints the exact command):\n"
        "python3 tools/governed_fs_executor.py --kind mutation --request ~/Downloads/mutation-request-<uuid>.json --confirm\n"
        "```\n\n"
        "## Hard guarantees\n\n"
        "- No daemon, no watcher, no autonomous agent.\n"
        "- Destructive overwrite is forbidden — the executor fails closed.\n"
        "- Knowledge-core, governance, runtime-implementation and the "
        "runtime-manifest event stores are immutable from intake.\n"
        "- Every successful operation appends to (a) operation event store, "
        "(b) lineage event store, (c) audit event store.\n"
        "- Every failed operation routes the source to "
        "`staging/quarantined/` and emits an audit event.\n"
    )
    write_text(OC_ROOT / "RUNTIME_README.md", body)


def main() -> None:
    staging = build_staging_tree()
    stores = build_runtime_manifest_stores()
    rules = build_rule_tables()
    assets = build_assets()
    consoles = build_consoles()
    doctrines = build_doctrines()
    reports = build_reports()
    build_runtime_readme()
    print(
        "Phase 46 — governed filesystem orchestration written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Staging buckets: {staging} | Event stores: {stores} | "
        f"Rule tables: {rules} | JS assets: {assets} | "
        f"Exec consoles: {consoles} | Doctrines: {doctrines} | "
        f"Reports: {reports}"
    )


if __name__ == "__main__":
    main()
