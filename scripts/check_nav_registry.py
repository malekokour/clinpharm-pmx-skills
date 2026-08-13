#!/usr/bin/env python3
"""Check catalog/nav_registry.json against the router's field contract.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

The contract
------------
The router design method asks the registry to make ten things available:
``id``, ``title``, ``description``, ``locator``, ``nav_path``, ``neighbors``,
``conflicts``, ``risk_tier``, refuse tags, and ``aliases``.

It does **not** follow that all ten are *stored in* ``nav_registry.json``, and
storing them there would be the wrong reading. This repository holds one source
of record per thing: package status lives in ``collections/*/collection.json``,
the activation contract and its exclusion clause live in ``skills/<id>/SKILL.md``,
and the virtual navigation tree lives in the registry. Copying titles and refuse
clauses into a fourth file would create a second editable home for each of them,
and the copies would drift.

So this gate checks that every required field **resolves**, and reports where
each one resolved from. A field that resolves nowhere is a failure; a field that
resolves from its owning file is a pass.

  id           registry + collection row (must agree)
  title        collection row
  description  skills/<id>/SKILL.md frontmatter
  locator      skills/<id>/ on disk
  nav_path     registry
  neighbors    DERIVED from nav_path — see below
  conflicts    derived: siblings sharing a nav_path parent are the collision set
  risk_tier    collection row `qualification_profile`
  refuse tags  skills/<id>/SKILL.md exclusion clause (also gated by check_routing)
  aliases      registry (plus `previous_id` on the collection row)

Why neighbours are derived rather than stored
---------------------------------------------
On 2026-08-11 exactly 1 of 22 collection rows carried ``activation_neighbours``
and 3 of 22 carried ``never``. Hand-authoring 21 missing neighbour lists would
have produced a field that is (a) a second encoding of information ``nav_path``
already carries and (b) certain to go stale the first time a package moves in
the tree.

``nav_path`` *is* the neighbourhood structure — the method's own selection step
says "narrow by nav_path (band → domain → subdomain)". Two packages that share a
parent path are neighbours by construction, and they stay neighbours without
anyone remembering to update a list.

What this gate does not claim
-----------------------------
It says nothing about whether the routing is *good*. That is measured by
``scripts/check_router_selection.py``. This one checks the registry is complete,
internally consistent with the packages on disk, and resolvable field by field.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: A nav_path is a slash-separated virtual path. It must not look like a real
#: directory path — the packages are flat on disk, and a leading or trailing
#: slash would suggest otherwise.
NAV_PATH = re.compile(r"^[a-z0-9]+(?:[-/][a-z0-9]+)*$")

DESCRIPTION = re.compile(r"^description:\s*\S", re.MULTILINE)

#: The five exclusion phrasings in use across the packages. Copied deliberately
#: from ``scripts/check_routing.py`` so the two gates agree on what an exclusion
#: clause *is* — the alternative was a substring search for the word "never",
#: which this file briefly carried and which passed on every package including
#: ones whose only "never" was in an unrelated sentence. A check that cannot
#: fail is worse than no check, because it reports a denominator it never
#: actually examined.
EXCLUSION = re.compile(r"(?i)\bDo not use (?:when|for|to|it to|this skill)\b")


def neighbours_by_nav_path(registry: list[dict]) -> dict[str, list[str]]:
    """Group packages by their nav_path parent.

    A package at ``documents/csr`` has parent ``documents``; one at
    ``studies/analysis/nca`` has parent ``studies/analysis``. A top-level path
    such as ``library`` has no parent and therefore no neighbours, which is a
    fact about the tree rather than a defect.
    """
    by_parent: dict[str, list[str]] = defaultdict(list)
    for entry in registry:
        nav_path = str(entry.get("nav_path") or "")
        parent = nav_path.rsplit("/", 1)[0] if "/" in nav_path else ""
        by_parent[parent].append(str(entry["id"]))

    neighbours: dict[str, list[str]] = {}
    for entry in registry:
        skill_id = str(entry["id"])
        nav_path = str(entry.get("nav_path") or "")
        parent = nav_path.rsplit("/", 1)[0] if "/" in nav_path else ""
        neighbours[skill_id] = sorted(
            sibling for sibling in by_parent[parent] if sibling != skill_id
        )
    return neighbours


def main() -> int:
    registry_path = ROOT / "catalog" / "nav_registry.json"
    if not registry_path.is_file():
        print(f"FAILED: {registry_path} does not exist")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8")).get("skills") or []
    if not registry:
        print("FAILED: nav_registry.json declares no skills")
        return 1

    rows: dict[str, dict] = {}
    for catalog_path in sorted((ROOT / "collections").glob("*/collection.json")):
        for entry in json.loads(catalog_path.read_text(encoding="utf-8"))["skills"]:
            rows[entry["id"]] = entry

    on_disk = {p.name for p in sorted((ROOT / "skills").iterdir()) if p.is_dir()}
    registered = {str(e["id"]) for e in registry}

    problems: list[str] = []

    # Coverage in both directions. A package on disk with no registry entry is
    # unreachable by the router; a registry entry with no package is a promise
    # of something that is not there.
    for orphan in sorted(on_disk - registered):
        problems.append(f"{orphan}: package on disk has no nav_registry entry")
    for phantom in sorted(registered - on_disk):
        problems.append(f"{phantom}: nav_registry entry has no package on disk")

    seen_paths: Counter[str] = Counter()
    resolved: Counter[str] = Counter()
    fields_checked = 0

    for entry in registry:
        skill_id = str(entry.get("id") or "")
        if not skill_id:
            problems.append("a nav_registry entry has no id")
            continue
        row = rows.get(skill_id, {})
        skill_md = ROOT / "skills" / skill_id / "SKILL.md"
        skill_text = skill_md.read_text(encoding="utf-8") if skill_md.is_file() else ""

        nav_path = str(entry.get("nav_path") or "")
        seen_paths[nav_path] += 1

        checks = {
            "id": bool(skill_id) and skill_id in rows,
            "title": bool(row.get("title")),
            "description": bool(DESCRIPTION.search(skill_text)),
            "locator": (ROOT / "skills" / skill_id).is_dir(),
            "nav_path": bool(NAV_PATH.match(nav_path)),
            "risk_tier": bool(row.get("qualification_profile")),
            "refuse_tags": bool(row.get("never")) or bool(EXCLUSION.search(skill_text)),
            "aliases": isinstance(entry.get("aliases"), list),
        }
        for field, ok in checks.items():
            fields_checked += 1
            if ok:
                resolved[field] += 1
            else:
                problems.append(f"{skill_id}: required field {field!r} does not resolve")

    for nav_path, count in sorted(seen_paths.items()):
        if count > 1:
            problems.append(
                f"nav_path {nav_path!r} is claimed by {count} packages — "
                "a virtual path must identify one package"
            )

    neighbours = neighbours_by_nav_path(registry)
    isolated = sorted(sid for sid, sibs in neighbours.items() if not sibs)

    print(
        f"\nNav registry: {len(registry)} entry(ies), {len(on_disk)} package(s) on "
        f"disk, {fields_checked} field check(s)"
    )
    for field in sorted(resolved):
        print(f"  {field:12s} resolved {resolved[field]}/{len(registry)}")
    print(
        f"  neighbours derived from nav_path: "
        f"{sum(len(v) for v in neighbours.values())} edge-ends across "
        f"{len(neighbours)} package(s); {len(isolated)} package(s) sit alone at "
        f"their level ({', '.join(isolated) if isolated else 'none'})"
    )

    if problems:
        print(f"\nFAILED: {len(problems)} nav-registry error(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("PASS: every required router field resolves for every registered package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
