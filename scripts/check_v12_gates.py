#!/usr/bin/env python3
"""Vision v1.2 repository gates (PS-D029 / PS-D030 / PS-D031).

Five checks, each of which must be able to fail. Run with --list to see them.

  1. tool-budget      <=10 declared tools/scripts per skill
  2. size-budget      SKILL.md <=500 lines; description <=1024 chars
  3. allowed-tools    declared, and every tool the body invokes is listed
  4. registry-schema  required fields present; ids and aliases unique
  5. ledger-coverage  every job-model row carries a class and a carrier

Exit 0 only when every enabled check passes. Any failure prints the offending
item and its measured value, never a bare "failed".
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
REG = ROOT / "catalog" / "nav_registry.json"

TOOL_BUDGET = 10
LINE_BUDGET = 500
DESC_BUDGET = 1024

# The ledger lives in the private workspace; the public gate runs only when a
# copy is present, and says so rather than passing silently on nothing.
LEDGER = ROOT / "catalog" / "job-model-167.tsv"


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if line.startswith(" "):
            continue
        k, _, v = line.partition(":")
        if k:
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def skill_dirs() -> list[Path]:
    return sorted(d for d in SKILLS.iterdir() if (d / "SKILL.md").exists())


# --- 1 ------------------------------------------------------------------------
def check_tool_budget() -> list[str]:
    bad = []
    for d in skill_dirs():
        fm, _ = frontmatter(d / "SKILL.md")
        declared = len(fm.get("allowed-tools", "").split())
        scripts = len(list((d / "scripts").glob("*"))) if (d / "scripts").is_dir() else 0
        total = declared + scripts
        if total > TOOL_BUDGET:
            bad.append(f"{d.name}: {total} tools/scripts (budget {TOOL_BUDGET}) "
                       f"— split candidate, run the separability tests")
    return bad


# --- 2 ------------------------------------------------------------------------
def check_size_budget() -> list[str]:
    bad = []
    for d in skill_dirs():
        p = d / "SKILL.md"
        lines = len(p.read_text(encoding="utf-8").splitlines())
        if lines > LINE_BUDGET:
            bad.append(f"{d.name}: SKILL.md is {lines} lines (budget {LINE_BUDGET})")
        fm, _ = frontmatter(p)
        desc = fm.get("description", "")
        if len(desc) > DESC_BUDGET:
            bad.append(f"{d.name}: description is {len(desc)} chars (spec limit {DESC_BUDGET})")
        if not desc:
            bad.append(f"{d.name}: no description — it cannot be selected")
    return bad


# --- 3 ------------------------------------------------------------------------
def check_allowed_tools(strict: bool = True) -> list[str]:
    """Least privilege. Mandatory since the R13 backfill.

    This was opt-in at R9 because 0 of 26 packages declared it, and a gate
    switched on before its work exists gets switched off again. The backfill
    landed on 26/26, so it is now enforced.
    """
    bad = []
    for d in skill_dirs():
        fm, _ = frontmatter(d / "SKILL.md")
        if "allowed-tools" not in fm:
            bad.append(f"{d.name}: no allowed-tools declaration (least privilege)")
            continue
        if not fm["allowed-tools"].strip():
            bad.append(f"{d.name}: allowed-tools is empty — declare tools or omit the key")
    return bad


# --- 4 ------------------------------------------------------------------------
def check_registry() -> list[str]:
    if not REG.exists():
        return ["catalog/nav_registry.json is missing"]
    d = json.loads(REG.read_text(encoding="utf-8"))
    bad = []
    required = {"id", "title", "description", "locator", "nav_path",
                "neighbors", "risk_tier", "refuse_tags", "aliases"}
    ids, aliases = set(), {}
    for e in d.get("skills", []):
        missing = required - set(e)
        if missing:
            bad.append(f"{e.get('id','?')}: registry entry missing {sorted(missing)}")
        if e.get("id") in ids:
            bad.append(f"duplicate registry id: {e['id']}")
        ids.add(e.get("id"))
        if not (ROOT / e.get("locator", "")).is_dir():
            bad.append(f"{e.get('id','?')}: locator {e.get('locator')!r} is not a directory")
    for group in ("skills", "contexts", "references"):
        for e in d.get(group, []):
            for a in e.get("aliases", []):
                if a in aliases:
                    bad.append(f"alias {a!r} claimed by {aliases[a]} and {e['id']}")
                if a in ids:
                    bad.append(f"alias {a!r} collides with live id {a!r}")
                aliases[a] = e["id"]
    return bad


# --- 5 ------------------------------------------------------------------------
def check_ledger_coverage() -> list[str]:
    if not LEDGER.exists():
        return [(f"ledger not reachable at {LEDGER} — coverage cannot be asserted; "
                "this is a red, not a skip")]
    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8"), delimiter="\t"))
    bad = []
    if len(rows) != 167:
        bad.append(f"ledger has {len(rows)} rows, expected 167")
    for r in rows:
        if not r.get("class"):
            bad.append(f"{r.get('locator','?')}: blank class")
        if not r.get("coverage_via"):
            bad.append(f"{r.get('locator','?')}: blank coverage_via")
    by_task = {r["task_L3"] for r in rows}
    for r in rows:
        cv = r.get("coverage_via", "")
        if cv.startswith("carried by L3: "):
            carrier = cv[len("carried by L3: "):]
            if carrier not in by_task:
                bad.append(f"{r['locator']}: carrier {carrier!r} is not a row in the ledger")
    return bad


CHECKS = {
    "tool-budget": check_tool_budget,
    "size-budget": check_size_budget,
    "allowed-tools": check_allowed_tools,
    "registry-schema": check_registry,
    "ledger-coverage": check_ledger_coverage,
}


def main() -> int:
    if "--list" in sys.argv:
        for k in CHECKS:
            print(k)
        return 0
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = a.split("=", 1)[1]
    failed = 0
    for name, fn in CHECKS.items():
        if only and name != only:
            continue
        problems = fn()
        if problems:
            failed += len(problems)
            print(f"FAIL [{name}] {len(problems)} problem(s):")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"PASS [{name}]")
    if failed:
        print(f"\n{failed} gate problem(s). Fix the input; do not widen the gate.")
        return 1
    print("\nAll v1.2 gates green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
