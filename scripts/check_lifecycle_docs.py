#!/usr/bin/env python3
"""Check that the lifecycle runbook names things that actually exist.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why (FIX-09 / PS-D027 D-L6)
---------------------------
`docs/LIFECYCLE.md` tells a user how to install, update, roll back and uninstall
this library. A runbook is worth exactly as much as its commands are runnable,
and the failure mode is silent: a script gets renamed, the runbook keeps naming
the old path, and nobody finds out until someone follows it.

So every repository path and every `python3 scripts/…` command the runbook names
is resolved against the tree. A renamed script fails the build.

What this cannot check, and says so
-----------------------------------
Whether the **Claude UI steps** work. Those need Malek's own account, so they are
an owner step. This gate deliberately does not imply otherwise: it verifies the
deterministic half and the runbook itself states that the UI half is UNVERIFIED
against the current library.

The distinction is the whole point. A gate that reported "lifecycle verified"
from a documentation check would be the exact overclaim this repository exists
to avoid.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "LIFECYCLE.md"

#: `python3 scripts/<name>.py` invocations inside fenced blocks or prose.
SCRIPT_CALL = re.compile(r"python3\s+(scripts/[\w./-]+\.py)")

#: Backticked repository paths. Restricted to the directories this repository
#: actually has, so prose like `SKILL.md` or a shell flag is not mistaken for one.
REPO_PATH = re.compile(r"`((?:scripts|skills|docs|evals|collections|catalog)/[\w./<>-]+)`")

#: The runbook must keep saying which parts are not verified. If this sentence is
#: ever edited away, the gate should notice — a runbook that quietly starts
#: reading as fully tested is worse than one that was never written.
REQUIRED_HONESTY = ("UNVERIFIED", "owner step")


def main() -> int:
    if not RUNBOOK.is_file():
        print(f"FAILED: {RUNBOOK.relative_to(ROOT)} does not exist")
        return 1

    text = RUNBOOK.read_text(encoding="utf-8")
    # Collapse whitespace before any phrase check. The first version of this gate
    # searched the raw text for "owner step" and went red because the phrase
    # happened to wrap across a line — the same phrase-brittleness recorded as
    # B23 for the eval assertions, reproduced here in the gate written to prevent
    # that class of problem. A doc gate that fails on line wrapping teaches people
    # to reword documents to suit the checker, which is backwards.
    flat = re.sub(r"\s+", " ", text)
    problems: list[str] = []
    checked = 0

    for script in sorted(set(SCRIPT_CALL.findall(text))):
        checked += 1
        if not (ROOT / script).is_file():
            problems.append(f"runbook invokes a script that does not exist: {script}")

    for raw in sorted(set(REPO_PATH.findall(text))):
        # Placeholders like skills/<id>/ are intentional; resolve the parent.
        target = ROOT / raw.split("<")[0].rstrip("/")
        checked += 1
        if not target.exists():
            problems.append(f"runbook names a path that does not exist: {raw}")

    for phrase in REQUIRED_HONESTY:
        checked += 1
        if phrase not in flat:
            problems.append(
                f"runbook no longer contains {phrase!r} — the Claude UI steps are "
                "still untested against the current library and the document must "
                "keep saying so"
            )

    covered = [
        operation
        for operation in ("Install", "Update", "Roll back", "Uninstall")
        if re.search(rf"^#+\s+{operation}\b", text, re.MULTILINE)
    ]
    checked += 4

    print(
        f"\nLifecycle runbook: {checked} reference(s) checked; "
        f"{len(covered)}/4 operations documented ({', '.join(covered) or 'none'})"
    )
    print("  not covered here (needs the owner's host accounts): the Claude UI steps")

    if len(covered) < 4:
        problems.append(
            "runbook does not document all four operations: "
            "install, update, roll back, uninstall"
        )

    if problems:
        print(f"\nFAILED: {len(problems)} lifecycle runbook problem(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("PASS: every path and script the lifecycle runbook names exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
