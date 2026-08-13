#!/usr/bin/env python3
"""Check PK parameter units, ranges and arithmetic relations.

Usage:
    python3 check_pk.py --params params.json [--json]

params.json: {"parameters":[{"name":"Cmax","unit":"ng/mL","value":412,
              "locator":"T14.2.1"}],
              "accumulation":{"half_life_h":12,"tau_h":24,"reported_ratio":1.33,
                              "locator":"§12.3"},
              "ratios":[{"point":1.05,"ci_low":0.92,"ci_high":1.20,
                         "locator":"T14.2.5"}]}

Every output is a mechanical finding, never a scientific conclusion.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pk_plausibility as t03


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--params", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--declared-units",
        help="JSON file mapping parameter to the unit the analysis plan specifies, "
             'e.g. {"cl": "L/h"}. May also be supplied as a "declared_units" key '
             "inside --params. Without it the unit check falls back to class "
             "membership only, which passes a 1000x error like mL/h for L/h.",
    )
    a = ap.parse_args()
    if not Path(a.params).is_file():
        print(f"CANNOT_ASSESS: input not found: {a.params}", file=sys.stderr)
        return 2
    data = json.loads(Path(a.params).read_text(encoding="utf-8"))
    r = t03.Report()

    # `check_unit` has always accepted `declared_units`, and its docstring names
    # the defect it exists to catch: "A clearance reported in mL/h where the plan
    # says L/h is a 1000x error that passes any class check." No CLI ever passed
    # it, so the check could not fire from the shipped entry point. Three
    # independent runs on 2026-08-06 fed exactly that error to this script and
    # got zero findings.
    declared: dict[str, str] | None = data.get("declared_units")
    if a.declared_units:
        if not Path(a.declared_units).is_file():
            print(f"CANNOT_ASSESS: declared-units file not found: {a.declared_units}", file=sys.stderr)
            return 2
        declared = json.loads(Path(a.declared_units).read_text(encoding="utf-8"))
    if declared is None:
        print(
            "NOTE: no declared units supplied, so the unit check tests class "
            "membership only. A unit that is valid for the parameter but "
            "contradicts the analysis plan will NOT be flagged.",
            file=sys.stderr,
        )

    for p in data.get("parameters", []):
        loc = p.get("locator", "unspecified")
        if p.get("unit"):
            t03.check_unit(p["name"], p["unit"], loc, r, declared_units=declared)
        if isinstance(p.get("value"), (int, float)):
            t03.check_range(p["name"], float(p["value"]), loc, r)

    acc = data.get("accumulation")
    if acc:
        t03.check_accumulation_consistency(
            float(acc["half_life_h"]), float(acc["tau_h"]),
            float(acc["reported_ratio"]), acc.get("locator", "unspecified"), r)

    for ratio in data.get("ratios", []):
        t03.check_ratio_statistic(float(ratio["point"]), float(ratio["ci_low"]),
                                  float(ratio["ci_high"]),
                                  ratio.get("locator", "unspecified"), r)

    if a.json:
        print(json.dumps({"summary": r.summary(),
                          "findings": [f.as_dict() for f in r.findings],
                          "skipped": r.skipped}, indent=2))
    else:
        s = r.summary()
        print(f"Checked {s['checked']}; {s['findings']} findings; "
              f"{s['skipped']} skipped for want of a rule")
        for f in r.findings:
            print(f"  [{f.severity}] {f.rule}: {f.parameter}")
            print(f"    observed {f.observed} · expected {f.expected} @ {f.locator}")
            print(f"    {f.detail}")
        for s_ in r.skipped:
            print(f"  CANNOT_ASSESS: {s_}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
