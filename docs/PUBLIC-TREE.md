# Public tree — what is here, what is not, and why

This repository ships three layers. Every root folder belongs to one of them.
A folder without its first real artifact is not created.

**Source of record for published HTML map pages:** [`site/map/`](../site/map/).
**Source of record for citable Markdown task pages:** [`map/`](../map/).
Both are generated from [`catalog/job-model-167.tsv`](../catalog/job-model-167.tsv).
Do not hand-edit either view.

## Present

| Path | Layer | What it is |
|---|---|---|
| `map/` | 1 | 167 Markdown task pages + `job-model.json` |
| `site/map/` | 1 | HTML rendering of the same ledger |
| `skills/` | 2 | 151 flat packages |
| `shared/contexts/` | 2 | Composable contexts (modality, therapeutic area). Not a root `contexts/` |
| `skills/library-router/` | 2 | Router skill. Not a root `router/` |
| `docs/assets/`, `shared/assets/`, `site/assets/` | 2–3 | Assets live next to their consumer. No empty root `assets/` |
| `evals/` | 3 | Suites sit outside packages so an installed skill stays portable |
| `CLAIM-LEDGER.md` | 3 | Regenerated public counts |

## Deferred until they have real content

| Agreed name | Why it is absent |
|---|---|
| `plugin.json` | Generated with host adapters. No lifecycle evidence yet (S04) |
| `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.agents/plugins/` | Host adapters. Shipping an empty adapter is a false "works with" claim |
| Root `contexts/` | Content already lives at `shared/contexts/`. A second home would split the source of record |
| Root `router/` | The router is `skills/library-router/` plus `scripts/library_router.py` |
| Root `assets/` | Assets already live under `docs/`, `shared/`, and `site/` |

GitHub Pages is **not** enabled. `malekokour.github.io/clinpharm-pmx-skills` is
not a published site. The map is this repository.

## Retired

`starter/` was the attach-first route from the single-skill era. Archived at
[`archive/starter/`](archive/starter/). Use `skills/<id>/PASTE.md`.

## Allowlist

New root directories must be added to `scripts/public_surface.py` `PUBLIC_ROOTS`
before they exist, or `validate_repo.py` fails with "unlisted directory at
repository root". Do not add a name to that set to make an empty folder pass.
