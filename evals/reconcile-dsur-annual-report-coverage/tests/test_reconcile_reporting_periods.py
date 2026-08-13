"""Unit tests for the package-local reporting-period reconciler.

Author: Malek Okour
Date: 2026-08-11
Dependencies: Python 3.11+ standard library only
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVAL_ROOT = HERE.parent
SCRIPT = EVAL_ROOT.parents[1] / "skills" / EVAL_ROOT.name / "scripts" / "reconcile_reporting_periods.py"
FIXTURE = EVAL_ROOT / "fixtures" / "synthetic-reporting-periods.json"
CLEAN_FIXTURE = EVAL_ROOT / "fixtures" / "synthetic-clean-periods.json"

SPEC = importlib.util.spec_from_file_location("reconcile_reporting_periods", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ReportingPeriodTests(unittest.TestCase):
    def test_fixture_denominators_and_rules(self) -> None:
        report = MODULE.reconcile(json.loads(FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(report["counts"], {
            "reports_supplied": 7,
            "reports_assessable": 5,
            "reports_unassessable": 2,
            "same_kind_adjacency_comparisons": 3,
            "cross_format_comparisons": 6,
            "findings": 7,
            "policy_unknowns": 2,
        })
        rules = [item["rule"] for item in report["findings"]]
        self.assertEqual(rules.count("same-kind-gap"), 1)
        self.assertEqual(rules.count("same-kind-overlap"), 1)
        self.assertEqual(rules.count("same-kind-duplicate-period"), 1)
        self.assertEqual(rules.count("cross-format-potential-duplicate-coverage"), 4)

    def test_exact_gap_and_overlap_dates(self) -> None:
        report = MODULE.reconcile(json.loads(FIXTURE.read_text(encoding="utf-8")))
        by_rule = {item["rule"]: item for item in report["findings"] if item["rule"] in {"same-kind-gap", "same-kind-overlap"}}
        self.assertEqual((by_rule["same-kind-gap"]["affected_start"], by_rule["same-kind-gap"]["affected_end"]), ("2025-04-01", "2025-04-02"))
        self.assertEqual((by_rule["same-kind-overlap"]["affected_start"], by_rule["same-kind-overlap"]["affected_end"]), ("2026-03-30", "2026-03-31"))

    def test_unassessable_records_remain_visible(self) -> None:
        report = MODULE.reconcile(json.loads(FIXTURE.read_text(encoding="utf-8")))
        by_id = {item["report_id"]: item for item in report["unassessable"]}
        self.assertEqual(set(by_id), {"BROKEN-LOCATOR", "BAD-RANGE"})
        self.assertEqual({item["state"] for item in by_id.values()}, {"NEEDS_INPUT"})

    def test_clean_calendar_keeps_policy_unknowns(self) -> None:
        payload = json.loads(CLEAN_FIXTURE.read_text(encoding="utf-8"))
        report = MODULE.reconcile(payload)
        self.assertEqual(report["findings"], [])
        self.assertEqual({item["id"] for item in report["policy_unknowns"]}, {"UNKNOWN_FINAL_RULE_STATUS", "UNKNOWN_DSUR_IN_LIEU_PRACTICE"})
        self.assertIn("does not determine", report["boundary"])

    def test_duplicate_identifier_fails_visible(self) -> None:
        record = {"id": "DUP", "kind": "DSUR", "version": "v1", "status": "final", "period_start": "2024-01-01", "period_end": "2024-12-31", "locator": "p.1"}
        report = MODULE.reconcile({"documents": [record, dict(record)]})
        self.assertEqual(report["counts"]["reports_assessable"], 1)
        self.assertEqual(report["counts"]["reports_unassessable"], 1)
        self.assertIn("duplicate report id", report["unassessable"][0]["why"])

    def test_invalid_top_level_input_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty 'documents' list"):
            MODULE.reconcile({"documents": []})


if __name__ == "__main__":
    unittest.main()
