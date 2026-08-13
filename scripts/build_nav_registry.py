#!/usr/bin/env python3
"""Generate catalog/nav_registry.json from the tree.

The registry is a derived view. Its inputs are the packages on disk, the shared
layer, and the collections. Never hand-edit the output — fix an input and
regenerate.

Nine fields per entry (PS-D030):
    id · description · nav_path · neighbors · conflicts · risk_tier ·
    refuse_tags · aliases · collection

Three entry kinds:
    skill            selectable by the router
    context          never selected; attached after selection
    shared-reference never selected; loaded by a named carrier

Contexts and references appear so the router can *resolve* a question about them
to the right place. Appearing is not the same as being selectable.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "catalog" / "nav_registry.json"

FIELDS = ["id", "kind", "description", "nav_path", "neighbors", "conflicts",
          "risk_tier", "refuse_tags", "aliases", "collection"]

# evidence-level / human-review in SKILL.md metadata -> risk tier (PS-D024)
def risk_tier(meta: dict) -> str:
    if meta.get("human-review") == "required":
        return "HIGH" if "qualification" not in meta.get("evidence-level", "") else "MEDIUM"
    return "LOW"


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    out, meta, in_meta = {}, {}, False
    for line in m.group(1).splitlines():
        if line.startswith("metadata:"):
            in_meta = True
            continue
        if in_meta and line.startswith("  "):
            k, _, v = line.strip().partition(":")
            meta[k.strip()] = v.strip().strip('"')
            continue
        in_meta = False
        k, _, v = line.partition(":")
        if k and not k.startswith(" "):
            out[k.strip()] = v.strip()
    out["metadata"] = meta
    return out


def main() -> int:
    prior = json.loads(REG.read_text(encoding="utf-8")) if REG.exists() else {}
    prior_by_id = {e["id"]: e for e in prior.get("skills", [])}

    # titles are owned by the collection rows — the registry points, never copies
    titles: dict[str, str] = {}
    for cf in sorted((ROOT / "collections").glob("*/collection.json")):
        for s in json.loads(cf.read_text(encoding="utf-8")).get("skills", []):
            if isinstance(s, dict) and s.get("id"):
                titles[s["id"]] = s.get("title", "")

    entries: list[dict] = []
    pending: list[str] = []

    # --- skills -------------------------------------------------------------
    for d in sorted((ROOT / "skills").iterdir()):
        if not (d / "SKILL.md").exists():
            continue
        fm = frontmatter(d / "SKILL.md")
        meta = fm.get("metadata", {})
        old = prior_by_id.get(d.name, {})
        # `nav_path` is a LEAF, not a branch: it must identify exactly one package,
        # because it is the package's position in the virtual job tree. A split
        # therefore cannot inherit its parent's path — and the parent's own path
        # usually has to change too, because after a split it no longer owns the
        # whole subdomain it was named for. So the path is authored in the package
        # (`metadata.nav-path`) rather than guessed here.
        nav = meta.get("nav-path") or old.get("nav_path", "")
        e = {
            "id": d.name,
            "kind": "skill",
            "title": titles.get(d.name, meta.get("title", "")),
            "description": fm.get("description", ""),
            "locator": f"skills/{d.name}",
            "nav_path": nav,
            "neighbors": old.get("neighbors", []),
            "conflicts": old.get("conflicts", []),
            "risk_tier": old.get("risk_tier") or risk_tier(meta),
            "refuse_tags": old.get("refuse_tags", []),
            "aliases": old.get("aliases", []),
            "collection": meta.get("collection", ""),
        }
        if not e["neighbors"] or not e["refuse_tags"]:
            pending.append(e["id"])
        entries.append(e)

    # --- contexts and shared references -------------------------------------
    # Deliberately NOT in `skills`. The existing gate requires every entry there
    # to resolve to a `skills/<id>/` directory, which is exactly the right test:
    # a context has no package because it is never selected. Separate arrays keep
    # them addressable without pretending they are selectable.
    def resolvable(kind: str, path: Path, nav: str) -> dict:
        return {
            "id": path.stem,
            "kind": kind,
            "locator": str(path.relative_to(ROOT)),
            "nav_path": nav,
            "selectable": False,
            "refuse_tags": ["not-selectable"],
        }

    # README.md documents the folder; it is not an addressable artifact. Registering
    # it would inflate every count that quotes this file.
    def content(paths):
        return [p for p in paths if p.name != "README.md"]

    cdir = ROOT / "shared" / "contexts"
    contexts = [resolvable("context", f, f"context/{f.parent.name}/{f.stem}")
                for f in content(sorted(cdir.rglob("*.md")))] if cdir.exists() else []

    rdir = ROOT / "shared" / "references"
    references = [resolvable("shared-reference", f, f"reference/{f.stem}")
                  for f in content(sorted(rdir.glob("*.md")))] if rdir.exists() else []

    # --- invariants ---------------------------------------------------------
    ids = [e["id"] for e in entries] + [e["id"] for e in contexts + references]
    if len(ids) != len(set(ids)):
        dupes = {i for i in ids if ids.count(i) > 1}
        sys.exit(f"FAIL: duplicate registry ids: {sorted(dupes)}")

    seen: dict[str, str] = {}
    for e in entries:
        for a in e["aliases"]:
            if a in seen:
                sys.exit(f"FAIL: alias '{a}' claimed by {seen[a]} and {e['id']}")
            if a in ids:
                sys.exit(f"FAIL: alias '{a}' collides with a live id ({e['id']})")
            seen[a] = e["id"]

    for e in entries:
        if e["kind"] == "skill" and not e["description"]:
            sys.exit(f"FAIL: skill '{e['id']}' has no description — it cannot be selected")

    out = {
        "schema_version": "2.0",
        "updated": "2026-08-11",
        "authority": "PS-D030-v1",
        "layout_note": (
            "Generated by scripts/build_nav_registry.py. Do not hand-edit — fix an "
            "input and regenerate. `skills` is the selectable set and every entry "
            "resolves to skills/<id>/. `contexts` and `references` are addressable "
            "but never selectable: a question about them resolves to the right file, "
            "and the router attaches them after it has chosen a skill."
        ),
        "counts": {
            "skill": len(entries),
            "context": len(contexts),
            "shared-reference": len(references),
            "total": len(entries) + len(contexts) + len(references),
        },
        "pending_routing_contract": sorted(pending),
        "skills": entries,
        "contexts": contexts,
        "references": references,
    }
    REG.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"OK  {out['counts']}")
    print(f"    pending routing contract (neighbors/refuse_tags): {len(pending)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
