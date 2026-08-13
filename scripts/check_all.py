#!/usr/bin/env python3
"""Run every portable local quality gate for ClinPharm PMx Skills.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: Python standard library plus project dependencies
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> None:
    print(f"\n== {label} ==", flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    python = sys.executable
    run("Repository contract", [python, "scripts/validate_repo.py"])
    run("Benchmark digests", [python, "scripts/verify_benchmark_digests.py"])
    run("Owed DOCX present", [python, "scripts/build_docs.py", "--check"])
    run("Catalog Markdown freshness", [python, "scripts/build_catalog_docs.py", "--check"])
    run("Markdown/DOCX parity", [python, "scripts/check_docx_parity.py"])
    run("Generated artifact freshness", [python, "scripts/check_generated_freshness.py"])
    run("Evaluation suites", [python, "scripts/eval_suite_check.py"])
    run("Defect assertion shape", [python, "scripts/check_defect_assertion_shape.py"])
    run("Vendored module freshness", [python, "scripts/check_vendored.py"])
    run("Skill routing partition", [python, "scripts/check_routing.py"])
    run("Nav registry field contract", [python, "scripts/check_nav_registry.py"])
    run("Nav registry is regenerable", [python, "scripts/build_nav_registry.py"])
    # Vision v1.2 gates (PS-D029/030/031). Each was proven able to fail against a
    # planted input before being wired in — see
    # _ADMIN/2-Dev/1-Evidence/2026-08-11-v12-gate-canary-proofs.md
    run("v1.2 gates", [python, "scripts/check_v12_gates.py"])
    run("allowed-tools matches package evidence",
        [python, "scripts/backfill_allowed_tools.py", "--check"])
    # Generated surfaces. Both derive from a source of record, so a stale output
    # means someone edited a derived file or forgot to regenerate.
    run("Paste blocks current", [python, "scripts/build_paste_blocks.py", "--check"])
    run("Published map current", [python, "scripts/build_map_site.py", "--check"])
    run("Map is current and honest", [python, "scripts/check_map.py"])
    run("README counts synced", [python, "scripts/sync_readme_counts.py", "--check"])
    run("Router scale fixtures", [python, "scripts/build_scale_fixtures.py", "--check"])
    run("Router selection cases", [python, "scripts/check_router_selection.py"])
    run("Public claim ledger", [python, "scripts/check_claim_ledger.py", "--check"])
    # The ledger above checks every number. This checks the claims that are not
    # numbers — the gap that let CLAIM-LEDGER.md assert the evaluation gate had
    # passed while AGENTS.md cited it saying the opposite, with every count on
    # both pages correct throughout.
    run("Claim consistency", [python, "scripts/check_claim_consistency.py"])
    run("Lifecycle runbook", [python, "scripts/check_lifecycle_docs.py"])
    run("Static site gates", [python, "scripts/check_site_gates.py"])
    run("Fixture grounding", [python, "scripts/check_fixture_grounding.py"])
    run("Fixture arithmetic", [python, "scripts/check_fixture_arithmetic.py"])
    run("Portable frontmatter", [python, "scripts/check_portable_frontmatter.py"])
    run("Package portability", [python, "scripts/check_portability.py"])
    run("Contract tests", [python, "-m", "unittest", "discover", "-s", "tests", "-v"])
    run("Public-release privacy scan", [python, "scripts/privacy_scan.py"])
    run(
        "Python compilation",
        [
            python,
            "-m",
            "compileall",
            "-q",
            "scripts",
            "tests",
        ],
    )
    print("\nPASS: all ClinPharm PMx Skills quality gates completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
