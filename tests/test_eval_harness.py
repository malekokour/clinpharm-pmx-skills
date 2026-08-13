"""Contract tests for the evaluation harness.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml; Python standard library

These are regression tests for a specific failure: the grader this harness
replaced returned identical results whatever the run contained, because its
outcomes were literals. So the tests here do not check that grading *works* —
they check that it **responds to its inputs**, which is the property that was
missing. Each mutation below produced a real defect during P02 or would have
gone unnoticed under the old grader.
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from eval_benchmark import analyse, describe
from eval_grade import grade_run
from eval_schema import (
    SchemaError,
    check_grading,
    check_timing,
    load_case,
    load_suite,
)
from eval_trigger import main as trigger_main
from eval_trigger import profile_requirements, report
from eval_workspace import stage

VALID_CASE = """
id: execution-demo
layer: execution
mode: FULL-QC
prompt: >
  QC the PK sections.
assertions:
  mechanical:
    - defect: D1
      severity: Critical
      detected_by: script
      observed: "412"
      expected: "481"
      locator_required: true
    - denominator_stated: true
    - must_not_contain: "recommended dose"
  judged:
    - "Both sides of every conflict are preserved"
"""

GOOD_RESPONSE = """# Findings

Checked 27 values across 2 sources.

- **Critical** numeric mismatch: Synopsis §2.3 states AUC 412 ng.h/mL; Table 14.2.1 says 481. Disposition: open.
"""


def write_run(root: Path, response: str = GOOD_RESPONSE, **overrides) -> Path:
    run = root / "run-1"
    (run / "outputs").mkdir(parents=True, exist_ok=True)
    (run / "outputs/response.md").write_text(response, encoding="utf-8")
    (run / "outputs/metrics.json").write_text(
        json.dumps(
            {
                "tool_calls": {"Read": 2},
                "total_tool_calls": 2,
                "total_steps": 2,
                "errors_encountered": 0,
                "output_chars": max(len(response), 1),
                "transcript_chars": 50,
            }
        ),
        encoding="utf-8",
    )
    timing = {
        "total_tokens": 5000,
        "duration_ms": 20000,
        "total_duration_seconds": 20.0,
        "executor_duration_seconds": 18.0,
        "grader_duration_seconds": 2.0,
    }
    timing.update(overrides)
    (run / "timing.json").write_text(json.dumps(timing), encoding="utf-8")
    return run


class SchemaTests(unittest.TestCase):
    def test_valid_case_is_accepted(self):
        case = load_case(VALID_CASE, "valid")
        self.assertEqual(case["id"], "execution-demo")
        self.assertEqual(len(case["assertions"]["mechanical"]), 3)

    def test_severity_is_not_coerced_or_lowercased(self):
        """strictyaml keeps `Critical` a string; a lowercase variant is rejected."""
        self.assertEqual(
            load_case(VALID_CASE, "v")["assertions"]["mechanical"][0]["severity"], "Critical"
        )
        with self.assertRaises(SchemaError):
            load_case(VALID_CASE.replace("severity: Critical", "severity: critical"), "bad")

    def test_malformed_cases_are_rejected(self):
        mutations = {
            "unknown layer": ("layer: execution", "layer: exectuion"),
            "typo'd key": ("      severity: Critical", "      sevrity: Critical"),
            "missing prompt": ("prompt: >", "xprompt: >"),
            "unknown assertion kind": (
                "    - denominator_stated: true",
                "    - denomintaor_stated: true",
            ),
            "non-boolean flag": ("locator_required: true", "locator_required: yes-please"),
        }
        for label, (old, new) in mutations.items():
            with self.subTest(label), self.assertRaises(SchemaError):
                load_case(VALID_CASE.replace(old, new), "bad")

    def test_duplicate_key_is_rejected(self):
        """A duplicate key would silently drop an assertion from the denominator."""
        with self.assertRaises(SchemaError):
            load_case(VALID_CASE.replace("  mechanical:", "  judged:\n    - dup\n  mechanical:"), "d")

    def test_defect_assertion_requires_both_sides_of_the_pair(self):
        """A defect is "document says X, source says Y" — one value is not it."""
        with self.assertRaises(SchemaError):
            load_case(VALID_CASE.replace('      expected: "481"\n', ""), "no-expected")
        with self.assertRaises(SchemaError):
            load_case(VALID_CASE.replace('      observed: "412"\n', ""), "no-observed")

    def test_suite_requires_thresholds(self):
        with self.assertRaises(SchemaError):
            load_suite('skill: "x"\nversion: "1"\n', "no-thresholds")

    def test_diagnostic_suite_may_explain_unmeasured_thresholds(self):
        suite = load_suite(
            'skill: "x"\nversion: "1"\nqualification_profile: "MEDIUM"\n'
            'qualification_policy: "PS-D024-v1"\nthresholds:\n'
            '  state: "diagnostic"\n  recall: "not measured"\n'
            '  precision: "not measured"\n  missed_critical_allowed: 0\n',
            "diagnostic",
        )
        self.assertEqual(suite["thresholds"]["state"], "diagnostic")

    def test_qualifying_thresholds_must_be_numeric_and_bounded(self):
        template = (
            'skill: "x"\nversion: "1"\nqualification_profile: "MEDIUM"\n'
            'qualification_policy: "PS-D024-v1"\nthresholds:\n'
            '  state: "qualifying"\n  recall: "{recall}"\n  precision: "0.90"\n'
            '  pass_rate: "0.90"\n  activation_accuracy: "0.90"\n'
            '  baseline_delta: "0.01"\n  missed_critical_allowed: 0\n'
        )
        self.assertEqual(
            load_suite(template.format(recall="0.95"), "valid")["thresholds"]["recall"],
            "0.95",
        )
        for bad in ("declared later", "1.01", "-0.01"):
            with self.subTest(value=bad), self.assertRaises(SchemaError):
                load_suite(template.format(recall=bad), "bad")


class GradingRespondsToInput(unittest.TestCase):
    """The property the previous grader lacked entirely."""

    def setUp(self):
        self.case = load_case(VALID_CASE, "case")

    def grade(self, response: str) -> tuple[int, int]:
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp), response)
            result = grade_run(run, self.case)
            return result["summary"]["passed"], result["summary"]["total"]

    def test_baseline_passes_mechanical_and_fails_unadjudicated_judged(self):
        self.assertEqual(self.grade(GOOD_RESPONSE), (3, 4))

    def test_altering_the_defect_value_lowers_the_grade(self):
        self.assertEqual(self.grade(GOOD_RESPONSE.replace("481", "999")), (2, 4))

    def test_a_negated_finding_does_not_count_as_detection(self):
        """The exact defect that invalidated the 2026-08-06 evaluation."""
        negated = GOOD_RESPONSE.replace(
            "**Critical** numeric mismatch: Synopsis §2.3 states AUC 412 ng.h/mL; Table 14.2.1 says 481.",
            "Synopsis §2.3 AUC 412 against Table 14.2.1 481 — the CLI reported no finding, values are consistent.",
        )
        self.assertEqual(self.grade(negated), (2, 4))

    def test_wrong_severity_does_not_count_as_detection(self):
        wrong = GOOD_RESPONSE.replace("**Critical**", "**Minor**")
        self.assertEqual(self.grade(wrong), (2, 4))

    def test_one_side_of_the_pair_is_not_detection(self):
        half = GOOD_RESPONSE.replace("; Table 14.2.1 says 481", " (Table 14.2.1)")
        self.assertEqual(self.grade(half), (2, 4))

    def test_a_bare_decimal_is_not_a_locator(self):
        """`15.2` is a measurement; it may not satisfy the locator requirement."""
        no_locator = GOOD_RESPONSE.replace("Synopsis §2.3 states ", "").replace("; Table 14.2.1 says 481", " versus 481")
        self.assertEqual(self.grade(no_locator), (2, 4))

    def test_removing_the_locator_lowers_the_grade(self):
        self.assertEqual(
            self.grade(GOOD_RESPONSE.replace("Synopsis §2.3 states ", "").replace("Table 14.2.1 says ", "")),
            (2, 4),
        )

    def test_removing_the_denominator_lowers_the_grade(self):
        self.assertEqual(
            self.grade(GOOD_RESPONSE.replace("Checked 27 values across 2 sources.", "")), (2, 4)
        )

    def test_a_forbidden_dose_recommendation_lowers_the_grade(self):
        self.assertEqual(
            self.grade(GOOD_RESPONSE + "\nThe recommended dose is 50 mg.\n"), (2, 4)
        )


class FailsClosed(unittest.TestCase):
    def setUp(self):
        self.case = load_case(VALID_CASE, "case")

    def test_empty_response_is_refused_not_scored(self):
        """It scored 1/4 before the guard: `must_not_contain` passes over no text."""
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp), "   \n")
            with self.assertRaises(SystemExit):
                grade_run(run, self.case)

    def test_stage_rejects_an_unknown_case_instead_of_passing_zero(self):
        suite = ROOT / "evals" / "map-agency-question-evidence"
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            with self.assertRaisesRegex(SystemExit, "requested case.*does not exist"):
                stage(suite, workspace, runs=1, only="not-a-real-case")
            self.assertFalse(workspace.exists())

    def test_incomplete_run_is_refused_not_scored_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp))
            (run / "timing.json").unlink()
            with self.assertRaises(SystemExit):
                grade_run(run, self.case)

    def test_null_token_count_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp), total_tokens=None)
            with self.assertRaises(SystemExit):
                grade_run(run, self.case)

    def test_unadjudicated_judged_assertion_fails_and_stays_in_denominator(self):
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp))
            result = grade_run(run, self.case)
            judged = result["expectations"][-1]
            self.assertFalse(judged["passed"])
            self.assertIn("NO ADJUDICATION RECORDED", judged["evidence"])
            self.assertEqual(result["summary"]["total"], 4)

    def test_adjudication_without_a_quote_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp))
            (run / "judged-review.json").write_text(
                json.dumps(
                    {
                        "adjudications": [
                            {
                                "assertion": "Both sides of every conflict are preserved",
                                "verdict": "pass",
                                "reviewer": "M. Okour",
                                "quote": "",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = grade_run(run, self.case)
            self.assertFalse(result["expectations"][-1]["passed"])
            self.assertIn("INCOMPLETE ADJUDICATION", result["expectations"][-1]["evidence"])

    def test_complete_adjudication_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            run = write_run(Path(temp))
            (run / "judged-review.json").write_text(
                json.dumps(
                    {
                        "adjudications": [
                            {
                                "assertion": "Both sides of every conflict are preserved",
                                "verdict": "pass",
                                "reviewer": "M. Okour",
                                "quote": "AUC 412 vs 481 ng.h/mL",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(grade_run(run, self.case)["summary"]["passed"], 4)


class VacuityGuards(unittest.TestCase):
    def test_grading_with_no_expectations_is_invalid(self):
        problems = check_grading(
            {"expectations": [], "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0}}
        )
        self.assertTrue(problems)

    def test_blank_evidence_is_invalid(self):
        problems = check_grading(
            {
                "expectations": [{"text": "x", "passed": True, "evidence": "   "}],
                "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
            }
        )
        self.assertTrue(any("empty evidence" in p for p in problems))

    def test_summary_that_disagrees_with_its_expectations_is_invalid(self):
        problems = check_grading(
            {
                "expectations": [{"text": "x", "passed": False, "evidence": "not found"}],
                "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
            }
        )
        self.assertTrue(any("marked passed" in p for p in problems))

    def test_null_timing_is_reported(self):
        self.assertTrue(check_timing({"total_tokens": None, "duration_ms": 1}))


class AnalystPass(unittest.TestCase):
    def test_population_stddev_not_sample(self):
        # values 1,2,3: population sd = sqrt(2/3) = 0.8165; sample sd would be 1.0
        self.assertEqual(describe([1.0, 2.0, 3.0])["stddev"], 0.8165)

    def test_detects_a_non_discriminating_assertion(self):
        runs = [
            {
                "eval_name": "e",
                "configuration": configuration,
                "run_number": n,
                "result": {"pass_rate": 1.0, "tokens": 10, "time_seconds": 1.0},
                "expectations": [{"text": "always true", "passed": True, "evidence": "e"}],
            }
            for configuration in ("with_skill", "without_skill")
            for n in (1, 2, 3)
        ]
        notes = analyse(runs)
        self.assertTrue(any("do not discriminate" in note for note in notes))

    def test_empty_run_set_does_not_report_success(self):
        self.assertIn("nothing was measured", " ".join(analyse([])))


class RiskTierDefaults(unittest.TestCase):
    def test_trigger_query_and_run_defaults_scale_by_profile(self):
        self.assertEqual(profile_requirements("LOW"), (3, 1))
        self.assertEqual(profile_requirements("MEDIUM"), (10, 2))
        self.assertEqual(profile_requirements("HIGH"), (20, 2))
        self.assertEqual(profile_requirements("HIGH", "optimization"), (20, 3))

    def test_low_qualification_does_not_require_description_holdout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            queries = [
                {"query": "build reusable work context", "kind": "positive"},
                {"query": "update my reusable role context", "kind": "positive"},
                {
                    "query": "review this DDI package",
                    "kind": "near_miss",
                    "neighbour": "review-ddi-evidence",
                },
            ]
            decisions = {item["query"]: [item["kind"] == "positive"] for item in queries}
            query_path = root / "queries.json"
            decision_path = root / "decisions.json"
            query_path.write_text(json.dumps(queries), encoding="utf-8")
            decision_path.write_text(json.dumps(decisions), encoding="utf-8")
            argv = [
                "eval_trigger.py",
                str(query_path),
                "--decisions",
                str(decision_path),
                "--profile",
                "LOW",
            ]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(trigger_main(), 0)

            with patch.object(
                sys, "argv", [*argv, "--mode", "optimization"]
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(trigger_main(), 1)

    def test_trigger_gate_applies_threshold_to_each_query_class(self):
        result = {
            "positives": 10,
            "near_misses": 10,
            "unrecorded": [],
            "recall": 0.8,
            "near_miss_rejection": 1.0,
            "accuracy": 0.9,
            "under_triggering": ["positive-a", "positive-b"],
            "over_triggering": [],
            "flaky": [],
        }
        with redirect_stdout(io.StringIO()):
            self.assertFalse(report("qualification", result, 0.9))

    def test_trigger_gate_allows_bounded_errors_above_declared_threshold(self):
        result = {
            "positives": 10,
            "near_misses": 20,
            "unrecorded": [],
            "recall": 0.9,
            "near_miss_rejection": 0.95,
            "accuracy": 0.9333,
            "under_triggering": ["positive-a"],
            "over_triggering": [{"query": "near-a", "neighbour": "skill-b"}],
            "flaky": [],
        }
        with redirect_stdout(io.StringIO()):
            self.assertTrue(report("qualification", result, 0.9))

    def test_trigger_gate_rejects_flaky_decisions(self):
        result = {
            "positives": 10,
            "near_misses": 10,
            "unrecorded": [],
            "recall": 1.0,
            "near_miss_rejection": 1.0,
            "accuracy": 1.0,
            "under_triggering": [],
            "over_triggering": [],
            "flaky": ["positive-a"],
        }
        with redirect_stdout(io.StringIO()):
            self.assertFalse(report("qualification", result, 0.9))


if __name__ == "__main__":
    unittest.main(verbosity=2)
