"""Real test suite for the first operational runtime."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Make `runtime` importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime import (  # noqa: E402
    assembly,
    config,
    flows,
    observability,
    provenance,
    retrieval,
    safety,
    supervision,
)


class ConfigTests(unittest.TestCase):
    def test_products_declared(self):
        self.assertIn("e-prime", config.PRODUCTS)
        self.assertEqual(len(config.PRODUCTS), 6)

    def test_assert_in_scope_blocks_outside_path(self):
        with self.assertRaises(PermissionError):
            config.assert_in_scope(Path("/etc/passwd"))


class ProvenanceTests(unittest.TestCase):
    def test_manifest_has_required_keys(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write('{"id":"x"}')
            tmp = Path(fh.name)
        try:
            m = provenance.build_manifest(
                run_id="r", slice_id="s", package_kind="retrieval-package",
                source_files=[tmp], source_node_ids=["x"],
            )
            self.assertEqual(m["package_kind"], "retrieval-package")
            self.assertEqual(m["source_node_ids"], ["x"])
            self.assertTrue(m["source_files"][0]["sha256"])
            self.assertTrue(m["manifest_id"].startswith("prov-"))
        finally:
            tmp.unlink(missing_ok=True)


class RetrievalTests(unittest.TestCase):
    def test_retrieve_onboarding_returns_results_for_known_query(self):
        pkg = retrieval.retrieve(
            run_id="r", slice_id="s", product="e-prime",
            query="vincular cerradura administrador", kind="onboarding",
        )
        self.assertFalse(pkg.no_results, "expected at least one onboarding hit on e-prime")
        self.assertTrue(all(0 < n.score <= 1 for n in pkg.nodes))
        self.assertEqual(pkg.manifest["package_kind"], "retrieval-package")

    def test_retrieve_unknown_kind_raises(self):
        with self.assertRaises(ValueError):
            retrieval.retrieve(run_id="r", slice_id="s", product="e-prime",
                               query="x", kind="not-a-kind")

    def test_retrieve_empty_query_returns_no_results(self):
        pkg = retrieval.retrieve(run_id="r", slice_id="s", product="e-prime",
                                 query="", kind="onboarding")
        self.assertTrue(pkg.no_results)


class AssemblyTests(unittest.TestCase):
    def _pkg(self, **kw):
        defaults = dict(package_id="p", run_id="r", slice_id="s", query="q",
                        kind="onboarding", product="e-prime", nodes=[],
                        manifest={"manifest_id": "prov-x"}, ambiguous=False, no_results=True)
        defaults.update(kw)
        return retrieval.RetrievalPackage(**defaults)

    def test_assembly_blocks_when_no_procedure(self):
        asm = assembly.assemble(
            run_id="r", slice_id="s",
            procedure_pkg=self._pkg(),
            warning_pkg=self._pkg(kind="warnings"),
            troubleshooting_pkg=self._pkg(kind="troubleshooting"),
        )
        self.assertIn("no-procedure-retrievable", asm.blockers)

    def test_safety_demotes_on_blockers(self):
        asm = assembly.assemble(
            run_id="r", slice_id="s",
            procedure_pkg=self._pkg(),
            warning_pkg=self._pkg(kind="warnings"),
            troubleshooting_pkg=self._pkg(kind="troubleshooting"),
        )
        report = safety.evaluate(asm)
        self.assertTrue(report["demote"])
        self.assertIn("no-unsafe-retrieval", report["failed"])


class SupervisionTests(unittest.TestCase):
    def test_supervise_with_auto_decision(self):
        r = supervision.supervise(
            run_id="r", slice_id="s", checkpoint="pre-emission",
            payload_summary={"x": 1}, operator="op", auto_decision="approve",
        )
        self.assertEqual(r.decision, "approve")
        self.assertTrue(r.receipt_id.startswith("sup-"))

    def test_invalid_checkpoint_raises(self):
        with self.assertRaises(ValueError):
            supervision.supervise(run_id="r", slice_id="s", checkpoint="not-a-checkpoint",
                                  payload_summary={}, operator="op", auto_decision="approve")


class FlowTests(unittest.TestCase):
    def test_onboarding_flow_with_auto_approve_emits_guidance_or_demotes(self):
        result = flows.run_flow(
            flow="onboarding", product="e-prime",
            query="vincular cerradura administrador", auto_decision="approve",
        )
        # Either emits a guidance-package or demotes for declared reasons.
        if result.demoted:
            self.assertTrue(result.demote_reasons)
            self.assertIsNone(result.guidance_package)
        else:
            self.assertIsNotNone(result.guidance_package)
            self.assertEqual(result.guidance_package["flow"], "onboarding")

    def test_reject_demotes(self):
        result = flows.run_flow(
            flow="onboarding", product="e-prime",
            query="vincular cerradura", auto_decision="reject",
        )
        self.assertTrue(result.demoted)
        self.assertIn("operator-reject", result.demote_reasons)


class ObservabilityTests(unittest.TestCase):
    def test_emit_appends_record(self):
        before = len(observability.read_all("orchestration-trace"))
        observability.emit("orchestration-trace", {"kind": "test-event"})
        after = len(observability.read_all("orchestration-trace"))
        self.assertEqual(after, before + 1)

    def test_unknown_channel_raises(self):
        with self.assertRaises(ValueError):
            observability.emit("not-a-channel", {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
