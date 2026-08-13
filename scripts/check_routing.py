"""Check that the current packages' declared scopes actually partition.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: Python standard library only

Why this is a gate and not an evaluation
----------------------------------------
P20 asks whether a request lands on the right skill. Most of that question needs
model runs — but one part does not, and it is the part that fails silently.

A collection routes correctly only if two things hold, and both are properties of
the text, checkable without running anything:

1. **No two skills claim the same trigger.** If A's declared example falls
   comfortably inside B's declared scope, no router can be right, and no amount of
   evaluation will reveal which one "should" have won — the collection itself has
   not decided.

2. **Every exclusion routes somewhere.** A skill saying "do not use me for X" is
   only useful if some sibling handles X, or if X is genuinely outside the whole
   collection. An exclusion pointing at nothing sends the user in a circle.

Both are reported with denominators. The pair count is ``n(n-1)/2`` and is printed,
so "no collisions" can be read as "checked 120 pairs" rather than as an assertion
about an unknown population.

Two different measures, because the two questions are different shapes. Scope
overlap compares two similarly sized term sets, so it uses Jaccard. Exclusion
routing asks whether a short clause's subject matter is *contained* in a much
larger scope, so it uses the overlap coefficient — Jaccard was tried first and
reported that 14 of 16 exclusions routed nowhere, which reading any one of them
disproves.

**Both are screens, and neither renders a verdict.** An exclusion clause typically
excludes three or four different things at once — `verify-nca-outputs` excludes
re-deriving an analysis (outside the collection), reviewing bioanalytical
validation (a sibling), reviewing a report that quotes NCA values (another
sibling), and deciding which conflicting value is correct (the no-conclusion
boundary). Collapsing that into one similarity score and printing "routes outside
the collection" would be asserting something the measure cannot see. So this gate
prints the nearest sibling and its score, and fails only on the one condition it
can actually decide: a skill with no exclusion clause at all, which claims an
unbounded scope.
"""

from __future__ import annotations

import itertools
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

#: Words carrying no routing signal. Kept explicit rather than pulled from a
#: library so the list is auditable — a stopword list is a thumb on the scale.
STOP = {
    "a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "is", "are", "it",
    "this", "that", "with", "when", "not", "do", "use", "skill", "used", "using",
    "example", "such", "as", "by", "from", "at", "be", "been", "has", "have", "was",
    "were", "which", "what", "who", "any", "all", "its", "their", "they", "them",
    "you", "your", "we", "our", "before", "after", "into", "out", "over", "under",
    "produces", "performs", "without", "against", "each", "one", "two", "more",
    "than", "other", "also", "only", "already", "still", "should", "would", "could",
    "can", "cannot", "will", "may", "must", "if", "then", "so", "but", "no", "yes",
}

#: Above this Jaccard overlap on domain terms, two declared scopes are close
#: enough that a reviewer should look. Chosen so the known-adjacent pairs in this
#: collection surface and the unrelated ones do not; it is a screening threshold,
#: not a correctness boundary.
NEAR_THRESHOLD = 0.30

#: Below this containment, no sibling looks close to the excluded subject matter
#: and the clause is worth a human read. It flags for review; it does not decide.
#: Not a pass/fail boundary — a multi-item clause can route well and still score
#: low, because the score sees the clause as one bag of words.
ROUTE_THRESHOLD = 0.15

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)
    print(f"- {message}")


