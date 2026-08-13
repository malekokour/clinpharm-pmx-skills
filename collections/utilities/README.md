# Utilities

Optional cross-collection tools. **Not a scientific collection.**

A utility helps a professional establish reusable working context before a task
begins. It never performs the task, and no workflow skill may require one — every
skill in every collection must work correctly when no utility output exists.

This directory is a catalog and holds no implementation. Released packages live
at `skills/<skill-id>/`.

## What is released

| Skill | Visible title | What it produces |
|---|---|---|
| [`build-work-context`](../../skills/build-work-context/) | Pharma Work Context | A professional context file, a project capsule, an AI working pack, and a change summary |

Operating modes: `CREATE` · `UPDATE` · `PROJECT` · `REFRESH` · `EXPORT`.

## A note on this identifier

This skill was previously `pharma-context-builder`. The trailing `builder` suffix
is banned by the library's naming grammar, and was retained only because it was
the single published identifier the project had.

Deleting the prior repository and its release removed that obligation entirely,
so the exception was closed rather than carried forward. The skill is now
`build-work-context`, consistent with every other package.

## Relationship to workflow skills

```text
Utility
    captures role, permitted sources, constraints, approval rules
                         ↓ optional input
Workflow skill
    performs one bounded task using approved sources
                         ↓
Qualified human
    decides, corrects, approves, or rejects
```

When a context file is available, a workflow skill treats it as **bounded
evidence** about how the user works — never as authority that overrides the
current task, the supplied source documents, or the skill's own safety rules.
