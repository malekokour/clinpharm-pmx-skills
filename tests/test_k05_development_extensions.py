"""Tests for K05 development-plan extensions and public retrieval.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "assess-development-plan-gaps" / "fixtures"
TOOL_PATH = Path(
    os.environ.get(
        "CLINPHARM_K05_TOOL_PATH",
        ROOT / "shared" / "scripts" / "public_development_intelligence.py",
    )
)
SPEC = importlib.util.spec_from_file_location("k05_public_development_intelligence", TOOL_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import contract guard
    raise RuntimeError(f"cannot import {TOOL_PATH}")
pdi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pdi)


class SequenceFetcher:
    def __init__(self, pages: list[bytes | Exception]):
        self.pages = pages
        self.urls: list[str] = []

    def __call__(self, url: str, _timeout: float) -> bytes:
        self.urls.append(url)
        if not self.pages:
            raise OSError("unexpected extra request")
        value = self.pages.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


class IncrementingClock:
    def __init__(self):
        self.value = datetime(2026, 8, 11, 7, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        value = self.value
        self.value += timedelta(seconds=1)
        return value


def fixture(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


class RegulatoryPrecedentRetrieval(unittest.TestCase):
    def test_filters_pages_timestamps_ids_and_exclusion_are_preserved(self) -> None:
        filters = json.loads((FIXTURES / "synthetic-regulatory-filters.json").read_text(encoding="utf-8"))
        fetcher = SequenceFetcher(
            [fixture("synthetic-regulatory-page-1.json"), fixture("synthetic-regulatory-page-2.json")]
        )
        result = pdi.retrieve(
            pdi.REGULATORY_PRECEDENT,
            filters,
            page_size=2,
            max_pages=2,
            exclude_ids=["BLA000002"],
            fetcher=fetcher,
            clock=IncrementingClock(),
        )

        self.assertEqual(result["status"], "COMPLETE")
        self.assertTrue(result["complete"])
        self.assertEqual(result["caller_filters"], filters)
        self.assertEqual([row["public_record_id"] for row in result["records"]], ["NDA000001", "NDA000003"])
        self.assertEqual(result["exclusions"][0]["public_record_id"], "BLA000002")
        self.assertEqual(result["exclusions"][0]["reason"], "caller-specified-exclusion")
        self.assertEqual(result["counts"], {
            "requests_attempted": 2,
            "pages_retrieved": 2,
            "records_retained": 2,
            "records_excluded": 1,
            "caller_exclusions_declared": 1,
        })
        self.assertIn("skip=2", fetcher.urls[1])
        self.assertTrue(all(row["retrieved_at"].endswith("Z") for row in result["requests"]))
        self.assertTrue(all(row["request_url"].startswith(pdi.ENDPOINTS[pdi.REGULATORY_PRECEDENT]) for row in result["records"]))

    def test_duplicate_and_missing_public_ids_are_explicit_exclusions(self) -> None:
        payload = {
            "meta": {"results": {"total": 3}},
            "results": [
                {"application_number": "NDA000010"},
                {"application_number": "NDA000010", "note": "duplicate"},
                {"sponsor_name": "Synthetic sponsor"},
            ],
        }
        result = pdi.retrieve(
            pdi.REGULATORY_PRECEDENT,
            {},
            page_size=3,
            fetcher=SequenceFetcher([json.dumps(payload).encode()]),
            clock=IncrementingClock(),
        )
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(len(result["records"]), 1)
        self.assertEqual(
            [row["reason"] for row in result["exclusions"]],
            ["duplicate-public-record-id", "missing-public-record-id"],
        )
        self.assertEqual(result["exclusions"][1]["public_record_id"], "UNKNOWN")


class TrialLandscapeRetrieval(unittest.TestCase):
    def test_filters_token_pages_timestamps_and_nct_ids_are_preserved(self) -> None:
        filters = json.loads((FIXTURES / "synthetic-trial-filters.json").read_text(encoding="utf-8"))
        fetcher = SequenceFetcher(
            [fixture("synthetic-trial-page-1.json"), fixture("synthetic-trial-page-2.json")]
        )
        result = pdi.retrieve(
            pdi.TRIAL_LANDSCAPE,
            filters,
            page_size=2,
            max_pages=2,
            fetcher=fetcher,
            clock=IncrementingClock(),
        )

        self.assertEqual(result["caller_filters"], filters)
        self.assertEqual(
            [row["public_record_id"] for row in result["records"]],
            ["NCT00000001", "NCT00000002", "NCT00000003"],
        )
        self.assertEqual(result["requests"][0]["next_cursor"], "synthetic-page-token-2")
        self.assertIn("pageToken=synthetic-page-token-2", fetcher.urls[1])
        self.assertIn("filter.overallStatus=RECRUITING", fetcher.urls[0])
        self.assertIn("filter.overallStatus=COMPLETED", fetcher.urls[0])
        self.assertEqual(result["source"], "ClinicalTrials.gov API v2")
        self.assertTrue(result["complete"])


class FailureAndBoundaryBehavior(unittest.TestCase):
    def test_initial_network_failure_is_cannot_assess_and_non_vacuous(self) -> None:
        result = pdi.retrieve(
            pdi.TRIAL_LANDSCAPE,
            {"query.cond": "Synthetic condition Q"},
            fetcher=SequenceFetcher([OSError("synthetic network failure")]),
            clock=IncrementingClock(),
        )
        self.assertEqual(result["status"], "CANNOT_ASSESS")
        self.assertFalse(result["complete"])
        self.assertEqual(result["error"]["completed_pages"], 0)
        self.assertEqual(result["counts"]["requests_attempted"], 1)
        self.assertEqual(result["counts"]["pages_retrieved"], 0)
        self.assertIn("synthetic network failure", result["error"]["message"])

    def test_later_network_failure_preserves_completed_page(self) -> None:
        fetcher = SequenceFetcher(
            [fixture("synthetic-trial-page-1.json"), OSError("second page unavailable")]
        )
        result = pdi.retrieve(
            pdi.TRIAL_LANDSCAPE,
            {},
            page_size=2,
            max_pages=2,
            fetcher=fetcher,
            clock=IncrementingClock(),
        )
        self.assertEqual(result["status"], "CANNOT_ASSESS")
        self.assertEqual(result["error"]["completed_pages"], 1)
        self.assertEqual(result["counts"]["pages_retrieved"], 1)
        self.assertEqual(len(result["records"]), 2)

    def test_page_bound_before_exhaustion_is_not_called_complete(self) -> None:
        result = pdi.retrieve(
            pdi.TRIAL_LANDSCAPE,
            {},
            page_size=2,
            max_pages=1,
            fetcher=SequenceFetcher([fixture("synthetic-trial-page-1.json")]),
            clock=IncrementingClock(),
        )
        self.assertFalse(result["complete"])
        self.assertEqual(result["status"], "CANNOT_ASSESS")
        self.assertEqual(result["error"]["message"], "bounded_before_exhaustion")
        self.assertEqual(result["pagination"]["next_cursor"], "synthetic-page-token-2")

    def test_credential_like_filter_is_rejected_before_fetch(self) -> None:
        fetcher = SequenceFetcher([])
        with self.assertRaises(pdi.RetrievalInputError):
            pdi.retrieve(pdi.REGULATORY_PRECEDENT, {"api_key": "not-a-real-key"}, fetcher=fetcher)
        self.assertEqual(fetcher.urls, [])

    def test_invalid_openfda_cursor_is_rejected_before_fetch(self) -> None:
        fetcher = SequenceFetcher([])
        with self.assertRaises(pdi.RetrievalInputError):
            pdi.retrieve(
                pdi.REGULATORY_PRECEDENT,
                {},
                start_cursor="not-an-offset",
                fetcher=fetcher,
            )
        self.assertEqual(fetcher.urls, [])

    def test_pagination_control_is_not_accepted_as_a_caller_filter(self) -> None:
        fetcher = SequenceFetcher([])
        with self.assertRaises(pdi.RetrievalInputError):
            pdi.retrieve(pdi.TRIAL_LANDSCAPE, {"pageToken": "opaque"}, fetcher=fetcher)
        self.assertEqual(fetcher.urls, [])

    def test_output_contract_contains_no_decision_field(self) -> None:
        result = pdi.retrieve(
            pdi.TRIAL_LANDSCAPE,
            {},
            fetcher=SequenceFetcher([json.dumps({"studies": []}).encode()]),
            clock=IncrementingClock(),
        )
        self.assertEqual(result["status"], "COMPLETE")
        forbidden = {"similarity", "agency_acceptance", "competitive_importance", "valuation", "go_no_go"}
        self.assertTrue(forbidden.isdisjoint(result))
        self.assertIn("Human review decides", result["boundary"])


class OfflineCli(unittest.TestCase):
    def test_fixture_cli_runs_both_pages_without_network(self) -> None:
        with tempfile.TemporaryDirectory(prefix="k05-public-cli-") as temp:
            output = Path(temp) / "result.json"
            exit_code = pdi.main([
                "--mode", pdi.REGULATORY_PRECEDENT,
                "--filters-json", str(FIXTURES / "synthetic-regulatory-filters.json"),
                "--page-size", "2",
                "--max-pages", "2",
                "--exclude-id", "BLA000002",
                "--fixture-page", str(FIXTURES / "synthetic-regulatory-page-1.json"),
                "--fixture-page", str(FIXTURES / "synthetic-regulatory-page-2.json"),
                "--output", str(output),
            ])
            result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["counts"]["pages_retrieved"], 2)

    def test_fixture_cli_returns_nonzero_on_network_shape_failure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="k05-public-cli-fail-") as temp:
            malformed = Path(temp) / "bad.json"
            malformed.write_text('{"unexpected": []}', encoding="utf-8")
            output = Path(temp) / "result.json"
            exit_code = pdi.main([
                "--mode", pdi.TRIAL_LANDSCAPE,
                "--fixture-page", str(malformed),
                "--output", str(output),
            ])
            result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 2)
        self.assertEqual(result["status"], "CANNOT_ASSESS")
        self.assertIn("studies", result["error"]["message"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
