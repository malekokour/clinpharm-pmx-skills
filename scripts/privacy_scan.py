#!/usr/bin/env python3
"""Scan the intended public tree and packaged metadata for private material.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: Python standard library; Pillow for image metadata inspection
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import public_surface as _surface

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_qa/release-scan-report.json"
IGNORED_PARTS = {
    ".git",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "_eval-workspace",
    "_qa",
    "dist",
    "launch",
}
TEXT_SUFFIXES = {
    "",
    ".cff",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
FORBIDDEN_SUFFIXES = {
    ".csv",
    ".env",
    ".key",
    ".pem",
    ".sas7bdat",
    ".xpt",
    ".xlsx",
}
PATH_PATTERNS = [
    re.compile(re.escape("/" + "Users/")),
    re.compile(re.escape("/" + "home/")),
    re.compile(re.escape("/" + "Volumes/")),
    re.compile(re.escape("/" + "tmp/")),
    re.compile("file" + re.escape("://"), re.IGNORECASE),
    re.compile("codex" + re.escape("-runtimes"), re.IGNORECASE),
    re.compile(r"\b" + "local" + r"host\b", re.IGNORECASE),
    re.compile(r"\b127\." + r"0\.0\.1\b"),
]
PRIVATE_PRODUCT_TERMS = [
    "Context" + "Pharma",
    "AIML-" + "PharmaDom",
]
PRIVATE_ENTITY_TERMS = [
    "Ser" + "vier",
    "Oni" + "vyde",
    "Tib" + "sovo",
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:ghp|github_pat|sk-proj|sk-ant)-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgho_[A-Za-z0-9]{20,}\b"),
]
# The trailing group is an explicit TLD list, not `[A-Za-z]{2,}`.
#
# Binary assets are scanned by extracting printable strings, and any two letters
# after a dot satisfied the old pattern. A real case: the mapping video reported
# `ly@tf.zs` as an unexpected email address and turned the release gate red.
# `.zs` is not a delegated TLD -- it was encoder bytes that happened to look like
# an address.
#
# This narrows rather than weakens. Every deliverable address ends in a real TLD,
# so no genuine finding is lost; what is dropped is the class of match that can
# only ever be noise. Widening the list is fine when a real address needs it.
# Loosening it back to `[A-Za-z]{2,}` re-admits the false positives, and the
# temptation to do that arrives disguised as "the scan is too strict".
#
# Canaried both directions -- see tests/test_privacy_scan_email_tld.py.
_EMAIL_TLDS = (
    "com|org|net|edu|gov|mil|int|info|biz|io|ai|co|dev|app|me|us|uk|eu|ca|au|nz|"
    "de|fr|es|it|nl|be|ch|at|se|no|dk|fi|ie|pt|pl|cz|gr|jp|cn|kr|in|sg|hk|il|"
    "br|mx|za|ru|tr|edu\\.au|ac\\.uk|co\\.uk|org\\.uk|gov\\.uk|com\\.au"
)
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:" + _EMAIL_TLDS + r")\b",
    re.IGNORECASE,
)
ALLOWED_PUBLIC_EMAILS = {"34357016+malekokour@users.noreply.github.com"}
PATIENT_IDENTIFIER_PATTERNS = [
    re.compile(
        r"\b(?:patient|participant|subject)[ _-]?(?:id|number)\s*[:=]\s*"
        r"(?!SYN-)[A-Za-z0-9][A-Za-z0-9_-]{3,}\b",
        re.IGNORECASE,
    ),
]
UNSUPPORTED_CLAIM_PATTERNS = [
    re.compile(r"\b(?:is|are)\s+(?:a\s+)?GxP[- ]validated\b", re.IGNORECASE),
    re.compile(r"\bclinically " + r"validated\b", re.IGNORECASE),
    re.compile(
        r"\breplaces?\s+(?:clinical pharmacology|pharmacometrics|medical review|"
        r"qualified (?:scientific|regulatory|medical) judgment)\b",
        re.IGNORECASE,
    ),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


#: The public surface is defined once, in ``public_surface``. See that module
#: for why this is not restated here.
PUBLIC_ROOTS = _surface.PUBLIC_ROOTS
PUBLIC_ROOT_FILES = _surface.PUBLIC_ROOT_FILES


def candidates(scan_root: Path, ignored_parts: set[str]) -> list[Path]:
    """Enumerate the public surface by allowlist (PS-D018).

    Delegates to ``public_surface.allowlist_walk`` so this scanner and the
    repository validator can never protect different sets of files.
    """
    return _surface.allowlist_walk(scan_root, ignored_parts)


def symlinks(scan_root: Path, ignored_parts: set[str]) -> list[Path]:
    """Enumerate every symlink on the public surface, **including broken ones**.

    This exists because ``allowlist_walk`` filters on ``Path.is_file()``, and a
    broken symlink is not a file. That is correct for a *content* walk — there
    are no bytes to inspect — but it meant a symlink rule could never fire on
    the case that matters most.

    Found 2026-08-13 by planting one. The plant pointed at ``../_ADMIN/``, which
    does not exist inside the public root precisely because the privacy boundary
    is geometric, so the link was broken, so the walk dropped it, so the scan
    reported ``0 findings`` over an unchanged file count. A gate that cannot see
    the thing it has a rule about is the failure mode this repository is built
    to catch, and it was sitting inside the privacy scanner.

    The sweep is deliberately separate from the content walk: it answers "what
    links out of here", not "what bytes ship", and conflating them is what hid
    the gap.
    """
    skip = ignored_parts or {"__pycache__"}
    found: list[Path] = []
    for name in sorted(_surface.PUBLIC_ROOT_FILES):
        candidate = scan_root / name
        if candidate.is_symlink():
            found.append(candidate)
    for name in sorted(_surface.PUBLIC_ROOTS):
        base = scan_root / name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if any(part in skip for part in path.parts):
                continue
            if path.is_symlink():
                found.append(path)
    return sorted(set(found))


def inspect_text(label: str, text: str, findings: list[dict[str, str]]) -> None:
    for pattern in PATH_PATTERNS:
        if pattern.search(text):
            findings.append({"path": label, "rule": "machine-specific-path"})
            break
    for term in PRIVATE_PRODUCT_TERMS:
        if term.casefold() in text.casefold():
            findings.append({"path": label, "rule": "private-product-name"})
            break
    for term in PRIVATE_ENTITY_TERMS:
        if term.casefold() in text.casefold():
            findings.append({"path": label, "rule": "private-entity-name"})
            break
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append({"path": label, "rule": "possible-secret"})
            break
    unexpected_emails = {
        match.casefold()
        for match in EMAIL_PATTERN.findall(text)
        if match.casefold() not in ALLOWED_PUBLIC_EMAILS
    }
    if unexpected_emails:
        findings.append({"path": label, "rule": "unexpected-email-address"})
    for pattern in PATIENT_IDENTIFIER_PATTERNS:
        if pattern.search(text):
            findings.append({"path": label, "rule": "possible-patient-identifier"})
            break
    for pattern in UNSUPPORTED_CLAIM_PATTERNS:
        for match in pattern.finditer(text):
            prefix = text[max(0, match.start() - 32) : match.start()].casefold()
            if not any(negation in prefix for negation in ("not ", "never ", "do not ")):
                findings.append({"path": label, "rule": "unsupported-regulated-claim"})
                return


def inspect_docx(
    path: Path, scan_root: Path, findings: list[dict[str, str]]
) -> int:
    members = 0
    try:
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                members += 1
                if name.endswith((".xml", ".rels", ".txt")):
                    text = archive.read(name).decode("utf-8", errors="replace")
                    inspect_text(f"{path.relative_to(scan_root)}::{name}", text, findings)
                if name.startswith(("word/embeddings/", "word/oleObject")):
                    findings.append(
                        {
                            "path": f"{path.relative_to(scan_root)}::{name}",
                            "rule": "embedded-docx-object",
                        }
                    )
    except zipfile.BadZipFile:
        findings.append({"path": str(path.relative_to(scan_root)), "rule": "invalid-docx"})
    return members


def inspect_image(
    path: Path, scan_root: Path, findings: list[dict[str, str]]
) -> int:
    try:
        from PIL import Image
    except ImportError:
        findings.append(
            {
                "path": str(path.relative_to(scan_root)),
                "rule": "image-metadata-not-inspected",
            }
        )
        return 0
    with Image.open(path) as image:
        metadata = {str(key): str(value) for key, value in image.info.items()}
        try:
            metadata.update({str(key): str(value) for key, value in image.getexif().items()})
        except (AttributeError, TypeError):
            pass
    inspect_text(
        f"{path.relative_to(scan_root)}::metadata",
        json.dumps(metadata, sort_keys=True),
        findings,
    )
    return len(metadata)


def inspect_video(path: Path, scan_root: Path, findings: list[dict[str, str]]) -> int:
    """Inspect printable MP4 metadata without storing matched content."""
    printable = re.findall(rb"[\x20-\x7e]{4,}", path.read_bytes())
    strings = [value.decode("ascii", errors="replace") for value in printable]
    inspect_text(
        f"{path.relative_to(scan_root)}::printable-metadata",
        "\n".join(strings),
        findings,
    )
    if not path.read_bytes()[:32].find(b"ftyp") >= 0:
        findings.append({"path": str(path.relative_to(scan_root)), "rule": "invalid-mp4"})
    return len(strings)


def inspect_zip(path: Path, scan_root: Path, findings: list[dict[str, str]]) -> int:
    members = 0
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                members += 1
                member_path = Path(info.filename)
                label = f"{path.relative_to(scan_root)}::{info.filename}"
                if member_path.is_absolute() or ".." in member_path.parts:
                    findings.append({"path": label, "rule": "unsafe-archive-path"})
                    continue
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    findings.append({"path": label, "rule": "archive-symlink"})
                if member_path.suffix.casefold() in TEXT_SUFFIXES:
                    inspect_text(
                        label,
                        archive.read(info).decode("utf-8", errors="replace"),
                        findings,
                    )
    except zipfile.BadZipFile:
        findings.append({"path": str(path.relative_to(scan_root)), "rule": "invalid-zip"})
    return members


def scan_tree(
    scan_root: Path,
    report_path: Path,
    ignored_parts: set[str] | None = None,
) -> int:
    """Scan the public surface under ``scan_root`` by allowlist (PS-D018)."""
    ignored = IGNORED_PARTS if ignored_parts is None else ignored_parts
    return scan_paths(
        candidates(scan_root, ignored),
        scan_root,
        report_path,
        links=symlinks(scan_root, ignored),
    )


def scan_paths(
    files: list[Path],
    scan_root: Path,
    report_path: Path,
    links: list[Path] | None = None,
) -> int:
    """Scan an explicit list of files, reporting paths relative to ``scan_root``.

    ``scan_tree`` enumerates the *repository's* public surface: it looks for
    directories named ``skills/``, ``docs/``, ``scripts/`` and for known root
    files. That is correct for the repository and deliberately an allowlist,
    because a denylist fails open.

    It is wrong for any tree of a different shape. ``build_release.py`` called
    ``scan_tree`` on the release output directory, which holds ``*.zip``,
    ``*.docx``, ``*.gif`` and ``*.mp4`` — none of them names the allowlist
    knows. The allowlist matched nothing, the scan read **zero files**, and it
    reported ``status: PASS`` with ``finding_count: 0``. The only privacy
    control over the bytes actually shipped never opened one of them.

    The fix is not to relax the allowlist. It is to let a caller that already
    knows exactly which files it produced pass that list in directly — still an
    allowlist, just the right one for that tree.

    Callers must assert a denominator on the result. ``files_scanned`` of zero
    is a vacuous pass, not a clean one.
    """
    findings: list[dict[str, str]] = []
    docx_members = 0
    image_metadata_fields = 0
    video_metadata_strings = 0
    archive_members = 0
    total_bytes = 0

    # Symlinks are swept separately from the content walk. A symlink is an
    # exfiltration vector — git stores a few bytes of link text, and
    # `ln -s ../../_ADMIN/private.md innocent.md` ships private content to
    # everyone who clones. The content walk cannot carry this check because it
    # filters on `is_file()`, which is False for a broken link.
    #
    # Permitted is narrow and *checked*, never named: a link whose target
    # resolves inside the scan root. That covers CLAUDE.md and GEMINI.md ->
    # AGENTS.md without exempting them by filename, so any future symlink
    # pointing elsewhere is still a finding.
    links_checked = 0
    for link in links or []:
        links_checked += 1
        label = str(link.relative_to(scan_root))
        try:
            target = link.resolve(strict=True)
        except (OSError, RuntimeError):
            findings.append({"path": label, "rule": "broken-symlink"})
            continue
        try:
            target.relative_to(scan_root.resolve())
        except ValueError:
            findings.append({"path": label, "rule": "escaping-symlink"})
    digests: dict[str, str] = {}
    for path in files:
        relative = str(path.relative_to(scan_root))
        total_bytes += path.stat().st_size
        digests[relative] = sha256(path)
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            findings.append({"path": relative, "rule": "forbidden-file-type"})
        if path.stat().st_size > 10_000_000:
            findings.append({"path": relative, "rule": "file-over-10mb"})
        suffix = path.suffix.casefold()
        if suffix in TEXT_SUFFIXES:
            inspect_text(relative, path.read_text(encoding="utf-8", errors="replace"), findings)
        elif suffix == ".docx":
            docx_members += inspect_docx(path, scan_root, findings)
        elif suffix in {".gif", ".jpeg", ".jpg", ".png"}:
            image_metadata_fields += inspect_image(path, scan_root, findings)
        elif suffix == ".mp4":
            video_metadata_strings += inspect_video(path, scan_root, findings)
        elif suffix == ".zip":
            archive_members += inspect_zip(path, scan_root, findings)

    report = {
        "schema_version": "1.0",
        "status": "PASS" if not findings else "FAIL",
        "rules_applied": [
            "machine-specific-path",
            "private-product-name",
            "private-entity-name",
            "possible-secret",
            "unexpected-email-address",
            "possible-patient-identifier",
            "unsupported-regulated-claim",
            "forbidden-file-type",
            "escaping-symlink",
            "broken-symlink",
            "file-over-10mb",
            "embedded-docx-object",
            "image-metadata",
            "video-printable-metadata",
            "archive-path-and-content",
        ],
        "exceptions": [
            "Public safety warnings are allowed when they negate restricted-data or regulated-use claims.",
            "Synthetic identifier prefix SYN- is allowed.",
            "The selected GitHub no-reply identity is allowed.",
        ],
        "files_scanned": len(files),
        "bytes_scanned": total_bytes,
        "docx_members_scanned": docx_members,
        "image_metadata_fields_scanned": image_metadata_fields,
        "video_metadata_strings_scanned": video_metadata_strings,
        "archive_members_scanned": archive_members,
        "finding_count": len(findings),
        "findings": findings,
        "file_digests": digests,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if findings:
        print(f"FAILED: {len(findings)} public-release finding(s) across {len(files)} files")
        for finding in findings:
            print(f"- {finding['rule']}: {finding['path']}")
        return 1
    print(
        "PASS: public-release scan checked "
        f"{len(files)} files, {docx_members} DOCX members, and "
        f"{image_metadata_fields} image metadata fields, "
        f"{video_metadata_strings} video metadata strings, "
        f"{archive_members} archive members, and "
        f"{links_checked} symlink(s); 0 findings"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Do not apply repository-only ignored-directory rules.",
    )
    args = parser.parse_args()
    scan_root = args.root.resolve()
    report_path = args.report.resolve()
    ignored = set() if args.include_all else IGNORED_PARTS
    return scan_tree(scan_root, report_path, ignored)


if __name__ == "__main__":
    raise SystemExit(main())
