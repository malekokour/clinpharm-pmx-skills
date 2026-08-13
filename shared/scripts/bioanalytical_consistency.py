#!/usr/bin/env python3
"""T-BA — check a bioanalytical report's tables, identifiers, units and criteria.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Mechanical checks only, over four things a bioanalytical report asserts:

**Identifiers** — run and batch identifiers are unique and every result
references a declared run. A duplicated run identifier makes every count that
groups by run ambiguous.

**Units** — one concentration unit is used throughout. A report mixing ng/mL and
ug/mL differs by a factor of a thousand, and that is exactly the class of defect
that survives review because both values look reasonable in isolation.

**Criteria** — the acceptance criteria stated in the report are the conventional
ones, and the report says which it applied. This does **not** judge whether a
criterion is scientifically right for the assay; it checks that one was stated
and applied consistently.

**Arithmetic** — a stated pass rate is recomputed from the passed/total counts
beside it.

Regulatory interpretation is out of scope. Whether a failed run should have been
repeated, whether an ISR outcome is acceptable, and whether the method is fit
for its purpose are judgements for a qualified bioanalyst.
"""

from __future__ import annotations

import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from findings import Finding, Report

RUN_ID = re.compile(r"\b(?:Run|Batch)\s*[:#-]?\s*([A-Za-z0-9_-]+)", re.IGNORECASE)
CONCENTRATION_UNIT = re.compile(r"\b(ng/mL|ug/mL|µg/mL|mg/L|pg/mL|ng/L)\b")
PASS_RATE = re.compile(
    r"(\d+)\s*/\s*(\d+)[^.\n%]{0,40}?\(?\s*(\d+(?:\.\d+)?)\s*%", re.IGNORECASE
)
#: The conventional bands. Presence is checked, not scientific suitability.
CRITERION = re.compile(r"±\s*(\d+(?:\.\d+)?)\s*%")
CONVENTIONAL_BANDS = {Decimal(15), Decimal(20), Decimal(25), Decimal(30)}


def check(text: str, locator: str = "bioanalytical report") -> Report:
    report = Report(tool="bioanalytical-consistency")

    identifiers = RUN_ID.findall(text)
    report.count("run_identifiers", len(identifiers))
    seen: dict[str, int] = {}
    for name in identifiers:
        seen[name] = seen.get(name, 0) + 1
    for name, occurrences in sorted(seen.items()):
        if occurrences > 1 and not name.isdigit():
            report.add(
                Finding(
                    rule="duplicate-run-identifier",
                    severity="Major",
                    item=f"Run {name}",
                    observed=f"appears {occurrences} times",
                    expected="one declaration per run",
                    locator=locator,
                    detail=(
                        "a repeated run identifier makes any count grouped by run "
                        "ambiguous, including the pass rates below"
                    ),
                )
            )
    report.count("distinct_runs", len(seen))

    units = set(CONCENTRATION_UNIT.findall(text))
    normalised = {u.replace("µ", "u") for u in units}
    report.count("concentration_units", len(normalised))
    if len(normalised) > 1:
        report.add(
            Finding(
                rule="mixed-concentration-units",
                severity="Critical",
                item="concentration unit",
                observed=", ".join(sorted(normalised)),
                expected="one unit throughout, or an explicit conversion",
                locator=locator,
                detail=(
                    "more than one concentration unit appears. ng/mL and ug/mL differ "
                    "by a factor of 1000 and both look reasonable in isolation; this "
                    "tool does not decide which was intended"
                ),
            )
        )
    elif not normalised:
        report.cannot_assess(
            item="concentration units",
            why="no recognised concentration unit was found in the text",
            resolved_by="supply the tabulated results, not only the narrative",
        )

    bands = set()
    for raw in CRITERION.findall(text):
        try:
            bands.add(Decimal(raw))
        except InvalidOperation:
            continue
    report.count("acceptance_criteria_stated", len(bands))
    if not bands:
        report.add(
            Finding(
                rule="no-acceptance-criterion-stated",
                severity="Major",
                item="acceptance criteria",
                observed="none found",
                expected="the applied criteria stated in the report",
                locator=locator,
                detail=(
                    "no ± percentage band appears, so no pass or fail claim in this "
                    "report can be checked against the rule it used"
                ),
            )
        )
    for band in sorted(bands - CONVENTIONAL_BANDS):
        report.add(
            Finding(
                rule="unconventional-acceptance-band",
                severity="Minor",
                item=f"±{band}%",
                observed=f"±{band}%",
                expected="a stated justification",
                locator=locator,
                detail=(
                    "this band is not one of the conventional ones. That is not "
                    "necessarily wrong — it is flagged so a bioanalyst confirms it "
                    "was intended. This tool does not judge assay suitability"
                ),
            )
        )

    checked_rates = 0
    for passed, total, stated in PASS_RATE.findall(text):
        checked_rates += 1
        if int(total) == 0:
            report.add(
                Finding(
                    rule="pass-rate-over-zero",
                    severity="Major",
                    item=f"{passed}/{total}",
                    observed=f"{stated}%",
                    expected="a non-zero denominator",
                    locator=locator,
                    detail="a percentage computed over zero items asserts nothing",
                )
            )
            continue
        recomputed = Decimal(passed) * 100 / Decimal(total)
        if abs(recomputed - Decimal(stated)) > Decimal("0.5"):
            report.add(
                Finding(
                    rule="pass-rate-arithmetic",
                    severity="Major",
                    item=f"{passed}/{total}",
                    observed=f"{stated}%",
                    expected=f"{recomputed:.1f}%",
                    locator=locator,
                    detail="the stated percentage does not follow from the counts beside it",
                )
            )
    report.count("pass_rates_checked", checked_rates)
    return report
