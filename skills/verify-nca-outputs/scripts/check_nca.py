#!/usr/bin/env python3
"""Recompute NCA parameters from a profile and reconcile them with what was reported.

Usage:
    python3 check_nca.py --profile profile.txt --reported auc_linear=412 cmax=88.1 \
        [--lambda-z 0.0608] [--tolerance 0.02] [--json]

Emits mechanical findings only. Both the reported and recomputed values are
preserved; the script never decides which is correct.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import nca_recompute as engine


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", required=True, help="time/concentration rows")
    ap.add_argument("--reported", nargs="*", default=[], metavar="NAME=VALUE",
                    help="parameters as stated in the report")
    ap.add_argument("--lambda-z", default=None,
                    help="terminal rate constant from the analysis; without it "
                         "half-life is recorded as not assessable")
    ap.add_argument("--tolerance", default=str(engine.DEFAULT_TOLERANCE),
                    help="relative agreement band; take it from the analysis plan")
    ap.add_argument("--locator", default="NCA output")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    path = Path(a.profile)
    if not path.is_file():
        print(f"CANNOT_ASSESS: input not found: {a.profile}", file=sys.stderr)
        return 2

    reported = {}
    for item in a.reported:
        if "=" not in item:
            print(f"CANNOT_ASSESS: --reported needs NAME=VALUE, got {item!r}", file=sys.stderr)
            return 2
        name, _, value = item.partition("=")
        try:
            reported[name.strip()] = Decimal(value.strip())
        except InvalidOperation:
            print(f"CANNOT_ASSESS: {value!r} is not numeric", file=sys.stderr)
            return 2

    points, rejected = engine.parse_profile(path.read_text(encoding="utf-8", errors="replace"))
    lam = Decimal(a.lambda_z) if a.lambda_z else None
    report = engine.check(points, reported, rejected, lam, Decimal(a.tolerance), a.locator)

    if a.json:
        print(json.dumps({"summary": report.summary(),
                          "counts": report.counts,
                          "findings": [f.as_dict() for f in report.findings],
                          "not_assessable": report.unassessable}, indent=2))
    else:
        print(report.summary())
        for f in report.findings:
            print(f"- [{f.severity}] {f.rule}: {f.item} — reported {f.observed}, {f.expected} ({f.locator})")
        for u in report.unassessable:
            print(f"- NOT ASSESSABLE: {u['item']} — {u['why']}; resolved by {u['resolved_by']}")
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
