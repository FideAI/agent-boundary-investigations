# Challenge or improve this work

Start with the claim ID in `CLAIMS.md`. Identify the report/field or experiment row, explain why the present interpretation is incomplete or wrong, and propose a replacement. Distinguish a different inference from a factual extraction or calculation error. Negative results and successful reproductions are useful contributions.

Do not submit private logs, credentials or personal data to public issues. A new source download that differs from the frozen hash should be described without replacing the existing source pin. Preserve the difference for review.

Corrections should update the claim register, affected tables and study guides together. Record any changed aggregate counts in `CHANGELOG.md`. Public discussion does not automatically constitute accepted adjudication.

Maintainers regenerate `CLAIMS.md` with `python3 scripts/render_claims.py`, then regenerate the file manifest with `python3 scripts/update_manifest.py` after inspecting the intended changes. Run `python3 scripts/verify_release.py` and `python3 scripts/reproduce_transfer.py` before publishing an empirical revision. Update source claims only after checking the corresponding original record. Git history preserves earlier states; cite a commit when discussing a finding.
