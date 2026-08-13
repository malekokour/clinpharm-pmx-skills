#!/usr/bin/env python3
"""Compare two Markdown reference-safety lists by term membership.

Expected input rows are ``| Term | Category | Source locator |``. The utility
reports only list/string membership differences. It never determines whether a
term is clinically equivalent, whether a local change is required, or which list
is authoritative.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
from pathlib import Path


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_terms(path: Path) -> tuple[dict[str, tuple[str, str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_index = next((i for i, line in enumerate(lines) if line.startswith("|") and "Term" in line), None)
    if header_index is None or header_index + 1 >= len(lines):
        return {}, ["table header with Term was not found"]
    header = cells(lines[header_index])
    required = ("Term", "Category", "Source locator")
    missing = [column for column in required if column not in header]
    if missing:
        return {}, [f"required column(s) absent: {', '.join(missing)}"]
    positions = {column: header.index(column) for column in required}
    terms: dict[str, tuple[str, str]] = {}
    problems: list[str] = []
    for line_number, line in enumerate(lines[header_index + 2 :], header_index + 3):
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-", ":"}:
            continue
        row = cells(line)
        if len(row) != len(header):
            problems.append(f"line {line_number}: {len(row)} cells; expected {len(header)}")
            continue
        term, category, locator = (row[positions[column]] for column in required)
        if not term or not category or not locator:
            problems.append(f"line {line_number}: Term, Category, and Source locator are required")
            continue
        key = term.casefold()
        if key in terms:
            problems.append(f"line {line_number}: duplicate term {term!r}")
            continue
        terms[key] = (term, f"{category}; {locator}")
    return terms, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", required=True, type=Path, help="first reference-safety list")
    parser.add_argument("--right", required=True, type=Path, help="second reference-safety list")
    parser.add_argument("--left-name", default="left list")
    parser.add_argument("--right-name", default="right list")
    args = parser.parse_args()
    if not args.left.is_file() or not args.right.is_file():
        print("CANNOT_ASSESS: both --left and --right files are required")
        return 2
    left, left_problems = load_terms(args.left)
    right, right_problems = load_terms(args.right)
    if left_problems or right_problems:
        print("FAILED: list structure invalid")
        for problem in [*left_problems, *right_problems]:
            print(f"- {problem}")
        return 1
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    compared = len(set(left) & set(right))
    print(f"Compared {compared} shared term(s) across {len(left)} and {len(right)} supplied term(s).")
    for key in only_left:
        term, locator = left[key]
        print(f"- present only in {args.left_name}: {term} @ {locator}")
    for key in only_right:
        term, locator = right[key]
        print(f"- present only in {args.right_name}: {term} @ {locator}")
    print(f"Mechanical list differences: {len(only_left) + len(only_right)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
