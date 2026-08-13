# Library Router

Utility skill for **selecting** which ClinPharm PMx Skills skill to run inside a
whole-repo install.

## Status

`built` — advisory deterministic helper exists (`scripts/library_router.py` in
the repository root). Full selection evaluation suite and measured top-1
accuracy are not yet complete (`evidence_gap`).

## What it does

- Classifies requests: SIMPLE / SINGLE / AMBIGUOUS / MULTI
- Narrows by job-tree `nav_path`, then picks top-1 or asks / refuses
- Honours safe preferences from repo `scripts/settings.example.json`

## What it does not do

- Multi-agent swarms or silent skill chaining
- Clinical, regulatory, or dose decisions
- Bypass of human-only / OOS / safety refuses

## Install route

**Whole-repo primary.** This skill expects the ClinPharm PMx Skills repository (catalog,
settings, sibling skills). Do not claim ZIP-standalone routing until that route is
tested with vendored registry material.

## Deterministic helper (from repo root)

```bash
python3 scripts/library_router.py "review csr pk consistency"
```

Advisory only — the host still activates the chosen skill.

## Related (repo paths; whole-repo install)

- `ROADMAP.md`
- `catalog/nav_registry.json`
- `REFERENCES.md`
- `scripts/settings.example.json`
