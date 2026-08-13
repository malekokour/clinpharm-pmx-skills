#!/usr/bin/env python3
"""Verify committed DOCX contents match deterministic Markdown generation.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: python-docx
"""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

from build_docx import PACKAGE_TIME, markdown_to_docx

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (
        "examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.md",
        "examples/clinpharm-pmx/outputs/My-Pharma-Work-Context.docx",
    ),
    (
        "examples/clinpharm-pmx/outputs/AI-Working-Pack-SYN-101.md",
        "examples/clinpharm-pmx/outputs/AI-Working-Pack-SYN-101.docx",
    ),
)


def package_members(path: Path) -> dict[str, bytes]:
    """Return uncompressed package members keyed by their portable ZIP names."""
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def package_metadata_errors(path: Path) -> list[str]:
    """Check the stable ZIP metadata controlled by the DOCX generator."""
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != sorted(names):
            errors.append("members are not sorted")
        for info in archive.infolist():
            if info.date_time != PACKAGE_TIME:
                errors.append(f"{info.filename}: timestamp is not normalized")
            if info.create_system != 3:
                errors.append(f"{info.filename}: creator system is not normalized")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                errors.append(f"{info.filename}: compression type is not normalized")
            if info.external_attr != 0o100644 << 16:
                errors.append(f"{info.filename}: file mode is not normalized")
    return errors


def differing_members(left: Path, right: Path) -> list[str]:
    """List package members whose presence or uncompressed content differs."""
    left_members = package_members(left)
    right_members = package_members(right)
    return sorted(
        name
        for name in left_members.keys() | right_members.keys()
        if left_members.get(name) != right_members.get(name)
    )


def main() -> int:
    failures: list[tuple[str, list[str]]] = []
    with tempfile.TemporaryDirectory(prefix="clinpharm-docx-") as temp:
        temporary_root = Path(temp)
        for source_name, generated_name in PAIRS:
            source = ROOT / source_name
            committed = ROOT / generated_name
            rebuilt = temporary_root / Path(generated_name).name
            markdown_to_docx(source, rebuilt)
            differences = differing_members(committed, rebuilt)
            metadata_errors = [
                *(f"committed: {error}" for error in package_metadata_errors(committed)),
                *(f"rebuilt: {error}" for error in package_metadata_errors(rebuilt)),
            ]
            if differences or metadata_errors:
                details = [
                    *(f"member differs: {name}" for name in differences),
                    *metadata_errors,
                ]
                failures.append((generated_name, details))
            else:
                print(f"PASS: generated artifact is current: {generated_name}")
    if failures:
        print(f"FAILED: {len(failures)} generated DOCX file(s) are stale")
        for generated_name, details in failures:
            print(f"- {generated_name}")
            for detail in details[:8]:
                print(f"  - {detail}")
        return 1
    print(f"PASS: {len(PAIRS)}/{len(PAIRS)} generated DOCX files are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
