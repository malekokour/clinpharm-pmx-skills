# v0.2.0 — library router, claim ledger, four new packages

**26 packages: 1 `released`, 25 `built`.**

That ratio is the honest headline, and it has not improved since v0.1.0. Four new
packages were added and none of them is qualified, because the qualification path
is blocked on evidence that does not exist yet. This release makes the library
larger and its verification stronger; it does not make more of it *ready*.

## What `built` means here

The package exists, validates, installs cleanly, and ships an evaluation suite.
**Its evaluation gate has not been run.** Every `built` package carries a written
`evidence_gap` naming exactly what is missing.

The distinction is enforced by CI rather than by intention: `released` requires a
risk-tiered dossier under the qualification policy, and no package can acquire
the status by editing a file.

## New packages

| Package | What it reviews |
|---|---|
| `review-eu-smpc-cp-sections` | EU SmPC 4.2 / 4.5 / 5.2 and the quantitative statements in 4.4 — including cross-section consistency, which the US-label reviewer has no equivalent of |
| `review-adc-analyte-strategy` | ADC and multi-analyte definitions across documents, coverage against stated exposure questions, containment and unit consistency |
| `review-human-pk-prediction` | Allometric scaling, IVIVE and PBPK deliverables — assumption completeness, input provenance, qualification scope |
| `review-exposure-safety-margins` | Stated exposure safety margins — whether the basis is declared, the two sides are comparable, and the arithmetic reconciles |

`review-human-pk-prediction` opens the **pharmacometrics track**, which until now
was roadmap language with no artifact behind it.

None of the four decides anything. They report what is stated, what is missing,
and what contradicts what, with locators on both sides.

## New verification

Seven gates were added, and each was proven by watching it fail before it was
trusted.

| Gate | What it checks | Denominator |
|---|---|---|
| Router selection cases | Which package the router actually returns | 42 cases, 7 settings profiles |
| Router scale fixtures | That selection holds as the library grows | n = 26, 50, 100 |
| Nav registry field contract | Every field the router design needs resolves | 208 field checks |
| **Public claim ledger** | Every public count re-derived from its source | 9 stated counts |
| Static site gates | No trackers, no JavaScript, keyboard reachability | 21 tracker signatures |
| Lifecycle runbook | Every path and command the runbook names exists | 4/4 operations |
| Defect assertion shape | Eval assertions bind a value, not a description | 138 sides |

### Three defects these gates found in this repository

1. **An operator preference could bypass a safety refusal.** `force_skill` was
   evaluated before request classification, so a pinned skill turned "select a
   dose for this cohort" into a routed request — contradicting the router's own
   written contract. Classification now runs first.
2. **Routing degraded at scale.** Top-1 accuracy fell from 21/21 to 18/21 at 50
   packages, because common words like `review` and `report` carried the same
   weight as the discriminating ones. Scoring now weights terms by rarity;
   accuracy holds at 21/21 through 100 packages.
3. **The README's own counts were stale.** A sentence carrying that day's date
   stated five numbers that were already wrong. The claim ledger now fails the
   build when any public count disagrees with its source.

## Documentation

- **`../CLAIM-LEDGER.md`** — generated; every public number with its source of record.
- **`docs/LIFECYCLE.md`** — install, update, roll back, uninstall, for Claude and Codex. The Codex half is gated; the Claude UI half is marked `UNVERIFIED` against the current library, and the gate enforces that it keeps saying so.
- **`docs/COMPATIBILITY.md`** — scope note added. The Agent Skill verifications were obtained on 2026-07-30 against **one** package, and now read as covering 26. They do not.

## Still not true of this release

Stated plainly, because a release note is where an overclaim is easiest.

- **No skill's behaviour has been evaluated.** Every gate above is structural or
  deterministic. They prove the material is real and consistent; they prove
  nothing about how well a skill does its job.
- **25 of 26 packages are unqualified**, each with a written `evidence_gap`.
- **No performance claim of any kind** — no accuracy, no time saved, no multiplier.
- **The host lifecycle is documented, not demonstrated**, against the current library.
- **Not a validated GxP system**, not clinical decision support, not medical advice.

## Verification for this release

```
check_all.py   EXIT 0        unittest   EXIT 0 (211 tests)
gitleaks       no leaks found
trufflehog     0 verified secrets, 0 scan errors
privacy scan   0 findings
```

Run on an independent clean copy — no `.git`, no cached virtualenv, dependencies
installed fresh from `requirements.lock`.

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
cd clinpharm-pmx-skills && python3 scripts/check_all.py
```
