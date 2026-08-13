# Changelog

All notable changes to ClinPharm PMx Skills are documented here.

## [Unreleased]

## [1.0.0] - 2026-08-13

First GitHub Release of this repository.

### Added

- **151 skill packages** (133 clinical pharmacology · 16 pharmacometrics · 2
  utilities). **151 `released`, 0 `built`.** `released` means the assigned
  evidence gate passed; it is not a clinical-validation claim.
- **The job map** — 167 task pages under [`map/`](map/), generated from
  `catalog/job-model-167.tsv`. 53 tasks are carried by a skill today; 114 are
  not.
- Deterministic checkers with unit tests against cited sources, vendored into
  the packages that use them so each ZIP installs standalone.
- Two-axis organisation — artifact kind × domain collection — joined by
  `catalog/catalog.json`. The collections are the source of record; the catalog
  is a derived view, and CI fails when they disagree.
- Zero-install `PASTE.md` per package, a static tracking-free site, and
  portable quality, privacy, benchmark-digest, and release checks.
- Public contribution, support, security, and governance documentation.
- [`plugin.json`](plugin.json) ([Agent Plugins 1.0.0](https://agent-plugins.org/))
  and [`.claude-plugin/`](.claude-plugin/) for Claude Code. How to use on
  Claude, ChatGPT / Codex, Cursor, and Antigravity: [`docs/HOSTS.md`](docs/HOSTS.md).

### Changed

- The privacy boundary is **structural**: the Git root is a subdirectory of
  the working tree, so private material is a sibling of the repository rather
  than a child of it. No ignore rule is load-bearing for privacy.
- Enumeration is **allowlist-based** (`scripts/public_surface.py`), never a
  filesystem walk filtered by a denylist.
- Repository validation is **discovery-based** over `skills/*/SKILL.md` rather
  than hard-coded to a single package.
- The product name is **ClinPharm PMx Skills** — the repository name,
  title-cased. The earlier brand "ClinPharm AI" is retired.
- Attach-first `starter/` files are archived under `docs/archive/starter/`.
  Zero-install is each package's `PASTE.md`.
- Public tree notes live in [`docs/PUBLIC-TREE.md`](docs/PUBLIC-TREE.md).

### Note on version numbering

A `0.1.0` was released on 2026-07-30 under this project's predecessor, which had
a different name, a single skill, and a repository that no longer exists. That
history is preserved privately and is deliberately not carried forward here.
This repository's first public tag is **v1.0.0**.
