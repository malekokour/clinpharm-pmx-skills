"""Deterministic K05 checks for protocol consent, vulnerability, and PD routes.

Purpose: verify the three Wave-2-A artifacts without touching shared registries or
qualification state, including fail-then-pass canaries for every new check.
Author: Malek Okour
Date: 2026-08-11
Dependencies: Python standard library plus project-pinned strictyaml
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/review-protocol-pk-sections"
EVAL = ROOT / "evals/review-protocol-pk-sections"
CANONICAL_TOOL = ROOT / "shared/scripts/vulnerable_population_gap_register.py"
VENDORED_TOOL = SKILL / "scripts/vulnerable_population_gap_register.py"
CANONICAL_MODULE = ROOT / "shared/references/pd-biomarker-context.md"
VENDORED_MODULE = SKILL / "references/pd-biomarker-context.md"

sys.path.insert(0, str(ROOT / "scripts"))
from check_vendored import BANNER
from eval_schema import load_case, load_suite


def load_tool(path: Path):
    spec = importlib.util.spec_from_file_location("vulnerable_population_gap_register", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    return load(match.group(1)).data


def consent_contract_errors(text: str) -> list[str]:
    errors: list[str] = []
    normalized = re.sub(r"\s+", " ", text)
    required = (
        "CONSENT-CONSISTENCY",
        "procedures traced / protocol-declared procedures",
        "version links checked / version links supplied",
        "Consent adequacy, validity, voluntariness",
        "scripts/vulnerable_population_gap_register.py",
        "references/pd-biomarker-context.md",
    )
    for marker in required:
        if marker not in normalized:
            errors.append(f"missing {marker}")
    return errors


def module_contract_errors(text: str) -> list[str]:
    errors: list[str] = []
    required = (
        "ICH E16",
        "Draft, nonbinding",
        "Check exactly **8 fields per declared biomarker or PD measure**",
        "`UNKNOWN`",
        "biological plausibility, qualification sufficiency",
        "clinical meaningfulness, surrogate validity, or dose implications",
        "review-csr-pk-consistency",
        "reconcile-cross-document-facts",
    )
    for marker in required:
        if marker not in text:
            errors.append(f"missing {marker}")
    numbered_fields = re.findall(r"^\| ([1-8]) \|", text, re.MULTILINE)
    if numbered_fields != list("12345678"):
        errors.append(f"core fields are not exactly 1..8: {numbered_fields}")
    return errors


class K05ProtocolExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool(CANONICAL_TOOL)

    def fixture_json(self, name: str) -> dict[str, object]:
        return json.loads((EVAL / "fixtures" / name).read_text(encoding="utf-8"))

    def test_tool_canonical_and_vendored_copies_are_byte_identical(self) -> None:
        vendored = VENDORED_TOOL.read_text(encoding="utf-8")
        self.assertIn(BANNER, vendored)
        self.assertEqual(
            CANONICAL_TOOL.read_text(encoding="utf-8"),
            vendored.replace(BANNER, "", 1),
        )

    def test_module_canonical_and_vendored_copies_are_byte_identical(self) -> None:
        self.assertEqual(CANONICAL_MODULE.read_bytes(), VENDORED_MODULE.read_bytes())

    def test_vulnerable_register_known_bad_then_clean_canary(self) -> None:
        bad = self.tool.build_register(
            self.fixture_json("synthetic-vulnerable-population-manifest.json")
        )
        self.assertEqual(2, bad["denominators"]["populations_declared"])
        self.assertEqual(10, bad["denominators"]["artifact_fields_checked"])
        self.assertEqual({"PRESENT": 8, "MISSING": 1, "UNKNOWN": 1}, bad["counts"])
        self.assertEqual("HUMAN_REVIEW", bad["result"])
        self.assertTrue(all(row["human_disposition"] == "UNSET" for row in bad["rows"]))

        clean = self.tool.build_register(
            self.fixture_json("synthetic-vulnerable-population-manifest-clean.json")
        )
        self.assertEqual(5, clean["denominators"]["artifact_fields_checked"])
        self.assertEqual({"PRESENT": 5, "MISSING": 0, "UNKNOWN": 0}, clean["counts"])
        self.assertEqual("SUPPLIED", clean["applicability"]["state"])

    def test_vulnerable_register_unknown_applicability_fails_closed(self) -> None:
        manifest = self.fixture_json("synthetic-vulnerable-population-manifest-clean.json")
        manifest["applicability"] = {"profile_id": "partial"}
        report = self.tool.build_register(manifest)
        self.assertEqual("UNKNOWN", report["applicability"]["state"])
        self.assertEqual(
            ["profile_version", "as_of", "jurisdictions", "owner"],
            report["applicability"]["missing_fields"],
        )

    def test_vulnerable_register_rejects_participant_level_payload_keys(self) -> None:
        manifest = self.fixture_json("synthetic-vulnerable-population-manifest-clean.json")
        manifest["subject_ids"] = ["SYN-001"]
        with self.assertRaisesRegex(self.tool.ManifestError, "participant-level"):
            self.tool.build_register(manifest)

    def test_consent_extension_contract_red_then_green(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        planted = text.replace("CONSENT-CONSISTENCY", "CONSENT-CONSISTENCX")
        self.assertGreater(len(consent_contract_errors(planted)), 0)
        self.assertEqual([], consent_contract_errors(text))

    def test_skill_frontmatter_is_strict_yaml_and_metadata_is_nested(self) -> None:
        metadata = frontmatter(SKILL / "SKILL.md")
        self.assertNotIn("evidence-level", metadata)
        self.assertIsInstance(metadata.get("metadata"), dict)
        nested = metadata["metadata"]
        self.assertEqual("cursor-release150-paired-runs-ps-d024", nested["evidence-level"])
        self.assertEqual("required", nested["human-review"])

    def test_pd_module_contract_red_then_green(self) -> None:
        text = CANONICAL_MODULE.read_text(encoding="utf-8")
        planted = text.replace("`UNKNOWN`", "`UNSTATED`")
        self.assertGreater(len(module_contract_errors(planted)), 0)
        self.assertEqual([], module_contract_errors(text))

    def test_three_extension_cases_and_all_inputs_validate(self) -> None:
        suite = load_suite(
            (EVAL / "suite.yaml").read_text(encoding="utf-8"),
            str(EVAL / "suite.yaml"),
        )
        self.assertEqual("MEDIUM", suite["qualification_profile"])
        case_paths = sorted((EVAL / "cases").glob("1[1-3]-*.yaml"))
        self.assertEqual(3, len(case_paths))
        inputs_checked = 0
        for path in case_paths:
            case = load_case(path.read_text(encoding="utf-8"), str(path))
            for relative in case.get("inputs", []):
                self.assertTrue((EVAL / relative).is_file(), relative)
                inputs_checked += 1
        self.assertEqual(7, inputs_checked)


if __name__ == "__main__":
    unittest.main()
