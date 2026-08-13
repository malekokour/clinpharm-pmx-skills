#!/usr/bin/env python3
"""Reject a `defect` assertion whose sides describe a value instead of being one.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Why (FIX-10, finding 2026-08-06-eval-assertions-phrase-brittle, item 3)
----------------------------------------------------------------------
A `defect` assertion binds a value pair: ``observed`` is the wrong value as the
document writes it, ``expected`` is what the source says. The grader looks for
both in one finding.

That only works when each side **is** the value. On 2026-08-06 a batch of
assertions bound descriptions instead — ``starting dose of 10 mg`` rather than
``10 mg`` — and a response reporting exactly that defect writes the number
differently from the sentence around it. First runs scored Critical 22/47 while
**0 of 83 misses were defects nobody found**. The assertions were measuring
phrasing.

The finding's third remedy asks for this gate, so the shape cannot be authored
again silently.

The rule, and why it is not "must contain a digit"
--------------------------------------------------
The obvious rule — both sides must contain a number — was tried against the
corpus and rejected. It fails on legitimate defects:

    observed: "mL/h"          expected: "L/h"      ← a unit mismatch, no digit
    observed: "NEEDS_INPUT"   expected: "Table 7"  ← a marker and a locator

What actually separates a value from a description is a **descriptive function
word**. ``starting dose of 10 mg`` contains ``of``; ``100 mg and 150 mg once
daily`` does not, and is a legitimate compound value.

Calibrated against all 69 defect assertions in the repository (138 sides):
**0 rejected**. Against the shapes the finding names as broken: all rejected.

Two exemptions, both measured rather than assumed:

* ``62 of 70`` — ``of`` between two digits is a count, not a description.
* ``SYN-PBPK-RUN-2026-08-11-A`` — matching is on whitespace-delimited tokens, so
  a trailing ``-A`` inside an identifier is not read as the word "a".

What this gate does not do
--------------------------
It does not rebind the existing assertions, and it does not judge whether a
defect is worth asserting. The finding is explicit that rebinding must happen in
a separate pass, frozen before a fresh run — *"do not fix this in the same pass
that discovered it, and do not re-run to a target"*. This gate only stops the
shape being introduced again.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_schema import load_case

ROOT = Path(__file__).resolve().parents[1]

#: Function words that turn a value into a description of a value. Deliberately
#: small and auditable: every entry earns its place by appearing in the broken
#: shapes the finding recorded, and none appears in the 138 sides now shipping.
DESCRIPTIVE = frozenset(
    {
        "of", "the", "a", "an", "that", "which", "was", "were", "is", "are",
        "with", "for", "from", "in", "on", "to", "by", "its", "their", "this",
        "these", "when", "where",
    }
)

#: "62 of 70" is a count. The `of` between two digits is not a description.
NUMERIC_OF = re.compile(r"\d\s+of\s+\d")

#: A side longer than this is prose whatever words it uses. The longest
#: legitimate side in the corpus is 28 characters ("100 mg and 150 mg once
#: daily"), so this leaves real headroom without admitting a sentence.
MAX_SIDE_CHARS = 48


def descriptive_words(value: str) -> list[str]:
    """Descriptive function words in a defect side, as whole tokens."""
    text = str(value)
    tokens = [token.strip(".,;:()[]'\"").lower() for token in text.split()]
    found = {token for token in tokens if token in DESCRIPTIVE}
    if NUMERIC_OF.search(text):
        found.discard("of")
    return sorted(found)


def main() -> int:
    cases = sorted((ROOT / "evals").glob("*/cases/*.yaml"))
    if not cases:
        print("FAILED: no evaluation cases found under evals/*/cases/*.yaml")
        return 1

    problems: list[str] = []
    assertions = sides = 0

    for path in cases:
        document = load_case(path.read_text(encoding="utf-8"), str(path))
        label = f"{path.parent.parent.name}/{document['id']}"
        for item in document["assertions"].get("mechanical", []):
            if not isinstance(item, dict) or "defect" not in item:
                continue
            assertions += 1
            for side in ("observed", "expected"):
                value = str(item.get(side, ""))
                sides += 1
                if not value.strip():
                    problems.append(f"{label}: {side} is empty")
                    continue
                if len(value) > MAX_SIDE_CHARS:
                    problems.append(
                        f"{label}: {side} is {len(value)} characters — a defect "
                        f"side binds a value, not prose: {value[:50]!r}"
                    )
                found = descriptive_words(value)
                if found:
                    problems.append(
                        f"{label}: {side} describes a value rather than being one "
                        f"— contains {found} — {value!r}. Bind the value as the "
                        "document writes it."
                    )

    print(
        f"\nDefect assertion shape: {len(cases)} case file(s), "
        f"{assertions} defect assertion(s), {sides} side(s) checked"
    )

    if problems:
        print(f"\nFAILED: {len(problems)} malformed defect side(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"PASS: {sides}/{sides} defect sides bind a value rather than a description")
    return 0


if __name__ == "__main__":
    sys.exit(main())
