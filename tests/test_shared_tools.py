"""Deterministic tests for the shared tools T01–T06.

Each numeric expectation is derived from the cited guidance's own stated rule,
computed independently in the test, not copied from the implementation. A test
that asserts what the code already does proves only that the code is
self-consistent.
"""

from __future__ import annotations

import math
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared" / "scripts"))

import cross_document_consistency as t05
import ctd_placement as t06
import label_conformance as t04
import mrsd_calculator as t01
import pk_plausibility as t03
import renal_staging as t02


class MRSDCalculatorTests(unittest.TestCase):
    """T01 against the FDA 2005 body-surface-area conversion."""

    def test_km_factors_match_the_guidance_table(self) -> None:
        # Km = body weight / body surface area, FDA 2005 Table 1.
        for species, km in (("human", 37.0), ("rat", 6.0), ("dog", 20.0),
                            ("monkey", 12.0), ("mouse", 3.0), ("rabbit", 12.0)):
            self.assertEqual(t01.KM_FACTORS[species], km, species)

    def test_hed_equals_noael_times_km_ratio(self) -> None:
        # Rule: HED = NOAEL x (Km_animal / Km_human). Computed here, not read.
        for species, noael in (("rat", 10.0), ("dog", 5.0), ("monkey", 25.0)):
            expected = noael * (t01.KM_FACTORS[species] / 37.0)
            hed, step = t01.hed_from_noael(noael, species)
            self.assertAlmostEqual(hed, expected, places=9, msg=species)
            self.assertEqual(step.unit, "mg/kg")

    def test_rat_worked_example(self) -> None:
        # 10 mg/kg in rat -> 10 * 6/37 = 1.6216... mg/kg
        hed, _ = t01.hed_from_noael(10.0, "rat")
        self.assertAlmostEqual(hed, 60.0 / 37.0, places=9)

    def test_mrsd_divides_by_the_safety_factor(self) -> None:
        result = t01.mrsd_from_hed(1.62, safety_factor=10.0, human_weight_kg=60.0)
        self.assertAlmostEqual(result.mrsd_mg_kg, 0.162, places=9)
        self.assertAlmostEqual(result.mrsd_mg_total, 0.162 * 60.0, places=9)
        self.assertEqual(result.warnings, [])

    def test_reduced_safety_factor_warns_rather_than_silently_accepting(self) -> None:
        result = t01.mrsd_from_hed(1.62, safety_factor=3.0)
        self.assertTrue(any("below the default 10" in w for w in result.warnings))

    def test_most_sensitive_species_is_lowest_hed_and_shows_the_ranking(self) -> None:
        species, hed, ranking = t01.most_sensitive_species(
            {"rat": 10.0, "dog": 5.0, "monkey": 25.0}
        )
        # dog: 5*20/37 = 2.70 ; rat: 10*6/37 = 1.62 ; monkey: 25*12/37 = 8.11
        self.assertEqual(species, "rat")
        self.assertAlmostEqual(hed, 60.0 / 37.0, places=9)
        self.assertEqual(len(ranking), 3, "the full ranking must be visible")

    def test_unknown_species_and_bad_input_raise(self) -> None:
        with self.assertRaises(ValueError):
            t01.hed_from_noael(10.0, "unicorn")
        with self.assertRaises(ValueError):
            t01.hed_from_noael(-1.0, "rat")


class RenalStagingTests(unittest.TestCase):
    """T02 against the FDA March 2024 eGFR bands."""

    def test_band_boundaries(self) -> None:
        for egfr, expected in ((120, "Normal or high"), (90, "Normal or high"),
                               (89, "Mild impairment"), (60, "Mild impairment"),
                               (59, "Moderate impairment"), (30, "Moderate impairment"),
                               (29, "Severe impairment"), (15, "Severe impairment"),
                               (14, "Kidney failure"), (0, "Kidney failure")):
            self.assertEqual(t02.stage(egfr), expected, f"eGFR {egfr}")

    def test_mismatch_is_flagged_and_agreement_is_silent(self) -> None:
        self.assertIsNone(t02.check_reported_stage(45, "Moderate impairment", "T14.1"))
        finding = t02.check_reported_stage(45, "Mild impairment", "T14.1")
        self.assertIsNotNone(finding)
        self.assertEqual(finding["rule"], "renal-stage-mismatch")
        self.assertEqual(finding["kind"], "mechanical")


class PKPlausibilityTests(unittest.TestCase):
    """T03 — units, ranges, and arithmetic relationships."""

    def test_unit_swap_is_critical(self) -> None:
        r = t03.Report()
        t03.check_unit("CL", "mL/h", "T14.2 row 3", r)
        self.assertEqual(len(r.findings), 0, "mL/h is a valid clearance unit")
        t03.check_unit("Cmax", "L/h", "T14.2 row 4", r)
        self.assertEqual(r.findings[-1].rule, "unit-inconsistency")
        self.assertEqual(r.findings[-1].severity, "Critical")

    def test_accumulation_matches_the_one_compartment_relation(self) -> None:
        # R = 1 / (1 - exp(-ln2 * tau / t-half)); t-half 12 h, tau 24 h -> 1.333
        expected = 1.0 / (1.0 - math.exp(-math.log(2) * 24.0 / 12.0))
        r = t03.Report()
        t03.check_accumulation_consistency(12.0, 24.0, expected, "§12.3", r)
        self.assertEqual(len(r.findings), 0, "a consistent ratio must not flag")
        t03.check_accumulation_consistency(12.0, 24.0, expected * 3, "§12.3", r)
        self.assertEqual(r.findings[-1].rule, "accumulation-half-life-inconsistency")

    def test_confidence_interval_must_bracket_its_point_estimate(self) -> None:
        r = t03.Report()
        t03.check_ratio_statistic(1.05, 0.92, 1.20, "T14.2.5", r)
        self.assertEqual(len(r.findings), 0)
        t03.check_ratio_statistic(1.45, 0.92, 1.20, "T14.2.5", r)
        self.assertEqual(r.findings[-1].rule, "point-estimate-outside-ci")
        t03.check_ratio_statistic(1.05, 1.20, 0.92, "T14.2.5", r)
        self.assertEqual(r.findings[-1].rule, "ci-bounds-reversed")

    def test_every_finding_is_labelled_mechanical(self) -> None:
        r = t03.Report()
        t03.check_unit("Cmax", "L/h", "x", r)
        t03.check_range("t1/2", 99999.0, "y", r)
        self.assertTrue(all(f.kind == "mechanical" for f in r.findings))

    def test_summary_always_carries_a_denominator(self) -> None:
        r = t03.Report()
        t03.check_unit("Cmax", "ng/mL", "x", r)
        self.assertEqual(r.summary()["checked"], 1)
        self.assertIn("by_severity", r.summary())


