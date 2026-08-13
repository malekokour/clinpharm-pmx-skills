#!/usr/bin/env python3
"""Sync the package counts stated in README.md to their source of record.

`check_claim_ledger.py` verifies that every public count matches its source and
fails when it does not. That is the gate. This is the fix: it rewrites the three
counts the README states so a human never types them.

The counts were being hand-edited on every package addition, which is exactly the
hand-maintained-derived-value pattern this repository forbids everywhere else.
Two consecutive package additions both failed the claim gate for the same reason
before this script existed.

Source of record: `collections/*/collection.json`. Never the catalog, which is
itself derived.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


def counts() -> dict[str, int]:
    out = {"released": 0, "built": 0}
    for cf in sorted((ROOT / "collections").glob("*/collection.json")):
        for s in json.loads(cf.read_text(encoding="utf-8")).get("skills", []):
            if isinstance(s, dict):
                st = s.get("status", "")
                if st in out:
                    out[st] += 1
    out["total"] = out["released"] + out["built"]
    return out


PATTERNS = [
    (r"(\| `released` \| \*\*)\d+(\*\*)", "released"),
    (r"(\| `built` \| \*\*)\d+(\*\*)", "built"),
    (r"(\| \*\*Total\*\* \| \*\*)\d+(\*\*)", "total"),
    (r"(\bskills/ +)\d+( independently installable)", "total"),
    (r"(\n)\d+( are built\. That gap is the work)", "total"),
]


def main() -> int:
    check = "--check" in sys.argv
    c = counts()
    text = original = README.read_text(encoding="utf-8")
    for pat, key in PATTERNS:
        text = re.sub(pat, lambda m, k=key: f"{m.group(1)}{c[k]}{m.group(2)}", text)

    if check:
        if text != original:
            print("FAILED: README counts are stale; run scripts/sync_readme_counts.py")
            return 1
        print(f"PASS: README counts match the collections "
              f"({c['released']} released, {c['built']} built, {c['total']} packages)")
        return 0

    if text != original:
        README.write_text(text, encoding="utf-8")
        print(f"synced README: {c['released']} released, {c['built']} built, "
              f"{c['total']} packages")
    else:
        print("README already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
