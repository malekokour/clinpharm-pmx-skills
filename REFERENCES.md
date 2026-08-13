# References — ClinPharm PMx Skills

Library-wide starting points. Individual skills still carry their own
`references/` for progressive disclosure.

## Agent Skills and setup

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Plugins 1.0.0](https://agent-plugins.org/)
- [Anthropic — Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude — Use skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenAI Codex — Build skills](https://developers.openai.com/codex/skills)

## Library design (selection at scale)

- Kim et al., *Towards a Science of Scaling Agent Systems*, arXiv:2512.08296  
  (Google Research, DeepMind, MIT, and co-authors). Use **qualitative** lessons
  on coordination and tool cost until numbers are verified against the paper.
- Li, *When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail*,
  arXiv:2601.04748 — skill-selection stress at library scale; hierarchical routing.

## Clinical pharmacology and pharmacometrics

Primary ICH / FDA / EMA and method sources are attached per skill and shared
reference as they freeze. This index grows as shared sources are promoted (three
or more consumers).

## Platform and hosting sources

Folded in from the former `docs/SOURCES.md` on 2026-08-11 so there is one home
for citations rather than two. Verified 2026-07-30 — recheck before quoting.

| Source | Why it matters |
|---|---|
| [GitHub repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) | Current repository and agent instruction surfaces |
| [GitHub repository transfers](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository) | Preservation and redirects if this repository later moves to an organisation |
| [R Consortium Pharma Skills](https://github.com/RConsortium/pharma-skills) | Adjacent task-specific pharmaceutical R&D skill collection |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Adjacent large scientific catalog and its security model |
| [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | Governs the static public site |
| [GitHub repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) | Branch and tag protection |
| [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) | Release-asset provenance |

This register supports product and compatibility decisions. It is not trademark
clearance, legal advice, or proof of behaviour in every host.

## Honesty

- `built` ≠ `released`. Counts always need a live denominator.  
- Skills review, reconcile, verify, structure, and flag — humans decide.  
- See [ROADMAP.md](ROADMAP.md) for Now / Next / Later / Not planned.
