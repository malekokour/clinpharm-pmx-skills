#!/usr/bin/env python3
"""Re-derive every measurable public claim and check the surfaces that state it.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why this exists (FIX-08 / PS-D027 D-L12)
----------------------------------------
This repository publishes counts across several surfaces — README, ROADMAP, the
site, the catalog — and they drift. Not hypothetically: on 2026-08-11 the README
carried a dated sentence reading *"21 evaluation suites, 214 cases, 1,095
assertions, 147 declared inputs, 63 portable scripts, and 191 repository tests"*.
Five of those six numbers were already wrong, and the sentence carried the
current date, which made it read as freshly verified.

That is the exact failure the product's own credibility rule exists to prevent,
occurring in the product's own front door.

So no count is written by hand. Each is **re-derived from its source of record**,
and the surfaces that state it are checked against the derivation.

Sources of record
-----------------
    packages, released, built   collections/*/collection.json
    suites, cases, assertions   evals/*/suite.yaml and evals/*/cases/*.yaml
    declared inputs             `inputs:` entries across the case files
    portable scripts            skills/*/scripts/*.py
    repository tests            `def test_*` across tests/*.py

Counting is textual and stdlib-only on purpose: this gate must run on a clean
checkout with nothing installed, exactly like `validate_repo.py`. The test count
is a static count of test methods rather than a unittest discovery, and it was
verified equal to what `make test` reports (211 = 211) at the time of writing —
if the two ever diverge, the static count is the one to fix.

What it does not do
-------------------
It checks **numbers**, not adjectives. "Building THE library" versus "we are THE
place" is a positioning claim governed by the Vision and the owner gate, and no
script should be trusted to adjudicate it. What this gate guarantees is narrower
and checkable: no public surface states a count that its source of record
contradicts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
#: Moved from `docs/` to the repository root on 2026-08-13 (S02.9). The ledger is
#: a trust artifact, and a visitor checking whether the numbers are honest should
#: not have to open a subdirectory to find it.
LEDGER = ROOT / "CLAIM-LEDGER.md"

#: Public surfaces allowed to state a **repository-wide** measured count. A count
#: appearing anywhere else is not policed here, which is why the list is explicit.
#:
#: `docs/CATALOG.md` is deliberately absent. It is generated from the collections
#: and states **per-package** figures — one package's `evidence_gap` mentions "42
#: cases", meaning that package's 42 selection cases, not the repository's. Adding
#: it here made the gate report that 42 should be 229, which would have been the
#: gate misreading a correct sentence. Its freshness is already gated by
#: `build_catalog_docs.py --check`.
CLAIM_SURFACES = ("README.md", "ROADMAP.md", "site/index.html")

#: Claim key -> the phrasing that introduces it on a public surface. Written as
#: "<number> <noun>" because that is how every current surface states them.
CLAIM_NOUNS = {
    "suites": r"evaluation suites?",
    "cases": r"cases?",
    "assertions": r"assertions?",
    "inputs": r"declared inputs?",
    "scripts": r"portable scripts?",
    "tests": r"repository tests?",
    # Map nouns. The README states these on its first screen, so they are the
    # numbers most likely to be quoted and least likely to be re-derived.
    "tasks": r"(?:tasks?(?: in the job model)?|task pages?)",
    "carried": r"[Cc]arried by a skill(?: today)?",
    "uncarried": r"[Nn]ot yet carried",
}


def measure() -> dict[str, int]:
    """Re-derive every measurable claim from its source of record."""
    facts: dict[str, int] = {}

    released = built = 0
    for catalog in sorted((ROOT / "collections").glob("*/collection.json")):
        for entry in json.loads(catalog.read_text(encoding="utf-8"))["skills"]:
            status = entry.get("status")
            if status == "released":
                released += 1
            elif status == "built":
                built += 1
    facts["released"] = released
    facts["built"] = built
    facts["packages"] = released + built

    suites = sorted((ROOT / "evals").glob("*/suite.yaml"))
    facts["suites"] = len(suites)

    # Map counts, added 2026-08-13 with the map itself.
    #
    # The README now states 167 tasks / 53 carried / 114 not yet on its first
    # screen. Those are exactly the numbers a reader would quote back, and until
    # this block existed the ledger gate policed nine counts while the three most
    # prominent ones on the page were unchecked. Derived from the same source of
    # record the map generator reads, so a ledger edit moves the gate and the
    # page together or fails the build.
    ledger = ROOT / "catalog" / "job-model-167.tsv"
    if ledger.exists():
        with ledger.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh, delimiter="\t"))
        facts["tasks"] = len(rows)
        facts["carried"] = sum(1 for r in rows if r.get("current_disposition") == "skill")
        facts["uncarried"] = len(rows) - facts["carried"]

    cases = assertions = inputs = 0
    for suite in suites:
        for case in sorted((suite.parent / "cases").glob("*.yaml")):
            cases += 1
            text = case.read_text(encoding="utf-8")
            # One assertion per list item under mechanical: / judged:. Counted
            # textually rather than by parsing YAML so this stays stdlib-only.
            in_assertions = False
            for line in text.splitlines():
                if re.match(r"^assertions:", line):
                    in_assertions = True
                    continue
                if in_assertions and line and not line.startswith(" "):
                    in_assertions = False
                if in_assertions and re.match(r"^\s{4}- ", line):
                    assertions += 1
            # Declared inputs sit under an `inputs:` key, one quoted path per
            # line. Scoped to that block rather than matched loosely: a bare
            # "ends in .md" pattern also swept up prose bullets elsewhere in the
            # file and reported 0 against the suite checker's 147.
            in_inputs = False
            for line in text.splitlines():
                if re.match(r"^inputs:", line):
                    in_inputs = True
                    continue
                if in_inputs:
                    if re.match(r"^\s+- ", line):
                        inputs += 1
                    elif line.strip():
                        in_inputs = False
    facts["cases"] = cases
    facts["assertions"] = assertions
    facts["inputs"] = inputs

    facts["scripts"] = len(sorted((ROOT / "skills").glob("*/scripts/*.py")))
    facts["tests"] = sum(
        len(re.findall(r"^\s+def test_\w+", path.read_text(encoding="utf-8"), re.MULTILINE))
        for path in sorted((ROOT / "tests").glob("*.py"))
    )
    return facts


#: The status table on the README, which states the two numbers a visitor
#: actually reads. Policed separately because it is a **table**, not a
#: "<number> <noun>" sentence — and on 2026-08-11 it sat at "1 released / 21
#: built / Total 22" while every prose count on the same page was correct and
#: green. The most prominent claim on the front page was the one the gate could
#: not see.
STATUS_ROW = re.compile(
    r"^\|\s*(?:`(?P<status>released|built)`|\*\*Total\*\*)\s*\|\s*\*\*(?P<value>[\d,]+)\*\*",
    re.MULTILINE,
)


def stated_claims(text: str) -> dict[str, list[int]]:
    """Extract every claim this gate knows how to police.

    Two shapes, because public surfaces use both:

      prose  "167 tasks", "211 repository tests"      -> <number> <noun>
      table  "| Tasks in the job model | **167** |"   -> <noun> | <number>

    The table form was added 2026-08-13 after the prose matcher was caught
    reporting ``PASS: 14/14`` while a hand-edited table cell said 99 where the
    source said 114. The gate had found fourteen claims and checked them; the
    one that was wrong simply was not among them, because a table states its
    noun *before* its number and the pattern only understood the other order.

    That is the failure this gate exists to prevent, occurring inside the gate:
    a count of things checked is not a count of things checkable, and the
    README's most prominent numbers live in tables.
    """
    found: dict[str, list[int]] = {}
    for key, noun in CLAIM_NOUNS.items():
        for match in re.finditer(rf"([\d,]+)\s+{noun}\b", text, re.IGNORECASE):
            value = int(match.group(1).replace(",", ""))
            found.setdefault(key, []).append(value)
        # Table row: | <noun> | <value> |  — optional bold/backticks on either.
        table = rf"\|\s*\**\s*{noun}\s*\**\s*\|\s*\**\s*([\d,]+)\s*\**\s*\|"
        for match in re.finditer(table, text, re.IGNORECASE):
            value = int(match.group(1).replace(",", ""))
            found.setdefault(key, []).append(value)
    for match in STATUS_ROW.finditer(text):
        key = match.group("status") or "packages"
        value = int(match.group("value").replace(",", ""))
        found.setdefault(key, []).append(value)
    return found


def render(facts: dict[str, int]) -> str:
    rows = "\n".join(
        f"| `{key}` | **{value:,}** | {source} |"
        for key, value, source in (
            ("packages", facts["packages"], "`collections/*/collection.json`"),
            ("released", facts["released"], "`collections/*/collection.json`"),
            ("built", facts["built"], "`collections/*/collection.json`"),
            ("suites", facts["suites"], "`evals/*/suite.yaml`"),
            ("cases", facts["cases"], "`evals/*/cases/*.yaml`"),
            ("assertions", facts["assertions"], "`evals/*/cases/*.yaml`"),
            ("inputs", facts["inputs"], "`evals/*/cases/*.yaml`"),
            ("scripts", facts["scripts"], "`skills/*/scripts/*.py`"),
            ("tests", facts["tests"], "`tests/*.py`"),
        )
    )
    return f"""# Claim ledger

