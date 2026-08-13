# Security and data-safety policy

## Supported versions

No GitHub Release or tag has been published yet. The current `main` branch is
the supported surface. Tagged versions will be listed here when they exist.

## Report a repository security issue

Use GitHub's **Report a vulnerability** control in the repository Security tab.
Do not include secrets, credentials, confidential documents, patient
information, or proprietary examples in a public issue.

If a report concerns data accidentally committed to the public repository,
identify the path and exposure type without repeating the sensitive value.

## Data that must not enter this repository

- credentials, tokens, cookies, keys, or authentication files;
- protected health information or patient-level records;
- sponsor-confidential trial material;
- unpublished protocols, CSRs, analysis plans, or submission drafts;
- employer-proprietary templates, procedures, or internal correspondence;
- raw clinical or pharmacometric datasets and model outputs;
- licensed material without redistribution rights; or
- personal contact, payment, or identity information.

Examples and tests must be synthetic, public, or explicitly redistributable.

## Skill execution boundary

Agent Skills can influence an AI host and may be able to read files, call tools,
or modify content depending on the host. Review `SKILL.md` before installation,
install only the skill you need, and use the most restrictive available
permissions.

The flagship skill:

- does not request credentials;
- does not send, post, submit, or approve external content;
- does not install software or connect services;
- asks for the current data boundary before reading project material; and
- stops or switches to abstracted/synthetic context when the environment is not
  approved for the proposed material.

## Clinical and regulatory boundary

This library is not clinical decision support, medical advice, or a validated
GxP system. Generated work requires qualified human review before decision,
submission, publication, or patient impact.

## Response expectations

The maintainer will acknowledge a valid private report when reviewed, assess
the affected versions, and coordinate remediation before public disclosure
where feasible. This open-source project does not promise a fixed response
time.
