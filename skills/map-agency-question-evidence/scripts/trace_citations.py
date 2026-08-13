#!/usr/bin/env python3
"""Check that every citation in a response document points at something the document or its annex list defines.

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

#: A citation is a reference to a named location. The lead-in verb is optional,
#: because most documents do not use one.
#:
#: This pattern previously required `see`, `refer to` or `per` before the target.
#: On 2026-08-06 it reported `citations found: 0` on a response containing three
#: citations, every one written as `Source: Section 4.2` — an entirely ordinary
#: form — and printed a clean `Critical/Major/Minor` tally over them. A reviewer
#: reading that tally would have concluded the citations resolved. They were never
#: examined.
#:
#: The lead-in is now an optional prefix, so `see Table 3`, `per Annex A-4`,
#: `Source: Section 4.2` and a bare `Table 14.2.1` all register. Over-matching is
#: the safer error here: a target that turns out to be defined resolves and is
#: reported as resolved, while a citation never seen is silently absent from the
#: denominator.
CITE = re.compile(
    r"(?:\b(?:see|refer to|per|source|sources?|from|in|cited in|citation)\b[:\s]+)?"
    r"((?:Section|Table|Figure|Appendix|Annex)\s+[A-Za-z0-9.-]+)",
    re.IGNORECASE,
)
DEFINE = re.compile(r"^\s*#*\s*((?:Section|Table|Figure|Appendix|Annex)\s+[A-Za-z0-9.-]+)", re.IGNORECASE | re.MULTILINE)


def norm(s: str) -> str:
    return " ".join(s.split()).lower().rstrip(".")


def run(ns) -> Report:
    text = read(ns.response)
    report = Report(tool="trace_citations")

    cites = {norm(c) for c in CITE.findall(text)}
    defined = {norm(d) for d in DEFINE.findall(text)}
    if ns.annexes:
        defined |= {norm(line) for line in read(ns.annexes).splitlines() if line.strip()}

    report.count("citations found", len(cites))
    report.count("targets defined", len(defined))

    dangling = sorted(cites - defined)
    for d in dangling:
        report.add(Finding(
            rule="citation-target-not-found",
            severity="Major",
            item=d,
            observed="cited, no matching definition located",
            expected="a heading or annex entry with this identifier",
            locator="body text",
            detail="A reviewer following this citation lands nowhere. If the target is an "
                   "external annex, supply --annexes so it can be resolved.",
        ))
    report.count("citations resolved", len(cites) - len(dangling))

    if not cites:
        report.cannot_assess(
            "citation traceability",
            "no citations of the recognised forms were found",
            "a document citing sections, tables, figures, appendices or annexes",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--response", required=True, help="response document")
    parser.add_argument("--annexes", help="optional list of annex identifiers, one per line")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
