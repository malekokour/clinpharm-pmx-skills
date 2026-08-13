#!/usr/bin/env python3
"""Reconcile declared DSUR and IND annual-report periods without deciding obligations.

Author: Malek Okour
Date: 2026-08-11
Dependencies: Python 3.11+ standard library only
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from itertools import pairwise
from pathlib import Path
from typing import Any

KINDS = {"DSUR", "IND_ANNUAL_REPORT"}
UNKNOWN_POLICY_STATES = (
    {
        "id": "UNKNOWN_FINAL_RULE_STATUS",
        "state": "UNKNOWN",
        "as_of": "2026-08-10",
        "question": "Whether the proposed FDA DSUR rule had actually been finalized and made effective.",
        "required_action": "Regulatory owner re-checks current primary authority.",
    },
    {
        "id": "UNKNOWN_DSUR_IN_LIEU_PRACTICE",
        "state": "UNKNOWN",
        "as_of": "2026-08-10",
        "question": "Whether FDA accepted an ICH E2F DSUR in lieu of a 21 CFR 312.33 annual report as current practice.",
        "required_action": "Regulatory owner verifies current primary FDA policy and application-specific practice.",
    },
)


@dataclass(frozen=True)
class Period:
    report_id: str
    kind: str
    version: str
    status: str
    start: date
    end: date
    locator: str


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    report_a: str
    locator_a: str
    report_b: str
    locator_b: str
    affected_start: str
    affected_end: str
    detail: str
    disposition: str = "open"


def parse_iso(raw: Any, field: str, report_id: str) -> date:
    if not isinstance(raw, str):
        raise TypeError(f"{report_id}: {field} must be an ISO date string")
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{report_id}: {field} is not a valid ISO date: {raw!r}") from exc


def parse_documents(payload: dict[str, Any]) -> tuple[list[Period], list[dict[str, str]]]:
    raw_documents = payload.get("documents")
    if not isinstance(raw_documents, list) or not raw_documents:
        raise ValueError("input must contain a non-empty 'documents' list")

    periods: list[Period] = []
    unassessable: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_documents, 1):
        fallback_id = f"record-{index}"
        if not isinstance(item, dict):
            unassessable.append({
                "report_id": fallback_id,
                "state": "CANNOT_ASSESS",
                "why": "record is not an object",
                "resolved_by": "a record matching references/period-input-contract.md",
            })
            continue
        report_id = str(item.get("id", "")).strip() or fallback_id
        try:
            if report_id in seen:
                raise ValueError(f"{report_id}: duplicate report id")
            seen.add(report_id)
            kind = str(item.get("kind", "")).strip()
            if kind not in KINDS:
                raise ValueError(f"{report_id}: kind must be one of {sorted(KINDS)}")
            locator = str(item.get("locator", "")).strip()
            if not locator:
                raise ValueError(f"{report_id}: locator is required")
            start = parse_iso(item.get("period_start"), "period_start", report_id)
            end = parse_iso(item.get("period_end"), "period_end", report_id)
            if end < start:
                raise ValueError(f"{report_id}: period_end precedes period_start")
            periods.append(Period(
                report_id=report_id,
                kind=kind,
                version=str(item.get("version", "UNKNOWN")),
                status=str(item.get("status", "UNKNOWN")),
                start=start,
                end=end,
                locator=locator,
            ))
        except (TypeError, ValueError) as exc:
            unassessable.append({
                "report_id": report_id,
                "state": "NEEDS_INPUT",
                "why": str(exc),
                "resolved_by": "corrected structured period metadata with an exact locator",
            })
    return periods, unassessable


def overlap(a: Period, b: Period) -> tuple[date, date] | None:
    start = max(a.start, b.start)
    end = min(a.end, b.end)
    return (start, end) if start <= end else None


def reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    periods, unassessable = parse_documents(payload)
    findings: list[Finding] = []
    same_kind_comparisons = 0
    cross_format_comparisons = 0

    for kind in sorted(KINDS):
        ordered = sorted((period for period in periods if period.kind == kind), key=lambda p: (p.start, p.end, p.report_id))
        for prior, current in pairwise(ordered):
            same_kind_comparisons += 1
            if prior.start == current.start and prior.end == current.end:
                findings.append(Finding(
                    rule="same-kind-duplicate-period",
                    severity="Major",
                    report_a=prior.report_id,
                    locator_a=prior.locator,
                    report_b=current.report_id,
                    locator_b=current.locator,
                    affected_start=prior.start.isoformat(),
                    affected_end=prior.end.isoformat(),
                    detail="The two reports declare the same inclusive period. This is a date duplication flag, not a filing conclusion.",
                ))
            elif current.start > prior.end + timedelta(days=1):
                findings.append(Finding(
                    rule="same-kind-gap",
                    severity="Critical",
                    report_a=prior.report_id,
                    locator_a=prior.locator,
                    report_b=current.report_id,
                    locator_b=current.locator,
                    affected_start=(prior.end + timedelta(days=1)).isoformat(),
                    affected_end=(current.start - timedelta(days=1)).isoformat(),
                    detail="No supplied report of this kind declares the affected dates. Missing inventory records may resolve the flag.",
                ))
            else:
                shared = overlap(prior, current)
                if shared is not None:
                    findings.append(Finding(
                        rule="same-kind-overlap",
                        severity="Major",
                        report_a=prior.report_id,
                        locator_a=prior.locator,
                        report_b=current.report_id,
                        locator_b=current.locator,
                        affected_start=shared[0].isoformat(),
                        affected_end=shared[1].isoformat(),
                        detail="Successive reports of the same kind share inclusive dates. The skill does not decide whether that overlap is acceptable.",
                    ))

    dsurs = [period for period in periods if period.kind == "DSUR"]
    annuals = [period for period in periods if period.kind == "IND_ANNUAL_REPORT"]
    for dsur in dsurs:
        for annual in annuals:
            cross_format_comparisons += 1
            shared = overlap(dsur, annual)
            if shared is None:
                continue
            findings.append(Finding(
                rule="cross-format-potential-duplicate-coverage",
                severity="Major",
                report_a=dsur.report_id,
                locator_a=dsur.locator,
                report_b=annual.report_id,
                locator_b=annual.locator,
                affected_start=shared[0].isoformat(),
                affected_end=shared[1].isoformat(),
                detail="The two formats cover common dates. This does not determine which report was required or whether any obligation is satisfied.",
            ))

    source_count = len(payload.get("documents", [])) if isinstance(payload.get("documents"), list) else 0
    return {
        "tool": "reconcile_reporting_periods",
        "as_of_date": payload.get("as_of_date", "UNKNOWN"),
        "counts": {
            "reports_supplied": source_count,
            "reports_assessable": len(periods),
            "reports_unassessable": len(unassessable),
            "same_kind_adjacency_comparisons": same_kind_comparisons,
            "cross_format_comparisons": cross_format_comparisons,
            "findings": len(findings),
            "policy_unknowns": len(UNKNOWN_POLICY_STATES),
        },
        "periods": [
            {
                "report_id": period.report_id,
                "kind": period.kind,
                "version": period.version,
                "status": period.status,
                "period_start": period.start.isoformat(),
                "period_end": period.end.isoformat(),
                "locator": period.locator,
            }
            for period in sorted(periods, key=lambda p: (p.kind, p.start, p.end, p.report_id))
        ],
        "findings": [asdict(finding) for finding in findings],
        "unassessable": unassessable,
        "policy_unknowns": list(UNKNOWN_POLICY_STATES),
        "boundary": "Mechanical date findings only. This output does not determine whether an IND filing obligation is satisfied.",
    }


def render_text(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        (
            "reconcile_reporting_periods: "
            f"checked {counts['reports_assessable']} of {counts['reports_supplied']} supplied reports; "
            f"{counts['findings']} finding(s) across "
            f"{counts['same_kind_adjacency_comparisons']} same-kind adjacency comparison(s) and "
            f"{counts['cross_format_comparisons']} cross-format comparison(s); "
            f"{counts['reports_unassessable']} report(s) not assessable"
        )
    ]
    for finding in report["findings"]:
        lines.append(
            f"[{finding['severity']}] {finding['rule']}: {finding['report_a']} @ {finding['locator_a']} "
            f"vs {finding['report_b']} @ {finding['locator_b']}; "
            f"affected {finding['affected_start']} through {finding['affected_end']}; disposition open"
        )
    for item in report["unassessable"]:
        lines.append(f"[{item['state']}] {item['report_id']}: {item['why']}; resolve with {item['resolved_by']}")
    for item in report["policy_unknowns"]:
        lines.append(f"[UNKNOWN] {item['id']}: {item['question']} {item['required_action']}")
    lines.append(report["boundary"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="JSON input matching references/period-input-contract.md")
    parser.add_argument("--json", action="store_true", help="emit JSON rather than text")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("top-level JSON value must be an object")
        report = reconcile(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
