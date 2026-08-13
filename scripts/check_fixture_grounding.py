"""Every defect assertion's values must actually appear in that skill's fixtures.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Why this gate exists
--------------------
A defect assertion says "the document reads X where the source says Y". If X or Y
is not in the fixture at all, the assertion is **unfalsifiable**: no response could
ever satisfy it, and no response could ever be shown to have missed something real.
It would look exactly like a hard case and behave exactly like a broken one.

That is the specific failure mode of authoring fixtures at volume, and it is
invisible to every other gate here. `eval_suite_check` proves the YAML is
well-formed. The grader proves a response does or does not contain the values.
Neither asks whether the values were ever in the source documents.

The check is deliberately literal: the exact string, case-insensitively, somewhere
in the skill's own `fixtures/`. Whitespace is normalised because a value can wrap
across lines in a markdown table; nothing else is relaxed, because a "close enough"
match is how a wrong number passes.
"""

from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from eval_schema import load_case

ROOT = pathlib.Path(__file__).resolve().parent.parent


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


#: A defect assertion binds "the document says X where the source says Y". Both
#: sides must be *short and specific* enough that a response reporting the defect
#: cannot avoid reproducing them, and at least one must carry a number, since a
#: mismatch between two bare words is a judgment rather than a value comparison.
#:
#: Not "both sides numeric". That rule was tried first and rejected the adjudicated
#: CSR fixture's D6, which binds `decrease` against `1.34` — a reversed comparison
#: direction, and a perfectly good value defect. A rule that fails the one fixture
#: known to produce defensible results is wrong about the rule, not the fixture.
#: The essence of a value mismatch is that the two sides are *nearly the same*
#: and differ in a value. `80 mg once daily` against `60 mg once daily` differ in
#: one token and are a textbook example. `time-dependent inhibitor of CYP3A4`
#: against `Total studies listed: 6` share nothing — they are not two readings of
#: one fact, they are a description of an absence dressed as a comparison.
#:
#: Word count was tried first and was the wrong measure twice: at three words it
#: rejected `80 mg once daily`, and any limit loose enough to admit that also
#: admits prose. Difference, not length, is what distinguishes the two.
# 4, not 3: a date pair such as `31 March 2027` against `30 September 2027`
# differs in four tokens and is plainly a value mismatch. Prose pairs differ in
# eight or more, so the boundary is not delicate.
MAX_DIFFERING_TOKENS = 4
MAX_TOKENS = 8


def _tokens(text: str) -> list[str]:
    return [w.strip(".,;:()").casefold() for w in text.split() if w.strip(".,;:()")]


def value_shaped(pair: tuple[str, str]) -> bool:
    """True when the pair reads as two values of one fact rather than as prose."""
    left, right = (_tokens(s) for s in pair)
    if not left or not right:
        return False
    if len(left) > MAX_TOKENS or len(right) > MAX_TOKENS:
        return False

    differing = set(left).symmetric_difference(right)
    if len(differing) > MAX_DIFFERING_TOKENS:
        return False

    # At least one thing that actually differs must be a value, otherwise the pair
    # differs only in wording and the "mismatch" is a judgment call.
    if any(any(ch.isdigit() for ch in tok) for tok in differing):
        return True
    # No digit among the differences is still a value pair for compact tokens —
    # `mL/h` against `L/h` is the adjudicated D4 unit swap, and a rule that failed
    # the one fixture known to produce defensible results would be wrong about the
    # rule, not the fixture.
    return all(len(tok) <= 12 for tok in differing)


def main() -> int:
    problems: list[str] = []
    checked = skipped_no_fixture = 0
    suites_with_defects = 0

    for suite in sorted((ROOT / "evals").iterdir()):
        cases_dir = suite / "cases"
        if not cases_dir.is_dir():
            continue
        fixtures = suite / "fixtures"
        blob = ""
        if fixtures.is_dir():
            for f in sorted(fixtures.rglob("*")):
                # The expert key is not a source document. Grounding an assertion
                # in the answer key would be circular: the key restates the very
                # values the fixture is supposed to contain, so a defect that was
                # never planted would still "ground" successfully.
                if f.is_file() and "EXPERT-KEY" not in f.name.upper():
                    blob += "\n" + f.read_text(encoding="utf-8", errors="replace")
        haystack = normalise(blob)

        suite_has_defects = False
        for case_path in sorted(cases_dir.glob("*.yaml")):
            case = load_case(case_path.read_text(encoding="utf-8"), str(case_path))
            for assertion in case["assertions"].get("mechanical", []):
                if "defect" not in assertion:
                    continue
                suite_has_defects = True
                if not haystack:
                    skipped_no_fixture += 1
                    problems.append(
                        f"{suite.name}/{case_path.name}: asserts defect "
                        f"{assertion['defect']} but the suite has no readable fixture "
                        "documents — the assertion cannot be grounded in anything"
                    )
                    continue
                # A defect assertion whose sides are not both value-shaped is not
                # describing a value mismatch. On 2026-08-06, 82 of 122 such
                # assertions across fifteen suites bound prose like
                # "time-dependent inhibitor of CYP3A4" against
                # "Total studies listed: 6" — completeness gaps and unsupported
                # claims forced into an X-versus-Y shape. The defect there is an
                # absence, so there is no observed value to bind, and the grader
                # ended up testing whether a response reproduced an invented
                # string. Those belong in `must_contain` or in the judged layer.
                if not value_shaped((str(assertion["observed"]), str(assertion["expected"]))):
                    problems.append(
                        f"{suite.name}/{case_path.name}: {assertion['defect']} binds "
                        f"{assertion['observed']!r} against {assertion['expected']!r}, "
                        "which is not a value pair — a `defect` assertion means "
                        "'the document says X where the source says Y'. A completeness "
                        "gap or unsupported claim belongs in `must_contain` or the "
                        "judged layer"
                    )
                for field in ("observed", "expected"):
                    value = normalise(str(assertion[field]))
                    checked += 1
                    if value not in haystack:
                        problems.append(
                            f"{suite.name}/{case_path.name}: {assertion['defect']}."
                            f"{field} is {assertion[field]!r}, which appears nowhere in "
                            f"evals/{suite.name}/fixtures/ — the assertion is "
                            "unfalsifiable as written"
                        )
        suites_with_defects += suite_has_defects

    for problem in problems:
        print(f"- {problem}")
    if problems:
        print(f"\nFAILED: {len(problems)} ungrounded assertion value(s)")
        return 1
    print(
        f"PASS: {checked} defect assertion value(s) across {suites_with_defects} "
        f"suite(s) all appear verbatim in their own fixtures"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
