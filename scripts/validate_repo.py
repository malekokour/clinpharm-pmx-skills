#!/usr/bin/env python3
"""Validate the public ClinPharm PMx Skills repository contract.

Discovery-based: every released package under ``skills/*/SKILL.md`` is validated
by the same rules, and the collection catalogs under ``collections/*/collection.json``
are checked against what actually exists on disk.

``catalog/catalog.json`` joins the two axes (artifact kind x domain collection).
It is a derived view, not a second source of truth: every claim it makes is
re-derived from the collections and from disk, and any disagreement fails.

Enumeration policy (PS-D018)
----------------------------
The public surface is enumerated from ``git ls-files`` when a Git checkout is
available, and otherwise from an explicit **allowlist** of public roots. It is
never enumerated by a recursive filesystem walk filtered through a denylist.

A denylist fails silently on anything nobody thought to list. On 2026-08-04 that
defect made this gate read the private ``_ADMIN/`` control plane and fail on a
clean ``main``. For a repository whose premise is a privacy boundary, the
enumeration source *is* the boundary.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-04
Dependencies: Python standard library only — this gate must run from a clean
checkout with nothing installed.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import public_surface as _surface

ROOT = Path(__file__).resolve().parents[1]

#: This module deliberately imports nothing outside the standard library.
#: On 2026-08-06 it briefly imported `eval_schema`, which needs `strictyaml`,
#: and `make validate` began failing on any machine without the virtualenv.
#: CI installs requirements.lock, so CI stayed green while the guarantee in the
#: docstring above was false — a gate proving less than it claimed. Deep suite
#: validation lives in `scripts/eval_suite_check.py` (`make evals`), which is
#: allowed dependencies; what remains here is structural and regex-level.

ERRORS: list[str] = []

# --- public surface definition -------------------------------------------------

#: The public surface is defined once, in ``public_surface``. Importing rather
#: than restating it is what keeps this gate and the privacy scanner from
#: protecting subtly different sets of files.
PUBLIC_ROOTS = _surface.PUBLIC_ROOTS
PUBLIC_ROOT_FILES = _surface.PUBLIC_ROOT_FILES

#: Required regardless of which skills are released.
EXPECTED = [
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/workflows/quality.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/links.yml",
    ".github/workflows/pages.yml",
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "docs/PRIVACY.md",
    "docs/COMPATIBILITY.md",
    "site/index.html",
    "site/sitemap.xml",
]

FORBIDDEN_SUFFIXES = {".csv", ".xpt", ".sas7bdat", ".xlsx", ".env", ".pem", ".key"}
FORBIDDEN_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_-]{20,}\b"),
]
TEXT_SUFFIXES = {".cff", ".json", ".md", ".py", ".toml", ".xml", ".yaml", ".yml"}

#: 'released' means the package exists AND passed its qualification gate.
#: 'built' means the package exists and the gate has NOT been passed — a
#: distinction the vocabulary originally lacked, which forced a choice between
#: overclaiming and a red gate. Only 'released' and 'built' may have a directory;
#: only 'released' is offered to users as ready.
VALID_STATUSES = {"released", "built", "planned", "held", "deferred", "excluded"}

#: PS-D024 makes the collection entry the public source of a package's
#: qualification profile. The root catalog mirrors these fields; private
#: reviewer and dossier paths deliberately do not enter the public repository.
QUALIFICATION_PROFILES = {"LOW", "MEDIUM", "HIGH"}
QUALIFICATION_PROFILE_STATUSES = {"provisional", "assigned"}
QUALIFICATION_POLICY = "PS-D024-v1"
QUALIFICATION_FIELDS = (
    "qualification_profile",
    "qualification_profile_status",
    "qualification_policy",
)

#: Populated during catalog validation so the PASS line can state what is
#: actually released rather than counting every package on disk as released.
STATUS_TALLY: dict[str, int] = {}
DIRECTORY_ALLOWED = {"released", "built"}
SKILL_LINE_LIMIT = 500
MAX_FILE_BYTES = 10_000_000


def fail(message: str) -> None:
    ERRORS.append(message)


# --- enumeration ---------------------------------------------------------------


def _git(*args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, check=False
        )
    except (OSError, ValueError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.decode("utf-8")


def _git_tracked() -> list[Path] | None:
    """Return tracked files, or None when ROOT is not itself a Git checkout.

    ``git -C <dir>`` walks upward until it finds a repository. If this tree is
    merely nested inside an unrelated outer repository, that search succeeds and
    ``ls-files`` returns an empty list — which would enumerate zero public files
    and pass every check vacuously. Requiring the toplevel to equal ROOT is what
    makes the fallback trigger correctly instead.
    """
    toplevel = _git("rev-parse", "--show-toplevel")
    if toplevel is None:
        return None
    if Path(toplevel.strip()).resolve() != ROOT.resolve():
        return None
    output = _git("ls-files", "-z")
    if output is None:
        return None
    names = [n for n in output.split("\0") if n]

    # Untracked-but-not-ignored files count too.
    #
    # `ls-files` alone lists only *tracked* files, so a newly written document
    # was invisible to every check downstream of this function — including the
    # broken-link check. On 2026-08-14 `make check` passed locally over a broken
    # link in a new `VALIDATION.md` that CI then rejected on all four runners,
    # because CI always works from a committed tree.
    #
    # That is a false green at exactly the moment the check matters most: adding
    # a new file is the likeliest way to introduce a broken link. It was also
    # self-concealing — re-running the gate after the CI failure reproduced the
    # green, because the fix had by then been committed.
    #
    # `--others --exclude-standard` adds untracked files while still honouring
    # `.gitignore`, so build output and local scratch stay out. The local gate
    # now sees what CI will see, one commit earlier.
    others = _git("ls-files", "-z", "--others", "--exclude-standard")
    if others is not None:
        names.extend(n for n in others.split("\0") if n)

    return [ROOT / n for n in names]


def _allowlist_walk() -> list[Path]:
    """Enumerate the public surface without Git, using the shared allowlist."""
    return _surface.allowlist_walk(ROOT)


def public_files() -> list[Path]:
    tracked = _git_tracked()
    if tracked is not None:
        return [p for p in tracked if p.is_file()]
    return _allowlist_walk()


def check_enumeration_boundary(files: list[Path]) -> None:
    """No enumerated file may sit outside the declared public surface."""
    for path in files:
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            fail(f"enumerated file outside repository root: {path}")
            continue
        top = relative.parts[0]
        if len(relative.parts) == 1:
            if top not in PUBLIC_ROOT_FILES:
                fail(f"unexpected root-level public file: {relative}")
        elif top not in PUBLIC_ROOTS:
            fail(f"file outside the declared public surface: {relative}")


# --- skill discovery -----------------------------------------------------------


def discover_skills() -> list[Path]:
    base = ROOT / "skills"
    if not base.is_dir():
        return []
    return sorted(p.parent for p in base.glob("*/SKILL.md"))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


FRONTMATTER_ROOT_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


def check_frontmatter_shape(skill_id: str, text: str) -> None:
    """Catch misplaced metadata without adding a YAML runtime dependency.

    The complete YAML parse remains covered by the contract test.  This
    standard-library validator enforces the package's deliberately small
    frontmatter shape so a metadata field accidentally moved to the document
    root cannot be silently ignored by ``parse_frontmatter``.
    """
    if not text.startswith("---\n"):
        fail(f"{skill_id}: SKILL.md is missing opening YAML frontmatter delimiter")
        return
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{skill_id}: SKILL.md is missing closing YAML frontmatter delimiter")
        return

    active_root = ""
    for line_number, line in enumerate(parts[1].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("\t"):
            fail(f"{skill_id}: SKILL.md frontmatter line {line_number} uses a tab")
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            fail(f"{skill_id}: SKILL.md frontmatter line {line_number} is not a key/value pair")
            continue
        key = stripped.split(":", 1)[0].strip()
        if indent == 0:
            active_root = key
            if key not in FRONTMATTER_ROOT_KEYS:
                fail(
                    f"{skill_id}: SKILL.md frontmatter line {line_number} has "
                    f"unexpected root key '{key}'; package metadata must be nested under metadata"
                )
        elif active_root != "metadata" or indent != 2:
            fail(
                f"{skill_id}: SKILL.md frontmatter line {line_number} has invalid "
                "nesting; metadata fields must use exactly two spaces"
            )


#: Present on disk during development, deliberately outside the public surface.
#: Listed so the stray-entry check below reports genuine surprises only.
#: Local artifacts that exist on a working machine and must never be public.
#:
#: This is NOT ``PUBLIC_ROOTS``. The two sets answer different questions:
#: ``PUBLIC_ROOTS`` is *what ships*; this is *what is local, expected, and
#: acknowledged*. Listing something here declares it — it does not publish it,
#: and everything here is also gitignored.
#:
#: ``.claude-flow`` and ``.swarm`` were added 2026-08-13. Agent tooling writes
#: them relative to whatever directory it was invoked from, so they reappear in
#: the public root whenever a session or daemon runs with that cwd — three times
#: during this slice alone, each removal followed by another regeneration. The
#: undeclared-entry check was therefore failing on a directory that is gitignored,
#: untracked, and cannot reach a clone. Repeatedly deleting it is not a fix; the
#: honest fix is to declare a known local artifact as one.
KNOWN_NON_PUBLIC = {
    ".git",
    ".gitleaks-report.json",
    "_qa",
    "dist",
    ".venv",
    ".ruff_cache",
    "__pycache__",
    ".DS_Store",
    ".claude-flow",
    ".swarm",
}


def check_no_stray_root_entries() -> None:
    """Flag anything at the repository root that the allowlist does not cover.

    The allowlist makes unlisted files *invisible*, which is safe — they are
    never enumerated, so they cannot be published by these tools. But invisible
    is not the same as known, and silence here is dangerous in one specific way:
    a legitimate new public file that nobody added to the allowlist is skipped by
    both this validator and the privacy scanner, while still being perfectly
    committable by hand. It would reach a release having never been scanned.

    So the allowlist governs what is *read*, and this check reports what exists
    but is not covered. Enumeration stays closed; discovery stays loud.
    """
    for entry in sorted(ROOT.iterdir()):
        name = entry.name
        if name in KNOWN_NON_PUBLIC:
            continue
        if entry.is_dir():
            if name not in PUBLIC_ROOTS:
                fail(f"unlisted directory at repository root: {name}/ — add it to public_surface.PUBLIC_ROOTS or move it outside the repo")
        elif name not in PUBLIC_ROOT_FILES:
            fail(f"unlisted file at repository root: {name} — add it to public_surface.PUBLIC_ROOT_FILES or remove it")


#: Dot-directories that legitimately live inside the public tree.
ALLOWED_NESTED_DOT_DIRS = {
    ".github",
    ".githooks",
    ".claude-plugin",
    ".git",
    ".venv",
    ".ruff_cache",
}


def check_no_stray_dot_dirs() -> None:
    """Flag tool runtime state written *inside* the public tree, at any depth.

    ``check_no_stray_root_entries`` only inspects the repository root, which is
    where a stray dot-directory was first found on 2026-08-11 — agent tooling
    writing its runtime state there, caught loudly by the root allowlist.

    Hours later the same contamination reappeared several directories deep, under
    an eval folder, because the agent shell's working directory had moved into it.
    **The root check could not see it.** It surfaced only as an unexplained rise in
    the privacy scanner's file count — 879 to 911 — which is a number nobody would
    have questioned.

    The vendor is deliberately not named. Any tool that resolves its state
    directory relative to the working directory behaves this way, so naming one
    would imply the others are safe. What matters is the class, not the culprit.

    This is not cosmetic. Such state files have been observed carrying absolute
    paths that include the private container directory — material the public tree
    must never hold, whatever ``.gitignore`` says.

    The contamination lands wherever the working directory happens to be, so the
    check has to look wherever that could be. Depth-unbounded, allowlisted, and
    reported with a denominator.
    """
    checked = 0
    for name in sorted(PUBLIC_ROOTS):
        base = ROOT / name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_dir() or not path.name.startswith("."):
                continue
            checked += 1
            if path.name not in ALLOWED_NESTED_DOT_DIRS:
                fail(
                    f"stray dot-directory inside the public tree: "
                    f"{path.relative_to(ROOT)}/ — tool runtime state follows the "
                    "working directory. Move it out; do not add it to an allowlist"
                )
    print(f"PASS: no stray dot-directories in the public tree ({checked} inspected)")


def check_skills(skill_dirs: list[Path]) -> None:
    if not skill_dirs:
        fail("no released skill found: expected at least one skills/*/SKILL.md")
        return
    for directory in skill_dirs:
        skill_id = directory.name
        path = directory / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        check_frontmatter_shape(skill_id, text)
        frontmatter = parse_frontmatter(text)

        name = frontmatter.get("name")
        if name != skill_id:
            fail(f"{skill_id}: SKILL.md name '{name}' must equal its directory name")

        description = frontmatter.get("description", "")
        if len(description) < 80:
            fail(f"{skill_id}: SKILL.md description must state capability and trigger")
        if len(description) > 1024:
            fail(
                f"{skill_id}: SKILL.md description is {len(description)} characters; "
                "Agent Skills permits at most 1024"
            )
        if not re.search(r"(?i)\bUse (?:this skill|it|when)\b", description):
            fail(f"{skill_id}: SKILL.md description must state an activation condition")

        line_count = len(text.splitlines())
        if line_count > SKILL_LINE_LIMIT:
            fail(
                f"{skill_id}: SKILL.md is {line_count} lines, over the "
                f"{SKILL_LINE_LIMIT}-line progressive-disclosure limit"
            )

        if "RESTRICTED_DO_NOT_PROCESS" not in text:
            fail(f"{skill_id}: SKILL.md is missing restricted-data stop behavior")

        if not (directory / "README.md").is_file():
            fail(f"{skill_id}: package is missing README.md")

        for optional in ("references", "assets", "scripts"):
            candidate = directory / optional
            if candidate.is_dir() and not any(candidate.iterdir()):
                fail(f"{skill_id}: optional directory '{optional}/' exists but is empty")

        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1)
            if "://" in target or target.startswith("#"):
                continue
            if not (directory / target.split("#", 1)[0]).exists():
                fail(f"{skill_id}: broken SKILL.md link: {target}")


# --- catalog consistency -------------------------------------------------------


def load_collections() -> dict[str, dict]:
    base = ROOT / "collections"
    catalogs: dict[str, dict] = {}
    if not base.is_dir():
        return catalogs
    for path in sorted(base.glob("*/collection.json")):
        try:
            catalogs[path.parent.name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid collection catalog {path.parent.name}: {exc}")
    return catalogs


def check_catalog(catalogs: dict[str, dict], skill_dirs: list[Path]) -> None:
    if not catalogs:
        fail("no collection catalog found: expected collections/*/collection.json")
        return

    on_disk = {d.name for d in skill_dirs}
    declared_released: dict[str, str] = {}
    STATUS_TALLY.clear()
    seen_ids: dict[str, str] = {}

    for directory, catalog in catalogs.items():
        if not (ROOT / "collections" / directory / "README.md").is_file():
            fail(f"collection {directory}: missing README.md")
        if catalog.get("collection") != directory:
            fail(
                f"collection {directory}: 'collection' field is "
                f"'{catalog.get('collection')}' but the directory is '{directory}'"
            )
        for entry in catalog.get("skills", []):
            skill_id = entry.get("id")
            status = entry.get("status")
            if not skill_id:
                fail(f"collection {directory}: catalog entry without an id")
                continue
            if status not in VALID_STATUSES:
                fail(f"{skill_id}: invalid catalog status '{status}'")
            if skill_id in seen_ids:
                fail(
                    f"{skill_id}: appears in two collections "
                    f"({seen_ids[skill_id]} and {directory}); a skill has exactly "
                    "one primary collection"
                )
            else:
                seen_ids[skill_id] = directory
            STATUS_TALLY[status] = STATUS_TALLY.get(status, 0) + 1
            if status in DIRECTORY_ALLOWED:
                declared_released[skill_id] = directory
                profile = entry.get("qualification_profile")
                profile_status = entry.get("qualification_profile_status")
                policy = entry.get("qualification_policy")
                if profile not in QUALIFICATION_PROFILES:
                    fail(
                        f"{skill_id}: qualification_profile must be one of "
                        f"{sorted(QUALIFICATION_PROFILES)}; found {profile!r}"
                    )
                if profile_status not in QUALIFICATION_PROFILE_STATUSES:
                    fail(
                        f"{skill_id}: qualification_profile_status must be one of "
                        f"{sorted(QUALIFICATION_PROFILE_STATUSES)}; found {profile_status!r}"
                    )
                if policy != QUALIFICATION_POLICY:
                    fail(
                        f"{skill_id}: qualification_policy must be "
                        f"{QUALIFICATION_POLICY!r}; found {policy!r}"
                    )
                if status == "released" and profile_status != "assigned":
                    fail(
                        f"{skill_id}: released but qualification profile is not "
                        "assigned — a provisional risk classification cannot support release"
                    )
                if status == "built" and not entry.get("evidence_gap"):
                    fail(f"{skill_id}: status 'built' requires an 'evidence_gap' "
                         f"stating what is missing before it can be released")
                # The converse, which was missing: a `released` package may not
                # keep an `evidence_gap`. The gap states what evidence is
                # absent; if it is still there, the gate did not pass.
                #
                # Found by a canary on 2026-08-06 that re-promoted
                # review-csr-pk-consistency without removing its gap and was
                # accepted. Promotion is exactly where this must not be
                # possible, because a package can be flipped to `released` in
                # one edit while the record of what it lacks stays put.
                if status == "released" and entry.get("evidence_gap"):
                    fail(f"{skill_id}: status 'released' but an 'evidence_gap' "
                         f"remains — the gate cannot have passed while the "
                         f"record still states what evidence is missing")
            elif skill_id in on_disk:
                fail(
                    f"{skill_id}: status is '{status}' but a package exists at "
                    f"skills/{skill_id}/ — only released candidates get a directory"
                )
            if status in {"held", "deferred"} and not (
                entry.get("hold_reason") or entry.get("defer_reason")
            ):
                fail(f"{skill_id}: status '{status}' requires a stated reason")

    for skill_id in sorted(declared_released):
        if skill_id not in on_disk:
            fail(
                f"{skill_id}: catalogued as released but no package exists at "
                f"skills/{skill_id}/"
            )
    for skill_id in sorted(on_disk):
        if skill_id not in declared_released:
            fail(
                f"{skill_id}: package exists but no collection catalogues it as "
                "released — orphan package"
            )


# --- remaining public checks ---------------------------------------------------


def check_root_catalog(catalogs: dict[str, dict], skill_dirs: list[Path]) -> None:
    """Validate ``catalog/catalog.json`` as a derived view, never as a second truth.

    The root catalog joins the two axes — artifact kind and domain collection —
    and is generated from ``collections/*/collection.json`` by
    ``scripts/build_catalog_json.py``.

    Every claim it makes is therefore re-derived here and compared. The
    collections remain the source of record; a disagreement always fails rather
    than being reconciled in favour of the catalog.
    """
    path = ROOT / "catalog" / "catalog.json"
    if not path.is_file():
        fail("missing catalog/catalog.json")
        return
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid catalog/catalog.json: {exc}")
        return

    artifacts = catalog.get("artifacts")
    if not isinstance(artifacts, list):
        fail("catalog/catalog.json: 'artifacts' must be a list")
        return

    # Re-derive status from the collections rather than trusting the catalog.
    declared: dict[str, str] = {}
    declared_qualification: dict[str, dict[str, object]] = {}
    for collection in catalogs.values():
        for entry in collection.get("skills", []):
            ident = entry.get("id")
            if ident:
                declared[ident] = entry.get("status", "")
                declared_qualification[ident] = {
                    field: entry.get(field) for field in QUALIFICATION_FIELDS
                }
    if not declared:
        # A cross-check with an empty right-hand side passes vacuously and is
        # indistinguishable from a check that ran. Fail loudly instead.
        fail("catalog/catalog.json: no statuses derivable from collections — cross-check would be vacuous")

    on_disk = {d.name for d in skill_dirs}
    seen: set[str] = set()
    tally: dict[str, int] = {}

    for artifact in artifacts:
        ident = artifact.get("id")
        if not ident:
            fail("catalog/catalog.json: artifact missing 'id'")
            continue
        if ident in seen:
            fail(f"catalog/catalog.json: duplicate artifact id '{ident}'")
        seen.add(ident)

        status = artifact.get("status", "")
        tally[status] = tally.get(status, 0) + 1
        if status not in VALID_STATUSES:
            fail(f"catalog/catalog.json: '{ident}' has unknown status '{status}'")

        # 'built' means the package exists but the evaluation gate has NOT passed.
        # Without a stated gap the status silently reads as 'done' to a browser.
        if status == "built" and not artifact.get("evidence_gap"):
            fail(f"catalog/catalog.json: '{ident}' is 'built' but declares no evidence_gap")

        if status in DIRECTORY_ALLOWED and ident not in on_disk:
            fail(f"catalog/catalog.json: '{ident}' is '{status}' but no package on disk")

        # The collections are the source of record for status. This is the
        # invariant that stops a package being promoted to 'released' in the
        # browsable index without passing the gate that word claims.
        if ident not in declared:
            fail(f"catalog/catalog.json: '{ident}' appears in no collection")
        elif declared[ident] != status:
            fail(
                f"catalog/catalog.json: '{ident}' says '{status}' but its "
                f"collection says '{declared[ident]}'"
            )

        if ident in declared_qualification:
            for field, expected_value in declared_qualification[ident].items():
                actual_value = artifact.get(field)
                if actual_value != expected_value:
                    fail(
                        f"catalog/catalog.json: '{ident}' has {field}={actual_value!r} "
                        f"but its collection says {expected_value!r}"
                    )

        rel = artifact.get("path")
        if rel and not (ROOT / rel).exists():
            fail(f"catalog/catalog.json: '{ident}' points at missing path '{rel}'")

        primary = artifact.get("primary_collection")
        if primary and primary not in catalogs:
            fail(f"catalog/catalog.json: '{ident}' names unknown collection '{primary}'")

    for name in sorted(on_disk - seen):
        fail(f"catalog/catalog.json: package '{name}' on disk is absent from the catalog")

    # A counts block that is not re-derived is decoration.
    counts = catalog.get("counts")
    if isinstance(counts, dict):
        expected = {k: v for k, v in tally.items() if v}
        expected["total"] = len(artifacts)
        if {k: v for k, v in counts.items() if v} != expected:
            fail(f"catalog/catalog.json: counts {counts} do not match artifacts {expected}")


def check_shipped_evidence_level(catalogs: dict[str, dict], skill_dirs: list[Path]) -> None:
    """A package's own ``evidence-level`` must match the catalog's.

    ``SKILL.md`` is the file that goes into the user's ZIP. The catalog does
    not. So when the two disagree, the claim a practitioner actually reads is
    the one this repository never checked.

    On 2026-08-06 all sixteen disagreed, and six disagreed in the direction that
    matters: packages whose evaluation gate has never run shipped
    ``evidence-level: synthetic-benchmark``, asserting a benchmark that does not
    exist. Five different vocabularies were in use across the sixteen files —
    ``synthetic-benchmark``, ``synthetic-benchmark-pending-run``,
    ``not-yet-evaluated``, ``unevaluated-pending-fixture``, and one absent —
    against the catalog's three. Nothing compared them, so nothing objected.

    That is the same overclaim the ``built`` status exists to prevent, escaping
    into the shipped artifact through a field no gate read.
    """
    path = ROOT / "catalog" / "catalog.json"
    if not path.is_file():
        return  # check_root_catalog already reports the absence
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # likewise
    declared = {
        artifact.get("id"): artifact.get("evidence_level")
        for artifact in payload.get("artifacts", [])
    }
    pattern = re.compile(r"^\s*evidence-level:\s*(.+?)\s*$", re.MULTILINE)
    for directory in skill_dirs:
        skill_id = directory.name
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        match = pattern.search(text)
        if match is None:
            fail(
                f"{skill_id}: SKILL.md declares no evidence-level, so the package "
                "ships without the claim the catalog makes for it"
            )
            continue
        shipped = match.group(1).strip().strip('"')
        expected = declared.get(skill_id)
        if expected is None:
            fail(f"{skill_id}: no catalog artifact, so its evidence-level cannot be checked")
        elif shipped != expected:
            fail(
                f"{skill_id}: SKILL.md ships evidence-level '{shipped}' but the "
                f"catalog says '{expected}'. The shipped file is what a user reads"
            )


def check_expected() -> None:
    for relative in EXPECTED:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}")


def check_markdown_links(files: list[Path]) -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")) or not target:
                continue
            file_target = target.split("#", 1)[0]
            if not file_target:
                continue
            resolved = (path.parent / file_target).resolve()
            # A link that leaves the repository is worse than a broken one. It
            # resolves on the maintainer's machine — where `_ADMIN/` sits beside
            # `clinpharm-pmx-skills/` — and is dead for every person who clones the
            # repository, while naming a private path in a public file.
            #
            # `exists()` cannot catch this: on 2026-08-06 two suite READMEs
            # linked to `../../../_ADMIN/1-Docs/3-Decisions/...`, the target existed
            # locally, and this gate passed. An isolated copy without the
            # sibling directory is what exposed it, so the boundary is now
            # checked directly rather than inferred from existence.
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(
                    "Markdown link escapes the public repository: "
                    f"{path.relative_to(ROOT)} -> {raw_target}. It resolves only "
                    "where the private tree sits alongside this one"
                )
                continue
            if not resolved.exists():
                fail(
                    "broken local Markdown link: "
                    f"{path.relative_to(ROOT)} -> {raw_target}"
                )


def check_evals(catalogs: dict[str, dict], skill_dirs: list[Path]) -> None:
    """Every released skill needs its *own* eval suite.

    The suite has to belong to the skill. This check previously resolved a
    missing suite by falling back to the shared ``evals/evals.json`` — which
    belonged to ``build-work-context``. All sixteen packages therefore satisfied
    "has an eval suite", fourteen of them by borrowing an unrelated skill's
    cases, so a fully self-consistent promotion with no evaluation material
    validated clean.

    Structural only, and stdlib only. Whether a case file is *well formed* is a
    schema question answered by ``make evals``; whether a released package
    **owns** a suite at all is a contract question, and it is answered here so
    that it holds on a clean checkout with nothing installed.

    ``built`` packages are held to a weaker rule on purpose: they declare an
    ``evidence_gap`` saying the gate has not run, so an absent suite is the
    honest state. The requirement attaches to the claim.
    """
    declared_modes: dict[str, list[str]] = {}
    status_by_id: dict[str, str] = {}
    for catalog in catalogs.values():
        for entry in catalog.get("skills", []):
            skill_id = entry.get("id")
            if not skill_id:
                continue
            status_by_id[skill_id] = entry.get("status")
            declared_modes[skill_id] = entry.get("modes", [])

    owner_pattern = re.compile(r"^skill:\s*[\"\']?([A-Za-z0-9_-]+)", re.MULTILINE)
    mode_pattern = re.compile(r"^mode:\s*[\"\']?([A-Za-z0-9_-]+)", re.MULTILINE)

    for directory in skill_dirs:
        skill_id = directory.name
        released = status_by_id.get(skill_id) == "released"
        suite_dir = ROOT / "evals" / skill_id
        suite_path = suite_dir / "suite.yaml"
        if not suite_path.is_file():
            if released:
                fail(
                    f"{skill_id}: released but no eval suite exists at "
                    f"evals/{skill_id}/suite.yaml"
                )
            continue

        owner = owner_pattern.search(suite_path.read_text(encoding="utf-8"))
        if owner is None:
            fail(f"{skill_id}: evals/{skill_id}/suite.yaml declares no 'skill:'")
            continue
        if owner.group(1) != skill_id:
            fail(
                f"{skill_id}: evals/{skill_id}/suite.yaml declares skill "
                f"'{owner.group(1)}' — a suite must belong to its package"
            )
            continue

        for required in ("README.md", "rubric.md"):
            if not (suite_dir / required).is_file():
                fail(f"{skill_id}: eval suite is missing {required}")

        # A released package must ship a readable synthetic example, and the
        # fixture IS that example — it is the thing a practitioner can open to
        # see what the skill consumes and what it is expected to catch.
        #
        # Enforced for `released` only, and not because `built` packages do not
        # need one. Each qualification packet (P05-P18) builds its package's
        # fixture and expert key as part of earning the status, so requiring it
        # here would demand the work twice and, worse, invite synthetic clinical
        # content written to satisfy a gate rather than to test a skill.
        #
        # The `released` guard below was missing until 2026-08-06. The comment
        # above already said "enforced for `released` only"; the code did not
        # implement it, so the rule fired for every suite and printed
        # "released but ships no readable synthetic example" about packages
        # whose status is `built` — a message that was simply false. The bug
        # stayed latent while only two suites existed and surfaced the moment
        # fourteen more were added. A check whose message contradicts the
        # repository's own status vocabulary is worse than a missing check,
        # because it teaches a reader to distrust the status words.
        fixtures = sorted((suite_dir / "fixtures").glob("*")) if (suite_dir / "fixtures").is_dir() else []
        readable = [f for f in fixtures if f.is_file() and f.suffix.lower() in {".md", ".txt", ".csv"}]
        if released and not readable:
            fail(
                f"{skill_id}: released but ships no readable synthetic example — "
                f"expected fixtures under evals/{skill_id}/fixtures/"
            )
        # An expert key enumerates the planted defects a run is scored against
        # for what it MISSED. That is meaningful only where the suite asserts
        # defect detection. `build-work-context` is a context utility: its cases
        # assert behaviours (a conflict is preserved, a classification is
        # emitted), not detections, so demanding a key there would be demanding
        # a document with nothing to put in it.
        declares_defects = any(
            "defect:" in case.read_text(encoding="utf-8")
            for case in (suite_dir / "cases").glob("*.yaml")
        )
        # An expert key whose severities have not been adjudicated by a
        # practitioner may exist, and should — defect *presence* is a fact the
        # fixture author plants deliberately, and it can be authored, reviewed
        # and run against long before anyone rules on how bad each defect is.
        #
        # What it may not do is promote anything. B20 is the precedent: a
        # severity changed after outputs were inspected turned nine completed
        # runs into diagnostic evidence, because the Critical denominator that a
        # promotion gate turns on had moved. So a key must declare its own state,
        # and a `provisional` key blocks `released` outright.
        # `_`-prefixed files are provenance by this repository's naming convention —
        # a superseded key retained so a decision's history survives. Validating one
        # as a live key would demand that frozen history be edited, which is the
        # opposite of why it is kept.
        key_files = [
            f for f in fixtures
            if "EXPERT-KEY" in f.name.upper() and not f.name.startswith("_")
        ]
        for key_file in key_files:
            text = key_file.read_text(encoding="utf-8")
            match = re.search(r"^severity_status:\s*(\S+)", text, re.MULTILINE)
            if match is None:
                fail(
                    f"{skill_id}: {key_file.name} declares no 'severity_status:' — a key "
                    "must state whether its severities are 'provisional' or 'adjudicated', "
                    "because the Critical denominator a promotion gate turns on depends on it"
                )
            elif match.group(1) not in {"provisional", "adjudicated"}:
                fail(
                    f"{skill_id}: {key_file.name} has severity_status "
                    f"'{match.group(1)}'; expected 'provisional' or 'adjudicated'"
                )
            elif match.group(1) == "provisional" and released:
                fail(
                    f"{skill_id}: status 'released' but its expert key's severities are "
                    "still 'provisional' — no promotion may rest on a denominator that "
                    "has not been adjudicated"
                )

        if released and declares_defects and not any("EXPERT-KEY" in f.name.upper() for f in fixtures):
            fail(
                f"{skill_id}: released and its suite asserts defect detection, but "
                "its fixtures carry no expert key, so no run can be scored for "
                "what it missed"
            )

        case_paths = sorted((suite_dir / "cases").glob("*.yaml"))
        if len(case_paths) < 7:
            fail(
                f"{skill_id}: eval suite must include at least seven cases; "
                f"found {len(case_paths)}"
            )
        modes: set[str] = set()
        for case_path in case_paths:
            modes.update(mode_pattern.findall(case_path.read_text(encoding="utf-8")))
        for required_mode in declared_modes.get(skill_id, []):
            if required_mode not in modes:
                fail(f"{skill_id}: eval suite missing declared mode: {required_mode}")


def check_public_surface(files: list[Path]) -> None:
    for path in files:
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden public file type: {relative}")
        if path.stat().st_size > MAX_FILE_BYTES:
            fail(f"file exceeds 10 MB: {relative}")
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(text):
                    fail(f"possible secret in {relative}")


def check_template_defaults(skill_dirs: list[Path]) -> None:
    for directory in skill_dirs:
        for path in sorted((directory / "assets").glob("*.template.md")):
            text = path.read_text(encoding="utf-8")
            if (
                "data_classification:" in text
                and "data_classification: UNKNOWN" not in text
            ):
                fail(f"blank template must default to UNKNOWN: {path.relative_to(ROOT)}")


def check_action_pins() -> None:
    pattern = re.compile(r"^\s*(?:-\s+)?uses:\s+[^@\s]+@([^\s#]+)", re.MULTILINE)
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for reference in pattern.findall(text):
            if not re.fullmatch(r"[0-9a-f]{40}", reference):
                fail(
                    "GitHub Action must use a full commit SHA: "
                    f"{path.relative_to(ROOT)} -> {reference}"
                )


def check_docx(files: list[Path]) -> None:
    for path in files:
        if path.suffix.lower() != ".docx":
            continue
        try:
            with zipfile.ZipFile(path) as archive:
                if "word/document.xml" not in set(archive.namelist()):
                    fail(f"invalid DOCX: {path.relative_to(ROOT)}")
        except zipfile.BadZipFile:
            fail(f"corrupt DOCX: {path.relative_to(ROOT)}")


def main() -> int:
    files = public_files()
    source = "git ls-files" if _git_tracked() is not None else "public allowlist"
    skill_dirs = discover_skills()
    catalogs = load_collections()

    check_enumeration_boundary(files)
    check_no_stray_root_entries()
    check_no_stray_dot_dirs()
    check_expected()
    check_skills(skill_dirs)
    check_catalog(catalogs, skill_dirs)
    check_root_catalog(catalogs, skill_dirs)
    check_shipped_evidence_level(catalogs, skill_dirs)
    check_markdown_links(files)
    check_evals(catalogs, skill_dirs)
    check_public_surface(files)
    check_template_defaults(skill_dirs)
    check_action_pins()
    check_docx(files)

    if ERRORS:
        print(f"FAILED: {len(ERRORS)} repository contract error(s)")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    released = STATUS_TALLY.get("released", 0)
    built = STATUS_TALLY.get("built", 0)
    print(
        f"PASS: repository contract validated across {len(files)} public files "
        f"(enumerated from {source}); {len(skill_dirs)} package(s) on disk — "
        f"{released} released, {built} built-but-unqualified — "
        f"in {len(catalogs)} collection(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
