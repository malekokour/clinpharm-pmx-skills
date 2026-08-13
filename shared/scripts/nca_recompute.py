#!/usr/bin/env python3
"""T-NCA — recompute NCA parameters and reconcile them against what was reported.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Mechanical checks only. This module recomputes a small, well-defined set of
non-compartmental parameters from a concentration-time profile and compares the
result to the value a report states. It never decides which is correct, never
selects a dose, and never issues a pharmacokinetic conclusion — a disagreement
is reported with both values and their locators for a qualified human.

Scope, stated plainly because the boundary is the point
-------------------------------------------------------
Recomputed here: AUC by the linear trapezoidal rule, AUC by linear-up/log-down,
Cmax and Tmax by inspection, and terminal half-life from a supplied lambda-z.

**Not** recomputed here: lambda-z itself. Choosing the terminal points for the
regression is a judgement about where the terminal phase begins, and a script
that guessed at it would be manufacturing exactly the kind of scientific
decision this product refuses to make. When lambda-z is supplied the half-life
relation is checked; when it is absent that is recorded as not assessable, with
what would make it assessable — never passed over in silence.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from itertools import pairwise
from math import log
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from findings import Finding, Report

#: Recomputation is floating point against a reported value that has been
#: rounded for presentation. This is the default agreement band, and it is a
#: *presentation* tolerance, not a scientific one — take the real number from
#: the analysis plan.
DEFAULT_TOLERANCE = Decimal("0.02")


@dataclass(frozen=True)
class Point:
    time: Decimal
    concentration: Decimal


def parse_profile(text: str) -> tuple[list[Point], list[str]]:
    """Parse `time<sep>concentration` rows. Returns points and rejected lines.

    Rejected lines are returned rather than skipped, because a parser that
    quietly drops rows changes the denominator of everything computed from
    them.
    """
    points: list[Point] = []
    rejected: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p for p in line.replace(",", " ").replace("\t", " ").split(" ") if p]
        if len(parts) < 2:
            rejected.append(raw)
            continue
        try:
            points.append(Point(Decimal(parts[0]), Decimal(parts[1])))
        except InvalidOperation:
            rejected.append(raw)
    return sorted(points, key=lambda p: p.time), rejected


def auc_linear(points: list[Point]) -> Decimal:
    """AUC by the linear trapezoidal rule."""
    total = Decimal(0)
    for first, second in pairwise(points):
        total += (second.time - first.time) * (first.concentration + second.concentration) / 2
    return total


def auc_linear_up_log_down(points: list[Point]) -> Decimal:
    """AUC by linear-up / log-down, the convention most plans declare.

    Falls back to the trapezoid across any interval where the logarithmic form
    is undefined (a zero or rising concentration), because the alternative —
    dropping the interval — would silently shrink the area.
    """
    total = Decimal(0)
    for first, second in pairwise(points):
        width = second.time - first.time
        c1, c2 = first.concentration, second.concentration
        if c2 < c1 and c1 > 0 and c2 > 0:
            ratio = Decimal(str(log(float(c1 / c2))))
            total += width * (c1 - c2) / ratio
        else:
            total += width * (c1 + c2) / 2
    return total


def half_life(lambda_z: Decimal) -> Decimal:
    return Decimal(str(log(2))) / lambda_z


def _disagrees(observed: Decimal, expected: Decimal, tolerance: Decimal) -> bool:
    if expected == 0:
        return observed != 0
    return abs((observed - expected) / expected) > tolerance


def check(
    points: list[Point],
    reported: dict[str, Decimal],
    rejected: list[str],
    lambda_z: Decimal | None = None,
    tolerance: Decimal = DEFAULT_TOLERANCE,
    locator: str = "NCA output",
) -> Report:
    report = Report(tool="nca-recompute")
    report.count("profile_points", len(points))
    report.count("reported_parameters", len(reported))
    report.count("unparsed_rows", len(rejected))

    for raw in rejected:
        report.cannot_assess(
            item=f"row {raw!r}",
            why="not a `time concentration` pair",
            resolved_by="supply the row as two numeric columns",
        )

    if len(points) < 2:
        report.cannot_assess(
            item="every recomputed parameter",
            why=f"a profile needs at least two points; {len(points)} supplied",
            resolved_by="supply the full concentration-time profile",
        )
        return report

    computed: dict[str, Decimal] = {
        "auc_linear": auc_linear(points),
        "auc_linear_up_log_down": auc_linear_up_log_down(points),
        "cmax": max(p.concentration for p in points),
    }
    peak = max(points, key=lambda p: p.concentration)
    computed["tmax"] = peak.time

    if lambda_z is not None and lambda_z > 0:
        computed["half_life"] = half_life(lambda_z)
    else:
        report.cannot_assess(
            item="half_life",
            why="lambda-z was not supplied, and selecting terminal points is a "
            "scientific judgement this script will not make",
            resolved_by="supply --lambda-z from the analysis, or state that no "
            "terminal phase was estimable",
        )

    for name, stated in reported.items():
        if name not in computed:
            report.cannot_assess(
                item=name,
                why="this parameter is not recomputed by this tool",
                resolved_by="check it by hand or against the analysis output",
            )
            continue
        recomputed = computed[name]
        if _disagrees(recomputed, stated, tolerance):
            severity = "Critical" if name.startswith("auc") or name == "cmax" else "Major"
            report.add(
                Finding(
                    rule="recomputation-mismatch",
                    severity=severity,
                    item=name,
                    observed=f"{stated}",
                    expected=f"{recomputed:.6g} (recomputed)",
                    locator=locator,
                    detail=(
                        f"reported {name} differs from the value recomputed from the "
                        f"supplied profile by more than the {tolerance} relative "
                        "tolerance. Both values are preserved; this tool does not "
                        "determine which is correct."
                    ),
                )
            )

    if "tmax" in reported and reported["tmax"] not in {p.time for p in points}:
        report.add(
            Finding(
                rule="value-not-in-profile",
                severity="Major",
                item="tmax",
                observed=f"{reported['tmax']}",
                expected="one of the sampled times",
                locator=locator,
                detail=(
                    "the reported Tmax is not a time present in the supplied "
                    "profile, so it cannot have come from these data"
                ),
            )
        )
    return report
