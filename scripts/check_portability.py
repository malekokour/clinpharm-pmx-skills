#!/usr/bin/env python3
"""Prove every package installs and runs with no repository present.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library

Why this is separate from ``build_release.py``
----------------------------------------------
The release builder packages **released** skills only — that is the honesty
gate P01 installed, and it must not be loosened. Portability is a different
question: *every* package on disk claims to be self-contained, including the
twenty whose qualification gate has not passed, and REQ-REL-003 asks for all
current packages to be installed in empty directories.

Conflating the two would force a choice between shipping unqualified packages
and never testing them. So this tool packages all current skills for **testing only**,
writes nothing to `dist/`, and produces no release artifact.

What "installs standalone" is taken to mean
-------------------------------------------
Extraction into an empty directory, with no repository root anywhere above it,
after which:

- ``SKILL.md``, ``README.md`` and ``LICENSE`` are present;
- every relative link inside the package resolves **within the extracted tree**
  — a link that only resolves in the repository is the defect this checks for;
- every shipped script answers ``--help`` with exit 0 and imports nothing from
  outside its own package.

The scripts are run because a package that ships a script it cannot execute has
promised something it does not deliver, and no amount of file-presence checking
detects that.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("SKILL.md", "README.md")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)#][^)]*)\)")


def package(skill: Path, target: Path) -> Path:
    archive_path = target / f"{skill.name}.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, str(path.relative_to(skill.parent)))
        archive.write(ROOT / "LICENSE", "LICENSE")
    return archive_path


def check_one(skill: Path) -> list[str]:
    problems: list[str] = []
    name = skill.name
    with tempfile.TemporaryDirectory(prefix=f"portability-{name}-") as temp:
        area = Path(temp)
        archive_path = package(skill, area)

        # Resolved, because on macOS the temporary directory lives under /var,
        # which is a symlink to /private/var. Comparing a resolved link target
        # against an unresolved root made every in-package link look like an
        # escape — 36 false positives before this was fixed.
        install = (area / "install").resolve()
        install.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path) as archive:
            for info in archive.infolist():
                member = Path(info.filename)
                if member.is_absolute() or ".." in member.parts:
                    problems.append(f"{name}: unsafe archive path {info.filename}")
                    return problems
            archive.extractall(install)

        extracted = install / name
        for required in (*REQUIRED,):
            if not (extracted / required).is_file():
                problems.append(f"{name}: extracted package lacks {required}")
        if not (install / "LICENSE").is_file():
            problems.append(f"{name}: extracted package lacks LICENSE")
        if problems:
            return problems

        # Links must resolve inside the extraction, not in the repository.
        for markdown in sorted(extracted.rglob("*.md")):
            for raw in LINK.findall(markdown.read_text(encoding="utf-8", errors="replace")):
                target = raw.strip().split(maxsplit=1)[0].strip("<>").split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (markdown.parent / target).resolve()
                try:
                    resolved.relative_to(install)
                except ValueError:
                    problems.append(
                        f"{name}: {markdown.relative_to(extracted)} links outside the "
                        f"installed package: {target}"
                    )
                    continue
                if not resolved.exists():
                    problems.append(
                        f"{name}: {markdown.relative_to(extracted)} has a dead link "
                        f"once installed: {target}"
                    )

        # Every shipped script must actually run from the extraction.
        for script in sorted((extracted / "scripts").glob("*.py")):
            completed = subprocess.run(
                [sys.executable, str(script), "--help"],
                capture_output=True,
                text=True,
                cwd=install,
                check=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip().splitlines()
                problems.append(
                    f"{name}: scripts/{script.name} --help exited "
                    f"{completed.returncode} with no repository present"
                    + (f" — {detail[-1]}" if detail else "")
                )
    return problems


def main() -> int:
    skills = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        print("FAILED: no packages found under skills/*/SKILL.md")
        return 1

    problems: list[str] = []
    scripts_run = 0
    for skill in skills:
        scripts_run += len(list((skill / "scripts").glob("*.py")))
        problems.extend(check_one(skill))

    if problems:
        print(f"FAILED: {len(problems)} portability problem(s) across {len(skills)} package(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(
        f"PASS: {len(skills)} package(s) built, extracted into empty directories with no "
        f"repository present, links resolved, and {scripts_run} shipped script(s) ran"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
