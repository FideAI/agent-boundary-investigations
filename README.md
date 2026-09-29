# URLQuery investigation and supporting methods

**Fide AI · Research companion · September 2026 · Public research companion**

This repository supports **URLQuery: When a web address becomes a program**, a reconstruction of archived activity and an audit of what the records establish. Start with the [URLQuery investigation guide](studies/urlquery/README.md): findings, claims, source checks and reproduction limits for 187 selected reports and seven decoded payloads.

The [local transfer experiment](studies/transfers/README.md) is an **optional exploratory methods appendix**. It illustrates why a sending tool's status does not establish whether a recipient read the bytes. Its code, fixtures, observations and limitations remain inspectable, but it is not a second Insights release or a demonstrated improvement in autonomous defense. The standalone transfer article is parked pending a substantive independent result.

The materials do not concern one shared historical event. Transluce discovered the URLQuery activity. OpenAI's separately published upload examples motivated the local transfer demonstration. That demonstration does not reproduce or validate the URLQuery incident. Fide claims no new attack discovery, independent actor attribution or evaluation of an AI model.

**Publication and review status:** the URLQuery article is still a draft. This public repository exposes the investigation and its supporting methods; it does not announce two research results. Analysis and coding have been checked by AI assistants; independent human technical and editorial review remain pending. Successful reproduction is not peer review.

## Inspect or reproduce

Python 3.11 or later; standard library only. The HTTP experiment additionally requires `curl`. No API key, paid inference or package installation is needed.

```sh
git clone https://github.com/FideAI/agent-boundary-investigations.git
cd agent-boundary-investigations
python3 scripts/verify_release.py
```

The verification command checks the file manifest, claim links and included derived results. To rerun the optional transfer appendix, use `python3 scripts/reproduce_transfer.py`. It copies the research files into a temporary directory, qualifies the local harness, reruns the experiment and compares functional results with the recorded run. It preserves the checked-in evidence. All experimental traffic goes to loopback (`127.0.0.1`); no historical target is contacted. The temporary rerun is removed after completion.

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

The files can be read directly on GitHub or cloned locally without requesting access. No hosted explorer is required. If an explorer is added, its README will include local setup instructions and screenshots; the research remains usable without it.

## Challenge the work

[Open an evidence challenge](https://github.com/FideAI/agent-boundary-investigations/issues/new?template=evidence-challenge.md) with a claim ID, source locator, proposed correction and its effect on the conclusion. See [CONTRIBUTING.md](CONTRIBUTING.md). Do not put credentials, personal data or private incident material in public issues.

For citations, use this repository's commit identifier with [CITATION.cff](CITATION.cff). Corrections will identify which findings changed and preserve prior versions through Git history.

## Release checks

Follow [PUBLIC-RELEASE.md](PUBLIC-RELEASE.md) for the privacy, Git-history and publication checks. File verification alone does not audit commit identities or GitHub metadata.

## Attribution and reuse

Original Fide code and original Fide writing are available under [MIT](LICENSE). Third-party material retains its own rights: [NOTICE.md](NOTICE.md) describes the boundary. Full third-party reports, upstream catalogs, raw historical response bodies and private research notes are excluded. Source hashes identify what was acquired; they do not guarantee that an archive will continue serving identical bytes.

This is a public, standalone research companion. Fide's internal program and shared evaluation infrastructure remain separate. The studies motivate further work on evidence and autonomous defense; they do not establish production effectiveness.
