# Supporting methods: client status and recipient evidence

**Optional exploratory appendix · standalone article parked**

This appendix supports a concise explanation in the URLQuery investigation. It illustrates a known engineering distinction; it does not reproduce that incident or establish the effectiveness of an AI defense. Publication as a separate Insights article is on hold pending an independent substantive result.

OpenAI reported a photograph upload followed by a blocked reverse-image search. That account motivates a separate experiment: what does the sender's status establish, and what changes when an investigator can inspect the recipient?

## Findings to inspect

- A deliberately closed connection after complete receipt produces a failed client even though all intended bytes arrived.
- Deliberately sending half the intended fixture produces a successful request with incomplete task delivery. This does not show HTTP silently losing bytes it was asked to carry.
- Equivalent per-tool and shared-service controls prevent the same 25 prohibited route variants. Of 22 permitted variants, they complete 16 and 13 respectively; the additional loss is the injected shared-service outage. Both use the same decision function.
- A raw client bypasses both sets of adapters. These are not operating-system network boundaries.

The experiment contains 17 authored cases, 47 named route variants, 33 distinct operational configurations under the documented grouping, and 188 condition cells. These are dependent synthetic examples, not independent incidents or operational success rates. No model was evaluated. Claims T01–T09 are in the [claim register](../../CLAIMS.md).

## Reproduce without overwriting the released evidence

From the repository root, with Python 3.11+ and `curl` installed:

```sh
python3 scripts/verify_release.py
python3 scripts/reproduce_transfer.py
```

The rerun uses only temporary files, an ephemeral loopback port and harmless authored bytes. It qualifies receipt and denial behavior before the comparison, checks outcomes with a separate verifier, and compares condition counts, challenge results and operational grouping against the frozen run. Timing and timestamps are deliberately not compared. On Windows, run in WSL; native Windows execution has not been verified.

To retain and inspect a new run, use a separate disposable copy and run:

```sh
python3 scripts/transfer_experiment.py --qualify
python3 scripts/transfer_experiment.py
python3 scripts/transfer_coverage.py
python3 scripts/verify_public.py
```

These direct commands overwrite files under `results/`. The checked-in `verification.json` describes the original run; its `scripts/verify_results.py` producer additionally requires all pinned archive sources. It is not a certificate for a rerun. Use the fresh verifier output to assess the new run. No external recipient or API key is required.

## Inspect the observations

- [Authored cases](../../data/transfer-cases.json) and [experiment assumptions](../../EXPERIMENT.md).
- [Decisions and client statuses](../../results/transfer-decisions.csv), [recipient journal](../../results/transfer-receipts.csv) and [summary](../../results/transfer-summary.json).
- [Distinct-input grouping](../../results/transfer-coverage.json).
- [Bypass, fixed-permission and deletion-scope challenges](../../results/transfer-challenges.json), [events](../../results/challenge-events.csv) and [receipts](../../results/challenge-receipts.csv).
- [Worked evidence record](../../data/evidence-records.json): a permitted transfer with a failed client and complete recipient receipt.

Our journal establishes bytes read, not durable storage, later access or deletion of all copies. “Delivery unknown” describes a visibility limit when equivalent recipient evidence is missing; it is not a third experimental treatment. We have not tested which autonomous defensive response works best under that uncertainty.

## Attribution and publication status

The [OpenAI report](https://alignment.openai.com/misalignment-reports/uploading-files-to-the-internet-in-order-to-cite-them/) is the source for the historical example. Fide did not independently verify that transfer. The standalone visual article is parked. The runnable demonstration and methods remain supporting material in this public research companion. See [NOTICE.md](../../NOTICE.md).
