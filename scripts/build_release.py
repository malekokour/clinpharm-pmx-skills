#!/usr/bin/env python3
"""Build deterministic ClinPharm PMx Skills release assets and checksums.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: Python standard library
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from privacy_scan import scan_paths
from skill_status import released_ids

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
FIXED_ZIP_TIME = (2026, 7, 30, 12, 0, 0)
BUILDER_VERSION = "1.0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "uncommitted-source"


def add_to_zip(archive: zipfile.ZipFile, source: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def discover_skills() -> list[Path]:
    """Every *released* package. Discovery, never a hard-coded name (PS-D010).

    Discovery is by declared status, not by what exists on disk. The previous
    implementation globbed ``skills/*/SKILL.md`` and therefore packaged all
    all package directories — including the twenty whose qualification gate has
    never run — while this docstring already claimed it returned released
    packages only. Reading the status is what makes the claim true.
    """
    base = ROOT / "skills"
    if not base.is_dir():
        return []
    selected: list[Path] = []
    for skill_id in released_ids(ROOT):
        directory = base / skill_id
        if not (directory / "SKILL.md").is_file():
            raise SystemExit(
                f"{skill_id}: declared 'released' but skills/{skill_id}/SKILL.md "
                "does not exist, so the release cannot be built"
            )
        selected.append(directory)
    return selected


def build(output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    skills = discover_skills()
    if not skills:
        raise SystemExit("no released skill found: expected at least one skills/*/SKILL.md")

    packages = [output / f"{s.name}-v{VERSION}.zip" for s in skills]
    expected_names = {p.name for p in packages} | {
        "Pharma-Work-Context.docx",
        "Pharma-Work-Context.md",
        "clinpharm-pmx-skills-workflow.gif",
        "clinpharm-pmx-skills-workflow.mp4",
        "RELEASE-SCAN-REPORT.json",
        "RELEASE-MANIFEST.json",
        "SHA256SUMS.txt",
    }
    # per-skill starters, when they exist
    for skill in skills:
        for suffix in (".md", ".docx"):
            for candidate in (ROOT / "docs" / "archive" / "starter" / skill.name).glob(f"*{suffix}"):
                expected_names.add(candidate.name)

    unexpected = sorted(
        path.name for path in output.iterdir() if path.name not in expected_names
    )
    if unexpected:
        raise SystemExit(f"release output contains unexpected files: {unexpected}")
    for path in output.iterdir():
        if path.is_file():
            path.unlink()

    # One self-contained archive per skill. Each extracts to <skill-id>/ and
    # carries LICENSE, so it installs from extraction alone with no repo root.
    for skill, package in zip(skills, packages):
        with zipfile.ZipFile(package, "w") as archive:
            for path in sorted(skill.rglob("*")):
                if path.is_file():
                    add_to_zip(archive, path, str(path.relative_to(skill.parent)))
            add_to_zip(archive, ROOT / "LICENSE", "LICENSE")

    copies = [
        (
            ROOT / "docs/assets/clinpharm-pmx-skills-workflow.gif",
            output / "clinpharm-pmx-skills-workflow.gif",
        ),
        (
            ROOT / "docs/assets/clinpharm-pmx-skills-workflow.mp4",
            output / "clinpharm-pmx-skills-workflow.mp4",
        ),
    ]
    for source, target in copies:
        shutil.copy2(source, target)

    assets = sorted([*packages, *(target for _, target in copies)])
    scan_report = output / "RELEASE-SCAN-REPORT.json"
    # Scan the assets by name, not by walking the output directory through the
    # repository allowlist. That allowlist matches no release asset, so it
    # scanned nothing and passed. `verify` re-checks the denominator.
    if scan_paths(assets, output, scan_report):
        raise SystemExit("release asset privacy scan failed")
    assets.append(scan_report)
    manifest = {
        "schema_version": "1.0",
        "release": f"v{VERSION}",
        "source_commit": source_commit(),
        "tool_versions": {
            "builder": BUILDER_VERSION,
            "python": platform.python_version(),
        },
        "assets": [
            {
                "name": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in assets
        ],
    }
    manifest_path = output / "RELEASE-MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    assets.append(manifest_path)
    checksums = output / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in sorted(assets)),
        encoding="utf-8",
    )
    assets.append(checksums)
    return assets


