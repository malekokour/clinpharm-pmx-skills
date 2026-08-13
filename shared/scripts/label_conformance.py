#!/usr/bin/env python3
"""T04 — USPI Section 12 content-conformance checker.

Checks presence and ordering of required Clinical Pharmacology labelling content
against `cfr-201-57-c-13` and `fda-labeling-cp` (December 2016).

Presence and phrasing only. The tool takes no position in a labelling
negotiation and never releases label text.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

import re

REQUIRED_SUBSECTIONS = ["12.1 Mechanism of Action", "12.2 Pharmacodynamics",
                        "12.3 Pharmacokinetics"]
PK_ELEMENT_ORDER = ["Absorption", "Distribution", "Elimination", "Specific Populations",
                    "Drug Interaction Studies"]
#: Phrasing the 2016 guidance excludes from a pharmacokinetics section.
PROHIBITED = [
    (re.compile(r"\bwell[- ]tolerated\b", re.IGNORECASE), "tolerability claim in a PK section"),
    (re.compile(r"\bsuperior(?:ity)? to\b", re.IGNORECASE), "comparative efficacy claim"),
    (re.compile(r"\bsafe and effective\b", re.IGNORECASE), "benefit claim in a PK section"),
    (re.compile(r"\bfirst[- ]line\b", re.IGNORECASE), "implied indication"),
]


def check(text: str, locator_prefix: str = "Section 12") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for sub in REQUIRED_SUBSECTIONS:
        if sub.split(" ", 1)[0] not in text:
            findings.append({"rule": "missing-required-subsection", "severity": "Critical",
                             "kind": "mechanical", "observed": "absent", "expected": sub,
                             "locator": locator_prefix,
                             "detail": f"{sub} is required content under 21 CFR 201.57(c)(13)."})
    present = [(text.index(e), e) for e in PK_ELEMENT_ORDER if e in text]
    if present and [e for _, e in sorted(present)] != [e for _, e in present]:
        findings.append({"rule": "element-order-deviation", "severity": "Minor",
                         "kind": "mechanical", "observed": ", ".join(e for _, e in present),
                         "expected": ", ".join(PK_ELEMENT_ORDER), "locator": locator_prefix,
                         "detail": "Section 12.3 elements deviate from the conventional order."})
    for pattern, why in PROHIBITED:
        for m in pattern.finditer(text):
            findings.append({"rule": "prohibited-phrasing", "severity": "Major",
                             "kind": "mechanical", "observed": m.group(0), "expected": "—",
                             "locator": f"{locator_prefix} @ char {m.start()}",
                             "detail": f"Excluded by the December 2016 labelling guidance: {why}."})
    return findings
