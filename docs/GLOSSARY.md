# Glossary

One word per concept. Where the Agent Skills specification names a thing, we use its
word unchanged. Where the community has a convention, we follow it. Where neither
exists — the shared layer between skills — we pick the plainest word and record it here
before it appears in a path.

## Inside a skill directory — specification terms

| Term | Meaning |
|---|---|
| **Skill** | A directory containing `SKILL.md` plus optional resources. The product unit |
| `SKILL.md` | Required file: YAML frontmatter and a markdown body |
| `name` | Lowercase, hyphens, ≤64 characters, matches the directory name |
| `description` | ≤1024 characters. What it does **and** when to use it. This is the selection surface |
| `allowed-tools` | Space-separated list of pre-approved tools. Least privilege |
| `references/` | Documentation read on demand |
| `scripts/` | Executable code the skill runs |
| `assets/` | Templates and static resources |
| **Progressive disclosure** | Metadata always loaded (~100 tokens) → body on activation → resources only when needed |

## Around the skill — community terms

| Term | How we use it |
|---|---|
| **Tool** | A callable function exposed to a model — MCP or function calling. **Our Python files are scripts, never tools** |
| **Rules** | Always-on instructions to a coding agent (`AGENTS.md`, editor rule files). Ours are **policies** |
| **Collection** | A domain grouping of skills that owns their status. Equivalent to what some hosts call a plugin |
| **Catalog** | The browse surface over the library |
| **Registry** | The machine-readable index (`catalog/nav_registry.json`) |
| **Router** | Selects which skill runs. Also called a skill finder or skill retrieval elsewhere |

## The shared layer — our terms

| Term | Path | Meaning |
|---|---|---|
| **Context** | `contexts/` | A modality, therapeutic area, population, or region that changes *how* a skill runs. **Attached after selection, never selected** |
| **Shared reference** | `shared/references/` | Reusable knowledge with no independent user journey. Loaded by a named skill |
| **Policy** | `shared/policies/` | An always-on constraint every skill applies — evidence hierarchy, output states, human review, source preflight, untrusted content, privacy routing |
| **Script** | `shared/scripts/` | A deterministic transform or check. No scientific judgment |
| **Asset** | `shared/assets/` | Rubrics, banks, and templates a skill produces or consumes |
| **Workflow** | `docs/workflows/` | An ordered chain of skills with human gates, for requests spanning several skills. **Documented, never auto-run** |
| **Pattern** | — | The structural shape of one skill's body: linear, pipeline, safety gate, routing, task-driven |
| **Paste block** | `skills/<id>/PASTE.md` | A generated, self-contained form of a skill for use in any chat window, with no install |
| **Map page** | the published site | A generated page for one of the 167 job-model tasks |

## Status vocabulary

| Status | Means |
|---|---|
| `released` | The evaluation gate passed |
| `built` | The package exists and validates. **The gate has not run** |

`built` exists because "done" would have been a lie. Counts are regenerated from the
collections, never remembered.

## Why the router selects only one skill

Selection returns exactly one skill. That has one consequence worth stating plainly:

> **Skills cannot compose. Only contexts can.**

A question about population PK in a rare-disease antibody programme activates one
workflow and carries two dimensions of context. If modality and therapeutic area were
skills, they would compete with the workflow for selection and the answer would still
lack its context. As contexts they leave the ranking entirely, and one file improves
every skill that loads it.

## Words this project does not use

| Not used | Why | Instead |
|---|---|---|
| Module | Means **CTD Module** to this audience, and Python module to developers — ambiguous both ways | Shared reference, or context |
| Tool, for our scripts | Means an MCP callable everywhere else | Script |
| Rules, for our policies | Claimed by `AGENTS.md` and editor rule files | Policy |
| Agent · swarm · orchestrator | Describes what this project is not | Router, selector |

## Provenance markers

A `PS-D` id (for example `PS-D024`) is an internal product-decision marker.
The records live outside this repository. They are cited, not linked.

