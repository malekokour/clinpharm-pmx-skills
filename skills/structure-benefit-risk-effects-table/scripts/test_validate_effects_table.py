#!/usr/bin/env python3
"""Unit tests for the local effects-table structural validator."""

from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path

import validate_effects_table as target

VALID = """| Effect ID | Domain | Population / analysis set | Endpoint / time point | Comparator | Effect as written | Uncertainty as written | Source / version | Locator | Structural state | Disposition |
|---|---|---|---|---|---|---|---|---|---|---|
| E-01 | efficacy | ITT | Week 12 response | placebo | 42% | 95% CI 30–54 | Study A v1 | Table 3 | complete | open |
"""


class EffectsTableTests(unittest.TestCase):
    def write(self, body: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "table.md"
        path.write_text(body, encoding="utf-8")
        return path

    def test_complete_row_is_clean(self) -> None:
        checked, findings = target.validate(self.write(VALID))
        self.assertEqual(checked, 1)
        self.assertEqual(findings, [])

    def test_missing_locator_is_reported(self) -> None:
        checked, findings = target.validate(self.write(VALID.replace("Table 3", "NEEDS_INPUT")))
        self.assertEqual(checked, 1)
        self.assertTrue(any("Locator" in finding for finding in findings))

    def test_absent_required_header_is_fatal(self) -> None:
        checked, findings = target.validate(self.write("| Effect ID | Domain |\n|---|---|\n| E-01 | efficacy |\n"))
        self.assertEqual(checked, 0)
        self.assertIn("required column", findings[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    known, remaining = parser.parse_known_args()
    if known.help:
        print(__doc__)
    else:
        unittest.main(argv=[__file__, *remaining])
