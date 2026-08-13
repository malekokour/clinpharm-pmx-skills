#!/usr/bin/env python3
"""Reconcile PK values within a report and against its source outputs.

Usage:
    python3 reconcile.py --left synopsis.txt --right nca_table.txt \
        [--tolerance 0.005] [--json]

Emits mechanical findings only. Both sides of every conflict are preserved with
their locators; the script never decides which value is correct.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cross_document_consistency as engine


def select_markdown_rows(text: str, pattern: str, label: str) -> str:
    """Return matching Markdown table rows with their header and separator.

    Whole committee packages commonly repeat a PK parameter across cohorts,
    summaries, and appendices. The shared engine correctly refuses to guess how
    those repeated values pair. This selector lets the caller name the exact
    row(s) represented by its locators while retaining the table header needed
    to identify each value's parameter.
    """
    try:
        matcher = re.compile(pattern)
    except re.error as exc:
        raise ValueError(f"{label} row regex is invalid: {exc}") from exc

    lines = text.splitlines()
    selected: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for index, line in enumerate(lines):
        if not matcher.search(line):
            continue
        if not line.lstrip().startswith("|"):
            raise ValueError(f"{label} row regex matched a non-table line")
        separator_index: int | None = None
        for candidate in range(index - 1, -1, -1):
            row = lines[candidate]
            if not row.lstrip().startswith("|"):
                break
            compact = row.replace("|", "").replace(" ", "")
            if compact and set(compact) <= {"-", ":"}:
                separator_index = candidate
                break
        if separator_index is None or separator_index == 0:
            raise ValueError(f"{label} row regex matched a row without a table header")
        block = (lines[separator_index - 1], lines[separator_index], line)
        if block not in seen:
            seen.add(block)
            selected.extend(block)
    if not selected:
        raise ValueError(f"{label} row regex matched 0 rows")
    return "\n".join(selected)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--left", required=True, help="document under review")
    ap.add_argument("--right", required=True, help="authoritative source")
    ap.add_argument("--left-name", default="CSR")
    ap.add_argument("--right-name", default="Source")
    ap.add_argument("--left-version", default="draft")
    ap.add_argument("--right-version", default="final")
    ap.add_argument("--left-locator", default="body")
    ap.add_argument("--right-locator", default="table")
    ap.add_argument(
        "--left-row-regex",
        help="regex selecting exact Markdown table row(s) from the left input",
    )
    ap.add_argument(
        "--right-row-regex",
        help="regex selecting exact Markdown table row(s) from the right input",
    )
    ap.add_argument("--tolerance", type=str, default="0.005",
                    help="relative tolerance; take this from the analysis plan, "
                         "not from this default")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    for p in (a.left, a.right):
        if not Path(p).is_file():
            print(f"CANNOT_ASSESS: input not found: {p}", file=sys.stderr)
            return 2

    if bool(a.left_row_regex) != bool(a.right_row_regex):
        print(
            "CANNOT_ASSESS: --left-row-regex and --right-row-regex must be supplied together",
            file=sys.stderr,
        )
        return 2

    reg = engine.Register()
    left_text = Path(a.left).read_text(encoding="utf-8", errors="replace")
    right_text = Path(a.right).read_text(encoding="utf-8", errors="replace")
    try:
        if a.left_row_regex:
            left_text = select_markdown_rows(left_text, a.left_row_regex, "left")
            right_text = select_markdown_rows(right_text, a.right_row_regex, "right")
    except ValueError as exc:
        print(f"CANNOT_ASSESS: {exc}", file=sys.stderr)
        return 2

    left = engine.extract(left_text,
                          a.left_name, a.left_version, a.left_locator)
    right = engine.extract(right_text,
                           a.right_name, a.right_version, a.right_locator)
    for v in left:
        reg.add(v)
    engine.reconcile(reg, left, right, relative_tolerance=Decimal(a.tolerance))

    summary = reg.summary()
    summary["left_values_extracted"] = len(left)
    summary["right_values_extracted"] = len(right)
    if reg.compared == 0:
        message = (
            "reconciliation is vacuous: 0 comparable pairs across "
            f"{len(left)} left and {len(right)} right extracted value(s); "
            f"{len(reg.ambiguous)} ambiguous key(s) were not compared"
        )
        if a.json:
            print(json.dumps({"status": "FAILED", "error": message,
                              "summary": summary, "findings": [],
                              "tolerance_applied": a.tolerance}, indent=2))
        else:
            print(f"FAILED: {message}")
            print("  Narrow repeated tables to explicitly located row pairs with "
                  "--left-row-regex and --right-row-regex.")
        return 1

    if a.json:
        print(json.dumps({"status": "COMPLETE", "summary": summary,
                          "findings": [d.as_dict() for d in reg.discrepancies],
                          "tolerance_applied": a.tolerance}, indent=2))
    else:
        print(f"Extracted {len(left)} left and {len(right)} right values; "
              f"{summary['comparisons']} comparisons; {summary['discrepancies']} discrepancies "
              f"(tolerance {a.tolerance})")
        for d in reg.discrepancies:
            r = d.as_dict()
            print(f"  [{r['severity']}] {r['rule']}")
            print(f"    as written: {r['statement_as_written']}  @ {r['statement_locator']}")
            print(f"    expected:   {r['expected_value_or_content']}  @ {r['expected_locator']}")
        if not reg.discrepancies:
            print("  no discrepancies beyond tolerance")
            print("  NOTE: this means the compared values agree. It does not mean "
                  "the document is correct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
