#!/usr/bin/env python3
"""Compare labelled facts across two or more programme documents and preserve every disagreement.

Emits mechanical findings only. Both sides of every conflict are preserved with
their locators; this script never decides which is correct.

Author: Malek Okour
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findings import Finding, Report

FACT = re.compile(
    r"(?P<label>[A-Za-z][A-Za-z0-9 /_%()-]{2,44}?)\s*[:=]\s*"
    r"(?P<value>-?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµ/·%]+(?:/[A-Za-z]+)?)?",
)


#: `| CL/F | 15.2 L/h |` — the way clinical documents actually present parameters.
#:
#: `FACT` above handles `label: value` prose only. On 2026-08-06 that extracted
#: **1 fact from 3 documents** whose parameters were all in markdown tables, so the
#: tool reported "comparisons made: 0" and, having compared nothing, found nothing
#: to disagree about. A reconciliation tool that reconciles zero pairs and reports
#: no findings is indistinguishable from one that reconciled everything and found
#: agreement — which is precisely the claim it exists to support.
TABLE_FACT = re.compile(
    r"^\s*\|\s*(?P<label>[^|]{2,60}?)\s*\|\s*"
    r"(?P<value>-?\d+(?:[.,]\d+)?)\s*(?P<unit>[A-Za-zµ%·]+(?:/[A-Za-z]+)?)?\s*(?:\||$)"
)

#: Rows whose left cell is a header or a separator, not a parameter name.
NOT_A_LABEL = re.compile(r"^[\s:-]*$|^(parameter|analyte|value|item|field|metric)s?$", re.IGNORECASE)


def extract(path: str) -> dict[str, tuple[str, str]]:
    """label -> (value, locator). First occurrence wins; later ones are duplicates.

    Both prose (`label: value`) and table rows (`| label | value |`) are read. A
    document that states its parameters one way must not be invisible to a tool
    that only understands the other.
    """
    out: dict[str, tuple[str, str]] = {}
    for i, line in enumerate(read(path).splitlines(), 1):
        m = TABLE_FACT.match(line) or FACT.search(line)
        if not m:
            continue
        label = " ".join(m.group("label").split()).lower().strip("*` ")
        if not label or NOT_A_LABEL.match(label):
            continue
        value = m.group("value") + (f" {m.group('unit')}" if m.group("unit") else "")
        out.setdefault(label, (value, f"{Path(path).name}:{i}"))
    return out


def run(ns) -> Report:
    if len(ns.documents) < 2:
        raise SystemExit("reconcile_programme: need at least two documents to compare")

    report = Report(tool="reconcile_programme")
    per_doc = {d: extract(d) for d in ns.documents}

    report.count("documents", len(per_doc))
    report.count("facts extracted", sum(len(v) for v in per_doc.values()))

    labels: dict[str, list[tuple[str, str, str]]] = {}
    for doc, facts in per_doc.items():
        for label, (value, loc) in facts.items():
            labels.setdefault(label, []).append((doc, value, loc))

    shared = {k: v for k, v in labels.items() if len(v) > 1}
    report.count("facts appearing in more than one document", len(shared))
    report.count("comparisons made", sum(len(v) - 1 for v in shared.values()))

    for label, entries in sorted(shared.items()):
        values = {v for _, v, _ in entries}
        if len(values) > 1:
            a, b = entries[0], entries[1]
            report.add(Finding(
                rule="cross-document-disagreement",
                severity="Critical",
                item=label,
                observed=f"{a[1]} @ {a[2]}",
                expected=f"{b[1]} @ {b[2]}",
                locator=a[2],
                detail="Both values are preserved with their locations. This tool does not "
                       "determine which document is correct.",
            ))

    singletons = [k for k, v in labels.items() if len(v) == 1]
    report.count("facts stated in only one document", len(singletons))
    if not shared:
        report.cannot_assess(
            "cross-document comparison",
            "no label appeared in more than one document, so nothing could be compared",
            "documents using consistent labels, or a supplied label mapping",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--documents", required=True, nargs="+", help="two or more documents")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
