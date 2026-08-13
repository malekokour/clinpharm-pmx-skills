#!/usr/bin/env python3
"""Check a dose-justification pack for the factors a justification is normally expected to address.

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
    ("exposure-response for efficacy", r"exposure[- ]response.{0,40}efficacy|\be-r\b.{0,20}efficacy"),
    ("exposure-response for safety", r"exposure[- ]response.{0,40}safety|\be-r\b.{0,20}safety"),
    ("intrinsic factors", r"intrinsic factor|\bage\b|body weight|\brenal\b|\bhepatic\b"),
    ("extrinsic factors", r"extrinsic factor|concomitant medication|\bfood\b"),
    ("dose proportionality", r"dose[- ]proportional"),
    ("accumulation", r"accumulat"),
    ("special populations", r"special population|paediatric|pediatric|elderly"),
    ("therapeutic window", r"therapeutic (?:window|index|margin)"),
]


def run(ns) -> Report:
    text = read(ns.pack).lower()
    report = Report(tool="factor_coverage")
    report.count("required factors", len(REQUIRED))

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
    report.count("factors present", present)

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


def exit_code(report: Report) -> int:
    """Fail closed when no coverage assessment could be made."""
    if report.unassessable:
        return 2
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pack", required=True, help="document text")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())
