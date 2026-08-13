#!/usr/bin/env python3
"""Generate `map/` — the profession's 167 tasks as citable Markdown and JSON.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

    python3 scripts/build_map.py            # write map/
    python3 scripts/build_map.py --check    # fail if anything is missing or stale

Why a second map surface
------------------------
`scripts/build_map_site.py` already renders the same ledger to `site/map/*.html`
for the published site. This writes Markdown and JSON instead, because the two
answer different questions:

  site/map/*.html   a person browsing the site
  map/tasks/*.md    a person reading the repository, and anything that cites a
                    task by a stable path in a pull request or a paper
  map/job-model.json a program joining the map to the library

**One source of record, two views.** Both generators read
`catalog/job-model-167.tsv` and neither reads the other. Editing a generated page
by hand is a defect; fix the ledger and regenerate.

The honesty requirement
-----------------------
A map that hides gaps is marketing. 114 of the 167 tasks currently have no skill
— that number is the most useful thing on the page, and it is rendered, not
suppressed.

Links are emitted **only for paths that exist**. The ledger names 49
`knowledge_pack` targets of which 15 resolve today; the other 34 are planned
modules. Rendering those as links would produce 34 dead links in the published
map and a false impression of coverage, so an unresolved target renders as
*planned, not built* with no link. That distinction is checked by
`scripts/check_map.py`, not left to this script's good intentions.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "catalog" / "job-model-167.tsv"
OUT = ROOT / "map"

EXPECTED_ROWS = 167

BAND_TITLE = {
    "A": "Band A — Scientific and quantitative foundations",
    "B": "Band B — Development, evidence and regulatory work",
    "C": "Band C — Safety, ethics, access and function leadership",
}

CLASS_COPY = {
    "skill": (
        "Skill",
        "A workflow you can run. The router selects it from your request.",
    ),
    "context": (
        "Context",
        ("Not a workflow. It attaches to whichever skill you are running and "
        "changes how that skill interprets your data."),
    ),
    "shared-reference": (
        "Shared reference",
        "Criteria other skills read. It has no workflow of its own.",
    ),
    "boundary": (
        "Outside this product",
        ("Real professional work, deliberately not covered here. Named rather "
        "than hidden."),
    ),
}

#: Columns that reach the published map. An **allowlist** — a column added to
#: the ledger later is invisible here until someone decides it should publish,
#: which is the opposite of the denylist failure mode where nobody remembers.
PUBLISHED_COLUMNS = (
    "locator",
    "band",
    "domain",
    "subdomain",
    "task_L3",
    "current_disposition",
    "class",
    "coverage_via",
    "knowledge_pack",
    "roadmap_wave",
    "box_trigger",
    "box_input",
    "box_output",
    "box_refuses",
    "four_box_status",
)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def resolves(target: str) -> bool:
    """True only if the target is a real path in this repository."""
    target = target.strip()
    if not target or target.startswith(("http://", "https://")):
        return False
    # The ledger sometimes annotates a path: "shared/x.md (composes with y)"
    target = target.split("(")[0].strip()
    if not target or " " in target:
        return False
    return (ROOT / target).exists()


def link_targets(row: dict) -> tuple[list[str], list[str]]:
    """Split the row's named targets into (resolving, planned)."""
    found: list[str] = []
    planned: list[str] = []
    for field in ("coverage_via", "knowledge_pack"):
        raw = (row.get(field) or "").strip()
        if not raw or raw == "self":
            continue
        for part in raw.split(";"):
            candidate = part.split("(")[0].strip()
            if not candidate or candidate == "self":
                continue
            (found if resolves(candidate) else planned).append(candidate)
    return sorted(set(found)), sorted(set(planned))


def read_rows() -> list[dict]:
    if not LEDGER.exists():
        raise SystemExit(f"FAILED: ledger not found at {LEDGER}")
    with LEDGER.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(
            f"FAILED: ledger has {len(rows)} rows, expected {EXPECTED_ROWS}. "
            "The denominator is the claim; a short read must not pass quietly."
        )
    return rows


