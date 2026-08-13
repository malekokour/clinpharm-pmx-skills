#!/usr/bin/env python3
"""Check that a stated PK sampling schedule can support the parameters the protocol claims to estimate.

Emits mechanical findings only. Both sides of every conflict are preserved with
their locators; this script never decides which is correct.

Author: Malek Okour
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findings import Finding, Report

# A schedule is normally written as a comma-separated list carrying one trailing
# unit — "0, 0.5, 1, 2, 4, 8 h post-dose". Requiring a unit on every number finds
# only the last, which silently understates the schedule and produced a
# confidently wrong "0 samples in the first 4 h" on the first real fixture.
TIME_LIST = re.compile(
    r"(?P<list>\d+(?:\.\d+)?(?:\s*,\s*\d+(?:\.\d+)?)*)\s*(?P<unit>h|hr|hours?|min|minutes?|d|days?)\b",
    re.IGNORECASE,
)
HALFLIFE = re.compile(
    r"(?:terminal\s+)?half[- ]life[^.\n]{0,60}?(\d+(?:\.\d+)?)\s*(h|hr|hours?|d|days?)", re.IGNORECASE
)
# Lines describing a half-life, duration or window are not sampling schedules.
NOT_A_SCHEDULE = re.compile(r"half[- ]life|duration|washout|window|expected to be", re.IGNORECASE)
PARAMS = {
    "auc0-inf": "AUC extrapolated to infinity",
    "auc0-∞": "AUC extrapolated to infinity",
    "t1/2": "terminal half-life",
    "half-life": "terminal half-life",
    "cmax": "maximum concentration",
    "tmax": "time to maximum concentration",
    "cl/f": "apparent clearance",
    "vz/f": "apparent volume of distribution",
}


def to_hours(value: float, unit: str) -> float:
    u = unit.lower()
    if u.startswith("min"):
        return value / 60.0
    if u.startswith("d"):
        return value * 24.0
    return value


def extract_times(text: str) -> set[float]:
    """Sampling times in hours, from lines that describe a schedule.

    Lines about half-life, washout or duration are skipped: their numbers are
    parameters of the drug, not times at which blood is drawn, and counting them
    as samples makes the schedule look longer than it is.
    """
    out: set[float] = set()
    for line in text.splitlines():
        if NOT_A_SCHEDULE.search(line):
            continue
        for m in TIME_LIST.finditer(line):
            unit = m.group("unit")
            for value in m.group("list").split(","):
                out.add(to_hours(float(value.strip()), unit))
    return out


def run(ns) -> Report:
    text = read(ns.protocol)
    report = Report(tool="check_sampling")

    times = sorted(extract_times(text))
    claimed = sorted({label for key, label in PARAMS.items() if key in text.lower()})

    report.count("sampling times found", len(times))
    report.count("parameters claimed", len(claimed))

    if not times:
        report.cannot_assess(
            "sampling schedule",
            "no sampling times could be extracted from the text",
            "a schedule stating nominal times with units",
        )
        return report
    if not claimed:
        report.cannot_assess(
            "PK parameters",
            "no named PK parameters were found",
            "an endpoints section naming the parameters to be estimated",
        )
        return report

    last = max(times)

    # A terminal half-life cannot be estimated without samples in the terminal
    # phase. Three half-lives past Tmax is the conventional minimum; this is an
    # arithmetic check against the protocol's own stated half-life, not a
    # judgement about the study.
    hl = HALFLIFE.search(text)
    if hl and any("half-life" in c for c in claimed):
        hours = to_hours(float(hl.group(1)), hl.group(2))
        need = 3 * hours
        if last < need:
            report.add(Finding(
                rule="schedule-cannot-support-parameter",
                severity="Critical",
                item="terminal half-life",
                observed=f"last sample {last:g} h",
                expected=f"at least {need:g} h (3 x stated t1/2 of {hours:g} h)",
                locator="sampling schedule",
                detail="The schedule ends before the terminal phase the protocol itself describes, "
                       "so the stated half-life cannot be estimated from these samples.",
            ))
    elif any("half-life" in c for c in claimed):
        report.cannot_assess(
            "terminal half-life adequacy",
            "the protocol claims a terminal half-life but states no expected value",
            "an expected half-life, from prior data or the investigator brochure",
        )

    # AUC0-inf requires the same terminal coverage.
    if any("infinity" in c for c in claimed) and len(times) < 3:
        report.add(Finding(
            rule="schedule-cannot-support-parameter",
            severity="Major",
            item="AUC extrapolated to infinity",
            observed=f"{len(times)} sampling time(s)",
            expected="enough terminal-phase samples to estimate a slope",
            locator="sampling schedule",
            detail="Extrapolation to infinity needs a terminal slope, which needs at least "
                   "three points in the terminal phase.",
        ))

    # A Cmax claim needs samples dense enough around the expected peak.
    if any("maximum concentration" in c for c in claimed):
        early = [t for t in times if t <= 4]
        if len(early) < 3:
            report.add(Finding(
                rule="sparse-early-sampling",
                severity="Major",
                item="maximum concentration",
                observed=f"{len(early)} sample(s) in the first 4 h",
                expected="at least 3 samples bracketing the expected peak",
                locator="sampling schedule",
                detail="With this spacing the observed maximum may not be near the true peak.",
            ))
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--protocol", required=True, help="protocol text")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
