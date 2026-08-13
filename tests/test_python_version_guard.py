"""The interpreter prerequisite must fail at the prerequisite, naming the remedy.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-13
Dependencies: Python standard library only

`pyproject.toml`, `README.md`, and `AGENTS.md` all state Python 3.11 or later.
Until 2026-08-13 none of them enforced it, and macOS ships **3.9** as
`/usr/bin/python3` — so the most likely newcomer, on the most likely platform,
running the exact command the README gives, got an `ImportError` about
`datetime.UTC` twelve frames deep in a DOCX builder they never asked for.

These tests pin two things: the guard's threshold tracks `pyproject.toml`, and
the message it prints actually tells the reader what to do.
"""

from __future__ import annotations

import importlib.util
import io
import re
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_all", ROOT / "scripts" / "check_all.py"
)
assert _spec and _spec.loader
check_all = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_all)


class VersionGuardTests(unittest.TestCase):
    def test_the_threshold_matches_pyproject(self) -> None:
        """Two declarations of one requirement must not drift apart."""
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        m = re.search(r'requires-python\s*=\s*"[><=]*\s*(\d+)\.(\d+)"', text)
        self.assertIsNotNone(m, "pyproject.toml has no parseable requires-python")
        assert m
        self.assertEqual(
            (int(m.group(1)), int(m.group(2))),
            check_all.MINIMUM_PYTHON,
            "check_all.MINIMUM_PYTHON and pyproject requires-python disagree",
        )

    def test_an_old_interpreter_is_rejected_with_an_actionable_message(self) -> None:
        buf = io.StringIO()
        with (
            mock.patch.object(check_all.sys, "version_info", (3, 9, 6)),
            self.assertRaises(SystemExit) as raised,
            redirect_stderr(buf),
        ):
            check_all.require_python()
        self.assertEqual(1, raised.exception.code)

        message = buf.getvalue()
        # The message has to survive being read by someone who does not already
        # know the answer, so assert on what it must tell them.
        self.assertIn("3.11", message, "does not say which version is needed")
        self.assertIn("3.9.6", message, "does not say which version they have")
        self.assertIn("venv", message, "does not give a remedy")
        self.assertIn("requirements.lock", message, "does not name the install step")

    def test_a_supported_interpreter_passes_silently(self) -> None:
        buf = io.StringIO()
        with (
            mock.patch.object(check_all.sys, "version_info", (3, 11, 0)),
            redirect_stderr(buf),
        ):
            check_all.require_python()
        self.assertEqual("", buf.getvalue(), "the guard is noisy on a valid interpreter")


if __name__ == "__main__":
    unittest.main(verbosity=2)
