"""Operator supervision — review checkpoints, override channel, supervision receipts."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable

from . import provenance

REVIEW_CHECKPOINTS = (
    "pre-emission",
    "post-emission",
    "pre-handoff",
    "pre-completion",
    "post-anomaly",
)

VALID_DECISIONS = ("approve", "reject", "request-more-info", "escalate", "demote")


@dataclass
class SupervisionReceipt:
    receipt_id: str
    run_id: str
    slice_id: str
    checkpoint: str
    decision: str
    operator: str
    timestamp: str
    payload_summary: dict
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def _interactive_prompt(checkpoint: str, summary: dict) -> tuple[str, str]:
    sys.stdout.write(
        f"\n[supervision] checkpoint={checkpoint}\n"
        f"[supervision] summary={summary}\n"
        f"[supervision] decision ({'/'.join(VALID_DECISIONS)}) [approve]: "
    )
    sys.stdout.flush()
    line = sys.stdin.readline().strip().lower() or "approve"
    if line not in VALID_DECISIONS:
        line = "reject"
    sys.stdout.write("[supervision] notes (optional, single line): ")
    sys.stdout.flush()
    notes = sys.stdin.readline().rstrip("\n")
    return line, notes


def supervise(
    *,
    run_id: str,
    slice_id: str,
    checkpoint: str,
    payload_summary: dict,
    operator: str,
    auto_decision: str | None = None,
    prompt: Callable[[str, dict], tuple[str, str]] | None = None,
) -> SupervisionReceipt:
    if checkpoint not in REVIEW_CHECKPOINTS:
        raise ValueError(f"unknown checkpoint: {checkpoint}")
    if auto_decision is not None:
        if auto_decision not in VALID_DECISIONS:
            raise ValueError(f"invalid auto_decision: {auto_decision}")
        decision, notes = auto_decision, "auto"
    else:
        decision, notes = (prompt or _interactive_prompt)(checkpoint, payload_summary)
    return SupervisionReceipt(
        receipt_id=provenance.new_id("sup"),
        run_id=run_id,
        slice_id=slice_id,
        checkpoint=checkpoint,
        decision=decision,
        operator=operator,
        timestamp=provenance.now_iso(),
        payload_summary=payload_summary,
        notes=notes,
    )


def is_blocking(decision: str) -> bool:
    return decision in {"reject", "demote"}


def is_advancing(decision: str) -> bool:
    return decision == "approve"
