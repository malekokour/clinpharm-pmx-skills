"""Did a run flag one of the documented false-positive traps?

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Why this can only be written now
--------------------------------
Assertion 5 — "flags none of the five documented false-positive traps" — was
judged, and was blocked besides. Two of the five traps were unsound: the old
Table 14.2.1 printed a CL/F that disagreed with its own dose and AUC by ~30x in
every cohort, so a run reporting that irreconcilability was *correct* and would
have been scored as a false positive for it (B26).

The table has since been rebuilt. `Dose/AUC` now gives 15.2 L/h in all four
cohorts and `Cmax/Cavg` is 2.20, inside the band a one-compartment drug at
t-half 11.4 h and tau 24 h should show. Trap 1 is therefore true and trap 2 is
sound, and the question becomes measurable.

What this does and does not decide
----------------------------------
It **screens**. It finds blocks that assert a defect against something the key
says is correct, and prints them for a reader. It does not rule — deciding
whether a flagged item is genuinely a false positive is clinical, and that half
stays with the practitioner.

The distinction matters because the naive version of this check is worse than
useless. A run that *mentions* 15.2 L/h while correctly explaining that cohorts
1, 2 and 4 are fine is not flagging a trap; a keyword search would say it is.
So each trap carries both a locator pattern and a set of assertion verbs, and a
hit requires the two together in one block.

Run against the REBUILT fixture only. Runs graded before the rebuild quote the
old table's values and cannot be screened here — they would report against
numbers that no longer exist.
"""

from __future__ import annotations

import pathlib
import re
import sys


#: A block: a table row, a list item, or a paragraph. Same unit the grader binds
#: findings in, so "flagged in one place" means the same thing in both.
def blocks(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 1
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("|", "-", "*", "1.")):
            if buf:
                out.append((start, "\n".join(buf)))
                buf = []
            out.append((number, line))
        elif not stripped:
            if buf:
                out.append((start, "\n".join(buf)))
                buf = []
        else:
            if not buf:
                start = number
            buf.append(line)
    if buf:
        out.append((start, "\n".join(buf)))
    return out


#: Asserting something is wrong. A trap hit needs one of these, not a mention.
ASSERTS_DEFECT = re.compile(
    r"\b(discrepan\w+|mismatch|inconsisten\w+|error|incorrect|wrong|does not match"
    r"|disagree\w*|conflict\w*|implausible|violat\w+|fails?\b|flag\w*)",
    re.IGNORECASE,
)

#: Explicitly NOT a finding. Runs are told to show their reasoning, so a block
#: can name a trap precisely because it decided the trap is fine.
#: `correct` must not match inside `incorrect`, and `consistent` must not match
#: inside `inconsistent`. Both did, and dropped genuine trap flags: "the body
#: value 11.4 h is incorrect" was exonerated by its own accusation.
#:
#: This is the same substring-for-word error fixed in the consistency engine's
#: `parameter_label` an hour before this screen was written — where
#: "concentration" contains "ratio". Knowing the failure mode did not stop me
#: reproducing it, which is the argument for the canary rather than for care.
EXONERATES = re.compile(
    r"(?<![a-z])(no discrepan|not a discrepan|no finding|not a finding|correct\b"
    r"|consistent with|as expected|no issue|not flagged|deliberately not"
    r"|no action|verified|agrees)",
    re.IGNORECASE,
)

