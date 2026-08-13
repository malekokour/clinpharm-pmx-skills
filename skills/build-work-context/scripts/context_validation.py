#!/usr/bin/env python3
"""VENDORED at build time from shared/scripts/ — do not edit here.
Edit the canonical source and rebuild; a freshness check compares them.

T-CTX — validate a work-context document's schema, classification and sources.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Mechanical checks only, over what a context document promises about itself:

**Schema** — the required sections are present. A context missing its review
metadata cannot be known to be current.

**Classification** — the data-boundary classification is one of the declared
tokens. A context labelled with an invented classification will not be honoured
by anything downstream, and will look labelled while being unenforceable.

**Sources** — every source carries a precedence marker, so an assistant reading
the context knows which wins. Sources without precedence are the mechanism by
which a draft quietly outranks a final result.

**Conflicts** — an unresolved conflict is *stated as unresolved*. This is the
check that matters most: the failure mode is a context that silently picks a
side, which destroys exactly the information a human needed to see.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from findings import Finding, Report

REQUIRED_SECTIONS = (
    "role",
    "sources",
    "constraints",
    "approval",
    "review",
)

#: The tokens this product recognises. An unlisted value is a defect rather than
#: an extension, because downstream behaviour keys on these exact strings.
CLASSIFICATIONS = {
    "PUBLIC",
    "INTERNAL",
    "CONFIDENTIAL",
    "RESTRICTED_DO_NOT_PROCESS",
}

CLASSIFICATION_LINE = re.compile(r"\bclassification\b\s*[:=]\s*([A-Za-z0-9_]+)", re.IGNORECASE)
PRECEDENCE = re.compile(r"\b(final|approved|authoritative|draft|superseded|historical)\b", re.IGNORECASE)
CONFLICT = re.compile(r"\b(conflict|unresolved|disagree\w*|contradict\w*)\b", re.IGNORECASE)
RESOLVED_LANGUAGE = re.compile(
    r"\b(resolved|decided|concluded|the correct value is|we use)\b", re.IGNORECASE
)


def sections(text: str) -> list[str]:
    return [line.lstrip("#").strip().lower() for line in text.splitlines() if line.startswith("#")]


def check(text: str, locator: str = "work context") -> Report:
    report = Report(tool="context-validation")
    heads = sections(text)
    report.count("sections", len(heads))

    for required in REQUIRED_SECTIONS:
        if not any(required in head for head in heads):
            report.add(
                Finding(
                    rule="missing-required-section",
                    severity="Major",
                    item=required,
                    observed="absent",
                    expected=f"a section covering '{required}'",
                    locator=locator,
                    detail=(
                        "the context contract requires this section; without it the "
                        "document cannot be known to be complete"
                    ),
                )
            )

    declared = CLASSIFICATION_LINE.findall(text)
    report.count("classification_declarations", len(declared))
    if not declared:
        report.add(
            Finding(
                rule="no-classification",
                severity="Critical",
                item="classification",
                observed="absent",
                expected=f"one of {sorted(CLASSIFICATIONS)}",
                locator=locator,
                detail=(
                    "an unclassified context carries no data boundary, so nothing "
                    "downstream can enforce one"
                ),
            )
        )
    for value in declared:
        if value.upper() not in CLASSIFICATIONS:
            report.add(
                Finding(
                    rule="unrecognised-classification",
                    severity="Critical",
                    item=value,
                    observed=value,
                    expected=f"one of {sorted(CLASSIFICATIONS)}",
                    locator=locator,
                    detail=(
                        "downstream behaviour keys on the exact token. An unlisted "
                        "value looks labelled while being unenforceable"
                    ),
                )
            )

    source_lines = [
        line for line in text.splitlines()
        if re.match(r"\s*[-*]\s", line) and re.search(r"\.(md|docx|pdf|csv|xlsx)\b|\bsource\b", line, re.IGNORECASE)
    ]
    report.count("source_entries", len(source_lines))
    without_precedence = [line for line in source_lines if not PRECEDENCE.search(line)]
    for line in without_precedence:
        report.add(
            Finding(
                rule="source-without-precedence",
                severity="Major",
                item=line.strip()[:80],
                observed="no precedence marker",
                expected="final / approved / draft / superseded",
                locator=locator,
                detail=(
                    "without a precedence marker an assistant cannot tell which "
                    "source wins, which is how a draft quietly outranks a final result"
                ),
            )
        )

    conflict_lines = [line for line in text.splitlines() if CONFLICT.search(line)]
    report.count("conflict_mentions", len(conflict_lines))
    for line in conflict_lines:
        if RESOLVED_LANGUAGE.search(line):
            report.add(
                Finding(
                    rule="conflict-resolved-in-context",
                    severity="Critical",
                    item=line.strip()[:80],
                    observed="the context resolves the conflict",
                    expected="both sides preserved, marked unresolved",
                    locator=locator,
                    detail=(
                        "a context that picks a side destroys the information the "
                        "human needed to see. Conflicts are surfaced, never settled, "
                        "and this tool does not settle it either"
                    ),
                )
            )
    if not conflict_lines:
        report.cannot_assess(
            item="conflict handling",
            why="the context mentions no conflicts, so the behaviour is untested here",
            resolved_by="exercise it with a context containing a known conflict",
        )
    return report
