#!/usr/bin/env python3
"""Generate the public Markdown catalog from catalog/catalog.json.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog/catalog.json"
TARGET = ROOT / "docs/CATALOG.md"
GAP_LIMIT = 120


def cell(value: object) -> str:
    """Return one safe, single-line Markdown table cell."""
    text = " ".join(str(value).split()).replace("|", "\\|")
    if len(text) > GAP_LIMIT:
        return text[: GAP_LIMIT - 1].rstrip() + "…"
    return text


def render(data: dict) -> str:
    """Render the complete deterministic catalog document."""
    lines = [
        "# Catalog",
        "",
        "> **Generated from `catalog/catalog.json`. Do not hand-edit.**",
        "",
        f"*Generated {data['generated']}.*",
        "",
        "## What each status means",
        "",
        "| Status | Meaning |",
        "|---|---|",
    ]
    for status, meaning in data["status_meaning"].items():
        lines.append(f"| `{cell(status)}` | {cell(meaning)} |")
    lines.extend(
        [
            "",
            "**`released` and `built` both have a package on disk. Only `released` has passed",
            "its qualification gate.** A `built` entry states exactly what is missing.",
            "",
            "## Counts",
            "",
            "| Status | Count |",
            "|---|---:|",
        ]
    )
    for status in ("built", "released"):
        lines.append(f"| {status} | {data['counts'].get(status, 0)} |")
    lines.append(f"| **total** | **{data['counts']['total']}** |")
    lines.extend(["", "## Artifacts", ""])

    grouped: dict[str, list[dict]] = defaultdict(list)
    for artifact in data["artifacts"]:
        grouped[artifact["primary_collection"]].append(artifact)
    for collection in sorted(grouped):
        lines.extend(
            [
                f"### {collection}",
                "",
                "| ID | Title | Status | Evidence | Gap |",
                "|---|---|---|---|---|",
            ]
        )
        for artifact in sorted(grouped[collection], key=lambda item: item["id"]):
            gap = artifact.get("evidence_gap") or "—"
            lines.append(
                f"| [`{cell(artifact['id'])}`](../{artifact['path']}/) "
                f"| {cell(artifact['title'])} | `{cell(artifact['status'])}` "
                f"| {cell(artifact['evidence_level'])} | {cell(gap)} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    expected = render(data)
    if args.check:
        actual = TARGET.read_text(encoding="utf-8") if TARGET.is_file() else ""
        if actual != expected:
            print("FAILED: docs/CATALOG.md is stale; run `make docs`")
            return 1
        print(f"PASS: docs/CATALOG.md matches {len(data['artifacts'])} catalog artifacts")
        return 0
    TARGET.write_text(expected, encoding="utf-8")
    print(f"Built {TARGET} from {len(data['artifacts'])} catalog artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
