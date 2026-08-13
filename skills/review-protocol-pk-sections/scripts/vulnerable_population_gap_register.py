#!/usr/bin/env python3
"""VENDORED at build time from shared/scripts/ — do not edit here.
Edit the canonical source and rebuild; a freshness check compares them.

Map owner-declared vulnerable-population mentions to structural artifact locators.

Source basis (accessed 2026-08-11): ICH E6(R3) Annex 1 participant-protection
sections; WMA Declaration of Helsinki 2024; 21 CFR 50/56; 45 CFR 46; EU Clinical
Trials Regulation Articles 31-35; and Japan's 2023-amended ethical guidelines.
These sources motivate an artifact inventory. They do not supply a universal
vulnerability taxonomy or permit this tool to decide applicability.

The input is a structural manifest, never participant-level data. The accountable
owner declares the populations and the jurisdiction/site applicability profile.
For each declared population, this tool checks only whether locators were supplied
for rationale, assent/representative process, compensation, specialist input, and
committee records. Every row remains HUMAN_REVIEW with disposition UNSET.

The tool never judges vulnerability, capacity, coercion, safeguard adequacy, or
risk-benefit, and never recommends enrolment, continuation, or a safety action.

Author: Malek Okour
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ARTIFACT_FIELDS = (
    "rationale",
    "assent_or_representative",
    "compensation",
    "specialist_input",
    "committee_record",
)

APPLICABILITY_FIELDS = (
    "profile_id",
    "profile_version",
    "as_of",
    "jurisdictions",
    "owner",
)

SOURCE_BASIS = (
    "ICH E6(R3) Annex 1 participant-protection sections",
    "WMA Declaration of Helsinki 2024",
    "21 CFR Parts 50 and 56",
    "45 CFR Part 46",
    "EU Clinical Trials Regulation Articles 31-35",
    "Japan 2023-amended ethical guidelines for human-subject research",
)

PROHIBITED_KEYS = {
    "participant_data",
    "participant_records",
    "individual_records",
    "subject_ids",
    "dates_of_birth",
}

HUMAN_ONLY_BOUNDARY = (
    "Vulnerability, capacity, coercion, safeguard adequacy, and risk-benefit are "
    "human judgments. This register reports supplied structural locators only."
)


class ManifestError(ValueError):
    """The input is not a bounded structural manifest."""


def _find_prohibited_keys(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in PROHIBITED_KEYS:
                found.append(child_path)
            found.extend(_find_prohibited_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_prohibited_keys(child, f"{path}[{index}]"))
    return found


def _status_for(artifacts: dict[str, Any], field: str) -> tuple[str, str | None, str]:
    if field not in artifacts:
        return (
            "UNKNOWN",
            None,
            "The manifest does not state whether this artifact was assessed.",
        )
    value = artifacts[field]
    if value is None or (isinstance(value, str) and not value.strip()):
        return (
            "MISSING",
            None,
            "The owner explicitly supplied no artifact locator for this field.",
        )
    if not isinstance(value, str):
        raise ManifestError(f"artifact {field!r} must be a locator string or null")
    return "PRESENT", value.strip(), "A locator was supplied; adequacy was not assessed."


def build_register(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic presence/locator register with explicit denominators."""
    if not isinstance(manifest, dict):
        raise ManifestError("input must be one JSON object")

    prohibited = _find_prohibited_keys(manifest)
    if prohibited:
        joined = ", ".join(prohibited)
        raise ManifestError(
            "participant-level fields are prohibited; supply a structural manifest only: "
            f"{joined}"
        )

    source_set = manifest.get("source_set")
    if not isinstance(source_set, list) or not all(
        isinstance(item, str) and item.strip() for item in source_set
    ):
        raise ManifestError("source_set must be a non-empty list of document identities")

    applicability = manifest.get("applicability", {})
    if not isinstance(applicability, dict):
        raise ManifestError("applicability must be an object when supplied")
    applicability_unknown = [
        field for field in APPLICABILITY_FIELDS if not applicability.get(field)
    ]

    populations = manifest.get("populations")
    if populations is None:
        populations = []
        population_state = "UNKNOWN"
    elif not isinstance(populations, list):
        raise ManifestError("populations must be a list when supplied")
    else:
        population_state = "PRESENT"

    rows: list[dict[str, Any]] = []
    counts = {"PRESENT": 0, "MISSING": 0, "UNKNOWN": 0}
    for index, population in enumerate(populations):
        if not isinstance(population, dict):
            raise ManifestError(f"populations[{index}] must be an object")
        population_id = population.get("population_id")
        population_label = population.get("population_label")
        source_locator = population.get("source_locator")
        if not all(
            isinstance(value, str) and value.strip()
            for value in (population_id, population_label, source_locator)
        ):
            raise ManifestError(
                f"populations[{index}] needs population_id, population_label, and "
                "source_locator strings"
            )
        artifacts = population.get("artifacts", {})
        if not isinstance(artifacts, dict):
            raise ManifestError(f"populations[{index}].artifacts must be an object")

        checks: list[dict[str, Any]] = []
        for field in ARTIFACT_FIELDS:
            status, locator, note = _status_for(artifacts, field)
            counts[status] += 1
            checks.append(
                {
                    "artifact": field,
                    "status": status,
                    "locator": locator,
                    "note": note,
                    "human_disposition": "UNSET",
                }
            )
        rows.append(
            {
                "population_id": population_id.strip(),
                "population_label": population_label.strip(),
                "source_locator": source_locator.strip(),
                "checks": checks,
                "result": "HUMAN_REVIEW",
                "human_disposition": "UNSET",
            }
        )

    field_denominator = len(populations) * len(ARTIFACT_FIELDS)
    return {
        "artifact_id": "vulnerable-population-gap-register",
        "source_basis": list(SOURCE_BASIS),
        "input_source_set": source_set,
        "applicability": {
            "state": "UNKNOWN" if applicability_unknown else "SUPPLIED",
            "missing_fields": applicability_unknown,
            "values": applicability,
        },
        "population_declaration_state": population_state,
        "denominators": {
            "populations_declared": len(populations),
            "artifact_fields_per_population": len(ARTIFACT_FIELDS),
            "artifact_fields_checked": field_denominator,
        },
        "counts": counts,
        "rows": rows,
        "result": "HUMAN_REVIEW",
        "boundary": HUMAN_ONLY_BOUNDARY,
    }


