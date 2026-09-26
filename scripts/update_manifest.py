"""Maintainer-only snapshot update after reviewing staged files."""
import hashlib
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def tracked_files():
    return [p for p in subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0') if p]

if __name__ == '__main__':
    files = tracked_files()
    if not files:
        raise SystemExit('Stage the intended public files first; no implicit recursive export.')
    excluded = {'release-manifest.json'}
    pins = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(files) if p not in excluded}
    (ROOT / 'release-manifest.json').write_text(json.dumps(pins, indent=2) + '\n')
    print(f'Manifest covers {len(pins)} files. Review and stage it before committing.')
