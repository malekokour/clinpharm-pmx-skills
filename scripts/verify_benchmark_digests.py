#!/usr/bin/env python3
"""Verify recorded benchmark outputs against their published SHA-256 digests.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: Python standard library
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = ROOT / "benchmark/results/2026-07-30-codex"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    scores_path = RESULT_ROOT / "scores.json"
    payload = json.loads(scores_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0
    for run in payload["runs"]:
        run_index = int(run["run"])
        for score_key, file_name in (("baseline", "baseline.md"), ("working_pack", "context.md")):
            path = RESULT_ROOT / f"run-{run_index:02d}" / file_name
            expected = run[score_key]["sha256"]
            observed = sha256(path)
            checked += 1
            if observed != expected:
                failures.append(
                    f"{path.relative_to(ROOT)}: expected {expected}, observed {observed}"
                )
    if failures:
        print(f"FAILED: {len(failures)} of {checked} benchmark digests differ")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: {checked}/{checked} benchmark output digests match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
