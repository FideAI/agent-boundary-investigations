"""Acquire pinned public JSON only; never execute or visit archived payloads."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.parse import urlsplit
import uuid
ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 16 * 1024 * 1024

class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=('carriers', 'all'), required=True)
    parser.add_argument('--cached-only', action='store_true', help='Check local pinned files without network requests')
    args = parser.parse_args()
    records = json.loads((ROOT / 'data/acquisition.json').read_text())
    carrier_ids = {r['report_id'] for r in json.loads((ROOT / 'results/carrier-audit.json').read_text())['records']}
    cache = ROOT / '.cache/reports'
    cache.mkdir(parents=True, exist_ok=True)
    opener = build_opener(NoRedirects())
    failures = []
    count = 0
    for record in records:
        rid = record['report_id']
        if args.scope == 'carriers' and rid not in carrier_ids:
            continue
        if str(uuid.UUID(rid)) != rid:
            raise SystemExit('Invalid report ID')
        expected_url = f'https://urlquery.net/report/{rid}/json'
        if record['url'] != expected_url or urlsplit(record['url']).hostname != 'urlquery.net':
            raise SystemExit(f'Unexpected acquisition URL for {rid}')
        target = cache / (rid + '.json')
        try:
            if target.exists():
                raw = target.read_bytes()
            elif args.cached_only:
                raise ValueError('missing pinned local source')
            else:
                request = Request(expected_url, headers={'User-Agent': 'Fide-Research-Reproduction/1.0', 'Accept': 'application/json'})
                try:
                    with opener.open(request, timeout=45) as response:
                        raw = response.read(MAX_BYTES + 1)
                finally:
                    time.sleep(1)
            if len(raw) > MAX_BYTES:
                raise ValueError('response exceeds download bound')
            actual = hashlib.sha256(raw).hexdigest()
            if actual != record['sha256']:
                if not args.cached_only:
                    quarantine = ROOT / '.cache/source-mismatches'
                    quarantine.mkdir(parents=True, exist_ok=True)
                    (quarantine / f'{rid}-{actual}.json').write_bytes(raw)
                raise ValueError(f'hash mismatch; expected {record["sha256"]}, got {actual}')
            if json.loads(raw)['report_id'] != rid:
                raise ValueError('report ID differs')
            if not target.exists():
                target.write_bytes(raw)
            count += 1
        except Exception as exc:
            failures.append(rid)
            print(f'FAIL {rid}: {exc}')
    print(f'{count} pinned sources verified; {len(failures)} unresolved. No pins changed.')
    raise SystemExit(1 if failures else 0)

if __name__ == '__main__':
    main()
