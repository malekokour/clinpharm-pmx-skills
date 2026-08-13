# Structure Benefit-Risk Effects Table

Portable skill for transcribing already-computed effects into a traceable Markdown
table. It preserves sources, estimates, uncertainty, and locators; it does not
conclude whether benefits outweigh risks.

## Included

- `SKILL.md` — installed workflow and safety boundary.
- `scripts/validate_effects_table.py` — structural row validation only.
- `assets/Effects-Table.template.md` — copyable output template.
- `references/` — vendored preflight, evidence, human-review, and output-state rules.

Run `python3 scripts/validate_effects_table.py --help` for the optional validator.
Use the Markdown starter for a degraded no-script route.
