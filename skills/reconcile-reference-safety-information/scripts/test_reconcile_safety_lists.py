#!/usr/bin/env python3
"""Unit tests for the local reference-safety list comparator."""

from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path

import reconcile_safety_lists as target

VALID = """| Term | Category | Source locator |
|---|---|---|
| Hepatotoxicity | hepatic | §4.8 |
| Neutropenia | hematologic | §4.8 |
"""


class SafetyListTests(unittest.TestCase):
    def write(self, body: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "list.md"
        path.write_text(body, encoding="utf-8")
        return path

    def test_valid_list_loads(self) -> None:
        terms, problems = target.load_terms(self.write(VALID))
        self.assertEqual(len(terms), 2)
        self.assertEqual(problems, [])

    def test_duplicate_term_is_reported(self) -> None:
        terms, problems = target.load_terms(self.write(VALID + "| hepatotoxicity | hepatic | §5.1 |\n"))
        self.assertEqual(len(terms), 2)
        self.assertTrue(any("duplicate" in problem for problem in problems))

    def test_missing_locator_header_is_fatal(self) -> None:
        terms, problems = target.load_terms(self.write("| Term | Category |\n|---|---|\n| Rash | skin |\n"))
        self.assertEqual(terms, {})
        self.assertIn("Source locator", problems[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    known, remaining = parser.parse_known_args()
    if known.help:
        print(__doc__)
    else:
        unittest.main(argv=[__file__, *remaining])
