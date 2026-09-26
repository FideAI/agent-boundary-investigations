# Agent boundaries: what the records can establish

**Fide AI · Working research companion · September 2026**

A tool's last message is not a complete account of what happened. This repository makes two related investigations inspectable: a reconstruction of archived web activity and a separate local experiment comparing request status with recipient evidence.

| Study | What we examined | Start here |
| --- | --- | --- |
| **URLQuery: When a web address becomes a program** | 187 selected archived reports; all seven decoded httpbin payloads compared with response and script metadata | [Study, findings and source checks](studies/urlquery/README.md) |
| **The browser said no. The upload had already happened.** | 17 synthetic cases, 47 route variants and 188 condition cells using local HTTP services | [Study, findings and reproduction](studies/transfers/README.md) |

These studies do not concern one shared historical event. Transluce discovered the URLQuery activity. OpenAI's separately published upload examples motivate our transfer demonstration. Fide claims no new attack discovery, independent actor attribution or evaluation of an AI model.

**Review status:** analysis and coding have been checked by AI assistants; independent human technical and editorial review remain pending. The companion articles remain unpublished drafts. Public availability and successful reproduction are not peer review.

## Inspect or reproduce

Python 3.11 or later; standard library only. The HTTP experiment additionally requires `curl`. No API key, paid inference or package installation is needed.

```sh
git clone https://github.com/FideAI/agent-boundary-investigations.git
cd agent-boundary-investigations
python3 scripts/verify_release.py
python3 scripts/reproduce_transfer.py
```

The first command verifies the release file manifest, claim links and included derived results. The second copies the research files into a temporary directory, qualifies the local harness, reruns the experiment and compares functional results with the released run. It preserves the checked-in evidence. All experimental traffic goes to loopback (`127.0.0.1`); no historical target is contacted. The temporary rerun is removed after completion.

These are different levels of verification:

1. **Release integrity:** are the files the declared snapshot?
2. **Computational reproduction:** do the included tables and executable experiment support the reported calculations?
3. **Source verification:** do the original third-party records support our observations? This requires separate source acquisition; see the [archive guide](studies/urlquery/README.md).
4. **Interpretation:** are our conclusions justified? That remains open to challenge even when all code checks pass.

## Follow a claim to its evidence

- [Readable claim register](CLAIMS.md): 16 claims, evidence links, reasoning basis and limits.
- [Machine-readable claims](data/claims.json) and [two worked evidence records](data/evidence-records.json).
- [Methods and results](METHODS.md), [experiment design and assumptions](EXPERIMENT.md), and [interpretive notes](RESEARCH-NOTES.md).
- [Executed evidence notebook](evidence-checks.ipynb): optional notebook view of derived-data checks; the command-line checks require no notebook software.
- [Review status and corrections](REVIEW.md).

The files can be read directly on GitHub or locally. No hosted explorer is required. If an explorer is added, its README will include local setup instructions and screenshots; the research remains usable without it.

## Challenge the work

[Open an evidence challenge](https://github.com/FideAI/agent-boundary-investigations/issues/new?template=evidence-challenge.md) with a claim ID, source locator, proposed correction and its effect on the conclusion. See [CONTRIBUTING.md](CONTRIBUTING.md). Do not put credentials, personal data or private incident material in public issues.

For citations, use this repository's commit identifier with [CITATION.cff](CITATION.cff). Corrections will identify which findings changed and preserve prior versions through Git history.

## Attribution and reuse

Original Fide code and original Fide writing are available under [MIT](LICENSE). Third-party material retains its own rights: [NOTICE.md](NOTICE.md) describes the boundary. Full third-party reports, upstream catalogs, raw historical response bodies and private research notes are excluded. Source hashes identify what was acquired; they do not guarantee that an archive will continue serving identical bytes.

This is a standalone public research companion. Fide's internal program and shared evaluation infrastructure remain separate. The studies motivate further work on evidence and autonomous defense; they do not establish production effectiveness.
