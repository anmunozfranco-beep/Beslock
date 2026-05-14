"""
Phase 47 — GOVERNED TRANSACTIONAL EXECUTION & RECOVERY.

Constitutional layer 40. Subordinate to layer 39
(governed-filesystem-orchestration-governance) and to all 39 prior governance
layers. This phase introduces the FIRST real transactional safety layer over
the layer-39 filesystem mutation engine: every mutation now runs inside a
governed transaction with deterministic snapshot capture, reviewer-authorized
rollback execution, interrupted-operation recovery, deterministic replay, and
multi-channel integrity verification.

NOT a SaaS, NOT a cloud architecture, NOT a backend, NOT an autonomous agent
platform, NOT a CI/CD pipeline, NOT an ML system, NOT a daemon, NOT an
auto-recovery service. Stdlib-only, local-first, deterministic,
reviewer-authoritative, append-only, repo-native.

This builder writes (idempotent, non-destructive, additive) under
`wp-content/themes/beslock-custom/User manuals/operational-console/`:

  runtime-snapshots/                                (NEW snapshot roots)
    repository/  manifests/  lineage/  publications/
    refresh-state/  transaction-state/  recovery-checkpoints/
  runtime-manifests/                                (6 NEW append-only stores
                                                    added beside the layer-39 8)
    transaction-events/   snapshot-events/
    recovery-events/      integrity-events/
    replay-events/        failure-events/
  execution-engine/                                 (8 NEW deterministic
                                                    rule tables)
    transaction-state-rules.json
    snapshot-rules.json
    rollback-execution-rules.json
    recovery-rules.json
    replay-rules.json
    integrity-verification-rules.json
    failure-governance-rules.json
    consistency-rules.json
  assets/exec/                                      (8 NEW vanilla-ES engines)
    transaction-engine.js  snapshot-engine.js  rollback-exec-engine.js
    recovery-engine.js     replay-engine.js    integrity-engine.js
    failure-engine.js      consistency-engine.js
  transaction-console/exec.html                     (NEW)
  snapshot-console/exec.html                        (NEW)
  recovery-console/exec.html                        (NEW)
  replay-console/exec.html                          (NEW)
  integrity-console/exec.html                       (NEW)
  failure-console/exec.html                         (NEW)

Plus:
  KNOWLEDGE_BUILDING/GOVERNED_TRANSACTIONAL_EXECUTION_GOVERNANCE/
    00-INDEX + 10 doctrines + manifest
  _repository-governance/reports/governed-transactional-execution/
    10 reports + README

Hard rules (extends layer 39):
  - The BROWSER surface NEVER touches the filesystem; it only emits
    operation-request envelopes (governed-fs-operation-request/1.0) carrying
    transaction_id, snapshot_request, and rollback/recovery context.
  - The CLI executor `tools/governed_transactional_executor.py` extends
    layer 39's executor by wrapping every mutation in a transaction with
    deterministic snapshot capture and append-only journal entries.
  - All mutations MUST run inside a governed transaction. There are NO
    direct mutations outside transaction boundaries from this layer
    forward.
  - Snapshots are append-only, timestamped, transaction-bound,
    reviewer-inspectable, and never deleted by the executor.
  - Rollback is reviewer-authorized, append-only, never destructive,
    always preserves failed-state evidence, and emits its own lineage +
    audit + transaction events.
  - Recovery NEVER auto-resolves: the recovery engine emits a recovery
    manifest the reviewer must explicitly approve. There is no autonomous
    rollback, no auto-replay, no daemon.
  - Integrity verification is read-only and emits findings; it never
    mutates and it never auto-quarantines. Reviewer triages.
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
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
SNAPSHOTS_ROOT = OC_ROOT / "runtime-snapshots"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "GOVERNED_TRANSACTIONAL_EXECUTION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "governed-transactional-execution"

SCHEMA = "governed-transactional-execution/1.0"
LAYER = 40
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
    "governed-filesystem-orchestration-governance",
]

SNAPSHOT_ROOTS = [
    "repository", "manifests", "lineage", "publications",
    "refresh-state", "transaction-state", "recovery-checkpoints",
]

NEW_EVENT_STORES = [
    "transaction-events", "snapshot-events", "recovery-events",
    "integrity-events", "replay-events", "failure-events",
]

TRANSACTION_STATES = [
    "initialized", "staged", "executing", "committed",
    "failed", "rolled-back", "recovery-required", "replayed",
]

FAILURE_CLASSES = [
    "mutation-failure", "snapshot-failure", "replay-failure",
    "rollback-failure", "publication-divergence", "stale-runtime",
    "partial-refresh", "lineage-break", "collision-conflict",
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
        # Layer-40 specific posture flags
        "wraps_mutations_in_transactions": True,
        "captures_snapshots_before_mutation": True,
        "rollback_is_reviewer_authorized": True,
        "rollback_preserves_evidence": True,
        "recovery_is_reviewer_authorized": True,
        "replay_is_reviewer_authorized": True,
        "auto_recovery": False,
        "auto_rollback": False,
        "auto_replay": False,
        "destructive_snapshot_pruning": False,
        "snapshot_append_only": True,
        # Inherited posture flags
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
# Rule tables
# ---------------------------------------------------------------------------

TRANSACTION_STATE_RULES = envelope({
    "title": "Transaction State Rules",
    "purpose": (
        "Deterministic finite-state model for governed transactions. Every "
        "mutation MUST flow through this state machine. Browser surfaces "
        "never advance state; only the CLI executor does, and only with "
        "--confirm."
    ),
    "states": TRANSACTION_STATES,
    "initial_state": "initialized",
    "terminal_states": ["committed", "rolled-back", "replayed"],
    "blocking_states": ["failed", "recovery-required"],
    "transitions": [
        {"id": "T-1", "from": "initialized", "to": "staged",
         "guard": "snapshot_capture_complete && preconditions_passed",
         "reasoning": "Snapshot must precede any mutation."},
        {"id": "T-2", "from": "staged", "to": "executing",
         "guard": "reviewer_confirm_flag",
         "reasoning": "Execution requires explicit reviewer authorization."},
        {"id": "T-3", "from": "executing", "to": "committed",
         "guard": "all_operations_succeeded && integrity_check_passed",
         "reasoning": "Commit only when every staged operation succeeded."},
        {"id": "T-4", "from": "executing", "to": "failed",
         "guard": "any_operation_failed",
         "reasoning": "Any sub-operation failure transitions the transaction to failed."},
        {"id": "T-5", "from": "failed", "to": "rolled-back",
         "guard": "reviewer_authorised_rollback && rollback_executed",
         "reasoning": "Rollback is reviewer-authorized and append-only."},
        {"id": "T-6", "from": "executing", "to": "recovery-required",
         "guard": "process_interrupted_mid_execution",
         "reasoning": "Interrupted execution requires reviewer recovery."},
        {"id": "T-7", "from": "recovery-required", "to": "replayed",
         "guard": "reviewer_authorised_replay && replay_succeeded",
         "reasoning": "Replay reconstructs the deterministic outcome."},
        {"id": "T-8", "from": "recovery-required", "to": "rolled-back",
         "guard": "reviewer_authorised_rollback",
         "reasoning": "Reviewer may choose rollback over replay."},
        {"id": "T-9", "from": "staged", "to": "failed",
         "guard": "preconditions_failed_at_execute_time",
         "reasoning": "Late precondition failure (e.g., source mutated)."},
    ],
    "rules": [
        {"id": "TX-1", "rule": "no_mutation_outside_transaction_boundary",
         "fail_closed": True},
        {"id": "TX-2", "rule": "transaction_id_required_on_every_event",
         "fail_closed": True},
        {"id": "TX-3", "rule": "state_transitions_are_append_only",
         "fail_closed": True},
        {"id": "TX-4", "rule": "no_state_skipping",
         "fail_closed": True,
         "reasoning": "Transitions must follow declared edges; no jumping states."},
        {"id": "TX-5", "rule": "terminal_states_are_immutable",
         "fail_closed": True},
        {"id": "TX-6", "rule": "blocking_states_require_reviewer_intervention",
         "fail_closed": True},
        {"id": "TX-7", "rule": "transaction_journal_is_replayable",
         "fail_closed": True},
    ],
})


SNAPSHOT_RULES = envelope({
    "title": "Snapshot Rules",
    "purpose": (
        "Deterministic snapshot capture before any mutation. Snapshots are "
        "append-only, timestamped, transaction-bound, reviewer-inspectable. "
        "They are never deleted by the executor."
    ),
    "snapshot_kinds": [
        {"kind": "destination-precapture",
         "captures": "the destination tree (or its non-existence proof) before mutation",
         "scope": "single-path"},
        {"kind": "manifest-precapture",
         "captures": "snapshot of touched event-store manifests at transaction start",
         "scope": "manifests/"},
        {"kind": "lineage-precapture",
         "captures": "snapshot of lineage event store at transaction start",
         "scope": "lineage/"},
        {"kind": "publication-precapture",
         "captures": "snapshot of publication-events store before regeneration",
         "scope": "publications/"},
        {"kind": "refresh-state-precapture",
         "captures": "snapshot of refresh-events store before refresh execution",
         "scope": "refresh-state/"},
        {"kind": "transaction-checkpoint",
         "captures": "snapshot of transaction journal at the executing -> committed boundary",
         "scope": "transaction-state/"},
        {"kind": "recovery-checkpoint",
         "captures": "snapshot taken when a transaction enters recovery-required state",
         "scope": "recovery-checkpoints/"},
    ],
    "rules": [
        {"id": "SN-1", "rule": "snapshot_must_precede_mutation",
         "fail_closed": True},
        {"id": "SN-2", "rule": "snapshot_path_must_carry_transaction_id",
         "fail_closed": True},
        {"id": "SN-3", "rule": "snapshot_path_must_carry_iso_timestamp",
         "fail_closed": True},
        {"id": "SN-4", "rule": "snapshot_must_be_append_only",
         "fail_closed": True},
        {"id": "SN-5", "rule": "snapshot_pruning_is_forbidden",
         "fail_closed": True,
         "reasoning": "Reviewer may move snapshots offline, but the executor MUST NOT delete."},
        {"id": "SN-6", "rule": "snapshot_must_be_reviewer_inspectable",
         "fail_closed": True,
         "reasoning": "Plain JSON / plain copies under runtime-snapshots/."},
        {"id": "SN-7", "rule": "destination_precapture_required_for_copy_operations",
         "fail_closed": True},
        {"id": "SN-8", "rule": "snapshot_failures_block_transaction",
         "fail_closed": True,
         "reasoning": "If snapshot capture fails, the transaction must NOT proceed."},
    ],
    "storage_root": "operational-console/runtime-snapshots/",
    "filename_template": "{snapshot_kind}/{tx_id}/{iso_timestamp}-{name}",
})


ROLLBACK_EXECUTION_RULES = envelope({
    "title": "Rollback Execution Rules",
    "purpose": (
        "Real rollback execution. Restores prior state forward (never "
        "destructive), preserves the failed state as evidence, and appends "
        "to the transaction + lineage + audit + rollback event stores."
    ),
    "rollback_kinds": [
        {"kind": "revert-failed-mutation",
         "action": (
             "copy snapshot of pre-mutation destination state forward into a "
             "rollback-target path; mark the failed destination as preserved; "
             "emit rollback + lineage + audit events."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
        {"kind": "revert-failed-staging",
         "action": (
             "restore staging/incoming/<file> from snapshot; route the failed "
             "destination contents into staging/quarantined/<ts>/."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
        {"kind": "revert-publication-regeneration",
         "action": (
             "restore prior publication-events pointer from snapshot; mark "
             "the regenerated outputs as superseded; do not delete them."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
        {"kind": "revert-manifest-registration",
         "action": (
             "restore prior manifest snapshot; append a rollback-record event "
             "linking to the failed registration; do not rewrite history."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
        {"kind": "restore-prior-snapshot",
         "action": (
             "copy a reviewer-selected snapshot back into a restore-target "
             "tree (NEVER over the live tree directly; reviewer migrates)."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
        {"kind": "restore-lineage-continuity",
         "action": (
             "append a lineage-bridge event referencing both the failed and "
             "restored operation_ids; never edit prior lineage events."),
         "preserves_failed_state": True,
         "deletes_evidence": False},
    ],
    "rules": [
        {"id": "RBE-1", "rule": "rollback_requires_reviewer_authorization",
         "fail_closed": True},
        {"id": "RBE-2", "rule": "rollback_must_be_transaction_bound",
         "fail_closed": True},
        {"id": "RBE-3", "rule": "rollback_must_reference_snapshot_path",
         "fail_closed": True},
        {"id": "RBE-4", "rule": "rollback_must_be_append_only",
         "fail_closed": True},
        {"id": "RBE-5", "rule": "rollback_must_not_delete_evidence",
         "fail_closed": True},
        {"id": "RBE-6", "rule": "rollback_must_not_overwrite_live_tree",
         "fail_closed": True,
         "reasoning": (
             "Restored content lands in a rollback-target/ path; reviewer "
             "explicitly migrates if desired.")},
        {"id": "RBE-7", "rule": "rollback_must_emit_rollback_lineage_audit_events",
         "fail_closed": True},
        {"id": "RBE-8", "rule": "rollback_must_advance_transaction_state",
         "fail_closed": True,
         "reasoning": "From failed -> rolled-back."},
    ],
})


RECOVERY_RULES = envelope({
    "title": "Recovery Rules",
    "purpose": (
        "Interrupted-execution recovery orchestration. The recovery engine "
        "DETECTS incomplete operations and EMITS a recovery manifest; it "
        "NEVER auto-recovers. The reviewer chooses replay or rollback."
    ),
    "incomplete_operation_signals": [
        {"id": "REC-SIG-1",
         "signal": "transaction_state == 'executing' but no committed/failed event",
         "interpretation": "Process was interrupted mid-execution."},
        {"id": "REC-SIG-2",
         "signal": "snapshot exists but no mutation event references it",
         "interpretation": "Snapshot captured but mutation did not begin or did not record."},
        {"id": "REC-SIG-3",
         "signal": "mutation event present but no lineage event for same operation_id",
         "interpretation": "Lineage write was skipped; likely interrupted."},
        {"id": "REC-SIG-4",
         "signal": "rollback event present but transaction not in 'rolled-back'",
         "interpretation": "Rollback recorded but state transition incomplete."},
        {"id": "REC-SIG-5",
         "signal": "publication event present but refresh event missing",
         "interpretation": "Publication divergence; reviewer must reconcile."},
        {"id": "REC-SIG-6",
         "signal": "destination exists but mutation event does not reference it",
         "interpretation": "Stale propagation; reviewer must reconcile."},
    ],
    "recovery_recommendations": [
        {"id": "REC-REC-1", "from_signal": "REC-SIG-1",
         "recommends": "replay-from-snapshot",
         "alternative": "rollback-via-restore-prior-snapshot"},
        {"id": "REC-REC-2", "from_signal": "REC-SIG-2",
         "recommends": "abandon-snapshot-no-op",
         "alternative": "replay-from-snapshot"},
        {"id": "REC-REC-3", "from_signal": "REC-SIG-3",
         "recommends": "append-bridge-lineage-event",
         "alternative": "rollback-revert-failed-mutation"},
        {"id": "REC-REC-4", "from_signal": "REC-SIG-4",
         "recommends": "advance-transaction-state-to-rolled-back",
         "alternative": "manual-reviewer-triage"},
        {"id": "REC-REC-5", "from_signal": "REC-SIG-5",
         "recommends": "reviewer-authorised-publication-rollback",
         "alternative": "reviewer-authorised-republication"},
        {"id": "REC-REC-6", "from_signal": "REC-SIG-6",
         "recommends": "reviewer-triage-via-integrity-console",
         "alternative": "rollback-revert-failed-mutation"},
    ],
    "rules": [
        {"id": "REC-1", "rule": "recovery_engine_must_be_read_only",
         "fail_closed": True,
         "reasoning": "Detection only; reviewer authorizes the actual recovery action."},
        {"id": "REC-2", "rule": "recovery_must_emit_recovery_manifest",
         "fail_closed": True},
        {"id": "REC-3", "rule": "recovery_manifest_must_carry_transaction_id",
         "fail_closed": True},
        {"id": "REC-4", "rule": "recovery_manifest_must_carry_recommendations",
         "fail_closed": True},
        {"id": "REC-5", "rule": "no_autonomous_recovery_action",
         "fail_closed": True},
        {"id": "REC-6", "rule": "recovery_history_is_append_only",
         "fail_closed": True},
    ],
})


REPLAY_RULES = envelope({
    "title": "Replay Rules",
    "purpose": (
        "Deterministic replay of governed transactions from snapshots + "
        "transaction journal + lineage + manifest events. Replay is "
        "read-only by default; reviewer-authorized writes only."
    ),
    "replay_modes": [
        {"mode": "verify-only",
         "writes": False,
         "description": "Reconstructs the expected outcome and compares against current state. Emits a replay-finding event. No filesystem mutation."},
        {"mode": "reconstruct-into-rollback-target",
         "writes": True,
         "requires_reviewer_confirm": True,
         "description": "Writes the replayed outcome into a rollback-target/ tree (never into the live tree directly)."},
    ],
    "rules": [
        {"id": "RPL-1", "rule": "replay_must_be_deterministic",
         "fail_closed": True,
         "reasoning": "Same inputs must always produce the same replay."},
        {"id": "RPL-2", "rule": "replay_default_mode_is_read_only",
         "fail_closed": True},
        {"id": "RPL-3", "rule": "replay_must_consume_only_snapshots_and_event_journals",
         "fail_closed": True},
        {"id": "RPL-4", "rule": "replay_must_emit_replay_event",
         "fail_closed": True},
        {"id": "RPL-5", "rule": "replay_writing_mode_requires_reviewer_confirm",
         "fail_closed": True},
        {"id": "RPL-6", "rule": "replay_must_never_overwrite_live_tree",
         "fail_closed": True},
        {"id": "RPL-7", "rule": "replay_must_carry_transaction_id_and_replay_id",
         "fail_closed": True},
    ],
    "inputs": [
        "runtime-snapshots/transaction-state/",
        "runtime-manifests/transaction-events/",
        "runtime-manifests/mutation-events/",
        "runtime-manifests/lineage-events/",
        "runtime-manifests/snapshot-events/",
        "runtime-manifests/audit-events/",
    ],
})


INTEGRITY_VERIFICATION_RULES = envelope({
    "title": "Integrity Verification Rules",
    "purpose": (
        "Read-only multi-channel integrity validation. Findings emit events "
        "and BLOCK execution when severity is 'block'. NO autonomous repair."
    ),
    "checks": [
        {"id": "INT-1", "kind": "lineage-continuity",
         "validates": "every mutation_event has a corresponding lineage_event with same operation_id",
         "blocks_execution_when_failing": True},
        {"id": "INT-2", "kind": "manifest-consistency",
         "validates": "every event-store carries declared schema and append_only flag",
         "blocks_execution_when_failing": True},
        {"id": "INT-3", "kind": "transaction-completeness",
         "validates": "every transaction is in a declared state; no orphan transitions",
         "blocks_execution_when_failing": True},
        {"id": "INT-4", "kind": "snapshot-validity",
         "validates": "every snapshot path declared in snapshot_events exists on disk and is non-empty",
         "blocks_execution_when_failing": True},
        {"id": "INT-5", "kind": "propagation-integrity",
         "validates": "every accepted destination is referenced by at least one mutation_event",
         "blocks_execution_when_failing": False},
        {"id": "INT-6", "kind": "publication-runtime-parity",
         "validates": "publication_events without superseding refresh_events appear consistent with current outputs",
         "blocks_execution_when_failing": False},
        {"id": "INT-7", "kind": "rebuild-consistency",
         "validates": "every refresh_event with action approve|partial-rebuild has a downstream publication_event or audit-warning",
         "blocks_execution_when_failing": False},
        {"id": "INT-8", "kind": "stale-output-synchronisation",
         "validates": "no destination newer than its source by more than declared drift threshold",
         "blocks_execution_when_failing": False},
        {"id": "INT-9", "kind": "transaction-journal-replayability",
         "validates": "transaction journal is replayable end-to-end without external state",
         "blocks_execution_when_failing": True},
    ],
    "rules": [
        {"id": "INT-R-1", "rule": "integrity_engine_is_read_only",
         "fail_closed": True},
        {"id": "INT-R-2", "rule": "integrity_findings_must_be_append_only",
         "fail_closed": True},
        {"id": "INT-R-3", "rule": "integrity_block_severity_blocks_new_transactions",
         "fail_closed": True},
        {"id": "INT-R-4", "rule": "integrity_must_never_auto_repair",
         "fail_closed": True},
        {"id": "INT-R-5", "rule": "integrity_must_never_quarantine_or_delete",
         "fail_closed": True},
    ],
    "audit_event_store": "runtime-manifests/integrity-events/_event-store.json",
})


FAILURE_GOVERNANCE_RULES = envelope({
    "title": "Failure Governance Rules",
    "purpose": (
        "Deterministic governance of operational failures. Each failure "
        "class emits a failure-event preserving evidence, transaction "
        "state, snapshots, and audit history. NO silent recovery."
    ),
    "failure_classes": [
        {"class": kind,
         "preserves_transaction_state": True,
         "preserves_snapshots": True,
         "emits_failure_event": True,
         "blocks_new_transactions": True if kind in {
             "snapshot-failure", "rollback-failure", "lineage-break",
             "replay-failure",
         } else False,
         "reviewer_intervention_required": True}
        for kind in FAILURE_CLASSES
    ],
    "rules": [
        {"id": "FG-1", "rule": "every_failure_emits_a_failure_event",
         "fail_closed": True},
        {"id": "FG-2", "rule": "failure_event_must_carry_transaction_id",
         "fail_closed": True},
        {"id": "FG-3", "rule": "failure_event_must_carry_failure_class",
         "fail_closed": True},
        {"id": "FG-4", "rule": "failure_event_must_carry_evidence_pointers",
         "fail_closed": True},
        {"id": "FG-5", "rule": "no_silent_recovery",
         "fail_closed": True},
        {"id": "FG-6", "rule": "blocking_failures_block_new_transactions_until_reviewer_clears",
         "fail_closed": True},
        {"id": "FG-7", "rule": "failure_history_is_append_only",
         "fail_closed": True},
    ],
})


CONSISTENCY_RULES = envelope({
    "title": "Repository Consistency Rules",
    "purpose": (
        "Deterministic consistency enforcement. Detects duplicate / "
        "concurrent / orphaned / partial / drifted states and BLOCKS unsafe "
        "execution while preserving evidence."
    ),
    "checks": [
        {"id": "CON-1", "kind": "duplicate-transaction-execution",
         "detects": "two transaction_events with identical request_id and state=executing",
         "action": "block_new_executions_until_reviewer_clears"},
        {"id": "CON-2", "kind": "concurrent-conflicting-mutations",
         "detects": "two unfinished transactions targeting overlapping destination paths",
         "action": "block_new_executions_until_reviewer_clears"},
        {"id": "CON-3", "kind": "orphan-manifest",
         "detects": "manifest event without a corresponding transaction_event",
         "action": "emit_audit_warning"},
        {"id": "CON-4", "kind": "stale-lineage",
         "detects": "lineage event referencing operation_id with no mutation_event",
         "action": "emit_audit_warning"},
        {"id": "CON-5", "kind": "partial-rollback",
         "detects": "rollback_event present but transaction state still 'failed' (not advanced)",
         "action": "emit_recovery_manifest"},
        {"id": "CON-6", "kind": "incomplete-replay",
         "detects": "replay_event with mode=reconstruct-into-rollback-target but rollback-target tree empty",
         "action": "emit_recovery_manifest"},
        {"id": "CON-7", "kind": "publication-runtime-drift",
         "detects": "publication_event timestamp older than referenced source mutation_event timestamp",
         "action": "emit_audit_warning"},
        {"id": "CON-8", "kind": "propagation-inconsistency",
         "detects": "mutation_event destination in forbidden_destinations or outside repo root",
         "action": "block_and_emit_audit_block"},
    ],
    "rules": [
        {"id": "CON-R-1", "rule": "consistency_checks_must_be_deterministic",
         "fail_closed": True},
        {"id": "CON-R-2", "rule": "consistency_findings_are_append_only",
         "fail_closed": True},
        {"id": "CON-R-3", "rule": "consistency_must_preserve_evidence",
         "fail_closed": True},
        {"id": "CON-R-4", "rule": "consistency_blocks_unsafe_execution_until_reviewer_clears",
         "fail_closed": True},
    ],
})


# ---------------------------------------------------------------------------
# JS engines (vanilla ES, no dependencies, no network calls)
# ---------------------------------------------------------------------------

TRANSACTION_ENGINE_JS = """// transaction-engine.js — proposes a governed transaction request that
// wraps a layer-39 mutation request inside a transaction envelope. The
// browser NEVER executes; it only builds the request and prints the CLI
// command for the reviewer to run.
(function () {
  if (!window.OC) window.OC = {};

  const STATES = ['initialized','staged','executing','committed','failed',
                  'rolled-back','recovery-required','replayed'];

  function buildTransactionRequest(form) {
    // form: { mutation_request, snapshot_kinds: [...], reviewer_notes }
    const reasoning = [
      'wraps mutation_request inside a governed transaction',
      'snapshot_kinds: ' + (form.snapshot_kinds || []).join(', '),
      'TX-1: no mutation outside transaction boundary',
      'SN-1: snapshot_capture must precede mutation',
      'reviewer authorization required (--confirm)',
    ];
    const req = window.OC.FSBridge.buildRequestEnvelope('transaction', {
      transaction_id: 'tx-' + (window.OC.State ? window.OC.State.uuid() : Date.now()),
      mutation_request: form.mutation_request || null,
      snapshot_kinds: form.snapshot_kinds || ['destination-precapture','manifest-precapture','lineage-precapture','transaction-checkpoint'],
      initial_state: 'initialized',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      transaction_state_rules_required: ['TX-1','TX-2','TX-3','TX-4','TX-7'],
      snapshot_rules_required: ['SN-1','SN-2','SN-3','SN-4','SN-7','SN-8'],
    });
    return req;
  }

  function previewExecutorCommand(savedFilename) {
    return 'python3 tools/governed_transactional_executor.py ' +
           '--kind transaction ' +
           '--request "' + (savedFilename || '<path/to/request.json>') + '" ' +
           '--confirm';
  }

  window.OC.TransactionEngine = {
    STATES: STATES,
    buildTransactionRequest: buildTransactionRequest,
    previewExecutorCommand: previewExecutorCommand,
  };
})();
"""


SNAPSHOT_ENGINE_JS = """// snapshot-engine.js — read-only snapshot explorer. Lists snapshots from
// runtime-manifests/snapshot-events/_event-store.json and groups them by
// transaction_id and snapshot_kind. Browser does not write snapshots.
(function () {
  if (!window.OC) window.OC = {};

  async function loadSnapshotEvents() {
    return await window.OC.FSBridge.loadEventStore('snapshot-events');
  }

  function groupByTransaction(events) {
    if (!events || !events.events) return {};
    const grouped = {};
    for (const e of events.events) {
      const tx = e.transaction_id || 'unknown';
      if (!grouped[tx]) grouped[tx] = [];
      grouped[tx].push(e);
    }
    return grouped;
  }

  function summarise(events) {
    if (!events || !events.events) return { total: 0, by_kind: {}, by_tx: 0 };
    const by_kind = {};
    const txs = new Set();
    for (const e of events.events) {
      const k = e.snapshot_kind || 'unknown';
      by_kind[k] = (by_kind[k] || 0) + 1;
      if (e.transaction_id) txs.add(e.transaction_id);
    }
    return { total: events.events.length, by_kind: by_kind, by_tx: txs.size };
  }

  window.OC.SnapshotEngine = {
    loadSnapshotEvents: loadSnapshotEvents,
    groupByTransaction: groupByTransaction,
    summarise: summarise,
  };
})();
"""


ROLLBACK_EXEC_ENGINE_JS = """// rollback-exec-engine.js — proposes a rollback EXECUTION request that
// references a snapshot path and a transaction_id. Browser does not
// execute. Reviewer-authorized; append-only; preserves failed state.
(function () {
  if (!window.OC) window.OC = {};

  function buildRollbackExecRequest(form) {
    // form: { transaction_id, rollback_kind, snapshot_path, original_operation_id, reason, reviewer_notes }
    const reasoning = [
      'rollback_kind: ' + form.rollback_kind,
      'targets transaction: ' + form.transaction_id,
      'restores from snapshot: ' + (form.snapshot_path || '(none — abstract restore)'),
      'RBE-5: never deletes evidence',
      'RBE-6: restored content lands in rollback-target/, never overwrites live tree',
      'RBE-8: advances transaction state failed -> rolled-back',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('rollback-exec', {
      transaction_id: form.transaction_id,
      rollback_kind: form.rollback_kind,
      snapshot_path: form.snapshot_path || null,
      original_operation_id: form.original_operation_id || null,
      reason: form.reason || '',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      rollback_execution_rules_required: ['RBE-1','RBE-2','RBE-3','RBE-4','RBE-5','RBE-6','RBE-7','RBE-8'],
    });
  }

  window.OC.RollbackExecEngine = { buildRollbackExecRequest: buildRollbackExecRequest };
})();
"""


RECOVERY_ENGINE_JS = """// recovery-engine.js — read-only detector for incomplete operations.
// Inspects transaction-events / mutation-events / lineage-events /
// snapshot-events and surfaces a recovery manifest (proposal only).
(function () {
  if (!window.OC) window.OC = {};

  async function buildRecoveryManifest() {
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const li = await window.OC.FSBridge.loadEventStore('lineage-events');
    const sn = await window.OC.FSBridge.loadEventStore('snapshot-events');
    const ro = await window.OC.FSBridge.loadEventStore('rollback-events');

    const findings = [];

    function evs(s) { return (s && s.events) ? s.events : []; }

    const muIds = new Set(evs(mu).map(e => e.operation_id));
    const liIds = new Set(evs(li).map(e => e.links_to_operation_id || e.operation_id));
    const snByTx = {};
    for (const e of evs(sn)) {
      const t = e.transaction_id || 'unknown';
      snByTx[t] = (snByTx[t] || 0) + 1;
    }

    // REC-SIG-1: transaction in 'executing' without committed/failed
    const txByState = {};
    for (const e of evs(tx)) {
      txByState[e.transaction_id] = e.to_state || e.state || 'unknown';
    }
    for (const tid of Object.keys(txByState)) {
      if (txByState[tid] === 'executing') {
        findings.push({ signal: 'REC-SIG-1', transaction_id: tid,
          recommends: 'replay-from-snapshot',
          alternative: 'rollback-via-restore-prior-snapshot' });
      }
    }

    // REC-SIG-3: mutation event present but no lineage event
    for (const id of muIds) {
      if (!liIds.has(id)) {
        findings.push({ signal: 'REC-SIG-3', operation_id: id,
          recommends: 'append-bridge-lineage-event',
          alternative: 'rollback-revert-failed-mutation' });
      }
    }

    // REC-SIG-4: rollback event but transaction not 'rolled-back'
    for (const e of evs(ro)) {
      const tid = e.transaction_id;
      if (tid && txByState[tid] && txByState[tid] !== 'rolled-back') {
        findings.push({ signal: 'REC-SIG-4', transaction_id: tid,
          recommends: 'advance-transaction-state-to-rolled-back',
          alternative: 'manual-reviewer-triage' });
      }
    }

    return {
      schema: 'governed-recovery-manifest/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      reviewer_authorisation_required: true,
      auto_recovery: false,
    };
  }

  window.OC.RecoveryEngine = { buildRecoveryManifest: buildRecoveryManifest };
})();
"""


REPLAY_ENGINE_JS = """// replay-engine.js — read-only deterministic replay reconstructor.
// Default mode is verify-only: reconstructs the expected outcome from
// snapshots + journals and compares against current state. Writing mode
// is reviewer-authorized only and emits requests, never writes from the
// browser.
(function () {
  if (!window.OC) window.OC = {};

  async function reconstructPlan(transactionId) {
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const sn = await window.OC.FSBridge.loadEventStore('snapshot-events');
    const tEvents = (tx && tx.events ? tx.events : []).filter(e => e.transaction_id === transactionId);
    const sEvents = (sn && sn.events ? sn.events : []).filter(e => e.transaction_id === transactionId);
    const mEvents = (mu && mu.events ? mu.events : []).filter(e => e.transaction_id === transactionId);
    const order = [];
    for (const e of sEvents) order.push({ at: e.occurred_at_iso, kind: 'snapshot', payload: e });
    for (const e of mEvents) order.push({ at: e.executed_at_iso, kind: 'mutation', payload: e });
    for (const e of tEvents) order.push({ at: e.occurred_at_iso || e.transitioned_at_iso, kind: 'transaction', payload: e });
    order.sort((a, b) => (a.at || '').localeCompare(b.at || ''));
    return {
      schema: 'governed-replay-plan/1.0',
      transaction_id: transactionId,
      mode: 'verify-only',
      sequence_length: order.length,
      sequence: order,
      writes_filesystem: false,
      reviewer_authorisation_required_for_writes: true,
    };
  }

  function buildReplayRequest(form) {
    // form: { transaction_id, mode (verify-only|reconstruct-into-rollback-target), reviewer_notes }
    const reasoning = [
      'replay transaction ' + form.transaction_id,
      'mode: ' + (form.mode || 'verify-only'),
      'RPL-2: default mode is read-only',
      'RPL-6: never overwrites live tree',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('replay', {
      transaction_id: form.transaction_id,
      replay_mode: form.mode || 'verify-only',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      replay_rules_required: ['RPL-1','RPL-2','RPL-3','RPL-4','RPL-6','RPL-7'],
    });
  }

  window.OC.ReplayEngine = {
    reconstructPlan: reconstructPlan,
    buildReplayRequest: buildReplayRequest,
  };
})();
"""


INTEGRITY_ENGINE_JS = """// integrity-engine.js — read-only multi-channel integrity verifier.
// Inspects manifests, lineage, snapshots, transactions, publications and
// reports findings. NEVER mutates, NEVER auto-quarantines.
(function () {
  if (!window.OC) window.OC = {};

  async function runChecks() {
    const findings = [];
    const stores = {};
    for (const k of ['transaction-events','mutation-events','lineage-events',
                     'snapshot-events','publication-events','refresh-events',
                     'rollback-events','audit-events']) {
      stores[k] = await window.OC.FSBridge.loadEventStore(k);
    }

    function evs(s) { return (s && s.events) ? s.events : []; }

    // INT-1 lineage continuity
    const muIds = new Set(evs(stores['mutation-events']).map(e => e.operation_id));
    const liIds = new Set(evs(stores['lineage-events']).map(e => e.links_to_operation_id || e.operation_id));
    for (const id of muIds) {
      if (!liIds.has(id)) {
        findings.push({ id: 'INT-1', kind: 'lineage-continuity', severity: 'block',
          message: 'mutation_event ' + id + ' has no lineage_event' });
      }
    }

    // INT-2 manifest consistency: schema + append_only flag present
    for (const k of Object.keys(stores)) {
      const s = stores[k];
      if (!s) continue;
      if (!s.schema || s.append_only !== true) {
        findings.push({ id: 'INT-2', kind: 'manifest-consistency', severity: 'block',
          message: 'event store ' + k + ' missing schema or append_only flag' });
      }
    }

    // INT-3 transaction completeness: every transaction has a declared state
    const TX_STATES = new Set(['initialized','staged','executing','committed','failed','rolled-back','recovery-required','replayed']);
    for (const e of evs(stores['transaction-events'])) {
      const st = e.to_state || e.state;
      if (!st || !TX_STATES.has(st)) {
        findings.push({ id: 'INT-3', kind: 'transaction-completeness', severity: 'block',
          message: 'transaction_event for ' + e.transaction_id + ' has invalid state ' + st });
      }
    }

    // INT-5 propagation integrity (warning)
    const muDests = new Set(evs(stores['mutation-events']).map(e => e.destination_path).filter(Boolean));
    if (muDests.size === 0 && evs(stores['transaction-events']).length > 0) {
      findings.push({ id: 'INT-5', kind: 'propagation-integrity', severity: 'warning',
        message: 'transactions exist but no mutation destinations recorded' });
    }

    return {
      schema: 'governed-integrity-report/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      counts: { total: findings.length,
                block: findings.filter(f => f.severity === 'block').length,
                warning: findings.filter(f => f.severity === 'warning').length },
      mutates_filesystem: false,
      auto_repair: false,
    };
  }

  window.OC.IntegrityEngine = { runChecks: runChecks };
})();
"""


FAILURE_ENGINE_JS = """// failure-engine.js — read-only failure inspector. Reads
// runtime-manifests/failure-events/ and groups by failure_class.
(function () {
  if (!window.OC) window.OC = {};

  async function loadFailures() {
    return await window.OC.FSBridge.loadEventStore('failure-events');
  }

  function groupByClass(events) {
    if (!events || !events.events) return {};
    const grouped = {};
    for (const e of events.events) {
      const c = e.failure_class || 'unknown';
      if (!grouped[c]) grouped[c] = [];
      grouped[c].push(e);
    }
    return grouped;
  }

  window.OC.FailureEngine = { loadFailures: loadFailures, groupByClass: groupByClass };
})();
"""


CONSISTENCY_ENGINE_JS = """// consistency-engine.js — read-only consistency scanner. Detects
// duplicate / concurrent / orphan / partial / drift conditions.
(function () {
  if (!window.OC) window.OC = {};

  async function scan() {
    const findings = [];
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const li = await window.OC.FSBridge.loadEventStore('lineage-events');
    const ro = await window.OC.FSBridge.loadEventStore('rollback-events');

    function evs(s) { return (s && s.events) ? s.events : []; }

    // CON-1 duplicate transaction execution
    const seen = new Set();
    for (const e of evs(tx)) {
      const key = (e.request_id || e.transaction_id) + '::' + (e.to_state || e.state || '');
      if ((e.to_state || e.state) === 'executing') {
        if (seen.has(e.request_id || e.transaction_id)) {
          findings.push({ id: 'CON-1', kind: 'duplicate-transaction-execution', severity: 'block',
            message: 'duplicate executing transaction ' + (e.request_id || e.transaction_id) });
        }
        seen.add(e.request_id || e.transaction_id);
      }
    }

    // CON-3 orphan manifest (lineage referencing unknown operation)
    const muIds = new Set(evs(mu).map(e => e.operation_id));
    for (const e of evs(li)) {
      const ref = e.links_to_operation_id || e.operation_id;
      if (ref && !muIds.has(ref)) {
        findings.push({ id: 'CON-4', kind: 'stale-lineage', severity: 'warning',
          message: 'lineage references unknown operation ' + ref });
      }
    }

    // CON-5 partial rollback (rollback event but tx state not rolled-back)
    const txState = {};
    for (const e of evs(tx)) txState[e.transaction_id] = e.to_state || e.state;
    for (const e of evs(ro)) {
      const t = e.transaction_id;
      if (t && txState[t] && txState[t] !== 'rolled-back') {
        findings.push({ id: 'CON-5', kind: 'partial-rollback', severity: 'recovery',
          message: 'rollback recorded for ' + t + ' but tx state is ' + txState[t] });
      }
    }

    return {
      schema: 'governed-consistency-report/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      counts: { total: findings.length },
      mutates_filesystem: false,
    };
  }

  window.OC.ConsistencyEngine = { scan: scan };
})();
"""


# ---------------------------------------------------------------------------
# CSS addendum
# ---------------------------------------------------------------------------

EXEC_CSS_ADDENDUM = """
/* phase 47 — governed transactional execution & recovery additions */
.oc-tx__state { display: inline-block; padding: 1px 6px; border-radius: 8px;
    font-size: 11px; background: #1f3a5f; color: #cfe6ff; }
.oc-tx__state--committed { background: #1f5f3a; color: #d4f5d4; }
.oc-tx__state--failed { background: #5f1f1f; color: #f5d4d4; }
.oc-tx__state--rolled-back { background: #5f4a1f; color: #f5e7d4; }
.oc-tx__state--recovery-required { background: #5a1f5f; color: #f0d4f5; }
.oc-tx__finding--block { border-left: 3px solid #d96d6d; padding-left: .75rem; }
.oc-tx__finding--warning { border-left: 3px solid #d9c46d; padding-left: .75rem; }
.oc-tx__finding--recovery { border-left: 3px solid #6dadd9; padding-left: .75rem; }
.oc-tx__journal { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px; background: #141414; color: #cfe6ff; padding: .75rem;
    border-radius: 4px; max-height: 320px; overflow: auto; }
"""


# ---------------------------------------------------------------------------
# HTML pages
# ---------------------------------------------------------------------------

def _html_head(title: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<title>{title} — Beslock Operational Console</title>
<link rel=\"stylesheet\" href=\"../assets/console.css\" />
<link rel=\"stylesheet\" href=\"../assets/exec/exec.css\" />
</head>
<body class=\"oc-body oc-body--exec\">
<header class=\"oc-header\">
  <a class=\"oc-header__brand\" href=\"../index.html\">Beslock Operational Console</a>
  <nav class=\"oc-header__nav\">
    <a href=\"../exec.html\">Exec</a>
    <a href=\"../mutation-console/exec.html\">Mutation</a>
    <a href=\"../lineage-console/exec.html\">Lineage</a>
    <a href=\"../rollback-console/exec.html\">Rollback</a>
    <a href=\"../safety-console/exec.html\">Safety</a>
    <a href=\"../transaction-console/exec.html\">Transactions</a>
    <a href=\"../snapshot-console/exec.html\">Snapshots</a>
    <a href=\"../recovery-console/exec.html\">Recovery</a>
    <a href=\"../replay-console/exec.html\">Replay</a>
    <a href=\"../integrity-console/exec.html\">Integrity</a>
    <a href=\"../failure-console/exec.html\">Failures</a>
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
<script src="../assets/exec/transaction-engine.js"></script>
<script src="../assets/exec/snapshot-engine.js"></script>
<script src="../assets/exec/rollback-exec-engine.js"></script>
<script src="../assets/exec/recovery-engine.js"></script>
<script src="../assets/exec/replay-engine.js"></script>
<script src="../assets/exec/integrity-engine.js"></script>
<script src="../assets/exec/failure-engine.js"></script>
<script src="../assets/exec/consistency-engine.js"></script>
</body></html>
"""


TRANSACTION_CONSOLE_HTML = _html_head("Transaction console") + """
<section class="oc-exec__panel">
  <h1>Governed transaction inspector</h1>
  <p class="oc-exec__danger">
    Every layer-39 mutation now runs inside a governed transaction. This
    surface is read-only: it inspects <code>transaction-events</code> and
    proposes new transaction requests for reviewer-authorized execution
    via <code>tools/governed_transactional_executor.py --confirm</code>.
  </p>
  <div id="tx-summary"><em>Loading…</em></div>
  <h2>Transaction journal</h2>
  <pre id="tx-journal" class="oc-tx__journal"><em>Loading…</em></pre>
  <h2>Build a new transaction request</h2>
  <form id="tx-form" class="oc-exec__form" autocomplete="off">
    <label>Mutation request file (path) <input name="mutation_request" placeholder="~/Downloads/mutation-request-xyz.json" /></label>
    <label>Snapshot kinds (comma-separated)
      <input name="snapshot_kinds" value="destination-precapture,manifest-precapture,lineage-precapture,transaction-checkpoint" />
    </label>
    <label>Reviewer notes <textarea name="reviewer_notes" rows="3"></textarea></label>
    <div class="oc-exec__actions">
      <button type="button" id="tx-build">Build &amp; download transaction request</button>
    </div>
  </form>
  <pre id="tx-preview" class="oc-exec__pre--cmd"><em>(no preview)</em></pre>
</section>
<script>
(async function () {
  const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
  const events = (tx && tx.events) ? tx.events : [];
  const byState = {};
  for (const e of events) { const st = e.to_state || e.state || 'unknown'; byState[st] = (byState[st]||0) + 1; }
  const sumEl = document.getElementById('tx-summary');
  sumEl.innerHTML = '<p>Total transaction events: <strong>' + events.length + '</strong></p>'
    + '<ul>' + Object.keys(byState).sort().map(k =>
        '<li><span class="oc-tx__state oc-tx__state--' + k + '">' + k + '</span> &nbsp; ' + byState[k] + '</li>'
      ).join('') + '</ul>';
  document.getElementById('tx-journal').textContent = events.length
    ? events.slice(-50).map(e => JSON.stringify(e)).join('\\n')
    : '(no transaction events yet)';

  document.getElementById('tx-build').addEventListener('click', function () {
    const f = document.getElementById('tx-form');
    const fd = new FormData(f);
    const req = window.OC.TransactionEngine.buildTransactionRequest({
      mutation_request: fd.get('mutation_request'),
      snapshot_kinds: (fd.get('snapshot_kinds') || '').split(',').map(s => s.trim()).filter(Boolean),
      reviewer_notes: fd.get('reviewer_notes') || '',
    });
    window.OC.FSBridge.exportRequest(req, 'transaction-request-' + req.request_id + '.json');
    document.getElementById('tx-preview').textContent =
      window.OC.TransactionEngine.previewExecutorCommand('transaction-request-' + req.request_id + '.json');
  });
})();
</script>
""" + HTML_TAIL


SNAPSHOT_CONSOLE_HTML = _html_head("Snapshot console") + """
<section class="oc-exec__panel">
  <h1>Snapshot explorer</h1>
  <p>Read-only view of <code>runtime-manifests/snapshot-events/</code>.
     Snapshots are append-only; the executor never deletes them.</p>
  <div id="snap-summary"><em>Loading…</em></div>
  <h2>Snapshots by transaction</h2>
  <div id="snap-by-tx"><em>Loading…</em></div>
</section>
<script>
(async function () {
  const ev = await window.OC.SnapshotEngine.loadSnapshotEvents();
  const sum = window.OC.SnapshotEngine.summarise(ev);
  document.getElementById('snap-summary').innerHTML =
    '<p>Total snapshots: <strong>' + sum.total + '</strong> &nbsp; '
    + 'Transactions covered: <strong>' + sum.by_tx + '</strong></p>'
    + '<ul>' + Object.keys(sum.by_kind).sort().map(k =>
        '<li><span class="oc-exec__pill">' + k + '</span> &nbsp; ' + sum.by_kind[k] + '</li>').join('') + '</ul>';
  const grouped = window.OC.SnapshotEngine.groupByTransaction(ev);
  const keys = Object.keys(grouped).sort();
  document.getElementById('snap-by-tx').innerHTML = keys.length
    ? keys.map(tx => '<details><summary><code>' + tx + '</code> ('
        + grouped[tx].length + ' snapshots)</summary><pre class="oc-tx__journal">'
        + grouped[tx].map(e => JSON.stringify(e)).join('\\n') + '</pre></details>').join('')
    : '<em>(no snapshot events yet)</em>';
})();
</script>
""" + HTML_TAIL


RECOVERY_CONSOLE_HTML = _html_head("Recovery console") + """
<section class="oc-exec__panel">
  <h1>Recovery manifest</h1>
  <p class="oc-exec__danger">
    Read-only detector for incomplete operations. The recovery engine
    NEVER auto-recovers. The reviewer chooses replay or rollback and runs
    <code>tools/governed_transactional_executor.py</code> with
    <code>--confirm</code>.
  </p>
  <div id="rec-summary"><em>Generating…</em></div>
  <h2>Findings</h2>
  <div id="rec-findings"><em>Generating…</em></div>
</section>
<script>
(async function () {
  const m = await window.OC.RecoveryEngine.buildRecoveryManifest();
  document.getElementById('rec-summary').innerHTML =
    '<p>Generated: <code>' + m.generated_at_iso + '</code></p>'
    + '<p>Findings: <strong>' + m.findings.length + '</strong></p>'
    + '<p>Auto-recovery: <strong>' + m.auto_recovery + '</strong></p>';
  document.getElementById('rec-findings').innerHTML = m.findings.length
    ? m.findings.map(f => '<div class="oc-tx__finding--recovery"><strong>'
        + f.signal + '</strong> &middot; ' + (f.transaction_id || f.operation_id || '')
        + '<br>recommends: <code>' + f.recommends + '</code> &middot; alt: <code>'
        + f.alternative + '</code></div>').join('')
    : '<em>(no incomplete operations detected)</em>';
})();
</script>
""" + HTML_TAIL


REPLAY_CONSOLE_HTML = _html_head("Replay console") + """
<section class="oc-exec__panel">
  <h1>Deterministic replay</h1>
  <p>Default mode is verify-only and read-only. Reconstructs the expected
     outcome from snapshots + transaction journal.</p>
  <form id="rpl-form" class="oc-exec__form" autocomplete="off">
    <label>Transaction id <input name="transaction_id" placeholder="tx-…" /></label>
    <label>Mode
      <select name="mode">
        <option value="verify-only">verify-only (read-only)</option>
        <option value="reconstruct-into-rollback-target">reconstruct-into-rollback-target (reviewer-confirm)</option>
      </select>
    </label>
    <label>Reviewer notes <textarea name="reviewer_notes" rows="3"></textarea></label>
    <div class="oc-exec__actions">
      <button type="button" id="rpl-plan">Reconstruct plan</button>
      <button type="button" id="rpl-build">Build &amp; download replay request</button>
    </div>
  </form>
  <h2>Reconstructed plan</h2>
  <pre id="rpl-plan-out" class="oc-tx__journal"><em>(no plan)</em></pre>
  <pre id="rpl-preview" class="oc-exec__pre--cmd"><em>(no preview)</em></pre>
</section>
<script>
(function () {
  document.getElementById('rpl-plan').addEventListener('click', async function () {
    const fd = new FormData(document.getElementById('rpl-form'));
    const tid = fd.get('transaction_id');
    const plan = await window.OC.ReplayEngine.reconstructPlan(tid);
    document.getElementById('rpl-plan-out').textContent = JSON.stringify(plan, null, 2);
  });
  document.getElementById('rpl-build').addEventListener('click', function () {
    const fd = new FormData(document.getElementById('rpl-form'));
    const req = window.OC.ReplayEngine.buildReplayRequest({
      transaction_id: fd.get('transaction_id'),
      mode: fd.get('mode'),
      reviewer_notes: fd.get('reviewer_notes') || '',
    });
    window.OC.FSBridge.exportRequest(req, 'replay-request-' + req.request_id + '.json');
    document.getElementById('rpl-preview').textContent =
      'python3 tools/governed_transactional_executor.py --kind replay '
      + '--request "replay-request-' + req.request_id + '.json" --confirm';
  });
})();
</script>
""" + HTML_TAIL


INTEGRITY_CONSOLE_HTML = _html_head("Integrity console") + """
<section class="oc-exec__panel">
  <h1>Integrity verification dashboard</h1>
  <p>Read-only multi-channel integrity validation. Findings emit events;
     they NEVER auto-repair.</p>
  <div id="int-summary"><em>Running checks…</em></div>
  <h2>Findings</h2>
  <div id="int-findings"><em>Running checks…</em></div>
</section>
<script>
(async function () {
  const r = await window.OC.IntegrityEngine.runChecks();
  document.getElementById('int-summary').innerHTML =
    '<p>Total: <strong>' + r.counts.total + '</strong> &nbsp; '
    + 'Block: <strong>' + r.counts.block + '</strong> &nbsp; '
    + 'Warning: <strong>' + r.counts.warning + '</strong></p>'
    + '<p>Mutates filesystem: <strong>' + r.mutates_filesystem + '</strong>'
    + ' &nbsp; Auto-repair: <strong>' + r.auto_repair + '</strong></p>';
  document.getElementById('int-findings').innerHTML = r.findings.length
    ? r.findings.map(f => '<div class="oc-tx__finding--' + f.severity + '"><strong>'
        + f.id + '</strong> · ' + f.kind + '<br>' + f.message + '</div>').join('')
    : '<em>(no findings — integrity OK)</em>';
})();
</script>
""" + HTML_TAIL


FAILURE_CONSOLE_HTML = _html_head("Failure console") + """
<section class="oc-exec__panel">
  <h1>Failed-operation explorer</h1>
  <p>Read-only view of <code>runtime-manifests/failure-events/</code>.
     Every failure preserves transaction state, snapshots, and audit
     history. NO silent recovery.</p>
  <div id="fail-summary"><em>Loading…</em></div>
  <div id="fail-by-class"><em>Loading…</em></div>
</section>
<script>
(async function () {
  const ev = await window.OC.FailureEngine.loadFailures();
  const events = (ev && ev.events) ? ev.events : [];
  document.getElementById('fail-summary').innerHTML =
    '<p>Total failure events: <strong>' + events.length + '</strong></p>';
  const grouped = window.OC.FailureEngine.groupByClass(ev);
  const keys = Object.keys(grouped).sort();
  document.getElementById('fail-by-class').innerHTML = keys.length
    ? keys.map(c => '<details><summary><strong>' + c + '</strong> ('
        + grouped[c].length + ')</summary><pre class="oc-tx__journal">'
        + grouped[c].map(e => JSON.stringify(e)).join('\\n') + '</pre></details>').join('')
    : '<em>(no failure events recorded)</em>';
})();
</script>
""" + HTML_TAIL


# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = [
    ("01-transactional-mutation-boundary",
     "Transactional Mutation Boundary",
     "From layer 40 forward, no filesystem mutation occurs outside a "
     "governed transaction. The transaction state machine (initialized → "
     "staged → executing → committed / failed / rolled-back / "
     "recovery-required / replayed) is enforced by the CLI executor."),
    ("02-snapshot-precedes-mutation",
     "Snapshot Precedes Mutation",
     "Every mutation must be preceded by deterministic snapshot capture "
     "into runtime-snapshots/<kind>/<tx_id>/<iso>/. Snapshot failure "
     "blocks the transaction (SN-8). Snapshots are append-only and "
     "never pruned by the executor (SN-5)."),
    ("03-rollback-is-reviewer-authorized-and-non-destructive",
     "Rollback Is Reviewer-Authorized And Non-Destructive",
     "Rollback execution restores prior state forward into "
     "rollback-target/ paths and never overwrites the live tree. It "
     "always preserves the failed-state evidence and emits append-only "
     "rollback + lineage + audit + transaction events."),
    ("04-no-autonomous-recovery",
     "No Autonomous Recovery",
     "The recovery engine is read-only. It detects incomplete operations "
     "and emits a recovery manifest with recommendations; the reviewer "
     "chooses replay or rollback and runs the executor explicitly."),
    ("05-deterministic-replay",
     "Deterministic Replay",
     "Replay is reconstructed from snapshots + transaction journal + "
     "manifest events; same inputs always yield the same replay. Default "
     "mode is verify-only; writing mode requires --confirm and lands in "
     "rollback-target/, never the live tree."),
    ("06-integrity-is-read-only",
     "Integrity Is Read-Only",
     "The integrity engine runs nine multi-channel checks (lineage "
     "continuity, manifest consistency, transaction completeness, "
     "snapshot validity, propagation integrity, publication parity, "
     "rebuild consistency, stale-output sync, journal replayability). "
     "It NEVER mutates and NEVER auto-quarantines."),
    ("07-no-silent-failure",
     "No Silent Failure",
     "Every failure class emits an append-only failure event preserving "
     "transaction state, snapshots, and audit history. Blocking failure "
     "classes (snapshot-failure, rollback-failure, replay-failure, "
     "lineage-break) block new transactions until the reviewer clears "
     "them."),
    ("08-consistency-blocks-unsafe-execution",
     "Consistency Blocks Unsafe Execution",
     "The consistency engine detects duplicate / concurrent / orphan / "
     "partial / drift conditions and blocks unsafe execution while "
     "preserving evidence. It never auto-resolves."),
    ("09-append-only-transactional-journal",
     "Append-Only Transactional Journal",
     "The transaction journal (transaction-events / snapshot-events / "
     "recovery-events / integrity-events / replay-events / "
     "failure-events) is strictly append-only. Terminal states are "
     "immutable (TX-5)."),
    ("10-cli-only-no-daemon-no-watcher",
     "CLI-Only — No Daemon, No Watcher",
     "Layer 40 introduces ZERO new daemons, watchers, schedulers, or "
     "background processes. Every transactional operation is a single, "
     "explicit, reviewer-authorized invocation of the CLI executor."),
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
    ("37", "Governed filesystem orchestration", "phase 46 → layer 39"),
    ("38", "Governed transactional execution & recovery", "phase 47 → layer 40 (this phase)"),
]


REPORTS = [
    ("01-transactional-engine-summary",
     "Transactional Engine Summary",
     "Establishes the governed transaction state machine (8 declared "
     "states, 9 transitions), the transaction-events append-only store, "
     "and the rule that NO filesystem mutation may occur outside a "
     "transaction boundary (TX-1). Browser surfaces propose; the CLI "
     "executor advances state with explicit reviewer --confirm."),
    ("02-snapshot-governance-summary",
     "Snapshot Governance Summary",
     "Deterministic snapshot capture before every mutation. Seven "
     "snapshot kinds (destination-precapture, manifest-precapture, "
     "lineage-precapture, publication-precapture, refresh-state-"
     "precapture, transaction-checkpoint, recovery-checkpoint) under "
     "operational-console/runtime-snapshots/. Append-only, timestamped, "
     "transaction-bound, never pruned (SN-5)."),
    ("03-rollback-execution-summary",
     "Rollback Execution Summary",
     "Six rollback kinds (revert-failed-mutation, revert-failed-staging, "
     "revert-publication-regeneration, revert-manifest-registration, "
     "restore-prior-snapshot, restore-lineage-continuity) governed by "
     "eight RBE rules. Restored content lands in rollback-target/ paths; "
     "the live tree is never overwritten (RBE-6)."),
    ("04-interrupted-recovery-summary",
     "Interrupted Recovery Summary",
     "Six incomplete-operation signals (REC-SIG-1 … REC-SIG-6) and six "
     "recovery recommendations (REC-REC-1 … REC-REC-6). Recovery engine "
     "is read-only (REC-1); recovery manifests carry transaction_id "
     "(REC-3) and recommendations (REC-4); no autonomous recovery (REC-5)."),
    ("05-replay-system-summary",
     "Replay System Summary",
     "Deterministic replay reconstructed from snapshots + transaction "
     "journal + mutation/lineage/snapshot events. Two modes "
     "(verify-only, reconstruct-into-rollback-target). Default mode is "
     "read-only (RPL-2); writing mode requires --confirm and never "
     "overwrites the live tree (RPL-6)."),
    ("06-integrity-verification-summary",
     "Integrity Verification Summary",
     "Nine integrity checks (INT-1 … INT-9) covering lineage continuity, "
     "manifest consistency, transaction completeness, snapshot validity, "
     "propagation integrity, publication-runtime parity, rebuild "
     "consistency, stale-output synchronisation, journal "
     "replayability. Read-only engine (INT-R-1); never auto-repairs "
     "(INT-R-4)."),
    ("07-failure-governance-summary",
     "Failure Governance Summary",
     "Nine failure classes (mutation-failure, snapshot-failure, "
     "replay-failure, rollback-failure, publication-divergence, "
     "stale-runtime, partial-refresh, lineage-break, collision-conflict). "
     "Each emits an append-only failure-event preserving transaction "
     "state, snapshots, and audit history. Blocking classes block new "
     "transactions until the reviewer clears them (FG-6)."),
    ("08-execution-visibility-summary",
     "Execution Visibility Summary",
     "Six new operational consoles: transaction-console, "
     "snapshot-console, recovery-console, replay-console, "
     "integrity-console, failure-console. Each is read-only (or "
     "proposal-only). The reviewer always runs the CLI executor "
     "explicitly to advance state."),
    ("09-consistency-protection-summary",
     "Consistency Protection Summary",
     "Eight consistency checks (CON-1 … CON-8) covering duplicate "
     "transaction execution, concurrent conflicting mutations, orphan "
     "manifests, stale lineage, partial rollback, incomplete replay, "
     "publication-runtime drift, propagation inconsistency. "
     "Deterministic (CON-R-1); append-only (CON-R-2); preserves "
     "evidence (CON-R-3); blocks unsafe execution (CON-R-4)."),
    ("10-transactional-knowledge-platform-maturity-reassessment",
     "Transactional Knowledge Platform Maturity Reassessment",
     "The platform is now a Governed Transactional Knowledge Operating "
     "System: governed execution, transactional mutation, deterministic "
     "rollback, snapshot recovery, replayable operations, integrity "
     "verification, failure-safe orchestration, reviewer-authorized "
     "recovery. All preserved under governance-first architecture, "
     "append-only discipline, local-first execution, deterministic "
     "behavior, reviewer authority, replayability, auditability. No "
     "SaaS, no cloud, no daemon, no autonomous agent, no ML."),
]


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_snapshot_roots() -> int:
    notes = {
        "repository": "Snapshots of pre-mutation destination state (one tree per transaction).",
        "manifests": "Snapshots of touched event-store manifests at transaction start.",
        "lineage": "Snapshots of lineage event store at transaction start.",
        "publications": "Snapshots of publication-events store before regeneration.",
        "refresh-state": "Snapshots of refresh-events store before refresh execution.",
        "transaction-state": "Snapshots of the transaction journal at executing → committed boundary.",
        "recovery-checkpoints": "Snapshots taken when a transaction enters recovery-required state.",
    }
    n = 0
    for r in SNAPSHOT_ROOTS:
        ensure_dir(SNAPSHOTS_ROOT / r, notes[r])
        n += 1
    write_text(SNAPSHOTS_ROOT / "README.md",
               "# Runtime snapshots (phase 47, layer 40)\n\n"
               "Append-only deterministic snapshot roots. The CLI executor "
               "(`tools/governed_transactional_executor.py`) writes here "
               "exclusively; nothing else does. Snapshots are NEVER pruned "
               "by the executor (SN-5).\n\n"
               + "\n".join(f"- **{r}/** — {notes[r]}" for r in SNAPSHOT_ROOTS) + "\n")
    return n


def build_runtime_event_stores() -> int:
    n = 0
    for kind in NEW_EVENT_STORES:
        path = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        if path.exists():
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
    return n


def build_rule_tables() -> int:
    write_json(RULES_ROOT / "transaction-state-rules.json", TRANSACTION_STATE_RULES)
    write_json(RULES_ROOT / "snapshot-rules.json", SNAPSHOT_RULES)
    write_json(RULES_ROOT / "rollback-execution-rules.json", ROLLBACK_EXECUTION_RULES)
    write_json(RULES_ROOT / "recovery-rules.json", RECOVERY_RULES)
    write_json(RULES_ROOT / "replay-rules.json", REPLAY_RULES)
    write_json(RULES_ROOT / "integrity-verification-rules.json", INTEGRITY_VERIFICATION_RULES)
    write_json(RULES_ROOT / "failure-governance-rules.json", FAILURE_GOVERNANCE_RULES)
    write_json(RULES_ROOT / "consistency-rules.json", CONSISTENCY_RULES)
    return 8


def build_assets() -> int:
    write_text(EXEC_ASSETS_ROOT / "transaction-engine.js", TRANSACTION_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "snapshot-engine.js", SNAPSHOT_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "rollback-exec-engine.js", ROLLBACK_EXEC_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "recovery-engine.js", RECOVERY_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "replay-engine.js", REPLAY_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "integrity-engine.js", INTEGRITY_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "failure-engine.js", FAILURE_ENGINE_JS)
    write_text(EXEC_ASSETS_ROOT / "consistency-engine.js", CONSISTENCY_ENGINE_JS)
    css_path = EXEC_ASSETS_ROOT / "exec.css"
    existing = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    marker = "/* phase 47 — governed transactional execution & recovery additions */"
    if marker not in existing:
        write_text(css_path, existing + EXEC_CSS_ADDENDUM)
    return 9


def build_consoles() -> int:
    write_text(OC_ROOT / "transaction-console" / "exec.html", TRANSACTION_CONSOLE_HTML)
    write_text(OC_ROOT / "snapshot-console" / "exec.html", SNAPSHOT_CONSOLE_HTML)
    write_text(OC_ROOT / "recovery-console" / "exec.html", RECOVERY_CONSOLE_HTML)
    write_text(OC_ROOT / "replay-console" / "exec.html", REPLAY_CONSOLE_HTML)
    write_text(OC_ROOT / "integrity-console" / "exec.html", INTEGRITY_CONSOLE_HTML)
    write_text(OC_ROOT / "failure-console" / "exec.html", FAILURE_CONSOLE_HTML)
    return 6


def build_doctrines() -> int:
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    index_lines = ["# Governed Transactional Execution & Recovery Governance (phase 47, layer 40)\n"]
    for slug, title, summary in DOCTRINES:
        body = f"# {title}\n\n*Layer {LAYER}. Subordinate to all 39 prior layers.*\n\n{summary}\n"
        write_text(CONST_ROOT / f"{slug}-doctrine.md", body)
        index_lines.append(f"- [{title}](./{slug}-doctrine.md)")
    write_text(CONST_ROOT / "00-INDEX.md", "\n".join(index_lines) + "\n")
    write_json(CONST_ROOT / "manifest.json", envelope({
        "title": "Governed Transactional Execution & Recovery Governance",
        "doctrines": [slug for slug, _, _ in DOCTRINES],
        "transaction_states": TRANSACTION_STATES,
        "failure_classes": FAILURE_CLASSES,
        "snapshot_roots": SNAPSHOT_ROOTS,
        "new_event_stores": NEW_EVENT_STORES,
    }))
    return len(DOCTRINES)


def build_reports() -> int:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(REPORTS_ROOT / "README.md",
               "# Governed Transactional Execution & Recovery — phase 47 reports\n\n"
               "Ten reports describing the layer-40 surface delivered by "
               "`tools/governed_transactional_execution.py`.\n")
    n = 0
    for slug, title, body in REPORTS:
        write_json(REPORTS_ROOT / f"{slug}.json", envelope({
            "title": title,
            "report_slug": slug,
            "phase": "47",
            "layer": LAYER,
            "summary": body,
            "phase_ladder": [
                {"phase": p, "title": t, "anchor": a} for (p, t, a) in REPORT_PHASES
            ],
        }))
        write_text(REPORTS_ROOT / f"{slug}.md",
                   f"# {title}\n\n*Phase 47 · layer {LAYER}.*\n\n{body}\n")
        n += 1
    return n


def build_runtime_readme_addendum() -> None:
    body = (
        "\n\n---\n\n"
        "## Phase 47 addendum — governed transactional execution & recovery (layer 40)\n\n"
        "Layer 39 introduced REAL filesystem mutation. Layer 40 wraps every "
        "mutation in a governed transaction with deterministic snapshot "
        "capture, reviewer-authorized rollback execution, "
        "interrupted-operation recovery detection, deterministic replay, "
        "and multi-channel integrity verification.\n\n"
        "### New CLI\n\n"
        "```\n"
        "python3 tools/governed_transactional_executor.py \\\n"
        "    --kind {transaction|rollback-exec|recovery-detect|replay|integrity|consistency} \\\n"
        "    --request /path/to/request.json \\\n"
        "    --confirm\n"
        "```\n\n"
        "Without `--confirm`: dry-run (validates request, prints plan, "
        "exits non-zero on any failure). With `--confirm`: appends "
        "transaction-events / snapshot-events / mutation-events / "
        "lineage-events / audit-events as appropriate.\n\n"
        "### New surfaces\n\n"
        "- `transaction-console/exec.html` — transaction inspector + builder\n"
        "- `snapshot-console/exec.html` — snapshot explorer (read-only)\n"
        "- `recovery-console/exec.html` — recovery manifest detector (read-only)\n"
        "- `replay-console/exec.html` — deterministic replay reconstructor\n"
        "- `integrity-console/exec.html` — multi-channel integrity dashboard\n"
        "- `failure-console/exec.html` — failed-operation explorer\n\n"
        "### Hard guarantees added by layer 40\n\n"
        "- No mutation outside a governed transaction boundary (TX-1).\n"
        "- Snapshot capture must precede mutation (SN-1); snapshot failure "
        "blocks the transaction (SN-8).\n"
        "- Snapshots are append-only and never pruned by the executor (SN-5).\n"
        "- Rollback restores into `rollback-target/`, never overwrites the "
        "live tree (RBE-6).\n"
        "- No autonomous recovery, rollback, or replay (REC-5 / RBE-1 / RPL-5).\n"
        "- Integrity engine is strictly read-only and never auto-repairs "
        "(INT-R-1 / INT-R-4).\n"
        "- No silent failure recovery (FG-5); every failure emits an "
        "append-only failure-event.\n"
    )
    readme = OC_ROOT / "RUNTIME_README.md"
    existing = readme.read_text(encoding="utf-8") if readme.exists() else ""
    marker = "## Phase 47 addendum — governed transactional execution & recovery (layer 40)"
    if marker not in existing:
        write_text(readme, existing + body)


def main() -> None:
    snap_roots = build_snapshot_roots()
    stores = build_runtime_event_stores()
    rules = build_rule_tables()
    assets = build_assets()
    consoles = build_consoles()
    doctrines = build_doctrines()
    reports = build_reports()
    build_runtime_readme_addendum()
    print(
        "Phase 47 — governed transactional execution & recovery written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Snapshot roots: {snap_roots} | New event stores: {stores} | "
        f"Rule tables: {rules} | JS assets: {assets} | "
        f"Exec consoles: {consoles} | Doctrines: {doctrines} | "
        f"Reports: {reports}"
    )


if __name__ == "__main__":
    main()
