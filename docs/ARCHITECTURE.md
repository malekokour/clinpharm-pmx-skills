# Architecture

## Product boundary

ClinPharm PMx Skills is a portable content and workflow layer: 151 packages,
no server, database, account, autonomous agent, connector, or external upload.

Each package turns permitted information into findings a qualified professional
can review. Zero-install is `PASTE.md`. Host adapters are not in this tree.

## Four-layer model

```text
Safety Kernel
    ↓ governs
Professional Constitution
    ↓ selects relevant context for
Project Capsule
    ↓ combines into
AI Working Pack
```

### Safety Kernel

Stable rules that must travel with every derivative:

- data classification and approved environment;
- prohibited inputs and destinations;
- permitted tools and actions;
- human-review gates; and
- stop conditions.

### Professional Constitution

Relatively stable professional context. It is not a resume and should not
contain unnecessary biography.

### Project Capsule

Mutable project context. It references the operational source of truth and does
not replace task, document, trial, quality, or regulatory systems.

### AI Working Pack

A focused, self-contained export for one project or task. It includes only the
professional context needed for that work.

## Source and generated artifacts

Markdown is canonical. DOCX is generated for usability.

```text
canonical .md
    ├── reviewed directly
    ├── parsed by compatible AI hosts
    └── rendered to .docx for human reading (archived starters; live route is PASTE.md)
```

Generated DOCX files must be rebuilt, privacy scrubbed, rendered, and visually
inspected before release.

## Public interface

The stable library interface consists of:

- 151 flat packages under `skills/<id>/`, each with `SKILL.md` and `PASTE.md`;
- the 167-task map under `map/`;
- `CLAIM-LEDGER.md` as the regenerated public counts;
- required Agent Skills headings and metadata; and
- conservative update semantics.

`build-work-context` remains one package in that set, not the product.

Provider-specific adapters may be added later, but the canonical content must
remain provider-neutral.

## Product-family separation

- **ClinPharm AI R** remains the computational pharmacometrics product.
- **ClinPharm PMx Skills** provides portable professional context and workflows.
- Monitoring, hosted-workspace, and autonomous-agent products remain separate
  product categories and are not imported into this repository.

No repository imports private product bodies merely because the products share
an owner or domain.
