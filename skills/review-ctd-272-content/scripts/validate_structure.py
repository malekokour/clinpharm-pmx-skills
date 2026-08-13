#!/usr/bin/env python3
"""Check a CTD 2.7.2 document for expected subsections, resolvable cross-references, and cited tables.

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

EXPECTED = {
    "2.7.2.1": "Background and overview",
    "2.7.2.2": "Summary of results of individual studies",
    "2.7.2.3": "Comparison and analyses of results across studies",
    "2.7.2.4": "Special studies",
}
XREF = re.compile(r"(?:see|refer to|per)\s+(?:Section\s+)?(\d+(?:\.\d+){1,3})", re.IGNORECASE)
HEADING = re.compile(r"^\s*#*\s*(\d+(?:\.\d+){1,3})", re.MULTILINE)
TABLE_DEF = re.compile(r"^\s*#*\s*Table\s+(\d+)", re.IGNORECASE | re.MULTILINE)
TABLE_CITE = re.compile(r"\bTable\s+(\d+)", re.IGNORECASE)


def run(ns) -> Report:
    text = read(ns.document)
    report = Report(tool="validate_structure")

    headings = set(HEADING.findall(text))
    report.count("expected subsections", len(EXPECTED))
    report.count("headings found", len(headings))

    present = 0
    for num, title in EXPECTED.items():
        if num in headings or num in text:
            present += 1
        else:
            report.add(Finding(
                rule="expected-subsection-absent",
                severity="Major",
                item=f"{num} {title}",
                observed="not found",
                expected=f"a subsection numbered {num}",
                locator="whole document",
                detail="Searched for the number as a heading and as literal text.",
            ))
    report.count("expected subsections present", present)

    refs = set(XREF.findall(text))
    report.count("cross-references", len(refs))
    unresolved = sorted(r for r in refs if r not in headings and r not in EXPECTED)
    for r in unresolved:
        report.add(Finding(
            rule="cross-reference-unresolved",
            severity="Major",
            item=f"Section {r}",
            observed="referenced but no matching heading found",
            expected=f"a heading numbered {r}",
            locator="cross-reference",
            detail="A reader following this pointer lands nowhere.",
        ))

    defined = set(TABLE_DEF.findall(text))
    cited = set(TABLE_CITE.findall(text)) - defined
    report.count("tables defined", len(defined))
    for t in sorted(cited):
        report.add(Finding(
            rule="table-cited-not-defined",
            severity="Minor",
            item=f"Table {t}",
            observed="cited in text, no matching table heading",
            expected=f"a heading for Table {t}",
            locator="body text",
            detail="Either the table is missing or its heading is not in the expected form.",
        ))
    if not headings:
        report.cannot_assess(
            "document structure",
            "no numbered headings were found",
            "a document with numbered section headings",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--document", required=True, help="CTD 2.7.2 text")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
