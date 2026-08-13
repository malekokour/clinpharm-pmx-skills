#!/usr/bin/env python3
"""Inventory declared IND mechanism/ADME content or IMPD Module-4/5 shape.

This utility checks only whether named declarations can be located in supplied
Markdown/plain text. It never determines scientific adequacy, trial-phase support,
filing readiness, or regulatory acceptance.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python 3.11+ standard library only
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IND_ITEMS = {
    "mechanism-or-pharmacological-effects": re.compile(
        r"mechanism(?:s)? of action|pharmacological effects?", re.IGNORECASE
    ),
    "absorption": re.compile(r"\babsorption\b", re.IGNORECASE),
    "distribution": re.compile(r"\bdistribution\b", re.IGNORECASE),
    "metabolism": re.compile(r"\bmetabolism\b", re.IGNORECASE),
    "excretion": re.compile(r"\bexcretion\b|\belimination\b", re.IGNORECASE),
}

IMPD_ITEMS = {
    "module-4-shaped-nonclinical-summary": re.compile(
        r"\bmodule\s*4\b|non[- ]clinical (?:pharmacology|toxicology) summary",
        re.IGNORECASE,
    ),
    "module-5-shaped-clinical-summary": re.compile(
        r"\bmodule\s*5\b|summary of (?:all )?(?:available )?(?:clinical data|previous clinical trials|human experience)",
        re.IGNORECASE,
    ),
}

UNKNOWN = re.compile(
    r"\bunknown\b|\bnot known\b|\bno (?:data|information) (?:are|is) available\b",
    re.IGNORECASE,
)


def first_match(text: str, pattern: re.Pattern[str]) -> tuple[str, str] | None:
    for number, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            state = "declared-unknown" if UNKNOWN.search(line) else "present"
            return state, f"line {number}"
    return None


def inspect(text: str, document_type: str) -> dict[str, object]:
    items = IND_ITEMS if document_type == "IND" else IMPD_ITEMS
    rows: list[dict[str, str]] = []
    for item, pattern in items.items():
        located = first_match(text, pattern)
        if located is None:
            rows.append(
                {
                    "item": item,
                    "state": "missing-declaration",
                    "locator": "supplied scope",
                    "classification": f"{item}-absent",
                }
            )
        else:
            state, locator = located
            rows.append(
                {
                    "item": item,
                    "state": state,
                    "locator": locator,
                    "classification": "none",
                }
            )
    missing = sum(row["state"] == "missing-declaration" for row in rows)
    return {
        "document_type": document_type,
        "counts": {
            "items_expected": len(items),
            "items_checked": len(items),
            "located_or_declared_unknown": len(items) - missing,
            "missing_declarations": missing,
        },
        "findings": [row for row in rows if row["state"] == "missing-declaration"],
        "inventory": rows,
        "boundary": (
            "Presence/location only; no scientific adequacy, trial-phase, filing, "
            "approval, dose, or regulatory conclusion."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document-type", required=True, choices=("IND", "IMPD"))
    parser.add_argument("--document", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.document.is_file():
        print(f"CANNOT_ASSESS: input not found: {args.document}")
        return 2
    result = inspect(args.document.read_text(encoding="utf-8", errors="replace"), args.document_type)
    counts = result["counts"]
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"Checked {counts['items_checked']}/{counts['items_expected']} declared "
            f"{args.document_type} content item(s); "
            f"{counts['located_or_declared_unknown']} located or declared unknown; "
            f"{counts['missing_declarations']} missing declaration(s)."
        )
        for row in result["inventory"]:
            print(f"- {row['item']}: {row['state']} @ {row['locator']}")
        print(result["boundary"])
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
