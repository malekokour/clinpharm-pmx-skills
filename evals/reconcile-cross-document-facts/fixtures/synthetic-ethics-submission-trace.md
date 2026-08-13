# SYNTHETIC — ethics-submission clinical-pharmacology trace

> Fully synthetic. Committee, study, document, question, response, and decision
> identifiers are fictional and contain no real submission material.

## Submission manifest

| Item | Document | Version | Submitted | Owner declared in responsibility map |
|---|---|---|---|---|
| M-01 | Protocol SYN-201 | v3.0 | 2026-06-01 | Regulatory operations |
| M-02 | PK sampling appendix | v2.0 | 2026-06-01 | Clinical pharmacology |
| M-03 | Participant information sheet | v4.0 | 2026-06-01 | Clinical operations |

## Clinical-pharmacology fact register

| Fact | Submitted statement | Source locator |
|---|---|---|
| CP-01 | Intensive PK samples are collected at 0, 1, 2, 4, 8, and 24 hours. | Protocol SYN-201 v3.0 §8.4 |
| CP-02 | Optional genomic sampling occurs at baseline only. | PK sampling appendix v2.0 §3 |

## Committee interaction

| Question | Question date | Fact | Response | Response source | Recorded state |
|---|---|---|---|---|---|
| Q-01 | 2026-06-12 | CP-01 | The schedule is 0, 1, 2, 4, 8, and 24 hours. | Protocol SYN-201 **v2.0** §8.4 | RESPONSE-RECORDED |
| Q-02 | 2026-06-12 | CP-02 | `UNKNOWN` | `UNKNOWN` | OPEN |

## Recorded decision and condition

| Record | Date | Statement | Carry-through evidence |
|---|---|---|---|
| D-01 | 2026-06-20 | Decision record received; exact approval state reserved to the committee record. | PRESENT |
| C-01 | 2026-06-20 | Revise participant-facing description of optional genomic sampling. | `UNKNOWN` |

## Planted trace defects

- Q-01 cites superseded Protocol SYN-201 v2.0 although manifest item M-01 is v3.0.
- Q-02 has no response or source locator and remains open.
- Condition C-01 has no carry-through evidence and remains `UNKNOWN`.

The task is to report those three trace states. It is not to decide ethics
approval, submission-owner correctness, or response adequacy.
