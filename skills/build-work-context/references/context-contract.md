# ClinPharm PMx Skills context contract

Schema version: `1.0`

Use these headings and field meanings so a context file can be updated
reliably across AI hosts.

## Professional context

```markdown
---
clinpharm_context_schema: "1.0"
document_type: professional-context
version: "1.0"
updated_at: "YYYY-MM-DD"
status: draft | confirmed
owner_label: "<user-selected label or unknown>"
data_classification: PUBLIC_OR_SYNTHETIC | INTERNAL_APPROVED | RESTRICTED_DO_NOT_PROCESS | UNKNOWN
approved_environment: "<confirmed environment or unknown>"
review_due: "YYYY-MM-DD or unknown"
---

# My Pharma Work Context

## How to use this file
## Safety Kernel
### Data boundary
### Permitted tools and actions
### Human review and approval gates
### Stop conditions

## Professional Constitution
### Professional scope
### Responsibilities and outcomes
### Decision rights and escalation
### Recurring workflows and deliverables
### Terminology and definitions
### Source and evidence hierarchy
### Quality expectations
### Tools and constraints
### Output and communication preferences

## Active project index
## Known unknowns and conflicts
## Maintenance
### Review triggers
### Change history
```

Rules:

- Use `unknown` rather than an inferred value.
- Blank templates default to `UNKNOWN`; only a confirmed synthetic example may
  default to `PUBLIC_OR_SYNTHETIC`.
- Keep project detail in a project capsule; the index contains only safe names,
  status, and capsule references.
- Put mutable facts with an effective date when known.
- Include the data boundary in every exported derivative.

## Project capsule

```markdown
---
clinpharm_context_schema: "1.0"
document_type: project-capsule
project_slug: "<lowercase-safe-slug>"
version: "1.0"
updated_at: "YYYY-MM-DD"
status: proposed | active | on-hold | completed | unknown
data_classification: PUBLIC_OR_SYNTHETIC | INTERNAL_APPROVED | RESTRICTED_DO_NOT_PROCESS | UNKNOWN
---

# Project Context: <Project>

## How to use this capsule
## Purpose and current status
## Deliverables and success criteria
## Stakeholders and required reviewers
## Source manifest and authority order
## Decisions already made
## Constraints and non-goals
## Risks and contradictions
## Open questions
## Next action and review point
```

## Working pack

```markdown
---
clinpharm_context_schema: "1.0"
document_type: ai-working-pack
project_slug: "<project-slug>"
generated_from:
  professional_context_version: "<version>"
  project_capsule_version: "<version>"
generated_at: "YYYY-MM-DD"
data_classification: PUBLIC_OR_SYNTHETIC | INTERNAL_APPROVED | RESTRICTED_DO_NOT_PROCESS | UNKNOWN
---

# AI Working Pack: <Project>

## How to use this file
## Task for this session
## Safety Kernel
## Relevant Professional Constitution
## Project Capsule
## Required output
## Sources and authority
## Unknowns, conflicts, and assumptions
## Human review before external use
```

## Change summary

```markdown
---
clinpharm_context_schema: "1.0"
document_type: context-change-summary
previous_version: "<version>"
new_version: "<version>"
updated_at: "YYYY-MM-DD"
---

# Context Change Summary

## Why this update was requested
## Added
## Updated
## Removed
## Conflicts requiring confirmation
## Stale items
## Unchanged critical controls
## Source and user confirmations
## Next review
```

## Version behavior

- Increment the minor version for confirmed additions or corrections.
- Increment the major version when the role, function, or Safety Kernel changes
  materially.
- Do not increment for a REFRESH report that makes no accepted change.
- Record the previous version and reason in the embedded change history.

## Filenames

- `My-Pharma-Work-Context.md`
- `Project-Context-<project-slug>.md`
- `AI-Working-Pack-<project-slug>.md`
- `Context-Change-Summary.md`

If DOCX versions are created, use the same stem.
