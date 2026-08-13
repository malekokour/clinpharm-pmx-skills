# Interoperability

ClinPharm PMx Skills is designed to precede task-specific skills.

## Pattern

```text
ClinPharm PMx Skills context builder
    → AI Working Pack
        → task-specific skill
            → human-reviewed deliverable
```

The working pack supplies:

- data and action boundaries;
- professional and project context;
- authority order;
- output requirements;
- unknowns and contradictions; and
- human-review gates.

The downstream skill supplies the specialized task workflow.

## Example

Before using a clinical-trial simulation or statistical-review skill:

1. create or refresh the professional context;
2. create the project capsule from permitted sources;
3. export a focused working pack;
4. attach or load the working pack with the task-specific skill;
5. require the downstream skill to cite its source inputs and retain unresolved
   conflicts; and
6. route the result to qualified human review.

## R Consortium Pharma Skills

[R Consortium Pharma Skills](https://github.com/RConsortium/pharma-skills)
provides task-specific pharmaceutical R&D skills such as trial simulation,
group-sequential design, ADaM workflows, and statistical review.

ClinPharm PMx Skills does not vendor, fork, or imply affiliation with that project.
Its distinctive responsibility is professional context, project boundaries,
and portable working packs.

## K-Dense Scientific Agent Skills

[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)
provides a large scientific skill catalog. Review every third-party skill,
dependency, network requirement, and data destination before use.

## Provider-specific files

Future adapters may create:

- `AGENTS.md`;
- `.github/copilot-instructions.md`;
- Claude project instructions; or
- other provider-specific context files.

Those adapters must be generated from the provider-neutral working pack and
must not become a second editable source of truth.
