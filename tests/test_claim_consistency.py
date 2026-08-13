"""The claim-consistency gate must go red for the *planted* reason, not any reason.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

`scripts/check_claim_consistency.py` ships a `--canary` mode. A canary that
nobody runs is a mode, not a guarantee, so it runs here on every `make test`.

The distinction these tests defend is narrow and was learned the hard way. The
first version of the canary asked only *"is there any problem?"* and printed
three confident RED-as-expected lines while all three were firing on the same
unrelated false positive — no planted defect was detected at all. So each test
below asserts on the **content** of the problem, never merely on its existence.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_claim_consistency", ROOT / "scripts" / "check_claim_consistency.py"
)
assert _spec and _spec.loader
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)


def problems_for(**overrides: str) -> list[str]:
    """Run the gate over the real tree with named surfaces replaced."""
    texts = cc.load()
    texts.update(overrides)
    return cc.run(texts)


class RealTreeTests(unittest.TestCase):
    def test_the_published_tree_is_green(self) -> None:
        self.assertEqual([], cc.run(cc.load()))

    def test_every_status_surface_is_actually_examined(self) -> None:
        """The PASS line's denominator must equal STATUS_SURFACES, not less.

        This is the regression guard for a real defect: the definition detector
        matched only a dash or a table pipe, so it silently skipped `AGENTS.md`
        — which writes "What `released` means here" — and the gate reported a
        confident PASS over 2 surfaces while believing it covered 3.
        """
        texts = cc.load()
        examined = [
            name
            for name in cc.STATUS_SURFACES
            if cc.DEFINES_RELEASED.search(texts.get(name, ""))
        ]
        self.assertEqual(
            sorted(cc.STATUS_SURFACES),
            sorted(examined),
            "a surface listed in STATUS_SURFACES is not detected as defining "
            "`released`, so the gate would not notice it regressing",
        )


class PlantedDefectTests(unittest.TestCase):
    def test_a_bare_overclaim_is_caught(self) -> None:
        texts = cc.load()
        found = problems_for(
            **{"README.md": texts["README.md"] + "\n\nEvery package passes every gate.\n"}
        )
        self.assertTrue(
            any("banned claim" in p for p in found),
            f"planted overclaim was not caught; got {found}",
        )

    def test_a_quoted_prohibition_is_not_a_finding(self) -> None:
        """Banning a phrase requires writing it. That must not trip the gate."""
        texts = cc.load()
        found = problems_for(
            **{
                "README.md": texts["README.md"]
                + '\n\nDo not write "passes every gate": name the gate.\n'
            }
        )
        self.assertEqual(
            [], found, f"a quoted prohibition was misread as a claim: {found}"
        )

    def test_a_wrapped_overclaim_is_still_caught(self) -> None:
        """The real 2026-08-13 hit matched across a line break.

        A line-based classifier splits `passes every\\ngate` in half and misses
        it on both halves, which is why this gate windows over characters.
        """
        texts = cc.load()
        found = problems_for(
            **{
                "README.md": texts["README.md"]
                + "\n\nEvery shipped package in this repository passes every\ngate.\n"
            }
        )
        self.assertTrue(
            any("banned claim" in p for p in found),
            f"a line-wrapped overclaim escaped the gate; got {found}",
        )

    def test_a_caveat_far_from_the_definition_does_not_count(self) -> None:
        """Proximity regression.

        A concurrent edit once left `README.md` defining `released` in a table
        at line 84 while the only caveat phrase on the page sat at line 144, in
        a different section, about denominators. Two earlier versions of the
        check passed that. A reader of the definition never reaches the distant
        sentence before forming a belief, so it is not a disclaimer.
        """
        far = (
            "| `released` | **151** | Passed its gate. |\n"
            + ("\nfiller line that says nothing about status\n" * 200)
            + "\nThis does not mean clinical validation of the evaluation suite.\n"
        )
        found = problems_for(**{"README.md": far})
        self.assertTrue(
            any("README.md" in p and "released" in p for p in found),
            f"a caveat {len(far)} characters from the definition was accepted; "
            f"got {found}",
        )

    def test_dropping_the_caveat_anchor_is_caught_on_every_status_surface(self) -> None:
        texts = cc.load()
        for surface in cc.STATUS_SURFACES:
            with self.subTest(surface=surface):
                stripped = texts[surface].replace("evaluation", "assessment").replace(
                    "Evaluation", "Assessment"
                )
                found = problems_for(**{surface: stripped})
                self.assertTrue(
                    any(surface in p and "caveat" in p for p in found),
                    f"{surface} lost its caveat anchor without the gate noticing; "
                    f"got {found}",
                )


class BadgeAttestationTests(unittest.TestCase):
    def test_badge_may_not_name_a_host_without_executed_evidence(self) -> None:
        texts = cc.load()
        found = problems_for(
            **{
                "README.md": texts["README.md"].replace(
                    "Claude%20Code%20%7C%20Cursor",
                    "Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20CLI",
                )
            }
        )
        self.assertTrue(
            any("badge names" in p and "Codex CLI" in p for p in found),
            f"the badge named an unevidenced host and the gate allowed it; got {found}",
        )

    def test_badge_may_not_omit_a_host_that_has_evidence(self) -> None:
        texts = cc.load()
        found = problems_for(
            **{
                "README.md": texts["README.md"].replace(
                    "Claude%20Code%20%7C%20Cursor", "Claude%20Code"
                )
            }
        )
        self.assertTrue(
            any("badge omits it" in p for p in found),
            f"a verified host vanished from the badge unnoticed; got {found}",
        )

    def test_the_attestation_is_an_allowlist_and_records_only_clean_exits(self) -> None:
        import json

        data = json.loads(
            (ROOT / "catalog" / "adapter-evidence.json").read_text(encoding="utf-8")
        )
        evidenced = {h["display_name"] for h in data["hosts"]}
        untested = {h["display_name"] for h in data["not_evidenced"]}
        self.assertEqual(
            set(), evidenced & untested, "a host is both evidenced and untested"
        )
        self.assertTrue(evidenced, "hosts[] is empty, so the badge has no legal source")
        for host in data["hosts"]:
            for step in host["lifecycle_steps_executed"]:
                self.assertEqual(
                    0,
                    step["exit"],
                    f"{host['display_name']} is in hosts[] but step "
                    f"{step['step']!r} records exit {step['exit']}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
