#!/usr/bin/env python3
"""Retrieve public development records while preserving provenance and scope.

Modes
-----
``REGULATORY-PRECEDENT`` retrieves public Drugs@FDA application records from
openFDA. ``TRIAL-LANDSCAPE`` retrieves public study records from the
ClinicalTrials.gov API v2.

This is a retrieval recorder, not an interpretation engine. It preserves the
caller's filters, page boundaries, timestamps, exclusions, raw records, and
exact public identifiers. It never decides similarity, agency acceptance,
competitive importance, differentiation, materiality, valuation,
approvability, or go/no-go.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections.abc import Callable, Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REGULATORY_PRECEDENT = "REGULATORY-PRECEDENT"
TRIAL_LANDSCAPE = "TRIAL-LANDSCAPE"
MODES = (REGULATORY_PRECEDENT, TRIAL_LANDSCAPE)

ENDPOINTS = {
    REGULATORY_PRECEDENT: "https://api.fda.gov/drug/drugsfda.json",
    TRIAL_LANDSCAPE: "https://clinicaltrials.gov/api/v2/studies",
}
SOURCES = {
    REGULATORY_PRECEDENT: "openFDA Drugs@FDA",
    TRIAL_LANDSCAPE: "ClinicalTrials.gov API v2",
}
FORBIDDEN_FILTER_PARTS = ("api_key", "apikey", "token", "password", "secret", "authorization")
PAGINATION_FILTERS = {"limit", "skip", "pagesize", "pagetoken", "format"}
BOUNDARY = (
    "Public-record retrieval only. Human review decides similarity, agency acceptance, "
    "competitive importance, differentiation, materiality, valuation, approvability, "
    "and go/no-go."
)

Fetcher = Callable[[str, float], bytes]
Clock = Callable[[], datetime]


class RetrievalInputError(ValueError):
    """The caller's retrieval specification is unsafe or malformed."""


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_utc(clock: Clock) -> str:
    value = clock()
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def http_get(url: str, timeout: float) -> bytes:
    request = Request(url, headers={"User-Agent": "ClinPharm-PMx-Skills-public-retrieval/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        raise OSError(f"HTTP {exc.code} from public endpoint") from exc
    except URLError as exc:
        raise OSError(f"public endpoint unavailable: {exc.reason}") from exc


def _validate_filters(filters: Mapping[str, Any]) -> None:
    if not isinstance(filters, Mapping):
        raise RetrievalInputError("filters must be a JSON object")
    for key, value in filters.items():
        if not isinstance(key, str) or not key.strip():
            raise RetrievalInputError("every filter name must be a non-empty string")
        lowered = key.casefold()
        if any(part in lowered for part in FORBIDDEN_FILTER_PARTS):
            raise RetrievalInputError(
                f"filter {key!r} looks credential-bearing; use public unauthenticated retrieval only"
            )
        if lowered in PAGINATION_FILTERS:
            raise RetrievalInputError(
                f"filter {key!r} is pagination control; use page_size or start_cursor instead"
            )
        values: Iterable[Any] = value if isinstance(value, list) else (value,)
        if not all(isinstance(item, (str, int, float, bool)) for item in values):
            raise RetrievalInputError(
                f"filter {key!r} must be a string, number, boolean, or a list of them"
            )


def _query_items(filters: Mapping[str, Any]) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    for key in sorted(filters):
        value = filters[key]
        if isinstance(value, list):
            items.extend((key, item) for item in value)
        else:
            items.append((key, value))
    return items


def _build_url(
    mode: str,
    filters: Mapping[str, Any],
    page_size: int,
    cursor: str | int | None,
) -> str:
    params = _query_items(filters)
    if mode == REGULATORY_PRECEDENT:
        params.append(("limit", page_size))
        if cursor not in (None, "", 0, "0"):
            params.append(("skip", int(cursor)))
    else:
        params.extend((("format", "json"), ("pageSize", page_size)))
        if cursor not in (None, ""):
            params.append(("pageToken", str(cursor)))
    return f"{ENDPOINTS[mode]}?{urlencode(params, doseq=True)}"


def _page_records(mode: str, payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    field = "results" if mode == REGULATORY_PRECEDENT else "studies"
    records = payload.get(field)
    if not isinstance(records, list):
        raise TypeError(f"response field {field!r} is missing or is not a list")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"response field {field!r} contains a non-object record")
    return records


def public_record_id(mode: str, record: Mapping[str, Any]) -> str | None:
    """Return the exact public identifier without normalization or inference."""
    if mode == REGULATORY_PRECEDENT:
        value = record.get("application_number")
    else:
        protocol = record.get("protocolSection")
        identification = protocol.get("identificationModule") if isinstance(protocol, dict) else None
        value = identification.get("nctId") if isinstance(identification, dict) else None
    return value if isinstance(value, str) and value.strip() else None


def _next_cursor(
    mode: str,
    payload: Mapping[str, Any],
    cursor: str | int | None,
    records_seen_on_page: int,
) -> str | int | None:
    if mode == TRIAL_LANDSCAPE:
        token = payload.get("nextPageToken")
        if token is None:
            return None
        if not isinstance(token, str) or not token:
            raise ValueError("nextPageToken is present but is not a non-empty string")
        return token

    meta = payload.get("meta")
    results = meta.get("results") if isinstance(meta, dict) else None
    total = results.get("total") if isinstance(results, dict) else None
    if not isinstance(total, int) or total < 0:
        raise ValueError("openFDA response lacks a non-negative meta.results.total")
    current = int(cursor or 0)
    next_offset = current + records_seen_on_page
    if next_offset >= total:
        return None
    if records_seen_on_page == 0:
        raise ValueError("openFDA pagination made no progress before reaching total")
    return next_offset


def retrieve(
    mode: str,
    filters: Mapping[str, Any],
    *,
    page_size: int = 50,
    max_pages: int = 1,
    start_cursor: str | int | None = None,
    exclude_ids: Iterable[str] = (),
    fetcher: Fetcher = http_get,
    clock: Clock = utc_now,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Retrieve bounded public records and return a complete provenance ledger.

    Transport and response defects are represented as ``CANNOT_ASSESS`` in the
    returned object. Input-contract defects raise ``RetrievalInputError`` so the
    caller can correct them before any request is made.
    """
    if mode not in MODES:
        raise RetrievalInputError(f"mode must be one of {MODES}")
    _validate_filters(filters)
    if not 1 <= page_size <= (99 if mode == REGULATORY_PRECEDENT else 1000):
        raise RetrievalInputError("page_size is outside the public endpoint's supported bound")
    if max_pages < 1:
        raise RetrievalInputError("max_pages must be at least 1")
    if timeout <= 0:
        raise RetrievalInputError("timeout must be positive")
    if mode == REGULATORY_PRECEDENT and start_cursor not in (None, ""):
        try:
            if int(start_cursor) < 0:
                raise ValueError
        except (TypeError, ValueError) as exc:
            raise RetrievalInputError(
                "REGULATORY-PRECEDENT start_cursor must be a non-negative integer offset"
            ) from exc

    caller_filters = copy.deepcopy(dict(filters))
    requested_exclusions = [str(value) for value in exclude_ids]
    exclusion_set = set(requested_exclusions)
    started = iso_utc(clock)
    output: dict[str, Any] = {
        "mode": mode,
        "status": "CANNOT_ASSESS",
        "complete": False,
        "source": SOURCES[mode],
        "endpoint": ENDPOINTS[mode],
        "caller_filters": caller_filters,
        "pagination": {
            "page_size": page_size,
            "max_pages": max_pages,
            "start_cursor": start_cursor,
            "next_cursor": start_cursor,
        },
        "retrieval_started_at": started,
        "retrieval_finished_at": None,
        "requests": [],
        "records": [],
        "exclusions_requested": requested_exclusions,
        "exclusions": [],
        "error": None,
        "counts": {},
        "boundary": BOUNDARY,
    }

    cursor = start_cursor
    seen_ids: set[str] = set()
    next_cursor: str | int | None = cursor

    for page_number in range(1, max_pages + 1):
        url = _build_url(mode, filters, page_size, cursor)
        request_row: dict[str, Any] = {
            "page": page_number,
            "cursor_in": cursor,
            "url": url,
            "retrieved_at": None,
            "outcome": "error",
        }
        output["requests"].append(request_row)
        try:
            body = fetcher(url, timeout)
            retrieved_at = iso_utc(clock)
            request_row["retrieved_at"] = retrieved_at
            payload = json.loads(body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise TypeError("response root is not a JSON object")
            page_records = _page_records(mode, payload)
            next_cursor = _next_cursor(mode, payload, cursor, len(page_records))
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            request_row["error"] = f"{type(exc).__name__}: {exc}"
            output["error"] = {
                "state": "CANNOT_ASSESS",
                "stage": "public_retrieval",
                "message": str(exc),
                "page": page_number,
                "completed_pages": page_number - 1,
            }
            break

        request_row["outcome"] = "retrieved"
        request_row["records_returned"] = len(page_records)
        request_row["next_cursor"] = next_cursor

        for ordinal, record in enumerate(page_records, start=1):
            exact_id = public_record_id(mode, record)
            base = {
                "page": page_number,
                "record_ordinal": ordinal,
                "public_record_id": exact_id or "UNKNOWN",
                "source": SOURCES[mode],
                "request_url": url,
                "retrieved_at": retrieved_at,
            }
            if exact_id is None:
                output["exclusions"].append(
                    {**base, "reason": "missing-public-record-id", "record": record}
                )
                continue
            if exact_id in exclusion_set:
                output["exclusions"].append(
                    {**base, "reason": "caller-specified-exclusion", "record": record}
                )
                continue
            if exact_id in seen_ids:
                output["exclusions"].append(
                    {**base, "reason": "duplicate-public-record-id", "record": record}
                )
                continue
            seen_ids.add(exact_id)
            output["records"].append({**base, "record": record})

        if next_cursor is None:
            output["status"] = "COMPLETE"
            output["complete"] = True
            break
        cursor = next_cursor
    else:
        output["error"] = {
            "state": "CANNOT_ASSESS",
            "stage": "pagination",
            "message": "bounded_before_exhaustion",
            "page": max_pages,
            "completed_pages": max_pages,
        }

    output["pagination"]["next_cursor"] = next_cursor
    output["retrieval_finished_at"] = iso_utc(clock)
    output["counts"] = {
        "requests_attempted": len(output["requests"]),
        "pages_retrieved": sum(row["outcome"] == "retrieved" for row in output["requests"]),
        "records_retained": len(output["records"]),
        "records_excluded": len(output["exclusions"]),
        "caller_exclusions_declared": len(requested_exclusions),
    }
    return output


class FixtureFetcher:
    """Serve deterministic JSON pages in order for tests and offline examples."""

    def __init__(self, paths: Iterable[Path]):
        self.paths = list(paths)
        self.index = 0

    def __call__(self, _url: str, _timeout: float) -> bytes:
        if self.index >= len(self.paths):
            raise OSError("fixture pages exhausted before pagination completed")
        path = self.paths[self.index]
        self.index += 1
        return path.read_bytes()


def _filters_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.filters_json:
        value = json.loads(Path(args.filters_json).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise RetrievalInputError("--filters-json must contain one JSON object")
        return value
    filters: dict[str, Any] = {}
    for item in args.filter:
        if "=" not in item:
            raise RetrievalInputError(f"filter {item!r} must use NAME=VALUE")
        name, value = item.split("=", 1)
        if name in filters:
            current = filters[name]
            filters[name] = [*current, value] if isinstance(current, list) else [current, value]
        else:
            filters[name] = value
    return filters


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--filter", action="append", default=[], metavar="NAME=VALUE")
    parser.add_argument("--filters-json", help="path to a JSON object of caller filters")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--start-cursor")
    parser.add_argument("--exclude-id", action="append", default=[])
    parser.add_argument(
        "--fixture-page",
        action="append",
        default=[],
        help="offline deterministic JSON response page; may be repeated",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output", help="write JSON to this path instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.filters_json and args.filter:
        parser.error("use either --filters-json or --filter, not both")
    try:
        filters = _filters_from_args(args)
        fetcher: Fetcher = (
            FixtureFetcher(Path(value) for value in args.fixture_page)
            if args.fixture_page
            else http_get
        )
        result = retrieve(
            args.mode,
            filters,
            page_size=args.page_size,
            max_pages=args.max_pages,
            start_cursor=args.start_cursor,
            exclude_ids=args.exclude_id,
            fetcher=fetcher,
            timeout=args.timeout,
        )
    except (RetrievalInputError, OSError, json.JSONDecodeError) as exc:
        result = {
            "status": "CANNOT_ASSESS",
            "complete": False,
            "error": {"stage": "input", "message": str(exc)},
            "boundary": BOUNDARY,
        }

    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result.get("complete") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
