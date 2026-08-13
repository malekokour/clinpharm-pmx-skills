#!/usr/bin/env python3
"""Scan only the skill files a pull request touches, including forked PRs.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only, plus `git` on PATH

    python3 scan_pr_skills.py                  # diff against origin/main
    python3 scan_pr_skills.py --base <ref>     # diff against something else

Why this exists separately from `scan_skills.py`
------------------------------------------------
`scan_skills.py` reads the whole tree and is the right gate for a release. It is
the wrong gate for a pull request from a fork, for two reasons.

**Coverage is not the problem; blast radius is.** A contributor cannot be blocked
by a pre-existing finding somewhere else in the tree, or the first outside
contribution fails for reasons the contributor cannot fix. This scans exactly
what the PR changed.

**A forked PR is untrusted input by definition.** The whole point of a skill
library is that a package is *instructions an agent will follow*. A malicious
package is not a bug report, it is a supply-chain attack with a friendly
filename, and it arrives through the normal contribution path. That is why this
runs on `pull_request_target`-style intake rather than only on branches a
maintainer already controls.

What it does NOT do
-------------------
It does not fail on a finding in a file the PR did not touch. If the diff is
empty of skill files it reports that plainly and exits 0 — but it prints the
denominator, so "0 files changed" is visible rather than looking like a pass.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scan_skills import scan  # intentional: one source of patterns

#: Only these trees hold shippable package content. A PR touching `docs/` is not
#: skipped by accident — it is out of scope for *this* gate, and `make check`
#: still runs over it.
SCANNED_TREES = ("skills/", "shared/")


def changed_files(base: str) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        print(f"FAILED: could not diff against {base}: {exc.stderr.strip()}")
        raise SystemExit(1) from exc

    files = []
    for line in out.splitlines():
        if line.startswith(SCANNED_TREES):
            path = ROOT / line
            if path.is_file():
                files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/main", help="base ref to diff against")
    args = parser.parse_args()

    files = changed_files(args.base)
    print(
        f"PR skill scan: base={args.base} · "
        f"{len(files)} changed file(s) under {', '.join(SCANNED_TREES)}"
    )
    if not files:
        print("PASS: this pull request changes no skill or shared files — nothing to scan")
        return 0

    for path in files:
        print(f"  changed: {path.relative_to(ROOT)}")

    return scan(files)


if __name__ == "__main__":
    sys.exit(main())
