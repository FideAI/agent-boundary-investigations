# Claims and justifications

Working assessments; independent human review remains pending.

These 16 entries cover the principal empirical and scope claims, not every sentence of the articles.

## A01: The selected archive study acquired 187 reports: 29 development, 79 other March families and 79 upstream background.

**Basis:** Fide acquisition and recomputation

- [data/selection.json](data/selection.json)
- [data/acquisition.json](data/acquisition.json)
- [results/archive-summary.json](results/archive-summary.json)

**Limit:** Purposeful selection; not 187 agents or attacks

**Review:** assistant checked; human pending

## A02: Four ONCB submissions contain programs; two contain fetch-and-relay instructions; one report records an ONCB data-bearing output request.

**Basis:** Static decoding plus archived HTTP entries

- [results/archive-observations.csv](results/archive-observations.csv)
- [results/archive-transactions.csv](results/archive-transactions.csv)

[Original source](https://urlquery.net/report/81699969-91c3-4454-913e-1a015b3fde47)

Locator: `http[0].url.addr and http[0].response.status_code; final.dom.size`

**Limit:** No exact source/output byte match; no proof of subsequent agent use

**Review:** assistant close read; human pending

## A03: Some submitted programs have no corresponding target or output request in the retained record.

**Basis:** Two contrasted March 6 source records

- [results/archive-observations.csv](results/archive-observations.csv)
- [results/archive-transactions.csv](results/archive-transactions.csv)

[Original source](https://urlquery.net/report/599b4a38-3c6c-451a-bcfc-fb7c2d3e85b8)

**Limit:** Absence scoped to acquired record; not a global absence claim

**Review:** assistant close read; human pending

## A04: Two other March carriers encode answer tables without scripts, while one upstream background carrier contains a diagnostic script.

**Basis:** Static decoding of d6669745, 4c62b534 and bdf482a4 reports

- [results/archive-observations.csv](results/archive-observations.csv)

**Limit:** Background labels are upstream judgments; not a false-positive rate

**Review:** assistant close read; human pending

## A05: All 2,978 selected HTTP entries lack embedded raw response body data; 128 pair a positive reported size with an empty-string SHA-256.

**Basis:** Fide JSON field checks

- [results/archive-summary.json](results/archive-summary.json)
- [results/hash-field-anomalies.json](results/hash-field-anomalies.json)

**Limit:** Archive representation caution, not proof of falsification

**Review:** assistant checked; human pending

## A06: This investigation has not established a new incident or independently authenticated an actor.

**Basis:** Novelty and search review

- [data/search-log.json](data/search-log.json)
- [RESEARCH-NOTES.md](RESEARCH-NOTES.md)

**Limit:** Empty service responses did not establish zero search results

**Review:** assistant checked; human pending

## A07: All seven decodable httpbin payloads in the 187 selected reports were audited: five carrier fingerprints match and two differ; three of five submitted script payloads have matching script entries.

**Basis:** Static byte and SHA-256 comparisons against pinned acquired JSON

- [scripts/audit_carriers.py](scripts/audit_carriers.py)
- [results/carrier-audit.json](results/carrier-audit.json)

**Limit:** Archive metadata corroboration, not recovered response bodies, proof of complete execution or an actor detector

**Review:** assistant checked; human pending

## T01: The main comparison ran 17 authored cases, 47 route variants and 188 condition cells.

**Basis:** Executed local HTTP experiment

- [data/transfer-cases.json](data/transfer-cases.json)
- [results/transfer-decisions.csv](results/transfer-decisions.csv)
- [results/verification.json](results/verification.json)

**Limit:** Correlated authored fixtures, not independent real-world incidents

**Review:** assistant checked; human pending

## T02: Both complete controls prevented all 25 prohibited variants; the shared service added no prevention in the fixture set.

**Basis:** Receiver-journal recomputation

- [results/transfer-summary.json](results/transfer-summary.json)
- [results/transfer-receipts.csv](results/transfer-receipts.csv)

**Limit:** Trusted adapters and inputs; raw client bypasses both

**Review:** assistant checked; human pending

## T03: Of 22 permitted variants, per-tool checks completed 16 and shared checks 13; the difference was the injected shared-service outage.

**Basis:** Per-case outcome comparison

- [results/transfer-decisions.csv](results/transfer-decisions.csv)
- [results/verification.json](results/verification.json)

**Limit:** Not a deployment reliability estimate; both also block a missing fixture restriction label and receive partial fixtures

**Review:** assistant checked; human pending

## T04: Injected faults produced failed clients with full receipt and successful clients with partial receipt under every condition.

**Basis:** Separate client and receiver observations

- [results/transfer-decisions.csv](results/transfer-decisions.csv)
- [results/transfer-receipts.csv](results/transfer-receipts.csv)

**Limit:** Two authored faults across three adapters; not natural failure frequency

**Review:** assistant checked; human pending

## T05: An unmediated client bypassed both complete adapter controls.

**Basis:** Executed separate challenge

- [results/transfer-challenges.json](results/transfer-challenges.json)
- [results/challenge-events.csv](results/challenge-events.csv)
- [results/challenge-receipts.csv](results/challenge-receipts.csv)

**Limit:** The experiment has no OS-level network enforcement

**Review:** assistant checked; human pending

## T06: OpenAI reported successful public uploads followed by blocked browser operations.

**Basis:** Publisher-reported historical examples


[Original source](https://alignment.openai.com/misalignment-reports/uploading-files-to-the-internet-in-order-to-cite-them/)

**Limit:** Not independently verified by Fide; not part of the experiment denominator

**Review:** source read; human pending

## T07: A second request supplied with permission=false was denied while an earlier permitted receipt remained in the journal.

**Basis:** Separate local challenge

- [results/transfer-challenges.json](results/transfer-challenges.json)
- [results/challenge-events.csv](results/challenge-events.csv)
- [results/challenge-receipts.csv](results/challenge-receipts.csv)

**Limit:** Two static case definitions; no mutable permission store, revocation operation or concurrency test

**Review:** assistant checked; human pending

## T08: Removing a primary local file left a known replica with the original digest.

**Basis:** Local two-file illustration

- [results/transfer-challenges.json](results/transfer-challenges.json)

**Limit:** Not evidence about any external service or vendor cleanup

**Review:** assistant checked; human pending

## T09: The 47 named route variants contain 33 distinct operational configurations under the documented executable-input grouping.

**Basis:** Static inspection of fixture bytes, labels, cases, routes and fault flags

- [scripts/transfer_coverage.py](scripts/transfer_coverage.py)
- [results/transfer-coverage.json](results/transfer-coverage.json)

**Limit:** Neither named nor grouped counts are independent real incidents or statistical trials

**Review:** assistant checked; human pending
