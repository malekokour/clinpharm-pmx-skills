#!/usr/bin/env python3
"""Check the *claims* public surfaces make, not the numbers they state.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

Why this exists, and why it is not `check_claim_ledger.py`
----------------------------------------------------------
`check_claim_ledger.py` guarantees something narrow and valuable: **no public
surface states a count that its source of record contradicts.** It says so
itself. Every defect it catches is a number.

On 2026-08-13 a defect slipped past it that was not a number.

`CLAIM-LEDGER.md` said:

    `released` — the package's evaluation gate has been run and passed.

while `AGENTS.md` said, correctly:

    passed the structural gates … evaluation-gate qualification is explicitly
    incomplete — see CLAIM-LEDGER.md

So the document carrying the caveat **cited as its authority the document
denying it**. A reader who followed the pointer — which is what a careful reader
does — landed on the overclaim. Every count on both pages was correct
throughout.

The claim was false for a reason worth stating plainly: all three
`blocker`-severity findings against the evaluation suite are open and frozen,
and all three are themselves `kind: vacuous-check`. The suite said to have
"passed" is the one suite this project had already established cannot
discriminate a good run from a bad one.

The mechanism
-------------
A claim gets stronger each time it is restated one document further from its
evidence::

    "passed PS-D024 qualification"                  precise, true, checkable
      -> "passed its assigned evidence gate"        vaguer, still defensible
        -> "the evaluation gate has been run and passed"    false

No single step is a lie. Each is a fair paraphrase of the one before. The drift
is invisible from inside any single document, which is why careful writing
cannot catch it and a cross-surface check can.

`AGENTS.md` already prohibited the end state in prose — *"Do not write 'passes
every gate': name the gate."* That rule was live, correct, and violated one line
below its own citation. Prose is the weakest enforcement layer available; this
file moves the same three rules to the strongest one that fits.

What is checked
---------------
1. **Banned overclaims** — phrasings that assert a gate stronger than the one
   that ran. Absence is necessary but not sufficient, which is why 2 and 3 exist.
2. **Status-vocabulary anchor** — every surface that *defines* `released` must
   also carry the disclaimer. Definition and caveat travel together or the
   caveat is one copy-paste from being lost.
3. **Badge / attestation agreement** — the README's works-with badge may name a
   host only if it appears in `catalog/adapter-evidence.json` `hosts[]`. That
   file is an allowlist; this check is what makes it one in practice rather than
   in intent.

Design note, so a later reader can disagree deliberately
--------------------------------------------------------
Check 2 tests for a **short canonical anchor substring**, not for identical
paragraphs and not for a semantic match. Three options were considered:

    (a) require byte-identical paragraphs   -> rejected: forces awkward prose and
                                               breaks on a comma
    (b) ban a list of phrases only          -> rejected: this is what AGENTS.md
                                               already did, and it failed
    (c) require a short shared anchor       -> chosen

(c) is the weakest check that would actually have caught the real defect, and it
leaves each surface free to phrase the surrounding paragraph for its own reader.
Its known limit: a surface could carry the anchor and still contradict it
elsewhere on the page. That is a smaller hole than the one being closed, and
narrowing it further needs a human reading, not a stricter regex.

Proving it works
----------------
Run with ``--canary`` to plant each defect in memory, confirm the check goes
red, then confirm it goes green again with the real files. A gate nobody has
watched fail is untested, and three of this repository's own open findings are
checks that passed over nothing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Surfaces that may state what `released` means. Adding a surface here is the
#: deliberate act of putting it under this gate.
STATUS_SURFACES = ("README.md", "CLAIM-LEDGER.md", "AGENTS.md")

#: The shared anchor. Short on purpose -- see the design note above. Any surface
#: that defines `released` must also say this, so the definition cannot travel
#: without its caveat.
STATUS_ANCHOR = "evaluation"

#: A surface only has to carry the anchor if it actually defines the word.
#:
#: The first version of this pattern was ``\`released\`\s*[-—|]`` — a dash or a
#: table pipe. It matched `README.md` and `CLAIM-LEDGER.md` and **missed
#: `AGENTS.md`**, which writes *"What `released` means here, precisely."* That is
#: the one surface whose wording was correct throughout, so the gate reported a
#: confident PASS over a denominator of 2 while believing it covered 3 — and had
#: anyone later broken `AGENTS.md`, it would have stayed green. Caught by reading
#: the PASS line's own number against `STATUS_SURFACES`, which is the only reason
#: a denominator belongs in a PASS line at all.
DEFINES_RELEASED = re.compile(
    r"`released`\s*(?:[-—|]|means\b|is\b)", re.IGNORECASE
)

#: Phrasings that assert a gate stronger than the one that ran. Each entry is
#: (regex, why it is banned).
BANNED_CLAIMS: tuple[tuple[str, str], ...] = (
    (r"pass(?:es|ed)?\s+(?:every|all)\s+gates?",
     "names no gate; the evaluation suite is frozen with three open blockers"),
    (r"fully\s+validated",
     "'validated' has a specific regulatory meaning this project does not claim"),
    (r"clinically\s+validated",
     "no package has clinical validation"),
    (r"GxP[- ]validated",
     "no package has GxP validation"),
    (r"evaluation\s+gate\s+has\s+been\s+run\s+and\s+passed",
     "the exact 2026-08-13 overclaim; the evaluation suite is frozen"),
)

#: Files the banned-claim scan reads. Docs under archive/ are dated historical
#: records and are excluded deliberately -- they describe a past state.
def public_markdown() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".venv/", "docs/archive/", "skills/")):
            continue
        out.append(p)
    return out


ATTESTATION = ROOT / "catalog" / "adapter-evidence.json"
README = ROOT / "README.md"

#: The works-with badge. Group 1 is the URL-encoded host list.
BADGE = re.compile(r"!\[Works with\]\(https://img\.shields\.io/badge/[^-]+-([^-]+)-")


#: A prohibition verb beside a quoted phrase means the text is *forbidding* the
#: claim, not making it. `AGENTS.md` bans "passes every gate" by quoting it, and
#: this file's own docstring quotes the 2026-08-13 overclaim in order to explain
#: it. Borrowed from `scan_skills.py`, which solved the identical problem for
#: prompt-injection strings; its rule that quoted hits stay *counted* rather than
#: allowlisted away is kept here too, so the number never silently reaches zero.
PROHIBITION = re.compile(
    r"(?i)\b(?:do not write|never write|do not say|never say|must not|do not claim"
    r"|prohibited|banned|is an overclaim|was an overclaim|previously read"
    r"|name the gate|does \*?\*?not\*?\*? mean|rejected)\b"
)

#: The claim wrapped in quotes — straight, curly, or backtick.
QUOTED = re.compile(r"[\"“”'`*]")

#: How far either side of a match to look for the quote-and-verb pair. A wrapped
#: sentence stays inside this; an unrelated paragraph does not.
WINDOW = 160


def classify(text: str, start: int, end: int) -> str:
    """Return 'bare' (a real overclaim) or 'quoted-prohibition' (documentation).

    Unlike `scan_skills.py` this looks at a character window rather than a
    single line, because a banned phrase can wrap: the real 2026-08-13 hit in
    `CLAIM-LEDGER.md` matched as ``'passes every\\ngate'``, which a line-based
    classifier splits in half and misses on both halves.
    """
    around = text[max(0, start - WINDOW) : end + WINDOW]
    if QUOTED.search(around) and PROHIBITION.search(around):
        return "quoted-prohibition"
    return "bare"


def check_banned(problems: list[str], texts: dict[str, str]) -> tuple[int, int]:
    checked = 0
    quoted = 0
    for name, text in texts.items():
        checked += 1
        for pattern, why in BANNED_CLAIMS:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                if classify(text, m.start(), m.end()) == "quoted-prohibition":
                    quoted += 1
                    continue
                line = text[: m.start()].count("\n") + 1
                problems.append(
                    f"{name}:{line}: banned claim {m.group(0)!r} — {why}"
                )
    return checked, quoted


def check_anchor(problems: list[str], texts: dict[str, str]) -> int:
    checked = 0
    for name in STATUS_SURFACES:
        text = texts.get(name)
        if text is None:
            problems.append(f"{name}: listed in STATUS_SURFACES but not readable")
            continue
        if not DEFINES_RELEASED.search(text):
            continue
        checked += 1
        if STATUS_ANCHOR.lower() not in text.lower():
            problems.append(
                f"{name}: defines `released` but never says {STATUS_ANCHOR!r} — "
                "the definition must not travel without its caveat"
            )
    return checked


def check_badge(problems: list[str], readme: str) -> int:
    if not ATTESTATION.is_file():
        problems.append(
            "catalog/adapter-evidence.json is missing — the badge has no source"
        )
        return 0
    data = json.loads(ATTESTATION.read_text(encoding="utf-8"))
    allowed = {h["display_name"] for h in data.get("hosts", [])}
    denied = {h["display_name"] for h in data.get("not_evidenced", [])}

    if allowed & denied:
        problems.append(
            "adapter-evidence.json: "
            f"{sorted(allowed & denied)} appear in both hosts[] and not_evidenced[]"
        )
    for h in data.get("hosts", []):
        bad = [s for s in h.get("lifecycle_steps_executed", []) if s.get("exit") != 0]
        if bad:
            problems.append(
                f"adapter-evidence.json: {h['display_name']} is in hosts[] but "
                f"records a non-zero exit for {[s['step'] for s in bad]}"
            )

    m = BADGE.search(readme)
    if not m:
        problems.append("README.md: no works-with badge found to check")
        return len(allowed)

    named = {
        part.strip()
        for part in m.group(1).replace("%20", " ").split("%7C")
        if part.strip()
    }
    for host in sorted(named - allowed):
        problems.append(
            f"README.md: badge names {host!r}, which is not in "
            "adapter-evidence.json hosts[] — untested is not a works-with claim"
        )
    for host in sorted(allowed - named):
        problems.append(
            f"README.md: {host!r} has executed evidence but the badge omits it"
        )
    return len(allowed)


def run(texts: dict[str, str]) -> list[str]:
    problems: list[str] = []
    check_banned(problems, texts)
    check_anchor(problems, texts)
    check_badge(problems, texts.get("README.md", ""))
    return problems


def load() -> dict[str, str]:
    texts = {
        p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8", errors="replace")
        for p in public_markdown()
    }
    # AGENTS.md is a real file; CLAUDE.md and GEMINI.md are symlinks to it, so
    # they are read but never independently authoritative.
    return texts


def canary() -> int:
    """Plant each defect, confirm red **for the planted reason**; restore, confirm green.

    The first version of this function only asked *"is there any problem?"*. It
    reported three confident RED-as-expected lines while every one of them was
    firing on the same unrelated false positive, and not one planted defect was
    actually detected. That is a vacuous canary — a check on a check that passed
    over nothing — and it is the third instance of that shape in this repository.
    So each case now carries a `expect` fragment, and the planted defect only
    counts as caught if a problem mentioning that fragment appears.
    """
    real = load()
    if not real.get("README.md"):
        print("FAIL: cannot canary — README.md unreadable")
        return 1

    #: (label, mutated texts, fragment that MUST appear in the resulting problem)
    cases: list[tuple[str, dict[str, str], str]] = []

    bad = dict(real)
    bad["README.md"] = real["README.md"] + "\n\nEvery package passes every gate.\n"
    cases.append(("banned claim planted in README", bad, "banned claim"))

    bad = dict(real)
    bad["CLAIM-LEDGER.md"] = re.sub(
        r"(?i)evaluation", "assessment", real.get("CLAIM-LEDGER.md", "`released` — x")
    )
    cases.append(("caveat anchor stripped from CLAIM-LEDGER.md", bad, "caveat"))

    # AGENTS.md defines `released` with the word "means", not a dash. The first
    # detector missed it entirely, so it gets its own case: the surface that was
    # right all along is the one most worth watching for regression.
    bad = dict(real)
    bad["AGENTS.md"] = re.sub(
        r"(?i)evaluation", "assessment", real.get("AGENTS.md", "`released` means x")
    )
    cases.append(("caveat anchor stripped from AGENTS.md", bad, "AGENTS.md"))

    bad = dict(real)
    bad["README.md"] = real["README.md"].replace(
        "Claude%20Code%20%7C%20Cursor",
        "Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20CLI",
    )
    cases.append(("badge names an unevidenced host", bad, "badge names"))

    baseline = run(real)
    failures = 0

    for label, texts, expect in cases:
        problems = run(texts)
        new = [p for p in problems if p not in baseline]
        hit = [p for p in new if expect in p]
        if hit:
            print(f"  RED for the planted reason — {label}\n      {hit[0]}")
        elif new:
            print(
                f"  RED, BUT FOR THE WRONG REASON — {label}\n"
                f"      expected a problem mentioning {expect!r}, got: {new[0]}"
            )
            failures += 1
        else:
            print(f"  NOT RED — {label}: the gate did not notice the planted defect")
            failures += 1

    if baseline:
        print(f"  NOT GREEN on the real files: {baseline[0]}")
        failures += 1
    else:
        print("  GREEN on the real files")

    if failures:
        print(f"\nFAIL: canary found {failures} problem(s) with the gate itself")
        return 1
    print(
        f"\nPASS: gate goes red for the right reason on {len(cases)}/{len(cases)} "
        "planted defects, and green on the real tree"
    )
    return 0


def main() -> int:
    if "--canary" in sys.argv:
        return canary()

    texts = load()
    problems: list[str] = []
    n_banned, n_quoted = check_banned(problems, texts)
    n_anchor = check_anchor(problems, texts)
    n_hosts = check_badge(problems, texts.get("README.md", ""))

    if problems:
        for p in problems:
            print(f"  {p}")
        print(f"\nFAIL: {len(problems)} claim-consistency problem(s)")
        return 1

    # Every number here is a denominator. A PASS line that does not say what it
    # examined is indistinguishable from a PASS line for a check that read
    # nothing, which is the failure this repository files findings about.
    print(
        f"PASS: claim consistency — {n_banned} public Markdown file(s) scanned for "
        f"{len(BANNED_CLAIMS)} banned claim(s) ({n_quoted} hit(s) quoted inside a "
        f"prohibition, counted not ignored); {n_anchor} surface(s) defining "
        f"`released` carry the caveat anchor; badge names exactly the "
        f"{n_hosts} host(s) with executed evidence"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
