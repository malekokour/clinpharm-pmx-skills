"""The canonical reading of per-skill qualification status.

Single source of record. ``validate_repo.py`` and ``build_release.py`` both
import from here; neither keeps its own copy.

Why this module exists
----------------------
``build_release.py`` previously discovered release packages with a bare
``skills/*/SKILL.md`` glob, under a docstring that called the result "every
released package". It was not. The glob returns every package *on disk*,
including the twenty that are ``built`` — structurally valid, qualification gate
not passed. A release built from it would ship unqualified packages
labelled as a release, and ``make release-check`` exited 0 while it happened,
because nothing in the release path ever read a status.

The status vocabulary is the product's central honesty claim (``AGENTS.md``):
``released`` means the gate passed, ``built`` means it did not. A release that
ignores the distinction reproduces exactly the overclaim the vocabulary exists
to prevent.

The collections are the source of record; ``catalog/catalog.json`` is a derived
view. This module reads the collections, never the catalog.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only — these gates must run from a clean
checkout with nothing installed.
"""

from __future__ import annotations

import json
from pathlib import Path

#: ``released`` means the package exists AND passed its qualification gate.
#: ``built`` means the package exists and the gate has NOT been passed.
RELEASED = "released"
BUILT = "built"

#: Every status a collection entry may declare.
VALID_STATUSES: frozenset[str] = frozenset(
    {"released", "built", "planned", "held", "deferred", "excluded"}
)

#: Only these two may own a ``skills/<id>/`` directory.
DIRECTORY_ALLOWED: frozenset[str] = frozenset({"released", "built"})


def collection_files(root: Path) -> list[Path]:
    """Every collection manifest under ``root``, in a stable order."""
    return sorted((root / "collections").glob("*/collection.json"))


def statuses(root: Path) -> dict[str, str]:
    """Map skill id to declared status, read from the collections.

    A skill declared in two collections is a defect that ``validate_repo.py``
    reports with its own message. This function does not mask it: the later
    read wins here, and the validator fails the build regardless.
    """
    found: dict[str, str] = {}
    for path in collection_files(root):
        catalog = json.loads(path.read_text(encoding="utf-8"))
        for entry in catalog.get("skills", []):
            skill_id = entry.get("id")
            if isinstance(skill_id, str) and skill_id:
                found[skill_id] = entry.get("status")
    return found


def released_ids(root: Path) -> list[str]:
    """Sorted ids of the skills whose qualification gate has passed.

    This is the only definition of "goes into a release". It is deliberately
    derived from declared status rather than from what happens to exist on
    disk, so adding a package cannot silently add it to a release.
    """
    return sorted(
        skill_id
        for skill_id, status in statuses(root).items()
        if status == RELEASED
    )
