# URLQuery: When a web address becomes a program

**Archive reconstruction and evidence audit · working study**

Transluce identified this activity first. We checked how a known March 6 sequence is supported by the retained records, then compared all seven decodable httpbin payloads in our selected 187 reports. Selection is purposeful, not a population sample.

## Findings to inspect

- Five decoded payloads match their archived response fingerprints; two differ. Three of the five script-bearing payloads have matching script entries. [Complete seven-carrier audit](../../results/carrier-audit.json).
- Two March 6 reports record requests to the statistics endpoint; one records a later request carrying statistics fields to httpbin. That last report also lists zero bytes in final document metadata. [Transaction table](../../results/archive-transactions.csv).
- A submitted program is not proof that it was delivered or executed. An empty document field does not establish that no consequential request occurred.

The records do not establish the original agent's use of the output, exact source-to-output byte equality, the operator's permission policy or what a defender could have observed before intervention. We do not report a new incident or authenticate an actor. See claims A01–A07 in the [claim register](../../CLAIMS.md).

## Trace the evidence

1. [Selection](../../data/selection.json) and [acquisition inventory](../../data/acquisition.json): report IDs, source URLs, dates and frozen whole-file hashes.
2. [Observations](../../results/archive-observations.csv) and [HTTP entries](../../results/archive-transactions.csv): derived facts, including report IDs and entry indices.
3. [Carrier audit](../../results/carrier-audit.json): submitted-content hashes, archived response metadata, script comparisons and field locators.
4. [Methods](../../METHODS.md) and [interpretive notes](../../RESEARCH-NOTES.md): selection logic, alternative explanations and missing evidence.

## Check against original records

Raw third-party reports are not redistributed. To acquire only the seven carriers needed for the close audit:

```sh
python3 scripts/acquire_sources.py --scope carriers
```

For all 187 selected reports:

```sh
python3 scripts/acquire_sources.py --scope all
python3 scripts/analyze_archive.py
python3 scripts/audit_carriers.py
python3 scripts/verify_public.py
```

Run these commands from the repository root in a disposable clone: the analyzers overwrite derived results. Acquisition requests only public JSON report endpoints on `urlquery.net`; it never opens submitted URLs or executes their contents. Downloads are sequential, size-bounded and hash-checked. Matching files go to ignored `.cache/reports/`. A mismatching download is quarantined in ignored `.cache/source-mismatches/`, causes a failing exit and is not accepted as the pinned source. No pin is automatically rewritten.

The archive can change resource-level metadata between acquisitions. A mismatch prevents exact frozen-source reproduction; it does not alone show that event evidence changed or that our finding is false. Inspect changes separately and report any substantive difference. A partial seven-carrier download supports inspection of those sources, but the full analyzer and audit script require all 187 pinned inputs.

The selection originated in [Transluce's September 23 dataset](https://transluce.org/data/urlquery-agent-activity-2026-09-23.zip), with the archive hash recorded in `selection.json`. This package does not redistribute that catalog or independently regenerate selection from it. The [original investigation](https://transluce.org/agent-activity) owns the discovery and attribution analysis.

## Publication status

The visual article remains a draft. This guide is the main entry point for the public research companion. The [transfer appendix](../transfers/README.md) supplies an optional demonstration of client status versus receipt, not an additional incident finding. Original source rights and attribution are described in [NOTICE.md](../../NOTICE.md).
