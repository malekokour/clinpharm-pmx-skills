# Install, update, roll back, uninstall

The four operations a library you actually depend on has to support, for the two
hosts this project advertises: **Claude** and **Codex**.

> **Scope, stated first.** Only these two hosts are advertised for the Agent
> Skill route. ChatGPT, GitHub Copilot and Microsoft 365 Copilot are documented
> in [`COMPATIBILITY.md`](COMPATIBILITY.md) for the attach-first route only, and
> nothing here claims an Agent Skill route for them.

## Before anything: which install shape do you want?

| Shape | What you get | When to choose it |
|---|---|---|
| **Whole repository** | Every package, the shared modules and tools, the nav registry, and the router | The default. Cross-skill routing and the shared modules only work when the whole tree is present |
| **Single package** | One `skills/<id>/` directory | You want exactly one workflow and accept that routing, neighbour separation and study-type modules are unavailable |

A single-package install is a **supported but reduced** mode, not a broken one.
Every package states which of its checks stop working without the whole tree,
and each eval suite carries a `portability` case that exercises that disclosure.

---

## Claude

### Install

1. Clone or download the repository.
2. Zip the directory you want:
   - whole repository → zip the repository root;
   - single package → zip `skills/<id>/` so `SKILL.md` sits at the archive root.
3. Claude → **Settings → Capabilities → Skills → Upload skill**.
4. Confirm the skill appears in the list with the name from its `SKILL.md`
   frontmatter — **not the folder name you zipped**. If they differ, you zipped
   the wrong level.

Verify in a **fresh** conversation, not the one you installed from:

> "Which ClinPharm PMx Skills skill applies to reviewing PK sections of a CSR?"

A correct install names `review-csr-pk-consistency` and says it is `built`, not
ready. If it answers without naming a package, the skill did not load.

### Update

Claude has no in-place update. **Uninstall, then install** — in that order.

Installing a second copy under the same name is the failure mode worth naming:
you get two skills whose descriptions both match, the host picks one, and which
one is not visible to you. If you are unsure whether an old copy is present,
list your skills before installing.

### Roll back

Releases are tagged. Download the previous release asset rather than
reconstructing it:

```bash
gh release download v0.1.0 --repo malekokour/clinpharm-pmx-skills
```

Then uninstall the current version and install the downloaded one. **Roll back by
reinstalling a known artifact, never by editing an installed skill in place** — an
edited install has no version, and nothing can tell you what it contains.

### Uninstall

Settings → Capabilities → Skills → the skill → **Remove**. Then confirm in a
fresh conversation that a request which previously routed now does not.

**Removal is not revocation.** Anything the skill produced during use — files,
conversation content — is unaffected by uninstalling it.

---

## Codex

### Install

Skills are read from the filesystem, so installation is a checkout:

```bash
git clone https://github.com/malekokour/clinpharm-pmx-skills.git
cd clinpharm-pmx-skills
```

Point Codex at the repository root for the whole-library route, or at a single
`skills/<id>/` directory for the reduced route.

Verify the deterministic router responds — this needs no model at all:

```bash
python3 scripts/library_router.py "review csr pk consistency across tables"
```

Expect a JSON selection record naming `review-csr-pk-consistency`. If that
command fails, the checkout is incomplete and no model-side test is meaningful
yet.

### Update

```bash
git -C <checkout> pull --ff-only
python3 scripts/check_all.py
```

`--ff-only` is deliberate: it refuses rather than merging if you have local
edits, which is what you want from a library you did not intend to fork.

Run the gates after updating. A pull that leaves `check_all.py` red is a state to
roll back from, not to work in.

### Roll back

```bash
git -C <checkout> checkout v0.1.0
python3 scripts/check_all.py
```

Tags are immutable; branches are not. Roll back to a tag.

### Uninstall

Remove the checkout directory and any Codex configuration pointing at it.
Confirm the router no longer resolves:

```bash
python3 scripts/library_router.py "review csr pk consistency" ; echo "exit=$?"
```

A missing checkout should fail loudly. If it still answers, a second copy exists
somewhere.

---

## After any of the four, on either host

Run the same one-line check, because all four operations can leave the same
failure: two copies, or none.

| Host | Check | Correct result |
|---|---|---|
| Claude | Ask a routing question in a **fresh** chat | Exactly one package named, with its status |
| Codex | `python3 scripts/library_router.py "<request>"` | One JSON record, or a clean failure |

---

## What is verified, and what is not

**Verified:** the Codex-side commands on this page are deterministic and run in
this repository's own gates — `scripts/check_lifecycle_docs.py` confirms every
path and script this page names actually exists, and `make check` fails if one
is renamed.

**UNVERIFIED — and this matters:** the Claude UI steps were confirmed on
**2026-07-30, for one package** (`build-work-context`), when the library was
substantially smaller. They have **not** been re-run against the current
23-package whole-repository install, and no update, rollback or uninstall
sequence has been executed end to end on either host.

Re-verification needs Malek's own Claude and Codex accounts, so it is an owner
step rather than something this repository can self-certify. Until it happens,
treat the Claude section as a documented procedure rather than a tested one, and
read [`COMPATIBILITY.md`](COMPATIBILITY.md) for exactly what was verified when.
