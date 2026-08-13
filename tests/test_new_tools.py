"""Contract tests for the four tools added by P03.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library

Each tool is checked for the same two properties, because they are the ones a
script in this product can plausibly get wrong in a way review would miss:

**It finds the planted defect.** A clean input yields no findings; a defective
input yields the specific finding, with both values preserved.

**It refuses rather than guesses.** Where the answer needs a scientific
judgement — which points define a terminal phase, whether an assay is fit for
purpose — the tool records "not assessable" with what would make it assessable,
instead of returning a number.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared" / "scripts"))

import bioanalytical_consistency as ba
import context_validation as ctx
import deliverable_consistency as deliv
import nca_recompute as nca

PROFILE = "0 0\n1 100\n2 50\n4 25\n"


def rules(report) -> set[str]:
    return {finding.rule for finding in report.findings}


class NCARecompute(unittest.TestCase):
    def setUp(self):
        self.points, self.rejected = nca.parse_profile(PROFILE)

    def test_trapezoid_is_arithmetic_not_approximation(self):
        # (1-0)*(0+100)/2 + (2-1)*(100+50)/2 + (4-2)*(50+25)/2 = 50 + 75 + 75 = 200
        self.assertEqual(nca.auc_linear(self.points), Decimal(200))

    def test_correct_report_yields_no_findings(self):
        report = nca.check(self.points, {"auc_linear": Decimal(200)}, self.rejected)
        self.assertEqual(report.findings, [])

    def test_wrong_auc_is_critical_and_keeps_both_values(self):
        report = nca.check(self.points, {"auc_linear": Decimal(412)}, self.rejected)
        self.assertIn("recomputation-mismatch", rules(report))
        finding = report.findings[0]
        self.assertEqual(finding.severity, "Critical")
        self.assertIn("412", finding.observed)
        self.assertIn("200", finding.expected)

    def test_tmax_absent_from_the_profile_is_flagged(self):
        report = nca.check(self.points, {"tmax": Decimal(3)}, self.rejected)
        self.assertIn("value-not-in-profile", rules(report))

    def test_half_life_is_refused_without_lambda_z(self):
        """Choosing terminal points is a scientific judgement, not a computation."""
        report = nca.check(self.points, {}, self.rejected)
        self.assertTrue(any(u["item"] == "half_life" for u in report.unassessable))
        self.assertNotIn("half_life", [f.item for f in report.findings])

    def test_half_life_is_checked_when_lambda_z_is_supplied(self):
        report = nca.check(self.points, {}, self.rejected, lambda_z=Decimal("0.693"))
        self.assertFalse(any(u["item"] == "half_life" for u in report.unassessable))

    def test_unparsed_rows_are_reported_not_dropped(self):
        points, rejected = nca.parse_profile("0 0\nrubbish\n1 100\n")
        report = nca.check(points, {}, rejected)
        self.assertEqual(report.counts["unparsed_rows"], 1)
        self.assertTrue(any("rubbish" in u["item"] for u in report.unassessable))

    def test_a_one_point_profile_refuses_rather_than_computing(self):
        points, rejected = nca.parse_profile("0 0\n")
        report = nca.check(points, {"auc_linear": Decimal(5)}, rejected)
        self.assertEqual(report.findings, [])
        self.assertTrue(report.unassessable)


class BioanalyticalConsistency(unittest.TestCase):
    CLEAN = "Run: R01 — QC within ±15%. 19/20 (95.0%) passed. Values in ng/mL.\n"

    def test_clean_report_yields_no_findings(self):
        self.assertEqual(ba.check(self.CLEAN).findings, [])

    def test_mixed_units_are_critical(self):
        report = ba.check(self.CLEAN + "Repeat reported in ug/mL.\n")
        self.assertIn("mixed-concentration-units", rules(report))
        self.assertEqual(
            [f.severity for f in report.findings if f.rule == "mixed-concentration-units"],
            ["Critical"],
        )

    def test_pass_rate_arithmetic_is_recomputed(self):
        report = ba.check("Run: R02 — 18/20 (95.0%) passed within ±15%. ng/mL\n")
        self.assertIn("pass-rate-arithmetic", rules(report))

    def test_duplicate_run_identifier_is_flagged(self):
        report = ba.check(self.CLEAN + "Run: R01 — repeat. ng/mL ±15%\n")
        self.assertIn("duplicate-run-identifier", rules(report))

    def test_missing_acceptance_criteria_is_flagged(self):
        report = ba.check("Run: R01 — 19/20 (95.0%) passed. ng/mL\n")
        self.assertIn("no-acceptance-criterion-stated", rules(report))

    def test_pass_rate_over_zero_is_not_silently_accepted(self):
        report = ba.check("Run: R01 — 0/0 (0%) within ±15%. ng/mL\n")
        self.assertIn("pass-rate-over-zero", rules(report))


class ContextValidation(unittest.TestCase):
    CLEAN = (
        "# Role\nx\n# Sources\n- Analysis-Summary.md (final)\n"
        "# Constraints\nclassification: INTERNAL\n# Approval\nx\n# Review\n2026-09-01\n"
    )

    def test_clean_context_yields_no_findings(self):
        self.assertEqual(ctx.check(self.CLEAN).findings, [])

    def test_unrecognised_classification_is_critical_and_reported_in_full(self):
        report = ctx.check(self.CLEAN.replace("INTERNAL", "RESTRICTED_LEVEL_4"))
        self.assertIn("unrecognised-classification", rules(report))
        self.assertIn("RESTRICTED_LEVEL_4", [f.item for f in report.findings])

    def test_missing_classification_is_critical(self):
        report = ctx.check(self.CLEAN.replace("classification: INTERNAL", ""))
        self.assertIn("no-classification", rules(report))

    def test_a_context_that_settles_a_conflict_is_critical(self):
        """The failure this tool exists to catch."""
        report = ctx.check(self.CLEAN + "There is a conflict; we use 14.2 L/h.\n")
        self.assertIn("conflict-resolved-in-context", rules(report))

    def test_a_context_that_surfaces_a_conflict_is_accepted(self):
        report = ctx.check(self.CLEAN + "Conflict on clearance remains unresolved.\n")
        self.assertNotIn("conflict-resolved-in-context", rules(report))

    def test_source_without_precedence_is_flagged(self):
        report = ctx.check(self.CLEAN.replace("Analysis-Summary.md (final)", "Some-Notes.md"))
        self.assertIn("source-without-precedence", rules(report))


class DeliverableConsistency(unittest.TestCase):
    def build(self, rows: int, claim: str, promised: list[str]):
        area = Path(tempfile.mkdtemp())
        (area / "data").mkdir()
        body = "ID,TIME,DV\n" + "".join(f"{i},0,1\n" for i in range(rows))
        (area / "data/adpk.csv").write_text(body, encoding="utf-8")
        (area / "output.lst").write_text("THETA1 1\n", encoding="utf-8")
        return area, deliv.check(
            root=area,
            promised=promised,
            report_text=claim,
            dataset="data/adpk.csv",
            outputs_text="THETA1 1\n",
        )

    def test_matching_record_count_yields_no_count_finding(self):
        _, report = self.build(3, "n = 3 records. THETA1 estimated.", ["data/adpk.csv"])
        self.assertNotIn("record-count-mismatch", rules(report))

    def test_stale_record_count_is_critical(self):
        _, report = self.build(3, "n = 128 records. THETA1 estimated.", ["data/adpk.csv"])
        self.assertIn("record-count-mismatch", rules(report))

    def test_promised_file_absent_is_critical(self):
        _, report = self.build(3, "n = 3 records. THETA1 estimated.", ["run/model.ctl"])
        self.assertIn("promised-file-absent", rules(report))

    def test_identifier_cross_check_refuses_without_outputs(self):
        area = Path(tempfile.mkdtemp())
        report = deliv.check(root=area, promised=[], report_text="CL was estimated.",
                             dataset=None, outputs_text="")
        self.assertTrue(any("identifier" in u["item"] for u in report.unassessable))
        self.assertNotIn("reported-identifier-absent-from-outputs", rules(report))


class DenominatorDiscipline(unittest.TestCase):
    def test_every_tool_refuses_to_summarise_without_a_denominator(self):
        """`Report.summary()` raising is what stops a bare finding count shipping."""
        from findings import Report

        with self.assertRaises(ValueError):
            Report(tool="empty").summary()

    def test_each_new_tool_states_its_denominators(self):
        points, rejected = nca.parse_profile(PROFILE)
        for report in (
            nca.check(points, {}, rejected),
            ba.check("Run: R01 ng/mL ±15%\n"),
            ctx.check(ContextValidation.CLEAN),
        ):
            with self.subTest(report.tool):
                self.assertTrue(report.counts)
                self.assertIn("across", report.summary())


if __name__ == "__main__":
    unittest.main(verbosity=2)
