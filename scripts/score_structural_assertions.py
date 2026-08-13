"""Score the judged assertions that never needed a clinical reader.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Why this exists
---------------
Five assertions on the hero case were classified `judged` and therefore failed
closed in every arm, on the stated grounds that nobody had scored them. During
R7 adjudication Malek pointed out that this conflates *unscored* with *failed*,
and that four of the five need no clinical judgment at all:

> "Assertions 2, 3 and 4 are structural — locator present, disposition field =
>  open, tolerance value and its source cited — and none of them need a clinical
>  read. Those four should not be failing closed for want of a clinical
>  pharmacologist; they should be scored by a script."

He is right, and the error is the same category mistake as scoring a detection
success as a detection failure because its severity label was wrong (B24).

What is scored here, and what deliberately is not
-------------------------------------------------
| # | Assertion | Scored how |
|---|---|---|
| 1 | Detects >= 11 of 12 keyed defects | arithmetic, from the grading record |
| 2 | Every finding carries a locator | structural |
| 3 | Every disposition is `open` | structural |
| 4 | Names the tolerance and cites its source | structural |
| 5 | Flags none of the five traps | **NOT scored — needs judgment, and is blocked on B26** |

Assertion 5 stays judged for two independent reasons. It requires deciding
whether a flagged item is a false positive, which is clinical. And B26 showed
two of the five traps are unsound — the fixture's CL/F disagrees with its own
dose and AUC, so a run reporting that irreconcilability is correct and would be
scored as a false positive for it. Scoring assertion 5 against traps known to be
wrong would manufacture exactly the result this project keeps catching.

The output is a *screen*, not a verdict. It reports what each run does
structurally so a reviewer spends their time on assertion 5 and on the earned-
marker residue, rather than on counting locators by hand.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

#: A register row: pipe-delimited, at least four cells.
ROW = re.compile(r"^\s*\|.*\|.*\|.*\|", re.MULTILINE)

#: Any locator a reviewer could actually turn to.
LOCATOR = re.compile(
    r"(§|\bSection\b|\bTable\b|\bFigure\b|\bAppendix\b|\bSynopsis\b|\bProtocol\b"
    r"|\bp\.\s*\d|\bpage\s*\d|\bline\s*\d|\bListing\b|\bcohort\s*\d|\b\d+\.\d+\.\d+\b)",
    re.IGNORECASE,
)

#: `disposition: open` in any of the shapes the register uses.
DISPOSITION = re.compile(r"disposition[^|\n]{0,20}[:|]\s*`?(\w+)", re.IGNORECASE)

#: A tolerance figure, and separately a citation of where it came from.
TOLERANCE = re.compile(r"(\d+(?:\.\d+)?\s*%|tolerance)", re.IGNORECASE)
PLAN_SOURCE = re.compile(
    r"(analysis plan|PK analysis plan|SAP|statistical analysis plan|I4)", re.IGNORECASE
)


def score(run: pathlib.Path) -> dict[str, object] | None:
    """Score one run. Returns None when the run has no response to read."""
    # Two layouts in the wild: the staging harness writes `outputs/response.md`,
    # the preserved evidence directories write `response.md` beside the grading
    # record. Accept both rather than silently finding nothing — an empty result
    # from a path mismatch looks exactly like an empty result from no data.
    response = run / "outputs/response.md"
    if not response.is_file():
        response = run / "response.md"
    if not response.is_file() or response.stat().st_size == 0:
        return None
    text = response.read_text(encoding="utf-8", errors="replace")

    # Count only rows that could BE findings. The first pass counted every
    # pipe-delimited line — headers, separators, and unrelated tables — and
    # reported "51% of rows carry a locator", a percentage of the wrong
    # denominator. A finding row names a defect or a discrepancy; a header does
    # not.
    rows = [
        r
        for r in ROW.findall(text)
        if not set(r.strip()) <= set("|- :")
        and not re.search(r"\|\s*(id|#|item|finding|severity|location|status)\s*\|", r, re.IGNORECASE)
    ]
    with_locator = [r for r in rows if LOCATOR.search(r)]

    dispositions = DISPOSITION.findall(text)
    non_open = [d for d in dispositions if d.lower() != "open"]

    # A grading record produced by a superseded grader is not evidence, and it
    # is indistinguishable from a current one by filename. On 2026-08-06 this
    # script read six v1 records — mtime 14:11, grader rebuilt 16:28 — and
    # reported 5/5 detection for every arm including the no-skill baseline. One
    # of those records passed D4 on the evidence "the CLI reported **no
    # finding**", which is the precise defect the rebuild removed.
    #
    # So: refuse any record older than the grader that would have produced it,
    # and say so, rather than reporting a retracted number as current.
    detected = total = None
    stale = False
    grading = run / "grading.json"
    grader = pathlib.Path(__file__).resolve().parent / "eval_grade.py"
    if grading.is_file() and grader.is_file() and grading.stat().st_mtime < grader.stat().st_mtime:
        stale = True
    if grading.is_file() and not stale:
        record = json.loads(grading.read_text(encoding="utf-8"))
        defects = [
            e for e in record.get("expectations", []) if e.get("text", "").startswith("Detects D")
        ]
        if defects:
            detected = sum(1 for e in defects if e.get("passed"))
            total = len(defects)

    return {
        "run": run.name if "run-" in run.name and "_" in run.name else f"{run.parent.name}/{run.name}",
        "rows": len(rows),
        "locator": len(with_locator),
        "dispositions": len(dispositions),
        "non_open": len(non_open),
        "tolerance": bool(TOLERANCE.search(text)),
        "cites_plan": bool(PLAN_SOURCE.search(text)),
        "detected": detected,
        "asserted": total,
        "stale": stale,
    }


def main(root: pathlib.Path) -> int:
    candidates = sorted(root.glob("*/run-*")) + sorted(
        d for d in root.iterdir() if d.is_dir() and "run-" in d.name
    )
    results = [s for run in candidates if (s := score(run))]
    if not results:
        print(f"FAILED: no runs with a response found under {root}")
        return 1

    print("Structural assertions 2-4, scored mechanically. Assertion 5 is NOT here:")
    print("it needs judgment AND two of its five traps are unsound under B26.\n")
    print(f"{'run':<22}{'rows':>6}{'w/ locator':>12}{'dispositions':>14}{'non-open':>10}{'tol':>5}{'cites plan':>12}")
    for r in results:
        print(
            f"{r['run']:<22}{r['rows']:>6}{r['locator']:>12}{r['dispositions']:>14}"
            f"{r['non_open']:>10}{'Y' if r['tolerance'] else 'n':>5}{'Y' if r['cites_plan'] else 'n':>12}"
        )

    rows = sum(int(r["rows"]) for r in results)
    loc = sum(int(r["locator"]) for r in results)
    non_open = sum(int(r["non_open"]) for r in results)
    print(f"\nA2  locator present     {loc}/{rows} rows ({100 * loc / rows:.0f}%)")
    print(f"A3  disposition open    {non_open} non-open across {len(results)} runs — 0 is a pass")
    print(f"A4  tolerance + source  {sum(1 for r in results if r['tolerance'] and r['cites_plan'])}/{len(results)} runs state both")

    stale = [r for r in results if r["stale"]]
    if stale:
        print(
            f"\n!!  {len(stale)} of {len(results)} grading record(s) PREDATE the current grader "
            f"and were NOT read.\n"
            "    A record produced by a superseded grader is not evidence. Re-grade before\n"
            "    quoting any detection figure from this directory."
        )
    scored = [r for r in results if r["detected"] is not None]
    if scored:
        print("\nA1  detection, from the grading record (denominator is what the case asserts,")
        print("    not the key's twelve — see B23):")
        for r in scored:
            print(f"      {r['run']:<20} {r['detected']}/{r['asserted']}")

    print(
        "\nThis is a screen, not a verdict. It exists so a reviewer spends their time on\n"
        "assertion 5 and the earned-marker residue rather than counting locators by hand."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(pathlib.Path(sys.argv[1])))
