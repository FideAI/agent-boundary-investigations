# Public release checks

This public repository contains the URLQuery investigation with an optional transfer-methods appendix. The standalone transfer article remains parked. Making this repository public is a separate decision from publishing the website article.

## Privacy boundary

Publish original analytical code, synthetic fixtures, derived observations, claim reasoning and source locators. Keep raw third-party reports, decoded historical programs, credentials, local caches and internal coordination out of the repository and release attachments. Report identifiers, timestamps and domains in the derived tables are deliberate references to public archive records, not private Fide telemetry. Source locators can lead to third-party content we do not control. Hashes identify records; they are not a guarantee of anonymity.

Git history is part of a public release. Check every branch and tag, author and committer identities, commit messages, earlier file versions, release assets and Actions artifacts. A clean current tree does not remove information from an older commit. `.gitignore` prevents ordinary accidental additions; it does not remove already tracked files or protect a manually assembled ZIP.

## Current review — September 29, 2026

- Gitleaks found no credential matches in the working directory or either reachable commit. A separate text review covered all 59 historical file blobs, notebook metadata and outputs, private paths, internal repository references, email addresses and archived data fields.
- No private workspace paths, internal repository references, email addresses in file contents, raw response bodies or decoded historical programs were found in the tracked snapshot or historical blobs. The derived transaction table retains domains and hashes rather than original request paths and query values.
- The maintainer approved retaining the existing author and committer email metadata for public release on September 29, 2026. No history rewrite was requested or performed.
- At the pre-release review, the remote had one branch, no tags, no releases, no issues or pull requests, and no Actions artifacts. Pages and the wiki were disabled. Recheck these surfaces for subsequent releases.
- Release integrity and the isolated loopback transfer reproduction passed. These checks do not authenticate historical actors or replace independent human review.

This is a bounded review, not a guarantee that automated scanners detect every possible secret. Repeat it on the exact commit and attachments intended for publication.

## Final publication procedure

1. Confirm the intended commit identities and scan the history. Any rewrite needs a coordinated update of the remote; do not assume a new commit conceals prior metadata.
2. Review all intended files, including additions. Stage the intended release, regenerate `release-manifest.json`, then stage that manifest. Run `python3 scripts/verify_release.py` and `python3 scripts/reproduce_transfer.py`.
3. Scan both the working directory and complete history with Gitleaks: `gitleaks dir --redact .` and `gitleaks git --log-opts=--all --redact .`. Keep scanner reports outside this repository. Inspect metadata separately because credential scanning does not assess personal email disclosure.
4. Commit and push the reviewed changes. Verify the same checks from a fresh clone of the remote. Audit any downloadable bundle separately; release only explicitly reviewed files, never the whole working directory.
5. Complete the article's editorial review and decide repository visibility separately. At publication, replace the current-private/draft status statements with the actual release state, retain the human-review status accurately, and link the final article. Do not describe the optional transfer appendix as a separate validated defense result.

See [NOTICE.md](NOTICE.md) for attribution and redistribution boundaries and [REVIEW.md](REVIEW.md) for methodological limits.
