# Contributing to ClinPharm PMx Skills

Thank you for helping build portable, high-trust Agent Skills for
pharmaceutical work.

## Before contributing

1. Use only public, synthetic, or explicitly redistributable material.
2. Remove company, compound, study, patient, employee, and system identifiers.
3. Do not adapt an employer's internal template, SOP, prompt, or confidential
   workflow.
4. Explain the human-review boundary.
5. Include realistic failure cases, not only a happy path.

## Proposing a new skill

Open a skill request with:

- the user and recurring job-to-be-done;
- what the skill adds beyond a prompt;
- inputs and outputs;
- safety and privacy boundaries;
- one synthetic example;
- objective acceptance checks; and
- related public projects the skill should complement rather than duplicate.

Do not create a folder for a roadmap-only skill. Add the skill only when there
is a working `SKILL.md`, example, and validation path.

## Skill requirements

Every contributed skill must:

- follow the open Agent Skills specification;
- use a lowercase, hyphenated directory and matching `name` field;
- explain what it does and when it should trigger in `description`;
- keep the main `SKILL.md` focused and use progressive disclosure;
- declare external tools, packages, or network requirements;
- default to prepare-only behavior for external communications;
- preserve facts, assumptions, unknowns, and sources distinctly;
- provide at least three behavioral fixtures; and
- use the MIT License.

## Development checks

From the repository root:

```bash
python3 scripts/check_all.py
```

To rebuild generated documents, run `make docs`, then rerun the full check.
Use `skills-ref validate ./skills/<skill-name>` when available; the repository
also carries a self-contained specification check for offline use.

## Pull requests

Describe:

- the problem solved;
- the public/synthetic evidence used;
- files and interfaces changed;
- validation performed;
- known limitations; and
- whether the change affects generated DOCX files.

Never weaken a safety boundary merely to make a test pass.

## Community standard

Participation is governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
Security or accidental-exposure reports must follow [`SECURITY.md`](SECURITY.md)
rather than a public issue.
