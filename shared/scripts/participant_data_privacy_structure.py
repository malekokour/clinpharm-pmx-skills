#!/usr/bin/env python3
"""Inventory participant-data privacy structures from synthetic schemas only.

The caller supplies an applicability declaration from its accountable owner.
This tool checks identifiers, required schema fields, flows, recipients, and
agreement references. It never ingests participant records and never concludes
lawful basis, privacy compliance, safeguard adequacy, or acceptable
re-identification risk.

Author: Malek Okour
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SYNTHETIC_CLASSIFICATION = "SYNTHETIC_SCHEMA"
APPLICABILITY_STATES = {"APPLICABLE", "NOT_APPLICABLE", "UNKNOWN"}
FORBIDDEN_PAYLOAD_KEYS = {
    "participants",
    "participant_records",
    "subjects",
    "subject_records",
    "records",
    "rows",
    "observations",
    "values",
}
APPLICABILITY_FIELDS = (
    "owner_role",
    "status",
    "jurisdictions",
    "frameworks",
    "as_of_date",
    "source_register",
)
DATASET_FIELDS = (
    "purpose",
    "fields",
    "data_classes",
    "coding_state",
    "key_custodian",
    "access_roles",
    "access_logging",
    "recipients",
    "retention_statement",
    "withdrawal_statement",
)


class RestrictedInputError(ValueError):
    """Raised before structural checks when input is not a synthetic schema."""


@dataclass(frozen=True)
class StructuralFinding:
    rule: str
    state: str
    item: str
    observed: str
    expected: str
    locator: str
    detail: str
    severity: str = "Major"


@dataclass(frozen=True)
class UnknownState:
    state: str
    question: str
    resolved_by: str
    locator: str


@dataclass
class PrivacyStructureReport:
    findings: list[StructuralFinding] = field(default_factory=list)
    unknowns: list[UnknownState] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def count(self, name: str, value: int) -> None:
        self.counts[name] = value

    def add_finding(self, **kwargs: str) -> None:
        self.findings.append(StructuralFinding(**kwargs))

    def add_unknown(self, question: str, resolved_by: str, locator: str) -> None:
        self.unknowns.append(
            UnknownState(
                state="UNKNOWN",
                question=question,
                resolved_by=resolved_by,
                locator=locator,
            )
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "tool": "participant-data-privacy-structure",
            "input_boundary": SYNTHETIC_CLASSIFICATION,
            "counts": dict(sorted(self.counts.items())),
            "findings": [asdict(item) for item in self.findings],
            "unknowns": [asdict(item) for item in self.unknowns],
            "boundary": (
                "Mechanical structure only. No participant records were processed. "
                "Applicability, lawful basis, privacy/legal compliance, safeguard "
                "adequacy, and acceptable re-identification risk remain HUMAN-REVIEW."
            ),
        }

    def render(self) -> str:
        if not self.counts:
            raise ValueError("refusing to render without visible denominators")
        denominator = " · ".join(
            f"{name} {value}" for name, value in sorted(self.counts.items())
        )
        lines = [
            (
                "participant-data-privacy-structure: "
                f"{len(self.findings)} finding(s), {len(self.unknowns)} UNKNOWN across "
                f"{denominator}"
            )
        ]
        for finding in self.findings:
            lines.append(
                f"[{finding.severity}] [{finding.state}] {finding.rule}: "
                f"{finding.item} @ {finding.locator}"
            )
            lines.append(f"  observed: {finding.observed}")
            lines.append(f"  expected: {finding.expected}")
            lines.append(f"  detail: {finding.detail}")
        for unknown in self.unknowns:
            lines.append(f"[UNKNOWN] {unknown.question} @ {unknown.locator}")
            lines.append(f"  resolved by: {unknown.resolved_by}")
        lines.append(self.as_dict()["boundary"])
        return "\n".join(lines)


def _mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _nonempty(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, (str, list, dict, tuple, set)):
        return bool(value)
    return True


def preflight(payload: dict[str, Any]) -> None:
    """Reject anything other than a declared synthetic schema envelope."""
    if payload.get("data_classification") != SYNTHETIC_CLASSIFICATION:
        raise RestrictedInputError(
            "RESTRICTED_DO_NOT_PROCESS: input must declare SYNTHETIC_SCHEMA; "
            "participant or operational data are outside this tool"
        )
    def prohibited_keys(value: Any) -> set[str]:
        found: set[str] = set()
        if isinstance(value, dict):
            for raw_key, child in value.items():
                key = str(raw_key).lower()
                if key in FORBIDDEN_PAYLOAD_KEYS:
                    found.add(key)
                    continue
                found.update(prohibited_keys(child))
        elif isinstance(value, list):
            for child in value:
                found.update(prohibited_keys(child))
        return found

    discovered = prohibited_keys(payload)
    if discovered:
        raise RestrictedInputError(
            "RESTRICTED_DO_NOT_PROCESS: record-like payload keys are prohibited; "
            "supply field names and structural metadata only"
        )


def check(payload: dict[str, Any], locator: str = "synthetic schema") -> PrivacyStructureReport:
    preflight(payload)
    report = PrivacyStructureReport()
    applicability = payload.get("applicability")
    if not isinstance(applicability, dict):
        applicability = {}

    report.count("applicability_fields_checked", len(APPLICABILITY_FIELDS) + 1)
    if applicability.get("owner_supplied") is not True:
        report.add_unknown(
            "privacy/legal applicability was not declared by an accountable owner",
            "an owner-supplied applicability declaration with owner_supplied=true",
            f"{locator}.applicability",
        )
    for field_name in APPLICABILITY_FIELDS:
        if not _nonempty(applicability.get(field_name)):
            report.add_unknown(
                f"applicability.{field_name} is not established",
                f"the accountable owner supplies applicability.{field_name}",
                f"{locator}.applicability.{field_name}",
            )
    status = str(applicability.get("status", "UNKNOWN")).upper()
    if status not in APPLICABILITY_STATES:
        report.add_finding(
            rule="unrecognised-applicability-state",
            state="MISMATCH",
            item="applicability.status",
            observed=status,
            expected="APPLICABLE, NOT_APPLICABLE, or UNKNOWN",
            locator=f"{locator}.applicability.status",
            detail="The tool preserves an owner declaration but accepts only the routing vocabulary.",
        )
    elif status == "UNKNOWN":
        report.add_unknown(
            "privacy/legal applicability remains UNKNOWN",
            "the accountable owner resolves the applicability declaration",
            f"{locator}.applicability.status",
        )

    datasets = _mapping_list(payload.get("datasets"))
    flows = _mapping_list(payload.get("flows"))
    agreements = _mapping_list(payload.get("agreements"))
    report.count("datasets", len(datasets))
    report.count("flows", len(flows))
    report.count("agreements", len(agreements))
    report.count("dataset_fields_checked", len(datasets) * len(DATASET_FIELDS))

    dataset_by_id: dict[str, dict[str, Any]] = {}
    for index, dataset in enumerate(datasets, 1):
        dataset_id = str(dataset.get("dataset_id", "")).strip()
        dataset_locator = f"{locator}.datasets[{index}]"
        if not dataset_id:
            report.add_finding(
                rule="missing-dataset-identifier",
                state="MISSING",
                item=f"dataset {index}",
                observed="absent",
                expected="a stable dataset_id",
                locator=dataset_locator,
                detail="A flow cannot resolve deterministically without an identifier.",
            )
            continue
        if dataset_id in dataset_by_id:
            report.add_finding(
                rule="duplicate-dataset-identifier",
                state="MISMATCH",
                item=dataset_id,
                observed="declared more than once",
                expected="one schema entry per dataset_id",
                locator=dataset_locator,
                detail="Duplicate identifiers make flow and agreement resolution ambiguous.",
            )
        dataset_by_id[dataset_id] = dataset
        for field_name in DATASET_FIELDS:
            if not _nonempty(dataset.get(field_name)):
                report.add_finding(
                    rule="missing-structural-field",
                    state="MISSING",
                    item=f"{dataset_id}.{field_name}",
                    observed="absent or empty",
                    expected=f"a declared {field_name} value",
                    locator=f"{dataset_locator}.{field_name}",
                    detail="Presence is checked mechanically; adequacy remains human review.",
                )

    agreement_by_id = {
        str(item.get("agreement_id", "")).strip(): item
        for item in agreements
        if str(item.get("agreement_id", "")).strip()
    }
    report.count("flow_references_checked", len(flows) * 3)
    for index, flow in enumerate(flows, 1):
        flow_locator = f"{locator}.flows[{index}]"
        dataset_id = str(flow.get("dataset_id", "")).strip()
        recipient = str(flow.get("recipient", "")).strip()
        agreement_id = str(flow.get("agreement_id", "")).strip()
        dataset = dataset_by_id.get(dataset_id)
        if dataset is None:
            report.add_finding(
                rule="flow-dataset-unresolved",
                state="MISMATCH",
                item=dataset_id or "UNKNOWN",
                observed="flow references an undeclared dataset",
                expected="dataset_id present in datasets",
                locator=f"{flow_locator}.dataset_id",
                detail="No participant data are inspected; this is identifier resolution only.",
            )
        elif recipient and recipient not in dataset.get("recipients", []):
            report.add_finding(
                rule="recipient-not-declared-for-dataset",
                state="MISMATCH",
                item=recipient,
                observed=recipient,
                expected=(
                    "one of dataset.recipients: "
                    + ", ".join(str(item) for item in dataset.get("recipients", []))
                ),
                locator=f"{flow_locator}.recipient",
                detail="The mismatch is preserved; transfer legality is not decided.",
            )
        if not recipient:
            report.add_unknown(
                "flow recipient is not established",
                "the data owner supplies the recipient identifier",
                f"{flow_locator}.recipient",
            )
        agreement = agreement_by_id.get(agreement_id)
        if agreement is None:
            report.add_finding(
                rule="agreement-unresolved",
                state="MISSING",
                item=agreement_id or "UNKNOWN",
                observed="no matching agreement record",
                expected="agreement_id present in agreements",
                locator=f"{flow_locator}.agreement_id",
                detail="Agreement presence is structural evidence, not a conclusion about sufficiency.",
            )
        elif recipient and recipient not in agreement.get("recipients", []):
            report.add_finding(
                rule="recipient-not-declared-in-agreement",
                state="MISMATCH",
                item=recipient,
                observed=f"flow cites {agreement_id}",
                expected="recipient listed in the referenced agreement",
                locator=f"{flow_locator}.agreement_id",
                detail="The tool does not interpret agreement terms or transfer legality.",
            )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, type=Path, help="synthetic schema JSON")
    parser.add_argument("--json", action="store_true", help="render machine-readable JSON")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RestrictedInputError(
                "RESTRICTED_DO_NOT_PROCESS: input must be a synthetic schema object"
            )
        report = check(payload, locator=args.input.name)
    except RestrictedInputError as exc:
        print(str(exc))
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print(f"CANNOT_ASSESS: could not read synthetic schema: {exc}")
        return 2
    print(json.dumps(report.as_dict(), indent=2) if args.json else report.render())
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
