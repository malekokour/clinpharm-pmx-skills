# Investigator's Brochure PK Section Check

Portable skill for inventorying declared human PK/product-metabolism content in
an IB and reconciling its version/date with a supplied DSUR citation register.
It never approves medical content, makes a live-study decision, recommends a
dose, or determines a filing obligation.

## Included

- `SKILL.md` — workflow and human/live-study boundary.
- `scripts/check_ib_pk_section.py` — deterministic presence/version checker.
- `assets/IB-PK-Section-Check.template.md` — draft review register.
- `references/` — source caveats, preflight, uncertainty, and review rules.

Run `python3 scripts/check_ib_pk_section.py --help`. Use the repository's
Markdown starter for a disclosed no-script route.
