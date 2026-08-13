# Synthetic topline route-selection requests

All records are synthetic and contain no participant-level information.

## Request A — CSR-local

Snapshot SYN-TL-A and every named source belong to CSR SYN-101: Protocol SYN-101
v2.0, SAP SYN-101 v1.0, locked output SYN-101-L01, cutoff record SYN-101-C01,
analysis-set record SYN-101-AS01, exposure output SYN-101-PK01, and deviation log
SYN-101-D01.

Expected route: keep the source check in `review-csr-pk-consistency`.

## Request B — programme thread

Snapshot SYN-TL-B requires CSR SYN-102, CSR SYN-103, Module 2.7.2 v4.0, and
Briefing Package BP-01 to establish where the same effect and exposure values
were restated.

Expected route: `reconcile-cross-document-facts` in `TOPLINE-SNAPSHOT` mode.

Neither route may infer clinical meaning, causality, benefit-risk, disclosure
language, or commitments.
