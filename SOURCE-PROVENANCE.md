# Snapshot provenance

The initial release candidate was prepared from an explicit allowlist of the September 26, 2026 research package. No private Git history was copied. The frozen analysis scripts, cases, source inventories and experimental results are retained unchanged; repository documentation and release/reproduction helpers were added separately. Later documentation and source-locator corrections are recorded in CHANGELOG.md.

`original-package-manifest.json` preserves the file hashes of that earlier portable package. Its README hash describes the original package README, which the repository README supersedes; it is historical provenance, not the current integrity check. `release-manifest.json` is the manifest for the current public snapshot.

During preparation of the initial candidate, the retained 187 hash-matching source reports reproduced `archive-summary.json`, `archive-observations.csv`, `archive-transactions.csv`, `hash-field-anomalies.json` and `carrier-audit.json` byte-for-byte in a temporary copy. Those original JSON reports are not redistributed. This check used retained sources; it does not claim a fresh network download still matches the frozen hashes.

The isolated transfer rerun reproduced the functional condition results, separate challenges and operational configuration grouping. Source-corruption and release-corruption checks correctly failed on deliberately altered copies. Independent human interpretation review remains pending.
