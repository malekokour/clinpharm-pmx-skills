#!/usr/bin/env python3
"""Score a skill description's activation behaviour.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library

PS-D024 scales activation evidence by consequence. LOW uses at least 3 queries
and one trial, MEDIUM at least 10 and two trials, and HIGH description
optimization uses at least 20 and three trials. An ordinary qualification run
scores the declared balanced corpus directly. Train/validation/fresh-holdout
splits are required when wording is being optimized or routing ambiguity is
being resolved, because that is when overfitting becomes a live risk.

What this scores, and what it does not
--------------------------------------
This tool does **not** decide whether a skill fires. A host does that. It
consumes *recorded decisions* — one boolean per (query, run) — and turns them
into the two numbers that matter, keeping them separate:

**Under-triggering** is a positive query that did not fire: the skill exists and
was not used. **Over-triggering** is a near-miss that did fire: the skill was
used where a neighbour should have been. They are different failures with
different fixes — a narrow description causes the first, a broad one the second
— and a single "accuracy" number hides which is happening. The promotion gate
asks for accuracy against *named neighbours*, so the neighbour is recorded per
query rather than left implicit.

The split exists because a description tuned until it scores well on the same
queries used to tune it has been fitted, not measured. Train drives revision;
validation is looked at once per iteration; the holdout is written last, by
someone who has not seen the description, and is read once.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

TRAIN_FRACTION = 0.6

#: PS-D024 activation defaults. Repetition counts distinguish ordinary
#: qualification from wording optimization, where overfitting and routing
#: ambiguity justify a third HIGH trial.
PROFILE_REQUIREMENTS = {
    "LOW": {"queries": 3, "qualification_runs": 1, "optimization_runs": 1},
    "MEDIUM": {"queries": 10, "qualification_runs": 2, "optimization_runs": 2},
    "HIGH": {"queries": 20, "qualification_runs": 2, "optimization_runs": 3},
}


def profile_requirements(profile: str, mode: str = "qualification") -> tuple[int, int]:
    """Return minimum query and run counts for one PS-D024 profile and mode."""
    rule = PROFILE_REQUIREMENTS[profile]
    return rule["queries"], rule[f"{mode}_runs"]


def split(queries: list[dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    """Deterministic 60/40 split, stratified so both halves hold both kinds.

    Deterministic on purpose: a random split reshuffles what "validation" means
    on every run, so a description could be revised until a lucky split flattered
    it. Interleaving by index keeps the split stable across iterations.
    """
    train: list[dict] = []
    validation: list[dict] = []
    for kind in ("positive", "near_miss"):
        group = [q for q in queries if q["kind"] == kind]
        cut = round(len(group) * TRAIN_FRACTION)
        train.extend(group[:cut])
        validation.extend(group[cut:])
    return train, validation


def score(queries: list[dict[str, Any]], decisions: dict[str, list[bool]]) -> dict[str, Any]:
    """Score one set of queries against recorded decisions.

    A query with no recorded decision is a hole in the measurement, not a pass.
    It is counted and reported, and it makes the result incomplete.
    """
    under: list[str] = []
    over: list[dict[str, Any]] = []
    unrecorded: list[str] = []
    positives = near_misses = 0
    fired_positive = correct_near_miss = 0

    for query in queries:
        runs = decisions.get(query["query"])
        if not runs:
            unrecorded.append(query["query"])
            continue
        # Majority across repeated runs; a description that fires inconsistently
        # is reported through `flaky` rather than silently rounded.
        fired = sum(1 for value in runs if value) > len(runs) / 2
        flaky = 0 < sum(1 for value in runs if value) < len(runs)
        if query["kind"] == "positive":
            positives += 1
            if fired:
                fired_positive += 1
            else:
                under.append(query["query"])
        else:
            near_misses += 1
            if fired:
                over.append(
                    {"query": query["query"], "neighbour": query.get("neighbour", "unnamed")}
                )
            else:
                correct_near_miss += 1
        query["flaky"] = flaky

    total = positives + near_misses
    return {
        "positives": positives,
        "near_misses": near_misses,
        "unrecorded": unrecorded,
        "recall": round(fired_positive / positives, 4) if positives else None,
        "near_miss_rejection": (
            round(correct_near_miss / near_misses, 4) if near_misses else None
        ),
        "accuracy": (
            round((fired_positive + correct_near_miss) / total, 4) if total else None
        ),
        "under_triggering": under,
        "over_triggering": over,
        "flaky": [q["query"] for q in queries if q.get("flaky")],
    }


def report(label: str, result: dict[str, Any], threshold: float) -> bool:
    """Print one split's result. Returns True when it passes."""
    total = result["positives"] + result["near_misses"]
    print(f"\n## {label} — {total} queries "
          f"({result['positives']} positive, {result['near_misses']} near-miss)")
    if result["unrecorded"]:
        print(f"  INCOMPLETE: {len(result['unrecorded'])} query(ies) have no recorded "
              f"decision: {result['unrecorded'][:3]}")
        return False
    if total == 0:
        print("  FAILED: no queries — an empty split cannot pass")
        return False
    print(f"  recall (positives that fired):        {result['recall']}")
    print(f"  near-miss rejection:                  {result['near_miss_rejection']}")
    print(f"  accuracy:                             {result['accuracy']}")
    for query in result["under_triggering"]:
        print(f"  UNDER-TRIGGER: {query!r} did not fire")
    for item in result["over_triggering"]:
        print(f"  OVER-TRIGGER:  {item['query']!r} fired; belongs to {item['neighbour']}")
    for query in result["flaky"]:
        print(f"  FLAKY: {query!r} did not fire consistently across runs")
    if result["recall"] is None or result["near_miss_rejection"] is None:
        print("  FAILED: both positive and near-miss queries are required")
        return False
    return (
        result["recall"] >= threshold
        and result["near_miss_rejection"] >= threshold
        and not result["flaky"]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", type=Path, help="JSON: [{query, kind, neighbour?}]")
    parser.add_argument("--decisions", type=Path, required=True,
                        help="JSON: {query: [bool, bool, bool]} — one entry per run")
    parser.add_argument("--holdout", type=Path, default=None)
    parser.add_argument("--holdout-decisions", type=Path, default=None)
    parser.add_argument("--threshold", type=float, default=0.90)
    parser.add_argument(
        "--profile", choices=sorted(PROFILE_REQUIREMENTS), default="HIGH"
    )
    parser.add_argument(
        "--mode",
        choices=("qualification", "optimization"),
        default="qualification",
        help="Optimization requires train/validation and a fresh holdout.",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Override the PS-D024 profile default when variance requires it.",
    )
    args = parser.parse_args()

    queries = json.loads(args.queries.read_text(encoding="utf-8"))
    decisions = json.loads(args.decisions.read_text(encoding="utf-8"))

    min_queries, profile_runs = profile_requirements(args.profile, args.mode)
    expected_runs = args.runs or profile_runs
    if expected_runs < profile_runs:
        print(
            f"FAILED: {args.profile} requires at least {profile_runs} run(s) per query; "
            f"requested {expected_runs}"
        )
        return 1

    for query, runs in decisions.items():
        if len(runs) != expected_runs:
            print(f"FAILED: {query!r} has {len(runs)} recorded run(s), expected {expected_runs}")
            return 1

    if len(queries) < min_queries:
        print(f"FAILED: {len(queries)} queries; {args.profile} requires at least {min_queries}. "
              "A rate over fewer reads stronger than it is.")
        return 1

    if args.mode == "qualification":
        if args.holdout or args.holdout_decisions:
            print(
                "FAILED: --holdout is an optimization input; use --mode optimization "
                "or omit the holdout arguments"
            )
            return 1
        passed = report("qualification", score(queries, decisions), args.threshold)
    else:
        train_set, validation_set = split(queries)
        passed = report("train", score(train_set, decisions), args.threshold)
        passed &= report("validation", score(validation_set, decisions), args.threshold)

        if args.holdout and args.holdout_decisions:
            holdout = json.loads(args.holdout.read_text(encoding="utf-8"))
            holdout_decisions = json.loads(
                args.holdout_decisions.read_text(encoding="utf-8")
            )
            for query, runs in holdout_decisions.items():
                if len(runs) != expected_runs:
                    print(
                        f"FAILED: holdout {query!r} has {len(runs)} recorded run(s), "
                        f"expected {expected_runs}"
                    )
                    return 1
            passed &= report(
                "holdout", score(holdout, holdout_decisions), args.threshold
            )
        else:
            print("\n## holdout — NOT SUPPLIED")
            print(
                "  Optimization without a fresh holdout measures a description "
                "against queries it may have been tuned on."
            )
            passed = False

    print(
        f"\n{'PASS' if passed else 'FAILED'}: {args.profile} {args.mode} activation "
        f"threshold {args.threshold} over {len(queries)} queries x "
        f"{expected_runs} run(s)"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