class CrossDocumentConsistencyTests(unittest.TestCase):
    """T05 — extraction, tolerance, and contradiction preservation."""

    def test_extracts_value_and_unit(self) -> None:
        vals = t05.extract("Mean AUC was 412 ng·h/mL overall.", "CSR", "3", "§12.3")
        self.assertEqual(vals[0].number, Decimal(412))
        self.assertEqual(vals[0].unit, "ng·h/mL")

    def test_thousands_separators_do_not_break_parsing(self) -> None:
        vals = t05.extract("AUC 12,480 ng·h/mL", "CSR", "3", "§12.3")
        self.assertEqual(vals[0].number, Decimal(12480))

    def test_rounding_inside_tolerance_is_not_a_discrepancy(self) -> None:
        self.assertTrue(t05.within_tolerance(Decimal("412.0"), Decimal("412.4"),
                                             Decimal("0.005")))
        self.assertFalse(t05.within_tolerance(Decimal(412), Decimal(481),
                                              Decimal("0.005")))

    def test_conflict_preserves_both_sides_with_locators(self) -> None:
        reg = t05.Register()
        left = t05.extract("steady state AUC 412 ng·h/mL", "CSR", "3", "Synopsis §2.3")
        right = t05.extract("steady state AUC 481 ng·h/mL", "NCA", "1", "Table 14.2.1")
        t05.reconcile(reg, left, right)
        self.assertEqual(len(reg.discrepancies), 1)
        row = reg.discrepancies[0].as_dict()
        self.assertIn("412", row["statement_as_written"])
        self.assertIn("481", row["expected_value_or_content"])
        self.assertIn("Synopsis", row["statement_locator"])
        self.assertIn("Table 14.2.1", row["expected_locator"])
        self.assertEqual(row["disposition"], "open",
                         "a tool may only ever open an item, never close one")

    def test_stale_version_is_its_own_finding_class(self) -> None:
        reg = t05.Register()
        vals = t05.extract("dose 200 mg", "Protocol", "2", "§9.3")
        t05.check_version_baseline(vals, {"Protocol": "3"}, reg)
        self.assertEqual(reg.discrepancies[0].rule, "stale-version")

    def test_register_summary_reports_comparisons(self) -> None:
        reg = t05.Register()
        t05.reconcile(reg, t05.extract("AUC 412 ng·h/mL", "A", "1", "x"),
                      t05.extract("AUC 412 ng·h/mL", "B", "1", "y"))
        self.assertGreaterEqual(reg.summary()["comparisons"], 1)
        self.assertEqual(reg.summary()["discrepancies"], 0)


class LabelConformanceTests(unittest.TestCase):
    """T04 — required content and prohibited phrasing."""

    def test_missing_required_subsection_is_critical(self) -> None:
        findings = t04.check("12.1 Mechanism of Action\n12.2 Pharmacodynamics\n")
        rules = {f["rule"] for f in findings}
        self.assertIn("missing-required-subsection", rules)
        self.assertTrue(any(f["severity"] == "Critical" for f in findings))

    def test_complete_section_with_conventional_order_is_clean(self) -> None:
        text = ("12.1 Mechanism of Action\n12.2 Pharmacodynamics\n12.3 Pharmacokinetics\n"
                "Absorption\nDistribution\nElimination\nSpecific Populations\n"
                "Drug Interaction Studies\n")
        self.assertEqual(t04.check(text), [])

    def test_prohibited_phrasing_is_flagged(self) -> None:
        text = ("12.1 Mechanism of Action\n12.2 Pharmacodynamics\n12.3 Pharmacokinetics\n"
                "The drug was well-tolerated at all doses.\n")
        rules = {f["rule"] for f in t04.check(text)}
        self.assertIn("prohibited-phrasing", rules)


class CTDPlacementTests(unittest.TestCase):
    """T06 — placement by primary objective."""

    def test_known_objectives_map_to_their_sections(self) -> None:
        for objective, section in (("bioequivalence", "5.3.1"),
                                   ("food effect", "5.3.3.4"),
                                   ("renal impairment", "5.3.3.3"),
                                   ("population pk", "5.3.3.5")):
            self.assertEqual(t06.expected_section(objective), section, objective)

    def test_mismatch_is_flagged_and_agreement_is_silent(self) -> None:
        self.assertIsNone(t06.check("Study 101", "food effect", "5.3.3.4"))
        finding = t06.check("Study 101", "food effect", "5.3.3.1")
        self.assertEqual(finding["rule"], "ctd-placement-mismatch")

    def test_unmappable_objective_emits_unknown_rather_than_guessing(self) -> None:
        finding = t06.check("Study 999", "exploratory imaging substudy", "5.3.5.2")
        self.assertEqual(finding["expected"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
