"""Regression and fail-closed canaries for K07 Wave-A remediations.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class DevelopmentPlanDashTests(unittest.TestCase):
    def test_fixture_en_dash_is_present_not_a_false_gap(self) -> None:
        command = [
            sys.executable,
            str(ROOT / "skills/assess-development-plan-gaps/scripts/assess_coverage.py"),
            "--plan",
            str(ROOT / "evals/assess-development-plan-gaps/fixtures/synthetic-cp-development-plan.md"),
            "--json",
        ]
        completed = subprocess.run(command, text=True, capture_output=True, check=True)
        result = json.loads(completed.stdout)
        missing = {row["item"] for row in result["findings"]}
        self.assertNotIn("drug-drug interaction", missing)
        self.assertEqual(result["counts"]["study types present"], 8)

    def test_match_is_narrow_not_arbitrary_punctuation(self) -> None:
        tool = load_module(
            "k07_assess_coverage",
            ROOT / "skills/assess-development-plan-gaps/scripts/assess_coverage.py",
        )
        pattern = dict(tool.REQUIRED)["drug-drug interaction"]
        self.assertRegex("Drug–drug interaction".lower(), pattern)
        self.assertRegex("drug-drug interaction", pattern)
        self.assertNotRegex("drug/drug interaction", pattern)
        self.assertNotRegex("drug interaction", pattern)


class ExplicitValueComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ctd = load_module(
            "k07_ctd_source_compare",
            ROOT / "skills/review-ctd-272-content/scripts/source_value_compare.py",
        )
        cls.uspi = load_module(
            "k07_uspi_source_compare",
            ROOT / "skills/review-uspi-section-12-content/scripts/source_value_compare.py",
        )

    def test_ctd_cross_module_route_is_non_vacuous(self) -> None:
        base = ROOT / "evals/review-ctd-272-content"
        spec = json.loads((base / "fixtures/synthetic-cross-module-comparison-spec.json").read_text(encoding="utf-8"))
        result = self.ctd.compare(spec, {
            "module272": (base / "fixtures/synthetic-module-272-draft.md").read_text(encoding="utf-8"),
            "modules273274": (base / "fixtures/synthetic-module-273-274-extracts.md").read_text(encoding="utf-8"),
        })
        self.assertEqual(result["summary"], {"pairs_declared": 1, "comparisons": 1, "discrepancies": 1})
        self.assertEqual(result["findings"][0]["id"], "D1")

    def test_zero_pair_and_ambiguous_match_canaries_fail_closed(self) -> None:
        with self.assertRaises(self.ctd.ComparisonInputError):
            self.ctd.compare({"pairs": []}, {"left": "dose 1 mg", "right": "dose 2 mg"})
        spec = {"pairs": [{
            "id": "canary", "left": {"document": "left", "pattern": r"(?P<value>\d+) mg"},
            "right": {"document": "right", "pattern": r"(?P<value>\d+) mg"},
        }]}
        with self.assertRaises(self.ctd.ComparisonInputError):
            self.ctd.compare(spec, {"left": "1 mg and 2 mg", "right": "3 mg"})

    def test_uspi_script_executes_three_promised_pairs(self) -> None:
        base = ROOT / "evals/review-uspi-section-12-content"
        spec = json.loads((base / "fixtures/synthetic-label-source-comparison-spec.json").read_text(encoding="utf-8"))
        result = self.uspi.compare(spec, {
            "label": (base / "fixtures/synthetic-uspi-draft.md").read_text(encoding="utf-8"),
            "sources": (base / "fixtures/synthetic-source-values.md").read_text(encoding="utf-8"),
            "module272": (base / "fixtures/synthetic-module-272-extract.md").read_text(encoding="utf-8"),
        })
        self.assertEqual(result["summary"], {"pairs_declared": 3, "comparisons": 3, "discrepancies": 3})
        self.assertEqual({row["id"] for row in result["findings"]}, {"D2", "D5", "D6"})


class FIHConversionBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_module(
            "k07_fih_conversion",
            ROOT / "skills/review-fih-dose-rationale/scripts/fih_conversion_calculator.py",
        )

    def test_sponsor_divisor_reproduces_fixture_step(self) -> None:
        result = self.tool.calculate(60, 10, 60, sponsor_conversion_factor=6.2)
        self.assertAlmostEqual(result["hed_mg_kg"], 60 / 6.2, places=12)
        self.assertEqual(result["hed_mg_kg_rounded_2dp"], 9.68)
        self.assertEqual(result["basis"], "sponsor-supplied divisor")

    def test_species_mode_remains_available_and_explicit(self) -> None:
        result = self.tool.calculate(60, 10, 60, species="rat")
        self.assertAlmostEqual(result["hed_mg_kg"], 60 * 6 / 37, places=12)
        self.assertIn("species=rat", result["basis"])

    def test_missing_dual_and_invalid_basis_canaries_fail(self) -> None:
        with self.assertRaises(ValueError):
            self.tool.calculate(60, 10, 60)
        with self.assertRaises(ValueError):
            self.tool.calculate(60, 10, 60, sponsor_conversion_factor=6.2, species="rat")
        with self.assertRaises(ValueError):
            self.tool.calculate(60, 10, 60, sponsor_conversion_factor=0)


class HighCaseFloorTests(unittest.TestCase):
    def test_assigned_case_floors(self) -> None:
        expected = {
            "assess-development-plan-gaps": 12,
            "review-ctd-272-content": 10,
            "review-uspi-section-12-content": 10,
            "review-fih-dose-rationale": 10,
        }
        for skill, count in expected.items():
            with self.subTest(skill=skill):
                self.assertEqual(len(list((ROOT / "evals" / skill / "cases").glob("*.yaml"))), count)


if __name__ == "__main__":
    unittest.main()
