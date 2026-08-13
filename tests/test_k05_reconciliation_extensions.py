"""Deterministic tests for the K05 Wave 2-B reconciliation extensions.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library plus repository-pinned StrictYAML

These tests cover exactly the four accepted Wave 2-B IDs: the privacy routing
module, the synthetic-schema structural tool, ETHICS-SUBMISSION-TRACE, and
TOPLINE-SNAPSHOT. They are build diagnostics, not MEDIUM qualification.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from strictyaml import dirty_load

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "reconcile-cross-document-facts"
EVAL = ROOT / "evals" / "reconcile-cross-document-facts"
sys.path.insert(0, str(ROOT / "shared" / "scripts"))

import participant_data_privacy_structure as privacy

TOOL_BANNER = (
    "VENDORED at build time from shared/scripts/ — do not edit here.\n"
    "Edit the canonical source and rebuild; a freshness check compares them.\n\n"
)
MODULE_BANNER = (
    "<!-- VENDORED from shared/policies/privacy-routing.md at build time. Do not edit here.\n"
    "     Edit the canonical source and rebuild; a freshness check compares them. -->\n\n"
)


def fixture(name: str) -> dict[str, object]:
    return json.loads((EVAL / "fixtures" / name).read_text(encoding="utf-8"))


class ParticipantDataPrivacyStructureTests(unittest.TestCase):
    def test_clean_schema_has_visible_denominators_and_applicability_unknown(self) -> None:
        report = privacy.check(fixture("synthetic-privacy-schema-clean.json"))
        self.assertEqual(report.findings, [])
        self.assertEqual(len(report.unknowns), 1)
        self.assertEqual(report.unknowns[0].state, "UNKNOWN")
        self.assertEqual(
            report.counts,
            {
                "agreements": 1,
                "applicability_fields_checked": 7,
                "dataset_fields_checked": 10,
                "datasets": 1,
                "flow_references_checked": 3,
                "flows": 1,
            },
        )
        rendered = report.render()
        for denominator in (
            "datasets 1",
            "dataset_fields_checked 10",
            "flows 1",
            "agreements 1",
            "1 UNKNOWN",
        ):
            self.assertIn(denominator, rendered)

    def test_planted_recipient_and_agreement_defects_preserve_both_sides(self) -> None:
        report = privacy.check(fixture("synthetic-privacy-schema-defects.json"))
        by_rule = {finding.rule: finding for finding in report.findings}
        self.assertEqual(
            set(by_rule),
            {"recipient-not-declared-for-dataset", "agreement-unresolved"},
        )
        recipient = by_rule["recipient-not-declared-for-dataset"]
        self.assertIn("SYN-REPOSITORY-C", recipient.observed)
        self.assertIn("SYN-REPOSITORY-B", recipient.expected)
        agreement = by_rule["agreement-unresolved"]
        self.assertEqual(agreement.item, "SYN-AGR-404")
        self.assertEqual(agreement.severity, "Major")
        self.assertEqual(len(report.unknowns), 1)

    def test_missing_owner_applicability_fails_open_as_unknown_not_as_not_applicable(self) -> None:
        payload = fixture("synthetic-privacy-schema-clean.json")
        payload["applicability"] = {}
        report = privacy.check(payload)
        self.assertGreaterEqual(len(report.unknowns), 7)
        self.assertTrue(all(item.state == "UNKNOWN" for item in report.unknowns))
        self.assertNotIn("NOT_APPLICABLE", report.render())

    def test_record_payload_is_rejected_before_structural_checks(self) -> None:
        payload = fixture("synthetic-privacy-schema-clean.json")
        nested = copy.deepcopy(payload)
        nested["datasets"][0]["records"] = [{"SYN_SUBJECT_KEY": "SYN-001"}]
        with self.assertRaisesRegex(privacy.RestrictedInputError, "RESTRICTED_DO_NOT_PROCESS"):
            privacy.check(nested)

    def test_unclassified_input_is_rejected(self) -> None:
        payload = fixture("synthetic-privacy-schema-clean.json")
        payload["data_classification"] = "UNKNOWN"
        with self.assertRaisesRegex(privacy.RestrictedInputError, "SYNTHETIC_SCHEMA"):
            privacy.check(payload)


class VendoringAndModuleContractTests(unittest.TestCase):
    def test_vendored_tool_is_byte_identical_after_banner_strip(self) -> None:
        canonical = (ROOT / "shared/scripts/participant_data_privacy_structure.py").read_text(encoding="utf-8")
        vendored = (PACKAGE / "scripts/participant_data_privacy_structure.py").read_text(encoding="utf-8")
        self.assertIn(TOOL_BANNER, vendored)
        self.assertEqual(vendored.replace(TOOL_BANNER, "", 1), canonical)

    def test_vendored_module_is_byte_identical_after_banner_strip(self) -> None:
        canonical = (ROOT / "shared/policies/privacy-routing.md").read_text(encoding="utf-8")
        vendored = (PACKAGE / "references/privacy-routing.md").read_text(encoding="utf-8")
        self.assertTrue(vendored.startswith(MODULE_BANNER))
        self.assertEqual(vendored.removeprefix(MODULE_BANNER), canonical)

    def test_privacy_module_carries_canonical_sections_and_human_boundaries(self) -> None:
        text = (ROOT / "shared/policies/privacy-routing.md").read_text(encoding="utf-8")
        for heading in (
            "## Design conventions to check",
            "## Expected statements in a report",
            "## Mechanical checks this module enables",
            "## Boundaries",
        ):
            self.assertIn(heading, text)
        for boundary in (
            "lawful basis",
            "privacy or legal compliance",
            "acceptable re-identification risk",
            "clinically significant",
            "justify a dose",
        ):
            self.assertIn(boundary, text)


class PackageAndDiagnosticTraceTests(unittest.TestCase):
    def test_skill_frontmatter_parses_and_nests_evidence_metadata(self) -> None:
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        block = text.split("---", 2)[1]
        frontmatter = dirty_load(block).data
        self.assertEqual(frontmatter["name"], "reconcile-cross-document-facts")
        self.assertEqual(frontmatter["metadata"]["version"], "0.2.0")
        self.assertEqual(
            frontmatter["metadata"]["evidence-level"],
            "cursor-release150-paired-runs-ps-d024",
        )
        self.assertEqual(frontmatter["metadata"]["human-review"], "required")
        self.assertIn("Provider-neutral", frontmatter["metadata"]["compatibility"])
        self.assertNotIn("evidence-level", frontmatter)
        self.assertNotIn("human-review", frontmatter)
        self.assertNotIn("compatibility", frontmatter)

    def test_exact_extension_markers_and_boundaries_are_present(self) -> None:
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        for marker in ("ETHICS-SUBMISSION-TRACE", "TOPLINE-SNAPSHOT"):
            self.assertIn(marker, text)
        for boundary in (
            "ethics approval",
            "committee-response adequacy",
            "Clinical meaning, causality, benefit-risk, disclosure wording, and commitments",
        ):
            self.assertIn(boundary, text)

    def test_extension_fixture_key_has_exact_three_route_and_ten_state_denominators(self) -> None:
        text = (EVAL / "fixtures/EXTENSION-KEY.md").read_text(encoding="utf-8")
        self.assertIn("3/3 extension routes", text)
        self.assertIn("10/10 planted findings or UNKNOWN states", text)
        self.assertIn("5/5 topline false-positive traps", text)
        for route in ("PRIVACY-STRUCTURE", "ETHICS-SUBMISSION-TRACE", "TOPLINE-SNAPSHOT"):
            self.assertIn(route, text)

    def test_exact_three_extension_cases_exist_and_reference_real_synthetic_inputs(self) -> None:
        expected = {
            "08-execution-privacy-structure.yaml",
            "09-execution-ethics-submission-trace.yaml",
            "11-execution-topline-snapshot.yaml",
        }
        cases = {path.name for path in (EVAL / "cases").glob("*.yaml")}
        self.assertTrue(expected.issubset(cases))
        for name in expected:
            payload = dirty_load(
                (EVAL / "cases" / name).read_text(encoding="utf-8")
            ).data
            for relative in payload["inputs"]:
                path = EVAL / relative
                self.assertTrue(path.is_file(), f"missing declared input {relative}")
                self.assertIn("synthetic", path.name.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
