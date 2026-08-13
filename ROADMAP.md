# Roadmap — ClinPharm PMx Skills

**Open Agent Skills library for clinical pharmacology and pharmacometrics.**

> **North star:** ClinPharm PMx Skills aims to be **THE place people go for AI +
> Clinical Pharmacology + Pharmacometrics.** We earn that with coverage, a library
> router, honest qualification status, and this roadmap kept aligned with reality.

## Status vocabulary

| Status | Means |
|---|---|
| `released` | The package passed its assigned evaluation gate |
| `built` | The package exists and validates; the gate has **not** passed |

Regenerate live tallies from the catalog before quoting counts. Package count is
not readiness.

## Now (V1)

**Shipped**

- **The map** — one published page per job-model task, generated from the coverage
  ledger. Usable with no AI and no install
- **Zero-install paste blocks** — every package ships a generated `PASTE.md` that works
  in any chat window
- Whole-repository **skills-first** library — flat `skills/<id>/`; virtual job-tree navigation
- **Composable context** — modality and therapeutic area attach to a skill after
  selection rather than competing with it
- Shared layer: contexts, references, policies, scripts, assets
- **Documented multi-skill workflows** with their human gates named. Never auto-run
- **The authoring method, published** — anyone can extend the library to the same standard
- Site: no-tracking and accessibility enforced as release gates
- Human boundary on every skill: review / reconcile / verify / structure / flag — humans decide
- **Skill volume floor** — Vision v1.2 target of 151 packages is on disk; live
  `released`/`built` tallies regenerate from `collections/*/collection.json`
- **Qualification vocabulary applied across the library** — packages carry
  `released` only with an evidence-level stamp; regenerate the catalog before quoting

**In progress**

- **Operational router** — registry, complexity classes, selection SLO, and the
  selection evaluation suite exist; host wiring and productization continue
- Independent re-review of HIGH-risk packages (owner discretion)
- Proven host install/update/rollback/uninstall for every advertised host

## Next

- Keep HIGH-risk re-review and evidence depth proportional to use
- **Pharmacometrics as a first-class track** (collection depth, skills/modules, docs parity)
- Keep the task→skill coverage join current, with denominators
- Clear contributor path to request or propose skills
- Shared [REFERENCES.md](REFERENCES.md) index (skills keep local refs)

## Later

- Full skillable coverage of in-scope job-model tasks (human-only and out-of-scope rows stay explicit)
- Optional per-skill ZIP install with vendored shared material
- Fixture/dataset packs and reusable evaluation kits **around** skills
- Optional host adapters (e.g. MCP) only if they serve the skill library
- New domain collections only with named owner, research package, safety boundary, and release gate

## Not planned

- Autonomous dosing, submission sign-off, or replacing professional judgment
- Becoming a general pharma agent OS or swarm runtime
- Broad domains outside clinical pharmacology / pharmacometrics without a scoped decision
- Calling unfinished packages production-ready

## Human boundary

**Skills review, reconcile, verify, structure, and flag. Qualified humans decide,
approve, sign off, submit, and act.**
