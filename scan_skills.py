#!/usr/bin/env python3
"""Scan every skill package for content that must never ship.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

    python3 scan_skills.py            # scan skills/ and shared/
    python3 scan_skills.py --path X   # scan somewhere else

Why this sits at the repository root
------------------------------------
A visitor deciding whether to install 151 packages authored by a stranger wants
to know what is checked before it reaches them. A scanner buried in `scripts/`
answers that question only for someone already reading the build. This one is
visible where the decision is made.

It is deliberately narrow. It does **not** replace `gitleaks` or `trufflehog`,
which run over the whole tree and its history at the push gate. This checks the
four things that are specific to *skill packages* and that a generic secret
scanner has no opinion about:

  1. Machine-specific absolute paths, which leak a filesystem layout and break
     for everyone else.
  2. Patient-level or subject-identifiable field names in fixtures.
  3. Prompt-injection shapes in package bodies — a skill is instructions, so a
     package that tells an agent to ignore its safety rules is a supply-chain
     problem, not a typo.
  4. Contact details and named individuals in what should be synthetic material.

Denominator
-----------
Every run prints files scanned, bytes read, and findings by category. A scan
that reads zero bytes and reports success is the failure mode this repository
has already met once (2026-08-05, the release-asset scan), so the byte count is
printed whether or not anything is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

#: Text-bearing files inside a package. Binary assets are counted, not read.
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".csv", ".tsv"}

#: (category, compiled pattern, one-line explanation shown on a hit)
CHECKS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "machine-path",
        re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
        "an absolute path from someone's machine — breaks on every other machine",
    ),
    (
        "patient-data",
        re.compile(
            r"\b(?:USUBJID|SUBJID|PATID|RFSTDTC|DTHDTC|BRTHDTC)\b"
        ),
        "a subject-identifiable CDISC field; fixtures must be synthetic by construction",
    ),
    (
        "prompt-injection",
        re.compile(
            r"(?i)\b(?:ignore (?:all |any )?(?:previous|prior|above) instructions"
            r"|disregard (?:the )?(?:system|safety|previous)"
            r"|you are now (?:in )?developer mode"
            r"|reveal your (?:system )?prompt)\b"
        ),
        "an instruction that would subvert the host agent's own rules",
    ),
    (
        "contact-detail",
        re.compile(
            r"[A-Za-z0-9._%+-]+@(?!example\.(?:com|org)\b)"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        ),
        "an email address that is not on a reserved example domain",
    ),
]

#: Paths that legitimately contain a pattern above, each with a reason. An
#: allowlist entry is a claim that needs justifying, so it carries one.
ALLOW: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"^scan_skills\.py$"),
        "*",
        "this file defines the patterns it would otherwise match",
    ),
    (
        re.compile(r"^scan_pr_skills\.py$"),
        "*",
        "imports the patterns from this file",
    ),
]


#: A prohibition verb near a quoted injection string means the text is *forbidding*
#: the attack, not attempting it. This repository's own `untrusted-content.md`
#: policy quotes "ignore previous instructions" in order to ban it.
PROHIBITION = re.compile(
    r"(?i)\b(?:do not obey|not obey|never obey|record its locator|record the locator"
    r"|treat .{0,30}as evidence|evidence,? not instructions|ignore embedded"
    r"|must not|do not follow|refuse|reads? \*?\"|says \"|occupies the same channel)\b"
)

#: The injection string wrapped in quotes — straight, curly, or backtick.
QUOTED = re.compile(r"[\"“”'`]")


def classify(line: str, category: str) -> str:
    """Return 'bare' (a real finding) or 'quoted-prohibition' (documentation).

    Only `prompt-injection` is context-sensitive. A machine path or a subject
    identifier is a defect regardless of the prose around it, so those always
    return 'bare'.

    The distinction matters because the alternative — allowlisting the policy
    files by path — would stop scanning them, and a policy file is exactly where
    an attacker would want an instruction to sit unread. Here the file stays
    scanned; only the classification changes, and quoted hits are still counted
    and printed so the number never silently drops to zero.
    """
    if category != "prompt-injection":
        return "bare"
    if QUOTED.search(line) and PROHIBITION.search(line):
        return "quoted-prohibition"
    return "bare"


def allowed(rel: str, category: str) -> str | None:
    for pattern, cat, reason in ALLOW:
        if pattern.search(rel) and cat in ("*", category):
            return reason
    return None


def scan(paths: list[Path]) -> int:
    files = 0
    binaries = 0
    total_bytes = 0
    findings: list[tuple[str, str, int, str]] = []
    by_category: Counter[str] = Counter()
    allowed_hits: Counter[str] = Counter()
    documented: Counter[str] = Counter()

    # Accept both directories (release scan) and individual files (PR scan).
    # Globbing a file path yields nothing, so a file-list caller would silently
    # scan zero bytes and then fail on the empty-target check below — which reads
    # like a broken gate rather than a broken call. Handle both explicitly.
    targets: list[Path] = []
    for base in paths:
        if not base.exists():
            print(f"FAILED: {base} does not exist — nothing was scanned")
            return 1
        if base.is_file():
            targets.append(base)
        else:
            targets.extend(p for p in sorted(base.rglob("*")) if p.is_file())

    if not targets:
        print(f"FAILED: no files found under {', '.join(str(p) for p in paths)}")
        return 1

    for path in targets:
        rel = str(path.relative_to(ROOT))
        if "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            binaries += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            binaries += 1
            continue
        files += 1
        total_bytes += len(text)
        for line_no, line in enumerate(text.splitlines(), 1):
            for category, pattern, why in CHECKS:
                if pattern.search(line):
                    reason = allowed(rel, category)
                    if reason:
                        allowed_hits[category] += 1
                        continue
                    if classify(line, category) == "quoted-prohibition":
                        documented[category] += 1
                        continue
                    by_category[category] += 1
                    findings.append((rel, category, line_no, why))

    print(
        f"\nSkill scan: {files} text file(s) read, {total_bytes:,} bytes, "
        f"{binaries} binary/undecodable file(s) counted but not read"
    )
    for category, _pattern, _why in CHECKS:
        print(f"  {by_category[category]:5d} finding(s)  {category}")
    for category, count in sorted(documented.items()):
        print(
            f"  {count:5d} quoted in a prohibition, not a finding  {category}"
            "  (still scanned — the file is not exempted, only this line's reading)"
        )
    for category, count in sorted(allowed_hits.items()):
        print(f"  {count:5d} allowlisted  {category}")

    if findings:
        print(f"\nFAILED: {len(findings)} finding(s)")
        for rel, category, line_no, why in findings:
            print(f"- {rel}:{line_no}  [{category}] {why}")
        return 1

    print(f"PASS: 0 findings across {files} file(s) / {total_bytes:,} bytes")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--path",
        action="append",
        type=Path,
        help="scan this path instead of the defaults (repeatable)",
    )
    args = parser.parse_args()
    paths = args.path or [ROOT / "skills", ROOT / "shared"]
    return scan([p if p.is_absolute() else ROOT / p for p in paths])


if __name__ == "__main__":
    sys.exit(main())
