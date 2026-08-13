"""Deterministic tests for the K05 analysis-reproducibility artifact.

Purpose: prove the shared tool's bounded checks, explicit denominators,
fail-then-pass canaries, non-execution boundary, and vendored portability.
Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals/review-model-analysis-deliverable/fixtures"
PACKAGE_ROOT = EVAL / "synthetic-reproducibility-package"
CANONICAL = ROOT / "shared/scripts/analysis_reproducibility.py"
VENDORED = ROOT / "skills/review-model-analysis-deliverable/scripts/analysis_reproducibility.py"
sys.path.insert(0, str(ROOT / "shared/scripts"))

import analysis_reproducibility as reproducibility

VENDOR_BANNER = (
    "VENDORED at build time from shared/scripts/ — do not edit here.\n"
    "Edit the canonical source and rebuild; a freshness check compares them.\n\n"
)


def manifest(name: str) -> dict[str, object]:
    return json.loads((EVAL / name).read_text(encoding="utf-8"))


class AnalysisReproducibilityTests(unittest.TestCase):
    def test_clean_manifest_checks_six_artifacts_and_five_lineage_references(self) -> None:
        report = reproducibility.check(
            manifest("synthetic-reproducibility-clean.json"), PACKAGE_ROOT
        )
        self.assertEqual([], report.findings)
        self.assertEqual([], report.unassessable)
        self.assertEqual(6, report.counts["artifacts_declared"])
        self.assertEqual(6, report.counts["artifacts_present"])
        self.assertEqual(6, report.counts["hashes_checked"])
        self.assertEqual(6, report.counts["hashes_matched"])
        self.assertEqual(5, report.counts["lineage_references_checked"])

    def test_defect_manifest_reports_exact_structural_rules_and_unknown(self) -> None:
        report = reproducibility.check(
            manifest("synthetic-reproducibility-defects.json"), PACKAGE_ROOT
        )
        self.assertEqual(
            {
                "artifact-absent",
                "artifact-hash-mismatch",
                "lineage-reference-unresolved",
                "unsupported-completeness-claim",
            },
            {finding.rule for finding in report.findings},
        )
        self.assertEqual(1, len(report.unassessable))
        self.assertEqual("run seed", report.unassessable[0]["item"])

    def test_missing_file_completeness_canary_is_red_then_clean_fixture_is_green(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copied_root = Path(directory) / "package"
            shutil.copytree(PACKAGE_ROOT, copied_root)
            (copied_root / "logs/run.log").unlink()
            red = reproducibility.check(
                manifest("synthetic-reproducibility-clean.json"), copied_root
            )
            self.assertIn("artifact-absent", {finding.rule for finding in red.findings})
            self.assertIn(
                "unsupported-completeness-claim",
                {finding.rule for finding in red.findings},
            )

        green = reproducibility.check(
            manifest("synthetic-reproducibility-clean.json"), PACKAGE_ROOT
        )
        self.assertEqual([], green.findings)

    def test_checker_records_but_never_executes_declared_command(self) -> None:
        payload = manifest("synthetic-reproducibility-clean.json")
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist"
            payload["run"]["command"] = f"touch {marker}"
            report = reproducibility.check(payload, PACKAGE_ROOT)
            self.assertEqual([], report.findings)
            self.assertFalse(marker.exists())

    def test_unsafe_or_unconfirmed_inputs_fail_before_hashing(self) -> None:
        payload = manifest("synthetic-reproducibility-clean.json")
        payload["artifacts"][0]["path"] = "../outside"
        with self.assertRaisesRegex(reproducibility.ManifestError, "inside package root"):
            reproducibility.check(payload, PACKAGE_ROOT)

        payload = manifest("synthetic-reproducibility-clean.json")
        payload["preflight_state"] = "UNKNOWN"
        with self.assertRaisesRegex(reproducibility.ManifestError, "must be PASSED"):
            reproducibility.check(payload, PACKAGE_ROOT)

        with tempfile.TemporaryDirectory() as directory:
            copied_root = Path(directory) / "package"
            shutil.copytree(PACKAGE_ROOT, copied_root)
            link = copied_root / "code/linked-run.py"
            link.symlink_to(copied_root / "code/run.py")
            payload = manifest("synthetic-reproducibility-clean.json")
            payload["artifacts"][0]["path"] = "code/linked-run.py"
            report = reproducibility.check(payload, copied_root)
            self.assertIn(
                "artifact-symlink-not-checked",
                {finding.rule for finding in report.findings},
            )

    def test_lineage_reference_must_have_the_declared_structural_role(self) -> None:
        payload = manifest("synthetic-reproducibility-clean.json")
        payload["lineage"][0]["input_artifact_ids"] = ["SYN-CODE-017"]
        report = reproducibility.check(payload, PACKAGE_ROOT)
        self.assertIn("lineage-role-mismatch", {finding.rule for finding in report.findings})

    def test_render_preserves_the_scientific_and_regulated_system_boundary(self) -> None:
        report = reproducibility.check(
            manifest("synthetic-reproducibility-clean.json"), PACKAGE_ROOT
        )
        rendered = reproducibility.render(report)
        for boundary in (
            "does not establish scientific reproducibility",
            "fitness for purpose",
            "regulated-system certification",
            "Human review is required",
        ):
            self.assertIn(boundary, rendered)

    def test_vendored_copy_matches_canonical_after_standard_banner(self) -> None:
        vendored = VENDORED.read_text(encoding="utf-8")
        self.assertIn(VENDOR_BANNER, vendored)
        self.assertEqual(
            CANONICAL.read_text(encoding="utf-8"), vendored.replace(VENDOR_BANNER, "", 1)
        )

    def test_cli_returns_red_for_defects_and_green_for_clean_manifest(self) -> None:
        base = [sys.executable, str(CANONICAL), "--root", str(PACKAGE_ROOT)]
        red = subprocess.run(
            base + ["--manifest", str(EVAL / "synthetic-reproducibility-defects.json")],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, red.returncode)
        self.assertIn("unsupported-completeness-claim", red.stdout)

        green = subprocess.run(
            base + ["--manifest", str(EVAL / "synthetic-reproducibility-clean.json")],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, green.returncode)
        self.assertIn("artifacts_declared 6", green.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
