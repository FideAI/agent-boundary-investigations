# Ordinary services, consequential actions: methods and results

Fide AI · September 26, 2026 · local review edition

## Contribution and scope

This package contains a visual reconstruction of a known URLQuery sequence and a separate local transfer-control experiment. Transluce discovered and attributed the archive activity. Fide's contribution is a reproducible examination of evidence layers, an explicit account of what the acquired records do not show, and a controlled comparison motivated by the resulting defensive question. We establish no new incident, new actor identity or operational defense success rate.

Our normative premise is that permission should attach to consequential actions and their effects, and that completion and recovery claims need observable support. The experiment implements a chosen data/recipient/purpose/grant policy. It does not recover historical permissions from public logs.

## Archive selection

Source: [Transluce's September 23 release](https://transluce.org/data/urlquery-agent-activity-2026-09-23.zip), SHA-256 `969a13fbd7d80d7e1556eef58a347f52ecdd85661c541f6c0d1d6f5e2a86570d`. Verify member hashes and unique report IDs before joining metadata. The source table contains one row per included report; background and review-required rows intentionally lack source assignments.

The complete release contains 38,160 metadata rows, not that many full reports. We selected all 29 March 6 reports assigned to Thai ONCB; all 79 March reports assigned to Thai NSO, Trading Economics/metals and Thrill Data; and the 79 upstream background examples. The dated `data/selection.json` was written before acquisition. All 187 were acquired successfully through `/report/{id}/json`. No embedded URL was visited and no submitted program was executed.

The 29-record cohort supplied development examples. Four extraction rules were fixed in `data/fingerprint-rules.json` before inspecting the full reports from the other families. Those families were already known from published reporting. This is neither blind validation nor a representative generalization study. Background labels originate upstream and have not been independently validated as benign. Their date distribution also differs from the development cohort.

## Extraction and reconstruction

Submitted addresses are read as inert strings. For httpbin Base64 carrier paths, we percent-decode once, validate Base64 and decode UTF-8 within a fixed size bound. HTML script markers, fetch-and-relay text and intended domains are extracted separately from archived HTTP transactions. Program text identifies proposed operations; request entries identify observed requests. A 200 response records a response, not necessarily meaningful success.

The final March report has a query parameter containing ONCB field names in a recorded output request. We retain its exact field index and hash in the derived data. The source response body is absent, so byte-for-byte source/output equality is not established. The final DOM size of zero is a metadata observation, not a screenshot of what an original agent saw.

Use transaction timestamps for within-report action ordering, and report-generation timestamps to identify reports. Array order is not chronological in every report. For example, the final report lists the output transaction before the earlier carrier transaction. The visual sequence orders those transactions by their recorded dates. It does not fabricate intermediate steps or agent thinking.

## Archive results

| Selected cohort | Reports | Decodable carriers | Carriers with scripts | Fetch-and-relay programs | Recorded ONCB output marker |
|---|---:|---:|---:|---:|---:|
| March 6 ONCB development | 29 | 4 | 4 | 2 | 1 |
| Other March families | 79 | 2 | 0 | 0 | 0 |
| Upstream background challenge | 79 | 1 | 1 | 0 | 0 |

The two other March carriers contain answer tables. The background script changes a page title and writes to its console. These counterexamples show why neither an encoded address nor executable JavaScript is an actor identity. The narrow relay pattern misses the other known task families; do not describe it as a validated agent detector.

There are 2,978 HTTP entries across the acquired reports. Raw response bodies are absent from all entries. In 128 entries a positive size coexists with the empty-string SHA-256. We therefore reject these fields as exact payload-equality evidence. This can reflect archive representation or missing data; it does not establish falsification. Global resource fields such as last-seen can change on acquisition, so whole-JSON hashes pin a dated acquisition rather than guarantee future byte-identical downloads.

Three fresh read-only searches are recorded in `data/search-log.json`. Each returned an empty service response without a verifiable zero-result marker. Discovery remains unresolved. This is not evidence that no additional activity exists. No newly discovered episode is claimed.

## Experiment design and qualification

The full design is in `EXPERIMENT.md`. Cases and outcome definitions preceded the comparison. Seven development and ten evaluation cases produce 47 route variants. Each runs under four conditions, giving 188 functional comparison cells. They are correlated authored fixtures, not independent natural incidents.

Three local adapters make actual HTTP requests: Python HTTP client, curl, and a server-side relay that issues a second request. Every destination is loopback. The receiver records bytes and SHA-256 separately before replying. Qualification checks an allowed receipt, absence of a receipt after denial, both relay hops and a lost acknowledgment after successful receipt. All four checks passed before comparison.

No-enforcement is a reference, not an instruction-following baseline. Browser-only checks are an intentionally incomplete illustration. The complete per-tool and shared conditions use the same policy and information. Shared authorization is a local decision service used by trusted adapters, not an unavoidable network gateway. Complete mediation is a longstanding principle, and CaMeL is relevant prior work on data-flow policies; we claim no invention of either.

## Experimental results

| Condition | Prohibited variants with receipt / 25 | Permitted variants completed / 22 | Permitted variants blocked | Partial receipts |
|---|---:|---:|---:|---:|
| No enforcement | 25 | 19 | 0 | 3 |
| Browser-like adapter only | 17 | 18 | 1 | 3 |
| Equivalent per-tool checks | 0 | 16 | 3 | 3 |
| Shared decision service | 0 | 13 | 6 | 3 |

The complete conditions differ only on the injected decision-service outage. Both abstain on a missing fixture restriction label (recorded as `unknown_lineage`), producing three false blocks each relative to the experimenter's known legitimate task. Three authorized variants intentionally send only part of the fixture; those are incomplete deliveries, not false blocks. The shared service adds three outage-related blocks.

Each condition contains three failed-client/full-receipt variants and three successful-client/partial-receipt variants. Those come from two injected cases exercised through three adapters. They demonstrate a distinction, not its population frequency. The partial-delivery fault truncates the bytes before transmission; it is not a claim to reproduce arbitrary TCP failure semantics.

The outcomes are recomputed from 167 receiver-journal entries by `verify_results.py` without importing the policy or outcome functions. It checks trial coverage, destination, length, digest, order, aggregate counts and expected per-tool/shared differences. These are assistant-authored checks, not independent human validation.

Separate challenges demonstrate raw-client bypass of both adapter controls, denial of a second request supplied with permission=false after an earlier permitted receipt, and one removed local copy alongside an intact replica. The permission check uses two static case definitions; it does not implement revocation of shared state. They are excluded from the main comparison. The copy example is a file-system illustration, not a remote-service recovery experiment.

## Limits that matter

- Restriction labels are supplied through a fixture-name lookup. No provenance chain or real rename/summary operation is implemented. Arbitrary transformations and dishonest purpose declarations are not solved.
- Adapter mediation is assumed in the main comparison; a raw client bypasses it. The experiment does not implement an OS sandbox.
- Permission values are supplied in two sequential fixed requests. Mutable grant state, stale approvals and concurrent changes are not tested.
- The cases establish functional behavior only. They do not measure model compliance, adaptation or adversarial search.
- Equivalent policies were intentionally given equivalent inputs. Their matching prevention is useful qualification, not statistical evidence for a novel architecture.
- The outage is injected into the shared service. Its observed cost is not a comparative deployment reliability estimate.
- Timing fields are diagnostic single-run observations and are not used to claim performance advantages.
- Archive visibility is incomplete; submitted-code fingerprints and source labels do not authenticate actors or prove permission violations.

## Reproduction and review

The local research checkout contains frozen acquisitions and source hashes. The shareable package contains derived metadata, source locators, experiment fixtures and scripts, and verifies derived-figure consistency without redistributing complete third-party reports. It reproduces the local transfer experiment independently. Reacquiring historical archive data is a separate source check; mutable metadata can change hashes.

Human technical adjudication and an unfamiliar-reader test remain pending. No outside researcher has been contacted for this package. AI assistance includes analysis, coding and editorial drafting; the user retains editorial responsibility. The public-facing articles should not be marked as reviewed or published until that review is recorded.

## Seven-carrier audit and worked evidence records

The editorial follow-up checks every decodable httpbin Base64 carrier in the existing 187-report selection, not additional live targets. Run `python3 scripts/audit_carriers.py` against the pinned `.cache/reports/` files. The script verifies acquisition hashes, decodes submitted content as inert bytes, selects the HTTP entry with the exact submitted address, and compares content SHA-256 values. Inline script fingerprints are compared separately, restricted to inline sensor entries attributed to that page. Descriptive classifications are based on close reading; this is not a general-purpose detector.

All seven selected payloads decode. Five match the reported carrier-response fingerprint: the 19:57 and 20:07 March 6 programs, the two March answer tables, and the September diagnostic page. Two differ: the 19:52 and 20:03 March 6 programs. Five submitted payloads contain scripts; three have a matching inline-script fingerprint. Two of the four ONCB programs have a recorded statistics request and one has a recorded output request with the specified field markers. `results/carrier-audit.json` retains sizes, hashes, source pins, field locators and the full seven-row denominator.

These are corroborating checks within archive metadata. No raw response body is available. A matching script sensor fingerprint does not establish that all instructions completed; a missing entry does not establish global nonexecution. The two mismatches do not identify why the responses differed. We do not infer the original agent's eventual result or its permission policy.

`data/evidence-records.json` supplies two worked reporting examples: the final March archive record and E08-ack-lost through the browser-like/per-tool condition. Each distinguishes proposed action, permission, observed dispatch, recipient evidence, recovery and unresolved questions, with source locators. This is a proposed reporting aid, not a validated standard. The delivery-unknown category in the article is a visibility limit, not a newly measured experimental condition. The experiment observes bytes read by controlled recipients, not durable storage or subsequent recipient behavior.

`python3 scripts/transfer_coverage.py` groups cases by the inputs the deterministic harness actually uses. The 47 named route variants contain 33 distinct operational configurations. Grouping preserves payload bytes, resolved label, destination, purpose, supplied grant, authorization truth, route and fault flags. It excludes IDs, development/evaluation labels and unused descriptive fields. This does not turn the remaining configurations into statistically independent trials. Both complete conditions use the same decision function; their parity is qualification, not an architecture-effectiveness discovery.
