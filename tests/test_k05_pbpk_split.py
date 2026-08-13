"""Deterministic tests for the K05 PBPK/FIH split gate.

Purpose: prove that PBPK reporting trace stays in the MEDIUM package while
FIH stated-dose-chain arithmetic routes to the existing HIGH package.
Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library plus repository-pinned StrictYAML
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "skills/review-model-analysis-deliverable"
FIH = ROOT / "skills/review-fih-dose-rationale"
MODEL_EVAL = ROOT / "evals/review-model-analysis-deliverable"
FIH_EVAL = ROOT / "evals/review-fih-dose-rationale"


def frontmatter(path: Path) -> dict[str, object]:
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    if match is None:
        raise AssertionError(f"missing frontmatter: {path}")
    return load(match.group(1)).data


def split_errors(model_text: str, fih_text: str) -> list[str]:
    errors: list[str] = []
    normalized_model = " ".join(model_text.split())
    required_model = (
        "PBPK-HUMAN-PK-PREDICTION-REVIEW",
        "context of use stated verbatim",
        "source/model identity",
        "parameter provenance",
        "run identity",
        "observed dataset identity",
        "pre-stated acceptance criterion",
        "route the whole arithmetic request to `review-fih-dose-rationale`",
    )
    for marker in required_model:
        if marker not in normalized_model:
            errors.append(f"model package missing {marker}")

    if "### Inbound PBPK/FIH split" not in fih_text or "`CHAIN-RECOMPUTE`" not in fih_text:
        errors.append("FIH package does not accept the inbound written-chain route")

    try:
        allowed = model_text.split("For an in-scope PBPK report", 1)[1].split(
            "Report presence, absence", 1
        )[0]
    except IndexError:
        errors.append("PBPK allowed-check block is not bounded")
        return errors
    prohibited = (
        "NOAEL",
        "HED",
        "MRSD",
        "starting-dose calculation",
        "safety-factor arithmetic",
        "escalation arithmetic",
    )
    for phrase in prohibited:
        if phrase.casefold() in allowed.casefold():
            errors.append(f"MEDIUM PBPK checks contain dose-chain operation: {phrase}")
    return errors


class PbpkSplitTests(unittest.TestCase):
    def test_split_gate_known_bad_then_live_green(self) -> None:
        model_text = (MODEL / "SKILL.md").read_text(encoding="utf-8")
        fih_text = (FIH / "SKILL.md").read_text(encoding="utf-8")
        planted = model_text.replace(
            "1. context of use stated verbatim",
            "1. Recompute the FIH NOAEL to HED to MRSD chain.\n2. context of use stated verbatim",
            1,
        )
        self.assertGreater(len(split_errors(planted, fih_text)), 0)
        self.assertEqual([], split_errors(model_text, fih_text))

    def test_exact_marker_and_human_only_boundaries_are_present(self) -> None:
        text = (MODEL / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        self.assertIn("PBPK-HUMAN-PK-PREDICTION-REVIEW", normalized)
        for boundary in (
            "Species relevance",
            "model choice",
            "parameter plausibility",
            "predictive adequacy",
            "extrapolation acceptability",
            "dose selection remain human-only",
        ):
            self.assertIn(boundary, normalized)

    def test_frontmatter_is_strict_yaml_and_versions_are_0_2_0(self) -> None:
        for package in (MODEL, FIH):
            data = frontmatter(package / "SKILL.md")
            self.assertEqual("0.2.0", data["metadata"]["version"])
            self.assertEqual(
                "cursor-release150-paired-runs-ps-d024", data["metadata"]["evidence-level"]
            )
            self.assertEqual("required", data["metadata"]["human-review"])

    def test_new_case_denominator_and_declared_inputs_are_exact(self) -> None:
        expected = {
            MODEL_EVAL / "cases/11-execution-reproducibility-package.yaml": 7,
            MODEL_EVAL / "cases/12-execution-pbpk-reporting-trace.yaml": 1,
            FIH_EVAL / "cases/11-activation-pbpk-fih-dose-chain-route.yaml": 0,
        }
        inputs_checked = 0
        for path, expected_inputs in expected.items():
            self.assertTrue(path.is_file())
            data = load(path.read_text(encoding="utf-8")).data
            inputs = data.get("inputs", [])
            self.assertEqual(expected_inputs, len(inputs))
            eval_root = MODEL_EVAL if path.is_relative_to(MODEL_EVAL) else FIH_EVAL
            for relative in inputs:
                self.assertTrue((eval_root / relative).is_file(), relative)
                inputs_checked += 1
        self.assertEqual(8, inputs_checked)

    def test_suite_case_counts_preserve_medium_and_high_profiles(self) -> None:
        self.assertEqual(10, len(list((MODEL_EVAL / "cases").glob("*.yaml"))))
        self.assertEqual(10, len(list((FIH_EVAL / "cases").glob("*.yaml"))))
        self.assertIn(
            'qualification_profile: "MEDIUM"',
            (MODEL_EVAL / "suite.yaml").read_text(encoding="utf-8"),
        )
        self.assertIn(
            'qualification_profile: "HIGH"',
            (FIH_EVAL / "suite.yaml").read_text(encoding="utf-8"),
        )

    def test_pbpk_fixture_contains_both_sides_of_each_mechanical_pair(self) -> None:
        text = (
            MODEL_EVAL / "fixtures/synthetic-pbpk-reporting-source.md"
        ).read_text(encoding="utf-8")
        for value in (
            "SYN-PBPK-MODEL-007 v2.0",
            "SYN-PBPK-MODEL-007 v2.1",
            "SYN-PBPK-RUN-2026-08-11-B",
            "SYN-PBPK-RUN-2026-08-11-A",
        ):
            self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
