#!/usr/bin/env python3
"""Check ordering and unit consistency across ADC analyte parameters.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Usage:
    python3 analyte_consistency.py analytes.json
    python3 analyte_consistency.py --self-test

What it checks — and what it deliberately does not
--------------------------------------------------
Two relations, both properties of the reported numbers rather than of the
pharmacology:

1. **Containment ordering.** A conjugated species cannot exceed its
   corresponding total on the same measure. If a document reports conjugated
   antibody AUC above total antibody AUC, at least one of the two is wrong, and
   that conclusion needs no biology.
2. **Unit consistency.** The same analyte and measure must carry the same unit
   everywhere it is reported. A unit that changes between documents makes every
   downstream comparison meaningless.

**It does not judge whether a ratio is biologically reasonable.** Whether a
conjugated-to-total ratio of 0.3 is expected for a given DAR and linker is a
scientific judgment, and a script asserting it would be inventing a criterion.
The skill's `Never` list says so, and this script is built to make that
impossible rather than merely discouraged.

Input shape
-----------
    {
      "containment": [["conjugated-antibody", "total-antibody"]],
      "measurements": [
        {"analyte": "total-antibody", "measure": "AUC", "value": 1200,
         "unit": "ug*h/mL", "document": "CSR", "locator": "Table 14.2.1"},
        {"analyte": "conjugated-antibody", "measure": "AUC", "value": 1400,
         "unit": "ug*h/mL", "document": "CSR", "locator": "Table 14.2.2"}
      ]
    }

``containment`` pairs are supplied rather than inferred from names. Inferring
"conjugated is inside total" from a naming convention would break on the first
programme that names its analytes differently, and would do so silently.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def check(document: dict) -> int:
    measurements = document.get("measurements") or []
    containment = [tuple(pair) for pair in (document.get("containment") or [])]

    if not measurements:
        print("CANNOT_ASSESS: 0 measurements supplied — nothing was checked")
        print("checked 0/0 relations")
        return 2

    findings: list[str] = []
    relations = 0

    # 1 — unit consistency per (analyte, measure)
    units: dict[tuple[str, str], set[tuple[str, str, str]]] = defaultdict(set)
    for row in measurements:
        key = (row.get("analyte", ""), row.get("measure", ""))
        units[key].add(
            (
                str(row.get("unit", "")),
                str(row.get("document", "")),
                str(row.get("locator", "")),
            )
        )
    for (analyte, measure), seen in sorted(units.items()):
        relations += 1
        distinct = {unit for unit, _, _ in seen}
        if len(distinct) > 1:
            where = "; ".join(
                f"{unit!r} in {doc or '?'} at {loc or '?'}" for unit, doc, loc in sorted(seen)
            )
            findings.append(
                f"UNIT_INCONSISTENCY {analyte} {measure}: {len(distinct)} distinct "
                f"units — {where}"
            )

    # 2 — containment ordering, compared only within the same document and measure
    indexed: dict[tuple[str, str, str], dict] = {}
    for row in measurements:
        indexed[
            (
                str(row.get("document", "")),
                str(row.get("measure", "")),
                str(row.get("analyte", "")),
            )
        ] = row
    for inner, outer in containment:
        for (doc, measure, analyte), row in sorted(indexed.items()):
            if analyte != inner:
                continue
            partner = indexed.get((doc, measure, outer))
            if partner is None:
                continue
            relations += 1
            try:
                inner_value = float(row["value"])
                outer_value = float(partner["value"])
            except (KeyError, TypeError, ValueError):
                findings.append(
                    f"CANNOT_ASSESS {inner} vs {outer} {measure} in {doc or '?'}: "
                    "non-numeric or absent value"
                )
                continue
            if row.get("unit") != partner.get("unit"):
                findings.append(
                    f"CANNOT_ASSESS {inner} vs {outer} {measure} in {doc or '?'}: "
                    f"units differ ({row.get('unit')!r} vs {partner.get('unit')!r})"
                )
                continue
            if inner_value > outer_value:
                findings.append(
                    f"CONTAINMENT_VIOLATION {inner} {measure} {inner_value:g} exceeds "
                    f"{outer} {outer_value:g} in {doc or '?'} "
                    f"({row.get('locator', '?')} vs {partner.get('locator', '?')})"
                )

    for finding in findings:
        print(finding)

    violations = sum(1 for f in findings if not f.startswith("CANNOT_ASSESS"))
    print(
        f"checked {relations} relation(s) across {len(measurements)} measurement(s); "
        f"{violations} violation(s), "
        f"{len(findings) - violations} CANNOT_ASSESS"
    )
    return 1 if violations else 0


def self_test() -> int:
    base = {
        "containment": [["conjugated-antibody", "total-antibody"]],
        "measurements": [
            {"analyte": "total-antibody", "measure": "AUC", "value": 1400,
             "unit": "ug*h/mL", "document": "CSR", "locator": "T1"},
            {"analyte": "conjugated-antibody", "measure": "AUC", "value": 1200,
             "unit": "ug*h/mL", "document": "CSR", "locator": "T2"},
        ],
    }
    if check(base) != 0:
        print("SELF_TEST_ERROR: a consistent set was reported as violating")
        return 1

    violating = json.loads(json.dumps(base))
    violating["measurements"][1]["value"] = 1600
    if check(violating) != 1:
        print("SELF_TEST_ERROR: conjugated exceeding total was not caught")
        return 1

    # The same analyte and measure reported in two units across documents. This
    # IS a defect and must exit 1 — the first draft of this self-test expected 0
    # and was wrong: a unit that changes between documents makes every downstream
    # comparison meaningless, which is exactly what this script exists to catch.
    mixed_units = json.loads(json.dumps(base))
    mixed_units["measurements"][1]["unit"] = "ng*h/mL"
    mixed_units["measurements"].append(
        {"analyte": "conjugated-antibody", "measure": "AUC", "value": 1200,
         "unit": "ug*h/mL", "document": "IB", "locator": "T9"}
    )
    if check(mixed_units) != 1:
        print("SELF_TEST_ERROR: a unit inconsistency across documents was not caught")
        return 1

    if check({"measurements": []}) != 2:
        print("SELF_TEST_ERROR: an empty set did not report CANNOT_ASSESS")
        return 1

    print("self_test_canaries=4/4")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check ADC analyte consistency")
    parser.add_argument("analytes", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.analytes is None:
        parser.error("an analytes JSON file is required unless --self-test is given")
    return check(json.loads(args.analytes.read_text(encoding="utf-8")))


if __name__ == "__main__":
    sys.exit(main())
