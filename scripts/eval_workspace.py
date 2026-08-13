#!/usr/bin/env python3
"""Create and inspect isolated paired evaluation workspaces.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Why the directories are built before anything runs
--------------------------------------------------
``_Protocol.md`` step 5 requires the with-skill and old-skill baseline runs to
be launched together and never to share model context, and step 7 requires
timing captured immediately. Both are properties of *how the run is staged*,
not of the model, so they are enforced here.

Each run directory is created empty, with the exact prompt and an input
manifest written alongside it. The executor fills ``outputs/``. That ordering
matters: a workspace laid out in advance makes an incomplete run visible as a
missing file rather than as a quietly smaller denominator.

The layout matches what skill-creator's ``aggregate_benchmark.py`` and
``eval-viewer/generate_review.py`` read — verified against their source, not
assumed::

    <workspace>/
      feedback.json
      eval-<case-id>/
        with_skill/run-1/{PROMPT.md, provenance.json, outputs/}
        without_skill/run-1/{PROMPT.md, provenance.json, outputs/}

Inventing a parallel layout would mean the official viewer could not open the
artifacts, which is exactly what REQ-SC-008 forbids.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_schema import (
    CONFIGURATIONS,
    PROFILE_CORE_RUNS,
    REQUIRED_RUN_FILES,
    load_case,
    load_suite,
)

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_suite(suite_dir: Path) -> tuple[dict[str, Any], list[tuple[Path, dict[str, Any]]]]:
    suite_path = suite_dir / "suite.yaml"
    if not suite_path.is_file():
        raise SystemExit(f"no suite.yaml at {suite_dir}")
    suite = load_suite(suite_path.read_text(encoding="utf-8"), str(suite_path))
    cases = []
    for path in sorted((suite_dir / "cases").glob("*.yaml")):
        cases.append((path, load_case(path.read_text(encoding="utf-8"), str(path))))
    if not cases:
        raise SystemExit(f"suite {suite['skill']} declares no cases")
    return suite, cases


def stage(
    suite_dir: Path,
    workspace: Path,
    runs: int | None,
    only: str | None = None,
) -> tuple[int, int, int]:
    """Create the paired run tree using the suite profile's run default."""
    suite, cases = read_suite(suite_dir)
    known_case_ids = {case["id"] for _, case in cases}
    if only and only not in known_case_ids:
        available = ", ".join(sorted(known_case_ids))
        raise SystemExit(
            f"requested case {only!r} does not exist in {suite['skill']}; "
            f"available cases: {available}"
        )
    run_count = runs or PROFILE_CORE_RUNS[suite["qualification_profile"]]
    workspace.mkdir(parents=True, exist_ok=True)

    staged = made = 0
    for case_path, case in cases:
        if only and case["id"] != only:
            continue
        staged += 1
        fixtures = {}
        for relative in case.get("inputs", []):
            fixture = suite_dir / relative
            if not fixture.is_file():
                raise SystemExit(
                    f"{case['id']}: declared input {relative} does not exist at {fixture}"
                )
            fixtures[relative] = sha256(fixture)

        for configuration in CONFIGURATIONS:
            for number in range(1, run_count + 1):
                run_dir = workspace / f"eval-{case['id']}" / configuration / f"run-{number}"
                (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
                made += 1

                # The prompt is written verbatim. The baseline condition differs
                # only in that the skill is absent — the task is identical, or
                # the comparison measures two different questions.
                (run_dir / "PROMPT.md").write_text(
                    f"# {case['id']} — {configuration}, run {number}\n\n"
                    f"{case['prompt'].strip()}\n\n"
                    + (
                        "## Supplied inputs\n\n"
                        + "".join(f"- `{name}`\n" for name in fixtures)
                        if fixtures
                        else "## Supplied inputs\n\nNone.\n"
                    )
                    + (
                        "\n> The expert key is never supplied to the model under "
                        "evaluation.\n"
                    ),
                    encoding="utf-8",
                )

                (run_dir / "provenance.json").write_text(
                    json.dumps(
                        {
                            "schema_version": "1.0",
                            "skill": suite["skill"],
                            "suite_version": suite["version"],
                            "case_id": case["id"],
                            "case_file": case_path.name,
                            "case_sha256": sha256(case_path),
                            "layer": case["layer"],
                            "mode": case.get("mode"),
                            "configuration": configuration,
                            "run_number": number,
                            "fixture_sha256": fixtures,
                            "skill_present": configuration == "with_skill",
                        },
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )

    feedback = workspace / "feedback.json"
    if not feedback.is_file():
        feedback.write_text(json.dumps({"feedback": {}}, indent=2) + "\n", encoding="utf-8")
    return staged, made, run_count


def inspect(workspace: Path) -> tuple[list[Path], list[Path]]:
    """Split staged run directories into complete and incomplete."""
    complete: list[Path] = []
    incomplete: list[Path] = []
    for run_dir in sorted(workspace.glob("eval-*/*/run-*")):
        if all((run_dir / name).is_file() for name in REQUIRED_RUN_FILES):
            complete.append(run_dir)
        else:
            incomplete.append(run_dir)
    return complete, incomplete


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    staged = sub.add_parser("stage", help="Create the empty paired run tree.")
    staged.add_argument("suite_dir", type=Path)
    staged.add_argument("--workspace", type=Path, required=True)
    staged.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Override PS-D024 profile default (LOW=1, MEDIUM=2, HIGH=3).",
    )
    staged.add_argument("--case", dest="only", default=None)

    checked = sub.add_parser("check", help="Report complete and incomplete runs.")
    checked.add_argument("workspace", type=Path)

    args = parser.parse_args()

    if args.command == "stage":
        if args.runs is not None and args.runs < 1:
            raise SystemExit("--runs must be at least 1")
        cases, dirs, run_count = stage(
            args.suite_dir.resolve(), args.workspace.resolve(), args.runs, args.only
        )
        print(
            f"PASS: staged {cases} case(s) x {len(CONFIGURATIONS)} configuration(s) "
            f"x {run_count} run(s) = {dirs} run directories in {args.workspace}"
        )
        return 0

    complete, incomplete = inspect(args.workspace.resolve())
    total = len(complete) + len(incomplete)
    if total == 0:
        # A workspace with nothing in it must not report a clean bill of health.
        print(f"FAILED: {args.workspace} contains no staged runs")
        return 1
    for run_dir in incomplete:
        missing = [n for n in REQUIRED_RUN_FILES if not (run_dir / n).is_file()]
        print(f"- incomplete {run_dir.relative_to(args.workspace)}: missing {missing}")
    print(
        f"{'PASS' if not incomplete else 'FAILED'}: {len(complete)}/{total} run(s) complete"
    )
    return 0 if not incomplete else 1


if __name__ == "__main__":
    raise SystemExit(main())
