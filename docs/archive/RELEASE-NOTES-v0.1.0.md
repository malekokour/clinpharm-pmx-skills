# ClinPharm PMx Skills v0.1.0

> **Draft — this release has not been cut.** These notes describe what v0.1.0
> will contain when it is published. Until then, treat them as a plan, not a
> record.

Portable Agent Skills for clinical pharmacology document review. A skill checks
a Clinical Study Report, protocol, briefing document, or label section for
internal inconsistencies and reports what it found.

## What is in it

**Twenty-one packages. One is `released`, twenty are `built`.**

| Status | Count | Means |
|---|---:|---|
| `released` | 1 | The predecessor evaluation gate passed; K06 still owns reconciliation against the current PS-D024 policy |
| `built` | 20 | The package exists and validates. **Current qualification has not passed.** Each declares an `evidence_gap` naming what is missing |

Released: `build-work-context` (the context utility). The prior qualification
claim for `review-csr-pk-consistency` was retracted; that package is `built`
pending fresh qualification.

`built` exists because "done" would have been a lie. A package can validate,
install cleanly, and still miss the defects it was written to catch. Structural
validity is not evidence of detection — only a fixture with planted defects is.
See [GOVERNANCE.md](../../.github/GOVERNANCE.md).

Also included:

- deterministic checkers and shared tools with unit tests against cited sources;
- seventeen study-type modules and six shared review assets;
- an expert-keyed synthetic fixture for the hero — 12 planted defects across
  five Critical, four Major, three Minor, plus five documented false-positive traps;
- attach-first Word and Markdown starters;
- a static, tracking-free site and portable quality, privacy, and release checks.

## Install or use

Download a package ZIP and attach its Markdown or DOCX starter to an ordinary AI
chat. Skill-aware tools can install the ZIP directly. Each package vendors what
it needs, so it works standalone with no repository present.

## Evidence boundary

The CSR skill's deterministic **script path** was measured at recall 6/6 = 1.00
against its required threshold, with 0 of 5 false-positive traps triggered.
That narrow result is retained as diagnostic history, not qualification. The
twenty `built` packages have diagnostic suites, but none has a current accepted
qualification dossier.

The retained three-pair synthetic benchmark for the context utility found one
consistent difference: the Working Pack condition made source-authority
traceability explicit. That result is dated, task-specific, and does not
establish cross-model performance.

No performance claim here extends beyond what the recorded runs measured.

## Safety boundary

Every tool reports **mechanical findings** and states its denominator. None
recommends a dose. None issues a clinical conclusion. Reporting that two
documents disagree is not deciding which is right — a human reviewer does that.

Use only information permitted in your current AI environment. ClinPharm PMx Skills is
not medical advice, clinical decision support, a validated GxP system, or a
replacement for qualified scientific, medical, or regulatory judgment.
