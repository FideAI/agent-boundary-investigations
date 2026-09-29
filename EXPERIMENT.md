# Transfer-control qualification and comparison

Design recorded before first execution · September 26, 2026

Implementation clarification added during critical review: the restriction lookup and supplied grant values described below are simplified fixture inputs. The original case definitions and execution results are preserved.

## Question

Does placing an authorization decision in a shared service improve transfer enforcement over equivalent checks in each tool? What happens when a request fails after a recipient has received bytes?

This is a controlled mechanism study with authored fixtures and actual HTTP exchanges on loopback. It is not an evaluation of an AI model, historical safeguards, an internet-scale attacker or a production security boundary. No paid inference is used.

## Prior work and incremental contribution

[Complete mediation](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html) is an established security principle. [CaMeL](https://arxiv.org/abs/2503.18813) applies explicit control/data-flow policies to agent tools. [Redwood's timing analysis](https://www.redwoodresearch.org/blog/blocking-live-failures-with-synchronous) distinguishes detection and prevention. We claim no invention of authorization, information-flow tracking or pre-execution checks.

Our incremental purpose is to connect disclosed cross-tool transfers to an inspectable engineering comparison, preserving successful controls and receiver-side effects. A null difference between equivalent per-tool and shared enforcement is an informative outcome. Any contribution beyond that must be earned by the results.

## Environment and trust boundaries

A local HTTP server represents an approved recipient, an outside recipient and a relay. Every address is hard-coded to 127.0.0.1 with an ephemeral port. Harmless fixture bytes carry synthetic markers. A separate receipt journal records recipient, length and SHA-256 before sending the HTTP response. The client cannot write that journal. The relay makes a second real HTTP request to the final recipient and is itself a recipient of the fixture bytes.

The policy checks a fixture-name restriction lookup, every recipient in the route, stated purpose, and a supplied permission boolean at dispatch. The lookup is authored by the experimenter. Prepared fixtures represent transformations; no rename, summarization operation or source-parent chain is implemented. A missing lookup entry causes abstention (the recorded reason is named `unknown_lineage`). This is a trusted-fixture assumption, not a demonstrated general solution for tracking arbitrary transformed data. Purpose is declared by the client; the study cannot validate its truth.

Three adapters initiate actions: a Python HTTP client (browser-like operation, not an actual browser), a command-line HTTP client, and a local relay. These do not implement real browser sandboxing or agent tool APIs. The program issues no live exploit probes.

## Conditions

- **No enforcement:** fixed requested actions execute. This is a reference condition, not instruction-only model compliance.
- **Browser adapter only:** only that adapter checks the same policy. An explicitly incomplete coverage illustration, not a claim about any vendor's configuration.
- **Equivalent per-tool:** all three adapters check the same policy with identical inputs immediately before dispatch.
- **Shared decision service:** all three adapters request the same policy decision over loopback immediately before dispatch. It fails closed when unavailable.

Policy decision equivalence is held fixed. Placement is the variable. No result supports effectiveness against an agent that can bypass the adapters: a raw-client bypass challenge will explicitly test that assumption. There is no operating-system network sandbox. The controlled dispatch point is not a transactional guarantee under arbitrary concurrent permission changes.

## Cases and allocations

Development cases: approved public transfer; restricted data to approved recipient; restricted data to outside recipient; wrong purpose; missing grant; renamed restricted artifact; permission revoked before dispatch.

Evaluation cases (fixed before comparison): traced summary to approved/outside recipients; misleading self-declared public label; missing lineage for an otherwise permitted transformation; approved relay with approved/outside final recipient; decision service outage; receiver closes connection after full receipt; receiver acknowledges only a partial body; destination changed before dispatch.

Every applicable case runs through all three adapters under all four conditions. Cases marked for a relay route run only there. Repeated routes are correlated variants of an authored case, not independent incidents. No statistical population inference or operational success rate will be reported. One execution per fixture/route/condition is enough for the functional comparison; timing values are diagnostic and do not establish production latency.

Separate challenges: an unmediated raw HTTP client; two sequential requests with fixed permission values of true and false; deletion of a primary copy while a known replica remains. The permission illustration does not implement mutable grant state or a revocation operation. These are not pooled into the main authorization score.

## Outcome rules, set before comparison

- Authorization truth follows the authored case's explicit grant and purpose at dispatch, independently recorded in the case definition. Missing lineage may create a false block relative to the experimenter's known legitimate task.
- Any prohibited recipient receiving any nonzero bytes is an unauthorized transfer. Partial receipt is consequential.
- Full receipt requires the destination's digest and byte length to match the intended fixture. Client success is recorded separately.
- Authorized work completes when the intended final recipient has the complete matching payload. A client exception does not automatically mean failure of that objective.
- A false block is an authorized case denied/abstained by a control. Network-caused partial delivery is separate from false blocking.
- Unknown or absent receipts are explicitly distinguished from full or partial receipts. Local journal coverage is bounded to the controlled services.
- Report case counts, route counts, main comparison cells, unauthorized receipts, authorized completions, false blocks, partial receipts and client/receiver disagreements.
- Recovery evidence names the affected copy. Blocking a later action does not erase bytes already received.

## Qualification and review

Before the full comparison, confirm an authorized fixture is received with matching digest; a blocked dispatch produces no receiver entry; the relay records both hops; a lost acknowledgment still leaves a receipt. Store those checks separately from the comparison. Retain failed qualification output and repair notes if the harness changes.

The first comparison remains an engineering mechanism study even if every fixture passes. A technical human review and a non-specialist read remain outstanding before publication of the companion articles; assistant checks are identified as self-review. The research companion is working material prepared for public release, not reviewed publication signoff. The deferred instruction-following/adaptation condition requires a separately qualified free inference route.
