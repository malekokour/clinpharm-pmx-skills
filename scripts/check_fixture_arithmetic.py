"""A fixture's own numbers must reconcile with each other.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Why this gate exists
--------------------
`check_fixture_grounding` proves that an assertion's values appear in the fixture.
Nothing proved that the fixture's values are consistent *with each other* — so a
fixture could be perfectly grounded and pharmacokinetically impossible, and every
other gate would stay green.

On 2026-08-06 the owner read Table 14.2.1 of the hero fixture and spotted in one
pass what the whole automated apparatus had missed across nine graded runs:

```
| Cohort | Dose (mg) | AUC0–τ (ng·h/mL) | Cmax (ng/mL) | CL/F |
| 2      | 100       | 206              | 124          | 15.1 L/h |
```

`Dose / AUC0–τ` is 485 L/h. The table prints 15.1 L/h — a 30-fold disagreement,
present in all four cohorts, including the three the expert key lists as a
*false-positive trap* on the grounds that their CL/F is correct. A run reporting
that irreconcilability is doing valid pharmacokinetics and is scored as a false
positive for it.

That inverts the interpretation of precision, which was the only clean-looking
score family in the evaluation.

What this checks
----------------
Only relations that are arithmetic, not judgment:

- **CL/F reconciles with dose and AUC.** At steady state CL/F = Dose / AUC0–τ.
  Flagged beyond a generous 2-fold band, because fixtures round and the point is
  to catch order-of-magnitude construction errors, not rounding.

It deliberately does not check plausibility of half-life against accumulation or
peak-to-trough: those depend on compartmental assumptions the fixture may not
state, and a gate that guesses at them would manufacture the false positives it
exists to prevent. Where a fixture states t½ and τ explicitly, that check belongs
in a later pass with the assumptions written down.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: `| 2 | 100 | 206 | 124 | 15.1 L/h |` — dose, AUC, Cmax, CL/F in one row.
ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*(?P<dose>\d+(?:\.\d+)?)\s*\|\s*(?P<auc>\d+(?:\.\d+)?)\s*\|"
    r"\s*(?P<cmax>\d+(?:\.\d+)?)\s*\|\s*\**(?P<clf>\d+(?:\.\d+)?)\s*(?P<unit>m?L/h)\**\s*\|",
    re.MULTILINE,
)

#: Header confirming the units this check assumes: dose in mg, AUC in ng·h/mL.
HEADER = re.compile(r"Dose\s*\(mg\).*AUC[^|]*\(ng·h/mL\)", re.IGNORECASE)

#: Fixtures round; a 2-fold band catches construction errors, not presentation.
TOLERANCE_FOLD = 2.0


def main() -> int:
    problems: list[str] = []
    outliers: list[str] = []
    tables = rows_checked = 0

    for fixture in sorted((ROOT / "evals").rglob("fixtures/*.md")):
        if "EXPERT-KEY" in fixture.name.upper():
            continue
        text = fixture.read_text(encoding="utf-8", errors="replace")
        if not HEADER.search(text):
            continue
        tables += 1
        matches = list(ROW.finditer(text))
        # A fixture may deliberately plant a unit swap in one row — that is a
        # defect under test, not a construction error. Reconcile every row against
        # the column's MAJORITY unit so the arithmetic check measures what it is
        # for, and report the outlier separately instead of failing on it.
        units = [m.group("unit").lower() for m in matches]
        majority = max(set(units), key=units.count) if units else "l/h"
        for match in matches:
            rows_checked += 1
            dose_mg = float(match.group("dose"))
            auc = float(match.group("auc"))
            printed = float(match.group("clf"))
            unit = match.group("unit").lower()
            if unit != majority:
                outliers.append(
                    f"{fixture.relative_to(ROOT)}: one row prints CL/F in {match.group('unit')} "
                    f"where the column's other rows use {majority} — reconciled against "
                    f"{majority}; if this is a planted unit defect that is expected, and if "
                    "it is not, it is one"
                )
            if majority == "ml/h":
                printed /= 1000.0
            if auc <= 0:
                continue
            # ng / (ng.h/mL) = mL/h; /1000 -> L/h
            implied = (dose_mg * 1e6) / auc / 1000.0
            fold = max(implied, printed) / min(implied, printed)
            if fold > TOLERANCE_FOLD:
                rel = fixture.relative_to(ROOT)
                problems.append(
                    f"{rel}: dose {dose_mg:g} mg with AUC0–τ {auc:g} ng·h/mL implies "
                    f"CL/F {implied:.1f} L/h, but the table prints {printed:.4g} L/h "
                    f"({fold:.0f}-fold apart). The fixture contradicts itself, so a run "
                    "reporting this is correct and any trap calling it a false positive "
                    "is wrong"
                )

    for note in outliers:
        print(f"  note: {note}")
    for problem in problems:
        print(f"- {problem}")
    if problems:
        print(f"\nFAILED: {len(problems)} internally inconsistent fixture row(s)")
        return 1
    print(
        f"PASS: {rows_checked} PK parameter row(s) across {tables} table(s) — CL/F "
        f"reconciles with dose and AUC in every one ({len(outliers)} unit outlier(s) noted)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