**Generated by `scripts/check_claim_ledger.py`. Do not edit by hand.**

Every number this project states publicly is re-derived here from its source of
record, and `make check` fails if any public surface disagrees.

## Measured

| Claim | Value | Source of record |
|---|---:|---|
{rows}

## What the two status words mean

`released` — the package exists, validates, and has passed **the structural
gates and its assigned qualification route** (PS-D024, risk-tiered: a paired-run
dossier per package plus explicit owner authorization).
`built` — the package exists and validates, and **its assigned gate has not been
run**. It carries an `evidence_gap` saying so.

**Name the gate.** `released` does **not** mean clinical validation, and it does
**not** mean the evaluation suite has qualified the package's behaviour. Three
`blocker`-severity findings against that suite are open and frozen, so
evaluation-gate qualification is explicitly incomplete. Writing *"passes every
gate"* anywhere is prohibited for exactly this reason.

> This paragraph previously read: *"`released` — the package's evaluation gate
> has been run and passed."* That was an overclaim on a published surface, and a
> circular one: [`AGENTS.md`](AGENTS.md) correctly says evaluation-gate
> qualification is incomplete **and cites this file as the source** — so the
> document carrying the caveat pointed at the document denying it. Corrected
> toward `AGENTS.md`, whose wording was already right. Recorded rather than
> silently swapped, because the failure mode is a claim that gets stronger each
> time it is restated one document further from its evidence.