def verify(assets: list[Path]) -> None:
    """Every skill archive must be self-contained: its own SKILL.md plus LICENSE.

    Checked per package rather than for one named skill, so adding a skill
    cannot silently escape verification.
    """
    packages = [p for p in assets if p.suffix == ".zip"]
    if not packages:
        raise SystemExit("no skill archive found in the release assets")
    # Checked here as well as at discovery. `released` is the product's central
    # honesty claim, and a release is the one artifact where breaking it is
    # public and permanent, so it is asserted on the bytes that were actually
    # built rather than only on the intent that built them.
    qualified = set(released_ids(ROOT))
    for package in packages:
        shipped = package.name.rsplit("-v", 1)[0]
        if shipped not in qualified:
            raise SystemExit(
                f"release contains {package.name}, but '{shipped}' is not "
                "'released' — its evaluation gate has not passed"
            )
    for package in packages:
        skill_id = package.name.rsplit("-v", 1)[0]
        with zipfile.ZipFile(package) as archive:
            names = set(archive.namelist())
            required = {f"{skill_id}/SKILL.md", f"{skill_id}/README.md", "LICENSE"}
            missing = required - names
            if missing:
                raise SystemExit(
                    f"release package {package.name} missing: {sorted(missing)}"
                )
            for info in archive.infolist():
                member = Path(info.filename)
                if member.is_absolute() or ".." in member.parts:
                    raise SystemExit(f"unsafe release archive path: {info.filename}")
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise SystemExit(
                        f"release archive contains symlink: {info.filename}"
                    )
            # Extract into an empty directory with no repository present and
            # prove the package stands alone.
            with tempfile.TemporaryDirectory(prefix="clinpharm-release-extract-") as temp:
                archive.extractall(temp)
                extracted = Path(temp)
                if not (extracted / f"{skill_id}/SKILL.md").is_file():
                    raise SystemExit(f"{package.name}: extracted package missing SKILL.md")
                if not (extracted / "LICENSE").is_file():
                    raise SystemExit(f"{package.name}: extracted package missing LICENSE")
    for path in assets:
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"invalid release asset: {path}")
    manifest = json.loads(
        next(path for path in assets if path.name == "RELEASE-MANIFEST.json").read_text(
            encoding="utf-8"
        )
    )
    if manifest.get("source_commit") != source_commit():
        raise SystemExit("release manifest source commit does not match HEAD")
    scan = json.loads(
        next(path for path in assets if path.name == "RELEASE-SCAN-REPORT.json").read_text(
            encoding="utf-8"
        )
    )
    if scan.get("status") != "PASS" or scan.get("finding_count") != 0:
        raise SystemExit("release scan report is not a zero-finding pass")

    # A zero-finding pass over zero files is not a pass. The release scan
    # reported exactly that for as long as it walked the output directory
    # through the repository allowlist, so the denominator is checked here
    # rather than trusted.
    generated = {"RELEASE-SCAN-REPORT.json", "RELEASE-MANIFEST.json", "SHA256SUMS.txt"}
    expected_scanned = [path for path in assets if path.name not in generated]
    if not expected_scanned:
        raise SystemExit("release scan had nothing to scan: no assets were built")
    if scan.get("files_scanned") != len(expected_scanned):
        raise SystemExit(
            "release scan denominator is wrong: it scanned "
            f"{scan.get('files_scanned')} file(s) but the release contains "
            f"{len(expected_scanned)}"
        )
    # Every release carries skill archives, so a scan that opened no archive
    # member never looked inside a ZIP — the one place private material would
    # actually hide.
    if scan.get("archive_members_scanned", 0) < 1:
        raise SystemExit(
            "release scan opened no archive members, so the skill packages "
            "were never inspected"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build and verify in an isolated temporary directory.",
    )
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="clinpharm-release-") as temp:
            assets = build(Path(temp))
            verify(assets)
            print(f"PASS: release package verified with {len(assets)} assets")
        return 0
    assets = build(args.output.resolve())
    verify(assets)
    print(f"PASS: built {len(assets)} release assets in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
