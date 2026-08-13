# Compatibility

Current zero-install route: paste `skills/<id>/PASTE.md` into an ordinary chat.
Current library install: clone this whole repository. Host adapters and
`plugin.json` are **not** shipped — do not read this page as "works with
Claude / Codex / Cursor."

The table below is a **dated one-package record**, not a claim about the
151-package library on `main`.

> **What was measured.** Every `Verified` row was obtained on **2026-07-30**
> against **one package**, `build-work-context`, when the library was
> substantially smaller. It is **not** a verification of the current
> 151-package whole-repository install, and no update, rollback or uninstall
> sequence has been executed end to end on any host.
>
> Attach-first DOCX/Markdown starters from that date are archived at
> [`archive/starter/`](archive/starter/). Use `PASTE.md` now.
>
> The procedures are written up in [`LIFECYCLE.md`](LIFECYCLE.md), whose
> deterministic half is gated by `scripts/check_lifecycle_docs.py`. Re-running
> the host-side half needs the owner's own accounts, so it is an owner
> step. Until it happens, read these rows as *"this route worked for one
> package on that date"* — which is what they measured.

| Host | Paste / attach (2026-07-30) | Agent Skill route (2026-07-30) | Current evidence |
|---|---|---|---|
| Codex | Verified locally through file-input evaluation; hosted attachment UI not tested | Verified locally on all synthetic behavior cases; `skills-ref` valid | Current local Codex environment and [`../evals/LOCAL-EVALUATION.md`](../evals/LOCAL-EVALUATION.md) |
| ChatGPT | **Verified:** DOCX starter produced a complete context from synthetic facts | Not claimed | ChatGPT Pro, High; exact model not exposed |
| Claude | **Verified:** DOCX starter produced a complete context from synthetic facts | **Verified:** ZIP installed, persisted, loaded in a fresh chat, and produced the contracted Markdown | Claude Max, Opus 5 High |
| GitHub Copilot | **Verified with material limitations:** Markdown attached and produced output; DOCX was rejected as unsupported | Not claimed | Copilot Free, Auto; see limitations below |
| Microsoft 365 Copilot | **Manual test required:** authenticated host and upload control verified; automated local file transfer was not permitted | Not claimed | Copilot Chat (Basic), Auto; no content was transmitted |

## Compatibility labels

- `Verified`: completed in the named environment with synthetic content and
  persistence/output inspection.
- `Manual test required`: the design is plausible, but no current authenticated
  end-to-end proof exists.
- `Untested`: no runtime claim is made.
- `Not claimed`: the host does not have a verified equivalent interface.
- `Verified with material limitations`: the route executed, but the observed
  behavior requires a documented fallback or additional human review.

“Verified locally” is deliberately narrower than a hosted-product support
claim. It proves the local file and skill routes used in this repository, not a
particular account, plan, attachment UI, persistence feature, or future host
version.

## Authenticated synthetic test record

All tests below used the same fictional Regulatory Operations profile on
2026-07-30. Company, manager, and formal decision rights were deliberately
skipped. No employer, patient, sponsor, or real submission content was used.

| Host and plan | Route tested | Observed result | Classification |
|---|---|---|---|
| ChatGPT Pro, High | `Pharma-Work-Context.docx` in ordinary chat | Created a complete `My-Pharma-Work-Context`, preserved skipped fields, and exposed unknowns and approval boundaries | Verified |
| Claude Max, Opus 5 High | `Pharma-Work-Context.docx` in ordinary chat | Created a complete context and kept organization, tools, authority, and readiness criteria unknown | Verified |
| Claude Max, Opus 5 High | Installed `build-work-context` ZIP in Skills, selected it in a fresh chat | Claude displayed “Loaded build-work-context skill,” read its references, produced the contracted Markdown, and explicitly declined to invent standard-sounding Regulatory Operations details | Verified |
| GitHub Copilot Free, Auto | DOCX upload | Host rejected `.docx` and requested a plain-text file | Unsupported file type |
| GitHub Copilot Free, Auto | Markdown upload | Host accepted the starter and created a context, but invented an escalation flow, reviewer functions, workflow deliverables, authority hierarchy, and review cadence that the user had not supplied | Verified with material limitations |
| Microsoft 365 Copilot, Copilot Chat (Basic), Auto | DOCX attach on 2026-07-30 | Authenticated host and upload control were verified. The browser automation environment could not transfer the local file because local-file access was disabled, so no prompt or document was sent and no output claim is made. | Manual test required |

The Copilot result validates the Markdown transport but not safety fidelity. Use
the Markdown route only with careful human review, and treat any plausible
industry convention as inference unless the user or a governing source confirms
it.

## Agent Skill contract

Each package follows the open specification:

- a directory containing `SKILL.md`;
- required `name` and `description`;
- lowercase letters, numbers, and hyphens in the name;
- a directory name matching the skill name;
- optional `references/` and `assets/`; and
- progressive disclosure.

Specification: <https://agentskills.io/specification>

## GitHub Copilot project adapter

An exported working pack can inform project-specific instructions. GitHub
supports repository-wide `.github/copilot-instructions.md`, path-specific
instruction files, and `AGENTS.md` for agent instructions. This repository
does not generate or install those files; users may adapt a working pack
inside their approved repository.

Documentation:
<https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>

## Validation needed for broader support claims

For each host:

1. use a synthetic professional and project;
2. run CREATE, UPDATE, PROJECT, REFRESH, and EXPORT where the host supports the
   route;
3. check filenames and content;
4. restart or open a new conversation;
5. verify the exported context remains usable;
6. record product, plan, model, date, and limitations; and
7. avoid claims that generalize beyond the tested environment.
