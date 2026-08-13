#!/usr/bin/env python3
"""Enforce the portability claim: standard frontmatter keys, no host-only syntax.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why this exists
---------------
The product describes portable packages as a differentiator. A differentiator
that nothing enforces is a preference, and the finding
`2026-08-11-docs-portability-claim-unenforced` says so plainly: *"the vision
claims portable packages as a differentiator, and nothing enforces it."*

Two halves, both now checked with denominators:

1. **Frontmatter keys.** The open Agent Skills standard defines six: ``name``,
   ``description``, ``license``, ``compatibility``, ``metadata``,
   ``allowed-tools``. A seventh key makes the package non-portable to any host
   that validates strictly — the standard's own error message reads
   *"Unexpected key(s) in SKILL.md frontmatter"*.
2. **Body syntax.** A body carrying host-specific template or context syntax
   (`{{var}}`, `@workspace`, `#codebase`, `${CLAUDE_…}`) reads correctly on one
   host and is noise or breakage everywhere else.

Why a separate gate when `validate_repo.py` already checks the keys
-------------------------------------------------------------------
It checks them and **says nothing about how many it checked**. The finding's own
requirement is explicit: *"a run reporting `checked 0` fails rather than passes."*
That is the failure mode this repository keeps meeting — a check that reports
success over a population it never examined — and the fix is a denominator, not
another key comparison.

This gate therefore duplicates the key check on purpose, and adds the count. If
the two ever disagree about what is allowed, that disagreement is the bug.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: The six keys the open standard defines. Kept in sync with
#: `validate_repo.FRONTMATTER_ROOT_KEYS`; a divergence is a defect in one of them.
STANDARD_KEYS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)

#: Host-specific syntax. Each entry names the host family it belongs to, so a
#: finding tells the author *why* the string is a portability problem rather than
#: only that it matched.
HOST_ONLY_SYNTAX = (
    (re.compile(r"\{\{\s*[A-Za-z_][\w.]*\s*\}\}"), "handlebars-style template variable"),
    (re.compile(r"(?<![\w`])@workspace\b"), "Copilot workspace context reference"),
    (re.compile(r"(?<![\w`])#codebase\b"), "Copilot codebase context reference"),
    (re.compile(r"\$\{CLAUDE_[A-Z_]+\}"), "Claude Code environment interpolation"),
    (re.compile(r"(?<![\w`])@terminal\b"), "host terminal context reference"),
)


def frontmatter_keys(text: str) -> tuple[list[str], str | None]:
    """Return top-level frontmatter keys, or an error describing why it failed."""
    if not text.startswith("---\n"):
        return [], "no opening frontmatter delimiter"
    end = text.find("\n---", 4)
    if end == -1:
        return [], "no closing frontmatter delimiter"
    keys: list[str] = []
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        if ":" not in line:
            return keys, f"frontmatter line is not a key/value pair: {line!r}"
        keys.append(line.split(":", 1)[0].strip())
    return keys, None


def main() -> int:
    packages = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    if not packages:
        print("FAILED: no packages found under skills/*/SKILL.md — nothing was checked")
        return 1

    problems: list[str] = []
    keys_checked = bodies_checked = 0

    for directory in packages:
        skill_id = directory.name
        text = (directory / "SKILL.md").read_text(encoding="utf-8")

        keys, error = frontmatter_keys(text)
        if error:
            problems.append(f"{skill_id}: {error}")
        else:
            keys_checked += 1
            for key in keys:
                if key not in STANDARD_KEYS:
                    problems.append(
                        f"{skill_id}: frontmatter key {key!r} is outside the open "
                        f"standard. Allowed: {', '.join(sorted(STANDARD_KEYS))}"
                    )

        bodies_checked += 1
        body = text[text.find("\n---", 4) + 4 :] if "\n---" in text else text
        for pattern, description in HOST_ONLY_SYNTAX:
            for match in pattern.finditer(body):
                problems.append(
                    f"{skill_id}: body contains {description}: {match.group()!r} — "
                    "this reads correctly on one host and breaks portability"
                )

    print(
        f"\nPortable frontmatter: {len(packages)} package(s) found, "
        f"{keys_checked} frontmatter block(s) parsed, {bodies_checked} body(ies) "
        f"scanned for {len(HOST_ONLY_SYNTAX)} host-only syntax pattern(s)"
    )

    if keys_checked == 0:
        problems.append(
            "0 frontmatter blocks were parsed — a portability claim cannot rest "
            "on a check that examined nothing"
        )

    if problems:
        print(f"\nFAILED: {len(problems)} portability problem(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(
        f"PASS: {keys_checked}/{len(packages)} packages carry only standard "
        f"frontmatter keys and no host-only body syntax"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
