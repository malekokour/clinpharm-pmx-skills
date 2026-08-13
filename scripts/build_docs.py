#!/usr/bin/env python3
"""Generate every DOCX the repository owes, derived from status.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: python-docx (via scripts/build_docx.py); Python standard library

The `docs` recipe previously named four Markdown/DOCX conversions by hand.
A hard-coded recipe describes the repository on the day someone typed it: when
`review-csr-pk-consistency` gained a starter, the recipe was updated and the
*parity check* was not, so a generated DOCX went unverified. Two hand-kept
lists of the same thing will always drift; the fix is to have neither.

What is owed, stated as a rule rather than a list:

- every `released` package with a `starter/<skill-id>/` directory owes a DOCX
  for each Markdown file in it;
- every example output that already has a DOCX owes a regenerated one.

`built` packages are excluded deliberately. A starter is a thing a user is
invited to pick up and run, and offering one for a package whose evaluation
gate has never passed is the same overclaim the status vocabulary exists to
prevent.

`--check` reports what would be built without building it, so the rule can be
inspected without a python-docx install.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from skill_status import released_ids

ROOT = Path(__file__).resolve().parents[1]


def owed() -> list[tuple[Path, Path]]:
    """Every (markdown, docx) pair this repository owes. Sorted, deduplicated."""
    pairs: set[tuple[Path, Path]] = set()

    for skill_id in released_ids(ROOT):
        starter = ROOT / "docs" / "archive" / "starter" / skill_id
        if not starter.is_dir():
            continue
        for markdown in starter.glob("*.md"):
            pairs.add((markdown, markdown.with_suffix(".docx")))

    examples = ROOT / "examples"
    if examples.is_dir():
        for generated in examples.rglob("*.docx"):
            source = generated.with_suffix(".md")
            if source.is_file():
                pairs.add((source, generated))

    return sorted(pairs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="List what is owed and verify it exists, without regenerating.",
    )
    args = parser.parse_args()

    pairs = owed()
    if not pairs:
        print("FAILED: nothing is owed a DOCX — expected example output pairs")
        return 1

    if args.check:
        missing = [markdown for markdown, generated in pairs if not generated.is_file()]
        for markdown, generated in pairs:
            state = "present" if generated.is_file() else "MISSING"
            print(f"  {state:<8} {generated.relative_to(ROOT)}")
        if missing:
            print(f"FAILED: {len(missing)} owed DOCX not generated; run `make docs`")
            return 1
        print(f"PASS: {len(pairs)} owed DOCX present, derived from status")
        return 0

    for markdown, generated in pairs:
        if not markdown.is_file():
            print(f"FAILED: owed source is missing: {markdown.relative_to(ROOT)}")
            return 1
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_docx.py"), str(markdown), str(generated)],
            check=False,
        )
        if completed.returncode:
            return completed.returncode
    print(f"PASS: generated {len(pairs)} DOCX, derived from status")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
