#!/usr/bin/env python3
"""Unit tests for the package-local IB content and version checker."""

from __future__ import annotations

import argparse
import unittest

import check_ib_pk_section as target

COMPLETE = """IB version: IB-v3
IB date: 2026-07-01
Absorption; plasma protein binding; distribution; metabolism; elimination;
bioavailability; pharmacodynamics; safety and efficacy; dose-response.
"""

REGISTER = {
    "current_ib": {"version": "IB-v3", "date": "2026-07-01", "locator": "register row 1"},
    "dsur_citation": {"version": "IB-v3", "date": "2026-07-01", "locator": "DSUR section 2.6"},
}


class IBCheckTests(unittest.TestCase):
    def test_complete_matching_ib_is_green(self) -> None:
        result = target.inspect(COMPLETE, REGISTER)
        self.assertEqual(result["counts"]["content_items_checked"], 9)
        self.assertEqual(result["findings"], [])

    def test_missing_content_is_red(self) -> None:
        result = target.inspect(COMPLETE.replace("plasma protein binding; ", ""), REGISTER)
        self.assertTrue(any(row.get("classification") == "plasma-protein-binding-absent" for row in result["findings"]))

    def test_stale_dsur_version_is_red(self) -> None:
        register = {
            **REGISTER,
            "dsur_citation": {"version": "IB-v2", "date": "2026-01-15", "locator": "DSUR section 2.6"},
        }
        result = target.inspect(COMPLETE, register)
        stale = [row for row in result["findings"] if row.get("classification") == "stale-version"]
        self.assertEqual(len(stale), 2)

    def test_missing_register_is_needs_input_not_match(self) -> None:
        result = target.inspect(COMPLETE, None)
        self.assertEqual(result["version_state"], "NEEDS_INPUT")
        self.assertEqual(result["counts"]["version_comparisons_checked"], 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    known, remaining = parser.parse_known_args()
    if known.help:
        print(__doc__)
    else:
        unittest.main(argv=[__file__, *remaining])
