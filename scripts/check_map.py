#!/usr/bin/env python3
"""Gate the published map: denominator, zero blanks, and no dead links.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

    python3 scripts/check_map.py

Four checks, in the order they can fail vacuously
-------------------------------------------------
1. **The denominator itself.** ``rows_read == 167``, asserted before anything is
   measured. This is first because it is the check the other three depend on:
   blanking one carrier proves the gate notices a blank *in the rows it read*,
   and a truncated ledger would still report "167/167 of what I saw". A gate
   that cannot detect a short read cannot assert coverage at all.

2. **Zero blank carriers.** Every row carries a non-empty ``class`` and
   ``current_disposition``. A blank is a **defect**; a gap is an explicit value.
   The difference matters: `gap` is a claim the map makes on purpose, and a
   blank is the map failing to make any claim while looking complete.

3. **The map is current.** Delegates to ``build_map.py --check`` so a ledger
   edit that was never regenerated cannot ship.

4. **No dead links.** Every relative link in every generated page resolves. The
   ledger names 34 modules that do not exist yet; those must render as *planned,
   not built* with no link, and this is what proves the generator honoured that.

Every count printed is a denominator. "No problems found" is not evidence.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "catalog" / "job-model-167.tsv"
MAP = ROOT / "map"

EXPECTED_ROWS = 167

#: A blank here is a defect. `gap` is a value; "" is an absence of one.
CARRIER_COLUMNS = ("class", "current_disposition", "band", "domain", "task_L3")

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def fail(problems: list[str], message: str) -> None:
    problems.append(message)


def main() -> int:
    problems: list[str] = []

    # --- 1 · the denominator -------------------------------------------------
    if not LEDGER.exists():
        print(f"FAILED: ledger not found at {LEDGER.relative_to(ROOT)}")
        return 1
    with LEDGER.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    rows_read = len(rows)
    if rows_read != EXPECTED_ROWS:
        print(
            f"FAILED: ledger has {rows_read} rows, expected {EXPECTED_ROWS}.\n"
            "  The denominator IS the claim. A short read must fail loudly here,\n"
            "  because every check below would otherwise report a clean result\n"
            "  over whatever subset survived."
        )
        return 1

    # --- 2 · zero blank carriers --------------------------------------------
    blanks = 0
    for row in rows:
        for col in CARRIER_COLUMNS:
            if not (row.get(col) or "").strip():
                fail(problems, f"blank {col} at locator {row.get('locator', '?')!r}")
                blanks += 1

    covered = sum(1 for r in rows if r.get("current_disposition") == "skill")
    gaps = sum(1 for r in rows if r.get("current_disposition") == "gap")

    # --- 3 · the map is current ---------------------------------------------
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_map.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        fail(problems, "map is stale — run `python3 scripts/build_map.py`")
        for line in proc.stdout.splitlines()[:6]:
            fail(problems, f"  {line}")

    # --- 4 · no dead links ---------------------------------------------------
    pages = sorted(MAP.rglob("*.md"))
    links_checked = 0
    dead = 0
    for page in pages:
        for raw in LINK.findall(page.read_text(encoding="utf-8")):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            links_checked += 1
            if not (page.parent / target).resolve().exists():
                fail(problems, f"dead link {page.relative_to(ROOT)} -> {raw}")
                dead += 1

    task_pages = len(list((MAP / "tasks").glob("*.md"))) if (MAP / "tasks").is_dir() else 0

    # --- report --------------------------------------------------------------
    print(
        f"\nMap gate: {rows_read}/{EXPECTED_ROWS} ledger rows read, "
        f"{task_pages} task page(s), {len(pages)} Markdown page(s), "
        f"{links_checked} relative link(s) checked"
    )
    print(f"  carriers   : {rows_read - blanks}/{rows_read} non-blank, {blanks} blank")
    print(f"  coverage   : {covered} carried by a skill, {gaps} explicit gaps")
    print(f"  dead links : {dead}")

    if (MAP / "job-model.json").exists():
        doc = json.loads((MAP / "job-model.json").read_text(encoding="utf-8"))
        n = doc.get("counts", {}).get("tasks")
        if n != EXPECTED_ROWS:
            fail(problems, f"job-model.json reports {n} tasks, expected {EXPECTED_ROWS}")
        if len(doc.get("tasks", [])) != EXPECTED_ROWS:
            fail(
                problems,
                f"job-model.json holds {len(doc.get('tasks', []))} entries, "
                f"expected {EXPECTED_ROWS}",
            )
    else:
        fail(problems, "map/job-model.json is missing")

    if task_pages != EXPECTED_ROWS:
        fail(problems, f"{task_pages} task pages on disk, expected {EXPECTED_ROWS}")

    if problems:
        print(f"\nFAILED: {len(problems)} map problem(s)")
        for p in problems:
            print(f"- {p}")
        return 1

    print(
        f"PASS: {rows_read}/{EXPECTED_ROWS} carriers non-blank, "
        f"{task_pages}/{EXPECTED_ROWS} task pages current, "
        f"{links_checked} link(s) resolve, 0 dead"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