def task_page(row: dict) -> str:
    cls = row["class"]
    label, note = CLASS_COPY.get(cls, (cls, ""))
    found, planned = link_targets(row)
    covered = row["current_disposition"] == "skill"

    out = [
        f"# {row['task_L3']}",
        "",
        f"> {note}" if note else "",
        "",
        "## Where this sits",
        "",
        "| | |",
        "|---|---|",
        f"| Band | {row['band']} |",
        f"| Domain | {row['domain']} |",
        f"| Sub-domain | {row['subdomain']} |",
        f"| Locator | `{row['locator']}` |",
        f"| Carrier | **{label}** |",
        "",
        "## Is this covered today?",
        "",
    ]
    if covered:
        out += [
            "**Yes — a skill carries this task.** It is in the library now.",
        ]
    else:
        out += [
            ("**Not yet.** No skill carries this task today. It is on the "
            f"**{row['roadmap_wave']}** wave."),
            "",
            ("This is stated rather than hidden. A map that shows only what it "
            "covers tells you nothing about the rest of your job."),
        ]
    out += [""]

    if found:
        out += ["## What it reads", ""]
        out += [f"- [`{t}`](../../{t})" for t in found]
        out += [""]
    if planned:
        out += [
            "## Planned, not built",
            "",
            ("Named in the ledger, absent from the repository today. Listed "
            "without links, because a link to a file that does not exist is a "
            "worse answer than an honest gap."),
            "",
        ]
        out += [f"- `{t}`" for t in planned]
        out += [""]

    if row.get("four_box_status") == "RECORDED" and (row.get("box_trigger") or "").strip():
        out += [
            "## What it does, and what it refuses",
            "",
            "| | |",
            "|---|---|",
            f"| Trigger | {row['box_trigger']} |",
            f"| Input | {row['box_input']} |",
            f"| Output | {row['box_output']} |",
            f"| **Refuses** | {row['box_refuses']} |",
            "",
        ]
    else:
        out += [
            "## What it does, and what it refuses",
            "",
            ("**Not yet authored.** The four-box contract for this task has not "
            "been written, so nothing is claimed about it."),
            "",
        ]

    out += [
        "---",
        "",
        (f"Part of the [ClinPharm PMx Skills job model](../README.md) · "
        f"[Band {row['band']}](../bands/{row['band']}.md)"),
        "",
        ("*Generated from `catalog/job-model-167.tsv` by `scripts/build_map.py`. "
        "Do not edit by hand — fix the ledger and regenerate.*"),
        "",
    ]
    return "\n".join(line for line in out if line is not None)


def band_page(band: str, rows: list[dict]) -> str:
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_domain[r["domain"]].append(r)
    covered = sum(1 for r in rows if r["current_disposition"] == "skill")

    out = [
        f"# {BAND_TITLE.get(band, f'Band {band}')}",
        "",
        (f"**{len(rows)} tasks · {covered} carried by a skill today · "
        f"{len(rows) - covered} not yet.**"),
        "",
    ]
    for domain, drows in sorted(by_domain.items()):
        dcov = sum(1 for r in drows if r["current_disposition"] == "skill")
        out += [
            f"## {domain}",
            "",
            f"{len(drows)} tasks · {dcov} carried · {len(drows) - dcov} open",
            "",
            "| Task | Sub-domain | Carrier | Covered |",
            "|---|---|---|---|",
        ]
        for r in sorted(drows, key=lambda x: x["task_L3"]):
            mark = "yes" if r["current_disposition"] == "skill" else f"{r['roadmap_wave']}"
            out.append(
                f"| [{r['task_L3']}](../tasks/{slug(r['task_L3'])}.md) "
                f"| {r['subdomain']} | {r['class']} | {mark} |"
            )
        out.append("")
    out += [
        "---",
        "",
        "[Back to the job model](../README.md)",
        "",
        "*Generated by `scripts/build_map.py`. Do not edit by hand.*",
        "",
    ]
    return "\n".join(out)


