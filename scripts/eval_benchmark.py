#!/usr/bin/env python3
"""Aggregate repeated evaluation runs and run the analyst pass.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library

Produces ``benchmark.json`` in skill-creator's published shape — the review
viewer reads ``configuration``, and ``pass_rate`` nested under ``result``,
exactly — plus ``analysis.md``, which is the part that decides whether a number
means anything.

REQ-SC-007 names four things the analyst pass must detect, and each exists
because of a way a benchmark can look good while proving nothing:

**Non-discriminating assertions** pass in both configurations every time. They
inflate both pass rates and measure nothing about the skill. The CSR benchmark
already carries a real instance of this shape — "Output is a PDF file" in
skill-creator's own example.

**Shared failures** fail in both configurations. They are usually a defect in
the assertion, not in the skill.

**Variance** across repeated runs. A single run cannot distinguish a real
improvement from one lucky sample, which is why the repository refused to quote
an aggregate figure from its one-run CSR script-path measurement.

**Cost outliers** — a run far off the median in tokens or seconds.

Standard deviation is the **population** form (divide by n), not the sample
form, because these runs are the whole set being described rather than a sample
drawn from a larger population. With the run counts involved — typically three —
the two differ enough to matter, so the choice is stated rather than left to the
reader to infer.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_schema import CONFIGURATIONS, check_grading

#: A run more than this many times the median is reported as a cost outlier.
OUTLIER_FACTOR = 2.0

#: Runs needed before variance is meaningful enough to comment on.
MIN_RUNS_FOR_VARIANCE = 3


def describe(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": round(statistics.fmean(values), 4),
        "stddev": round(statistics.pstdev(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def collect(workspace: Path) -> list[dict[str, Any]]:
    """Read every graded run in the workspace into the viewer's run shape."""
    runs: list[dict[str, Any]] = []
    for eval_dir in sorted(workspace.glob("eval-*")):
        name = eval_dir.name[len("eval-") :]
        for configuration in CONFIGURATIONS:
            for run_dir in sorted((eval_dir / configuration).glob("run-*")):
                grading_path = run_dir / "grading.json"
                if not grading_path.is_file():
                    continue
                grading = json.loads(grading_path.read_text(encoding="utf-8"))
                problems = check_grading(grading)
                if problems:
                    raise SystemExit(f"{grading_path}: invalid grading.json: {problems}")
                summary = grading["summary"]
                timing = grading.get("timing", {})
                metrics = grading.get("execution_metrics", {})
                runs.append(
                    {
                        "eval_id": name,
                        "eval_name": name,
                        "configuration": configuration,
                        "run_number": int(run_dir.name.split("-")[-1]),
                        "result": {
                            "pass_rate": summary["pass_rate"],
                            "passed": summary["passed"],
                            "failed": summary["failed"],
                            "total": summary["total"],
                            "time_seconds": timing.get("total_duration_seconds") or 0.0,
                            "tokens": timing.get("total_tokens") or 0,
                            "tool_calls": metrics.get("total_tool_calls", 0),
                            "errors": metrics.get("errors_encountered", 0),
                        },
                        "expectations": grading["expectations"],
                        "notes": [],
                    }
                )
    return runs


