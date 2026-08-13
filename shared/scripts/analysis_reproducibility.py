#!/usr/bin/env python3
"""Check declared structural evidence in an analysis reproducibility package.

This tool verifies only deterministic package facts: declared file presence and
identity, SHA-256 hashes, environment identity, run-command/seed/log evidence,
and data/code/output lineage references. It does not execute the analysis or
inspect scientific values.

It must not be described as proving scientific reproducibility, fitness for
purpose, validation, correctness, or regulated-system certification.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from findings import Finding, Report

PERMITTED_CLASSIFICATIONS = {
    "SYNTHETIC",
    "PUBLIC",
    "EXPLICITLY_REDISTRIBUTABLE",
    "OWNER_CONFIRMED_LOCAL",
}
ARTIFACT_ROLES = {"code", "configuration", "input", "output", "log", "environment"}
SEED_STATES = {"SUPPLIED", "NOT_APPLICABLE", "UNKNOWN"}
BOUNDARY = (
    "Structural evidence only. This check does not establish scientific "
    "reproducibility, fitness for purpose, validation, correctness, or "
    "regulated-system certification. Human review is required."
)


class ManifestError(ValueError):
    """The manifest cannot be checked safely or deterministically."""


def _required_text(value: Any, locator: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{locator} must be a non-empty string")
    return value.strip()


def _safe_file(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ManifestError(f"artifact path must stay inside package root: {relative!r}")
    resolved_root = root.resolve()
    lexical = resolved_root / candidate
    resolved = lexical.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ManifestError(f"artifact path escapes package root: {relative!r}")
    return lexical


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _finding(
    rule: str,
    item: str,
    observed: str,
    expected: str,
    locator: str,
    detail: str,
) -> Finding:
    return Finding(
        rule=rule,
        severity="Major",
        item=item,
        observed=observed,
        expected=expected,
        locator=locator,
        detail=detail,
    )


def check(manifest: dict[str, Any], root: Path) -> Report:
    """Return a denominator-bearing report over the manifest's declared facts."""
    if not isinstance(manifest, dict):
        raise ManifestError("manifest must be one JSON object")

    classification = _required_text(manifest.get("data_classification"), "data_classification")
    if classification not in PERMITTED_CLASSIFICATIONS:
        raise ManifestError(
            "data_classification must be one of "
            f"{sorted(PERMITTED_CLASSIFICATIONS)}; received {classification!r}"
        )
    if manifest.get("preflight_state") != "PASSED":
        raise ManifestError("preflight_state must be PASSED before package files are checked")
    package_id = _required_text(manifest.get("package_id"), "package_id")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ManifestError("artifacts must be a non-empty list")

    report = Report(tool="analysis-reproducibility")
    report.count("artifacts_declared", len(artifacts))
    report.count("package_identities_checked", 1)

    by_id: dict[str, dict[str, str]] = {}
    present_ids: set[str] = set()
    hashes_checked = hashes_matched = 0
    for index, row in enumerate(artifacts):
        if not isinstance(row, dict):
            raise ManifestError(f"artifacts[{index}] must be an object")
        artifact_id = _required_text(row.get("id"), f"artifacts[{index}].id")
        if artifact_id in by_id:
            raise ManifestError(f"duplicate artifact id: {artifact_id}")
        relative = _required_text(row.get("path"), f"artifacts[{index}].path")
        role = _required_text(row.get("role"), f"artifacts[{index}].role")
        if role not in ARTIFACT_ROLES:
            raise ManifestError(
                f"artifacts[{index}].role must be one of {sorted(ARTIFACT_ROLES)}"
            )
        expected_hash = _required_text(row.get("sha256"), f"artifacts[{index}].sha256")
        if len(expected_hash) != 64 or any(ch not in "0123456789abcdef" for ch in expected_hash):
            raise ManifestError(f"artifacts[{index}].sha256 must be lowercase SHA-256")
        by_id[artifact_id] = {"path": relative, "role": role, "sha256": expected_hash}

        path = _safe_file(root, relative)
        if path.is_symlink():
            report.add(
                _finding(
                    "artifact-symlink-not-checked",
                    artifact_id,
                    "symbolic link",
                    "regular file inside the declared package root",
                    f"manifest.artifacts[{index}]",
                    "Symlinks are not followed because they can escape the declared package.",
                )
            )
            continue
        if not path.is_file():
            report.add(
                _finding(
                    "artifact-absent",
                    artifact_id,
                    "absent",
                    relative,
                    f"manifest.artifacts[{index}]",
                    "The manifest declares an artifact that is not present.",
                )
            )
            continue

        present_ids.add(artifact_id)
        actual_hash = _sha256(path)
        hashes_checked += 1
        if actual_hash == expected_hash:
            hashes_matched += 1
        else:
            report.add(
                _finding(
                    "artifact-hash-mismatch",
                    artifact_id,
                    actual_hash,
                    expected_hash,
                    relative,
                    "The present file does not match the identity declared by the manifest.",
                )
            )

    report.count("artifacts_present", len(present_ids))
    report.count("hashes_checked", hashes_checked)
    report.count("hashes_matched", hashes_matched)

    environment = manifest.get("environment")
    if not isinstance(environment, dict):
        raise ManifestError("environment must be an object")
    environment_checks = 0
    environment_id = environment.get("manifest_artifact_id")
    environment_checks += 1
    if not isinstance(environment_id, str) or environment_id not in by_id:
        report.add(
            _finding(
                "environment-manifest-unresolved",
                "environment manifest",
                repr(environment_id),
                "an artifact id declared with role environment",
                "manifest.environment.manifest_artifact_id",
                "The environment identity cannot be traced to a declared artifact.",
            )
        )
    elif by_id[environment_id]["role"] != "environment":
        report.add(
            _finding(
                "environment-role-mismatch",
                environment_id,
                by_id[environment_id]["role"],
                "environment",
                "manifest.environment.manifest_artifact_id",
                "The referenced artifact has the wrong structural role.",
            )
        )
    environment_checks += 1
    if not isinstance(environment.get("identity"), str) or not environment["identity"].strip():
        report.add(
            _finding(
                "environment-identity-absent",
                "environment identity",
                "absent",
                "a declared runtime/environment identity",
                "manifest.environment.identity",
                "Presence of a manifest file alone does not identify the environment.",
            )
        )
    report.count("environment_fields_checked", environment_checks)

    run = manifest.get("run")
    if not isinstance(run, dict):
        raise ManifestError("run must be an object")
    run_checks = 0
    run_checks += 1
    if not isinstance(run.get("command"), str) or not run["command"].strip():
        report.add(
            _finding(
                "run-command-absent",
                "declared run command",
                "absent",
                "a non-empty command string",
                "manifest.run.command",
                "The tool records the command but never executes it.",
            )
        )
    run_checks += 1
    log_id = run.get("log_artifact_id")
    if not isinstance(log_id, str) or log_id not in by_id:
        report.add(
            _finding(
                "run-log-unresolved",
                "run log",
                repr(log_id),
                "a declared artifact id with role log",
                "manifest.run.log_artifact_id",
                "The run identity cannot be traced to declared log evidence.",
            )
        )
    elif by_id[log_id]["role"] != "log":
        report.add(
            _finding(
                "run-log-role-mismatch",
                log_id,
                by_id[log_id]["role"],
                "log",
                "manifest.run.log_artifact_id",
                "The referenced artifact has the wrong structural role.",
            )
        )
    run_checks += 1
    seed = run.get("seed")
    if not isinstance(seed, dict) or seed.get("state") not in SEED_STATES:
        raise ManifestError(f"run.seed.state must be one of {sorted(SEED_STATES)}")
    if seed["state"] == "SUPPLIED" and seed.get("value") in (None, ""):
        report.add(
            _finding(
                "seed-value-absent",
                "run seed",
                "state SUPPLIED without a value",
                "a seed value",
                "manifest.run.seed",
                "A supplied seed state is not evidence without its value.",
            )
        )
    elif seed["state"] == "NOT_APPLICABLE" and not str(seed.get("rationale", "")).strip():
        report.add(
            _finding(
                "seed-rationale-absent",
                "run seed",
                "state NOT_APPLICABLE without rationale",
                "a stated non-applicability rationale",
                "manifest.run.seed",
                "Non-applicability must be declared rather than inferred.",
            )
        )
    elif seed["state"] == "UNKNOWN":
        report.cannot_assess(
            item="run seed",
            why="the manifest records the seed state as UNKNOWN",
            resolved_by="supply the seed or a documented NOT_APPLICABLE rationale",
        )
    report.count("run_fields_checked", run_checks)

    lineage = manifest.get("lineage")
    if not isinstance(lineage, list) or not lineage:
        raise ManifestError("lineage must be a non-empty list")
    references_checked = 0
    for index, row in enumerate(lineage):
        if not isinstance(row, dict):
            raise ManifestError(f"lineage[{index}] must be an object")
        refs: list[tuple[str, str, set[str]]] = []
        output_id = _required_text(row.get("output_artifact_id"), f"lineage[{index}].output_artifact_id")
        refs.append(("output_artifact_id", output_id, {"output"}))
        log_ref = _required_text(row.get("log_artifact_id"), f"lineage[{index}].log_artifact_id")
        refs.append(("log_artifact_id", log_ref, {"log"}))
        for field in ("code_artifact_ids", "input_artifact_ids"):
            values = row.get(field)
            if not isinstance(values, list) or not values:
                raise ManifestError(f"lineage[{index}].{field} must be a non-empty list")
            for value in values:
                roles = {"code", "configuration"} if field == "code_artifact_ids" else {"input"}
                refs.append(
                    (field, _required_text(value, f"lineage[{index}].{field}"), roles)
                )
        for field, artifact_id, expected_roles in refs:
            references_checked += 1
            if artifact_id not in by_id:
                report.add(
                    _finding(
                        "lineage-reference-unresolved",
                        artifact_id,
                        "not declared",
                        "an artifact id in manifest.artifacts",
                        f"manifest.lineage[{index}].{field}",
                        "The declared output cannot be traced through all named inputs, code, and log evidence.",
                    )
                )
            elif by_id[artifact_id]["role"] not in expected_roles:
                report.add(
                    _finding(
                        "lineage-role-mismatch",
                        artifact_id,
                        by_id[artifact_id]["role"],
                        " or ".join(sorted(expected_roles)),
                        f"manifest.lineage[{index}].{field}",
                        "The lineage reference resolves but identifies the wrong structural role.",
                    )
                )
    report.count("lineage_rows_checked", len(lineage))
    report.count("lineage_references_checked", references_checked)

    if manifest.get("declared_complete") is True and (report.findings or report.unassessable):
        report.add(
            _finding(
                "unsupported-completeness-claim",
                package_id,
                "declared_complete=true",
                "all declared checks resolved before claiming completeness",
                "manifest.declared_complete",
                "The manifest's completeness claim is unsupported by the structural results.",
            )
        )
    return report


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"could not read JSON manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError("manifest must be one JSON object")
    return data


def render(report: Report, as_json: bool = False) -> str:
    if as_json:
        payload = report.as_dict()
        payload["boundary"] = BOUNDARY
        return json.dumps(payload, indent=2)
    return f"{report.render()}\n{BOUNDARY}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", required=True, type=Path, help="structural JSON manifest")
    parser.add_argument("--root", required=True, type=Path, help="declared package root")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args(argv)
    try:
        report = check(load_manifest(args.manifest), args.root)
    except ManifestError as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(render(report, args.json))
    return 1 if report.findings or report.unassessable else 0


if __name__ == "__main__":
    raise SystemExit(main())
