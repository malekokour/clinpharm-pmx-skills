# How to use ClinPharm PMx Skills

This library is packaged as [Agent Skills](https://agentskills.io/specification)
plus an [Agent Plugins 1.0.0](https://agent-plugins.org/) manifest
([`plugin.json`](../plugin.json)). Skills live in [`skills/`](../skills/).

**What this page is.** Install and use steps for Claude, ChatGPT / Codex,
Cursor, and Google Antigravity, on web and on desktop. Paste works in any
ordinary chat. Native skill install is the host's own loader reading this
repository.

**What this page is not.** A claim that every host was re-run end-to-end
against all 151 packages on your account. That is an [owner step](LIFECYCLE.md).
The dated one-package record is in [`COMPATIBILITY.md`](COMPATIBILITY.md).

Skills review, reconcile, verify, structure, and flag. **You** decide, approve,
sign, and submit. Never upload patient-level, sponsor-confidential, or
employer-proprietary material.

---

## Pick a shape

| Shape | Use when |
|---|---|
| **Paste one block** | Any web chat. No clone. Open `skills/<id>/PASTE.md`, paste it, attach only permitted files, ask. |
| **Open the clone** | Desktop agents (Claude Code, Codex, Cursor, Antigravity). Whole library, router, shared modules. |
| **One package folder** | The host only accepts a single `SKILL.md` directory. Routing and shared modules are unavailable. |

Start with the worked example: [`skills/verify-nca-outputs/PASTE.md`](../skills/verify-nca-outputs/PASTE.md)
and [`examples/verify-nca-outputs/inputs/`](../examples/verify-nca-outputs/inputs/).

When you do not know which skill to run, use
[`skills/library-router/`](../skills/library-router/) or ask:

> Which ClinPharm PMx Skills skill applies to reviewing PK sections of a CSR?

A loaded library names `review-csr-pk-consistency`. If the host answers without
naming a package, the skills did not load.

---

## Claude

Web and desktop **do not share** an installed skill list. Install on the surface
you actually use. Official: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude),
[Claude Code skills](https://code.claude.com/docs/en/skills).

### Web — [claude.ai](https://claude.ai)

1. Enable **Code execution and file creation** under Settings → Capabilities
   (Free / Pro / Max) or Organization settings → Skills (Team / Enterprise).
2. **One skill:** zip `skills/<id>/` so `SKILL.md` is at the zip root. Customize
   → Skills → Upload a skill.
3. **Do not zip the whole repository** for claude.ai. The web uploader expects
   one skill folder per zip, not 151 packages.
4. **Any chat, no upload:** paste `skills/<id>/PASTE.md` into the conversation
   and attach only permitted source files.

Confirm in a **new** chat, not the one you uploaded from.

### Desktop — Claude Code

From a checkout of this repository:

```
/plugin marketplace add malekokour/clinpharm-pmx-skills
/plugin install clinpharm-pmx-skills@clinpharm-pmx-skills
```

Or, without the marketplace:

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
cd clinpharm-pmx-skills
claude --plugin-dir .
```

Project-local alternative: clone, open the folder in Claude Code. The plugin
manifest is [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json); skills
are `./skills`.

SSH errors on `/plugin marketplace add` usually mean GitHub SSH is not set up.
Use the HTTPS URL instead:

```
/plugin marketplace add https://github.com/malekokour/clinpharm-pmx-skills.git
```

---

## ChatGPT and Codex

Skills in ChatGPT desktop / Codex follow the Agent Skills format. Plugins
(this repo's `plugin.json` + `skills/`) are the distributable package for
ChatGPT Work and Codex. Official: [Build skills](https://developers.openai.com/codex/skills),
[Agent Plugins](https://agent-plugins.org/).

### Web — [chatgpt.com](https://chatgpt.com)

Paste `skills/<id>/PASTE.md` into the chat. Attach only permitted files. Ask
the same question you would ask a skill-aware host.

ChatGPT's hosted skill/plugin catalogs are workspace features (ChatGPT Work).
They are not the same as pasting a block. Until that catalog lists this
repository, **paste is the web route**.

### Desktop — ChatGPT app and Codex CLI

Clone, then point Codex at the repository root:

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
cd clinpharm-pmx-skills
```

Codex CLI (v0.147.0 or later reads Agent Plugins):

```bash
codex plugin marketplace add malekokour/clinpharm-pmx-skills
codex plugin add clinpharm-pmx-skills@clinpharm-pmx-skills
```

> **UNVERIFIED: the version number and these two commands have not been executed
> by this project.** `codex` was not installed on the machine that produced
> [`catalog/adapter-evidence.json`](../catalog/adapter-evidence.json), so the
> block above is a documented expectation, not a tested route. Treat a failure
> here as our claim being wrong, not your typing — and please open an issue.
> What *is* verified: root [`plugin.json`](../plugin.json) is a valid Agent
> Plugins 1.0.0 manifest, checked with a schema validator.

If your Codex build does not yet have `plugin` subcommands, open the clone as
the working directory. Codex reads `SKILL.md` trees from the project. That
fallback is the same shape as the Cursor route, which **is** verified.

Prove the checkout before involving a model:

```bash
python3 scripts/library_router.py "review csr pk consistency across tables"
```

Expect JSON naming `review-csr-pk-consistency`.

---

## Cursor

Cursor is a **desktop** app. There is no separate Cursor web skill host.

1. `git clone https://github.com/malekokour/clinpharm-pmx-skills.git`
2. File → Open Folder on that clone.
3. Ask in Agent chat. Cursor-compatible clients discover Agent Plugins from
   [`plugin.json`](../plugin.json) and load `skills/`.

To use the skills **inside a different project**, copy or symlink individual
`skills/<id>/` directories into that project's `.cursor/skills/` (one folder
per skill, `SKILL.md` at that folder's root). Do not paste a full `SKILL.md`
into a Cursor rule file.

Optional installer used by many Agent Skills libraries:

```bash
npx skills add malekokour/clinpharm-pmx-skills
```

That copies skill folders into the agent directories the [skills CLI](https://github.com/vercel-labs/skills)
knows about. Prefer cloning this repository when you want the router and
shared modules.

---

## Google Antigravity

Antigravity is a **desktop** IDE (plus `agy` CLI). Google is on the Agent
Plugins steering group; skills live under `skills/` with `plugin.json` at the
plugin root.

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
```

Open that folder as the Antigravity workspace.

If your `agy` build supports plugin install from Git:

```bash
agy plugin install https://github.com/malekokour/clinpharm-pmx-skills
```

> **UNVERIFIED: this command has not been executed by this project.** `agy` was
> not installed on the machine that produced
> [`catalog/adapter-evidence.json`](../catalog/adapter-evidence.json). It is kept
> here, behind its conditional, rather than in the README, because a bare command
> in a README reads as a promise that it runs. If it fails, that is our claim
> being wrong, not your typing.

If that command is not available, the clone is the supported path. This
repository also ships [`GEMINI.md`](../GEMINI.md) (a pointer to `AGENTS.md`)
for Gemini-family hosts — also unverified, for the same reason: no `gemini` on
the test machine.

---

## After install — same checks on every host

| Check | Pass |
|---|---|
| Routing question in a **fresh** session | Names `review-csr-pk-consistency` (or the skill you installed) |
| Worked example | Reports the planted NCA defects; refuses to pick the scientifically “correct” value or a dose |
| `python3 scripts/library_router.py "…"` (clone only) | One JSON record, or a clean failure |

Update a clone with `git pull --ff-only` and `python3 scripts/check_all.py`
(the checkout needs `python3 -m pip install --requirement requirements.lock` once
before any gate will run — see [`LIFECYCLE.md`](LIFECYCLE.md)).
Roll back to tag `v1.0.0` (or a later release). Uninstall by removing the
checkout, the plugin, or the uploaded zip — then confirm a fresh session no
longer names the package.

Full install / update / rollback / uninstall: [`LIFECYCLE.md`](LIFECYCLE.md).
