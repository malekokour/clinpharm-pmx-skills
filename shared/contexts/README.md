# Contexts

A context is **not a skill.** The router never selects one. It attaches after a skill
has been chosen, from the work context, and changes *how* that skill runs.

## Why this class exists

The router returns exactly one skill. That has one consequence:

> **Skills cannot compose. Only contexts can.**

A question about population PK in a rare-disease antibody programme needs one workflow
and two dimensions of context. If modality and therapeutic area were skills they would
compete with the workflow for selection, the margin would be small, the router would
ask every time, and the answer would still arrive without its context.

As contexts they leave the ranking entirely, and one file improves every skill that
loads it. Six modality contexts across 149 skills is **10 files, not 894 packages.**

## How a skill uses one

A skill declares which context dimensions it is sensitive to. At run time,
`build-work-context` establishes the programme's modality, therapeutic area,
population and region, and the matching files load alongside the skill body.

A skill must still be correct with **no** context attached. A context sharpens an
answer; it is never load-bearing for safety, and it never relaxes a refusal.

## What belongs in a context

| Belongs | Does not belong |
|---|---|
| What this dimension changes about interpretation | A procedure — that is a skill |
| Parameters and behaviours that differ from the default | General background — that is a shared reference |
| Regulatory expectations specific to this dimension | A decision — that stays with the human |
| Where the usual assumption breaks | Anything that would fire on its own |

## Layout

```
contexts/
├── modality/            what the molecule is
└── therapeutic-area/    what the disease demands
```

Population and region dimensions are planned; they are not in this release. The
trigger for adding them is a measured gap, not symmetry.

## Boundary

A context is guidance, not authority. It carries `refuse_tags: [not-selectable]` in the
registry so a request cannot activate one directly. Asking about a context resolves to
the file; it does not run anything.
