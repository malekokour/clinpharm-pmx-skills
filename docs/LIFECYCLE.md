# Install, update, roll back, uninstall

The four operations a library you actually depend on has to support.

Per-host **web and desktop** steps live in [`HOSTS.md`](HOSTS.md). This page is
the library-level runbook (clone, pull, tag, remove).

> **Scope, stated first.** Zero-install is each package's `PASTE.md`. Clone is
> the whole-library install. [`plugin.json`](../plugin.json) and
> [`.claude-plugin/`](../.claude-plugin/) are the manifests hosts look for.
> Claude, Codex, Cursor, and Antigravity steps in [`HOSTS.md`](HOSTS.md) are
> documented procedures. They are **UNVERIFIED** against the current 151-package
> library on the owner's accounts — that re-run is an owner step. The dated
> one-package record is in [`COMPATIBILITY.md`](COMPATIBILITY.md).

## Before anything: which install shape do you want?

| Shape | What you get | When to choose it |
|---|---|---|
| **Paste a block** | One package's `skills/<id>/PASTE.md` in an ordinary chat | No clone, no host skill install. Works on claude.ai, ChatGPT, and any other web chat |
| **Whole repository** | Every package, shared modules, the nav registry, and the router | Default on desktop agents (Claude Code, Codex, Cursor, Antigravity) |
| **Single package** | One `skills/<id>/` directory | The host only accepts one `SKILL.md` folder (claude.ai zip upload) |

A single-package install is a **supported but reduced** mode, not a broken one.
Every package states which of its checks stop working without the whole tree,
and each eval suite carries a `portability` case that exercises that disclosure.

---

## Install

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
cd clinpharm-pmx-skills
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install --requirement requirements.lock
python3 scripts/check_all.py
```

The dependency install is required. Without it the run stops at the
evaluation-suite gate with `ModuleNotFoundError: No module named 'strictyaml'`
and exits 1 — the gate working, not a broken checkout. The update and rollback
commands later in this document assume this step was done once for the checkout.

Then follow the host row in [`HOSTS.md`](HOSTS.md).

Verify the deterministic router — this needs no model:

```bash
python3 scripts/library_router.py "review csr pk consistency across tables"
```

Expect a JSON selection record naming `review-csr-pk-consistency`. If that
command fails, the checkout is incomplete and no model-side test is meaningful
yet.

On a skill-aware host, also ask in a **fresh** session:

> "Which ClinPharm PMx Skills skill applies to reviewing PK sections of a CSR?"

A correct install names `review-csr-pk-consistency` and its catalog status
(`released` today). If it answers without naming a package, the skill did not
load.

## Update

```bash
git -C <checkout> pull --ff-only
python3 scripts/check_all.py
```

`--ff-only` is deliberate: it refuses rather than merging if you have local
edits, which is what you want from a library you did not intend to fork.

Run the gates after updating. A pull that leaves `check_all.py` red is a state to
roll back from, not to work in.

Hosts that loaded a zip or a plugin copy (claude.ai, some plugin installs) have
no in-place update. **Uninstall, then install** the new copy — in that order.
Installing a second copy under the same name is the failure mode worth naming:
you get two skills whose descriptions both match, the host picks one, and which
one is not visible to you.

## Roll back

```bash
git -C <checkout> checkout v1.0.0
python3 scripts/check_all.py
```

A tag is a point in history; `main` is not. Later releases use the same pattern
with that tag. **Never edit an installed skill in place** — an edited install
has no version, and nothing can tell you what it contains.

```bash
git -C <checkout> log --oneline
git -C <checkout> checkout <sha>
```

also works when you need a commit that is not a tag.

## Uninstall

Remove the checkout directory and any host configuration pointing at it
(Claude Code plugin, Codex plugin, Cursor `.cursor/skills/` copies, Antigravity
plugin, uploaded claude.ai zip). Confirm the router no longer resolves:

```bash
python3 scripts/library_router.py "review csr pk consistency" ; echo "exit=$?"
```

A missing checkout should fail loudly. If it still answers, a second copy exists
somewhere.

On Claude / ChatGPT web, also confirm in a fresh conversation that a request
which previously routed now does not.

**Removal is not revocation.** Anything the skill produced during use — files,
conversation content — is unaffected by uninstalling it.

---

## After any of the four, on any host

Run the same one-line check, because all four operations can leave the same
failure: two copies, or none.

| Surface | Check | Correct result |
|---|---|---|
| Any skill-aware chat | Ask a routing question in a **fresh** session | Exactly one package named, with its status |
| Clone | `python3 scripts/library_router.py "<request>"` | One JSON record, or a clean failure |

---

## What is verified, and what is not

**Verified:** the clone-side commands on this page are deterministic and run in
this repository's own gates — `scripts/check_lifecycle_docs.py` confirms every
path and script this page names actually exists, and `make check` fails if one
is renamed.

**UNVERIFIED — and this matters:** host UI steps (claude.ai upload, ChatGPT
desktop plugin catalogs, Cursor Agent discovery, Antigravity `agy plugin
install`, Claude Code `/plugin install`) were last confirmed on **2026-07-30,
for one package** (`build-work-context`) on Claude, when the library was
substantially smaller. They have **not** been re-run against the current
151-package whole-repository install, and no update, rollback or uninstall
sequence has been executed end to end on those UIs.

Re-verification needs the owner's own host accounts, so it is an owner
step rather than something this repository can self-certify. Until it happens,
treat [`HOSTS.md`](HOSTS.md) as documented procedure rather than a tested
matrix, and read [`COMPATIBILITY.md`](COMPATIBILITY.md) for exactly what was
verified when.
