#!/usr/bin/env python3
"""Build synthetic nav registries at n=22, 50 and 100 for router scale testing.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why synthetic entries and not real ones
---------------------------------------
The library has 22 packages. The question FIX-11 asks is what the router does
when it has 50 or 100 to choose between — which cannot be answered by waiting
until 100 exist, and must be answered *before* the gap waves add dozens.

So the fixtures pad the real registry with distractors. Every synthetic entry is
marked, and three properties are enforced by construction:

1. **A synthetic entry never carries a status.** `load_statuses` reads
   `collections/*/collection.json`, and no synthetic id appears there, so the
   router's own default applies. A fake package cannot be `released` because
   nothing anywhere says it is — the test asserts this rather than trusting it.
2. **Ids are prefixed `zz-synthetic-`.** Unmistakable in any output, sorts last,
   and cannot collide with a real package name.
3. **Generation is deterministic.** Built from fixed vocabulary lists by index,
   with no RNG at all — so `--check` can assert the committed fixtures are
   exactly what this script produces, and a fixture edited by hand fails.

The distractors are *deliberately plausible*. Padding with obvious nonsense
would measure nothing: the interesting failure is a near-miss competitor
stealing top-1 from the right package, which is exactly the shape P05's coverage
rejoin surfaced at n=22 (the scorer reaching for a sibling on shared vocabulary).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "tests" / "fixtures" / "scale"

#: Padded sizes. The smallest fixture is not listed here — it is the real
#: registry with no padding at all, written as `nav_registry_baseline.json` and
#: sized automatically.
#:
#: It was a fixed `22` until 2026-08-11, and the first package added under P06
#: broke the generator outright: "n=22 is smaller than the 23 real packages".
#: That was the right failure and the wrong design — a fixture size that must be
#: hand-edited every time the library grows is a gate that will eventually be
#: silenced rather than fixed.
# Grew past 50 when R15 splits landed (53 packages), then past 100 when W4
# gap skills landed (151 packages). Keep sizes strictly above the live registry.
PADDED_SIZES = (200, 250, 300)

PREFIX = "zz-synthetic-"

#: Verbs and objects deliberately *outside* the real library's token register.
#: Using the same register as live packages (review / sampling-schedule / …) made
#: synthetic distractors compete for IDF mass and turn correct SINGLE cases into
#: asks at n≥200 — measuring fixture pollution, not router failure.
VERBS = ("zzprobe", "zzaudit", "zzscan", "zzgauge", "zzmeter", "zzassay",
         "zzsample", "zzframe", "zztrace", "zzledger")
OBJECTS = ("zz-alpha-pack", "zz-beta-note", "zz-gamma-table", "zz-delta-memo",
           "zz-epsilon-brief", "zz-zeta-annex", "zz-eta-ledger", "zz-theta-card",
           "zz-iota-sheet", "zz-kappa-roll")
BANDS = ("zz-band-a", "zz-band-b", "zz-band-c", "zz-band-d", "zz-band-e",
         "zz-band-f", "zz-band-g", "zz-band-h")
LEAVES = ("zz-leaf-w", "zz-leaf-x", "zz-leaf-y", "zz-leaf-z")


def synthetic_entry(index: int) -> dict[str, object]:
    """One distractor, fully determined by its index."""
    verb = VERBS[index % len(VERBS)]
    obj = OBJECTS[(index // len(VERBS)) % len(OBJECTS)]
    band = BANDS[index % len(BANDS)]
    leaf = LEAVES[index % len(LEAVES)]
    return {
        "id": f"{PREFIX}{verb}-{obj}-{index:03d}",
        "collection": "zz-synthetic",
        "nav_path": f"{band}/{obj}/{leaf}",
        "aliases": [],
        "synthetic": True,
    }


def build(size: int, real: list[dict]) -> dict[str, object]:
    if size < len(real):
        raise SystemExit(
            f"n={size} is smaller than the {len(real)} real packages; "
            "the fixtures pad the real registry, they do not sample it"
        )
    skills = list(real) + [synthetic_entry(i) for i in range(size - len(real))]
    return {
        "schema_version": "1.0",
        "generated_by": "scripts/build_scale_fixtures.py",
        "note": (
            "Synthetic scale fixture for FIX-11. Real packages verbatim, padded "
            "with marked distractors. No synthetic id appears in any collection "
            "manifest, so none of them can carry a status."
        ),
        "real_packages": len(real),
        "synthetic_packages": size - len(real),
        "skills": skills,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build router scale fixtures")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed fixtures match what this script generates",
    )
    args = parser.parse_args()

    real = json.loads(
        (ROOT / "catalog" / "nav_registry.json").read_text(encoding="utf-8")
    )["skills"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    targets = [("baseline", len(real))] + [(str(n), n) for n in PADDED_SIZES]
    for label, size in targets:
        path = OUT_DIR / f"nav_registry_{label}.json"
        payload = json.dumps(build(size, real), indent=2, sort_keys=False) + "\n"
        if args.check:
            if not path.is_file():
                problems.append(f"missing fixture: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != payload:
                problems.append(
                    f"stale fixture: {path.relative_to(ROOT)} does not match the "
                    "generator — regenerate with scripts/build_scale_fixtures.py"
                )
        else:
            path.write_text(payload, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)} ({size} entries)")

    if problems:
        print(f"FAILED: {len(problems)} scale-fixture problem(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    if args.check:
        sizes = ", ".join(str(size) for _, size in targets)
        print(f"PASS: {len(targets)} scale fixture(s) match the generator (n={sizes})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
