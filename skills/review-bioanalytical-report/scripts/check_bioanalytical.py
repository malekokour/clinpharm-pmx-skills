#!/usr/bin/env python3
"""Check a bioanalytical report's identifiers, units, criteria and arithmetic.

Usage:
    python3 check_bioanalytical.py --report bioanalytical.md [--json]

Emits mechanical findings only. It does not judge assay suitability or any
regulatory question.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import bioanalytical_consistency as engine


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", required=True)
    ap.add_argument("--locator", default="bioanalytical report")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    path = Path(a.report)
    if not path.is_file():
        print(f"CANNOT_ASSESS: input not found: {a.report}", file=sys.stderr)
        return 2

    report = engine.check(path.read_text(encoding="utf-8", errors="replace"), a.locator)

    if a.json:
        print(json.dumps({"summary": report.summary(), "counts": report.counts,
                          "findings": [f.as_dict() for f in report.findings],
                          "not_assessable": report.unassessable}, indent=2))
    else:
        print(report.summary())
        for f in report.findings:
            print(f"- [{f.severity}] {f.rule}: {f.item} — {f.observed}; expected {f.expected}")
        for u in report.unassessable:
            print(f"- NOT ASSESSABLE: {u['item']} — {u['why']}; resolved by {u['resolved_by']}")
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
