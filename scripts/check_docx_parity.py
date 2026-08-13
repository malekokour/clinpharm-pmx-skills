#!/usr/bin/env python3
"""Verify that canonical Markdown content survives DOCX generation.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-29
Dependencies: Python standard library
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

#: Where a generated DOCX may legitimately live beside its Markdown source.
PAIR_ROOTS = ("docs/archive/starter", "examples")


def discover_pairs() -> list[tuple[Path, Path]]:
    """Every Markdown file that has a generated DOCX beside it.

    Discovery, not a hard-coded list. The list held three pairs while four
    existed: `make docs` built `starter/review-csr-pk-consistency/`'s DOCX and
    nothing ever compared it to its source. A skill promoted to `released`
    gained a starter and the parity gate did not notice, which is the failure
    mode a hard-coded tuple always eventually has — it describes the repository
    on the day someone typed it.

    Pairing on `X.md` / `X.docx` means a new pair is covered the moment it is
    generated, and a DOCX whose source has been deleted becomes visible as a
    missing source rather than silently dropping out of the denominator.
    """
    pairs: list[tuple[Path, Path]] = []
    for base in PAIR_ROOTS:
        directory = ROOT / base
        if not directory.is_dir():
            continue
        for generated in sorted(directory.rglob("*.docx")):
            pairs.append((generated.with_suffix(".md"), generated))
    return pairs


PAIRS = tuple(discover_pairs())


def markdown_body(text: str) -> str:
    """Remove presentation-only Markdown syntax while retaining content."""
    if text.startswith("---\n"):
        _, _, text = text.partition("\n---\n")
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s*#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text, flags=re.MULTILINE)
    text = text.replace("```markdown", "").replace("```", "")
    return text.translate(str.maketrans("", "", "`*~|"))


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    return " ".join(
        node.text or "" for node in root.iter(f"{{{WORD_NS}}}t")
    )


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[._/%<>-][A-Za-z0-9]+)*", text.casefold())


def missing_ordered_tokens(source: list[str], generated: list[str]) -> list[str]:
    cursor = 0
    missing: list[str] = []
    for token in source:
        while cursor < len(generated) and generated[cursor] != token:
            cursor += 1
        if cursor == len(generated):
            missing.append(token)
            if len(missing) == 8:
                break
        else:
            cursor += 1
    return missing


def main() -> int:
    if not PAIRS:
        # Discovery makes an empty result possible in a way a hard-coded tuple
        # never was, and "verified for 0 pairs" would exit 0 while proving
        # nothing. The denominator is the check.
        print("FAILED: no Markdown/DOCX pairs discovered under " + ", ".join(PAIR_ROOTS))
        return 1
    failures: list[str] = []
    for source, generated in PAIRS:
        if not source.is_file() or not generated.is_file():
            failures.append(f"missing pair: {source.name} / {generated.name}")
            continue
        missing = missing_ordered_tokens(
            tokens(markdown_body(source.read_text(encoding="utf-8"))),
            tokens(docx_text(generated)),
        )
        if missing:
            failures.append(
                f"{generated.relative_to(ROOT)} lost or reordered tokens: "
                + ", ".join(missing)
            )
        else:
            print(f"PASS: {source.relative_to(ROOT)} -> {generated.relative_to(ROOT)}")
    if failures:
        print(f"FAILED: {len(failures)} Markdown/DOCX parity error(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: Markdown/DOCX content parity verified for {len(PAIRS)} pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
