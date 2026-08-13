#!/usr/bin/env python3
"""Prove every vendored module still matches its canonical source.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only — this gate must run from a clean
checkout with nothing installed.

Why this exists
---------------
Every vendored copy under ``skills/*/scripts/`` carries this banner::

    VENDORED at build time from shared/scripts/ — do not edit here.
    Edit the canonical source and rebuild; a freshness check compares them.

**That check did not exist.** ``check_generated_freshness.py`` compares
Markdown to DOCX and nothing else, so the banner promised a guarantee no code
provided — the same shape of defect as a scanner that reports success over zero
files, except here the false claim was shipped inside the product.

It was not hypothetical. On 2026-08-06 the B19 severity fix was applied to
``shared/scripts/cross_document_consistency.py`` and the skill kept emitting the
old classification, because the CLI imports its vendored copy. Two further
copies were found already drifted, from a linter reformatting the canonical
sources after they had been vendored.

Vendoring is the right call — it is what makes a package install standalone —
but a copy is only safe when something compares it to its original.

Comparison method
-----------------
The banner is stripped from the copy and the remainder must be **byte
identical** to the canonical file. Not "close", not "same functions": a
vendored module that differs at all has diverged, and which difference matters
is not a judgement this gate should be making.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "shared" / "scripts"

BANNER = (
    "VENDORED at build time from shared/scripts/ — do not edit here.\n"
    "Edit the canonical source and rebuild; a freshness check compares them.\n\n"
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    if not CANONICAL.is_dir():
        print(f"FAILED: no canonical source directory at {CANONICAL.relative_to(ROOT)}")
        return 1

    problems: list[str] = []
    checked = 0
    packages: set[str] = set()

    for copy in sorted(ROOT.glob("skills/*/scripts/*.py")):
        canonical = CANONICAL / copy.name
        if not canonical.is_file():
            continue  # a package-local script with no canonical source
        checked += 1
        packages.add(copy.parent.parent.name)
        body = copy.read_text(encoding="utf-8")

        if BANNER not in body:
            problems.append(
                f"{copy.relative_to(ROOT)}: vendored from shared/scripts/{copy.name} but "
                "carries no vendoring banner, so nothing tells a reader not to edit it"
            )
            stripped = body
        else:
            stripped = body.replace(BANNER, "", 1)

        if digest(stripped) != digest(canonical.read_text(encoding="utf-8")):
            problems.append(
                f"{copy.relative_to(ROOT)}: has drifted from "
                f"shared/scripts/{copy.name}. Re-vendor from the canonical source; "
                "do not reconcile by editing the copy"
            )

    if checked == 0:
        # Discovery can legitimately return nothing, and "0 checked" must never
        # read as "all fresh" — the failure this whole file exists to prevent.
        print("FAILED: no vendored modules found under skills/*/scripts/")
        return 1

    if problems:
        print(f"FAILED: {len(problems)} vendoring problem(s) across {checked} copies")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(
        f"PASS: {checked} vendored module(s) across {len(packages)} package(s) are "
        "byte-identical to their canonical source in shared/scripts/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
