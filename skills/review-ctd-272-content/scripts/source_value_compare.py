#!/usr/bin/env python3
"""Compare explicitly located numeric values across supplied documents.

The JSON specification owns each comparison's two document names, exact regex
patterns, locators, and provisional severity. Each regex must match exactly once
and expose a named ``value`` group plus an optional ``unit`` group. Zero pairs,
zero comparisons, ambiguous matches, or missing documents fail closed.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


class ComparisonInputError(ValueError):
    """The comparison specification cannot produce bounded comparisons."""


def _extract(side: dict[str, str], documents: dict[str, str]) -> tuple[Decimal, str, str]:
    name = side.get("document", "")
    if name not in documents:
        raise ComparisonInputError(f"unknown document {name!r}")
    pattern = side.get("pattern", "")
    try:
        matches = list(re.finditer(pattern, documents[name], re.IGNORECASE | re.MULTILINE))
    except re.error as exc:
        raise ComparisonInputError(f"invalid regex for {name!r}: {exc}") from exc
    if len(matches) != 1:
        raise ComparisonInputError(
            f"{name!r} pattern must match exactly once; matched {len(matches)}"
        )
    match = matches[0]
    if "value" not in match.groupdict():
        raise ComparisonInputError(f"{name!r} pattern lacks named group 'value'")
    try:
        value = Decimal(match.group("value").replace(",", ""))
    except (InvalidOperation, AttributeError) as exc:
        raise ComparisonInputError(f"{name!r} captured a non-numeric value") from exc
    unit = match.groupdict().get("unit") or ""
    return value, unit, match.group(0)


def compare(spec: dict[str, object], documents: dict[str, str]) -> dict[str, object]:
    pairs = spec.get("pairs")
    if not isinstance(pairs, list) or not pairs:
        raise ComparisonInputError("spec must declare at least one comparison pair")
    findings: list[dict[str, str]] = []
    identifiers: set[str] = set()
    comparisons = 0
    for raw in pairs:
        if not isinstance(raw, dict):
            raise ComparisonInputError("every pair must be an object")
        pair_id = str(raw.get("id", "")).strip()
        if not pair_id or pair_id in identifiers:
            raise ComparisonInputError("pair ids must be non-empty and unique")
        identifiers.add(pair_id)
        left, right = raw.get("left"), raw.get("right")
        if not isinstance(left, dict) or not isinstance(right, dict):
            raise ComparisonInputError(f"{pair_id}: left and right must be objects")
        left_value, left_unit, left_raw = _extract(left, documents)
        right_value, right_unit, right_raw = _extract(right, documents)
        comparisons += 1
        if left_value == right_value and left_unit.casefold() == right_unit.casefold():
            continue
        findings.append({
            "id": pair_id,
            "rule": "source-value-mismatch",
            "severity": str(raw.get("severity", "Major")),
            "statement_as_written": left_raw,
            "statement_locator": str(left.get("locator", left.get("document", ""))),
            "expected_value_or_content": right_raw,
            "expected_locator": str(right.get("locator", right.get("document", ""))),
            "disposition": "open",
        })
    if comparisons == 0:
        raise ComparisonInputError("no comparisons were executed")
    return {
        "summary": {
            "pairs_declared": len(pairs),
            "comparisons": comparisons,
            "discrepancies": len(findings),
        },
        "findings": findings,
        "boundary": "Mechanical comparison only; a qualified reviewer decides which statement governs.",
    }


def _documents(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ComparisonInputError("--document must use NAME=PATH")
        name, path = item.split("=", 1)
        if not name or name in result:
            raise ComparisonInputError("document names must be non-empty and unique")
        source = Path(path)
        if not source.is_file():
            raise ComparisonInputError(f"document not found: {path}")
        result[name] = source.read_text(encoding="utf-8", errors="replace")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", required=True)
    parser.add_argument("--document", action="append", default=[], metavar="NAME=PATH")
    args = parser.parse_args()
    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        result = compare(spec, _documents(args.document))
    except (OSError, json.JSONDecodeError, ComparisonInputError) as exc:
        print(json.dumps({"status": "CANNOT_ASSESS", "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
