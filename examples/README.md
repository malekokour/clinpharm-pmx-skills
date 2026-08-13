# Worked examples

**Start here if you want to see the library do something before deciding whether
to install it.**

Three examples, three different input shapes. Each ships its synthetic inputs
alongside it, states what comes back, and — the part that matters — states what
the skill **refuses** to do.

| Example | Input shape | Skill | What it catches |
|---|---|---|---|
| [`verify-nca-outputs/`](verify-nca-outputs/) | **Numeric / dataset** — an NCA report, its parameter dataset, the analysis plan, the exclusion log | [`verify-nca-outputs`](../skills/verify-nca-outputs/) | A reported `AUC` that disagrees with the dataset by 8%, a 1000-fold unit swap, an exclusion applied outside the plan, a "geometric mean" computed arithmetically |
| [`review-uspi-section-12/`](review-uspi-section-12/) | **Regulatory** — a draft US Prescribing Information, its sources, the content rules | [`review-uspi-section-12-content`](../skills/review-uspi-section-12-content/) | A protein-binding claim no source reports, an interaction stated in the wrong direction, a required subsection missing, a predictive qualifier over a population that was never evaluated |
| [`clinpharm-pmx/`](clinpharm-pmx/) | **Document / context** — a project brief, an analysis summary, a draft conclusion | [`build-work-context`](../skills/build-work-context/) | A draft conclusion that overreaches beyond the represented population, a stale clearance value, inconsistent confidence-interval wording |

## Everything here is synthetic

Every compound, study, subject identifier and value in these directories is
invented. `SYN-101`, `QLX-101`, `PX-101`, `Quilaxatan` — none of them exist.

This is not anonymised trial data. It is **synthetic by construction**, which is
a stronger guarantee: there is no real study behind it to re-identify. The same
rule binds any fixture contributed to this repository.

## Two ways to run any of them

**In an agent host.** Install the library, attach the files from that example's
`inputs/`, and use the prompt in its README.

**In a plain chat window, with no install.** Every package ships a generated
`PASTE.md`. Paste it into any chat, attach the same files, ask the same question.
That route exists because most clinical pharmacologists will never clone a
repository, and a library the majority of the field cannot open is not much of a
library.

## What the examples are actually demonstrating

Not that a model can read a document. That the workflow **states its findings
with locators and then stops**.

Each example's fixture carries deliberately planted defects, and the skill's job
is to surface them as findings a qualified professional then adjudicates. In
every case the refusal list includes some version of *"decide which of two
conflicting values is scientifically correct"* — because that decision belongs to
a pharmacokineticist, a regulatory lead, or a medical monitor, and the value of
the tool is that it does not pretend otherwise.

## The answer keys are not here, on purpose

Each fixture has an expert key enumerating its planted defects. Those live with
the evaluation suites under `evals/<skill>/fixtures/EXPERT-KEY.md`, **not in these
directories**. An example that ships its own answer key demonstrates nothing —
you could not tell whether the run found the defects or read the key.
