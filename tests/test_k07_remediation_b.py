"""Regression tests for K07 Wave-B deterministic remediation.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "skills/review-study-conduct-pk/scripts/reconcile.py"
STUDY_FIXTURES = ROOT / "evals/review-study-conduct-pk/fixtures"
DOSE_SCRIPT = ROOT / "skills/prepare-dose-justification-evidence/scripts/factor_coverage.py"
DOSE_FIXTURE = ROOT / "evals/prepare-dose-justification-evidence/fixtures/synthetic-factor-coverage-sources.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class StudyReconciliationTests(unittest.TestCase):
    def command(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(STUDY),
                "--left",
                str(STUDY_FIXTURES / "synthetic-cohort3-package.md"),
                "--right",
                str(STUDY_FIXTURES / "synthetic-interim-listings.md"),
                *extra,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_zero_comparable_pair_canary_fails_closed(self) -> None:
        result = self.command()
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAILED: reconciliation is vacuous: 0 comparable pairs", result.stdout)
        self.assertNotIn("no discrepancies beyond tolerance", result.stdout)

    def test_explicit_fixture_rows_make_one_meaningful_pair(self) -> None:
        result = self.command(
            "--left-row-regex",
            r"^\| Mean Cmax",
            "--right-row-regex",
            r"^\| \*\*Mean\*\*",
            "--left-locator",
            "Slide 4 Mean Cmax",
            "--right-locator",
            "Listing 16.2.2 Mean",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 comparisons; 1 discrepancies", result.stdout)
        self.assertIn("318 ng/mL", result.stdout)
        self.assertIn("381 ng/mL", result.stdout)

    def test_row_selectors_are_a_pair(self) -> None:
        result = self.command("--left-row-regex", r"^\| Mean Cmax")
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be supplied together", result.stderr)


class DoseCoverageVacuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.target = load_module("k07_factor_coverage", DOSE_SCRIPT)

    def run_pack(self, path: Path):
        return self.target.run(argparse.Namespace(pack=str(path), json=False))

    def test_synthetic_factor_fixture_has_nonzero_denominator(self) -> None:
        report = self.run_pack(DOSE_FIXTURE)
        self.assertEqual(report.counts["required factors"], 8)
        self.assertGreater(report.counts["factors present"], 0)
        self.assertEqual(report.unassessable, [])
        self.assertEqual(self.target.exit_code(report), 0)

    def test_zero_matched_factor_canary_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-document.md"
            path.write_text("Unrelated synthetic narrative with no coverage terms.\n", encoding="utf-8")
            report = self.run_pack(path)
        self.assertEqual(report.counts, {"required factors": 8, "factors present": 0})
        self.assertEqual(len(report.unassessable), 1)
        self.assertEqual(self.target.exit_code(report), 2)


if __name__ == "__main__":
    unittest.main()
