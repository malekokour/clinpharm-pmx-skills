# Awesome Pharma AI

A curated, honestly-annotated index of open resources for AI in pharmaceutical
R&D — including projects that compete with this one.

**Inclusion is not endorsement.** Each entry records what it covers, its licence,
and whether it ships evaluation artifacts, because those are the properties that
decide whether you can trust a skill you did not write.

Corrections and additions are welcome by pull request. Entries are re-checked at
each release; repository state is the shortest-lived claim in this file.

*Last verified: 2026-08-05.*

## Agent Skills — specification and reference

| Project | What it is | Licence | Evaluations |
|---|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | The open Agent Skills specification and validator | Open | Spec-level guidance |
| [anthropics/skills](https://github.com/anthropics/skills) | Reference implementations — document skills, progressive disclosure patterns | Open | Reference examples |

## Pharmaceutical and life-science skill collections

| Project | Coverage | Licence | Evaluations |
|---|---|---|---|
| [RConsortium/pharma-skills](https://github.com/RConsortium/pharma-skills) | Biostatistics, ADaM/SDTM, trial simulation, statistical review. **Zero clinical pharmacology coverage** | MIT | Design→development→evaluation→release lifecycle |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Broad scientific tooling — PK/PD, literature, scientific writing, clinical reports | Declared | Per-skill versions, repository meta-tests |
| **ClinPharm PMx Skills** (this project) | Clinical Pharmacology + Pharmacometrics + MIDD | MIT | Planted-defect fixtures with expert keys, published rubrics |

## Adjacent and specialist

| Project | Coverage | Caution |
|---|---|---|
| [trailofbits/skills](https://github.com/trailofbits/skills) | Security workflows grouped into plugins | Different domain; useful as a package-design reference |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Large community catalog with a generated discovery site | Scale requires machinery a focused library does not need |
| [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) | Prompt-injection, exfiltration and overlap scanning for skills | Best-effort detection; clean output is not proof a skill is safe |

## What to look for before trusting any pharmaceutical skill

1. **A declared licence.** Several pharma-adjacent skill repositories ship without one, which makes reuse legally ambiguous.
2. **Evaluation artifacts.** Fixtures, an expert key, a rubric, and published run results — not a claim of quality.
3. **An explicit human-review boundary.** What the skill refuses to decide matters more than what it does.
4. **Stated data boundaries.** Any skill inviting patient-level or sponsor-confidential material into a general AI service is a hazard regardless of output quality.
5. **A dated provenance trail.** Guidance references without issuing body, status and date will drift silently.

## Regulatory anchors commonly cited in this space

Verify each against the issuing body's own page before relying on it — secondary
compilations are frequently wrong about status and date.

- ICH E3 — structure and content of clinical study reports
- ICH M4E(R2) — CTD efficacy, including the five-part 2.7.2 structure
- ICH M10 — bioanalytical method validation
- ICH M12 — drug interaction studies
- ICH M15 — general principles for model-informed drug development
- 21 CFR 201.57(c)(13) — Clinical Pharmacology labelling content
