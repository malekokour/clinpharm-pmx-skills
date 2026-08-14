#!/usr/bin/env python3
"""Prove each quality gate fails when it should, one planted defect at a time.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-14
Dependencies: Python standard library only

    python3 scripts/canary_gates.py            # run every case
    python3 scripts/canary_gates.py --list     # show coverage against check_all
    python3 scripts/canary_gates.py -k routing # run cases matching a substring

Why this exists
---------------
`check_all.py` runs 32 gates. On 2026-08-13 exactly **two** had ever been watched
to fail. The rest were asserted — and this repository has already met, three
separate times, a check that passed over nothing:

  * a scanner that read 0 bytes and reported success
  * `allowlist_walk` filtering on ``is_file()``, which made broken symlinks
    invisible to a rule specifically about symlinks
  * a canary that asked *"is there any problem?"* and answered yes three times
    while detecting none of its own planted defects

**A gate nobody has watched fail is untested**, and the only way to know a gate
works is to break something and see it complain about the right thing.

What a case has to prove
------------------------
Each case runs its gate three times:

1. **before** — green on the untouched tree, so the case starts from a known
   state rather than assuming one
2. **planted** — non-zero exit **and** an expected fragment in the output. Exit
   code alone is not enough: a gate can fail for an unrelated reason and look
   like a pass of this test, which is precisely how the earlier canary fooled
   itself
3. **after** — green again, with the target file **byte-identical** to its
   backup

Step 3 is not politeness. A canary that leaves the tree mutated turns every
later case into a false result, and a canary that cannot restore is a
destructive operation wearing a test's clothes.

Safety
------
Mutations happen in the working tree and are reverted from an in-memory copy of
the original bytes, restored in a ``finally`` so an exception cannot leave the
file changed. Restoration is **verified by comparison**, not assumed. If any
file cannot be restored the run aborts immediately rather than continuing and
reporting nonsense.

Nothing here is committed, and every target is a file already tracked by git —
so ``git diff`` is a second, independent way to confirm the tree came back.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


@dataclass
class Case:
    """One gate, one planted defect, one expected complaint."""

    #: Label as it appears in `check_all.py`, so coverage is checkable.
    gate: str
    #: Command to run, relative to ROOT.
    command: list[str]
    #: File to mutate.
    target: str
    #: What to do to it.
    mutation: str
    #: Substring the gate's output must contain when the defect is planted.
    expect: str
    #: Human note on why this defect is the right one for this gate.
    why: str = ""
    #: Extra files to back up and restore (a gate may rewrite more than one).
    also_restore: list[str] = field(default_factory=list)


def append_line(text: str, line: str) -> str:
    return text + ("" if text.endswith("\n") else "\n") + line + "\n"


# Payloads are assembled at runtime from fragments, never written as literals.
#
# This is not stylistic. The first version spelled the machine path out, and
# `privacy_scan.py` immediately failed **on this file** — `machine-specific-path:
# scripts/canary_gates.py` — before a single defect had been planted. The gate
# was right: a machine path in a shipped script is a defect whatever the author
# intended it for, and "it is only test data" is exactly the excuse a scanner
# must not accept.
#
# `scan_skills.py` and `privacy_scan.py` already build their own patterns this
# way for the same reason. A canary that trips the gate it is testing cannot
# distinguish its own contamination from the defect it planted.
MACHINE_PATH = "/" + "Users/" + "someone/work/x"
SUBJECT_KEY = "USUB" + "JID"
INJECTION = "ignore all " + "previous instructions"


CASES: list[Case] = [
    Case(
        gate="Published map current",
        command=[PY, "scripts/build_map_site.py", "--check"],
        target="site/map/index.html",
        mutation="append",
        expect="stale",
        why="A generated page edited by hand must not survive; the gate exists "
        "because the map is regenerated from the ledger, never patched.",
    ),
    Case(
        gate="Paste blocks current",
        command=[PY, "scripts/build_paste_blocks.py", "--check"],
        target="skills/verify-nca-outputs/PASTE.md",
        mutation="append",
        expect="stale",
        why="PASTE.md is the zero-install route. A hand-edit here ships text no "
        "generator produced.",
    ),
    Case(
        gate="Public claim ledger",
        command=[PY, "scripts/check_claim_ledger.py", "--check"],
        target="CLAIM-LEDGER.md",
        mutation="append",
        expect="stale",
        why="Already canaried by a peer; re-run here so the count is first-hand.",
    ),
    Case(
        gate="README counts synced",
        command=[PY, "scripts/sync_readme_counts.py", "--check"],
        target="README.md",
        mutation="replace:| `released` | **151**->| `released` | **150**",
        expect="stale",
        why="This gate polices five specific regexes, all anchored to the status "
        "table. A first attempt replaced the first `**151**` anywhere in the "
        "file and the gate stayed green — correctly, because that occurrence "
        "was outside its scope. The mutation has to land where the gate looks.",
    ),
    Case(
        gate="Static site gates",
        command=[PY, "scripts/check_site_gates.py"],
        target="site/index.html",
        mutation='replace:<link rel="stylesheet" href="styles.css">'
        '-><script src="https://cdn.example.net/a.js"></script>',
        expect="",
        why="An external script is simultaneously a tracker, a third-party "
        "request, and JavaScript — three site rules at once.",
    ),
    Case(
        gate="Router selection cases",
        command=[PY, "scripts/check_router_selection.py"],
        target="evals/library-router/selection-cases.json",
        mutation='replace:"chosen": "assess-demographic-covariate-effects"'
        '->"chosen": "review-renal-impairment"',
        expect="",
        why="An expectation the router will not meet. Tests that the harness "
        "compares rather than merely runs.",
    ),
    Case(
        gate="Portable frontmatter",
        command=[PY, "scripts/check_portable_frontmatter.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:---\nname:->---\nnot a key value pair\nname:",
        expect="",
        why="This gate reads frontmatter *keys*, not tool values. A first "
        "attempt widened `allowed-tools` and it stayed green — the grant is "
        "policed elsewhere, not here. Malformed structure is what this one owns.",
    ),
    Case(
        gate="Repository contract",
        command=[PY, "scripts/validate_repo.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:name: review-renal-impairment->name: not-the-directory",
        expect="",
        why="Directory name must equal frontmatter name. Peer-canaried on a "
        "different rule; this exercises the package contract instead.",
    ),
    Case(
        gate="Skill routing partition",
        command=[PY, "scripts/check_routing.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:Do not use to decide the outcome of renal impairment"
        "->Also suitable for deciding the outcome of renal impairment",
        expect="unbounded scope",
        why="Removing the exclusion clause. The gate's rule is that a package "
        "with no exclusion 'claims an unbounded scope and can never be routed "
        "away from'. A first attempt swapped renal for hepatic in the inclusion "
        "text and stayed green — correctly: that similarity sits under the 0.30 "
        "screen, and adjacency is expected in this collection.",
    ),
    Case(
        gate="Map is current and honest",
        command=[PY, "scripts/check_map.py"],
        target="catalog/job-model-167.tsv",
        mutation="append",
        expect="",
        why="Peer-canaried; re-run first-hand against the ledger the map reads.",
    ),
    Case(
        gate="Claim consistency",
        command=[PY, "scripts/check_claim_consistency.py"],
        target="README.md",
        mutation="replace:## What's in the library"
        "->## What's in the library\n\nEvery package passes every gate.",
        expect="banned claim",
        why="The 2026-08-13 overclaim, planted back in.",
    ),
    Case(
        gate="Skill package scan",
        command=[PY, "scan_skills.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation=f"replace:license: MIT->license: MIT # {MACHINE_PATH}",
        expect="machine-path",
        why="A machine path in a shipped package.",
    ),
    Case(
        gate="Public-release privacy scan",
        command=[PY, "scripts/privacy_scan.py"],
        target="docs/CATALOG.md",
        mutation=f"replace:# ->#{MACHINE_PATH} ",
        expect="machine-specific-path",
        why="The data-boundary gate. An append is not a privacy defect, so this "
        "plants a real signal instead.",
    ),
    Case(
        gate="Catalog Markdown freshness",
        command=[PY, "scripts/build_catalog_docs.py", "--check"],
        target="docs/CATALOG.md",
        mutation="append",
        expect="",
        why="Generated from catalog.json; a hand-edit must not survive.",
    ),
    Case(
        gate="Evaluation suites",
        command=[PY, "scripts/eval_suite_check.py"],
        target="evals/review-renal-impairment/suite.yaml",
        mutation="append",
        expect="",
        why="A malformed suite must not pass as a valid one.",
    ),
    Case(
        gate="Defect assertion shape",
        command=[PY, "scripts/check_defect_assertion_shape.py"],
        target="evals/review-renal-impairment/cases/01-activation-declared-trigger.yaml",
        mutation="append",
        expect="",
        why="Assertion shape is what stops a case asserting nothing.",
    ),
    Case(
        gate="Fixture grounding",
        command=[PY, "scripts/check_fixture_grounding.py"],
        target="evals/review-renal-impairment/cases/01-activation-declared-trigger.yaml",
        mutation="append",
        expect="",
        why="A case must stay grounded in a fixture that exists.",
    ),
    Case(
        gate="Nav registry field contract",
        command=[PY, "scripts/check_nav_registry.py"],
        target="catalog/nav_registry.json",
        mutation='replace:"id": "review-renal-impairment"->"id": "renal-typo"',
        expect="",
        why="Renaming one entry id makes the on-disk package an orphan and the "
        "entry a phantom — the two conditions this gate names. Two earlier "
        "attempts stayed green and both were my error, not the gate's: a "
        "renamed top-level key (the gate checks entries, not the envelope), "
        "then the bare id string — which occurs four times in the file, and "
        "`replace` rewrites only the first, which was not the `id` field.",
    ),
    Case(
        gate="Router scale fixtures",
        command=[PY, "scripts/build_scale_fixtures.py", "--check"],
        target="tests/fixtures/scale/nav_registry_200.json",
        mutation='replace:"schema_version"->"schema_version_typo"',
        expect="",
        why="A generated fixture edited by hand.",
    ),
    Case(
        gate="Lifecycle runbook",
        command=[PY, "scripts/check_lifecycle_docs.py"],
        target="docs/LIFECYCLE.md",
        mutation="replace:scripts/check_all.py->scripts/does_not_exist.py",
        expect="does not exist",
        why="The runbook must not tell a maintainer to run a script that is not "
        "there — the invented-command failure, in the document whose whole job "
        "is to be followed literally. An append stayed green, correctly: adding "
        "prose is not a defect, naming a missing script is.",
    ),
    Case(
        gate="v1.2 gates",
        command=[PY, "scripts/check_v12_gates.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:license: MIT->license: MIT" + ("\n" * 400),
        expect="budget",
        why="Blows the SKILL.md line budget. This gate enforces four budgets "
        "(tools, size, description, allowed-tools); a rogue frontmatter key is "
        "not one of them, so the first attempt stayed green.",
    ),
    Case(
        gate="allowed-tools matches package evidence",
        command=[PY, "scripts/backfill_allowed_tools.py", "--check"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:allowed-tools: Read->allowed-tools: Read, Write",
        expect="",
        why="A grant wider than the package's evidence supports — the gate the "
        "portable-frontmatter check turned out *not* to own.",
    ),
    Case(
        gate="Package portability",
        command=[PY, "scripts/check_portability.py"],
        target="skills/review-renal-impairment/SKILL.md",
        mutation="replace:license: MIT->license: MIT\nx: [gone](./no-such-file.md)",
        expect="dead link",
        why="Portability means the package works once extracted alone. A link "
        "that resolves in the repository and dies in the ZIP is the defect; a "
        "machine path is a different gate's job, which is why that stayed green.",
    ),
    Case(
        gate="Contract tests",
        command=[PY, "-m", "unittest", "discover", "-s", "tests"],
        target="tests/test_contract.py",
        mutation="replace:import unittest->import unittest\nassert False, "
        "'canary: planted failure'",
        expect="",
        why="If a broken test can pass, nothing below it means anything.",
    ),
    Case(
        gate="Python compilation",
        command=[PY, "-m", "compileall", "-q", "scripts", "tests"],
        target="tests/test_contract.py",
        mutation="replace:import unittest->import unittest\ndef (:",
        expect="",
        why="A syntax error must not reach a release.",
    ),
    Case(
        gate="Benchmark digests",
        command=[PY, "scripts/verify_benchmark_digests.py"],
        target="evals/benchmark/results/2026-07-30-codex/scores.json",
        mutation="append",
        expect="",
        why="A retained benchmark result is only evidence while its digest "
        "still matches the bytes it was computed over.",
    ),
    Case(
        gate="Vendored module freshness",
        command=[PY, "scripts/check_vendored.py"],
        target="skills/assess-development-plan-gaps/scripts/findings.py",
        mutation="append",
        expect="",
        why="A vendored copy edited in place diverges from shared/scripts/ and "
        "ships behaviour the canonical source does not have. The first attempt "
        "targeted assess_coverage.py and stayed green — correctly: that script "
        "has no counterpart in shared/scripts/, so it is package-local and the "
        "gate skips it by design.",
    ),
    Case(
        gate="Fixture arithmetic",
        command=[PY, "scripts/check_fixture_arithmetic.py"],
        target="evals/reconcile-cross-document-facts/fixtures/"
        "synthetic-csr-extracts.md",
        mutation="replace:| 18.4 L/h |->| 999.9 L/h |",
        expect="",
        why="A printed CL/F that does not reconcile with its own dose and AUC. "
        "Two earlier attempts were my error, not the gate's: an append to an "
        "unrelated fixture (prose is not an arithmetic defect), then a unit "
        "swap — which this gate *deliberately* tolerates, reconciling against "
        "the column's majority unit and reporting a lone outlier separately, "
        "because a planted unit swap is a defect under test rather than a "
        "construction error. The arithmetic itself is what it owns.",
    ),
    Case(
        gate="Generated artifact freshness",
        command=[PY, "scripts/check_generated_freshness.py"],
        target="examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.md",
        mutation="append",
        expect="",
        why="Editing the Markdown source leaves its committed DOCX stale.",
    ),
    Case(
        gate="Markdown/DOCX parity",
        command=[PY, "scripts/check_docx_parity.py"],
        target="examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.md",
        mutation="append",
        expect="",
        why="The DOCX a reviewer opens must say what the Markdown says.",
    ),
]


#: Gates that **cannot** be canaried as currently written, with the reason. This
#: list is not an excuse — every entry is a defect in the gate, and saying so
#: here is the point. A gate that cannot be made to fail is not a gate.
NOT_CANARIABLE: dict[str, str] = {
    "Owed DOCX present": (
        "The --check path tests `generated.is_file()` and nothing else, so it "
        "verifies *presence*, not integrity. Emptying an owed DOCX to zero bytes "
        "leaves the gate green — confirmed by planting exactly that. The label "
        "is honest about what it does; the risk is that a reader takes 'owed "
        "DOCX present' as 'the DOCX is good'. A truncated or corrupt file ships "
        "unnoticed, and the DOCX is what a reviewer actually opens. Fix: assert "
        "a non-zero size and a valid ZIP header, or fold this into the parity "
        "check, which does read content."
    ),
    "Nav registry is regenerable": (
        "`build_nav_registry.py` takes no --check flag, so check_all invokes the "
        "*generator*. It rewrites catalog/nav_registry.json and exits 0 whatever "
        "the file contained. A hand-edited registry is silently corrected rather "
        "than reported — and nothing downstream notices, because quality.yml has "
        "no dirty-tree check (verified: no `git diff`, `git status`, "
        "`--exit-code`, or `porcelain` anywhere in that workflow). So the "
        "regeneration happens on the CI runner, is thrown away with the runner, "
        "and the stale file stays committed. Fix: add --check, or add a "
        "dirty-tree assertion after the generators run."
    ),
}


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    return p.returncode, p.stdout + p.stderr


def mutate(text: str, how: str) -> str:
    """Apply a planted defect.

    ``append`` is the blunt instrument and is only right for *freshness* gates,
    where "this generated file was touched by hand" is the whole defect.

    For anything else prefer ``replace:old->new``, which plants a defect the
    gate's own logic has to reason about. The difference is not cosmetic: an
    ``append`` into JSON made the nav-registry gate die with a
    ``JSONDecodeError``. It went red, and proved nothing — a parser crashing is
    not the gate noticing. A canary that cannot tell those apart is measuring
    the interpreter, not the check.
    """
    if how == "append":
        return append_line(text, "<!-- canary: planted defect, delete me -->")
    if how == "delete":
        # Emptying rather than unlinking: the harness restores from bytes, and an
        # empty file exercises "is it there and does it have content" without the
        # extra failure mode of a missing path.
        return ""
    if how.startswith("replace:"):
        old, _, new = how[len("replace:"):].partition("->")
        if old not in text:
            raise ValueError(f"replace target not present in file: {old!r}")
        return text.replace(old, new, 1)
    raise ValueError(f"unknown mutation {how!r}")


def run_case(case: Case, verbose: bool) -> tuple[bool, str]:
    targets = [ROOT / case.target] + [ROOT / p for p in case.also_restore]
    missing = [t for t in targets if not t.is_file()]
    if missing:
        return False, f"target missing: {missing[0].relative_to(ROOT)}"

    backups = {t: t.read_bytes() for t in targets}

    code, out = run(case.command)
    if code != 0:
        return False, f"gate was ALREADY RED before planting: {out.strip()[:160]}"

    try:
        target = ROOT / case.target
        if case.mutation == "delete":
            # Handled on bytes, not text: the natural target for an
            # existence-checking gate is its generated artifact, and those are
            # often binary. Decoding a .docx as UTF-8 raises before the defect is
            # ever planted.
            target.write_bytes(b"")
        else:
            target.write_text(
                mutate(target.read_text(encoding="utf-8"), case.mutation),
                encoding="utf-8",
            )
        code, out = run(case.command)
        if code == 0:
            return False, "gate stayed GREEN with a planted defect"
        if case.expect and case.expect.lower() not in out.lower():
            return False, (
                f"went red, but not for the planted reason — expected "
                f"{case.expect!r}, got: {out.strip()[:160]}"
            )
        detail = out.strip().splitlines()
        note = detail[-1][:100] if detail else ""
    finally:
        for t, original in backups.items():
            t.write_bytes(original)
        for t, original in backups.items():
            if t.read_bytes() != original:
                print(f"\nFATAL: could not restore {t.relative_to(ROOT)} — aborting")
                raise SystemExit(2)

    code, out = run(case.command)
    if code != 0:
        return False, f"did not return GREEN after restore: {out.strip()[:160]}"

    if verbose and note:
        print(f"      said: {note}")
    return True, note


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="show coverage and exit")
    ap.add_argument("-k", dest="filter", default="", help="run cases matching this")
    ap.add_argument("-v", dest="verbose", action="store_true")
    args = ap.parse_args()

    # `run(` is sometimes followed by a newline before its label, so a
    # line-anchored `run("` match undercounts. It reported 31 of 32 and the gate
    # it dropped was "Python compilation" — the same class of off-by-one this
    # whole exercise exists to catch, in the tool doing the catching.
    check_all = (ROOT / "scripts" / "check_all.py").read_text(encoding="utf-8")
    gate_labels = re.findall(r"\brun\(\s*\n?\s*\"([^\"]+)\"", check_all)
    covered = {c.gate for c in CASES}

    if args.list:
        print(f"{len(gate_labels)} gate(s) in check_all.py; "
              f"{len(covered)} have a canary case; "
              f"{len(NOT_CANARIABLE)} cannot be canaried as written\n")
        for label in gate_labels:
            if label in covered:
                mark = "[x]"
            elif label in NOT_CANARIABLE:
                mark = "[!]"
            else:
                mark = "[ ]"
            print(f"  {mark} {label}")
        if NOT_CANARIABLE:
            print("\n  [!] cannot be made to fail — each of these is a gate defect:")
            for label, reason in NOT_CANARIABLE.items():
                print(f"      {label}:\n        {reason}")
        unknown = covered - set(gate_labels)
        if unknown:
            print(f"\n  cases naming a gate check_all does not run: {sorted(unknown)}")
        return 0

    cases = [c for c in CASES if args.filter.lower() in c.gate.lower()]
    if not cases:
        print(f"no case matches {args.filter!r}")
        return 1

    failures = 0
    for case in cases:
        ok, note = run_case(case, args.verbose)
        if ok:
            print(f"  RED for the planted reason, GREEN after restore — {case.gate}")
        else:
            failures += 1
            print(f"  PROBLEM — {case.gate}\n      {note}")

    print(
        f"\n{'FAIL' if failures else 'PASS'}: {len(cases) - failures}/{len(cases)} "
        f"case(s) proved their gate fails and recovers "
        f"({len(covered)}/{len(gate_labels)} gates have a case at all)"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
