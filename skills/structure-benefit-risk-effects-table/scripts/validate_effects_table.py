#!/usr/bin/env python3
"""Validate the structure of a Markdown benefit-risk effects table.

Reports mechanical omissions only. It never interprets an effect, weighs benefit
against risk, or decides a clinical/safety conclusion.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_COLUMNS = (
    "Effect ID",
    "Domain",
    "Population / analysis set",
    "Endpoint / time point",
    "Comparator",
    "Effect as written",
    "Source / version",
    "Locator",
)
MISSING_MARKERS = {"", "NEEDS_INPUT", "UNKNOWN", "CANNOT_ASSESS"}


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def validate(path: Path) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_index = next((i for i, line in enumerate(lines) if line.startswith("|") and "Effect ID" in line), None)
    if header_index is None or header_index + 1 >= len(lines):
        return 0, ["table header with Effect ID was not found"]
    header = cells(lines[header_index])
    absent = [column for column in REQUIRED_COLUMNS if column not in header]
    if absent:
        return 0, [f"required column(s) absent: {', '.join(absent)}"]
    positions = {column: header.index(column) for column in REQUIRED_COLUMNS}
    findings: list[str] = []
    checked = 0
    for line_number, line in enumerate(lines[header_index + 2 :], header_index + 3):
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-", ":"}:
            continue
        row = cells(line)
        if len(row) != len(header):
            findings.append(f"line {line_number}: {len(row)} cells; expected {len(header)}")
            continue
        checked += 1
        for column, position in positions.items():
            if row[position] in MISSING_MARKERS:
                findings.append(f"line {line_number}: {column} is {row[position] or 'blank'}")
    return checked, findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Markdown effects table to check")
    args = parser.parse_args()
    if not args.input.is_file():
        print(f"CANNOT_ASSESS: input not found: {args.input}")
        return 2
    checked, findings = validate(args.input)
    if checked == 0 and findings:
        print(f"FAILED: table structure invalid — {findings[0]}")
        return 1
    print(f"Checked {checked} effect row(s); found {len(findings)} structural omission(s).")
    for finding in findings:
        print(f"- {finding}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
