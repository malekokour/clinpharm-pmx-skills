#!/usr/bin/env python3
"""Validate every evaluation suite against the PS-D028 contract.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Repository-wide and run-free: it checks that the suites are well formed, that
every declared input exists, and that each suite belongs to its own package.
It says nothing about whether a skill works — only that its evaluation material
is real. That distinction is the whole of `built` versus `released`.

The denominator is printed because a suite checker that finds no suites must not
report success. That is the shape of defect this repository keeps meeting.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_schema import SchemaError, load_case, load_suite

ROOT = Path(__file__).resolve().parents[1]
MIN_CASES = 7
MIN_ASSERTIONS = 3


def main() -> int:
    suites = sorted((ROOT / "evals").glob("*/suite.yaml"))
    if not suites:
        print("FAILED: no evaluation suites found under evals/*/suite.yaml")
        return 1

    problems: list[str] = []
    cases_seen = assertions_seen = inputs_seen = 0

    for suite_path in suites:
        directory = suite_path.parent
        label = directory.name
        try:
            suite = load_suite(suite_path.read_text(encoding="utf-8"), str(suite_path))
        except SchemaError as exc:
            problems.append(str(exc))
            continue

        if suite["skill"] != label:
            problems.append(
                f"{label}: suite.yaml declares skill '{suite['skill']}' but lives in "
                f"evals/{label}/ — a suite must belong to its package"
            )

        for required in ("README.md", "rubric.md"):
            if not (directory / required).is_file():
                problems.append(f"{label}: PS-D028 requires {required}")

        case_paths = sorted((directory / "cases").glob("*.yaml"))
        if len(case_paths) < MIN_CASES:
            problems.append(
                f"{label}: {len(case_paths)} case(s); at least {MIN_CASES} required"
            )

        identifiers: set[str] = set()
        for case_path in case_paths:
            try:
                case = load_case(case_path.read_text(encoding="utf-8"), str(case_path))
            except SchemaError as exc:
                problems.append(str(exc))
                continue
            cases_seen += 1
            if case["id"] in identifiers:
                problems.append(f"{label}: duplicate case id {case['id']!r}")
            identifiers.add(case["id"])

            assertions = case["assertions"]
            count = len(assertions.get("mechanical", [])) + len(assertions.get("judged", []))
            assertions_seen += count
            if count < MIN_ASSERTIONS:
                problems.append(
                    f"{label}/{case['id']}: {count} assertion(s); "
                    f"{MIN_ASSERTIONS} is the minimum"
                )
            for relative in case.get("inputs", []):
                inputs_seen += 1
                if not (directory / relative).is_file():
                    problems.append(
                        f"{label}/{case['id']}: declared input does not exist: {relative}"
                    )

    if problems:
        print(f"FAILED: {len(problems)} evaluation-suite error(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(
        f"PASS: {len(suites)} suite(s), {cases_seen} case(s), {assertions_seen} "
        f"assertion(s), {inputs_seen} declared input(s) — all present and well formed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
