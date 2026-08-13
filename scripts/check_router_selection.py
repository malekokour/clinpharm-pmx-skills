#!/usr/bin/env python3
"""Execute the deterministic library-router selection cases as a gate.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why this is separate from ``scripts/eval_suite_check.py``
---------------------------------------------------------
``eval_suite_check.py`` answers a *structural* question about PS-D028 suites:
are the case files well formed, and does each suite belong to its package. It
never runs anything, because the suites it validates need a model in the loop.

The router is different in kind. ``scripts/library_router.py`` is a pure
function over ``catalog/nav_registry.json`` and a settings dict, so "does it
pick the right skill" is decided by *calling it*, not by grading prose. Running
it here means the answer holds on a clean checkout with nothing installed, and
means a scoring change that breaks selection fails the build rather than
surviving until someone notices.

That is also why ``evals/library-router/`` deliberately carries no
``suite.yaml``: a PS-D028 suite would announce a model-graded evaluation that
does not exist. ``library-router`` is ``built``, and ``validate_repo.py`` only
requires a suite of ``released`` packages, so the absence is the honest state.

What it reports
---------------
Denominators, not adjectives. Every run prints how many cases executed, the
top-1 accuracy over the SINGLE class with its denominator, and the per-class
tallies — so "the router works" can be read as "21 of 21 SINGLE requests
resolved to the declared package" rather than as an assertion about an unknown
population.

Proving the gate can fail
-------------------------
A gate nobody has seen go red is untested. Change any ``expect.chosen`` in
``selection-cases.json`` to another package id and re-run: the case is reported
as a mismatch with both the expected and the observed value, and the exit code
is 1. Restore the file and it returns to green. Evidence for the run that was
actually performed lives under
``_ADMIN/2-Dev/1-Evidence/`` in the private workspace.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from library_router import load_registry, load_settings, load_statuses, select

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "library-router" / "selection-cases.json"

#: Keys that describe a profile to a human rather than configuring the router.
PROFILE_NOTE_KEYS = frozenset({"note"})

#: Every expectation key this runner knows how to check. An unrecognised key is
#: an error rather than an ignored field: a typo'd ``chosen`` would otherwise
#: silently remove the only assertion a case makes, which is the same class of
#: defect as a scanner that reads zero bytes.
EXPECT_KEYS = frozenset(
    {"decision", "chosen", "complexity", "reason_contains", "candidates_exclude"}
)


def build_settings(profile: dict[str, Any]) -> dict[str, Any]:
    """Overlay one profile onto the shipped settings file."""
    settings = load_settings()
    for key, value in profile.items():
        if key in PROFILE_NOTE_KEYS:
            continue
        settings[key] = value
    return settings


def check_case(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    """Return one message per failed expectation; empty list means the case passed."""
    expect = case["expect"]
    unknown = set(expect) - EXPECT_KEYS
    if unknown:
        return [f"unknown expectation key(s): {sorted(unknown)}"]

    failures: list[str] = []
    if "decision" in expect and result["decision"] != expect["decision"]:
        failures.append(
            f"decision: expected {expect['decision']!r}, observed {result['decision']!r}"
        )
    if "chosen" in expect and result["chosen"] != expect["chosen"]:
        failures.append(
            f"chosen: expected {expect['chosen']!r}, observed {result['chosen']!r}"
        )
    if "complexity" in expect and result["complexity"] != expect["complexity"]:
        failures.append(
            f"complexity: expected {expect['complexity']!r}, "
            f"observed {result['complexity']!r}"
        )
    for reason in expect.get("reason_contains", []):
        if reason not in result["reasons"]:
            failures.append(
                f"reason {reason!r} absent; observed reasons {result['reasons']}"
            )
    for excluded in expect.get("candidates_exclude", []):
        if excluded in result["candidates"]:
            failures.append(
                f"candidate {excluded!r} should have been excluded; "
                f"observed candidates {result['candidates']}"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print one line per case, not only the failures",
    )
    args = parser.parse_args()

    if not args.cases.is_file():
        print(f"FAILED: selection cases not found at {args.cases}")
        return 1

    document = json.loads(args.cases.read_text(encoding="utf-8"))
    profiles = document.get("profiles") or {}
    cases = document.get("cases") or []
    if not cases:
        print(f"FAILED: {args.cases} declares no cases")
        return 1

    # Loaded once so every case is scored against the same registry and the same
    # status map. Reloading per case would let a mid-run edit split the suite.
    registry = load_registry()
    statuses = load_statuses()

    identifiers: set[str] = set()
    failures: list[tuple[str, list[str]]] = []
    by_class: Counter[str] = Counter()
    single_hits = 0
    single_total = 0

    for case in cases:
        case_id = case["id"]
        if case_id in identifiers:
            failures.append((case_id, ["duplicate case id"]))
            continue
        identifiers.add(case_id)

        profile_name = case["profile"]
        if profile_name not in profiles:
            failures.append((case_id, [f"unknown profile {profile_name!r}"]))
            continue

        result = select(
            case["utterance"],
            settings=build_settings(profiles[profile_name]),
            skills=registry,
            statuses=statuses,
        )
        problems = check_case(case, result)
        by_class[case["class"]] += 1
        if case["class"] == "SINGLE":
            single_total += 1
            if not problems:
                single_hits += 1
        if problems:
            failures.append((case_id, problems))
        elif args.verbose:
            print(
                f"  ok  {case_id:16s} {profile_name:20s} "
                f"{result['decision']:7s} {result['chosen']}"
            )

    print(
        f"\nRouter selection: {len(cases)} case(s) across "
        f"{len(profiles)} profile(s), registry of {len(registry)} package(s)"
    )
    for class_name, count in sorted(by_class.items()):
        print(f"  {class_name:12s} {count}")
    if single_total:
        print(
            f"  top-1 accuracy (SINGLE class): {single_hits}/{single_total} "
            f"= {single_hits / single_total:.0%}"
        )

    if failures:
        print(f"\nFAILED: {len(failures)} of {len(cases)} selection case(s)")
        for case_id, problems in failures:
            for problem in problems:
                print(f"- {case_id}: {problem}")
        return 1

    print(f"PASS: {len(cases)}/{len(cases)} selection case(s) matched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