#: The five traps, each requiring a LOCATOR **and** the specific PREDICATE that
#: would make naming it a false positive.
#:
#: Rewritten 2026-08-06 after the first version returned 7 hits of which every
#: readable one was a genuine defect: D3's accumulation ratio caught as T1,
#: D2's synopsis half-life caught as T3, and D8's significant-figure breach
#: caught as T4. Malek predicted that last collision before the screen existed —
#: "the slope 1.08 with CI 0.94-1.22 is simultaneously a false-positive trap and
#: the site of D8; if it's keyword-matching on 1.08 these will cross-contaminate."
#: They did.
#:
#: The fix is not a tighter number pattern. A trap and the defect sharing its
#: numbers are distinguished by *what is claimed about them*, so each entry now
#: pairs a locator with the predicate that makes it a false positive. Written
#: before any run it is applied to, and frozen.
TRAPS = {
    # Claiming a NON-cohort-3 clearance is wrong. D4 is cohort 3 and is real.
    "T1 cohorts 1/2/4 CL/F": (
        re.compile(r"cohort\s*[124]\b", re.IGNORECASE),
        re.compile(r"CL/F|clearance", re.IGNORECASE),
    ),
    # Comparing AUC directly against Cmax as if a mismatch. The ratio-versus-
    # half-life argument is legitimate PK and is NOT this trap.
    "T2 AUC compared against Cmax": (
        re.compile(r"cohort\s*2\b", re.IGNORECASE),
        re.compile(r"(AUC.{0,40}(vs\.?|versus|against|does not match|differs from).{0,20}Cmax"
                   r"|Cmax.{0,40}(vs\.?|versus|against|does not match|differs from).{0,20}AUC)",
                   re.IGNORECASE),
    ),
    # Claiming the BODY's 11.4 h is the error. The synopsis's 8.2 h is D2.
    "T3 body half-life 11.4 h": (
        re.compile(r"11\.4", re.IGNORECASE),
        re.compile(r"(body|§\s*12\.3|section\s*12\.3).{0,60}(incorrect|wrong|error|should be)"
                   r"|(incorrect|wrong|error|should be).{0,60}(body|§\s*12\.3)", re.IGNORECASE),
    ),
    # Concluding NON-PROPORTIONALITY from a CI that spans 1.0. The significant-
    # figure inconsistency on the same three numbers is D8 and is real.
    "T4 non-proportionality from slope 1.08": (
        re.compile(r"1\.08", re.IGNORECASE),
        re.compile(r"(not|non-?)\s*(dose[- ])?proportional|fails?\s+proportionality"
                   r"|proportionality\s+(is\s+)?(not\s+)?(demonstrated|supported|met)",
                   re.IGNORECASE),
    ),
    # Claiming the food-effect ratio itself is a defect.
    "T5 food-effect AUC ratio 1.29": (
        re.compile(r"1\.29", re.IGNORECASE),
        re.compile(r"(discrepan|mismatch|inconsisten|implausible|error|incorrect)", re.IGNORECASE),
    ),
}


def screen(run: pathlib.Path) -> dict[str, object] | None:
    response = run / "outputs/response.md"
    if not response.is_file():
        response = run / "response.md"
    if not response.is_file() or response.stat().st_size == 0:
        return None
    text = response.read_text(encoding="utf-8", errors="replace")

    hits: list[dict[str, object]] = []
    for name, (locator, predicate) in TRAPS.items():
        for line_number, block in blocks(text):
            # Both the locator AND the trap-specific predicate must be present.
            # The locator alone is what produced the false alarms: D8 and trap 4
            # share three numbers and differ only in what is claimed about them.
            if not (locator.search(block) and predicate.search(block)):
                continue
            if not ASSERTS_DEFECT.search(block):
                continue
            if EXONERATES.search(block):
                continue
            hits.append({"trap": name, "line": line_number, "excerpt": block[:160].replace("\n", " ")})
            break
    return {"run": run.name, "hits": hits}


def main(root: pathlib.Path) -> int:
    runs = sorted(d for d in root.iterdir() if d.is_dir() and d.name.startswith("run-"))
    results = [r for run in runs if (r := screen(run))]
    if not results:
        print(f"FAILED: no runs with a response under {root}")
        return 1

    print("Assertion 5 screen — traps apparently flagged as defects.")
    print("A SCREEN, NOT A RULING. Every hit needs a clinical read before it counts.\n")
    total = 0
    for result in results:
        hits = result["hits"]
        assert isinstance(hits, list)
        total += len(hits)
        print(f"{result['run']}: {len(hits)} apparent trap flag(s) of {len(TRAPS)}")
        for hit in hits:
            print(f"    {hit['trap']}  (line {hit['line']})")
            print(f"      {hit['excerpt']}")
    print(f"\n{total} apparent flag(s) across {len(results)} run(s), {len(TRAPS)} traps each.")
    print("0 would be a clean precision result. Anything above 0 is a candidate list,")
    print("not a failure — a run may name a trap precisely because it cleared it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(pathlib.Path(sys.argv[1])))
