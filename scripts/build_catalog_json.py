#!/usr/bin/env python3
"""Generate catalog/catalog.json from collection authorities and skill metadata.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "catalog/catalog.json"

STATUS_MEANING = {
    "released": "package exists AND passed its qualification gate",
    "built": "package exists; qualification gate NOT passed — see evidence_gap",
    "planned": "no package",
    "held": "no package; risk or ownership gate",
    "deferred": "no package; outside the current programme",
}


def skill_frontmatter(skill_id: str) -> dict[str, object]:
    """Read the small frontmatter subset needed by the catalog."""
    path = ROOT / "skills" / skill_id / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    block = text.split("---", 2)[1]
    root: dict[str, object] = {}
    metadata: dict[str, str] = {}
    active = ""
    for line in block.splitlines():
        if not line.strip() or ":" not in line:
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, value = line.strip().split(":", 1)
        value = value.strip().strip('"')
        if indent == 0:
            active = key
            root[key] = value
        elif active == "metadata" and indent == 2:
            metadata[key] = value
    root["metadata"] = metadata
    return root


def build() -> dict[str, object]:
    """Return the deterministic catalog derived from every collection row."""
    collection_paths = sorted((ROOT / "collections").glob("*/collection.json"))
    collections = [json.loads(path.read_text(encoding="utf-8")) for path in collection_paths]
    memberships: dict[str, list[str]] = defaultdict(list)
    for collection in collections:
        for row in collection["skills"]:
            memberships[row["id"]].append(collection["collection"])

    artifacts = []
    for collection in collections:
        collection_id = collection["collection"]
        for row in collection["skills"]:
            skill_id = row["id"]
            frontmatter = skill_frontmatter(skill_id)
            metadata = frontmatter.get("metadata", {})
            artifacts.append(
                {
                    "id": skill_id,
                    "kind": "skill",
                    "title": row["title"],
                    "primary_collection": collection_id,
                    "related_collections": [
                        item for item in memberships[skill_id] if item != collection_id
                    ],
                    "status": row["status"],
                    "path": f"skills/{skill_id}",
                    "evidence_level": row["evidence_level"],
                    "evidence_gap": row.get("evidence_gap"),
                    "prior_status": row.get("prior_status"),
                    "previous_id": row.get("previous_id"),
                    "human_review": metadata.get("human-review", "required"),
                    "licence": frontmatter.get("license", "MIT"),
                    "qualification_profile": row["qualification_profile"],
                    "qualification_profile_status": row["qualification_profile_status"],
                    "qualification_policy": row["qualification_policy"],
                }
            )

    tally = Counter(row["status"] for row in artifacts)
    generated = max(collection["updated"] for collection in collections)
    return {
        "schema_version": "1.1",
        "generated": generated,
        "generator": "regenerate from collections/*/collection.json — do not hand-edit",
        "status_meaning": STATUS_MEANING,
        "counts": {
            "released": tally.get("released", 0),
            "built": tally.get("built", 0),
            "total": len(artifacts),
        },
        "artifacts": artifacts,
    }


def render() -> str:
    return json.dumps(build(), indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        actual = TARGET.read_text(encoding="utf-8") if TARGET.is_file() else ""
        if actual != expected:
            print("FAILED: catalog/catalog.json is stale; run `make docs`")
            return 1
        print(f"PASS: catalog/catalog.json matches {len(build()['artifacts'])} collection rows")
        return 0
    TARGET.write_text(expected, encoding="utf-8")
    print(f"Built {TARGET} from {len(build()['artifacts'])} collection rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
