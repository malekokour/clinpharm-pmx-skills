#!/usr/bin/env python3
"""Check a clinical pharmacology development plan for the study types a programme is normally expected to address.

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

REQUIRED = [
    ("single ascending dose", r"single[- ]ascending|\bsad\b"),
    ("multiple ascending dose", r"multiple[- ]ascending|\bmad\b"),
    ("food effect", r"food[- ]effect|fed[/ ]fasted"),
    # Accept the three deliberate prose separators only. The synthetic plan uses
    # an en dash; allowing arbitrary punctuation would weaken this into a fuzzy
    # match and could hide a genuinely absent interaction section.
    ("drug-drug interaction", r"drug(?:-|–| )drug interaction|\bddi\b"),
    ("renal impairment", r"renal impairment"),
    ("hepatic impairment", r"hepatic impairment"),
    ("QT assessment", r"\bqt\b|thorough qt|cardiac repolarisation"),
    ("mass balance / ADME", r"mass balance|\badme\b|human radiolabel"),
    ("population PK", r"population pk|\bpoppk\b|nonlinear mixed"),
    ("exposure-response", r"exposure[- ]response|\be-r\b"),
]


def run(ns) -> Report:
    text = read(ns.plan).lower()
    report = Report(tool="assess_coverage")
    report.count("required study types", len(REQUIRED))

    present = 0
    for name, pattern in REQUIRED:
        if re.search(pattern, text):
            present += 1
        else:
            report.add(Finding(
                rule="required-element-absent",
                severity="Major",
                item=name,
                observed="not found",
                expected="an explicit statement addressing this item",
                locator="whole document",
                detail="Absence is reported as absence. A missing element is not assumed "
                       "to be covered elsewhere or intentionally omitted.",
            ))
    report.count("study types present", present)

    if present == 0:
        report.cannot_assess(
            "coverage assessment",
            "none of the expected elements were found, which usually means the wrong "
            "document was supplied",
            "the document this checker targets",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--plan", required=True, help="document text")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
