#!/usr/bin/env python3
"""Check whether stated in vitro findings trigger a clinical DDI study that the document does not mention.

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

#: DDI results are reported as a geometric mean ratio far more often than as
#: "AUCR". Omitting that form made the tool report "interaction ratios found: 0"
#: on a summary stating several, and then report no findings — a clean result
#: over nothing examined.
RATIO_LABEL = re.compile(
    r"AUCR|GMR|geometric\s+mean\s+ratio|Cmax\s*ratio|AUC\s*ratio|ratio\s+of\s+(?:AUC|Cmax)",
    re.IGNORECASE,
)
RATIO_DIRECT_VALUE = re.compile(r"^\s*(\d+(?:\.\d+)?)")
RATIO_LINKED_VALUE = re.compile(
    r"(?:\b(?:was|is|of)\b|[=:|])\s*(\d+(?:\.\d+)?)", re.IGNORECASE
)
INHIB = re.compile(r"\b(IC50|Ki)\b\D{0,20}(\d+(?:\.\d+)?)\s*(nM|uM|µM|mM)", re.IGNORECASE)
CLINICAL = re.compile(r"clinical (?:DDI|drug[- ]drug interaction) study|dedicated interaction study", re.IGNORECASE)
#: CYP2B6 was absent, and it is the enzyme carrying the open time-dependent
#: inhibition branch in this skill's own fixture — so the one trigger the tool
#: most needed to raise was invisible to it. 2B6, 2C8 and the OATP/OCT/MATE
#: transporters are added; an enzyme the tool cannot name is a branch it cannot
#: report as open.
ENZYMES = ("CYP3A4", "CYP3A5", "CYP2D6", "CYP2C8", "CYP2C9", "CYP2C19", "CYP2B6",
           "CYP1A2", "P-gp", "BCRP", "OATP1B1", "OATP1B3", "OATP", "OCT2",
           "MATE1", "MATE2-K", "BSEP")


def extract_ratios(text: str) -> list[tuple[str, float]]:
    """Extract ratios without mistaking parameter-name digits for values.

    A descriptor such as ``AUC0-inf`` legitimately contains a digit. The old
    pattern stopped at the first digit after the ratio label and therefore read
    that ``0`` as the result. Values must now either immediately follow the
    label or follow an explicit linguistic/table linker such as ``was``, ``=``,
    ``:``, or ``|`` within the same bounded statement.
    """
    ratios: list[tuple[str, float]] = []
    for label in RATIO_LABEL.finditer(text):
        tail = text[label.end() : label.end() + 120].split("\n\n", 1)[0]
        value = RATIO_DIRECT_VALUE.match(tail) or RATIO_LINKED_VALUE.search(tail)
        if value is not None:
            ratios.append((label.group(0), float(value.group(1))))
    return ratios


def run(ns) -> Report:
    text = read(ns.document)
    report = Report(tool="check_ddi_triggers")

    ratios = extract_ratios(text)
    inhib = [(m.group(1), float(m.group(2)), m.group(3)) for m in INHIB.finditer(text)]
    enzymes = [e for e in ENZYMES if e.lower() in text.lower()]
    has_clinical = bool(CLINICAL.search(text))

    report.count("interaction ratios found", len(ratios))
    report.count("inhibition constants found", len(inhib))
    report.count("enzymes or transporters named", len(enzymes))

    if not ratios and not inhib:
        report.cannot_assess(
            "DDI trigger assessment",
            "no interaction ratios or inhibition constants were found",
            "a document reporting AUCR/Cmax ratios or IC50/Ki values",
        )
        return report

    # A ratio at or beyond the conventional no-effect boundary is a mechanical
    # trigger for further evaluation. Whether a study is actually warranted is a
    # regulatory and scientific judgement this tool does not make.
    for label, value in ratios:
        if value >= 1.25 or value <= 0.80:
            sev = "Critical" if (value >= 2.0 or value <= 0.5) else "Major"
            if not has_clinical:
                report.add(Finding(
                    rule="trigger-without-stated-followup",
                    severity=sev,
                    item=f"{label} = {value:g}",
                    observed=f"{label} {value:g}, outside 0.80-1.25",
                    expected="a stated clinical interaction study, or a stated rationale for not doing one",
                    locator="interaction results",
                    detail="The ratio crosses the conventional no-effect boundary and the document "
                           "does not mention a clinical interaction study. Reported as a gap in the "
                           "document, not as a conclusion about the interaction.",
                ))
            else:
                report.add(Finding(
                    rule="trigger-noted",
                    severity="Minor",
                    item=f"{label} = {value:g}",
                    observed=f"{label} {value:g}, outside 0.80-1.25",
                    expected="—",
                    locator="interaction results",
                    detail="A clinical study is mentioned; this row records the trigger for traceability.",
                ))

    if inhib and not enzymes:
        report.add(Finding(
            rule="constant-without-named-target",
            severity="Major",
            item="inhibition constant",
            observed=f"{len(inhib)} value(s) with no named enzyme or transporter",
            expected="each constant attributed to a named CYP or transporter",
            locator="in vitro results",
            detail="An unattributed constant cannot be traced to a mechanism.",
        ))
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--document", required=True, help="DDI summary or briefing text")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
