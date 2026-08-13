# Public tree — what is here, what is not, and why

This repository ships three layers. Every root folder belongs to one of them.
A folder without its first real artifact is not created.

**Source of record for published HTML map pages:** [`site/map/`](../site/map/).
**Source of record for citable Markdown task pages:** [`map/`](../map/).
Both are generated from [`catalog/job-model-167.tsv`](../catalog/job-model-167.tsv).
Do not hand-edit either view.

## Present — fifteen directory roots

| Path | Layer | What it is |
|---|---|---|
| `map/` | 1 | 167 Markdown task pages + `job-model.json` |
| `site/map/` | 1 | HTML rendering of the same ledger |
| `skills/` | 2 | 151 flat packages. Never nested |
| `contexts/` | 2 | Composable contexts (modality, therapeutic area). Promoted from `shared/` because a context is a product surface, not plumbing |
| `skills/library-router/` | 2 | Router skill. The executable is `scripts/library_router.py`; settings live at `scripts/settings.example.json`. Not a root `router/` |
| `docs/assets/`, `shared/assets/`, `site/assets/` | 2–3 | Assets live next to their consumer. No empty root `assets/` |
| `evals/` | 3 | Suites sit outside packages so an installed skill stays portable. Historical benchmark records live at `evals/benchmark/` |
| `shared/` | 2 | Modules, tools, contracts — vendored into packages |
| `collections/` | 2 | Status source of record |
| `catalog/` | 2 | Derived view. CI fails if it disagrees with collections |
| `examples/` | 2 | Worked synthetic examples |
| `docs/` · `scripts/` · `tests/` · `site/` | 3 | Documentation, gates, regression tests, static rendering |
| `.github/` · `.githooks/` | 3 | CI and authorship hook |
| `.claude-plugin/` | 3 | Claude Code marketplace (`plugin.json`, `marketplace.json`) |
| `plugin.json` | 3 | Agent Plugins 1.0.0 manifest (file at root, not a directory) |
| `CLAIM-LEDGER.md` | 3 | Regenerated public counts |

## Deliberately not at root

| Agreed name | Why it is absent |
|---|---|
| `.codex-plugin/`, `.cursor-plugin/`, `.agents/plugins/` | Codex, Cursor, Copilot, and Antigravity read the root [`plugin.json`](../plugin.json) plus `skills/`. A second empty adapter would be a false extra claim |
| Root `router/` | The router is `skills/library-router/` plus `scripts/library_router.py` |
| Root `assets/` | Assets already live under `docs/`, `shared/`, and `site/` |
| Root `config/` | One file. It lives at `scripts/settings.example.json` |
| Root `benchmark/` | Evaluation evidence. It lives at `evals/benchmark/` |
| `contexts/region/`, `contexts/population/` | No first artifact yet. Empty axes are not created |

GitHub Pages is enabled. The published site is
[malekokour.github.io/clinpharm-pmx-skills](https://malekokour.github.io/clinpharm-pmx-skills)
(source: `site/`). The Markdown map remains this repository under `map/`.

## Retired

`starter/` was the attach-first route from the single-skill era. Archived at
[`archive/starter/`](archive/starter/). Use `skills/<id>/PASTE.md`.

## Allowlist

New root directories must be added to `scripts/public_surface.py` `PUBLIC_ROOTS`
before they exist, or `validate_repo.py` fails with "unlisted directory at
repository root". Do not add a name to that set to make an empty folder pass.
