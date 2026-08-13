#!/usr/bin/env python3
"""T06 — CTD Module 5 placement validator.

Placement is decided by a study's PRIMARY objective, per ICH M4E(R2)
granularity rules (`ich-m4e-r2`). A study with a secondary PK objective does not
move on that basis.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

PLACEMENT = {
    "biopharmaceutic": "5.3.1", "bioavailability": "5.3.1", "bioequivalence": "5.3.1",
    "in vitro in vivo correlation": "5.3.1",
    "pk biomaterial": "5.3.2", "plasma protein binding": "5.3.2", "hepatic metabolism": "5.3.2",
    "healthy volunteer pk": "5.3.3.1", "patient pk": "5.3.3.2",
    "intrinsic factor": "5.3.3.3", "renal impairment": "5.3.3.3", "hepatic impairment": "5.3.3.3",
    "extrinsic factor": "5.3.3.4", "drug interaction": "5.3.3.4", "food effect": "5.3.3.4",
    "population pk": "5.3.3.5",
    "healthy volunteer pd": "5.3.4.1", "patient pd": "5.3.4.2",
    "efficacy controlled": "5.3.5.1", "uncontrolled": "5.3.5.2",
}


def expected_section(primary_objective: str) -> str | None:
    key = primary_objective.strip().lower()
    if key in PLACEMENT:
        return PLACEMENT[key]
    for k, v in PLACEMENT.items():
        if k in key:
            return v
    return None


def check(study: str, primary_objective: str, placed_in: str) -> dict[str, str] | None:
    expected = expected_section(primary_objective)
    if expected is None:
        return {"rule": "placement-undetermined", "severity": "Minor", "kind": "mechanical",
                "observed": placed_in, "expected": "UNKNOWN", "locator": study,
                "detail": ("Primary objective did not map to a known placement rule. "
                           "Emitting UNKNOWN rather than guessing.")}
    if not placed_in.strip().startswith(expected):
        return {"rule": "ctd-placement-mismatch", "severity": "Major", "kind": "mechanical",
                "observed": placed_in, "expected": expected, "locator": study,
                "detail": (f"Primary objective '{primary_objective}' places this study in "
                           f"{expected} under M4E(R2) granularity rules.")}
    return None
