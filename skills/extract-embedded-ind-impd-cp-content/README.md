# Embedded IND/IMPD Clinical Pharmacology Inventory

Portable skill for locating mechanism/ADME disclosures in an IND and Module-4/5-
shaped summaries in an IMPD. It inventories presence and locators for qualified
reviewers; it never decides adequacy, filing readiness, approval, or dose.

## Included

- `SKILL.md` — workflow and human-only boundary.
- `scripts/check_ind_impd_content.py` — deterministic presence inventory.
- `assets/IND-IMPD-CP-Inventory.template.md` — draft review register.
- `references/` — source caveats, preflight, uncertainty, and review rules.

Run `python3 scripts/check_ind_impd_content.py --help`. Use the repository's
Markdown starter for a disclosed no-script route.
