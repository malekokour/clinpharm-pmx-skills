"""Deterministic checks for K05 Wave 3-C secondary consumers.

Purpose: prove the exact three loading/routing obligations, module freshness,
strict YAML, and fail-then-pass canaries without claiming behavioral qualification.
Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library plus repository-pinned StrictYAML
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parents[1]
CSR_SKILL = ROOT / "skills/review-csr-pk-consistency"
CSR_EVAL = ROOT / "evals/review-csr-pk-consistency"
PROGRAMME_SKILL = ROOT / "skills/reconcile-cross-document-facts"
PROGRAMME_EVAL = ROOT / "evals/reconcile-cross-document-facts"
CANONICAL_MODULE = ROOT / "shared/references/pd-biomarker-context.md"

sys.path.insert(0, str(ROOT / "scripts"))
from eval_schema import load_case, load_suite

FIELDS = (
    "Identity",
    "Role",
    "Context of use",
    "Specimen",
    "Method",
    "Timing",
    "Decision rule",
    "Validation reference",
)

OBLIGATIONS = {
    "review-csr-pk-consistency#pd-biomarker-context": (
        CSR_SKILL / "references/pd-biomarker-context.md",
        CSR_SKILL / "SKILL.md",
        "pd-biomarker-context",
    ),
    "reconcile-cross-document-facts#pd-biomarker-context": (
        PROGRAMME_SKILL / "references/pd-biomarker-context.md",
        PROGRAMME_SKILL / "SKILL.md",
        "pd-biomarker-context",
    ),
    "review-csr-pk-consistency#TOPLINE-SNAPSHOT": (
        CSR_SKILL / "SKILL.md",
        CSR_SKILL / "SKILL.md",
        "TOPLINE-SNAPSHOT",
    ),
}


def frontmatter(path: Path) -> dict[str, object]:
    """Parse one Markdown frontmatter block with StrictYAML."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    return load(match.group(1)).data


def module_contract_errors(text: str) -> list[str]:
    """Return faults in the frozen eight-field/status/human boundary."""
    errors: list[str] = []
    numbered = re.findall(r"^\| ([1-8]) \| ([^|]+?) \|", text, re.MULTILINE)
    names = tuple(name.strip() for _, name in numbered)
    if names != FIELDS:
        errors.append(f"fields differ from exact 8-field contract: {names}")
    for marker in (
        "fields traced / (8 × declared measures)",
        "`UNKNOWN`",
        "source/version register",
        "biological plausibility, qualification sufficiency",
        "clinical meaningfulness, surrogate validity, or dose implications",
        "HUMAN_REVIEW",
    ):
        if marker not in text:
            errors.append(f"missing module marker: {marker}")
    return errors


def route_contract_errors(csr_text: str, programme_text: str) -> list[str]:
    """Return faults in the two PD routes and one topline route."""
    errors: list[str] = []
    shared = (
        "PD-BIOMARKER-TRACE",
        "fields traced / (8 × declared measures)",
        "source",
        "version/status",
        "`UNKNOWN`",
        "human-only",
    )
    for label, text in (("csr", csr_text), ("programme", programme_text)):
        for marker in shared:
            if marker not in text:
                errors.append(f"{label} route missing {marker}")
        for field in FIELDS:
            if field not in text:
                errors.append(f"{label} route missing field {field}")

    for marker in (
        "TOPLINE-SNAPSHOT",
        "reconcile-cross-document-facts",
        "multiple documents beyond this CSR or any programme thread",
        "clinical meaning, causality, benefit-risk, disclosure language, or",
        "commitments",
    ):
        if marker not in csr_text:
            errors.append(f"csr topline route missing {marker}")
    if "existing `scripts/reconcile_programme.py` programme" not in programme_text:
        errors.append("programme PD route does not name the existing engine")
    return errors


