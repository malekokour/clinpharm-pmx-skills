#!/usr/bin/env python3
"""Recompute allometric scaling relations and compare against reported values.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Usage:
    python3 scaling_check.py relations.json
    python3 scaling_check.py --self-test

What it checks
--------------
One relation only, the simple allometric form:

    predicted = reference * (weight / reference_weight) ** exponent

Given a reference value, both weights, and an exponent, it recomputes the
prediction and compares it against the reported one within a stated tolerance.

Why it is this narrow
---------------------
This is the one relation in a human PK prediction that is fully determined by
values the deliverable already reports. Everything else — IVIVE scaling,
PBPK output, protein-binding correction — depends on model structure and
platform internals that are not recoverable from a report.

A script that appeared to check those would be asserting a computation it cannot
actually perform. So it checks the one thing it can, and the skill's procedure
says explicitly that zero checkable relations is ``CANNOT_ASSESS`` rather than a
pass.

Input shape
-----------
    {
      "tolerance_percent": 10.0,
      "relations": [
        {"parameter": "CL", "unit": "L/h",
         "reference_value": 0.5, "reference_weight_kg": 0.25,
         "weight_kg": 70.0, "exponent": 0.75, "reported_value": 43.0,
         "locator": "Table 3"}
      ]
    }

Every field is required except ``locator``. A missing field is reported as
``CANNOT_ASSESS`` for that relation, never silently skipped — a relation dropped
without comment is how a denominator quietly shrinks.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = (
    "parameter",
    "reference_value",
    "reference_weight_kg",
    "weight_kg",
    "exponent",
    "reported_value",
)


def evaluate(relation: dict, tolerance_percent: float) -> dict:
    missing = [key for key in REQUIRED if relation.get(key) is None]
    if missing:
        return {
            "parameter": relation.get("parameter", "<unnamed>"),
            "state": "CANNOT_ASSESS",
            "detail": f"missing required field(s): {', '.join(missing)}",
        }
    try:
        reference = float(relation["reference_value"])
        reference_weight = float(relation["reference_weight_kg"])
        weight = float(relation["weight_kg"])
        exponent = float(relation["exponent"])
        reported = float(relation["reported_value"])
    except (TypeError, ValueError) as exc:
        return {
            "parameter": relation.get("parameter", "<unnamed>"),
            "state": "CANNOT_ASSESS",
            "detail": f"non-numeric value: {exc}",
        }

    if reference_weight <= 0 or weight <= 0:
        return {
            "parameter": relation["parameter"],
            "state": "CANNOT_ASSESS",
            "detail": "weights must be positive",
        }

    recomputed = reference * (weight / reference_weight) ** exponent
    if recomputed == 0:
        deviation = 0.0 if reported == 0 else float("inf")
    else:
        deviation = abs(reported - recomputed) / abs(recomputed) * 100.0

    return {
        "parameter": relation["parameter"],
        "unit": relation.get("unit", ""),
        "locator": relation.get("locator", ""),
        "recomputed": recomputed,
        "reported": reported,
        "deviation_percent": deviation,
        "state": "MATCH" if deviation <= tolerance_percent else "MISMATCH",
    }


def report(document: dict) -> int:
    tolerance = float(document.get("tolerance_percent", 10.0))
    relations = document.get("relations") or []

    if not relations:
        print("CANNOT_ASSESS: 0 scaling relations supplied — nothing was checked")
        print("checked 0/0 relations")
        return 2

    results = [evaluate(relation, tolerance) for relation in relations]
    for result in results:
        if result["state"] == "CANNOT_ASSESS":
            print(f"CANNOT_ASSESS {result['parameter']}: {result['detail']}")
        else:
            print(
                f"{result['state']} {result['parameter']} "
                f"reported={result['reported']:g}{result['unit']} "
                f"recomputed={result['recomputed']:.4g}{result['unit']} "
                f"deviation={result['deviation_percent']:.1f}% "
                f"tolerance={tolerance:g}% locator={result['locator'] or '-'}"
            )

    matched = sum(1 for r in results if r["state"] == "MATCH")
    mismatched = sum(1 for r in results if r["state"] == "MISMATCH")
    unassessable = sum(1 for r in results if r["state"] == "CANNOT_ASSESS")
    print(
        f"checked {matched + mismatched}/{len(results)} relations "
        f"({matched} match, {mismatched} mismatch, {unassessable} CANNOT_ASSESS)"
    )
    return 1 if mismatched else 0


def self_test() -> int:
    """Prove the checker separates a correct relation from a wrong one."""
    exact = {
        "tolerance_percent": 5.0,
        "relations": [
            {
                "parameter": "CL",
                "unit": " L/h",
                "reference_value": 1.0,
                "reference_weight_kg": 1.0,
                "weight_kg": 16.0,
                "exponent": 0.5,
                "reported_value": 4.0,
                "locator": "self-test",
            }
        ],
    }
    if report(exact) != 0:
        print("SELF_TEST_ERROR: an exact relation was not reported as MATCH")
        return 1

    wrong = json.loads(json.dumps(exact))
    wrong["relations"][0]["reported_value"] = 8.0
    if report(wrong) != 1:
        print("SELF_TEST_ERROR: a 100% deviation was not reported as MISMATCH")
        return 1

    empty = {"tolerance_percent": 5.0, "relations": []}
    if report(empty) != 2:
        print("SELF_TEST_ERROR: an empty relation set did not report CANNOT_ASSESS")
        return 1

    incomplete = {"tolerance_percent": 5.0, "relations": [{"parameter": "CL"}]}
    if report(incomplete) != 0:
        print("SELF_TEST_ERROR: an incomplete relation should be CANNOT_ASSESS, not a mismatch")
        return 1

    print("self_test_canaries=4/4")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute allometric scaling relations")
    parser.add_argument("relations", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.relations is None:
        parser.error("a relations JSON file is required unless --self-test is given")
    return report(json.loads(args.relations.read_text(encoding="utf-8")))


if __name__ == "__main__":
    sys.exit(main())