def render_text(report: dict[str, Any]) -> str:
    denominators = report["denominators"]
    counts = report["counts"]
    lines = [
        "vulnerable-population-gap-register",
        (
            "checked "
            f"{denominators['artifact_fields_checked']} artifact fields across "
            f"{denominators['populations_declared']} declared populations "
            f"({denominators['artifact_fields_per_population']} fields each)"
        ),
        (
            f"PRESENT {counts['PRESENT']} · MISSING {counts['MISSING']} · "
            f"UNKNOWN {counts['UNKNOWN']} · result HUMAN_REVIEW"
        ),
    ]
    for row in report["rows"]:
        lines.append(
            f"[{row['population_id']}] {row['population_label']} @ {row['source_locator']}"
        )
        for check in row["checks"]:
            locator = check["locator"] or "no locator supplied"
            lines.append(f"  {check['artifact']}: {check['status']} — {locator}")
    if report["applicability"]["state"] == "UNKNOWN":
        missing = ", ".join(report["applicability"]["missing_fields"])
        lines.append(f"applicability: UNKNOWN — missing {missing}")
    lines.append(report["boundary"])
    return "\n".join(lines)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"could not read JSON manifest {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, type=Path, help="structural JSON manifest")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args(argv)

    try:
        report = build_register(load_manifest(args.input))
    except ManifestError as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    print(json.dumps(report, indent=2) if args.json else render_text(report))
    has_gap = (
        report["population_declaration_state"] == "UNKNOWN"
        or report["applicability"]["state"] == "UNKNOWN"
        or report["counts"]["MISSING"] > 0
        or report["counts"]["UNKNOWN"] > 0
    )
    return 1 if has_gap else 0


if __name__ == "__main__":
    raise SystemExit(main())
