#!/usr/bin/env python3
"""Check declared IB human-PK content and supplied DSUR-to-IB version identity.

This utility performs presence and exact supplied-value comparisons only. It does
not approve medical content, decide live-study conduct, recommend a dose, interpret
safety, or determine a filing obligation.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python 3.11+ standard library only
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CONTENT_ITEMS = {
    "absorption": re.compile(r"\babsorption\b", re.IGNORECASE),
    "plasma-protein-binding": re.compile(r"plasma protein binding", re.IGNORECASE),
    "distribution": re.compile(r"\bdistribution\b", re.IGNORECASE),
    "metabolism": re.compile(r"\bmetabolism\b|product metabolism", re.IGNORECASE),
    "elimination": re.compile(r"\belimination\b|\bexcretion\b", re.IGNORECASE),
    "bioavailability": re.compile(r"\bbioavailability\b", re.IGNORECASE),
    "pharmacodynamics": re.compile(r"\bpharmacodynamics?\b|\bPD\b", re.IGNORECASE),
    "safety-and-efficacy": re.compile(r"safety and efficacy|efficacy and safety", re.IGNORECASE),
    "dose-response": re.compile(r"dose[- ]response", re.IGNORECASE),
}

UNKNOWN = re.compile(
    r"\bunknown\b|\bnot known\b|\bno (?:data|information) (?:are|is) available\b",
    re.IGNORECASE,
)
VERSION = re.compile(r"^\s*IB version:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
DATE = re.compile(r"^\s*IB date:\s*(\d{4}-\d{2}-\d{2})\s*$", re.IGNORECASE | re.MULTILINE)


def first_match(text: str, pattern: re.Pattern[str]) -> tuple[str, str] | None:
    for number, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            return ("declared-unknown" if UNKNOWN.search(line) else "present", f"line {number}")
    return None


def inspect_content(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item, pattern in CONTENT_ITEMS.items():
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
            rows.append({"item": item, "state": state, "locator": locator, "classification": "none"})
    return rows


def load_register(path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("version register must be a JSON object")
    for group in ("current_ib", "dsur_citation"):
        row = data.get(group)
        if not isinstance(row, dict):
            raise TypeError(f"version register missing object: {group}")
        for field in ("version", "date", "locator"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"version register {group}.{field} is required")
    return data


def compare_versions(text: str, register: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    actual_version = VERSION.search(text)
    actual_date = DATE.search(text)
    current = register["current_ib"]
    cited = register["dsur_citation"]
    comparisons = [
        ("ib-file-version", actual_version.group(1).strip() if actual_version else "NEEDS_INPUT", current["version"], "IB header", current["locator"]),
        ("ib-file-date", actual_date.group(1) if actual_date else "NEEDS_INPUT", current["date"], "IB header", current["locator"]),
        ("dsur-cited-ib-version", cited["version"], current["version"], cited["locator"], current["locator"]),
        ("dsur-cited-ib-date", cited["date"], current["date"], cited["locator"], current["locator"]),
    ]
    rows: list[dict[str, str]] = []
    for field, observed, expected, observed_locator, expected_locator in comparisons:
        if observed == "NEEDS_INPUT":
            state = "NEEDS_INPUT"
            classification = "missing-ib-identity"
        elif observed != expected:
            state = "mismatch"
            classification = "stale-version"
        else:
            state = "match"
            classification = "none"
        rows.append(
            {
                "field": field,
                "observed": observed,
                "expected": expected,
                "observed_locator": observed_locator,
                "expected_locator": expected_locator,
                "state": state,
                "classification": classification,
            }
        )
    return rows


def inspect(text: str, register: dict[str, dict[str, str]] | None) -> dict[str, object]:
    content = inspect_content(text)
    version_rows = compare_versions(text, register) if register is not None else []
    content_findings = [row for row in content if row["state"] == "missing-declaration"]
    version_findings = [row for row in version_rows if row["state"] != "match"]
    return {
        "counts": {
            "content_items_expected": len(CONTENT_ITEMS),
            "content_items_checked": len(CONTENT_ITEMS),
            "content_items_located_or_declared_unknown": len(CONTENT_ITEMS) - len(content_findings),
            "content_missing_declarations": len(content_findings),
            "version_comparisons_expected": 4,
            "version_comparisons_checked": len(version_rows),
            "version_findings": len(version_findings),
        },
        "content_inventory": content,
        "version_inventory": version_rows,
        "findings": [*content_findings, *version_findings],
        "version_state": "NEEDS_INPUT" if register is None else "checked",
        "boundary": (
            "Presence and supplied-version identity only; no medical approval, "
            "dose, live-study, safety, or filing conclusion."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ib", required=True, type=Path)
    parser.add_argument("--version-register", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.ib.is_file():
        print(f"CANNOT_ASSESS: input not found: {args.ib}")
        return 2
    register = None
    if args.version_register is not None:
        if not args.version_register.is_file():
            print(f"CANNOT_ASSESS: version register not found: {args.version_register}")
            return 2
        try:
            register = load_register(args.version_register)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(f"CANNOT_ASSESS: invalid version register: {exc}")
            return 2

    result = inspect(args.ib.read_text(encoding="utf-8", errors="replace"), register)
    counts = result["counts"]
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"Checked {counts['content_items_checked']}/{counts['content_items_expected']} "
            f"IB content item(s); {counts['content_items_located_or_declared_unknown']} located "
            f"or declared unknown; {counts['content_missing_declarations']} missing declaration(s)."
        )
        print(
            f"Checked {counts['version_comparisons_checked']}/{counts['version_comparisons_expected']} "
            f"version/date comparison(s); {counts['version_findings']} finding(s); "
            f"state {result['version_state']}."
        )
        for row in result["findings"]:
            if "field" in row:
                print(
                    f"- {row['classification']}: {row['field']} observed {row['observed']} "
                    f"@ {row['observed_locator']}; expected {row['expected']} "
                    f"@ {row['expected_locator']}"
                )
            else:
                print(f"- {row['classification']}: {row['item']} @ {row['locator']}")
        print(result["boundary"])
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