def readme(rows: list[dict]) -> str:
    covered = sum(1 for r in rows if r["current_disposition"] == "skill")
    domains = Counter(r["domain"] for r in rows)
    classes = Counter(r["class"] for r in rows)

    out = [
        "# The job model — 167 tasks",
        "",
        ("This is Layer 1 of ClinPharm PMx Skills: **the profession, mapped**. Every "
        "comparable library ships skills and evaluations. None ships a map of "
        "the job its skills are for."),
        "",
        (f"**{len(rows)} tasks · {len(domains)} domains · 3 bands.** "
        f"**{covered} are carried by a skill today; {len(rows) - covered} are not.**"),
        "",
        ("That second number is the point. A library that lists only what it "
        "covers cannot tell you what percentage of your job it touches, and "
        "cannot be wrong in public. This one can."),
        "",
        "## The three bands",
        "",
        "| Band | Tasks | Carried | Open | |",
        "|---|---:|---:|---:|---|",
    ]
    for b in ("A", "B", "C"):
        brows = [r for r in rows if r["band"] == b]
        bcov = sum(1 for r in brows if r["current_disposition"] == "skill")
        out.append(
            f"| **{b}** | {len(brows)} | {bcov} | {len(brows) - bcov} | "
            f"[open](bands/{b}.md) |"
        )
    out += [
        "",
        "## How to read a task page",
        "",
        ("Each of the 167 tasks has its own page under [`tasks/`](tasks/), named "
        "by a stable slug so it can be cited in a pull request, an issue, or a "
        "paper."),
        "",
        "A page states four things:",
        "",
        "1. **Where the task sits** — band, domain, sub-domain, and a stable locator.",
        "2. **Whether anything carries it today**, and on which roadmap wave if not.",
        ("3. **What it reads** — only files that actually exist. A target named in "
        "   the ledger but absent from the repository is listed under *planned, "
        "   not built*, without a link."),
        "4. **What it refuses.** The refusal is a feature, not a disclaimer.",
        "",
        "## What a carrier means",
        "",
        "| Carrier | Count | Means |",
        "|---|---:|---|",
    ]
    for cls, (label, note) in CLASS_COPY.items():
        out.append(f"| {label} | {classes.get(cls, 0)} | {note} |")
    out += [
        "",
        "## What `not yet` honestly means",
        "",
        ("It means no skill in this repository carries that task. It does **not** "
        "mean the task is unimportant, or that the work is not being done — a "
        "clinical pharmacologist does all 167 of these. It means the library "
        "does not help with that one yet."),
        "",
        "## Source of record",
        "",
        "[`catalog/job-model-167.tsv`](../catalog/job-model-167.tsv) — 167 rows.",
        "",
        ("Everything under `map/` is generated from it by "
        "[`scripts/build_map.py`](../scripts/build_map.py), and "
        "[`site/map/`](../site/map/) is generated from the same file by "
        "`scripts/build_map_site.py`. **Two views, one source.** Editing a "
        "generated page by hand is a defect; fix the ledger and regenerate."),
        "",
        ("`scripts/check_map.py` fails the build if a page is missing, stale, "
        "carries a blank carrier, or links to a path that does not exist."),
        "",
        "*Generated by `scripts/build_map.py`. Do not edit by hand.*",
        "",
    ]
    return "\n".join(out)


def job_model_json(rows: list[dict]) -> str:
    entries = []
    for r in rows:
        found, planned = link_targets(r)
        entries.append(
            {
                "id": slug(r["task_L3"]),
                "locator": r["locator"],
                "band": r["band"],
                "domain": r["domain"],
                "subdomain": r["subdomain"],
                "task": r["task_L3"],
                "carrier_class": r["class"],
                "covered_by_skill": r["current_disposition"] == "skill",
                "roadmap_wave": r["roadmap_wave"],
                "reads": found,
                "planned_not_built": planned,
                "contract_recorded": r.get("four_box_status") == "RECORDED",
                "page": f"map/tasks/{slug(r['task_L3'])}.md",
                "site_page": f"site/map/{slug(r['task_L3'])}.html",
            }
        )
    covered = sum(1 for e in entries if e["covered_by_skill"])
    doc = {
        "schema_version": "1.0",
        "source_of_record": "catalog/job-model-167.tsv",
        "generated_by": "scripts/build_map.py",
        "counts": {
            "tasks": len(entries),
            "carried_by_skill": covered,
            "not_yet_carried": len(entries) - covered,
            "domains": len({e["domain"] for e in entries}),
            "bands": len({e["band"] for e in entries}),
        },
        "tasks": entries,
    }
    return json.dumps(doc, indent=2, sort_keys=False, ensure_ascii=False) + "\n"


def build() -> dict[str, str]:
    rows = read_rows()
    files: dict[str, str] = {"README.md": readme(rows), "job-model.json": job_model_json(rows)}
    for band in sorted({r["band"] for r in rows}):
        files[f"bands/{band}.md"] = band_page(band, [r for r in rows if r["band"] == band])
    seen: set[str] = set()
    for r in rows:
        name = f"tasks/{slug(r['task_L3'])}.md"
        if name in seen:
            raise SystemExit(
                f"FAILED: two tasks slug to the same page: {name}. "
                "Slugs are the citable identity; a collision silently drops a task."
            )
        seen.add(name)
        files[name] = task_page(r)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if stale, write nothing")
    args = parser.parse_args()

    files = build()
    stale: list[str] = []
    for rel, content in sorted(files.items()):
        path = OUT / rel
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    task_pages = sum(1 for k in files if k.startswith("tasks/"))
    if args.check:
        if stale:
            print(f"FAILED: {len(stale)} map file(s) missing or stale")
            for rel in stale[:10]:
                print(f"- map/{rel}")
            if len(stale) > 10:
                print(f"  ... and {len(stale) - 10} more")
            return 1
        print(
            f"PASS: map is current — {len(files)} generated file(s), "
            f"{task_pages}/{EXPECTED_ROWS} task pages"
        )
        return 0

    print(
        f"Wrote {len(files)} file(s) to map/: {task_pages} task pages, "
        f"3 band pages, README.md, job-model.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
