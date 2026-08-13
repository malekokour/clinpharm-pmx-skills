# Workflows

A workflow is an **ordered list of skills and human gates** for work that spans more than
one skill. It is documentation. **Nothing here runs automatically.**

## Why they are documents and not automation

The router returns exactly one skill. When a request spans several — *"prepare the whole
CTD clinical pharmacology set"*, *"run the full first-in-human package"* — the correct
behaviour is to say which skills, in which order, with which decisions in between, and
then let a human drive.

That is a deliberate limit, and it rests on evidence rather than caution. Across the
published work on multi-agent scaling, chaining agents through sequential reasoning
tasks degraded performance in every configuration tested, often severely. Clinical
pharmacology review work is overwhelmingly sequential: each step's output is the next
step's input, and an error early is an error carried. **Auto-chaining these skills would
make the output worse, not faster.**

The second reason is accountability. Every workflow below contains at least one gate
where a qualified human decides something. An automated chain would run straight through
those gates, and the gate is the point.

## How to read one

| Element | Meaning |
|---|---|
| **Step** | One skill, invoked normally |
| **Gate** | A human decision. The chain stops here until it is made |
| **Carries forward** | What the next step needs from this one |
| **Common failure** | What goes wrong here in practice |

## When a workflow is the wrong answer

If the request is really one job with a broad name, the answer is a skill, not a
workflow. Workflows exist for genuine journeys, not for vague requests. The router
classifies before it offers: a request it can resolve to one skill gets that skill.

## The eight

| Workflow | Journey |
|---|---|
| [`population-pk-analysis`](population-pk-analysis.md) | Data through model to accepted deliverable |
| [`first-in-human-package`](first-in-human-package.md) | Nonclinical synthesis to a defensible starting dose and escalation |
| [`ctd-clinical-pharmacology-submission`](ctd-clinical-pharmacology-submission.md) | The 2.7.x set and its cross-document consistency |
| [`us-prescribing-information-set`](us-prescribing-information-set.md) | Sections 2, 7, 8 and 12 as one coherent story |
| [`study-delivery-lifecycle`](study-delivery-lifecycle.md) | Concept through conduct to CSR |
| [`ddi-programme`](ddi-programme.md) | In-vitro through clinical to management and label |
| [`organ-impairment-programme`](organ-impairment-programme.md) | Renal, hepatic and dialysis as one decision set |
| [`agency-meeting-cycle`](agency-meeting-cycle.md) | Strategy through briefing to minutes and commitments |

## Status

Several steps below name skills that are **planned rather than shipped**. That is stated
per step rather than hidden, because a workflow that silently assumes a package exists is
the same defect as a broken link.
