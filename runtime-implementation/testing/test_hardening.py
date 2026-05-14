"""Tests for confidence-weighted retrieval, replay determinism, and the
candidate-only escalation trigger introduced by Phase 27."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime import config, flows, replay, retrieval  # noqa: E402


class ConfigHardeningTests(unittest.TestCase):
    def test_new_domains_allowed(self):
        for d in ("troubleshooting-expanded", "warnings-expanded",
                  "continuity-checkpoints", "causal-graphs", "confidence-tiers"):
            self.assertIn(d, config.ALLOWED_DOMAINS)

    def test_candidate_weight_is_low(self):
        self.assertLess(config.CONFIDENCE_WEIGHTS["candidate"],
                        config.CONFIDENCE_WEIGHTS["verified-oem"])


class CandidateWeightingTests(unittest.TestCase):
    def test_candidate_only_marker_appears_in_manifest(self):
        # A query targeted at the supplemental troubleshooting corpus
        # (which is candidate-only by construction).
        pkg = retrieval.retrieve(
            run_id="r", slice_id="s", product="e-prime",
            query="emparejamiento huella sensor reintento", kind="troubleshooting",
        )
        # If we got results, the manifest must declare candidate_only honestly.
        if not pkg.no_results:
            self.assertIn("candidate_only", pkg.manifest["extra"])
            # Scores must remain bounded under weighting.
            self.assertTrue(all(0 < n.score <= 1 for n in pkg.nodes))


class ReplayDeterminismTests(unittest.TestCase):
    def test_replay_run_is_deterministic(self):
        # Generate at least one captured run.
        result = flows.run_flow(
            flow="onboarding", product="e-prime",
            query="vincular cerradura administrador", auto_decision="approve",
        )
        rp = replay.replay_run(result.run_id)
        self.assertIsNotNone(rp, "expected the just-emitted run to be replayable")
        self.assertTrue(rp.deterministic, f"replay drift: {rp.drift}")

    def test_replay_summary_shape(self):
        flows.run_flow(flow="onboarding", product="e-prime",
                       query="vincular", auto_decision="approve")
        runs = replay.replay_all()
        s = replay.summary(runs)
        self.assertEqual(s["schema"], "runtime-replay/1.0")
        self.assertGreaterEqual(s["runs"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
