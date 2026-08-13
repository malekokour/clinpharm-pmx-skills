#!/usr/bin/env python3
"""Check a briefing package for the elements a regulatory meeting request is normally expected to contain.

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

#: Bundled with the skill, so the check works from a clean install with no flag.
DEFAULT_BANK = Path(__file__).resolve().parent.parent / "assets" / "qbr-question-bank.md"

#: Common words that carry no discriminating signal in a clinical question.
STOPWORDS = {"which", "there", "these", "those", "their", "about", "would", "could",
             "should", "based", "study", "studies", "where", "whether",
             "propos", "proposed", "across", "between", "within"}

REQUIRED = [
    ("meeting objective", r"objectiv|purpose of (?:the )?meeting"),
    ("numbered questions", r"question\s*\d|\bq\d+\b"),
    ("company position per question", r"position|proposal|we propose"),
    ("supporting data reference", r"see\s+|section\s+\d|table\s+\d|appendix"),
    ("development status", r"development status|programme status|program status"),
    ("regulatory history", r"previous (?:meeting|interaction)|regulatory history"),
]


def run(ns) -> Report:
    text = read(ns.package).lower()
    report = Report(tool="align_questions")
    report.count("required elements", len(REQUIRED))

    present = 0
    for name, pattern in REQUIRED:
        if re.search(pattern, text):
            present += 1
        else:
            report.add(Finding(
                rule="required-element-absent",
                severity="Major",
                item=name,
                observed="not found",
                expected="an explicit statement addressing this item",
                locator="whole document",
                detail="Absence is reported as absence. A missing element is not assumed "
                       "to be covered elsewhere or intentionally omitted.",
            ))
    report.count("elements present", present)

    # The question bank, which this script is documented as vendoring and did not
    # read. SKILL.md step 5 says it "vendors the shared question bank"; until
    # 2026-08-06 the script checked six hardcoded structural elements and never
    # opened the bank, so a package could omit every question the bank asks and
    # still score six of six. The denominator was real but it was the wrong one.
    bank_path = Path(ns.bank) if ns.bank else DEFAULT_BANK
    if not bank_path.is_file():
        report.cannot_assess(
            "question-bank coverage",
            f"question bank not found at {bank_path}",
            "the vendored bank at assets/qbr-question-bank.md",
        )
        return report

    questions = [
        line.lstrip("-* ").strip()
        for line in bank_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.lstrip().startswith(("- ", "* ")) and line.rstrip().endswith("?")
    ]
    report.count("bank questions", len(questions))
    if not questions:
        report.cannot_assess(
            "question-bank coverage",
            "the bank parsed to zero questions, so coverage would be vacuous",
            "a bank listing questions as '- ...?' bullets",
        )
        return report

    # A question counts as addressed when the package contains its distinctive
    # terms. Deliberately coarse and deliberately reported as a proportion with
    # its denominator, not as a pass.
    addressed = 0
    for question in questions:
        terms = [w for w in re.findall(r"[a-z]{5,}", question.lower())
                 if w not in STOPWORDS]
        if terms and sum(term in text for term in terms) >= max(2, len(terms) // 3):
            addressed += 1
    report.count("bank questions addressed", addressed)

    for question in questions:
        terms = [w for w in re.findall(r"[a-z]{5,}", question.lower())
                 if w not in STOPWORDS]
        if terms and sum(term in text for term in terms) < max(2, len(terms) // 3):
            report.add(Finding(
                rule="bank-question-unaddressed",
                severity="Major",
                item=question[:90],
                observed="no matching content found in the package",
                expected="a position or an explicit statement that it is out of scope",
                locator="whole document",
                detail="Reported as unaddressed, not as absent from the bank. Whether "
                       "the question applies to this programme is a judgement for the "
                       "author; this check only says the package does not answer it.",
            ))

    if present == 0:
        report.cannot_assess(
            "coverage assessment",
            "none of the expected elements were found, which usually means the wrong "
            "document was supplied",
            "the document this checker targets",
        )
    return report


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--package", required=True, help="document text")
    parser.add_argument("--bank", help="question bank (defaults to the vendored assets/ copy)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args()
    report = run(ns)
    print(report.render(as_json=ns.json))
    return 1 if any(f.severity == "Critical" for f in report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