def analyse(runs: list[dict[str, Any]]) -> list[str]:
    """The analyst pass. Returns human-readable notes, most consequential first."""
    notes: list[str] = []
    if not runs:
        return ["No graded runs found: nothing was measured."]

    by_config: dict[str, list[dict[str, Any]]] = {c: [] for c in CONFIGURATIONS}
    for run in runs:
        by_config.setdefault(run["configuration"], []).append(run)

    # --- non-discriminating and shared-failure assertions ---------------------
    verdicts: dict[str, dict[str, list[bool]]] = {}
    for run in runs:
        for item in run["expectations"]:
            slot = verdicts.setdefault(item["text"], {c: [] for c in CONFIGURATIONS})
            slot.setdefault(run["configuration"], []).append(bool(item["passed"]))

    non_discriminating, shared_failures = [], []
    for text, sides in verdicts.items():
        with_side, without_side = sides.get("with_skill", []), sides.get("without_skill", [])
        if not with_side or not without_side:
            continue
        if all(with_side) and all(without_side):
            non_discriminating.append(text)
        if not any(with_side) and not any(without_side):
            shared_failures.append(text)

    if non_discriminating:
        notes.append(
            f"{len(non_discriminating)} assertion(s) pass in BOTH configurations in every "
            "run, so they do not discriminate and inflate both pass rates: "
            + "; ".join(f"{text!r}" for text in sorted(non_discriminating)[:5])
        )
    if shared_failures:
        notes.append(
            f"{len(shared_failures)} assertion(s) fail in BOTH configurations in every run "
            "— usually a defect in the assertion rather than in the skill: "
            + "; ".join(f"{text!r}" for text in sorted(shared_failures)[:5])
        )

    # --- variance -------------------------------------------------------------
    for configuration, group in by_config.items():
        per_eval: dict[str, list[float]] = {}
        for run in group:
            per_eval.setdefault(run["eval_name"], []).append(run["result"]["pass_rate"])
        for name, rates in sorted(per_eval.items()):
            if len(rates) < MIN_RUNS_FOR_VARIANCE:
                notes.append(
                    f"{name} / {configuration}: {len(rates)} run(s) — fewer than "
                    f"{MIN_RUNS_FOR_VARIANCE}, so variance is not estimated and no "
                    "aggregate claim may be quoted from it."
                )
                continue
            spread = statistics.pstdev(rates)
            if spread > 0.15:
                notes.append(
                    f"{name} / {configuration}: high variance across runs "
                    f"({statistics.fmean(rates):.2f} +/- {spread:.2f}, "
                    f"range {min(rates):.2f}-{max(rates):.2f}) — may be flaky."
                )

    # --- cost outliers --------------------------------------------------------
    for field in ("tokens", "time_seconds"):
        values = [run["result"][field] for run in runs if run["result"][field]]
        if len(values) >= MIN_RUNS_FOR_VARIANCE:
            middle = statistics.median(values)
            for run in runs:
                value = run["result"][field]
                if middle and value > middle * OUTLIER_FACTOR:
                    notes.append(
                        f"cost outlier: {run['eval_name']} / {run['configuration']} "
                        f"run {run['run_number']} used {value} {field} against a median "
                        f"of {middle} (>{OUTLIER_FACTOR}x)."
                    )

    if not notes:
        notes.append(
            "No non-discriminating assertions, shared failures, high variance or cost "
            f"outliers found across {len(runs)} run(s). This is a bounded check, not a "
            "statement that the suite is sound."
        )
    return notes


def build(workspace: Path, skill: str) -> dict[str, Any]:
    runs = collect(workspace)
    summary: dict[str, Any] = {}
    for configuration in CONFIGURATIONS:
        group = [r for r in runs if r["configuration"] == configuration]
        summary[configuration] = {
            "pass_rate": describe([r["result"]["pass_rate"] for r in group]),
            "time_seconds": describe([r["result"]["time_seconds"] for r in group]),
            "tokens": describe([float(r["result"]["tokens"]) for r in group]),
        }
    delta = {}
    for field in ("pass_rate", "time_seconds", "tokens"):
        difference = (
            summary["with_skill"][field]["mean"] - summary["without_skill"][field]["mean"]
        )
        delta[field] = f"{difference:+.4g}"
    summary["delta"] = delta

    return {
        "metadata": {
            "skill_name": skill,
            "workspace": str(workspace),
            "evals_run": sorted({r["eval_name"] for r in runs}),
            "runs_per_configuration": max(
                (r["run_number"] for r in runs), default=0
            ),
            "stddev": "population (n), not sample (n-1)",
        },
        "runs": runs,
        "run_summary": summary,
        "notes": analyse(runs),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    benchmark = build(workspace, args.skill_name)
    if not benchmark["runs"]:
        print(f"FAILED: no graded runs under {workspace}; nothing to aggregate")
        return 1

    target = args.output or workspace / "benchmark.json"
    target.write_text(json.dumps(benchmark, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = workspace / "analysis.md"
    lines = [f"# Analyst pass — {args.skill_name}", ""]
    lines.append(f"Runs aggregated: **{len(benchmark['runs'])}**")
    for configuration in CONFIGURATIONS:
        stats = benchmark["run_summary"][configuration]["pass_rate"]
        lines.append(
            f"- `{configuration}` pass rate {stats['mean']} +/- {stats['stddev']} "
            f"(range {stats['min']}-{stats['max']})"
        )
    lines += ["", "## Findings", ""]
    lines += [f"- {note}" for note in benchmark["notes"]]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"PASS: aggregated {len(benchmark['runs'])} run(s) -> {target}")
    for note in benchmark["notes"]:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
