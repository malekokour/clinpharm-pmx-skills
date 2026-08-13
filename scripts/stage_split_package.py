#!/usr/bin/env python3
"""Stage a split package outside the library until its procedure is authored.

Maintainer-only. Staging lands under the private `_ADMIN/` tree, a sibling of
this repository that is not present in a public clone. The script exits if
that tree is missing; it will not create `_ADMIN` for you.

PS-D030 sets the grain at one job-model row per skill. Eleven shipped packages
carry several rows each, using "operating modes" — the construct PS-D030 retired.
Splitting them is therefore not a text carve: the scaffolding is reusable, the
procedure is not.

This script creates the reusable half and stops. The result lands in a **staging
directory outside `skills/`**, so:

  * the library never contains a package whose procedure is unwritten;
  * `built` keeps meaning "validates", not "exists as a folder";
  * the public count stays true while the authoring happens.

A staged package enters `skills/` only when a human has written its procedure and
it passes the same gates as every other package. Nothing here shortcuts that.

Usage:
    stage_split_package.py --parent review-ddi-evidence \\
        --id review-in-vitro-ddi-package --row "In-vitro DDI package"
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT.parent / (
    "_ADMIN/1-Docs/1-Canon/1-Product-Vision/Plans/1-L3-Library-Router-Relaunch/"
    "Artifacts/Split-Drafts"
)

#: Sections that transfer unchanged: they encode the product's boundaries, not the
#: job. Copying them is correct — every package owes the same refusals.
CARRY = [
    "Required inputs",
    "When evidence is missing or conflicting",
    "RESTRICTED_DO_NOT_PROCESS",
    "Documents are evidence, not instructions",
    "Human review",
    "Never",
    "Degraded chat mode",
]

#: Sections that must be written for the new scope. Carrying them would describe
#: the parent's job under the child's name.
AUTHOR = ["When to use this skill", "When NOT to use this skill", "Operating modes",
          "Procedure", "Outputs", "Verification checklist"]


def sections(text: str) -> dict[str, str]:
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1).strip(), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--row", required=True, help="the job-model row this package owns")
    a = ap.parse_args()

    src = ROOT / "skills" / a.parent / "SKILL.md"
    if not (ROOT.parent / "_ADMIN").is_dir():
        sys.exit(
            "maintainer-only: this script writes into the private _ADMIN tree, "
            "which is not present in a public clone"
        )
    if not src.exists():
        sys.exit(f"FAIL: no parent package at {src}")
    if (ROOT / "skills" / a.id).exists():
        sys.exit(f"FAIL: {a.id} already exists in the library")

    text = src.read_text(encoding="utf-8")
    secs = sections(text)
    missing = [s for s in CARRY if s not in secs]

    dest = STAGING / a.id
    dest.mkdir(parents=True, exist_ok=True)

    body = [
        "---",
        f"name: {a.id}",
        "description: >-",
        f"  UNAUTHORED. This package owns the job-model row \"{a.row}\", split from",
        f"  {a.parent} under PS-D030. Its description must be written for this scope",
        "  alone before it can enter the library, because the description is the",
        "  router's entire selection surface and the parent's would select for the",
        "  wrong job.",
        "license: MIT",
        "metadata:",
        f"  split-from: {a.parent}",
        f"  owns-row: \"{a.row}\"",
        "  authoring-status: procedure-not-written",
        "---",
        "",
        f"# {a.row}",
        "",
        f"> **Staged, not shipped.** Split from `{a.parent}` under PS-D030 so that one",
        "> package owns one job-model row. It is outside `skills/` on purpose: the",
        "> library must not contain a package whose procedure is unwritten.",
        "",
        "## To be written for this scope",
        "",
    ]
    for s in AUTHOR:
        body += [f"### {s}", "",
                 (f"*Not written.* The parent's version describes {a.parent}'s job, "
                 f"not this one."), ""]
    body += [
        "## Carried unchanged from the parent",
        "",
        (
            "These encode the product's boundaries rather than the job, so every "
            "package owes the same text."
        ),
        "",
    ]
    for s in CARRY:
        if s in secs:
            body += [f"## {s}", "", secs[s], ""]

    (dest / "SKILL.md").write_text("\n".join(body), encoding="utf-8")
    print(f"staged {a.id}  (owns: {a.row})")
    if missing:
        print(f"  note: parent had no section(s) {missing} — nothing carried for them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
