#!/usr/bin/env python3
"""Recompute stated exposure safety margins from the exposures they cite.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Usage:
    python3 margin_check.py margins.json
    python3 margin_check.py --self-test

What it checks
--------------
One relation: ``margin = nonclinical_exposure / clinical_exposure``, recomputed
and compared against the stated value within a tolerance.

It refuses to compute when the two sides are not comparable:

* different exposure metrics (nonclinical AUC against clinical Cmax)
* different binding bases (total against unbound)
* different units

Those are reported as findings in their own right, not as mismatches, because a
ratio between incomparable quantities has no correct value to deviate from.

Why the refusals matter more than the arithmetic
------------------------------------------------
Dividing two numbers is trivial. The failure this exists for is a margin whose
two sides answer different questions — and a script that divided them anyway
would launder that defect into a confident number. So incomparability is checked
first and short-circuits the division.

Input shape
-----------
    {
      "tolerance_percent": 5.0,
      "margins": [
        {"label": "hepatic NOAEL margin", "stated_margin": 12.0,
         "nonclinical": {"value": 4800, "unit": "ng*h/mL", "metric": "AUC",
                          "basis": "total", "species": "rat"},
         "clinical":    {"value": 400,  "unit": "ng*h/mL", "metric": "AUC",
                          "basis": "total", "dose_level": "100 mg"},
         "locator": "IB 5.3"}
      ]
    }
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

COMPARABLE_KEYS = ("metric", "basis", "unit")


def evaluate(margin: dict, tolerance_percent: float) -> dict:
    label = margin.get("label", "<unlabelled>")
    nonclinical = margin.get("nonclinical") or {}
    clinical = margin.get("clinical") or {}
    locator = margin.get("locator", "")

    for side, payload in (("nonclinical", nonclinical), ("clinical", clinical)):
        if payload.get("value") is None:
            return {"label": label, "state": "CANNOT_ASSESS", "locator": locator,
                    "detail": f"{side} exposure value absent"}

    mismatches = [
        key for key in COMPARABLE_KEYS
        if nonclinical.get(key) is not None
        and clinical.get(key) is not None
        and nonclinical[key] != clinical[key]
    ]
    if mismatches:
        detail = "; ".join(
            f"{key}: nonclinical={nonclinical[key]!r} clinical={clinical[key]!r}"
            for key in mismatches
        )
        return {"label": label, "state": "INCOMPARABLE", "locator": locator,
                "detail": detail}

    missing = [k for k in COMPARABLE_KEYS
               if nonclinical.get(k) is None or clinical.get(k) is None]
    if missing:
        return {"label": label, "state": "CANNOT_ASSESS", "locator": locator,
                "detail": f"basis not fully stated: {', '.join(sorted(missing))}"}

    try:
        numerator = float(nonclinical["value"])
        denominator = float(clinical["value"])
        stated = float(margin["stated_margin"])
    except (KeyError, TypeError, ValueError) as exc:
        return {"label": label, "state": "CANNOT_ASSESS", "locator": locator,
                "detail": f"non-numeric value: {exc}"}

    if denominator == 0:
        return {"label": label, "state": "CANNOT_ASSESS", "locator": locator,
                "detail": "clinical exposure is zero"}

    recomputed = numerator / denominator
    deviation = abs(stated - recomputed) / abs(recomputed) * 100.0 if recomputed else float("inf")
    return {"label": label, "locator": locator, "stated": stated,
            "recomputed": recomputed, "deviation_percent": deviation,
            "state": "MATCH" if deviation <= tolerance_percent else "MISMATCH"}


def report(document: dict) -> int:
    tolerance = float(document.get("tolerance_percent", 5.0))
    margins = document.get("margins") or []
    if not margins:
        print("CANNOT_ASSESS: 0 margins supplied — nothing was checked")
        print("checked 0/0 margins")
        return 2

    results = [evaluate(m, tolerance) for m in margins]
    for r in results:
        if r["state"] in {"CANNOT_ASSESS", "INCOMPARABLE"}:
            print(f"{r['state']} {r['label']}: {r['detail']} locator={r['locator'] or '-'}")
        else:
            print(f"{r['state']} {r['label']} stated={r['stated']:g}-fold "
                  f"recomputed={r['recomputed']:.4g}-fold "
                  f"deviation={r['deviation_percent']:.1f}% tolerance={tolerance:g}% "
                  f"locator={r['locator'] or '-'}")

    matched = sum(1 for r in results if r["state"] == "MATCH")
    mismatched = sum(1 for r in results if r["state"] == "MISMATCH")
    incomparable = sum(1 for r in results if r["state"] == "INCOMPARABLE")
    unassessable = sum(1 for r in results if r["state"] == "CANNOT_ASSESS")
    print(f"checked {matched + mismatched}/{len(results)} margins "
          f"({matched} match, {mismatched} mismatch, {incomparable} incomparable, "
          f"{unassessable} CANNOT_ASSESS)")
    return 1 if (mismatched or incomparable) else 0


def self_test() -> int:
    exact = {"tolerance_percent": 5.0, "margins": [{
        "label": "exact", "stated_margin": 12.0,
        "nonclinical": {"value": 4800, "unit": "ng*h/mL", "metric": "AUC", "basis": "total"},
        "clinical": {"value": 400, "unit": "ng*h/mL", "metric": "AUC", "basis": "total"},
        "locator": "self-test"}]}
    if report(exact) != 0:
        print("SELF_TEST_ERROR: an exact margin was not MATCH"); return 1

    wrong = json.loads(json.dumps(exact)); wrong["margins"][0]["stated_margin"] = 30.0
    if report(wrong) != 1:
        print("SELF_TEST_ERROR: a wrong stated margin was not MISMATCH"); return 1

    metric = json.loads(json.dumps(exact)); metric["margins"][0]["clinical"]["metric"] = "Cmax"
    out = report(metric)
    if out != 1:
        print("SELF_TEST_ERROR: an AUC-vs-Cmax margin was not caught"); return 1

    binding = json.loads(json.dumps(exact)); binding["margins"][0]["clinical"]["basis"] = "unbound"
    if report(binding) != 1:
        print("SELF_TEST_ERROR: a total-vs-unbound margin was not caught"); return 1

    if report({"margins": []}) != 2:
        print("SELF_TEST_ERROR: an empty set did not report CANNOT_ASSESS"); return 1

    print("self_test_canaries=5/5")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute exposure safety margins")
    parser.add_argument("margins", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.margins is None:
        parser.error("a margins JSON file is required unless --self-test is given")
    return report(json.loads(args.margins.read_text(encoding="utf-8")))


if __name__ == "__main__":
    sys.exit(main())
