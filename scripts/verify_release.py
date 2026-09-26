"""Verify snapshot integrity and inspectable claims, without network access."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from render_claims import render
ROOT = Path(__file__).resolve().parents[1]

def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O: research verifiers use assertions.')
    pins = json.loads((ROOT / 'release-manifest.json').read_text())
    for name, expected in pins.items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            raise SystemExit(f'Invalid manifest path: {name}')
        p = ROOT / path
        if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Release mismatch: {name}')
    claims = json.loads((ROOT / 'data/claims.json').read_text())
    assert len(claims) == len({c['id'] for c in claims}) == 16
    for claim in claims:
        assert all((ROOT / p).is_file() for p in claim.get('evidence', [])), claim['id']
        assert claim['basis'] and claim['limit'] and claim['review']
    assert (ROOT / 'CLAIMS.md').read_text() == render(), 'Regenerate readable claim register'
    acquisition = json.loads((ROOT / 'data/acquisition.json').read_text())
    selection = json.loads((ROOT / 'data/selection.json').read_text())
    assert len(acquisition) == len({r['report_id'] for r in acquisition}) == 187
    assert {r['report_id'] for r in acquisition} == {r['report_id'] for r in selection['records']}
    assert all(r['status'] == 'retrieved' and len(r['sha256']) == 64 for r in acquisition)
    subprocess.run([sys.executable, str(ROOT / 'scripts/verify_public.py')], check=True)
    print(f'PASS: {len(pins)} pinned files and 16 source-linked claims. Interpretation and original-source authentication are separate checks.')

if __name__ == '__main__':
    main()