A `built` package is not a promise. The distinction is the whole of this
project's credibility, and it is why the ledger reports both numbers rather
than one total.

## What this ledger does not police

Positioning language. Whether the project says *"building THE library"* or
*"we are THE place"* is governed by the Vision and by an owner gate, not by a
script. This file guarantees something narrower and checkable: **no public
surface states a count that its source of record contradicts.**

## Surfaces checked

{chr(10).join(f'- `{s}`' for s in CLAIM_SURFACES)}

A count stated anywhere outside these surfaces is not policed here.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public claims against sources")
    parser.add_argument("--check", action="store_true", help="verify, do not write")
    args = parser.parse_args()

    facts = measure()
    problems: list[str] = []
    checked = 0

    for name in CLAIM_SURFACES:
        path = ROOT / name
        if not path.is_file():
            problems.append(f"claim surface missing: {name}")
            continue
        for key, values in stated_claims(path.read_text(encoding="utf-8")).items():
            for value in values:
                checked += 1
                if value != facts[key]:
                    problems.append(
                        f"{name}: states {value:,} {key}; the source of record "
                        f"says {facts[key]:,}"
                    )

    payload = render(facts)
    if args.check:
        if not LEDGER.is_file():
            problems.append("CLAIM-LEDGER.md does not exist")
        elif LEDGER.read_text(encoding="utf-8") != payload:
            problems.append(
                "CLAIM-LEDGER.md is stale — regenerate with "
                "scripts/check_claim_ledger.py"
            )
    else:
        LEDGER.write_text(payload, encoding="utf-8")
        print(f"wrote {LEDGER.relative_to(ROOT)}")

    summary = " · ".join(f"{k} {v:,}" for k, v in facts.items())
    print(
        f"\nClaim ledger: {len(CLAIM_SURFACES)} surface(s), {checked} stated "
        f"count(s) checked against {len(facts)} derived fact(s)"
    )
    print(f"  {summary}")

    if problems:
        print(f"\nFAILED: {len(problems)} claim problem(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"PASS: {checked}/{checked} stated public count(s) match their source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
