#!/usr/bin/env python3
"""VENDORED at build time from shared/scripts/ — do not edit here.
Edit the canonical source and rebuild; a freshness check compares them.

T-DEL — check that a deliverable's promised parts exist and agree.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Mechanical checks only, over the three things an analysis deliverable claims
about itself:

**Existence** — every file the manifest promises is actually present. A
deliverable that names a dataset it does not ship is incomplete regardless of
how good the report reads.

**Counts** — a record count stated in the report is recomputed from the dataset
it names. This is the check that catches a report describing an earlier data
cut, which is invisible to a reader holding only the report.

**Identifiers** — parameter and analysis identifiers named in the report appear
in the outputs, and vice versa. An output nobody reports and a report claim with
no output are different defects and are reported separately.

What it does not do: judge whether a model is appropriate, whether an estimate
is plausible, or whether a conclusion follows. Those are scientific judgements
and belong to a qualified reviewer.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from findings import Finding, Report

#: `n = 128`, `N=128`, `128 subjects`, `128 records`.
COUNT_CLAIM = re.compile(
    r"\b(?:n\s*=\s*(\d+)|N\s*=\s*(\d+)|(\d+)\s+(?:subjects?|records?|observations?|rows?))\b",
    re.IGNORECASE,
)

#: Conventional population-PK parameter names, plus THETA/OMEGA/SIGMA forms.
IDENTIFIER = re.compile(
    r"\b(?:CL|V[cp]?\d?|Q\d?|KA|F\d?|THETA\d*|OMEGA\d*|SIGMA\d*|IIV|RUV)\b"
)


def dataset_rows(path: Path) -> tuple[int, str | None]:
    """Count data rows in a delimited text dataset, excluding the header.

    Returns (rows, why_not) so a caller can distinguish "0 rows" from
    "could not be counted" — collapsing those two is how an empty check starts
    reporting success.
    """
    try:
        lines = [
            line
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    except OSError as exc:
        return 0, str(exc)
    if not lines:
        return 0, "file contains no non-comment lines"
    return max(len(lines) - 1, 0), None


def check(
    root: Path,
    promised: list[str],
    report_text: str,
    dataset: str | None = None,
    outputs_text: str = "",
    locator: str = "deliverable",
) -> Report:
    report = Report(tool="deliverable-consistency")
    report.count("promised_files", len(promised))

    present: list[str] = []
    for relative in promised:
        if (root / relative).is_file():
            present.append(relative)
        else:
            report.add(
                Finding(
                    rule="promised-file-absent",
                    severity="Critical",
                    item=relative,
                    observed="absent",
                    expected="present in the deliverable",
                    locator=locator,
                    detail=(
                        "the deliverable's manifest promises this file and it is not "
                        "there, so any claim resting on it cannot be checked"
                    ),
                )
            )
    report.count("files_present", len(present))

    claimed_counts = {
        int(next(g for g in match.groups() if g))
        for match in COUNT_CLAIM.finditer(report_text)
    }
    report.count("record_count_claims", len(claimed_counts))

    if dataset and (root / dataset).is_file():
        rows, why_not = dataset_rows(root / dataset)
        if why_not:
            report.cannot_assess(
                item=f"record counts against {dataset}",
                why=why_not,
                resolved_by="supply the dataset as delimited text with a header row",
            )
        else:
            report.count("dataset_rows", rows)
            if claimed_counts and rows not in claimed_counts:
                report.add(
                    Finding(
                        rule="record-count-mismatch",
                        severity="Critical",
                        item="record count",
                        observed=f"report states {sorted(claimed_counts)}",
                        expected=f"{rows} data rows in {dataset}",
                        locator=locator,
                        detail=(
                            "no record count stated in the report matches the dataset "
                            "it names. Both are preserved; this often means the report "
                            "describes an earlier data cut"
                        ),
                    )
                )
    elif dataset:
        report.cannot_assess(
            item="record counts",
            why=f"named dataset {dataset} is not present",
            resolved_by="ship the dataset, or stop naming it in the manifest",
        )
    else:
        report.cannot_assess(
            item="record counts",
            why="no dataset was supplied to recompute against",
            resolved_by="pass --dataset with the analysis dataset",
        )

    in_report = set(IDENTIFIER.findall(report_text))
    in_outputs = set(IDENTIFIER.findall(outputs_text))
    report.count("identifiers_in_report", len(in_report))
    report.count("identifiers_in_outputs", len(in_outputs))

    if not outputs_text.strip():
        report.cannot_assess(
            item="identifier cross-check",
            why="no outputs text was supplied, so the comparison would be vacuous",
            resolved_by="pass --outputs with the estimation output",
        )
        return report

    for name in sorted(in_report - in_outputs):
        report.add(
            Finding(
                rule="reported-identifier-absent-from-outputs",
                severity="Major",
                item=name,
                observed="named in the report",
                expected="present in the outputs",
                locator=locator,
                detail="the report discusses a parameter the supplied outputs do not contain",
            )
        )
    for name in sorted(in_outputs - in_report):
        report.add(
            Finding(
                rule="output-identifier-not-reported",
                severity="Minor",
                item=name,
                observed="present in the outputs",
                expected="discussed in the report",
                locator=locator,
                detail="the outputs contain a parameter the report does not mention",
            )
        )
    return report
