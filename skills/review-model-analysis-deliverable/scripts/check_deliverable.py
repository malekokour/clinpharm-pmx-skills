#!/usr/bin/env python3
"""Check that an analysis deliverable's promised parts exist and agree.

Usage:
    python3 check_deliverable.py --root ./deliverable --report report.md \
        --promised data/adpk.csv run/model.ctl report.md \
        [--dataset data/adpk.csv] [--outputs run/output.lst] [--json]

Emits mechanical findings only. It does not judge whether a model is
appropriate or a conclusion sound.

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
import deliverable_consistency as engine


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="deliverable root")
    ap.add_argument("--report", required=True, help="the analysis report")
    ap.add_argument("--promised", nargs="*", default=[], help="files the manifest promises")
    ap.add_argument("--dataset", default=None, help="dataset to recompute record counts from")
    ap.add_argument("--outputs", default=None, help="estimation output to cross-check identifiers")
    ap.add_argument("--locator", default="deliverable")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    root = Path(a.root)
    report_path = root / a.report if not Path(a.report).is_file() else Path(a.report)
    if not report_path.is_file():
        print(f"CANNOT_ASSESS: report not found: {a.report}", file=sys.stderr)
        return 2

    outputs_text = ""
    if a.outputs:
        candidate = root / a.outputs if not Path(a.outputs).is_file() else Path(a.outputs)
        if candidate.is_file():
            outputs_text = candidate.read_text(encoding="utf-8", errors="replace")

    report = engine.check(
        root=root,
        promised=a.promised,
        report_text=report_path.read_text(encoding="utf-8", errors="replace"),
        dataset=a.dataset,
        outputs_text=outputs_text,
        locator=a.locator,
    )

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
