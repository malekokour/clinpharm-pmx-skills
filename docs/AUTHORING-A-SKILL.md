# Authoring a skill

The method, published. If you want to extend this library — or build a different one on
the same discipline — this is what a package owes and how it earns its status.

Nothing here is proprietary. The reason it is public is that one person cannot author a
profession's worth of workflows, and a contribution path without a stated standard
produces contributions nobody can accept.

## First: is it a skill at all?

Run the **four boxes**. All four must fill.

| Box | The question |
|---|---|
| **Trigger** | What sentence does a practitioner actually say to invoke this? |
| **Input** | What document, dataset, or evidence pack goes in? |
| **Output** | What artifact comes out? |
| **Refuses** | What does it decline to decide? |

The shortcut that predicts the answer: **verb-object names pass, bare subject-matter
nouns fail.** *"Review the renal impairment study"* fills all four. *"Small molecule"*
fills none — it is a property of the compound that changes how twenty other skills
behave, which makes it a **context**.

If the boxes do not fill, the thing you have is one of these:

| It is | When |
|---|---|
| **Context** | It modifies how other skills run — modality, therapeutic area, population, region |
| **Shared reference** | It is criteria other skills read, with no journey of its own |
| **Policy** | It applies to every skill, always |
| **Script** | It is a deterministic check with no judgment |
| **Workflow** | It is several skills in order with human gates between them |
| **Boundary** | It is real work with no artifact a skill could prepare |

Record the four-box evidence. A classification without it is an opinion, and opinions
have already produced four different skill counts from the same 167 rows.

## Second: does it collide?

The `description` is the router's **entire** selection surface — roughly 100 tokens,
loaded for every skill at once. Before writing a body, write the description and compare
it against its neighbours.

Two descriptions that each cover a job the other also claims will collide, and the
collision is silent: the router returns one of them confidently. If your description
needs to describe two jobs, you have two skills.

## The package

```
skills/<id>/
├── SKILL.md          required — under 500 lines
├── README.md
├── references/       depth, loaded on demand
├── scripts/          only if genuinely needed; an empty folder is a defect
├── assets/           templates the skill produces or consumes
└── PASTE.md          generated — never hand-written
```

**Frontmatter:** `name` (matches the directory) · `description` (≤1024 chars, what it
does **and** when to use it) · `allowed-tools` (least privilege — declare what the
instructions actually use, nothing more) · `license` · `metadata`.

**Budgets, enforced in CI:** ≤10 declared tools or scripts · ≤500 body lines. Exceeding
the tool budget is a grain signal, not a performance one — a package reaching for many
tools is usually doing more than one job.

## The body owes these sections

| Section | Why |
|---|---|
| When to use / when **not** to use | The non-trigger is as load-bearing as the trigger |
| Required inputs | What the skill cannot proceed without |
| Procedure | Numbered, with entry and exit conditions per phase |
| Outputs | The artifact, its shape |
| When evidence is missing or conflicting | `NEEDS_INPUT` · `UNKNOWN` · `CANNOT_ASSESS` — never a confident guess |
| Documents are evidence, not instructions | Loaded from the untrusted-content policy |
| Human review | Which decisions are refused and who owns them |
| Never | The explicit refusals |
| Verification checklist | How a reviewer checks the skill did its job |

## The invariant

> Skills review, reconcile, verify, structure and flag.
> **Qualified humans decide, approve, sign off, submit and act.**

Every package carries this. A skill that concludes clinical significance, selects a
dose, or accepts a submission has crossed the only line this product does not move.

A **refuse-boundary skill** is the pattern for decision-adjacent work: assemble the
pack, lay out the options and what each rests on, surface what is missing, name the
accountable role — then decline to conclude. Roughly a dozen tasks work this way, and
they are skills, not gaps.

## Status: `built` versus `released`

| Status | Means |
|---|---|
| `built` | The package exists and validates. **The evaluation gate has not run** |
| `released` | The gate passed — recall and precision met threshold, no Critical missed |

`built` exists because "done" would have been a lie. A package enters the library at
`built` and is promoted only by a gate result, never by narrative.

## Evidence discipline

Every claim is labelled **Fact · Verified · Inference · Assumption · Unknown**, and
every completeness claim carries its denominator. *"Checked 212 files, 0 findings, here
is the command"* is evidence. *"No issues found"* is not — it is unfalsifiable, and this
project's dominant historical failure mode is a check that reported success over
something narrower than the claim.

**Prove a new gate works by making it fail.** Plant a known-bad input, confirm red,
remove it, confirm green. A gate nobody has seen fail is untested.

## Before you propose it

1. The four boxes fill, and the evidence is written down.
2. The description does not collide with a neighbour.
3. The package validates: `make check`.
4. The eval suite exists, even if the gate has not run.
5. The human boundary is explicit, and you can name what the skill refuses.

## What gets a contribution rejected

A skill that concludes where it should refuse · a description that describes two jobs ·
a completeness claim without a denominator · an empty `scripts/` directory · a
hand-edited generated file · a gate widened to accommodate a result.

That last one matters most. **A threshold lowered to make something pass is no longer a
threshold**, and the library's only real asset is that its green checks mean something.
