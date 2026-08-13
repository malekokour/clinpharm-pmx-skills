---
asset: chat-starter-templates
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
consumers: [all skills]
---

# Chat-starter templates

The pattern for the degraded, attachment-only route. Most professionals will
first encounter this library in ChatGPT or Copilot, where no user-installable
skill mechanism exists.

## The honesty requirement

A starter states its own limits **on the page**, above the workflow:

> **This is the chat-starter form.** It carries the workflow, the rules and the
> output structure, but it cannot run this skill's deterministic checks. Numeric
> reconciliation is performed by the assistant with its arithmetic shown for you
> to confirm, not verified by a script. Scope it to a section — a synopsis plus
> one results section, tens of values rather than hundreds.

Never present the starter as equivalent to an installed package.

## Structure

1. What this does, and what it will not do — three lines
2. The restricted-data stop, verbatim from `source-preflight`
3. Owner-confirmation block
4. What to attach, artifact-exact
5. The numbered procedure, inlined
6. Output template, inlined
7. Severity taxonomy, inlined
8. The human-review gate and sign-off block
9. Degradation notice repeated at the end

## Filenames are for humans

`CSR-PK-Consistency-Review.docx`, not `review-csr-pk-consistency-starter-v0.2.0.docx`.
The technical id is an address; the filename is what someone recognises in their
Downloads folder six weeks later.

## Empirically recorded host behaviour

An authenticated Copilot web-chat test **rejected DOCX and accepted Markdown**.
Both formats therefore ship for every skill, and the Markdown is not optional.