class SecondaryConsumerContractTests(unittest.TestCase):
    def test_exact_three_obligations_are_loaded(self) -> None:
        present = {}
        for obligation, (vendored, skill, marker) in OBLIGATIONS.items():
            present[obligation] = (
                vendored.is_file()
                and skill.is_file()
                and marker in skill.read_text(encoding="utf-8")
            )
        self.assertEqual(3, len(present))
        self.assertEqual([], sorted(key for key, value in present.items() if not value))

    def test_both_vendored_modules_are_byte_identical_to_canonical(self) -> None:
        canonical = CANONICAL_MODULE.read_bytes()
        copies = (
            CSR_SKILL / "references/pd-biomarker-context.md",
            PROGRAMME_SKILL / "references/pd-biomarker-context.md",
        )
        self.assertEqual(2, len(copies))
        for path in copies:
            self.assertEqual(canonical, path.read_bytes(), path)

    def test_module_contract_and_drift_canary_red_then_green(self) -> None:
        canonical = CANONICAL_MODULE.read_text(encoding="utf-8")
        self.assertEqual([], module_contract_errors(canonical))
        planted = canonical.replace(
            "fields traced / (8 × declared measures)",
            "fields traced / variable denominator",
            1,
        )
        self.assertGreater(len(module_contract_errors(planted)), 0)

        vendored = (CSR_SKILL / "references/pd-biomarker-context.md").read_bytes()
        self.assertNotEqual(CANONICAL_MODULE.read_bytes(), vendored + b"\nDRIFT")
        self.assertEqual(CANONICAL_MODULE.read_bytes(), vendored)

    def test_route_removal_canary_red_then_green(self) -> None:
        csr = (CSR_SKILL / "SKILL.md").read_text(encoding="utf-8")
        programme = (PROGRAMME_SKILL / "SKILL.md").read_text(encoding="utf-8")
        planted = csr.replace("TOPLINE-SNAPSHOT", "TOPLINE-REMOVED")
        self.assertGreater(len(route_contract_errors(planted, programme)), 0)
        self.assertEqual([], route_contract_errors(csr, programme))

    def test_skill_frontmatter_is_strict_yaml(self) -> None:
        csr = frontmatter(CSR_SKILL / "SKILL.md")
        programme = frontmatter(PROGRAMME_SKILL / "SKILL.md")
        self.assertEqual("review-csr-pk-consistency", csr["name"])
        self.assertEqual("reconcile-cross-document-facts", programme["name"])
        self.assertEqual("required", csr["metadata"]["human-review"])
        self.assertEqual("required", programme["metadata"]["human-review"])

    def test_three_new_cases_and_inputs_validate(self) -> None:
        expected = {
            CSR_EVAL: (
                "13-execution-pd-biomarker-local-trace.yaml",
                "14-execution-topline-secondary-routing.yaml",
            ),
            PROGRAMME_EVAL: ("12-execution-pd-biomarker-programme-trace.yaml",),
        }
        cases = inputs = 0
        for eval_root, names in expected.items():
            load_suite(
                (eval_root / "suite.yaml").read_text(encoding="utf-8"),
                str(eval_root / "suite.yaml"),
            )
            for name in names:
                path = eval_root / "cases" / name
                case = load_case(path.read_text(encoding="utf-8"), str(path))
                cases += 1
                for relative in case.get("inputs", []):
                    fixture = eval_root / relative
                    self.assertTrue(fixture.is_file(), fixture)
                    self.assertIn("synthetic", fixture.name.lower())
                    inputs += 1
        self.assertEqual(3, cases)
        self.assertEqual(3, inputs)

    def test_provisional_keys_state_exact_route_denominators(self) -> None:
        csr = (CSR_EVAL / "fixtures/SECONDARY-CONSUMER-KEY.md").read_text(encoding="utf-8")
        programme = (
            PROGRAMME_EVAL / "fixtures/SECONDARY-CONSUMER-KEY.md"
        ).read_text(encoding="utf-8")
        self.assertIn("2/2 secondary route contracts", csr)
        self.assertIn("2/2 routing decisions", csr)
        self.assertIn("1/1 secondary route contract", programme)
        self.assertIn("5/5 planted non-clean", programme)
        self.assertIn("not MEDIUM qualification evidence", " ".join(csr.split()))
        self.assertIn("not MEDIUM qualification evidence", " ".join(programme.split()))

    def test_wave2_reconciliation_key_denominators_remain_unchanged(self) -> None:
        text = (PROGRAMME_EVAL / "fixtures/EXTENSION-KEY.md").read_text(encoding="utf-8")
        self.assertIn("3/3 extension routes", text)
        self.assertIn("10/10 planted findings or UNKNOWN states", text)
        self.assertIn("5/5 topline false-positive traps", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
