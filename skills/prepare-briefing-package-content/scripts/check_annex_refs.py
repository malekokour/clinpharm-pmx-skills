#!/usr/bin/env python3
"""Check that every annex referenced in a briefing package is listed, and every listed annex is referenced.

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

#: An identifier must actually look like one: a letter-and-digit form (`A-01`,
#: `B2`), a bare number (`3.1`), or one or two letters (`A`). Admitting any word
#: made "Annex Inventory" and "Annex identifier" register as annexes — prose
#: swept in while widening the pattern, found by comparing the tool's extraction
#: against a direct count instead of trusting that the number had gone up.
#:
#: The identifier may carry hyphens and dots. `[A-Za-z0-9]{1,4}` did not, so
#: every `Annex A-12` matched only its leading `A` and thirteen distinct annex
#: IDs in one document collapsed into a single reference. The tool then reported
#: "annexes referenced in text: 1" and could not, structurally, see a dangling
#: reference or an orphaned annex — the two things it exists to find.
REF = re.compile(r"\b(Annex|Appendix)\s+((?:[A-Za-z]{1,2}[-.]?\d[A-Za-z0-9.-]*|\d[A-Za-z0-9.-]*|[A-Za-z]{1,2}))\b", re.IGNORECASE)
LISTED = re.compile(r"^\s*(?:[-*]|\d+\.)?\s*(Annex|Appendix)\s+((?:[A-Za-z]{1,2}[-.]?\d[A-Za-z0-9.-]*|\d[A-Za-z0-9.-]*|[A-Za-z]{1,2}))\b", re.IGNORECASE | re.MULTILINE)


def key(kind: str, ident: str) -> str:
    return f"{kind.lower()} {ident.lower()}"


def run(ns) -> Report:
    text = read(ns.package)
    report = Report(tool="check_annex_refs")

    referenced = {key(k, i) for k, i in REF.findall(text)}
    listed = {key(k, i) for k, i in LISTED.findall(text)}
    if ns.annex_list:
        for line in read(ns.annex_list).splitlines():
            m = REF.search(line)
            if m:
                listed.add(key(m.group(1), m.group(2)))

    report.count("annexes referenced in text", len(referenced))
    report.count("annexes listed", len(listed))

    for missing in sorted(referenced - listed):
        report.add(Finding(
            rule="annex-referenced-not-listed",
            severity="Major",
            item=missing,
            observed="referenced in the text",
            expected="an entry in the annex list",
            locator="body text",
            detail="The package points at an annex that its own list does not contain.",
        ))
    for orphan in sorted(listed - referenced):
        report.add(Finding(
            rule="annex-listed-not-referenced",
            severity="Minor",
            item=orphan,
            observed="listed",
            expected="at least one reference from the body text",
            locator="annex list",
            detail="An annex nothing points to is often a leftover from a previous version.",
        ))

    if not referenced and not listed:
        report.cannot_assess(
            "annex cross-referencing",
            "no annexes or appendices were found in either the text or the list",
            "a package containing annexes",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--package", required=True, help="briefing package text")
    parser.add_argument("--annex-list", help="optional annex list, one identifier per line")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
