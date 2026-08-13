"""Assemble the judged assertions a practitioner must score, with their outputs.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Why this exists
---------------
Judged assertions fail closed. That is correct — an unscored assertion must never
count as a pass — but it means the practitioner gate is the only route to any
promotion, and until 2026-08-06 that gate was not merely unmet, it was
*unreachable*: 62 of the 119 cases had never been run, so there was no output for
anyone to score. "Blocked on the practitioner" was hiding "blocked on us".

This script turns the gate into something a person can actually sit down and do:
it pairs every judged assertion with the response that has to be read to score it,
groups them so one skill's outputs are read once rather than seven times, and
writes a review form with the fields the grader requires.

It refuses to include a case with no run, and says so with a count, rather than
silently emitting a shorter bundle — a review pack that quietly covers less than
it claims is the same defect as a check that scans zero files.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from eval_schema import load_case

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", required=True, help="Workspace holding <skill>/<case>/run-1/")
    parser.add_argument("--out", required=True, help="Directory to write the bundle into")
    args = parser.parse_args()

    runs = pathlib.Path(args.runs)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    included: dict[str, list[dict]] = {}
    no_run: list[str] = []
    judged_total = 0

    for case_path in sorted((ROOT / "evals").glob("*/cases/*.yaml")):
        skill = case_path.parent.parent.name
        case = load_case(case_path.read_text(encoding="utf-8"), str(case_path))
        judged = case["assertions"].get("judged", [])
        if not judged:
            continue
        response = runs / skill / case_path.stem / "run-1/outputs/response.md"
        if not response.is_file() or response.stat().st_size == 0:
            no_run.append(f"{skill}/{case_path.stem}")
            continue
        included.setdefault(skill, []).append(
            {
                "case": case_path.stem,
                "layer": case["layer"],
                "prompt": case["prompt"],
                "response": str(response),
                "assertions": judged,
            }
        )
        judged_total += len(judged)

    form = {
        "instructions": "One entry per assertion. All fields required. An assertion "
                        "with no entry is recorded as FAILED, never skipped.",
        "adjudications": [
            {
                "skill": skill,
                "case": entry["case"],
                "assertion": assertion,
                "verdict": "",
                "reviewer": "",
                "date": "",
                "quote": "",
                "reason": "",
            }
            for skill, entries in sorted(included.items())
            for entry in entries
            for assertion in entry["assertions"]
        ],
    }
    (out / "judged-review-FORM.json").write_text(
        json.dumps(form, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Judged assertions awaiting adjudication",
        "",
        (f"**{judged_total} assertions across {sum(len(v) for v in included.values())} "
         f"cases in {len(included)} packages.** Every one currently counts as FAILED, "
         "because an unscored assertion must never be assumed to pass."),
        "",
    ]
    if no_run:
        lines += [
            (f"> **{len(no_run)} case(s) are excluded because no run exists for them.** "
             "They cannot be scored and are not silently dropped from the denominator:"),
            "",
            *(f"> - `{n}`" for n in no_run),
            "",
        ]
    else:
        lines += ["Every case with judged assertions has a run. Nothing is excluded.", ""]

    for skill, entries in sorted(included.items()):
        lines += [f"## {skill}", ""]
        for entry in entries:
            lines += [
                f"### {entry['case']}  ·  layer: {entry['layer']}",
                "",
                f"**Prompt:** {entry['prompt']}",
                "",
                f"**Response:** `{entry['response']}`",
                "",
                "Score each of these:",
                "",
                *(f"- [ ] {a}" for a in entry["assertions"]),
                "",
            ]
    (out / "REVIEW-PACK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"bundle written to {out}")
    print(f"  packages: {len(included)}")
    print(f"  cases:    {sum(len(v) for v in included.values())}")
    print(f"  judged assertions to score: {judged_total}")
    print(f"  cases excluded for having no run: {len(no_run)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
