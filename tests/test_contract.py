"""Contract tests for the public ClinPharm PMx Skills v0.1 artifacts."""

from __future__ import annotations

import ast
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from strictyaml import dirty_load

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def discovered_skills() -> list[Path]:
    """Every released package. Tests parametrise over discovery, never a name.

    A hard-coded package name means a second skill escapes every contract test
    silently. Discovery makes coverage automatic and the denominator visible.
    """
    base = ROOT / "skills"
    return sorted(p.parent for p in base.glob("*/SKILL.md")) if base.is_dir() else []

sys.path.insert(0, str(SCRIPTS))

import validate_repo
from build_catalog_docs import render as render_catalog
from build_catalog_json import build as build_catalog
from check_generated_freshness import differing_members
from check_routing import split_clauses


class ClinPharmAIContractTests(unittest.TestCase):
    def test_pathlib_text_io_declares_utf8(self) -> None:
        """Keep text decoding deterministic on Windows, macOS, and Linux."""
        missing: list[str] = []
        roots = (ROOT / "scripts", ROOT / "tests", ROOT / "skills")
        for path in sorted(file for root in roots for file in root.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                    continue
                if node.func.attr not in {"read_text", "write_text"}:
                    continue
                positional_encoding = len(node.args) >= (1 if node.func.attr == "read_text" else 2)
                keyword_encoding = any(item.arg == "encoding" for item in node.keywords)
                if not positional_encoding and not keyword_encoding:
                    missing.append(f"{path.relative_to(ROOT)}:{node.lineno} {node.func.attr}")
        self.assertEqual([], missing, "Path text I/O must declare encoding='utf-8'")

    def test_every_skill_frontmatter_is_valid_nested_yaml(self) -> None:
        skills = discovered_skills()
        self.assertGreater(len(skills), 0, "no skills/*/SKILL.md discovered")
        for skill in skills:
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"), "missing frontmatter")
                frontmatter = text.split("---\n", 2)[1]
                parsed = dirty_load(frontmatter).data
                metadata = parsed.get("metadata")
                self.assertIsInstance(metadata, dict)

    def test_frontmatter_shape_gate_rejects_root_level_metadata_canary(self) -> None:
        malformed = """---
name: planted-skill
description: Use this skill for a planted validation canary only.
license: MIT
metadata:
  author: Example
evidence-level: escaped-root
  human-review: required
---
"""
        with mock.patch.object(validate_repo, "ERRORS", []):
            validate_repo.check_frontmatter_shape("planted-skill", malformed)
            self.assertTrue(
                any("unexpected root key 'evidence-level'" in error for error in validate_repo.ERRORS),
                "planted root-level metadata escaped detection",
            )

    def test_skill_gate_rejects_overlong_description_canary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "planted-skill"
            skill.mkdir()
            (skill / "README.md").write_text("# Planted skill\n", encoding="utf-8")
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: planted-skill\n"
                f"description: Use this skill when testing. {'x' * 1024}\n"
                "license: MIT\n"
                "metadata:\n"
                "  author: Example\n"
                "---\n\n"
                "# Planted\n\nRESTRICTED_DO_NOT_PROCESS\n",
                encoding="utf-8",
            )
            with mock.patch.object(validate_repo, "ERRORS", []):
                validate_repo.check_skills([skill])
                self.assertTrue(
                    any("at most 1024" in error for error in validate_repo.ERRORS),
                    "planted overlong description escaped detection",
                )

    def test_catalog_markdown_is_fresh_and_mutation_sensitive(self) -> None:
        catalog = json.loads((ROOT / "catalog/catalog.json").read_text(encoding="utf-8"))
        rendered = render_catalog(catalog)
        self.assertEqual(
            rendered,
            (ROOT / "docs/CATALOG.md").read_text(encoding="utf-8"),
        )
        planted = json.loads(json.dumps(catalog))
        planted["counts"]["released"] += 1
        self.assertNotEqual(render_catalog(planted), rendered)

    def test_catalog_json_is_derived_from_collections(self) -> None:
        actual = json.loads((ROOT / "catalog/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(build_catalog(), actual)
        planted = json.loads(json.dumps(actual))
        # Flip away from the live status so the red path stays meaningful when
        # the whole library is `released`.
        live = planted["artifacts"][0]["status"]
        planted["artifacts"][0]["status"] = "built" if live == "released" else "released"
        self.assertNotEqual(build_catalog(), planted)

    def test_routing_split_accepts_all_supported_exclusion_phrases(self) -> None:
        for phrase in (
            "Do not use when",
            "Do not use for",
            "Do not use to",
            "Do not use it to",
            "Do not use this skill",
        ):
            with self.subTest(phrase=phrase):
                inclusion, exclusion = split_clauses(f"Use when appropriate. {phrase} decide.")
                self.assertEqual(inclusion, "Use when appropriate. ")
                self.assertTrue(exclusion.startswith(phrase))

    def test_all_five_operating_modes_have_evaluation_coverage(self) -> None:
        # Reads the PS-D028 suite rather than the retired evals/evals.json.
        # That file was `build-work-context`'s suite living at the shared root,
        # which is what let every other package borrow it and pass the
        # "has an eval suite" check without owning one.
        from eval_schema import load_case

        cases = sorted((ROOT / "evals/build-work-context/cases").glob("*.yaml"))
        self.assertTrue(cases, "no cases under evals/build-work-context/cases/")
        parsed = [load_case(path.read_text(encoding="utf-8"), str(path)) for path in cases]
        modes = {case.get("mode") for case in parsed}
        for required in ("CREATE", "UPDATE", "PROJECT", "REFRESH", "EXPORT"):
            self.assertIn(required, modes)
        identifiers = [case["id"] for case in parsed]
        self.assertTrue(any("restricted" in name for name in identifiers))
        self.assertTrue(any("prompt-injection" in name for name in identifiers))

    def test_skill_progressive_disclosure_links_resolve(self) -> None:
        skills = discovered_skills()
        self.assertGreater(len(skills), 0, "no skills/*/SKILL.md discovered")
        for skill in skills:
            with self.subTest(skill=skill.name):
                path = skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 500)
                self.assertTrue((skill / "README.md").is_file())
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    if "://" not in target and not target.startswith("#"):
                        self.assertTrue(
                            (path.parent / target.split("#", 1)[0]).exists(), target
                        )

    def test_synthetic_example_preserves_governing_numbers(self) -> None:
        capsule = (ROOT / "examples/clinpharm-pmx/outputs/Project-Context-SYN-101.md").read_text(encoding="utf-8")
        pack = (ROOT / "examples/clinpharm-pmx/outputs/AI-Working-Pack-SYN-101.md").read_text(encoding="utf-8")
        for text in (capsule, pack):
            self.assertIn("14.2 L/h", text)
            self.assertIn("12.4 L/h", text)
            self.assertIn("90%", text)
            self.assertIn("80%", text)
            self.assertIn("unsupported", text.lower())

    def test_secondary_benchmark_review_is_reconciled(self) -> None:
        results = ROOT / "evals/benchmark/results/2026-07-30-codex"
        scores = json.loads((results / "scores.json").read_text(encoding="utf-8"))
        review = scores["review"]["secondary"]
        record = (results / review["record"]).read_text(encoding="utf-8")
        self.assertTrue(review["condition_labels_masked"])
        self.assertFalse(review["independent"])
        self.assertEqual("48/48", review["agreement"]["dimension_scores"])
        self.assertEqual("6/6", review["agreement"]["critical_failure_classifications"])
        self.assertEqual(0, review["agreement"]["total_score_disagreements"])
        for run in scores["runs"]:
            self.assertIn(run["baseline"]["sha256"], record)
            self.assertIn(run["working_pack"]["sha256"], record)

    def test_public_example_is_explicitly_synthetic(self) -> None:
        for path in (ROOT / "examples/clinpharm-pmx").rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("synthetic", text, path)

    def test_generated_docx_files_are_valid_packages(self) -> None:
        for relative in (
            "examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.docx",
            "examples/clinpharm-pmx/outputs/AI-Working-Pack-SYN-101.docx",
        ):
            path = ROOT / relative
            if not path.exists():
                self.skipTest(f"{relative} not built yet")
            with zipfile.ZipFile(path) as archive:
                self.assertIn("word/document.xml", archive.namelist())

    def test_docx_freshness_ignores_zip_compression_envelope(self) -> None:
        source = ROOT / "examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.docx"
        if not source.exists():
            self.skipTest("example DOCX not built yet")
        with tempfile.TemporaryDirectory() as temp:
            rewritten = Path(temp) / source.name
            with zipfile.ZipFile(source) as archive:
                members = [(name, archive.read(name)) for name in archive.namelist()]
            with zipfile.ZipFile(
                rewritten, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1
            ) as archive:
                for name, data in members:
                    archive.writestr(name, data)
            self.assertNotEqual(source.read_bytes(), rewritten.read_bytes())
            self.assertEqual([], differing_members(source, rewritten))

    def test_paste_block_states_zero_install(self) -> None:
        text = (ROOT / "skills/build-work-context/PASTE.md").read_text(encoding="utf-8")
        self.assertIn("Zero-install", text)
        self.assertIn("skills/build-work-context/SKILL.md", text)

    def test_blank_templates_default_to_unknown(self) -> None:
        for path in sorted(
            p for skill in discovered_skills() for p in (skill / "assets").glob("*.template.md")
        ):
            text = path.read_text(encoding="utf-8")
            if "data_classification:" in text:
                self.assertIn("data_classification: UNKNOWN", text, path)

    def test_public_governance_and_site_exist(self) -> None:
        for relative in (
            "AGENTS.md",
            "CODE_OF_CONDUCT.md",
            "SUPPORT.md",
            ".github/CODEOWNERS",
            "docs/assets/clinpharm-pmx-skills-workflow.gif",
            "docs/assets/clinpharm-pmx-skills-workflow.mp4",
            "site/index.html",
            "site/sitemap.xml",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_release_video_is_mp4(self) -> None:
        video = ROOT / "docs/assets/clinpharm-pmx-skills-workflow.mp4"
        header = video.read_bytes()[:64]
        self.assertGreater(video.stat().st_size, 100_000)
        self.assertEqual(header[4:8], b"ftyp")
        self.assertTrue(
            any(brand in header for brand in (b"isom", b"iso2", b"mp41", b"mp42")),
            "expected a recognized ISO Base Media brand",
        )

    def test_prompt_injection_fixture_is_treated_as_untrusted(self) -> None:
        # Moved to the owning suite by the PS-D028 migration: fixtures now live
        # beside the cases that use them, so a suite is self-contained.
        fixture = (
            ROOT / "evals/build-work-context/fixtures/prompt-injection-source.md"
        ).read_text(encoding="utf-8")
        self.assertIn("hostile test content", fixture)
        for skill in discovered_skills():
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                # A required SECTION, not one skill's prose. Asserting an exact
                # sentence couples a safety contract to a wording choice and
                # breaks the moment a second skill states the same rule
                # differently — which is exactly what happened.
                self.assertRegex(
                    text, r"(?im)^#+ .*evidence, not instructions",
                    f"{skill.name}: SKILL.md must carry an 'evidence, not "
                    f"instructions' section",
                )


if __name__ == "__main__":
    unittest.main()