def description(skill: pathlib.Path) -> str:
    block = (skill / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    lines = [line for line in block.splitlines() if line.startswith("description:")]
    if len(lines) != 1:
        fail(f"{skill.name}: expected one description line, found {len(lines)}")
        return ""
    return lines[0][len("description:") :].strip()


def split_clauses(text: str) -> tuple[str, str]:
    """Return (inclusion, exclusion) halves of a description.

    Five phrasings are in use — "Do not use when", "Do not use for", "Do not
    use to", "Do not use it to", and "Do not use this skill". A pattern matching
    only a subset reports valid bounded skills as unbounded, so every supported
    grammatical form is regression-tested.
    """
    match = re.search(r"(?i)\bDo not use (?:when|for|to|it to|this skill)\b", text)
    if not match:
        return text, ""
    return text[: match.start()], text[match.start() :]


def terms(text: str) -> set[str]:
    words = re.findall(r"[a-z][a-z0-9\-]{2,}", text.lower())
    return {w for w in words if w not in STOP}


def jaccard(left: set[str], right: set[str]) -> float:
    """Symmetric similarity. Appropriate only when both sets are comparably sized."""
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def containment(small: set[str], large: set[str]) -> float:
    """How much of the smaller set the larger one covers.

    Jaccard is wrong for the exclusion check and was used here first. An
    exclusion clause is ~20 terms; a scope is ~90. Their union is dominated by
    the scope, so even a clause naming its sibling exactly scored ~0.08, and the
    gate reported that 14 of 16 exclusions "route outside the collection" — a
    conclusion contradicted by reading any one of them. The question being asked
    is containment ("is the excluded work claimed by a sibling?"), not
    similarity, so the measure is the overlap coefficient.
    """
    if not small or not large:
        return 0.0
    return len(small & large) / min(len(small), len(large))


def main() -> int:
    skills = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    inclusion: dict[str, set[str]] = {}
    exclusion: dict[str, str] = {}

    for skill in skills:
        text = description(skill)
        if not text:
            continue
        include, exclude = split_clauses(text)
        inclusion[skill.name] = terms(include)
        exclusion[skill.name] = exclude
        if not exclude:
            fail(
                f"{skill.name}: declares no exclusion clause, so it claims an "
                "unbounded scope and can never be routed away from"
            )

    # --- 1. do any two inclusion scopes collide? ---------------------------
    pairs = list(itertools.combinations(sorted(inclusion), 2))
    near: list[tuple[float, str, str]] = []
    for left, right in pairs:
        score = jaccard(inclusion[left], inclusion[right])  # comparable sizes: symmetric is right
        if score >= NEAR_THRESHOLD:
            near.append((score, left, right))
    near.sort(reverse=True)

    print(f"== Scope overlap ==\nchecked {len(pairs)} skill pairs "
          f"(n={len(inclusion)}, n(n-1)/2)")
    if not near:
        print(f"no pair exceeds the {NEAR_THRESHOLD:.2f} screening threshold")
    for score, left, right in near:
        # Adjacency is expected in a clinical-pharmacology collection; what is
        # NOT acceptable is adjacency without either side naming the other.
        mutual = right.replace("-", " ") in exclusion[left].lower() or left.replace(
            "-", " "
        ) in exclusion[right].lower()
        shared = ", ".join(sorted(inclusion[left] & inclusion[right])[:6])
        if mutual:
            print(f"  {score:.2f}  {left} <-> {right}  (routed explicitly)")
        else:
            print(f"  {score:.2f}  {left} <-> {right}  shared: {shared}")

    # --- 2. does every exclusion point at something real? ------------------
    print("\n== Exclusion routing ==")
    others = {name: terms(" ".join(sorted(inclusion[name]))) for name in inclusion}
    unrouted = 0
    for name in sorted(exclusion):
        if not exclusion[name]:
            continue
        excluded_terms = terms(exclusion[name])
        best_name, best = "", 0.0
        for candidate, candidate_terms in others.items():
            if candidate == name:
                continue
            score = containment(excluded_terms, candidate_terms)
            if score > best:
                best, best_name = score, candidate
        if best < ROUTE_THRESHOLD:
            unrouted += 1
            print(f"  {name}: nearest sibling {best_name} at {best:.2f} — below the "
                  f"{ROUTE_THRESHOLD:.2f} screen, read this clause by hand")
        else:
            print(f"  {name}: -> {best_name} ({best:.2f})")

    print(f"\nchecked {len(exclusion)} exclusion clauses; {unrouted} scored below the "
          f"{ROUTE_THRESHOLD:.2f} screen and are flagged for a human read, not failed")

    if failures:
        print(f"\nFAILED: {len(failures)} routing problem(s)")
        return 1
    print(f"\nPASS: {len(inclusion)} package(s), {len(pairs)} pairs screened, "
          f"{len(near)} adjacent pair(s) surfaced for review, 0 unbounded scopes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
