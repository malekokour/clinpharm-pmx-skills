#!/usr/bin/env python3
"""Check a protocol's PK sections for objective-endpoint-parameter chains that do not close.

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

SECTIONS = {
    "objectives": r"\bobjectiv",
    "endpoints": r"\bendpoint|\boutcome measure",
    "sampling": r"\bsampl",
    "analysis population": r"\banalysis (?:set|population)",
    "bioanalytical method": r"\bassay|\bbioanalytical|\bLC-MS",
    "missing data handling": r"\bmissing\b|\bBLQ\b|below (?:the )?limit",
}
UNITS = re.compile(r"\b(ng/mL|ug/mL|µg/mL|mg/L|ng·h/mL|ng\*h/mL|h|L/h|L)\b")


def run(ns) -> Report:
    text = read(ns.protocol)
    low = text.lower()
    report = Report(tool="check_conformance")

    report.count("required sections", len(SECTIONS))
    present = 0
    for name, pattern in SECTIONS.items():
        if re.search(pattern, low):
            present += 1
        else:
            report.add(Finding(
                rule="required-section-absent",
                severity="Major",
                item=name,
                observed="not found",
                expected="a section addressing this item",
                locator="whole document",
                detail="Absence is reported as absence. It is not inferred to be covered elsewhere.",
            ))
    report.count("sections present", present)

    # An objective without an endpoint is a chain that does not close.
    n_obj = len(re.findall(r"\bobjectiv", low))
    n_end = len(re.findall(r"\bendpoint", low))
    report.count("objective mentions", n_obj)
    report.count("endpoint mentions", n_end)
    if n_obj and not n_end:
        report.add(Finding(
            rule="objective-without-endpoint",
            severity="Critical",
            item="PK objectives",
            observed=f"{n_obj} objective mention(s), 0 endpoint mentions",
            expected="every stated objective has a matching endpoint",
            locator="objectives section",
            detail="An objective with no endpoint cannot be assessed by the study as written.",
        ))

    units = set(UNITS.findall(text))
    report.count("distinct units used", len(units))
    if {"ng/mL", "mg/L"} <= units:
        report.add(Finding(
            rule="mixed-equivalent-units",
            severity="Minor",
            item="concentration units",
            observed="both ng/mL and mg/L appear",
            expected="one convention throughout, or an explicit conversion",
            locator="whole document",
            detail="These are numerically equal but differently scaled in reported tables; "
                   "mixing them is a common source of downstream transcription error.",
        ))
    if not units:
        report.cannot_assess(
            "unit consistency",
            "no recognised concentration or PK units were found",
            "a document stating parameter units",
        )
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
