"""Deterministic K05 checks for the DDI enzyme/transporter extension.

Purpose: verify the Wave-3-A artifact, inventory fixtures, vendoring, strict YAML,
and provisional key without changing qualification or release state.
Author: Malek Okour
Date: 2026-08-11
Dependencies: Python standard library plus project-pinned strictyaml
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

from strictyaml import load
from strictyaml.exceptions import StrictYAMLError

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/review-ddi-evidence"
EVAL = ROOT / "evals/review-ddi-evidence"
CANONICAL_MODULE = ROOT / "shared/references/drug-drug-interaction.md"
VENDORED_MODULE = SKILL / "references/drug-drug-interaction.md"

sys.path.insert(0, str(ROOT / "scripts"))
from eval_schema import load_case, load_suite

sys.path.insert(0, str(SKILL / "scripts"))
from check_ddi_triggers import extract_ratios

FIELDS = (
    "Enzyme/transporter identity",
    "Assay system",
    "Substrate/inhibitor/inducer role",
    "Concentration",
    "Result",
    "Qualifier",
    "Source status",
    "Exact locator",
)
HUMAN_BOUNDARIES = (
    "Biological relevance",
    "assay adequacy",
    "clinical significance",
    "untested-pathway relevance",
    "study or dose decision",
)


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError("missing YAML frontmatter")
    try:
        metadata = load(match.group(1)).data
    except StrictYAMLError as exc:
        raise AssertionError(f"invalid strict YAML: {exc}") from exc
    return metadata, text[match.end() :]


def skill_contract_errors(text: str) -> list[str]:
    errors: list[str] = []
    try:
        metadata, _body = split_frontmatter(text)
    except AssertionError as exc:
        return [str(exc)]
    nested = metadata.get("metadata")
    if not isinstance(nested, dict):
        errors.append("metadata is not nested")
        nested = {}
    for key in ("compatibility", "evidence-level", "human-review"):
        if key in metadata:
            errors.append(f"{key} is at document root")
        if key not in nested:
            errors.append(f"metadata.{key} is missing")
    required = (
        "ENZYME-TRANSPORTER-INVENTORY",
        "references/drug-drug-interaction.md",
        "checked / expected",
        "Never query without authority",
        "Only a qualified human reviewer may judge biological relevance",
    )
    for marker in required:
        if marker not in text:
            errors.append(f"missing {marker}")
    return errors


def module_contract_errors(text: str) -> list[str]:
    errors: list[str] = []
    normalized = re.sub(r"\s+", " ", text)
    required = (
        "## `ENZYME-TRANSPORTER-INVENTORY`",
        "owner-declared source set",
        "Licensed-database provenance is recorded, never reconstructed",
        "An `UNKNOWN` cell is checked but unresolved",
        "Biological relevance, assay adequacy, clinical significance, untested-",
    )
    for marker in required:
        if marker not in normalized:
            errors.append(f"missing {marker}")
    numbered_fields = re.findall(r"^\| ([1-8]) \| ([^|]+?) \|", text, re.MULTILINE)
    if [number for number, _field in numbered_fields] != list("12345678"):
        errors.append("inventory fields are not exactly numbered 1..8")
    if tuple(field.strip() for _number, field in numbered_fields) != FIELDS:
        errors.append("inventory field names differ from the eight-field contract")
    return errors


def inventory_contract_errors(text: str) -> list[str]:
    errors: list[str] = []
    try:
        metadata, body = split_frontmatter(text)
    except AssertionError as exc:
        return [str(exc)]
    rows = [line for line in body.splitlines() if line.startswith("|")]
    if len(rows) < 2:
        return ["inventory table is missing"]
    header = tuple(cell.strip() for cell in rows[0].strip("|").split("|"))
    if header != FIELDS:
        errors.append(f"unexpected header: {header}")
    data_rows = rows[2:]
    cells = [tuple(cell.strip() for cell in row.strip("|").split("|")) for row in data_rows]
    if any(len(row) != 8 for row in cells):
        errors.append("a data row does not contain exactly eight fields")
    expected_rows = int(str(metadata["expected-inventory-rows"]))
    expected_fields = int(str(metadata["expected-fields-per-row"]))
    expected_cells = int(str(metadata["expected-field-cells"]))
    expected_unknown = int(str(metadata["expected-unknown-cells"]))
    if len(cells) != expected_rows:
        errors.append(f"found {len(cells)} rows; expected {expected_rows}")
    if expected_fields != 8 or expected_cells != expected_rows * 8:
        errors.append("declared field-cell denominator is not rows × 8")
    unknown = sum(cell == "UNKNOWN" for row in cells for cell in row)
    if unknown != expected_unknown:
        errors.append(f"found {unknown} UNKNOWN cells; expected {expected_unknown}")
    return errors


def key_contract_errors(text: str) -> list[str]:
    required = (
        "severity_status: provisional",
        "5 / 5",
        "40 / 40",
        "3 | `NEEDS_INPUT`",
        "2 / 2",
        "16 / 16",
        "five false-positive traps",
    )
    return [f"missing {marker}" for marker in required if marker not in text]


class K05DDIExtensionTests(unittest.TestCase):
    def test_ratio_parser_ignores_digits_inside_auc_parameter_names(self) -> None:
        text = (
            "The geometric mean\n"
            "ratio for vorastol AUC0-inf with veltrapib was 2.14.\n"
            "AUCR 1.50.\n"
            "| Geometric mean ratio (with inhibitor / alone) | 2.41 |\n"
        )
        self.assertEqual(
            [("geometric mean\nratio", 2.14), ("AUCR", 1.5), ("Geometric mean ratio", 2.41)],
            extract_ratios(text),
        )

    def test_module_contract_red_then_green(self) -> None:
        text = CANONICAL_MODULE.read_text(encoding="utf-8")
        planted = text.replace("ENZYME-TRANSPORTER-INVENTORY", "INVENTORY-OMITTED")
        self.assertGreater(len(module_contract_errors(planted)), 0)
        self.assertEqual([], module_contract_errors(text))

    def test_skill_contract_and_strict_frontmatter_red_then_green(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        planted = text.replace(
            "  evidence-level: cursor-release150-paired-runs-ps-d024\n"
            "  human-review: required\n"
            "  compatibility:",
            "evidence-level: cursor-release150-paired-runs-ps-d024\n"
            "human-review: required\n"
            "compatibility:",
            1,
        )
        self.assertGreater(len(skill_contract_errors(planted)), 0)
        self.assertEqual([], skill_contract_errors(text))

    def test_module_canonical_and_vendored_red_then_green(self) -> None:
        canonical = CANONICAL_MODULE.read_bytes()
        vendored = VENDORED_MODULE.read_bytes()
        self.assertNotEqual(canonical, vendored + b"\nplanted drift")
        self.assertEqual(canonical, vendored)

    def test_unknown_inventory_fixture_red_then_green(self) -> None:
        text = (EVAL / "fixtures/synthetic-enzyme-transporter-inventory-unknown.md").read_text(
            encoding="utf-8"
        )
        planted = text.replace("expected-unknown-cells: 3", "expected-unknown-cells: 2")
        self.assertGreater(len(inventory_contract_errors(planted)), 0)
        self.assertEqual([], inventory_contract_errors(text))

    def test_clean_inventory_fixture_red_then_green(self) -> None:
        text = (EVAL / "fixtures/synthetic-enzyme-transporter-inventory-clean.md").read_text(
            encoding="utf-8"
        )
        planted = text.replace("expected-field-cells: 16", "expected-field-cells: 15")
        self.assertGreater(len(inventory_contract_errors(planted)), 0)
        self.assertEqual([], inventory_contract_errors(text))

    def test_provisional_key_red_then_green(self) -> None:
        text = (EVAL / "fixtures/EXPERT-KEY.md").read_text(encoding="utf-8")
        planted = text.replace("40 / 40", "39 / 40", 1)
        self.assertGreater(len(key_contract_errors(planted)), 0)
        self.assertEqual([], key_contract_errors(text))

    def test_two_extension_cases_and_inputs_red_then_green(self) -> None:
        suite_path = EVAL / "suite.yaml"
        suite = load_suite(suite_path.read_text(encoding="utf-8"), str(suite_path))
        self.assertEqual("MEDIUM", suite["qualification_profile"])
        case_paths = sorted((EVAL / "cases").glob("1[12]-*.yaml"))
        self.assertEqual(2, len(case_paths))
        inputs_checked = 0
        for path in case_paths:
            text = path.read_text(encoding="utf-8")
            planted = text.replace("inputs:", "inputz:", 1)
            with self.assertRaises(ValueError):
                load_case(planted, f"planted:{path.name}")
            case = load_case(text, str(path))
            self.assertEqual("ENZYME-TRANSPORTER-INVENTORY", case["mode"])
            for relative in case.get("inputs", []):
                self.assertTrue((EVAL / relative).is_file(), relative)
                inputs_checked += 1
        self.assertEqual(2, inputs_checked)


if __name__ == "__main__":
    unittest.main()
