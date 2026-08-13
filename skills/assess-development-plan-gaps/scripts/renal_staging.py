#!/usr/bin/env python3
"""VENDORED at build time from shared/scripts/ — do not edit here.
Edit the canonical source and rebuild; a freshness check compares them.

T02 — eGFR renal-function staging checker.

Categories per the FDA March 2024 renal-impairment guidance (`fda-renal`).
Classification only: the tool states the category an eGFR falls in. It never
recommends a dose.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

#: (lower_inclusive, upper_inclusive, label)
BANDS = [
    (90.0, float("inf"), "Normal or high"),
    (60.0, 89.999999, "Mild impairment"),
    (30.0, 59.999999, "Moderate impairment"),
    (15.0, 29.999999, "Severe impairment"),
    (0.0, 14.999999, "Kidney failure"),
]


def stage(egfr: float) -> str:
    if egfr < 0:
        raise ValueError("eGFR cannot be negative")
    for low, high, label in BANDS:
        if low <= egfr <= high:
            return label
    raise ValueError(f"eGFR {egfr} did not match any band")


def check_reported_stage(egfr: float, reported: str, locator: str) -> dict[str, str] | None:
    """Return a mechanical finding when a reported category contradicts its eGFR."""
    computed = stage(egfr)
    if computed.lower().split()[0] == reported.strip().lower().split()[0]:
        return None
    return {
        "rule": "renal-stage-mismatch", "severity": "Major", "kind": "mechanical",
        "observed": f"{reported} (eGFR {egfr})", "expected": computed, "locator": locator,
        "detail": ("Reported renal category does not match the category its eGFR falls in "
                   "under the FDA March 2024 bands. Which is correct is a reviewer decision."),
    }
