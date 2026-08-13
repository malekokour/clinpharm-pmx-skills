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
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cross_document_consistency as engine


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
    ap.add_argument("--tolerance", type=str, default="0.005",
                    help="relative tolerance; take this from the analysis plan, "
                         "not from this default")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    for p in (a.left, a.right):
        if not Path(p).is_file():
            print(f"CANNOT_ASSESS: input not found: {p}", file=sys.stderr)
            return 2

    reg = engine.Register()
    left = engine.extract(Path(a.left).read_text(encoding="utf-8", errors="replace"),
                          a.left_name, a.left_version, a.left_locator)
    right = engine.extract(Path(a.right).read_text(encoding="utf-8", errors="replace"),
                           a.right_name, a.right_version, a.right_locator)
    for v in left:
        reg.add(v)
    engine.reconcile(reg, left, right, relative_tolerance=Decimal(a.tolerance))

    if a.json:
        print(json.dumps({"summary": reg.summary(),
                          "findings": [d.as_dict() for d in reg.discrepancies],
                          "tolerance_applied": a.tolerance}, indent=2))
    else:
        s = reg.summary()
        print(f"Extracted {s['values_extracted']} values; "
              f"{s['comparisons']} comparisons; {s['discrepancies']} discrepancies "
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
