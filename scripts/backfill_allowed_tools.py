#!/usr/bin/env python3
"""Declare `allowed-tools` on every package, derived from evidence in the package.

Least privilege (PS-D030 D-A10): a package declares the capabilities its
instructions actually use, and nothing more. The declaration is derived rather
than guessed:

  Read            every skill reads supplied documents — universal
  Bash            only when the package ships scripts/ that its body runs
  Write           only when the body produces a file artifact

`--check` verifies without writing, so CI can assert the declaration still
matches the evidence after a package changes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

#: A body that PRODUCES a file artifact needs write capability.
#:
#: The first version matched a bare `DOCX` anywhere in the body, and immediately
#: mis-declared a read-only package as needing Write — because its *inputs* table
#: listed "PDF/DOCX" as an accepted input format. Reading a DOCX is not writing one.
#: A producing verb is now required, which is the property that actually implies the
#: capability.
WRITES = re.compile(
    r"\b(?:writes?|produces?|generates?|exports?|emits?|saves?)\b[^.\n]{0,40}"
    r"\b(?:file|docx|\.md\b|\.csv\b|document|report|deliverable)\b",
    re.IGNORECASE)


def derive(d: Path) -> str:
    body = (d / "SKILL.md").read_text(encoding="utf-8")
    tools = ["Read"]
    scripts = list((d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else []
    if scripts:
        tools.append("Bash")
    if WRITES.search(body):
        tools.append("Write")
    return " ".join(tools)


def main() -> int:
    check = "--check" in sys.argv
    changed, mismatched = [], []
    for d in sorted(SKILLS.iterdir()):
        p = d / "SKILL.md"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            mismatched.append(f"{d.name}: no frontmatter")
            continue
        want = derive(d)
        cur = re.search(r"^allowed-tools:(.*)$", m.group(1), re.MULTILINE)
        if cur and cur.group(1).strip() == want:
            continue
        if check:
            have = cur.group(1).strip() if cur else "<absent>"
            mismatched.append(f"{d.name}: declares {have!r}, evidence supports {want!r}")
            continue
        block = m.group(1)
        block = (re.sub(r"^allowed-tools:.*$", f"allowed-tools: {want}", block, flags=re.MULTILINE)
                 if cur else
                 re.sub(r"^(description:.*(?:\n(?![a-z-]+:).*)*)$",
                        rf"\1\nallowed-tools: {want}", block, count=1, flags=re.MULTILINE))
        p.write_text(f"---\n{block}\n---\n{text[m.end():]}", encoding="utf-8")
        changed.append(f"{d.name}: {want}")

    if check:
        if mismatched:
            print(f"FAILED: {len(mismatched)} package(s) whose allowed-tools does not "
                  f"match the capabilities their package shows:")
            for x in mismatched:
                print(f"  - {x}")
            return 1
        n = sum(1 for d in SKILLS.iterdir() if (d / "SKILL.md").exists())
        print(f"PASS: allowed-tools matches package evidence for {n}/{n} package(s)")
        return 0

    for c in changed:
        print(f"  {c}")
    print(f"declared allowed-tools on {len(changed)} package(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
