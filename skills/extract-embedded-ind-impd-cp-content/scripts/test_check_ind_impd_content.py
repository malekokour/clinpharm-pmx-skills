#!/usr/bin/env python3
"""Unit tests for the package-local IND/IMPD content inventory."""

from __future__ import annotations

import argparse
import unittest

import check_ind_impd_content as target


class ContentInventoryTests(unittest.TestCase):
    def test_complete_ind_is_green(self) -> None:
        text = (
            "Mechanism of action: stated.\nAbsorption: stated.\nDistribution: stated.\n"
            "Metabolism: stated.\nExcretion: not known.\n"
        )
        result = target.inspect(text, "IND")
        self.assertEqual(result["counts"]["items_checked"], 5)
        self.assertEqual(result["counts"]["missing_declarations"], 0)

    def test_missing_ind_excretion_is_red(self) -> None:
        text = (
            "Mechanism of action: stated.\nAbsorption: stated.\nDistribution: stated.\n"
            "Metabolism: stated.\n"
        )
        result = target.inspect(text, "IND")
        self.assertEqual(result["counts"]["missing_declarations"], 1)
        self.assertEqual(result["findings"][0]["classification"], "excretion-absent")

    def test_impd_requires_both_shapes(self) -> None:
        result = target.inspect("Module 4 non-clinical summary only.\n", "IMPD")
        self.assertEqual(result["counts"]["items_checked"], 2)
        self.assertEqual(result["findings"][0]["classification"], "module-5-shaped-clinical-summary-absent")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    known, remaining = parser.parse_known_args()
    if known.help:
        print(__doc__)
    else:
        unittest.main(argv=[__file__, *remaining])
