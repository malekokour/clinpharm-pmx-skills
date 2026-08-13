"""Tests for scripts/library_router.py advisory selector."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from library_router import classify, load_settings, select


class LibraryRouterTests(unittest.TestCase):
    def test_refuse_human_only(self) -> None:
        out = select("please select a dose for the patient")
        self.assertEqual(out["decision"], "refuse")
        self.assertIn("human_only", out["reasons"])

    def test_multi_asks(self) -> None:
        out = select("run full poppk development end to end")
        self.assertEqual(out["complexity"], "MULTI")
        self.assertEqual(out["decision"], "ask")

    def test_force_skill(self) -> None:
        settings = load_settings()
        settings["force_skill"] = "review-csr-pk-consistency"
        out = select("anything", settings=settings)
        self.assertEqual(out["decision"], "force")
        self.assertEqual(out["chosen"], "review-csr-pk-consistency")

    def test_unknown_settings_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "settings.json"
            path.write_text(
                json.dumps({"selection_mode": "ask", "evil": True}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_settings(path)

    def test_csr_utterance_recommends_csr_skill(self) -> None:
        settings = load_settings()
        settings["eligible_statuses"] = ["released", "built"]
        out = select(
            "review csr pk consistency across tables",
            settings=settings,
        )
        self.assertIn(out["decision"], {"ask", "top1"})
        self.assertEqual(out["chosen"], "review-csr-pk-consistency")

    def test_classify_oos(self) -> None:
        self.assertEqual(classify("design a wet-lab assay"), "OOS")

    def test_force_skill_cannot_bypass_human_only_refuse(self) -> None:
        """An operator preference must not open a refuse path.

        skills/library-router/SKILL.md has always said preferences cannot
        bypass human-only, OOS or safety refuses. Until 2026-08-11 the code
        read force_skill before classifying, so a pinned skill routed a
        dose-selection request instead of refusing it.
        """
        settings = load_settings()
        settings["force_skill"] = "review-ddi-evidence"
        out = select("select a dose for this cohort", settings=settings)
        self.assertEqual(out["decision"], "refuse")
        self.assertEqual(out["chosen"], None)
        self.assertIn("preference_cannot_bypass_refuse", out["reasons"])

    def test_force_skill_cannot_bypass_oos_refuse(self) -> None:
        settings = load_settings()
        settings["force_skill"] = "review-ddi-evidence"
        out = select("design a wet-lab assay for this compound", settings=settings)
        self.assertEqual(out["decision"], "refuse")
        self.assertIn("preference_cannot_bypass_refuse", out["reasons"])

    def test_force_skill_still_applies_to_ordinary_requests(self) -> None:
        """The refuse ordering above must not have disabled force_skill."""
        settings = load_settings()
        settings["force_skill"] = "review-ddi-evidence"
        out = select("review the bioanalytical validation report", settings=settings)
        self.assertEqual(out["decision"], "force")
        self.assertEqual(out["chosen"], "review-ddi-evidence")

    def test_two_named_targets_ask_rather_than_dropping_one(self) -> None:
        """A request naming two packages must not resolve to one of them."""
        settings = load_settings()
        settings["selection_mode"] = "auto"
        settings["allow_agent_auto_select"] = True
        settings["eligible_statuses"] = ["released", "built"]
        out = select(
            "review the csr and the protocol pk sections together",
            settings=settings,
        )
        self.assertEqual(out["decision"], "ask")
        self.assertEqual(out["chosen"], None)
        self.assertIn("two_strong_candidates", out["reasons"])
        self.assertIn("review-csr-pk-consistency", out["candidates"])
        self.assertIn("review-protocol-pk-sections", out["candidates"])

    def test_single_target_is_not_caught_by_the_two_target_guard(self) -> None:
        settings = load_settings()
        settings["selection_mode"] = "auto"
        settings["allow_agent_auto_select"] = True
        settings["eligible_statuses"] = ["released", "built"]
        out = select("review csr pk consistency across tables", settings=settings)
        self.assertEqual(out["decision"], "top1")
        self.assertEqual(out["chosen"], "review-csr-pk-consistency")

    def test_prose_section_number_survives_tokenizing(self) -> None:
        """`2.7.2` must reach scoring; it used to be dropped as three fragments."""
        settings = load_settings()
        settings["selection_mode"] = "auto"
        settings["allow_agent_auto_select"] = True
        settings["eligible_statuses"] = ["released", "built"]
        out = select("review ctd 2.7.2 content", settings=settings)
        self.assertEqual(out["chosen"], "review-ctd-272-content")

    def test_router_persists_no_trace(self) -> None:
        """D-L17: the router must not write a selection trace anywhere.

        The router design method suggests persisting utterance class, chosen
        nav_path, candidate ids and scores "for evals". This implementation
        deliberately does not: an utterance can carry sponsor-confidential or
        patient-level text, and a trace file inside a package directory would
        be the easiest possible way to move it somewhere it does not belong.
        The selection record is returned to the caller and nothing else.

        Asserted by snapshotting the repository tree rather than by reading
        the source, so a future `open(..., "w")` fails here even if nobody
        remembers this rule.
        """
        before = {p for p in ROOT.rglob("*") if p.is_file()}
        settings = load_settings()
        settings["selection_mode"] = "auto"
        settings["allow_agent_auto_select"] = True
        settings["eligible_statuses"] = ["released", "built"]
        for utterance in (
            "review csr pk consistency across tables",
            "select a dose for this cohort",
            "run full poppk development end to end",
        ):
            select(utterance, settings=settings)
        after = {p for p in ROOT.rglob("*") if p.is_file()}
        self.assertEqual(
            sorted(str(p.relative_to(ROOT)) for p in after - before),
            [],
            "routing wrote a file; see D-L17 — no selection traces are persisted",
        )

    def test_disabled_skill_never_appears_as_a_candidate(self) -> None:
        settings = load_settings()
        settings["selection_mode"] = "auto"
        settings["allow_agent_auto_select"] = True
        settings["eligible_statuses"] = ["released", "built"]
        settings["disabled_skills"] = ["review-csr-pk-consistency"]
        out = select("review csr pk consistency across tables", settings=settings)
        self.assertNotIn("review-csr-pk-consistency", out["candidates"])
        self.assertNotEqual(out["chosen"], "review-csr-pk-consistency")


if __name__ == "__main__":
    unittest.main()
