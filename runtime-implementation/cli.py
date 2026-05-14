"""Supervised CLI for the first operational runtime track.

Subcommands:
  retrieve  — execute a single retrieval over knowledge-core
  flow      — execute a supervised flow (halts at pre-emission for operator approval)
  test      — run the embedded test suite
  channels  — print observability channel summaries
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python runtime-implementation/cli.py ...` without installation.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from runtime import config, flows, observability, provenance, replay, retrieval  # noqa: E402


def cmd_retrieve(args: argparse.Namespace) -> int:
    pkg = retrieval.retrieve(
        run_id=provenance.new_id("run"),
        slice_id=provenance.new_id("slice"),
        product=args.product,
        query=args.query,
        kind=args.kind,
        top_k=args.top_k,
    )
    print(json.dumps(retrieval.package_to_dict(pkg), indent=2, ensure_ascii=False))
    return 0 if pkg.nodes else 2


def cmd_flow(args: argparse.Namespace) -> int:
    auto = None
    if args.approve:
        auto = "approve"
    elif args.reject:
        auto = "reject"
    elif args.demote:
        auto = "demote"
    result = flows.run_flow(
        flow=args.flow, product=args.product, query=args.query,
        operator=args.operator, auto_decision=auto,
    )
    out = {
        "run_id": result.run_id,
        "slice_id": result.slice_id,
        "flow": result.flow,
        "product": result.product,
        "query": result.query,
        "demoted": result.demoted,
        "demote_reasons": result.demote_reasons,
        "pre_emission_receipt": result.pre_emission_receipt,
        "safety_report": result.safety_report,
        "assembly_package": result.assembly_package,
        "guidance_package": result.guidance_package,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if result.demoted else 0


def cmd_test(_: argparse.Namespace) -> int:
    import subprocess
    test_dir = Path(__file__).resolve().parent / "testing"
    return subprocess.call([sys.executable, "-m", "unittest", "discover",
                            "-s", str(test_dir), "-p", "test_*.py", "-v"])


def cmd_replay(args: argparse.Namespace) -> int:
    if args.run_id:
        rp = replay.replay_run(args.run_id)
        if rp is None:
            print(json.dumps({"error": "run-id not found", "run_id": args.run_id}))
            return 2
        out = {
            "run_id": rp.run_id, "flow": rp.flow, "product": rp.product,
            "query": rp.query, "deterministic": rp.deterministic,
            "captured": rp.captured_retrievals,
            "replayed": rp.replayed_retrievals,
            "drift": rp.drift,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0 if rp.deterministic else 1
    runs = replay.replay_all()
    out = {
        "summary": replay.summary(runs),
        "runs": [
            {"run_id": r.run_id, "flow": r.flow, "product": r.product,
             "deterministic": r.deterministic, "drift_count": len(r.drift)}
            for r in runs
        ],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if all(r.deterministic for r in runs) else 1


def cmd_channels(_: argparse.Namespace) -> int:
    summary: dict = {}
    for ch in observability.CHANNELS:
        records = observability.read_all(ch)
        summary[ch] = {"count": len(records), "last_event": records[-1] if records else None}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="beslock-runtime", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("retrieve", help="execute a single retrieval over knowledge-core")
    r.add_argument("--product", required=True, choices=config.PRODUCTS)
    r.add_argument("--query", required=True)
    r.add_argument("--kind", required=True, choices=sorted(retrieval.KIND_DOMAINS.keys()))
    r.add_argument("--top-k", type=int, default=5)
    r.set_defaults(func=cmd_retrieve)

    f = sub.add_parser("flow", help="execute a supervised flow")
    f.add_argument("flow", choices=sorted(flows.FLOW_KINDS.keys()))
    f.add_argument("--product", required=True, choices=config.PRODUCTS)
    f.add_argument("--query", required=True)
    f.add_argument("--operator", default="operator-cli")
    g = f.add_mutually_exclusive_group()
    g.add_argument("--approve", action="store_true", help="auto-approve at pre-emission (non-interactive)")
    g.add_argument("--reject", action="store_true", help="auto-reject at pre-emission (non-interactive)")
    g.add_argument("--demote", action="store_true", help="auto-demote at pre-emission (non-interactive)")
    f.set_defaults(func=cmd_flow)

    t = sub.add_parser("test", help="run the embedded unittest suite")
    t.set_defaults(func=cmd_test)

    c = sub.add_parser("channels", help="print observability channel summaries")
    c.set_defaults(func=cmd_channels)

    rp = sub.add_parser("replay", help="deterministically replay captured flow runs")
    rp.add_argument("--run-id", help="replay only this run id (default: all)")
    rp.set_defaults(func=cmd_replay)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
